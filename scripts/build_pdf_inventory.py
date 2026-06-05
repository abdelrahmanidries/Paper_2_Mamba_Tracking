"""Build a CSV inventory for PDFs in papers/ using PyMuPDF."""

from __future__ import annotations

import csv
import re
from pathlib import Path

import fitz  # PyMuPDF


ROOT = Path(__file__).resolve().parents[1]
PAPERS_DIR = ROOT / "papers"
OUTPUT_PATH = ROOT / "tables" / "pdf_inventory.csv"


def make_paper_id(pdf_path: Path) -> str:
    """Create a filesystem-friendly paper_id from the PDF filename stem."""
    paper_id = re.sub(r"[^A-Za-z0-9]+", "_", pdf_path.stem).strip("_")
    return paper_id or "paper"


def clean_line(line: str) -> str:
    return re.sub(r"\s+", " ", line).strip()


def is_unlikely_title(line: str) -> bool:
    lowered = line.lower()
    if len(line) < 8:
        return True
    if lowered.startswith(("abstract", "keywords", "introduction", "references")):
        return True
    if "@" in line or "http://" in lowered or "https://" in lowered:
        return True
    if re.fullmatch(r"[\d\s.,:/-]+", line):
        return True
    return False


def guess_title_from_first_page(text: str, fallback: str) -> str:
    """Use early first-page lines to make a conservative title guess."""
    lines = [clean_line(line) for line in text.splitlines()]
    lines = [line for line in lines if line and not is_unlikely_title(line)]
    if not lines:
        return fallback

    title_parts: list[str] = []
    for line in lines[:8]:
        lowered = line.lower()
        if lowered.startswith(("abstract", "keywords", "1 introduction")):
            break
        title_parts.append(line)
        combined = " ".join(title_parts)
        if len(combined) >= 35 or combined.endswith(("?", "!", ".")):
            break

    guessed = " ".join(title_parts).strip()
    if not guessed:
        return fallback
    return guessed[:300]


def inspect_pdf(pdf_path: Path) -> dict[str, str | int]:
    paper_id = make_paper_id(pdf_path)
    row: dict[str, str | int] = {
        "paper_id": paper_id,
        "filename": pdf_path.name,
        "guessed_title": pdf_path.stem,
        "num_pages": 0,
        "extraction_status": "not_started",
    }

    try:
        doc = fitz.open(pdf_path)
    except Exception as exc:
        row["extraction_status"] = f"open_error: {exc}"
        return row

    with doc:
        row["num_pages"] = len(doc)
        if len(doc) == 0:
            row["extraction_status"] = "empty_pdf"
            return row

        try:
            first_page_text = doc.load_page(0).get_text("text")
        except Exception as exc:
            row["extraction_status"] = f"first_page_text_error: {exc}"
            return row

        row["guessed_title"] = guess_title_from_first_page(first_page_text, pdf_path.stem)
        row["extraction_status"] = "ok"
        return row


def main() -> int:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    pdf_paths = sorted(PAPERS_DIR.glob("*.pdf"))

    rows = [inspect_pdf(pdf_path) for pdf_path in pdf_paths]
    fieldnames = [
        "paper_id",
        "filename",
        "guessed_title",
        "num_pages",
        "extraction_status",
    ]
    with OUTPUT_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    problem_rows = [row for row in rows if row["extraction_status"] != "ok"]
    print(f"Found {len(pdf_paths)} PDF(s) in {PAPERS_DIR}")
    print(f"Wrote {len(rows)} inventory row(s) to {OUTPUT_PATH}")
    if problem_rows:
        print("PDFs with inventory extraction problems:")
        for row in problem_rows:
            print(f"  - {row['filename']}: {row['extraction_status']}")
    else:
        print("PDFs with inventory extraction problems: none")

    return 0 if not problem_rows else 2


if __name__ == "__main__":
    raise SystemExit(main())
