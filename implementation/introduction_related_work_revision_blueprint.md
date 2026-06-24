# Introduction and Related Work Revision Blueprint

No manuscript files were modified. This blueprint now uses the authorship-structure-aware style audit.

## Introduction Plan

| Current paragraph | Current function | Missing element | Group-weighted recommendation | Corpus support | Citations needed |
|---|---|---|---|---|---|
| P1 | Broad tracking/degradation/MambaIR setup. | Practical tracking failure chain and prior tracking context are compressed. | Split into application/task paragraph and degradation-specific tracking-feature paragraph. | Group A/B restoration papers for degradation motivation; Group C tracking papers for terminology. | OSTrack, degradation tracking, MambaIR/MambaIRv2. |
| P2 | Caveat, InvTrack, gap, and method preview. | Too many roles in one paragraph. | Separate prior-work boundary, exact missing intersection, and controlled method preview. | Group A/B limitation-to-method transitions. | InvTrack, Mamba tracking papers, MambaIR papers. |
| P3 | Contributions. | Contributions mix method, protocol, provenance, efficiency, and claim boundary. | Use 3-4 testable contribution bullets modeled after Group A/B IEEE Transactions papers. | `T1_2021_TBC_UPDRESNN`, `T1_2025_TGRS_UADIFF`, `T1_2023_TAI_THREE_PRIOR_SR`. | Claim audit and traceability CSV. |

## Related Work Plan

| Needed subsection | Recommendation | Style source | Technical source need |
|---|---|---|---|
| Template-search RGB tracking | Method-family overview ending with OSTrack boundary. | Group A/B method-family organization; Group C tracking terminology. | OSTrack and representative template-search trackers. |
| Mamba/state-space tracking | Organize by functional use, not chronology. | Group A/B prior-family limitation pattern. | Existing Mamba tracker cards/matrices. |
| Degradation-robust tracking | Put InvTrack as direct novelty boundary. | Cautious limitation framing from Group A/B. | InvTrack and degradation-robust tracking sources. |
| Restoration-oriented Mamba | Explain restoration feature recovery and non-tracking objective. | Alireza-centered restoration papers plus MambaIR evidence. | MambaIR, MambaIRv2. |
| Position of present work | Synthesize missing intersection without overclaiming. | Group A/B final bridge pattern. | Evidence matrices and claim audit. |

## Bibliography Note

Current `references.bib` contains only the existing core entries. Later rewrite must add any new Mamba-tracking, RGB-T tracking, or supervisor-corpus citation before use.
