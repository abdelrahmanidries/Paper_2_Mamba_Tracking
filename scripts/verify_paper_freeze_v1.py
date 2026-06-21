#!/usr/bin/env python3
"""Verify Paper Freeze V1 provenance and corrected-result anchors."""

from __future__ import annotations

import csv
import math
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASELINE_CONFIG = "vitb_256_mae_ce_32x4_ep300"
RGSSB_CONFIG = "vitb_256_mae_ce_32x4_ep300_rgssb_head_train_lasot_degraded_hpc_featcons_lam002"
OLD_INVALID_CHANGE = "-0.403866"


AUTHORITATIVE_FILES = [
    "experiments/baseline_results.csv",
    "experiments/invalid_nfs_rows_before_xyxy_fix.csv",
    "experiments/rgssb_hpc_broader_otb_comparison.csv",
    "experiments/rgssb_hpc_nfs_expanded32_comparison.csv",
    "experiments/rgssb_hpc_failure_focused_uav_nfs_comparison.csv",
    "experiments/rgssb_hpc_cross_benchmark_failure_inspection.csv",
    "experiments/paper_level_result_table_current.csv",
    "experiments/paper_level_benchmark_summary.csv",
    "experiments/nfs_corrected_drift_onset_analysis.csv",
    "experiments/paper_claim_traceability.csv",
    "implementation/paper_freeze_v1_manifest.md",
    "implementation/final_ablation_gate.md",
    "reports/09_experiments_current.md",
    "reports/10_discussion_limitations_current.md",
]

CURRENT_REPORTS = [
    "implementation/paper_freeze_v1_manifest.md",
    "implementation/nfs_result_recovery_manifest.md",
    "implementation/rgssb_hpc_nfs_expanded32_result_analysis.md",
    "implementation/rgssb_hpc_cross_benchmark_failure_inspection.md",
    "implementation/rgssb_current_method_evidence_summary.md",
    "implementation/paper_level_results_summary.md",
    "implementation/paper_level_risk_and_claims.md",
    "implementation/final_ablation_gate.md",
    "reports/09_experiments_current.md",
    "reports/10_discussion_limitations_current.md",
]


def read_rows(path: str) -> list[dict[str, str]]:
    with (ROOT / path).open("r", encoding="utf-8", newline="") as csv_file:
        return list(csv.DictReader(csv_file))


def assert_close(actual: float, expected: float, label: str, tol: float = 1e-6) -> None:
    if not math.isclose(actual, expected, rel_tol=0.0, abs_tol=tol):
        raise AssertionError(f"{label}: expected {expected:.6f}, got {actual:.6f}")


def signed_float(value: str) -> float:
    return float(value.replace("+", ""))


def avg_auc_change(rows: list[dict[str, str]]) -> float:
    return sum(signed_float(row["auc_change"]) for row in rows) / len(rows)


def exact_baseline_row(rows: list[dict[str, str]], config: str, sequence: str, degradation: str, severity: str, seed: str) -> dict[str, str]:
    matches = [
        row
        for row in rows
        if row["config"] == config
        and row["sequence"] == sequence
        and row["degradation"] == degradation
        and row["severity"] == severity
        and row["seed"] == seed
    ]
    if len(matches) != 1:
        raise AssertionError(f"Expected one row for {config} {sequence} {degradation}/{severity} seed {seed}, found {len(matches)}")
    return matches[0]


def verify_files_exist() -> None:
    missing = [path for path in AUTHORITATIVE_FILES if not (ROOT / path).exists()]
    if missing:
        raise AssertionError(f"Missing authoritative files: {missing}")


