# Final Audit Report

## 1. Executive summary

Final judgment: **proceed with caution**.

The project is internally consistent. The workflow moves from evidence extraction, paper cards, matrices, missing-intersection analysis, gap generation, reviewer attacks, subagent review, novelty checking, experiment planning, method design, and complete paper planning. The selected idea is consistently framed as **Tracking-Aware Restoration Mamba for Degradation-Robust RGB Template-Search Tracking** / **TAR-MambaTrack**.

The selected paper idea is defensible but not safely novel in a broad form. The strongest novelty threats are InvTrack, MambaIR, MambaIRv2, MambaTrack Night UAV, MambaNUT, SMTrack, MamTrack, MambaEVT, MambaVT, and Multi-State Tracker. The idea remains defensible only if the paper focuses on the narrow intersection of restoration-oriented Mamba, tracking-aware feature recovery, RGB-only template-search matching, and generic image-quality degradation.

Novelty status: **risky but defensible**.

Implementation readiness: **ready for a minimal proof of concept**, not ready for a full multi-module implementation all at once.

Main remaining risks:

1. The method may be judged as InvTrack plus Mamba unless RG-SSB shows value beyond clean-degraded consistency and response-map fusion.
2. The method may be judged as MambaIR/MambaIRv2 plus tracker unless restoration is optimized and evaluated through tracking features, response maps, and localization.
3. Night UAV Mamba trackers partially threaten low-light/adverse-condition claims.
4. Some distinctions are based on `not reported` fields rather than explicit author-stated limitations.
5. MambaVLT is mentioned in planning text but is not represented by a completed paper card or matrix row.
6. The full method may become too complex; the first implementation should use the minimal architecture.

## 2. Files audited

| file or group | purpose | used in audit | missing or suspicious information |
|---|---|---|---|
| `AGENTS.md` | Project rules, topic, claim restrictions, required workflow, verification rules. | Yes | No issue. It correctly emphasizes evidence-backed gaps and dangerous claims to avoid. |
| `paper_cards/` | Evidence cards with page-number support and explicit/implicit limitation separation. | Yes | Contains 20 Markdown cards. MambaVLT is not present as a card. |
| `tables/paper_matrix.csv` | Paper-level matrix summarizing task, modality, method, degradation, limitations, relevance. | Yes | Contains 20 rows. No MambaVLT row. |
| `tables/mamba_usage_matrix.csv` | Classification of how each paper uses Mamba. | Yes | Useful for distinguishing restoration, memory, fusion, motion, and tracking uses. |
| `tables/degradation_matrix.csv` | Degradation and restoration coverage matrix. | Yes | Many cells rely on `Not reported`; this is acceptable but must not be treated as proof of absence. |
| `tables/missing_intersection_matrix.csv` | Intersection coverage and gap potential matrix. | Yes | Key target intersections are weakly studied/high potential, but several cells rely on partial coverage rather than empty coverage. |
| `tables/gap_scorecard.csv` | Risk-adjusted scoring of proposed ideas. | Yes | Selected idea ranks first with action "Proceed with caution as main direction." |
| `reports/01_evidence_summary.md` | Summary of matrix evidence. | Yes | Correctly warns that `not reported` should not be treated as a negative finding beyond reviewed evidence. |
| `reports/02_gap_analysis.md` | Ten candidate research gaps. | Yes | Some early gap language is broader than final wording; final reports narrow it appropriately. |
| `reports/03_reviewer_attack.md` | Strict reviewer critique of gaps. | Yes | Useful and appropriately harsh; supports merging/downgrading weak gaps. |
| `reports/03b_subagent_review.md` | Four-role review synthesis. | Yes | Supports final merged direction; flags missing evidence and experimental risks. |
| `reports/04_top_paper_ideas.md` | Converts refined gaps into paper ideas. | Yes | Selects TAR-MambaTrack as strongest but risky. |
| `reports/04_novelty_danger_check.md` | Strict novelty comparison against threat papers. | Yes | Strong source for current audit; exact unsafe phrases appear only in warning lists. |
| `reports/05_experiment_plan.md` | Experiment plan to prove or falsify the gap. | Yes | Realistic, but broad; must be staged. |
| `reports/05b_final_recommendation.md` | Final scorecard and selected direction. | Yes | Central source for final judgment. |
| `reports/06_research_gap_paragraph.md` | Paper-ready gap wording. | Yes | Strong wording, with explicit safe alternatives. |
| `reports/07_related_work_draft.md` | Related Work draft. | Yes | Good structure. MambaVLT is explicitly marked as lacking a separate card, so do not cite it as evidence until a card exists. |
| `reports/08_method_architecture.md` | Detailed method architecture. | Yes | Strong but complex; minimal version should be prioritized. |
| `reports/09_complete_paper_plan.md` | Complete paper plan. | Yes | Internally consistent and implementation-oriented. |

## 3. Unsupported claim audit

