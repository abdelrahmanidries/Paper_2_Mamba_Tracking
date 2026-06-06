# Method Architecture: Restoration-Guided Mamba Tracking

## 1. Method goal

The goal is to recover target-discriminative tracking features from degraded RGB template and search images using restoration-guided Mamba blocks while preserving the efficiency and localization behavior of template-search visual object tracking. The method is not intended to produce visually perfect restored images. Its objective is to improve feature quality, template-search matching reliability, response-map stability, and bounding-box localization under image-quality degradation.

The selected direction is RGB-only tracking under general degradation, including blur, noise, low resolution, compression, low light, and mixed degradation. This distinguishes the method from multimodal robustness, nighttime-only tracking, motion prediction for multi-object tracking, and generic image restoration.

## 2. High-level architecture overview

Inputs:

- Template image `Z`, which may be clean or degraded.
- Search image `X`, which may be clean or degraded.
- Optional degradation token or degradation prompt `d`.
- Optional historical memory state `M_{t-1}`.

Outputs:

- Classification score map `S`.
- Bounding-box regression output `B`.
- Optional response map `R`.
- Optional degradation reliability score `q`.
- Optional updated memory state `M_t`.

Architecture stages:

1. Patch embedding / shallow feature extraction.
2. Restoration-Guided Mamba Backbone with RG-SSB blocks.
3. Template-search interaction, optionally using Template-Guided Attentive Scan.
4. Optional degradation-aware memory update.
5. Restoration-guided response fusion.
6. Tracking head.

```text
        Template Z                         Search X
            |                                |
            v                                v
    Patch / shallow features         Patch / shallow features
            |                                |
            +------------+-------------------+
                         |
                         v
              Degradation token / prompt d
                         |
                         v
        +---------------------------------------------+
        | Restoration-Guided Mamba Backbone           |
        | RG-SSB: Mamba branch + local enhancement    |
        |         + channel selection + residual       |
        +----------------------+----------------------+
                               |
                 +-------------+-------------+
                 |                           |
                 v                           v
          Template features Fz        Search features Fx
                 |                           |
                 +-------------+-------------+
                               |
                               v
              Template-Guided Attentive Scan
                               |
                               v
                 Template-search interaction
                               |
                 +-------------+-------------+
                 |                           |
                 v                           v
         Original response Ro       Restoration-guided response Rr
                 |                           |
                 +-------------+-------------+
                               |
                               v
              Restoration-guided response fusion
                               |
                               v
                   Tracking head: S, B
                               |
                               v
            Optional degradation-aware memory update
```

## 3. Module 1: Restoration-Guided State Space Block, RG-SSB

RG-SSB is the core module. It adapts restoration-oriented Mamba design from MambaIR to tracking features rather than pixel reconstruction.

Input:

- Feature tensor `F in R^{H x W x C}` from the template or search branch.
- Optional degradation token `d`.

Output:

- Restoration-guided feature tensor `F' in R^{H x W x C}`.

Operations:

1. Normalize the input feature.
2. Apply a 2D/Vision Mamba branch for long-range spatial dependency modeling.
3. Apply a local enhancement branch to recover local degraded details.
4. Apply a channel selection branch to suppress redundant or degradation-sensitive channels.
5. Optionally modulate the block with degradation token `d`.
6. Add a residual connection to preserve stable tracking features.

Mathematical formulation:

```text
U = LN(F)

G_s = VSSM_2D(U; theta_s(d))
G_l = Conv_{3x3}(U)

a_c = sigmoid(MLP([GAP(U), d]))
G = Proj(a_c * [G_s, G_l])

F' = F + gamma(d) * G
```

where `VSSM_2D` is a vision/state-space Mamba branch, `G_l` is the local enhancement output, `a_c` is a channel selection vector, and `gamma(d)` controls degradation-aware restoration strength. If no degradation token is used in the minimal version, `theta_s` and `gamma` are learned global parameters.

How it borrows from MambaIR:

- It uses state-space long-range modeling for image-like features.
- It adds a local enhancement branch to compensate for local detail loss.
- It uses channel attention or channel selection to reduce channel redundancy.
- It keeps residual state-space processing as the basic design pattern.

