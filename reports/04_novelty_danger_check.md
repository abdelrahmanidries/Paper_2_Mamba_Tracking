# Novelty Danger Check: TAR-MambaTrack

Selected idea from `reports/04_top_paper_ideas.md`: **TAR-MambaTrack**, proposed as "Tracking-Aware Restoration Mamba for Degradation-Robust RGB Template-Search Tracking."

Selected one-sentence contribution: study whether restoration-oriented Mamba can be adapted from image restoration to RGB template-search tracking by recovering target-discriminative representations under generic degradation and validating the effect on localization and matching reliability.

## 1. Executive summary

Judgment: **risky novelty, but defensible if narrowed**.

The idea is not safely novel in a broad form. InvTrack already covers degradation-invariant RGB template-search tracking with synthetic blur, low resolution, noise, JPEG corruption, clean/degraded feature consistency, low-pass residual modules, and response-map fusion. MambaIR and MambaIRv2 already cover restoration-oriented Mamba for image restoration. MambaTrack Night UAV already places a Mamba low-light enhancer inside a template-search tracking pipeline. SMTrack and MCITrack already cover Mamba memory/update in tracking.

The idea becomes defensible only if it is framed as a **tracking-aware restoration-oriented Mamba** study for **generic degraded RGB template-search matching**, where success is measured by localization and matching reliability, not image quality alone. The paper must not claim novelty in using Mamba for tracking, low-light tracking, memory, or image restoration by itself.

Evidence basis:

- Missing-intersection matrix: `Restoration-aware Mamba / RGB single-object tracking`, `Tracking-aware restoration / RGB single-object tracking`, `Restoration-guided template-search matching / RGB single-object tracking`, and `General RGB degradation robustness / RGB single-object tracking` are weakly studied with high gap potential.
- MambaIR paper card: restoration-oriented Mamba is covered for image restoration but not tracking, pp. 1, 3, 6, 7, 8, 9, 13, 14.
- MambaIRv2 paper card: attentive state-space restoration is covered for image restoration but not tracking, pp. 1, 2, 3, 4, 5, 6, 7, 8.
- InvTrack paper card: degradation-invariant RGB tracking is covered without Mamba or restoration output, pp. 1, 2, 3, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17.
- MambaTrack Night UAV paper card: Mamba low-light enhancement is used on template/search crops, but in low-light/night UAV vision-language tracking, pp. 1, 2, 3, 4.

## 2. Main novelty threats

1. InvTrack

- Why it is dangerous: It is the closest paper to generic degraded RGB template-search tracking.
- What it already covers: Synthetic blur, low resolution/downsampling, noise, JPEG compression, clean/degraded consistency, LPRM, and four-way response-map fusion.
- What it does not cover: Mamba, restoration-oriented state-space blocks, image reconstruction output, or restoration-guided feature recovery.
- How our idea must differ: The method must use restoration-oriented Mamba recovery and tracking-supervised matching/localization evidence, not only invariant feature consistency.
- Evidence: InvTrack pp. 7, 8, 10, 12, 14, 15, 16; degradation matrix marks InvTrack as `Yes` for degradation-invariant learning and degradation-aware response-map fusion.

2. MambaTrack Night UAV

- Why it is dangerous: It already uses a Mamba-based low-light enhancer on cropped template/search regions inside a tracker.
- What it already covers: Low-light/night UAV tracking, image-level low-light enhancement, language-assisted tracking, and template/search crops.
- What it does not cover: Generic degradation beyond low light, language-free RGB-only tracking, or mixed blur/noise/low-resolution/JPEG robustness.
- How our idea must differ: The selected idea must focus on generic RGB degradation and not claim novelty for low-light Mamba enhancement in tracking.
- Evidence: MambaTrack Night UAV pp. 1, 2, 3, 4; degradation matrix marks low light `Yes`, image-level restoration `Yes`, and restoration-guided template-search matching `Partial`.

3. MambaIRv2

- Why it is dangerous: It already provides attentive restoration-oriented Mamba through ASE and SGN.
- What it already covers: Image restoration for SR, JPEG CAR, and denoising using attentive state-space restoration.
- What it does not cover: Visual tracking, template-search matching, target localization, response maps, or tracking losses.
- How our idea must differ: It must show that restoration-oriented Mamba is adapted to target-discriminative tracking, not merely inserted as image pre-processing.
- Evidence: MambaIRv2 pp. 1, 2, 3, 4, 5, 8; paper matrix marks tracking-specific fields as not reported.

