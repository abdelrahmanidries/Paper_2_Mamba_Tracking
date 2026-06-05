# Paper Card: 2024_arXiv_Mamba_FETrack

## Bibliographic information
- Title: Mamba-FETrack: Frame-Event Tracking via State Space Model
- Authors: Ju Huang, Shiao Wang, Shuai Wang, Zhe Wu, Xiao Wang, Bo Jiang
- Year: 2024
- Venue: arXiv 2024
- Task: RGB-Event single-object visual tracking
- Modality: RGB frames plus event stream converted into event images

## Motivation
- Summary: The paper is motivated by RGB-Event tracking under challenging scenarios and by reducing the high computation and memory cost of Transformer-based RGB-Event trackers.
- Evidence: The abstract defines RGB-Event tracking as integrating synchronized exposure video frames and asynchronous event streams, while noting that Transformer-based trackers require significant memory and computation due to self-attention (p. 1). The introduction says tracking under fast motion and low illumination is still unsatisfactory for RGB-only trackers, so the paper uses event cameras as external cues (p. 2). The paper also states that existing Transformer RGB-Event trackers have O(N^2) attention complexity and high GPU memory requirements (p. 3).

## Main problem addressed
- Summary: The paper addresses efficient RGB-Event template-search tracking by replacing a heavy Transformer backbone with Mamba-based feature extraction and cross-modal fusion.
- Evidence: The paper asks how to design an RGB-Event framework with a good balance between high performance and low model complexity, then motivates SSM/Mamba because of linear complexity (p. 3). The approach uses RGB and Event Mamba blocks, a FusionMamba block, and a tracking head to predict target location (p. 6).

## Main contributions
1. A state-space-model-based RGB-Event tracking framework, Mamba-FETrack, targeting high performance with lower complexity.
2. A FusionMamba block for interactive feature learning between RGB and event modalities.
3. Experiments on FE108 and FELT validating effectiveness and efficiency.
Evidence: The contribution list states these three contributions, including lower GPU memory, FLOPs, and parameters than a ViT-S OSTrack RGB-Event version (p. 3). The abstract reports Mamba-FETrack results of 43.5/55.6 SR/PR and reduced memory, FLOPs, and parameters versus ViT-S OSTrack (p. 1).

## Methodology
- Overall architecture: The framework takes RGB and event template/search patches, projects them into tokens, uses modality-specific RGB and Event Mamba blocks, applies FusionMamba for RGB-event interaction, and sends fused search features to an OSTrack-style tracking head (p. 6, p. 8).
- Main modules: RGB Mamba backbone, Event Mamba backbone, FusionMamba, an additional Transformer block after modal interaction, and OSTrack-style tracking head (p. 6, p. 8, p. 12).
- Mamba usage: Mamba is used as a lightweight feature backbone for each modality and as a fusion mechanism for RGB-event interactive learning (p. 3, p. 6, p. 8).
- Loss functions: The tracking head uses focal loss, L1 loss, and GIoU loss, with weights lambda1=1, lambda2=14, and lambda3=1 (p. 8).
- Training strategy: The tracker is extended from OSTrack but replaces the ViT backbone with lightweight Vision Mamba; it uses learning rate 0.0004, weight decay 0.0001, batch size 32, AdamW, PyTorch, and an RTX 3090 GPU. The number of epochs is not reported in the extracted text (p. 9).
- Evidence: The method overview and RGB/event token processing are described on p. 6-p. 8. Loss and training settings are described on p. 8-p. 9.

## Degradation/restoration analysis
- Handles degradation? Partial
- Degradation types: Fast motion, low illumination, motion blur, and high dynamic range are discussed through the use of event-camera cues and benchmark attributes.
- Restoration/enhancement? Not reported
- Image-level or feature-level? Feature-level multimodal fusion; no image restoration or enhancement module is reported.
- Evidence: The paper says event cameras provide external cues for challenging scenarios including fast motion and low illumination (p. 2). It states that the FE108 dataset includes degraded tracking conditions such as motion blur and high dynamic range (p. 9). No restoration or enhancement component is described in the architecture or loss sections (p. 6-p. 9).

## Tracking-specific analysis
- Template-search matching: Yes; RGB and event template/search patches are used, and search features are sent to the tracking head (p. 6, p. 8).
- Temporal memory: Partial; Mamba provides sequence modeling, but the paper does not report a dedicated temporal memory module for online tracking.
- Dynamic template update: Not reported.
- Response-map design: The tracking head outputs a target classification score map, local offset, and normalized bounding-box size (p. 8).
- Evidence: The method explicitly uses template and search patches for RGB and event images (p. 6-p. 7). The tracking head design is described on p. 8.

## Datasets and metrics
- Datasets: FE108 and FELT.
- Metrics: SR, PR, NPR, and AUC/PR are reported across experiments and tables.
- Evidence: The experiment section validates the tracker on FE108 and FELT (p. 9). FE108 and FELT results use SR/PR and ablations report SR, PR, and NPR (p. 10-p. 11).

## Explicit limitations
- Limitations stated by authors: The authors state that they simply transform event streams into event images, which may fail to capture event-point dynamics well; they also state that effective event-data modeling with Mamba remains an ongoing challenge.
- Evidence: The limitation analysis lists these two improvement points explicitly (p. 13). The conclusion says future work will explore diverse event representations such as event points and event voxels (p. 15).

## Implicit limitations
- Limitation inferred from method/evaluation: The robustness comes from extra event-sensor cues and multimodal feature fusion, not from RGB-only degradation robustness or restoration-oriented Mamba.
- Why this is an inference, not an author claim: This follows from the RGB-event inputs, event-image conversion, RGB/Event Mamba backbones, and FusionMamba design (p. 6-p. 8); the authors do not present it as an RGB-only degradation method.

## Relevance to our second paper
- How this paper supports our research gap: It supports the missing-intersection analysis because it uses Mamba for efficient RGB-event feature extraction and fusion, not restoration-oriented RGB template-search recovery.
- How this paper threatens our novelty: It threatens broad claims that Mamba has not been used in template-search tracking or multimodal tracking, because it is explicitly an RGB-Event Mamba tracker with template/search inputs (p. 6).
- What remains unsolved: RGB-only degraded template-search tracking with restoration-oriented Mamba blocks remains not reported; degradation robustness is tied to event-camera sensing and fusion.
