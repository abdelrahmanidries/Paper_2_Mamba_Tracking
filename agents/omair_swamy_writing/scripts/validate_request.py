#!/usr/bin/env python3
"""Validate an Omair_Swamy_Writing request template.

The validator intentionally uses only the Python standard library. It performs
schema-level checks that are robust enough for the agent request files without
depending on PyYAML.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


ALLOWED_MODES = {
    "WRITE_FROM_SCRATCH",
    "REWRITE",
    "PLAN",
    "CRITIQUE",
    "SHORTEN",
    "EXPAND",
    "POLISH",
    "RELATED_WORK_SYNTHESIS",
    "REVIEWER_RESPONSE",
}

ALLOWED_SECTIONS = {
    "abstract",
    "introduction",
    "related_work",
    "method",
    "experiments",
    "results",
    "discussion",
    "conclusion",
    "reviewer_response",
}

REQUIRED_KEYS = ("request_id", "mode", "section_type", "task", "constraints", "evidence", "output")
REQUIRED_CONSTRAINTS = (
    "do_not_modify_active_manuscript: true",
    "do_not_download_papers: true",
    "do_not_copy_corpus_passages: true",
)


def scalar(text: str, key: str) -> str | None:
    match = re.search(rf"(?m)^{re.escape(key)}:\s*['\"]?([^'\"\n#]+)", text)
    return match.group(1).strip() if match else None


def validate(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    for key in REQUIRED_KEYS:
        if not re.search(rf"(?m)^{re.escape(key)}:", text):
            errors.append(f"missing required key: {key}")

    mode = scalar(text, "mode")
    if mode not in ALLOWED_MODES:
        errors.append(f"invalid mode: {mode}")

    section = scalar(text, "section_type")
    if section not in ALLOWED_SECTIONS:
        errors.append(f"invalid section_type: {section}")

    lowered = text.lower()
    for constraint in REQUIRED_CONSTRAINTS:
        if constraint not in lowered:
            errors.append(f"missing or false constraint: {constraint}")

    if "evidence_status: supported" not in text and "evidence_status: needs_evidence" not in text:
        errors.append("at least one evidence item must declare evidence_status")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("request", type=Path)
    args = parser.parse_args()
    errors = validate(args.request)
    if errors:
        print(f"INVALID {args.request}")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"VALID {args.request}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