How it differs from MambaIR:

- It operates on tracking features rather than reconstructing RGB pixels.
- It is supervised by tracking, feature consistency, and response-map losses rather than only reconstruction-oriented losses.
- It enhances target-discriminative features for template-search matching rather than restoring all image content uniformly.
- It is inserted into a tracker whose final objective is localization accuracy.

Degradations it is expected to help test:

- Motion blur and defocus blur, by recovering local and long-range target structure.
- Low resolution, by enhancing target-discriminative feature detail.
- Sensor noise and JPEG compression, by suppressing degraded channels and local artifacts.
- Low light, by improving feature reliability without relying on a separate enhancer.

Supervision:

- `L_track` for classification and box regression.
- `L_feat` for clean-degraded feature consistency.
- `L_resp` for response-map consistency.
- `L_targRest` for target-region feature restoration.

Ablations:

- Replace RG-SSB with a vanilla Mamba block.
- Remove the local enhancement branch.
- Remove channel selection.
- Remove degradation-aware modulation.
- Replace RG-SSB with a convolutional restoration block.
- Compare feature-level RG-SSB against external image restoration followed by tracking.

## 4. Module 2: Degradation Token / Degradation Prompt

The degradation token estimates image-quality degradation type and severity from template and search features. It should help the model adapt restoration strength, channel selection, scan behavior, response fusion, and optional memory update. The method should not depend on explicit degradation labels at test time.

Input:

- Template features `F_z`.
- Search features `F_x`.
- Optional shallow image statistics from `Z` and `X`.

Output:

- Template degradation token `d_z`.
- Search degradation token `d_x`.
- Pair degradation token `d`.
- Reliability score `q`, where higher values indicate more reliable tracking features.

Possible degradation classes:

- Blur.
- Noise.
- Low resolution.
- Compression.
- Low light.
- Mixed degradation.
- Unknown degradation.

Estimation:

```text
e_z = Pool(phi_deg(F_z))
e_x = Pool(phi_deg(F_x))

d = MLP([e_z, e_x, abs(e_z - e_x)])
p_deg = softmax(W_c d)
s_deg = sigmoid(W_s d)
q = 1 - s_deg
```

`p_deg` is an optional degradation-type distribution, `s_deg` is a severity estimate, and `q` is a reliability score. During training with synthetic degradation, degradation labels can supervise `p_deg` and severity labels can supervise `s_deg`. For real degraded videos without labels, the token can be trained through tracking loss, consistency loss, response sharpness, or self-supervised severity estimation.

How the token modulates RG-SSB:

- Controls local enhancement strength through `gamma(d)`.
- Modulates channel selection weights.
- Adjusts Mamba scan parameters or state update gates.
- Controls memory update reliability.
- Provides adaptive weights for response fusion.

Training supervision:

- Synthetic degradation classification loss when labels are available.
- Severity regression for known degradation levels.
- Self-supervised reliability loss from response-map sharpness or tracking confidence when labels are unavailable.
- Tracking loss so the token remains task-aligned.

Ablations:

- No degradation token.
- Oracle synthetic degradation label during training only.
- Predicted degradation token.
- Severity-only token.
- Random or shuffled token.
- Token used only in RG-SSB versus token used in RG-SSB, memory, and response fusion.

## 5. Module 3: Template-Guided Attentive Scan, TG-AS

TG-AS adapts the idea behind MambaIRv2's attentive state-space restoration and semantic-guided neighboring to tracking. Instead of grouping semantically related pixels for image restoration, TG-AS groups template-relevant search tokens so target-related search regions become closer in the Mamba scan sequence.

Input:

- Template feature tokens `F_z = {z_j}`.
- Search feature tokens `F_x = {x_i}`.
- Optional degradation token `d`.

Output:

- Target-aware scanned search features `F_x^{tg}`.
- Optional target-aware template-search interaction features.

Template prototype:

```text
p_z = Pool_target(F_z)
```

`Pool_target` can use the known template box in training and the initial target crop at inference. If a one-stream tracker is used, `p_z` can also be computed from template tokens after patch embedding.

Similarity and routing:

