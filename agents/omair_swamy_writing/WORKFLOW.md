# Workflow

## Common Preflight

1. Read the request YAML.
2. Validate mode, section type, evidence inputs, output target, and constraints.
3. Confirm that manuscript editing is not requested unless explicitly authorized.
4. Load style profile and relevant section playbook.
5. Confirm that evidence items are sufficient for the requested claims.

## WRITE_FROM_SCRATCH

1. Validate request.
2. Create a paragraph-role outline.
3. Create a claim-to-evidence map.
4. Draft the section using only supplied evidence.
5. Run citation audit.
6. Run claim audit.
7. Run style scoring.
8. Run phrase-overlap audit.
9. Return the draft and revision report.

Required report sections:

- `Paragraph-role outline`
- `Claim-to-evidence map`
- `Draft`
- `Citation audit`
- `Claim audit`
- `Style score`
- `Phrase-overlap audit`
- `Uncertain fields`
- `Recommended next edits`

## REWRITE

1. Validate request.
2. Identify immutable facts, values, equations, citations, and claims.
3. Identify structural and language weaknesses.
4. Create a preservation map.
5. Rewrite without changing scientific meaning.
6. Report major changes.
7. Run citation audit.
8. Run claim audit.
9. Run phrase-overlap audit.
10. Return rewritten text and rewrite report.

Required report sections:

- `Immutable preservation map`
- `Weakness diagnosis`
- `Rewritten text`
- `Major changes`
- `Citation audit`
- `Claim audit`
- `Phrase-overlap audit`
- `Uncertain fields`

## Auxiliary Modes

`PLAN`: return outline, evidence needs, risks, and execution steps only.

`CRITIQUE`: identify argument, evidence, citation, structure, and tone issues. Do not rewrite unless requested.

`SHORTEN`: preserve citations, numbers, and claims while reducing length. Report removed or merged claims.

`EXPAND`: add only evidence-supported detail. Flag any requested expansion that lacks evidence.

`POLISH`: improve clarity, transitions, and IEEE tone while preserving meaning.

`RELATED_WORK_SYNTHESIS`: group papers by mechanism, establish novelty boundaries, and state only evidence-supported gaps.

`REVIEWER_RESPONSE`: separate response-to-reviewer text from manuscript-change text. Be specific, respectful, and evidence-grounded.
