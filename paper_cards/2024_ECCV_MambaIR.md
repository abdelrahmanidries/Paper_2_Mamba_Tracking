# Paper Card: 2024_ECCV_MambaIR

## Bibliographic information
- Title: MambaIR: A Simple Baseline for Image Restoration with State-Space Model
- Authors: Hang Guo, Jinmin Li, Tao Dai, Zhihao Ouyang, Xudong Ren, Shu-Tao Xia
- Year: 2024
- Venue: ECCV, from PDF filename `2024_ECCV_MambaIR.pdf`
- Task: Image restoration, including super-resolution, image denoising, real-world denoising, and JPEG compression artifact reduction.
- Modality: Single-image restoration from low-quality image input to high-quality image output; not video tracking.

## Motivation
- Summary: The paper is motivated by an image-restoration backbone tradeoff: CNNs are efficient but have limited global receptive fields, while Transformer-style global modeling is expensive. Mamba is investigated as a linear-complexity long-range model, but vanilla Mamba is not directly suited to low-level vision because of local pixel forgetting and channel redundancy.
- Evidence:
  - p.1: The abstract says image restoration backbones face a dilemma between global receptive fields and efficient computation, and that Mamba offers long-range dependency modeling with linear complexity.
  - p.1: The authors state that standard Mamba has challenges in low-level vision, including "local pixel forgetting" and "channel redundancy."
  - p.3: The paper explains that flattened 1D image sequences can make spatially close pixels distant in the sequence, causing local pixel forgetting, and that large hidden states can cause channel redundancy.

## Main problem addressed
- Summary: The paper addresses how to adapt Mamba/state-space modeling to image restoration while preserving local pixel structure and reducing redundant channel representations.
- Evidence:
  - p.3: The authors introduce MambaIR as a benchmark model "to adapt Mamba for image restoration."
  - p.3: The paper describes RSSB as using local convolution to mitigate local pixel forgetting and channel attention to reduce channel redundancy.

## Main contributions
1. Adapts state-space models to low-level image restoration as a simple Mamba-based restoration baseline.
2. Proposes the Residual State-Space Block (RSSB) with local enhancement and channel attention.
3. Evaluates the model across multiple restoration tasks and reports competitive restoration performance.
Evidence:
- p.3: The contributions list states that MambaIR adapts state-space models for low-level image restoration.
- p.3: The same list identifies RSSB as the block that improves standard Mamba with local enhancement and channel redundancy reduction.
- p.9: The experiments cover image super-resolution, denoising, real-world denoising, and JPEG compression artifact reduction.

## Methodology
- Overall architecture: MambaIR has shallow feature extraction, deep feature extraction through Residual State-Space Groups/Blocks, and high-quality image reconstruction.
- Main modules: Residual State-Space Groups (RSSGs), Residual State-Space Blocks (RSSBs), Vision State-Space Module (VSSM), 2D Selective Scan Module (2D-SSM), local convolution, channel attention, and reconstruction layers.
- Mamba usage: Mamba is used as an image-restoration state-space backbone through VSSM and 2D-SSM. The 2D-SSM scans image features in four directions, applies the discrete state-space equation to each sequence, then merges them back into 2D structure.
- Loss functions: L1 loss for image super-resolution; Charbonnier loss for image denoising.
- Training strategy: Data augmentation uses horizontal flips and rotations; cropped patches are used for SR and denoising; Adam optimizer is used with initial learning rate 2e-4 and scheduled halving; training uses 8 NVIDIA V100 GPUs.
- Evidence:
  - p.3: The three-stage formulation is shallow feature extraction, RSSB-based deep feature extraction, and high-quality image reconstruction.
  - p.6: Fig. 2 and the method text identify RSSG, RSSB, VSSM, and 2D-SSM as the main architecture components.
  - p.7: The paper adds local convolution after VSSM and channel attention in RSSB to handle local pixel forgetting and channel redundancy.
  - p.8: VSSM captures long-range dependencies with the state-space equation, and 2D-SSM scans four directions before merging back to 2D.
  - p.8: The loss section states L1 loss for SR and Charbonnier loss for denoising.
  - p.9: The training details specify augmentation, crop sizes, batch sizes, Adam optimizer, learning rate schedule, and GPU setup.

