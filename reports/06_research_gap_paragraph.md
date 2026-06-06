# Final Research-Gap Paragraph

Purpose: write final paper-ready research-gap wording for the Introduction of the second paper. This report does not create a method architecture, related work section, or final paper plan.

## 1. Final selected research gap

Restoration-oriented Mamba has been established for image restoration, and Mamba-based trackers have been explored for temporal context, memory, fusion, motion prediction, dynamic templates, and adverse-condition tracking, but tracking-aware restoration-guided Mamba for generic degraded RGB template-search visual tracking remains underexplored in the reviewed evidence.

## 2. Short version

MambaIR and MambaIRv2 show that state-space models can be adapted for image restoration by addressing low-level vision issues such as local pixel forgetting, channel redundancy, causal modeling limitations, and token-neighborhood organization. In visual tracking, however, existing Mamba-based methods mainly exploit Mamba for temporal memory, context modeling, multimodal fusion, motion prediction, dynamic template update, efficient backbones, or low-light/adverse-condition tracking. InvTrack directly studies degradation-invariant RGB template-search tracking, but it does not use restoration-guided state-space modeling from MambaIR/MambaIRv2. This leaves an underexplored gap: restoration-guided Mamba for degradation-robust RGB template-search tracking across blur, noise, low resolution, compression, and mixed degradation.

## 3. Full paragraph version

Recent restoration-oriented Mamba models indicate that state-space architectures can be specialized for low-level image recovery. MambaIR adapts Mamba to image restoration by addressing local pixel forgetting and channel redundancy through restoration-specific state-space design, local enhancement, and channel attention, while MambaIRv2 further targets causal state-space limitations through attentive state-space restoration and semantic-guided neighboring. In visual object tracking, however, the reviewed Mamba-based trackers mainly use Mamba for temporal memory, video-level context modeling, multimodal fusion, motion prediction, dynamic template update, efficient backbone design, or nighttime/adverse-condition tracking. These directions are important but are not equivalent to tracking-aware restoration of degraded RGB template-search features. InvTrack provides strong evidence that degradation-invariant RGB tracking is meaningful, using clean-degraded consistency and response-map fusion under blur, low resolution, noise, and compression; nevertheless, it does not incorporate restoration-guided Mamba or the restoration-specific state-space mechanisms developed in MambaIR/MambaIRv2. Similarly, existing low-light or night-UAV Mamba trackers address important illumination-specific settings, but they do not systematically cover generic RGB degradation-robust template-search tracking across blur, noise, low resolution, compression, and mixed degradation. Therefore, the underexplored intersection is restoration-guided Mamba for degradation-robust RGB template-search visual tracking, where restored or recovered representations should be judged by target localization and matching reliability rather than image quality alone.

## 4. Stronger version

Although MambaIR and MambaIRv2 demonstrate that Mamba can be redesigned for restoration-oriented image recovery, the reviewed tracking literature has not directly established how these restoration-specific state-space ideas should be adapted to RGB template-search tracking under generic degradation. Existing Mamba trackers largely emphasize temporal memory, context propagation, multimodal fusion, motion prediction, dynamic template update, efficient feature modeling, or low-light/adverse-condition robustness, while InvTrack addresses degradation-invariant tracking without restoration-guided Mamba. As a result, the direct intersection of restoration-oriented Mamba and degradation-robust RGB template-search matching remains insufficiently investigated, especially for degradations such as blur, noise, low resolution, compression, and their mixtures.

## 5. Conservative version

The reviewed evidence suggests a remaining opportunity at the intersection of Mamba-based image restoration and RGB template-search tracking. MambaIR and MambaIRv2 show restoration-specific Mamba designs for recovering degraded images, while Mamba-based tracking papers primarily study other uses of state-space modeling, including temporal context, memory, multimodal fusion, motion prediction, dynamic templates, efficient tracking, and low-light or sensor-assisted robustness. InvTrack already studies degradation-invariant RGB template-search tracking, so the gap should not be framed as degradation tracking being absent. Rather, what appears underexplored in this evidence set is whether restoration-guided Mamba mechanisms can be adapted to recover target-discriminative template/search representations under generic RGB degradation and improve tracking localization.

## 6. Contribution bridge paragraph

This gap motivates a tracking formulation in which restoration is not treated as a separate image-preprocessing step, but as a tracking-aware mechanism for recovering target-discriminative template and search representations under degradation. Such a formulation should be evaluated against degradation-invariant tracking, generic image-restoration pre-processing, low-light Mamba trackers, and Mamba trackers based on memory or context, using localization, response reliability, and robustness under controlled template/search degradation. This naturally motivates **Restoration-Guided Mamba Tracking for robust RGB visual tracking under degradation**.

