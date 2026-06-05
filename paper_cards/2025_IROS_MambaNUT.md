# Paper Card: 2025_IROS_MambaNUT

## Bibliographic information
- Title: MambaNUT: Nighttime UAV Tracking via Mamba-based Adaptive Curriculum Learning
- Authors: You Wu, Xiangyang Yang, Xucheng Wang, Hengzhou Ye, Dan Zeng, Shuiwang Li
- Year: 2025
- Venue: IROS
- Task: Nighttime UAV single-object tracking
- Modality: RGB video

## Motivation
- Summary: The paper targets nighttime UAV tracking under low illumination, where standard UAV trackers trained mostly on daytime data degrade and nighttime data are scarce.
- Evidence: Page 1 states that images captured by UAVs under nighttime conditions have lower contrast, brightness, and signal-to-noise ratio, causing severe degradation in tracking performance. Page 2 describes sharp imbalance between daytime and nighttime datasets.

## Main problem addressed
- Summary: The paper addresses nighttime UAV tracking with an end-to-end Mamba tracker and adaptive curriculum learning, rather than using a separate low-light enhancer or domain-adaptation pipeline.
- Evidence: Page 1 says prior low-light enhancement and domain adaptation approaches suffer from over-reliance on image enhancement, limited high-quality nighttime data, and poor integration between daytime and nighttime trackers. Page 2 says MambaNUT uses a compact Mamba-based framework and ACL for imbalanced day/night data.

## Main contributions
1. It proposes a pure Mamba-based nighttime UAV tracker with a one-stream Vision Mamba backbone and tracking head.
2. It introduces adaptive curriculum learning with a sampling scheduler and an adaptive data weighted loss scheduler for day/night imbalance.
3. It reports state-of-the-art nighttime UAV tracking results with low computational cost.
Evidence: Page 2 lists the proposed Mamba-based tracking framework, ACL with dynamic sampling and Adaptive Data Weighted loss, and strong benchmark performance. Page 6 reports results on NAT2024-1, NAT2021, and UAVDark135 with FPS, FLOPs, and parameter counts.

## Methodology
- Overall architecture: One-stream template-search tracker with a Vision Mamba backbone and a center-based tracking head.
- Main modules: Patch embedding, stacked bidirectional Vision Mamba encoders, adaptive curriculum learning, sampling scheduler, Adaptive Data Weighted loss scheduler, center-based tracking head.
- Mamba usage: Vision Mamba is the backbone; template and search patches are tokenized together and processed through bidirectional Vision Mamba encoders.
- Loss functions: Weighted focal classification loss, L1 loss, GIoU loss, and Adaptive Data Weighted loss.
- Training strategy: Trains with four daytime datasets and three nighttime datasets; the sampling scheduler gradually increases nighttime samples from easier daytime to harder nighttime data, and the loss scheduler weights samples by dataset size and IoU.
- Evidence: Page 3 describes the one-stream framework with template image and search image inputs. Page 4 explains the sampling scheduler and loss scheduler. Page 5 describes bidirectional Vision Mamba, the center-based head, the total loss, and training datasets including GOT-10k, LaSOT, COCO, TrackingNet, BDD100K-Night, SHIFT-Night, and ExDark.

## Degradation/restoration analysis
- Handles degradation? Partial
- Degradation types: Nighttime/low-light conditions; not general degradation.
- Restoration/enhancement? No
- Image-level or feature-level? Feature-level robustness through Mamba representation learning and curriculum learning; no image restoration or low-light enhancement module in the proposed method.
- Evidence: Page 1 frames the degradation as nighttime low contrast, low brightness, and low signal-to-noise ratio. Page 2 discusses low-light enhancement as prior work and criticizes plug-and-play enhancer use. Pages 3-5 describe the proposed modules as Vision Mamba backbone, ACL, and loss scheduling, not image restoration.

## Tracking-specific analysis
- Template-search matching: Yes; the framework takes template image Z and search image X, embeds them into tokens, and integrates feature learning with template-search coupling.
- Temporal memory: Not reported
- Dynamic template update: Not reported
- Response-map design: Center-based tracking head outputs offsets, box sizes, and an object classification score map; the highest classification score selects the target location.
- Evidence: Page 1 says the architecture integrates feature learning and template-search coupling within Vision Mamba. Page 5 states template and search images are embedded into tokens, processed by Vision Mamba, and the head outputs offsets, normalized box sizes, and a classification score map.

## Datasets and metrics
- Datasets: Training uses GOT-10k, LaSOT, COCO, TrackingNet, BDD100K-Night, SHIFT-Night, and ExDark; evaluation uses NAT2024-1, NAT2021, and UAVDark135.
- Metrics: Precision, normalized precision, success rate, FPS, FLOPs, parameters.
- Evidence: Page 5 lists training datasets and evaluation benchmarks. Page 6 provides the main comparison table with precision, normalized precision, success, average FPS, FLOPs, and parameters.

## Explicit limitations
- Limitations stated by authors: Not reported.
- Evidence: The searched abstract, method, experiment, and conclusion pages do not state explicit limitations; page 7 concludes by summarizing MambaNUT and ACL without a limitation section.

## Implicit limitations
- Limitation inferred from method/evaluation: The curriculum learning is designed for nighttime/low-light tracking and day/night data imbalance, not for generic image degradation such as blur, compression, noise, or low resolution as a restoration target.
- Why this is an inference, not an author claim: Pages 1-5 repeatedly define the problem as nighttime UAV tracking and day/night imbalance, and the method lacks a restoration/enhancement module. The authors do not explicitly claim generic degradation robustness as a limitation.

## Relevance to our second paper
- How this paper supports our research gap: It supports the evidence that Mamba trackers can target low-light tracking without restoration, using Mamba mainly for efficient template-search feature modeling and curriculum learning.
- How this paper threatens our novelty: It narrows novelty for any claim that no Mamba tracker addresses nighttime UAV tracking or low-light robustness.
- What remains unsolved: Restoration-oriented Mamba blocks for generic RGB template-search degradation are not studied; the method is nighttime-only and curriculum-based rather than restoration-guided.
