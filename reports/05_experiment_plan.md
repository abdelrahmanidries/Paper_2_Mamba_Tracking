# Experiment Plan for TAR-MambaTrack

Selected idea from `reports/04_top_paper_ideas.md` and `reports/04_novelty_danger_check.md`: **TAR-MambaTrack**, or **Tracking-Aware Restoration Mamba for Degradation-Robust RGB Template-Search Tracking**.

Purpose: design experiments that can prove or falsify the selected research gap. This is not a method architecture, final paper plan, related-work section, or gap scorecard.

## 1. Main hypothesis

A restoration-guided Mamba tracker should improve RGB template-search tracking under general image-quality degradation by recovering target-discriminative representations, not merely by improving image appearance or adding a larger Mamba backbone.

The hypothesis is deliberately narrow. It does not claim novelty in Mamba tracking, low-light tracking, temporal memory, image restoration, or degradation-invariant tracking by itself. The target claim is that restoration-oriented Mamba can be adapted to RGB template-search matching and validated by localization and matching reliability under generic degradation.

Evidence motivation:

- InvTrack already covers degradation-invariant RGB template-search tracking without Mamba restoration, pp. 7, 8, 10, 12, 14-16.
- MambaIR and MambaIRv2 already cover restoration-oriented Mamba for image restoration, not tracking, MambaIR pp. 1, 3, 6-9, 13, 14; MambaIRv2 pp. 1-5, 8.
- MambaTrack Night UAV already covers Mamba low-light enhancement inside a template-search tracker, but only for low-light/night UAV vision-language tracking, pp. 1-4.

## 2. What the experiments must prove

1. The method improves RGB tracking under multiple degradations: motion blur, defocus blur, noise, low resolution, JPEG compression, low light, and mixed degradation.
2. The improvement is not only from using Mamba: compare against a vanilla Mamba tracker and a non-restoration Mamba variant.
3. The improvement is not only from image-level enhancement: compare against MambaIR/MambaIRv2 or other external restoration/enhancement pre-processing before the same tracker.
4. Restoration-guided feature modeling improves template-search matching: show better response reliability, fewer false peaks, and better localization under degraded template/search cases.
5. If memory/template update is included, degradation-aware update reduces drift: compare against no update, update-all, confidence-only update, and SMTrack/MCITrack-style update.
6. The method remains efficient enough for tracking: report FPS, FLOPs, parameters, and GPU memory against external restoration pre-processing and vanilla trackers.
7. The gain is not only from degradation training data: use matched training data and leave-one-degradation-out testing.
8. The method is distinct from InvTrack: directly compare against InvTrack and InvTrack-style degradation-invariant learning under the same degradation protocol.

## 3. Datasets

| Dataset | Use | Why it is useful | What it tests | Metrics |
|---|---|---|---|---|
| LaSOT | Train/test, or test if following standard protocol | Long-term RGB SOT with diverse attributes | Standard tracking, long sequences, drift under degradation overlays | Success/AUC, precision, normalized precision |
| GOT-10k | Train/test following official split if used | Standard generalization benchmark | Category generalization and degradation robustness under controlled corruptions | AO, SR0.5, SR0.75 |
| TrackingNet | Train/test if resources allow | Large-scale RGB tracking benchmark | Robustness at scale and compatibility with prior trackers | Success/AUC, precision, normalized precision |
| UAV123 | Test | UAV viewpoint, scale, fast motion, low resolution tendencies | UAV tracking under synthetic and natural difficulty | Success/AUC, precision |
| OTB100 | Lightweight test/debug | Small, fast benchmark for early sanity checks | Early degradation protocol validation and visualization | Success, precision |
| NfS | Test | High-frame-rate tracking benchmark; useful for motion/blur stress tests when degraded or downsampled | High-speed motion and frame-rate-related stress | Success/AUC, precision |
| AVisT | Test | Adverse visual tracking benchmark if available in the workspace/lab setup | Natural adverse factors, including occlusion, weather, illumination, blur-like difficulty | Success/AUC, precision, normalized precision where supported |
| UAVDark70 | Test if available | Dark UAV tracking | Night/low-light subset, comparison to MambaTrack Night UAV and MambaNUT | Success/AUC, precision |
| UAVDark135 | Test if available | Night UAV tracking used in related night-tracking context | Low-light/night robustness, but not general degradation alone | Success/AUC, precision |
| DarkTrack2021 | Test if available | Dark tracking benchmark candidate | Real low-light videos | Success/AUC, precision |
| NAT2021 | Test if available | Nighttime/adverse tracking candidate | Natural adverse tracking, especially night and low illumination | Success/AUC, precision |
| NAT2021L | Test if available | Larger nighttime/adverse tracking candidate | Longer or larger adverse-condition evaluation | Success/AUC, precision |

