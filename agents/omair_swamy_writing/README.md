# Omair_Swamy_Writing

Reusable Codex-native academic writing agent for IEEE-style computer vision, image restoration, and tracking manuscripts guided by verified Ahmad-Swamy style metadata.

## Purpose

`Omair_Swamy_Writing` supports controlled academic writing without copying corpus prose. It is designed for:

- `WRITE_FROM_SCRATCH`
- `REWRITE`
- `PLAN`
- `CRITIQUE`
- `SHORTEN`
- `EXPAND`
- `POLISH`
- `RELATED_WORK_SYNTHESIS`
- `REVIEWER_RESPONSE`

The agent uses the verified local style artifacts listed in [corpus/style_sources.yaml](corpus/style_sources.yaml). It must not modify the active manuscript unless a request explicitly names an output path outside manuscript sources or asks the user to apply the result manually.

## Quick Start

Prepare a request:

```bash
python agents/omair_swamy_writing/scripts/validate_request.py agents/omair_swamy_writing/requests/introduction_from_scratch.yaml
```

Build an invocation prompt:

```bash
python agents/omair_swamy_writing/scripts/build_agent_prompt.py agents/omair_swamy_writing/requests/introduction_from_scratch.yaml
```

Run audits on a draft:

```bash
python agents/omair_swamy_writing/scripts/check_claim_evidence.py draft.md
python agents/omair_swamy_writing/scripts/check_citation_coverage.py draft.md
python agents/omair_swamy_writing/scripts/check_phrase_overlap.py draft.md
python agents/omair_swamy_writing/scripts/score_draft.py draft.md
```

## Safety Boundary

This agent may create request files, reports, and standalone drafts. It must not:

- download papers,
- package PDFs,
- reproduce copyrighted corpus passages,
- rewrite claims without evidence,
- silently alter facts, citations, equations, values, or experimental results,
- modify `paper/`, manuscript `.tex` files, or active submission files unless explicitly authorized.

## Agent Files

- [SYSTEM_PROMPT.md](SYSTEM_PROMPT.md): operational prompt for Codex.
- [STYLE_PROFILE.md](STYLE_PROFILE.md): compact style model derived from verified artifacts.
- [CORPUS_POLICY.md](CORPUS_POLICY.md): copyright and corpus-use constraints.
- [WORKFLOW.md](WORKFLOW.md): required workflow for each mode.
- [REQUEST_SCHEMA.yaml](REQUEST_SCHEMA.yaml): request contract.
- [section_playbooks/](section_playbooks): section-specific writing rules.
- [rubrics/](rubrics): scoring rubrics.
- [requests/](requests): reusable request templates.
- [scripts/](scripts): validation and audit tools.
- [demonstrations/](demonstrations): fictional examples only.
