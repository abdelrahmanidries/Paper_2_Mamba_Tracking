# Reviewer Attack on Candidate Research Gaps

Reviewer stance: strict CVPR/ICCV/ECCV area reviewer. I treat a gap as weak if it is obvious, a direct combination of two existing papers, already partially solved by the uploaded set, not experimentally falsifiable, or dependent on vague wording. Scores use 1-5, where 5 is strong for novelty/importance/feasibility/difference/clarity, and 5 is high danger for reviewer risk.

## Gap 1: Restoration-oriented Mamba for generic RGB template-search degradation

1. Is this gap too obvious? Partly. "Use MambaIR-style restoration in tracking" is obvious. The stronger version is target-discriminative restoration for degraded template-search matching, not generic restoration pre-processing.
2. Is this gap already solved by one of the uploaded papers? Not fully. InvTrack already covers degradation-invariant RGB template-search tracking with synthetic blur, low resolution, noise, JPEG, feature consistency, LPRM, and response-map fusion. MambaIR and MambaIRv2 already cover restoration-oriented Mamba. MambaTrack Night UAV already places a Mamba low-light enhancer inside a template-search tracker. The unsolved portion is the exact intersection: generic RGB degradation, restoration-oriented Mamba, and tracking-aware template-search matching.
3. Is this gap only a simple engineering combination? It will look like one unless the work proves that restoration is target-discriminative and tracking-aware, not just MambaIR/MambaIRv2 used as pre-processing before a tracker.
4. Is the novelty strong enough for a high-level conference or journal? Potentially, but only after narrowing. As currently written, it is borderline because the novelty threat from InvTrack plus MambaIR/MambaIRv2 is obvious.
5. What evidence supports the gap? Missing-intersection matrix marks `Restoration-aware Mamba / RGB single-object tracking` and `Restoration-guided template-search matching / RGB single-object tracking` as weakly studied with high gap potential. Paper cards show MambaIR/MambaIRv2 are image restoration papers, InvTrack is degradation-invariant tracking without Mamba/restoration output, and MambaTrack Night UAV is low-light vision-language tracking.
6. What evidence is missing? Evidence that restoration-oriented Mamba improves tracking-specific discriminability under generic degradation beyond image-quality metrics. Evidence against a simple pipeline of MambaIRv2 pre-restoration plus InvTrack is especially missing.
7. What experiment would be required to prove this gap? A controlled RGB SOT degradation benchmark with asymmetric template/search degradation, comparing target localization and response quality against InvTrack, MambaIR/MambaIRv2 pre-processing, low-light MambaTrack where applicable, and strong RGB Mamba trackers.
8. What baseline would threaten the novelty? InvTrack plus MambaIRv2 pre-processing; MambaTrack Night UAV for low-light; SMTrack for memory/template update; Multi-State Tracker for feature enhancement; MambaNUT for nighttime robustness.
9. What would a reviewer criticize? "This is just combining MambaIR with InvTrack." "You changed the backbone but the degradation formulation is InvTrack." "Image restoration may improve PSNR but not tracking robustness."
10. How should the gap be rewritten to be more precise? Restoration-oriented Mamba has not been directly evaluated as a tracking-aware feature recovery mechanism for generic degraded RGB template-search matching, where success is measured by target localization and matching reliability rather than image reconstruction quality alone.
11. Should this gap be kept, merged, downgraded, or removed? Keep, but merge with Gaps 2 and 5 into the main gap. Do not keep the broad version.

Scores:

| Criterion | Score |
|---|---:|
| Novelty | 4 |
| Importance | 5 |
| Feasibility | 4 |
| Difference from InvTrack | 3 |
| Difference from MambaIR | 4 |
| Difference from MambaIRv2 | 4 |
| Difference from existing Mamba trackers | 4 |
| Experimental clarity | 5 |
| Reviewer risk | 3 |

Evidence references: MambaIR pp. 1, 3, 6, 7, 8, 9, 13, 14; MambaIRv2 pp. 1, 2, 3, 4, 5, 6, 7, 8; InvTrack pp. 1, 2, 3, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17; MambaTrack Night UAV pp. 1, 2, 3, 4; missing-intersection matrix rows listed above.

## Gap 2: Tracking-aware feature-level restoration for template-search matching

