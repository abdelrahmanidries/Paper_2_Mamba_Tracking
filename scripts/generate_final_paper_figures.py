#!/usr/bin/env python3
"""Generate final Paper Freeze V1 tables, figures, and report drafts from CSV evidence."""

from __future__ import annotations

import csv
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Sequence

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


PROJECT_ROOT = Path.cwd()
TABLES_DIR = PROJECT_ROOT / "tables"
FIGURES_DIR = PROJECT_ROOT / "figures" / "paper_freeze_v1"
REPORTS_DIR = PROJECT_ROOT / "reports"
IMPLEMENTATION_DIR = PROJECT_ROOT / "implementation"

BASELINE_CONFIG = "vitb_256_mae_ce_32x4_ep300"
FINAL_CONFIG = "vitb_256_mae_ce_32x4_ep300_rgssb_head_train_lasot_degraded_hpc_featcons_lam002"


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: Sequence[Dict[str, object]], fieldnames: Sequence[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def fmt_float(value: object, digits: int = 6, signed: bool = False) -> str:
    if value in ("", None):
        return ""
    val = float(value)
    if math.isnan(val):
        return "nan"
    prefix = "+" if signed and val >= 0 else ""
    return f"{prefix}{val:.{digits}f}"


def numeric(value: str) -> float:
    if value in ("", None):
        return float("nan")
    return float(str(value).replace("+", ""))


def mean(values: Iterable[float]) -> float:
    vals = [v for v in values if not math.isnan(v)]
    if not vals:
        return float("nan")
    return sum(vals) / len(vals)


def escape_tex(text: object) -> str:
    s = str(text)
    replacements = {
        "\\": "\\textbackslash{}",
        "&": "\\&",
        "%": "\\%",
        "$": "\\$",
        "#": "\\#",
        "_": "\\_",
        "{": "\\{",
        "}": "\\}",
        "~": "\\textasciitilde{}",
        "^": "\\textasciicircum{}",
    }
    for old, new in replacements.items():
        s = s.replace(old, new)
    return s


def write_latex_table(path: Path, rows: Sequence[Dict[str, object]], columns: Sequence[str], caption: str, label: str) -> None:
    aligns = "l" * len(columns)
    lines = [
        "\\begin{table}[t]",
        "\\centering",
        f"\\caption{{{escape_tex(caption)}}}",
        f"\\label{{{escape_tex(label)}}}",
        f"\\begin{{tabular}}{{{aligns}}}",
        "\\toprule",
        " & ".join(escape_tex(c) for c in columns) + " \\\\",
        "\\midrule",
    ]
    for row in rows:
        lines.append(" & ".join(escape_tex(row.get(c, "")) for c in columns) + " \\\\")
    lines.extend(["\\bottomrule", "\\end{tabular}", "\\end{table}", ""])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def condition_label(condition: str) -> str:
    return {
        "clean": "Clean",
        "motion_blur_medium": "Motion blur",
        "low_resolution_medium": "Low resolution",
        "gaussian_noise_medium": "Gaussian noise",
    }.get(condition, condition.replace("_", " "))


def load_benchmark_tables():
    benchmark_rows = read_csv(PROJECT_ROOT / "experiments" / "paper_level_benchmark_summary.csv")
    detailed_rows = read_csv(PROJECT_ROOT / "experiments" / "paper_level_result_table_current.csv")
    cross_rows = read_csv(PROJECT_ROOT / "experiments" / "rgssb_hpc_cross_benchmark_failure_inspection.csv")
    return benchmark_rows, detailed_rows, cross_rows


def generate_main_benchmark_table() -> List[Dict[str, object]]:
    benchmark_rows, _detailed_rows, cross_rows = load_benchmark_tables()
    rows: List[Dict[str, object]] = []
    for row in benchmark_rows:
        rows.append(
            {
                "Benchmark": row["benchmark"],
                "Sequences": row["sequence_count"],
                "Pairs": row["compared_pairs"],
                "Baseline AUC": fmt_float(row["baseline_avg_auc"]),
                "RG-SSB AUC": fmt_float(row["rgssb_avg_auc"]),
                "AUC Change": fmt_float(row["avg_auc_change"], signed=True),
                "Precision Change": fmt_float(row["avg_precision_change"], signed=True),
                "Center Error Change": fmt_float(row["avg_center_error_change"], signed=True),
                "Conclusion": row["conclusion"],
            }
        )
    rows.append(
        {
            "Benchmark": "Cross-benchmark aggregate",
            "Sequences": len({(r["benchmark"], r["sequence"]) for r in cross_rows}),
            "Pairs": len(cross_rows),
            "Baseline AUC": fmt_float(mean(numeric(r["baseline_auc"]) for r in cross_rows)),
            "RG-SSB AUC": fmt_float(mean(numeric(r["hpc_rgssb_auc"]) for r in cross_rows)),
            "AUC Change": fmt_float(mean(numeric(r["auc_change"]) for r in cross_rows), signed=True),
            "Precision Change": fmt_float(mean(numeric(r["precision_20_change"]) for r in cross_rows), signed=True),
            "Center Error Change": fmt_float(mean(numeric(r["center_error_change"]) for r in cross_rows), signed=True),
            "Conclusion": "Near-neutral positive overall; not uniformly improved",
        }
    )
    fields = list(rows[0].keys())
    write_csv(TABLES_DIR / "paper_main_benchmark_table.csv", rows, fields)
    write_latex_table(
        TABLES_DIR / "paper_main_benchmark_table.tex",
        rows,
        fields,
        "Paper Freeze V1 benchmark summary.",
        "tab:paper-freeze-benchmark",
    )
    return rows


def generate_condition_table() -> List[Dict[str, object]]:
    _bench, detailed_rows, _cross = load_benchmark_tables()
    groups: Dict[str, List[Dict[str, str]]] = defaultdict(list)
    for row in detailed_rows:
        groups[row["condition"]].append(row)
    order = ["clean", "motion_blur_medium", "low_resolution_medium", "gaussian_noise_medium"]
    rows: List[Dict[str, object]] = []
    for cond in order:
        vals = groups[cond]
        rows.append(
            {
                "Condition": condition_label(cond),
                "Pairs": len(vals),
                "Baseline AUC": fmt_float(mean(numeric(r["baseline_auc"]) for r in vals)),
                "RG-SSB AUC": fmt_float(mean(numeric(r["rgssb_auc"]) for r in vals)),
                "AUC Change": fmt_float(mean(numeric(r["auc_change"]) for r in vals), signed=True),
                "Precision Change": fmt_float(mean(numeric(r["precision_change"]) for r in vals), signed=True),
                "Center Error Change": fmt_float(mean(numeric(r["center_error_change"]) for r in vals), signed=True),
                "Conclusion": "improves on average" if mean(numeric(r["auc_change"]) for r in vals) > 0 else "mixed / negative",
            }
        )
    fields = list(rows[0].keys())
    write_csv(TABLES_DIR / "paper_condition_table.csv", rows, fields)
    write_latex_table(TABLES_DIR / "paper_condition_table.tex", rows, fields, "Condition-level robustness summary.", "tab:conditions")
    return rows


def generate_ablation_table() -> List[Dict[str, object]]:
    lambda_rows = read_csv(PROJECT_ROOT / "experiments" / "rgssb_featcons_lambda_sweep_comparison.csv")
    response_rows = read_csv(PROJECT_ROOT / "experiments" / "rgssb_featcons_lam002_vs_respcons_comparison.csv")
    target_rows = read_csv(PROJECT_ROOT / "experiments" / "rgssb_target_vs_global_featcons_comparison.csv")
    tdm_rows = read_csv(PROJECT_ROOT / "experiments" / "rgssb_tdm_gate_comparison.csv")
    rows = [
        {
            "Ablation": "Global feature consistency lambda 0.02",
            "Scope": "3 OTB sequences x 4 conditions",
            "Primary Comparison": "vs OSTrack baseline",
            "Average AUC Change": fmt_float(mean(numeric(r["lambda_0.02_vs_baseline_auc_change"]) for r in lambda_rows), signed=True),
            "Decision": "kept for Paper Freeze V1",
            "Evidence": "experiments/rgssb_featcons_lambda_sweep_comparison.csv",
        },
        {
            "Ablation": "Response consistency",
            "Scope": "3 OTB sequences x 4 conditions",
            "Primary Comparison": "vs feature-only lambda 0.02",
            "Average AUC Change": fmt_float(mean(numeric(r["response_consistency_gain_over_feature_only_auc"]) for r in response_rows), signed=True),
            "Decision": "rejected",
            "Evidence": "experiments/rgssb_featcons_lam002_vs_respcons_comparison.csv",
        },
        {
            "Ablation": "Target-region feature consistency",
            "Scope": "3 OTB sequences x 4 conditions",
            "Primary Comparison": "vs global feature consistency lambda 0.02",
            "Average AUC Change": fmt_float(mean(numeric(r["target_vs_global_auc_change"]) for r in target_rows), signed=True),
            "Decision": "rejected",
            "Evidence": "experiments/rgssb_target_vs_global_featcons_comparison.csv",
        },
        {
            "Ablation": "Target-vs-distractor margin",
            "Scope": "3 OTB sequences x 4 conditions",
            "Primary Comparison": "vs global feature consistency lambda 0.02",
            "Average AUC Change": fmt_float(mean(numeric(r["tdm_minus_global_auc_change"]) for r in tdm_rows), signed=True),
            "Decision": "rejected by gate",
            "Evidence": "experiments/rgssb_tdm_gate_comparison.csv",
        },
    ]
    fields = list(rows[0].keys())
    write_csv(TABLES_DIR / "paper_ablation_table.csv", rows, fields)
    write_latex_table(TABLES_DIR / "paper_ablation_table.tex", rows, fields, "Ablation summary for Paper Freeze V1.", "tab:ablations")
    return rows


def generate_efficiency_table() -> List[Dict[str, object]]:
    rows_in = read_csv(PROJECT_ROOT / "experiments" / "paper_efficiency_results.csv")
    complexity = {r["config"]: r for r in rows_in if r["measurement_type"] == "complexity"}
    aggregate = {r["config"]: r for r in rows_in if r["measurement_type"] == "controlled_runtime_aggregate"}
    rows: List[Dict[str, object]] = []
    labels = [
        ("OSTrack baseline", BASELINE_CONFIG),
        ("RG-SSB final", FINAL_CONFIG),
    ]
    for label, config in labels:
        c = complexity[config]
        a = aggregate[config]
        rows.append(
            {
                "Model": label,
                "GPU": a["gpu_name"],
                "Params": c["total_params"],
                "Trainable Params": c["trainable_params"],
                "Frozen Params": c["frozen_params"],
                "Init ms": fmt_float(a["initialization_ms"], 3),
                "Latency ms": fmt_float(a["mean_latency_ms"], 3),
                "FPS": fmt_float(a["fps"], 3),
                "Peak Alloc MB": fmt_float(a["peak_allocated_memory_mb"], 3),
                "Peak Reserved MB": fmt_float(a["peak_reserved_memory_mb"], 3),
                "FLOPs/MACs": c["flops_or_macs"],
            }
        )
    fields = list(rows[0].keys())
    write_csv(TABLES_DIR / "paper_efficiency_table.csv", rows, fields)
    write_latex_table(TABLES_DIR / "paper_efficiency_table.tex", rows, fields, "Controlled same-GPU efficiency comparison.", "tab:efficiency")
    return rows


def save_plot(fig, name: str) -> None:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    for ext in ["svg", "pdf", "png"]:
        kwargs = {"bbox_inches": "tight"}
        if ext == "png":
            kwargs["dpi"] = 300
        fig.savefig(FIGURES_DIR / f"{name}.{ext}", **kwargs)
    plt.close(fig)


def plot_bar(labels: List[str], values: List[float], title: str, ylabel: str, name: str) -> None:
    fig, ax = plt.subplots(figsize=(7, 4))
    colors = ["#2b6cb0" if v >= 0 else "#c53030" for v in values]
    ax.bar(labels, values, color=colors)
    ax.axhline(0.0, color="black", linewidth=0.9)
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.tick_params(axis="x", rotation=20)
    for idx, val in enumerate(values):
        ax.text(idx, val + (0.002 if val >= 0 else -0.002), f"{val:+.3f}", ha="center", va="bottom" if val >= 0 else "top")
    save_plot(fig, name)


def generate_figures(benchmark_rows, condition_rows, efficiency_rows, ablation_rows) -> List[str]:
    plot_bar(
        [r["Benchmark"] for r in benchmark_rows],
        [numeric(r["AUC Change"]) for r in benchmark_rows],
        "Average AUC Change by Benchmark",
        "AUC change (RG-SSB - OSTrack)",
        "benchmark_auc_change",
    )
    plot_bar(
        [r["Condition"] for r in condition_rows],
        [numeric(r["AUC Change"]) for r in condition_rows],
        "Average AUC Change by Condition",
        "AUC change (RG-SSB - OSTrack)",
        "condition_auc_change",
    )
    fig, ax = plt.subplots(figsize=(7, 4))
    labels = [r["Model"] for r in efficiency_rows]
    fps = [numeric(r["FPS"]) for r in efficiency_rows]
    latency = [numeric(r["Latency ms"]) for r in efficiency_rows]
    x = range(len(labels))
    ax.bar([i - 0.18 for i in x], fps, width=0.36, label="FPS", color="#2f855a")
    ax2 = ax.twinx()
    ax2.bar([i + 0.18 for i in x], latency, width=0.36, label="Latency ms", color="#805ad5")
    ax.set_xticks(list(x))
    ax.set_xticklabels(labels, rotation=15, ha="right")
    ax.set_ylabel("FPS")
    ax2.set_ylabel("Latency (ms)")
    ax.set_title("Controlled V100 Runtime")
    lines, line_labels = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines + lines2, line_labels + labels2, loc="upper right")
    save_plot(fig, "efficiency_comparison")
    plot_bar(
        [r["Ablation"].replace(" feature consistency", "\nfeat. cons.") for r in ablation_rows],
        [numeric(r["Average AUC Change"]) for r in ablation_rows],
        "Ablation Decisions",
        "Average AUC change",
        "ablation_decision",
    )
    drift_rows = read_csv(PROJECT_ROOT / "experiments" / "nfs_corrected_drift_onset_analysis.csv")
    counts = Counter(r["terminal_failure_mode"] for r in drift_rows)
    fig, ax = plt.subplots(figsize=(7, 4))
    labels = list(counts.keys())
    values = [counts[k] for k in labels]
    ax.bar(labels, values, color="#dd6b20")
    ax.set_title("Corrected NFS Failure Modes")
    ax.set_ylabel("Cases")
    ax.tick_params(axis="x", rotation=25)
    save_plot(fig, "nfs_failure_mode_distribution")
    return [str(p.relative_to(PROJECT_ROOT)) for p in sorted(FIGURES_DIR.glob("*"))]


