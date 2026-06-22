#!/usr/bin/env python3
"""Verify the clean IEEE Transactions submission source package."""

from __future__ import annotations

import re
import shutil
import subprocess
import zipfile
from pathlib import Path


ROOT = Path.cwd()
PAPER = ROOT / "paper" / "ieee_transactions"
SUBMISSION = PAPER / "submission"
ZIP_PATH = PAPER / "Paper_2_IEEE_Transactions_source.zip"

REQUIRED_SECTIONS = [
    "abstract.tex",
    "introduction.tex",
    "related_work.tex",
    "method.tex",
    "experiments.tex",
    "results.tex",
    "discussion.tex",
    "conclusion.tex",
    "appendix.tex",
]

REQUIRED_TABLES = [
    "paper_main_benchmark_table.tex",
    "paper_condition_table.tex",
    "paper_ablation_table.tex",
    "paper_efficiency_table.tex",
]

REQUIRED_FIGURES = [
    "benchmark_auc_change.pdf",
    "condition_auc_change.pdf",
    "efficiency_comparison.pdf",
    "ablation_decision.pdf",
    "nfs_failure_mode_distribution.pdf",
]

REQUIRED_ROOT_FILES = [
    "main.tex",
    "references.bib",
    "IEEEtran.cls",
    "IEEEtran.bst",
    "README.md",
]

MANDATORY_ANCHORS = [
    "+0.033144",
    "+0.017405",
    "-0.009638",
    "+0.001478",
    "92,518,533",
    "94,598,469",
    "93.247",
    "86.766",
    "Tesla V100-PCIE-32GB",
]

