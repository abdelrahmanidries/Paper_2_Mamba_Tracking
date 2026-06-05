# Evidence-Supported Candidate Research Gaps

Scope: This report proposes candidate gaps only. It does not define a final paper idea, method architecture, experiment plan, or gap scorecard. Claims are limited to evidence in `paper_cards/`, `tables/paper_matrix.csv`, `tables/mamba_usage_matrix.csv`, `tables/degradation_matrix.csv`, and `tables/missing_intersection_matrix.csv`.

## Gap 1: Restoration-oriented Mamba for generic RGB template-search degradation

1. Gap title: Restoration-oriented Mamba for generic RGB template-search degradation.
2. Exact gap statement: Existing evidence in this project suggests that restoration-oriented Mamba is well supported for image restoration, and degradation-invariant RGB tracking is studied by InvTrack, but restoration-oriented Mamba for generic degraded RGB single-object template-search tracking is underexplored rather than directly solved.
3. Gap type: restoration gap.
4. Papers that partially address the gap: `2024_ECCV_MambaIR`, `2025_CVPR_MambaIRv2`, `InvTrack`, `2025_ICASSP_MambaTrack`, `2025_IROS_MambaNUT`, `2026_IEEE_Transaction_SMTrack`.
5. What those papers already solve: MambaIR and MambaIRv2 solve image restoration tasks with Mamba-style restoration modules. InvTrack solves degradation-invariant template-search tracking with synthetic blur, low resolution, noise, and JPEG degradation, but without Mamba or restoration output. MambaTrack uses a Mamba-based low-light enhancer in a night UAV vision-language tracker. MambaNUT targets nighttime UAV tracking without image enhancement. SMTrack uses SSM/Mamba-style hidden-state template memory and update.
6. What remains unsolved: The direct intersection of restoration-oriented Mamba, generic RGB degradation robustness, and RGB template-search tracking remains weakly studied in the matrix. The unsolved part is not "Mamba for tracking" or "degradation-aware tracking" in general; it is tracking-oriented restoration under broad image-quality degradation in RGB template/search matching.
7. Why the gap matters for visual object tracking: Template and search crops can be differently degraded. Restoration that preserves target-discriminative cues may improve matching more directly than generic image restoration, motion prediction, or sensor fusion.
8. Why the gap is not already solved by InvTrack: InvTrack uses synthetic degradation, clean/degraded feature consistency, low-pass residual modules, and response-map fusion, but its card reports no Mamba/state-space restoration module and no image reconstruction or enhancement target.
9. Why the gap is not already solved by MambaIR: MambaIR is an image restoration paper covering SR, denoising, real denoising, and JPEG artifact reduction. Its card reports no template-search matching, no temporal tracking memory, no dynamic template update, and no response-map design.
10. Why the gap is not already solved by MambaIRv2: MambaIRv2 introduces attentive state-space restoration for SR, JPEG CAR, and denoising, but its card reports no tracking datasets, no template/search tracking pipeline, and no target-discriminative tracking objective.
11. Why the gap is not already solved by existing Mamba trackers: Mamba trackers in the cards mainly use Mamba for temporal context, hidden states, multimodal fusion, motion prediction, dynamic template update, efficient backbones, low-light/night tracking, or spectral/event/RGB-T cues. These are not the same as restoration-oriented RGB feature recovery.
12. How the missing_intersection_matrix supports this gap: `Restoration-aware Mamba / RGB single-object tracking` is marked weakly studied with high gap potential; `Restoration-guided template-search matching / RGB single-object tracking` is also weakly studied with high gap potential; `Restoration-aware Mamba / Image restoration` is well studied, which confirms the restoration side is covered outside tracking.
13. Possible high-level method direction: Study whether restoration-oriented Mamba blocks can be adapted to recover target-discriminative template/search features under broad RGB degradation, without committing to a full architecture here.
14. Possible experiments that could prove the gap: Controlled degraded RGB SOT evaluation with blur, low resolution, noise, JPEG, and mixed degradation; clean-to-degraded and degraded-to-degraded template/search settings; comparison of tracking accuracy and robustness before and after restoration-aware processing.
15. Possible baselines that must be compared: InvTrack, MambaIR/MambaIRv2 as restoration pre-processing baselines, MambaTrack night tracker where applicable, MambaNUT, SMTrack, MCITrack, TemTrack, MambaLCT, and a strong non-Mamba RGB SOT baseline.
16. Risk level: medium.
17. Reviewer criticism: A reviewer may argue this is an engineering combination of MambaIR and InvTrack.
18. How to defend against the criticism: The defense must show that generic image restoration is not enough for tracking, and that a tracking-aware restoration objective or representation improves template-search matching under controlled degradation. This is experimentally testable.
19. Evidence pages or evidence references from paper_cards and matrices: MambaIR pp. 1, 3, 6, 7, 8, 9, 13, 14; MambaIRv2 pp. 1, 2, 3, 4, 5, 6, 7, 8; InvTrack pp. 1, 2, 3, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17; MambaTrack pp. 1, 2, 3, 4; missing matrix rows named above; degradation matrix fields for image/feature restoration and degradation-invariant learning.
20. Final strength score: 5.

Limitation basis: The key limitations for MambaIR, MambaIRv2, InvTrack, and most trackers are implicit from task/method scope. SMTrack adds explicit failure evidence under out-of-view/occlusion and degraded target features, but the restoration gap itself is still inferred from absence of restoration evidence.