| file | section | problematic wording | why it is risky | safer replacement wording | action |
|---|---|---|---|---|---|
| `reports/02_gap_analysis.md` | Several candidate gaps | Some early gaps say a topic is "not systematically studied" or "not directly addressed." | This is often based on paper-card fields marked `not reported`, not explicit author limitations. | "Within the reviewed evidence, this topic is not directly established or is only partially covered." | Keep with safer wording in final manuscript. |
| `reports/03b_subagent_review.md` | Missing evidence notes | "Existing RGB Mamba SOT failure under blur/noise/JPEG/low resolution is inferred..." | Correctly flags the issue, but the final paper must not turn this inference into a factual claim. | "The reviewed papers do not report a systematic evaluation of this setting." | Keep as warning. |
| `reports/04_top_paper_ideas.md` | Idea 1 problem statement | "Current evidence does not directly show..." | Safe but should remain tied to the reviewed evidence set. | "The reviewed cards and matrices do not directly show..." | Keep, minor wording improvement for manuscript. |
| `reports/04_novelty_danger_check.md` | MambaIR/MambaIRv2 comparisons | "Paper matrix tracking-specific fields are not reported." | Safe if interpreted as evidence absence, not proof the methods cannot be adapted. | "The reviewed paper cards do not report template-search tracking, response maps, or target-localization evaluation for these restoration papers." | Keep. |
| `reports/06_research_gap_paragraph.md` | Evidence support | Some distinctions from trackers are based on "not reported." | This is acceptable but must be clearly labeled as implicit. | "This is an inference from the reviewed method/evaluation scope, not an author-stated limitation." | Keep. |
| `reports/07_related_work_draft.md` | Multimodal and specialized tracking | MambaVLT appears as a citation placeholder even though no separate paper card exists. | This could create an unsupported citation if used in a manuscript. | "Vision-language evidence in the reviewed set comes from MambaTrack Night UAV; add a MambaVLT card before citing MambaVLT separately." | Revise before manuscript if MambaVLT will be cited. |
| `reports/08_method_architecture.md` | Novelty comparison table | "MambaEVT and related specialized trackers use memory or dynamic templates..." | Mostly supported by cards, but "related" is broad. | Name the specific supported papers and avoid broad grouping. | Keep with caution. |
| `reports/09_complete_paper_plan.md` | Abstract draft | "Recent Mamba-based trackers ... do not systematically adapt..." | Safe if scoped to reviewed evidence; risky if presented globally. | "In the reviewed evidence, recent Mamba-based trackers do not systematically report..." | Revise for manuscript. |
| `reports/09_complete_paper_plan.md` | Dataset section | Some adverse datasets are listed as useful. | Dataset availability, licenses, and exact metrics still need manual confirmation. | "Candidate datasets include..." until verified. | Keep for planning; verify before experiments. |

No active unsupported numerical performance claims were found.

## 4. Dangerous overclaim audit

Exact unsafe phrases about absence of Mamba tracking, absence of low-light tracking, absence of Mamba memory, first-style degradation-robust tracking, MambaIR never being used in tracking, and trackers ignoring degradation were found only inside sections explicitly labeled as unsafe wording, dangerous claims to avoid, or avoided wording. They are not used as active project claims.

| location | original wording type | risk | safer corrected wording |
|---|---|---|---|
| `reports/04_novelty_danger_check.md`, dangerous-claims section | Unsafe Mamba-tracking absence claim listed as a claim to avoid. | Would be false because many reviewed papers use Mamba for tracking. | "Existing Mamba trackers in the reviewed set mainly use Mamba for temporal/contextual/multimodal/motion/template-update purposes." |
| `reports/06_research_gap_paragraph.md`, dangerous-claims table | Unsafe low-light absence claim listed as a claim to avoid. | Would be false because MambaTrack Night UAV and MambaNUT address low-light/night UAV tracking. | "Low-light/night UAV tracking is studied, while generic RGB degradation across blur, noise, low resolution, compression, and mixed degradation remains underexplored for the selected setting." |
| `reports/06_research_gap_paragraph.md`, dangerous-claims table | Unsafe memory absence claim listed as a claim to avoid. | Would be false because several trackers use memory, context, hidden states, or dynamic templates. | "Temporal memory is different from degradation-aware memory or restoration-reliability-controlled update." |
| `reports/06_research_gap_paragraph.md`, dangerous-claims table | Unsafe first-style degradation-robust tracker claim listed as a claim to avoid. | Would ignore InvTrack and adverse-condition trackers. | "The underexplored part is restoration-guided Mamba for RGB template-search degradation robustness." |
| `reports/07_related_work_draft.md`, unsafe wording removed | Unsafe tracker-ignores-degradation claim listed as avoided. | Would be too broad; some trackers handle adverse conditions, blur, low light, or robustness indirectly. | "The reviewed Mamba trackers mostly focus on other robustness mechanisms and do not systematically report restoration-guided RGB degradation recovery." |

Audit result: no active dangerous overclaim requires immediate file modification. The final manuscript should continue to use cautious wording.

## 5. Novelty consistency audit

