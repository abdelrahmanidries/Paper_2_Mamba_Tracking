# IEEE Transactions Assembly Manifest

## Manuscript Root

Root:

```text
paper/ieee_transactions/
```

Class:

```tex
\documentclass[journal]{IEEEtran}
```

The final source uses `IEEEtran` with local section, table, figure, and BibTeX files. The clean submission package also includes `IEEEtran.cls` and `IEEEtran.bst` for self-contained compilation.

## Integrated Source Files

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
- `figures/benchmark_auc_change.pdf`
- `figures/condition_auc_change.pdf`
- `figures/efficiency_comparison.pdf`
- `figures/ablation_decision.pdf`
- `figures/nfs_failure_mode_distribution.pdf`

## Citation Status

Resolved entries:

- OSTrack: `ye2022ostrack`
- LaSOT: `fan2019lasot`
- OTB: `wu2013otb`
- UAV123: `mueller2016uav123`
- NFS: `galoogahi2017nfs`
- MambaIR: `guo2024mambair`
- MambaIRv2: `guo2025mambairv2`
- InvTrack local evidence: `invtrack_local`

Unresolved citation placeholders: 0.

## Author Status

Candidate author names, order, affiliations, corresponding-author name, and funding text were copied from `papers/InvTrack.pdf`. `main.tex` retains an explicit `[AUTHOR INFORMATION REQUIRES CONFIRMATION]` note because ORCIDs, exact corresponding-author email punctuation, biographies, and final manuscript-author confirmation remain manual tasks.

## Build Outputs

- Main PDF: `paper/ieee_transactions/main.pdf`
- Main log: `paper/ieee_transactions/main.log`
- Page count: 5
- Rendered page audit: `paper/ieee_transactions/rendered_pages/`
- Contact sheet: `paper/ieee_transactions/rendered_pages/contact_sheet.png`

Build command executed:

```bash
cd paper/ieee_transactions
latexmk -C
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

Final log scan found no undefined citations, undefined references, LaTeX errors, duplicate-label diagnostics, or overfull boxes.

## Submission Package

Source directory:

```text
paper/ieee_transactions/submission/
```

Source ZIP:

```text
paper/ieee_transactions/Paper_2_IEEE_Transactions_source.zip
```

ZIP size: 149,690 bytes.

The ZIP contains 23 source files and excludes auxiliary files, logs, rendered pages, datasets, checkpoints, experiment outputs, and Git metadata. The submission directory was compiled independently and then cleaned back to source-only contents.

## Verification

Commands passed:

```bash
python3 -m py_compile scripts/verify_ieee_transaction_manuscript.py scripts/verify_ieee_submission_package.py
python3 scripts/verify_ieee_transaction_manuscript.py
python3 scripts/verify_ieee_submission_package.py
```

Claim anchors verified:

- OTB `+0.033144`
- UAV123 `+0.017405`
- corrected NFS `-0.009638`
- combined `+0.001478`
- baseline parameters `92,518,533`
- final parameters `94,598,469`
- baseline FPS `93.247`
- final FPS `86.766`
- hardware `Tesla V100-PCIE-32GB`

Unsupported C13/C14 claims remain absent. TDM appears only as a rejected negative ablation. FLOPs/MACs remain unavailable and are not reported as measured.