1. Is this gap too obvious? Somewhat. Feature-level restoration for tracking is a natural refinement of Gap 1. It is not strong enough as a separate headline unless it defines a measurable tracking-specific feature-recovery target.
2. Is this gap already solved by one of the uploaded papers? Partially. InvTrack already enforces clean/degraded feature consistency. Multi-State Tracker already reports feature-state enhancement for RGB tracking. SMTrack already uses template hidden-state propagation. MambaIR/MambaIRv2 already perform feature-level restoration blocks for image reconstruction.
3. Is this gap only a simple engineering combination? High risk. Without a clear distinction between "feature enhancement", "feature consistency", and "restoration", it will read as rebranding existing feature modules.
4. Is the novelty strong enough for a high-level conference or journal? Not as a standalone gap. It can strengthen the main gap if tied to target-discriminative matching.
5. What evidence supports the gap? Missing-intersection matrix marks `Feature-level restoration / RGB single-object tracking` as weakly studied with high gap potential. Paper cards say MambaIR/MambaIRv2 use feature blocks for image-level restoration, while InvTrack uses feature consistency without Mamba restoration.
6. What evidence is missing? A definition of feature-level restoration that is not simply feature enhancement, invariance, or hidden-state propagation. The current evidence does not prove existing feature-enhancement trackers fail under generic degradation.
7. What experiment would be required to prove this gap? Ablate image-level pre-restoration, feature-level restoration, feature consistency, and no restoration on the same degraded template/search protocol; measure localization, response confidence, and robustness under held-out degradation.
8. What baseline would threaten the novelty? InvTrack, Multi-State Tracker, SMTrack, MambaIRv2 pre-processing, and MambaTrack Night UAV.
9. What would a reviewer criticize? "Feature-level restoration is undefined." "Multi-State Tracker and InvTrack already do feature-level robustness." "The paper is just replacing feature blocks."
10. How should the gap be rewritten to be more precise? Existing trackers partially improve degraded features through invariance, feature-state modeling, or hidden-state propagation, but tracking-supervised restoration of target-discriminative template/search features under generic RGB degradation is not directly established.
11. Should this gap be kept, merged, downgraded, or removed? Merge into Gap 1. Do not keep as a separate main gap.

Scores:

| Criterion | Score |
|---|---:|
| Novelty | 3 |
| Importance | 4 |
| Feasibility | 3 |
| Difference from InvTrack | 2 |
| Difference from MambaIR | 4 |
| Difference from MambaIRv2 | 4 |
| Difference from existing Mamba trackers | 3 |
| Experimental clarity | 4 |
| Reviewer risk | 4 |

Evidence references: InvTrack pp. 7, 8, 10, 12, 14-16; Multi-State Tracker pp. 1, 2, 4, 7, 8; SMTrack pp. 6, 7, 10, 11; MambaIR pp. 1, 6-9, 13, 14; MambaIRv2 pp. 1, 4, 5, 8.

## Gap 3: Restoration-guided response-map fusion for degraded template-search pairs

1. Is this gap too obvious? Moderately. It is a direct extension of InvTrack's response-map fusion with restoration/Mamba added.
2. Is this gap already solved by one of the uploaded papers? Partially and seriously threatened. InvTrack already fuses four clean/degraded template-search response maps and shows ablation evidence. Multi-State Tracker uses a classification response map with a Hanning window. SMTrack and MamTrack use score maps, although not degradation-aware response fusion.
3. Is this gap only a simple engineering combination? Yes, if stated as "add Mamba restoration to InvTrack's fusion". It needs a sharper reason why restoration-guided fusion differs from degradation-invariant fusion.
4. Is the novelty strong enough for a high-level conference or journal? Weak as a standalone gap; acceptable as a component inside the main restoration-guided template-search gap.
5. What evidence supports the gap? Missing-intersection matrix marks `Response-map fusion / RGB single-object tracking` as weakly studied with high gap potential and `Degradation-aware response-map fusion / RGB single-object tracking` as partially studied because InvTrack covers it without Mamba.
6. What evidence is missing? Evidence that restoration-guided response fusion is meaningfully different from InvTrack's clean/degraded response fusion. Also missing is evidence that current score-map heads fail specifically because they lack restoration.
7. What experiment would be required to prove this gap? Compare InvTrack-style response fusion, restored-feature response fusion, original/restored dual-branch fusion, and no-fusion heads under identical degradation settings.
8. What baseline would threaten the novelty? InvTrack is the direct threat. Multi-State Tracker and SMTrack threaten weaker claims about response maps in RGB tracking.
9. What would a reviewer criticize? "InvTrack already does the key response-map idea." "The only addition is Mamba/restoration, which is incremental unless the fusion objective is new and necessary."
10. How should the gap be rewritten to be more precise? Degradation-aware response-map fusion is partially addressed by InvTrack, but restoration-conditioned response fusion with Mamba-derived recovered features is not directly studied for RGB template-search tracking.
11. Should this gap be kept, merged, downgraded, or removed? Merge into Gap 1 as a possible sub-problem. Downgrade as a standalone gap.

Scores:

| Criterion | Score |
|---|---:|
| Novelty | 3 |
| Importance | 4 |
| Feasibility | 3 |
| Difference from InvTrack | 2 |
| Difference from MambaIR | 5 |
| Difference from MambaIRv2 | 5 |
| Difference from existing Mamba trackers | 3 |
| Experimental clarity | 4 |
| Reviewer risk | 4 |

