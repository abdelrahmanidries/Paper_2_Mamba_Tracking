#!/usr/bin/env python3
"""Verify the failure-focused UAV123 + NFS evaluation batch without running evaluation."""

from __future__ import annotations

import ast
import json
import py_compile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
UAV_DATASET_PY = ROOT / "external" / "OSTrack" / "lib" / "test" / "evaluation" / "uavdataset.py"
NFS_DATASET_PY = ROOT / "external" / "OSTrack" / "lib" / "test" / "evaluation" / "nfsdataset.py"
BATCH_CONFIG = ROOT / "configs" / "failure_focused_eval_batch.json"
SUITE_CONFIGS = [
    ROOT / "configs" / "uav123_eval_suite_failure_expanded_ostrack.json",
    ROOT / "configs" / "uav123_eval_suite_failure_expanded_hpc_rgssb_featcons_lam002.json",
    ROOT / "configs" / "nfs_eval_suite_failure_expanded_ostrack.json",
    ROOT / "configs" / "nfs_eval_suite_failure_expanded_hpc_rgssb_featcons_lam002.json",
]
SCRIPTS = [
    ROOT / "scripts" / "run_failure_focused_eval_batch.py",
    ROOT / "scripts" / "verify_failure_focused_eval_batch.py",
]
EXPECTED_RUNS = [
    {"degradation": "clean", "severity": "none", "seed": 0},
    {"degradation": "motion_blur", "severity": "medium", "seed": 42},
    {"degradation": "low_resolution", "severity": "medium", "seed": 42},
    {"degradation": "gaussian_noise", "severity": "medium", "seed": 42},
]
EXPECTED_UAV_SEQUENCES = [
    "uav_car10",
    "uav_person1",
    "uav_truck1",
    "uav_bike1",
    "uav_boat1",
    "uav_building1",
    "uav_person3",
    "uav_car11",
    "uav_car12",
    "uav_car13",
    "uav_person10",
    "uav_person12_1",
    "uav_person14_1",
    "uav_truck2",
    "uav_bike2",
    "uav_wakeboard1",
]
EXPECTED_NFS_SEQUENCES = [
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
]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_sequence_info(path: Path) -> dict[str, dict[str, Any]]:
    module = ast.parse(path.read_text(encoding="utf-8"))
    for node in ast.walk(module):
        if isinstance(node, ast.FunctionDef) and node.name == "_get_sequence_info_list":
            for child in ast.walk(node):
                if isinstance(child, ast.Assign):
                    for target in child.targets:
                        if isinstance(target, ast.Name) and target.id == "sequence_info_list":
                            infos = ast.literal_eval(child.value)
                            return {str(info["name"]): info for info in infos}
    raise RuntimeError(f"Could not parse sequence_info_list from {path}")


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


def verify_uav_files(root: Path, sequences: list[str], infos: dict[str, dict[str, Any]]) -> None:
    if not root.is_dir():
        print(f"UAV123 root not found; skipping filesystem checks: {root}")
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
        gt_lines = count_nonempty_lines(anno_path) - int(info.get("initOmit", 0))
        if not (seq_dir.is_dir() and anno_path.is_file() and first.is_file() and last.is_file() and frames == gt_lines):
            raise AssertionError(f"Invalid UAV123 sequence {sequence}: frames={frames} gt={gt_lines}")
    print(f"UAV123 filesystem checks passed for {len(sequences)} sequences at {root}")


def verify_nfs_files(root: Path, sequences: list[str], infos: dict[str, dict[str, Any]]) -> None:
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
    for script in SCRIPTS:
        py_compile.compile(str(script), doraise=True)

    for config_path in SUITE_CONFIGS:
        if not config_path.is_file():
            raise FileNotFoundError(config_path)
    if not BATCH_CONFIG.is_file():
        raise FileNotFoundError(BATCH_CONFIG)

    batch = load_json(BATCH_CONFIG)
    referenced = [ROOT / suite["suite_config"] for suite in batch["suites"]]
    if referenced != SUITE_CONFIGS:
        raise AssertionError("Batch config suite order does not match expected failure-focused order")

    uav_infos = load_sequence_info(UAV_DATASET_PY)
    nfs_infos = load_sequence_info(NFS_DATASET_PY)
    for sequence in EXPECTED_UAV_SEQUENCES:
        if sequence not in uav_infos:
            raise AssertionError(f"UAV123 sequence missing from OSTrack metadata: {sequence}")
    for sequence in EXPECTED_NFS_SEQUENCES:
        if sequence not in nfs_infos:
            raise AssertionError(f"NFS sequence missing from OSTrack metadata: {sequence}")

    total_pairs = 0
    dataset_pairs = {"uav123": 0, "nfs": 0}
    for config_path in SUITE_CONFIGS:
        config = load_json(config_path)
        expected_sequences = EXPECTED_UAV_SEQUENCES if "uav123" in config_path.name else EXPECTED_NFS_SEQUENCES
        if config["sequences"] != expected_sequences:
            raise AssertionError(f"Unexpected sequence list in {config_path}")
        if config["runs"] != EXPECTED_RUNS:
            raise AssertionError(f"Unexpected condition list in {config_path}")
        verify_no_duplicate_pairs(config, config_path)
        pairs = len(config["sequences"]) * len(config["runs"])
        total_pairs += pairs
        dataset_pairs["uav123" if "uav123" in config_path.name else "nfs"] += pairs

    uav_config = load_json(SUITE_CONFIGS[0])
    nfs_config = load_json(SUITE_CONFIGS[2])
    verify_uav_files(Path(uav_config["clean_uav_root"]), EXPECTED_UAV_SEQUENCES, uav_infos)
    local_uav = Path(uav_config.get("local_clean_uav_root", ""))
    if local_uav != Path(uav_config["clean_uav_root"]):
        verify_uav_files(local_uav, EXPECTED_UAV_SEQUENCES, uav_infos)

    verify_nfs_files(Path(nfs_config["clean_nfs_root"]), EXPECTED_NFS_SEQUENCES, nfs_infos)
    local_nfs = Path(nfs_config.get("local_clean_nfs_root", ""))
    if local_nfs != Path(nfs_config["clean_nfs_root"]):
        verify_nfs_files(local_nfs, EXPECTED_NFS_SEQUENCES, nfs_infos)

    nfs_script = (ROOT / "scripts" / "run_ostrack_nfs_eval.py").read_text(encoding="utf-8")
    if "aligned_annotation_indices" not in nfs_script or "load_aligned_gt" not in nfs_script:
        raise AssertionError("NFS evaluation script does not expose aligned annotation logic")
    print("NFS aligned annotation logic: verified by script markers")
    print(f"uav123_sequences: {', '.join(EXPECTED_UAV_SEQUENCES)}")
    print(f"nfs_sequences: {', '.join(EXPECTED_NFS_SEQUENCES)}")
    print(f"uav123_sequence_condition_pairs_across_two_configs: {dataset_pairs['uav123']}")
    print(f"nfs_sequence_condition_pairs_across_two_configs: {dataset_pairs['nfs']}")
    print(f"total_sequence_condition_pairs_across_batch: {total_pairs}")
    print("verification: failure-focused evaluation batch passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