## Gap 2: Tracking-aware feature-level restoration for template-search matching

1. Gap title: Tracking-aware feature-level restoration for template-search matching.
2. Exact gap statement: Feature-level enhancement appears in several trackers, and feature-level restoration exists in MambaIR/MambaIRv2 as part of image reconstruction, but feature-level restoration optimized for RGB template-search tracking under degradation is not systematically studied.
3. Gap type: restoration gap.
4. Papers that partially address the gap: `InvTrack`, `2024_ECCV_MambaIR`, `2025_CVPR_MambaIRv2`, `2025_ACM_MultiStateTracker`, `2026_IEEE_Transaction_SMTrack`, `2025_ICASSP_MambaTrack`.
5. What those papers already solve: InvTrack enforces clean/degraded feature consistency. MultiStateTracker performs feature-state specialization and feature enhancement. SMTrack propagates template hidden states. MambaTrack enhances low-light template/search crops. MambaIR and MambaIRv2 perform restoration through feature blocks but for image reconstruction.
6. What remains unsolved: A feature-level restoration mechanism whose success criterion is target matching rather than only image reconstruction or generic feature enhancement remains weakly studied for RGB SOT.
7. Why the gap matters for visual object tracking: Tracking failure can occur when restored images look visually plausible but remove small target-specific cues. A feature-level target-discriminative restoration criterion may matter more than full image quality.
8. Why the gap is not already solved by InvTrack: InvTrack's feature consistency is degradation-invariant learning and response fusion, not restoration-oriented Mamba or reconstruction-guided feature recovery.
9. Why the gap is not already solved by MambaIR: MambaIR reconstructs high-quality images from low-quality inputs, but its paper card reports no target identity, template-search discrimination, or tracking metrics.
10. Why the gap is not already solved by MambaIRv2: MambaIRv2 restores image observations with attentive state-space blocks, but does not test target-discriminative tracking features.
11. Why the gap is not already solved by existing Mamba trackers: MultiStateTracker and SMTrack enhance/model features for efficient tracking and hidden-state propagation, but the cards do not report explicit degradation restoration losses or generic synthetic degradation training.
12. How the missing_intersection_matrix supports this gap: `Feature-level restoration / RGB single-object tracking` is weakly studied with high gap potential; `Tracking-aware restoration / RGB single-object tracking` is weakly studied with high gap potential; `Tracking-aware restoration / Image restoration` is weakly studied with medium gap potential.
13. Possible high-level method direction: Compare tracking-oriented feature restoration against image-level restoration and degradation-invariant feature learning, without prescribing the architecture.
14. Possible experiments that could prove the gap: Ablate feature-level restoration versus image-level pre-restoration; test whether matching response quality, localization accuracy, and robustness improve under different template/search degradation combinations.
15. Possible baselines that must be compared: InvTrack, MambaIR/MambaIRv2 restoration pre-processing, MultiStateTracker, SMTrack, MambaTrack, standard SOT trackers with and without degraded input.
16. Risk level: medium.
17. Reviewer criticism: A reviewer may say feature enhancement in MultiStateTracker or SMTrack already covers this.
18. How to defend against the criticism: Show that those papers model target states or hidden states, while the proposed gap is specifically restoration under known image-quality degradations. The defense should include degradation-specific ablations and not rely on attribute plots alone.
19. Evidence pages or evidence references from paper_cards and matrices: InvTrack pp. 7, 8, 10, 12, 14-16; MultiStateTracker pp. 1, 2, 4, 7, 8; SMTrack pp. 6, 7, 10, 11; MambaIR pp. 1, 6-9, 13, 14; MambaIRv2 pp. 1, 4, 5, 8; missing matrix rows listed above.
20. Final strength score: 5.

Limitation basis: This is mostly an implicit gap from method/evaluation scope. MultiStateTracker has an explicit limitation about too many feature layers adding noise, but it does not explicitly state a restoration limitation.

## Gap 3: Restoration-guided response-map fusion for degraded template-search pairs