## 7. Dangerous claims to avoid

- "No one has used Mamba for tracking."
- "No one has handled low-light tracking."
- "No one has used memory."
- "This is the first degradation-robust tracker."
- "MambaIR has never been used in tracking."
- "No one has handled degradation in RGB tracking."
- "InvTrack is irrelevant because it does not use Mamba."
- "Low-light tracking is the same as general degradation-robust tracking."
- "Multimodal robustness proves RGB-only degradation robustness."
- "Motion prediction solves degraded visual feature recovery."
- "Image restoration is the same as tracking-aware restoration."
- "Feature enhancement, feature consistency, and feature restoration are equivalent."
- "Response-map fusion is novel without qualification."
- "Dynamic template update is novel without qualification."
- "Better PSNR or SSIM proves better tracking."

## 8. Safe wording alternatives

| Dangerous claim | Safer replacement |
|---|---|
| No one has used Mamba for tracking. | Existing Mamba trackers mainly use Mamba for temporal memory, context, fusion, motion prediction, dynamic templates, efficient backbones, or adverse-condition tracking. |
| No one has handled low-light tracking. | Low-light and nighttime tracking have been studied, including by Mamba-based trackers, but low-light is only one part of generic RGB degradation. |
| No one has used memory. | Mamba memory and hidden-state tracking are already studied; degradation-aware restoration of template/search features is a different question. |
| This is the first degradation-robust tracker. | Degradation-invariant tracking has been studied, notably by InvTrack; the underexplored part is restoration-guided Mamba for RGB template-search degradation. |
| MambaIR has never been used in tracking. | The reviewed evidence does not directly show MambaIR/MambaIRv2-style restoration mechanisms adapted to tracking-aware template-search matching. |
| No one has handled degradation in RGB tracking. | InvTrack directly studies RGB degradation-invariant tracking; the remaining gap concerns restoration-guided Mamba recovery. |
| InvTrack is irrelevant because it does not use Mamba. | InvTrack is a central novelty threat and should be distinguished by invariant learning versus restoration-guided state-space recovery. |
| Low-light tracking is the same as general degradation-robust tracking. | Low-light tracking is a related but narrower setting than generic degradation across blur, noise, low resolution, compression, and mixtures. |
| Multimodal robustness proves RGB-only degradation robustness. | Event, thermal, hyperspectral, and language-assisted robustness should be separated from RGB-only degradation robustness. |
| Motion prediction solves degraded visual feature recovery. | MOT motion prediction addresses trajectory or association failures, not necessarily restoration of degraded RGB template/search features. |
| Image restoration is the same as tracking-aware restoration. | Image restoration optimizes visual reconstruction, while tracking-aware restoration should be evaluated by localization and matching reliability. |
| Feature enhancement, feature consistency, and feature restoration are equivalent. | Feature enhancement and invariant consistency are related but distinct from restoration-guided recovery. |
| Response-map fusion is novel. | InvTrack already uses degradation-aware response-map fusion; any response contribution must be restoration-conditioned or otherwise clearly distinguished. |
| Dynamic template update is novel. | SMTrack, MambaVT, MambaEVT, HyMamba, and related trackers already study dynamic templates or memory. |
| Better PSNR or SSIM proves better tracking. | Restoration quality should be secondary; tracking metrics and response reliability are the primary evidence. |

## 9. Evidence support