Dataset policy:

- Use LaSOT, GOT-10k, and TrackingNet for standard RGB SOT evidence.
- Use UAV123 and NfS for motion/UAV/high-speed stress.
- Use AVisT and night/adverse datasets for real adverse-condition evaluation, while clearly separating low-light results from generic degradation claims.
- Use OTB100 only for rapid first implementation and visualization, not as the main final evidence.
- Verify dataset licenses, splits, and evaluator compatibility before final experiments.

## 4. Synthetic degradation protocol

Synthetic degradation should be applied to RGB frames or crops after standard dataset loading, while preserving ground-truth boxes. Use fixed random seeds and report degradation type, severity, and whether it affects template, search, or both.

Template/search cases:

1. Degraded search only: clean initial template, degraded current search. This is common in tracking after a clean first frame.
2. Degraded template only: degraded initial template, clean search. This tests first-frame contamination.
3. Degraded template and search: both are degraded with the same type/severity.
4. Clean template but degraded search: same as search-only, reported explicitly because it is the common practical case.
5. Degraded template but clean search: same as template-only, reported explicitly because template contamination can persist.
6. Mismatched degradation: template and search have different degradation types or severities.

| Degradation | Mild | Medium | Severe | Apply to | Why it matters for tracking | How it tests the gap |
|---|---|---|---|---|---|---|
| Motion blur | short kernel, small angle variation | longer kernel, random direction | long kernel, strong directional blur | template, search, both, mismatched | Smears target edges and can shift response peaks | Tests target-discriminative recovery under motion-induced appearance loss |
| Defocus blur | small Gaussian/disk radius | medium radius | large radius | template, search, both | Removes high-frequency texture without directional motion cues | Separates generic blur recovery from motion prediction |
| Gaussian noise | low sigma | medium sigma | high sigma | template, search, both | Corrupts local appearance and feature activations | Tests denoising-style restoration in matching |
| Sensor noise | low Poisson/shot noise or signal-dependent noise | medium | severe | template, search, both | Simulates low-signal imaging, especially UAV/night cameras | Tests robustness beyond simple additive Gaussian noise |
| Low resolution | mild down/up-sampling | stronger down/up-sampling | very small effective target resolution | template, search, both | Removes target details and harms box localization | Tests whether restoration recovers discriminative structure |
| JPEG compression | high quality factor | medium quality factor | low quality factor | template, search, both | Introduces blocking/ringing artifacts that can confuse matching | Distinguishes from InvTrack's JPEG degradation with restoration-guided recovery |
| Low light | mild gamma/exposure reduction | strong darkening with noise | extreme darkening with color/noise artifacts | template, search, both | Tests low-light while separating from night-only papers | Must show generic degradation performance, not low-light-only novelty |
| Mixed degradation | two mild degradations | two/three medium degradations | severe mixture with random order | template, search, both, mismatched | Real videos often contain multiple artifacts | Tests generality beyond single corruption |