| threat paper | what it already covers | what it does not directly cover in reviewed evidence | how selected idea differs | strong enough? | what to emphasize | risk |
|---|---|---|---|---|---|---|
| InvTrack | RGB template-search tracking under synthetic degradations; clean-degraded consistency; low-pass residual modules; response-map fusion. | Restoration-oriented Mamba/state-space recovery from MambaIR/MambaIRv2. | TAR-MambaTrack should recover target-discriminative features with restoration-guided Mamba blocks and tracking losses. | Medium if ablations are strong. | Compare to InvTrack and an InvTrack-style consistency baseline. | High |
| MambaIR | Image restoration with restoration-specific Mamba, local enhancement, channel attention/selection, reconstruction losses. | Tracking, template-search branches, response maps, target localization. | TAR-MambaTrack uses restoration ideas for tracking features and localization. | Medium. | Do not optimize only pixel reconstruction; show tracking metrics. | High |
| MambaIRv2 | Attentive state-space restoration and semantic-guided neighboring for restoration tasks. | Template-guided target-aware scan for tracking. | TG-AS should route search tokens by template relevance. | Medium if TG-AS is validated. | Show template-search response and localization benefit. | High |
| MambaLCT | Long-term context Mamba for tracking. | Restoration-guided degraded feature recovery. | Focus is RGB degradation recovery, not only long-term context. | Yes. | Temporal context is not degradation-aware restoration. | Medium |
| MCITrack | Contextual information, hidden-state/memory-style tracking cues. | General degradation-restoration feature recovery and restoration-guided response analysis. | Optional memory is degradation/reliability gated; core is RG-SSB. | Yes if memory is not overclaimed. | Do not claim memory novelty. | Medium |
| TemTrack | Mamba-based context-aware token learning for tracking. | Restoration/enhancement and degradation-aware update are not reported. | TAR-MambaTrack targets degraded template-search feature recovery. | Yes. | Compare temporal token learning vs degraded feature recovery. | Medium |
| SMTrack | Efficient temporal modeling, state-aware Mamba, scanned templates/dynamic template behavior, template degradation awareness in reviewed evidence. | Restoration-oriented Mamba recovery for generic RGB degradations is not reported. | TAR-MambaTrack should focus on restoration-guided feature recovery; memory/update is optional. | Medium. | Avoid claiming template-update novelty; test against SMTrack if possible. | High |
| MambaTrack Night UAV | Night UAV tracking; low-light enhancement; vision-language prompt evidence in reviewed cards. | Generic RGB degradation beyond low light and language-free robustness. | TAR-MambaTrack covers blur, noise, low resolution, compression, low light, and mixed degradation in RGB template-search tracking. | Medium. | Low-light is one condition, not the whole claim. | High |
| MambaNUT | Nighttime UAV tracking using Mamba and adaptive curriculum learning. | General degradation beyond nighttime is not established in reviewed evidence. | TAR-MambaTrack uses restoration-guided feature recovery across multiple degradation types. | Medium. | Distinguish curriculum/night robustness from restoration-guided generic degradation. | High |
| MambaEVT | Event-only tracking with Mamba/memory and dynamic-template style mechanisms. | RGB-only degraded-image feature recovery. | TAR-MambaTrack uses RGB only and does not rely on event sensors. | Yes. | Modality-based robustness differs from RGB-only degradation robustness. | Medium |
| MamTrack | RGB-event tracking with Mamba fusion/historical information and target-aware ideas. | RGB-only restoration-guided degradation recovery. | TAR-MambaTrack cannot rely on event input; TG-AS must be tracking/restoration-specific. | Medium. | Show RGB-only evaluation; be cautious with target-aware scan novelty. | High |
| Mamba-FETrack | RGB-event single-object tracking. | RGB-only degradation recovery without event modality. | TAR-MambaTrack focuses on RGB observations only. | Yes. | Additional sensors are not assumed. | Medium |
| MambaVT | RGB-T tracking with visible/thermal data and spatio-temporal context. | RGB-only degradation robustness without thermal input. | TAR-MambaTrack cannot use thermal modality. | Yes. | Distinguish thermal-assisted robustness from RGB recovery. | Medium |
| MambaVLT | Not represented by a completed card/matrix row in the audited evidence set. | Unknown within current evidence package. | No supported comparison should be made until a card is created. | Not auditable yet. | Add a paper card if it will be cited. | Unknown |
| HyMamba | Hyperspectral object tracking. | RGB-only degradation recovery. | TAR-MambaTrack targets RGB template-search tracking. | Yes. | Hyperspectral modality is out of scope. | Low |
| All-Day MCMT | All-day multi-camera multi-target tracking using RGB/thermal evidence in matrices. | RGB-only SOT template-search restoration. | TAR-MambaTrack is RGB SOT, not RGBT MCMT. | Yes. | Multi-camera/multimodal robustness differs from RGB-only SOT. | Medium |
| MambaTrack MOT | MOT tracking-by-detection with state-space modeling. | RGB SOT template-search restoration. | TAR-MambaTrack is SOT feature matching, not MOT association. | Yes. | Motion/association differs from degraded visual feature recovery. | Low to medium |
| MambaMOT | Mamba as MOT motion predictor. | Template-search feature recovery and restoration. | TAR-MambaTrack addresses visual features, not trajectory prediction. | Yes. | Distinguish motion prediction from restoration. | Low |
| MM-Tracker | UAV MOT with Motion Mamba, motion maps, detector/association handling; blur-related MOT evidence. | RGB SOT restoration-guided template-search matching. | TAR-MambaTrack should not claim blur is unstudied; it addresses visual feature recovery. | Yes. | Blur handling through motion/detection is different from feature restoration. | Medium |
| SportMamba | Sports MOT with nonlinear motion/state-space modeling. | RGB SOT degradation-restoration. | TAR-MambaTrack focuses on image-quality degradation in template-search matching. | Yes. | Motion modeling is not degraded feature recovery. | Low |
| Multi-State Tracker | Efficient SOT with multi-state feature modeling/enhancement. | Explicit restoration-guided Mamba for degradation-state recovery is only partial/implicit in reviewed evidence. | TAR-MambaTrack should use degradation-specific feature recovery and evaluation. | Medium. | Compare multi-state feature enhancement vs restoration-guided degradation recovery. | High |

