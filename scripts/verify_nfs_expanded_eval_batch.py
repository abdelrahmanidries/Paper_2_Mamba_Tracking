#!/usr/bin/env python3
"""Verify expanded NFS evaluation batch configs without running evaluation."""

from __future__ import annotations

import ast
import json
import py_compile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
NFS_DATASET_PY = ROOT / "external" / "OSTrack" / "lib" / "test" / "evaluation" / "nfsdataset.py"
BATCH_CONFIG = ROOT / "configs" / "nfs_expanded32_eval_batch.json"
CONFIGS = [
    ROOT / "configs" / "nfs_eval_suite_expanded32_ostrack.json",
    ROOT / "configs" / "nfs_eval_suite_expanded32_hpc_rgssb_featcons_lam002.json",
]
EXPECTED_RUNS = [
    {"degradation": "clean", "severity": "none", "seed": 0},
    {"degradation": "motion_blur", "severity": "medium", "seed": 42},
    {"degradation": "low_resolution", "severity": "medium", "seed": 42},
    {"degradation": "gaussian_noise", "severity": "medium", "seed": 42},
]
EXPECTED_SEQUENCES = [
    "nfs_Gymnastics",
    "nfs_basketball_player",
    "nfs_car",
    "nfs_dog",
    "nfs_running",
    "nfs_bottle",
    "nfs_bird_2",
    "nfs_walking",
    "nfs_basketball_player_2",
    "nfs_car_drifting",
    "nfs_car_jumping",
    "nfs_cheetah",
    "nfs_horse_running",
    "nfs_motorcross",
    "nfs_person_scooter",
    "nfs_soccer_player_2",
    "nfs_basketball_1",
    "nfs_biker_acrobat",
    "nfs_biker_all_1",
    "nfs_biker_whole_body",
    "nfs_bowling_1",
    "nfs_car_camaro",
    "nfs_car_rc_rolling",
    "nfs_car_side",
    "nfs_dog_1",
    "nfs_drone",
    "nfs_footbal_skill",
    "nfs_helicopter",
    "nfs_parkour",
    "nfs_running_100_m",
    "nfs_soccer_ball_2",
    "nfs_tiger",
]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_sequence_info() -> dict[str, dict[str, Any]]:
    module = ast.parse(NFS_DATASET_PY.read_text(encoding="utf-8"))
    for node in ast.walk(module):
        if isinstance(node, ast.FunctionDef) and node.name == "_get_sequence_info_list":
            for child in ast.walk(node):
                if isinstance(child, ast.Assign):
                    for target in child.targets:
                        if isinstance(target, ast.Name) and target.id == "sequence_info_list":
                            infos = ast.literal_eval(child.value)
                            return {str(info["name"]): info for info in infos}
    raise RuntimeError(f"Could not parse sequence_info_list from {NFS_DATASET_PY}")


def count_nonempty_lines(path: Path) -> int:
    if not path.is_file():
        return 0
    return sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip())


def aligned_annotation_info(raw_lines: int, frame_count: int, init_omit: int) -> tuple[int, int]:
    available = max(0, raw_lines - init_omit)
    if frame_count <= 0:
        return 0, 0
    if available == frame_count:
        return available, 1
    if available > frame_count:
        stride = max(1, round(available / frame_count))
        sampled = (available + stride - 1) // stride
        if sampled >= frame_count:
            return frame_count, stride
    return available, 1


def verify_no_duplicate_pairs(config: dict[str, Any], config_path: Path) -> None:
    seen: set[tuple[str, str, str, str]] = set()
    for sequence in config["sequences"]:
        for run in config["runs"]:
            key = (str(sequence), str(run["degradation"]), str(run["severity"]), str(run["seed"]))
            if key in seen:
                raise AssertionError(f"Duplicate sequence-condition pair in {config_path}: {key}")
            seen.add(key)


