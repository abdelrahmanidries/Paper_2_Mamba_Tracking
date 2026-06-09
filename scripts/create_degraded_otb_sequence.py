"""Create a full OTB-style root with one degraded target sequence.

The output root mirrors all clean OTB sequence entries with symlinks, then
replaces the target sequence with generated frames:

    <output_root>/otb_<sequence>_<degradation>_<severity>/<sequence>/img
    <output_root>/otb_<sequence>_<degradation>_<severity>/<sequence>/groundtruth_rect.txt
    <output_root>/otb_<sequence>_<degradation>_<severity>/<sequence>/metadata.jsonl

Images keep their original names and dimensions, so OTB bounding boxes remain
unchanged.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.degradations.pipeline import apply_degradation
from src.degradations.protocols import DEGRADATION_TYPES, SEVERITIES


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a degraded OTB-style root for one sequence."
    )
    parser.add_argument("--clean_otb_root", required=True, type=Path)
    parser.add_argument("--sequence", required=True)
    parser.add_argument("--degradation", required=True, choices=list(DEGRADATION_TYPES))
    parser.add_argument("--severity", required=True)
    parser.add_argument("--seed", required=True, type=int)
    parser.add_argument("--output_root", required=True, type=Path)
    return parser.parse_args()


def iter_frames(img_dir: Path) -> list[Path]:
    return sorted(
        path
        for path in img_dir.iterdir()
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
    )


def count_nonempty_lines(path: Path) -> int:
    return sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip())


def link_or_copy(src: Path, dst: Path) -> str:
    if dst.exists() or dst.is_symlink():
        dst.unlink()
    try:
        dst.symlink_to(src.resolve())
        return "symlink"
    except OSError:
        shutil.copy2(src, dst)
        return "copy"


def remove_path(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)


def link_or_copy_sequence(src: Path, dst: Path) -> str:
    if dst.exists() or dst.is_symlink():
        remove_path(dst)
    try:
        dst.symlink_to(src.resolve(), target_is_directory=True)
        return "symlink"
    except OSError:
        shutil.copytree(src, dst, symlinks=True)
        return "copytree"


def mirror_clean_otb_sequences(clean_otb_root: Path, output_root: Path, target_sequence: str) -> int:
    output_root.mkdir(parents=True, exist_ok=True)
    count = 0
    for entry in sorted(clean_otb_root.iterdir()):
        if entry.name == target_sequence:
            continue
        if not entry.is_dir():
            continue
        link_or_copy_sequence(entry, output_root / entry.name)
        count += 1
    return count


def validate_args(args: argparse.Namespace) -> None:
    if args.degradation != "clean" and args.severity not in SEVERITIES:
        raise ValueError(
            f"Unsupported severity {args.severity!r}; expected one of {SEVERITIES}"
        )
    if args.degradation == "clean" and not args.severity:
        raise ValueError("--severity must be provided for metadata naming")

    sequence_dir = args.clean_otb_root / args.sequence
    img_dir = sequence_dir / "img"
    gt_path = sequence_dir / "groundtruth_rect.txt"
    if not img_dir.is_dir():
        raise FileNotFoundError(f"Clean image directory not found: {img_dir}")
    if not gt_path.is_file():
        raise FileNotFoundError(f"Clean ground truth not found: {gt_path}")


def main() -> int:
    args = parse_args()
    validate_args(args)

    clean_sequence_dir = args.clean_otb_root / args.sequence
    clean_img_dir = clean_sequence_dir / "img"
    clean_gt_path = clean_sequence_dir / "groundtruth_rect.txt"

    output_name = f"otb_{args.sequence}_{args.degradation}_{args.severity}"
    output_root = args.output_root / output_name
    output_sequence_dir = output_root / args.sequence
    output_img_dir = output_sequence_dir / "img"

    mirrored_count = mirror_clean_otb_sequences(args.clean_otb_root, output_root, args.sequence)
    if output_sequence_dir.exists() or output_sequence_dir.is_symlink():
        remove_path(output_sequence_dir)
    output_img_dir.mkdir(parents=True, exist_ok=True)

    output_gt_path = output_sequence_dir / "groundtruth_rect.txt"
    if output_gt_path.exists() or output_gt_path.is_symlink():
        output_gt_path.unlink()
    shutil.copy2(clean_gt_path, output_gt_path)

    frames = iter_frames(clean_img_dir)
    if not frames:
        raise FileNotFoundError(f"No image frames found in {clean_img_dir}")

    metadata_path = output_sequence_dir / "metadata.jsonl"
    processed = 0
    with metadata_path.open("w", encoding="utf-8", newline="\n") as metadata_file:
        for index, frame_path in enumerate(frames):
            output_path = output_img_dir / frame_path.name
            frame_seed = args.seed + index

            if args.degradation == "clean":
                method = link_or_copy(frame_path, output_path)
                with Image.open(frame_path) as image:
                    width, height = image.size
                metadata = {
                    "degradation_type": "clean",
                    "severity": args.severity,
                    "parameters": {},
                    "seed": frame_seed,
                    "copy_method": method,
                }
            else:
                if output_path.exists() or output_path.is_symlink():
                    output_path.unlink()
                with Image.open(frame_path) as image:
                    image = image.convert("RGB")
                    width, height = image.size
                    degraded, metadata = apply_degradation(
                        image,
                        args.degradation,
                        args.severity,
                        seed=frame_seed,
                    )
                    degraded_width, degraded_height = degraded.size
                    if (degraded_width, degraded_height) != (width, height):
                        raise RuntimeError(
                            "Degradation changed image size for "
                            f"{frame_path}: {(width, height)} -> "
                            f"{(degraded_width, degraded_height)}"
                        )
                    degraded.save(output_path)

            record = {
                "sequence": args.sequence,
                "frame_index": index,
                "input": str(frame_path),
                "output": str(output_path),
                "width": width,
                "height": height,
                "metadata": metadata,
            }
            metadata_file.write(json.dumps(record, sort_keys=True) + "\n")
            processed += 1

    gt_lines = count_nonempty_lines(output_gt_path)
    print(f"Output root: {output_root}")
    print(f"Mirrored non-target sequences: {mirrored_count}")
    print(f"Processed frames: {processed}")
    print(f"Ground-truth lines: {gt_lines}")
    print(f"Degradation type: {args.degradation}")
    print(f"Severity: {args.severity}")
    print(f"Seed: {args.seed}")
    print(f"Metadata JSONL: {metadata_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