## 6. Research gap audit

Answers:

1. Is the gap specific? Yes. It targets restoration-guided Mamba for RGB template-search tracking under image degradation.
2. Is the gap evidence-supported? Yes, but partly through `not reported` and weakly studied matrix cells, so wording must stay cautious.
3. Is the gap experimentally testable? Yes. It can be tested against InvTrack, MambaIR/MambaIRv2 preprocessing, standard trackers, Mamba trackers, and synthetic/real degraded benchmarks.
4. Is the gap different from InvTrack? Yes, if the method uses restoration-guided state-space feature recovery rather than only invariant consistency, low-pass residual modules, and response fusion.
5. Is the gap different from MambaIR/MambaIRv2? Yes, if the method is evaluated by tracking localization and response reliability rather than image restoration quality.
6. Is the gap different from existing Mamba trackers? Yes, if the claim is restoration-guided degraded feature recovery, not memory/context/fusion/motion/template update.
7. Is the gap too broad? It becomes too broad if phrased as general degradation-robust tracking or Mamba tracking novelty.
8. Is the gap too narrow? It is narrow enough for a defensible paper, but the experiments must cover multiple degradation types.
9. Is the wording safe? The final wording is mostly safe when scoped to "reviewed evidence" and "underexplored."

Current best gap statement:

Restoration-oriented Mamba has been established for image restoration, while degradation-invariant RGB template-search tracking has been partially addressed without Mamba restoration. Existing Mamba trackers in the reviewed evidence mainly use state-space modeling for temporal context, memory, dynamic templates, multimodal fusion, motion prediction, efficient tracking, or nighttime/adverse tracking. The underexplored intersection is tracking-aware restoration-guided Mamba for generic degraded RGB template-search tracking, where restoration is optimized for target-discriminative feature recovery, matching reliability, and localization rather than full-image visual reconstruction.

Revised safer gap statement:

Within the reviewed evidence, restoration-oriented Mamba is well supported for image restoration, and degradation-invariant RGB template-search tracking is partially addressed by InvTrack. However, the direct adaptation of restoration-oriented state-space feature recovery to tracking-aware RGB template-search matching under general image-quality degradations is only weakly studied. This motivates a focused study of restoration-guided Mamba features for target localization and response reliability under degraded template/search observations.

Final recommended gap statement:

Within the reviewed evidence, the underexplored gap is **tracking-aware restoration-guided Mamba for RGB template-search visual tracking under general image-quality degradation**, where restoration-oriented state-space modeling is evaluated by target-discriminative feature recovery, response reliability, and localization rather than full-image reconstruction.

## 7. Method architecture audit

| module | essential or optional | novelty contribution | implementation difficulty | reviewer risk | ablation required | minimal version? | postpone? |
|---|---|---|---|---|---|---|---|
| Restoration-Guided State Space Block | Essential | Core adaptation of restoration-oriented Mamba to tracking features. | Medium | High, because it may look like MambaIR plus tracker. | Vanilla Mamba, non-Mamba restoration block, no local enhancement, no channel selection. | Yes | No |
| Degradation token or prompt | Optional for first version | Adaptive degradation-aware modulation. | Medium | Medium, can look like extra complexity. | No token, predicted token, severity-only token. | No | Yes, unless easy |
| Template-Guided Attentive Scan | Optional but useful if feasible | Tracking adaptation of MambaIRv2-style attentive/token organization. | Medium to high | High, threatened by MambaIRv2 and MamTrack-style target-aware ideas. | Raster, four-direction, random, template-guided scan. | No | Yes |
| Tracking-aware feature restoration loss | Essential/recommended | Makes restoration useful for tracking features rather than image pixels. | Low to medium | Medium, related to InvTrack consistency. | Tracking only, feature consistency, response consistency, target-aware loss. | Yes | No |
| Degradation-aware memory update | Optional | Prevents degraded-frame memory contamination. | Medium | High, threatened by SMTrack/MCITrack and memory trackers. | No memory, confidence-only, degradation-aware, restored-feature memory. | No | Yes |
| Restoration-guided response fusion | Recommended after core | Tracking-specific matching/reliability mechanism. | Medium | High, because InvTrack already uses response fusion. | Original only, restored only, fixed fusion, adaptive fusion. | Maybe | Postpone until RG-SSB works |
| Degradation curriculum | Useful but not method core | Stabilizes general degradation training. | Low to medium | Medium, threatened by MambaNUT curriculum. | No curriculum, severity schedule, mixed schedule. | Yes as simple schedule | Expand later |
| Tracking head | Essential but not novelty | Provides localization output. | Low if using base tracker | Low | Keep same head, avoid changing too many variables. | Yes | No |

Recommended minimal architecture for first implementation:

1. Base one-stream RGB tracker.
2. RG-SSB inserted into one or two selected stages.
3. Synthetic degradation pipeline.
4. Tracking loss plus feature consistency and response consistency.
5. Standard center/classification-regression head.
6. Response-map logging.

Recommended full architecture for final paper:

1. RG-SSB.
2. Degradation prompt if it improves mixed/cross-degradation robustness.
3. Template-Guided Attentive Scan if it improves localization without excessive cost.
4. Restoration-guided response fusion if it beats InvTrack-style fusion.
5. Degradation-aware memory only if long-sequence drift is a demonstrated failure.
6. Degradation curriculum.