Severity implementation should be fixed before testing and not tuned on the test split. If using InvTrack-style synthetic degradations, document exact parameter ranges and include an InvTrack comparison under the same protocol.

## 5. Real degradation protocol

Real-degradation evaluation should be separate from synthetic evaluation because real degradations are not controlled, may co-occur, and may correlate with scene type or camera motion.

Real cases to include:

- Nighttime videos: UAVDark70, UAVDark135, DarkTrack2021, NAT2021/NAT2021L if available. Tests low-light and low-SNR tracking; cannot alone support generic degradation claims.
- UAV videos: UAV123 and dark UAV datasets. Tests scale changes, motion, camera shake, small targets, and practical aerial tracking.
- Low-frame-rate or high-speed videos: NfS or downsampled high-frame-rate sequences. Tests apparent motion, temporal discontinuity, and blur-like stress.
- Naturally blurred videos: AVisT or attribute-filtered benchmark subsets if available. Tests real motion/defocus blur without synthetic kernels.
- Compression/noisy videos: use available compressed/noisy video subsets if available; otherwise create a separate synthetic-compression study and label it synthetic.

Real versus synthetic distinction:

- Synthetic degradation gives controlled type/severity and causal claims.
- Real degradation tests external validity and reviewer concerns about artificial corruptions.
- Results should be reported separately and not mixed into a single score unless the protocol is clearly defined.

## 6. Baselines

### A. Standard RGB trackers

| Baseline | Why needed | Threat addressed | Conclusion supported |
|---|---|---|---|
| OSTrack | Strong RGB transformer tracker baseline | Shows performance against modern clean RGB tracking | Whether degradation-specific restoration adds value over strong SOT |
| MixFormer | Strong end-to-end tracking baseline | Guards against gains from weak baseline choice | Whether the method improves under degradation beyond generic tracking |
| SeqTrack | Sequence-style RGB tracker | Tests against sequence modeling without restoration | Whether restoration-guided recovery matters |
| TransT | Template-search transformer baseline | Historical template-search reference | Whether gains hold against established matching |
| Siamese tracker such as SiamRPN++/SiamFC-style baseline if needed | Lightweight/debug baseline | Helps response-map visualization and early proof-of-concept | Whether degradation effects are visible in classic matching |

### B. Mamba-based trackers

| Baseline | Why needed | Threat addressed | Conclusion supported |
|---|---|---|---|
| MambaLCT | Mamba temporal/context tracker | Mamba for long-term context | Improvement is not just temporal Mamba context |
| MCITrack | Mamba contextual memory tracker | Hidden-state memory and reliable-frame memory | Restoration differs from contextual memory |
| TemTrack | Mamba track-token temporal tracker | Temporal token modeling | Restoration differs from temporal token modeling |
| SMTrack | RGB SOT hidden-state/template memory threat | Dynamic template update and template degradation awareness | Restoration differs from state/template memory |
| TrackingMamba if available | Additional Mamba tracking baseline | Any broader Mamba tracking claim | Robustness is not merely from Mamba backbone |

### C. Degradation/adverse-condition trackers

| Baseline | Why needed | Threat addressed | Conclusion supported |
|---|---|---|---|
| InvTrack | Closest degradation-invariant RGB SOT threat | Generic synthetic degradation and response fusion | Proposed restoration-guided Mamba adds beyond invariant learning |
| MambaTrack Night UAV | Low-light Mamba enhancement in tracker | Low-light/night tracking novelty threat | Proposed method handles generic degradation beyond low light |
| MambaNUT | Nighttime RGB Vision Mamba curriculum | Night UAV and curriculum threat | Proposed method differs from low-light curriculum |
| Low-light/adverse trackers if available | Additional adverse-condition comparison | Low-light/adverse robustness | Avoids overstating night/adverse novelty |

### D. Restoration/enhancement baselines

