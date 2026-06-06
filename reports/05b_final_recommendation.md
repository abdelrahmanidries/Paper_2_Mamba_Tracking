# Final Recommendation and Gap Scorecard Summary

Purpose: create a final scorecard and recommend the best direction for the second paper. This report does not define a full method architecture, final paper plan, related work, or implementation details beyond the minimum proof-of-concept modules requested.

## Scoring method

The scorecard in `tables/gap_scorecard.csv` uses a risk-adjusted weighted score, not a simple average.

Positive weights emphasize novelty, importance, difference from InvTrack, difference from existing Mamba trackers, experimental clarity, feasibility, publication potential, connection to MambaIR/MambaIRv2, dataset availability, baseline availability, and ablation clarity.

Negative penalties are applied for reviewer risk, implementation difficulty, simple-combination risk, closeness to InvTrack, closeness to MambaIR/MambaIRv2, and closeness to night UAV Mamba trackers. This makes the top score conservative: the best idea remains risky, but it is still the strongest direction.

## 1. Executive summary

Best final paper direction: **Tracking-Aware Restoration Mamba for Degradation-Robust RGB Template-Search Tracking**.

Recommended acronym: **TAR-MambaTrack**.

Decision: **proceed with caution**.

The selected direction is strongest because it matches the final refined gap from `reports/03b_subagent_review.md`: restoration-oriented Mamba is established for image restoration, degradation-invariant RGB template-search tracking is partially addressed without Mamba restoration, and existing Mamba trackers mainly focus on temporal context, memory, dynamic templates, multimodal fusion, motion prediction, efficient backbones, low-light/night tracking, or sensor-assisted robustness.

The novelty is not safe in a broad form. InvTrack, MambaIR, MambaIRv2, MambaTrack Night UAV, and SMTrack are strong threats. The idea remains defensible only if the paper focuses on tracking-aware restoration-oriented Mamba for generic degraded RGB template-search matching, evaluated by target localization and matching reliability rather than image quality alone.

## 2. Ranked idea list

1. **TAR-MambaTrack**: Tracking-Aware Restoration Mamba for Degraded RGB Template-Search Tracking.
   - Overall score: 55.0.
   - Recommended action: proceed with caution as the main direction.
   - Why: It is the only idea that combines strong importance, direct connection to MambaIR/MambaIRv2, high experimental clarity, and the final reviewer-supported gap. Its risk comes from being close to InvTrack plus MambaIR/MambaIRv2 unless the tracking-aware part is proven.

2. **DAMU-Track**: Degradation-Aware Memory and Template Update for Restoration-Guided RGB Mamba Tracking.
   - Overall score: 51.2.
   - Recommended action: use as backup or secondary claim.
   - Why: It is clearly different from InvTrack and MambaIR/MambaIRv2, but it is close to SMTrack, MCITrack, MambaVT, MambaEVT, and HyMamba. It should be used only if degraded-frame memory contamination is demonstrated.

3. **ReCoR-Track**: Restoration-Conditioned Response Reliability for Degraded RGB Template-Search Tracking.
   - Overall score: 37.0.
   - Recommended action: postpone as standalone; merge as an analysis component.
   - Why: Response reliability is useful and experimentally clear, but InvTrack already strongly covers degradation-aware response-map fusion. This idea is better as an analysis section inside TAR-MambaTrack.

## 3. Best main idea

