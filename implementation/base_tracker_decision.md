# Base Tracker Decision

## Decision criteria

The first proof-of-concept needs a base tracker that is:

- RGB single-object tracking.
- Template-search based.
- Practical to reproduce.
- Easy to modify at the feature level.
- Able to expose response maps or classification maps.
- Compatible with clean/degraded template-search evaluation.
- Not so close to the proposed idea that novelty becomes confusing.

## Option 1: OSTrack-style one-stream tracker

| criterion | assessment |
|---|---|
| Implementation difficulty | Medium. Requires understanding the feature backbone and tracking head, but the architecture is widely used and suitable for modification. |
| Template-search compatibility | High. One-stream template-search tracking is directly aligned with the target problem. |
| Feature-level restoration compatibility | High. RG-SSB can be inserted into feature stages or interaction blocks. |
| Response-map analysis compatibility | High if classification/center maps are accessible. |
| Availability of baselines | High. OSTrack-style trackers are common reference points. |
| Novelty confusion risk | Low to medium. It is not itself a restoration Mamba tracker. |
| Recommended or not | **Recommended for first proof-of-concept.** |

Reason:

An OSTrack-style tracker provides a strong RGB template-search baseline while keeping the method focused on restoration-guided feature recovery.

## Option 2: MixFormer-style tracker

| criterion | assessment |
|---|---|
| Implementation difficulty | Medium to high. The architecture may be more complex to modify cleanly. |
| Template-search compatibility | High. It is relevant to template-search tracking. |
| Feature-level restoration compatibility | Medium. Feature insertion is possible but may require more careful integration. |
| Response-map analysis compatibility | Medium to high, depending on code structure. |
| Availability of baselines | High. It is a strong standard tracker baseline. |
| Novelty confusion risk | Low. It is not a Mamba/restoration tracker. |
| Recommended or not | Useful as a comparison; not the first implementation choice. |

Reason:

MixFormer-style tracking is useful for benchmarking, but an OSTrack-style base is likely simpler for the first RG-SSB integration.

## Option 3: Siamese-style tracker

| criterion | assessment |
|---|---|
| Implementation difficulty | Low to medium. Siamese trackers can be simpler and response-map friendly. |
| Template-search compatibility | High. Siamese tracking directly uses template-search matching. |
| Feature-level restoration compatibility | Medium. RG-SSB can be inserted into feature branches, but the baseline may be less aligned with current SOTA one-stream trackers. |
| Response-map analysis compatibility | High. Correlation response maps are often explicit. |
| Availability of baselines | Medium to high. Many variants exist. |
| Novelty confusion risk | Low. |
| Recommended or not | Good fallback if response-map access is the top priority. |

Reason:

A Siamese-style tracker may be easier for response-map analysis, but the first proof-of-concept should preferably use a stronger modern base tracker if reproducible.

## Option 4: Existing Mamba tracker, if code is available

| criterion | assessment |
|---|---|
| Implementation difficulty | Medium to high. Code availability and reproducibility are uncertain. |
| Template-search compatibility | Varies by tracker. Some are SOT, some MOT, some multimodal. |
| Feature-level restoration compatibility | Medium. Adding RG-SSB may be technically natural but can make novelty confusing. |
| Response-map analysis compatibility | Varies. |
| Availability of baselines | Uncertain. |
| Novelty confusion risk | High. It may be unclear whether gains come from restoration-guided Mamba or existing Mamba tracking design. |
| Recommended or not | Not recommended as the first base. Use later as a comparison if runnable. |

Reason:

Starting from a Mamba tracker may blur the core ablation. A non-Mamba base plus vanilla Mamba and RG-SSB controls is cleaner.

## Option 5: InvTrack-style tracker, if available

| criterion | assessment |
|---|---|
| Implementation difficulty | Medium to high. Code availability and reproducibility must be checked. |
| Template-search compatibility | High. InvTrack directly addresses degradation-invariant RGB template-search tracking. |
| Feature-level restoration compatibility | Medium. It is a strong degradation baseline, but modifying it may blur the distinction from InvTrack. |
| Response-map analysis compatibility | High, based on its response-map fusion emphasis. |
| Availability of baselines | Uncertain. |
| Novelty confusion risk | High. The proposed method may look like InvTrack plus Mamba. |
| Recommended or not | Essential comparison if runnable; not recommended as the first base. |

Reason:

InvTrack should be a threat baseline, not the first implementation foundation, unless no other reproducible tracker is available.

## Recommendation

Recommended first base tracker:

- **OSTrack-style one-stream RGB template-search tracker**

Fallback:

- Siamese-style tracker if response-map access or implementation simplicity becomes more important than SOTA strength.

Not recommended as first base:

- Existing Mamba tracker.
- InvTrack-style tracker.

Required first controls:

1. Base tracker.
2. Base tracker + same degradation training.
3. Base tracker + vanilla Mamba block.
4. Base tracker + minimal RG-SSB.
5. External restoration preprocessing + tracker if feasible.