Evidence references: InvTrack pp. 7, 8, 14-16; Multi-State Tracker p. 5; SMTrack pp. 6, 7; MamTrack pp. 4, 5; MambaTrack Night UAV pp. 2-4; missing-intersection matrix response-map rows.

## Gap 4: Degradation-aware template and memory update in Mamba RGB trackers

1. Is this gap too obvious? No, but it is adjacent to many existing Mamba memory papers. The novelty must be degradation-conditioned update, not memory itself.
2. Is this gap already solved by one of the uploaded papers? Partially. SMTrack uses hidden-state memory and dynamic template updates, and even analyzes a template evaluator against template degradation. MCITrack uses a memory bank and Mamba hidden states. MambaLCT, TemTrack, MambaVT, MambaEVT, MamTrack, HyMamba, MambaTrack MOT, MambaMOT, and SportMamba all threaten broad memory or temporal modeling claims.
3. Is this gap only a simple engineering combination? Medium risk. A quality gate based on degradation score could be incremental unless it is tied to restoration or experimentally shows memory contamination from degraded frames.
4. Is the novelty strong enough for a high-level conference or journal? Potentially as a secondary contribution, not as the only main gap. It is more defensible if paired with restoration-guided RGB degradation robustness.
5. What evidence supports the gap? Missing-intersection matrix marks `Degradation-aware memory update / RGB single-object tracking` and `Degradation-aware template update / RGB single-object tracking` as weakly studied with high gap potential. Paper cards show memory/update mechanisms, but not broad degradation-aware update.
6. What evidence is missing? Evidence that degraded frames contaminate Mamba memory in existing trackers. Also missing are controlled tests on whether SMTrack's template evaluator is insufficient under blur/noise/JPEG/low-resolution degradation.
7. What experiment would be required to prove this gap? Long-sequence degraded tracking with update contamination tests: clean update, degraded update, confidence-only update, degradation-aware update, restoration-aware update, and no update.
8. What baseline would threaten the novelty? SMTrack is the strongest threat. MCITrack threatens memory-bank claims. MambaVT, MambaEVT, HyMamba, MamTrack, MambaLCT, and TemTrack threaten broader Mamba memory/context claims.
9. What would a reviewer criticize? "SMTrack already does dynamic template hidden-state updates and template quality evaluation." "Confidence-based updates are common; degradation-aware gating may be incremental."
10. How should the gap be rewritten to be more precise? Mamba trackers already use temporal memory and dynamic template states, but the evidence set does not directly establish update rules that separate target appearance change from image-quality degradation and prevent degraded observations from corrupting RGB template/search memory.
11. Should this gap be kept, merged, downgraded, or removed? Keep as a secondary gap, preferably merged with the main restoration/degradation framing. Do not present it as the main novelty alone.

Scores:

| Criterion | Score |
|---|---:|
| Novelty | 4 |
| Importance | 4 |
| Feasibility | 3 |
| Difference from InvTrack | 5 |
| Difference from MambaIR | 5 |
| Difference from MambaIRv2 | 5 |
| Difference from existing Mamba trackers | 3 |
| Experimental clarity | 4 |
| Reviewer risk | 3 |

Evidence references: SMTrack pp. 6, 7, 10, 11; MCITrack pp. 1, 3, 4, 5, 6, 7; MambaLCT pp. 2, 4, 5, 7; TemTrack pp. 3, 4; MambaVT pp. 4, 5, 10; MambaEVT pp. 5, 6, 12; HyMamba pp. 3, 4, 7; MamTrack pp. 4, 5; missing-intersection matrix update rows.

## Gap 5: General RGB degradation robustness beyond low-light and sensor-assisted robustness

