# RG-SSB HPC Feature-Consistency Lambda 0.02 Result Analysis

Inputs:

- `experiments/baseline_results.csv`
- `experiments/rgssb_featcons_lambda_sweep_comparison.csv`
- `implementation/rgssb_featcons_lambda_sweep_result_analysis.md`
- `implementation/hpc_featcons_lam002_plan.md`

## 1. Executive summary

HPC-scale lambda `0.02` improves over the original OSTrack baseline on overall average AUC: baseline `0.589546`, HPC `0.606303`, change `+0.016757`.
HPC-scale lambda `0.02` does not improve over the best local lambda `0.02` setup: local `0.613026`, HPC `0.606303`, change `-0.006723`.
This is stronger than local debugging evidence, but it remains limited to three OTB sequences and four synthetic conditions.

## 2. Technical status

- HPC training completed.
- HPC checkpoint saved.
- HPC evaluation completed.
- 12 HPC rows were added to `experiments/baseline_results.csv`.
- This is stronger than local debugging, but still not final paper-scale evidence.

## 3. Per-sequence summary

### Car1

Average HPC vs baseline AUC change on Car1: `+0.035188`. Average HPC vs local lambda `0.02` change: `-0.037818`.
HPC improves over baseline on: clean (+0.038245), motion_blur_medium (+0.036042), low_resolution_medium (+0.012939), gaussian_noise_medium (+0.053524).
HPC drops below baseline on: none.
HPC improves over local lambda `0.02` on: clean (+0.030683), motion_blur_medium (+0.026170).
HPC drops relative to local lambda `0.02` on: low_resolution_medium (-0.003708), gaussian_noise_medium (-0.204417).
This sequence supports the method against baseline but not consistently against the local lambda `0.02` run.

### David2

Average HPC vs baseline AUC change on David2: `+0.007062`. Average HPC vs local lambda `0.02` change: `+0.027440`.
HPC improves over baseline on: clean (+0.003227), motion_blur_medium (+0.067279).
HPC drops below baseline on: low_resolution_medium (-0.004057), gaussian_noise_medium (-0.038203).
HPC improves over local lambda `0.02` on: clean (+0.010786), motion_blur_medium (+0.078028), low_resolution_medium (+0.009716), gaussian_noise_medium (+0.011229).
HPC drops relative to local lambda `0.02` on: none.
This sequence supports the method and HPC scaling.

### Coke

Average HPC vs baseline AUC change on Coke: `+0.008022`. Average HPC vs local lambda `0.02` change: `-0.009791`.
HPC improves over baseline on: clean (+0.004492), motion_blur_medium (+0.021742), low_resolution_medium (+0.004151), gaussian_noise_medium (+0.001701).
HPC drops below baseline on: none.
HPC improves over local lambda `0.02` on: none.
HPC drops relative to local lambda `0.02` on: clean (-0.005920), motion_blur_medium (-0.005240), low_resolution_medium (-0.010751), gaussian_noise_medium (-0.017251).
This sequence supports the method against baseline but not consistently against the local lambda `0.02` run.

## 4. Per-condition average summary

| condition | average baseline AUC | average local lambda 0.02 AUC | average HPC lambda 0.02 AUC | local vs baseline | HPC vs baseline | HPC vs local |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| clean | 0.709564 | 0.713036 | 0.724886 | +0.003472 | +0.015321 | +0.011850 |
| motion_blur_medium | 0.469092 | 0.477794 | 0.510780 | +0.008702 | +0.041688 | +0.032986 |
| low_resolution_medium | 0.589005 | 0.594930 | 0.593349 | +0.005925 | +0.004344 | -0.001581 |
| gaussian_noise_medium | 0.590524 | 0.666344 | 0.596198 | +0.075820 | +0.005674 | -0.070146 |

## 5. Overall average summary

| setup | overall average AUC |
| --- | ---: |
| baseline | 0.589546 |
| local lambda 0.02 | 0.613026 |
| HPC lambda 0.02 | 0.606303 |

HPC average gain over baseline: `+0.016757`. HPC average gain/loss versus local lambda `0.02`: `-0.006723`. Local lambda `0.02` average gain over baseline: `+0.023480`.

## 6. Main finding

HPC scaling improves over the original baseline but does not clearly beat the best local lambda `0.02` setup.
The setup is ready for broader benchmark evaluation as a next validation step, not for final paper claims. Remaining weaknesses include limited sequence coverage, one degradation seed, and condition-specific regressions relative to the local lambda `0.02` run.

## 7. Recommended next experiment

Options:

- A. Evaluate the HPC checkpoint on more OTB sequences.
- B. Evaluate on UAV123 / NFS / TrackingNet if available.
- C. Run longer HPC training.
- D. Add response consistency again.
- E. Add new architecture modules.
- F. Prepare paper-level experiment plan.

Recommended fastest high-quality next step: **A. Evaluate the HPC checkpoint on more OTB sequences.**
This recommendation is based only on the parsed results. Broader evaluation is more informative than adding modules or reintroducing response consistency now.

## 8. What to postpone

- degradation token
- template-guided scan
- memory update
- response fusion
- final paper claims

## 9. Decision

Decision: **proceed to broader evaluation with current HPC checkpoint**.

## 10. Final detailed table

| sequence | condition | baseline AUC | local lambda 0.02 AUC | HPC lambda 0.02 AUC | HPC vs baseline change | HPC vs local change | best model | note |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| Car1 | clean | 0.575995 | 0.583557 | 0.614240 | +0.038245 | +0.030683 | hpc | HPC beats baseline; HPC beats local lambda 0.02; best=hpc |
| Car1 | motion_blur_medium | 0.157212 | 0.167084 | 0.193254 | +0.036042 | +0.026170 | hpc | HPC beats baseline; HPC beats local lambda 0.02; best=hpc |
| Car1 | low_resolution_medium | 0.214881 | 0.231528 | 0.227820 | +0.012939 | -0.003708 | local | HPC beats baseline; HPC below local lambda 0.02; best=local |
| Car1 | gaussian_noise_medium | 0.207270 | 0.465211 | 0.260794 | +0.053524 | -0.204417 | local | HPC beats baseline; HPC below local lambda 0.02; best=local |
| David2 | clean | 0.794439 | 0.786880 | 0.797666 | +0.003227 | +0.010786 | hpc | HPC beats baseline; HPC beats local lambda 0.02; best=hpc |
| David2 | motion_blur_medium | 0.549680 | 0.538931 | 0.616959 | +0.067279 | +0.078028 | hpc | HPC beats baseline; HPC beats local lambda 0.02; best=hpc |
| David2 | low_resolution_medium | 0.806258 | 0.792485 | 0.802201 | -0.004057 | +0.009716 | baseline | HPC below baseline; HPC beats local lambda 0.02; best=baseline |
| David2 | gaussian_noise_medium | 0.817542 | 0.768110 | 0.779339 | -0.038203 | +0.011229 | baseline | HPC below baseline; HPC beats local lambda 0.02; best=baseline |
| Coke | clean | 0.758259 | 0.768671 | 0.762751 | +0.004492 | -0.005920 | local | HPC beats baseline; HPC below local lambda 0.02; best=local |
| Coke | motion_blur_medium | 0.700384 | 0.727366 | 0.722126 | +0.021742 | -0.005240 | local | HPC beats baseline; HPC below local lambda 0.02; best=local |
| Coke | low_resolution_medium | 0.745875 | 0.760777 | 0.750026 | +0.004151 | -0.010751 | local | HPC beats baseline; HPC below local lambda 0.02; best=local |
| Coke | gaussian_noise_medium | 0.746759 | 0.765711 | 0.748460 | +0.001701 | -0.017251 | local | HPC beats baseline; HPC below local lambda 0.02; best=local |

## 11. Average table

| condition | average baseline AUC | average local lambda 0.02 AUC | average HPC lambda 0.02 AUC | HPC vs baseline change | HPC vs local change | decision note |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| clean | 0.709564 | 0.713036 | 0.724886 | +0.015321 | +0.011850 | HPC improves over baseline and local on average |
| motion_blur_medium | 0.469092 | 0.477794 | 0.510780 | +0.041688 | +0.032986 | HPC improves over baseline and local on average |
| low_resolution_medium | 0.589005 | 0.594930 | 0.593349 | +0.004344 | -0.001581 | HPC improves over baseline but trails local on average |
| gaussian_noise_medium | 0.590524 | 0.666344 | 0.596198 | +0.005674 | -0.070146 | HPC improves over baseline but trails local on average |

## Verification

- Parsed `experiments/baseline_results.csv` with Python.
- Created `experiments/rgssb_hpc_featcons_lam002_comparison.csv`.
- Created `implementation/rgssb_hpc_featcons_lam002_result_analysis.md`.
- Did not run OSTrack.
- Did not run training or evaluation.
- Did not modify datasets or `external/OSTrack`.

Uncertain fields:

- Each degradation condition uses one seed.
- The comparison covers only Car1, David2, and Coke.
- These are stronger than local debugging results but not final paper-scale evidence.
