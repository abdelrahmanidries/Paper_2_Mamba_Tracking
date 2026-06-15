# Paper-Level Results Summary

Inputs:

- `experiments/baseline_results.csv`
- `experiments/paper_level_result_table_template.csv`
- `implementation/paper_level_experiment_plan.md`
- `implementation/paper_level_risk_and_claims.md`
- `implementation/rgssb_current_method_evidence_summary.md`
- `implementation/rgssb_hpc_broader_otb_result_analysis.md`
- `implementation/rgssb_hpc_uav123_result_analysis.md`
- `implementation/rgssb_hpc_nfs_result_analysis.md`
- `implementation/rgssb_hpc_failure_focused_uav_nfs_result_analysis.md`

### Executive summary

The current best RG-SSB method is compared against the original OSTrack baseline across `180` available sequence-condition pairs from broader OTB, expanded UAV123, and expanded NFS. Overall average AUC change is `+0.010716`. This is positive but small, with clear OTB gains and mixed UAV123/NFS transfer.
NaN center-error rows preserved in the detailed table: `40`. NaN center-error pairs ignored in averages: `20`.

### Benchmark table

| benchmark | sequences | conditions | pairs | baseline AUC | RG-SSB AUC | AUC change | Precision@20 change | center-error change | gains | neutral | drops | conclusion |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| OTB | 13 | 4 | 52 | 0.646964 | 0.680108 | +0.033144 | +0.050250 | -4.563202 | 16 | 31 | 5 | RG-SSB improves clearly on average |
| UAV123 | 16 | 4 | 64 | 0.660183 | 0.677587 | +0.017405 | +0.029983 | -3.500185 | 9 | 49 | 6 | RG-SSB improves slightly / near neutral |
| NFS | 16 | 4 | 64 | 0.325497 | 0.311302 | -0.014195 | -0.000662 | +5.228074 | 14 | 30 | 20 | Mixed / near neutral |

### Condition table

| condition | baseline AUC | RG-SSB AUC | AUC change | Precision@20 change | center-error change | conclusion |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| clean | 0.556364 | 0.567849 | +0.011485 | +0.017865 | -3.847199 | RG-SSB improves slightly / near neutral |
| motion_blur_medium | 0.506069 | 0.524283 | +0.018214 | +0.033784 | -4.279282 | RG-SSB improves slightly / near neutral |
| low_resolution_medium | 0.536012 | 0.538672 | +0.002660 | +0.018408 | +1.385267 | RG-SSB improves slightly / near neutral |
| gaussian_noise_medium | 0.551014 | 0.561520 | +0.010506 | +0.029710 | +5.323765 | RG-SSB improves slightly / near neutral |

### Key positive evidence

- `OTB` is positive on average: AUC change `+0.033144`.
- `UAV123` is positive on average: AUC change `+0.017405`.
- `clean` is positive across benchmarks: AUC change `+0.011485`.
- `motion_blur_medium` is positive across benchmarks: AUC change `+0.018214`.
- `low_resolution_medium` is positive across benchmarks: AUC change `+0.002660`.
- `gaussian_noise_medium` is positive across benchmarks: AUC change `+0.010506`.

### Key limitations

- UAV123/NFS transfer remains mixed; NFS is negative on the expanded table.
- Degradations are synthetic and currently use one seed per degraded condition.
- Sequences are selected/expanded subsets, not necessarily full benchmark coverage.
- The backbone is frozen, which limits adaptation capacity.
- Training is LaSOT-only, so domain shift to UAV123/NFS remains unresolved.
- FPS/runtime and memory results are not yet complete in the paper-level table.

### Safe wording for paper draft

- The current RG-SSB + head setup shows promising robustness potential on broader OTB.
- Cross-benchmark results are mixed, motivating broader evaluation on UAV123 and NFS.
- The method is evaluated as a proof-of-concept degradation-aware adaptation of OSTrack with frozen backbone.
- Global clean-degraded feature consistency with lambda `0.02` is the strongest training objective tested so far.

### Unsafe wording to avoid

- Do not claim state-of-the-art performance.
- Do not claim general robustness across all benchmarks.
- Do not claim universal degradation robustness.
- Do not claim final method superiority.
- Do not claim stable UAV123/NFS improvement without full benchmark evidence.

### Missing results

- full OTB or larger OTB subset
- full UAV123
- more NFS sequences
- multiple degradation seeds
- multiple severities
- FPS/inference cost table if incomplete

### Recommended immediate next run

Run the next NFS expansion or full-NFS baseline/current-best evaluation first, because NFS is the weakest benchmark in the current table.

## Verification

- Parsed `experiments/baseline_results.csv` with Python.
- Created `experiments/paper_level_result_table_current.csv`.
- Created `experiments/paper_level_benchmark_summary.csv`.
- Created `implementation/paper_level_results_summary.md`.
- Did not run OSTrack, training, or evaluation.
- Did not modify datasets or `external/OSTrack`.
