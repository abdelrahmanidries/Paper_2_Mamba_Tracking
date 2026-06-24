# Omair_Swamy_Writing Agent Design

## Objective

Create a reusable Codex-native academic writing agent that can draft, rewrite, critique, shorten, expand, polish, synthesize related work, and prepare reviewer responses while following verified Ahmad-Swamy IEEE-style guidance.

## Location

The agent is implemented under:

`agents/omair_swamy_writing/`

It is intentionally separate from active manuscript files.

## Design Principles

1. Style is derived from verified summaries and metadata, not copied corpus text.
2. Scientific claims must be traceable to request evidence.
3. Rewriting must preserve facts, values, equations, citations, and claim boundaries.
4. The active manuscript is read-only by default.
5. Phrase-overlap checking is mandatory before returning polished text.

## Key Components

- `SYSTEM_PROMPT.md`: agent role, safety rules, and supported modes.
- `STYLE_PROFILE.md`: group-weighted writing style profile.
- `CORPUS_POLICY.md`: copyright and corpus-use boundary.
- `WORKFLOW.md`: execution steps for all modes.
- `REQUEST_SCHEMA.yaml`: human-readable request contract.
- `section_playbooks/`: section-level writing procedures.
- `rubrics/`: evaluation criteria.
- `requests/`: reusable YAML templates.
- `scripts/`: request validation, prompt building, citation/claim checks, phrase overlap, and scoring.
- `demonstrations/`: fictional examples only.

## Corpus Weighting

- Alireza-centered core: 1.00.
- Tchebichef and Alzheimer papers: 0.75.
- RGB-T tracking papers: 0.45 stylistically and 1.00 for technical organization.
- Other Group C: at most 0.25.
- Group D: excluded.

## Workflow Coverage

`WRITE_FROM_SCRATCH` validates the request, builds a paragraph-role outline and claim-to-evidence map, drafts the section, audits citations and claims, scores style, checks phrase overlap, and returns a draft plus report.

`REWRITE` identifies immutable scientific content, diagnoses structure and language weaknesses, builds a preservation map, rewrites without changing meaning, reports major changes, and runs citation, claim, and phrase-overlap audits.

Auxiliary modes reuse the same evidence and preservation constraints.

## Verification Plan

Verification uses only local commands:

```bash
python -m py_compile agents/omair_swamy_writing/scripts/*.py
for f in agents/omair_swamy_writing/requests/*.yaml agents/omair_swamy_writing/demonstrations/*_request.yaml; do python agents/omair_swamy_writing/scripts/validate_request.py "$f"; done
python agents/omair_swamy_writing/scripts/check_claim_evidence.py agents/omair_swamy_writing/demonstrations/write_from_scratch_output.md
python agents/omair_swamy_writing/scripts/check_citation_coverage.py agents/omair_swamy_writing/demonstrations/write_from_scratch_output.md
python agents/omair_swamy_writing/scripts/check_phrase_overlap.py agents/omair_swamy_writing/demonstrations/write_from_scratch_output.md
python agents/omair_swamy_writing/scripts/score_draft.py agents/omair_swamy_writing/demonstrations/write_from_scratch_output.md
```

The agent directory must contain no PDFs and no copied corpus section text.
