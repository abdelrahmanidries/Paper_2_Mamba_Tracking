# Paper Card: 2025_AAAI_MM_Tracker

## Bibliographic information
- Title: MM-Tracker: Motion Mamba for UAV-platform Multiple Object Tracking
- Authors: Mufeng Yao, Jinlong Peng, Qingdong He, Bo Peng, Hao Chen, Mingmin Chi, Chao Liu, Jon Atli Benediktsson
- Year: 2025
- Venue: AAAI 2025
- Task: UAV-platform multi-object tracking (MOT)
- Modality: RGB UAV video with detector features, motion maps, and MOT association; not RGB single-object template-search tracking

## Motivation
- Summary: The paper targets UAV-MOT, where local object motion and global camera motion make motion modeling difficult, and motion blur makes large moving objects harder to detect.
- Evidence: The abstract states that UAV-MOT faces both local object motion and global camera motion, and that motion blur increases the difficulty of detecting large moving objects (p. 1). The introduction says severe motion blur from camera motion increases object-detection difficulty (p. 1).

## Main problem addressed
- Summary: The paper addresses fast global motion modeling and motion-blur-focused detector training for UAV-MOT.
- Evidence: The paper says prior UAV motion-modeling approaches either focus only on local motion or ignore motion blurring effects (p. 1). It also says previous studies ignore motion long-tailed distributions, so large-motion objects get less training than easy small-motion samples (p. 2).

## Main contributions
1. A Motion Mamba module that combines local correlation and global bi-directional Mamba scanning for motion modeling.
2. Motion Margin Loss (MMLoss) to improve detection of motion-blurred, large-motion objects.
3. A UAV-MOT tracker that reports state-of-the-art results on VisDrone and UAVDT.
Evidence: The contribution list states that Motion Mamba uses local correlation and bi-directional Mamba global scan, MMLoss imposes larger decision boundaries for large-motion objects, and MM-Tracker reaches state-of-the-art results on two public UAV-MOT datasets (p. 2).

## Methodology
- Overall architecture: MM-Tracker uses a YOLOX-style detector backbone and head, reuses bi-temporal detection features for Motion Mamba, generates multi-scale motion features and a motion map, and performs motion estimation plus spatial matching for tracking (p. 3, p. 4).
- Main modules: Detector backbone, detector head, Motion Mamba Module, local correlation, vertical and horizontal SSM scans, motion-map fusion, Motion Margin Loss, motion estimation, and spatial matching (p. 3, p. 4).
- Mamba usage: Mamba is used for feature-level motion modeling, not restoration. The Motion Mamba block uses SSM hidden states over scanned features and combines vertical and horizontal scanned feature maps for global interaction (p. 4).
- Loss functions: Detector classification is supervised by MMLoss, detector regression by IoU loss and L1 loss, and the motion feature map by L1 loss against a ground-truth motion map (p. 3, p. 5).
- Training strategy: The paper uses official VisDrone and UAVDT splits, YOLOX-S as detector, input size 1088 x 608, SGD with learning rate 0.0001, batch size 8, 10 epochs per dataset, a single 2080Ti GPU, L1 for Motion Mamba and regression, and MMLoss for classification (p. 5).
- Evidence: The architecture overview and losses are described on p. 3. The SSM/Motion Mamba block and motion-blur loss motivation are described on p. 4. Implementation details are provided on p. 5.

## Degradation/restoration analysis
- Handles degradation? Partial
- Degradation types: Motion blur due to camera/object motion; occlusion appears in qualitative comparison but is not the central degradation mechanism.
- Restoration/enhancement? Not reported
- Image-level or feature-level? Feature/detection-loss level; the method improves detector supervision and motion-map estimation rather than restoring degraded images.
- Evidence: The abstract explicitly says MMLoss addresses detection difficulties caused by motion blur (p. 1). The Motion Margin Loss section says camera-view rotation can cause severe motion blur, increasing detection difficulty, and a few missed frames can interrupt tracking (p. 4). The ablation shows MMLoss tracking a blurred moving bike missed without MMLoss (p. 6). No image restoration or enhancement module is described in the method (p. 3-p. 5).

## Tracking-specific analysis
- Template-search matching: Not reported; the method uses UAV MOT detection and association, not template-search matching.
- Temporal memory: Partial; SSM hidden states appear inside the Motion Mamba feature scan, but the paper's core motion input is bi-temporal detector features rather than long-term template-search memory (p. 3, p. 4).
- Dynamic template update: Not reported.
- Response-map design: Not reported for template-search response maps; the method predicts motion maps and uses spatial matching (p. 3, p. 4).
- Evidence: The architecture shows DetBackbone, DetHead, Motion Mamba Module, Motion Estimation, and Spatial Matching (p. 3). The Motion Mamba block outputs a motion map with horizontal and vertical motion channels (p. 4).

## Datasets and metrics
- Datasets: VisDrone and UAVDT.
- Metrics: MOTA and IDF1 are the main metrics; FPS/time is also reported in comparisons and ablations.
- Evidence: The datasets section says experiments use VisDrone and UAVDT, both open-source multi-class UAV MOT datasets suitable for global motion and motion-blur problems (p. 5). The metrics section selects MOTA and IDF1 (p. 5). Tables report MOTA, IDF1, time, and FPS (p. 5-p. 7).

## Explicit limitations
- Limitations stated by authors: Not reported.
- Evidence: The conclusion states that Motion Mamba reduces motion-modeling cost, bi-directional selective scan extracts global motion features, MMLoss improves fast-object detection, and MM-Tracker achieves best results on two UAV-MOT datasets, but it does not state an explicit limitation or future-work item (p. 7).

## Implicit limitations
- Limitation inferred from method/evaluation: The paper handles motion blur through detector loss and motion modeling, not through restoration-oriented Mamba blocks; it is also UAV MOT rather than RGB SOT template-search tracking.
- Why this is an inference, not an author claim: The inference comes from the documented use of MMLoss, motion maps, detector features, and spatial matching (p. 3-p. 6). The authors do not explicitly position the method against restoration-guided template-search tracking.

## Relevance to our second paper
- How this paper supports our research gap: It is important evidence because it shows an explicit Mamba-tracking paper that discusses motion blur, but its solution is motion modeling plus detection-loss reweighting, not restoration-oriented Mamba for RGB template-search features.
- How this paper threatens our novelty: It threatens any broad claim that Mamba trackers ignore blur, because MM-Tracker explicitly targets motion blur and improves blurred-object detection (p. 1, p. 4, p. 6).
- What remains unsolved: Generic degradation robustness, restoration/enhancement, and template-search target feature recovery remain not reported; blur handling is detector/motion-level rather than restoration-level.