1. Recommended title: Tracking-Aware Restoration Mamba for Degradation-Robust RGB Template-Search Tracking.
2. Recommended acronym: TAR-MambaTrack.
3. One-sentence novelty: We study whether restoration-oriented Mamba can be adapted from image restoration to RGB template-search tracking by recovering target-discriminative representations under generic degradation and validating the effect on localization and matching reliability.
4. Final gap statement: Within the reviewed evidence set, restoration-oriented Mamba is established for image restoration, while degradation-invariant RGB template-search tracking is partially addressed without Mamba restoration. The underexplored intersection is tracking-aware restoration-oriented Mamba for generic degraded RGB template-search matching.
5. Why this is the strongest idea: It is the only candidate that directly connects MambaIR/MambaIRv2 restoration evidence, InvTrack's degradation-tracking threat, and the tracking-specific need for template-search localization under degraded observations.
6. Why it is different from InvTrack: InvTrack uses degradation-invariant learning, clean/degraded consistency, low-pass residual modules, and response-map fusion; the selected idea must use restoration-oriented Mamba recovery with tracking-supervised matching/localization evidence.
7. Why it is different from MambaIR and MambaIRv2: MambaIR/MambaIRv2 restore images, while the selected idea must evaluate restored or recovered representations inside template-search tracking with tracking losses and tracking metrics.
8. Why it is different from temporal/context Mamba trackers: MambaLCT, MCITrack, TemTrack, and SMTrack focus on temporal context, hidden states, track tokens, memory, or dynamic template states. TAR-MambaTrack must focus on restoration-guided degradation recovery rather than Mamba memory.
9. Why it is different from night UAV Mamba trackers: MambaTrack Night UAV and MambaNUT address low-light/night UAV tracking. TAR-MambaTrack must cover generic RGB degradation beyond low light, including blur, low resolution, noise, JPEG compression, and mixed degradation.
10. Why it is experimentally testable: `reports/05_experiment_plan.md` defines direct tests against InvTrack, MambaIR/MambaIRv2 pre-processing, MambaTrack Night UAV, MambaNUT, SMTrack/MCITrack, standard RGB trackers, and controlled degradation protocols.
11. Main risk: The work can be criticized as a simple combination of MambaIR/MambaIRv2 and InvTrack.
12. How to reduce that risk: Use direct threat baselines, tracking-supervised restoration objectives, template/search asymmetry tests, Mamba-vs-non-Mamba restoration controls, and response/localization evidence rather than image-quality metrics alone.

## 4. Best backup idea

Best backup: **DAMU-Track**, degradation-aware memory and template update for RGB Mamba trackers.

Use this idea instead if early experiments show that the restoration-guided main idea does not beat InvTrack or MambaIR/MambaIRv2 pre-processing, but degraded-frame memory contamination is clearly visible in RGB Mamba trackers such as SMTrack or MCITrack.

This idea is safer against InvTrack because InvTrack does not report temporal memory or dynamic template update. It is less safe against existing Mamba trackers because SMTrack, MCITrack, MambaVT, MambaEVT, and HyMamba already cover memory, hidden states, dynamic templates, or reliability-like updates.

## 5. Idea to avoid or postpone

Postpone **ReCoR-Track** as a standalone paper idea.

Response-map and matching reliability analysis should be included inside the main paper, but it is too close to InvTrack if framed as the main novelty. InvTrack already computes and fuses clean/degraded response maps and is the direct threat for degradation-aware response-map fusion.

## 6. Minimum modules needed for first implementation

These are proof-of-concept modules only, not a full method architecture:

1. Baseline RGB template-search tracker.
2. Restoration-oriented Mamba feature recovery block inserted at a feature level or template/search representation level.
3. Tracking head using standard classification and box-regression losses.
4. Synthetic degradation loader for template/search pairs.
5. Comparison path for external restoration pre-processing, especially MambaIR/MambaIRv2 plus the same tracker.
6. Response-map or matching-reliability logging for visualization and analysis.

Minimum principle: keep the first implementation small enough to answer whether restoration-oriented Mamba improves degraded template-search localization beyond vanilla tracking and external restoration pre-processing.

## 7. Optional modules for final paper

Add these only after the main proof is positive:

1. Degradation-aware memory or template update.
2. Response-map fusion or restoration-conditioned response selection.
3. Degradation token or degradation prompt.
4. Template-guided attentive scan.
5. Degradation curriculum.
6. Real-degradation adaptation or domain-mixing strategy.
7. Efficiency-optimized lightweight restoration block.

These modules should not be added before the core claim is verified, because each one adds reviewer risk and makes the source of improvement harder to isolate.

## 8. Top novelty threats

1. **InvTrack**
   - Threat: broad synthetic RGB degradation, clean/degraded consistency, low-pass residual modules, and response-map fusion.
   - Distinction: TAR-MambaTrack must use restoration-oriented Mamba recovery and tracking-supervised localization/matching evidence beyond invariant learning.

2. **MambaTrack Night UAV**
   - Threat: Mamba low-light enhancement on template/search crops inside a tracker.
   - Distinction: TAR-MambaTrack must address generic RGB degradation and not rely on language prompts or low-light-only evaluation.

3. **MambaIRv2**
   - Threat: attentive restoration-oriented Mamba, ASE, and SGN.
   - Distinction: TAR-MambaTrack must adapt restoration to template-search tracking and evaluate target localization, not image reconstruction alone.