1. Gap title: Restoration-guided response-map fusion for degraded template-search pairs.
2. Exact gap statement: InvTrack directly studies degradation-aware clean/degraded response-map fusion, but the matrices indicate that Mamba-based response-map or matching enhancement under degraded RGB template-search tracking is not directly covered.
3. Gap type: response-map gap.
4. Papers that partially address the gap: `InvTrack`, `2025_ACM_MultiStateTracker`, `2026_IEEE_Transaction_SMTrack`, `2025_ICASSP_MambaTrack`, `2025_CVPR_RGBE_MamTrack`.
5. What those papers already solve: InvTrack computes and fuses four clean/degraded template-search response maps. MultiStateTracker uses a classification response map with a Hanning window. SMTrack uses score/offset/box-size maps. MambaTrack visualizes response maps after low-light enhancement. MamTrack uses a center-based score map in RGB-event tracking.
6. What remains unsolved: Restoration-guided response-map fusion using Mamba for generic RGB degradation is not directly shown. Existing score maps are not the same as degradation-aware response fusion.
7. Why the gap matters for visual object tracking: The final response map determines localization. Degradation can affect template and search asymmetrically, so fusing restoration-aware and degradation-aware matching evidence may be important.
8. Why the gap is not already solved by InvTrack: InvTrack is the strongest partial solution, but it does not use Mamba or restoration output; its fusion is degradation-invariant rather than restoration-guided.
9. Why the gap is not already solved by MambaIR: MambaIR has no response map or template-search matching.
10. Why the gap is not already solved by MambaIRv2: MambaIRv2 has no tracking response-map design.
11. Why the gap is not already solved by existing Mamba trackers: The Mamba tracker cards report tracking heads, score maps, motion maps, or association costs, but not restoration-guided response-map fusion under generic degradation.
12. How the missing_intersection_matrix supports this gap: `Response-map fusion / RGB single-object tracking` is weakly studied with high gap potential; `Degradation-aware response-map fusion / RGB single-object tracking` is partially studied with medium gap potential because InvTrack covers it without Mamba; `Restoration-guided template-search matching / RGB single-object tracking` is weakly studied with high gap potential.
13. Possible high-level method direction: Evaluate whether restored and original feature responses should be fused rather than replacing one with the other.
14. Possible experiments that could prove the gap: Compare clean-only, degraded-only, invariant, restored-only, and fused response-map variants under controlled template/search degradations.
15. Possible baselines that must be compared: InvTrack, MultiStateTracker, SMTrack, MambaTrack, MambaIR/MambaIRv2 pre-restoration plus standard response head, and a strong Siamese tracker.
16. Risk level: medium.
17. Reviewer criticism: InvTrack may be viewed as already solving response-map fusion under degradation.
18. How to defend against the criticism: The defense must be narrow: InvTrack solves degradation-invariant response fusion, but not restoration-guided Mamba response fusion. The paper would need to show additional value from restoration-aware state-space modeling, not merely reimplement InvTrack.
19. Evidence pages or evidence references from paper_cards and matrices: InvTrack pp. 7, 8, 14-16; MultiStateTracker p. 5; SMTrack pp. 6, 7; MambaTrack pp. 2-4; MamTrack pp. 4-5; missing matrix response-map rows; degradation matrix `degradation_aware_response_map_fusion`.
20. Final strength score: 4.

Limitation basis: InvTrack's limitation here is implicit, based on the absence of Mamba/restoration output. SMTrack has explicit degraded-feature drift/failure evidence, but not a response-fusion limitation.

## Gap 4: Degradation-aware template and memory update in Mamba RGB trackers

1. Gap title: Degradation-aware template and memory update in Mamba RGB trackers.
2. Exact gap statement: Mamba trackers already use temporal memory, hidden states, context tokens, track tokens, or dynamic templates, but the cards and matrices show that degradation-aware memory/template update for RGB template-search tracking remains weakly studied.
3. Gap type: memory gap.
4. Papers that partially address the gap: `2026_IEEE_Transaction_SMTrack`, `2025_AAAI_MCITrack`, `2025_AAAI_MambaLCT`, `2025_AAAI_TemTrack`, `2025_IEEE_Transaction_MambaVT`, `2026_IEEE_Transaction_MambaEVT`, `2025_arXiv_HyMamba`.
5. What those papers already solve: SMTrack uses hidden-state memory and dynamic template updates. MCITrack stores and updates contextual information with Mamba hidden states and a memory bank. MambaLCT models long-term context. TemTrack models historical track tokens. MambaVT, MambaEVT, and HyMamba use memory or dynamic templates in non-RGB-only settings.
6. What remains unsolved: Explicit update rules that identify degraded templates/search frames and control whether or how they enter Mamba memory are not systematically studied for RGB SOT.
7. Why the gap matters for visual object tracking: Updating memory with degraded observations can contaminate the target representation, while rejecting all uncertain frames can reduce adaptation.
8. Why the gap is not already solved by InvTrack: InvTrack has no temporal memory module and no dynamic template update.
9. Why the gap is not already solved by MambaIR: MambaIR is single-image restoration, not a memory-update tracker.
10. Why the gap is not already solved by MambaIRv2: MambaIRv2 is image restoration and does not report tracking memory.
11. Why the gap is not already solved by existing Mamba trackers: The trackers solve memory/context/template update, but their update evidence is not tied to broad image degradations such as blur, noise, low resolution, or compression. SMTrack has a template evaluator ablation, but the card notes it is not the central final degradation solution.
12. How the missing_intersection_matrix supports this gap: `Degradation-aware memory update / RGB single-object tracking` is weakly studied with high gap potential; `Degradation-aware template update / RGB single-object tracking` is weakly studied with high gap potential; `Dynamic template update / RGB single-object tracking` is partially studied with medium gap potential.
13. Possible high-level method direction: Study degradation-conditioned memory admission or weighting policies, without specifying the full update architecture.
14. Possible experiments that could prove the gap: Compare memory updates with clean frames, degraded frames, mixed degradation schedules, and degradation-aware gating; measure robustness after long sequences with degraded intervals.
15. Possible baselines that must be compared: SMTrack, MCITrack, MambaLCT, TemTrack, MambaVT, MambaEVT, HyMamba, and a no-update tracker.
16. Risk level: medium.
17. Reviewer criticism: Reviewers may argue SMTrack already handles template degradation.
18. How to defend against the criticism: State precisely that SMTrack partially addresses template degradation through evaluator analysis and hidden-state memory, but does not report broad degradation-aware restoration or synthetic degradation-controlled memory update as the central method.
19. Evidence pages or evidence references from paper_cards and matrices: SMTrack pp. 6, 7, 10, 11; MCITrack pp. 3-7; MambaLCT pp. 2, 4, 5, 7; TemTrack pp. 3, 4; MambaVT pp. 4, 5, 10; MambaEVT pp. 5, 6, 12; HyMamba pp. 3, 4, 7; missing matrix rows for degradation-aware memory and template update.
20. Final strength score: 4.

