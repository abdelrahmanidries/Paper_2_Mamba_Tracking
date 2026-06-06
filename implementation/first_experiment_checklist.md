# First Experiment Checklist

## 1. Dataset subset

- [ ] Select one small standard RGB SOT dataset subset.
- [ ] Confirm annotation format.
- [ ] Confirm template/search crop generation.
- [ ] Confirm evaluation script works on clean data.
- [ ] Save the exact sequence list.

Recommended first candidates:

- OTB100 subset for quick debugging.
- LaSOT subset for stronger evidence once the pipeline runs.
- UAV123 subset if UAV degradation is the first target.

## 2. Baseline tracker run

- [ ] Choose base tracker.
- [ ] Install dependencies manually as needed.
- [ ] Load pretrained checkpoint if available.
- [ ] Run clean baseline.
- [ ] Save raw predictions.
- [ ] Save clean metrics.
- [ ] Record command/config.

## 3. Degradation pipeline run

- [ ] Apply medium motion blur.
- [ ] Apply medium Gaussian noise.
- [ ] Apply medium low resolution.
- [ ] Apply medium JPEG compression.
- [ ] Apply medium mixed degradation.
- [ ] Verify degraded frames visually.
- [ ] Save degradation parameters and seeds.

## 4. Degraded baseline evaluation

- [ ] Run baseline on degraded search-only setting.
- [ ] Run baseline on degraded template-only setting if supported.
- [ ] Run baseline on template-and-search degradation.
- [ ] Compute degradation robustness drop.
- [ ] Identify the most damaging degradation.

## 5. Proposed minimal module integrated

- [ ] Insert vanilla Mamba block baseline.
- [ ] Insert minimal RG-SSB block.
- [ ] Keep tracker head unchanged.
- [ ] Confirm forward pass works.
- [ ] Confirm feature shapes match.
- [ ] Confirm parameter count.
- [ ] Confirm runtime does not break tracking use.

## 6. Training run

- [ ] Train base tracker with same degradation augmentation.
- [ ] Train base + vanilla Mamba.
- [ ] Train base + RG-SSB with tracking loss.
- [ ] Add feature consistency loss.
- [ ] Add response consistency loss if response maps are available.
- [ ] Save checkpoints.
- [ ] Save logs.

## 7. Clean vs degraded result comparison

- [ ] Compare clean performance.
- [ ] Compare degraded performance.
- [ ] Compute robustness drop.
- [ ] Compare runtime/FPS.
- [ ] Check whether RG-SSB improves over same-augmentation baseline.
- [ ] Check whether RG-SSB improves over vanilla Mamba.

## 8. Response-map visualization

- [ ] Select 5 to 10 representative sequences.
- [ ] Save clean response maps.
- [ ] Save degraded baseline response maps.
- [ ] Save RG-SSB response maps.
- [ ] Compare peak sharpness if feasible.
- [ ] Compare distractor suppression qualitatively.
- [ ] Save failure cases.

## 9. Ablation summary

- [ ] Base tracker.
- [ ] Base + degradation training.
- [ ] Base + vanilla Mamba.
- [ ] Base + RG-SSB.
- [ ] RG-SSB without local enhancement.
- [ ] RG-SSB without channel selection.
- [ ] RG-SSB without feature consistency.
- [ ] RG-SSB without response consistency if used.
- [ ] External restoration preprocessing + tracker if feasible.

## Decision after first experiment

Continue if:

- RG-SSB improves degraded tracking over base and same-augmentation baseline.
- RG-SSB improves over vanilla Mamba.
- Response maps become sharper or more localized under degradation.
- Runtime overhead remains acceptable.

Revise before adding optional modules if:

- Same-augmentation baseline matches RG-SSB.
- Vanilla Mamba matches RG-SSB.
- External restoration preprocessing clearly dominates.
- Improvements appear only in clean tracking, not degraded tracking.
- Runtime overhead is too high.