4. **MambaIR**
   - Threat: restoration-oriented Mamba, residual state-space blocks, local enhancement, and channel attention.
   - Distinction: TAR-MambaTrack must show tracking-aware recovery of target-discriminative features.

5. **SMTrack**
   - Threat: RGB SOT hidden-state memory, dynamic template update, and template degradation awareness.
   - Distinction: TAR-MambaTrack must not claim memory novelty unless the update is degradation/restoration-aware and tested against SMTrack.

## 9. Final recommended research gap statement

Existing evidence shows restoration-oriented Mamba is well studied for image restoration, and degradation-invariant RGB template-search tracking is partially addressed without Mamba restoration. Existing Mamba trackers mainly study temporal context, hidden-state memory, dynamic template update, multimodal fusion, motion prediction, efficient tracking, low-light/night tracking, or sensor-assisted robustness. What remains underexplored in the reviewed set is tracking-aware restoration-oriented Mamba for generic degraded RGB template-search matching, where recovered representations are evaluated by target localization and matching reliability rather than image restoration quality alone.

## 10. Final recommended contribution statement

Possible contribution bullets:

1. We formulate generic degraded RGB template-search tracking as a tracking-aware restoration problem and evaluate restored or recovered representations by localization and matching reliability.
2. We study restoration-oriented Mamba recovery inside a template-search tracking pipeline and compare it against InvTrack-style invariant learning, MambaIR/MambaIRv2 pre-processing, and existing Mamba trackers.
3. We provide controlled degradation, template/search asymmetry, response-map, and efficiency analyses to distinguish tracking-aware restoration from image enhancement, temporal memory, multimodal robustness, and motion prediction.

## 11. Final recommended title options

1. Tracking-Aware Restoration Mamba for Degradation-Robust RGB Template-Search Tracking.
2. Restoration-Guided Mamba Tracking under Generic RGB Degradation.
3. TAR-MambaTrack: Tracking-Aware Restoration Mamba for Degraded RGB Object Tracking.
4. Restoring Target-Discriminative Features with Mamba for Degraded RGB Tracking.
5. From Image Restoration to Template-Search Tracking: Restoration-Oriented Mamba under RGB Degradation.

## 12. Decision

Decision: **proceed with caution**.

The idea should proceed because it is experimentally testable and best matches the final refined gap. It should not proceed as a broad novelty claim. The paper must be written and tested as a narrow, evidence-supported intersection: restoration-oriented Mamba plus generic degraded RGB template-search tracking, with direct comparisons to InvTrack, MambaIR/MambaIRv2 pre-processing, MambaTrack Night UAV, MambaNUT, SMTrack, and standard RGB trackers.

## Files created or modified

- `tables/gap_scorecard.csv`
- `reports/05b_final_recommendation.md`

## How the output was verified

- Read the selected idea and ranking from `reports/04_top_paper_ideas.md`.
- Used the novelty-risk judgment and required novelty ingredients from `reports/04_novelty_danger_check.md`.
- Cross-checked recommendations against `reports/02_gap_analysis.md`, `reports/03_reviewer_attack.md`, `reports/03b_subagent_review.md`, `reports/05_experiment_plan.md`, and the four matrices.
- Verified that all three proposed ideas are represented in `tables/gap_scorecard.csv`.
- Used a risk-adjusted weighted score rather than a simple average.
- Did not modify existing reports.
- Did not create method architecture, final paper plan, related work, or any file other than the requested scorecard and recommendation report.

## Uncertain fields

- The scores are reviewer-style research judgments, not empirical results.
- External literature beyond the uploaded paper set was not assessed.
- Public code availability for some baselines is uncertain.
- Real degraded RGB SOT dataset availability is uncertain.
- The final score can change after first experiments, especially if MambaIR/MambaIRv2 pre-processing plus InvTrack performs similarly.

## Whether the selected idea is ready for research-gap paragraph writing

Yes. The selected idea is ready for research-gap paragraph writing with cautious wording. The paragraph should emphasize that the intersection is underexplored in the reviewed evidence, not that related components are absent. It should explicitly distinguish image restoration from tracking-aware restoration, temporal memory from degradation-aware recovery, multimodal robustness from RGB-only robustness, motion prediction from degraded visual feature recovery, and low-light tracking from general degradation-robust tracking.
