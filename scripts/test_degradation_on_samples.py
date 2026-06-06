"""Apply every supported degradation and severity to real sample images."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.degradations.pipeline import apply_degradation
from src.degradations.protocols import SEVERITIES, load_protocol


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp"}
DEGRADATION_LABELS = [
    ("motion_blur", "motion_blur"),
    ("defocus_blur", "defocus_blur"),
    ("gaussian_noise", "gaussian_noise"),
    ("sensor_noise", "sensor_noise"),
    ("low_resolution", "low_resolution"),
    ("jpeg_compression", "jpeg_compression"),
    ("low_light", "low_light"),
    ("mixed_degradation", "mixed"),
]


def iter_images(input_dir: Path) -> list[Path]:
    if not input_dir.exists():
        return []
    return sorted(p for p in input_dir.iterdir() if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS)


def safe_stem(path: Path) -> str:
    return path.stem.replace(" ", "_")


def write_jsonl_record(handle, record: dict[str, Any]) -> None:
    handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Test degradations on real sample images.")
    parser.add_argument("--input_dir", default="samples/raw_images", help="Folder containing sample images.")
    parser.add_argument("--output_dir", default="outputs/real_sample_degradation", help="Output folder.")
    parser.add_argument("--protocol", default="configs/degradation_protocol.json", help="Protocol JSON path.")
    parser.add_argument("--seed", type=int, default=123, help="Base random seed.")
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    protocol = load_protocol(args.protocol)
    images = iter_images(input_dir)
    metadata_path = output_dir / "metadata.jsonl"
    generated = 0
    failures: list[dict[str, str]] = []

    with metadata_path.open("w", encoding="utf-8", newline="\n") as metadata_file:
        for image_index, image_path in enumerate(images):
            try:
                original = Image.open(image_path).convert("RGB")
            except Exception as exc:  # pragma: no cover - defensive for corrupt samples
                failures.append({"image": str(image_path), "error": str(exc)})
                continue

            for degradation_index, (label, api_type) in enumerate(DEGRADATION_LABELS):
                for severity_index, severity in enumerate(SEVERITIES):
                    seed = args.seed + image_index * 1000 + degradation_index * 10 + severity_index
                    output_name = f"{safe_stem(image_path)}__{label}__{severity}.png"
                    output_path = output_dir / output_name
                    try:
                        degraded, metadata = apply_degradation(original, api_type, severity, seed=seed)
                        if degraded.size != original.size:
                            raise RuntimeError(f"size changed from {original.size} to {degraded.size}")
                        degraded.save(output_path)
                        write_jsonl_record(
                            metadata_file,
                            {
                                "input": str(image_path),
                                "output": str(output_path),
                                "original_size": list(original.size),
                                "output_size": list(degraded.size),
                                "requested_degradation": label,
                                "api_degradation_type": api_type,
                                "metadata": metadata,
                            },
                        )
                        generated += 1
                    except Exception as exc:  # pragma: no cover - defensive for unexpected image modes/files
                        failures.append(
                            {
                                "image": str(image_path),
                                "degradation": label,
                                "severity": severity,
                                "error": str(exc),
                            }
                        )

    print(f"Input directory: {input_dir}")
    print(f"Protocol: {protocol.get('name', args.protocol)}")
    print(f"Input images: {len(images)}")
    print(f"Degraded images generated: {generated}")
    print(f"Output directory: {output_dir}")
    print(f"Metadata JSONL: {metadata_path}")
    print(f"Failures: {len(failures)}")
    if failures:
        for failure in failures[:10]:
            print(f"  - {failure}")
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