## Degradation/restoration analysis
- Handles degradation? Yes, in image-restoration tasks; not in tracking.
- Degradation types: Low-resolution images for SR, Gaussian color noise, real-world denoising degradation, and JPEG compression artifacts.
- Restoration/enhancement? Yes.
- Image-level or feature-level? Both: feature-level restoration blocks are used to reconstruct image-level high-quality outputs.
- Evidence:
  - p.1: Image restoration is defined as reconstructing a high-quality image from a low-quality input, with subproblems such as super-resolution and denoising.
  - p.9: The experiments include classic SR, lightweight SR, real SR, Gaussian color image denoising, real-world denoising, and JPEG CAR.
  - p.13: The paper explicitly says real image denoising evaluates robustness when facing real-world degradation.
  - p.14: Tables report Gaussian color denoising and real image denoising results, with PSNR/SSIM on SIDD and DND.

## Tracking-specific analysis
- Template-search matching: Not reported.
- Temporal memory: Not reported for tracking; Mamba is used for image-token sequence modeling, not target-memory tracking.
- Dynamic template update: Not reported.
- Response-map design: Not reported.
- Evidence:
  - p.1: The task is image restoration from low-quality input to high-quality output.
  - p.9: The listed experiments are restoration tasks, not visual object tracking.
  - p.6-p.8: The architecture describes image feature reconstruction modules, not template-search matching, tracking response maps, or template update.

## Datasets and metrics
- Datasets: DIV2K, Flickr2K, Set5, Set14, B100/BSDS100, Urban100, Manga109, BSD500, WED, BSD68, Kodak24, McMaster, SIDD, DND. JPEG CAR is mentioned, but main-paper dataset details are deferred to supplementary material in the extracted text.
- Metrics: PSNR and SSIM; parameter count and MACs are also used for lightweight SR comparison.
- Evidence:
  - p.9: The dataset section lists DIV2K/Flickr2K for SR training, Set5/Set14/B100/Urban100/Manga109 for SR evaluation, BSD500/WED plus BSD68/Kodak24/McMaster/Urban100 for denoising, and SIDD/DND for real denoising.
  - p.9: The paper states that performance is evaluated with PSNR and SSIM on the Y channel.
  - p.13: Lightweight SR comparisons report parameters, MACs, PSNR, and SSIM.
  - p.14: Denoising tables report PSNR/SSIM for Gaussian and real denoising datasets.

## Explicit limitations
- Limitations stated by authors: Not reported for the proposed MambaIR method in the extracted main-paper text. The authors do explicitly state limitations of standard/vanilla Mamba that motivate MambaIR: local pixel forgetting and channel redundancy.
- Evidence:
  - p.1: The abstract identifies standard Mamba's low-level vision challenges as local pixel forgetting and channel redundancy.
  - p.3: The method motivation explains why vanilla Mamba is not a natural fit for image restoration.
  - p.14: The conclusion summarizes the proposed fixes and does not report a separate limitation or future-work section for MambaIR itself.

## Implicit limitations
- Limitation inferred from method/evaluation: The paper does not evaluate restoration-oriented Mamba inside an RGB template-search tracker, so it does not establish whether MambaIR improves target-discriminative tracking under degraded search/template frames.
- Why this is an inference, not an author claim: The authors do not claim a tracking limitation. This is inferred because the reported tasks and datasets are image restoration benchmarks, while template-search matching, temporal memory, dynamic template update, and response-map design are not reported.

## Relevance to our second paper
- How this paper supports our research gap: It provides direct evidence that Mamba can be adapted for restoration-specific image recovery with local enhancement, channel attention, and 2D state-space scanning.
- How this paper threatens our novelty: It already covers restoration-oriented Mamba for several image degradation/restoration settings, so our novelty cannot be simply "use Mamba for restoration" or "use Mamba for degraded images."
- What remains unsolved: It does not report RGB template-search tracking, target-discriminative feature recovery, degradation-robust matching, dynamic template update, or tracking response-map fusion under degradation.