Limitation basis: MCITrack and MambaLCT have explicit computational/training limitations. SMTrack explicitly reports out-of-view/occlusion failures and degraded target feature drift. The degradation-aware update gap itself is implicit from missing degradation-conditioned update evidence.

## Gap 5: General RGB degradation robustness beyond low-light and sensor-assisted robustness

1. Gap title: General RGB degradation robustness beyond low-light and sensor-assisted robustness.
2. Exact gap statement: Low-light/nighttime tracking and multimodal adverse-condition tracking are partially studied, but broad RGB-only degradation robustness across blur, low resolution, noise, compression, and mixed degradation is not directly solved by existing Mamba trackers in this project.
3. Gap type: multimodal-vs-RGB gap.
4. Papers that partially address the gap: `InvTrack`, `2025_ICASSP_MambaTrack`, `2025_IROS_MambaNUT`, `2024_arXiv_Mamba_FETrack`, `2025_CVPR_RGBE_MamTrack`, `2025_IEEE_Transaction_MambaVT`, `2025_CVPR_All_Day_MCMT`, `2026_IEEE_Transaction_MambaEVT`.
5. What those papers already solve: InvTrack handles broad synthetic degradations but is not Mamba/restoration. MambaTrack and MambaNUT target nighttime/low-light UAV tracking. RGB-event, event-only, RGB-T, and all-day MCMT papers use extra sensors or non-RGB modalities to improve robustness.
6. What remains unsolved: A Mamba RGB-only SOT tracker evaluated against broad generic degradation types remains weakly studied.
7. Why the gap matters for visual object tracking: RGB-only tracking remains common when event, thermal, hyperspectral, or language inputs are unavailable. Robustness from extra sensors does not answer whether RGB visual features can be restored or made robust.
8. Why the gap is not already solved by InvTrack: InvTrack addresses broad degradation but without Mamba or restoration-oriented state-space recovery.
9. Why the gap is not already solved by MambaIR: MambaIR restores images but does not perform tracking.
10. Why the gap is not already solved by MambaIRv2: MambaIRv2 restores images but does not evaluate RGB tracking under video degradation.
11. Why the gap is not already solved by existing Mamba trackers: Nighttime, RGB-event, event-only, RGB-T, hyperspectral, and MCMT trackers either narrow the degradation scope to low light or use additional modalities. RGB SOT trackers with Mamba mostly emphasize temporal context, states, or efficiency.
12. How the missing_intersection_matrix supports this gap: `General RGB degradation robustness / RGB single-object tracking` is weakly studied with high gap potential; the same row for RGB-event, RGB-T, vision-language, and nighttime UAV is weakly or partially studied with medium gap potential, showing related but not equivalent coverage.
13. Possible high-level method direction: Use a general degradation benchmark and protocol to separate RGB-only robustness from sensor-assisted or low-light-only robustness.
14. Possible experiments that could prove the gap: Evaluate on synthetic and real degraded RGB videos with blur, low resolution, noise, compression, low-light subsets, and mixed degradation; compare low-light-only and multimodal methods where possible.
15. Possible baselines that must be compared: InvTrack, MambaTrack night tracker, MambaNUT, Mamba-FETrack, MamTrack, MambaVT, MambaEVT, All-Day MCMT where modality/task comparisons are meaningful, plus RGB SOT baselines.
16. Risk level: medium.
17. Reviewer criticism: A reviewer may say low-light or RGB-event/RGB-T papers already address adverse conditions.
18. How to defend against the criticism: Keep the wording to "RGB-only generic image-quality degradation" and explicitly exclude claims that low-light, event, or thermal tracking are unsolved.
19. Evidence pages or evidence references from paper_cards and matrices: InvTrack pp. 7, 8, 10, 12; MambaTrack pp. 1-4; MambaNUT pp. 1-7; Mamba-FETrack pp. 1, 2, 6-9; MamTrack pp. 1, 4-8; MambaVT pp. 1-7, 10; All-Day MCMT pp. 1-8; MambaEVT pp. 1, 4-6, 11, 12; missing matrix `General RGB degradation robustness` row.
20. Final strength score: 5.

Limitation basis: This gap is mainly implicit from task and modality boundaries. MamTrack and MambaVT include explicit limitations about event temporal-resolution use or hardware/speed/special cases, but the RGB-only distinction is inferred from modality design.

## Gap 6: Degradation-state modeling instead of general feature-state modeling

