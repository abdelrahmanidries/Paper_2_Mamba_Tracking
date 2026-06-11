"""Run a reproducible local RG-SSB training/evaluation cycle.

This script orchestrates existing commands only. It does not edit OSTrack
source, create architectures, compute metrics directly, or delete outputs.
"""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
PROJECT_PYTHON = "python3"
TRACKER = "ostrack"
RUN_ID_COLUMNS = ("tracker", "config", "sequence", "degradation", "severity", "seed")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run one RG-SSB experiment cycle.")
    parser.add_argument(
        "--cycle_config",
        default="configs/rgssb_experiment_cycle_local.json",
        type=Path,
        help="Path to the experiment-cycle JSON config.",
    )
    parser.add_argument("--dry_run", action="store_true", help="Print commands without running them.")
    parser.add_argument("--skip_training", action="store_true", help="Skip training and verify checkpoint before evaluation.")
    parser.add_argument("--eval_only", action="store_true", help="Evaluation-only mode; same as --skip_training.")
    parser.add_argument(
        "--overwrite_existing",
        action="store_true",
        help="Replace matching CSV rows through run_ostrack_otb_eval.py.",
    )
    parser.add_argument(
        "--skip_existing",
        action="store_true",
        default=True,
        help="Skip matching CSV rows. Default: true unless --overwrite_existing is set.",
    )
    return parser.parse_args()


def command_text(command: list[str]) -> str:
    return " ".join(command)


class RunLogger:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def write(self, message: str = "") -> None:
        print(message)
        with self.path.open("a", encoding="utf-8", newline="\n") as log_file:
            log_file.write(message + "\n")


def resolve_project_path(path: str | Path) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    return ROOT / candidate


def load_cycle_config(path: Path) -> dict[str, Any]:
    config_path = resolve_project_path(path)
    with config_path.open("r", encoding="utf-8") as config_file:
        config = json.load(config_file)

    required = {
        "cycle_name",
        "config_name",
        "ostrack_root",
        "clean_otb_root",
        "output_root",
        "results_csv",
        "conda_env",
        "train",
        "eval",
        "overwrite_existing",
        "sequences",
        "conditions",
    }
    missing = sorted(required - set(config))
    if missing:
        raise ValueError(f"Cycle config missing required fields: {missing}")
    if not isinstance(config["sequences"], list) or not config["sequences"]:
        raise ValueError("Cycle config field 'sequences' must be a non-empty list")
    if not isinstance(config["conditions"], list) or not config["conditions"]:
        raise ValueError("Cycle config field 'conditions' must be a non-empty list")
    return config


def read_ostrack_yaml(ostrack_root: Path, config_name: str) -> tuple[Path, dict[str, Any]]:
    config_path = ostrack_root / "experiments" / TRACKER / f"{config_name}.yaml"
    if not config_path.is_file():
        raise FileNotFoundError(f"OSTrack training config not found: {config_path}")

    with config_path.open("r", encoding="utf-8") as yaml_file:
        data = yaml.safe_load(yaml_file) or {}
    return config_path, data


def test_epoch_from_yaml(config_path: Path, data: dict[str, Any]) -> int:
    try:
        epoch = data["TEST"]["EPOCH"]
    except KeyError as exc:
        raise KeyError(f"TEST.EPOCH missing in OSTrack config: {config_path}") from exc
    try:
        return int(epoch)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"TEST.EPOCH must be an integer in OSTrack config: {config_path}") from exc


def base_checkpoint_from_yaml(ostrack_root: Path, config_path: Path, data: dict[str, Any]) -> Path:
    try:
        pretrain_file = data["MODEL"]["PRETRAIN_FILE"]
    except KeyError as exc:
        raise KeyError(f"MODEL.PRETRAIN_FILE missing in OSTrack config: {config_path}") from exc

    checkpoint = Path(str(pretrain_file))
    if not checkpoint.is_absolute():
        checkpoint = ostrack_root / checkpoint
    return checkpoint


def expected_checkpoint_path(ostrack_root: Path, config_name: str, test_epoch: int) -> Path:
    return (
        ostrack_root
        / "output"
        / "checkpoints"
        / "train"
        / TRACKER
        / config_name
        / f"OSTrack_ep{test_epoch:04d}.pth.tar"
    )


