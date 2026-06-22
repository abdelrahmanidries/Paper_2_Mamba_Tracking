# Paper Draft Freeze V1

## Method

We study a restoration-guided state-space block integrated into OSTrack for degradation-robust RGB template-search tracking. The frozen method keeps the OSTrack backbone fixed and trains only `rgssb.*` and `box_head.*`. The selected training setup uses global clean/degraded feature consistency with weight 0.02. Response consistency, target-region feature consistency, and target-vs-distractor margin loss are disabled in the final method.

## Experiments

The baseline is `vitb_256_mae_ce_32x4_ep300`. The final method is `vitb_256_mae_ce_32x4_ep300_rgssb_head_train_lasot_degraded_hpc_featcons_lam002`. We evaluate clean, motion-blur, low-resolution, and Gaussian-noise conditions at medium severity with one degradation seed. NFS results use normalized aligned XYWH annotations; earlier XYXY-as-XYWH NFS metrics and qualitative overlays are superseded.

## Results

|Benchmark|Sequences|Pairs|Baseline AUC|RG-SSB AUC|AUC Change|Precision Change|Center Error Change|Conclusion|
|---|---|---|---|---|---|---|---|---|
|OTB|13|52|0.646964|0.680108|+0.033144|+0.050250|-4.563202|RG-SSB improves clearly on average|
|UAV123|16|64|0.660183|0.677587|+0.017405|+0.029983|-3.500185|RG-SSB improves slightly / near neutral|
|NFS|32|128|0.681149|0.671511|-0.009638|-0.006937|+3.705562|Mixed / negative average|
|Cross-benchmark aggregate|53|212|0.689269|0.690748|+0.001478|+0.007843|+1.161416|Near-neutral positive overall; not uniformly improved|

|Condition|Pairs|Baseline AUC|RG-SSB AUC|AUC Change|Precision Change|Center Error Change|Conclusion|
|---|---|---|---|---|---|---|---|
|Clean|61|0.685280|0.690648|+0.005368|+0.015220|+2.558046|improves on average|
|Motion blur|61|0.643687|0.663299|+0.019612|+0.029967|-7.502857|improves on average|
|Low resolution|61|0.672450|0.664175|-0.008275|-0.003989|+6.769353|mixed / negative|
|Gaussian noise|61|0.672042|0.681627|+0.009585|+0.018540|-0.342091|improves on average|

## Efficiency

|Model|GPU|Params|Trainable Params|Frozen Params|Init ms|Latency ms|FPS|Peak Alloc MB|Peak Reserved MB|FLOPs/MACs|
|---|---|---|---|---|---|---|---|---|---|---|
|OSTrack baseline|Tesla V100-PCIE-32GB|92518533|92518533|0|2.949|10.724|93.247|380.233|434.000|unavailable|
|RG-SSB final|Tesla V100-PCIE-32GB|94598469|8554053|86044416|3.165|11.525|86.766|388.917|434.000|unavailable|

## Ablations

|Ablation|Scope|Primary Comparison|Average AUC Change|Decision|Evidence|
|---|---|---|---|---|---|
|Global feature consistency lambda 0.02|3 OTB sequences x 4 conditions|vs OSTrack baseline|+0.023480|kept for Paper Freeze V1|experiments/rgssb_featcons_lambda_sweep_comparison.csv|
|Response consistency|3 OTB sequences x 4 conditions|vs feature-only lambda 0.02|-0.019360|rejected|experiments/rgssb_featcons_lam002_vs_respcons_comparison.csv|
|Target-region feature consistency|3 OTB sequences x 4 conditions|vs global feature consistency lambda 0.02|-0.023555|rejected|experiments/rgssb_target_vs_global_featcons_comparison.csv|
|Target-vs-distractor margin|3 OTB sequences x 4 conditions|vs global feature consistency lambda 0.02|-0.014549|rejected by gate|experiments/rgssb_tdm_gate_comparison.csv|

## Discussion

The results are positive on OTB and UAV123, but corrected NFS is slightly negative. This indicates promising but non-uniform cross-benchmark robustness. The rejected TDM ablation confirms that directly modifying the response objective can introduce regressions, especially under Gaussian noise.

## Limitations

The evidence uses selected benchmark subsets, synthetic corruptions, one seed, medium severity, a frozen backbone, and LaSOT-only training. No state-of-the-art or universal robustness claim is supported.

## Conclusion

RG-SSB with global feature consistency is a defensible Paper Freeze V1 method, but broader evaluation is required before stronger claims.
