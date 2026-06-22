#!/usr/bin/env python3
"""Verify final Paper Freeze V1 package assets and numeric anchors."""

from __future__ import annotations

import csv
import math
from pathlib import Path
from typing import Dict, List


ROOT = Path.cwd()
BASELINE_CONFIG = "vitb_256_mae_ce_32x4_ep300"
FINAL_CONFIG = "vitb_256_mae_ce_32x4_ep300_rgssb_head_train_lasot_degraded_hpc_featcons_lam002"

REQUIRED_FILES = [
    "implementation/paper_freeze_v1_manifest.md",
    "experiments/paper_claim_traceability.csv",
    "experiments/paper_level_result_table_current.csv",
    "experiments/paper_level_benchmark_summary.csv",
    "experiments/paper_efficiency_results.csv",
    "experiments/rgssb_tdm_gate_comparison.csv",
    "experiments/nfs_corrected_drift_onset_analysis.csv",
    "implementation/nfs_result_recovery_manifest.md",
    "reports/08_method_architecture.md",
    "reports/09_experiments_current.md",
    "reports/10_discussion_limitations_current.md",
    "implementation/paper_level_ablation_plan.md",
    "implementation/paper_level_risk_and_claims.md",
    "tables/paper_main_benchmark_table.csv",
    "tables/paper_main_benchmark_table.tex",
    "tables/paper_condition_table.csv",
    "tables/paper_condition_table.tex",
    "tables/paper_ablation_table.csv",
    "tables/paper_ablation_table.tex",
    "tables/paper_efficiency_table.csv",
    "tables/paper_efficiency_table.tex",
    "reports/11_results_final.md",
    "reports/12_conclusion_future_work.md",
    "reports/paper_draft_freeze_v1.md",
    "implementation/final_paper_asset_manifest.md",
    "implementation/final_reproducibility_checklist.md",
    "implementation/final_claim_audit.md",
]

FIGURE_STEMS = [
    "benchmark_auc_change",
    "condition_auc_change",
    "efficiency_comparison",
    "ablation_decision",
    "nfs_failure_mode_distribution",
]


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def num(value: str) -> float:
    return float(str(value).replace("+", ""))


def assert_close(name: str, actual: float, expected: float, tol: float = 1e-6) -> None:
    if math.isnan(actual) or abs(actual - expected) > tol:
        raise AssertionError(f"{name}: expected {expected:+.6f}, got {actual:+.6f}")


def require_files() -> None:
    missing = [path for path in REQUIRED_FILES if not (ROOT / path).exists()]
    for stem in FIGURE_STEMS:
        for ext in ["svg", "pdf", "png"]:
            fig = ROOT / "figures" / "paper_freeze_v1" / f"{stem}.{ext}"
            if not fig.exists():
                missing.append(str(fig.relative_to(ROOT)))
    if missing:
        raise FileNotFoundError("Missing final package assets: " + ", ".join(missing))


def verify_benchmark_anchors() -> None:
    rows = read_csv(ROOT / "experiments" / "paper_level_benchmark_summary.csv")
    by_bench = {r["benchmark"]: r for r in rows}
    assert_close("OTB avg AUC change", num(by_bench["OTB"]["avg_auc_change"]), 0.033144)
    assert_close("UAV123 avg AUC change", num(by_bench["UAV123"]["avg_auc_change"]), 0.017405)
    assert_close("NFS avg AUC change", num(by_bench["NFS"]["avg_auc_change"]), -0.009638)

    cross = read_csv(ROOT / "experiments" / "rgssb_hpc_cross_benchmark_failure_inspection.csv")
    assert_close("cross-benchmark avg AUC change", sum(num(r["auc_change"]) for r in cross) / len(cross), 0.001478)

    main = read_csv(ROOT / "tables" / "paper_main_benchmark_table.csv")
    main_text = "\n".join(",".join(r.values()) for r in main)
    for anchor in ["+0.033144", "+0.017405", "-0.009638", "+0.001478"]:
        if anchor not in main_text:
            raise AssertionError(f"Missing benchmark anchor in main table: {anchor}")


