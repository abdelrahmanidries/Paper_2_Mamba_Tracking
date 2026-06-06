# Implementation Planning

## 1. Project goal

Prepare the minimal proof-of-concept for **Restoration-Guided Mamba Tracking**. The goal is to test whether restoration-oriented Mamba feature recovery can improve RGB template-search visual object tracking under image degradation.

This folder is for implementation planning only. It does not contain model code, training code, repository downloads, or experimental results.

## 2. Final selected idea

Final direction from the audit:

- **Title:** Tracking-Aware Restoration Mamba for Degradation-Robust RGB Template-Search Tracking
- **Acronym:** TAR-MambaTrack
- **Decision:** proceed with caution

The paper idea should stay narrow: adapt restoration-oriented Mamba to tracking-aware feature recovery under general RGB image degradation, and evaluate the effect through tracking accuracy, robustness drop, and response-map reliability.

## 3. Minimum viable model

The minimal proof-of-concept should include:

1. A base RGB single-object template-search tracker.
2. A synthetic degradation pipeline.
3. A minimal Restoration-Guided State Space Block, RG-SSB.
4. Standard tracking losses.
5. Clean-degraded feature consistency loss.
6. Response consistency loss if feasible.
7. Clean and degraded evaluation.
8. Comparisons against:
   - base tracker
   - base tracker with the same degradation training
   - base tracker + vanilla Mamba block
   - base tracker + external restoration preprocessing if feasible
   - proposed minimal RG-Mamba tracker

## 4. Suggested folder structure

Planned structure after implementation starts:

```text
implementation/
  README.md
  TODO.md
  minimal_poc_plan.md
  base_tracker_decision.md
  degradation_protocol_plan.md
  first_experiment_checklist.md

src/                         # later, only after base tracker is chosen
  degradations/              # synthetic degradation transforms
  models/                    # RG-SSB and tracker integration
  losses/                    # feature/response consistency losses
  evaluation/                # clean/degraded tracking evaluation
  visualization/             # response-map visualization

experiments/                 # later
  configs/
  logs/
  results/
```

The `src/` and `experiments/` folders should be created only when implementation begins.

## 5. What should be implemented first

1. Choose a base tracker.
2. Reproduce the clean baseline on a small dataset subset.
3. Implement the synthetic degradation pipeline.
4. Evaluate the baseline under clean and degraded settings.
5. Add a minimal RG-SSB block in one selected feature stage.
6. Add feature consistency loss.
7. Add response consistency loss only if response maps are easy to access.
8. Run the first ablations.

## 6. What should not be implemented yet

Do not implement these in the first proof-of-concept:

- Full Template-Guided Attentive Scan.
- Degradation-aware memory update.
- Complex multi-response fusion.
- Degradation prompt learning, unless the minimal RG-SSB result is promising.
- Contrastive target-distractor loss.
- Real degraded fine-tuning.
- Broad multi-dataset training.
- Full manuscript figures or final paper assets.

These modules remain optional until the minimal RG-SSB experiment shows a measurable tracking benefit under degradation.
