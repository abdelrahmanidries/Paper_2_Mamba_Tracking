# Introduction and Related Work Rewrite Report

## Scope

Only the IEEE Transactions manuscript Introduction and Related Work source sections were rewritten:

- `paper/ieee_transactions/sections/introduction.tex`
- `paper/ieee_transactions/sections/related_work.tex`

No method, experiment, result, discussion, conclusion, or bibliography entries were changed for scientific content.

## 1. Introduction Paragraph Structure

The revised Introduction follows the requested six-stage narrowing pattern:

1. Single-object tracking context, practical importance, and benchmark setting.
2. One-stream/template-search tracking progress and degradation sensitivity.
3. Prior degradation-aware tracking and restoration work, with strengths acknowledged before limitations.
4. State-space/Mamba motivation and the precise unresolved gap, with missing external tracking citations marked explicitly.
5. Proposed `OSTrack` + `RG-SSB` configuration and method boundary.
6. Four concrete contribution items plus paper organization.

## 2. Related Work Subsection Structure

The revised Related Work is organized by method family:

1. One-Stream and Transformer-Based Visual Tracking.
2. Robust Tracking Under Degraded Observations.
3. State-Space and Mamba-Based Visual Tracking.
4. Restoration-Oriented State-Space Models.
5. Positioning of the Proposed Method.

The final positioning subsection distinguishes `RG-SSB` from ordinary one-stream tracking, image restoration preprocessing, generic Mamba vision backbones, InvTrack-style response fusion, and rejected consistency losses.

## 3. Supervisor-Style Patterns Applied

The rewrite applies the approved high-confidence corpus patterns:

- practical context before method detail;
- gradual narrowing from application pressure to a specific technical gap;
- prior-work strengths acknowledged before limitations;
- cautious novelty language;
- controlled method preview before contributions;
- concrete, testable contribution items;
- method-family Related Work organization rather than chronology;
- explicit claim boundaries for unsupported or mixed evidence.

## 4. Tracking-Specific Sources Used

Existing verified manuscript citations used:

- `ye2022ostrack` for the one-stream base tracker.
- `invtrack_local` for local degradation-invariant tracking evidence.
- `guo2024mambair` and `guo2025mambairv2` for restoration-oriented state-space motivation.
- `wu2013otb`, `mueller2016uav123`, `fan2019lasot`, and `galoogahi2017nfs` for benchmark/training context.

## 5. New Citations Added

No new BibTeX entries were added. No fabricated citations were introduced.

## 6. Unresolved Citations

The rewrite intentionally preserves citation gaps as explicit source text markers because `references.bib` does not yet contain the needed verified entries:

- Representative transformer trackers before `OSTrack`.
- Representative degradation-robust tracking literature.
- Mamba and visual state-space foundation papers.
- Representative Mamba-based visual tracking papers.

These markers appear as `[CITATION REQUIRED: ...]` text rather than unresolved `\cite{}` commands.

## 7. Phrase-Overlap Result

Commands run:

```bash
python3 scripts/check_supervisor_corpus_phrase_overlap.py --manuscript paper/ieee_transactions/sections/introduction.tex
python3 scripts/check_supervisor_corpus_phrase_overlap.py --manuscript paper/ieee_transactions/sections/related_work.tex
```

Results:

- Introduction overlap count: `0`.
- Related Work overlap count: `0`.

The checker was updated to accept the requested `--manuscript` option while preserving the prior positional-path interface.

## 8. Compilation Result

Commands run:

```bash
cd paper/ieee_transactions
latexmk -C
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cd ../..
python3 scripts/verify_ieee_transaction_manuscript.py
python3 scripts/verify_ieee_submission_package.py
```

Results:

- Main IEEE manuscript build succeeded.
- `verify_ieee_transaction_manuscript.py` passed.
- `verify_ieee_submission_package.py` passed.

## 9. Page-Count Change

- Previous `paper/ieee_transactions/main.pdf`: 5 pages.
- Rebuilt `paper/ieee_transactions/main.pdf`: 6 pages.
- Net change: +1 page.

## 10. Claims Requiring Human Review

The following claim areas require human review and citation completion before submission:

- Any broad statement about transformer-based trackers beyond `OSTrack`.
- Any broad statement about degradation-robust tracking beyond local InvTrack evidence.
- Any statement about specific roles of Mamba-based visual trackers.
- Any claim that state-space models provide computational advantages in vision.
- The local InvTrack citation remains unpublished/local evidence and should be replaced or confirmed when final metadata is available.

The rewrite avoids state-of-the-art, universal degradation robustness, and uniform-improvement claims.
