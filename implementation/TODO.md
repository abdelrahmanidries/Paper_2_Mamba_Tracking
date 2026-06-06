# Implementation TODO

## Stage 1: Set up base tracker

- [ ] Choose base tracker.
- [ ] Confirm license and code availability.
- [ ] Confirm pretrained checkpoint availability.
- [ ] Run tracker on a tiny sample sequence.
- [ ] Identify where template/search features are produced.
- [ ] Identify where response maps or classification maps are available.
- [ ] Record clean baseline command and environment.

## Stage 2: Create degradation pipeline

- [ ] Implement motion blur transform.
- [ ] Implement defocus blur transform.
- [ ] Implement Gaussian noise transform.
- [ ] Implement sensor noise transform.
- [ ] Implement low-resolution transform.
- [ ] Implement JPEG compression transform.
- [ ] Implement low-light transform.
- [ ] Implement mixed degradation transform.
- [ ] Support template-only degradation.
- [ ] Support search-only degradation.
- [ ] Support template-and-search degradation.
- [ ] Save degradation parameters for reproducibility.

## Stage 3: Reproduce clean baseline

- [ ] Select first dataset subset.
- [ ] Run base tracker on clean data.
- [ ] Record AUC/success, precision, and normalized precision if available.
- [ ] Confirm output format.
- [ ] Confirm evaluation scripts are stable.

## Stage 4: Evaluate baseline under degradation

- [ ] Run baseline with degraded search only.
- [ ] Run baseline with degraded template only.
- [ ] Run baseline with degraded template and search.
- [ ] Run baseline with mixed degradation.
- [ ] Compute degradation robustness drop.
- [ ] Identify the degradation settings where the baseline fails most clearly.

## Stage 5: Implement minimal RG-SSB

- [ ] Add vanilla Mamba block baseline.
- [ ] Add minimal RG-SSB block.
- [ ] Add local enhancement branch.
- [ ] Add channel selection branch.
- [ ] Add residual connection.
- [ ] Insert RG-SSB at one selected feature stage.
- [ ] Keep the tracking head unchanged.
- [ ] Confirm parameter count and runtime overhead.

## Stage 6: Train minimal proposed model

- [ ] Train base tracker with same degradation augmentation.
- [ ] Train base tracker + vanilla Mamba.
- [ ] Train base tracker + RG-SSB with tracking loss only.
- [ ] Train base tracker + RG-SSB with feature consistency loss.
- [ ] Add response consistency loss if response maps are available.
- [ ] Save checkpoints and config files.

## Stage 7: Run first ablations

- [ ] Base tracker.
- [ ] Base tracker + same degradation training.
- [ ] Base tracker + vanilla Mamba.
- [ ] Base tracker + RG-SSB.
- [ ] RG-SSB without local enhancement.
- [ ] RG-SSB without channel selection.
- [ ] RG-SSB without feature consistency.
- [ ] RG-SSB without response consistency, if used.
- [ ] External restoration preprocessing + tracker, if feasible.

## Stage 8: Generate response-map visualizations

- [ ] Select clean/degraded paired examples.
- [ ] Save baseline response maps.
- [ ] Save RG-SSB response maps.
- [ ] Compare peak sharpness or peak-to-sidelobe ratio if feasible.
- [ ] Save qualitative tracking boxes.
- [ ] Identify failure cases.

## Stage 9: Decide whether to add optional modules

- [ ] Check whether RG-SSB improves degraded tracking beyond same-augmentation baseline.
- [ ] Check whether RG-SSB improves over vanilla Mamba.
- [ ] Check whether external restoration preprocessing is weaker, similar, or stronger.
- [ ] If core result is promising, consider degradation prompt.
- [ ] If response maps remain weak, consider restoration-guided response fusion.
- [ ] If target-relevant tokens are poorly localized, consider Template-Guided Attentive Scan.
- [ ] If long-sequence drift appears, consider degradation-aware memory.
