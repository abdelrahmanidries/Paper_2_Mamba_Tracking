# Paper Card: 2025_ACM_MultiStateTracker

## Bibliographic information
- Title: Multi-State Tracker: Enhancing Efficient Object Tracking via Multi-State Specialization and Interaction
- Authors: Shilei Wang, Gong Cheng, Pujian Lai, Dong Gao, Junwei Han
- Year: 2025
- Venue: ACM MM
- Task: Efficient single-object visual tracking
- Modality: RGB visual tracking

## Motivation
- Summary: The paper targets the reduced feature-representation capacity of efficient trackers, which can limit their ability to capture target states in complex scenarios.
- Evidence: Page 1 says efficient trackers reduce computational complexity and parameters but weaken feature representation capacity, limiting their ability to capture target states using single-layer features.

## Main problem addressed
- Summary: The paper addresses efficient tracking robustness by generating multiple target feature states, enhancing each state, and aggregating them interactively.
- Evidence: Page 1 states that MST uses state-specific enhancement on multi-state features from MSG and aggregates them through CSI. Page 2 says MSG, SSE, and CSI generate diverse state representations, refine target-specific characteristics, and integrate complementary features.

## Main contributions
1. It introduces a Multi-State Tracker that uses multiple state representations for efficient tracking.
2. It proposes MSG, SSE, and CSI, with SSE and CSI built on HSA-SSD for lightweight state-space modeling.
3. It reports state-of-the-art performance among efficient trackers on multiple benchmarks while maintaining high speed.
Evidence: Page 2 lists these contributions, including the multi-state architecture, MSG/SSE/CSI with HSA-SSD, and performance across benchmark datasets. Page 6 reports GOT-10k, TrackingNet, LaSOT, GPU FPS, and CPU FPS comparisons.

## Methodology
- Overall architecture: MST uses a lightweight backbone, Multi-State Generation, State-Specific Enhancement, Cross-State Interaction, and a tracking head.
- Main modules: MSG, SSE, CSI, HSA-SSD, center-style tracking head.
- Mamba usage: HSA-SSD is described as enhancing Mamba's selective state-space model for efficient long-sequence modeling inside SSE and CSI.
- Loss functions: Weighted focal loss for classification, L1 loss and generalized IoU loss for regression; total loss is Lcls + lambda_iou Liou + lambda_1 L1 with lambda_iou = 2 and lambda_1 = 5.
- Training strategy: Built on a ViT-Tiny backbone with distilled MAE pretrained weights; trained on LaSOT, TrackingNet, GOT-10K, and COCO2017 using AdamW over 300 epochs, with GOT-10K training limited to 100 epochs.
- Evidence: Page 3 shows the MST architecture and HSA-SSD. Page 5 describes the tracking loss, implementation details, template/search sizes, training datasets, optimizer, epochs, and inference with a Hanning-windowed classification response map.

## Degradation/restoration analysis
- Handles degradation? Partial
- Degradation types: Motion blur and challenging attributes such as low resolution and illumination variation are evaluated; states are not degradation states.
- Restoration/enhancement? Partial
- Image-level or feature-level? Feature-level state-specific enhancement; no image-level restoration or enhancement is reported.
- Evidence: Page 2 says multi-state representations help handle appearance variations, occlusions, and motion blur. Page 7 includes LaSOT attributes such as low resolution, motion blur, and illumination variation. Pages 1-2 and 4 define the states as target feature representations produced by MSG and refined by SSE, not degradation states.

## Tracking-specific analysis
- Template-search matching: Yes; MSG processes template and search patches in a unified manner.
- Temporal memory: Not reported
- Dynamic template update: Not reported
- Response-map design: Classification response map is multiplied by a Hanning window during inference; the highest candidate region is used for tracking.
- Evidence: Page 4 states that MSG processes both template and search regions. Page 5 states template size 128 x 128 and search region size 256 x 256, and says inference multiplies the classification response map by a Hanning window.

## Datasets and metrics
- Datasets: LaSOT, TrackingNet, GOT-10K, COCO2017 for training; GOT-10k, TrackingNet, LaSOT, TNL2K, UAV123, NFS, and LaSOText for evaluation.
- Metrics: AO, SR0.5, SR0.75, AUC, PNorm, precision, FPS.
- Evidence: Page 5 lists the training datasets. Page 6 reports GOT-10k, TrackingNet, and LaSOT metrics with FPS. Page 7 reports TNL2K, UAV123, NFS, LaSOText, and attribute comparisons.

## Explicit limitations
- Limitations stated by authors: Using too many feature layers can introduce confusion/noise and plateau performance.
- Evidence: Page 8 states that when four or five layers are used, performance improvement plateaus, and that shallow features may introduce noise that interferes with final feature representation.

## Implicit limitations
- Limitation inferred from method/evaluation: Multi-state modeling is general target feature-state modeling, not degradation-state modeling; the paper does not include RGB image restoration or degradation-aware template update.
- Why this is an inference, not an author claim: Pages 1-4 describe MSG/SSE/CSI as generating and refining target feature representations from template/search patches, while the degradation-like evidence is attribute evaluation on page 7. The authors do not claim a degradation-state model or restoration module.

## Relevance to our second paper
- How this paper supports our research gap: It shows Mamba/SSM-style modules used for efficient feature-state specialization and interaction, not restoration-oriented degradation recovery.
- How this paper threatens our novelty: It weakens novelty claims around Mamba for efficient RGB tracking, response maps, motion blur robustness, or multi-state feature modeling.
- What remains unsolved: Generic degradation-robust RGB template-search tracking with restoration-oriented Mamba blocks and degradation-aware template/search recovery is not addressed.
