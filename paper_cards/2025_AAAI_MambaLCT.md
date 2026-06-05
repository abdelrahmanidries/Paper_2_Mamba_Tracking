# Paper Card: 2025_AAAI_MambaLCT

## Bibliographic information
- Title: MambaLCT: Boosting Tracking via Long-term Context State Space Model
- Authors: Xiaohai Li, Bineng Zhong, Qihua Liang, Guorong Li, Zhiyi Mo, Shuxiang Song
- Year: 2025
- Venue: AAAI, from PDF filename `2025_AAAI_MambaLCT.pdf`
- Task: Visual object tracking with long-term video context.
- Modality: Visual template-search tracking from image/video frames. Use of language, thermal, event, or restoration modalities is not reported as an input to the method.

## Motivation
- Summary: The paper argues that existing context-aware trackers use adjacent frames, fixed windows, or limited tokens, which restricts long-term context. MambaLCT is motivated by using Mamba's efficient long-sequence modeling to aggregate target variation cues from the first frame to the current frame.
- Evidence:
  - p.1: The abstract says existing context length is limited to adjacent frames or video clips, causing insufficient contextual-information use.
  - p.2: The paper says Transformer-based context modeling is limited by quadratic complexity, while Mamba has potential for efficient long-term dependencies.
  - p.2: The authors ask whether combining Transformer and Mamba can extend context length and enable more robust appearance features.

## Main problem addressed
- Summary: MambaLCT addresses long-term context construction for tracking by separating spatial/appearance modeling from temporal context modeling and using a Context Mamba module to aggregate target information across historical search frames.
- Evidence:
  - p.2: The authors introduce MambaLCT to expand context from the initial frame to the current frame.
  - p.3: The method text says appearance features in tracking are not naturally autoregressive, so the work applies Mamba to temporal modeling rather than spatial appearance modeling.
  - p.4: The Context Mamba module continuously feeds search features from the first frame to the current frame into Mamba and compresses target-related information into hidden states.

## Main contributions
1. Proposes MambaLCT for capturing long-term target behavior and motion.
2. Designs a Context Mamba module for low-resource construction of long-term temporal context.
3. Reports state-of-the-art performance on six tracking benchmarks.
Evidence:
- p.2: The contribution list states that MambaLCT captures long-term behavior and overall motion.
- p.2: The same list states that the Context Mamba module constructs long-term contextual information along the temporal dimension with low resource consumption.
- p.2: The authors list LaSOT, LaSOText, GOT-10K, TrackingNet, TNL2K, and UAV123 as benchmarks where their method achieves state-of-the-art tracking performance.

## Methodology
- Overall architecture: MambaLCT has three main components: ucaEncoder, Context Mamba module, and tracking head.
- Main modules: Hierarchical ViT/HiViT backbone, ucaEncoder for unified context and appearance modeling, Context Mamba module, cross-frame/context token `cp`, and classification/regression tracking head.
- Mamba usage: Mamba is used for temporal context construction. Historical search-frame features are scanned along the temporal dimension, target-related information is compressed into hidden states, and context information is propagated frame-to-frame through hidden-state transfer and the context token.
- Loss functions: Classification loss, L1 regression loss, and GIoU loss with total loss `L = Lcls + lambda1 L1 + lambda2 LGIoU`; reported weights are lambda1 = 5 and lambda2 = 2.
- Training strategy: Uses video clip sampling to preserve contextual connections, trains on GOT-10K, LaSOT, COCO, and TrackingNet, uses HiViT-Base initialized with MAE, Vim-Small for the Mamba cross-frame information network with unidirectional scanning, AdamW optimizer, 300 epochs generally and 150 epochs for GOT-10K, batch size 16.
- Evidence:
  - p.3: The overview names ucaEncoder, Context Mamba module, and tracking head as the three main components.
  - p.3: The paper says input frames are tokenized, combined with contextual information, and fed into ucaEncoder; search features are continuously fed into Context Mamba.
  - p.4: Equations and text describe target-related information compressed into hidden state `H`, historical information recorded by empty token `T`, and context `Y_T` used to update `cp`.
  - p.4: The ucaEncoder injects context token `cp` into the attention operations of search and template tokens.
  - p.4: The training/loss section says the tracking head has classification and regression heads and uses classification, L1, and GIoU losses.
  - p.5: Training details report datasets, HiViT-Base, Vim-Small, unidirectional scanning, AdamW, epochs, batch size, and loss weights.