4. MambaIR

- Why it is dangerous: It already establishes restoration-oriented Mamba blocks, local enhancement, and channel attention for low-level restoration.
- What it already covers: Image SR, denoising, real-world denoising, JPEG artifact reduction, VSSM/2D-SSM, local convolution, and channel attention.
- What it does not cover: RGB template-search tracking or tracking-aware target recovery.
- How our idea must differ: It must evaluate restoration by tracking localization and matching reliability rather than image reconstruction quality.
- Evidence: MambaIR pp. 1, 3, 6, 7, 8, 9, 13, 14.

5. SMTrack

- Why it is dangerous: It strongly threatens any claim about Mamba/SSM memory, dynamic templates, hidden states, and template degradation awareness in RGB SOT.
- What it already covers: Hidden-state memory, scanned template states, dynamic template update, template evaluator analysis, and RGB tracking.
- What it does not cover: Restoration/enhancement, generic synthetic degradation training, or restoration-guided template-search recovery.
- How our idea must differ: Avoid making memory or dynamic template update the core novelty unless update is explicitly tied to degradation/restoration reliability and tested against SMTrack.
- Evidence: SMTrack pp. 6, 7, 10, 11; paper matrix marks temporal memory and dynamic template update as `Yes`.

## 3. Difference from InvTrack

InvTrack partially addresses the same application area, so the selected idea is high risk unless the distinction is explicit.

- Invariant feature learning vs restoration-guided state-space modeling: InvTrack trains clean/degraded feature consistency with synthetic degradations and low-pass residual modules. The selected idea must use restoration-oriented Mamba/state-space recovery and show tracking benefits from recovered target-discriminative features.
- Clean-degraded consistency vs restoration-aware Mamba feature recovery: InvTrack's card reports feature consistency and TV regularization, but no Mamba or restoration output. The selected idea must not simply reproduce consistency learning.
- Response-map fusion in InvTrack vs possible restoration-guided response fusion: InvTrack already fuses four clean/degraded response maps. A response-fusion contribution is novel only if restoration-conditioned or Mamba-recovered responses improve localization beyond InvTrack-style fusion.
- Low-pass residual modules vs MambaIR-style restoration blocks: InvTrack uses PRDB/LPRM/SConv-style modules, while MambaIR/MambaIRv2 use restoration-oriented state-space designs. The selected idea must show that Mamba restoration blocks are not just a backbone swap.

Evidence: InvTrack pp. 7, 8, 10, 12, 14, 15, 16; missing-intersection matrix marks `Degradation-aware response-map fusion / RGB single-object tracking` as partially studied by InvTrack and `Restoration-aware Mamba / Degradation-invariant tracking` as weakly studied.

## 4. Difference from MambaIR and MambaIRv2

MambaIR and MambaIRv2 threaten the restoration side of the idea but do not solve the tracking side in the reviewed evidence.

- Image restoration vs visual tracking: MambaIR and MambaIRv2 are image restoration papers. The selected idea is RGB template-search tracking.
- Pixel reconstruction vs target localization: MambaIR/MambaIRv2 optimize image restoration outputs; the selected idea must optimize or validate target localization and matching reliability.
- Restoration loss vs tracking loss: MambaIR uses restoration losses such as L1/Charbonnier for restoration tasks; MambaIRv2 uses restoration training for SR, JPEG CAR, and denoising. The selected idea must include tracking losses and tracking metrics.
- Generic image recovery vs template-search matching: MambaIR/MambaIRv2 do not report template/search branches, response maps, or target localization.
- Semantic-guided neighboring vs possible template-guided attentive scanning: MambaIRv2's SGN is image-restoration token ordering. If the selected idea uses template-guided scanning, it must be tied to target matching; otherwise it is too close to MambaIRv2 plus MamTrack.

Evidence: MambaIR pp. 1, 3, 6, 7, 8, 9, 13, 14; MambaIRv2 pp. 1, 2, 3, 4, 5, 8; paper matrix tracking-specific fields for both are not reported.

## 5. Difference from existing Mamba trackers

The selected idea differs from existing Mamba trackers only if the core is restoration-guided RGB degradation recovery, not general Mamba tracking.