```text
s_i = cosine(W_q x_i, W_k p_z)
P = Route(s, spatial_bins)
tilde_X = P X
```

`s_i` measures template relevance for each search token. `Route` constructs a permutation or soft routing matrix that places target-relevant tokens closer together while preserving coarse spatial structure through bins or local windows.

Attentive state-space update:

```text
h_i = A(d, s_i) h_{i-1} + B(d, s_i) tilde_x_i
y_i = C(d, s_i) h_i + D tilde_x_i

F_x^{tg} = P^{-1} Y
```

This makes the state-space update target-aware: search tokens that are likely to correspond to the template can receive stronger state propagation, while distractor or degraded tokens can be down-weighted.

How it differs from MambaIRv2 semantic-guided neighboring:

- MambaIRv2 groups semantically related pixels to improve restoration.
- TG-AS groups template-relevant search tokens to improve localization and matching.
- The objective is not generic image recovery; it is target localization under degradation.
- The routing uses template-search similarity, not only image-internal semantic similarity.

How it avoids excessive multi-directional scans:

- Use one target-guided scan plus a lightweight reverse scan rather than many dense directional scans.
- Use top-k routing or spatial bins instead of full global sorting.
- Restrict attentive routing to selected RG-SSB stages.
- Use normal raster scan in early layers and TG-AS only in high-level tracking features.

Supervision:

- Tracking loss from the final classification and regression head.
- Response-map consistency between clean and degraded pairs.
- Optional target center prior or target-region mask when available from tracking labels.
- Optional contrastive target-distractor loss.

Ablations:

- Normal raster scan.
- Four-direction scan.
- Random scan.
- Search-only attentive scan.
- Template-guided attentive scan.

## 6. Module 4: Tracking-Aware Feature Restoration Loss

The loss design should make restoration useful for tracking. The method should avoid relying only on full-image reconstruction losses, because visually pleasing images do not necessarily produce better target localization.

Tracking loss:

```text
L_track = L_cls + beta_1 L_box + beta_2 L_giou
```

`L_cls` can be focal loss or cross-entropy for the classification or center map. `L_box` is an L1 bounding-box loss. `L_giou` is generalized IoU loss.

Clean-degraded feature consistency:

```text
L_feat = || stopgrad(F_clean) - F_degraded^{rg} ||_1
```

This is inspired by InvTrack's clean-degraded consistency, but it is applied to restoration-guided Mamba features. The goal is not only invariance; it is recovery of target-discriminative feature structure after RG-SSB processing.

Response-map consistency:

```text
L_resp = KL(softmax(R_clean) || softmax(R_degraded^{rg}))
       + || norm(R_clean) - norm(R_degraded^{rg}) ||_1
```

This encourages degraded/restoration-guided features to produce response maps close to clean tracking responses.

Target-aware restoration loss:

```text
L_targRest = || M_target * (F_clean - F_degraded^{rg}) ||_1
```

`M_target` is a target-region mask or soft Gaussian center prior from the annotated box. This emphasizes target features and avoids turning the method into full-image restoration.

Optional contrastive target-distractor loss:

```text
L_con = -log exp(sim(f_t, f_t^+) / tau)
        / sum_k exp(sim(f_t, f_k^-) / tau)
```

This term can be folded into `L_targRest` or added separately if distractor annotations or mined negatives are available.

Degradation-token loss:

```text
L_deg = CE(p_deg, y_deg) + || s_deg - y_sev ||_1
```

Use this only when synthetic degradation labels or severity levels are available. For real videos without labels, this term can be omitted.

Memory reliability loss:

```text
L_mem = BCE(g_t, y_reliable)
```

This is optional and only applies if degradation-aware memory is included. Pseudo-labels can come from tracking confidence, response sharpness, and known synthetic severity.

Total loss:

```text
L_total = L_track
        + lambda_1 L_feat
        + lambda_2 L_resp
        + lambda_3 L_targRest
        + lambda_4 L_deg
        + lambda_5 L_mem
```

`L_track` is mandatory. `L_feat` and `L_resp` are recommended for the minimal method. `L_targRest`, `L_deg`, and `L_mem` can be staged based on implementation complexity and available annotations.