def validate_condition(condition: dict[str, Any], index: int) -> None:
    missing = sorted({"degradation", "severity", "seed"} - set(condition))
    if missing:
        raise ValueError(f"Condition #{index} missing fields: {missing}")
    if condition["degradation"] == "clean" and condition["severity"] != "none":
        raise ValueError("Clean condition must use severity 'none'")


def validate_sequence(clean_otb_root: Path, sequence: str) -> None:
    sequence_root = clean_otb_root / sequence
    img_dir = sequence_root / "img"
    gt_path = sequence_root / "groundtruth_rect.txt"
    if not img_dir.is_dir():
        raise FileNotFoundError(f"Clean OTB image directory not found: {img_dir}")
    if not gt_path.is_file():
        raise FileNotFoundError(f"Clean OTB ground truth not found: {gt_path}")


def validate_paths(config: dict[str, Any]) -> dict[str, Path | int]:
    project_root = ROOT
    if not project_root.is_dir():
        raise FileNotFoundError(f"Project root not found: {project_root}")

    ostrack_root = resolve_project_path(config["ostrack_root"])
    clean_otb_root = resolve_project_path(config["clean_otb_root"])
    output_root = resolve_project_path(config["output_root"])
    results_csv = resolve_project_path(config["results_csv"])

    if not ostrack_root.is_dir():
        raise FileNotFoundError(f"OSTrack root not found: {ostrack_root}")
    if not clean_otb_root.is_dir():
        raise FileNotFoundError(f"Clean OTB root not found: {clean_otb_root}")

    ostrack_config_path, ostrack_yaml = read_ostrack_yaml(ostrack_root, config["config_name"])
    base_checkpoint = base_checkpoint_from_yaml(ostrack_root, ostrack_config_path, ostrack_yaml)
    if not base_checkpoint.is_file():
        raise FileNotFoundError(f"Base checkpoint not found: {base_checkpoint}")

    test_epoch = test_epoch_from_yaml(ostrack_config_path, ostrack_yaml)
    expected_checkpoint = expected_checkpoint_path(
        ostrack_root,
        config["config_name"],
        test_epoch,
    )
    expected_checkpoint_parent = expected_checkpoint.parent
    checkpoint_root = ostrack_root / "output" / "checkpoints" / "train" / TRACKER
    if not checkpoint_root.is_dir():
        raise FileNotFoundError(f"OSTrack checkpoint root not found: {checkpoint_root}")

    for sequence in config["sequences"]:
        validate_sequence(clean_otb_root, str(sequence))
    for index, condition in enumerate(config["conditions"], start=1):
        validate_condition(condition, index)

    return {
        "project_root": project_root,
        "ostrack_root": ostrack_root,
        "clean_otb_root": clean_otb_root,
        "output_root": output_root,
        "results_csv": results_csv,
        "ostrack_config_path": ostrack_config_path,
        "base_checkpoint": base_checkpoint,
        "expected_checkpoint": expected_checkpoint,
        "expected_checkpoint_parent": expected_checkpoint_parent,
        "test_epoch": test_epoch,
    }


def build_training_command(config: dict[str, Any]) -> list[str]:
    return [
        "conda",
        "run",
        "-n",
        str(config["conda_env"]),
        "python",
        "lib/train/run_training.py",
        "--script",
        TRACKER,
        "--config",
        str(config["config_name"]),
        "--save_dir",
        "output",
        "--use_lmdb",
        "0",
        "--use_wandb",
        "0",
    ]


def degraded_root(output_root: Path, sequence: str, condition: dict[str, Any]) -> Path:
    return output_root / f"otb_{sequence}_{condition['degradation']}_{condition['severity']}"


def build_degrade_command(
    clean_otb_root: Path,
    output_root: Path,
    sequence: str,
    condition: dict[str, Any],
) -> list[str]:
    return [
        PROJECT_PYTHON,
        "scripts/create_degraded_otb_sequence.py",
        "--clean_otb_root",
        str(clean_otb_root),
        "--sequence",
        sequence,
        "--degradation",
        str(condition["degradation"]),
        "--severity",
        str(condition["severity"]),
        "--seed",
        str(condition["seed"]),
        "--output_root",
        str(output_root),
    ]