1. Is this gap too obvious? Yes if it is stated broadly. "General RGB degradation beyond low light and multimodal robustness" is more of a scope correction than a novel gap.
2. Is this gap already solved by one of the uploaded papers? Partially. InvTrack directly handles generic RGB degradation in tracking. MambaTrack Night UAV and MambaNUT address low-light/nighttime tracking. Mamba-FETrack, MamTrack, MambaVT, MambaEVT, HyMamba, and All-Day MCMT address adverse conditions through extra modalities or non-RGB sensors.
3. Is this gap only a simple engineering combination? It can be, if it merely says "evaluate more degradations". It becomes stronger only when tied to restoration-oriented Mamba and target-discriminative matching.
4. Is the novelty strong enough for a high-level conference or journal? Not as a standalone gap. It is important background framing but weak as a main contribution.
5. What evidence supports the gap? Missing-intersection matrix marks `General RGB degradation robustness / RGB single-object tracking` as weakly studied with high gap potential while related modality columns are weakly/partially studied. Degradation matrix separates low-light, multimodal robustness, and synthetic generic degradations.
6. What evidence is missing? Evidence that all existing RGB Mamba SOT methods fail under generic mixed degradation. Current matrices show missing design evidence, not performance failure.
7. What experiment would be required to prove this gap? A benchmark protocol comparing generic degradation types and severities against low-light-only and sensor-assisted methods, while controlling for task and modality.
8. What baseline would threaten the novelty? InvTrack is the direct generic-degradation threat. MambaNUT threatens low-light RGB claims. MambaTrack Night UAV threatens restoration-in-tracking under low light. MamTrack/Mamba-FETrack/MambaVT/MambaEVT/HyMamba/All-Day MCMT threaten adverse-condition claims via modality.
9. What would a reviewer criticize? "This is an evaluation scope, not a research gap." "InvTrack already covers broad synthetic degradations." "Do not discount multimodal robustness; just distinguish it from RGB-only."
10. How should the gap be rewritten to be more precise? Generic RGB degradation robustness is partially addressed by InvTrack without Mamba/restoration and by low-light or multimodal Mamba trackers in narrower settings; the underexplored part is restoration-oriented Mamba for RGB-only template-search robustness across multiple degradation types.
11. Should this gap be kept, merged, downgraded, or removed? Merge into Gap 1 as the degradation scope. Downgrade as a standalone gap.

Scores:

| Criterion | Score |
|---|---:|
| Novelty | 3 |
| Importance | 5 |
| Feasibility | 4 |
| Difference from InvTrack | 2 |
| Difference from MambaIR | 4 |
| Difference from MambaIRv2 | 4 |
| Difference from existing Mamba trackers | 4 |
| Experimental clarity | 5 |
| Reviewer risk | 3 |

Evidence references: InvTrack pp. 7, 8, 10, 12; MambaTrack Night UAV pp. 1-4; MambaNUT pp. 1-7; Mamba-FETrack pp. 1, 2, 6-9; MamTrack pp. 1, 4-8; MambaVT pp. 1-7, 10; MambaEVT pp. 1, 4-6, 11, 12; HyMamba pp. 1, 3-7; All-Day MCMT pp. 1-8.

## Gap 6: Degradation-state modeling instead of general feature-state modeling

1. Is this gap too obvious? It is not obvious, but it is vague. "Degradation state" is not sufficiently defined in the current evidence.
2. Is this gap already solved by one of the uploaded papers? Partially. InvTrack has clean/degraded branches and synthetic degradation consistency. Multi-State Tracker explicitly models multiple target feature states. SMTrack stores hidden template states. HyMamba models spectral hidden states. MambaNUT models nighttime robustness through curriculum.
3. Is this gap only a simple engineering combination? It risks becoming a label-estimation add-on: classify degradation type, then condition the tracker. That is not enough for a high-level venue without a clear mechanism and proof.
4. Is the novelty strong enough for a high-level conference or journal? Weak unless operationalized. As written, it is too abstract.
5. What evidence supports the gap? Missing-intersection matrix marks `Degradation-state modeling / RGB single-object tracking` and `/ Degradation-invariant tracking` as weakly studied with high gap potential. Paper cards distinguish Multi-State Tracker's target feature states from degradation states.
6. What evidence is missing? A precise definition of degradation state, labels, supervision, use in matching/update/restoration, and why it outperforms InvTrack's clean/degraded consistency.
7. What experiment would be required to prove this gap? Controlled degradation-type and severity labels, held-out degradation types, and ablations showing state-conditioned tracking decisions improve over invariant learning.
8. What baseline would threaten the novelty? InvTrack, Multi-State Tracker, SMTrack, MambaNUT, and HyMamba.
9. What would a reviewer criticize? "This is semantic relabeling of feature states." "The paper has no evidence that degradation-state labels are available or necessary." "InvTrack already trains against degradations without explicit states."
10. How should the gap be rewritten to be more precise? If retained, rewrite as: Current state-based trackers model target appearance, memory, or spectral states, but do not explicitly use measured degradation type/severity to control restoration, matching, or update decisions in RGB template-search tracking.
11. Should this gap be kept, merged, downgraded, or removed? Downgrade heavily. Merge as an optional analysis under Gap 4 or remove if the final study lacks explicit degradation-state supervision.

Scores:

| Criterion | Score |
|---|---:|
| Novelty | 3 |
| Importance | 3 |
| Feasibility | 2 |
| Difference from InvTrack | 3 |
| Difference from MambaIR | 5 |
| Difference from MambaIRv2 | 5 |
| Difference from existing Mamba trackers | 3 |
| Experimental clarity | 2 |
| Reviewer risk | 5 |

