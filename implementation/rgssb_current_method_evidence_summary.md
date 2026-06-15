# RG-SSB Current Method Evidence Summary

Inputs:

- `experiments/baseline_results.csv`
- `experiments/rgssb_hpc_broader_otb_comparison.csv`
- `experiments/rgssb_hpc_uav123_comparison.csv`
- `experiments/rgssb_hpc_nfs_comparison.csv`
- `experiments/rgssb_hpc_failure_focused_uav_nfs_comparison.csv`
- `experiments/rgssb_target_vs_global_featcons_comparison.csv`
- `implementation/rgssb_hpc_broader_otb_result_analysis.md`
- `implementation/rgssb_hpc_uav123_result_analysis.md`
- `implementation/rgssb_hpc_nfs_result_analysis.md`
- `implementation/rgssb_hpc_failure_focused_uav_nfs_result_analysis.md`
- `implementation/rgssb_target_vs_global_featcons_result_analysis.md`
- `implementation/rgssb_featcons_lambda_sweep_result_analysis.md`
- `implementation/rgssb_featcons_lam002_vs_respcons_result_analysis.md`

## 1. Current best setup

Current best setup: **RG-SSB + box head with frozen backbone and global clean-degraded feature consistency lambda `0.02`, response consistency disabled, target-region consistency disabled**.

Current best HPC checkpoint/config: `vitb_256_mae_ce_32x4_ep300_rgssb_head_train_lasot_degraded_hpc_featcons_lam002`.

- Trainable parameters are `rgssb.*` and `box_head.*`.
- Backbone remains frozen.
- Training data is LaSOT with synthetic search-only degradation.
- Global feature consistency uses clean/degraded post-RGSSB search-token alignment.
- Response consistency and target-region consistency are not part of the current best setup.

## 2. What worked

- RG-SSB integration works in OSTrack without adding new architecture beyond the RG-SSB block already under test.
- RG-SSB + head training works and checkpoint loading works with the expected newly initialized `rgssb.*` parameters.
- Evaluation automation works through the OTB/UAV123/NFS suite scripts and experiment-cycle runner.
- The broader OTB result is positive: average AUC change `+0.033144`.
- Expanded UAV123 is positive/mixed: average AUC change `+0.017405`.
- NFS remains mixed/slightly negative: selected NFS `-0.002660`, expanded NFS `-0.014195`.
- Lambda tuning worked locally: global feature consistency lambda `0.02` was best among `0.02`, `0.05`, and `0.10`.

## 3. What did not work

- RG-SSB-only training was insufficient in partial local evidence.
- Response consistency hurt overall versus feature-only lambda `0.02` by `-0.019360` AUC on the local 12-pair comparison.
- Target-region feature consistency hurt relative to global lambda `0.02` by `-0.023555` AUC on the local 12-pair comparison.
- Balanced clean/degraded 3000-sample training did not beat fully degraded 3000-sample training.
- UAV123/NFS transfer is not fully stable; expanded UAV123 improved, but expanded NFS worsened.

## 4. Evidence table