def build_eval_command(
    config: dict[str, Any],
    paths: dict[str, Path | int],
    sequence: str,
    condition: dict[str, Any],
    eval_otb_root: Path,
    overwrite_existing: bool,
    skip_existing: bool,
) -> list[str]:
    command = [
        PROJECT_PYTHON,
        "scripts/run_ostrack_otb_eval.py",
        "--ostrack_root",
        str(paths["ostrack_root"]),
        "--clean_otb_root",
        str(paths["clean_otb_root"]),
        "--eval_otb_root",
        str(eval_otb_root),
        "--sequence",
        sequence,
        "--config",
        str(config["config_name"]),
        "--tracker",
        TRACKER,
        "--degradation",
        str(condition["degradation"]),
        "--severity",
        str(condition["severity"]),
        "--seed",
        str(condition["seed"]),
        "--results_csv",
        str(paths["results_csv"]),
        "--conda_env",
        str(config["conda_env"]),
    ]
    if overwrite_existing:
        command.append("--overwrite_existing")
    elif skip_existing:
        command.append("--skip_existing")
    else:
        command.append("--no_skip_existing")
    return command


def run_command(command: list[str], cwd: Path, dry_run: bool, logger: RunLogger) -> None:
    logger.write(f"$ {command_text(command)}")
    if dry_run:
        logger.write("[dry-run] command not executed")
        return
    subprocess.run(command, cwd=cwd, check=True)


def append_failure(
    failure_log: Path,
    config_path: Path,
    cycle_name: str,
    sequence: str,
    condition: dict[str, Any],
    stage: str,
    error: BaseException,
    commands: list[list[str]],
) -> None:
    failure_log.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "cycle_config": str(config_path),
        "cycle_name": cycle_name,
        "sequence": sequence,
        "condition": condition,
        "stage": stage,
        "error_type": type(error).__name__,
        "error": str(error),
        "commands": [command_text(command) for command in commands],
    }
    with failure_log.open("a", encoding="utf-8", newline="\n") as failure_file:
        failure_file.write(json.dumps(record, sort_keys=True) + "\n")