1. Gap title: Degradation-state modeling instead of general feature-state modeling.
2. Exact gap statement: Multi-state and hidden-state Mamba trackers model target features, context, trajectories, or spectral states, but explicit degradation-state modeling for RGB template-search tracking is underexplored.
3. Gap type: degradation gap.
4. Papers that partially address the gap: `2025_ACM_MultiStateTracker`, `2026_IEEE_Transaction_SMTrack`, `InvTrack`, `2025_arXiv_HyMamba`, `2025_IROS_MambaNUT`.
5. What those papers already solve: MultiStateTracker specializes target feature states. SMTrack stores template hidden states. InvTrack creates clean/degraded branches and consistency. HyMamba models spectral hidden states. MambaNUT learns nighttime robustness with curriculum.
6. What remains unsolved: A model that explicitly represents degradation state, such as blur/noise/compression/low-resolution condition, and uses it to guide tracking decisions is not reported in the cards.
7. Why the gap matters for visual object tracking: Different degradations damage tracking cues differently. Treating all feature change as target appearance change may cause poor update or matching decisions.
8. Why the gap is not already solved by InvTrack: InvTrack uses clean/degraded consistency and synthetic degradations, but the matrix marks degradation-state modeling for degradation-invariant tracking as weakly studied, not directly solved.
9. Why the gap is not already solved by MambaIR: MambaIR handles restoration tasks but does not model target/tracking degradation states.
10. Why the gap is not already solved by MambaIRv2: MambaIRv2 uses attentive restoration token processing, not tracking degradation-state control.
11. Why the gap is not already solved by existing Mamba trackers: MultiStateTracker states are target feature states, SMTrack hidden states are template states, and HyMamba states are spectral or temporal states; none is reported as an explicit degradation-state tracker.
12. How the missing_intersection_matrix supports this gap: `Degradation-state modeling / RGB single-object tracking` is weakly studied with high gap potential; `Degradation-state modeling / Degradation-invariant tracking` is weakly studied with high gap potential; `Degradation-state modeling / Hyperspectral tracking` is weakly studied with medium gap potential.
13. Possible high-level method direction: Evaluate whether explicitly estimating degradation state improves restoration selection, memory update, or matching, without prescribing how to estimate it.
14. Possible experiments that could prove the gap: Measure performance when degradation type and severity are known, estimated, or ignored; ablate mixed degradation and state-conditioned decisions.
15. Possible baselines that must be compared: InvTrack, MultiStateTracker, SMTrack, HyMamba, MambaNUT, and a tracker with generic attribute robustness but no degradation-state signal.
16. Risk level: medium.
17. Reviewer criticism: The distinction between feature states and degradation states may look semantic.
18. How to defend against the criticism: Define degradation states operationally by measurable degradation type/severity and show different state-conditioned behavior or gains.
19. Evidence pages or evidence references from paper_cards and matrices: MultiStateTracker pp. 1, 2, 4, 7, 8; SMTrack pp. 6, 7, 10, 11; InvTrack pp. 7, 8, 10, 12; HyMamba pp. 1, 3-7; MambaNUT pp. 1-5; missing matrix `Degradation-state modeling` rows.
20. Final strength score: 4.

Limitation basis: The gap is implicit. MultiStateTracker's explicit limitation about shallow feature noise is relevant but not a degradation-state admission.

## Gap 7: Template-guided attentive scanning for degraded RGB template-search pairs

1. Gap title: Template-guided attentive scanning for degraded RGB template-search pairs.
2. Exact gap statement: MambaIRv2 shows attentive state-space restoration, and some trackers use target/template-aware scanning or hidden-state interactions, but template-guided attentive scanning for degraded RGB template-search restoration is weakly studied.
3. Gap type: scanning gap.
4. Papers that partially address the gap: `2025_CVPR_MambaIRv2`, `2025_CVPR_RGBE_MamTrack`, `2026_IEEE_Transaction_SMTrack`, `2025_ACM_MultiStateTracker`, `2025_ICASSP_MambaTrack`.
5. What those papers already solve: MambaIRv2 uses attentive state-space restoration with semantic neighboring. MamTrack uses Target-Aware Scan for RGB-event template/search interaction. SMTrack uses scanned template hidden states. MultiStateTracker processes template/search patches with state-specific interaction. MambaTrack processes enhanced template/search embeddings in a night vision-language tracker.
6. What remains unsolved: Attentive scanning guided by the target template and designed for restoration under generic RGB degradation is not directly addressed.
7. Why the gap matters for visual object tracking: Restoration should emphasize target-relevant degraded cues rather than background texture. Template-guided scanning may avoid spending restoration capacity on irrelevant regions.
8. Why the gap is not already solved by InvTrack: InvTrack has template/search branches and response fusion, but no Mamba attentive scanning or restoration-guided scan.
9. Why the gap is not already solved by MambaIR: MambaIR uses 2D scanning for image restoration but is not target/template guided.
10. Why the gap is not already solved by MambaIRv2: MambaIRv2 is attentive for image restoration, but its attention is not driven by a tracking template or target matching objective.
11. Why the gap is not already solved by existing Mamba trackers: MamTrack's Target-Aware Scan is RGB-event fusion, not RGB-only restoration; SMTrack/MultiStateTracker use template-state interactions but do not report degradation restoration.
12. How the missing_intersection_matrix supports this gap: `Template-guided attentive scanning / RGB single-object tracking` is weakly studied with medium gap potential; `Target-aware scanning / RGB single-object tracking` is weakly studied with medium gap potential; `Restoration-guided template-search matching / RGB single-object tracking` is weakly studied with high gap potential.
13. Possible high-level method direction: Test whether template cues can guide where restoration-oriented state-space processing focuses in the search crop.
14. Possible experiments that could prove the gap: Compare unguided restoration scanning, template-guided scanning, and no restoration under target-small, distractor, background clutter, and degraded search conditions.
15. Possible baselines that must be compared: MambaIRv2 pre-restoration, MamTrack for target-aware scan evidence, SMTrack, MultiStateTracker, MambaTrack, InvTrack.
16. Risk level: high.
17. Reviewer criticism: This may be too close to existing target-aware scan or attentive restoration unless the tracking/degradation connection is clear.
18. How to defend against the criticism: Keep the contribution framed as the missing intersection of template-guided restoration under degradation, not as attention or target-aware scanning alone.
19. Evidence pages or evidence references from paper_cards and matrices: MambaIRv2 pp. 1, 4, 5, 8; MamTrack pp. 3-6, 8; SMTrack pp. 6, 7; MultiStateTracker pp. 4, 5; MambaTrack pp. 2-4; missing matrix scanning rows.
20. Final strength score: 3.

