#!/usr/bin/env python3
"""Verify UAV123 evaluation setup without running OSTrack."""

from __future__ import annotations

import ast
import json
import py_compile
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
UAV_DATASET_PY = ROOT / "external" / "OSTrack" / "lib" / "test" / "evaluation" / "uavdataset.py"
SCRIPTS = [
    ROOT / "scripts" / "inspect_uav123_sequences.py",
    ROOT / "scripts" / "create_degraded_uav123_sequence.py",
    ROOT / "scripts" / "run_ostrack_uav123_eval.py",
    ROOT / "scripts" / "run_uav123_degradation_suite.py",
    ROOT / "scripts" / "verify_uav123_eval_setup.py",
]
CONFIGS = [
    ROOT / "configs" / "uav123_eval_suite_ostrack.json",
    ROOT / "configs" / "uav123_eval_suite_hpc_rgssb_featcons_lam002.json",
]
EXPECTED_SEQUENCES = [
    "uav_car10",
    "uav_person1",
    "uav_truck1",
    "uav_bike1",
    "uav_boat1",
    "uav_building1",
    "uav_person3",
    "uav_car11",
]
EXPECTED_RUNS = [
    {"degradation": "clean", "severity": "none", "seed": 0},
    {"degradation": "motion_blur", "severity": "medium", "seed": 42},
    {"degradation": "low_resolution", "severity": "medium", "seed": 42},
    {"degradation": "gaussian_noise", "severity": "medium", "seed": 42},
]


def load_sequence_info() -> list[dict]:
    module = ast.parse(UAV_DATASET_PY.read_text(encoding="utf-8"))
    for node in ast.walk(module):
        if isinstance(node, ast.FunctionDef) and node.name == "_get_sequence_info_list":
            for child in ast.walk(node):
                if isinstance(child, ast.Assign):
                    for target in child.targets:
                        if isinstance(target, ast.Name) and target.id == "sequence_info_list":
                            return ast.literal_eval(child.value)
    raise RuntimeError(f"Could not parse sequence_info_list from {UAV_DATASET_PY}")


def count_nonempty_lines(path: Path) -> int:
    if not path.is_file():
        return 0
    return sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip())


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


def verify_sequence_files(uav_root: Path, sequence_names: list[str]) -> list[dict[str, object]]:
    infos = {info["name"]: info for info in load_sequence_info()}
    rows = []
    if not uav_root.is_dir():
        print(f"Local UAV123 root not found; skipping file checks: {uav_root}")
        return rows

    for sequence in sequence_names:
        info = infos[sequence]
        start = int(info["startFrame"]) + int(info.get("initOmit", 0))
        end = int(info["endFrame"])
        nz = int(info["nz"])
        ext = str(info["ext"])
        frames = end - start + 1
        seq_dir = uav_root / info["path"]
        anno_path = uav_root / info["anno_path"]
        first = seq_dir / f"{start:0{nz}}.{ext}"
        last = seq_dir / f"{end:0{nz}}.{ext}"
        gt_lines = count_nonempty_lines(anno_path) - int(info.get("initOmit", 0))
        valid = seq_dir.is_dir() and anno_path.is_file() and first.is_file() and last.is_file() and frames == gt_lines
        if not valid:
            raise AssertionError(
                f"Invalid UAV123 sequence {sequence}: seq_dir={seq_dir.is_dir()} "
                f"anno={anno_path.is_file()} first={first.is_file()} last={last.is_file()} "
                f"frames={frames} gt={gt_lines}"
            )
        rows.append({"sequence": sequence, "frames": frames, "gt_lines": gt_lines, "path": str(info["path"])})
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
            raise AssertionError(f"Selected sequence missing from OSTrack UAV123 metadata: {sequence}")

    for config_path in CONFIGS:
        config = json.loads(config_path.read_text(encoding="utf-8"))
        assert_equal(f"{config_path.name} sequences", config["sequences"], EXPECTED_SEQUENCES)
        assert_equal(f"{config_path.name} runs", config["runs"], EXPECTED_RUNS)
        verify_no_duplicates(config["sequences"], config["runs"])
        ckpt = checkpoint_path(ROOT / config["ostrack_root"], config["tracker"], config["config"])
        print(f"{config_path.name}: expected checkpoint: {ckpt}")
        print(f"{config_path.name}: checkpoint exists: {ckpt.is_file()}")

    local_root = Path(json.loads(CONFIGS[0].read_text(encoding="utf-8"))["clean_uav_root"])
    sequence_rows = verify_sequence_files(local_root, EXPECTED_SEQUENCES)

    print(f"dataset_name: uav")
    print(f"selected_sequences: {', '.join(EXPECTED_SEQUENCES)}")
    print(f"condition_count: {len(EXPECTED_RUNS)}")
    print(f"sequence_condition_pairs_per_config: {len(EXPECTED_SEQUENCES) * len(EXPECTED_RUNS)}")
    if sequence_rows:
        print("local_uav123_sequence_checks:")
        for row in sequence_rows:
            print(f"  {row['sequence']}: frames={row['frames']} gt_lines={row['gt_lines']} path={row['path']}")
    print("verification: UAV123 evaluation setup passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
