#!/usr/bin/env python3
"""Report citation coverage by paragraph."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


CITE_RE = re.compile(r"\\cite[a-zA-Z*]*\{[^}]+\}|\[[0-9,\-\s]+\]")


def paragraphs(text: str) -> list[str]:
    return [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("draft", type=Path)
    args = parser.parse_args()
    text = args.draft.read_text(encoding="utf-8", errors="ignore")
    paras = paragraphs(text)
    missing = []
    skip_prefixes = (
        "#",
        "- claim:",
        "evidence:",
        "- citation audit:",
        "- claim audit:",
        "- phrase-overlap audit:",
        "- uncertain fields:",
        "- major changes:",
    )
    for idx, para in enumerate(paras, start=1):
        lower = para.lower()
        if lower.startswith(skip_prefixes) or re.match(r"^\d+\.\s", para):
            continue
        needs_citation = any(word in lower for word in ("prior", "existing", "recent", "method", "tracker", "restoration", "reported"))
        if needs_citation and not CITE_RE.search(para):
            missing.append(idx)

    print("citation_coverage_report")
    print(f"file: {args.draft}")
    print(f"paragraph_count: {len(paras)}")
    print(f"paragraphs_requiring_citation_without_marker: {missing}")
    print("status: PASS" if not missing else "status: REVIEW")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
