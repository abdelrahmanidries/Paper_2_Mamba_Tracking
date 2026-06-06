# Degradation Protocol Plan

## General protocol

The first degradation protocol should support:

1. Clean template + degraded search.
2. Degraded template + clean search.
3. Degraded template + degraded search.
4. Different degradations in template and search.
5. Mixed degradation.

All transforms should record parameters and random seeds for reproducibility.

The first proof-of-concept should start with medium severity before expanding to mild and severe levels.

## 1. Motion blur

Parameters:

- Blur kernel length.
- Blur angle.

Severity levels:

| level | suggested parameters |
|---|---|
| Mild | kernel length 5 to 7 |
| Medium | kernel length 9 to 13 |
| Severe | kernel length 15 to 21 |

Apply to:

- Search only for first test.
- Template only for asymmetry test.
- Both template and search for robustness test.

Why it matters:

Motion blur smears target edges and can flatten the response map, especially during fast motion.

## 2. Defocus blur

Parameters:

- Gaussian blur radius or disk blur radius.

Severity levels:

| level | suggested parameters |
|---|---|
| Mild | radius 1 to 2 |
| Medium | radius 3 to 4 |
| Severe | radius 5 to 7 |

Apply to:

- Search only.
- Template only.
- Both.

Why it matters:

Defocus blur removes local texture and weakens template-search feature similarity.

## 3. Gaussian noise

Parameters:

- Noise standard deviation.

Severity levels:

| level | suggested parameters |
|---|---|
| Mild | sigma 5 to 10 on 0-255 scale |
| Medium | sigma 15 to 25 |
| Severe | sigma 30 to 50 |

Apply to:

- Search only first.
- Both template and search for robustness.

Why it matters:

Noise corrupts local appearance and can create false response-map peaks.

## 4. Sensor noise

Parameters:

- Signal-dependent shot noise level.
- Optional read noise level.

Severity levels:

| level | suggested parameters |
|---|---|
| Mild | low shot/read noise |
| Medium | moderate shot/read noise |
| Severe | strong shot/read noise |

Apply to:

- Search only.
- Template and search for low-quality camera simulation.

Why it matters:

Sensor noise better approximates camera degradation than pure Gaussian noise and may affect channels unevenly.

## 5. Low resolution

Parameters:

- Downsample factor.
- Upsampling method.

Severity levels:

| level | suggested parameters |
|---|---|
| Mild | downsample 0.75x then resize back |
| Medium | downsample 0.5x then resize back |
| Severe | downsample 0.25x then resize back |

Apply to:

- Template only to test poor initial target detail.
- Search only to test low-quality current frame.
- Both for severe degraded tracking.

Why it matters:

Low resolution removes target details needed for classification and box regression.

## 6. JPEG compression

Parameters:

- JPEG quality factor.

Severity levels:

| level | suggested parameters |
|---|---|
| Mild | quality 60 to 80 |
| Medium | quality 30 to 50 |
| Severe | quality 10 to 25 |

Apply to:

- Search only.
- Template and search.

Why it matters:

Compression creates blocking artifacts and false textures that can confuse matching.

## 7. Low light

Parameters:

- Brightness factor.
- Gamma correction.
- Optional noise after darkening.

Severity levels:

| level | suggested parameters |
|---|---|
| Mild | brightness 0.7 to 0.8 |
| Medium | brightness 0.4 to 0.6 |
| Severe | brightness 0.2 to 0.35 with added noise |

Apply to:

- Search only.
- Both template and search.

Why it matters:

Low light reduces target visibility and response confidence. It should be evaluated as one degradation type, not as the entire robustness claim.

## 8. Mixed degradation

Parameters:

- Combination of two or more degradation types.
- Severity schedule.
- Order of operations.

Suggested first combinations:

- Motion blur + JPEG compression.
- Low resolution + Gaussian noise.
- Low light + sensor noise.
- Motion blur + low resolution + JPEG.

Severity levels:

| level | suggested parameters |
|---|---|
| Mild | two mild degradations |
| Medium | two medium degradations |
| Severe | one severe plus one or two medium degradations |

Apply to:

- Search only for first mixed test.
- Template and search after single-degradation tests are stable.

Why it matters:

Real videos often contain multiple degradations. Mixed degradation tests whether the model generalizes beyond single corruptions.

## First protocol recommendation

Start with:

1. Search-only medium motion blur.
2. Search-only medium Gaussian noise.
3. Search-only medium low resolution.
4. Search-only medium JPEG compression.
5. Search-only medium mixed degradation.

Then add:

1. Template-only degradation.
2. Template and search degradation.
3. Different template/search degradation types.
4. Mild and severe levels.
5. Low light and sensor noise.