- Temporal memory: MambaLCT, MCITrack, TemTrack, SMTrack, MambaVT, MambaEVT, HyMamba, MambaMOT, MambaTrack MOT, and SportMamba already use temporal memory, hidden states, track tokens, trajectory histories, or context. The selected idea must not claim novelty in memory.
- Context modeling: MambaLCT and MCITrack already use Mamba for video-level context and hidden-state context transmission.
- Multimodal fusion: MamTrack, Mamba-FETrack, MambaVT, HyMamba, and All-Day MCMT use Mamba or Mamba-like mechanisms for multimodal/sensor-rich fusion.
- Motion prediction: MambaTrack MOT, MambaMOT, MM-Tracker, and SportMamba use Mamba for trajectory or motion prediction; this is not the same as degraded visual feature recovery.
- Dynamic template update: SMTrack, MambaVT, MambaEVT, and HyMamba already cover dynamic templates or memory. The selected idea should not use dynamic update as the headline unless it is degradation-aware restoration update.
- Nighttime UAV tracking: MambaTrack Night UAV and MambaNUT already cover night/low-light tracking. Low light is only one degradation category for the selected idea.
- RGB-T/event/hyperspectral tracking: Robustness from event, thermal, hyperspectral, or RGBT cues is not equivalent to RGB-only degradation robustness.

Evidence: MambaLCT pp. 2, 4, 5; MCITrack pp. 3, 4, 5, 6, 7; TemTrack pp. 3, 4; SMTrack pp. 6, 7, 10, 11; MamTrack pp. 4, 5, 8; Mamba-FETrack pp. 1, 2, 6, 7, 8, 9; MambaVT pp. 4, 5, 6, 7, 10; MambaEVT pp. 5, 6, 11, 12; HyMamba pp. 3, 4, 7; MambaTrack MOT pp. 2, 3, 5, 6; MambaMOT pp. 2, 3, 4; MM-Tracker pp. 3, 4, 6; SportMamba pp. 3, 4, 6, 8.

## 6. Required novelty ingredients

1. Tracking-aware restoration objective

- Why it is needed: Separates the idea from MambaIR/MambaIRv2 image restoration and from simple pre-processing.
- Threat paper it helps distinguish from: MambaIR, MambaIRv2.
- Ablation to verify it: Restoration-only supervision versus tracking-supervised restoration; compare tracking metrics and response quality, not only PSNR/SSIM.

2. Restoration-oriented Mamba recovery inside template-search matching

- Why it is needed: Separates the idea from InvTrack's non-Mamba invariant learning and from generic Mamba tracking backbones.
- Threat paper it helps distinguish from: InvTrack, Multi-State Tracker, SMTrack.
- Ablation to verify it: Mamba restoration block versus non-Mamba restoration block versus no restoration under identical degradation.

3. Generic RGB degradation protocol beyond low light

- Why it is needed: Separates the idea from MambaTrack Night UAV, MambaNUT, and All-Day MCMT.
- Threat paper it helps distinguish from: MambaTrack Night UAV, MambaNUT, All-Day MCMT.
- Ablation to verify it: Evaluate blur, low resolution, noise, JPEG, low light, and mixed degradation separately and jointly.

4. Direct comparison with InvTrack and MambaIR/MambaIRv2 pre-processing

- Why it is needed: Prevents the paper from looking like a simple combination of prior methods.
- Threat paper it helps distinguish from: InvTrack, MambaIR, MambaIRv2.
- Ablation to verify it: InvTrack baseline; MambaIR/MambaIRv2 pre-restore plus tracker; selected idea under the same protocol.

5. Template-search asymmetry testing

- Why it is needed: Tracking degradation is not only single-image restoration; template and search frames can degrade differently.
- Threat paper it helps distinguish from: MambaIR/MambaIRv2 and InvTrack.
- Ablation to verify it: Clean-template/degraded-search, degraded-template/clean-search, both-degraded, and mixed-severity settings.

6. Matching or response reliability evidence

- Why it is needed: Shows target localization benefit rather than visual restoration benefit.
- Threat paper it helps distinguish from: MambaIR/MambaIRv2 and InvTrack.
- Ablation to verify it: Response peak sharpness, false-peak rate, distractor response, localization error, and tracking success with and without recovered representations.

7. RGB-only framing

