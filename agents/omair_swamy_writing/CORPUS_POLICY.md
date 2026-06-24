# Corpus Policy

The style corpus is used only as an abstract style signal. The agent must not copy, package, export, or reproduce corpus paper text.

## Allowed

- Referencing verified style-summary files by path.
- Using derived metadata such as paragraph counts, role sequences, citation density, and group weights.
- Running phrase-overlap checks against local corpus text.
- Describing style tendencies in original words.

## Not Allowed

- Copying corpus passages into prompts, demonstrations, drafts, reports, or agent files.
- Bundling PDFs, extracted `.txt` sections, or full copyrighted passages under `agents/omair_swamy_writing/`.
- Downloading new papers.
- Using corpus text as few-shot examples.
- Paraphrasing a corpus passage closely enough to preserve distinctive wording.

## Required Checks

Before returning generated or rewritten text:

1. Run `check_phrase_overlap.py` on the generated text.
2. Review any reported overlap manually.
3. Revise any nontrivial overlap that is not a common technical phrase.
4. State the overlap status in the final report.

## Demonstration Rule

Demonstrations must use fictional, non-project topics and invented placeholders. They must not include supervisor-corpus text, manuscript text, or copied paper passages.
