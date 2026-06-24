#!/usr/bin/env python3
"""Build a Codex invocation prompt from a request file."""

from __future__ import annotations

import argparse
from pathlib import Path

from validate_request import validate


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("request", type=Path)
    args = parser.parse_args()
    errors = validate(args.request)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    request_text = args.request.read_text(encoding="utf-8")
    print("Use the reusable agent at agents/omair_swamy_writing.")
    print("Read SYSTEM_PROMPT.md, STYLE_PROFILE.md, CORPUS_POLICY.md, WORKFLOW.md, and the relevant section playbook.")
    print("Execute the request below without modifying the active manuscript unless the request explicitly authorizes it.")
    print("\n```yaml")
    print(request_text.rstrip())
    print("```")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