- Why it is needed: Separates the idea from multimodal robustness using event, thermal, hyperspectral, or language signals.
- Threat paper it helps distinguish from: MamTrack, Mamba-FETrack, MambaVT, MambaEVT, HyMamba, All-Day MCMT, MambaTrack Night UAV.
- Ablation to verify it: RGB-only evaluation with no event/thermal/language/hyperspectral input.

## 7. Dangerous claims to avoid

- "No one has used Mamba for tracking."
- "No one has handled low-light tracking."
- "No one has used Mamba memory."
- "No one has handled degradation in RGB tracking."
- "No one has used restoration in tracking."
- "MambaIR or MambaIRv2 already prove tracking robustness."
- "InvTrack is not relevant because it does not use Mamba."
- "Low-light tracking is the same as general degradation robustness."
- "Multimodal robustness is the same as RGB-only degradation robustness."
- "MOT motion prediction is the same as degraded visual feature recovery."
- "Feature enhancement, feature consistency, and feature restoration are interchangeable."
- "Response-map fusion is novel without distinguishing from InvTrack."
- "Dynamic template update is novel without distinguishing from SMTrack, MCITrack, MambaVT, MambaEVT, and HyMamba."
- "A higher PSNR/SSIM restoration result proves better tracking."

## 8. Safe final novelty statement

Within the reviewed evidence set, restoration-oriented Mamba is well established for image restoration, and degradation-invariant RGB template-search tracking is partially addressed without Mamba-based restoration. Existing Mamba trackers mainly study temporal context, hidden-state memory, dynamic templates, multimodal fusion, motion prediction, efficient backbones, low-light/night tracking, or sensor-assisted robustness. The selected idea targets the underexplored intersection of tracking-aware restoration-oriented Mamba and generic degraded RGB template-search matching, where recovered representations are evaluated by target localization and matching reliability rather than by image restoration quality alone.

## 9. Final judgment

Final judgment: **risky novelty**.

The selected idea should not be considered safely novel because several papers cover adjacent pieces very strongly: InvTrack covers generic degradation-invariant RGB tracking, MambaIR/MambaIRv2 cover restoration-oriented Mamba, MambaTrack Night UAV covers Mamba low-light enhancement in tracking, and SMTrack/MCITrack cover memory/update in RGB tracking. However, the exact intersection of restoration-oriented Mamba, generic RGB degradation, tracking-aware template-search matching, and localization-based evaluation is not directly addressed in the reviewed evidence. The idea should proceed only if the final work is built around those required novelty ingredients and includes direct threat baselines.

## 10. Paper-by-paper novelty comparison

### 1. InvTrack

1. Does this paper already solve the selected idea? Partially, but not fully.
2. What is similar? RGB SOT under image-quality degradation, synthetic blur/low-resolution/noise/JPEG degradation, clean/degraded template-search branches, feature consistency, and response-map fusion.
3. What is different? InvTrack does not report Mamba, state-space restoration blocks, restoration output, or reconstruction-guided target recovery.
4. What part is threatened? Generic degradation robustness, clean/degraded feature learning, low-pass residual handling, and response-map fusion.
5. What must be added or emphasized? Restoration-oriented Mamba feature recovery with tracking-supervised localization/matching evidence beyond InvTrack-style invariance.
6. Distinguishing sentence: Unlike InvTrack's degradation-invariant feature consistency and response-map fusion, our work studies restoration-oriented Mamba recovery for target-discriminative RGB template-search matching under generic degradation.
7. Novelty risk level: high.

Evidence: InvTrack pp. 7, 8, 10, 12, 14, 15, 16; degradation matrix marks degradation-invariant learning and degradation-aware response-map fusion as covered by InvTrack.

### 2. MambaIR

1. Does this paper already solve the selected idea? No.
2. What is similar? Restoration-oriented Mamba, residual state-space blocks, local enhancement, channel attention, and low-level degradation recovery.
3. What is different? MambaIR is image restoration, not visual tracking; it does not report template-search matching, tracking heads, target localization, or response maps.
4. What part is threatened? Any broad claim about restoration-oriented Mamba or Mamba for degraded images.
5. What must be added or emphasized? Tracking-aware objectives and localization/matching evaluation.
6. Distinguishing sentence: Unlike MambaIR, which restores images on restoration benchmarks, our work evaluates restoration-oriented Mamba inside RGB template-search tracking with target localization as the criterion.
7. Novelty risk level: high.