Evidence references: Multi-State Tracker pp. 1, 2, 4, 7, 8; SMTrack pp. 6, 7, 10, 11; InvTrack pp. 7, 8, 10, 12; HyMamba pp. 1, 3-7; MambaNUT pp. 1-5; missing-intersection matrix degradation-state rows.

## Gap 7: Template-guided attentive scanning for degraded RGB template-search pairs

1. Is this gap too obvious? It is niche and mechanism-first. It reads like a method idea rather than a research gap.
2. Is this gap already solved by one of the uploaded papers? Partially. MambaIRv2 already studies attentive state-space restoration. MamTrack already has Target-Aware Scan for template-search interaction in RGB-event tracking. SMTrack uses template hidden states. Multi-State Tracker processes template/search patches jointly.
3. Is this gap only a simple engineering combination? High risk. Combining MambaIRv2 attentive restoration with MamTrack-style target-aware scan is exactly the obvious attack.
4. Is the novelty strong enough for a high-level conference or journal? Not as a standalone gap. It is too implementation-specific and too close to existing mechanisms.
5. What evidence supports the gap? Missing-intersection matrix marks `Template-guided attentive scanning / RGB single-object tracking` and `Target-aware scanning / RGB single-object tracking` as weakly studied with medium gap potential.
6. What evidence is missing? Evidence that scanning order or attentional scan guidance is the bottleneck in degraded RGB tracking. Evidence that target-aware scanning improves restoration rather than just fusion or matching is missing.
7. What experiment would be required to prove this gap? Ablate scan guidance under fixed restoration/tracking modules and show that template-guided scanning improves degraded matching over unguided attentive restoration and target-aware fusion.
8. What baseline would threaten the novelty? MambaIRv2, MamTrack, SMTrack, Multi-State Tracker, and MambaTrack Night UAV.
9. What would a reviewer criticize? "This is an architecture trick, not a gap." "MamTrack already has target-aware scan." "MambaIRv2 already has attentive state-space restoration."
10. How should the gap be rewritten to be more precise? Do not present it as a standalone gap. If used, frame it as one possible mechanism to test whether target cues should guide restoration-oriented scanning under RGB degradation.
11. Should this gap be kept, merged, downgraded, or removed? Remove as standalone. It can be a later method design option, but this report should not keep it as a core research gap.

Scores:

| Criterion | Score |
|---|---:|
| Novelty | 2 |
| Importance | 3 |
| Feasibility | 3 |
| Difference from InvTrack | 4 |
| Difference from MambaIR | 3 |
| Difference from MambaIRv2 | 2 |
| Difference from existing Mamba trackers | 2 |
| Experimental clarity | 3 |
| Reviewer risk | 5 |

Evidence references: MambaIRv2 pp. 1, 4, 5, 8; MamTrack pp. 3-6, 8; SMTrack pp. 6, 7; Multi-State Tracker pp. 4, 5; MambaTrack Night UAV pp. 2-4.

## Gap 8: Training strategy for general degradation, not only nighttime curriculum

1. Is this gap too obvious? Somewhat. A degradation curriculum is an expected extension after InvTrack and MambaNUT.
2. Is this gap already solved by one of the uploaded papers? Partially. InvTrack already trains with synthetic degradations. MambaNUT already uses adaptive curriculum learning for nighttime UAV tracking. MambaTrack Night UAV trains a low-light enhancer and tracker. MambaIR/MambaIRv2 train restoration tasks with task-specific losses.
3. Is this gap only a simple engineering combination? High risk if it is just "train on more degradation types" or "apply curriculum to InvTrack".
4. Is the novelty strong enough for a high-level conference or journal? Not as the main novelty. It can be a strong experimental support component.
5. What evidence supports the gap? Missing-intersection matrix marks `Curriculum learning / RGB single-object tracking` as weakly studied with medium gap potential and `Degradation-aware learning / RGB single-object tracking` as partially studied with medium gap potential.
6. What evidence is missing? Evidence that curriculum is required for Mamba restoration-guided tracking, not merely helpful. Evidence of held-out degradation generalization is missing.
7. What experiment would be required to prove this gap? Compare no degradation training, random degradation training, InvTrack-style synthetic degradation, nighttime curriculum, and general mixed-degradation curriculum on seen and unseen degradation types.
8. What baseline would threaten the novelty? InvTrack and MambaNUT are the direct threats. MambaTrack Night UAV threatens low-light training claims. MambaIR/MambaIRv2 threaten restoration loss/training claims.
9. What would a reviewer criticize? "This is a training recipe." "InvTrack already uses synthetic degradations." "MambaNUT already studies curriculum."
10. How should the gap be rewritten to be more precise? Generic degradation curriculum should be treated as an experimental requirement for validating restoration-oriented Mamba tracking, not as a standalone novelty claim unless it proves held-out degradation generalization.
11. Should this gap be kept, merged, downgraded, or removed? Merge into the experimental validation of Gap 1. Downgrade as a standalone gap.