def verify_sequence_files(root: Path, sequences: list[str], infos: dict[str, dict[str, Any]]) -> None:
    if not root.is_dir():
        print(f"NFS root not found; skipping filesystem checks: {root}")
        return
    if not (root / "sequences").is_dir() or not (root / "anno").is_dir():
        print(f"NFS root lacks extracted sequences/ and anno/ layout; skipping frame checks: {root}")
        return
    for sequence in sequences:
        info = infos[sequence]
        start = int(info["startFrame"]) + int(info.get("initOmit", 0))
        end = int(info["endFrame"])
        nz = int(info["nz"])
        ext = str(info["ext"])
        frames = end - start + 1
        seq_dir = root / info["path"]
        anno_path = root / info["anno_path"]
        first = seq_dir / f"{start:0{nz}}.{ext}"
        last = seq_dir / f"{end:0{nz}}.{ext}"
        raw_gt = count_nonempty_lines(anno_path)
        aligned_gt, stride = aligned_annotation_info(raw_gt, frames, int(info.get("initOmit", 0)))
        if not (seq_dir.is_dir() and anno_path.is_file() and first.is_file() and last.is_file() and frames == aligned_gt):
            raise AssertionError(f"Invalid NFS sequence {sequence}: frames={frames} raw_gt={raw_gt} aligned_gt={aligned_gt}")
        print(f"  {sequence}: frames={frames} raw_gt={raw_gt} aligned_gt={aligned_gt} stride={stride}")
    print(f"NFS filesystem checks passed for {len(sequences)} sequences at {root}")


def main() -> int:
    py_compile.compile(str(ROOT / "scripts" / "run_nfs_expanded_eval_batch.py"), doraise=True)
    py_compile.compile(str(ROOT / "scripts" / "verify_nfs_expanded_eval_batch.py"), doraise=True)

    if not BATCH_CONFIG.is_file():
        raise FileNotFoundError(BATCH_CONFIG)
    for config_path in CONFIGS:
        if not config_path.is_file():
            raise FileNotFoundError(config_path)

    batch = load_json(BATCH_CONFIG)
    referenced = [ROOT / suite["suite_config"] for suite in batch["suites"]]
    if referenced != CONFIGS:
        raise AssertionError("Batch config suite order must be baseline then HPC RG-SSB.")

    infos = load_sequence_info()
    for sequence in EXPECTED_SEQUENCES:
        if sequence not in infos:
            raise AssertionError(f"Selected sequence missing from OSTrack NFS metadata: {sequence}")

    total_pairs = 0
    for config_path in CONFIGS:
        config = load_json(config_path)
        if config["sequences"] != EXPECTED_SEQUENCES:
            raise AssertionError(f"Unexpected sequence list in {config_path}")
        if config["runs"] != EXPECTED_RUNS:
            raise AssertionError(f"Unexpected runs in {config_path}")
        verify_no_duplicate_pairs(config, config_path)
        total_pairs += len(config["sequences"]) * len(config["runs"])

    first_config = load_json(CONFIGS[0])
    verify_sequence_files(Path(first_config["clean_nfs_root"]), EXPECTED_SEQUENCES, infos)
    local_root = Path(first_config.get("local_clean_nfs_root", ""))
    if local_root != Path(first_config["clean_nfs_root"]):
        verify_sequence_files(local_root, EXPECTED_SEQUENCES, infos)

    nfs_eval_script = (ROOT / "scripts" / "run_ostrack_nfs_eval.py").read_text(encoding="utf-8")
    if "aligned_annotation_indices" not in nfs_eval_script or "load_aligned_gt" not in nfs_eval_script:
        raise AssertionError("NFS evaluation script does not expose aligned annotation logic.")

    print(f"selected_sequence_count: {len(EXPECTED_SEQUENCES)}")
    print(f"condition_count: {len(EXPECTED_RUNS)}")
    print(f"sequence_condition_pairs_per_config: {len(EXPECTED_SEQUENCES) * len(EXPECTED_RUNS)}")
    print(f"total_sequence_condition_pairs_across_batch: {total_pairs}")
    print(f"selected_sequences: {', '.join(EXPECTED_SEQUENCES)}")
    print("verification: expanded NFS evaluation batch passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
