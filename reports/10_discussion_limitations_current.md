# Discussion and Current Limitations

## 1. Main Observation

The current RG-SSB + head method provides a defensible proof-of-concept result, not a final superiority claim. It improves the broader OTB subset and the expanded UAV123 subset, but corrected expanded NFS remains mixed/slightly negative.

Current anchors:

- Broader OTB average AUC change: `+0.033144`.
- Expanded UAV123 average AUC change: `+0.017405`.
- Corrected expanded NFS average AUC change: `-0.009638`.
- Corrected cross-benchmark failure-inspection average: `+0.001478`.

## 2. Positive Evidence

The broader OTB result is the strongest current evidence. A `+0.033144` average AUC change across 52 sequence-condition pairs indicates that the frozen-backbone RG-SSB + box head setup can improve robustness under the tested degradation protocol.

The expanded UAV123 result is also positive on average, with `+0.017405` AUC change across 64 pairs. This suggests that the method can transfer beyond OTB in some aerial-view sequences, but the result should be described cautiously because UAV123 remains subset-based.

## 3. Corrected NFS Finding

NFS is the main weakness. After correcting the annotation protocol and rerunning NFS with normalized aligned XYWH annotations, the expanded NFS average AUC change is `-0.009638`.

The NFS correction is important. Previous NFS rows used invalid XYXY-as-XYWH initialization and metric evaluation. Those rows are archived in `experiments/invalid_nfs_rows_before_xyxy_fix.csv` and old NFS overlays are superseded.

The corrected `nfs_cheetah` low-resolution row is near-neutral:

- Baseline AUC: `0.519832`.
- RG-SSB AUC: `0.516986`.

This replaces the previous invalid large-drop interpretation.

## 4. Failure Modes

Corrected NFS drift analysis shows that the largest NFS drops are not uniform. Terminal outcomes across 10 inspected corrected failure cases are:

- persistent RG-SSB-specific target loss: `5`
- sudden center jump: `3`
- shared tracker failure: `1`
- ambiguous: `1`

The most concerning pattern is persistent RG-SSB-specific target loss. Some cases start with a shared failure, then the baseline recovers while RG-SSB remains lost or diverges later. This suggests that the current feature-consistency setup may not sufficiently preserve target-vs-distractor separation under some NFS conditions.

## 5. Low-Resolution Weakness

Low resolution is the weakest current condition in corrected NFS. The expanded NFS low-resolution average is negative, and several top corrected failure cases are low-resolution cases. This is a direct risk for a restoration-oriented tracking claim, because low-resolution robustness is a central motivation.

## 6. Synthetic Degradation Limitations

The current degradation protocol is controlled but narrow:

- one degradation seed,
- medium severity only,
- three synthetic degradation types plus clean,
- no JPEG/compression condition in the current table,
- no multiple-severity robustness curve.

This limits the strength of any general degradation-robustness claim.

## 7. Benchmark Scope Limitations

The current results are based on selected subsets:

- 13 OTB sequences,
- 16 UAV123 sequences,
- 32 NFS sequences.

These are useful for development and failure analysis, but not full benchmark evidence. Additional complete benchmark evaluation would be needed for stronger claims.

## 8. Training Scope Limitations

The model is trained with LaSOT only and uses a frozen backbone. This makes the experiment clean and controlled, but it may limit transfer to NFS, where high-frame-rate sampling, fast motion, sports sequences, and small objects can differ strongly from the training distribution.

The trainable set is intentionally limited to `rgssb.*` and `box_head.*`. This is good for attribution but may restrict adaptation capacity.

## 9. Rejected Directions

Response consistency and target-region feature consistency are not part of Paper Freeze V1. Both were tested in local proof-of-concept settings and not retained.

The following are postponed:

- degradation token,
- template-guided scan,
- memory update,
- response fusion,
- new architecture modules.

## 10. Paper Claim Boundary

Safe claim:

> RG-SSB can be integrated into OSTrack and trained with a frozen backbone and trainable RG-SSB plus box head. Under selected synthetic degradation tests, the method improves broader OTB and expanded UAV123 subsets, while corrected NFS remains mixed/slightly negative.

Claims to avoid:

- state-of-the-art tracking,
- universal degradation robustness,
- consistent superiority across all benchmarks,
- final paper-scale proof of robustness.

## 11. Why Paper Freeze V1 Is Still Useful

Paper Freeze V1 is a defensible fallback because it has:

- a clear current best method,
- corrected NFS provenance,
- archived invalid NFS rows,
- paper-level result tables,
- claim traceability,
- known failure modes,
- explicit limitations.

The next ablation should only be kept if it improves the corrected failure modes without damaging OTB or UAV123.
