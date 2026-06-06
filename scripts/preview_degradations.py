"""Generate preview images for the synthetic degradation pipeline."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.degradations.pipeline import apply_degradation
from src.degradations.protocols import SEVERITIES


DEGRADATION_TYPES = [
    "motion_blur",
    "defocus_blur",
    "gaussian_noise",
    "sensor_noise",
    "low_resolution",
    "jpeg_compression",
    "low_light",
    "mixed",
]


def make_test_image(size: tuple[int, int] = (320, 220)) -> Image.Image:
    width, height = size
    image = Image.new("RGB", size, (245, 245, 245))
    draw = ImageDraw.Draw(image)
    draw.rectangle((20, 20, width - 20, height - 20), outline=(20, 20, 20), width=3)
    draw.rectangle((45, 55, 150, 155), fill=(220, 40, 40), outline=(90, 0, 0), width=3)
    draw.ellipse((185, 45, 275, 135), fill=(40, 130, 220), outline=(0, 50, 110), width=3)
    draw.line((20, height - 45, width - 20, height - 70), fill=(20, 160, 80), width=5)
    draw.text((35, height - 35), "RGB tracking target / distractors", fill=(0, 0, 0))
    return image


def load_input(path: str | None) -> Image.Image:
    if path is None:
        return make_test_image()
    return Image.open(path).convert("RGB")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate synthetic degradation previews.")
    parser.add_argument("--input", type=str, default=None, help="Optional input image path.")
    parser.add_argument("--out", type=str, default="outputs/degradation_preview", help="Output folder.")
    parser.add_argument("--seed", type=int, default=123, help="Base random seed.")
    args = parser.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    image = load_input(args.input)

    records = []
    clean_path = out_dir / "clean_reference.png"
    image.save(clean_path)
    records.append({"output": str(clean_path), "degradation_type": "clean", "severity": "none"})

    for degradation_type in DEGRADATION_TYPES:
        for sev_index, severity in enumerate(SEVERITIES):
            seed = args.seed + len(records) + sev_index
            degraded, metadata = apply_degradation(image, degradation_type, severity, seed=seed)
            filename = f"{degradation_type}_{severity}.png"
            output_path = out_dir / filename
            degraded.save(output_path)
            records.append({"output": str(output_path), "metadata": metadata})

    metadata_path = out_dir / "metadata.json"
    with metadata_path.open("w", encoding="utf-8", newline="\n") as f:
        json.dump({"input": args.input, "outputs": records}, f, indent=2)
        f.write("\n")

    print(f"Saved {len(records)} preview images/records to {out_dir}")
    print(f"Metadata: {metadata_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
