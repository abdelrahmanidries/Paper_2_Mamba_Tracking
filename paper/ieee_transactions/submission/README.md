# IEEE Transactions Source Package

Build command:

```sh
latexmk -C
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

Contents:

- `main.tex`
- `sections/*.tex`
- `tables/*.tex`
- `figures/*.pdf`
- `references.bib`
- `IEEEtran.cls`
- `IEEEtran.bst`

Known manual check before submission:

- The author block is copied from local InvTrack evidence and is marked for human confirmation in `main.tex`.
- ORCIDs, biographies, and exact corresponding-author email punctuation remain unresolved.
- FLOPs/MACs are intentionally unavailable and are not reported as measured.
