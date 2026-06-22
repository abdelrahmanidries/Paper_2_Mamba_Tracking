# IEEE Transactions Manuscript Package

This directory contains the Paper Freeze V1 IEEE Transactions LaTeX source package.

## Build

Preferred command:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

In this Codex environment, `latexmk`, `pdflatex`, and `kpsewhich` were unavailable, so compilation could not be executed locally.

## Template Provenance

The requested local InvTrack IEEEtran manuscript template was searched under Desktop, Documents, and sibling project locations. No local IEEEtran manuscript root or `IEEEtran.cls` file was found. The source therefore uses:

```tex
\documentclass[journal]{IEEEtran}
```

and relies on a TeX installation that provides IEEEtran.

## Citation Status

Only local bibliographic metadata was used. Exact citations for OSTrack, LaSOT, OTB, UAV123, and NFS remain unresolved and are visibly marked in the manuscript.
