# Paper Draft Freeze V1, Polished Editorial Pass

## Title

Restoration-Guided State-Space Adaptation for Degradation-Robust RGB Object Tracking

## Abstract

Visual object trackers often degrade under image-quality corruptions such as blur, low resolution, and sensor noise. This paper studies a conservative restoration-guided state-space adaptation of OSTrack for RGB template-search tracking [CITATION NEEDED]. The final Paper Freeze V1 method inserts an RG-SSB module into OSTrack, keeps the backbone frozen, and trains only `rgssb.*` and `box_head.*` using degradation-aware LaSOT training with global clean/degraded feature consistency at weight 0.02 [CITATION NEEDED]. Response consistency, target-region feature consistency, and target-vs-distractor margin loss are not retained in the final method. On selected benchmark subsets, the method improves average AUC on broader OTB by +0.033144 and expanded UAV123 by +0.017405, while corrected expanded NFS is slightly negative at -0.009638. The cross-benchmark aggregate is near-neutral positive at +0.001478. These results support a cautious conclusion: restoration-guided feature adaptation shows robustness potential, but it does not yet establish state-of-the-art or universal degradation robustness.

## 1. Introduction

RGB object tracking must maintain target localization under appearance change, motion, and image-quality degradation. Synthetic and real corruptions such as blur, low resolution, and Gaussian noise can weaken template-search matching, response-map localization, and bounding-box regression. Recent Mamba and state-space models have been explored in vision and tracking, while restoration-oriented Mamba variants have shown promise for image restoration [CITATION NEEDED]. This work investigates a narrower question: whether a restoration-guided state-space block can improve target-discriminative tracking features without changing the overall OSTrack tracking architecture.

The goal is not to claim that Mamba is new to tracking, nor that degradation-robust tracking is unsolved. Instead, the paper evaluates a specific missing intersection: restoration-oriented state-space feature adaptation inside RGB template-search tracking. The final method remains intentionally conservative. It keeps the OSTrack backbone frozen, trains RG-SSB and the box head, and uses global clean/degraded feature consistency. This makes the empirical question testable while reducing the risk of conflating the proposed module with broad architecture changes.

## 2. Method

The final method uses OSTrack as the base tracker [CITATION NEEDED]. Given a template image and a search image, OSTrack extracts transformer features and predicts a response map and bounding box. Paper Freeze V1 adds a Restoration-Guided State-Space Block (RG-SSB) after the backbone search features and before the tracking head. The module is designed to adjust tracking features under degradation rather than reconstruct RGB images.

The frozen method is:

- Base tracker: OSTrack.
- Added module: RG-SSB.
- Frozen parameters: backbone.
- Trainable parameters: `rgssb.*` and `box_head.*`.
- Training data: degradation-aware LaSOT [CITATION NEEDED].
- Feature consistency: global clean/degraded feature consistency.
- Feature-consistency weight: 0.02.
- Disabled losses/modules: response consistency, target-region feature consistency, target-vs-distractor margin loss.
- Final config: `vitb_256_mae_ce_32x4_ep300_rgssb_head_train_lasot_degraded_hpc_featcons_lam002`.

The training objective combines the degraded-branch tracking loss with global clean/degraded feature consistency:

```text
L = L_track(degraded) + 0.02 * L_feature(clean, degraded)
```

The clean feature branch is detached for the feature-consistency term. The final model does not use response consistency, target-region consistency, degradation tokens, memory update, response fusion, or template-guided scan. Those components remain outside Paper Freeze V1.

## 3. Experimental Protocol

The baseline is original OSTrack config `vitb_256_mae_ce_32x4_ep300`. The final method is compared against this baseline under four conditions:

- clean
- motion blur, medium severity, seed 42
- low resolution, medium severity, seed 42
- Gaussian noise, medium severity, seed 42

The evaluated subsets are broader OTB, expanded UAV123, and corrected expanded NFS. The paper reports Success AUC, Precision@20, and mean center error. Changes are computed as RG-SSB minus the OSTrack baseline for the same sequence and condition.

The NFS evaluation required a correction before any NFS results could be used. Raw NFS annotations were confirmed to contain `[x1, y1, x2, y2]` coordinates, while the previous invalid path treated aligned rows as `[x, y, w, h]`. The invalid NFS rows were archived, normalized aligned XYWH annotations were prepared, and NFS tracking was rerun. The current NFS metrics and failure analysis use only corrected normalized aligned XYWH annotations. Earlier NFS metrics and qualitative overlays are superseded.

## 4. Main Results

