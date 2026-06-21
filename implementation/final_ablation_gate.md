# Final Ablation Gate: Target-versus-Distractor Response-Margin Loss

## 1. Purpose

The only allowed future experiment after Paper Freeze V1 is a minimal target-versus-distractor response-margin loss. The goal is to test whether persistent RG-SSB-specific target loss on corrected NFS can be reduced without adding new architecture modules.

This is a gated ablation, not a new method direction unless it passes all criteria below.

## 2. Fixed Base Method

The ablation must start from Paper Freeze V1:

- OSTrack + RG-SSB + box head.
- Backbone frozen.
- Trainable groups: `rgssb.*` and `box_head.*`.
- Global clean/degraded feature consistency lambda `0.02`.
- Response consistency disabled.
- Target-region consistency disabled.
- No degradation token.
- No template-guided scan.
- No memory update.
- No response fusion module.

## 3. Proposed Ablation

Add a loss that encourages target response to remain above distractor/background response by a margin. The loss should be computed from existing response/score maps and ground-truth target position. It must not add a new architecture module.

Candidate form:

```text
L_total = L_track + lambda_feat * L_global_feat + lambda_margin * L_target_vs_distractor_margin
```

The margin loss should penalize cases where high non-target responses approach or exceed the target-region response.

## 4. Local Proceed Gate

Proceed from local debug to HPC only if all conditions hold:

- Config loads.
- Verifier passes.
- One real-batch forward/backward pass completes.
- Trainable parameters remain `rgssb.*` and `box_head.*`.
- Backbone remains frozen.
- Local three-sequence average improves over current global lambda `0.02`.
- No severe clean collapse.

Severe clean collapse means clean-condition average AUC drops by more than `0.02` in the local debug subset.

## 5. HPC Keep Gate

Keep the ablation only if all conditions hold:

- Corrected expanded NFS improves meaningfully over Paper Freeze V1.
- Broader OTB average AUC decreases by no more than `0.005`.
- Expanded UAV123 average AUC decreases by no more than `0.005`.
- Overall cross-benchmark average improves.
- Persistent RG-SSB-specific target-loss cases decrease below the current count of `5`.

Current Paper Freeze V1 anchors:

- broader OTB: `+0.033144`.
- expanded UAV123: `+0.017405`.
- corrected expanded NFS: `-0.009638`.
- corrected cross-benchmark failure-inspection average: `+0.001478`.
- persistent RG-SSB-specific target-loss cases: `5`.

## 6. Reject Gate

Reject the ablation and return to Paper Freeze V1 if any condition holds:

- Corrected NFS does not improve.
- Broader OTB drops by more than `0.005` AUC.
- Expanded UAV123 drops by more than `0.005` AUC.
- Overall cross-benchmark average does not improve.
- Persistent RG-SSB-specific target-loss cases do not decrease.
- Clean condition collapses.
- The loss requires new architecture modules.
- The verifier shows backbone parameters became trainable.

If rejected, make no architecture change and use Paper Freeze V1 as the fallback paper version.

## 7. Strict Time Budget

Suggested maximum time budget:

- 1 session for implementation.
- 1 session for verifier and local debug run.
- 1 HPC cycle for gated training/evaluation.
- 1 session for analysis.

Stop immediately if the verifier fails after two focused fixes, if a real-batch backward pass is unstable, or if local clean performance collapses.

## 8. Required Outputs If Run

If the ablation proceeds, create:

- one config,
- one experiment-cycle config,
- one verifier,
- one local comparison CSV/report,
- one HPC comparison CSV/report only if local gate passes,
- one updated drift-onset comparison if HPC gate is reached.

Do not modify Paper Freeze V1 artifacts unless the ablation passes all keep gates.

## 9. Decision Rule

Default decision is Paper Freeze V1. The margin ablation must earn its way into the paper by passing the hard gates. Otherwise, it is rejected and documented as a negative ablation.