Evidence: MambaIR pp. 1, 3, 6, 7, 8, 9, 13, 14; paper matrix marks tracking-specific fields as not reported.

### 3. MambaIRv2

1. Does this paper already solve the selected idea? No.
2. What is similar? Attentive state-space restoration, ASE, SGN, and restoration for degraded images.
3. What is different? MambaIRv2 does not report visual tracking, template-search matching, target localization, or tracking losses.
4. What part is threatened? Any claim around attentive restoration Mamba or semantic-neighboring restoration.
5. What must be added or emphasized? Template-search tracking adaptation and matching/localization evidence.
6. Distinguishing sentence: Unlike MambaIRv2's attentive restoration for image reconstruction, our work studies whether restoration-oriented state-space modeling can recover target-discriminative template/search representations for RGB tracking.
7. Novelty risk level: high.

Evidence: MambaIRv2 pp. 1, 2, 3, 4, 5, 8; missing-intersection matrix marks `Tracking-aware restoration / Image restoration` as weakly studied because tracking objectives are not included.

### 4. MambaLCT

1. Does this paper already solve the selected idea? No.
2. What is similar? RGB-style template-search tracking and Mamba hidden-state context over video.
3. What is different? MambaLCT focuses on long-term context, not restoration or explicit degradation recovery.
4. What part is threatened? Broad claims about Mamba temporal context in tracking.
5. What must be added or emphasized? Restoration-guided recovery under image degradation, not temporal context alone.
6. Distinguishing sentence: Unlike MambaLCT's long-term context modeling, our work focuses on restoration-guided recovery of degraded RGB template/search representations for localization.
7. Novelty risk level: medium.

Evidence: MambaLCT pp. 2, 4, 5, 7; degradation matrix notes attribute evidence but no degradation-specific restoration.

### 5. MCITrack

1. Does this paper already solve the selected idea? No.
2. What is similar? Video-level RGB tracking, Mamba hidden states, context memory, and reliable-frame memory bank.
3. What is different? MCITrack does not report image restoration, explicit degradation handling, or degradation-aware template/search recovery.
4. What part is threatened? Mamba memory/context and reliable update claims.
5. What must be added or emphasized? Restoration-oriented degradation recovery and tracking-supervised feature matching.
6. Distinguishing sentence: Unlike MCITrack's contextual-information memory, our work targets restoration-aware recovery of degraded RGB template/search features rather than video-level context transmission.
7. Novelty risk level: medium.

Evidence: MCITrack pp. 1, 3, 4, 5, 6, 7; paper matrix marks restoration and degradation handling as not reported.

### 6. TemTrack

1. Does this paper already solve the selected idea? No.
2. What is similar? RGB-style template-search tracking and Mamba temporal token modeling.
3. What is different? TemTrack uses historical track tokens and does not report restoration, degradation generation, or degradation-aware matching.
4. What part is threatened? Claims about Mamba for temporal target representation in tracking.
5. What must be added or emphasized? Generic degraded RGB recovery and localization reliability.
6. Distinguishing sentence: Unlike TemTrack's Mamba-based temporal token learning, our work studies restoration-oriented recovery for degraded template-search matching.
7. Novelty risk level: medium.

Evidence: TemTrack pp. 2, 3, 4, 5; degradation matrix marks restoration and degradation-aware update as not reported.

### 7. SMTrack

1. Does this paper already solve the selected idea? No, but it is a serious partial threat.
2. What is similar? RGB SOT, Mamba/SSM-style hidden states, scanned templates, dynamic template update, and template degradation analysis.
3. What is different? SMTrack does not report restoration/enhancement, generic synthetic degradation training, or restoration-guided feature recovery.
4. What part is threatened? Memory, template update, target-aware scanning, and template degradation claims.
5. What must be added or emphasized? Restoration-oriented recovery under generic degradation and comparisons against SMTrack-style memory/update.
6. Distinguishing sentence: Unlike SMTrack's temporal hidden-state template memory, our work studies restoration-oriented Mamba recovery for degraded RGB template/search matching.
7. Novelty risk level: high.

Evidence: SMTrack pp. 6, 7, 10, 11; missing-intersection matrix marks degradation-aware memory/template update as weakly studied but reliability-controlled memory update as partially studied.

