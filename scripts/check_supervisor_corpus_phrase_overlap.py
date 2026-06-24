#!/usr/bin/env python3
"""Report phrase overlaps between a manuscript section and the supervisor corpus.

This is an originality-support tool, not a plagiarism detector. It reports exact
matches of N or more consecutive normalized words after filtering references and
common technical expressions.
"""

from __future__ import annotations

import argparse
import re
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CORPUS_DIR = ROOT / "papers" / "supervisor_style_corpus" / "section_text"
WORD_RE = re.compile(r"\b[a-z0-9][a-z0-9'-]*\b", re.I)
REF_RE = re.compile(r"(?im)^\s*references\s*$.*", re.S)

COMMON_PHRASES = {
    "in this paper",
    "the remainder of this paper is organized as follows",
    "experimental results show that",
    "state of the art",
    "single image super resolution",
    "convolutional neural network",
    "deep neural network",
    "mean square error",
    "peak signal to noise ratio",
    "structural similarity index",
    "visual object tracking",
    "template and search",
    "area under the curve",
    "precision at twenty pixels",
}


def clean(text: str) -> list[str]:
    text = REF_RE.sub("", text)
    return [w.lower().strip("'") for w in WORD_RE.findall(text)]


def shingles(words: list[str], n: int) -> dict[tuple[str, ...], list[int]]:
    out: dict[tuple[str, ...], list[int]] = defaultdict(list)
    for i in range(0, max(0, len(words) - n + 1)):
        gram = tuple(words[i : i + n])
        phrase = " ".join(gram)
        if any(common in phrase for common in COMMON_PHRASES):
            continue
        out[gram].append(i)
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manuscript_file", type=Path, nargs="?")
    parser.add_argument("--manuscript", dest="manuscript_option", type=Path)
    parser.add_argument("--corpus-dir", type=Path, default=CORPUS_DIR)
    parser.add_argument("--min-words", type=int, default=8)
    parser.add_argument("--max-report", type=int, default=100)
    args = parser.parse_args()

    manuscript_file = args.manuscript_option or args.manuscript_file
    if manuscript_file is None:
        parser.error("provide a manuscript file path or --manuscript")

    manuscript_words = clean(manuscript_file.read_text(encoding="utf-8", errors="ignore"))
    manuscript_grams = shingles(manuscript_words, args.min_words)
    reports = []

    for corpus_file in sorted(args.corpus_dir.glob("*.txt")):
        corpus_words = clean(corpus_file.read_text(encoding="utf-8", errors="ignore"))
        corpus_grams = shingles(corpus_words, args.min_words)
        for gram in sorted(set(manuscript_grams).intersection(corpus_grams)):
            reports.append(
                {
                    "corpus_file": str(corpus_file.relative_to(ROOT)),
                    "phrase": " ".join(gram),
                    "manuscript_positions": manuscript_grams[gram][:5],
                    "corpus_positions": corpus_grams[gram][:5],
                }
            )

    print("phrase_overlap_report")
    print(f"manuscript_file: {manuscript_file}")
    print(f"corpus_dir: {args.corpus_dir}")
    print(f"min_words: {args.min_words}")
    print(f"overlap_count: {len(reports)}")
    for item in reports[: args.max_report]:
        print("---")
        print(f"corpus_file: {item['corpus_file']}")
        print(f"phrase: {item['phrase']}")
        print(f"manuscript_positions: {item['manuscript_positions']}")
        print(f"corpus_positions: {item['corpus_positions']}")
    if len(reports) > args.max_report:
        print(f"... truncated {len(reports) - args.max_report} additional overlaps")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
