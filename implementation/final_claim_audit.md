# Final Claim Audit

## Safe Claims

|claim_id|claim_text|evidence_file|evidence_scope|caveat|
|---|---|---|---|---|
|C01|The current best setup is OSTrack with RG-SSB and box_head trainable, frozen backbone, global clean/degraded feature consistency at lambda 0.02, response consistency disabled, and target-region consistency disabled.|implementation/rgssb_current_method_evidence_summary.md|method/config provenance|Requires external OSTrack patch/config to reproduce.|
|C02|The current method improves average AUC on the broader 13-sequence OTB subset.|experiments/rgssb_hpc_broader_otb_comparison.csv|13 sequences x 4 conditions = 52 pairs|Subset evidence, not full OTB or state-of-the-art.|
|C03|The current method improves average AUC on the expanded 16-sequence UAV123 subset.|experiments/paper_level_benchmark_summary.csv|16 sequences x 4 conditions = 64 pairs|Subset evidence with one degradation seed and medium severity.|
|C04|The current method is slightly negative on corrected expanded 32-sequence NFS.|experiments/rgssb_hpc_nfs_expanded32_comparison.csv|32 sequences x 4 conditions = 128 pairs|NFS remains mixed/slightly negative after normalized aligned XYWH correction.|
|C05|The corrected cross-benchmark failure-inspection aggregate is near-neutral positive.|experiments/rgssb_hpc_cross_benchmark_failure_inspection.csv|212 OTB/UAV123/NFS failure-inspection pairs|This is not the same scope as the 244-pair paper-level table.|
|C07|Corrected NFS cheetah low-resolution AUC is near-neutral rather than the old large drop.|experiments/rgssb_hpc_nfs_expanded32_comparison.csv|nfs_cheetah low_resolution medium seed 42|The old invalid NFS XYXY-as-XYWH metrics are superseded.|
|C08|Historical invalid NFS rows were archived before correction.|experiments/invalid_nfs_rows_before_xyxy_fix.csv|128 baseline + 128 RG-SSB rows|Archive is provenance only and must not be used for current metrics.|

## Qualified Claims

|claim_id|claim_text|evidence_file|evidence_scope|caveat|
|---|---|---|---|---|
|C06|The broader paper-level table across OTB, expanded UAV123, and corrected expanded NFS is positive on average.|experiments/paper_level_result_table_current.csv|244 pairs|Average is small and includes a negative NFS component.|
|C09|Corrected NFS drift analysis identifies persistent RG-SSB-specific target loss as the largest terminal-failure category.|experiments/nfs_corrected_drift_onset_analysis.csv|top corrected NFS drops|Qualitative/per-frame failure subset, not benchmark-wide frequency.|
|C10|Corrected NFS drift analysis includes sudden center jump failures.|experiments/nfs_corrected_drift_onset_analysis.csv|top corrected NFS drops|Qualitative/per-frame failure subset.|
|C11|Response consistency is not retained in the current best method.|implementation/rgssb_featcons_lam002_vs_respcons_result_analysis.md|local proof-of-concept subset|Local small-scale evidence only.|
|C12|Target-region feature consistency is not retained in the current best method.|implementation/rgssb_target_vs_global_featcons_result_analysis.md|local proof-of-concept subset|Local small-scale evidence only.|

## Unsupported Claims

|claim_id|claim_text|caveat|
|---|---|---|
|C13|The current evidence supports state-of-the-art robustness claims.|No SOTA comparison table or full benchmark coverage.|
|C14|The current evidence proves universal degradation robustness.|Only selected synthetic degradations at medium severity and one seed.|

No unsupported claim should be promoted into the manuscript. The rejected TDM ablation is not the final method. Old invalid NFS values are superseded.
