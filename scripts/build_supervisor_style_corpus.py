#!/usr/bin/env python3
"""Build the Ahmad/Swamy writing-style corpus from lawful local PDFs.

The script reads experiments/supervisor_style_corpus_metadata.csv, extracts text
from rows with full_text_available=true and a local PDF path, and writes:

- papers/supervisor_style_corpus/extracted_text/<corpus_id>.txt
- papers/supervisor_style_corpus/section_text/<corpus_id>__*.txt

It never modifies source PDFs.
"""

from __future__ import annotations

import csv
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
METADATA = ROOT / "experiments" / "supervisor_style_corpus_metadata.csv"
EXTRACTED_DIR = ROOT / "papers" / "supervisor_style_corpus" / "extracted_text"
SECTION_DIR = ROOT / "papers" / "supervisor_style_corpus" / "section_text"


INTRO_PAT = re.compile(
    r"^\s*(?:\d+\s+)*"
    r"(?:(?:\d+|[ivx]+)\.?\s*)?"
    r"(?:i\s*n\s*t\s*r\s*o\s*d\s*u\s*c\s*t\s*i\s*o\s*n|background)\b"
    r"|^\s*(?:\d+\s+)*[ivx]+\.\s*i\s*n\s*t\s*r\s*o\s*d\s*u\s*c\s*t\s*i\s*o\s*n\b",
    re.I | re.M,
)
RELATED_PAT = re.compile(
    r"^\s*(?:\d+\s+)*(?:\d+\.?\s*)?"
    r"(?:related work|literature review|materials and methods|proposed method)\b",
    re.I | re.M,
)
STOP_PAT = re.compile(
    r"^\s*(?:\d+\s+)*(?:(?:\d+|[ivx]+)\.?\s*)?"
    r"(?:method(?:ology)?|proposed(?: method)?|problem formulation|system model|experiments?|results?|"
    r"materials and methods|conclusion|references|acknowledg(?:e)?ments?)\b"
    r"|^\s*(?:\d+\s+)*[ivx]+\.\s*"
    r"(?:p\s*r\s*o\s*b\s*l\s*e\s*m|p\s*r\s*o\s*p\s*o\s*s\s*e\s*d|m\s*e\s*t\s*h\s*o\s*d|"
    r"e\s*x\s*p\s*e\s*r\s*i\s*m\s*e\s*n\s*t|r\s*e\s*s\s*u\s*l\s*t|c\s*o\s*n\s*c\s*l\s*u\s*s\s*i\s*o\s*n)\b"
    r"|^\s*(?:\d+\s+)*(?:2|II)\.?\s+[A-Z][A-Za-z0-9 ,:/()_-]{2,80}$",
    re.I | re.M,
)
REFERENCE_PAT = re.compile(r"(?im)^\s*references\s*$")


@dataclass
class Section:
    name: str
    start: int
    end: int
    text: str


def as_bool(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "y"}


def run_pdftotext(pdf_path: Path) -> str:
    proc = subprocess.run(
        ["pdftotext", "-layout", "-enc", "UTF-8", str(pdf_path), "-"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return proc.stdout


def normalize_text(raw: str) -> str:
    raw = raw.replace("\r\n", "\n").replace("\r", "\n")
    raw = re.sub(r"\n\s*\f\s*\n", "\n\n[PAGE_BREAK]\n\n", raw)
    lines = []
    for line in raw.splitlines():
        stripped = line.strip()
        if not stripped:
            lines.append("")
            continue
        if re.fullmatch(r"\d{1,4}", stripped):
            continue
        if re.fullmatch(r"(?:ieee|IEEE).{0,80}", stripped):
            continue
        if re.search(r"^\s*(?:authorized licensed use|downloaded on|personal use only)", stripped, re.I):
            continue
        lines.append(re.sub(r"[ \t]+", " ", stripped))
    text = "\n".join(lines)
    text = re.sub(r"(?<=\w)-\n(?=\w)", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"


def paragraphize(section_text: str) -> str:
    paragraphs = []
    buf = []
    for line in section_text.splitlines():
        stripped = line.strip()
        if not stripped or stripped == "[PAGE_BREAK]":
            if buf:
                paragraphs.append(" ".join(buf))
                buf = []
            continue
        if len(stripped) < 80 and re.match(r"^\d*\.?\s*[A-Z][A-Za-z0-9 ,:()/-]{2,}$", stripped):
            if buf:
                paragraphs.append(" ".join(buf))
                buf = []
            paragraphs.append(stripped)
        else:
            buf.append(stripped)
    if buf:
        paragraphs.append(" ".join(buf))
    return "\n\n".join(p for p in paragraphs if p).strip() + "\n"


def page_for_offset(text: str, offset: int) -> int:
    return text[:offset].count("[PAGE_BREAK]") + 1


def find_section(text: str, name: str, start_match: re.Match[str], next_candidates: list[re.Match[str]]) -> Section:
    start = start_match.end()
    later = [m.start() for m in next_candidates if m.start() > start]
    ref = REFERENCE_PAT.search(text, start)
    if ref:
        later.append(ref.start())
    end = min(later) if later else len(text)
    body = paragraphize(text[start:end])
    return Section(name=name, start=start_match.start(), end=end, text=body)


def extract_sections(text: str) -> dict[str, Section]:
    sections: dict[str, Section] = {}
    intro = INTRO_PAT.search(text)
    if intro:
        stops = list(RELATED_PAT.finditer(text)) + list(STOP_PAT.finditer(text))
        sections["introduction"] = find_section(text, "introduction", intro, stops)

    related_matches = [
        m
        for m in RELATED_PAT.finditer(text)
        if "proposed method" not in m.group(0).lower() and "materials and methods" not in m.group(0).lower()
    ]
    if related_matches:
        rel = related_matches[0]
        stops = list(STOP_PAT.finditer(text))
        sections["related_work"] = find_section(text, "related_work", rel, stops)
    return sections


def main() -> int:
    if not METADATA.exists():
        raise SystemExit(f"Missing metadata CSV: {METADATA}")
    EXTRACTED_DIR.mkdir(parents=True, exist_ok=True)
    SECTION_DIR.mkdir(parents=True, exist_ok=True)

    processed = 0
    with METADATA.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            corpus_id = row["corpus_id"].strip()
            if not as_bool(row.get("full_text_available", "")):
                continue
            pdf_value = row.get("local_pdf_path", "").strip()
            if not pdf_value:
                continue
            pdf_path = ROOT / pdf_value
            if not pdf_path.exists():
                print(f"SKIP missing PDF: {corpus_id} {pdf_path}")
                continue

            raw = run_pdftotext(pdf_path)
            text = normalize_text(raw)
            (EXTRACTED_DIR / f"{corpus_id}.txt").write_text(text, encoding="utf-8")
            sections = extract_sections(text)
            for section_name, section in sections.items():
                header = (
                    f"corpus_id: {corpus_id}\n"
                    f"title: {row.get('title', '')}\n"
                    f"section: {section_name}\n"
                    f"source_pdf: {pdf_value}\n"
                    f"approx_start_page: {page_for_offset(text, section.start)}\n"
                    f"approx_end_page: {page_for_offset(text, section.end)}\n\n"
                )
                (SECTION_DIR / f"{corpus_id}__{section_name}.txt").write_text(
                    header + section.text, encoding="utf-8"
                )
            print(f"processed {corpus_id}: sections={','.join(sections) or 'none'}")
            processed += 1
    print(f"processed_full_text_papers={processed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