Scores:

| Criterion | Score |
|---|---:|
| Novelty | 3 |
| Importance | 4 |
| Feasibility | 5 |
| Difference from InvTrack | 2 |
| Difference from MambaIR | 4 |
| Difference from MambaIRv2 | 4 |
| Difference from existing Mamba trackers | 3 |
| Experimental clarity | 5 |
| Reviewer risk | 4 |

Evidence references: InvTrack pp. 7, 8, 10, 12; MambaNUT pp. 1-5, 7; MambaTrack Night UAV pp. 3, 4; MambaIR pp. 8, 9; MambaIRv2 pp. 5, 8; MambaLCT p. 7; MCITrack p. 7.

## Gap 9: Evaluation gap for restoration-guided tracking under mixed real and synthetic degradation

1. Is this gap too obvious? Yes as a research gap; evaluation is necessary but rarely enough for a high-level paper by itself.
2. Is this gap already solved by one of the uploaded papers? Partially. InvTrack gives the strongest degradation-tracking evaluation. MambaIR/MambaIRv2 give restoration evaluations. MambaTrack Night UAV and MambaNUT give night UAV evaluations. MM-Tracker and SportMamba evaluate blur-related MOT issues. Multi-State Tracker evaluates attributes including low resolution, illumination variation, and motion blur.
3. Is this gap only a simple engineering combination? Yes if it only combines existing benchmarks and metrics.
4. Is the novelty strong enough for a high-level conference or journal? Weak as a standalone gap. Strong as a required validation protocol for the main gap.
5. What evidence supports the gap? The matrices separate image restoration, degradation-invariant tracking, low-light tracking, multimodal robustness, MOT blur handling, and RGB SOT degradation robustness. No single matrix row shows restoration-guided Mamba tracking evaluation across mixed RGB degradation.
6. What evidence is missing? Evidence of an accepted benchmark deficiency or systematic failure. The current evidence supports an evaluation need, not a novel technical gap by itself.
7. What experiment would be required to prove this gap? A reproducible degradation evaluation suite with real and synthetic degraded RGB SOT videos, controlled template/search degradation, and comparison to restoration, tracking, and invariant-learning baselines.
8. What baseline would threaten the novelty? InvTrack; MambaIR/MambaIRv2 pre-processing; MambaTrack Night UAV; MambaNUT; Multi-State Tracker; SMTrack; MM-Tracker and SportMamba for blur context.
9. What would a reviewer criticize? "Evaluation-only." "Dataset construction is not a technical contribution." "The degradation protocol may be arbitrary."
10. How should the gap be rewritten to be more precise? The paper must include a mixed-degradation evaluation protocol to validate the main restoration-oriented Mamba tracking gap, but should not rely on the protocol alone as the core novelty.
11. Should this gap be kept, merged, downgraded, or removed? Merge into Gap 1 as required evidence. Downgrade as standalone.

Scores:

| Criterion | Score |
|---|---:|
| Novelty | 2 |
| Importance | 4 |
| Feasibility | 5 |
| Difference from InvTrack | 3 |
| Difference from MambaIR | 4 |
| Difference from MambaIRv2 | 4 |
| Difference from existing Mamba trackers | 4 |
| Experimental clarity | 5 |
| Reviewer risk | 4 |

Evidence references: InvTrack pp. 10, 12, 14-16; MambaIR pp. 9, 13, 14; MambaIRv2 pp. 5, 8; MambaTrack Night UAV pp. 3, 4; MambaNUT pp. 5-7; MM-Tracker pp. 1, 4, 6; SportMamba pp. 1, 6, 8; Multi-State Tracker p. 7.

## Gap 10: Visual degradation recovery versus motion prediction for blur-heavy tracking

1. Is this gap too obvious? It is clear but narrow. It is a subcase of the broader degradation/restoration problem.
2. Is this gap already solved by one of the uploaded papers? Partially. MambaTrack MOT, MambaMOT, MM-Tracker, and SportMamba all threaten broad motion/blur claims. InvTrack already includes blur degradation in RGB SOT. Multi-State Tracker and SMTrack include motion blur or template degradation evidence.
3. Is this gap only a simple engineering combination? It could become an incremental comparison between motion prediction and restoration. It is not enough as the main gap.
4. Is the novelty strong enough for a high-level conference or journal? Weak standalone. It may be useful as one experiment or motivating failure mode.
5. What evidence supports the gap? Degradation matrix shows motion blur is handled in MOT contexts through motion prediction, detector loss, association, or tracklet patching, while image-level restoration is not reported for those MOT papers. Missing-intersection matrix supports general RGB degradation and feature-level restoration gaps.
6. What evidence is missing? Evidence that a restoration-guided RGB SOT method outperforms motion-prediction approaches under comparable blur settings. Also missing is an apples-to-apples task bridge between MOT and SOT.
7. What experiment would be required to prove this gap? Blur-controlled RGB SOT experiments plus MOT-context comparisons where appropriate, carefully avoiding direct metric comparisons across incompatible tasks.
8. What baseline would threaten the novelty? InvTrack for blur in SOT; MM-Tracker and SportMamba for motion blur in MOT; MambaTrack MOT and MambaMOT for trajectory prediction; Multi-State Tracker and SMTrack for RGB tracking robustness claims.
9. What would a reviewer criticize? "MOT and SOT are different tasks." "Blur is already discussed by several Mamba trackers." "This is too narrow compared with generic degradation."
10. How should the gap be rewritten to be more precise? Treat blur as one controlled degradation case showing why motion prediction and degraded visual feature recovery are distinct; do not state it as the main gap.
11. Should this gap be kept, merged, downgraded, or removed? Remove as standalone; merge into Gap 1's degradation evaluation.