Limitation basis: Mostly implicit. MamTrack explicitly says it mainly focuses on Mamba for modality fusion and does not fully exploit event temporal resolution, but that is not the same as the RGB restoration-scanning gap.

## Gap 8: Training strategy for general degradation, not only nighttime curriculum

1. Gap title: Training strategy for general degradation, not only nighttime curriculum.
2. Exact gap statement: Curriculum and degradation-aware training are partly supported by MambaNUT and InvTrack, but a Mamba RGB tracker training strategy for generic mixed degradation remains underexplored.
3. Gap type: training-strategy gap.
4. Papers that partially address the gap: `InvTrack`, `2025_IROS_MambaNUT`, `2025_AAAI_MambaLCT`, `2025_AAAI_MCITrack`, `2025_ICASSP_MambaTrack`, `2024_ECCV_MambaIR`, `2025_CVPR_MambaIRv2`.
5. What those papers already solve: InvTrack trains with synthetic degradations and clean/degraded consistency. MambaNUT uses adaptive curriculum learning for nighttime UAV tracking. MambaLCT explicitly discusses training/testing sequence inconsistency due to resource constraints. MCITrack reports video-level training overhead. MambaIR/MambaIRv2 train restoration tasks with task-specific losses.
6. What remains unsolved: A general degradation curriculum or training protocol for Mamba RGB template-search tracking across multiple degradation types and severities is not directly reported.
7. Why the gap matters for visual object tracking: Trackers may overfit to clean data, low-light-only data, or isolated degradations. A controlled training strategy is needed to separate robustness gains from dataset bias.
8. Why the gap is not already solved by InvTrack: InvTrack provides synthetic degradation training but not Mamba or restoration-oriented training.
9. Why the gap is not already solved by MambaIR: MambaIR's training is restoration-task specific, not tracking-loss or template-search specific.
10. Why the gap is not already solved by MambaIRv2: MambaIRv2's training covers restoration benchmarks, not tracking sequences with degraded templates/search frames.
11. Why the gap is not already solved by existing Mamba trackers: MambaNUT's ACL is nighttime-specific; MambaTrack trains a low-light enhancer; other Mamba trackers report standard tracking training, context training, or MOT training rather than generic degradation curriculum.
12. How the missing_intersection_matrix supports this gap: `Curriculum learning / RGB single-object tracking` is weakly studied with medium gap potential; `Degradation-aware learning / RGB single-object tracking` is partially studied with medium gap potential; `General RGB degradation robustness / RGB single-object tracking` is weakly studied with high gap potential.
13. Possible high-level method direction: Design or evaluate a degradation sampling schedule and loss protocol for RGB SOT, without defining the final model.
14. Possible experiments that could prove the gap: Compare no degradation training, random degradation training, staged curriculum, mixed degradation, and degradation-held-out testing.
15. Possible baselines that must be compared: InvTrack, MambaNUT, MambaTrack, MambaIR/MambaIRv2 pre-restoration, standard Mamba trackers trained with and without synthetic degradation.
16. Risk level: medium.
17. Reviewer criticism: This may look like a training recipe rather than a research gap.
18. How to defend against the criticism: Tie the training strategy to measurable degradation generalization and template/search mismatch, and show held-out degradation improvements.
19. Evidence pages or evidence references from paper_cards and matrices: InvTrack pp. 7, 8, 10, 12; MambaNUT pp. 1-5, 7; MambaLCT p. 7; MCITrack p. 7; MambaTrack pp. 3, 4; MambaIR pp. 8, 9; MambaIRv2 pp. 5, 8; missing matrix curriculum/degradation-aware learning rows.
20. Final strength score: 4.

Limitation basis: MambaLCT and MCITrack have explicit training/resource limitations, but the generic degradation curriculum gap is implicit from missing evidence.

## Gap 9: Evaluation gap for restoration-guided tracking under mixed real and synthetic degradation

