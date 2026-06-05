"""Extract per-page text from PDFs into JSONL files.

Input:  papers/*.pdf
Output: data/extracted/<paper_id>.jsonl

This script uses PyMuPDF text extraction only. It does not perform OCR.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import fitz  # PyMuPDF


ROOT = Path(__file__).resolve().parents[1]
PAPERS_DIR = ROOT / "papers"
OUTPUT_DIR = ROOT / "data" / "extracted"


def make_paper_id(pdf_path: Path) -> str:
    """Create a filesystem-friendly paper_id from the PDF filename stem."""
    paper_id = re.sub(r"[^A-Za-z0-9]+", "_", pdf_path.stem).strip("_")
    return paper_id or "paper"


def extract_pdf(pdf_path: Path) -> tuple[str, int, list[str]]:
    """Extract one JSONL file and return paper_id, pages written, issues."""
    paper_id = make_paper_id(pdf_path)
    output_path = OUTPUT_DIR / f"{paper_id}.jsonl"
    issues: list[str] = []
    pages_written = 0

    try:
        doc = fitz.open(pdf_path)
    except Exception as exc:  # PyMuPDF may raise several exception types.
        issues.append(f"open_error: {exc}")
        output_path.write_text("", encoding="utf-8")
        return paper_id, pages_written, issues

    with doc:
        with output_path.open("w", encoding="utf-8", newline="\n") as handle:
            for page_index in range(len(doc)):
                page_number = page_index + 1
                try:
                    text = doc.load_page(page_index).get_text("text")
                except Exception as exc:
                    text = ""
                    issues.append(f"page {page_number}: text_extraction_error: {exc}")

                row = {
                    "paper_id": paper_id,
                    "filename": pdf_path.name,
                    "page_number": page_number,
                    "text": text,
                }
                handle.write(json.dumps(row, ensure_ascii=False) + "\n")
                pages_written += 1

    return paper_id, pages_written, issues


def main() -> int:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    pdf_paths = sorted(PAPERS_DIR.glob("*.pdf"))

    if not pdf_paths:
        print(f"No PDFs found in {PAPERS_DIR}")
        return 1

    total_pages = 0
    problem_count = 0
    print(f"Found {len(pdf_paths)} PDF(s) in {PAPERS_DIR}")

    for pdf_path in pdf_paths:
        paper_id, pages_written, issues = extract_pdf(pdf_path)
        total_pages += pages_written
        status = "ok" if not issues else "issues"
        if issues:
            problem_count += 1
        print(f"{paper_id}: {pages_written} page(s) extracted from {pdf_path.name} [{status}]")
        for issue in issues:
            print(f"  - {issue}")

    print(
        "Extraction complete: "
        f"{len(pdf_paths)} PDF(s), {total_pages} page row(s), "
        f"{problem_count} PDF(s) with extraction problems."
    )
    return 0 if problem_count == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
