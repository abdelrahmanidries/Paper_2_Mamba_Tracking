# Paper Card: 2025_AAAI_MCITrack

## Bibliographic information
- Title: Exploring Enhanced Contextual Information for Video-Level Object Tracking
- Authors: Ben Kang, Xin Chen, Simiao Lai, Yang Liu, Yi Liu, Dong Wang
- Year: 2025
- Venue: AAAI, from PDF filename `2025_AAAI_MCITrack.pdf`
- Task: Video-level visual object tracking with contextual-information transmission.
- Modality: Visual object tracking using video clips/search regions. Use of non-RGB modalities, natural-language input, thermal input, event input, or restoration input is not reported for the method.

## Motivation
- Summary: MCITrack is motivated by the limitation that prior video-level trackers often transmit contextual information through only a few tokens, which can lose information and limit context capture.
- Evidence:
  - p.1: The abstract says existing methods typically use only a few tokens to convey video-level contextual information, causing information loss.
  - p.1: The introduction contrasts dynamic templates and extra-token propagation with hidden-state layers.
  - p.2: The paper states that limited additional tokens restrict comprehensive contextual-information capture.

## Main problem addressed
- Summary: The paper addresses how to record and transmit richer contextual information across a video stream for tracking by using Mamba hidden states inside a Contextual Information Fusion module.
- Evidence:
  - p.1: The abstract says MCITrack leverages Mamba hidden states to continuously record and transmit contextual information throughout the video stream.
  - p.2: The authors introduce hidden-state layers to store and transmit richer contextual information.
  - p.3: The overview says CIF blocks integrate historical contextual information into backbone blocks and update hidden states based on current backbone output.

## Main contributions
1. Introduces a hidden-state-based method for transmitting contextual information in video-level object tracking.
2. Develops the MCITrack model family around the Contextual Information Fusion (CIF) module.
3. Demonstrates state-of-the-art or competitive results across multiple tracking datasets.
Evidence:
- p.2: The contribution list says the paper introduces a new method for transmitting contextual information and develops a new family of video-level tracking models named MCITrack.
- p.1: The abstract identifies CIF as the core module and reports benchmark examples including 76.6% AUC on LaSOT and 80.0% AO on GOT-10k.
- p.5-p.6: Tables and comparison text report results on large-scale and additional tracking benchmarks.

## Methodology
- Overall architecture: MCITrack consists of a visual backbone, Contextual Information Fusion module, and prediction head.
- Main modules: Fast-iTPN backbone, CIF module, CIF blocks, Mamba layer, in-attention layer, out-attention layer, FFN, OSTrack-style classification/regression head.
- Mamba usage: Mamba is used inside CIF blocks to store and update historical contextual information in hidden states. Cross-attention integrates the stored context into current backbone features, and hidden states are updated as the video progresses.
- Loss functions: Classification loss/focal loss, L1 regression loss, and GIoU loss; each frame contributes an individual loss in video-level training.
- Training strategy: Uses LaSOT, GOT-10k, TrackingNet, COCO, and VastTrack; uses 5-frame video clips and two search regions; stores contextual information in hidden states between search-region passes; uses AdamW, learning rates 4e-5 for the backbone and 4e-4 for other parameters, weight decay 1e-4, 300 epochs, 60k samples per epoch, and total batch size 128 on two 80GB Tesla A800 GPUs.
- Evidence:
  - p.3: Figure 2 and overview describe backbone, CIF module, and prediction head.
  - p.3: The CIF module is described as containing Mamba and cross-attention layers for storing, integrating, and updating contextual information.
  - p.4: The Mamba layer updates hidden states based on current input; the SSM equation states that previous hidden states store contextual information and current hidden states update from current input.
  - p.4: The head/loss section describes classification score, bounding-box size, offset outputs, focal/classification loss, L1, and GIoU.
  - p.5: Implementation details report the training data, clip/search inputs, hidden-state transmission during training, optimizer, learning rates, epochs, samples, batch size, and hardware.

