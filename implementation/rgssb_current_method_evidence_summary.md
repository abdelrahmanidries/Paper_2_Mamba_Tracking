# RG-SSB Current Method Evidence Summary

## 1. Current best setup

OSTrack + RG-SSB + box_head, frozen backbone, global clean-degraded feature consistency lambda `0.02`, response consistency disabled, target-region consistency disabled. HPC config: `vitb_256_mae_ce_32x4_ep300_rgssb_head_train_lasot_degraded_hpc_featcons_lam002`. NFS values use normalized aligned XYWH annotations.

## 2. What worked

OTB remains positive, UAV123 remains positive/mixed, and the NFS pipeline has been corrected and rerun using canonical XYWH annotations.

## 3. What did not work

Previous NFS tracking used invalid XYXY boxes as XYWH; old NFS metrics and overlays are superseded.

## 4. Evidence table

| setup | scope | pairs | AUC change | decision |
| --- | --- | --- | --- | --- |
| global feature consistency lambda 0.02 | current best method, corrected NFS included | 244 | +0.006572 | keep current best setup |
| HPC lambda 0.02 broader OTB | OTB broader | 52 | +0.033144 | valid; unchanged |
| HPC lambda 0.02 expanded UAV123 | UAV123 expanded | 64 | +0.017405 | valid; unchanged |
| HPC lambda 0.02 corrected expanded NFS | NFS expanded32 corrected | 128 | -0.009638 | inspect corrected failures |

## 5. Cross-benchmark status

| benchmark | pairs | AUC change | conclusion |
| --- | --- | --- | --- |
| OTB | 52 | +0.033144 | RG-SSB improves clearly on average |
| UAV123 | 64 | +0.017405 | RG-SSB improves slightly / near neutral |
| NFS | 128 | -0.009638 | Mixed / negative average |

## 6. Current risk

Subset benchmarks, synthetic degradations, one seed, frozen backbone, and LaSOT-only training remain risks.

## 7. Recommendation

Keep current best setup and inspect corrected NFS failures before architecture changes.

## 8. Next action

Run corrected qualitative NFS failure inspection.
