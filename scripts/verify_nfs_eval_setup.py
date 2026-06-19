#!/usr/bin/env python3
"""Verify NFS evaluation setup without running OSTrack."""

from __future__ import annotations

import ast
import json
import py_compile
from pathlib import Path

import yaml
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.evaluation.nfs_annotations import load_canonical_nfs_ground_truth

NFS_DATASET_PY = ROOT / "external" / "OSTrack" / "lib" / "test" / "evaluation" / "nfsdataset.py"
SCRIPTS = [
    ROOT / "scripts" / "inspect_nfs_sequences.py",
    ROOT / "scripts" / "create_degraded_nfs_sequence.py",
    ROOT / "scripts" / "run_ostrack_nfs_eval.py",
    ROOT / "scripts" / "run_nfs_degradation_suite.py",
    ROOT / "scripts" / "verify_nfs_eval_setup.py",
]
CONFIGS = [
    ROOT / "configs" / "nfs_eval_suite_ostrack.json",
    ROOT / "configs" / "nfs_eval_suite_hpc_rgssb_featcons_lam002.json",
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
]
EXPECTED_RUNS = [
    {"degradation": "clean", "severity": "none", "seed": 0},
    {"degradation": "motion_blur", "severity": "medium", "seed": 42},
    {"degradation": "low_resolution", "severity": "medium", "seed": 42},
    {"degradation": "gaussian_noise", "severity": "medium", "seed": 42},
]


def load_sequence_info() -> list[dict]:
    module = ast.parse(NFS_DATASET_PY.read_text(encoding="utf-8"))
    for node in ast.walk(module):
        if isinstance(node, ast.FunctionDef) and node.name == "_get_sequence_info_list":
            for child in ast.walk(node):
                if isinstance(child, ast.Assign):
                    for target in child.targets:
                        if isinstance(target, ast.Name) and target.id == "sequence_info_list":
                            return ast.literal_eval(child.value)
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


def assert_equal(name: str, actual, expected) -> None:
    if actual != expected:
        raise AssertionError(f"{name} mismatch: {actual!r} != {expected!r}")


def condition_key(run: dict) -> tuple[str, str, str]:
    return (str(run["degradation"]), str(run["severity"]), str(run["seed"]))


def verify_no_duplicates(sequences: list[str], runs: list[dict]) -> None:
    seen: set[tuple[str, str, str, str]] = set()
    for sequence in sequences:
        for run in runs:
            key = (sequence, *condition_key(run))
            if key in seen:
                raise AssertionError(f"Duplicate sequence-condition pair: {key}")
            seen.add(key)


def verify_sequence_files(nfs_root: Path, sequence_names: list[str]) -> list[dict[str, object]]:
    infos = {info["name"]: info for info in load_sequence_info()}
    rows = []
    if not nfs_root.is_dir():
        print(f"Local NFS root not found; skipping file checks: {nfs_root}")
        return rows
    if not (nfs_root / "sequences").is_dir() or not (nfs_root / "anno").is_dir():
        zip_count = len(list(nfs_root.glob("*.zip")))
        print(
            "Local NFS root found, but OSTrack extracted layout is missing "
            f"(expected sequences/ and anno/). Zip files present: {zip_count}. "
            "Skipping frame/annotation checks."
        )
        return rows

    for sequence in sequence_names:
        info = infos[sequence]
        start = int(info["startFrame"]) + int(info.get("initOmit", 0))
        end = int(info["endFrame"])
        nz = int(info["nz"])
        ext = str(info["ext"])
        frames = end - start + 1
        seq_dir = nfs_root / info["path"]
        anno_path = nfs_root / info["anno_path"]
        first = seq_dir / f"{start:0{nz}}.{ext}"
        last = seq_dir / f"{end:0{nz}}.{ext}"
        bundle = load_canonical_nfs_ground_truth(nfs_root, sequence)
        raw_gt_lines = bundle.raw_annotation_count
        aligned_gt_lines = bundle.aligned_annotation_count
        gt_stride = bundle.sampling_stride
        valid = (
            seq_dir.is_dir()
            and anno_path.is_file()
            and first.is_file()
            and last.is_file()
            and frames == aligned_gt_lines
        )
        if not valid:
            raise AssertionError(
                f"Invalid NFS sequence {sequence}: seq_dir={seq_dir.is_dir()} "
                f"anno={anno_path.is_file()} first={first.is_file()} last={last.is_file()} "
                f"frames={frames} raw_gt={raw_gt_lines} aligned_gt={aligned_gt_lines}"
            )
        rows.append(
            {
                "sequence": sequence,
                "frames": frames,
                "raw_gt_lines": raw_gt_lines,
                "aligned_gt_lines": aligned_gt_lines,
                "gt_stride": gt_stride,
                "coordinate_format": bundle.coordinate_format,
                "path": str(info["path"]),
            }
        )
    return rows


def checkpoint_path(ostrack_root: Path, tracker: str, config_name: str) -> Path:
    config_path = ostrack_root / "experiments" / tracker / f"{config_name}.yaml"
    if not config_path.is_file():
        raise FileNotFoundError(f"OSTrack config not found: {config_path}")
    data = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
    epoch = int(data["TEST"]["EPOCH"])
    return ostrack_root / "output" / "checkpoints" / "train" / tracker / config_name / f"OSTrack_ep{epoch:04d}.pth.tar"


def main() -> int:
    for script in SCRIPTS:
        py_compile.compile(str(script), doraise=True)

    infos = {info["name"]: info for info in load_sequence_info()}
    for sequence in EXPECTED_SEQUENCES:
        if sequence not in infos:
            raise AssertionError(f"Selected sequence missing from OSTrack NFS metadata: {sequence}")

    for config_path in CONFIGS:
        config = json.loads(config_path.read_text(encoding="utf-8"))
        assert_equal(f"{config_path.name} sequences", config["sequences"], EXPECTED_SEQUENCES)
        assert_equal(f"{config_path.name} runs", config["runs"], EXPECTED_RUNS)
        verify_no_duplicates(config["sequences"], config["runs"])
        ckpt = checkpoint_path(ROOT / config["ostrack_root"], config["tracker"], config["config"])
        print(f"{config_path.name}: expected checkpoint: {ckpt}")
        print(f"{config_path.name}: checkpoint exists: {ckpt.is_file()}")

    local_root = Path(json.loads(CONFIGS[0].read_text(encoding="utf-8"))["clean_nfs_root"])
    sequence_rows = verify_sequence_files(local_root, EXPECTED_SEQUENCES)

    print("dataset_name: nfs")
    print(f"selected_sequences: {', '.join(EXPECTED_SEQUENCES)}")
    print(f"condition_count: {len(EXPECTED_RUNS)}")
    print(f"sequence_condition_pairs_per_config: {len(EXPECTED_SEQUENCES) * len(EXPECTED_RUNS)}")
    if sequence_rows:
        print("local_nfs_sequence_checks:")
        for row in sequence_rows:
            print(
                f"  {row['sequence']}: frames={row['frames']} raw_gt={row['raw_gt_lines']} "
                f"aligned_gt={row['aligned_gt_lines']} stride={row['gt_stride']} "
                f"format={row['coordinate_format']} path={row['path']}"
            )
    print("verification: NFS evaluation setup passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
