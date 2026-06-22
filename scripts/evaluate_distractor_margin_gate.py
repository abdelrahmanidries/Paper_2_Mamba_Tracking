#!/usr/bin/env python3
"""Evaluate the local gate for the target-distractor margin ablation.

This script only reads existing result CSV rows. It does not run training or
evaluation.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path


BASE_CONFIG = "vitb_256_mae_ce_32x4_ep300_rgssb_head_train_lasot_degraded_3000_featcons_lam002_debug"
TDM_CONFIG = "vitb_256_mae_ce_32x4_ep300_rgssb_head_train_lasot_degraded_3000_featcons_lam002_tdm_debug"
SEQUENCES = ["Car1", "David2", "Coke"]
CONDITIONS = [
    ("clean", "none", "0"),
    ("motion_blur", "medium", "42"),
    ("low_resolution", "medium", "42"),
    ("gaussian_noise", "medium", "42"),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate local target-distractor margin gate from existing CSV rows.")
    parser.add_argument("--results_csv", default="experiments/baseline_results.csv", type=Path)
    parser.add_argument("--cycle_config", default="configs/rgssb_experiment_cycle_featcons_lam002_tdm.json", type=Path)
    parser.add_argument("--gate_file", default="implementation/final_ablation_gate.md", type=Path)
    parser.add_argument("--check_only", action="store_true")
    return parser.parse_args()


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as csv_file:
        return list(csv.DictReader(csv_file))


def key(row: dict[str, str]) -> tuple[str, str, str, str]:
    return (row["sequence"], row["degradation"], row["severity"], str(row["seed"]))


def row_map(rows: list[dict[str, str]], config: str) -> dict[tuple[str, str, str, str], dict[str, str]]:
    selected = {}
    for row in rows:
        if row.get("config") == config:
            selected[key(row)] = row
    return selected


def fmt(value: float) -> str:
    return f"{value:+.6f}"


def validate_static_files(args: argparse.Namespace) -> None:
    if not args.gate_file.is_file():
        raise FileNotFoundError(f"Missing gate file: {args.gate_file}")
    if not args.results_csv.is_file():
        raise FileNotFoundError(f"Missing results CSV: {args.results_csv}")
    cfg = json.loads(args.cycle_config.read_text(encoding="utf-8"))
    if cfg.get("config_name") != TDM_CONFIG:
        raise AssertionError(f"Cycle config_name mismatch: expected {TDM_CONFIG}, got {cfg.get('config_name')}")
    gate_text = args.gate_file.read_text(encoding="utf-8")
    gate_text_lower = gate_text.lower()
    required_gate_phrases = [
        "local proceed gate",
        "corrected expanded nfs improves meaningfully",
        "paper freeze v1",
    ]
    missing = [phrase for phrase in required_gate_phrases if phrase not in gate_text_lower]
    if missing:
        raise AssertionError(f"Gate file missing required phrases: {missing}")


def evaluate(rows: list[dict[str, str]]) -> tuple[str, dict[str, object]]:
    base = row_map(rows, BASE_CONFIG)
    tdm = row_map(rows, TDM_CONFIG)
    expected_keys = [(seq, deg, sev, seed) for seq in SEQUENCES for deg, sev, seed in CONDITIONS]
    missing_base = [k for k in expected_keys if k not in base]
    missing_tdm = [k for k in expected_keys if k not in tdm]
    if missing_base or missing_tdm:
        return "INSUFFICIENT_RESULTS", {
            "missing_base": missing_base,
            "missing_tdm": missing_tdm,
            "available_tdm_rows": len(tdm),
        }

    diffs = []
    per_condition = defaultdict(list)
    clean_diffs = []
    detailed = []
    for k in expected_keys:
        base_auc = float(base[k]["success_auc"])
        tdm_auc = float(tdm[k]["success_auc"])
        diff = tdm_auc - base_auc
        diffs.append(diff)
        condition_name = k[1] if k[2] == "none" else f"{k[1]}_{k[2]}"
        per_condition[condition_name].append(diff)
        if k[1] == "clean":
            clean_diffs.append(diff)
        detailed.append((k, base_auc, tdm_auc, diff))

    overall = sum(diffs) / len(diffs)
    condition_avgs = {condition: sum(values) / len(values) for condition, values in sorted(per_condition.items())}
    clean_avg = sum(clean_diffs) / len(clean_diffs)
    largest_clean_drop = min(clean_diffs)
    gates = {
        "all_12_pairs_present": len(diffs) == 12,
        "local_average_improves": overall > 0.0,
        "no_severe_clean_collapse": clean_avg >= -0.02,
    }
    decision = "PROMOTE_TO_HPC" if all(gates.values()) else "REJECT_AND_ROLL_BACK_TO_PAPER_FREEZE_V1"
    return decision, {
        "overall_average_auc_difference": overall,
        "per_condition_auc_differences": condition_avgs,
        "average_clean_difference": clean_avg,
        "largest_individual_clean_drop": largest_clean_drop,
        "gates": gates,
        "detailed": detailed,
    }


def main() -> int:
    args = parse_args()
    validate_static_files(args)
    rows = read_rows(args.results_csv)
    decision, report = evaluate(rows)
    print(f"base_config: {BASE_CONFIG}")
    print(f"tdm_config: {TDM_CONFIG}")
    print(f"decision: {decision}")
    if decision == "INSUFFICIENT_RESULTS":
        print(f"available_tdm_rows: {report['available_tdm_rows']}")
        print(f"missing_base_pairs: {len(report['missing_base'])}")
        print(f"missing_tdm_pairs: {len(report['missing_tdm'])}")
        if report["missing_tdm"]:
            print(f"first_missing_tdm_pair: {report['missing_tdm'][0]}")
        return 0

    print(f"overall_average_auc_difference: {fmt(report['overall_average_auc_difference'])}")
    print(f"average_clean_difference: {fmt(report['average_clean_difference'])}")
    print(f"largest_individual_clean_drop: {fmt(report['largest_individual_clean_drop'])}")
    print("per_condition_auc_differences:")
    for condition, value in report["per_condition_auc_differences"].items():
        print(f"  {condition}: {fmt(value)}")
    print("local_gates:")
    for gate, passed in report["gates"].items():
        print(f"  {gate}: {'PASS' if passed else 'FAIL'}")
    print("detailed_pairs:")
    for pair, base_auc, tdm_auc, diff in report["detailed"]:
        print(f"  {pair}: base={base_auc:.6f} tdm={tdm_auc:.6f} diff={fmt(diff)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
