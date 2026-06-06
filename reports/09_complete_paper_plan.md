# Complete Paper Plan

## 1. Recommended paper title

Possible titles:

1. Tracking-Aware Restoration Mamba for Degradation-Robust RGB Template-Search Tracking.
2. Restoration-Guided Mamba Tracking for Robust RGB Visual Object Tracking under Image Degradation.
3. TAR-MambaTrack: Tracking-Aware Restoration Mamba for Degraded RGB Template-Search Tracking.
4. Restoration-Oriented State Space Tracking for Degraded RGB Template-Search Matching.
5. Target-Aware Restoration Mamba for Robust RGB Object Tracking under Generic Degradation.

Recommended title:

- **Tracking-Aware Restoration Mamba for Degradation-Robust RGB Template-Search Tracking**

Recommended acronym:

- **TAR-MambaTrack**

Why this title is safest:

- It names the actual research intersection: tracking-aware restoration, Mamba, RGB template-search tracking, and degradation robustness.
- It does not imply novelty in Mamba tracking by itself.
- It does not imply a universal solution to all degraded tracking settings.
- It keeps the distinction from image restoration, multimodal tracking, nighttime-only tracking, and motion prediction visible in the title.

## 2. One-sentence paper idea

This paper studies whether restoration-oriented Mamba designs can be adapted from image restoration to tracking-aware feature recovery for RGB template-search visual object tracking under generic image degradation, with validation based on localization and matching reliability rather than image quality alone.

## 3. Abstract draft

Visual object tracking requires accurate target localization across changing appearance, motion, background clutter, and image-quality degradation. Recent Mamba-based trackers have shown promise for temporal context modeling, memory, multimodal fusion, motion prediction, dynamic template update, and efficient visual tracking. However, the reviewed evidence indicates that these trackers do not systematically adapt restoration-oriented Mamba designs to recover target-discriminative features for RGB template-search tracking under generic degradations such as blur, noise, low resolution, compression, low light, and mixed corruption. In parallel, MambaIR and MambaIRv2 demonstrate that state-space models can be specialized for image restoration through restoration-specific blocks, local enhancement, channel selection, attentive state-space modeling, and semantic-guided token organization. These image restoration methods, however, optimize visual recovery rather than target localization, response-map reliability, or template-search matching.

We propose **TAR-MambaTrack**, a tracking-aware restoration Mamba framework for robust RGB template-search tracking under image degradation. The method is designed around a Restoration-Guided State Space Block that recovers tracking features rather than reconstructed pixels, with optional degradation prompt learning, template-guided attentive scanning, restoration-guided response fusion, and degradation-aware memory update. The training objective combines tracking loss with clean-degraded feature consistency, response-map consistency, and target-aware feature restoration so that restoration benefits are evaluated through tracking behavior. The planned experiments compare against standard RGB trackers, Mamba-based trackers, degradation/adverse-condition trackers, and restoration-preprocessing baselines under clean benchmarks, synthetic degradation, mixed degradation, real adverse-condition videos, cross-degradation generalization, response-map analysis, and efficiency measurements. The intended contribution is a careful study of the underexplored intersection between restoration-oriented Mamba and degradation-robust RGB template-search tracking, without claiming novelty in Mamba tracking, image restoration, low-light tracking, or memory alone.

## 4. Introduction structure

Paragraph 1: importance of visual object tracking and degradation challenges.

- Goal of the paragraph: Motivate visual object tracking as a localization problem that must remain reliable under real-world image-quality degradation.
- Key points: VOT tracks a target from an initial template through search frames; real videos contain blur, noise, compression, low resolution, low light, and mixed degradations; degraded observations weaken template-search matching and response-map reliability.
- Papers to cite: Standard tracker baselines such as OSTrack, MixFormer, SeqTrack, TransT, plus degradation-focused evidence from InvTrack and adverse-condition trackers.
- Safe wording: "Image-quality degradation can reduce feature discriminability and response-map reliability in RGB template-search tracking."
- Dangerous wording to avoid: Claims that degradation robustness has not been studied at all.

Paragraph 2: progress of Transformer and Mamba-based trackers.

- Goal of the paragraph: Place the work after modern tracking architectures.
- Key points: Transformer-based trackers advanced template-search interaction; Mamba-based trackers explore state-space modeling for temporal context, memory, dynamic templates, multimodal fusion, motion prediction, and efficient tracking.
- Papers to cite: MambaLCT, MCITrack, TemTrack, SMTrack, MambaVT, MambaEVT, MamTrack, Mamba-FETrack, MambaTrack MOT, MambaMOT, MM-Tracker, SportMamba, Multi-State Tracker, HyMamba, All-Day MCMT.
- Safe wording: "Existing Mamba trackers in the reviewed set mostly emphasize temporal, contextual, multimodal, dynamic-template, motion, or efficiency-oriented uses of state-space modeling."
- Dangerous wording to avoid: Any wording implying that Mamba has not been used for tracking.

Paragraph 3: MambaIR and MambaIRv2 show restoration-oriented Mamba benefits.

- Goal of the paragraph: Motivate restoration-oriented Mamba as a relevant technical source.
- Key points: MambaIR addresses restoration-specific issues such as local pixel forgetting and channel redundancy with local enhancement and channel attention; MambaIRv2 addresses causal scanning limitations using attentive state-space restoration and semantic-guided neighboring; both optimize image restoration tasks.
- Papers to cite: MambaIR, MambaIRv2.
- Safe wording: "MambaIR and MambaIRv2 show that state-space models can be adapted for restoration-oriented image recovery."
- Dangerous wording to avoid: Claims that these methods solve tracking or report target-localization behavior.

Paragraph 4: gap.

- Goal of the paragraph: State the missing intersection narrowly and defensibly.
- Key points: InvTrack studies degradation-invariant RGB template-search tracking but does not use restoration-oriented Mamba state-space recovery; MambaIR/MambaIRv2 are not tracking methods; existing Mamba trackers mostly use Mamba for other tracking functions; low-light/night UAV trackers do not cover generic RGB degradation robustness across blur, noise, low resolution, compression, and mixed degradation.
- Papers to cite: InvTrack, MambaIR, MambaIRv2, MambaTrack Night UAV, MambaNUT, MambaLCT, MCITrack, TemTrack, SMTrack.
- Safe wording: "Tracking-aware restoration-guided Mamba for generic degraded RGB template-search tracking remains underexplored in the reviewed evidence."
- Dangerous wording to avoid: Absolute absence claims about Mamba tracking, degradation tracking, memory, or low-light tracking.

Paragraph 5: proposed solution.

- Goal of the paragraph: Introduce TAR-MambaTrack.
- Key points: Adapt restoration-oriented Mamba to tracking features; use RG-SSB for state-space feature recovery; optionally use degradation prompt, template-guided attentive scan, response fusion, and degradation-aware memory; optimize tracking and response behavior rather than image quality.
- Papers to cite: MambaIR and MambaIRv2 as inspiration; InvTrack as the degradation-tracking threat; Mamba trackers as context.
- Safe wording: "We study a tracking-aware restoration Mamba framework that recovers target-discriminative features under degradation."
- Dangerous wording to avoid: Claims that one module alone guarantees general robustness.

Paragraph 6: main contributions.

