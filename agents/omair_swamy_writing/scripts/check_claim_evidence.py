#!/usr/bin/env python3
"""Check simple claim-to-evidence markers in a draft or report."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


CLAIM_RE = re.compile(r"(?im)^\s*(?:[-*]\s*)?(claim|c\d+)\s*[:|-]\s*(.+)$")
EVIDENCE_RE = re.compile(r"(?im)^\s*(?:[-*]\s*)?(evidence|source|citation)\s*[:|-]\s*(.+)$")
RISK_WORDS = re.compile(r"\b(first|novel|state-of-the-art|significantly|outperform|proves?|guarantees?)\b", re.I)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("draft", type=Path)
    args = parser.parse_args()
    text = args.draft.read_text(encoding="utf-8", errors="ignore")
    claims = CLAIM_RE.findall(text)
    evidence = EVIDENCE_RE.findall(text)
    risky = RISK_WORDS.findall(text)

    print("claim_evidence_report")
    print(f"file: {args.draft}")
    print(f"claim_marker_count: {len(claims)}")
    print(f"evidence_marker_count: {len(evidence)}")
    print(f"risky_language_count: {len(risky)}")
    if claims and not evidence:
        print("status: FAIL")
        print("reason: claim markers found without evidence markers")
        return 1
    if risky:
        print("status: REVIEW")
        print("reason: risky claim language requires manual evidence confirmation")
        return 0
    print("status: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
