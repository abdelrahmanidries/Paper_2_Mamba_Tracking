#!/usr/bin/env python3
"""Verify the IEEE Transactions manuscript package without running experiments."""

from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path


ROOT = Path.cwd()
PAPER = ROOT / "paper" / "ieee_transactions"

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

MANDATORY_ANCHORS = [
    "+0.033144",
    "+0.017405",
    "-0.009638",
    "+0.001478",
    "92,518,533",
    "94,598,469",
    "2,079,936",
    "93.247",
    "86.766",
    "10.724",
    "11.525",
    "380.233",
    "388.917",
    "Tesla V100-PCIE-32GB",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def require(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"Missing required file: {path}")


def combined_tex() -> str:
    parts = [read(PAPER / "main.tex")]
    for section in REQUIRED_SECTIONS:
        parts.append(read(PAPER / "sections" / section))
    for table in REQUIRED_TABLES:
        parts.append(read(PAPER / "tables" / table))
    return "\n".join(parts)


def bib_keys() -> set[str]:
    text = read(PAPER / "references.bib")
    return set(re.findall(r"@\w+\{([^,]+),", text))


def citation_keys(tex: str) -> set[str]:
    keys = set()
    for body in re.findall(r"\\cite\{([^}]+)\}", tex):
        keys.update(k.strip() for k in body.split(",") if k.strip())
    return keys


def labels(tex: str) -> set[str]:
    return set(re.findall(r"\\label\{([^}]+)\}", tex))


def refs(tex: str) -> set[str]:
    found = set()
    for cmd in ["ref", "eqref", "autoref"]:
        for body in re.findall(rf"\\{cmd}\{{([^}}]+)\}}", tex):
            found.add(body.strip())
    return found


def verify_required_files() -> None:
    require(PAPER / "main.tex")
    require(PAPER / "references.bib")
    require(PAPER / "README.md")
    require(PAPER / "AUTHOR_INFORMATION_REVIEW.md")
    require(PAPER / "CITATION_RESOLUTION_REPORT.md")
    for section in REQUIRED_SECTIONS:
        require(PAPER / "sections" / section)
    for table in REQUIRED_TABLES:
        require(PAPER / "tables" / table)
    for figure in REQUIRED_FIGURES:
        require(PAPER / "figures" / figure)


def verify_citations(tex: str) -> None:
    missing = citation_keys(tex) - bib_keys()
    if missing:
        raise AssertionError(f"Citation keys missing from references.bib: {sorted(missing)}")
    uncited = bib_keys() - citation_keys(tex)
    if uncited:
        raise AssertionError(f"Bibliography entries not cited in manuscript: {sorted(uncited)}")


def verify_refs(tex: str) -> None:
    missing = refs(tex) - labels(tex)
    if missing:
        raise AssertionError(f"References without labels: {sorted(missing)}")


def verify_anchors(tex: str) -> None:
    for anchor in MANDATORY_ANCHORS:
        if anchor not in tex:
            raise AssertionError(f"Mandatory anchor missing from TeX package: {anchor}")
    if "-0.403866" in tex:
        raise AssertionError("Old invalid NFS value -0.403866 appears in manuscript")
    lower = tex.lower()
    forbidden_positive = [
        "achieves state-of-the-art",
        "state-of-the-art performance",
        "proves universal",
        "universally robust",
        "demonstrates uniform gains across all benchmarks",
        "achieves uniform gains across all benchmarks",
    ]
    for phrase in forbidden_positive:
        if phrase in lower:
            raise AssertionError(f"Unsupported positive claim found: {phrase}")
    if "tdm is retained" in lower or "tdm is the final" in lower:
        raise AssertionError("TDM appears to be described as final/retained")


def verify_placeholders(tex: str) -> None:
    for token in ["TODO", "TBD", "XXX"]:
        if token in tex:
            raise AssertionError(f"Unresolved placeholder token found: {token}")
    citation_markers = len(re.findall(r"\\citationneeded\{[^}]+\}", tex))
    if citation_markers:
        raise AssertionError(f"Genuine citation placeholders remaining: {citation_markers}")
    author_review = read(PAPER / "AUTHOR_INFORMATION_REVIEW.md")
    if "REQUIRES CONFIRMATION" not in read(PAPER / "main.tex") or "Human confirmation required" not in author_review:
        raise AssertionError("Author information requiring confirmation is not listed")


def verify_figures_and_tables_referenced(tex: str) -> None:
    for label in [
        "tab:paper-freeze-benchmark",
        "tab:conditions",
        "tab:ablations",
        "tab:efficiency",
        "fig:benchmark_auc_change",
        "fig:condition_auc_change",
        "fig:efficiency_comparison",
        "fig:ablation_decision",
        "fig:nfs_failure_modes",
    ]:
        if label not in labels(tex):
            raise AssertionError(f"Missing label: {label}")
        if label not in refs(tex):
            raise AssertionError(f"Label is not referenced: {label}")


def verify_build_log() -> None:
    log = PAPER / "main.log"
    if not log.exists():
        if shutil.which("latexmk") is None and shutil.which("pdflatex") is None:
            print("No build log/PDF found because LaTeX tooling is unavailable in this environment.")
            return
        raise AssertionError("LaTeX tooling appears available but main.log is missing")
    text = read(log)
    for needle in ["Undefined control sequence", "LaTeX Error", "Citation `", "Reference `", "Overfull \\hbox", "Overfull \\vbox"]:
        if needle in text:
            raise AssertionError(f"Build log contains unresolved issue: {needle}")


def pdf_page_count(pdf: Path) -> int:
    require(pdf)
    result = subprocess.run(["pdfinfo", str(pdf)], check=True, text=True, capture_output=True)
    match = re.search(r"^Pages:\s+(\d+)$", result.stdout, re.MULTILINE)
    if not match:
        raise AssertionError("Could not read PDF page count with pdfinfo")
    return int(match.group(1))


def main() -> int:
    verify_required_files()
    tex = combined_tex()
    verify_citations(tex)
    verify_refs(tex)
    verify_anchors(tex)
    verify_placeholders(tex)
    verify_figures_and_tables_referenced(tex)
    verify_build_log()
    pages = pdf_page_count(PAPER / "main.pdf")
    print(f"PDF exists: {PAPER / 'main.pdf'}")
    print(f"PDF page count: {pages}")
    print("IEEE Transactions manuscript package verification passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
