# IEEE Transactions Assembly Manifest

## Template Discovery

Search locations:

- `/home/abdel/Desktop`
- `/home/abdel/Documents`
- sibling directories of `/home/abdel/Desktop/Paper_2_Mamba_Tracking`

Result: no local InvTrack IEEEtran manuscript root, `main.tex`, `bare_jrnl.tex`, `bare_jrnl_compsoc.tex`, or `IEEEtran.cls` was found. Only InvTrack code/training directories and the local `papers/InvTrack.pdf` evidence file were found.

Selected InvTrack template root: not available.

Main TeX file: not available.

IEEEtran class/options used in assembled package:

```tex
\documentclass[journal]{IEEEtran}
```

The package relies on a TeX installation that provides IEEEtran. No InvTrack prose, figures, results, citations, or method claims were copied.

## Created Package

Root:

```text
paper/ieee_transactions/
```

Files:

- `main.tex`
- `references.bib`
- `sections/abstract.tex`
- `sections/introduction.tex`
- `sections/related_work.tex`
- `sections/method.tex`
- `sections/experiments.tex`
- `sections/results.tex`
- `sections/discussion.tex`
- `sections/conclusion.tex`
- `sections/appendix.tex`
- `tables/paper_main_benchmark_table.tex`
- `tables/paper_condition_table.tex`
- `tables/paper_ablation_table.tex`
- `tables/paper_efficiency_table.tex`
- `figures/*.pdf`
- `figures/*.png`
- `figures/*.svg`
- `latexmkrc`
- `Makefile`
- `README.md`
- `AUTHOR_INFORMATION_REVIEW.md`
- `CITATION_RESOLUTION_REPORT.md`

## Citation Resolution

Resolved locally:

- MambaIR from `paper_cards/2024_ECCV_MambaIR.md`.
- MambaIRv2 from `paper_cards/2025_CVPR_MambaIRv2.md`.
- InvTrack as local unpublished evidence because the local card reports title/authors but not year/venue.

Unresolved and visibly marked:

- OSTrack.
- LaSOT.
- OTB.
- UAV123.
- NFS.

## Figures and Tables

Integrated figures:

- `benchmark_auc_change.pdf`
- `condition_auc_change.pdf`
- `efficiency_comparison.pdf`
- `ablation_decision.pdf`
- `nfs_failure_mode_distribution.pdf`

Integrated tables:

- Main benchmark summary.
- Condition-level summary.
- Ablation summary.
- Efficiency summary.

No qualitative NFS panel was included because no corrected qualitative panel with confirmed aligned XYWH provenance was selected as a verified paper asset.

## Build Status

LaTeX tooling status in Codex environment:

- `latexmk`: unavailable.
- `pdflatex`: unavailable.
- `kpsewhich`: unavailable.

Therefore `main.pdf` could not be generated in this environment. The package includes `latexmkrc` and `Makefile` for a normal TeX installation.

Expected build command:

```bash
cd paper/ieee_transactions
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

## Human Confirmation Required

- Author names and order.
- Affiliations.
- ORCIDs.
- Corresponding author.
- Funding and acknowledgments.
- Final bibliography entries for unresolved citation markers.
- IEEE biography requirements.
