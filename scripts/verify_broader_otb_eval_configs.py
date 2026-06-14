#!/usr/bin/env python3
"""Verify broader OTB evaluation configs without running evaluation."""

from __future__ import annotations

import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BASELINE_CONFIG = PROJECT_ROOT / "configs" / "baseline_degradation_suite_otb_broader_ostrack.json"
RGSSB_CONFIG = PROJECT_ROOT / "configs" / "rgssb_experiment_cycle_hpc_featcons_lam002_otb_broader.json"
EXPECTED_SEQUENCES = [
    "Car1",
    "David2",
    "Coke",
    "Walking",
    "Walking2",
    "FaceOcc1",
    "Dog1",
    "Deer",
    "Football",
    "BlurBody",
    "BlurCar2",
    "BlurFace",
    "Box",
]
EXPECTED_CONDITIONS = [
    {"degradation": "clean", "severity": "none", "seed": 0},
    {"degradation": "motion_blur", "severity": "medium", "seed": 42},
    {"degradation": "low_resolution", "severity": "medium", "seed": 42},
    {"degradation": "gaussian_noise", "severity": "medium", "seed": 42},
]
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"}


def load_json(path: Path) -> dict:
    if not path.is_file():
        raise FileNotFoundError(path)
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def assert_equal(name: str, actual, expected) -> None:
    if actual != expected:
        raise AssertionError(f"{name} mismatch: {actual!r} != {expected!r}")


def condition_key(condition: dict) -> tuple[str, str, str]:
    return (
        str(condition["degradation"]),
        str(condition["severity"]),
        str(condition["seed"]),
    )


def verify_no_duplicates(sequences: list[str], conditions: list[dict]) -> None:
    seen: set[tuple[str, str, str, str]] = set()
    for sequence in sequences:
        for condition in conditions:
            key = (sequence, *condition_key(condition))
            if key in seen:
                raise AssertionError(f"Duplicate sequence-condition pair: {key}")
            seen.add(key)


def count_frames(img_dir: Path) -> int:
    if not img_dir.is_dir():
        return 0
    return sum(
        1
        for path in img_dir.iterdir()
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
    )


def count_gt_lines(gt_path: Path) -> int:
    if not gt_path.is_file():
        return 0
    return sum(1 for line in gt_path.read_text(encoding="utf-8").splitlines() if line.strip())


def verify_otb_root(otb_root: Path, sequences: list[str]) -> list[dict[str, object]]:
    rows = []
    if not otb_root.is_dir():
        print(f"Local OTB root not found; skipping sequence file checks: {otb_root}")
        return rows

    for sequence in sequences:
        sequence_dir = otb_root / sequence
        img_dir = sequence_dir / "img"
        gt_path = sequence_dir / "groundtruth_rect.txt"
        frames = count_frames(img_dir)
        gt_lines = count_gt_lines(gt_path)
        valid = sequence_dir.is_dir() and img_dir.is_dir() and gt_path.is_file() and frames > 0 and frames == gt_lines
        if not valid:
            raise AssertionError(
                f"Invalid OTB sequence {sequence}: "
                f"seq_dir={sequence_dir.is_dir()} img_dir={img_dir.is_dir()} "
                f"gt={gt_path.is_file()} frames={frames} gt_lines={gt_lines}"
            )
        rows.append({"sequence": sequence, "frames": frames, "gt_lines": gt_lines})
    return rows


def main() -> None:
    baseline = load_json(BASELINE_CONFIG)
    rgssb = load_json(RGSSB_CONFIG)

    assert_equal("baseline sequences", baseline["sequences"], EXPECTED_SEQUENCES)
    assert_equal("rgssb sequences", rgssb["sequences"], EXPECTED_SEQUENCES)
    assert_equal("baseline runs", baseline["runs"], EXPECTED_CONDITIONS)
    assert_equal("rgssb conditions", rgssb["conditions"], EXPECTED_CONDITIONS)
    assert_equal("baseline tracker", baseline["tracker"], "ostrack")
    assert_equal("baseline config", baseline["config"], "vitb_256_mae_ce_32x4_ep300")
    assert_equal(
        "rgssb config_name",
        rgssb["config_name"],
        "vitb_256_mae_ce_32x4_ep300_rgssb_head_train_lasot_degraded_hpc_featcons_lam002",
    )
    assert_equal("rgssb train", rgssb["train"], False)
    assert_equal("rgssb eval", rgssb["eval"], True)
    assert_equal("rgssb overwrite_existing", rgssb["overwrite_existing"], True)

    verify_no_duplicates(baseline["sequences"], baseline["runs"])
    verify_no_duplicates(rgssb["sequences"], rgssb["conditions"])

    baseline_rows = verify_otb_root(Path(baseline["clean_otb_root"]), baseline["sequences"])
    rgssb_rows = verify_otb_root(Path(rgssb["clean_otb_root"]), rgssb["sequences"])

    print(f"baseline_config: {BASELINE_CONFIG}")
    print(f"rgssb_config: {RGSSB_CONFIG}")
    print(f"selected_sequences: {', '.join(EXPECTED_SEQUENCES)}")
    print(f"condition_count: {len(EXPECTED_CONDITIONS)}")
    print(f"sequence_condition_pairs_per_config: {len(EXPECTED_SEQUENCES) * len(EXPECTED_CONDITIONS)}")
    if baseline_rows and rgssb_rows:
        print("local_otb_sequence_checks:")
        for row in baseline_rows:
            print(f"  {row['sequence']}: frames={row['frames']} gt_lines={row['gt_lines']}")
    print("verification: broader OTB evaluation configs passed")


if __name__ == "__main__":
    main()