## Degradation/restoration analysis
- Handles degradation? Not reported.
- Degradation types: Not reported as designed degradation inputs or objectives. Motion blur and low resolution appear as LaSOT attributes, not as explicit degradation handling.
- Restoration/enhancement? Not reported.
- Image-level or feature-level? Not reported for degradation/restoration. Feature-level temporal context is modeled, but not as restoration.
- Evidence:
  - p.5: LaSOT attribute evaluation includes motion blur and low resolution, but the method description and training details do not define degradation generation, degradation losses, or restoration objectives.
  - p.7: The visualization discussion says MambaLCT performs well on motion blur, full occlusion, and deformation challenges; it attributes this to longer context, not to image restoration or degradation-specific training.

## Tracking-specific analysis
- Template-search matching: Yes. The paper follows the template-search tracking paradigm and injects long-term context into relationship modeling between template and search frames.
- Temporal memory: Yes. Mamba's hidden states aggregate target information from historical search frames, and cross-frame tokens transmit information between frames.
- Dynamic template update: Not reported as a dynamic template-update mechanism. The method updates context information/token state rather than reporting template image replacement.
- Response-map design: Not reported. The extracted text describes a classification/regression tracking head, but not a response-map fusion design.
- Evidence:
  - p.2: The related-work section explains the search-template matching paradigm and positions MambaLCT against template-only and context-based trackers.
  - p.4: Context information from the first `i` frames is used to model relationships between template and search frames by updating `cp`.
  - p.4: Historical target information is continuously aggregated through hidden states and transmitted to the next frame.
  - p.5: During inference, search-frame features and cross-frame tokens construct cross-frame information flow over the test sequence.

## Datasets and metrics
- Datasets: Training uses GOT-10K, LaSOT, COCO, and TrackingNet. Evaluation reports LaSOT, LaSOText, GOT-10K, TrackingNet, TNL2K, and UAV123.
- Metrics: AUC, normalized precision (PNorm), precision (P), average overlap (AO), success rate at thresholds SR0.5 and SR0.75, parameters, MACs, and FPS.
- Evidence:
  - p.5: Training details list GOT-10K, LaSOT, COCO, and TrackingNet.
  - p.5-p.6: LaSOT, LaSOText, GOT-10K, and TrackingNet are evaluated with AUC/PNorm/P or AO/SR metrics.
  - p.6-p.7: TNL2K and UAV123 comparisons report AUC scores.
  - p.5: Table 1 reports parameters, MACs, speed, and device.

## Explicit limitations
- Limitations stated by authors: The authors state that computational resource constraints prevent unifying training and testing, because training samples only portions of sequences rather than modeling the entire video sequence. They identify a more coherent training strategy and sequence sampling as future work.
- Evidence:
  - p.7: The limitation paragraph says the proposed video-level context modeling faces computational-resource constraints and that training/testing cannot be unified.
  - p.7: The authors state that during training they do not model the entire video sequence but sample portions, and propose a more coherent training strategy as future work.

## Implicit limitations
- Limitation inferred from method/evaluation: The method uses Mamba for long-term temporal context, not for restoration-oriented recovery of degraded template/search features; degradation-aware memory update is not reported.
- Why this is an inference, not an author claim: The paper reports Context Mamba hidden-state aggregation and benchmark/attribute evaluation, but it does not report degradation generation, restoration/enhancement losses, or a memory update conditioned on image degradation.

## Relevance to our second paper
- How this paper supports our research gap: It is evidence that Mamba has already been used in tracking for long-term temporal context and hidden-state aggregation.
- How this paper threatens our novelty: It prevents novelty claims based only on using Mamba for temporal context, long-term memory, or hidden-state propagation in tracking.
- What remains unsolved: It does not report restoration-oriented Mamba, degradation-specific template/search recovery, restoration/enhancement objectives, or degradation-aware memory update.