Table 1 summarizes the benchmark-level results. Figure 1 visualizes the same average AUC changes.

**Table 1. Main benchmark summary.** Average AUC, Precision@20 change, and center-error change for the OSTrack baseline and Paper Freeze V1 RG-SSB method. Positive AUC and Precision@20 changes favor RG-SSB; negative center-error changes indicate lower error.

|Benchmark|Sequences|Pairs|Baseline AUC|RG-SSB AUC|AUC Change|Precision Change|Center Error Change|Conclusion|
|---|---|---|---|---|---|---|---|---|
|OTB|13|52|0.646964|0.680108|+0.033144|+0.050250|-4.563202|RG-SSB improves clearly on average|
|UAV123|16|64|0.660183|0.677587|+0.017405|+0.029983|-3.500185|RG-SSB improves slightly / near neutral|
|NFS|32|128|0.681149|0.671511|-0.009638|-0.006937|+3.705562|Mixed / negative average|
|Cross-benchmark aggregate|53|212|0.689269|0.690748|+0.001478|+0.007843|+1.161416|Near-neutral positive overall; not uniformly improved|

**Figure 1. Benchmark-level AUC change.** `figures/paper_freeze_v1/benchmark_auc_change.{svg,pdf,png}` compares average AUC changes on OTB, UAV123, NFS, and the cross-benchmark aggregate.

The strongest result is on OTB, where RG-SSB improves average AUC by +0.033144 across 52 sequence-condition pairs. UAV123 is also positive, with +0.017405 average AUC over 64 pairs. Corrected NFS is the main weakness: the method decreases average AUC by -0.009638 over 128 pairs. The combined cross-benchmark aggregate is +0.001478, which is best described as near-neutral positive rather than consistent superiority.

## 5. Condition-Level Results

Table 2 and Figure 2 summarize condition-level behavior across the paper-level benchmark table.

**Table 2. Condition-level summary.** Average results by corruption condition across OTB, UAV123, and corrected NFS subsets.

|Condition|Pairs|Baseline AUC|RG-SSB AUC|AUC Change|Precision Change|Center Error Change|Conclusion|
|---|---|---|---|---|---|---|---|
|Clean|61|0.685280|0.690648|+0.005368|+0.015220|+2.558046|improves on average|
|Motion blur|61|0.643687|0.663299|+0.019612|+0.029967|-7.502857|improves on average|
|Low resolution|61|0.672450|0.664175|-0.008275|-0.003989|+6.769353|mixed / negative|
|Gaussian noise|61|0.672042|0.681627|+0.009585|+0.018540|-0.342091|improves on average|

**Figure 2. Condition-level AUC change.** `figures/paper_freeze_v1/condition_auc_change.{svg,pdf,png}` shows average AUC change for clean, motion blur, low resolution, and Gaussian noise.

The method is most consistently positive under motion blur. Gaussian noise is positive on average in the paper-level condition table, but the rejected TDM ablation shows that response-margin modifications can severely regress Gaussian-noise behavior. Low resolution remains the clearest condition-level weakness, with -0.008275 average AUC and increased center error.

## 6. Ablation Results

Table 3 reports the final method-selection ablations. Figure 4 visualizes the ablation decisions.

**Table 3. Ablation summary.** Local ablations used for method selection. These are not full benchmark claims.

|Ablation|Scope|Primary Comparison|Average AUC Change|Decision|Evidence|
|---|---|---|---|---|---|
|Global feature consistency lambda 0.02|3 OTB sequences x 4 conditions|vs OSTrack baseline|+0.023480|kept for Paper Freeze V1|experiments/rgssb_featcons_lambda_sweep_comparison.csv|
|Response consistency|3 OTB sequences x 4 conditions|vs feature-only lambda 0.02|-0.019360|rejected|experiments/rgssb_featcons_lam002_vs_respcons_comparison.csv|
|Target-region feature consistency|3 OTB sequences x 4 conditions|vs global feature consistency lambda 0.02|-0.023555|rejected|experiments/rgssb_target_vs_global_featcons_comparison.csv|
|Target-vs-distractor margin|3 OTB sequences x 4 conditions|vs global feature consistency lambda 0.02|-0.014549|rejected by gate|experiments/rgssb_tdm_gate_comparison.csv|

**Figure 4. Ablation decision summary.** `figures/paper_freeze_v1/ablation_decision.{svg,pdf,png}` reports average AUC changes for retained and rejected ablations.

The final TDM ablation is important negative evidence. It improved several local sequence-condition pairs, but its Gaussian-noise regression dominated the aggregate gate result. It is therefore rejected and is not part of the frozen method.

