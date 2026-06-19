#!/usr/bin/env python3
"""Create an OSTrack-compatible normalized NFS root without modifying source data."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.evaluation.nfs_annotations import (
    dump_manifest,
    get_sequence_info,
    load_canonical_nfs_ground_truth,
    load_sequence_metadata,
    manifest_record,
    write_xywh_annotations,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Prepare a normalized NFS root with aligned XYWH annotations.")
    parser.add_argument("--raw_nfs_root", required=True, type=Path)
    parser.add_argument("--output_root", required=True, type=Path)
    parser.add_argument("--sequences", nargs="*", default=None)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--check_only", action="store_true")
    return parser.parse_args()


def link_or_copy(src: Path, dst: Path, is_dir: bool) -> str:
    if dst.exists() or dst.is_symlink():
        if dst.is_symlink() or dst.is_file():
            dst.unlink()
        else:
            shutil.rmtree(dst)
    dst.parent.mkdir(parents=True, exist_ok=True)
    try:
        dst.symlink_to(src.resolve(), target_is_directory=is_dir)
        return "symlink"
    except OSError:
        if is_dir:
            shutil.copytree(src, dst, symlinks=True)
            return "copytree"
        shutil.copy2(src, dst)
        return "copy"


def main() -> int:
    args = parse_args()
    if not args.raw_nfs_root.is_dir():
        raise FileNotFoundError(f"Raw NFS root not found: {args.raw_nfs_root}")
    if not (args.raw_nfs_root / "sequences").is_dir() or not (args.raw_nfs_root / "anno").is_dir():
        raise FileNotFoundError(f"Expected extracted NFS root with sequences/ and anno/: {args.raw_nfs_root}")
    if args.output_root.exists() and any(args.output_root.iterdir()) and not args.overwrite and not args.check_only:
        raise FileExistsError(f"Output root is not empty. Use --overwrite: {args.output_root}")

    selected = args.sequences or [info.name for info in load_sequence_metadata()]
    records = []
    for sequence in selected:
        info = get_sequence_info(sequence)
        bundle = load_canonical_nfs_ground_truth(args.raw_nfs_root, sequence)
        out_anno = args.output_root / info.anno_path
        records.append(manifest_record(bundle, out_anno))
        if args.check_only:
            print(
                f"[check] {sequence}: raw={bundle.raw_annotation_count} images={bundle.image_count} "
                f"aligned={bundle.aligned_annotation_count} stride={bundle.sampling_stride}"
            )
            continue
        link_or_copy(args.raw_nfs_root / info.path, args.output_root / info.path, is_dir=True)
        write_xywh_annotations(out_anno, bundle.gt_xywh)
        print(
            f"normalized {sequence}: raw={bundle.raw_annotation_count} images={bundle.image_count} "
            f"aligned={bundle.aligned_annotation_count} stride={bundle.sampling_stride}"
        )

    if not args.check_only:
        dump_manifest(args.output_root / "normalization_manifest.json", records)
        print(f"Output root: {args.output_root}")
        print(f"Manifest: {args.output_root / 'normalization_manifest.json'}")
    print(f"Sequences checked: {len(records)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