## 7. Module 5: Degradation-Aware Memory Update, optional but recommended

This module is optional for the first implementation but useful for long sequences. Its purpose is to prevent degraded or uncertain frames from contaminating the target memory or dynamic template.

Input:

- Current target feature `f_t^{rg}` from restoration-guided features.
- Tracking confidence `c_t`.
- Degradation severity `s_t`.
- Reliability score `q_t`.
- Response-map sharpness `rho_t`.
- Previous memory state `M_{t-1}`.

Output:

- Updated memory state `M_t`.
- Update gate `g_t`.

Update rule:

```text
rho_t = peak(R_t) / (mean(R_t) + epsilon)

g_t = sigmoid(w_c c_t + w_q q_t + w_r rho_t - w_s s_t + b)
g_t = g_t * I[c_t > tau_c]

M_t = (1 - g_t) M_{t-1} + g_t Proj(f_t^{rg})
```

The update is strong when the response is confident, the degradation is mild or recoverable, and the restored feature is reliable. The update is weak or skipped when the frame is heavily degraded, the response map is flat, or tracking confidence is low.

How it differs from existing Mamba memory or context trackers:

- MambaLCT uses Mamba for long-term context modeling.
- MCITrack uses hidden-state context or memory-style tracking cues.
- TemTrack and SMTrack focus on temporal cue propagation, memory, or dynamic templates.
- MambaEVT and related specialized trackers use memory or dynamic templates in event/multimodal settings.
- The proposed module specifically gates RGB target memory using degradation severity, restoration reliability, and response sharpness.

This distinction is important because temporal memory is not the same as degradation-aware memory. The memory gate is designed to prevent degraded feature contamination, not simply to extend temporal context.

Ablations:

- No memory update.
- Confidence-only memory update.
- Degradation-aware memory update.
- Memory updated from original features.
- Memory updated from restoration-guided features.
- Memory update without response-map sharpness.

## 8. Module 6: Restoration-Guided Response Fusion

This module fuses responses from original tracking features, restoration-guided features, and optional memory-guided features.

Inputs:

- Original feature response `R_o`.
- Restoration-guided feature response `R_r`.
- Optional memory-guided response `R_m`.
- Degradation reliability score `q`.
- Response sharpness statistics.

Output:

- Fused response map `R_f`.

Mathematical formulation:

```text
a = MLP([q, sharp(R_o), sharp(R_r), sharp(R_m), c_t])
w = softmax(a)

R_f = w_o R_o + w_r R_r + w_m R_m
```

If memory is not used, `R_m` and `w_m` are omitted.

Degradation-aware gating:

- When degradation is mild and original response is sharp, the model can keep more weight on `R_o`.
- When degradation is strong but restoration-guided response is sharp, the model can increase `w_r`.
- When the sequence is long and memory is reliable, the model can include `R_m`.

How it differs from InvTrack:

- InvTrack uses response-map fusion in a degradation-invariant learning framework.
- The proposed fusion combines original and restoration-guided responses after state-space feature recovery.
- The proposed fusion can be conditioned on degradation reliability and optional restored-feature memory.
- The distinction should be tested directly with InvTrack-style fusion versus restoration-guided fusion ablations.

Ablations:

- Original response only.
- Restoration-guided response only.
- Original plus restoration-guided response.
- Original plus restoration-guided plus memory response.
- Fixed fusion weights.
- Adaptive degradation-aware fusion weights.

## 9. Tracking head

The recommended first implementation is an OSTrack-style center head or a similar one-stream tracking head. This is practical because it already uses template-search feature interaction and produces standard classification and box regression outputs. It also makes response-map and feature consistency losses easy to attach.

Outputs:

- Classification or center score map `S`.
- Offset regression.
- Size regression.
- Final bounding box `B`.

Loss terms:

- Focal loss or cross-entropy for `S`.
- L1 loss for box coordinates.
- GIoU loss for box overlap.

Alternative heads:

- Siamese correlation head if the implementation starts from a Siamese tracker.
- Transformer-style classification/regression head if the base tracker already follows that design.

The main recommendation is to avoid changing the head before the restoration-guided feature modules are validated. The first proof-of-concept should keep the tracking head close to a known baseline.

