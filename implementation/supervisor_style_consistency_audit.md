# Supervisor Style Consistency Audit

This audit uses author-team structure as a proxy for likely supervisor-editing consistency. It does not claim that any named author wrote a section unless an explicit contribution statement says so. No such CRediT/writing statement was found in the local metadata or extracted section text used here.

## Group A Papers

Operational proxy: exactly one non-supervisor author plus both supervisors. This is not a confirmed student role unless separately documented.

- `T1_2024_TMRB_MIS_FMR`: A Very Fast and Robust Method for Refinement of Putative Matches of Features in MIS Images for Robotic-Assisted Surgery (2024, IEEE Transactions on Medical Robotics and Bionics)
- `T1_2023_APPLINT_EDGE`: A low-complexity residual deep neural network for image edge detection (2023, Applied Intelligence)
- `T1_2025_JBHI_ALZ_CNN`: A Lightweight Deep Convolutional Neural Network Extracting Local and Global Contextual Features for the Classification of Alzheimer's Disease Using Structural MRI (2025, IEEE Journal of Biomedical and Health Informatics)
- `T1_2024_MULTISYS_REFINERHASH`: RefinerHash: a new hashing-based re-ranking technique for image retrieval (2024, Multimedia Systems)
- `T1_2023_TAI_THREE_PRIOR_SR`: Ultralight-Weight Three-Prior Convolutional Neural Network for Single Image Super Resolution (2023, IEEE Transactions on Artificial Intelligence)
- `T1_2021_TCI_SRNSSI`: SRNSSI: A Deep Light-Weight Network for Single Image Super Resolution Using Spatial and Spectral Information (2021, IEEE Transactions on Computational Imaging)
- `T1_2021_TBC_UPDRESNN`: UPDResNN: A Deep Light-Weight Image Upsampling and Deblurring Residual Neural Network (2021, IEEE Transactions on Broadcasting)
- `T1_2019_TIP_TCHEBICHEF_DENOISING`: Tchebichef and Adaptive Steerable-Based Total Variation Model for Image Denoising (2019, IEEE Transactions on Image Processing)
- `T2_AS2024_PATHOWAVE`: PathoWAve: A Deep Learning-based Weight Averaging Method for Improving Domain Generalization in Histopathology Images (2024, arXiv preprint)
- `T2_AS2015_MSAINDELFR`: MSAIndelFR: a scheme for multiple protein sequence alignment using information on indel flanking regions (2015, BMC Bioinformatics)

## Group B Papers

Alireza Esmaeilzehi plus both supervisors, excluding papers already assigned primarily to Group A.

- `T1_2024_TBC_DMML`: DMML: Deep Multi-Prior and Multi-Discriminator Learning for Underwater Image Enhancement (2024, IEEE Transactions on Broadcasting)
- `T1_2025_TGRS_UADIFF`: UADiff: A Deep Underwater Image Enhancement Network Using Generative Diffusion Prior and Uncertainty-Aware Learning (2025, IEEE Transactions on Geoscience and Remote Sensing)
- `T1_2024_VISCOMP_HIGHBOOSTNET`: HighBoostNet: a deep light-weight image super-resolution network using high-boost residual blocks (2024, The Visual Computer)

## Group C Papers

- `T1_2026_TIP_MSD_RGBT`: A Multi-Level Self-Distillation-Based Unified Tracker for Efficient RGB-T Tracking (2026, IEEE Transactions on Image Processing)
- `T1_2025_ICIP_HFDAE_RGBT`: Adaptive Hierarchical Feature Difference Auto-Encoder for Robust RGB-T Object Tracking (2025, IEEE International Conference on Image Processing)
- `T1_2026_TPAMI_ACLI`: ACLI: A CNN Pruning Framework Leveraging Adjacent Convolutional Layer Interdependence and gamma-Weakly Submodularity (2026, IEEE Transactions on Pattern Analysis and Machine Intelligence)
- `T2_AS2018_VARIATIONAL_MIXED_NOISE`: A Variational Step for Reduction of Mixed Gaussian-Impulse Noise from Images (2018, arXiv preprint / ICECE paper)