Modules to postpone if time is limited:

- TG-AS.
- Degradation-aware memory update.
- Contrastive target-distractor loss.
- Complex multi-response fusion.
- Real degraded fine-tuning.

## 8. Experiment plan audit

| experiment group | necessary? | realistic? | claim it proves | reviewer criticism addressed | required baseline | do first |
|---|---|---|---|---|---|---|
| Datasets | Yes | Yes if staged | Method works on standard and degraded tracking settings. | "Only synthetic toy setup." | Base tracker, standard trackers. | One standard dataset subset. |
| Synthetic degradation protocol | Essential | Yes | Robustness under controlled blur/noise/LR/JPEG/low-light/mixed degradation. | "Claim not tested across degradations." | Base + same augmentation, InvTrack if runnable. | Yes |
| Real degradation protocol | Important | Moderately realistic | Synthetic findings transfer to real adverse videos. | "Synthetic degradation is unrealistic." | Low-light/adverse trackers. | After proof of concept |
| Baselines | Essential | Depends on code | Distinguishes novelty threats. | "Simple combination." | InvTrack, MambaIR/MambaIRv2 + tracker, vanilla Mamba. | Yes, at least internal controls |
| Metrics | Essential | Yes | Quantifies tracking and robustness. | "Only qualitative." | All compared methods. | Yes |
| Ablations | Essential | Yes if minimal first | Identifies module contribution. | "Too many modules." | Base, vanilla Mamba, no loss variants. | Yes |
| Efficiency analysis | Important | Yes | Practicality vs external restoration. | "Too heavy." | Base tracker, external restoration + tracker. | After stable model |
| Response-map analysis | Important | Yes | Shows matching/localization effect. | "Restoration does not help tracking." | Base, restoration preprocessing. | Early visualization |
| Cross-degradation generalization | Important | Yes but more compute | Tests robustness beyond memorized corruption. | "Only augmentation effect." | Base + same training. | Second stage |
| Memory contamination experiment | Optional | Only if memory included | Tests degradation-aware memory. | "Temporal memory already solves it." | SMTrack/MCITrack-style or confidence-only memory. | Postpone |

Minimum experiment set for first proof of concept:

1. One standard dataset subset.
2. Synthetic degradation with motion blur, Gaussian noise, low resolution, JPEG, and mixed degradation.
3. Base tracker without degradation modules.
4. Base tracker with same degradation training.
5. Base plus vanilla Mamba.
6. Base plus RG-SSB.
7. MambaIR or MambaIRv2 preprocessing plus tracker if available.
8. Feature and response consistency ablations.
9. Response-map visualization.

Full experiment set for final paper:

- Standard benchmark comparison.
- Synthetic degradation benchmark.
- Mixed degradation benchmark.
- Real adverse-condition evaluation.
- Cross-degradation generalization.
- Template/search degradation asymmetry.
- Baseline comparison against InvTrack, restoration preprocessing, standard trackers, and Mamba trackers.
- Module and loss ablations.
- Efficiency analysis.
- Response-map and failure-case analysis.
- Optional memory contamination analysis.

Experiments that can be postponed:

- Degradation-aware memory.
- Full TG-AS if runtime is high.
- Real degraded fine-tuning.
- Very broad baseline set beyond essential novelty threats.

## 9. Dataset and baseline audit

Dataset classification:

| dataset | classification | reason |
|---|---|---|
| LaSOT | Essential | Standard RGB SOT, long sequences, useful for clean/degraded evaluation. |
| GOT-10k | Essential or useful | Official metrics AO/SR; good generalization benchmark. |
| TrackingNet | Useful | Large-scale benchmark, but compute-heavy. |
| OTB100 | Useful | Fast early debugging and classic attributes. |
| UAV123 | Useful | UAV motion and scale changes; good for degraded UAV stress. |
| NfS | Useful | Motion-related challenges. |
| AVisT | Useful | Real adverse visual tracking. |
| UAVDark70 | Useful | Low-light UAV evaluation. |
| UAVDark135 | Useful | Larger low-light UAV evaluation. |
| DarkTrack2021 | Useful | Dark/low-light evaluation. |
| NAT2021 | Optional/useful | Night aerial tracking; relevant to low-light but not general degradation alone. |
| NAT2021L | Optional/useful | Long nighttime aerial tracking; useful if memory is included. |
| Degraded LaSOT | Essential | Main controlled degradation benchmark candidate. |
| Degraded GOT-10k | Useful | Generalization under degradation. |
| Degraded TrackingNet | Optional | Strong but expensive. |
| Degraded UAV123 | Useful | UAV-specific degraded tracking. |

Baseline classification:

