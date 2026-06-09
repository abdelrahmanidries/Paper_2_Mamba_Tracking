"""Inspect candidate OTB sequences for frame/ground-truth count sanity."""

from __future__ import annotations

import argparse
from pathlib import Path


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Inspect OTB candidate sequences.")
    parser.add_argument("--otb_root", required=True, type=Path)
    parser.add_argument("--candidates", required=True, nargs="+")
    return parser.parse_args()


def count_gt_lines(path: Path) -> int:
    if not path.is_file():
        return 0
    return sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip())


def count_frames(img_dir: Path) -> tuple[int, Path | None]:
    if not img_dir.is_dir():
        return 0, None
    frames = sorted(
        path
        for path in img_dir.iterdir()
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
    )
    first = frames[0] if frames else None
    return len(frames), first


def main() -> int:
    args = parse_args()
    rows = []
    recommendation = None

    for sequence in args.candidates:
        seq_dir = args.otb_root / sequence
        img_dir = seq_dir / "img"
        gt_path = seq_dir / "groundtruth_rect.txt"
        frame_count, first_image = count_frames(img_dir)
        gt_count = count_gt_lines(gt_path)
        first_exists = first_image is not None and first_image.is_file()
        counts_match = frame_count > 0 and frame_count == gt_count
        valid = seq_dir.is_dir() and img_dir.is_dir() and gt_path.is_file() and first_exists and counts_match

        if recommendation is None and valid:
            recommendation = sequence

        rows.append(
            {
                "sequence": sequence,
                "frames": str(frame_count),
                "gt_lines": str(gt_count),
                "first_image": "yes" if first_exists else "no",
                "counts_match": "yes" if counts_match else "no",
                "valid": "yes" if valid else "no",
            }
        )

    columns = ["sequence", "frames", "gt_lines", "first_image", "counts_match", "valid"]
    widths = {
        column: max(len(column), *(len(row[column]) for row in rows))
        for column in columns
    }
    print("  ".join(column.ljust(widths[column]) for column in columns))
    print("  ".join("-" * widths[column] for column in columns))
    for row in rows:
        print("  ".join(row[column].ljust(widths[column]) for column in columns))

    if recommendation is None:
        print("Recommended sequence: none")
        return 1

    print(f"Recommended sequence: {recommendation}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