| Baseline | Why needed | Threat addressed | Conclusion supported |
|---|---|---|---|
| Image-level restoration before tracker | Tests whether external pre-processing is enough | "Just restore image then track" criticism | Feature/tracking-aware restoration is necessary only if it beats this |
| MambaIR + tracker | Direct restoration-Mamba threat | MambaIR novelty threat | Tracking-aware adaptation beats generic restoration pre-processing |
| MambaIRv2 + tracker | Strong attentive restoration-Mamba threat | MambaIRv2 novelty threat | Tracking-aware adaptation beats attentive restoration pre-processing |
| Low-light enhancer + tracker | Low-light enhancement threat | MambaTrack Night UAV-like enhancement | Generic degradation result is not only low-light enhancement |

### E. Ablation baselines

| Baseline | Why needed | Threat addressed | Conclusion supported |
|---|---|---|---|
| Vanilla Mamba tracker | Controls for Mamba tracking backbone | "Gain is only Mamba" | Restoration component matters |
| Mamba tracker with no restoration block | Controls restoration contribution | Architecture size/backbone threat | Restoration-guided recovery matters |
| Restoration block without Mamba | Controls Mamba-specific restoration | "Any restoration block works" | State-space restoration matters if it wins |
| Full proposed method | Main comparison | All threats | Combined design must justify complexity |

## 7. Main comparison tables

Table 1: Standard tracking benchmark performance.

- Rows: Standard RGB trackers, Mamba trackers, degradation/adverse trackers where compatible, proposed method.
- Columns: LaSOT AUC/precision/normalized precision, GOT-10k AO/SR0.5/SR0.75, TrackingNet AUC/precision/normalized precision.
- Interpretation: The method should remain competitive on clean tracking. A large clean-performance drop would weaken the case even if degraded performance improves.

Table 2: Synthetic degradation benchmark performance.

- Rows: Same as Table 1 plus restoration-preprocessing baselines.
- Columns: degradation type by metric: motion blur, defocus blur, noise, sensor noise, low resolution, JPEG, low light; AUC/precision/normalized precision and robustness drop.
- Interpretation: Tests whether gains are broad and not low-light-only.

Table 3: Mixed degradation performance.

- Rows: InvTrack, MambaIR/MambaIRv2 pre-processing baselines, standard trackers, Mamba trackers, proposed method.
- Columns: mixed mild, mixed medium, mixed severe, random mixed, held-out mixed; AUC, precision, drop, relative robustness.
- Interpretation: Tests generic degradation robustness and generalization.

Table 4: Real adverse-condition tracking performance.

- Rows: standard trackers, MambaTrack Night UAV, MambaNUT, InvTrack if runnable, proposed method.
- Columns: UAVDark70/UAVDark135/DarkTrack/NAT/AVisT/UAV123/NfS as available; standard metrics.
- Interpretation: Tests whether synthetic gains transfer to real adverse video; low-light results are reported as low-light evidence, not generic-degradation proof.

Table 5: Efficiency comparison.

- Rows: vanilla tracker, tracker + MambaIR, tracker + MambaIRv2, tracker + low-light enhancer, feature-level restoration Mamba variant, full proposed method.
- Columns: FPS, FLOPs, parameters, GPU memory, input resolution, hardware.
- Interpretation: Shows whether the approach is tracking-feasible and whether feature-level restoration is more efficient than full image restoration pre-processing.

Table 6: Comparison against restoration-preprocessing baselines.

- Rows: no restoration, MambaIR + tracker, MambaIRv2 + tracker, low-light enhancer + tracker, non-Mamba restoration block + tracker, proposed tracking-aware variant.
- Columns: clean, each degradation type, mixed degradation, response reliability, PSNR/SSIM diagnostics.
- Interpretation: Separates tracking-aware restoration from generic image restoration.

## 8. Metrics

Tracking metrics:

- AUC / Success: main SOT success metric.
- Precision: center-location precision where benchmark supports it.
- Normalized Precision: scale-normalized location precision.
- AO for GOT-10k: official average overlap.
- SR0.5 and SR0.75 for GOT-10k: success rates at overlap thresholds.