- Goal of the paragraph: Summarize precise and testable contributions.
- Key points: Framework, restoration-guided state-space block, tracking-aware losses and response/matching analysis, degradation protocol and comparisons.
- Papers to cite: Cite groups only where needed; detailed citations belong in Related Work.
- Safe wording: "Our contributions are designed to be validated through degradation-specific tracking metrics, response analysis, and ablations."
- Dangerous wording to avoid: Overstating expected performance before experiments exist.

## 5. Final research gap statement

Short version:

MambaIR and MambaIRv2 show that state-space models can be adapted for image restoration by addressing restoration-specific low-level vision issues. Existing Mamba trackers in the reviewed set mainly use Mamba for temporal memory, context modeling, multimodal fusion, motion prediction, dynamic template update, efficient backbones, or low-light/adverse-condition tracking. InvTrack directly studies degradation-invariant RGB template-search tracking, but it does not use restoration-guided state-space modeling from MambaIR/MambaIRv2. This leaves an underexplored gap: restoration-guided Mamba for degradation-robust RGB template-search tracking across blur, noise, low resolution, compression, and mixed degradation.

Full version:

Restoration-oriented Mamba has been established for image restoration through designs such as local enhancement, channel attention or selection, attentive state-space restoration, and semantic-guided neighboring. In visual tracking, the reviewed Mamba-based methods instead mainly exploit state-space modeling for temporal context, hidden-state memory, multimodal fusion, motion prediction, dynamic template update, efficient backbones, or specialized adverse-condition tracking. InvTrack partially overlaps with the application setting by studying degradation-invariant RGB template-search tracking with clean-degraded consistency, low-pass residual modules, and response-map fusion, but it does not adapt restoration-oriented Mamba blocks for tracking-aware feature recovery. Therefore, the reviewed evidence supports a narrow and testable gap: restoration-guided Mamba for generic degraded RGB template-search tracking, where the goal is target localization and matching reliability rather than visually complete image reconstruction.

Conservative version:

Within the reviewed paper set, restoration-oriented Mamba is well supported for image restoration, and degradation-invariant RGB tracking is partially addressed by InvTrack. However, the direct adaptation of restoration-oriented state-space recovery to tracking-aware RGB template-search matching under general image-quality degradation appears insufficiently explored. A defensible paper should therefore study this intersection cautiously, compare against InvTrack and restoration-preprocessing baselines, and evaluate localization and response reliability rather than claiming broad novelty in Mamba tracking or degradation robustness.

Final recommended version:

Restoration-oriented Mamba has been established for image restoration, while degradation-invariant RGB template-search tracking has been partially addressed without Mamba restoration. Existing Mamba trackers in the reviewed evidence mainly use state-space modeling for temporal context, memory, dynamic templates, multimodal fusion, motion prediction, efficient tracking, or nighttime/adverse tracking. The underexplored intersection is tracking-aware restoration-guided Mamba for generic degraded RGB template-search tracking, where restoration is optimized for target-discriminative feature recovery, matching reliability, and localization rather than full-image visual reconstruction.

## 6. Related work plan

1. Mamba for image restoration.

- Papers to cite: MambaIR, MambaIRv2.
- Key message: These works demonstrate restoration-oriented Mamba designs for image recovery, including local enhancement, channel attention or selection, attentive state-space restoration, and semantic-guided neighboring.
- Gap connection: They motivate restoration-guided Mamba modules but do not directly solve template-search target localization.
- What not to overclaim: Do not state that restoration Mamba has no relation to tracking; state that the reviewed restoration papers optimize image restoration rather than tracking.

2. Mamba for temporal/contextual visual tracking.

- Papers to cite: MambaLCT, MCITrack, TemTrack, SMTrack.
- Key message: These works show Mamba can model long-term context, hidden states, track tokens, temporal cues, memory, or dynamic template behavior.
- Gap connection: Temporal memory and context are important but different from degradation-aware feature recovery.
- What not to overclaim: Do not imply that memory or temporal Mamba is absent from tracking.

3. Mamba for multimodal and specialized tracking.

- Papers to cite: Mamba-FETrack, MamTrack, MambaEVT, MambaVT, HyMamba, All-Day MCMT, and vision-language evidence available in the reviewed set.
- Key message: Mamba supports multimodal fusion, event/RGB-event tracking, RGB-T tracking, hyperspectral tracking, all-day multi-camera tracking, and specialized modality settings.
- Gap connection: These methods often gain robustness from extra sensors or modalities, which is different from RGB-only image-quality degradation recovery.
- What not to overclaim: Do not treat multimodal robustness as equivalent to RGB-only degradation robustness, and do not invent details for papers not represented by cards.

4. Mamba for motion prediction and multi-object tracking.

- Papers to cite: MambaTrack MOT, MambaMOT, MM-Tracker, SportMamba.
- Key message: These works use Mamba for motion prediction, nonlinear trajectory modeling, detection/association, sports tracking, UAV motion, or MOT robustness.
- Gap connection: Motion prediction and association differ from restoring degraded visual features for single-object template-search matching.
- What not to overclaim: Do not frame MOT motion modeling as irrelevant; frame it as addressing a different tracking failure mode.

5. Degradation-robust and low-light tracking.

- Papers to cite: InvTrack, MambaTrack Night UAV, MambaNUT, All-Day MCMT, MM-Tracker where relevant to blur.
- Key message: InvTrack is the strongest degradation-invariant RGB tracking threat; night UAV and low-light Mamba trackers address important adverse lighting scenarios; All-Day MCMT uses infrared/lighting-guided multimodal robustness.
- Gap connection: These works partially address robustness but do not fully cover tracking-aware restoration-oriented Mamba for general RGB degradations.
- What not to overclaim: Do not treat low-light tracking as the same as blur/noise/low-resolution/JPEG/mixed degradation tracking.

6. Positioning of our work.

- Papers to cite: MambaIR, MambaIRv2, InvTrack, MambaLCT, MCITrack, TemTrack, SMTrack, MambaTrack Night UAV, MambaNUT, MambaVT, MambaEVT, MamTrack.
- Key message: TAR-MambaTrack studies a narrow intersection: restoration-guided Mamba for RGB template-search feature recovery under generic degradation.
- Gap connection: This subsection should transition directly into the method by emphasizing tracking-aware feature recovery and response reliability.
- What not to overclaim: Do not claim the component ideas are absent; claim that their direct tracking-aware combination remains underexplored in the reviewed evidence.

## 7. Main contributions

1. We propose a restoration-guided Mamba tracking framework for RGB template-search tracking under generic image degradation, where restoration is optimized for target localization and matching reliability rather than pixel-level visual reconstruction.

2. We design a Tracking-Aware Restoration State Space Block that adapts restoration-oriented Mamba ideas such as local enhancement, channel selection, and state-space modeling to target-discriminative feature recovery.

3. We introduce tracking-specific mechanisms for degraded template-search matching, such as template-guided attentive scanning and restoration-guided response fusion, with degradation-aware memory treated as an optional extension.

4. We define an evaluation protocol for degradation-robust RGB tracking that includes template/search degradation asymmetry, mixed degradation, cross-degradation generalization, response-map analysis, restoration-preprocessing baselines, and comparisons against InvTrack and existing Mamba trackers.

## 8. Problem formulation

Given an initial template image `Z` with target box `B_0` and a sequence of search frames `{X_t}`, visual object tracking estimates the target state `B_t` in each frame. In clean tracking, the tracker learns a mapping:

```text
B_t = T(Z, X_t; B_0)
```

Under degradation, the observed template and search images can be written as:

```text
Z_d = D_i(Z)
X_{t,d} = D_j(X_t)
```

where `D_i` and `D_j` are degradation operators such as blur, noise, low resolution, compression, low light, or mixed degradation. The template and search image may be degraded differently, which is important because template-search matching can fail when either side is corrupted.

The goal is not to reconstruct clean images `Z` or `X_t`. The goal is to learn restoration-guided tracking features:

```text
F_z^r, F_x^r = Phi_rg(Z_d, X_{t,d})
```

such that the tracker predicts accurate target boxes and reliable response maps:

```text
B_t, R_t = H(F_z^r, F_x^r)
```

During training, clean/degraded pairs can be used for feature and response consistency. During inference, no clean image is assumed.

## 9. Proposed method overview

The method follows the architecture from `reports/08_method_architecture.md`.

Inputs:

- Template image `Z`.
- Search image `X_t`.
- Optional degradation token `d_t`.
- Optional historical memory state `M_{t-1}`.

Main components:

1. Input representation: patch embedding or shallow feature extraction for template and search images.
2. Restoration-Guided State Space Block: feature-level restoration using Mamba, local enhancement, channel selection, and residual recovery.
3. Degradation token or prompt: optional module that estimates degradation type/severity and modulates restoration, fusion, or memory.
4. Template-guided attentive scan: optional module that routes search tokens based on template relevance.
5. Restoration-guided response fusion: combines original, restoration-guided, and optional memory responses.
6. Optional degradation-aware memory update: prevents degraded frames from contaminating memory or dynamic templates.
7. Tracking head: predicts classification/center map and bounding box regression.

```text
     Template Z                     Search X_t
         |                              |
         v                              v
   Patch embedding                Patch embedding
         |                              |
         +--------------+---------------+
                        |
                        v
          Degradation prompt estimator G
                        |
                        v
       +-----------------------------------------+
       | Restoration-Guided Mamba Backbone       |
       | RG-SSB blocks: state-space + local      |
       | enhancement + channel selection         |
       +----------------+------------------------+
                        |
          +-------------+-------------+
          |                           |
          v                           v
    Template feature F_z^r      Search feature F_x^r
          |                           |
          +-------------+-------------+
                        |
                        v
           Template-Guided Attentive Scan
                        |
                        v
           Template-search interaction
                        |
             +----------+----------+
             |                     |
             v                     v
       Response R_o          Response R_r
             |                     |
             +----------+----------+
                        |
                        v
        Restoration-guided response fusion
                        |
                        v
             Tracking head: S_t, B_t
                        |
                        v
       Optional degradation-aware memory gate
```

## 10. Detailed method section outline

### 3.1 Overview

- Purpose: Present the full tracking pipeline and clarify which modules are essential versus optional.
- Technical details to include: Inputs, outputs, base tracker, degraded observations, feature-level restoration goal, inference without clean images.
- Equations needed: `Z_d = D_i(Z)`, `X_d = D_j(X)`, `B_t = H(F_z^r, F_x^r)`.
- Connection to prior work: Use MambaIR/MambaIRv2 as restoration inspiration; use InvTrack as degradation-tracking motivation; cite Mamba trackers as evidence of state-space tracking relevance.
- Distinction: The method is tracking-aware feature recovery, not image restoration, invariant learning alone, temporal memory alone, or multimodal robustness.

### 3.2 Restoration-Guided State Space Block

- Purpose: Define RG-SSB as the core method module.
- Technical details to include: Mamba branch, local enhancement branch, channel selection, residual connection, optional degradation modulation.
- Equations needed: `F' = RGSSB(F, d)`, branch fusion, channel selection, residual update.
- Connection to prior work: MambaIR's restoration-specific state-space block, local enhancement, and channel attention.
- Distinction: Optimized by tracking loss, feature consistency, response consistency, and target-aware feature recovery rather than pixel reconstruction.

### 3.3 Degradation Prompt Learning

- Purpose: Estimate degradation type/severity and provide adaptive restoration control.
- Technical details to include: Template/search feature pooling, degradation distribution, severity score, reliability score, test-time prediction without labels.
- Equations needed: `d = G(F_z, F_x)`, `p_deg = softmax(W_c d)`, `q = 1 - s_deg`.
- Connection to prior work: Degradation-aware training from InvTrack and adverse-condition trackers, but used here to modulate restoration-guided tracking features.
- Distinction: The prompt is optional and task-aligned; it should not require explicit test-time degradation labels.

### 3.4 Template-Guided Attentive Scan

- Purpose: Adapt attentive/semantic token organization from restoration to template-search tracking.
- Technical details to include: Template prototype, search-token similarity, target-aware routing, sparse scan, inverse routing.
- Equations needed: `p_z = Pool_target(F_z)`, `s_i = cosine(W_q x_i, W_k p_z)`, `F_x^{tg} = TGAS(F_z, F_x)`.
- Connection to prior work: MambaIRv2's attentive state-space restoration and semantic-guided neighboring.
- Distinction: MambaIRv2 groups image tokens for restoration; TG-AS groups template-relevant search tokens for tracking.

### 3.5 Restoration-Guided Response Fusion

- Purpose: Improve final matching reliability by adaptively fusing original and restoration-guided responses.
- Technical details to include: Original response, restoration-guided response, optional memory response, reliability-conditioned weights.
- Equations needed: `R = alpha_o R_o + alpha_r R_r + alpha_m R_m`.
- Connection to prior work: InvTrack's response-map fusion is the main threat.
- Distinction: The proposed fusion must be conditioned on restoration-guided state-space recovery, not only clean/degraded invariant response fusion.

### 3.6 Degradation-Aware Memory Update, optional

- Purpose: Prevent unreliable degraded observations from contaminating memory or dynamic templates.
- Technical details to include: Confidence, degradation severity, response sharpness, restored feature reliability, memory gate.
- Equations needed: `M_t = g_t Update(M_{t-1}, F_t) + (1 - g_t) M_{t-1}`.
- Connection to prior work: MCITrack, MambaLCT, TemTrack, SMTrack, MambaEVT, and MambaVT use memory/context/dynamic templates in different ways.
- Distinction: Temporal memory is not the claimed novelty; if included, the memory gate must be explicitly degradation-aware and restoration-reliability-aware.

### 3.7 Training Objectives

- Purpose: Define losses that make restoration useful for tracking.
- Technical details to include: Tracking loss, feature consistency, response consistency, target-aware feature restoration, degradation prompt loss, optional memory reliability loss.
- Equations needed: Full total loss.
- Connection to prior work: InvTrack's consistency is related; MambaIR/MambaIRv2 restoration losses are related but not sufficient.
- Distinction: Losses are evaluated by target localization and response maps, not PSNR or SSIM alone.

### 3.8 Inference Procedure

- Purpose: Explain how the method works when only degraded observations are available.
- Technical details to include: Template crop, search crop, degradation prompt prediction, RG-SSB features, optional TG-AS, response fusion, box prediction, optional memory update.
- Equations needed: `B_t = H(R_t)`.
- Connection to prior work: Standard tracking inference.
- Distinction: No clean image or explicit degradation label is assumed at test time.

## 11. Mathematical formulation

1. Degraded template/search:

```text
Z_d = D_i(Z),     X_{t,d} = D_j(X_t)
```