## 10. Full training pipeline

Training data:

1. Clean template-search pairs from standard RGB SOT datasets.
2. Synthetically degraded template-search pairs.
3. Optional real degraded videos for evaluation or fine-tuning.

Training cases:

- Clean template + degraded search.
- Degraded template + clean search.
- Degraded template + degraded search.
- Template and search degraded by different degradation types.
- Mixed degradation on template, search, or both.

Curriculum:

1. Train or warm up on clean tracking pairs.
2. Add mild synthetic degradation.
3. Increase to medium and severe degradation.
4. Add mixed degradation.
5. Optionally fine-tune or validate on real adverse-condition videos.

How this differs from InvTrack training:

- InvTrack focuses on degradation-invariant feature learning, clean-degraded consistency, response-map fusion, and low-pass residual modules.
- The proposed training explicitly supervises restoration-guided state-space feature recovery and target-aware template-search matching.
- The method should compare against InvTrack and against an InvTrack-style consistency-only variant to show that the benefit is not only clean-degraded invariance.

No clean image is assumed at test time. Clean-degraded pairs are used during training to provide supervision for feature and response consistency.

## 11. Inference pipeline

Inference steps:

1. Crop the initial template `Z`.
2. Crop the current search image `X_t`.
3. Extract shallow features from `Z` and `X_t`.
4. Estimate degradation token `d_t` and reliability score `q_t`.
5. Apply RG-SSB blocks to recover restoration-guided tracking features.
6. Apply TG-AS if included in the model.
7. Compute original and restoration-guided responses.
8. Fuse responses with degradation-aware weights.
9. Predict the target box with the tracking head.
10. Optionally update memory with the degradation-aware gate.

No clean image or explicit degradation label is available during inference. The degradation token must be predicted from the current template-search pair or omitted in the minimal version.

## 12. Minimal version for first implementation

The smallest feasible implementation should include:

1. A base one-stream RGB tracker.
2. RG-SSB inserted into the backbone or interaction stage.
3. Synthetic degradation training.
4. `L_track + L_feat + L_resp`.
5. Response-map visualization for clean versus degraded inputs.
6. No memory update in the first version unless the base tracker already provides an easy memory interface.

This minimal version is enough for a proof-of-concept because it tests the central claim: restoration-guided Mamba feature recovery can improve template-search matching under degradation beyond a vanilla tracker, external restoration preprocessing, and consistency-only degradation learning.

Recommended first tests:

- Baseline tracker.
- Baseline tracker plus synthetic degradation training.
- Baseline tracker plus RG-SSB.
- Baseline tracker plus RG-SSB and feature/response consistency.
- External MambaIR or MambaIRv2 preprocessing plus tracker, if code and runtime are available.

## 13. Full version for final paper

Full method components:

1. RG-SSB as the core restoration-guided Mamba block.
2. Degradation token or degradation prompt.
3. Template-Guided Attentive Scan.
4. Restoration-guided response fusion.
5. Optional degradation-aware memory update.
6. Degradation curriculum training.
7. Full loss with tracking, feature consistency, response consistency, target-aware restoration, degradation-token supervision, and optional memory reliability.

Essential modules:

- RG-SSB.
- Synthetic degradation training.
- Tracking-aware feature and response losses.
- Direct comparison against InvTrack, MambaIR-preprocessing, and existing Mamba trackers.

Recommended optional modules:

- Degradation token.
- Restoration-guided response fusion.
- TG-AS if routing cost is manageable.

Modules to treat as optional or future extension:

- Degradation-aware memory update.
- Contrastive target-distractor loss.
- Real degraded fine-tuning if labels and training splits are not cleanly available.

## 14. Novelty comparison table

