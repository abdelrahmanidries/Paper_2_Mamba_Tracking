#!/usr/bin/env python3
"""Inspect NFS sequences using OSTrack's NFS metadata."""

from __future__ import annotations

import argparse
import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NFS_DATASET_PY = ROOT / "external" / "OSTrack" / "lib" / "test" / "evaluation" / "nfsdataset.py"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Inspect NFS sequence validity.")
    parser.add_argument("--nfs_root", required=True, type=Path)
    parser.add_argument("--max_sequences", type=int, default=None)
    parser.add_argument("--candidates", nargs="*", default=None)
    return parser.parse_args()


def load_nfs_sequence_info() -> list[dict]:
    module = ast.parse(NFS_DATASET_PY.read_text(encoding="utf-8"))
    for node in ast.walk(module):
        if isinstance(node, ast.FunctionDef) and node.name == "_get_sequence_info_list":
            for child in ast.walk(node):
                if isinstance(child, ast.Assign):
                    for target in child.targets:
                        if isinstance(target, ast.Name) and target.id == "sequence_info_list":
                            return ast.literal_eval(child.value)
    raise RuntimeError(f"Could not parse sequence_info_list from {NFS_DATASET_PY}")


def count_nonempty_lines(path: Path) -> int:
    if not path.is_file():
        return 0
    return sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip())


def inspect_sequence(nfs_root: Path, info: dict) -> dict[str, object]:
    start = int(info["startFrame"]) + int(info.get("initOmit", 0))
    end = int(info["endFrame"])
    nz = int(info["nz"])
    ext = str(info["ext"])
    expected_frames = end - start + 1
    seq_dir = nfs_root / info["path"]
    anno_path = nfs_root / info["anno_path"]
    first_image = seq_dir / f"{start:0{nz}}.{ext}"
    last_image = seq_dir / f"{end:0{nz}}.{ext}"
    gt_lines = max(0, count_nonempty_lines(anno_path) - int(info.get("initOmit", 0)))
    zip_hint = nfs_root / f"{Path(info['path']).name}.zip"
    valid = (
        seq_dir.is_dir()
        and anno_path.is_file()
        and first_image.is_file()
        and last_image.is_file()
        and expected_frames > 0
        and gt_lines == expected_frames
    )
    return {
        "name": info["name"],
        "object_class": info.get("object_class", ""),
        "frames": expected_frames,
        "gt_lines": gt_lines,
        "valid": valid,
        "zip_present": zip_hint.is_file(),
        "path": info["path"],
    }


def print_table(rows: list[dict[str, object]]) -> None:
    columns = ["name", "object_class", "frames", "gt_lines", "valid", "zip_present", "path"]
    widths = {column: max(len(column), *(len(str(row[column])) for row in rows)) for column in columns}
    print("  ".join(column.ljust(widths[column]) for column in columns))
    print("  ".join("-" * widths[column] for column in columns))
    for row in rows:
        print("  ".join(str(row[column]).ljust(widths[column]) for column in columns))


def main() -> int:
    args = parse_args()
    infos = load_nfs_sequence_info()
    if args.candidates:
        wanted = set(args.candidates)
        infos = [info for info in infos if info["name"] in wanted]
        missing = sorted(wanted - {info["name"] for info in infos})
        if missing:
            raise ValueError(f"Unknown NFS candidate sequence names: {missing}")

    rows = [inspect_sequence(args.nfs_root, info) for info in infos]
    if args.max_sequences is not None:
        rows = rows[: args.max_sequences]
    print_table(rows)

    recommended = [str(row["name"]) for row in rows if row["valid"]][:10]
    if not recommended:
        recommended = [str(row["name"]) for row in rows if row["zip_present"]][:10]
    print()
    print(f"NFS root: {args.nfs_root}")
    print(f"Valid extracted sequences shown: {sum(1 for row in rows if row['valid'])}/{len(rows)}")
    print("Recommended sequences:", ", ".join(recommended) if recommended else "none")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
