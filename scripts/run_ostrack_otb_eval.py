"""Run one OSTrack OTB sequence evaluation and append baseline metrics."""

from __future__ import annotations

import argparse
import csv
import os
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.evaluate_tracking_result import compute_metrics, load_boxes


CSV_COLUMNS = [
    "tracker",
    "config",
    "sequence",
    "degradation",
    "severity",
    "seed",
    "frames",
    "mean_iou",
    "success_auc",
    "precision_20",
    "mean_center_error",
    "result_path",
    "time_path",
    "eval_otb_root",
    "notes",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run OSTrack on one OTB sequence and append metrics."
    )
    parser.add_argument("--ostrack_root", default="external/OSTrack", type=Path)
    parser.add_argument("--clean_otb_root", required=True, type=Path)
    parser.add_argument("--eval_otb_root", required=True, type=Path)
    parser.add_argument("--sequence", required=True)
    parser.add_argument("--config", default="vitb_256_mae_ce_32x4_ep300")
    parser.add_argument("--tracker", default="ostrack")
    parser.add_argument("--degradation", default="clean")
    parser.add_argument("--severity", default="none")
    parser.add_argument("--seed", default=0, type=int)
    parser.add_argument("--output_dir", default="outputs/ostrack_runs", type=Path)
    parser.add_argument("--results_csv", default="experiments/baseline_results.csv", type=Path)
    parser.set_defaults(skip_existing=True, skip_existing_requested=False)
    parser.add_argument(
        "--skip_existing",
        dest="skip_existing",
        action="store_true",
        help="Skip if this tracker/config/sequence/degradation/severity/seed row already exists. Default: true.",
    )
    parser.add_argument(
        "--no_skip_existing",
        dest="skip_existing",
        action="store_false",
        help="Do not skip existing rows unless --overwrite_existing is used.",
    )
    parser.add_argument(
        "--skip_existing_requested",
        action="store_true",
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--overwrite_existing",
        action="store_true",
        help="Run evaluation and replace the matching CSV row instead of appending a duplicate.",
    )
    parser.add_argument(
        "--conda_env",
        default="ostrack",
        help="Conda env used for OSTrack. Use an empty string to call python directly.",
    )
    parser.add_argument("--num_gpus", default=1, type=int)
    parser.add_argument("--threads", default=0, type=int)
    parser.add_argument(
        "--check_only",
        action="store_true",
        help="Validate inputs, print resolved checkpoint/output paths, and exit without running OSTrack.",
    )
    return parser.parse_args()


def resolve_existing(path: Path) -> Path:
    if not path.exists():
        raise FileNotFoundError(path)
    return path.resolve()


def read_test_epoch(ostrack_root: Path, tracker: str, config: str) -> int:
    config_path = ostrack_root / "experiments" / tracker / f"{config}.yaml"
    if not config_path.is_file():
        raise FileNotFoundError(f"OSTrack config file not found: {config_path}")

    with config_path.open("r", encoding="utf-8") as config_file:
        config_data = yaml.safe_load(config_file) or {}

    try:
        test_epoch = config_data["TEST"]["EPOCH"]
    except KeyError as exc:
        raise KeyError(f"TEST.EPOCH missing in OSTrack config: {config_path}") from exc

    try:
        return int(test_epoch)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"TEST.EPOCH must be an integer in OSTrack config: {config_path}") from exc


def expected_checkpoint_path(ostrack_root: Path, tracker: str, config: str) -> Path:
    test_epoch = read_test_epoch(ostrack_root, tracker, config)
    return (
        ostrack_root
        / "output"
        / "checkpoints"
        / "train"
        / tracker
        / config
        / f"OSTrack_ep{test_epoch:04d}.pth.tar"
    )


def output_run_dir(args: argparse.Namespace) -> Path:
    return (
        args.output_dir
        / args.tracker
        / args.config
        / args.sequence
        / f"{args.degradation}_{args.severity}_seed{args.seed}"
    )


def validate_inputs(args: argparse.Namespace) -> tuple[Path, Path, Path, Path]:
    ostrack_root = resolve_existing(args.ostrack_root)
    clean_otb_root = resolve_existing(args.clean_otb_root)
    eval_otb_root = resolve_existing(args.eval_otb_root)

    checkpoint = expected_checkpoint_path(ostrack_root, args.tracker, args.config)
    eval_img_dir = eval_otb_root / args.sequence / "img"
    eval_gt_path = eval_otb_root / args.sequence / "groundtruth_rect.txt"

    if not checkpoint.is_file():
        raise FileNotFoundError(f"Checkpoint not found: {checkpoint}")
    if not eval_img_dir.is_dir():
        raise FileNotFoundError(f"Evaluation image directory not found: {eval_img_dir}")
    if not eval_gt_path.is_file():
        raise FileNotFoundError(f"Evaluation ground truth not found: {eval_gt_path}")

    return ostrack_root, clean_otb_root, eval_otb_root, checkpoint