Efficiency metrics:

- FPS: report with hardware and batch size 1.
- FLOPs: use consistent input sizes.
- Parameters: total learnable parameters.
- GPU memory: peak inference memory.

Matching and degradation metrics:

- Response-map sharpness or peak-to-sidelobe ratio: measures localization confidence.
- False-peak/distractor ratio: if distractor annotations or reliable heuristics are available.
- Robustness drop under degradation:

`Drop = Clean performance - Degraded performance`

Example: `Drop_AUC = AUC_clean - AUC_degraded`.

- Relative degradation robustness:

`Relative robustness = Degraded performance / Clean performance`

or

`Relative drop = (Clean performance - Degraded performance) / Clean performance`.

Interpretation:

- Lower drop is better if clean performance is comparable.
- Relative robustness is useful when clean baselines differ substantially.
- Do not use PSNR/SSIM as primary evidence; use them only to diagnose restoration behavior.

## 9. Cross-degradation generalization

Experiment 1: Train on blur, test on noise.

- Purpose: Test whether the method learns general recovery or overfits blur.
- Setup: Train with motion/defocus blur only; test on Gaussian/sensor noise and clean.
- Expected evidence: A smaller drop than baselines supports generalizable feature recovery, but failure would indicate degradation-specific overfitting.
- Conclusion supported: Restoration-guided modeling is not merely blur augmentation.

Experiment 2: Train on noise, test on JPEG.

- Purpose: Test artifact transfer across stochastic and compression degradation.
- Setup: Train with Gaussian/sensor noise; test JPEG compression at three severities.
- Expected evidence: Better robustness than no-restoration and image-preprocessing baselines would support generality.
- Conclusion supported: Learned recovery is not tied only to noise statistics.

Experiment 3: Train on single degradations, test on mixed degradation.

- Purpose: Test compositional robustness.
- Setup: Train on separate single degradations; test random mixtures.
- Expected evidence: Graceful degradation under mixed settings supports practical robustness.
- Conclusion supported: The method handles more than isolated synthetic corruptions.

Experiment 4: Leave-one-degradation-out training.

- Purpose: Strongest generalization test.
- Setup: Train on all but one degradation type; test on held-out type.
- Expected evidence: If held-out drop is smaller than baselines, the method learns useful restoration/matching priors.
- Conclusion supported: Robustness is not only from seeing the exact corruption.

## 10. Template/search degradation analysis

Experiment 1: Clean template + degraded search.

- Why important: Common real setting where first frame is acceptable and later frames degrade.
- Test: Current-frame recovery and matching robustness.

Experiment 2: Degraded template + clean search.

- Why important: Initial template contamination can persist through the whole sequence.
- Test: Whether restoration-guided template representation prevents long-term bias.

Experiment 3: Degraded template + degraded search.

- Why important: Hard condition where both reference and current observations are unreliable.
- Test: Whether recovery improves target/background separation.

Experiment 4: Different degradation in template and search.

- Why important: Real videos can have mismatched first-frame and later-frame degradation.
- Test: Whether matching remains stable when template and search distributions differ.

Report a grid: template condition by search condition, with AUC, precision, normalized precision, and response reliability.

## 11. Memory contamination experiment

The selected main idea does not require memory or template update. This experiment should be optional unless the final method includes online memory, dynamic templates, or update control.

If memory/update is included, evaluate:

1. Update memory with all frames.
2. Update memory only with confidence.
3. Update memory with degradation-aware reliability.
4. Update memory using restored features.
5. No memory update.

Evaluation:

- Drift rate after degraded intervals.
- Failure rate.
- Long-sequence AUC/success.
- Recovery time after degradation ends.
- Response-map stability before, during, and after degradation.

Threat addressed:

- SMTrack and MCITrack already cover memory/update. This experiment is needed only if the paper claims degradation-aware update as a contribution.

## 12. Response-map analysis

Purpose: show whether restoration-guided features improve template-search matching rather than only image appearance.

Experiments:

- Visualize response maps for clean input, degraded input, externally restored input, and proposed recovered features.
- Measure peak sharpness or peak-to-sidelobe ratio.
- Measure distractor suppression when similar objects are present.
- Compare clean response, degraded response, restored-feature response, and original/restored fused response.
- Show failure cases where restoration creates sharper wrong peaks.

Figures to include:

- Qualitative grid: template, degraded search, restored/recovered representation diagnostic, response maps, predicted box, ground truth.
- Degradation severity curves: response sharpness versus severity.
- Distractor examples: false response peak before and after restoration-guided modeling.
- Template/search asymmetry examples: degraded template versus degraded search.

## 13. Ablation studies

| Ablation | What it tests | Expected evidence needed | Reviewer criticism addressed |
|---|---|---|---|
| Without restoration-guided state-space block | Core restoration-Mamba contribution | Degraded performance and response reliability should drop if the block matters | "Gain is not from restoration Mamba" |
| Without local enhancement | Role of local detail recovery | Drop on blur/noise/low-resolution if local detail matters | "Local enhancement is unnecessary" |
| Without channel attention or channel selection | Role of channel filtering | Drop under noise/JPEG if corrupted channels matter | "Channel attention is just extra capacity" |
| Without degradation token or degradation prompt | Need for degradation awareness | Drop in mixed or held-out degradation if degradation conditioning matters | "The method is not degradation-aware" |
| Without template-guided attentive scan | Optional target-guided processing | Only include if used; drop should be in distractor/asymmetry cases | "Template-guided scan is an architecture trick" |
| Without degradation-aware memory update | Optional update component | Only include if memory is part of method; drift should increase under degraded intervals | "SMTrack/MCITrack already solve update" |
| Without response-map fusion | Role of matching-level fusion | Response/localization metrics should drop under mismatched template/search degradation | "InvTrack already covers response fusion" |
| Without degradation curriculum | Role of training schedule | Held-out/mixed robustness should drop if curriculum matters | "Gains come from training recipe" |
| Image-level restoration instead of feature-level restoration | Whether external restoration is enough | Feature-level/tracking-aware variant should beat or be more efficient than pre-processing | "MambaIR + tracker is enough" |
| Full model | Combined evidence | Should improve degradation robustness without unacceptable clean/efficiency drop | Overall novelty and utility |

## 14. Loss ablation

| Loss setup | What it proves |
|---|---|
| Tracking loss only | Baseline for whether degradation training alone helps without restoration-specific supervision |
| Tracking loss + clean-degraded feature consistency | Direct comparison to InvTrack-style invariance |
| Tracking loss + response consistency | Tests whether matching-level stability matters |
| Tracking loss + restoration-guided feature loss | Tests tracking-aware feature recovery beyond pure tracking loss |
| Tracking loss + memory reliability loss | Optional; tests degraded-frame update control if memory is included |
| Full loss | Tests whether combined objectives are necessary |

Loss ablations must use the same training data, model capacity as closely as possible, and degradation protocol. Otherwise reviewers can argue that differences come from data or parameter count.

## 15. Efficiency analysis

Compare:

1. Vanilla tracker.
2. Tracker + external image restoration model.
3. Tracker + proposed feature-level restoration Mamba.
4. Full model.

Metrics:

- FPS.
- FLOPs.
- Parameters.
- GPU memory.
- Input resolution and hardware.

Why feature-level restoration may be better than full image restoration:

- It may avoid reconstructing the whole image.
- It may focus computation on target-discriminative features.
- It may reduce latency compared with running a full restoration model before tracking.
- This is only a hypothesis; it must be verified by Table 5 and Table 6.

## 16. Failure case analysis