Scores:

| Criterion | Score |
|---|---:|
| Novelty | 2 |
| Importance | 3 |
| Feasibility | 4 |
| Difference from InvTrack | 2 |
| Difference from MambaIR | 4 |
| Difference from MambaIRv2 | 4 |
| Difference from existing Mamba trackers | 2 |
| Experimental clarity | 3 |
| Reviewer risk | 5 |

Evidence references: MambaTrack MOT pp. 1, 2, 5, 6, 8; MM-Tracker pp. 1, 3-6; SportMamba pp. 1, 6, 8; InvTrack pp. 7, 10, 12; Multi-State Tracker pp. 2, 7; SMTrack pp. 10, 11.

## Cross-Paper Novelty Threat Map

- InvTrack: Directly threatens degradation-invariant RGB template-search tracking, synthetic blur/low-resolution/noise/JPEG claims, clean/degraded feature consistency, low-pass residual modules, and response-map fusion.
- MambaIR: Directly threatens restoration-oriented Mamba, image-level restoration, feature-level restoration blocks, low-resolution/noise/JPEG restoration, and 2D scanning claims.
- MambaIRv2: Directly threatens attentive/non-causal state-space restoration, semantic neighboring/token reordering for restoration, and claims around Mamba restoration design.
- MambaTrack Night UAV: Threatens low-light enhancement inside a template-search tracker, Mamba-based enhancement, and vision-language night UAV tracking claims.
- MambaNUT: Threatens nighttime RGB UAV tracking, Vision Mamba backbone for template-search, and curriculum learning under night/day imbalance.
- MambaLCT: Threatens temporal context, long-term hidden-state aggregation, and Mamba for video-level context.
- MCITrack: Threatens Mamba hidden-state memory, contextual-information transmission, reliable-frame memory bank, and video-level tracking context.
- TemTrack: Threatens track-token temporal memory and Mamba for historical token modeling.
- SMTrack: Threatens RGB SOT hidden-state template memory, dynamic template updates, template degradation awareness, and SSM/Mamba efficient tracking.
- MambaVT: Threatens RGB-T template memory, trajectory prompts, multimodal context, and sensor-assisted robustness.
- MambaEVT: Threatens event-only Mamba tracking, Memory Mamba, dynamic template generation, and adverse-condition event robustness.
- MamTrack: Threatens RGB-event multimodal fusion, Target-Aware Scan, historical Mamba decoder, score-map tracking, and template-search interaction.
- Mamba-FETrack: Threatens RGB-event Mamba feature extraction/fusion and adverse-condition robustness through event sensing.
- MambaTrack MOT: Threatens motion prediction, tracklet patching, and Mamba trajectory modeling under occlusion/motion blur.
- MambaMOT: Threatens Mamba replacing or complementing conventional MOT motion models for nonlinear trajectory prediction.
- MM-Tracker: Threatens motion blur claims through Motion Mamba and Motion Margin Loss in UAV MOT.
- SportMamba: Threatens sports MOT motion prediction, association, dynamic EMA, and blur/occlusion claims.
- Multi-State Tracker: Threatens efficient RGB tracking, feature-state enhancement, response-map use, and attribute robustness claims.
- HyMamba: Threatens hyperspectral Mamba tracking, dynamic templates, hidden states, and spectral feature enhancement.
- All-Day MCMT: Threatens low-light/all-day tracking claims through RGBT fusion and infrared-assisted robustness.

## Revised Ranked List Of Strongest Gaps

1. Merged Gap A: Tracking-aware restoration-oriented Mamba for generic degraded RGB template-search matching. This merges Gaps 1, 2, and 5, with Gap 9 as required evaluation support.
2. Gap B: Degradation-aware memory/template update for RGB Mamba trackers. This is Gap 4, narrowed to degradation-conditioned update rather than memory in general.
3. Gap C: Restoration-conditioned response-map fusion for RGB template-search matching. This is Gap 3, but only as a sub-gap because InvTrack is a major threat.
4. Gap D: General degradation training/evaluation protocol for restoration-guided RGB tracking. This merges Gaps 8 and 9 as supporting evidence, not primary novelty.
5. Gap E: Explicit degradation-state control for restoration/update decisions. This is Gap 6, but it is speculative and should be used only if operationalized.