def current_otb_target(otb_link: Path) -> Path | None:
    if not otb_link.exists() and not otb_link.is_symlink():
        return None
    if not otb_link.is_symlink():
        raise RuntimeError(
            f"{otb_link} exists but is not a symlink. Refusing to replace it automatically."
        )
    return Path(os.readlink(otb_link))


def point_otb_symlink(otb_link: Path, target: Path) -> None:
    if otb_link.exists() or otb_link.is_symlink():
        if not otb_link.is_symlink():
            raise RuntimeError(f"Refusing to replace non-symlink path: {otb_link}")
        otb_link.unlink()
    otb_link.parent.mkdir(parents=True, exist_ok=True)
    otb_link.symlink_to(target)


def restore_otb_symlink(otb_link: Path, previous_target: Path | None, clean_otb_root: Path) -> Path:
    restore_target = previous_target if previous_target is not None else clean_otb_root
    if not restore_target.is_absolute():
        restore_target = (otb_link.parent / restore_target).resolve()
    point_otb_symlink(otb_link, restore_target)
    return restore_target


def remove_previous_results(result_dir: Path, sequence: str) -> None:
    result_dir.mkdir(parents=True, exist_ok=True)
    for path in result_dir.glob(f"{sequence}*.txt"):
        path.unlink()


def build_command(args: argparse.Namespace) -> list[str]:
    test_args = [
        "tracking/test.py",
        args.tracker,
        args.config,
        "--dataset_name",
        "otb",
        "--sequence",
        args.sequence,
        "--threads",
        str(args.threads),
        "--num_gpus",
        str(args.num_gpus),
    ]
    if args.conda_env:
        return ["conda", "run", "-n", args.conda_env, "python", *test_args]
    return [sys.executable, *test_args]


def append_result_row(csv_path: Path, row: dict[str, object]) -> None:
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    needs_header = not csv_path.exists() or csv_path.stat().st_size == 0
    with csv_path.open("a", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=CSV_COLUMNS)
        if needs_header:
            writer.writeheader()
        writer.writerow(row)


def experiment_key_from_values(
    tracker: str,
    config: str,
    sequence: str,
    degradation: str,
    severity: str,
    seed: int | str,
) -> tuple[str, str, str, str, str, str]:
    return (
        str(tracker),
        str(config),
        str(sequence),
        str(degradation),
        str(severity),
        str(seed),
    )


def experiment_key_from_row(row: dict[str, object]) -> tuple[str, str, str, str, str, str]:
    return experiment_key_from_values(
        str(row.get("tracker", "")),
        str(row.get("config", "")),
        str(row.get("sequence", "")),
        str(row.get("degradation", "")),
        str(row.get("severity", "")),
        str(row.get("seed", "")),
    )