`Z` is the clean template, `X_t` is the clean search frame, `D_i` and `D_j` are degradation operators, and `Z_d`, `X_{t,d}` are observed degraded inputs. In real inference, clean `Z` and `X_t` are unavailable.

2. Feature extraction:

```text
F_z, F_x = Backbone(Z_d, X_{t,d})
```

`F_z` and `F_x` are template and search features from the base tracker backbone or patch embedding.

3. Restoration-guided Mamba block:

```text
F' = RGSSB(F, d)
```

Expanded form:

```text
U = LN(F)
G_s = VSSM_2D(U; theta_s(d))
G_l = Conv_{3x3}(U)
a_c = sigmoid(MLP([GAP(U), d]))
F' = F + gamma(d) * Proj(a_c * [G_s, G_l])
```

`G_s` is the state-space branch, `G_l` is the local enhancement branch, `a_c` is channel selection, and `gamma(d)` is optional degradation modulation.

4. Degradation token:

```text
d = G(F_z, F_x)
```

Expanded form:

```text
e_z = Pool(phi_deg(F_z))
e_x = Pool(phi_deg(F_x))
d = MLP([e_z, e_x, abs(e_z - e_x)])
p_deg = softmax(W_c d)
s_deg = sigmoid(W_s d)
q = 1 - s_deg
```

`p_deg` is an optional degradation type distribution, `s_deg` is severity, and `q` is feature reliability.

5. Template-guided attentive scan:

```text
S = TGAS(F_z, F_x)
```

Expanded form:

```text
p_z = Pool_target(F_z)
s_i = cosine(W_q x_i, W_k p_z)
P = Route(s, spatial_bins)
tilde_X = P X
h_i = A(d, s_i) h_{i-1} + B(d, s_i) tilde_x_i
y_i = C(d, s_i) h_i + D tilde_x_i
S = P^{-1} Y
```

`p_z` is the target template prototype, `s_i` is template relevance for each search token, `P` is a routing matrix, and `S` is the target-aware scanned feature sequence. This module is optional in the minimal version.

6. Response fusion:

```text
R = alpha_o R_o + alpha_r R_r + alpha_m R_m
```

`R_o` is the original response, `R_r` is the restoration-guided response, and `R_m` is an optional memory response. The weights are:

```text
[alpha_o, alpha_r, alpha_m] = softmax(MLP([q, sharp(R_o), sharp(R_r), sharp(R_m)]))
```

If memory is not used, `R_m` and `alpha_m` are removed.

7. Memory update, optional:

```text
g_t = sigmoid(w_c c_t + w_q q_t + w_r rho_t - w_s s_t + b)
M_t = g_t Update(M_{t-1}, F_t^r) + (1 - g_t) M_{t-1}
```

`c_t` is tracking confidence, `q_t` is reliability, `rho_t` is response sharpness, `s_t` is degradation severity, and `F_t^r` is the current restoration-guided target feature.

8. Total loss:

```text
L_total = L_track
        + lambda_1 L_feat
        + lambda_2 L_resp
        + lambda_3 L_targRest
        + lambda_4 L_deg
        + lambda_5 L_mem
```

`L_track` is mandatory. `L_feat` and `L_resp` are recommended for the minimal model. `L_targRest`, `L_deg`, and `L_mem` can be added based on implementation scope.

## 12. Loss functions

| loss | purpose | formula | reviewer concern addressed | essential or optional |
|---|---|---|---|---|
| Tracking loss | Train target localization. | `L_track = L_cls + beta_1 L1(B, B*) + beta_2 GIoU(B, B*)` | Ensures restoration is evaluated through tracking, not image quality. | Essential |
| Clean-degraded feature consistency | Align degraded/restored features with clean tracking features. | `L_feat = || stopgrad(F_clean) - F_degraded^r ||_1` | Addresses whether degraded feature recovery is learned. | Recommended |
| Response-map consistency | Preserve localization response under degradation. | `L_resp = KL(softmax(R_clean) || softmax(R_degraded^r))` | Addresses template-search matching reliability. | Recommended |
| Target-aware feature restoration | Focus recovery around the target region. | `L_targRest = || M_target * (F_clean - F_degraded^r) ||_1` | Addresses "generic restoration may not help tracking." | Optional but useful |
| Degradation prompt loss | Supervise degradation type/severity when labels exist. | `L_deg = CE(p_deg, y_deg) + || s_deg - y_sev ||_1` | Addresses whether degradation prompt is meaningful. | Optional |
| Memory reliability loss | Supervise update gates when memory is included. | `L_mem = BCE(g_t, y_reliable)` | Addresses degraded memory contamination. | Optional |

## 13. Training protocol

Stage 1: base tracker initialization.

- Choose a base tracker, preferably an OSTrack-style or similar one-stream RGB tracker.
- Initialize from a pretrained checkpoint if available.
- Verify clean benchmark behavior before adding degradation modules.

Stage 2: synthetic degradation training.

- Generate degraded template/search pairs.
- Include clean template + degraded search.
- Include degraded template + clean search.
- Include degraded template + degraded search.
- Include different degradation types in template and search.
- Include mixed degradation.

Stage 3: train restoration-guided Mamba modules.

- Insert RG-SSB into selected backbone or interaction stages.
- Train with `L_track`, `L_feat`, and `L_resp`.
- Compare against base tracker, base plus generic Mamba, and base plus non-Mamba restoration block.

Stage 4: add degradation prompt.

- Add degradation prompt only after RG-SSB is stable.
- Use synthetic labels for degradation type/severity during training if available.
- Keep inference label-free by predicting prompts from features.

Stage 5: add optional memory module.

- Add only if long-sequence drift or template contamination becomes a clear failure.
- Compare no memory, confidence-only memory, and degradation-aware memory.

Stage 6: optional real degraded fine-tuning.

- Fine-tune only if real degraded training data are available with appropriate splits.
- Keep a separate evaluation-only protocol if training data availability is uncertain.

Difference from InvTrack:

- InvTrack focuses on degradation-invariant learning, clean-degraded consistency, low-pass residual modules, and response fusion.
- TAR-MambaTrack must train restoration-guided state-space feature recovery and tracking-aware matching losses.
- Direct comparisons should include InvTrack or an InvTrack-style consistency baseline to avoid relying on a vague distinction.

## 14. Datasets

### Standard RGB SOT datasets

| dataset | role | why useful | metrics | gap tested |
|---|---|---|---|---|
| LaSOT | Training/testing depending on protocol | Large-scale long-term RGB SOT with diverse appearance changes. | AUC, precision, normalized precision. | General tracking behavior and long-sequence robustness. |
| GOT-10k | Training/testing under official split | Standard general object tracking benchmark. | AO, SR0.5, SR0.75. | Generalization to unseen object classes and clean/degraded comparison. |
| TrackingNet | Training/testing depending on available protocol | Large-scale web video benchmark. | AUC, precision, normalized precision. | Broad RGB tracking performance. |
| OTB100 | Testing | Lightweight benchmark useful for quick checks and classic attributes. | Success/AUC, precision. | Early debugging and attribute-based degradation sensitivity. |
| UAV123 | Testing | UAV tracking with scale, motion, and viewpoint variation. | AUC, precision. | UAV robustness and fast motion under synthetic degradation. |
| NfS | Testing | High-frame-rate tracking with motion-related challenges. | AUC, precision. | Motion blur and fast-motion stress cases. |

