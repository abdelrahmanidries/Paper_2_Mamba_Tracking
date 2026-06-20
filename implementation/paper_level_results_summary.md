# Paper-Level Results Summary

### Executive summary

Regenerated after the normalized aligned XYWH NFS fix. OTB and UAV123 values are unchanged. NFS values are corrected from `baseline_results.csv`; invalid historical rows are archived in `experiments/invalid_nfs_rows_before_xyxy_fix.csv`. Current paper-level table has `244` comparison pairs and overall average AUC change `+0.006572`.

### Benchmark table

| benchmark | sequences | pairs | baseline AUC | RG-SSB AUC | AUC change | conclusion |
| --- | --- | --- | --- | --- | --- | --- |
| OTB | 13 | 52 | 0.646964 | 0.680108 | +0.033144 | RG-SSB improves clearly on average |
| UAV123 | 16 | 64 | 0.660183 | 0.677587 | +0.017405 | RG-SSB improves slightly / near neutral |
| NFS | 32 | 128 | 0.681149 | 0.671511 | -0.009638 | Mixed / negative average |

### Condition table

| condition | baseline AUC | RG-SSB AUC | AUC change | Precision change | center-error change | gains | neutral | drops |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| clean | 0.685280 | 0.690648 | +0.005368 | +0.015220 | +2.558046 | 9 | 45 | 7 |
| motion_blur_medium | 0.643687 | 0.663299 | +0.019612 | +0.029967 | -7.502857 | 18 | 35 | 8 |
| low_resolution_medium | 0.672450 | 0.664175 | -0.008275 | -0.003989 | +6.769353 | 6 | 43 | 12 |
| gaussian_noise_medium | 0.672042 | 0.681627 | +0.009585 | +0.018540 | -0.342091 | 10 | 44 | 7 |

### Key positive evidence

OTB remains positive; UAV123 remains positive/mixed.

### Key limitations

Corrected NFS is mixed/slightly negative; benchmark coverage remains subset-based with one degradation seed.

### Safe wording for paper draft

The current RG-SSB + head setup shows promising OTB robustness and mixed cross-benchmark transfer under corrected normalized-NFS evaluation.

### Unsafe wording to avoid

Do not claim state-of-the-art, universal robustness, or final superiority.

### Missing results

Corrected NFS qualitative inspection, more seeds/severities, full benchmark coverage, and runtime reporting.

### Recommended immediate next run

Corrected NFS qualitative failure inspection.