def read_result_rows(csv_path: Path) -> tuple[list[dict[str, str]], list[str]]:
    if not csv_path.exists() or csv_path.stat().st_size == 0:
        return [], list(CSV_COLUMNS)

    with csv_path.open("r", encoding="utf-8", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        fieldnames = reader.fieldnames or list(CSV_COLUMNS)
        return list(reader), fieldnames


def find_existing_rows(csv_path: Path, key: tuple[str, str, str, str, str, str]) -> list[dict[str, str]]:
    rows, _ = read_result_rows(csv_path)
    return [row for row in rows if experiment_key_from_row(row) == key]


def print_existing_row(row: dict[str, str]) -> None:
    print("Existing result row:")
    for column in CSV_COLUMNS:
        print(f"  {column}: {row.get(column, '')}")


def write_result_rows(csv_path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    for column in CSV_COLUMNS:
        if column not in fieldnames:
            fieldnames.append(column)
    with csv_path.open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def upsert_result_row(
    csv_path: Path,
    row: dict[str, object],
    key: tuple[str, str, str, str, str, str],
    overwrite: bool,
) -> str:
    if not overwrite:
        append_result_row(csv_path, row)
        return "appended"

    rows, fieldnames = read_result_rows(csv_path)
    output_rows: list[dict[str, object]] = []
    replaced = False
    for existing_row in rows:
        if experiment_key_from_row(existing_row) == key:
            if not replaced:
                output_rows.append(row)
                replaced = True
            continue
        output_rows.append(existing_row)
    if not replaced:
        output_rows.append(row)

    write_result_rows(csv_path, output_rows, fieldnames)
    return "replaced" if replaced else "appended"


def main() -> int:
    args = parse_args()
    if "--skip_existing" in sys.argv:
        args.skip_existing_requested = True
    if args.skip_existing_requested and args.overwrite_existing:
        raise ValueError("--skip_existing and --overwrite_existing cannot be used together")
    if args.overwrite_existing:
        args.skip_existing = False

    ostrack_root, clean_otb_root, eval_otb_root, checkpoint = validate_inputs(args)
    run_dir = output_run_dir(args)
    if args.check_only:
        print(f"OSTrack root: {ostrack_root}")
        print(f"Clean OTB root: {clean_otb_root}")
        print(f"Evaluation OTB root: {eval_otb_root}")
        print(f"Expected checkpoint: {checkpoint}")
        print(f"Checkpoint exists: {checkpoint.is_file()}")
        print(f"Output directory: {run_dir}")
        return 0

    experiment_key = experiment_key_from_values(
        args.tracker,
        args.config,
        args.sequence,
        args.degradation,
        args.severity,
        args.seed,
    )
    existing_rows = find_existing_rows(args.results_csv, experiment_key)
    if args.skip_existing and existing_rows:
        print("Skipping existing experiment:")
        print_existing_row(existing_rows[0])
        if len(existing_rows) > 1:
            print(f"Warning: found {len(existing_rows)} matching rows; no run was performed.")
        return 0
    if existing_rows and not args.overwrite_existing:
        raise ValueError(
            "Matching result row already exists. Use --skip_existing to skip or "
            "--overwrite_existing to replace it."
        )

    otb_link = ostrack_root / "data" / "otb"
    previous_target = current_otb_target(otb_link)
    result_dir = (
        ostrack_root
        / "output"
        / "test"
        / "tracking_results"
        / args.tracker
        / args.config
    )

    restored_to: Path | None = None
    try:
        point_otb_symlink(otb_link, eval_otb_root)
        remove_previous_results(result_dir, args.sequence)

        command = build_command(args)
        subprocess.run(command, cwd=ostrack_root, check=True)

        result_path = result_dir / f"{args.sequence}.txt"
        time_path = result_dir / f"{args.sequence}_time.txt"
        if not result_path.is_file():
            raise FileNotFoundError(f"OSTrack result file not found: {result_path}")
        if not time_path.is_file():
            raise FileNotFoundError(f"OSTrack time file not found: {time_path}")

        run_dir.mkdir(parents=True, exist_ok=True)
        copied_result = run_dir / result_path.name
        copied_time = run_dir / time_path.name
        shutil.copy2(result_path, copied_result)
        shutil.copy2(time_path, copied_time)

        gt = load_boxes(eval_otb_root / args.sequence / "groundtruth_rect.txt")
        pred = load_boxes(copied_result)
        metrics = compute_metrics(gt, pred)

        row = {
            "tracker": args.tracker,
            "config": args.config,
            "sequence": args.sequence,
            "degradation": args.degradation,
            "severity": args.severity,
            "seed": args.seed,
            "frames": metrics["frames"],
            "mean_iou": f"{metrics['mean_iou']:.6f}",
            "success_auc": f"{metrics['success_auc']:.6f}",
            "precision_20": f"{metrics['precision_20']:.6f}",
            "mean_center_error": f"{metrics['mean_center_error']:.6f}",
            "result_path": str(copied_result),
            "time_path": str(copied_time),
            "eval_otb_root": str(eval_otb_root),
            "notes": "single-sequence baseline automation",
        }
        write_action = upsert_result_row(
            args.results_csv,
            row,
            experiment_key,
            overwrite=args.overwrite_existing,
        )

        print(f"Frames: {metrics['frames']}")
        print(f"Mean IoU: {metrics['mean_iou']:.4f}")
        print(f"Success AUC: {metrics['success_auc']:.4f}")
        print(f"Precision @20px: {metrics['precision_20']:.4f}")
        print(f"Mean center error: {metrics['mean_center_error']:.2f} px")
        print(f"Output directory: {run_dir}")
        print(f"Results CSV: {args.results_csv}")
        print(f"CSV action: {write_action}")
        return 0
    finally:
        restored_to = restore_otb_symlink(otb_link, previous_target, clean_otb_root)
        print(f"Restored OTB symlink: {otb_link} -> {restored_to}")


if __name__ == "__main__":
    raise SystemExit(main())