### Adverse or degraded tracking datasets

| dataset | role | why useful | metrics | gap tested |
|---|---|---|---|---|
| AVisT | Testing | Adverse visual tracking conditions. | Success/AUC, precision, normalized precision if supported. | Real adverse-condition robustness. |
| UAVDark70 | Testing | Dark UAV tracking scenarios. | AUC, precision. | Low-light UAV robustness. |
| UAVDark135 | Testing | Larger dark UAV tracking evaluation. | AUC, precision. | Low-light/night UAV comparison against MambaTrack Night UAV and MambaNUT. |
| DarkTrack2021 | Testing | Dark or low-light tracking sequences. | AUC, precision. | Low-light robustness without treating it as all degradation. |
| NAT2021 | Testing | Nighttime aerial tracking. | AUC, precision. | Night tracking and aerial degradation. |
| NAT2021L | Testing | Long nighttime aerial tracking. | AUC, precision, failure rate if available. | Long-sequence adverse-condition robustness. |

### Synthetic degradation versions

| dataset | role | why useful | metrics | gap tested |
|---|---|---|---|---|
| Degraded LaSOT | Training/testing split | Large-scale synthetic degradation evaluation. | AUC, precision, normalized precision, robustness drop. | Generic degradation robustness. |
| Degraded GOT-10k | Testing under official-style protocol | Measures degradation effect on generalization. | AO, SR0.5, SR0.75, robustness drop. | Degradation generalization. |
| Degraded TrackingNet | Training/testing if feasible | Broad data distribution for synthetic degradation. | AUC, precision, normalized precision. | Scalability of degraded tracking. |
| Degraded UAV123 | Testing | UAV-specific degradation stress test. | AUC, precision, robustness drop. | UAV motion plus image-quality degradation. |

## 15. Degradation protocol

Degradation types:

| degradation | severity levels | apply to template/search/both | why it matters for tracking | expected challenge |
|---|---|---|---|---|
| Motion blur | Mild, medium, severe kernel length/angle. | Template, search, or both. | Smears target edges and weakens response peaks. | Localization drift and distractor confusion. |
| Defocus blur | Mild, medium, severe blur radius. | Template, search, or both. | Removes local texture and detail. | Weak template-search similarity. |
| Gaussian noise | Mild, medium, severe sigma. | Template, search, or both. | Corrupts local appearance features. | Noisy response maps and unstable confidence. |
| Sensor noise | Mild, medium, severe signal-dependent noise. | Template, search, or both. | Mimics low-quality capture artifacts. | Channel-level feature corruption. |
| Low resolution | Mild, medium, severe downsample/upsample factor. | Template, search, or both. | Removes fine target structure. | Poor scale/box regression. |
| JPEG compression | Mild, medium, severe quality factor. | Template, search, or both. | Introduces blocking artifacts. | False texture matches. |
| Low light | Mild, medium, severe brightness/gamma/noise. | Template, search, or both. | Reduces visibility and contrast. | Low-confidence response maps. |
| Mixed degradation | Two or more corruptions at controlled severity. | Template, search, or both. | Reflects compound real-world degradation. | Cross-degradation failure and response ambiguity. |

Separate settings:

1. Clean template + degraded search.
2. Degraded template + clean search.
3. Degraded template + degraded search.
4. Different degradations in template and search.
5. Mixed degradation in either or both branches.

The protocol should report both absolute degraded performance and degradation robustness drop.

## 16. Experiments

Experiment 1: standard tracking benchmark comparison.

- Purpose: Verify that the method does not sacrifice normal RGB tracking behavior.
- Setup: Evaluate on clean LaSOT, GOT-10k, TrackingNet, UAV123, OTB100, or a subset based on compute.
- Baselines: Standard RGB trackers, base tracker, relevant Mamba trackers.
- Metrics: AUC, precision, normalized precision, AO, SR0.5, SR0.75.
- Conclusion it should support: The method remains a valid tracker, not only a degradation-specific model.

Experiment 2: synthetic degradation benchmark.

- Purpose: Test robustness under controlled degradation.
- Setup: Apply each degradation type at mild, medium, and severe levels to selected datasets.
- Baselines: Base tracker, InvTrack, MambaIR/MambaIRv2 preprocessing plus tracker, Mamba trackers if runnable.
- Metrics: Clean performance, degraded performance, robustness drop, relative robustness.
- Conclusion it should support: Restoration-guided tracking features reduce degradation sensitivity.

Experiment 3: mixed degradation robustness.

- Purpose: Test whether the method handles compound corruptions.
- Setup: Combine blur/noise/compression/low-resolution/low-light in controlled sequences.
- Baselines: Same as Experiment 2.
- Metrics: AUC, precision, robustness drop, failure rate.
- Conclusion it should support: The method is not limited to one degradation class.

Experiment 4: real adverse-condition evaluation.

- Purpose: Check transfer beyond synthetic corruption.
- Setup: Evaluate on AVisT, UAVDark70, UAVDark135, DarkTrack2021, NAT2021, NAT2021L as available.
- Baselines: Low-light/adverse trackers, MambaTrack Night UAV, MambaNUT, standard trackers.
- Metrics: Dataset-standard success/precision and failure rate if available.
- Conclusion it should support: Synthetic degradation gains are relevant to real adverse videos, with low-light analyzed separately.

Experiment 5: cross-degradation generalization.

- Purpose: Test whether learned recovery transfers across degradation types.
- Setup: Train on blur, test on noise; train on noise, test on JPEG; train on single degradations, test on mixed; leave-one-degradation-out.
- Baselines: Base tracker, degradation-trained base tracker, RG-SSB variants.
- Metrics: Robustness drop and relative robustness.
- Conclusion it should support: Improvements are not only memorization of one synthetic corruption.

Experiment 6: template/search degradation analysis.

- Purpose: Isolate template-search asymmetry.
- Setup: Evaluate clean template/degraded search, degraded template/clean search, both degraded, and mismatched degradation types.
- Baselines: Base tracker, InvTrack, restoration preprocessing, full method.
- Metrics: AUC, precision, response sharpness, failure rate.
- Conclusion it should support: The method addresses template-search matching, not only frame enhancement.

Experiment 7: response-map analysis.

- Purpose: Show whether restoration-guided features improve matching behavior.
- Setup: Visualize response maps for clean, degraded, externally restored, RG-SSB, and full model.
- Baselines: Base tracker, MambaIR preprocessing, InvTrack-style response fusion.
- Metrics: Peak sharpness, peak-to-sidelobe ratio, distractor suppression, localization error.
- Conclusion it should support: Feature recovery improves target localization signals.

Experiment 8: efficiency comparison.

- Purpose: Defend practical tracking use.
- Setup: Measure runtime and model size under the same hardware and input resolution.
- Baselines: Base tracker, external restoration plus tracker, RG-SSB minimal model, full model.
- Metrics: FPS, FLOPs, parameters, GPU memory.
- Conclusion it should support: Feature-level restoration is more practical than full external image restoration if the measured cost supports that claim.

Experiment 9: failure case analysis.

- Purpose: Identify limits and avoid overclaiming.
- Setup: Collect failures under full occlusion, extreme low light, severe blur, heavy compression, similar distractors, out-of-view, scale change, and mixed degradation.
- Baselines: Base tracker and strongest threat baseline.
- Metrics: Qualitative examples, failure rate, response maps.
- Conclusion it should support: The method has known limitations and future-work directions.