def verify_result_anchors() -> None:
    baseline_rows = read_rows("experiments/baseline_results.csv")
    base_anchor = exact_baseline_row(baseline_rows, BASELINE_CONFIG, "nfs_cheetah", "low_resolution", "medium", "42")
    rgssb_anchor = exact_baseline_row(baseline_rows, RGSSB_CONFIG, "nfs_cheetah", "low_resolution", "medium", "42")
    assert_close(float(base_anchor["success_auc"]), 0.519832, "baseline nfs_cheetah low-resolution AUC")
    assert_close(float(base_anchor["mean_iou"]), 0.519185, "baseline nfs_cheetah low-resolution mean IoU")
    assert_close(float(rgssb_anchor["success_auc"]), 0.516986, "RG-SSB nfs_cheetah low-resolution AUC")
    assert_close(float(rgssb_anchor["mean_iou"]), 0.516131, "RG-SSB nfs_cheetah low-resolution mean IoU")

    nfs_active = [row for row in baseline_rows if row["sequence"].startswith("nfs_") and row["config"] in {BASELINE_CONFIG, RGSSB_CONFIG}]
    counts = Counter(row["config"] for row in nfs_active)
    if len(nfs_active) != 256 or counts[BASELINE_CONFIG] != 128 or counts[RGSSB_CONFIG] != 128:
        raise AssertionError(f"Corrected active NFS row count mismatch: total={len(nfs_active)} counts={dict(counts)}")

    invalid_rows = read_rows("experiments/invalid_nfs_rows_before_xyxy_fix.csv")
    invalid_counts = Counter(row["config"] for row in invalid_rows)
    if len(invalid_rows) != 256 or invalid_counts[BASELINE_CONFIG] != 128 or invalid_counts[RGSSB_CONFIG] != 128:
        raise AssertionError(f"Invalid NFS archive mismatch: total={len(invalid_rows)} counts={dict(invalid_counts)}")

    nfs_pairs = read_rows("experiments/rgssb_hpc_nfs_expanded32_comparison.csv")
    keys = {(row["sequence"], row["degradation"], row["severity"], row["seed"]) for row in nfs_pairs}
    if len(nfs_pairs) != 128 or len(keys) != 128:
        raise AssertionError(f"Expanded NFS pairs mismatch: rows={len(nfs_pairs)} unique_keys={len(keys)}")
    if len({row["sequence"] for row in nfs_pairs}) != 32:
        raise AssertionError("Expanded NFS sequence count is not 32")
    assert_close(avg_auc_change(nfs_pairs), -0.009638, "corrected expanded NFS average AUC change")

    otb_rows = read_rows("experiments/rgssb_hpc_broader_otb_comparison.csv")
    assert_close(avg_auc_change(otb_rows), 0.033144, "broader OTB average AUC change")

    paper_bench = read_rows("experiments/paper_level_benchmark_summary.csv")
    uav = [row for row in paper_bench if row["benchmark"] == "UAV123"]
    if len(uav) != 1:
        raise AssertionError("Missing UAV123 paper-level benchmark summary row")
    assert_close(signed_float(uav[0]["avg_auc_change"]), 0.017405, "expanded UAV123 average AUC change")

    cross_rows = read_rows("experiments/rgssb_hpc_cross_benchmark_failure_inspection.csv")
    assert_close(avg_auc_change(cross_rows), 0.001478, "corrected cross-benchmark failure-inspection average")


def verify_drift() -> None:
    rows = read_rows("experiments/nfs_corrected_drift_onset_analysis.csv")
    if len(rows) != 10:
        raise AssertionError(f"Expected 10 corrected NFS drift rows, found {len(rows)}")
    counts = Counter(row["terminal_failure_mode"] for row in rows)
    expected = {
        "persistent RG-SSB-specific target loss": 5,
        "sudden center jump": 3,
        "shared tracker failure": 1,
        "ambiguous": 1,
    }
    if counts != expected:
        raise AssertionError(f"Drift terminal outcome mismatch: expected={expected} got={dict(counts)}")


def verify_no_stale_nfs_value() -> None:
    stale_hits = []
    for path in CURRENT_REPORTS:
        text = (ROOT / path).read_text(encoding="utf-8")
        if OLD_INVALID_CHANGE in text:
            stale_hits.append(path)
    if stale_hits:
        raise AssertionError(f"Old invalid NFS change {OLD_INVALID_CHANGE} found in current reports: {stale_hits}")


def verify_claim_traceability() -> tuple[Counter, list[str]]:
    rows = read_rows("experiments/paper_claim_traceability.csv")
    statuses = Counter(row["status"] for row in rows)
    unsupported = [row["claim_id"] for row in rows if row["status"] == "unsupported"]
    missing_evidence = []
    for row in rows:
        evidence = row["evidence_file"].strip()
        if row["status"] in {"safe", "qualified", "superseded"} and not evidence:
            missing_evidence.append(row["claim_id"])
        if evidence and not (ROOT / evidence).exists():
            missing_evidence.append(f"{row['claim_id']}:{evidence}")
    if missing_evidence:
        raise AssertionError(f"Missing claim evidence: {missing_evidence}")
    broad_safe = [
        row["claim_id"]
        for row in rows
        if row["status"] == "safe"
        and row["claim_type"] == "paper_claim"
        and row["evidence_scope"] in {"not evaluated", ""}
    ]
    if broad_safe:
        raise AssertionError(f"Broad unsupported claims marked safe: {broad_safe}")
    return statuses, unsupported


def main() -> int:
    try:
        verify_files_exist()
        verify_result_anchors()
        verify_drift()
        verify_no_stale_nfs_value()
        statuses, unsupported = verify_claim_traceability()
    except Exception as exc:
        print(f"paper_freeze_v1 verification FAILED: {exc}")
        return 1

    print("paper_freeze_v1 verification PASSED")
    print(f"claim_status_counts: {dict(statuses)}")
    print(f"unsupported_claims: {unsupported}")
    print("anchors: OTB +0.033144, UAV123 +0.017405, NFS -0.009638, cross +0.001478")
    print("corrected_nfs_active_rows: 256")
    print("invalid_nfs_archive_rows: 256")
    print("corrected_drift_rows: 10")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
