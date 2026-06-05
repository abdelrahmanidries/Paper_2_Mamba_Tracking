# Paper Card: 2025_CVPRW_SportMamba

## Bibliographic information
- Title: SportMamba: Adaptive Non-Linear Multi-Object Tracking with State Space Models for Team Sports
- Authors: Dheeraj Khanna, Jerrin Bright, Yuhao Chen, John S. Zelek
- Year: 2025
- Venue: CVPR Workshop 2025
- Task: Online multi-object tracking for team sports
- Modality: RGB sports video detections, player tracklets, ReID appearance features, and motion predictions; not RGB single-object template-search tracking

## Motivation
- Summary: The paper targets team-sports MOT, where fast motion, frequent occlusions, motion blur, ambiguous appearance, and nonlinear player trajectories make association difficult.
- Evidence: The abstract says team-sports MOT is challenging because fast-paced motion and frequent occlusions cause motion blur and identity switches, and player-position prediction is difficult due to highly nonlinear motion (p. 1). It also says current detection/appearance-based tracking struggles when appearance cues are ambiguous and motion is nonlinear (p. 1).

## Main problem addressed
- Summary: The paper addresses nonlinear motion prediction and robust detection-to-tracklet association in fast team-sports MOT.
- Evidence: The paper says conventional Kalman-filter methods struggle with arbitrary nonlinear motion, such as random ice-hockey skating, and transformer methods are computationally expensive for real-time sports tracking (p. 1). It defines SportMamba as a hybrid online tracking and association model for fast-moving team-sports objects (p. 2).

## Main contributions
1. SportMamba, a hybrid online MOT model for fast-paced nonlinear team-sports tracking.
2. A Mamba-attention motion predictor that combines Mamba state-space modeling with self-attention.
3. A height-adaptive IoU with extended buffers for spatial association, plus benchmark results on SportsMOT and zero-shot VIP-HTD.
Evidence: The contribution list states these items, including real-time inference near 30 FPS, Mamba/self-attention motion prediction, height-adaptive IoU with extended buffers, SportsMOT results, and VIP-HTD zero-shot generalization (p. 2).

## Methodology
- Overall architecture: SportMamba fine-tunes a detector, predicts future player positions from past tracklets using a Mamba-attention motion predictor, performs high-confidence association with appearance and height-adaptive spatial cost, performs low-confidence reassociation using relaxed spatial matching, then updates/creates/deletes tracklets and updates features with dynamic EMA (p. 2, p. 3, p. 5).
- Main modules: YOLOX detector, token embedding, Mamba-Attention Encoder, MHSA block, feed-forward network, prediction head, HCA/LCA association, HA-EIoU, ReID appearance features, tracklet memory, and dynamic EMA feature update (p. 3-p. 6).
- Mamba usage: Mamba is used for motion prediction from bounding-box tracklet sequences. The model encodes past object trajectories with token embedding, Mamba-Attention Encoder, MHSA refinement, FFN, stacked blocks, and an MLP prediction head for the next bounding box (p. 3, p. 4).
- Loss functions: The motion predictor uses Smooth L1 loss and Complete IoU loss, combined as a weighted objective with lambda values for L1 and CIoU (p. 6).
- Training strategy: SportMamba trains the motion predictor for 60 epochs with batch size 64, M=4 blocks, AdamW, learning rate 1e-4, weight decay 1e-3, YOLOX player detector training, temporal augmentation, spatial scaling/translation, and Gaussian-noise injection (p. 6).
- Evidence: The architecture is summarized on p. 2 and p. 3. The Mamba-attention model is described on p. 3-p. 4. Association and track management are described on p. 4-p. 5. Objective and training details are described on p. 6.

## Degradation/restoration analysis
- Handles degradation? Partial
- Degradation types: Motion blur, occlusion, missed detections, and weakened appearance cues in sports videos.
- Restoration/enhancement? Not reported
- Image-level or feature-level? Feature/association/motion-prediction level; no image restoration is reported.
- Evidence: The abstract links fast motion and occlusion to motion blur and identity switches (p. 1). The dynamic EMA section says occlusion and motion blur can make newly extracted features fail to reflect true appearance, so EMA is adjusted by detection confidence (p. 6). The conclusion explicitly states severe motion blur can still cause missed detections, weakened appearance cues, and broken tracklets (p. 8).

## Tracking-specific analysis
- Template-search matching: Not reported; SportMamba is MOT tracking-by-detection with detection-to-tracklet matching.
- Temporal memory: Yes; it uses past tracklets for motion prediction, hidden-state Mamba modeling, lost-tracklet memory, and dynamic tracklet feature updating (p. 3-p. 6).
- Dynamic template update: Not reported as template update; it does use dynamic EMA for tracklet appearance features (p. 6).
- Response-map design: Not reported; association uses cost matrices, HA-EIoU, ReID similarity, and linear assignment rather than template-search response maps (p. 4, p. 5).
- Evidence: SportMamba follows an online MOT tracking-by-detection formulation (p. 3). HCA/LCA establish correspondences between detections and Mamba-attention motion predictions (p. 4). Lost tracklets are stored in memory for re-identification, and feature updates use dynamic EMA (p. 5, p. 6).

## Datasets and metrics
- Datasets: SportsMOT and VIP-HTD.
- Metrics: HOTA, IDF1, AssA, DetA, and MOTA.
- Evidence: SportsMOT contains 240 sequences across basketball, soccer, and volleyball; VIP-HTD contains ice-hockey broadcast sequences and more motion blur due to faster pace (p. 6). The evaluation section names HOTA, IDF1, AssA, DetA, and MOTA (p. 6), and benchmark tables report these metrics (p. 7).

## Explicit limitations
- Limitations stated by authors: Severe motion blur can cause missed detections, weakened appearance cues, and broken tracklets.
- Evidence: The conclusion states that although SportMamba excels in motion prediction and data association, severe motion blur can lead to missed detections and weakened appearance cues, resulting in broken tracklets (p. 8).

## Implicit limitations
- Limitation inferred from method/evaluation: The paper does not solve restoration-oriented degradation robustness for RGB template-search tracking; its blur handling is through motion prediction, association, ReID/EMA updates, and detector confidence.
- Why this is an inference, not an author claim: This follows from the stated MOT pipeline, HA-EIoU/ReID association, dynamic EMA, and lack of image-restoration modules (p. 3-p. 6). The authors explicitly limit only severe motion blur causing broken tracklets (p. 8).

## Relevance to our second paper
- How this paper supports our research gap: It supports the missing-intersection analysis by showing Mamba used for nonlinear sports MOT motion prediction and association, while restoration-oriented Mamba for degraded RGB template-search features remains not reported.
- How this paper threatens our novelty: It threatens any broad claim that Mamba tracking papers ignore motion blur or occlusion, because SportMamba explicitly discusses both and includes dynamic EMA/association mechanisms (p. 1, p. 6, p. 8).
- What remains unsolved: Severe blur remains an explicit limitation, and restoration/enhancement for RGB template-search tracking is not reported.