## 17. Baselines

### A. Standard RGB trackers

| baseline | why needed | novelty threat addressed |
|---|---|---|
| OSTrack | Strong one-stream RGB tracker and practical base architecture candidate. | Shows gains are not due to choosing a weak tracker. |
| MixFormer | Strong template-search transformer-style tracker. | Tests against modern non-Mamba tracking. |
| SeqTrack | Sequence-style tracking baseline. | Tests against alternative sequence modeling. |
| TransT | Classic transformer template-search tracker. | Establishes historical template-search comparison. |
| Siamese-based trackers if useful | Useful for correlation-head comparisons and lightweight baselines. | Tests whether gains are tied to one-stream architecture. |

### B. Mamba-based trackers

| baseline | why needed | novelty threat addressed |
|---|---|---|
| MambaLCT | Long-term/context Mamba tracking. | Distinguishes restoration-guided recovery from temporal context. |
| MCITrack | Context/memory-style Mamba tracking. | Distinguishes degradation-aware recovery from hidden-state memory. |
| TemTrack | Temporal tracking with Mamba-style cues. | Distinguishes temporal propagation from degraded feature recovery. |
| SMTrack | Strong temporal/dynamic-template Mamba threat. | Distinguishes restoration-guided RGB degradation handling from memory/template update. |
| TrackingMamba if available | Additional Mamba tracker baseline if code/evidence is available. | Broadens Mamba tracking comparison without inventing unsupported claims. |

### C. Degradation/adverse trackers

| baseline | why needed | novelty threat addressed |
|---|---|---|
| InvTrack | Strongest degradation-invariant RGB template-search threat. | Tests whether restoration-guided Mamba adds more than invariant learning and response fusion. |
| MambaTrack Night UAV | Low-light/night UAV Mamba tracking threat. | Distinguishes generic RGB degradation from nighttime-specific tracking. |
| MambaNUT | Nighttime UAV Mamba and curriculum threat. | Tests whether curriculum/night robustness already covers the claim. |
| Other low-light/adverse trackers if relevant | Needed for real low-light datasets. | Prevents narrow comparison against only Mamba methods. |

### D. Restoration-preprocessing baselines

| baseline | why needed | novelty threat addressed |
|---|---|---|
| MambaIR + tracker | Direct restoration Mamba preprocessing threat. | Tests whether image restoration before tracking is enough. |
| MambaIRv2 + tracker | Stronger restoration Mamba preprocessing threat. | Tests whether attentive restoration alone solves degraded tracking. |
| Low-light enhancer + tracker | Low-light-specific enhancement baseline. | Distinguishes general degradation recovery from low-light enhancement. |
| Generic restoration model + tracker | Non-Mamba restoration preprocessing control. | Tests whether gains are from restoration generally, not Mamba-specific design. |

### E. Internal ablation baselines

| baseline | why needed | novelty threat addressed |
|---|---|---|
| Base tracker | Primary control. | Measures true add-on effect. |
| Base + vanilla Mamba | Tests generic Mamba insertion. | Addresses "the gain is only from Mamba capacity." |
| Base + restoration block without Mamba | Tests non-Mamba restoration features. | Addresses "Mamba is unnecessary." |
| Base + RG-SSB | Tests core proposed block. | Isolates restoration-guided state-space recovery. |
| Full model | Tests combined method. | Shows whether optional modules help beyond the core. |

## 18. Evaluation metrics

Tracking metrics:

- AUC / Success.
- Precision.
- Normalized Precision.
- AO for GOT-10k.
- SR0.5 for GOT-10k.
- SR0.75 for GOT-10k.

Efficiency metrics:

- FPS.
- FLOPs.
- Parameters.
- GPU memory.

Robustness metrics:

```text
Drop = Clean performance - Degraded performance
```

Relative robustness:

```text
Relative robustness = Degraded performance / Clean performance
```

Additional analysis metrics:

- Response-map sharpness.
- Peak-to-sidelobe ratio.
- Tracking failure rate if the benchmark/protocol supports it.
- Localization error under degradation.

The robustness metrics should be reported separately for each degradation type, severity level, template/search setting, and mixed degradation setting.

## 19. Ablation studies

| ablation | what it tests | expected conclusion | reviewer criticism addressed |
|---|---|---|---|
| Without RG-SSB | Necessity of the core restoration-guided Mamba block. | RG-SSB should be needed for degraded feature recovery if the idea is valid. | "The method is only degradation training." |
| Without local enhancement | Role of local detail recovery. | Local enhancement should help blur, low resolution, and compression. | "The Mamba block does not need restoration-specific design." |
| Without channel attention/selection | Role of suppressing degraded/redundant channels. | Channel selection should help noise and compression sensitivity. | "Channel branch is decorative." |
| Without degradation token | Role of adaptive degradation awareness. | Token should help mixed and cross-degradation settings if useful. | "The prompt is unnecessary." |
| Without template-guided attentive scan | Role of target-aware token routing. | TG-AS should improve matching/localization if justified. | "This is generic Mamba scanning." |
| Without response-map fusion | Role of original/restoration response combination. | Fusion should help when restoration is useful but imperfect. | "InvTrack already covers response fusion." |
| Without feature consistency loss | Role of clean-degraded feature alignment. | Feature consistency should reduce degradation-induced feature drift. | "The recovery objective is not trained." |
| Without response consistency loss | Role of matching-level alignment. | Response consistency should improve localization reliability. | "Restoration does not improve tracking response." |
| Without degradation curriculum | Role of progressive degradation training. | Curriculum should stabilize severe/mixed degradation training if used. | "The model only benefits from data augmentation." |
| Without memory update | Whether memory is necessary. | Core should still work; memory may help long sequences. | "The paper over-relies on memory." |
| Confidence-only memory vs degradation-aware memory | Whether degradation reliability matters beyond confidence. | Degradation-aware memory should reduce drift if memory is included. | "Temporal memory already solves it." |
| Image-level restoration preprocessing vs feature-level restoration | Whether external restoration is enough. | Tracking-aware feature restoration should be more aligned with localization if the method is valid. | "This is just MambaIR plus tracker." |

The "expected conclusion" column defines hypotheses to test, not results.

## 20. Figures to include

Figure 1: motivation figure showing degraded tracking challenge.

- What it should show: Clean tracking response versus degraded tracking response for the same sequence; examples of blur, noise, low resolution, JPEG, and low light.
- Where it belongs: Introduction.
- Why useful: Visually motivates why degraded RGB template-search matching fails.

Figure 2: overall architecture.

- What it should show: Template/search inputs, degradation prompt, RG-SSB backbone, TG-AS, response fusion, tracking head, optional memory.
- Where it belongs: Method overview.
- Why useful: Clarifies the full pipeline and optional modules.

Figure 3: Restoration-Guided State Space Block.

- What it should show: Mamba branch, local enhancement branch, channel selection, residual path, degradation modulation.
- Where it belongs: Method section 3.2.
- Why useful: Shows how MambaIR-inspired restoration is adapted to tracking features.

Figure 4: Template-Guided Attentive Scan.

- What it should show: Template prototype, search token similarity, routed sequence, state-space scan, inverse routing.
- Where it belongs: Method section 3.4.
- Why useful: Distinguishes target-aware scanning from generic semantic-guided restoration.

Figure 5: response-map comparison under degradation.