| paper | what it does | similarity to our method | what our method adds | novelty risk | required distinction |
|---|---|---|---|---|---|
| InvTrack | Degradation-invariant tracking with clean-degraded consistency, response-map fusion, and low-pass residual modules. | Directly addresses degradation robustness in tracking. | Restoration-guided state-space feature recovery inspired by MambaIR/MambaIRv2, target-aware Mamba processing, and tracking-aware feature restoration. | High | Show the method is not only invariant learning or response fusion; compare to InvTrack and consistency-only variants. |
| MambaIR | Image restoration with restoration-specific Mamba design, local enhancement, channel attention, and reconstruction-oriented training. | Provides restoration-oriented Mamba design inspiration. | Adapts restoration blocks to template-search localization and feature-level tracking objectives. | High | Avoid presenting the method as pixel restoration; show tracking-specific losses and localization gains. |
| MambaIRv2 | Image restoration with attentive state-space restoration and semantic-guided neighboring. | Inspires attentive scanning and token grouping. | Uses template-guided routing for target-aware search scanning instead of semantic grouping for image restoration. | High | Demonstrate template-search matching benefit, not only improved restoration features. |
| MambaLCT | Uses Mamba for long-term context in tracking. | Mamba-based tracking. | Focuses on degradation-aware restoration-guided features rather than long-term context alone. | Medium | Distinguish temporal context from degraded feature recovery. |
| MCITrack | Uses Mamba-style hidden-state or contextual memory for tracking. | Memory/context tracking threat. | Adds restoration reliability and degradation-aware feature recovery; memory is optional and gated by degradation. | Medium | Distinguish hidden-state memory from degradation-aware memory. |
| TemTrack | Uses temporal cues or track-token style propagation. | Mamba for temporal tracking. | Targets RGB degradation and template-search feature restoration rather than temporal propagation alone. | Medium | Evaluate degraded template/search cases, not only long temporal context. |
| SMTrack | Uses Mamba for temporal or memory-oriented tracking behavior and dynamic tracking cues. | Related to memory and template handling. | Adds restoration-guided state-space recovery and degradation-aware training for generic RGB degradations. | Medium to high | Avoid claiming memory novelty; emphasize restoration-guided degraded feature recovery. |
| MambaTrack Night UAV | Nighttime UAV tracking with low-light or vision-language Mamba components. | Addresses adverse/night tracking. | Targets RGB-only general degradation beyond nighttime and does not rely on language as the core robustness source. | High | Show blur, noise, low resolution, compression, and mixed degradation, not only low-light/night UAV. |
| MambaNUT | Nighttime UAV tracking with pure Mamba and adaptive curriculum learning. | Adverse-condition Mamba tracking and curriculum threat. | Uses restoration-guided feature recovery for general degradation rather than nighttime-only robustness. | Medium to high | Compare low-light separately from general degradation and include non-low-light degradations. |
| MambaEVT | Event-based or event-focused tracking with memory or dynamic template mechanisms. | Robust tracking with Mamba in a specialized modality. | RGB-only restoration-guided tracking without event sensors. | Medium | Distinguish modality-based robustness from RGB-only degradation robustness. |
| MamTrack | RGB-event tracking with Mamba-based fusion or target-aware processing. | Target-aware scanning/fusion is a potential conceptual threat. | Removes event input and focuses on restoration-guided RGB template-search features under degradation. | Medium | Show robustness without extra event modality. |
| MambaVT | RGB-T tracking with multimodal feature fusion or template/context modeling. | Robustness through thermal modality. | RGB-only degradation recovery without thermal input. | Medium | Distinguish thermal-assisted robustness from RGB image-quality recovery. |
| Multi-State Tracker | Uses multi-state feature modeling or state transitions for tracking. | Feature-state modeling may appear related. | Uses explicit restoration-guided degradation recovery and template-search losses. | Medium | Distinguish general feature-state modeling from degradation-state or restoration-guided feature recovery. |

## 15. Ablation plan linked to modules

