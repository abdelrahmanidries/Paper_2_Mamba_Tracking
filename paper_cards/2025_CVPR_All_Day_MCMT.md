# Paper Card: 2025_CVPR_All_Day_MCMT

## Bibliographic information
- Title: All-Day Multi-Camera Multi-Target Tracking
- Authors: Huijie Fan, Yu Qiao, Yihao Zhen, Tinghui Zhao, Baojie Fan, Qiang Wang
- Year: 2025
- Venue: CVPR
- Task: Multi-camera multi-target tracking
- Modality: RGBT, using visible RGB and infrared/thermal video

## Motivation
- Summary: The paper targets MCMT tracking in low-light/nighttime conditions, where daytime-focused MCMT methods lack detailed visible appearance features.
- Evidence: Page 1 states that previous MCMT methods focus on daytime tracking and overlook low-light conditions, and says the main difficulty under low light is the lack of detailed visible appearance features.

## Main problem addressed
- Summary: The paper addresses all-day MCMT by building an RGBT MCMT dataset and using infrared information with Mamba-based adaptive modality fusion.
- Evidence: Page 1 says the method incorporates infrared into MCMT to provide more useful information and constructs M3Track, an RGBT multi-camera multi-target dataset with low-light sequences. Page 2 says RGB and infrared are used as complementary information for low-light tracking.

## Main contributions
1. It constructs M3Track, an RGBT multi-camera multi-target tracking dataset captured at different times of day.
2. It proposes ADMCMT, an all-day MCMT network for modality fusion, detection, and tracking.
3. It proposes All-Day Mamba Fusion (ADMF) with lighting guidance and Nearby Target Collection for tracking.
Evidence: Page 2 lists the contributions: M3Track, ADMCMT, ADMF using lighting-relevant information, and Nearby Target Collection.

## Methodology
- Overall architecture: ADMCMT fuses visible and infrared features, performs detection, builds Re-ID features using nearby target collection, and sends Re-ID features to a transformer-based tracking model.
- Main modules: All-Day Mamba Fusion, Lighting Guidance Model, visible and infrared fusion channels, CenterNet detector, Nearby Target Collection, transformer-based tracking model.
- Mamba usage: Mamba is used inside ADMF to guide visible/infrared feature fusion with lighting-relevant information.
- Loss functions: Lighting category cross-entropy loss, detection loss, association loss; the total tracking loss is a weighted sum of Llight, Ldet, and Lassi.
- Training strategy: ADMCMT is trained on M3Track with DLA-34 feature extraction, CenterNet detection, batch size 40, 20,000 iterations, Adam optimizer, and 4 RTX A6000 GPUs.
- Evidence: Page 4 gives the ADMCMT pipeline. Page 5 explains ADMF and LGM, including day/night lighting prediction and cross-entropy loss. Page 6 states the total loss and implementation details.

## Degradation/restoration analysis
- Handles degradation? Partial
- Degradation types: Low-light/nighttime illumination in all-day MCMT.
- Restoration/enhancement? No
- Image-level or feature-level? Feature-level multimodal fusion using RGB and infrared; no RGB image restoration module is reported.
- Evidence: Page 1 identifies low-light visible feature loss and says the method incorporates infrared. Page 3 discusses low-light enhancement as related work, but page 2 and page 5 describe the proposed solution as RGBT fusion with ADMF and LGM.

## Tracking-specific analysis
- Template-search matching: Not reported; this is MCMT detection/Re-ID/association, not RGB single-object template-search tracking.
- Temporal memory: Not reported
- Dynamic template update: Not reported
- Response-map design: Not reported as a template-search response map; detection and association are used instead.
- Evidence: Page 4 says fused features are used for target detection, Nearby Target Collection builds Re-ID features, and a transformer-based tracking model obtains the tracking result. Page 6 reports detection and association losses.

## Datasets and metrics
- Datasets: M3Track, an aligned RGB and infrared MCMT dataset collected at noon, afternoon, and night under diverse scenes and weather.
- Metrics: MOTA, HOTA, IDF1, DetA, MOTP, MDA, CVIDF1, CVMA.
- Evidence: Page 2 says M3Track contains aligned RGB and infrared sequences captured at different times of day and weather. Page 6 defines the evaluation metrics, and page 7 reports results for all and night scenes.

## Explicit limitations
- Limitations stated by authors: Not reported for the proposed method.
- Evidence: Pages 1, 2, and 4 state limitations of previous daytime MCMT datasets/methods, but the conclusion on page 8 does not state limitations of ADMCMT.

## Implicit limitations
- Limitation inferred from method/evaluation: Robustness comes from adding infrared/thermal sensing and RGBT fusion, so the paper does not solve RGB-only template-search degradation robustness.
- Why this is an inference, not an author claim: Pages 1-2 explicitly motivate infrared as complementary to RGB under low light, and page 4 describes an MCMT detection/Re-ID pipeline. The authors do not state this as a limitation.

## Relevance to our second paper
- How this paper supports our research gap: It shows a Mamba tracker/fusion system addressing low light through an extra sensor modality rather than RGB restoration.
- How this paper threatens our novelty: It limits any novelty claim around Mamba for low-light/all-day tracking, especially in multimodal MCMT.
- What remains unsolved: RGB-only template-search restoration under generic degradation remains outside the paper, because ADMCMT is RGBT, MCMT, and fusion-based.
