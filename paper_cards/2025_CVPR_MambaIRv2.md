# Paper Card: 2025_CVPR_MambaIRv2

## Bibliographic information
- Title: MambaIRv2: Attentive State Space Restoration
- Authors: Hang Guo, Yong Guo, Yaohua Zha, Yulun Zhang, Wenbo Li, Tao Dai, Shu-Tao Xia, Yawei Li
- Year: 2025
- Venue: CVPR, from PDF filename `2025_CVPR_MambaIRv2.pdf`
- Task: Image restoration, including classic/lightweight super-resolution, JPEG compression artifact reduction, and Gaussian color image denoising.
- Modality: Single-image restoration from low-quality observations to high-quality images; not video or visual object tracking.

## Motivation
- Summary: The paper argues that Mamba-based image restoration backbones are promising but constrained by causal state-space modeling: each token depends only on previous tokens in the scanned sequence, which limits use of image-wide pixels and motivates a non-causal attentive state-space design.
- Evidence:
  - p.1: The abstract says Mamba-based restoration backbones balance global reception and efficiency, but causal modeling restricts full pixel utilization.
  - p.1: The introduction explains that each pixel is modeled only from preceding scanned pixels, creating detrimental effects for non-causal image restoration.
  - p.3: The motivation section states that causal modeling poses challenges for image restoration and that current methods use multi-directional scans with added complexity and redundancy.

## Main problem addressed
- Summary: The paper addresses the causal modeling mismatch between Mamba's scanned sequence processing and non-causal image restoration, aiming to let Mamba attend beyond scanned tokens and better connect distant but similar pixels.
- Evidence:
  - p.1: The authors propose MambaIRv2 to equip Mamba with non-causal modeling ability similar to ViTs.
  - p.2: The paper says the method uses the output matrix to query relevant pixels in the unscanned sequence and removes the need for multi-directional scanning.
  - p.3: The authors state that distant pixels suffer weak interaction because of long-range decay in causal Mamba.

## Main contributions
1. Proposes the Attentive State-space Equation (ASE), using prompt learning inside Mamba's state-space equation to query semantically similar pixels beyond scanned sequences.
2. Develops Semantic Guided Neighboring (SGN) to place semantically similar pixels closer in the 1D sequence and reduce long-range decay.
3. Integrates ASE, SGN, and auxiliary modules into MambaIRv2 as an attentive state-space restoration backbone.
Evidence:
- p.2: The contribution paragraph lists ASE, SGN, and the integrated MambaIRv2 restoration method.
- p.2: The authors state that ASE enables single-pass scanning and improved efficiency.
- p.2: The authors report improvements over SRFormer on Urban100 lightweight SR and HAT on Manga109 classical SR.

## Methodology
- Overall architecture: The model extracts shallow features from a low-quality image, processes them through Attentive State Space Groups/Blocks, and uses task-specific reconstruction modules to produce high-quality images.
- Main modules: Attentive State Space Module (ASSM), Attentive State-space Equation (ASE), Semantic Guided Neighboring (SGN), Attentive State Space Groups (ASSGs), Attentive State Space Blocks (ASSBs), window MHSA, FFN, convolution, pixelshuffle, and denoising reconstruction convolution.
- Mamba usage: Mamba is modified through ASE to add prompt-based non-causal querying into the output matrix, and SGN reorders image tokens so semantically similar pixels are closer in the scanned sequence.
- Loss functions: L1 loss for image SR; Charbonnier loss for denoising and JPEG CAR.
- Training strategy: Uses flips/rotations, 64x64 SR patches, 128x128 denoising patches, batch size 32 for SR and 8 for denoising/JPEG CAR, Adam optimizer with beta1=0.9 and beta2=0.999, initial learning rate 2e-4, and scheduled learning-rate halving.
- Evidence:
  - p.4: Fig. 3 and the method text define ASSM, ASE, and SGN as the core architecture.
  - p.4: ASE modifies Mamba's output matrix to query related pixels across the image using prompts.
  - p.5: SGN groups pixels by prompt-derived semantic labels and folds the sequence back to a spatial feature map.
  - p.5: The overall architecture uses a 3x3 convolution, ASSGs/ASSBs, window MHSA, ASSM, and task-specific reconstruction modules.
  - p.5: The training section reports augmentation, crop sizes, batch sizes, Adam optimizer, losses, learning rate, and model variants.

