"""Validate the expected project folders and generated pipeline files."""

from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FOLDERS = [
    "papers",
    "data",
    "data/extracted",
    "notes",
    "paper_cards",
    "scripts",
    "tables",
    "reports",
]


def make_paper_id(pdf_path: Path) -> str:
    paper_id = re.sub(r"[^A-Za-z0-9]+", "_", pdf_path.stem).strip("_")
    return paper_id or "paper"


def print_missing(label: str, items: list[Path]) -> None:
    if not items:
        print(f"{label}: none")
        return
    print(f"{label}:")
    for item in items:
        print(f"  - {item}")


def main() -> int:
    missing_folders = [ROOT / folder for folder in REQUIRED_FOLDERS if not (ROOT / folder).is_dir()]
    pdfs = sorted((ROOT / "papers").glob("*.pdf")) if (ROOT / "papers").is_dir() else []
    jsonl_files = (
        sorted((ROOT / "data" / "extracted").glob("*.jsonl"))
        if (ROOT / "data" / "extracted").is_dir()
        else []
    )
    inventory_path = ROOT / "tables" / "pdf_inventory.csv"
    expected_jsonl_files = [
        ROOT / "data" / "extracted" / f"{make_paper_id(pdf_path)}.jsonl"
        for pdf_path in pdfs
    ]
    missing_jsonl_files = [
        jsonl_path for jsonl_path in expected_jsonl_files if not jsonl_path.exists()
    ]
    inventory_rows = 0
    if inventory_path.exists():
        with inventory_path.open("r", encoding="utf-8", newline="") as handle:
            inventory_rows = sum(1 for _ in csv.DictReader(handle))

    print(f"Project root: {ROOT}")
    print(f"Required folders present: {len(REQUIRED_FOLDERS) - len(missing_folders)}/{len(REQUIRED_FOLDERS)}")
    print(f"PDFs found in papers/: {len(pdfs)}")
    print(f"Extracted JSONL files found in data/extracted/: {len(jsonl_files)}")
    print(f"Expected extracted JSONL files present: {len(expected_jsonl_files) - len(missing_jsonl_files)}/{len(expected_jsonl_files)}")
    print(f"Inventory exists: {inventory_path.exists()} ({inventory_path})")
    print(f"Inventory rows: {inventory_rows}")

    print_missing("Missing folders", missing_folders)
    if not pdfs:
        print(f"Missing PDFs: no *.pdf files found in {ROOT / 'papers'}")
    else:
        print("Missing PDFs: none")
    if not jsonl_files:
        print(f"Missing extracted JSONL files: no *.jsonl files found in {ROOT / 'data' / 'extracted'}")
    else:
        print_missing("Missing extracted JSONL files", missing_jsonl_files)
    if not inventory_path.exists():
        print(f"Missing inventory file: {inventory_path}")
    else:
        print("Missing inventory file: none")

    has_missing = (
        bool(missing_folders)
        or not pdfs
        or not jsonl_files
        or bool(missing_jsonl_files)
        or not inventory_path.exists()
    )
    if has_missing:
        print("Validation failed.")
        return 1

    print("Validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