## Degradation/restoration analysis
- Handles degradation? Not reported.
- Degradation types: Not reported. The paper mentions blurriness as a challenge for appearance-only trackers, but does not define degradation-specific training, testing, or objectives.
- Restoration/enhancement? Not reported. A feature visualization uses the word "enhancement" for emphasized target edges, not image restoration/enhancement.
- Image-level or feature-level? Not reported for degradation/restoration. Feature-level context fusion is used, but not for restoration.
- Evidence:
  - p.2: The related-work discussion says image-level trackers struggle with object deformation and blurriness, but MCITrack's proposed mechanism is contextual-information transmission.
  - p.7: The visualization text says CIF emphasizes target edge information; it does not report image restoration, enhancement output, or degraded-image recovery.

## Tracking-specific analysis
- Template-search matching: Yes. The paper frames visual tracking as using template/search images and implements video-clip/search-region inputs with a tracking head.
- Temporal memory: Yes. Mamba hidden states in CIF blocks store, update, and transmit historical contextual information.
- Dynamic template update: Partial. The paper discusses dynamic templates as prior work; MCITrack uses a memory bank to store reliable frames and update the video clip during inference, but does not report a degradation-aware template update.
- Response-map design: Not reported. The paper reports classification score, box size, and offset heads, not response-map fusion.
- Evidence:
  - p.1: The introduction says existing trackers use template and search region images for matching.
  - p.3: MCITrack takes a video clip and search region as input and passes backbone output to a prediction head.
  - p.4: Mamba hidden states store contextual information and are updated from current input.
  - p.5-p.6: During inference, the method maintains a memory bank of reliable frames; hidden states are only updated if the classification score exceeds a threshold to avoid misleading information.

## Datasets and metrics
- Datasets: Training uses LaSOT, GOT-10k, TrackingNet, COCO, and VastTrack. Evaluation reports LaSOT, LaSOText, TrackingNet, GOT-10k, TNL2K, NFS, UAV123, and VOT2020.
- Metrics: AUC, normalized precision (PNorm), precision (P), average overlap (AO), success rates SR0.5/SR0.75, EAO for VOT2020, parameters, FLOPs, and FPS.
- Evidence:
  - p.5: Table 1 reports LaSOT, LaSOText, TrackingNet, and GOT-10k with AUC/PNorm/P or AO/SR metrics.
  - p.5: Training details list LaSOT, GOT-10k, TrackingNet, COCO, and VastTrack.
  - p.6: Table 3 reports TNL2K, NFS, and UAV123 AUC; the text also reports VOT2020 EAO.
  - p.5: Table 2 reports parameters, FLOPs, and inference speed.

## Explicit limitations
- Limitations stated by authors: MCITrack has slow model training due to video-level modeling, and video-clip handling introduces more computational overhead than single-frame images. The authors propose accelerating training and reducing video-clip burden through efficient multi-frame integration and lightweight models.
- Evidence:
  - p.7: The limitation paragraph explicitly states slow model training and extra computational overhead from handling video clips.
  - p.7: The same paragraph says future work should accelerate training, minimize computational burden, reduce video clip size, and develop a lightweight model.

## Implicit limitations
- Limitation inferred from method/evaluation: MCITrack's memory update is confidence/score-based rather than degradation-aware, and the method does not report restoration or enhancement of degraded template/search frames.
- Why this is an inference, not an author claim: The paper reports hidden-state updates conditioned on classification score and focuses on contextual-information transmission; it does not report image degradation labels, synthetic degradation, restoration objectives, or degradation-conditioned update rules.

## Relevance to our second paper
- How this paper supports our research gap: It shows Mamba hidden states are already used in tracking to carry video-level context and memory across frames.
- How this paper threatens our novelty: It makes "Mamba hidden states for tracking context/memory" non-novel by itself.
- What remains unsolved: It does not report restoration-oriented Mamba, image degradation handling, degradation-aware memory update, or feature recovery for degraded RGB template-search tracking.
