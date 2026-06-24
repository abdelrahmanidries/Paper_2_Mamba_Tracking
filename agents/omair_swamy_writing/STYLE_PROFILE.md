# Omair-Swamy Style Profile

This profile is derived from verified local metadata and style summaries, not from copied corpus prose.

## Evidence Inputs

- `implementation/supervisor_style_high_confidence_core.md`
- `implementation/supervisor_style_consistency_audit.md`
- `implementation/ahmad_swamy_ieee_writing_style_guide.md`
- `implementation/introduction_related_work_revision_blueprint.md`
- `experiments/supervisor_style_authorship_structure.csv`
- `experiments/supervisor_style_group_summary.csv`
- `experiments/supervisor_style_features.csv`
- `experiments/supervisor_style_corpus_verified_manifest.csv`
- `scripts/check_supervisor_corpus_phrase_overlap.py`

## Corpus Weighting

| Corpus group | Use | Weight |
|---|---:|---:|
| Alireza-centered core | primary restoration/enhancement style, motivation, limitation-to-method flow | 1.00 |
| Tchebichef and Alzheimer papers | strong secondary structure and IEEE Transactions cadence | 0.75 |
| RGB-T tracking papers | tracking organization and terminology | 1.00 technical organization, 0.45 style |
| Other Group C | secondary structure only | at most 0.25 |
| Group D | excluded | 0.00 |

## Stable Patterns

- Start from an application or task pressure, then narrow to the technical obstacle.
- Acknowledge prior progress before stating unresolved limitations.
- Organize Related Work by method family or functional role rather than chronology.
- Present the proposed method as a bounded response to a specific limitation.
- Keep novelty claims cautious and experimentally testable.
- Use contribution lists only when each item corresponds to a verifiable technical deliverable.

## Paragraph Role Sequence

Typical Introduction:

1. Application/task importance.
2. Core technical challenge.
3. Prior method families and progress.
4. Narrow limitation or missing intersection.
5. Proposed method summary.
6. Concrete contributions.

Typical Related Work:

1. Category definition.
2. Representative methods and mechanisms.
3. Strengths and established progress.
4. Remaining limitation tied to the current paper.
5. Position of the present work without overclaiming.

## Tone Constraints

- Prefer measured terms: `effective`, `robust`, `compact`, `feature-discriminative`, `degradation-aware`, `experimentally evaluated`.
- Avoid unsupported superlatives: `first`, `novel`, `unprecedented`, `significantly superior`, unless directly proven.
- Avoid vague gap language. Every gap must name the missing mechanism, task setting, and testable consequence.
- Use `not reported` when a source does not discuss a property.

## Domain Transfer Rules

Restoration papers may guide motivation around degradation, image quality, and feature recovery. They cannot be used to claim tracking behavior unless the tracking evidence also supports it.

Tracking papers may guide technical organization, localization, template-search terminology, robustness framing, and evaluation framing. They should not dominate style when they come from larger Group C teams.
