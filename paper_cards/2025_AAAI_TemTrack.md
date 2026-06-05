# Paper Card: 2025_AAAI_TemTrack

## Bibliographic information
- Title: Robust Tracking via Mamba-based Context-aware Token Learning
- Authors: Jinxia Xie, Bineng Zhong, Qihua Liang, Ning Li, Zhiyi Mo, Shuxiang Song
- Year: 2025
- Venue: AAAI, from PDF filename `2025_AAAI_TemTrack.pdf`
- Task: Visual object tracking with temporal context learned from track tokens.
- Modality: RGB-style visual template-search tracking from image pairs/video frames. Use of thermal, event, language, or restoration modalities is not reported.

## Motivation
- Summary: TemTrack is motivated by the cost of trackers that combine temporal and appearance information by inputting more images or features. It proposes learning temporal relations from compact track tokens instead of additional images to reduce computational and learning burden.
- Evidence:
  - p.1: The abstract says current methods combine temporal and appearance information by inputting more images/features, increasing computational resources and learning burden.
  - p.2: The introduction says extra templates/search images require selection strategies and can introduce useless or interfering information.
  - p.2: The authors propose TemTrack to separate temporal-information learning from appearance modeling and learn context from track tokens instead of images.

## Main problem addressed
- Summary: TemTrack addresses how to integrate temporal information efficiently without feeding multiple large image templates/features into the tracker.
- Evidence:
  - p.1: The abstract introduces track tokens for each frame to collect target appearance and a Mamba-based Temporal Module for token-level context.
  - p.2: The method is designed to reduce the computational source and learning burden caused by inputting too many images.
  - p.3: The overview says the track token gathers appearance in the backbone and learns temporal context in the Temporal Module.

## Main contributions
1. Proposes a simple context-aware tracker that separates temporal information learning from appearance modeling.
2. Develops a Mamba-based Temporal Module that combines Mamba sequence modeling and attention-based global perception.
3. Reports detailed experiments showing effectiveness on multiple tracking benchmarks.
Evidence:
- p.2: The contribution list states these three contributions directly.
- p.4: The Temporal Module's Mamba Cross uses Mamba followed by cross-attention.
- p.6-p.7: Experiments and ablations report performance and component effects on six benchmarks.

## Methodology
- Overall architecture: TemTrack has a backbone for feature extraction/relation modeling, a Mamba-based Temporal Module for track-token context, and a center-based head for prediction.
- Main modules: Fast-iTPN backbone, per-frame track token, Mamba Cross Temporal Module, cross-attention layer, guidance mechanism from track token to search features, center-based classification/regression head.
- Mamba usage: Mamba is used in the Temporal Module to model historical track-token sequences within a sliding window. The track token prediction depends on previous hidden state space and the current track token; after Mamba and cross-attention, the track token gathers historical appearance changes and motion trends.
- Loss functions: Focal loss for classification, GIoU loss and L1 loss for regression, with weights `giou = 2` and `L1 = 5`.
- Training strategy: Uses COCO, LaSOT, TrackingNet, and GOT-10k; uses brightness jittering and horizontal flip; trains with AdamW; backbone learning rate 4e-5 and other parameters 4e-4; weight decay 1e-4; total batch size 128; 150 epochs and 60k image pairs per epoch, with GOT-10k trained for 40 epochs.
- Evidence:
  - p.3: Figure 2 and the overview describe template/search images concatenated with track token and processed by backbone, Temporal Module, and head.
  - p.3: The Temporal Module input is historical track tokens containing target appearance at different times.
  - p.4: Mamba Cross is described as combining Mamba with long-sequence/autoregressive properties, followed by cross-attention.
  - p.4: Guidance, head, and loss text defines search-feature adjustment, center-based head, focal loss, GIoU, and L1.
  - p.4-p.5: Implementation details report resolutions, Fast-iTPN initialization, training datasets, augmentations, optimizer, learning rates, batch size, epochs, and inference behavior.

## Degradation/restoration analysis
- Handles degradation? Not reported.
- Degradation types: Not reported as explicit degradation handling. Motion blur and low resolution appear as LaSOT/TrackingNet challenge attributes, not as degradation-specific training or method design.
- Restoration/enhancement? Not reported.
- Image-level or feature-level? Not reported for degradation/restoration. Search-feature adjustment is guided by temporal tokens, not restoration.
- Evidence:
  - p.5: Attribute plots include motion blur and low resolution, and the TrackingNet description mentions background clutter, full occlusion, and low resolution.
  - p.4-p.5: Training details report standard augmentations such as brightness jittering and horizontal flip, but no synthetic degradation, restoration target, or enhancement branch.

## Tracking-specific analysis
- Template-search matching: Yes. The input is one template image and one search image, embedded with a track token; the backbone models target appearance and template-search relationships.
- Temporal memory: Yes. Temporal context is represented by historical track tokens in a sliding window, and Mamba uses hidden-state/autoregressive sequence modeling over those tokens.
- Dynamic template update: Not reported. The paper explicitly positions TemTrack as avoiding image-selection/update strategies and learning temporal context from tokens.
- Response-map design: Not reported. The method reports a center-based head with classification and regression branches, not response-map fusion.
- Evidence:
  - p.3: The overview states the input is a template image and search image, plus a track token.
  - p.3: The track token gathers target appearance and learns temporal context in the Temporal Module.
  - p.4: Mamba Cross uses Mamba over historical track tokens, then cross-attention, so the current token gathers historical appearance changes and motion trend.
  - p.4: The head uses classification and regression branches to predict position and scale.
  - p.2: The related-work section says the method avoids updating strategies or inputting more images.

## Datasets and metrics
- Datasets: Training uses COCO, LaSOT, TrackingNet, and GOT-10k. Evaluation reports LaSOT, LaSOText, GOT-10k, TrackingNet, UAV123, and TNL2K.
- Metrics: AUC, normalized precision (PNorm), precision (P), average overlap (AO), success rate SR0.5/SR0.75, parameters, FLOPs, FPS, and success plots for challenge attributes.
- Evidence:
  - p.4: Training details list COCO, LaSOT, TrackingNet, and GOT-10k.
  - p.6: Table 2 reports LaSOT, LaSOText, GOT-10k, and TrackingNet with AUC/PNorm/P or AO/SR metrics.
  - p.6: Table 3 reports UAV123 and TNL2K AUC.
  - p.5: Table 1 reports parameters, FLOPs, and speed.

## Explicit limitations
- Limitations stated by authors: Not reported in the extracted text.
- Evidence:
  - p.7: The conclusion summarizes the method and experiments but does not state a limitation or future-work section.
  - p.1-p.7: The extracted main text discusses limitations of prior methods but does not explicitly state limitations of TemTrack.

## Implicit limitations
- Limitation inferred from method/evaluation: TemTrack uses Mamba for temporal token/context modeling, not for restoration-oriented recovery or degradation-robust feature reconstruction; memory/update is not degradation-aware.
- Why this is an inference, not an author claim: The paper reports track-token temporal modeling, standard tracking losses, and benchmark/attribute evaluation; it does not report degradation generation, restoration/enhancement objectives, or degradation-conditioned template/token updates.

## Relevance to our second paper
- How this paper supports our research gap: It shows Mamba is already used in tracking for temporal context through compact track tokens and sliding-window token interaction.
- How this paper threatens our novelty: It makes "Mamba for temporal information/track-token context in tracking" non-novel by itself.
- What remains unsolved: It does not report restoration-oriented Mamba blocks, explicit image-degradation handling, restoration/enhancement, or degradation-aware RGB template-search matching.
