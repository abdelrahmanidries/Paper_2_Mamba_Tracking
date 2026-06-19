#!/usr/bin/env python3
"""Verify a normalized NFS root contains one canonical XYWH row per frame."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.evaluation.nfs_annotations import get_sequence_info, metadata_frame_paths
from scripts.evaluate_tracking_result import load_boxes


DEFAULT_SEQUENCES = [
    "nfs_cheetah",
    "nfs_walking",
    "nfs_Gymnastics",
    "nfs_basketball_player",
    "nfs_bottle",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verify normalized NFS annotation root.")
    parser.add_argument("--nfs_root", required=True, type=Path)
    parser.add_argument("--sequences", nargs="*", default=DEFAULT_SEQUENCES)
    parser.add_argument("--check_loader", action="store_true")
    return parser.parse_args()


def verify_sequence(root: Path, sequence: str) -> dict[str, object]:
    info = get_sequence_info(sequence)
    frames = metadata_frame_paths(root, info)
    missing = [path for path in frames if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"Missing normalized frame for {sequence}: {missing[0]}")
    anno = root / info.anno_path
    if not anno.is_file():
        raise FileNotFoundError(f"Missing normalized annotation for {sequence}: {anno}")
    boxes = load_boxes(anno)
    if len(boxes) != len(frames):
        raise ValueError(f"Annotation/frame mismatch for {sequence}: anno={len(boxes)} frames={len(frames)}")
    if boxes.shape[1] != 4:
        raise ValueError(f"Expected 4-column XYWH annotation for {sequence}: {boxes.shape}")
    if np.any(boxes[:, 2] <= 0) or np.any(boxes[:, 3] <= 0):
        raise ValueError(f"Non-positive normalized XYWH size for {sequence}")
    if sequence == "nfs_cheetah" and boxes.shape != (167, 4):
        raise ValueError(f"Expected nfs_cheetah normalized shape (167,4), got {boxes.shape}")
    if sequence == "nfs_walking" and boxes.shape != (555, 4):
        raise ValueError(f"Expected nfs_walking normalized shape (555,4), got {boxes.shape}")
    if sequence == "nfs_cheetah":
        expected = np.array([525.0, 286.0, 420.0, 230.0])
        if not np.allclose(boxes[0], expected):
            raise ValueError(f"nfs_cheetah first row is not corrected XYWH: got {boxes[0].tolist()} expected {expected.tolist()}")
    if sequence == "nfs_walking":
        expected = np.array([270.0, 457.0, 92.0, 278.0])
        if not np.allclose(boxes[0], expected):
            raise ValueError(f"nfs_walking first row is not corrected XYWH: got {boxes[0].tolist()} expected {expected.tolist()}")
    return {"sequence": sequence, "frames": len(frames), "annotations": len(boxes), "first_row": boxes[0].tolist()}


def main() -> int:
    args = parse_args()
    if not args.nfs_root.is_dir():
        raise FileNotFoundError(f"Normalized NFS root not found: {args.nfs_root}")
    manifest = args.nfs_root / "normalization_manifest.json"
    if manifest.is_file():
        data = json.loads(manifest.read_text(encoding="utf-8"))
        print(f"manifest_sequences: {len(data.get('sequences', []))}")
    else:
        print(f"warning: manifest not found: {manifest}")

    rows = [verify_sequence(args.nfs_root, sequence) for sequence in args.sequences]
    for row in rows:
        print(f"{row['sequence']}: frames={row['frames']} annotations={row['annotations']} first_row={row['first_row']}")
    print("verification: normalized NFS root passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