### 8. MambaTrack Night UAV

1. Does this paper already solve the selected idea? Partially for low-light/night tracking, not for generic degradation.
2. What is similar? Mamba-based low-light enhancer, cropped template/search regions, tracking head, and response visualizations.
3. What is different? It is night UAV vision-language tracking and focuses on low light rather than generic RGB degradation.
4. What part is threatened? Mamba enhancement inside tracking and low-light restoration-guided template-search claims.
5. What must be added or emphasized? Generic degradation beyond low light, RGB-only/language-free setting, and direct comparison on low-light subsets.
6. Distinguishing sentence: Unlike MambaTrack Night UAV's language-assisted low-light enhancement, our work studies generic RGB degradation including blur, resolution loss, noise, and compression in template-search tracking.
7. Novelty risk level: high.

Evidence: MambaTrack Night UAV pp. 1, 2, 3, 4; missing-intersection matrix marks nighttime/vision-language restoration-aware Mamba as partially studied.

### 9. MambaNUT

1. Does this paper already solve the selected idea? No.
2. What is similar? RGB SOT, Vision Mamba backbone, template-search tokens, nighttime degradation, and adaptive curriculum.
3. What is different? MambaNUT does not use image restoration/enhancement and is nighttime/low-light focused rather than generic degradation focused.
4. What part is threatened? Nighttime RGB tracking and curriculum learning claims.
5. What must be added or emphasized? Restoration-guided recovery and general degradation beyond low contrast/brightness/SNR.
6. Distinguishing sentence: Unlike MambaNUT's curriculum-based nighttime RGB tracking, our work studies restoration-oriented Mamba recovery for generic degraded RGB template-search matching.
7. Novelty risk level: medium.

Evidence: MambaNUT pp. 1, 2, 3, 4, 5, 6, 7; degradation matrix marks low light `Yes`, image-level restoration `No`, and restoration-guided template-search matching `Not reported`.

### 10. MambaVT

1. Does this paper already solve the selected idea? No.
2. What is similar? Single-object tracking, Mamba spatio-temporal context, template memory, dynamic template selection, and adverse-condition attributes.
3. What is different? MambaVT is RGB-T tracking using thermal infrared and context modeling, not RGB-only restoration.
4. What part is threatened? Dynamic template memory, multimodal robustness, and low-illumination robustness claims.
5. What must be added or emphasized? RGB-only restoration-guided recovery without thermal input.
6. Distinguishing sentence: Unlike MambaVT's RGB-T contextual tracking with thermal cues, our work studies RGB-only restoration-guided template-search matching under image degradation.
7. Novelty risk level: medium.

Evidence: MambaVT pp. 1, 2, 3, 4, 5, 6, 7, 10; paper matrix marks restoration/enhancement as not reported.

### 11. MambaEVT

1. Does this paper already solve the selected idea? No.
2. What is similar? Mamba tracking, dynamic template generation, memory, response maps, and adverse-condition robustness.
3. What is different? MambaEVT is event-only tracking, not RGB image restoration or RGB template-search degradation recovery.
4. What part is threatened? Dynamic template Memory Mamba and adverse-condition tracking claims.
5. What must be added or emphasized? RGB-only degraded image recovery and restoration-guided matching.
6. Distinguishing sentence: Unlike MambaEVT's event-only Memory Mamba tracker, our work targets restoration-guided RGB template-search matching under image-quality degradation.
7. Novelty risk level: medium.

Evidence: MambaEVT pp. 1, 2, 3, 4, 5, 6, 7, 11, 12; degradation matrix marks image-level restoration and restoration-guided matching as not reported.

### 12. MamTrack

1. Does this paper already solve the selected idea? No, but it threatens target-aware scanning and multimodal tracking claims.
2. What is similar? Template-search tracking, Target-Aware Scan, Mamba fusion, historical modeling, and score-map tracking head.
3. What is different? MamTrack uses RGB-event inputs and multimodal fusion rather than RGB-only restoration.
4. What part is threatened? Target-aware scan, template-search interaction, historical Mamba modeling, and adverse-condition robustness via events.
5. What must be added or emphasized? Restoration-aware RGB-only degradation recovery and not merely target-aware scanning.
6. Distinguishing sentence: Unlike MamTrack's RGB-event Target-Aware Scan and multimodal fusion, our work studies restoration-oriented RGB-only recovery for degraded template-search matching.
7. Novelty risk level: medium.

