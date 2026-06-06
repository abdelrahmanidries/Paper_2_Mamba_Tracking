# Real Sample Degradation Test Notes

## 1. Why this test is needed

Unit tests verify that the degradation pipeline runs and preserves RGB image size, but real sample images are needed to check whether the degradation strength looks plausible for visual tracking. This step should happen before connecting the pipeline to a base tracker or dataset wrapper.

The goal is visual inspection and pipeline sanity checking. It does not produce tracking results.

## 2. What should be visually checked

Check these properties in `outputs/real_sample_degradation/` and `outputs/tracking_pair_degradation/`:

- Motion blur direction and strength should be visible but not destroy every target at mild severity.
- Defocus blur should remove detail without changing image geometry.
- Gaussian noise should visibly corrupt pixels, especially at medium and severe levels.
- Sensor noise should look different from simple Gaussian noise because it is signal-dependent.
- Low-resolution degradation should reduce detail but preserve final image size.
- JPEG compression should show blocking or texture artifacts, especially at severe quality.
- Low-light degradation should reduce brightness/contrast and add mild noise.
- Mixed degradation should combine effects without becoming unusable in every medium-severity case.
- Template/search pair modes should clearly show which branch was degraded.

## 3. What would indicate the pipeline is broken

The pipeline should be treated as broken if:

- Output image size differs from the original degraded image size.
- Output images are not RGB.
- Mild degradation is already visually extreme.
- Severe degradation has no visible effect.
- Mixed degradation produces all-black/all-white outputs.
- JPEG outputs cannot be opened.
- Metadata JSONL files are missing or malformed.
- Template-only mode degrades the search image.
- Search-only mode degrades the template image.
- Both-different mode uses the same degradation for both images.

## 4. What to adjust if degradation is too weak or too severe

If degradation is too weak:

- Increase motion blur kernel length.
- Increase Gaussian noise sigma.
- Lower JPEG quality.
- Lower low-resolution scale factor.
- Lower low-light brightness and contrast factors.

If degradation is too severe:

- Reduce motion blur kernel length.
- Reduce noise sigma or read-noise values.
- Raise JPEG quality.
- Increase low-resolution scale factor.
- Make mixed degradation use fewer transforms or lower severity.

Parameter tuning should be done before tracker training so degradation strength is consistent across baselines.

## 5. How this supports the first tracker experiment

The first tracker experiment needs clean/degraded comparisons for:

- base tracker
- base tracker with degradation training
- base tracker + vanilla Mamba
- base tracker + minimal RG-SSB
- external restoration preprocessing if feasible

Real-sample degradation testing confirms that the synthetic corruption pipeline is visually plausible before it is used inside a dataset wrapper or training loop. It also helps identify which degradations should be used first for the minimal proof-of-concept.

## 6. What remains intentionally unimplemented

This step does not implement:

- tracker model
- RG-SSB
- dataset loader
- training loop
- evaluation loop
- response-map extraction
- repository download scripts
