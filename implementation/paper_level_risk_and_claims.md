# Paper-Level Risk and Claims

## Safe Claims Now

The following claims are currently safe if worded carefully:

- The implementation pipeline works: training, checkpointing, evaluation, CSV logging, and comparison reporting are operational.
- RG-SSB can be integrated into OSTrack and trained with the box head while keeping the backbone frozen.
- Global clean-degraded feature consistency with lambda `0.02` is the strongest local training objective tested so far.
- Broader OTB results show positive robustness potential for the current RG-SSB + head setup.
- Cross-benchmark transfer remains mixed, especially on NFS.
- Response consistency and target-region feature consistency did not improve the current best local setup.

## Unsafe Claims Now

Do not claim:

- state-of-the-art performance;
- general robustness across all benchmarks;
- universal degradation robustness;
- final method superiority;
- that RG-SSB consistently improves UAV123 or NFS;
- that target-region consistency solves cross-benchmark transfer;
- that the method is ready for final paper claims without broader benchmark coverage.

## Reviewer Risks

- Selected sequences: UAV123 and NFS evidence still uses selected/expanded subsets, not necessarily full benchmarks.
- Synthetic degradations: current corruptions may not represent real degraded videos.
- Single seed: degraded conditions currently use one seed, usually `42`.
- Limited severities: current tables mostly use medium severity.
- Limited benchmarks: OTB is positive, but UAV123/NFS remain mixed.
- Frozen backbone: reviewers may ask whether full fine-tuning or partial backbone adaptation is needed.
- LaSOT-only training: domain shift to UAV123 and NFS is unresolved.
- NFS sampling: NFS annotation/frame alignment required special handling and should be clearly documented.
- Method scope: broader architecture ideas in earlier method notes are not implemented in the current best setup.

## Evidence Needed for Stronger Claims

Before stronger claims, collect:

- Full or clearly justified benchmark subsets for OTB, UAV123, and NFS.
- Baseline and current method rows for every benchmark/condition pair.
- Multiple degradation seeds if compute allows.
- Severity sweep for at least one benchmark.
- Runtime/FPS and parameter-count comparison.
- Clear failure-case table for sequences where RG-SSB drops.
- Reproducible config/checkpoint references.
- Optional comparison to additional trackers only after the OSTrack baseline comparison is complete.

## Recommended Claim Wording

Use:

```text
The current RG-SSB + head setup shows promising degradation-robust tracking behavior on broader OTB and mixed transfer on UAV123/NFS, motivating broader paper-level evaluation.
```

Avoid:

```text
The proposed method achieves robust tracking across benchmarks.
```

## Current Claim Boundary

Current evidence supports a method-development narrative and a proof-of-concept robustness claim. It does not yet support a final benchmark superiority claim.