def markdown_table(rows: Sequence[Dict[str, object]], columns: Sequence[str]) -> str:
    lines = ["|" + "|".join(columns) + "|", "|" + "|".join(["---"] * len(columns)) + "|"]
    for row in rows:
        lines.append("|" + "|".join(str(row.get(c, "")) for c in columns) + "|")
    return "\n".join(lines)


def generate_reports(benchmark_rows, condition_rows, ablation_rows, efficiency_rows, figures) -> None:
    safe_claims = [r for r in read_csv(PROJECT_ROOT / "experiments" / "paper_claim_traceability.csv") if r["status"] == "safe"]
    qualified_claims = [r for r in read_csv(PROJECT_ROOT / "experiments" / "paper_claim_traceability.csv") if r["status"] == "qualified"]
    unsupported_claims = [r for r in read_csv(PROJECT_ROOT / "experiments" / "paper_claim_traceability.csv") if r["status"] == "unsupported"]
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    IMPLEMENTATION_DIR.mkdir(parents=True, exist_ok=True)

    bench_md = markdown_table(benchmark_rows, list(benchmark_rows[0].keys()))
    cond_md = markdown_table(condition_rows, list(condition_rows[0].keys()))
    abl_md = markdown_table(ablation_rows, list(ablation_rows[0].keys()))
    eff_md = markdown_table(efficiency_rows, list(efficiency_rows[0].keys()))

    (REPORTS_DIR / "11_results_final.md").write_text(
        f"""# Final Results for Paper Freeze V1

## Benchmark Summary

{bench_md}

The frozen RG-SSB method improves the broader OTB subset by +0.033144 AUC and the expanded UAV123 subset by +0.017405 AUC. Corrected expanded NFS remains slightly negative at -0.009638 AUC. The mandatory cross-benchmark aggregate is +0.001478 AUC, so the result should be described as promising but not uniformly improved.

## Condition Summary

{cond_md}

## Efficiency Summary

{eff_md}

The runtime values are from a controlled same-GPU Tesla V100-PCIE-32GB comparison. Initialization and per-frame tracking latency are reported separately. FLOPs/MACs are unavailable and are not claimed.

## Ablation Summary

{abl_md}

TDM is a rejected negative ablation: it improves several local conditions but its Gaussian-noise regression dominates the aggregate gate outcome.
""",
        encoding="utf-8",
    )

    (REPORTS_DIR / "12_conclusion_future_work.md").write_text(
        """# Conclusion and Future Work

Paper Freeze V1 supports a cautious conclusion: adding RG-SSB and training the box head with global clean/degraded feature consistency can improve robustness on selected OTB and UAV123 subsets, while transfer to corrected NFS remains mixed. The method should not be described as state of the art or universally robust.

Future work should prioritize broader benchmark coverage, multiple degradation seeds, additional severities, and targeted analysis of persistent RG-SSB-specific target loss. Architecture changes such as degradation tokens, response fusion, memory modules, and template-guided scan mechanisms remain postponed for this paper version.
""",
        encoding="utf-8",
    )

    (REPORTS_DIR / "paper_draft_freeze_v1.md").write_text(
        f"""# Paper Draft Freeze V1

## Method

We study a restoration-guided state-space block integrated into OSTrack for degradation-robust RGB template-search tracking. The frozen method keeps the OSTrack backbone fixed and trains only `rgssb.*` and `box_head.*`. The selected training setup uses global clean/degraded feature consistency with weight 0.02. Response consistency, target-region feature consistency, and target-vs-distractor margin loss are disabled in the final method.

## Experiments

The baseline is `vitb_256_mae_ce_32x4_ep300`. The final method is `{FINAL_CONFIG}`. We evaluate clean, motion-blur, low-resolution, and Gaussian-noise conditions at medium severity with one degradation seed. NFS results use normalized aligned XYWH annotations; earlier XYXY-as-XYWH NFS metrics and qualitative overlays are superseded.

## Results

{bench_md}

{cond_md}

## Efficiency

{eff_md}

## Ablations

{abl_md}

## Discussion

The results are positive on OTB and UAV123, but corrected NFS is slightly negative. This indicates promising but non-uniform cross-benchmark robustness. The rejected TDM ablation confirms that directly modifying the response objective can introduce regressions, especially under Gaussian noise.

## Limitations

The evidence uses selected benchmark subsets, synthetic corruptions, one seed, medium severity, a frozen backbone, and LaSOT-only training. No state-of-the-art or universal robustness claim is supported.

## Conclusion

RG-SSB with global feature consistency is a defensible Paper Freeze V1 method, but broader evaluation is required before stronger claims.
""",
        encoding="utf-8",
    )

    (IMPLEMENTATION_DIR / "final_paper_asset_manifest.md").write_text(
        f"""# Final Paper Asset Manifest

## Tables

- `tables/paper_main_benchmark_table.csv`
- `tables/paper_main_benchmark_table.tex`
- `tables/paper_condition_table.csv`
- `tables/paper_condition_table.tex`
- `tables/paper_ablation_table.csv`
- `tables/paper_ablation_table.tex`
- `tables/paper_efficiency_table.csv`
- `tables/paper_efficiency_table.tex`

## Figures

{chr(10).join(f"- `{fig}`" for fig in figures)}

## Reports

- `reports/11_results_final.md`
- `reports/12_conclusion_future_work.md`
- `reports/paper_draft_freeze_v1.md`

## Authoritative Sources

- `experiments/paper_level_result_table_current.csv`
- `experiments/paper_level_benchmark_summary.csv`
- `experiments/paper_efficiency_results.csv`
- `experiments/rgssb_tdm_gate_comparison.csv`
- `experiments/nfs_corrected_drift_onset_analysis.csv`
- `implementation/nfs_result_recovery_manifest.md`

Previous invalid NFS XYXY-as-XYWH metrics and overlays are superseded and must not be used.
""",
        encoding="utf-8",
    )

    (IMPLEMENTATION_DIR / "final_reproducibility_checklist.md").write_text(
        """# Final Reproducibility Checklist

- Use config `vitb_256_mae_ce_32x4_ep300_rgssb_head_train_lasot_degraded_hpc_featcons_lam002`.
- Use normalized aligned XYWH NFS annotations for every NFS result.
- Do not use archived invalid NFS rows except as provenance.
- Do not mix historical timing files with controlled V100 efficiency measurements.
- Report FLOPs/MACs as unavailable.
- Keep TDM disabled and rejected.
- Do not commit checkpoints, generated tracker outputs, degraded datasets, or external/OSTrack outputs.
- Verify final assets with `python3 scripts/verify_final_paper_package.py`.
""",
        encoding="utf-8",
    )

    (IMPLEMENTATION_DIR / "final_claim_audit.md").write_text(
        f"""# Final Claim Audit

## Safe Claims

{markdown_table(safe_claims, ['claim_id', 'claim_text', 'evidence_file', 'evidence_scope', 'caveat'])}

## Qualified Claims

{markdown_table(qualified_claims, ['claim_id', 'claim_text', 'evidence_file', 'evidence_scope', 'caveat'])}

## Unsupported Claims

{markdown_table(unsupported_claims, ['claim_id', 'claim_text', 'caveat'])}

No unsupported claim should be promoted into the manuscript. The rejected TDM ablation is not the final method. Old invalid NFS values are superseded.
""",
        encoding="utf-8",
    )


def main() -> int:
    TABLES_DIR.mkdir(exist_ok=True)
    benchmark_rows = generate_main_benchmark_table()
    condition_rows = generate_condition_table()
    ablation_rows = generate_ablation_table()
    efficiency_rows = generate_efficiency_table()
    figures = generate_figures(benchmark_rows, condition_rows, efficiency_rows, ablation_rows)
    generate_reports(benchmark_rows, condition_rows, ablation_rows, efficiency_rows, figures)
    print("Generated final paper tables, figures, and report drafts.")
    for fig in figures:
        print(fig)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