| Failure case | Why the method may fail | Visualization | Future-work note |
|---|---|---|---|
| Full occlusion | No visual evidence exists to restore | Show response collapse or distractor switch | Need occlusion reasoning or re-detection |
| Extreme low light | Signal may be too weak for feature recovery | Show dark search, recovered response, box drift | Need sensor/temporal cues or low-light-specific training |
| Severe motion blur | Target structure may be unrecoverable | Show elongated blur and broad response | Need motion-aware modeling or temporal fusion |
| Heavy compression | Blocking artifacts can create false textures | Show false peaks around artifacts | Need compression-aware training |
| Similar distractors | Restoration may sharpen distractors too | Show target/distractor response peaks | Need target-aware discrimination |
| Out-of-view | Restoration cannot recover absent target | Show high-confidence false localization | Need re-detection/out-of-view handling |
| Severe scale change | Restored features may not fix scale mismatch | Show box size errors | Need scale-specific modeling |
| Mixed degradation | Multiple artifacts may exceed training support | Show degradation stack and failure mode | Need better mixed-degradation generalization |

## 17. Minimum experiment set for first implementation

1. One standard benchmark: OTB100 or a small LaSOT validation subset for rapid iteration.
2. One synthetic degradation protocol: motion blur, Gaussian noise, low resolution, JPEG, and mixed medium severity on search-only and both template/search.
3. Three baselines:
   - Vanilla selected tracker without restoration.
   - MambaIRv2 or MambaIR pre-processing + same tracker.
   - InvTrack if runnable, or InvTrack-style clean/degraded consistency baseline if the code is not available.
4. Three ablations:
   - No restoration-guided block.
   - Non-Mamba restoration block.
   - Tracking loss only versus tracking + restoration-guided feature loss.
5. One response-map visualization:
   - Clean, degraded, restored/pre-processed, and proposed recovered-feature response maps on the same sequence.

Minimum success criterion:

- The prototype should show lower degradation robustness drop than the vanilla tracker and external restoration pre-processing on at least two degradation types, without a large clean-performance collapse. This is a proof-of-concept threshold, not a publishable claim.

## 18. Full experiment set for final paper

1. Standard clean benchmark comparison on LaSOT, GOT-10k, and TrackingNet if resources allow.
2. Synthetic single-degradation benchmark on LaSOT/GOT-10k/TrackingNet-style test splits.
3. Mixed-degradation benchmark with severity levels.
4. Template/search asymmetry analysis.
5. Cross-degradation generalization: blur-to-noise, noise-to-JPEG, single-to-mixed, leave-one-out.
6. Real adverse-condition evaluation on UAV123, NfS, AVisT, UAVDark70/UAVDark135, DarkTrack2021, NAT2021/NAT2021L as available.
7. Direct comparison with InvTrack.
8. Direct comparison with MambaIR/MambaIRv2 pre-processing.
9. Comparison with MambaTrack Night UAV and MambaNUT for low-light/night subsets.
10. Comparison with MambaLCT, MCITrack, TemTrack, and SMTrack for Mamba tracking threats.
11. Restoration module ablations.
12. Loss ablations.
13. Response-map analysis and visualization.
14. Optional memory contamination experiment if update/memory is included.
15. Efficiency comparison.
16. Failure case analysis.

## 19. Reviewer criticism and defense

