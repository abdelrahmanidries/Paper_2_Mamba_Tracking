"""Apply one synthetic degradation to every image in a folder."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.degradations.pipeline import apply_degradation
from src.degradations.protocols import DEGRADATION_TYPES, SEVERITIES


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp"}


def iter_images(input_dir: Path) -> list[Path]:
    return sorted(p for p in input_dir.iterdir() if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS)


def main() -> int:
    parser = argparse.ArgumentParser(description="Apply a synthetic degradation to an image folder.")
    parser.add_argument("--input_dir", required=True, help="Input folder of images.")
    parser.add_argument("--output_dir", required=True, help="Output folder for degraded images.")
    parser.add_argument("--type", required=True, choices=[d for d in DEGRADATION_TYPES if d != "clean"], help="Degradation type.")
    parser.add_argument("--severity", required=True, choices=list(SEVERITIES), help="Degradation severity.")
    parser.add_argument("--seed", type=int, default=None, help="Optional base random seed.")
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    if not input_dir.exists() or not input_dir.is_dir():
        raise FileNotFoundError(f"Input directory not found: {input_dir}")
    output_dir.mkdir(parents=True, exist_ok=True)

    images = iter_images(input_dir)
    metadata_path = output_dir / "metadata.jsonl"
    count = 0
    with metadata_path.open("w", encoding="utf-8", newline="\n") as meta_file:
        for index, image_path in enumerate(images):
            seed = None if args.seed is None else args.seed + index
            image = Image.open(image_path).convert("RGB")
            degraded, metadata = apply_degradation(image, args.type, args.severity, seed=seed)
            output_path = output_dir / image_path.name
            degraded.save(output_path)
            record = {
                "input": str(image_path),
                "output": str(output_path),
                "metadata": metadata,
            }
            meta_file.write(json.dumps(record) + "\n")
            count += 1

    print(f"Processed {count} images")
    print(f"Metadata JSONL: {metadata_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
