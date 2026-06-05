# Paper Card: 2025_ICASSP_MambaMOT

## Bibliographic information
- Title: MambaMOT: State-Space Model as Motion Predictor for Multi-Object Tracking
- Authors: Hsiang-Wei Huang, Cheng-Yen Yang, Wenhao Chai, Zhongyu Jiang, Jeng-Neng Hwang
- Year: 2025
- Venue: ICASSP 2025
- Task: Multi-object tracking (MOT), tracking-by-detection motion prediction
- Modality: RGB-video MOT through detector outputs and bounding-box tracklets; the Mamba model operates on trajectory boxes, not RGB template-search pairs

## Motivation
- Summary: The paper is motivated by replacing Kalman-filter motion prediction in MOT when nonlinear motion and occlusion make linear assumptions unreliable.
- Evidence: The abstract says traditional MOT often relies on Kalman filtering for linear motion but struggles with complex nonlinear motion and occlusions in sports and dance environments (p. 1). The related-work section says Kalman-filter assumptions fail on DanceTrack and SportsMOT, where objects have diverse and irregular motion (p. 2).

## Main problem addressed
- Summary: The paper addresses learning-based motion prediction for MOT and evaluates whether Mamba can replace Kalman filtering in tracking-by-detection pipelines.
- Evidence: The abstract says the paper explores replacing the Kalman filter with a learning-based motion model and proposes MambaMOT and MambaMOT+ (p. 1). The method defines the motion-model task as predicting a tracklet's next bounding box from its past n bounding boxes (p. 2).

## Main contributions
1. MambaMOT, a Mamba-based motion predictor for MOT that predicts the next location from historical tracklets.
2. MambaMOT+, which adds trajectory embeddings from the same Mamba model to merge tracklets.
3. Benchmark evaluation on challenging MOT datasets including DanceTrack and SportsMOT.
Evidence: The abstract states that MambaMOT and MambaMOT+ improve over Kalman-filter-based tracking on DanceTrack and SportsMOT (p. 1). The MambaMOT+ section says it extracts a trajectory motion pattern as a feature and connects similar tracklets (p. 3).

## Methodology
- Overall architecture: MambaMOT predicts a next-frame bounding box from a sequence of past bounding boxes, then uses BYTE/ByteTrack-style data association between predicted locations and detections; MambaMOT+ additionally outputs trajectory embeddings for tracklet merging (p. 2, p. 3).
- Main modules: Linear projection, Mamba blocks, hidden-state propagation, prediction head, optional embedding head, BYTE association, cosine-similarity/hierarchical clustering for MambaMOT+ tracklet merging (p. 2, p. 3, p. 4).
- Mamba usage: Mamba is used as a trajectory-sequence model. The paper describes hidden states ht updated over time, final outputs passed to the prediction head, and MambaMOT+ updating hidden state hT while generating predictions and embeddings (p. 2, p. 3).
- Loss functions: Bounding-box prediction uses GIoU loss and MSE loss; trajectory representation uses cosine embedding loss; MambaMOT+ jointly trains prediction and embedding heads (p. 2, p. 3).
- Training strategy: Training trajectories are collected from MOT17, DanceTrack, and SportsMOT; trajectories are randomly sampled with length between 2 and n and padded to n, with the next box as ground truth. Training uses Adam, learning rate 0.0001, 500 epochs, batch size 32, two Mamba blocks, hidden dimension 64, expansion factor 2, and an RTX 4080 GPU (p. 4).
- Evidence: The task definition and loss are described on p. 2. MambaMOT+ architecture and embedding loss are described on p. 3. Training configuration is described on p. 4.

## Degradation/restoration analysis
- Handles degradation? Not reported
- Degradation types: Not reported for image-quality degradation; occlusion and nonlinear motion are discussed as tracking/motion challenges.
- Restoration/enhancement? Not reported
- Image-level or feature-level? Not reported for restoration; motion is modeled at the bounding-box trajectory level.
- Evidence: The abstract and related work discuss complex nonlinear motion and occlusion (p. 1, p. 2). Searches of the extracted text found no discussion of degradation, restoration, enhancement, or motion-blur handling in the proposed method; the method operates on bounding-box sequences and trajectory embeddings (p. 2-p. 4).

## Tracking-specific analysis
- Template-search matching: Not reported; the method is MOT tracking-by-detection rather than single-object template-search tracking.
- Temporal memory: Yes; the Mamba recurrence propagates hidden states, and MambaMOT+ updates hidden state hT over tracklet sequences (p. 2, p. 3).
- Dynamic template update: Not reported.
- Response-map design: Not reported; association is between predicted boxes and detections, with optional trajectory-feature clustering (p. 2-p. 4).
- Evidence: The model computes hidden states ht and predicts Yt from the Mamba output (p. 2). MambaMOT+ updates hidden state hT and uses trajectory embeddings for detecting/matching tracks and merging tracklets (p. 3).

## Datasets and metrics
- Datasets: DanceTrack, SportsMOT, and MOT17 for trajectory training data; benchmark evaluation emphasizes DanceTrack and SportsMOT.
- Metrics: HOTA, IDF1, MOTA, AssA, DetA; the implementation section specifically names HOTA, IDF1, and MOTA as common tracking metrics.
- Evidence: The implementation section lists DanceTrack and SportsMOT experiments and training trajectories from MOT17, DanceTrack, and SportsMOT (p. 3, p. 4). The evaluation metrics section names HOTA, IDF1, and MOTA (p. 4), and benchmark tables include HOTA, DetA, AssA, IDF1, and MOTA (p. 4).

## Explicit limitations
- Limitations stated by authors: Not reported for the proposed method.
- Evidence: The conclusion states that MambaMOT addresses Kalman-filter limitations and achieves comparable performance on public benchmarks, but it does not state an explicit limitation or future-work item for MambaMOT (p. 4).

## Implicit limitations
- Limitation inferred from method/evaluation: The method is a trajectory-level MOT motion predictor and does not address RGB template-search feature degradation, restoration, or image enhancement.
- Why this is an inference, not an author claim: This follows from the task definition over past bounding boxes, the Mamba hidden-state motion model, and BYTE-style association (p. 2-p. 4); the authors do not describe this absence as a limitation.

## Relevance to our second paper
- How this paper supports our research gap: It supports the missing-intersection analysis by showing Mamba used as a learned replacement for Kalman-filter motion prediction in MOT, not as restoration-oriented Mamba for degraded RGB template-search tracking.
- How this paper threatens our novelty: It threatens broad "Mamba replaces Kalman in tracking" novelty claims because the paper explicitly explores replacing Kalman filtering with Mamba (p. 1, p. 2).
- What remains unsolved: Image-quality degradation, restoration/enhancement, and RGB SOT template-search robustness remain not reported; occlusion/nonlinear motion are addressed through trajectory modeling and association.
