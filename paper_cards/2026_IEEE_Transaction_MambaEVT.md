# Paper Card: 2026_IEEE_Transaction_MambaEVT

## Bibliographic information
- Title: MambaEVT: Event Stream-Based Visual Object Tracking Using State Space Model
- Authors: Xiao Wang, Chao Wang, Shiao Wang, Xixi Wang, Zhicheng Zhao, Lin Zhu, Bo Jiang
- Year: 2026
- Venue: IEEE Transactions on Circuits and Systems for Video Technology
- Task: Event-camera single-object visual tracking
- Modality: Event-only tracking using event streams converted into event images

## Motivation
- Summary: The paper is motivated by event-camera tracking advantages and by limitations of Transformer-based event trackers that use static templates.
- Evidence: The abstract says event cameras provide low energy consumption, high dynamic range, and dense temporal resolution, while current event trackers are bottlenecked by Vision Transformers and static templates (p. 1). The introduction says event cameras outperform RGB cameras in low energy, high dynamic range, and dense temporal resolution (p. 1). Existing static-template event trackers are said to be unsatisfactory in long-term tracking or with significant appearance variation (p. 2).

## Main problem addressed
- Summary: The paper addresses event-based template-search tracking with a pure Mamba backbone and learnable dynamic template generation.
- Evidence: The abstract proposes a Mamba-based framework with linear-complexity backbone, search/template feature extraction and interaction, and dynamic template update via Memory Mamba (p. 1). The framework overview states that Vision Mamba performs feature extraction, interaction, and fusion, while Memory Mamba generates dynamic templates for robustness to appearance variation (p. 2).

## Main contributions
1. A pure Mamba-style event-camera visual tracking framework using Vision Mamba for feature extraction, interaction, and fusion.
2. A Memory Mamba dynamic template update strategy using short-term and long-term template libraries.
3. Experiments on EventVOT, VisEvent, and FE240hz validating effectiveness and efficiency.
Evidence: The paper states that it adopts a pure Mamba-style approach for efficient tracking and that Memory Mamba helps event tracking through dynamic template updating (p. 3). The contribution list includes a dynamic template update module and experiments on EventVOT, VisEvent, and FE240hz (p. 2).

## Methodology
- Overall architecture: Event streams are converted to event images; static template, dynamic template, and search tokens are concatenated and passed through Vision Mamba; search-region tokens feed an FCN tracking head; Memory Mamba uses long-term or short-term template libraries to generate a dynamic fused template for the next iteration (p. 4-p. 6).
- Main modules: Event image representation, Vision Mamba backbone, FCN tracking head, Memory Mamba, long-term memory library, short-term memory library, template-library update, and dynamic template generation (p. 4-p. 6).
- Mamba usage: Mamba is used as an efficient backbone and as a memory module for dynamic template generation. Vision Mamba extracts and interacts template/search features, while Memory Mamba fuses template sequences from memory into one dynamic template (p. 5-p. 6).
- Loss functions: The framework uses focal loss, L1 loss, and GIoU loss, combined as L = lambda1 L1 + lambda2 Lfocal + lambda3 LGIoU with lambda1=5, lambda2=1, lambda3=2 (p. 6).
- Training strategy: The tracker is implemented in PyTorch on NVIDIA RTX 3090 GPUs. It has MambaEVT and MambaEVT-P variants, uses Vim-S ImageNet-1K pretrained initialization, trains 50 epochs with AdamW, weight decay 1e-4, initial learning rate 0.0004 with decay after 30 epochs, templates resized to 128 x 128, search regions to 256 x 256, and K=7 dynamic templates during training (p. 7).
- Evidence: Data flow and tracking head are described on p. 5. Memory Mamba and library generation are described on p. 5-p. 6. Losses and datasets are described on p. 6. Implementation details are on p. 7.

## Degradation/restoration analysis
- Handles degradation? Partial
- Degradation types: Low light, high dynamic range, motion blur, fast motion, frame loss, occlusion-like disappearance, significant appearance variation, and cluttered backgrounds are discussed through event-camera tracking and memory.
- Restoration/enhancement? Not reported
- Image-level or feature-level? Feature/template-memory level; no image restoration or enhancement is reported.
- Evidence: EventVOT is described as pure event-based tracking with high-speed response, excellent low-light performance, low latency, and low power (p. 6). FE240hz addresses motion blur and high dynamic range (p. 6). The dynamic-template section says the tracker remains sensitive to appearance variation and clutter and uses Memory Mamba to collect tracking results and generate adaptive templates (p. 5). No restoration module is described (p. 4-p. 6).

## Tracking-specific analysis
- Template-search matching: Yes; static template, dynamic template, and search region tokens are processed together, and search tokens are sent to the tracking head (p. 5).
- Temporal memory: Yes; Memory Mamba uses short-term and long-term memory libraries for dynamic template generation (p. 5-p. 6).
- Dynamic template update: Yes; the method uses a learnable Memory Mamba update strategy and memory libraries, but it is not reported as degradation-aware specifically (p. 1, p. 5-p. 6).
- Response-map design: The FCN tracking head outputs a target classification score map, local offset, and normalized bounding-box size; the paper also visualizes response maps (p. 5, p. 11).
- Evidence: The head and memory data flow are described on p. 5. Template library update and Memory Mamba generation are described on p. 5-p. 6. Response-map visualization is described on p. 11.

## Datasets and metrics
- Datasets: EventVOT, FE240hz, and VisEvent.
- Metrics: Precision Rate (PR), Normalized Precision Rate (NPR), and Success Rate (SR).
- Evidence: The experiment section lists EventVOT, FE240hz, and VisEvent as event-based tracking datasets (p. 6). The metrics section defines PR, NPR, and SR (p. 6-p. 7).

## Explicit limitations
- Limitations stated by authors: The tracker has relatively low inference speed that limits real-time applicability; performance varies with Memory Mamba and backbone configurations; the current training strategy and sequence encoding may not fully exploit Mamba's long-sequence potential; backbone choice strongly affects representation.
- Evidence: The limitation analysis states these points and calls for architectural optimization/lightweight design (p. 12). The conclusion says future work will improve running efficiency and reduce energy consumption using spiking neural networks (p. 12).

## Implicit limitations
- Limitation inferred from method/evaluation: The method is event-only and does not solve RGB-only image degradation or restoration-guided RGB template-search tracking.
- Why this is an inference, not an author claim: This follows from its event-stream input representation, event-only datasets, and event-camera framing (p. 1, p. 4, p. 6); the authors do not present it as an RGB restoration method.

## Relevance to our second paper
- How this paper supports our research gap: It supports the missing-intersection analysis by showing Mamba used for event-camera tracking, efficient backbone design, and dynamic template memory, not RGB restoration-oriented degradation recovery.
- How this paper threatens our novelty: It threatens broad claims that Mamba trackers do not use dynamic templates or memory, because Memory Mamba is explicitly used for dynamic template generation (p. 1, p. 5-p. 6).
- What remains unsolved: RGB-only degradation robustness and restoration/enhancement for template-search tracking remain not reported; the template update is dynamic but not explicitly degradation-aware.
