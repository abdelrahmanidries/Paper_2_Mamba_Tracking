# Paper Card: 2025_arXiv_HyMamba

## Bibliographic information
- Title: Hyperspectral Mamba for Hyperspectral Object Tracking
- Authors: Long Gao, Yunhe Zhang, Yan Jiang, Weiying Xie, Yunsong Li
- Year: 2025
- Venue: IEEE Transactions on Image Processing manuscript header; file labelled arXiv
- Task: Hyperspectral single-object tracking
- Modality: Hyperspectral video plus false-color hyperspectral images

## Motivation
- Summary: The paper argues that hyperspectral trackers lose spectral information when they convert data to false-color images or process frames independently, and that RGB trackers deteriorate under challenging conditions.
- Evidence: Page 1 says existing hyperspectral trackers often fail to capture intrinsic spectral information, temporal dependencies, and cross-depth interactions. Page 1 also states that RGB tracker performance deteriorates under adverse conditions such as background clutter, occlusion, and deformation.

## Main problem addressed
- Summary: The paper addresses hyperspectral object tracking by modeling spectral, cross-depth, and temporal information with Mamba-based state-space modules.
- Evidence: Page 1 introduces HyMamba as a hyperspectral tracking network equipped with Mamba that unifies spectral, cross-depth, and temporal modeling through SSMs. Page 2 says HyMamba encodes intra-frame cross-depth spectral information and inter-frame temporal spectral information.

## Main contributions
1. It proposes HyMamba, a hyperspectral tracking framework that models spectral, cross-depth, and temporal information.
2. It introduces Spectral State Integration (SSI) to learn semantic information directly from unconverted hyperspectral images and maintain spectral hidden states across depths and frames.
3. It proposes Hyperspectral Mamba (HSM), modifying Mamba with forward, backward, and spectral scanning for hyperspectral tracking.
Evidence: Page 2 lists these contributions explicitly, including SSI, HSM, and experiments on seven hyperspectral datasets.

## Methodology
- Overall architecture: HyMamba contains Adaptive Spectral Distillation, a feature extraction network with SSI transformer encoder layers, a tracking head, and a dynamic template update strategy.
- Main modules: ASD, dual-branch patch embedding, SSI, Mamba Module, Joint Augment, Spectral Augment, HSM, tracking head, dynamic template update.
- Mamba usage: Mamba is used for spectral hidden-state modeling in SSI and extended by HSM to scan forward, backward, and spectral directions.
- Loss functions: Weighted focal loss for classification, L1 loss and generalized IoU loss for bounding-box regression; total loss is Lc + 5L1 + 2Liou.
- Training strategy: Only the ASD module, SSI module, and hyperspectral-specific patch embeddings are optimized; the tracking head and HiViT-based backbone are frozen.
- Evidence: Page 3 describes ASD, search/static/dynamic template groups, and the tracking framework. Page 4 shows the overall architecture and tracking head. Pages 5-6 describe SSI/HSM and hidden-state updates. Pages 6-7 provide the loss and training setup.

## Degradation/restoration analysis
- Handles degradation? Partial
- Degradation types: Challenging tracking attributes include illumination variation, low resolution, and motion blur, but the method is not framed as general image degradation restoration.
- Restoration/enhancement? Partial
- Image-level or feature-level? Feature-level spectral/spatial/temporal enhancement; no image-level restoration or RGB enhancement is reported.
- Evidence: Page 7 lists HOTC2020 attributes including illumination variation, low resolution, and motion blur. Page 1 calls the index term "Feature Enhancement" and says HyMamba enhances joint features through interaction with raw hyperspectral features. Pages 5 and 10 describe feature enhancement inside SSI, not image restoration.

## Tracking-specific analysis
- Template-search matching: Yes; HyMamba uses search, static template, and dynamic template groups.
- Temporal memory: Yes; spectral hidden states are propagated across frames when the classification score exceeds a confidence threshold.
- Dynamic template update: Yes; the dynamic template is updated based on a fixed temporal interval and a confidence threshold.
- Response-map design: The tracking head uses a classification score map and regression branch; no response-map fusion module is reported.
- Evidence: Page 3 states that the framework takes search, static template, and dynamic template groups. Page 4 states the tracking head uses the search-region feature to compute a classification score map and regression output. Page 7 states the dynamic template and hidden-state update rules.

## Datasets and metrics
- Datasets: HOTC2020, VIS2023, NIR2023, RedNIR2023, VIS2024, NIR2024, and RedNIR2024.
- Metrics: AUC and DP@20; attribute-based HOTC2020 comparisons are also reported.
- Evidence: Page 2 lists seven hyperspectral tracking benchmarks. Page 7 gives HOTC dataset details and attributes. Pages 8-11 report AUC, DP@20, and attribute-based comparisons.

## Explicit limitations
- Limitations stated by authors: Not reported for HyMamba.
- Evidence: Pages 1-2 describe limitations of existing hyperspectral trackers, but the conclusion on page 11 summarizes HyMamba without stating a limitation section for the proposed method.

## Implicit limitations
- Limitation inferred from method/evaluation: HyMamba depends on hyperspectral data and addresses spectral modeling, so it does not solve RGB-only degradation-robust template-search tracking or restoration-oriented RGB recovery.
- Why this is an inference, not an author claim: Page 3 states that each search/template group contains a hyperspectral image and corresponding false-color image, and page 7 evaluates hyperspectral datasets. The authors do not present this as a limitation.

## Relevance to our second paper
- How this paper supports our research gap: It shows Mamba used for temporal hidden states, dynamic templates, and non-RGB spectral feature enhancement, which helps separate sensor-rich robustness from RGB restoration.
- How this paper threatens our novelty: It weakens any novelty claim around Mamba-based dynamic templates or temporal hidden-state tracking, especially outside RGB.
- What remains unsolved: Restoration-oriented Mamba for RGB template-search tracking under generic image-quality degradation remains outside scope because HyMamba is hyperspectral and feature-level.