1. Gap title: Evaluation gap for restoration-guided tracking under mixed real and synthetic degradation.
2. Exact gap statement: The evidence base contains restoration benchmarks, standard tracking attributes, nighttime benchmarks, and InvTrack synthetic degradation tests, but a systematic evaluation of restoration-guided Mamba tracking under mixed RGB degradation is not yet established by the matrices.
3. Gap type: evaluation gap.
4. Papers that partially address the gap: `InvTrack`, `2024_ECCV_MambaIR`, `2025_CVPR_MambaIRv2`, `2025_ICASSP_MambaTrack`, `2025_IROS_MambaNUT`, `2025_AAAI_MM_Tracker`, `2025_CVPRW_SportMamba`, `2025_ACM_MultiStateTracker`.
5. What those papers already solve: InvTrack evaluates synthetic blur, low resolution, noise, and JPEG degradation. MambaIR/MambaIRv2 use restoration metrics and datasets. MambaTrack and MambaNUT evaluate night UAV tracking. MM-Tracker and SportMamba study motion blur in MOT contexts. MultiStateTracker reports tracking attributes such as low resolution, motion blur, and illumination variation.
6. What remains unsolved: A common evaluation protocol that tests restoration-guided Mamba RGB SOT across image-level and feature-level restoration, synthetic and real degradation, and template/search mismatch remains underdeveloped in this project evidence.
7. Why the gap matters for visual object tracking: Without evaluation protocols, gains may reflect clean tracking performance, low-light specialization, or generic restoration quality rather than degraded target localization.
8. Why the gap is not already solved by InvTrack: InvTrack provides strong degradation-invariant tracking evaluation, but not restoration-guided Mamba evaluation.
9. Why the gap is not already solved by MambaIR: MambaIR evaluates restoration quality, not tracking robustness.
10. Why the gap is not already solved by MambaIRv2: MambaIRv2 evaluates restoration quality, not tracking success/precision under template-search degradation.
11. Why the gap is not already solved by existing Mamba trackers: Existing Mamba trackers use standard tracking benchmarks, modality-specific benchmarks, nighttime benchmarks, or MOT benchmarks. Attribute robustness is useful but not a controlled restoration-guided degradation protocol.
12. How the missing_intersection_matrix supports this gap: High-potential cells for `Restoration-aware Mamba / RGB single-object tracking`, `General RGB degradation robustness / RGB single-object tracking`, and `Restoration-guided template-search matching / RGB single-object tracking` indicate the evaluation should target those weak intersections.
13. Possible high-level method direction: Create an evaluation-only study first, using existing trackers and restoration modules, before committing to a new architecture.
14. Possible experiments that could prove the gap: Cross degradation type, severity, and template/search asymmetry; measure tracking metrics and restoration metrics side by side; include real degraded videos where available.
15. Possible baselines that must be compared: InvTrack, MambaIR/MambaIRv2 pre-processing, MambaTrack, MambaNUT, SMTrack, MultiStateTracker, MM-Tracker/SportMamba for MOT blur context, and non-Mamba SOT trackers.
16. Risk level: low.
17. Reviewer criticism: The gap may be seen as evaluation-only rather than methodologically novel.
18. How to defend against the criticism: Use it as supporting evidence for the main gap, or make the evaluation contribution precise and reproducible if it becomes central.
19. Evidence pages or evidence references from paper_cards and matrices: InvTrack pp. 10, 12, 14-16; MambaIR pp. 9, 13, 14; MambaIRv2 pp. 5, 8; MambaTrack pp. 3, 4; MambaNUT pp. 5-7; MM-Tracker pp. 1, 4, 6; SportMamba pp. 1, 6, 8; MultiStateTracker p. 7; degradation matrix degradation-type fields.
20. Final strength score: 4.

Limitation basis: This gap is supported by implicit mismatch between evaluation types. SportMamba has an explicit severe-motion-blur limitation, and MambaLCT/MCITrack have explicit training/resource limitations, but mixed-degradation evaluation remains an inferred gap.

## Gap 10: Visual degradation recovery versus motion prediction for blur-heavy tracking

1. Gap title: Visual degradation recovery versus motion prediction for blur-heavy tracking.
2. Exact gap statement: Several Mamba MOT papers address motion blur through motion prediction, association, detector losses, or tracklet patching, but degraded visual feature recovery for RGB template-search tracking under blur is not directly solved by those MOT approaches.
3. Gap type: degradation gap.
4. Papers that partially address the gap: `2024_ACM_MambaTrack_MOT`, `2025_AAAI_MM_Tracker`, `2025_CVPRW_SportMamba`, `InvTrack`, `2025_ACM_MultiStateTracker`, `2026_IEEE_Transaction_SMTrack`.
5. What those papers already solve: MambaTrack MOT uses Mamba motion prediction and tracklet patching. MM-Tracker uses Motion Mamba and Motion Margin Loss for motion-blur detection difficulty. SportMamba uses Mamba-attention motion prediction, association, ReID, and dynamic EMA. InvTrack includes blur in synthetic degradation. MultiStateTracker and SMTrack report motion blur or template degradation challenges.
6. What remains unsolved: Blur-specific visual feature restoration or restoration-guided template-search matching in RGB SOT remains separate from trajectory-level MOT recovery.
7. Why the gap matters for visual object tracking: Motion prediction can bridge missed detections, but RGB SOT still needs discriminative appearance matching when the template or search crop is blurred.
8. Why the gap is not already solved by InvTrack: InvTrack covers blur degradation in SOT, but without Mamba or restoration-guided recovery.
9. Why the gap is not already solved by MambaIR: MambaIR does not report deblurring experiments in the extracted card and does not evaluate tracking.
10. Why the gap is not already solved by MambaIRv2: MambaIRv2 discusses related Mamba restoration tasks including deblurring as related work, but its extracted experiments cover SR, JPEG CAR, and denoising, not tracking.
11. Why the gap is not already solved by existing Mamba trackers: MOT trackers solve tracking-by-detection association and trajectory prediction, not RGB template-search restoration. RGB SOT Mamba trackers do not report broad blur restoration.
12. How the missing_intersection_matrix supports this gap: `General RGB degradation robustness / RGB single-object tracking` is weakly studied with high gap potential; `Feature-level restoration / RGB single-object tracking` is weakly studied with high gap potential; motion-prediction intersections are studied mainly in MOT rather than RGB SOT restoration.
13. Possible high-level method direction: Evaluate blur recovery as visual feature restoration, separately from motion-prediction compensation.
14. Possible experiments that could prove the gap: Compare motion-prediction/MOT-style robustness, InvTrack blur robustness, and restoration-guided RGB SOT under motion blur and mixed blur conditions.
15. Possible baselines that must be compared: MambaTrack MOT, MM-Tracker, SportMamba, InvTrack, MultiStateTracker, SMTrack, and RGB SOT trackers with restoration pre-processing.
16. Risk level: high.
17. Reviewer criticism: Reviewers may argue the gap is narrower than the main restoration/degradation gap or too focused on blur.
18. How to defend against the criticism: Present it as a supporting sub-gap, not the main paper claim, and avoid saying blur is unhandled by Mamba trackers.
19. Evidence pages or evidence references from paper_cards and matrices: MambaTrack MOT pp. 1, 2, 5, 6, 8; MM-Tracker pp. 1, 3-6; SportMamba pp. 1, 6, 8; InvTrack pp. 7, 10, 12; MultiStateTracker pp. 2, 7; SMTrack pp. 10, 11; degradation matrix `motion_blur` and `image_level_restoration` fields.
20. Final strength score: 3.

