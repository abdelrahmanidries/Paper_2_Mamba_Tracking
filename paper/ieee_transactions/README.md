# IEEE Transactions Manuscript Package

This directory contains the Paper Freeze V1 IEEE Transactions manuscript source.

## Build

```bash
latexmk -C
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

Generated output:

- `main.pdf`
- `main.log`

The final build completed successfully with 5 pages, no undefined citations, no undefined references, and no overfull boxes in the final log.

## Source Package

Clean submission source:

```text
submission/
```

Source ZIP:

```text
Paper_2_IEEE_Transactions_source.zip
```

The submission package includes the TeX source, section files, table files, used PDF figures, `references.bib`, `IEEEtran.cls`, `IEEEtran.bst`, and a build README. It excludes auxiliary files, logs, rendered page PNGs, datasets, checkpoints, experiment outputs, and Git metadata.

## Citation Status

All genuine citation placeholders have been resolved. The bibliography contains 8 entries, and all 8 are cited.

## Remaining Manual Author Check

The author block uses candidate information copied from `papers/InvTrack.pdf` and is explicitly marked for confirmation in `main.tex`. ORCIDs, exact corresponding-author email punctuation, biographies, and final current-manuscript author confirmation remain unresolved.
