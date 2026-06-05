# Subagent Review of Candidate Research Gaps

Purpose: independently verify and refine the candidate gaps after the first reviewer attack. This report merges four read-only reviewer passes: restoration, tracking, degradation, and experiment. It does not propose a paper idea, method architecture, experiment plan, or gap scorecard.

## Executive Summary

All four reviewers converged on the same conclusion: the safest surviving gap is a merged, narrow gap around tracking-aware restoration-oriented Mamba for generic degraded RGB template-search matching.

The gap is defensible only with cautious wording. MambaIR and MambaIRv2 establish restoration-oriented Mamba for image restoration, but their paper cards do not report template-search tracking, target localization, tracking heads, temporal memory, dynamic template update, or response-map fusion. InvTrack establishes degradation-invariant RGB template-search tracking with synthetic blur, low resolution, noise, JPEG degradation, clean/degraded feature consistency, low-pass residual modules, and response-map fusion, but it does not report Mamba, restoration output, or reconstruction-guided recovery. MambaTrack Night UAV shows Mamba-based low-light enhancement inside a template-search tracker, but its scope is night UAV vision-language tracking rather than generic RGB degradation.

The strongest final direction is therefore not "use Mamba for tracking", not "handle low-light tracking", and not "use Mamba memory". The strongest direction is the underexplored intersection of restoration-oriented Mamba and generic degradation-robust RGB SOT, where success must be measured by target localization and matching reliability rather than image quality alone.

## Summary From Restoration Reviewer

Strongest gap: tracking-aware restoration-oriented Mamba for generic degraded RGB template-search matching.

The restoration reviewer found that MambaIR's RSSB/local enhancement/channel attention and MambaIRv2's ASSB/ASE/SGN are established for image restoration, but not directly adapted to RGB SOT template-search matching with target-localization objectives. The safe claim is that this transfer is underexplored or not systematically studied in the provided evidence, not that it is absent from all literature.

Restoration ideas clearly not transferred to tracking in the provided cards:

- MambaIR residual state-space restoration blocks as tracking-aware target recovery modules.
- MambaIR local enhancement and channel attention as template/search matching modules.
- MambaIRv2 attentive state-space equation as a target-localization mechanism.
- MambaIRv2 semantic-guided neighboring as a tracking-aware template-search restoration mechanism.
- Local-to-global restoration modeling evaluated by tracking response reliability rather than image reconstruction quality.

Restoration ideas partially similar to existing tracking methods:

- Multi-State Tracker reports feature-state enhancement, but not restoration output or restoration-oriented Mamba.
- SMTrack propagates template hidden states and considers template degradation, but not restoration.
- InvTrack uses clean/degraded feature consistency and low-pass residual modules, but not Mamba restoration.
- MambaTrack Night UAV uses a Mamba low-light enhancer on cropped template/search regions, but only for low-light/night UAV vision-language tracking.
- MamTrack has Target-Aware Scan for RGB-event template-search interaction, but not restoration-aware RGB-only degradation recovery.

Weakest restoration-inspired gap: template-guided attentive scanning as a standalone gap. It is too close to MambaIRv2 attentive restoration and MamTrack Target-Aware Scan unless tied to generic RGB degradation and tracking-aware restoration.

Papers that threaten novelty: InvTrack, MambaTrack Night UAV, SMTrack, Multi-State Tracker, MamTrack, MambaIR, and MambaIRv2.

Missing evidence:

- Existing RGB Mamba SOT trackers have not been shown to fail under generic degradation in the current evidence.
- MambaIR/MambaIRv2 pre-restoration has not been compared against InvTrack.
- Feature restoration is not yet clearly separated from feature enhancement, feature consistency, or hidden-state propagation.
- Real degraded RGB SOT evidence is thin.
- It is not yet proven that restoration preserves target-discriminative cues rather than only improving image quality.

Required proof conditions:

- Controlled RGB SOT degradation tests across blur, low resolution, noise, JPEG compression, low light, and mixed degradation.
- Asymmetric template/search degradation tests.
- Comparisons with InvTrack, MambaIR/MambaIRv2 pre-processing, MambaTrack Night UAV, MambaNUT, SMTrack, Multi-State Tracker, and strong RGB SOT baselines.
- Tracking metrics and response reliability, not PSNR/SSIM alone.

Final recommendation: keep one merged restoration gap. Treat response-map fusion, feature-level restoration, and evaluation protocol as supporting sub-gaps. Do not present ASE/SGN/template-guided scanning or RSSB/channel attention transfer as standalone novelty.

## Summary From Tracking Reviewer

Strongest gap: tracking-aware restoration-oriented Mamba for generic degraded RGB template-search matching.