- What it should show: Base response, external restoration response, RG-SSB response, full model response.
- Where it belongs: Experiments or ablation analysis.
- Why useful: Demonstrates whether matching reliability improves.

Figure 6: memory update reliability visualization, optional.

- What it should show: Confidence, degradation severity, response sharpness, update gate over time.
- Where it belongs: Optional ablation section.
- Why useful: Supports degradation-aware memory only if included.

Figure 7: qualitative tracking results.

- What it should show: Tracking boxes under degradation across representative sequences and baselines.
- Where it belongs: Experiments.
- Why useful: Shows concrete behavior and failure modes.

## 21. Tables to include

| table | rows | columns | metrics | purpose |
|---|---|---|---|---|
| Table 1: standard benchmark comparison | Standard RGB trackers, Mamba trackers, ours | Datasets | AUC, precision, normalized precision, AO, SR0.5, SR0.75 | Show clean tracking competitiveness. |
| Table 2: synthetic degradation robustness | Baselines and ours | Degradation types/severities | AUC, precision, robustness drop | Test generic degradation robustness. |
| Table 3: mixed degradation | Baselines and ours | Mixed degradation settings | AUC, precision, drop | Test compound corruption. |
| Table 4: real adverse-condition tracking | Baselines and ours | Adverse datasets | Dataset-standard metrics | Test transfer to real degraded videos. |
| Table 5: ablation study | Internal variants | Modules removed | AUC, precision, drop, response sharpness | Validate modules. |
| Table 6: efficiency comparison | Base, external restoration, minimal model, full model | Runtime and size metrics | FPS, FLOPs, parameters, GPU memory | Defend practicality. |
| Table 7: novelty/module comparison | InvTrack, MambaIR, MambaIRv2, Mamba trackers, ours | Method properties | Qualitative coverage | Clarify distinctions in the paper. |

## 22. Reviewer risks and defense strategy

| reviewer risk | why reviewer may say it | defense | experiment or ablation needed |
|---|---|---|---|
| "This is just MambaIR + tracker." | MambaIR/MambaIRv2 already provide restoration Mamba. | Emphasize tracking-aware feature recovery, template-search losses, response reliability, and no pixel-reconstruction-only objective. | MambaIR/MambaIRv2 preprocessing plus tracker; feature-level versus image-level restoration ablation. |
| "This is just InvTrack + Mamba." | InvTrack already handles degradation-invariant tracking with consistency and response fusion. | Show restoration-guided state-space recovery beyond invariant consistency and low-pass residual modules. | InvTrack comparison; InvTrack-style consistency baseline; RG-SSB versus non-Mamba restoration block. |
| "Night UAV Mamba trackers already solve degradation." | MambaTrack Night UAV and MambaNUT address adverse/night tracking. | Frame low-light as one degradation, not the whole problem; evaluate blur, noise, low resolution, JPEG, and mixed degradation. | Non-low-light synthetic degradation and real adverse datasets. |
| "Temporal Mamba trackers already handle robustness." | MambaLCT, MCITrack, TemTrack, and SMTrack improve tracking through temporal/context mechanisms. | Distinguish temporal context from degraded feature recovery and template-search matching reliability. | Compare against temporal Mamba trackers; degraded template/search asymmetry tests. |
| "External restoration preprocessing is enough." | Restoration networks can improve degraded images before tracking. | Feature-level restoration is tracking-supervised and may be more efficient. | MambaIR/MambaIRv2 plus tracker; generic restoration plus tracker; efficiency table. |
| "Synthetic degradation is unrealistic." | Synthetic corruptions may not match real videos. | Include real adverse-condition evaluation and cross-degradation generalization. | AVisT, UAVDark, DarkTrack, NAT; leave-one-degradation-out tests. |
| "The method has too many modules." | RG-SSB, prompt, TG-AS, fusion, and memory may look over-combined. | Present RG-SSB as the core; mark memory and some prompts as optional; use staged ablations. | Minimal model results and incremental ablation table. |
| "The improvement may come from training data, not architecture." | Degradation augmentation itself can improve robustness. | Compare base tracker with the same degradation training against RG-SSB variants. | Base plus degradation training; vanilla Mamba; non-Mamba restoration block. |
| "The method is too heavy." | Restoration and Mamba modules may add runtime. | Keep feature-level restoration lightweight and report cost. | FPS, FLOPs, parameters, GPU memory. |
| "Template-guided scan is expensive." | Routing and sequence construction may add overhead. | Use sparse/top-k routing and apply TG-AS only in selected stages; postpone if not cost-effective. | Raster/four-direction/random/template-guided scan ablation with runtime. |

## 23. Minimal implementation roadmap

30-day plan:

Week 1:

- Choose the base tracker.
- Reproduce clean baseline on a small benchmark subset.
- Implement synthetic degradation pipeline for motion blur, Gaussian noise, low resolution, JPEG compression, and mixed medium severity.
- Create evaluation scripts for clean/degraded performance and robustness drop.

Week 2:

- Implement RG-SSB in one selected stage.
- Train the first model with tracking loss only.
- Run a small degradation evaluation on one standard benchmark subset.
- Check runtime and memory before adding modules.

Week 3:

- Add feature consistency and response consistency losses.
- Compare against base tracker with the same degradation training.
- Add restoration-preprocessing baseline if code is available.
- Compare against InvTrack if runnable; otherwise implement an InvTrack-style clean/degraded consistency control.

Week 4:

- Add either degradation prompt or template-guided attentive scan, not both at once.
- Run ablations for RG-SSB, local enhancement, channel selection, and losses.
- Prepare response-map visualizations and failure examples.

Minimum viable model:

- Base one-stream tracker + RG-SSB + synthetic degradation training + tracking loss + feature consistency + response consistency.

Minimum viable experiment:

- One standard dataset subset, one synthetic degradation protocol, base tracker comparison, external restoration-preprocessing comparison, and response-map visualization.

First failure check:

- If base plus degradation training matches RG-SSB, the architecture claim is weak.
- If MambaIRv2 preprocessing plus tracker matches the proposed method, the feature-level restoration distinction is weak.
- If RG-SSB is too slow, reduce insertion points and postpone TG-AS/memory.

## 24. Full implementation roadmap

Stage 1: proof of concept.

- Reproduce base tracker.
- Implement synthetic degradation.
- Add RG-SSB.
- Validate on a small clean/degraded benchmark.

Stage 2: full degradation evaluation.

- Expand to blur, defocus blur, Gaussian noise, sensor noise, low resolution, JPEG, low light, and mixed degradation.
- Evaluate template/search asymmetry.
- Add cross-degradation generalization.

Stage 3: ablation and efficiency.

- Run module ablations.
- Run loss ablations.
- Compare against external restoration preprocessing.
- Measure FPS, FLOPs, parameters, and GPU memory.

Stage 4: memory module if useful.

- Add degradation-aware memory only if drift under degraded long sequences is a clear failure case.
- Compare no memory, confidence-only memory, and degradation-aware memory.

Stage 5: writing and submission preparation.

- Finalize related work and method.
- Build final figures and tables.
- Write experiments and ablations.
- Write limitations and failure analysis.
- Perform final novelty audit against InvTrack, MambaIR, MambaIRv2, MambaTrack Night UAV, MambaNUT, SMTrack, and MCITrack.

## 25. Paper writing roadmap