| Criticism | Defense experiment |
|---|---|
| The idea is just MambaIR + tracker | Compare MambaIR/MambaIRv2 pre-processing against tracking-aware variant under identical degraded tracking metrics |
| The idea is just InvTrack + Mamba | Compare against InvTrack and InvTrack-style clean/degraded consistency; show restoration-guided recovery adds beyond invariant learning |
| Low-light Mamba trackers already exist | Include MambaTrack Night UAV and MambaNUT on low-light subsets; emphasize generic degradation beyond low light |
| Mamba temporal trackers already solve robustness | Compare MambaLCT, MCITrack, TemTrack, and SMTrack; show temporal/context memory is different from restoration-guided degradation recovery |
| External restoration preprocessing would be enough | Table 6: external restoration + tracker versus feature/tracking-aware restoration |
| Synthetic degradation is not realistic | Add real adverse-condition evaluation and clearly separate synthetic causal tests from real validity tests |
| The model is too heavy | Table 5 efficiency comparison against external restoration pre-processing and vanilla tracker |
| The improvement may come from training data, not the method | Matched training data, non-Mamba restoration control, vanilla Mamba control, and leave-one-degradation-out tests |
| PSNR/SSIM does not prove tracking | Use tracking metrics, response reliability, localization error, and degradation robustness drop as primary metrics |
| Response fusion is already InvTrack | Compare against InvTrack four-map fusion and show restoration-conditioned response behavior separately |

## 20. Final recommended experimental roadmap

Stage 1: Minimal proof-of-concept.

- Implement a small controlled degradation protocol.
- Run one standard benchmark or validation subset.
- Compare vanilla tracker, restoration pre-processing, and proposed restoration-guided variant.
- Produce one response-map visualization.

Stage 2: Full degradation evaluation.

- Run single-degradation and mixed-degradation benchmarks.
- Include template/search asymmetry.
- Report robustness drop and relative robustness.

Stage 3: Cross-degradation generalization.

- Run blur-to-noise, noise-to-JPEG, single-to-mixed, and leave-one-out protocols.
- Use matched training data to isolate method effect.

Stage 4: Ablation and visualization.

- Run module ablations, loss ablations, and response-map analysis.
- Add optional memory contamination experiment only if memory/update is part of the method.

Stage 5: Efficiency and final comparison.

- Compare FPS, FLOPs, parameters, and GPU memory.
- Run full baseline suite, including InvTrack, restoration-preprocessing baselines, Mamba trackers, low-light trackers, and standard RGB trackers.
- Add failure case analysis and real adverse-condition results.

## Files created or modified

- `reports/05_experiment_plan.md`

## How the output was verified

- Identified TAR-MambaTrack as the selected best idea from `reports/04_top_paper_ideas.md`.
- Used `reports/04_novelty_danger_check.md` to anchor novelty threats and required novelty ingredients.
- Cross-checked major threats and evidence against `reports/02_gap_analysis.md`, `reports/03_reviewer_attack.md`, `reports/03b_subagent_review.md`, the four matrices, and paper cards.
- Confirmed every experiment connects to a specific gap or novelty threat: InvTrack, MambaIR/MambaIRv2, MambaTrack Night UAV, MambaNUT, SMTrack/MCITrack, external restoration, synthetic degradation realism, and efficiency.
- Did not create method architecture, final paper plan, related work, or `gap_scorecard.csv`.

## Uncertain fields

- Exact availability and licenses for UAVDark70, UAVDark135, DarkTrack2021, NAT2021, NAT2021L, and AVisT should be verified before implementation.
- Exact degradation parameter ranges should be finalized after a small sanity check to avoid unrealistic corruptions.
- Whether InvTrack, MambaTrack Night UAV, MambaNUT, SMTrack, and other baselines have runnable public code is not established here.
- Real compressed/noisy RGB SOT videos may be difficult to source; synthetic compression/noise may need to be the controlled evidence.
- Some optional experiments depend on whether memory/template update is included in the eventual method.

## Whether the selected idea is ready for method architecture design

Yes, conditionally. The selected idea is ready for method architecture design only if the architecture is explicitly built to satisfy the novelty ingredients in `reports/04_novelty_danger_check.md`: tracking-aware restoration objective, restoration-oriented Mamba recovery inside template-search matching, generic RGB degradation protocol, direct comparisons against InvTrack and MambaIR/MambaIRv2 pre-processing, template/search asymmetry testing, matching reliability evidence, and RGB-only framing.
