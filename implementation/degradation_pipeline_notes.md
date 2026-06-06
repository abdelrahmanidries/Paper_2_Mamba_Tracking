# Degradation Pipeline Notes

## 1. What the degradation pipeline does

The synthetic degradation pipeline creates controlled RGB image-quality degradations for the minimal proof-of-concept. It supports single-image degradation and tracking-pair degradation for template/search experiments.

Implemented degradation types:

- motion blur
- defocus blur
- Gaussian noise
- sensor noise
- low resolution
- JPEG compression
- low light
- mixed degradation

Each transform returns:

- degraded RGB PIL image
- metadata with degradation type, severity, parameters, and seed

## 2. Why each degradation matters for tracking

Motion blur can smear target edges and flatten response peaks during fast motion. Defocus blur removes local texture and weakens template-search similarity. Gaussian noise and sensor noise corrupt local appearance and can create false response peaks. Low resolution removes target detail needed for classification and box regression. JPEG compression adds blocking artifacts and false textures. Low light reduces target visibility and confidence. Mixed degradation tests whether the method is robust beyond one isolated corruption.

## 3. How template/search pair modes support tracking experiments

The pipeline supports the tracking-specific settings from the proof-of-concept plan:

1. `clean`: clean template + clean search.
2. `search_only`: clean template + degraded search.
3. `template_only`: degraded template + clean search.
4. `both_same`: degraded template + degraded search with the same degradation type.
5. `both_different`: template and search degraded with different degradation types.

These modes matter because template-search tracking can fail when either the initial target template or the current search crop is degraded.

## 4. Why bounding boxes are unchanged

All degradations preserve image size. Low-resolution degradation temporarily downsamples the image but upsamples it back to the original dimensions. Because no transform changes the image geometry or final image dimensions, bounding-box coordinates remain valid.

This pipeline does not implement geometric transforms such as crop, rotation, scaling, or perspective changes.

## 5. How this supports the minimal proof-of-concept

The minimal proof-of-concept needs to compare:

- base tracker
- base tracker with the same degradation training
- base tracker + vanilla Mamba block
- base tracker + minimal RG-SSB
- external restoration preprocessing + tracker if feasible

This pipeline provides the degraded RGB inputs needed to test clean/degraded performance, robustness drop, template/search asymmetry, and response-map behavior before any full tracker modifications are added.

## 6. What is intentionally not implemented yet

Not implemented yet:

- dataset loader
- tracker model
- RG-SSB
- training loop
- evaluation loop
- response-map extraction
- base tracker integration
- data download scripts

Those should be added only after a base tracker is chosen.

## 7. First recommended usage

Generate previews:

```powershell
.\.venv\Scripts\python.exe scripts\preview_degradations.py
```

Run unit tests:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_degradation_pipeline.py
```

Apply one degradation to an image folder:

```powershell
.\.venv\Scripts\python.exe scripts\apply_degradation_to_folder.py --input_dir path\to\images --output_dir outputs\degraded_samples --type motion_blur --severity medium
```
