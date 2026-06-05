# Paper Card: 2026_IEEE_Transaction_SMTrack

## Bibliographic information
- Title: SMTrack: State-Aware Mamba for Efficient Temporal Modeling in Visual Tracking
- Authors: Yinchao Ma, Dengqing Yang, Zhangyu He, Wenfei Yang, Tianzhu Zhang
- Year: 2026
- Venue: IEEE Transactions on Image Processing, from extracted title page and PDF filename `2026_IEEE_Transaction_SMTrack.pdf`
- Task: Visual object tracking with efficient temporal modeling.
- Modality: RGB visual tracking. The paper explicitly contrasts SMTrack with MambaVT for RGB-T tracking.

## Motivation
- Summary: SMTrack is motivated by the cost and complexity of temporal modeling in CNN-, Transformer-, and earlier SSM-based trackers. It aims to use state propagation/updating to build long-range temporal interactions efficiently.
- Evidence:
  - p.1: The abstract says CNN and Transformer trackers have limitations for long-range temporal dependencies, often needing customized modules or high computational cost.
  - p.2: Figure/text contrasts CNN temporal modeling, Transformer temporal cues, prior bidirectional SSM templates, and SMTrack's temporal causal scanning with hidden-state propagation.
  - p.2: The paper says Mamba's state-shared timescale limits diverse hidden-state cue capture, motivating state-aware timescales.

## Main problem addressed
- Summary: The paper addresses efficient long-range temporal modeling for RGB tracking by creating a state-aware Mamba/SSM tracker where the search region interacts with previous templates through hidden states instead of repeated template scanning.
- Evidence:
  - p.1: SMTrack is described as a temporal modeling paradigm for tracking using hidden state propagation and updating.
  - p.2: The authors argue for decoupling templates from future information so the search region can interact with templates via hidden states without repetitive scanning.
  - p.6: Tracking with previous states lets the search region interact with scanned templates through hidden states without repeatedly scanning templates.

## Main contributions
1. Proposes SMTrack as a temporal modeling paradigm for visual tracking using hidden-state propagation/updating.
2. Proposes Selective State-Aware Space Model (SASM) with state-wise timescale parameters for diverse temporal cues.
3. Reports strong tracking performance with low computational costs.
Evidence:
- p.2: The contribution list states the new temporal modeling paradigm and hidden-state propagation/updating without customized modules or high computational cost.
- p.2: The same contribution list introduces SASM with state-wise timescale parameters.
- p.1 and p.11: The abstract and conclusion report promising/extensive experimental results with low computational costs.

## Methodology
- Overall architecture: SMTrack is a pure SSM/Mamba-style feature extractor for RGB tracking with SASM blocks, temporal causal scanning, hidden-state propagation, and an OSTrack-like box head.
- Main modules: SASM blocks, state-wise and channel-wise timescale parameters, temporal causal flipping/scanning, hidden-state memory, multi-frame propagation, three-branch fully convolutional box head.
- Mamba usage: SMTrack builds on selective state-space/Mamba ideas but modifies them with SASM. Hidden states carry temporal cues; the search region interacts with scanned templates through saved hidden states; new target templates from tracked frames can update hidden states.
- Loss functions: Weighted focal loss for classification, L1 loss and generalized IoU loss for bounding-box regression.
- Training strategy: Uses COCO, LaSOT, GOT-10K, and TrackingNet training splits; common augmentations include translation, horizontal flipping, and brightness jittering; minimal unit has four target templates and one search region; AdamW optimizer; learning rates 4e-5 for SASM blocks and 4e-4 for box head with cosine annealing; batch size 96; 300 epochs, with GOT-10k one-shot retraining for 100 epochs.
- Evidence:
  - p.4: SASM uses state-wise timescales so different hidden states can capture diverse temporal cues, and introduces interactions among hidden states.
  - p.5: SMTrack maintains temporal causality across frames while learning spatial-aware features in SASM blocks.
  - p.6: The box head regresses classification score map, offset map, and normalized box-size map; losses are focal, L1, and GIoU.
  - p.6: Tracking with previous states scans the initial template once, stores final hidden states, and lets the search region interact with the template via hidden states.
  - p.6: Training details report datasets, augmentations, minimal training unit, optimizer, learning rates, batch size, epochs, and GOT-10k retraining.