| ablation | removed module | hypothesis tested | expected effect | reviewer criticism addressed |
|---|---|---|---|---|
| Baseline tracker | All proposed modules | Establish clean and degraded baseline behavior. | Reference performance and degradation drop. | Shows improvements are not from evaluation protocol alone. |
| RG-SSB replaced by vanilla Mamba | Restoration-guided block design | Local enhancement and channel selection matter beyond generic Mamba. | Larger degradation drop than full RG-SSB. | Addresses "this is only adding Mamba." |
| No local enhancement | Local enhancement branch | Local detail recovery helps blur, low resolution, and compression. | Weaker response sharpness under local degradation. | Addresses MambaIR-inspired local recovery value. |
| No channel selection | Channel selection branch | Suppressing degradation-sensitive channels improves robustness. | More noise/compression sensitivity. | Addresses channel redundancy motivation. |
| No degradation token | Degradation prompt | Adaptive modulation improves mixed degradation handling. | Lower cross-degradation generalization. | Addresses whether degradation awareness is useful. |
| Raster scan instead of TG-AS | Template-guided attentive scan | Target-aware token routing improves matching. | Less precise localization under distractors/degradation. | Addresses "TG-AS is unnecessary complexity." |
| Random route instead of TG-AS | Template-guided routing | Improvements should come from template relevance, not arbitrary sequence changes. | Unstable or reduced matching quality. | Addresses routing validity. |
| No feature consistency | `L_feat` | Clean-degraded Mamba feature alignment improves robustness. | Higher degraded-clean feature gap. | Addresses relation to InvTrack-style consistency. |
| No response consistency | `L_resp` | Response-level alignment improves localization. | More diffuse degraded response maps. | Addresses matching-specific effect. |
| Full-image restoration preprocessing | Feature-level restoration module replaced externally | Feature-level tracking-aware restoration is preferable to generic image enhancement. | May improve appearance but not necessarily matching or efficiency. | Addresses "MambaIR plus tracker is enough." |
| No response fusion | Restoration-guided response fusion | Adaptive original/restored fusion improves reliability. | Lower robustness when restoration is imperfect. | Addresses relation to InvTrack response fusion. |
| Fixed response fusion | Adaptive fusion weights | Degradation-aware fusion is better than a constant mixture. | Less stable across degradation types. | Addresses adaptive gating value. |
| No memory | Degradation-aware memory update | Memory is optional; core should still work without it. | Similar short-sequence performance, possible long-sequence drop. | Keeps minimal method realistic. |
| Confidence-only memory | Degradation-aware gate | Degradation reliability adds information beyond confidence. | More drift under degraded frames. | Addresses temporal memory versus degradation-aware memory. |
| Full model | None | Combined modules improve robustness while remaining efficient. | Best expected trade-off if modules are well tuned. | Addresses overall contribution. |

The "expected effect" column states testable hypotheses, not experimental results.

## 16. Complexity and efficiency discussion

Feature-level restoration is expected to be more efficient than external full-image restoration because it operates on lower-resolution tracking features, shares computation with the tracker, and avoids running a separate restoration network on every frame. It also keeps the optimization target aligned with localization rather than visual quality.

Mamba-style state-space modeling can provide long-range dependency modeling with favorable sequence scaling compared with dense attention. RG-SSB should therefore be inserted selectively into the backbone or interaction stage rather than replacing every block.

Modules that may increase cost:

- TG-AS routing or sorting, especially if performed globally at high resolution.
- Multi-branch RG-SSB blocks.
- Response fusion with multiple response heads.
- Memory update and memory-response computation.
- Degradation-token estimation if it uses a heavy encoder.

Ways to keep the method lightweight:

- Use RG-SSB only in middle or high-level stages.
- Use depthwise convolutions for local enhancement.
- Use low-rank channel selection.
- Use spatial bins or top-k routing for TG-AS.
- Share degradation-token encoders for template and search.
- Disable memory in the minimal model.
- Report both minimal and full model efficiency.

Metrics to report:

- FPS.
- FLOPs.
- Number of parameters.
- GPU memory.
- AUC / success, precision, normalized precision.
- Degradation robustness drop.
- Response-map sharpness or peak-to-sidelobe ratio if included.

## 17. Risks and mitigation

