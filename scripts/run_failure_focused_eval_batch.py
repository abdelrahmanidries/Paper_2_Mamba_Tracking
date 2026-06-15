#!/usr/bin/env python3
"""Run the failure-focused UAV123 + NFS evaluation batch."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_PYTHON = "python3"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run failure-focused UAV123 and NFS suites.")
    parser.add_argument("--batch_config", required=True, type=Path)
    parser.add_argument("--dry_run", action="store_true")
    parser.add_argument("--no_skip_existing", action="store_true")
    return parser.parse_args()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def command_text(command: list[str]) -> str:
    return " ".join(command)


def suite_pair_count(path: Path) -> int:
    config = load_json(path)
    return len(config["sequences"]) * len(config["runs"])


def build_command(suite: dict[str, Any], dry_run: bool, skip_existing: bool) -> list[str]:
    command = [
        PROJECT_PYTHON,
        str(suite["runner"]),
        "--suite_config",
        str(suite["suite_config"]),
    ]
    if dry_run:
        command.append("--dry_run")
    if skip_existing:
        command.append("--skip_existing")
    else:
        command.append("--no_skip_existing")
    return command


def main() -> int:
    args = parse_args()
    batch_path = args.batch_config
    batch = load_json(batch_path)
    suites = batch.get("suites")
    if not isinstance(suites, list) or len(suites) != 4:
        raise ValueError("Batch config must contain exactly four suites")

    skip_existing = not args.no_skip_existing
    print(f"batch_name: {batch.get('batch_name', batch_path.stem)}")
    print(f"dry_run: {args.dry_run}")
    print(f"skip_existing: {skip_existing}")

    summary: list[dict[str, str]] = []
    total_pairs = 0
    for index, suite in enumerate(suites, start=1):
        suite_config = Path(suite["suite_config"])
        planned_pairs = suite_pair_count(suite_config)
        total_pairs += planned_pairs
        command = build_command(suite, args.dry_run, skip_existing)
        print()
        print(f"[{index}/{len(suites)}] {suite['name']}")
        print(f"planned_sequence_condition_pairs: {planned_pairs}")
        print(f"command: {command_text(command)}")
        subprocess.run(command, cwd=ROOT, check=True)
        summary.append(
            {
                "name": str(suite["name"]),
                "dataset": str(suite["dataset"]),
                "pairs": str(planned_pairs),
                "status": "dry_run_completed" if args.dry_run else "completed",
            }
        )

    print()
    print("Batch summary")
    print("name  dataset  sequence_condition_pairs  status")
    print("----  -------  ------------------------  ------")
    for row in summary:
        print(f"{row['name']}  {row['dataset']}  {row['pairs']}  {row['status']}")
    print(f"total_sequence_condition_pairs: {total_pairs}")
    print("metrics: computed by the underlying suite/evaluation scripts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
