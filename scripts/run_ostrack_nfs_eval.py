#!/usr/bin/env python3
"""Run one OSTrack NFS sequence evaluation and append metrics."""

from __future__ import annotations

import argparse
import ast
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


NFS_DATASET_PY = ROOT / "external" / "OSTrack" / "lib" / "test" / "evaluation" / "nfsdataset.py"
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
    parser = argparse.ArgumentParser(description="Run OSTrack on one NFS sequence and append metrics.")
    parser.add_argument("--ostrack_root", default="external/OSTrack", type=Path)
    parser.add_argument("--clean_nfs_root", required=True, type=Path)
    parser.add_argument("--eval_nfs_root", required=True, type=Path)
    parser.add_argument("--sequence", required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--tracker", default="ostrack")
    parser.add_argument("--degradation", default="clean")
    parser.add_argument("--severity", default="none")
    parser.add_argument("--seed", default=0, type=int)
    parser.add_argument("--output_dir", default="outputs/ostrack_runs", type=Path)
    parser.add_argument("--results_csv", default="experiments/baseline_results.csv", type=Path)
    parser.add_argument("--conda_env", default="ostrack")
    parser.add_argument("--num_gpus", default=1, type=int)
    parser.add_argument("--threads", default=0, type=int)
    parser.set_defaults(skip_existing=True, skip_existing_requested=False)
    parser.add_argument("--skip_existing", dest="skip_existing", action="store_true")
    parser.add_argument("--no_skip_existing", dest="skip_existing", action="store_false")
    parser.add_argument("--skip_existing_requested", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--overwrite_existing", action="store_true")
    parser.add_argument("--check_only", action="store_true")
    return parser.parse_args()


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


def get_sequence_info(sequence: str) -> dict:
    for info in load_sequence_info():
        if info["name"] == sequence:
            return info
    raise ValueError(f"Unknown NFS sequence: {sequence}")


def count_nonempty_lines(path: Path) -> int:
    return sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip())


def validate_nfs_sequence(root: Path, sequence: str) -> dict:
    info = get_sequence_info(sequence)
    seq_dir = root / info["path"]
    anno_path = root / info["anno_path"]
    start = int(info["startFrame"]) + int(info.get("initOmit", 0))
    end = int(info["endFrame"])
    nz = int(info["nz"])
    ext = str(info["ext"])
    first = seq_dir / f"{start:0{nz}}.{ext}"
    last = seq_dir / f"{end:0{nz}}.{ext}"
    if not seq_dir.is_dir():
        raise FileNotFoundError(f"NFS sequence image directory not found: {seq_dir}")
    if not anno_path.is_file():
        raise FileNotFoundError(f"NFS annotation file not found: {anno_path}")
    if not first.is_file() or not last.is_file():
        raise FileNotFoundError(f"Missing first/last NFS frame for {sequence}: {first}, {last}")
    frames = end - start + 1
    gt_lines = count_nonempty_lines(anno_path) - int(info.get("initOmit", 0))
    if frames != gt_lines:
        raise ValueError(f"Frame/annotation mismatch for {sequence}: frames={frames} gt={gt_lines}")
    return info


def read_test_epoch(ostrack_root: Path, tracker: str, config: str) -> int:
    config_path = ostrack_root / "experiments" / tracker / f"{config}.yaml"
    if not config_path.is_file():
        raise FileNotFoundError(f"OSTrack config file not found: {config_path}")
    data = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
    return int(data["TEST"]["EPOCH"])


def expected_checkpoint_path(ostrack_root: Path, tracker: str, config: str) -> Path:
    epoch = read_test_epoch(ostrack_root, tracker, config)
    return ostrack_root / "output" / "checkpoints" / "train" / tracker / config / f"OSTrack_ep{epoch:04d}.pth.tar"


def output_run_dir(args: argparse.Namespace) -> Path:
    return (
        args.output_dir
        / args.tracker
        / args.config
        / "nfs"
        / args.sequence
        / f"{args.degradation}_{args.severity}_seed{args.seed}"
    )


def experiment_key_from_values(tracker: str, config: str, sequence: str, degradation: str, severity: str, seed: int | str) -> tuple[str, str, str, str, str, str]:
    return (str(tracker), str(config), str(sequence), str(degradation), str(severity), str(seed))


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
        return list(reader), reader.fieldnames or list(CSV_COLUMNS)


def write_result_rows(csv_path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    for column in CSV_COLUMNS:
        if column not in fieldnames:
            fieldnames.append(column)
    with csv_path.open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def append_result_row(csv_path: Path, row: dict[str, object]) -> None:
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    needs_header = not csv_path.exists() or csv_path.stat().st_size == 0
    with csv_path.open("a", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=CSV_COLUMNS)
        if needs_header:
            writer.writeheader()
        writer.writerow(row)


def find_existing_rows(csv_path: Path, key: tuple[str, str, str, str, str, str]) -> list[dict[str, str]]:
    rows, _ = read_result_rows(csv_path)
    return [row for row in rows if experiment_key_from_row(row) == key]


def upsert_result_row(csv_path: Path, row: dict[str, object], key: tuple[str, str, str, str, str, str], overwrite: bool) -> str:
    if not overwrite:
        append_result_row(csv_path, row)
        return "appended"
    rows, fieldnames = read_result_rows(csv_path)
    output_rows: list[dict[str, object]] = []
    replaced = False
    for existing in rows:
        if experiment_key_from_row(existing) == key:
            if not replaced:
                output_rows.append(row)
                replaced = True
            continue
        output_rows.append(existing)
    if not replaced:
        output_rows.append(row)
    write_result_rows(csv_path, output_rows, fieldnames)
    return "replaced" if replaced else "appended"


def current_nfs_target(nfs_link: Path) -> Path | None:
    if not nfs_link.exists() and not nfs_link.is_symlink():
        return None
    if not nfs_link.is_symlink():
        raise RuntimeError(f"{nfs_link} exists but is not a symlink. Refusing to replace it automatically.")
    return Path(os.readlink(nfs_link))


def point_nfs_symlink(nfs_link: Path, target: Path) -> None:
    if nfs_link.exists() or nfs_link.is_symlink():
        if not nfs_link.is_symlink():
            raise RuntimeError(f"Refusing to replace non-symlink path: {nfs_link}")
        nfs_link.unlink()
    nfs_link.parent.mkdir(parents=True, exist_ok=True)
    nfs_link.symlink_to(target)


def restore_nfs_symlink(nfs_link: Path, previous_target: Path | None, clean_nfs_root: Path) -> Path:
    restore_target = previous_target if previous_target is not None else clean_nfs_root
    if not restore_target.is_absolute():
        restore_target = (nfs_link.parent / restore_target).resolve()
    point_nfs_symlink(nfs_link, restore_target)
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
        "nfs",
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


def print_existing_row(row: dict[str, str]) -> None:
    print("Existing result row:")
    for column in CSV_COLUMNS:
        print(f"  {column}: {row.get(column, '')}")


def main() -> int:
    args = parse_args()
    if "--skip_existing" in sys.argv:
        args.skip_existing_requested = True
    if args.skip_existing_requested and args.overwrite_existing:
        raise ValueError("--skip_existing and --overwrite_existing cannot be used together")
    if args.overwrite_existing:
        args.skip_existing = False

    ostrack_root = args.ostrack_root.resolve()
    clean_nfs_root = args.clean_nfs_root.resolve()
    eval_nfs_root = args.eval_nfs_root.resolve()
    if not ostrack_root.is_dir():
        raise FileNotFoundError(f"OSTrack root not found: {ostrack_root}")
    if not clean_nfs_root.is_dir():
        raise FileNotFoundError(f"Clean NFS root not found: {clean_nfs_root}")
    if not eval_nfs_root.is_dir():
        raise FileNotFoundError(f"Evaluation NFS root not found: {eval_nfs_root}")
    info = validate_nfs_sequence(eval_nfs_root, args.sequence)
    checkpoint = expected_checkpoint_path(ostrack_root, args.tracker, args.config)
    if not checkpoint.is_file():
        raise FileNotFoundError(f"Checkpoint not found: {checkpoint}")

    run_dir = output_run_dir(args)
    if args.check_only:
        print(f"OSTrack root: {ostrack_root}")
        print(f"Clean NFS root: {clean_nfs_root}")
        print(f"Evaluation NFS root: {eval_nfs_root}")
        print(f"Dataset name: nfs")
        print(f"Sequence path: {info['path']}")
        print(f"Annotation path: {info['anno_path']}")
        print(f"Expected checkpoint: {checkpoint}")
        print(f"Output directory: {run_dir}")
        return 0

    key = experiment_key_from_values(args.tracker, args.config, args.sequence, args.degradation, args.severity, args.seed)
    existing_rows = find_existing_rows(args.results_csv, key)
    if args.skip_existing and existing_rows:
        print("Skipping existing experiment:")
        print_existing_row(existing_rows[0])
        return 0
    if existing_rows and not args.overwrite_existing:
        raise ValueError("Matching result row already exists. Use --skip_existing or --overwrite_existing.")

    nfs_link = ostrack_root / "data" / "nfs"
    previous_target = current_nfs_target(nfs_link)
    result_dir = ostrack_root / "output" / "test" / "tracking_results" / args.tracker / args.config

    try:
        point_nfs_symlink(nfs_link, eval_nfs_root)
        remove_previous_results(result_dir, args.sequence)
        subprocess.run(build_command(args), cwd=ostrack_root, check=True)

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

        gt = load_boxes(eval_nfs_root / info["anno_path"])
        init_omit = int(info.get("initOmit", 0))
        if init_omit:
            gt = gt[init_omit:, :]
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
            "eval_otb_root": str(eval_nfs_root),
            "notes": "single-sequence NFS automation",
        }
        action = upsert_result_row(args.results_csv, row, key, overwrite=args.overwrite_existing)
        print(f"Frames: {metrics['frames']}")
        print(f"Success AUC: {metrics['success_auc']:.4f}")
        print(f"Precision @20px: {metrics['precision_20']:.4f}")
        print(f"Mean center error: {metrics['mean_center_error']:.2f} px")
        print(f"Output directory: {run_dir}")
        print(f"Results CSV: {args.results_csv}")
        print(f"CSV action: {action}")
        return 0
    finally:
        restored_to = restore_nfs_symlink(nfs_link, previous_target, clean_nfs_root)
        print(f"Restored NFS symlink: {nfs_link} -> {restored_to}")


if __name__ == "__main__":
    raise SystemExit(main())
