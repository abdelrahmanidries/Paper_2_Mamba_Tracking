#!/usr/bin/env python3
"""Run expanded NFS baseline and RG-SSB evaluation suites sequentially."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_PYTHON = "python3"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the expanded NFS evaluation batch.")
    parser.add_argument("--batch_config", required=True, type=Path)
    parser.add_argument("--dry_run", action="store_true")
    parser.add_argument("--no_skip_existing", action="store_true")
    return parser.parse_args()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def suite_pair_count(path: Path) -> int:
    config = load_json(path)
    return len(config["sequences"]) * len(config["runs"])


def command_text(command: list[str]) -> str:
    return " ".join(command)


def main() -> int:
    args = parse_args()
    batch = load_json(args.batch_config)
    suites = batch.get("suites")
    if not isinstance(suites, list) or len(suites) != 2:
        raise ValueError("Expanded NFS batch config must contain exactly two suites.")

    skip_existing = not args.no_skip_existing
    print(f"batch_name: {batch.get('batch_name', args.batch_config.stem)}")
    print(f"dry_run: {args.dry_run}")
    print(f"skip_existing: {skip_existing}")

    total_pairs = 0
    summary: list[dict[str, str]] = []
    for index, suite in enumerate(suites, start=1):
        suite_config = Path(suite["suite_config"])
        planned_pairs = suite_pair_count(suite_config)
        total_pairs += planned_pairs
        command = [
            PROJECT_PYTHON,
            str(suite["runner"]),
            "--suite_config",
            str(suite_config),
            "--skip_existing" if skip_existing else "--no_skip_existing",
        ]
        if args.dry_run:
            command.append("--dry_run")
        print()
        print(f"[{index}/{len(suites)}] {suite['name']}")
        print(f"planned_sequence_condition_pairs: {planned_pairs}")
        print(f"command: {command_text(command)}")
        subprocess.run(command, cwd=ROOT, check=True)
        summary.append(
            {
                "name": str(suite["name"]),
                "pairs": str(planned_pairs),
                "status": "dry_run_completed" if args.dry_run else "completed",
            }
        )

    print()
    print("Batch summary")
    print("name  sequence_condition_pairs  status")
    print("----  ------------------------  ------")
    for row in summary:
        print(f"{row['name']}  {row['pairs']}  {row['status']}")
    print(f"total_sequence_condition_pairs: {total_pairs}")
    print("metrics: computed by the underlying NFS suite/evaluation scripts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
