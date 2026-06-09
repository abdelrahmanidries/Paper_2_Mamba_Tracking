"""Run a reproducible OSTrack baseline degradation suite."""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_PYTHON = "python3"
RUN_ID_COLUMNS = ("tracker", "config", "sequence", "degradation", "severity", "seed")
FAILURE_LOG = Path("experiments/baseline_suite_failures.jsonl")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run an OSTrack degradation baseline suite.")
    parser.add_argument(
        "--suite_config",
        default="configs/baseline_degradation_suite_car1.json",
        type=Path,
        help="Path to the suite JSON config.",
    )
    parser.add_argument("--dry_run", action="store_true", help="Print commands without executing them.")
    parser.set_defaults(skip_existing=True)
    parser.add_argument(
        "--skip_existing",
        dest="skip_existing",
        action="store_true",
        help="Skip runs already present in the results CSV. Default: true.",
    )
    parser.add_argument(
        "--no_skip_existing",
        dest="skip_existing",
        action="store_false",
        help="Do not skip runs already present in the results CSV.",
    )
    parser.add_argument("--max_runs", type=int, default=None, help="Optional maximum number of non-skipped runs.")
    return parser.parse_args()


def load_suite_config(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as config_file:
        config = json.load(config_file)

    required = {
        "clean_otb_root",
        "output_root",
        "tracker",
        "config",
        "ostrack_root",
        "results_csv",
        "runs",
    }
    missing = sorted(required - set(config))
    if missing:
        raise ValueError(f"Suite config missing required fields: {missing}")
    if "sequence" not in config and "sequences" not in config:
        raise ValueError("Suite config must include either 'sequence' or 'sequences'")
    if not isinstance(config["runs"], list) or not config["runs"]:
        raise ValueError("Suite config field 'runs' must be a non-empty list")
    return config


def get_sequences(config: dict[str, Any]) -> list[str]:
    if "sequences" in config:
        sequences = config["sequences"]
        if not isinstance(sequences, list) or not sequences:
            raise ValueError("Suite config field 'sequences' must be a non-empty list")
        return [str(sequence) for sequence in sequences]
    return [str(config["sequence"])]


def run_key(
    tracker: str,
    config_name: str,
    sequence: str,
    degradation: str,
    severity: str,
    seed: int | str,
) -> tuple[str, str, str, str, str, str]:
    return (
        str(tracker),
        str(config_name),
        str(sequence),
        str(degradation),
        str(severity),
        str(seed),
    )


def load_existing_results(csv_path: Path) -> set[tuple[str, str, str, str, str, str]]:
    if not csv_path.exists() or csv_path.stat().st_size == 0:
        return set()

    existing: set[tuple[str, str, str, str, str, str]] = set()
    with csv_path.open("r", encoding="utf-8", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            if not row:
                continue
            existing.add(tuple(str(row.get(column, "")) for column in RUN_ID_COLUMNS))
    return existing


def degraded_root(config: dict[str, Any], sequence: str, run: dict[str, Any]) -> Path:
    output_root = Path(config["output_root"])
    return output_root / f"otb_{sequence}_{run['degradation']}_{run['severity']}"


def build_create_command(config: dict[str, Any], sequence: str, run: dict[str, Any]) -> list[str]:
    return [
        PROJECT_PYTHON,
        "scripts/create_degraded_otb_sequence.py",
        "--clean_otb_root",
        str(config["clean_otb_root"]),
        "--sequence",
        str(sequence),
        "--degradation",
        str(run["degradation"]),
        "--severity",
        str(run["severity"]),
        "--seed",
        str(run["seed"]),
        "--output_root",
        str(config["output_root"]),
    ]


def build_eval_command(
    config: dict[str, Any],
    sequence: str,
    run: dict[str, Any],
    eval_otb_root: Path | str,
    overwrite_existing: bool = False,
) -> list[str]:
    command = [
        PROJECT_PYTHON,
        "scripts/run_ostrack_otb_eval.py",
        "--ostrack_root",
        str(config["ostrack_root"]),
        "--clean_otb_root",
        str(config["clean_otb_root"]),
        "--eval_otb_root",
        str(eval_otb_root),
        "--sequence",
        str(sequence),
        "--config",
        str(config["config"]),
        "--tracker",
        str(config["tracker"]),
        "--degradation",
        str(run["degradation"]),
        "--severity",
        str(run["severity"]),
        "--seed",
        str(run["seed"]),
        "--results_csv",
        str(config["results_csv"]),
    ]
    if overwrite_existing:
        command.append("--overwrite_existing")
    return command


def command_text(command: list[str]) -> str:
    return " ".join(command)


def append_failure(
    failure_log: Path,
    config_path: Path,
    run: dict[str, Any],
    stage: str,
    error: BaseException,
    commands: list[list[str]],
) -> None:
    failure_log.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "suite_config": str(config_path),
        "run": run,
        "stage": stage,
        "error_type": type(error).__name__,
        "error": str(error),
        "commands": [command_text(command) for command in commands],
    }
    with failure_log.open("a", encoding="utf-8", newline="\n") as log_file:
        log_file.write(json.dumps(record, sort_keys=True) + "\n")


def print_summary(rows: list[dict[str, str]]) -> None:
    if not rows:
        print("No runs in summary.")
        return

    columns = ["sequence", "degradation", "severity", "seed", "status", "details"]
    widths = {
        column: max(len(column), *(len(str(row.get(column, ""))) for row in rows))
        for column in columns
    }
    header = "  ".join(column.ljust(widths[column]) for column in columns)
    print("\nSummary")
    print(header)
    print("  ".join("-" * widths[column] for column in columns))
    for row in rows:
        print("  ".join(str(row.get(column, "")).ljust(widths[column]) for column in columns))


def validate_run(run: dict[str, Any], index: int) -> None:
    missing = sorted({"degradation", "severity", "seed"} - set(run))
    if missing:
        raise ValueError(f"Run #{index} missing fields: {missing}")


def execute_command(command: list[str], dry_run: bool) -> None:
    if dry_run:
        print(f"[dry-run] {command_text(command)}")
        return
    subprocess.run(command, cwd=ROOT, check=True)


def main() -> int:
    args = parse_args()
    suite_config_path = args.suite_config
    config = load_suite_config(suite_config_path)
    results_csv = Path(config["results_csv"])
    existing = load_existing_results(results_csv)

    summary: list[dict[str, str]] = []
    attempted = 0
    sequences = get_sequences(config)

    for sequence in sequences:
        for index, run in enumerate(config["runs"], start=1):
            validate_run(run, index)
            key = run_key(
                config["tracker"],
                config["config"],
                sequence,
                run["degradation"],
                run["severity"],
                run["seed"],
            )

            row_base = {
                "sequence": str(sequence),
                "degradation": str(run["degradation"]),
                "severity": str(run["severity"]),
                "seed": str(run["seed"]),
            }

            if args.skip_existing and key in existing:
                summary.append({**row_base, "status": "skipped", "details": "already in results CSV"})
                continue
            if args.max_runs is not None and attempted >= args.max_runs:
                summary.append({**row_base, "status": "skipped", "details": "max_runs reached"})
                continue

            attempted += 1
            commands: list[list[str]] = []
            stage = "eval"
            run_record = {**run, "sequence": sequence}
            try:
                if run["degradation"] == "clean":
                    eval_root: Path | str = config["clean_otb_root"]
                else:
                    stage = "create_degraded_otb_sequence"
                    eval_root = degraded_root(config, sequence, run)
                    create_command = build_create_command(config, sequence, run)
                    commands.append(create_command)
                    execute_command(create_command, args.dry_run)

                stage = "run_ostrack_otb_eval"
                eval_command = build_eval_command(
                    config,
                    sequence,
                    run,
                    eval_root,
                    overwrite_existing=not args.skip_existing,
                )
                commands.append(eval_command)
                execute_command(eval_command, args.dry_run)

                status = "planned" if args.dry_run else "completed"
                details = "commands printed" if args.dry_run else "metrics appended by eval script"
                summary.append({**row_base, "status": status, "details": details})
                existing.add(key)
            except subprocess.CalledProcessError as error:
                append_failure(FAILURE_LOG, suite_config_path, run_record, stage, error, commands)
                summary.append({**row_base, "status": "failed", "details": f"{stage}: exit {error.returncode}"})
            except Exception as error:
                append_failure(FAILURE_LOG, suite_config_path, run_record, stage, error, commands)
                summary.append({**row_base, "status": "failed", "details": f"{stage}: {error}"})

    print_summary(summary)
    if not args.dry_run:
        print(f"\nFailure log: {FAILURE_LOG}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