FORBIDDEN_OLD_VALUES = ["-0.403866", "-0.014195", "+0.001605"]
FORBIDDEN_ZIP_SUFFIXES = {
    ".aux",
    ".bbl",
    ".blg",
    ".fdb_latexmk",
    ".fls",
    ".log",
    ".out",
    ".pdfsync",
    ".synctex.gz",
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def require(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"Missing required file: {path}")


def combined_source() -> str:
    paths = [SUBMISSION / "main.tex"]
    paths += [SUBMISSION / "sections" / name for name in REQUIRED_SECTIONS]
    paths += [SUBMISSION / "tables" / name for name in REQUIRED_TABLES]
    return "\n".join(read(path) for path in paths)


def bib_keys() -> set[str]:
    return set(re.findall(r"@\w+\{([^,]+),", read(SUBMISSION / "references.bib")))


def citation_keys(tex: str) -> set[str]:
    keys: set[str] = set()
    for body in re.findall(r"\\cite\{([^}]+)\}", tex):
        keys.update(k.strip() for k in body.split(",") if k.strip())
    return keys


def labels(tex: str) -> list[str]:
    return re.findall(r"\\label\{([^}]+)\}", tex)


def refs(tex: str) -> set[str]:
    found: set[str] = set()
    for cmd in ["ref", "eqref", "autoref"]:
        found.update(x.strip() for x in re.findall(rf"\\{cmd}\{{([^}}]+)\}}", tex))
    return found


def verify_required_files() -> None:
    for name in REQUIRED_ROOT_FILES:
        require(SUBMISSION / name)
    for name in REQUIRED_SECTIONS:
        require(SUBMISSION / "sections" / name)
    for name in REQUIRED_TABLES:
        require(SUBMISSION / "tables" / name)
    for name in REQUIRED_FIGURES:
        require(SUBMISSION / "figures" / name)


def verify_source_integrity(tex: str) -> None:
    for anchor in MANDATORY_ANCHORS:
        if anchor not in tex:
            raise AssertionError(f"Mandatory anchor missing: {anchor}")
    for old_value in FORBIDDEN_OLD_VALUES:
        if old_value in tex:
            raise AssertionError(f"Old invalid or superseded value found: {old_value}")
    for token in ["TODO", "TBD", "XXX", "citationneeded", "CITATION NEEDED"]:
        if token in tex:
            raise AssertionError(f"Unresolved placeholder token found: {token}")
    lower = tex.lower()
    if "tdm is retained" in lower or "tdm is the final" in lower:
        raise AssertionError("TDM appears to be described as retained/final")
    if "c13" in lower or "c14" in lower:
        raise AssertionError("Unsupported C13/C14 claim ids appear in manuscript source")
    if "flops/macs" in lower and "reported as measured" in lower and "not reported as measured" not in lower:
        raise AssertionError("FLOPs/MACs appear to be claimed as measured")
    if "AUTHOR INFORMATION REQUIRES CONFIRMATION" not in tex:
        raise AssertionError("Unresolved author information is not clearly listed")


def verify_citations_and_refs(tex: str) -> None:
    cited = citation_keys(tex)
    bib = bib_keys()
    if cited - bib:
        raise AssertionError(f"Missing BibTeX keys: {sorted(cited - bib)}")
    if bib - cited:
        raise AssertionError(f"Uncited BibTeX entries: {sorted(bib - cited)}")
    labs = labels(tex)
    duplicates = sorted({x for x in labs if labs.count(x) > 1})
    if duplicates:
        raise AssertionError(f"Duplicate labels: {duplicates}")
    missing_refs = refs(tex) - set(labs)
    if missing_refs:
        raise AssertionError(f"Undefined references by static source scan: {sorted(missing_refs)}")


def verify_figures_and_tables_referenced(tex: str) -> None:
    required_labels = [
        "tab:paper-freeze-benchmark",
        "tab:conditions",
        "tab:ablations",
        "tab:efficiency",
        "fig:benchmark_auc_change",
        "fig:condition_auc_change",
        "fig:efficiency_comparison",
        "fig:ablation_decision",
        "fig:nfs_failure_modes",
    ]
    source_refs = refs(tex)
    for label in required_labels:
        if label not in labels(tex):
            raise AssertionError(f"Missing label: {label}")
        if label not in source_refs:
            raise AssertionError(f"Label is not referenced: {label}")


def clean_submission_build() -> None:
    if shutil.which("latexmk") is None:
        raise RuntimeError("latexmk is unavailable")
    subprocess.run(["latexmk", "-C"], cwd=SUBMISSION, check=True)
    for name in ["main.aux", "main.bbl", "main.blg", "main.fdb_latexmk", "main.fls", "main.log", "main.out", "main.pdf"]:
        path = SUBMISSION / name
        if path.exists():
            path.unlink()


def compile_submission() -> None:
    subprocess.run(
        ["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error", "main.tex"],
        cwd=SUBMISSION,
        check=True,
    )
    require(SUBMISSION / "main.pdf")
    log = read(SUBMISSION / "main.log")
    for needle in ["Undefined control sequence", "LaTeX Error", "Citation `", "Reference `", "Overfull \\hbox", "Overfull \\vbox"]:
        if needle in log:
            raise AssertionError(f"Submission build log contains unresolved issue: {needle}")


def verify_zip() -> None:
    require(ZIP_PATH)
    with zipfile.ZipFile(ZIP_PATH) as zf:
        names = zf.namelist()
    for suffix in FORBIDDEN_ZIP_SUFFIXES:
        bad = [name for name in names if name.endswith(suffix)]
        if bad:
            raise AssertionError(f"ZIP contains generated files with suffix {suffix}: {bad[:5]}")
    required = [
        "submission/main.tex",
        "submission/references.bib",
        "submission/IEEEtran.cls",
        "submission/IEEEtran.bst",
        "submission/README.md",
    ]
    required += [f"submission/sections/{name}" for name in REQUIRED_SECTIONS]
    required += [f"submission/tables/{name}" for name in REQUIRED_TABLES]
    required += [f"submission/figures/{name}" for name in REQUIRED_FIGURES]
    missing = [name for name in required if name not in names]
    if missing:
        raise AssertionError(f"ZIP missing required source files: {missing}")


def main() -> int:
    verify_required_files()
    tex = combined_source()
    verify_source_integrity(tex)
    verify_citations_and_refs(tex)
    verify_figures_and_tables_referenced(tex)
    verify_zip()
    clean_submission_build()
    compile_submission()
    print(f"Submission PDF exists: {SUBMISSION / 'main.pdf'}")
    print(f"Source ZIP exists: {ZIP_PATH} ({ZIP_PATH.stat().st_size} bytes)")
    print("IEEE submission source package verification passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