def read_matching_rows(
    csv_path: Path,
    config_name: str,
    sequences: list[str],
    conditions: list[dict[str, Any]],
) -> list[dict[str, str]]:
    if not csv_path.exists() or csv_path.stat().st_size == 0:
        return []

    wanted = {
        (
            TRACKER,
            config_name,
            sequence,
            str(condition["degradation"]),
            str(condition["severity"]),
            str(condition["seed"]),
        )
        for sequence in sequences
        for condition in conditions
    }
    with csv_path.open("r", encoding="utf-8", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        return [
            row
            for row in reader
            if tuple(str(row.get(column, "")) for column in RUN_ID_COLUMNS) in wanted
        ]


def print_final_rows(
    logger: RunLogger,
    csv_path: Path,
    config_name: str,
    sequences: list[str],
    conditions: list[dict[str, Any]],
) -> None:
    rows = read_matching_rows(csv_path, config_name, sequences, conditions)
    logger.write("")
    logger.write(f"Final CSV rows matching config '{config_name}': {len(rows)}")
    if not rows:
        logger.write("No matching rows found.")
        return

    columns = [
        "sequence",
        "degradation",
        "severity",
        "seed",
        "frames",
        "mean_iou",
        "success_auc",
        "precision_20",
        "mean_center_error",
    ]
    for row in rows:
        logger.write(", ".join(f"{column}={row.get(column, '')}" for column in columns))


def main() -> int:
    args = parse_args()
    config_path = resolve_project_path(args.cycle_config)
    config = load_cycle_config(config_path)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_dir = ROOT / "outputs" / "experiment_cycle_logs"
    run_log = log_dir / f"{config['cycle_name']}_{timestamp}.log"
    failure_log = log_dir / f"{config['cycle_name']}_failures.jsonl"
    logger = RunLogger(run_log)

    overwrite_existing = bool(config["overwrite_existing"]) or args.overwrite_existing
    skip_existing = bool(args.skip_existing) and not overwrite_existing
    train_requested = bool(config["train"]) and not args.skip_training and not args.eval_only
    eval_requested = bool(config["eval"])

    paths = validate_paths(config)
    training_command = build_training_command(config)

    logger.write(f"Cycle name: {config['cycle_name']}")
    logger.write(f"Config name: {config['config_name']}")
    logger.write(f"Cycle config: {config_path}")
    logger.write(f"Run log: {run_log}")
    logger.write(f"Failure log: {failure_log}")
    logger.write(f"OSTrack config: {paths['ostrack_config_path']}")
    logger.write(f"Base checkpoint: {paths['base_checkpoint']}")
    logger.write(f"Expected checkpoint: {paths['expected_checkpoint']}")
    logger.write(f"TEST.EPOCH: {paths['test_epoch']}")
    logger.write(f"Training command: {command_text(training_command)}")

    if train_requested:
        logger.write("")
        logger.write("Training")
        run_command(training_command, Path(paths["ostrack_root"]), args.dry_run, logger)
    else:
        reason = "eval_only" if args.eval_only else "skip_training/config train=false"
        logger.write(f"Training skipped: {reason}")

    expected_checkpoint = Path(paths["expected_checkpoint"])
    if not expected_checkpoint.is_file() and args.dry_run and train_requested:
        logger.write(f"Checkpoint not present yet; dry-run training would create: {expected_checkpoint}")
    elif not expected_checkpoint.is_file():
        message = f"Expected checkpoint not found: {expected_checkpoint}"
        logger.write(message)
        if eval_requested:
            raise FileNotFoundError(message)
    else:
        logger.write(f"Checkpoint verified: {expected_checkpoint}")

    summary: list[dict[str, str]] = []
    if eval_requested:
        logger.write("")
        logger.write("Evaluation")
        for sequence in [str(value) for value in config["sequences"]]:
            for condition in config["conditions"]:
                commands: list[list[str]] = []
                stage = "run_ostrack_otb_eval"
                row_base = {
                    "sequence": sequence,
                    "degradation": str(condition["degradation"]),
                    "severity": str(condition["severity"]),
                    "seed": str(condition["seed"]),
                }
                try:
                    if condition["degradation"] == "clean":
                        eval_otb_root = Path(paths["clean_otb_root"])
                    else:
                        stage = "create_degraded_otb_sequence"
                        eval_otb_root = degraded_root(Path(paths["output_root"]), sequence, condition)
                        create_command = build_degrade_command(
                            Path(paths["clean_otb_root"]),
                            Path(paths["output_root"]),
                            sequence,
                            condition,
                        )
                        commands.append(create_command)
                        run_command(create_command, ROOT, args.dry_run, logger)

                    stage = "run_ostrack_otb_eval"
                    eval_command = build_eval_command(
                        config,
                        paths,
                        sequence,
                        condition,
                        eval_otb_root,
                        overwrite_existing=overwrite_existing,
                        skip_existing=skip_existing,
                    )
                    commands.append(eval_command)
                    run_command(eval_command, ROOT, args.dry_run, logger)

                    status = "planned" if args.dry_run else "completed"
                    summary.append({**row_base, "status": status, "details": str(eval_otb_root)})
                except subprocess.CalledProcessError as error:
                    append_failure(
                        failure_log,
                        config_path,
                        str(config["cycle_name"]),
                        sequence,
                        condition,
                        stage,
                        error,
                        commands,
                    )
                    summary.append({**row_base, "status": "failed", "details": f"{stage}: exit {error.returncode}"})
                    logger.write(f"FAILED {sequence} {condition}: {stage} exit {error.returncode}")
                except Exception as error:
                    append_failure(
                        failure_log,
                        config_path,
                        str(config["cycle_name"]),
                        sequence,
                        condition,
                        stage,
                        error,
                        commands,
                    )
                    summary.append({**row_base, "status": "failed", "details": f"{stage}: {error}"})
                    logger.write(f"FAILED {sequence} {condition}: {stage}: {error}")
    else:
        logger.write("Evaluation skipped: config eval=false")

    logger.write("")
    logger.write("Run summary")
    for row in summary:
        logger.write(
            f"{row['sequence']} {row['degradation']} {row['severity']} seed={row['seed']} "
            f"status={row['status']} details={row['details']}"
        )

    print_final_rows(
        logger,
        Path(paths["results_csv"]),
        str(config["config_name"]),
        [str(value) for value in config["sequences"]],
        config["conditions"],
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