| baseline | classification | reason |
|---|---|---|
| InvTrack | Essential novelty-threat baseline | Strongest degradation-invariant RGB tracking threat. |
| MambaIR + tracker | Essential novelty-threat baseline | Tests image-level restoration preprocessing. |
| MambaIRv2 + tracker | Essential novelty-threat baseline if code available | Strong restoration Mamba threat. |
| Vanilla Mamba tracker/internal vanilla Mamba | Essential internal baseline | Tests whether gains are from generic Mamba capacity. |
| Base tracker without RG-Mamba | Essential internal baseline | Required for all claims. |
| Base tracker with same degradation training | Essential internal baseline | Separates architecture from data augmentation. |
| OSTrack | Essential or base | Strong candidate base tracker and standard comparison. |
| MixFormer | Standard comparison | Useful modern tracker baseline. |
| SeqTrack | Standard comparison | Useful sequence-style tracker. |
| TransT | Optional standard comparison | Historical transformer baseline. |
| Siamese trackers | Optional | Useful if correlation-head comparison is needed. |
| MambaLCT | Useful Mamba baseline | Temporal/context threat. |
| MCITrack | Useful Mamba baseline | Memory/context threat. |
| TemTrack | Useful Mamba baseline | Track-token/context threat. |
| SMTrack | Essential Mamba threat if runnable | Strong temporal/template-state threat. |
| MambaTrack Night UAV | Essential adverse Mamba threat for low-light claims | Low-light/night tracking threat. |
| MambaNUT | Essential adverse Mamba threat for low-light/curriculum claims | Nighttime UAV curriculum threat. |
| MamTrack/MambaEVT/MambaVT | Optional or context baselines | Relevant for multimodal distinction; not directly comparable if modalities differ. |
| MOT Mamba papers | Optional context baselines | Not directly comparable to RGB SOT unless discussing motion blur/MOT. |

## 10. Writing audit

Academic tone: generally strong and cautious.

Fairness to related work: good. The reports repeatedly recognize InvTrack, MambaIR, MambaIRv2, low-light trackers, memory trackers, multimodal trackers, and MOT trackers as real threats.

Repeated claims: the main gap wording repeats across reports 05b, 06, 08, and 09, but this is acceptable for planning. The final manuscript should consolidate to avoid redundancy.

Overly strong novelty language: no blocking active overclaim was found. Manuscript wording must keep "within the reviewed evidence" or equivalent caution where claims are based on uploaded papers.

Confusing terms: the main risk is mixing restoration-guided tracking, degradation-invariant tracking, and image-level restoration. The terminology section below resolves this.

Missing transitions: Related Work and Introduction plans already include transitions. The final paper should move from restoration Mamba to tracking Mamba to degradation tracking to the selected intersection.

Best final research-gap paragraph:

Recent restoration-oriented Mamba models demonstrate that state-space architectures can be specialized for recovering degraded image details: MambaIR addresses local pixel forgetting and channel redundancy through restoration-specific Mamba design, while MambaIRv2 improves restoration modeling through attentive state-space restoration and semantic-guided neighboring. In visual tracking, however, the reviewed Mamba-based trackers mainly use state-space modeling for temporal context, memory, dynamic template update, multimodal fusion, motion prediction, efficient backbone design, or low-light/adverse-condition tracking. InvTrack directly studies degradation-invariant RGB template-search tracking, but it uses clean-degraded consistency, response-map fusion, and low-pass residual modules rather than restoration-guided state-space recovery inspired by MambaIR/MambaIRv2. Existing nighttime and multimodal Mamba trackers further address important adverse settings, but they do not fully cover RGB-only template-search tracking under general image-quality degradations such as blur, noise, low resolution, compression, and mixed degradation. Therefore, the underexplored gap in the reviewed evidence is restoration-guided Mamba for degradation-robust RGB template-search visual tracking, where restoration is optimized for target-discriminative feature recovery and localization rather than full-image reconstruction.

Best final novelty statement:

TAR-MambaTrack studies the underexplored intersection of restoration-oriented Mamba and RGB template-search tracking by adapting state-space restoration ideas to target-discriminative feature recovery, response reliability, and localization under generic image-quality degradation.

Best final contribution bullets:

- A restoration-guided Mamba tracking framework for RGB template-search tracking under generic degradation.
- A tracking-aware restoration state-space block that adapts local enhancement, channel selection, and Mamba feature recovery to target localization.
- Tracking-specific losses and analyses that evaluate restoration through feature consistency, response-map reliability, and bounding-box accuracy.
- A degradation robustness protocol with template/search asymmetry, mixed degradation, cross-degradation generalization, restoration-preprocessing baselines, and direct novelty-threat comparisons.

Best final title:

- Tracking-Aware Restoration Mamba for Degradation-Robust RGB Template-Search Tracking.

Unsafe wording to avoid:

- Any claim that Mamba tracking, low-light tracking, memory, or degradation-robust tracking is absent.
- Any claim that image restoration and tracking-aware restoration are the same problem.
- Any claim that low-light tracking proves general degradation robustness.
- Any claim that the method solves all degradation types.

## 11. Terminology consistency audit