Evidence: MamTrack pp. 1, 2, 3, 4, 5, 6, 7, 8; paper card notes no restoration/enhancement and robustness from event cues/fusion.

### 13. Mamba-FETrack

1. Does this paper already solve the selected idea? No.
2. What is similar? RGB-event tracking, Mamba feature extraction/fusion, adverse-condition motivation, and template/search tracking.
3. What is different? Robustness comes from event sensing and multimodal fusion, not RGB-only restoration-oriented Mamba.
4. What part is threatened? Adverse-condition Mamba tracking and multimodal robustness claims.
5. What must be added or emphasized? RGB-only degradation recovery without event input.
6. Distinguishing sentence: Unlike Mamba-FETrack's RGB-event fusion, our work studies restoration-guided recovery from degraded RGB template/search observations without extra event cues.
7. Novelty risk level: medium.

Evidence: Mamba-FETrack pp. 1, 2, 3, 6, 7, 8, 9, 10, 11, 12, 13, 15; paper matrix marks restoration/enhancement as not reported.

### 14. MambaTrack MOT

1. Does this paper already solve the selected idea? No.
2. What is similar? Mamba tracking and robustness discussion around occlusion/motion blur.
3. What is different? It is MOT tracking-by-detection with trajectory motion prediction and tracklet patching, not RGB SOT template-search restoration.
4. What part is threatened? Broad motion blur or Mamba tracking claims.
5. What must be added or emphasized? SOT template-search visual feature recovery rather than trajectory patching.
6. Distinguishing sentence: Unlike MambaTrack MOT's trajectory-level motion prediction and tracklet patching, our work studies degraded RGB template-search feature recovery for single-object localization.
7. Novelty risk level: low.

Evidence: MambaTrack MOT pp. 1, 2, 3, 4, 5, 6, 8; degradation matrix notes blur/occlusion are handled through trajectory patching and association, not restoration.

### 15. MambaMOT

1. Does this paper already solve the selected idea? No.
2. What is similar? Mamba hidden-state sequence modeling for tracking.
3. What is different? It operates on bounding-box trajectories for MOT, not RGB template-search visual features.
4. What part is threatened? Mamba motion prediction and temporal hidden-state claims.
5. What must be added or emphasized? Image-level/feature-level recovery of degraded RGB observations for SOT.
6. Distinguishing sentence: Unlike MambaMOT's trajectory-sequence motion prediction, our work targets restoration-guided visual matching in RGB template-search tracking.
7. Novelty risk level: low.

Evidence: MambaMOT pp. 1, 2, 3, 4; paper matrix marks visual degradation/restoration as not reported.

### 16. MM-Tracker

1. Does this paper already solve the selected idea? No.
2. What is similar? Mamba tracking, UAV video, motion blur discussion, and degradation-aware feature/detection handling.
3. What is different? MM-Tracker handles motion blur through detector supervision, Motion Mamba, motion maps, and MOT association, not restoration-guided RGB template-search matching.
4. What part is threatened? Broad motion blur and degradation-aware Mamba claims.
5. What must be added or emphasized? Generic RGB degradation recovery and SOT template-search matching, not motion-map detection.
6. Distinguishing sentence: Unlike MM-Tracker's Motion Mamba for UAV MOT detection and motion modeling, our work studies restoration-guided RGB SOT matching under image degradation.
7. Novelty risk level: medium.

Evidence: MM-Tracker pp. 1, 3, 4, 5, 6; degradation matrix marks motion blur `Yes` but restoration-guided template-search matching as not reported.

### 17. SportMamba

1. Does this paper already solve the selected idea? No.
2. What is similar? Mamba tracking, motion blur/occlusion discussion, temporal memory, and dynamic EMA feature updating.
3. What is different? SportMamba is sports MOT with motion prediction, ReID/association, and EMA updates, not RGB SOT restoration.
4. What part is threatened? Broad blur/occlusion and motion prediction claims.
5. What must be added or emphasized? Degraded visual feature recovery for template-search localization.
6. Distinguishing sentence: Unlike SportMamba's MOT motion prediction and association under sports-video blur, our work studies restoration-guided RGB template-search localization under degradation.
7. Novelty risk level: low.