def verify_efficiency_anchors() -> None:
    rows = read_csv(ROOT / "experiments" / "paper_efficiency_results.csv")
    complexity = {r["config"]: r for r in rows if r["measurement_type"] == "complexity"}
    runtime = [r for r in rows if r["measurement_type"] == "controlled_runtime"]
    aggregate = [r for r in rows if r["measurement_type"] == "controlled_runtime_aggregate"]

    if int(complexity[BASELINE_CONFIG]["total_params"]) != 92518533:
        raise AssertionError("Baseline parameter anchor failed")
    final = complexity[FINAL_CONFIG]
    if int(final["total_params"]) != 94598469:
        raise AssertionError("Final parameter anchor failed")
    if int(final["trainable_params"]) != 8554053:
        raise AssertionError("Final trainable parameter anchor failed")
    if int(final["frozen_params"]) != 86044416:
        raise AssertionError("Final frozen parameter anchor failed")
    if int(final["total_params"]) - int(complexity[BASELINE_CONFIG]["total_params"]) != 2079936:
        raise AssertionError("Parameter increase anchor failed")
    if final["flops_or_macs"] != "unavailable":
        raise AssertionError("FLOPs/MACs must remain unavailable")

    gpus = {r["gpu_name"] for r in runtime + aggregate if r["gpu_name"]}
    if gpus != {"Tesla V100-PCIE-32GB"}:
        raise AssertionError(f"Runtime rows must use only Tesla V100-PCIE-32GB, got {gpus}")
    for config in [BASELINE_CONFIG, FINAL_CONFIG]:
        reps = [r for r in runtime if r["config"] == config]
        aggs = [r for r in aggregate if r["config"] == config]
        if len(reps) != 3 or len(aggs) != 1:
            raise AssertionError(f"{config} must have three runtime repetitions and one aggregate")


def verify_nfs_and_tdm() -> None:
    nfs_manifest = (ROOT / "implementation" / "nfs_result_recovery_manifest.md").read_text(encoding="utf-8")
    if "XYXY" not in nfs_manifest or "XYWH" not in nfs_manifest:
        raise AssertionError("NFS recovery manifest must mention normalized XYXY to XYWH provenance")
    drift = read_csv(ROOT / "experiments" / "nfs_corrected_drift_onset_analysis.csv")
    if len(drift) != 10:
        raise AssertionError("Corrected NFS drift analysis must have 10 rows")
    tdm_rows = read_csv(ROOT / "experiments" / "rgssb_tdm_gate_comparison.csv")
    avg_tdm = sum(num(r["tdm_minus_global_auc_change"]) for r in tdm_rows) / len(tdm_rows)
    assert_close("TDM avg gate difference", avg_tdm, -0.014549)
    report = (ROOT / "reports" / "11_results_final.md").read_text(encoding="utf-8")
    if "rejected" not in report.lower() or "TDM" not in report:
        raise AssertionError("Final results report must describe TDM as rejected")


def verify_tables_and_figures() -> None:
    for stem in [
        "paper_main_benchmark_table",
        "paper_condition_table",
        "paper_ablation_table",
        "paper_efficiency_table",
    ]:
        csv_path = ROOT / "tables" / f"{stem}.csv"
        tex_path = ROOT / "tables" / f"{stem}.tex"
        if not csv_path.exists() or not tex_path.exists():
            raise AssertionError(f"Missing table pair for {stem}")
        if "\\begin{table}" not in tex_path.read_text(encoding="utf-8"):
            raise AssertionError(f"{tex_path} does not look like a LaTeX table")
        if not read_csv(csv_path):
            raise AssertionError(f"{csv_path} has no rows")


def verify_claims() -> None:
    claims = read_csv(ROOT / "experiments" / "paper_claim_traceability.csv")
    unsupported = [c for c in claims if c["status"] == "unsupported"]
    for claim in claims:
        evidence = claim.get("evidence_file", "")
        if claim["status"] in {"safe", "qualified", "superseded"} and evidence and not (ROOT / evidence).exists():
            raise AssertionError(f"Claim {claim['claim_id']} evidence missing: {evidence}")
    report_text = "\n".join(
        path.read_text(encoding="utf-8", errors="ignore")
        for path in [
            ROOT / "reports" / "11_results_final.md",
            ROOT / "reports" / "paper_draft_freeze_v1.md",
            ROOT / "implementation" / "final_claim_audit.md",
        ]
    )
    if "-0.403866" in report_text:
        raise AssertionError("Old invalid NFS cheetah value appears in final reports")
    forbidden_positive_phrases = [
        "achieves state-of-the-art",
        "is state-of-the-art",
        "state-of-the-art performance",
        "proves universal robustness",
        "universally robust",
        "consistent superiority across all benchmarks",
    ]
    lower_report = report_text.lower()
    for phrase in forbidden_positive_phrases:
        if phrase in lower_report:
            raise AssertionError(f"Potential unsupported claim found: {phrase}")
    print(f"Unsupported claims remaining in traceability file: {len(unsupported)}")
    for claim in unsupported:
        print(f"  {claim['claim_id']}: {claim['claim_text']}")


def main() -> int:
    require_files()
    verify_benchmark_anchors()
    verify_efficiency_anchors()
    verify_nfs_and_tdm()
    verify_tables_and_figures()
    verify_claims()
    print("Final paper package verification passed.")
    print("Missing citations/assets requiring human review: full paper references and final manuscript formatting.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