| term | recommended definition | inconsistent usage found | final wording |
|---|---|---|---|
| restoration-guided tracking | Tracking where restoration-inspired feature recovery guides localization and matching. | Sometimes close to image restoration wording. | "Restoration-guided tracking features" or "tracking-aware restoration features." |
| degradation-invariant tracking | Tracking that learns features/responses stable across clean and degraded inputs. | Could be confused with restoration. | "Degradation-invariant learning, as in InvTrack, is related but distinct from feature recovery." |
| tracking-aware restoration | Restoration objective optimized for tracking behavior rather than visual quality. | Mostly consistent. | "Tracking-aware feature restoration." |
| feature-level restoration | Recovery/enhancement of latent tracking features. | Good. | "Feature-level restoration for target-discriminative representations." |
| image-level restoration | Pixel/image reconstruction or enhancement before tracking. | Good. | "External image-level restoration preprocessing." |
| degradation-aware memory | Memory update controlled by degradation severity/reliability. | Sometimes optional status needs emphasis. | "Optional degradation-aware memory update." |
| temporal memory | Long-term or hidden-state tracking context over time. | Must not be treated as degradation-aware memory. | "Temporal memory/context, distinct from degradation-aware memory." |
| modality-based robustness | Robustness from event, thermal, language, hyperspectral, or other modalities. | Good. | "Sensor- or modality-assisted robustness." |
| RGB-only degradation robustness | Robustness using only RGB inputs under image-quality degradation. | Good. | "RGB-only degradation robustness under controlled degradations." |
| template-search matching | Matching initial/updated template features to search-region features. | Good. | "RGB template-search matching." |
| response-map fusion | Combining multiple response maps for localization. | Needs distinction from InvTrack. | "Restoration-guided response fusion, compared against InvTrack-style fusion." |
| target-aware scanning | Mamba/token scan guided by target relevance. | Threatened by MamTrack. | "Target-aware scanning in RGB template-search tracking." |
| template-guided attentive scanning | Routing search tokens by template similarity before/within Mamba scan. | Speculative until implemented. | "Optional Template-Guided Attentive Scan." |

## 12. Final novelty threat table

| threat paper | threat type | what it already solves | what our idea adds | novelty risk | required distinction | required experiment or ablation |
|---|---|---|---|---|---|---|
| InvTrack | Degradation-invariant RGB tracking | Clean-degraded consistency, low-pass residual modules, response fusion. | Restoration-guided state-space feature recovery and tracking-aware restoration losses. | High | Not just consistency or response fusion. | InvTrack comparison; consistency-only baseline; RG-SSB ablation. |
| MambaIR | Restoration Mamba | Image restoration with local enhancement/channel attention. | Target-localization objective and template-search feature recovery. | High | Not pixel restoration. | MambaIR + tracker baseline; feature-level vs image-level ablation. |
| MambaIRv2 | Attentive restoration Mamba | ASE/SGN for image restoration. | Template-guided scan and tracking response evaluation. | High | Not semantic restoration routing alone. | TG-AS vs raster/random/four-direction scan. |
| MambaTrack Night UAV | Low-light/night UAV | Low-light/night UAV tracking with enhancement/language evidence. | General RGB degradation beyond low light. | High | Low light is one subset. | Non-low-light degradation tests; language-free RGB comparison. |
| MambaNUT | Nighttime UAV curriculum | Mamba and curriculum for nighttime UAV tracking. | Restoration-guided feature recovery across multiple degradations. | High | Curriculum/night setting differs from general degradation. | Low-light and non-low-light degradation comparison. |
| SMTrack | Temporal/template state tracking | Temporal modeling, dynamic template/state-aware mechanisms. | Restoration-guided degraded feature recovery. | High | Memory/update is not the main novelty. | SMTrack comparison; no-memory minimal model. |
| MambaEVT | Event tracking | Event-only Mamba tracking and memory/dynamic template behavior. | RGB-only degradation recovery. | Medium | No event sensor. | RGB-only protocol; modality distinction table. |
| MamTrack | RGB-event target-aware/multimodal tracking | RGB-event tracking and target-aware/fusion ideas. | RGB-only restoration-guided template-search features. | High | Target-aware scan must be restoration/tracking-specific. | TG-AS ablation; no event input comparison. |
| Multi-State Tracker | Efficient feature-state modeling | Multi-state feature specialization/interactions. | Degradation-specific restoration-guided state-space recovery. | High | General feature states vs degradation/restoration states. | Multi-state-style feature baseline if feasible. |
| MambaVT | RGB-T tracking | Thermal-assisted tracking robustness. | RGB-only degradation feature recovery. | Medium | No thermal input. | RGB-only evaluation; modality baseline discussion. |
| MambaLCT | Long-term context | Context Mamba for tracking. | Restoration-guided degradation recovery. | Medium | Context is not restoration. | Degraded template/search tests. |
| MCITrack | Context/memory | Enhanced contextual information and memory-like update. | Degradation-aware recovery and optional reliability-gated memory. | Medium | Confidence/context memory differs from degradation-aware memory. | Confidence-only vs degradation-aware memory if memory is included. |
| TemTrack | Temporal token learning | Context-aware token learning. | Degraded feature recovery with restoration Mamba. | Medium | Temporal token learning differs from restoration. | Vanilla/degradation-trained tracker comparisons. |

## 13. Final implementation readiness

1. Is the selected idea ready for implementation? Yes, with caution and a minimal-first scope.
2. What should be implemented first? Base tracker reproduction, degradation pipeline, RG-SSB, feature consistency, response consistency, and evaluation scripts.
3. What should not be implemented first? TG-AS, degradation-aware memory, complex multi-response fusion, contrastive losses, and real degraded fine-tuning.
4. What is the minimum viable model? Base one-stream tracker + RG-SSB + synthetic degradation training + tracking/feature/response losses.
5. What is the minimum viable experiment? Clean and degraded evaluation on one dataset subset with base tracker, base plus same degradation training, base plus vanilla Mamba, base plus RG-SSB, and restoration-preprocessing baseline if available.
6. What failure would indicate the idea is weak? Base plus degradation training, MambaIRv2 preprocessing plus tracker, or InvTrack-style consistency matches the proposed model while being simpler or faster.
7. What success would justify continuing? RG-SSB improves degraded tracking and response reliability over base, vanilla Mamba, same-augmentation base, and restoration-preprocessing controls without unacceptable runtime cost.