| risk | why it matters | mitigation |
|---|---|---|
| The method may look like InvTrack plus Mamba. | InvTrack is the strongest degradation-invariant tracking threat. | Emphasize restoration-guided state-space feature recovery, target-aware losses, and compare against InvTrack-style consistency and response fusion. |
| The method may look like MambaIR plus tracker. | MambaIR and MambaIRv2 are the strongest restoration threats. | Avoid pixel-restoration framing; use feature-level target losses, response consistency, and tracking benchmarks. |
| The method may look like night UAV Mamba tracking. | MambaTrack Night UAV and MambaNUT address adverse low-light tracking. | Evaluate general degradations beyond low light: blur, noise, low resolution, compression, and mixed degradation. |
| Too many modules may weaken the contribution. | Reviewers may see the method as an over-combined system. | Implement RG-SSB first; add TG-AS, degradation token, response fusion, and memory only if ablations justify them. |
| Synthetic degradation may not transfer to real videos. | Real-world artifacts can differ from synthetic corruptions. | Include real adverse-condition evaluation and cross-degradation generalization tests. |
| Memory update may be unstable. | Incorrect updates can cause drift. | Treat memory as optional; use confidence, degradation reliability, and response sharpness gates. |
| TG-AS may be expensive. | Routing can increase inference cost. | Use sparse routing, spatial bins, and apply TG-AS only at selected layers. |
| External restoration preprocessing may perform competitively. | It is a direct baseline against restoration-guided design. | Compare against MambaIR/MambaIRv2 preprocessing plus tracker in accuracy and efficiency. |

## 18. Recommended final architecture choice

Best minimal architecture:

1. One-stream RGB tracker backbone.
2. RG-SSB inserted into the feature backbone or template-search interaction stage.
3. Synthetic degradation training with clean/degraded template-search pairs.
4. Tracking loss plus clean-degraded feature consistency and response consistency.
5. Standard center-based tracking head.
6. Response-map visualization for clean versus degraded search images.

Best full architecture:

1. RG-SSB as the core block.
2. Degradation token for adaptive restoration strength and fusion.
3. TG-AS for template-guided target-aware scanning.
4. Restoration-guided response fusion.
5. Optional degradation-aware memory update for long sequences.
6. Curriculum training from mild to severe and mixed degradation.

Modules to implement first:

- Synthetic degradation data pipeline.
- Baseline tracker reproduction.
- RG-SSB block.
- Feature consistency loss.
- Response consistency loss.
- Degraded template/search evaluation.

Modules to postpone:

- Degradation-aware memory update.
- Full TG-AS routing if initial RG-SSB results are weak or too slow.
- Contrastive target-distractor loss.
- Real degraded fine-tuning.
- Multi-response fusion beyond original plus restoration-guided response.

Final method name options:

- Restoration-Guided Mamba Tracker.
- Restoration-Guided Mamba Tracking.
- Target-Aware Restoration Mamba Tracker.
- Degradation-Robust Restoration Mamba Tracker.
- Restoration-Mamba Tracking.

Final acronym options:

- RG-MambaTrack.
- RGMTrack.
- TAR-MambaTrack.
- DR-MambaTrack.
- ReMambaTrack.

Recommended first acronym:

- `RG-MambaTrack`, because it directly communicates restoration-guided Mamba tracking without implying unsupported claims about being a universal degradation solution.

Files created or modified:

- `reports/08_method_architecture.md`

How the output was verified:

- The report follows the requested section structure from method goal through recommended architecture choice.
- The design keeps the minimal implementation separate from optional full-paper extensions.
- Novelty distinctions are stated against InvTrack, MambaIR, MambaIRv2, temporal/context Mamba trackers, multimodal Mamba trackers, MOT/motion Mamba trackers, and nighttime UAV Mamba trackers.
- The report does not include experimental results, implementation code, a final paper plan, or unsupported "first" claims.

Uncertain fields:

- The exact base tracker should be selected after checking available code and compute.
- Public code availability for some Mamba trackers and restoration baselines may affect baseline selection.
- TG-AS routing cost is uncertain until implemented.
- Degradation-token supervision depends on the final synthetic degradation protocol.
- A separate MambaVLT paper card was not part of the current reviewed paper-card set, so vision-language distinctions should remain tied to the available nighttime UAV and matrix evidence unless a MambaVLT card is added.

Whether the project is ready for the complete paper plan:

- Yes, with caution. The evidence package now supports a concrete method direction, but the complete paper plan should preserve the minimal-first implementation path and keep memory, TG-AS, and complex fusion as staged extensions unless early experiments justify them.
