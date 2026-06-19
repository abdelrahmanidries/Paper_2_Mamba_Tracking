#!/usr/bin/env python3
"""Export invalid pre-fix NFS rows from baseline_results.csv."""

from __future__ import annotations

import argparse
import csv
import shutil
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export NFS rows known invalid before the XYXY normalization fix.")
    parser.add_argument("--results_csv", type=Path, default=Path("experiments/baseline_results.csv"))
    parser.add_argument("--output_csv", type=Path, default=Path("experiments/invalid_nfs_rows_before_xyxy_fix.csv"))
    parser.add_argument("--backup_csv", type=Path, default=Path("experiments/baseline_results_before_nfs_xyxy_fix_backup.csv"))
    parser.add_argument("--remove_from_main_csv", action="store_true")
    parser.add_argument("--check_only", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.results_csv.is_file():
        raise FileNotFoundError(f"Results CSV not found: {args.results_csv}")
    with args.results_csv.open("r", encoding="utf-8", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        fieldnames = reader.fieldnames or []
        rows = list(reader)
    invalid = [row for row in rows if str(row.get("sequence", "")).startswith("nfs_")]
    kept = [row for row in rows if not str(row.get("sequence", "")).startswith("nfs_")]

    if not args.check_only:
        args.output_csv.parent.mkdir(parents=True, exist_ok=True)
        with args.output_csv.open("w", encoding="utf-8", newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(invalid)
        if args.remove_from_main_csv:
            shutil.copy2(args.results_csv, args.backup_csv)
            with args.results_csv.open("w", encoding="utf-8", newline="") as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(kept)

    print(f"total_rows: {len(rows)}")
    print(f"invalid_nfs_rows: {len(invalid)}")
    print(f"non_nfs_rows: {len(kept)}")
    print(f"output_csv: {args.output_csv}")
    print(f"remove_from_main_csv: {args.remove_from_main_csv}")
    print(f"check_only: {args.check_only}")
    if args.remove_from_main_csv and not args.check_only:
        print(f"backup_csv: {args.backup_csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