## Top 3 Gaps That Should Be Kept

1. Merged Gap A: Tracking-aware restoration-oriented Mamba for generic degraded RGB template-search matching.
2. Gap B: Degradation-aware memory/template update for RGB Mamba trackers.
3. Gap C: Restoration-conditioned response-map fusion for RGB template-search matching, kept only as a component of the main gap.

## Gaps That Should Be Merged

- Merge Gap 1, Gap 2, and Gap 5 into one main gap.
- Merge Gap 3 into the main gap as the matching/response-map component.
- Merge Gap 8 and Gap 9 into the evaluation/training validation section for the main gap.
- Merge Gap 10 into the degradation evaluation as a blur-specific case.
- Merge Gap 6 into Gap 4 only if degradation state is used to control memory/update; otherwise do not use it.

## Gaps That Should Be Removed

- Remove Gap 7 as a standalone gap. It is too mechanism-specific and too close to MambaIRv2 plus MamTrack.
- Remove Gap 10 as a standalone gap. It is narrow, heavily threatened by MOT blur papers and InvTrack, and should only be a subcase.
- Remove standalone Gap 9 if the paper needs a high-level technical novelty. Keep it only as required validation.
- Remove standalone Gap 6 unless degradation state is precisely defined and experimentally validated.

## Top 5 Papers That Most Threaten Novelty

1. InvTrack: most direct threat to generic degradation-invariant RGB template-search tracking, feature consistency, LPRM, and response-map fusion.
2. MambaTrack Night UAV: direct threat to Mamba-based low-light enhancement inside a template-search tracker.
3. MambaIRv2: strongest threat to attentive restoration-oriented Mamba claims.
4. MambaIR: strong threat to restoration-oriented Mamba and low-level degradation recovery claims.
5. SMTrack: strongest Mamba RGB tracking threat for hidden-state memory, dynamic template update, and template degradation awareness.

Close secondary threats: MCITrack for Mamba memory/context, MambaNUT for nighttime curriculum, MamTrack for target-aware scan and multimodal fusion, Multi-State Tracker for RGB feature-state enhancement, and MM-Tracker/SportMamba for blur-related MOT claims.

## Safest Wording For The Main Research Gap

The evidence set suggests that restoration-oriented Mamba is established for image restoration, degradation-invariant RGB template-search tracking is partially addressed by InvTrack without Mamba restoration, and existing Mamba trackers mainly cover temporal context, hidden-state memory, dynamic templates, multimodal fusion, motion prediction, efficient backbones, low-light/night tracking, or sensor-assisted robustness. What remains underexplored is tracking-aware restoration-oriented Mamba for generic degraded RGB template-search matching, where restored or recovered representations are evaluated by target localization and matching reliability rather than image quality alone.

## Strongest Final Gap After Reviewer Attack

Tracking-aware restoration-oriented Mamba for generic degraded RGB template-search matching is the strongest surviving gap, but only after merging the overlapping restoration, feature-level, RGB-only degradation, response-map, and evaluation gaps. The core claim should be narrow: not that Mamba tracking, low-light tracking, memory, or degradation handling are absent, but that the direct intersection of restoration-oriented Mamba and generic degradation-robust RGB template-search matching is not directly established by the uploaded evidence.

## Files Created Or Modified

- `reports/03_reviewer_attack.md`

## How The Report Was Verified

- Reviewed `reports/02_gap_analysis.md` and preserved all 10 candidate gaps.
- Cross-checked paper threats against `tables/paper_matrix.csv`, `tables/mamba_usage_matrix.csv`, `tables/degradation_matrix.csv`, `tables/missing_intersection_matrix.csv`, and `paper_cards/`.
- Checked that the attack distinguishes image restoration from tracking-aware restoration, temporal memory from degradation-aware memory, multimodal robustness from RGB-only robustness, motion prediction from degraded visual recovery, and low-light tracking from generic degradation-robust tracking.
- The report does not create paper ideas, method architecture, experiment plan, or `gap_scorecard.csv`.

## Uncertain Fields

- The numeric scores are reviewer-style judgments based on the existing evidence matrices, not a formal gap scorecard.
- Several attack points are implicit because the paper cards do not always contain explicit limitation statements.
- Difference from existing Mamba trackers is hardest to score for gaps involving memory, templates, or response maps because SMTrack, MCITrack, MamTrack, MambaEVT, MambaVT, and HyMamba each cover parts of that space.