| setup | benchmark/scope | average AUC change vs baseline | conclusion | decision |
| --- | --- | ---: | --- | --- |
| local RG-SSB-only smoke test | partial local OTB/debug rows | -0.004832 | RG-SSB-only training was insufficient in partial local evidence. | do not use RG-SSB-only as current setup |
| RG-SSB + head 1000 local | Car1/David2/Coke x 4 local | +0.020811 | RG-SSB + head was viable and positive locally. | continue with RG-SSB + head, scale/tune objective |
| RG-SSB + head 3000 local | Car1/David2/Coke x 4 local | +0.010857 | Fully degraded 3000 local setup was positive but not best. | use as baseline for objective refinements |
| balanced 3000 local | Car1/David2/Coke x 4 local | +0.002874 | Balanced clean/degraded training did not beat fully degraded 3000. | do not prioritize balanced training |
| global feature consistency lambda 0.05 | Car1/David2/Coke x 4 local | +0.004981 | Original global feature consistency helped only modestly. | superseded by lambda 0.02 |
| global feature consistency lambda 0.02 | Car1/David2/Coke x 4 local | +0.023480 | Best local feature-consistency lambda. | keep as current objective |
| global feature consistency lambda 0.10 | Car1/David2/Coke x 4 local | +0.012359 | Lambda 0.10 was positive but below lambda 0.02 overall. | do not use as current setup |
| response consistency | Car1/David2/Coke x 4 local | +0.004119 | Response consistency hurt overall relative to feature-only lambda 0.02. | drop response consistency |
| target-region feature consistency | Car1/David2/Coke x 4 local | -0.000075 | Target-region consistency hurt relative to global lambda 0.02. | do not replace global consistency |
| HPC lambda 0.02 broader OTB | 13 OTB sequences x 4 conditions | +0.033144 | Broader OTB result is clearly positive. | keep current HPC setup as best evidence |
| HPC lambda 0.02 selected UAV123 | 8 UAV123 sequences x 4 conditions | -0.005511 | Selected UAV123 was mixed/slightly negative. | do not claim stable UAV transfer from selected subset |
| HPC lambda 0.02 selected NFS | 8 NFS sequences x 4 conditions | -0.002660 | Selected NFS was mixed/slightly negative. | inspect/expand before claims |
| HPC lambda 0.02 expanded UAV123/NFS | expanded UAV123+NFS failure-focused subsets | +0.001605 | Expanded UAV123 was positive, expanded NFS was negative, combined near neutral. | keep setup but require broader evidence |

## 5. Cross-benchmark status

- Broader OTB: `+0.033144` average AUC change across 52 sequence-condition pairs.
- Selected UAV123: `-0.005511` average AUC change across 32 pairs.
- Expanded UAV123: `+0.017405` average AUC change across 64 pairs.
- Selected NFS: `-0.002660` average AUC change across 32 pairs.
- Expanded NFS: `-0.014195` average AUC change across 64 pairs.
- Expanded UAV123+NFS combined: `+0.001605` average AUC change across 128 pairs.

Overall interpretation: the method has a credible positive signal on OTB and a mixed transfer signal on UAV123/NFS. The current evidence supports paper-level planning and broader evaluation, not final paper claims yet.

## 6. Current risk

- Benchmarks are still limited and use selected sequence subsets for UAV123/NFS.
- Degradation evaluation uses one seed and medium severity for synthetic corruptions.
- Training remains LaSOT-only, so UAV123/NFS domain shift is unresolved.
- The backbone is frozen, which limits adaptation capacity.
- The degradation protocol is synthetic and may not cover real-world corruption diversity.
- Expanded NFS is negative, so cross-benchmark robustness is not stable enough for final claims.
- Current results are local/HPC proof-of-concept evidence, not final paper-scale evidence.

## 7. Recommendation

- Keep the current best setup: RG-SSB + head with frozen backbone and global feature consistency lambda `0.02`.
- Stop adding architecture modules for now.
- Do not keep response consistency or target-region feature consistency as the main setup based on current parsed results.
- Prepare the paper-level experiment plan and result table structure.
- Evaluate more complete benchmarks if time/resources allow.
- Write the method section carefully as proof-of-concept until full benchmark results are available.

## 8. Next action

Immediate next action: **Create the paper-level experiment plan and result table structure for the current best RG-SSB + head global feature consistency lambda `0.02` setup.**

## Verification

- Parsed existing CSV files with Python.
- Created `experiments/rgssb_current_method_evidence_summary.csv`.
- Created `implementation/rgssb_current_method_evidence_summary.md`.
- Did not run OSTrack, training, or evaluation.
- Did not modify datasets or `external/OSTrack`.

Uncertain fields:

- Early RG-SSB-only smoke-test evidence has partial row coverage only.
- UAV123/NFS expanded subsets are not full benchmark evaluations.
- Paper-level claims require broader benchmark coverage and repeated degradation seeds if feasible.