The tracking reviewer emphasized that the gap is tracking-specific only when framed around SOT template-search matching, target localization, response quality, and degraded template/search asymmetry. Generic restoration modules or generic Mamba architecture changes are not enough.

Gaps that are truly tracking-specific:

- Tracking-aware restoration for template-search matching.
- Restoration-conditioned response or matching reliability under degradation.
- Degradation-aware memory/template update, but only as a secondary gap because SMTrack and MCITrack already threaten memory/update claims.
- Feature restoration only if it is evaluated by localization and matching, not image quality.

Gaps that look like generic architecture combinations:

- Template-guided attentive scanning as a standalone claim.
- Degradation-state modeling without a measurable state definition.
- General curriculum learning without held-out degradation proof.
- Evaluation protocol alone.
- Blur recovery as a standalone distinction from motion prediction.

Gaps that would improve localization or matching if proven:

- The merged main gap, because it targets degraded template/search matching directly.
- Restoration-conditioned response-map behavior, because localization depends on response peaks and target/background separation.
- Degradation-aware memory/template update, if degraded frames are shown to corrupt online memory or template states.

Gaps that would be hard to prove in tracking benchmarks:

- Template-guided attentive scanning, because scan guidance must be isolated from restoration and tracking-head changes.
- Degradation-state modeling, because degradation states need operational labels or estimates.
- Training/evaluation-only gaps, because they can look necessary but not novel.
- Blur-only claims, because MOT blur handling papers are not directly comparable to RGB SOT template-search tracking.

Papers that threaten novelty: InvTrack, MambaTrack Night UAV, MambaIR, MambaIRv2, SMTrack, Multi-State Tracker, MamTrack, MambaNUT, MambaTrack MOT, MM-Tracker, and SportMamba.

Missing evidence:

- Direct proof that restoration-oriented Mamba improves target localization.
- Comparisons against InvTrack plus MambaIR/MambaIRv2 pre-processing.
- Response-map evidence showing sharper peaks, fewer distractors, or better target/background separation.
- Controlled evidence that degraded frames contaminate Mamba memory/update.
- Clear definition of feature-level restoration distinct from feature enhancement or invariance.

Required proof conditions:

- RGB SOT benchmarks with controlled degradation.
- Clean-template/degraded-search, degraded-template/clean-search, both-degraded, and severity-shift settings.
- Tracking metrics such as AUC/success, precision, normalized precision, AO/SR where applicable, localization error, and response reliability.
- Baselines including InvTrack, MambaIR/MambaIRv2 pre-processing, MambaTrack Night UAV, SMTrack, MCITrack, Multi-State Tracker, MambaNUT, and strong non-Mamba RGB SOT trackers.

Final recommendation: keep one main gap judged by target localization and matching reliability. Keep degradation-aware memory/template update only as a secondary, risky gap if controlled evidence supports it. Downgrade or remove standalone Gaps 6-10 from the earlier report.

## Summary From Degradation Reviewer

Strongest gap: tracking-aware restoration-oriented Mamba for generic degraded RGB template-search matching.

The degradation reviewer found that this gap survives only if it is framed as generic RGB degradation: motion blur, low resolution, sensor noise, JPEG compression, mixed degradation, and possibly real degraded RGB video. A low-light-only claim is weak because low-light and night UAV tracking are already addressed by MambaTrack Night UAV and MambaNUT, and all-day/low-light settings are also covered through multimodal sensing in All-Day MCMT.

Gaps already partly covered by InvTrack:

- General RGB degradation robustness.
- Degradation-invariant learning.
- Clean/degraded feature consistency.
- Low-pass residual handling.
- Synthetic blur, low resolution, noise, and JPEG degradation.
- Degradation-aware response-map fusion.

Gaps already partly covered by low-light/night UAV papers:

- Low-light enhancement in tracking: MambaTrack Night UAV.
- Nighttime RGB tracking with Vision Mamba and adaptive curriculum: MambaNUT.
- Low-light/all-day tracking via RGBT infrared fusion: All-Day MCMT.

General degradation gaps rather than low-light-only gaps:

- Restoration-oriented Mamba for RGB template-search matching under blur, low resolution, noise, JPEG compression, and mixed degradation.
- Tracking-aware feature recovery evaluated by localization and matching reliability.
- Generic mixed-degradation evaluation, but only as support for the main gap.

Most defensible degradation gap: tracking-aware restoration-oriented Mamba for generic degraded RGB SOT, explicitly separated from InvTrack's invariant learning, MambaTrack/MambaNUT low-light scope, and multimodal robustness.

Papers that threaten novelty: InvTrack, MambaTrack Night UAV, MambaNUT, MambaIR, MambaIRv2, SMTrack, Multi-State Tracker, MM-Tracker, SportMamba, MamTrack, Mamba-FETrack, MambaVT, MambaEVT, HyMamba, and All-Day MCMT.