## Group D Papers

- `T1_2023_SPL_DPAN`: DPAN: A Deep Light-Weight Attention-Based Image Super Resolution Network Using Multi-Dimensional Filter Design Technique (2023, IEEE Signal Processing Letters)
- `T2_AH2020_R_SPATIOGRAM_TRACKING`: Applying R-spatiogram in Object Tracking for Occlusion Handling (2020, Signal & Image Processing: An International Journal)
- `T2_AS2014_EURASIP_ECHO`: Single-channel acoustic echo cancellation in noise based on gradient-based adaptive filtering (2014, EURASIP Journal on Audio Speech and Music Processing)
- `T2_AS2010_EURASIP_CEPSTRUM`: A Ramp Cosine Cepstrum Model for the Parameter Estimation of Autoregressive Systems at Low SNR (2010, EURASIP Journal on Advances in Signal Processing)
- `T2_SW2019_HEARING_AIDS`: Sound Quality Improvement for Hearing Aids in Presence of Multiple Inputs (2019, Circuits Systems and Signal Processing)
- `T2_SW2015_COSINE_TCHEBICHEF`: A Comparison of Integer Cosine and Tchebichef Transforms for Image Compression Using Variable Quantization (2015, Journal of Signal and Information Processing)
- `T2_SW2013_FRONTIERS_SYNAPTIC`: Inferring trial-to-trial excitatory and inhibitory synaptic inputs from membrane potential using Gaussian mixture Kalman filtering (2013, Frontiers in Computational Neuroscience)

## Consistency Findings

- within Group A: mean similarity 0.4051 (weakly consistent)
- within Group B: mean similarity 0.5598 (weakly consistent)
- within Group C: mean similarity 0.4250 (weakly consistent)
- within Group D: mean similarity 0.4949 (weakly consistent)
- Group A versus Group B: mean similarity 0.4666 (weakly consistent)
- Group A/B versus Group C: mean similarity 0.4242 (weakly consistent)
- core groups versus Group D: mean similarity 0.3766 (weakly consistent)

Group A is the most internally consistent high-confidence style group because it combines the requested one-author-plus-supervisors structure with repeated IEEE-style contribution and motivation patterns. Group B is also strongly useful, especially for restoration/super-resolution/enhancement phrasing, but includes more team/venue variation. Group C should confirm technical organization and terminology, not define the house style. Group D should be treated as secondary or excluded for rewrite guidance.

## Highly Consistent Pairs

### Within Group A

- `T1_2025_JBHI_ALZ_CNN` / `T1_2021_TCI_SRNSSI`: 0.7788 (moderately consistent)
- `T1_2024_TMRB_MIS_FMR` / `T2_AS2024_PATHOWAVE`: 0.6149 (moderately consistent)
- `T1_2025_JBHI_ALZ_CNN` / `T1_2021_TBC_UPDRESNN`: 0.6037 (moderately consistent)
- `T1_2021_TCI_SRNSSI` / `T1_2021_TBC_UPDRESNN`: 0.6027 (moderately consistent)
- `T1_2019_TIP_TCHEBICHEF_DENOISING` / `T2_AS2024_PATHOWAVE`: 0.6021 (moderately consistent)

### Within Group B

- `T1_2024_TBC_DMML` / `T1_2025_TGRS_UADIFF`: 0.7727 (moderately consistent)
- `T1_2024_TBC_DMML` / `T1_2024_VISCOMP_HIGHBOOSTNET`: 0.4667 (weakly consistent)
- `T1_2025_TGRS_UADIFF` / `T1_2024_VISCOMP_HIGHBOOSTNET`: 0.4399 (weakly consistent)

### Group A versus Group B

