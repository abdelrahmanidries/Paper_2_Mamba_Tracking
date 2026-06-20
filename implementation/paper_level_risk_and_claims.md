# Paper-Level Risk and Claims

## Safe Claims Now

- RG-SSB is integrated and trainable inside OSTrack.
- OTB evidence remains positive.
- UAV123 evidence remains unchanged.
- NFS evidence is corrected using normalized aligned XYWH annotations from `/speed-scratch/a_idrais/nfs_ostrack_normalized`.
- Cross-benchmark transfer remains mixed.

## Unsafe Claims Now

Do not claim state-of-the-art performance, universal degradation robustness, general benchmark superiority, or stable NFS improvement without corrected qualitative inspection and broader coverage.

## Reviewer Risks

Selected subsets, synthetic degradation, one seed, frozen backbone, LaSOT-only training, and the need to document the corrected NFS protocol.

## Evidence Needed for Stronger Claims

Fuller benchmark coverage, multiple seeds/severities, runtime reporting, corrected qualitative failure inspection, and reproducible normalized NFS protocol.

## Recommended Claim Wording

```text
The current RG-SSB + head setup shows promising OTB robustness and mixed cross-benchmark transfer under a corrected NFS evaluation protocol.
```

## Current Claim Boundary

This supports proof-of-concept robustness evidence, not final benchmark superiority.