## Degradation/restoration analysis
- Handles degradation? Yes, in image-restoration tasks; not in tracking.
- Degradation types: Low-quality observations for SR, JPEG compression artifacts, and Gaussian color noise. Low-light, dehazing, deraining, and deblurring are discussed as related Mamba restoration work, not as MambaIRv2 experiments in the extracted main text.
- Restoration/enhancement? Yes.
- Image-level or feature-level? Both: feature-level ASSM/ASE/SGN processing is used for image-level reconstruction.
- Evidence:
  - p.1: The paper defines image restoration as recovering high-quality images from low-quality observations, including SR, denoising, and JPEG compression reduction.
  - p.5: The experiments cover super-resolution, JPEG CAR, and Gaussian color image denoising.
  - p.8: Table 6 reports JPEG CAR on Classic5 and LIVE1 across quality factors.
  - p.8: Table 7 reports Gaussian color denoising on CBSD68, Kodak24, McMaster, and Urban100.
  - p.2: The related-work paragraph mentions deraining, low-light enhancement, dehazing, and deblurring as other Mamba restoration tasks, not as MambaIRv2's evaluated tasks.

## Tracking-specific analysis
- Template-search matching: Not reported. The word "template" on p.5 refers to a block-design template, not a tracking template/search pair.
- Temporal memory: Not reported for tracking; Mamba is used for image-token state-space restoration.
- Dynamic template update: Not reported.
- Response-map design: Not reported.
- Evidence:
  - p.1: The task is image restoration from low-quality observations to high-quality images.
  - p.5: The experiments are SR, JPEG CAR, and Gaussian denoising, not tracking.
  - p.5: The architecture discussion describes image reconstruction modules rather than template-search matching, template update, or response maps.

## Datasets and metrics
- Datasets: DIV2K is reported for ablation training; Set5, Set14, BSDS100, Urban100, and Manga109 are used in SR tables; Classic5 and LIVE1 are used for JPEG CAR; CBSD68, Kodak24, McMaster, and Urban100 are used for Gaussian color denoising.
- Metrics: PSNR and SSIM for restoration quality; parameter count and MACs for efficiency comparisons.
- Evidence:
  - p.5: Ablations use MambaIRv2-light x2 SR trained on DIV2K.
  - p.6-p.7: SR comparison tables report Set5, Set14, BSDS100, Urban100, Manga109, PSNR, SSIM, parameter count, and MACs.
  - p.8: JPEG CAR table reports Classic5/LIVE1 with PSNR and SSIM across quality factors.
  - p.8: Gaussian denoising table reports PSNR on CBSD68, Kodak24, McMaster, and Urban100.

## Explicit limitations
- Limitations stated by authors: Not reported for the proposed MambaIRv2 method in the extracted main-paper text. The authors explicitly state limitations of existing Mamba-based restoration methods: causal modeling, redundant multi-directional scans, and long-range decay.
- Evidence:
  - p.1: The abstract identifies Mamba's causal modeling limitation as restricting full pixel utilization.
  - p.3: The paper states that existing Mamba-based methods rely on scanning strategies, that multi-directional scans add complexity and redundancy, and that causal Mamba has long-range decay.
  - p.8: The conclusion summarizes ASE and SGN as solutions and does not report a separate limitation or future-work section for MambaIRv2 itself.

## Implicit limitations
- Limitation inferred from method/evaluation: The paper does not test whether attentive state-space restoration improves RGB template-search tracking under image-quality degradation.
- Why this is an inference, not an author claim: The authors do not claim a tracking limitation. This is inferred from the task definition and experiment set, which are image restoration benchmarks rather than tracking datasets, tracking metrics, or template-search pipelines.

## Relevance to our second paper
- How this paper supports our research gap: It strengthens the evidence base for restoration-oriented Mamba by showing a non-causal attentive state-space design for restoration and by explicitly discussing degradation/restoration tasks.
- How this paper threatens our novelty: It reduces novelty for claims based only on restoration-oriented Mamba, non-causal Mamba restoration, or Mamba under image degradation. It also notes related Mamba restoration work for low-light, deraining, dehazing, and deblurring.
- What remains unsolved: It does not report degradation-robust RGB template-search tracking, target-specific template/search restoration, temporal tracking memory, dynamic template update, or response-map fusion under degraded tracking conditions.