Missing evidence:

- No direct evidence that restoration-oriented Mamba improves localization beyond InvTrack-style invariance.
- No comparison against MambaIR/MambaIRv2 as pre-restoration baselines.
- No controlled proof that feature restoration is different from feature enhancement, feature consistency, or hidden-state propagation.
- Real-world mixed-degradation evidence is limited in the reviewed sources.
- Existing RGB Mamba SOT failure under blur/noise/JPEG/low resolution is inferred from missing reported experiments, not directly proven.

Required proof conditions:

- Controlled RGB SOT degradation benchmark covering motion blur, low resolution, sensor noise, JPEG compression, low light, and mixed degradation.
- Asymmetric template/search degradation and mixed severity.
- Baselines including InvTrack, MambaIR/MambaIRv2 pre-processing, MambaTrack Night UAV, MambaNUT, SMTrack, Multi-State Tracker, and strong non-Mamba RGB SOT.
- Ablations that separate image-level restoration, feature-level restoration, invariant learning, and no restoration.
- Tracking metrics and response reliability, not image-quality metrics alone.

Final recommendation: keep one merged main gap. Do not keep low-light-only, response-map-only, blur-only, curriculum-only, or template-guided scanning gaps as standalone claims.

## Summary From Experiment Reviewer

Strongest gap: merged Gap A, tracking-aware restoration-oriented Mamba for generic degraded RGB template-search matching.

The experiment reviewer found this gap has the clearest ablation path because it can compare no restoration, image restoration pre-processing, degradation-invariant learning, feature-level recovery, image-level recovery, and Mamba versus non-Mamba restoration controls under the same degraded template/search protocol.

Weakest gaps:

- Template-guided attentive scanning as a standalone gap, because it is mechanism-first and difficult to isolate.
- Blur recovery versus motion prediction as a standalone gap, because blur is better treated as one degradation case.
- Degradation-state modeling unless state definitions are operational and measurable.
- Training/evaluation protocol alone, because it supports validation but is weak as primary novelty.

Experiment required to prove each surviving gap:

- Main merged gap: controlled RGB SOT degradation protocol using InvTrack-style degradation categories, severity levels, mixed degradation, and asymmetric template/search corruption. Include real degraded videos or labeled real-degradation subsets if available.
- Degradation-aware memory/template update: long sequences with degraded intervals, comparing no update, update-all, confidence-only update, SMTrack-style update, MCITrack-style memory, and degradation/restoration-aware update. Required proof is post-degradation drift and recovery, not only average AUC.
- Restoration-conditioned response-map fusion: compare InvTrack four-map fusion, clean-only, degraded-only, restored-only, original/restored fusion, and no fusion under identical degradation.
- Training/evaluation support: show held-out degradation generalization against no degradation training, random degradation training, InvTrack-style synthetic training, nighttime curriculum, and mixed-degradation curriculum.
- Degradation-state control: requires explicit degradation type/severity labels and held-out degradation tests showing that state-conditioned decisions improve over invariant learning and feature-state models.

Baselines that most threaten each gap:

- Main merged gap: InvTrack, MambaIR/MambaIRv2 pre-processing, MambaTrack Night UAV, MambaNUT, SMTrack, MCITrack, Multi-State Tracker, and strong clean RGB SOT trackers.
- Memory/template update gap: SMTrack and MCITrack.
- Response-map gap: InvTrack.
- Training/curriculum gap: InvTrack and MambaNUT.
- Degradation-state gap: InvTrack, Multi-State Tracker, SMTrack, and MambaNUT.

Experimentally difficult or risky gaps:

- Template-guided attentive scanning.
- Degradation-state modeling.
- Blur-only distinction from MOT motion prediction.
- Evaluation-only gap.

Clearest ablation path: the merged main gap, provided the experiments separate restoration benefit, Mamba benefit, degradation-aware training benefit, and capacity/training-data effects.

Final recommendation: keep only the merged main gap as the primary experimentally provable gap. Keep degradation-aware memory/template update as a secondary claim only if memory contamination is demonstrated. Use response-map fusion as a component, not a headline. Treat training and evaluation as validation requirements, not standalone novelty.

## Final Ranked Gap List After Subagent Review

1. Tracking-aware restoration-oriented Mamba for generic degraded RGB template-search matching.
2. Degradation-aware memory/template update for RGB Mamba trackers, only if degraded-frame memory contamination is demonstrated.
3. Restoration-conditioned response-map or matching-reliability analysis under degraded template/search pairs, only as a component of the main gap.
4. Mixed-degradation training and evaluation protocol for RGB SOT, as validation support rather than primary novelty.
5. Degradation-state control for restoration/update decisions, only if degradation type/severity is operationally defined.

