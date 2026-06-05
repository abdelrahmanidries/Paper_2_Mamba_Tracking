# Paper Card: 2025_CVPR_RGBE_MamTrack

## Bibliographic information
- Title: Exploring Historical Information for RGBE Visual Tracking with Mamba
- Authors: Chuanyu Sun, Jiqing Zhang, Yang Wang, Huilin Ge, Qianchen Xia, Baocai Yin, Xin Yang
- Year: 2025
- Venue: CVPR 2025
- Task: RGB-Event single-object visual tracking, with additional RGB-T generalization experiments
- Modality: RGB plus event; additional experiments use visible plus thermal infrared

## Motivation
- Summary: The paper is motivated by the complexity of existing RGBE fusion modules and by the lack of effective historical information modeling for target appearance and motion changes.
- Evidence: The abstract says existing RGBE trackers use complex cross-modal fusion modules with higher computational complexity and training challenges, and generally ignore historical information needed to grasp target appearance and motion trends (p. 1). The introduction says event cameras offer high temporal resolution and dynamic range, and RGBE approaches improve tracking in challenging conditions such as fast motion and limited illumination (p. 1).

## Main problem addressed
- Summary: The paper addresses adaptive RGB-event fusion and historical temporal modeling for robust RGBE tracking.
- Evidence: The paper proposes Mamba-based modules for robust RGB-E tracking through efficient multimodal fusion and historical information transmission (p. 2). It states that prior multimodal trackers emphasize fusion but overlook mining historical information, while MamTrack uses Mamba for both adaptive RGB-E fusion and historical cues (p. 3).

## Main contributions
1. MamTrack, a framework incorporating Mamba into RGBE multimodal tracking.
2. A Mamba-based Fusion Mamba module and Historical Decoder for adaptive multimodal fusion and target history modeling.
3. State-of-the-art results on multiple short-term and long-term RGBE benchmarks.
Evidence: The contribution list states these three points (p. 2). The abstract also names the Mamba fusion module and historical decoder, and reports SOTA performance on RGBE benchmarks (p. 1).

## Methodology
- Overall architecture: MamTrack has RGB and event branches with shared weights, a Multimodal Encoder for feature extraction and fusion, a Fusion Mamba module inserted between Transformer encoder layers, a Historical Decoder for temporal cues, and a prediction head for target localization (p. 3-p. 5).
- Main modules: Multimodal Encoder, Fusion Mamba, Target-Aware Scan, Cross-Modality Scan, Historical Decoder, Historical State Aware module, Feature-Sequence Attention module, and center-based prediction head (p. 3-p. 5).
- Mamba usage: Mamba is used for modality-selective fusion and historical temporal modeling. Target-Aware Scan enhances template-search interaction with bidirectional SSM, Cross-Modality Scan adaptively fuses RGB and event modalities, and the Historical State Aware module captures historical states as a sequence (p. 4-p. 5).
- Loss functions: The center-based head outputs classification score, bounding-box size, and offset; training uses weighted focal loss for classification plus GIoU and L1 losses for bounding-box regression, with lambda_iou=2 and lambda_L1=5 (p. 5).
- Training strategy: The implementation uses PyTorch, 8 NVIDIA RTX 4090 GPUs, batch size 16, AdamW, weight decay 1e-4, learning rate 4e-4, pretrained HiViT-Base as a 20-layer Transformer encoder, 50 epochs on the RGB-Event training set, Fusion Mamba inserted into layers 12, 15, and 18, and a 3-layer decoder (p. 5).
- Evidence: The architecture is summarized on p. 3. Multimodal encoder, Fusion Mamba, and Historical Decoder details are on p. 4-p. 5. Loss and training details are on p. 5.

## Degradation/restoration analysis
- Handles degradation? Partial
- Degradation types: Fast motion, limited illumination, motion blur, partial occlusion, complex background, and general degraded-condition attributes are discussed.
- Restoration/enhancement? Not reported
- Image-level or feature-level? Feature-level multimodal fusion and historical temporal modeling; no image restoration or enhancement is reported.
- Evidence: The introduction says RGBE approaches enhance tracking in fast motion and limited illumination (p. 1). The VisEvent attribute analysis says MamTrack performs best under degraded conditions by fusing RGB and event strengths (p. 6). The visualization discussion says RGB-event fusion improves confidence under motion blur or fast motion, while historical cues help with partial occlusion and complex background (p. 8).

## Tracking-specific analysis
- Template-search matching: Yes; the encoder receives RGB/event template and search tokens, and Target-Aware Scan facilitates interaction between template and search tokens (p. 4, p. 6).
- Temporal memory: Yes; the Historical Decoder uses Mamba-based Historical State Aware modeling and autoregressive queries to capture target appearance changes and motion trends (p. 1, p. 4-p. 5).
- Dynamic template update: Not reported as an online template-update policy; historical information is modeled through the decoder rather than a stated degradation-aware template update.
- Response-map design: The center-based head outputs a classification score map, bounding-box size, and offset (p. 5).
- Evidence: Template/search tokens are described in the Multimodal Encoder section (p. 4). Historical Decoder and HSA/FSA modules are described on p. 4-p. 5. The head output is described on p. 5.

## Datasets and metrics
- Datasets: VisEvent, FELT, FE108; additional RGB-T experiments on LasHeR and RGBT234.
- Metrics: Success Rate (SR), Precision Rate (PR), and Overlap Precision (OPT).
- Evidence: Experiments compare against SOTA trackers on VisEvent, FELT, and FE108 (p. 5-p. 6). RGB-T experiments use LasHeR and RGBT234 (p. 7-p. 8). The evaluation section defines SR, PR, and OPT (p. 5).

## Explicit limitations
- Limitations stated by authors: The authors state that they mainly focus on Mamba for modality fusion and do not leverage the high temporal resolution characteristics of event data; future work will explore this.
- Evidence: The conclusion explicitly states this limitation and future direction (p. 8).

## Implicit limitations
- Limitation inferred from method/evaluation: MamTrack does not solve RGB-only degradation robustness through restoration; robustness is obtained from event/thermal complementary sensing, Mamba fusion, and historical temporal modeling.
- Why this is an inference, not an author claim: This follows from the RGB-event input design, cross-modality fusion modules, RGB-T generalization experiments, and lack of restoration/enhancement components (p. 1, p. 4-p. 8); the authors do not frame it as an RGB-only restoration method.

## Relevance to our second paper
- How this paper supports our research gap: It supports the missing-intersection analysis by showing Mamba used for multimodal fusion and temporal history, not restoration-oriented RGB degradation recovery.
- How this paper threatens our novelty: It threatens broad claims about Mamba not being used for template-search interaction, multimodal fusion, or historical tracking cues; Target-Aware Scan and the Historical Decoder directly cover these areas (p. 4-p. 5).
- What remains unsolved: RGB-only degradation-robust template-search tracking using restoration-oriented Mamba remains not reported; event high temporal resolution is also not fully exploited by the authors.