Limitation basis: SportMamba explicitly states severe motion blur can cause missed detections and broken tracklets. The broader RGB SOT restoration interpretation is implicit.

## Ranked List From Strongest To Weakest

1. Gap 1: Restoration-oriented Mamba for generic RGB template-search degradation - score 5.
2. Gap 2: Tracking-aware feature-level restoration for template-search matching - score 5.
3. Gap 5: General RGB degradation robustness beyond low-light and sensor-assisted robustness - score 5.
4. Gap 3: Restoration-guided response-map fusion for degraded template-search pairs - score 4.
5. Gap 4: Degradation-aware template and memory update in Mamba RGB trackers - score 4.
6. Gap 6: Degradation-state modeling instead of general feature-state modeling - score 4.
7. Gap 8: Training strategy for general degradation, not only nighttime curriculum - score 4.
8. Gap 9: Evaluation gap for restoration-guided tracking under mixed real and synthetic degradation - score 4.
9. Gap 7: Template-guided attentive scanning for degraded RGB template-search pairs - score 3.
10. Gap 10: Visual degradation recovery versus motion prediction for blur-heavy tracking - score 3.

## Top 3 Recommended Gaps

1. Restoration-oriented Mamba for generic RGB template-search degradation.
2. Tracking-aware feature-level restoration for template-search matching.
3. General RGB degradation robustness beyond low-light and sensor-assisted robustness.

These three are the safest core because the matrices support all three with high-potential RGB SOT intersections, and the novelty threats can be stated precisely: MambaIR/MambaIRv2 cover restoration without tracking; InvTrack covers degradation-invariant tracking without Mamba restoration; MambaTrack/MambaNUT cover low-light/night settings; multimodal trackers rely on extra modalities.

## Weakest 2 Gaps And Why They Are Risky

1. Template-guided attentive scanning for degraded RGB template-search pairs: It is risky because MambaIRv2 already supports attentive restoration, and MamTrack already supports target-aware scan in RGB-event tracking. The remaining novelty depends on proving that template-guided scanning specifically improves degraded RGB restoration/matching.
2. Visual degradation recovery versus motion prediction for blur-heavy tracking: It is risky because several Mamba MOT papers already discuss motion blur. The gap must be framed narrowly around RGB SOT visual recovery, not as an absence of blur handling.

## Top 5 Papers That Threaten Novelty

1. `InvTrack`: Strongest threat to any degradation-invariant RGB template-search claim because it covers synthetic blur, low resolution, noise, JPEG, clean/degraded feature consistency, and response-map fusion.
2. `2025_ICASSP_MambaTrack`: Threatens any claim about Mamba-based low-light enhancement inside a template-search tracking pipeline.
3. `2024_ECCV_MambaIR`: Threatens any broad claim about restoration-oriented Mamba or Mamba for degraded images.
4. `2025_CVPR_MambaIRv2`: Threatens claims around attentive state-space restoration and restoration-specific Mamba design.
5. `2026_IEEE_Transaction_SMTrack`: Threatens claims around Mamba/SSM hidden-state memory, dynamic template update, and template degradation awareness.

## Safest Wording For The Main Research Gap

Existing Mamba trackers in this evidence set primarily use state-space modeling for temporal context, hidden-state memory, multimodal fusion, motion prediction, dynamic template handling, efficient backbones, or low-light/sensor-assisted tracking. MambaIR and MambaIRv2 demonstrate restoration-oriented Mamba for image restoration, while InvTrack demonstrates degradation-invariant RGB template-search tracking without Mamba-based restoration. The underexplored intersection is restoration-oriented Mamba for degradation-robust RGB template-search tracking, especially where restoration is evaluated by target-discriminative matching under broad image-quality degradation rather than by image quality alone.

## Files Created Or Modified

- `reports/02_gap_analysis.md`

## How The Output Was Verified

- The candidate gaps were selected from high and medium cells in `tables/missing_intersection_matrix.csv`.
- Each gap was cross-checked against `tables/paper_matrix.csv`, `tables/mamba_usage_matrix.csv`, and `tables/degradation_matrix.csv`.
- Paper-level support was checked against the corresponding Markdown paper cards in `paper_cards/`.
- The report avoids the banned broad novelty claims about Mamba tracking, low-light tracking, and Mamba memory.
- The report separates explicit limitations from implicit scope gaps in each candidate section.

## Uncertain Fields

- The final strength scores are evidence-based prioritization, not a formal gap scorecard.
- Several gaps are implicit because the papers do not state them as author limitations; they follow from task, modality, method, and evaluation boundaries.
- Some high-level method directions may overlap, so the strongest final paper framing should likely combine only a small subset after reviewer-risk analysis.
