#!/usr/bin/env python3
"""Lightweight style and risk score for generated drafts."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


HEDGE_RE = re.compile(r"\b(may|can|could|suggests?|indicates?|not reported|limited|bounded)\b", re.I)
CITE_RE = re.compile(r"\\cite[a-zA-Z*]*\{[^}]+\}|\[[0-9,\-\s]+\]")
RISK_RE = re.compile(r"\b(first|unprecedented|guarantees?|proves?|always|never|significantly superior)\b", re.I)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("draft", type=Path)
    args = parser.parse_args()
    text = args.draft.read_text(encoding="utf-8", errors="ignore")
    words = re.findall(r"\b\w+\b", text)
    paragraphs = [p for p in re.split(r"\n\s*\n", text) if p.strip()]
    sentence_count = max(1, len(re.findall(r"[.!?](?:\s|$)", text)))
    mean_sentence_words = len(words) / sentence_count
    citation_count = len(CITE_RE.findall(text))
    hedge_count = len(HEDGE_RE.findall(text))
    risk_count = len(RISK_RE.findall(text))

    score = 10
    if not paragraphs:
        score -= 4
    if mean_sentence_words > 38:
        score -= 1
    if citation_count == 0 and len(words) > 120:
        score -= 2
    if risk_count:
        score -= min(3, risk_count)
    if hedge_count == 0 and len(words) > 250:
        score -= 1
    score = max(0, score)

    print("draft_score_report")
    print(f"file: {args.draft}")
    print(f"word_count: {len(words)}")
    print(f"paragraph_count: {len(paragraphs)}")
    print(f"mean_sentence_words: {mean_sentence_words:.2f}")
    print(f"citation_count: {citation_count}")
    print(f"hedge_count: {hedge_count}")
    print(f"risky_language_count: {risk_count}")
    print(f"score_0_to_10: {score}")
    print("status: PASS" if score >= 7 and risk_count == 0 else "status: REVIEW")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
