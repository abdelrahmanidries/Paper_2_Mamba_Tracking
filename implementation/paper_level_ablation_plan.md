# Paper-Level Ablation Plan

## Required Ablations

| ablation | status | purpose | run now? |
| --- | --- | --- | --- |
| OSTrack baseline | already used | Anchor all robustness comparisons. | Run missing benchmark rows only |
| RG-SSB disabled | equivalent to OSTrack baseline for current integration | Confirms default behavior is unchanged. | No separate run needed unless reviewer asks |
| RG-SSB enabled untrained | partial smoke evidence only | Checks whether adding RG-SSB without training helps or hurts. | Do not run yet |
| RG-SSB-only training | partial/local evidence done; insufficient | Tests whether RG-SSB alone can adapt. | Do not prioritize |
| RG-SSB + head training | local evidence done | Shows head adaptation is needed. | Keep as design-support ablation |
| global feature consistency lambda `0.02` | done locally and HPC-scaled | Current best objective. | Main method |
| response consistency | done locally; rejected | Tests response-map alignment. | Do not run further now |
| target-region consistency | done locally; rejected against global `0.02` | Tests target-focused feature alignment. | Do not run further now |

## Optional Ablations

| ablation | status | purpose | priority |
| --- | --- | --- | --- |
| lambda `0.05` | done locally | Original feature-consistency weight. | Low |
| lambda `0.10` | done locally | Stronger feature-consistency weight. | Low |
| balanced degradation probability `0.5` | done locally; weaker than fully degraded | Tests clean/degraded balance. | Low |
| longer HPC training | future | Tests whether current objective scales with more epochs/samples. | Medium if NFS remains negative |
| more degradation types | future | Tests compression or additional corruption robustness. | Medium after core table is stable |
| different severities | future | Tests robustness curve rather than one medium severity. | Medium/high for paper tables |

## Do Not Run Yet

Do not run new architecture ablations yet:

- degradation token
- template-guided scan
- memory update
- response fusion
- new restoration modules

These are postponed because the current evidence still needs benchmark-level completion for the minimal RG-SSB + head setup.

## Immediate Ablation Policy

For the next paper-level stage, use only:

- Original OSTrack baseline.
- Current best RG-SSB + head global feature consistency lambda `0.02`.
- Existing local ablation results for explanation.

Only add more ablations if a reviewer-facing table needs them or if broader benchmark results contradict the current evidence.