## 14. Final recommended direction

Final recommended title:

- Tracking-Aware Restoration Mamba for Degradation-Robust RGB Template-Search Tracking.

Final recommended acronym:

- TAR-MambaTrack.

Final recommended gap statement:

Within the reviewed evidence, tracking-aware restoration-guided Mamba for RGB template-search visual tracking under general image-quality degradation remains weakly studied. The target gap is to adapt restoration-oriented state-space feature recovery to target localization, response reliability, and degraded template-search matching rather than full-image reconstruction.

Final recommended novelty statement:

TAR-MambaTrack studies a narrow but testable intersection: restoration-oriented Mamba adapted to RGB template-search tracking features under generic degradation, evaluated through tracking accuracy, response-map reliability, and robustness drop.

Final contribution bullets:

1. A restoration-guided Mamba framework for degraded RGB template-search tracking.
2. A tracking-aware restoration state-space block for target-discriminative feature recovery.
3. Tracking-specific losses and response analysis that evaluate restoration through localization.
4. A degradation robustness protocol with template/search asymmetry, mixed degradation, cross-degradation generalization, and direct novelty-threat baselines.

Final minimum architecture:

- Base RGB tracker.
- RG-SSB.
- Synthetic degradation training.
- Tracking loss + feature consistency + response consistency.
- Standard tracking head.

Final minimum experiment set:

- One standard RGB SOT benchmark subset.
- Controlled synthetic degradation protocol.
- Base tracker, same-augmentation base, vanilla Mamba, RG-SSB, and restoration-preprocessing baseline.
- Module/loss ablations.
- Response-map visualization and efficiency check.

Final implementation order:

1. Base tracker.
2. Degradation pipeline.
3. Evaluation scripts.
4. RG-SSB.
5. Feature/response losses.
6. Internal baselines.
7. Restoration-preprocessing baseline.
8. Response visualization.
9. Cross-degradation tests.
10. Optional modules only after the core works.

## 15. Action plan after audit

1. Choose the base tracker based on code availability, reproducibility, and compatibility with feature insertion.
2. Reproduce clean baseline results on a small subset before adding degradation.
3. Build the clean/degraded template-search data pipeline.
4. Implement synthetic degradations: blur, Gaussian noise, low resolution, JPEG compression, low light, and mixed corruption.
5. Implement evaluation for clean performance, degraded performance, and robustness drop.
6. Implement the minimal RG-SSB block in one selected tracker stage.
7. Train the base, base plus same degradation training, vanilla Mamba, and RG-SSB variants.
8. Add feature consistency and response consistency losses.
9. Compare with MambaIR or MambaIRv2 preprocessing plus tracker if code is available.
10. Visualize response maps and decide whether TG-AS, degradation prompt, or memory is justified.

## 16. Final decision

Final decision: **proceed with caution**.

The project is ready for implementation planning because the evidence chain, gap statement, novelty-risk analysis, experiment plan, method architecture, and complete paper plan are internally aligned. The selected idea is not broadly safe, but it is defensible if the implementation starts with a narrow minimal model and tests the strongest threats early. The first milestone should be a falsifiable proof of concept, not the full architecture.

## 17. Verification

Files created or modified:

- `reports/10_final_audit.md`

How the output was verified:

- Confirmed `AGENTS.md`, all listed tables, reports 01 through 09, and `paper_cards/` are present.
- Confirmed `paper_cards/` contains 20 Markdown cards and `tables/paper_matrix.csv` contains 20 paper rows.
- Checked `tables/gap_scorecard.csv`: TAR-MambaTrack is ranked first with "Proceed with caution as main direction."
- Checked `tables/missing_intersection_matrix.csv`: key target intersections for RGB single-object tracking are weakly studied with high gap potential, while template-guided attentive scanning is weakly studied with medium gap potential.
- Scanned reports and paper cards for exact unsafe overclaim phrases; hits occur only in avoid/unsafe wording sections, not as active project claims.
- Checked MambaVLT references and found no completed MambaVLT paper card or matrix row in the audited evidence set.

Uncertain fields:

- Whether InvTrack code and evaluation protocol can be reproduced exactly.
- Whether MambaIR/MambaIRv2 preprocessing baselines are computationally feasible.
- Whether Mamba trackers have public code and compatible evaluation settings.
- Whether TG-AS runtime is acceptable.
- Whether degradation prompt learning improves beyond simple augmentation.
- Whether real adverse datasets are available with consistent metrics and licenses.
- Whether MambaVLT should be included after a separate card is created.

Claims that need manual human review:

- Any claim based on `not reported` fields should be reviewed before manuscript submission.
- Any claim about MambaVLT should be withheld until a paper card and matrix entries are created.
- Any claim that the method is broader than low-light tracking should be supported by non-low-light degradation experiments.
- Any claim that feature-level restoration is more efficient than image-level restoration should be supported by runtime/FLOPs/memory measurements.
- Any claim that TG-AS improves matching should be supported by scan ablations and response-map analysis.

Whether any previous files should be revised:

- No previous file must be revised before starting implementation.
- Before manuscript drafting, revise or annotate MambaVLT-related wording unless a MambaVLT card is created.
- Before manuscript drafting, convert any "does not" wording based on `not reported` fields into "not reported in the reviewed evidence" or "not directly established by the reviewed papers."