| Paper or source | What it supports | Evidence reference |
|---|---|---|
| MambaIR | Restoration-oriented Mamba for image restoration; addresses local pixel forgetting and channel redundancy using restoration-specific design, local enhancement, and channel attention | Paper card pp. 1, 3, 6, 7, 8, 9, 13, 14 |
| MambaIRv2 | Attentive state-space restoration and semantic-guided neighboring for image restoration; not tracking | Paper card pp. 1, 2, 3, 4, 5, 8 |
| InvTrack | Degradation-invariant RGB template-search tracking with synthetic blur, downsampling/low resolution, noise, JPEG, clean/degraded feature consistency, and response-map fusion | Paper card pp. 7, 8, 10, 12, 14, 15, 16 |
| MambaTrack Night UAV | Mamba-based low-light enhancement on cropped template/search regions inside a night UAV vision-language tracker | Paper card pp. 1, 2, 3, 4 |
| MambaNUT | Nighttime RGB UAV tracking with Vision Mamba and adaptive curriculum, without image restoration | Paper card pp. 1, 2, 3, 4, 5, 6, 7 |
| MambaLCT | Mamba for long-term context and hidden-state aggregation, not restoration-guided degradation recovery | Paper card pp. 2, 4, 5, 7 |
| MCITrack | Mamba hidden states and contextual memory for video-level tracking; no image restoration or explicit degradation handling reported | Paper card pp. 1, 3, 4, 5, 6, 7 |
| TemTrack | Mamba track-token temporal modeling; restoration and degradation-specific handling not reported | Paper card pp. 2, 3, 4, 5 |
| SMTrack | RGB SOT hidden-state memory, scanned templates, dynamic template update, and template degradation awareness; restoration/enhancement not reported | Paper card pp. 6, 7, 10, 11 |
| MamTrack and Mamba-FETrack | RGB-event Mamba tracking and fusion; robustness is tied to event/multimodal cues rather than RGB-only restoration | MamTrack pp. 1, 4, 5, 6, 8; Mamba-FETrack pp. 1, 2, 6, 7, 8, 9 |
| MambaVT, MambaEVT, HyMamba, All-Day MCMT | Mamba tracking with RGB-T, event-only, hyperspectral, or RGBT settings; these support the distinction between multimodal/sensor-assisted robustness and RGB-only degradation robustness | MambaVT pp. 1, 4, 5, 6, 7, 10; MambaEVT pp. 5, 6, 11, 12; HyMamba pp. 3, 4, 7; All-Day MCMT pp. 1, 2, 5 |
| MambaTrack MOT, MambaMOT, MM-Tracker, SportMamba | Mamba for MOT motion prediction, trajectory modeling, detector/motion maps, association, or blur-related MOT handling; distinct from RGB SOT visual restoration | MambaTrack MOT pp. 1, 2, 5, 6; MambaMOT pp. 1, 2, 3, 4; MM-Tracker pp. 1, 3, 4, 6; SportMamba pp. 1, 3, 4, 6, 8 |
| Missing-intersection matrix | High-potential weakly studied cells for Restoration-aware Mamba, Tracking-aware restoration, Restoration-guided template-search matching, and General RGB degradation robustness in RGB SOT | `tables/missing_intersection_matrix.csv` |
| Final recommendation | Selects TAR-MambaTrack and recommends proceeding with caution | `reports/05b_final_recommendation.md` |
| Novelty danger check | Judges the idea as risky novelty but defensible if narrowed and directly compared to threats | `reports/04_novelty_danger_check.md` |

## 10. Final recommended paragraph

Recent restoration-oriented Mamba models demonstrate that state-space architectures can be specialized for recovering degraded image details: MambaIR addresses local pixel forgetting and channel redundancy with restoration-specific Mamba design, while MambaIRv2 further mitigates causal state-space limitations through attentive state-space restoration and semantic-guided neighboring. In visual object tracking, however, the reviewed Mamba-based trackers primarily exploit Mamba for temporal memory, video-level context, multimodal fusion, motion prediction, dynamic template update, efficient backbone design, or low-light/adverse-condition tracking. These uses are important, but they are not equivalent to tracking-aware restoration of degraded RGB template-search representations. InvTrack shows that degradation-invariant RGB tracking is a meaningful direction through clean-degraded consistency and response-map fusion, yet it does not incorporate restoration-guided state-space modeling from MambaIR/MambaIRv2. Likewise, existing low-light or night-UAV Mamba trackers address important illumination-specific settings, but do not systematically cover generic RGB template-search degradation across blur, noise, low resolution, compression, and mixed artifacts. This leaves an underexplored gap in restoration-guided Mamba tracking: adapting restoration-oriented state-space modeling to recover target-discriminative template and search representations for robust RGB visual tracking under general image degradation.

## Files created or modified

- `reports/06_research_gap_paragraph.md`

## How the output was verified

- Used `reports/05b_final_recommendation.md` for the final selected direction and scorecard-backed decision.
- Used `reports/04_novelty_danger_check.md` for dangerous claims, safe novelty wording, and distinctions from InvTrack, MambaIR/MambaIRv2, and Mamba trackers.
- Used `reports/03b_subagent_review.md` and `reports/02_gap_analysis.md` for final gap synthesis.
- Cross-checked evidence references against paper cards and matrices.
- Verified that the final paragraph does not claim broad absence of Mamba tracking, low-light tracking, memory, or degradation tracking.
- Did not create method architecture, related work, or final paper plan.

## Uncertain fields

- The paragraph is based only on the reviewed paper set and matrices, not a full external literature search.
- Some distinctions are based on fields marked "not reported" in paper cards, not explicit limitations stated by authors.
- The final method name remains provisional until the architecture is designed.

## Whether the project is ready for related work drafting

Yes. The project is ready for related work drafting, provided the related work keeps the same distinctions used here: image restoration versus tracking-aware restoration, temporal memory versus degradation-aware recovery, multimodal robustness versus RGB-only degradation robustness, motion prediction versus degraded visual feature recovery, and low-light tracking versus general degradation-robust tracking.
