#!/usr/bin/env python3
"""Wrapper for the project phrase-overlap checker."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
REFERENCE = ROOT / "scripts" / "check_supervisor_corpus_phrase_overlap.py"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("draft", type=Path)
    parser.add_argument("--min-words", type=int, default=8)
    args = parser.parse_args()
    if not REFERENCE.exists():
        print(f"ERROR: missing reference checker: {REFERENCE}")
        return 1
    cmd = [sys.executable, str(REFERENCE), str(args.draft), "--min-words", str(args.min_words)]
    result = subprocess.run(cmd, check=False)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