| section | what to write | files to use | expected length | key figures/tables |
|---|---|---|---|---|
| Introduction | Motivation, evidence-backed gap, proposed direction, contributions. | `reports/06_research_gap_paragraph.md`, `reports/05b_final_recommendation.md`. | 1.5 to 2 pages. | Figure 1. |
| Related Work | Six-subsection related-work structure. | `reports/07_related_work_draft.md`, paper cards. | 1.5 to 2 pages. | Optional Table 7. |
| Method | Problem formulation, RG-SSB, prompt, TG-AS, fusion, optional memory, losses, inference. | `reports/08_method_architecture.md`, this plan. | 3 to 4 pages. | Figures 2, 3, 4. |
| Experiments | Datasets, protocol, baselines, metrics, main tables. | `reports/05_experiment_plan.md`, this plan. | 3 to 4 pages. | Tables 1 to 4, 6. |
| Ablations | Module/loss/response/efficiency ablations. | `reports/08_method_architecture.md`, this plan. | 1.5 to 2 pages. | Table 5, Figure 5. |
| Conclusion | Summary, limitations, future work. | Final results and failure cases. | 0.5 page. | Figure 7 optional. |

## 26. Final recommended paper outline

1. Abstract

2. Introduction

- Motivation: degradation in RGB template-search tracking.
- Existing Mamba trackers and restoration Mamba.
- Evidence-backed gap.
- TAR-MambaTrack overview.
- Contributions.

3. Related Work

- 3.1 Mamba for Image Restoration.
- 3.2 Mamba for Temporal and Contextual Visual Tracking.
- 3.3 Mamba for Multimodal and Specialized Tracking.
- 3.4 Mamba for Motion Prediction and Multi-Object Tracking.
- 3.5 Degradation-Robust, Low-Light, and Adverse-Condition Tracking.
- 3.6 Positioning of Our Work.

4. Method

- 4.1 Overview and Problem Formulation.
- 4.2 Restoration-Guided State Space Block.
- 4.3 Degradation Prompt Learning.
- 4.4 Template-Guided Attentive Scan.
- 4.5 Restoration-Guided Response Fusion.
- 4.6 Degradation-Aware Memory Update, optional.
- 4.7 Training Objectives.
- 4.8 Inference Procedure.

5. Experiments

- 5.1 Experimental Setup.
- 5.2 Datasets and Metrics.
- 5.3 Degradation Protocol.
- 5.4 Comparison on Standard Tracking Benchmarks.
- 5.5 Synthetic Degradation Robustness.
- 5.6 Real Adverse-Condition Evaluation.
- 5.7 Cross-Degradation and Template/Search Analysis.
- 5.8 Efficiency Comparison.

6. Ablation Study

- 6.1 Module Ablations.
- 6.2 Loss Ablations.
- 6.3 Response-Map Analysis.
- 6.4 Memory Update Analysis, optional.
- 6.5 Failure Cases.

7. Conclusion

- Summary.
- Limitations.
- Future work.

## 27. Final safe novelty statement

Within the reviewed evidence, restoration-oriented Mamba has been developed for image restoration and Mamba-based trackers have been explored for temporal context, memory, multimodal fusion, dynamic templates, motion prediction, efficient backbones, and low-light/adverse tracking. Degradation-invariant RGB template-search tracking is partially addressed by InvTrack, but restoration-guided state-space feature recovery from MambaIR/MambaIRv2 has not been systematically adapted to tracking-aware RGB template-search matching under generic image-quality degradation. TAR-MambaTrack studies this underexplored intersection by optimizing restoration-oriented Mamba features for localization, response reliability, and degraded template-search matching rather than full-image reconstruction.

## 28. Final contribution bullets

- We introduce TAR-MambaTrack, a restoration-guided Mamba tracking framework for RGB template-search tracking under generic image degradation, where restoration is formulated as target-discriminative feature recovery rather than pixel reconstruction.

- We design a Restoration-Guided State Space Block that adapts restoration-oriented Mamba components, including long-range state-space modeling, local enhancement, channel selection, and residual recovery, to tracking-supervised feature learning.

- We propose tracking-specific mechanisms for degraded matching, including optional degradation prompt learning, template-guided attentive scanning, restoration-guided response fusion, and optional degradation-aware memory update.

- We define an evaluation protocol for robust RGB tracking under degradation, including template/search asymmetry, mixed degradation, cross-degradation generalization, response-map analysis, restoration-preprocessing baselines, efficiency comparison, and direct novelty-threat comparisons.

## 29. Final checklist before implementation

- [ ] Base tracker chosen.
- [ ] Base tracker clean performance reproduced.
- [ ] Synthetic degradation protocol implemented.
- [ ] Clean/degraded template-search pairs generated.
- [ ] Baselines selected and code availability checked.
- [ ] InvTrack comparison path decided.
- [ ] MambaIR/MambaIRv2 preprocessing baseline path decided.
- [ ] RG-SSB implementation location chosen.
- [ ] Local enhancement branch implemented.
- [ ] Channel selection branch implemented.
- [ ] Feature consistency loss implemented.
- [ ] Response consistency loss implemented.
- [ ] Target-aware feature restoration loss planned.
- [ ] Degradation prompt marked optional for staged implementation.
- [ ] TG-AS marked optional for staged implementation.
- [ ] Memory update marked optional for staged implementation.
- [ ] First ablations planned.
- [ ] Evaluation scripts ready for AUC/precision/drop.
- [ ] Efficiency measurement script ready.
- [ ] Response-map visualization planned.
- [ ] Failure-case collection planned.

## 30. Verification

Files created or modified:

- `reports/09_complete_paper_plan.md`

How the output was verified:

- Used `reports/05b_final_recommendation.md` to identify the selected direction as TAR-MambaTrack and preserve the "proceed with caution" framing.
- Used `reports/04_novelty_danger_check.md` to keep the novelty narrow and explicitly defend against InvTrack, MambaIR, MambaIRv2, night UAV Mamba trackers, and temporal/context Mamba trackers.
- Used `reports/05_experiment_plan.md` for datasets, degradation protocols, baselines, metrics, and experiments.
- Used `reports/06_research_gap_paragraph.md` for the safe gap wording.
- Used `reports/07_related_work_draft.md` for the related-work structure.
- Used `reports/08_method_architecture.md` for the method modules, equations, minimal version, and full version.
- Kept optional modules marked optional and speculative components marked as staged extensions.
- Did not create implementation code, experimental results, manuscript files, or modify previous reports.

Uncertain fields:

- The final base tracker depends on code availability, compute, and reproducibility.
- Some Mamba tracker baselines may require reimplementation or may be unavailable.
- InvTrack and restoration-preprocessing comparisons depend on runnable code and compatible evaluation settings.
- TG-AS, degradation prompt, and memory update should remain optional until the RG-SSB proof of concept is validated.
- Real adverse-condition dataset availability and licenses should be checked before finalizing the experiment table.
- Vision-language-specific claims should remain limited to the reviewed evidence unless additional paper cards are added.

Whether the project is ready for final audit:

- Yes. The project is ready for a final audit of novelty wording, required baselines, and method scope before implementation starts.

Whether the project is ready for implementation planning:

- Yes. The plan is specific enough to start implementation planning with the minimal model: base tracker, synthetic degradation pipeline, RG-SSB, tracking loss, feature consistency, response consistency, and degraded-template/search evaluation.
