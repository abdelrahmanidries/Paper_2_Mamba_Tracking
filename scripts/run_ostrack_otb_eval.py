"""Run one OSTrack OTB sequence evaluation and append baseline metrics."""

from __future__ import annotations

import argparse
import csv
import os
import shutil
import subprocess
import sys
from pathlib import Path

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
    parser.add_argument(
        "--conda_env",
        default="ostrack",
        help="Conda env used for OSTrack. Use an empty string to call python directly.",
    )
    parser.add_argument("--num_gpus", default=1, type=int)
    parser.add_argument("--threads", default=0, type=int)
    return parser.parse_args()


def resolve_existing(path: Path) -> Path:
    if not path.exists():
        raise FileNotFoundError(path)
    return path.resolve()


def validate_inputs(args: argparse.Namespace) -> tuple[Path, Path, Path]:
    ostrack_root = resolve_existing(args.ostrack_root)
    clean_otb_root = resolve_existing(args.clean_otb_root)
    eval_otb_root = resolve_existing(args.eval_otb_root)

    checkpoint = (
        ostrack_root
        / "output"
        / "checkpoints"
        / "train"
        / args.tracker
        / args.config
        / "OSTrack_ep0300.pth.tar"
    )
    eval_img_dir = eval_otb_root / args.sequence / "img"
    eval_gt_path = eval_otb_root / args.sequence / "groundtruth_rect.txt"

    if not checkpoint.is_file():
        raise FileNotFoundError(f"Checkpoint not found: {checkpoint}")
    if not eval_img_dir.is_dir():
        raise FileNotFoundError(f"Evaluation image directory not found: {eval_img_dir}")
    if not eval_gt_path.is_file():
        raise FileNotFoundError(f"Evaluation ground truth not found: {eval_gt_path}")

    return ostrack_root, clean_otb_root, eval_otb_root


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


def main() -> int:
    args = parse_args()
    ostrack_root, clean_otb_root, eval_otb_root = validate_inputs(args)

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

        run_dir = (
            args.output_dir
            / args.tracker
            / args.config
            / args.sequence
            / f"{args.degradation}_{args.severity}_seed{args.seed}"
        )
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
        append_result_row(args.results_csv, row)

        print(f"Frames: {metrics['frames']}")
        print(f"Mean IoU: {metrics['mean_iou']:.4f}")
        print(f"Success AUC: {metrics['success_auc']:.4f}")
        print(f"Precision @20px: {metrics['precision_20']:.4f}")
        print(f"Mean center error: {metrics['mean_center_error']:.2f} px")
        print(f"Output directory: {run_dir}")
        print(f"Results CSV: {args.results_csv}")
        return 0
    finally:
        restored_to = restore_otb_symlink(otb_link, previous_target, clean_otb_root)
        print(f"Restored OTB symlink: {otb_link} -> {restored_to}")


if __name__ == "__main__":
    raise SystemExit(main())