## Degradation/restoration analysis
- Handles degradation? Partial for template-update quality, but not image-degradation tracking in the restoration sense.
- Degradation types: The paper mentions motion blur as a challenging scenario and "template degradation" in a template-evaluator ablation, but does not define synthetic blur/noise/compression/low-resolution degradation handling or image restoration.
- Restoration/enhancement? Not reported.
- Image-level or feature-level? Feature-level temporal hidden-state modeling; no image-level restoration/enhancement is reported.
- Evidence:
  - p.10: A template evaluator is tried to select high-quality templates, with templates scoring above 0.5 reserved for hidden-state updating to ensure robustness against template degradation; the authors report the evaluator contributes little.
  - p.11: Visual comparisons include challenging scenarios such as deformation, occlusion, distractor, and motion blur.
  - p.6-p.7: Training details and metrics do not report synthetic degradation generation or restoration/enhancement losses.

## Tracking-specific analysis
- Template-search matching: Yes. SMTrack uses target templates and search regions; search features interact with template hidden states, then a box head predicts target state.
- Temporal memory: Yes. Hidden states of scanned templates are saved into memory, sampled during tracking, averaged as initial states, and used for multi-frame propagation.
- Dynamic template update: Yes. A new target template is cropped every 20 frames using tracking results and scanned to obtain hidden states saved to memory. This update is temporal/hidden-state based, not explicitly image-degradation-aware in the final design.
- Response-map design: Not reported as response-map fusion. The paper reports a classification score map, offset map, and box-size map in a box head.
- Evidence:
  - p.6: The search region builds interactions with scanned templates via hidden states, and new target templates can update hidden states.
  - p.7: Algorithm 1 crops a new target template every 20 frames, saves hidden states to memory, samples hidden states, averages them, and sets memory size to 50.
  - p.10: The authors analyze update interval, propagation strategies, and memory size; they also test but avoid a template evaluator.
  - p.6: The box head predicts classification score map, offset map, and normalized box size map.

## Datasets and metrics
- Datasets: Training uses COCO, LaSOT, GOT-10K, and TrackingNet. Evaluation reports GOT-10k, TrackingNet, LaSOT, LaSOText, AAV123, and NFS.
- Metrics: AO, SR, AUC, precision P, normalized precision PNorm, parameters/FLOPs or computational cost, FPS, and qualitative visualizations.
- Evidence:
  - p.6: Training details list COCO, LaSOT, GOT-10K, and TrackingNet.
  - p.7: Metrics are defined as AO, SR, AUC, P, and PNorm.
  - p.7-p.8: Evaluation discusses GOT-10k, TrackingNet, LaSOT, LaSOText, AAV123, and NFS.
  - p.11: Failure-case and qualitative visualizations are reported for challenging scenarios.

## Explicit limitations
- Limitations stated by authors: SASM has inferior parallelization capability to Transformer because advanced state-space models such as SASM and Mamba do not use matrix multiplication units optimized by GPUs/TPUs; this limits SMTrack's speed advantage over Transformer trackers on GPUs. The authors also report failure cases under out-of-view and occlusion.
- Evidence:
  - p.11: The Limitations section states SASM parallelization is inferior to Transformer and explains the GPU/TPU matrix-multiplication issue.
  - p.11: The Failure Cases section states SMTrack is limited in out-of-view and occlusion scenarios and can drift when target features degrade in the tracking frame.

## Implicit limitations
- Limitation inferred from method/evaluation: SMTrack is a temporal hidden-state tracker, not a restoration-guided tracker; its memory update is mostly temporal/state-based and not built around explicit image-quality degradation detection or restoration.
- Why this is an inference, not an author claim: The paper does not claim a restoration limitation. This is inferred because the method reports SASM hidden-state propagation, template memory, and box-head losses, while image restoration/enhancement objectives and synthetic degradation robustness experiments are not reported.

## Relevance to our second paper
- How this paper supports our research gap: It strongly documents Mamba/SSM use for temporal memory, hidden states, dynamic template-state propagation, and efficient RGB tracking.
- How this paper threatens our novelty: It blocks novelty claims based only on Mamba temporal modeling, hidden-state memory, dynamic template update, or RGB tracking with Mamba.
- What remains unsolved: It does not report restoration-oriented Mamba for degraded RGB template/search feature recovery, explicit synthetic image-degradation training, or restoration/enhancement-guided response design.