- `T1_2024_TBC_DMML` / `T1_2021_TCI_SRNSSI`: 0.6750 (moderately consistent)
- `T1_2025_TGRS_UADIFF` / `T1_2021_TCI_SRNSSI`: 0.6743 (moderately consistent)
- `T1_2025_TGRS_UADIFF` / `T1_2021_TBC_UPDRESNN`: 0.6260 (moderately consistent)
- `T1_2025_TGRS_UADIFF` / `T1_2025_JBHI_ALZ_CNN`: 0.5960 (moderately consistent)
- `T1_2024_TBC_DMML` / `T1_2021_TBC_UPDRESNN`: 0.5904 (moderately consistent)

## Alireza-Specific Analysis

The Alireza subset is internally coherent in how it introduces image degradation/restoration tasks: practical image-quality problem, prior lightweight/restoration methods, limitation in feature richness or degradation modeling, then a module-level proposal. It is more consistent than the full corpus because most papers share image restoration or super-resolution framing. Differences arise between short IEEE SPL format, full IEEE Transactions papers, and Springer journal formatting.

## One-Student-Plus-Supervisors Analysis

Group A papers form the strongest operational proxy for a stable student-supervisor writing/editing pattern. Their introductions usually move from application context to technical challenge, then prior-method limitations, then a proposed compact architecture or regularizer. Contribution statements are clearest in IEEE Transactions papers and less explicit in some Springer/open venues.

## Strongest Introduction Models

- `T1_2023_TAI_THREE_PRIOR_SR`
- `T1_2025_TGRS_UADIFF`
- `T1_2021_TBC_UPDRESNN`

## Strongest Related Work Models

- `T1_2025_TGRS_UADIFF`
- `T1_2024_TBC_DMML`
- `T1_2021_TCI_SRNSSI`

## Strongest Tracking-Domain Models

- `T1_2026_TIP_MSD_RGBT`: strongest technical organization model for tracking, but Group C due to larger team.
- `T1_2025_ICIP_HFDAE_RGBT`: useful tracking terminology and fusion positioning, but conference format and Group C.
- `T2_AH2020_R_SPATIOGRAM_TRACKING`: tracking topic, but Group D and not a primary style model.

## Style-Only Evidence

Use biomedical, pruning, retrieval, and older Tier 2 papers only for rhetorical structure, not technical claims in Paper_2.

## Recommended Exclusions From Rewrite Guide

- `T1_2023_SPL_DPAN`: DPAN: A Deep Light-Weight Attention-Based Image Super Resolution Network Using Multi-Dimensional Filter Design Technique (2023, IEEE Signal Processing Letters)
- `T2_AH2020_R_SPATIOGRAM_TRACKING`: Applying R-spatiogram in Object Tracking for Occlusion Handling (2020, Signal & Image Processing: An International Journal)
- `T2_AS2010_EURASIP_CEPSTRUM`: A Ramp Cosine Cepstrum Model for the Parameter Estimation of Autoregressive Systems at Low SNR (2010, EURASIP Journal on Advances in Signal Processing)
- `T2_AS2014_EURASIP_ECHO`: Single-channel acoustic echo cancellation in noise based on gradient-based adaptive filtering (2014, EURASIP Journal on Audio Speech and Music Processing)
- `T2_SW2013_FRONTIERS_SYNAPTIC`: Inferring trial-to-trial excitatory and inhibitory synaptic inputs from membrane potential using Gaussian mixture Kalman filtering (2013, Frontiers in Computational Neuroscience)
- `T2_SW2015_COSINE_TCHEBICHEF`: A Comparison of Integer Cosine and Tchebichef Transforms for Image Compression Using Variable Quantization (2015, Journal of Signal and Information Processing)
- `T2_SW2019_HEARING_AIDS`: Sound Quality Improvement for Hearing Aids in Presence of Multiple Inputs (2019, Circuits Systems and Signal Processing)