## Top 3 Recommended Gaps

1. Main gap: tracking-aware restoration-oriented Mamba for generic degraded RGB template-search matching.
2. Secondary gap: degradation-aware memory/template update for RGB Mamba trackers.
3. Supporting gap: restoration-conditioned response-map or matching reliability under degraded template/search pairs.

## Gaps To Merge

- Merge the original restoration-aware Mamba, feature-level restoration, tracking-aware restoration, restoration-guided template-search matching, and general RGB degradation robustness gaps into the main gap.
- Merge response-map fusion into the main gap as a matching/localization component.
- Merge curriculum and evaluation gaps into the validation requirements for the main gap.
- Merge blur-only analysis into the degradation protocol as one test case.
- Merge degradation-state modeling into the memory/update gap only if degradation state is measurable.

## Gaps To Avoid

- Template-guided attentive scanning as a standalone gap.
- Low-light-only restoration claims.
- Blur-only claims framed against MOT motion prediction.
- Evaluation-only gap.
- Curriculum-only gap.
- Response-map-only gap.
- Vague degradation-state modeling without measurable degradation state.
- Broad feature-restoration claims that do not distinguish restoration from feature enhancement, invariance, or hidden-state propagation.

## Main Novelty Threats

1. InvTrack: broad synthetic RGB degradation, degradation-invariant tracking, clean/degraded feature consistency, low-pass residual modules, and response-map fusion.
2. MambaTrack Night UAV: Mamba-based low-light enhancement on template/search crops inside a tracker.
3. MambaIRv2: attentive restoration-oriented Mamba, ASE, and SGN.
4. MambaIR: restoration-oriented Mamba, residual state-space restoration blocks, local enhancement, and channel attention.
5. SMTrack: RGB SOT hidden-state memory, dynamic template update, and template degradation awareness.

Secondary threats: MCITrack for contextual memory, Multi-State Tracker for feature-state enhancement, MambaNUT for nighttime curriculum, MamTrack for Target-Aware Scan and RGB-event template-search interaction, Mamba-FETrack/MambaVT/MambaEVT/HyMamba/All-Day MCMT for sensor-assisted or non-RGB adverse-condition robustness, and MambaTrack MOT/MM-Tracker/SportMamba for MOT motion/blur handling.

## Safest Final Gap Wording

Within the reviewed evidence set, restoration-oriented Mamba is established for image restoration, and degradation-invariant RGB template-search tracking is partially addressed without Mamba restoration. Existing Mamba trackers mainly use state-space modeling for temporal context, hidden-state memory, dynamic templates, multimodal fusion, motion prediction, efficient backbones, low-light/night tracking, or sensor-assisted robustness. The underexplored intersection is tracking-aware restoration-oriented Mamba for generic degraded RGB template-search matching, where recovered representations are evaluated by target localization and matching reliability rather than by image quality alone.

## Strongest Final Gap Statement

Tracking-aware restoration-oriented Mamba for generic degraded RGB template-search matching is not directly addressed by the reviewed papers: MambaIR and MambaIRv2 provide restoration-specific Mamba designs without tracking evaluation, InvTrack provides degradation-invariant RGB template-search tracking without Mamba restoration, and current Mamba trackers cover memory, context, dynamic templates, multimodal fusion, motion prediction, low-light/night settings, or sensor-assisted robustness rather than generic RGB restoration-guided matching.

## Files Created Or Modified

- `reports/03b_subagent_review.md`

## How The Output Was Verified

- Waited for all four requested reviewer agents to complete.
- Merged the completed outputs from the restoration, tracking, degradation, and experiment reviewers.
- Cross-checked the merged conclusions against `reports/02_gap_analysis.md`, `reports/03_reviewer_attack.md`, the four matrices, and the high-threat paper cards cited by the reviewers.
- Verified that the report keeps the distinctions required by the project: image restoration versus tracking-aware restoration, temporal memory versus degradation-aware memory, multimodal robustness versus RGB-only degradation robustness, motion prediction versus degraded visual recovery, and low-light tracking versus general degradation-robust tracking.
- Confirmed that no paper idea, method architecture, experiment plan, or `gap_scorecard.csv` was created.

## Uncertain Fields

- External literature beyond the uploaded papers was not assessed.
- Several limitations are implicit from task/method/evaluation scope rather than stated by authors.
- Real-world mixed-degradation RGB SOT availability is not established by the reviewed evidence.
- Exact baseline comparability is uncertain because some high-threat papers are SOT, some are MOT, and some use extra modalities.
- The final ranking is a conservative reviewer synthesis, not a quantitative scorecard.