## 7. Efficiency and Complexity

Table 4 and Figure 3 report same-GPU controlled efficiency measurements. The comparison uses a Tesla V100-PCIE-32GB, the same Car1 clean sequence, 50 warm-up frames, 3 repetitions, synchronized CUDA timing, and separate initialization/per-frame tracking measurements. Historical timing files are not mixed with this controlled comparison.

**Table 4. Efficiency and parameter summary.** Controlled same-GPU runtime and complexity comparison. FLOPs/MACs are unavailable and are not reported as measured.

|Model|GPU|Params|Trainable Params|Frozen Params|Init ms|Latency ms|FPS|Peak Alloc MB|Peak Reserved MB|FLOPs/MACs|
|---|---|---|---|---|---|---|---|---|---|---|
|OSTrack baseline|Tesla V100-PCIE-32GB|92518533|92518533|0|2.949|10.724|93.247|380.233|434.000|unavailable|
|RG-SSB final|Tesla V100-PCIE-32GB|94598469|8554053|86044416|3.165|11.525|86.766|388.917|434.000|unavailable|

**Figure 3. Controlled efficiency comparison.** `figures/paper_freeze_v1/efficiency_comparison.{svg,pdf,png}` compares FPS and latency for the baseline and RG-SSB method under the same V100 protocol.

The final method adds 2,079,936 parameters over the baseline, for 94,598,469 total parameters. Because the backbone is frozen during training, the final training setup has 8,554,053 trainable parameters and 86,044,416 frozen parameters. Runtime decreases from 93.247 FPS to 86.766 FPS in the controlled V100 measurement. Peak allocated memory increases from 380.233 MB to 388.917 MB.

## 8. Corrected NFS Failure Analysis

Figure 5 summarizes terminal outcomes for the corrected NFS failure-case drift analysis.

**Figure 5. Corrected NFS failure-mode distribution.** `figures/paper_freeze_v1/nfs_failure_mode_distribution.{svg,pdf,png}` summarizes terminal outcomes for 10 corrected NFS failure cases selected from the largest corrected drops.

The corrected drift analysis contains 10 cases. Terminal outcomes are: persistent RG-SSB-specific target loss in 5 cases, sudden center jump in 3 cases, shared tracker failure in 1 case, and ambiguous behavior in 1 case. This analysis is qualitative and failure-focused; it should not be interpreted as benchmark-wide frequency. It does suggest that several NFS failures are not only shared tracker difficulty. Some cases follow a multi-stage pattern where both trackers are disturbed, the baseline recovers, and RG-SSB later remains on a distractor or loses the target.

## 9. Discussion

The evidence supports a narrow, defensible claim: restoration-guided state-space adaptation can improve selected robustness outcomes in RGB template-search tracking, especially on the tested OTB subset. UAV123 is positive but mixed, and corrected NFS is slightly negative. The result is therefore promising but not uniformly improved.

The low-resolution weakness and corrected NFS failures are important limitations. They suggest that global feature consistency may not fully protect target identity under fast motion, high-frame-rate sampling behavior, or severe target/background ambiguity. The rejected TDM ablation further shows that adding a response-margin objective is not automatically beneficial; poorly balanced response constraints can introduce large condition-specific regressions.

## 10. Limitations

This paper version has several boundaries:

- The benchmark coverage uses selected subsets, not complete benchmark suites.
- Degradations are synthetic, medium severity, and use one seed.
- Training uses LaSOT only.
- The backbone remains frozen.
- FLOPs/MACs are unavailable.
- Corrected NFS required annotation normalization and rerunning NFS tracking; older NFS metrics and overlays are superseded.
- The evidence does not support state-of-the-art claims.
- The evidence does not prove universal degradation robustness.

## 11. Conclusion

Paper Freeze V1 establishes a conservative fallback method: OSTrack with RG-SSB and box-head training under global clean/degraded feature consistency. The method is positive on OTB and UAV123, mixed on corrected NFS, and near-neutral positive in the mandatory cross-benchmark aggregate. This is sufficient for a cautious proof-of-concept paper position, but not for claims of broad superiority. Future work should expand benchmark coverage, test multiple seeds and severities, and investigate failure-specific refinements only after the current evidence is presented with appropriate limits.

## Citation Placeholders

The draft still requires citations for OSTrack, LaSOT, OTB, UAV123, NFS, Mamba/state-space models, MambaIR-style restoration models, and degradation-robust tracking literature. These are marked as `[CITATION NEEDED]` and listed in `implementation/final_citation_todo.md`.