Evidence: SportMamba pp. 1, 3, 4, 6, 8; paper card explicitly notes severe blur remains a limitation but no image restoration is reported.

### 18. Multi-State Tracker

1. Does this paper already solve the selected idea? No, but it partially threatens feature-recovery wording.
2. What is similar? RGB SOT, Mamba/SSM-style efficient feature-state modeling, feature enhancement, response-map inference, and robustness to tracking attributes.
3. What is different? Multi-State Tracker models general target feature states, not restoration-oriented Mamba recovery or explicit degradation-state restoration.
4. What part is threatened? Feature enhancement, multi-state representation, and RGB attribute robustness claims.
5. What must be added or emphasized? Restoration-specific recovery under measured degradation and tracking-aware matching evidence.
6. Distinguishing sentence: Unlike Multi-State Tracker's feature-state enhancement, our work studies restoration-oriented Mamba recovery for degraded RGB template/search matching.
7. Novelty risk level: medium.

Evidence: Multi-State Tracker pp. 1, 2, 4, 5, 7, 8; degradation matrix marks feature-level restoration as partial but image-level restoration and degradation-aware updates as not reported.

### 19. HyMamba

1. Does this paper already solve the selected idea? No.
2. What is similar? Mamba tracking, hidden states, dynamic templates, feature enhancement, and adverse-condition attribute robustness.
3. What is different? HyMamba is hyperspectral tracking with spectral hidden-state modeling, not RGB-only restoration.
4. What part is threatened? Dynamic templates, hidden states, and feature enhancement outside RGB.
5. What must be added or emphasized? RGB-only generic degradation recovery without hyperspectral cues.
6. Distinguishing sentence: Unlike HyMamba's hyperspectral hidden-state feature enhancement, our work targets restoration-guided RGB template-search tracking under image degradation.
7. Novelty risk level: medium.

Evidence: HyMamba pp. 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11; paper matrix states it does not solve RGB-only degradation-robust tracking.

### 20. All-Day MCMT

1. Does this paper already solve the selected idea? No.
2. What is similar? Low-light/all-day tracking and Mamba-based visible/infrared feature fusion.
3. What is different? It is multi-camera multi-target tracking with RGBT/infrared fusion, not RGB-only SOT or restoration.
4. What part is threatened? Low-light/all-day robustness and Mamba multimodal fusion claims.
5. What must be added or emphasized? RGB-only template-search restoration under generic degradation.
6. Distinguishing sentence: Unlike All-Day MCMT's RGBT fusion for low-light multi-camera tracking, our work studies RGB-only restoration-guided template-search matching under generic image degradation.
7. Novelty risk level: medium.

Evidence: All-Day MCMT pp. 1, 2, 3, 4, 5, 6, 7, 8; paper matrix marks restoration/enhancement as `No` and template-search response maps as not reported.

## Files created or modified

- `reports/04_novelty_danger_check.md`

## How the output was verified

- Identified TAR-MambaTrack as the selected best idea from `reports/04_top_paper_ideas.md`.
- Cross-checked the novelty framing against `reports/02_gap_analysis.md`, `reports/03_reviewer_attack.md`, and `reports/03b_subagent_review.md`.
- Used `tables/paper_matrix.csv`, `tables/mamba_usage_matrix.csv`, `tables/degradation_matrix.csv`, `tables/missing_intersection_matrix.csv`, and the paper cards for evidence references.
- Confirmed every requested comparison paper is included.
- Confirmed the report does not create an experiment plan, method architecture, final paper plan, or `gap_scorecard.csv`.

## Uncertain fields

- External literature beyond the uploaded paper set was not assessed.
- Some differences are inferred from `not reported` fields rather than explicit author-stated limitations.
- Real-world mixed-degradation RGB SOT data availability remains uncertain.
- The final risk level can change if direct experiments show that MambaIR/MambaIRv2 pre-processing plus InvTrack already matches the selected idea.

## Should the selected idea proceed to experiment planning?

Yes, but only with **risky novelty** status. It should proceed to experiment planning only if the plan includes direct comparisons against InvTrack, MambaIR/MambaIRv2 pre-processing, MambaTrack Night UAV, MambaNUT, SMTrack, Multi-State Tracker, and strong RGB SOT baselines, and only if the experiments separate restoration benefit from Mamba benefit and tracking-supervised benefit.
