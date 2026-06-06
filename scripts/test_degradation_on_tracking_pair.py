"""Generate template-search degradation cases for one real tracking pair."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.degradations.pipeline import apply_pair_degradation
from src.degradations.protocols import SEVERITIES, load_protocol


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


def safe_label(text: str) -> str:
    return text.replace(" ", "_").replace("/", "_").replace("\\", "_")


def resize_for_display(image: Image.Image, target_height: int) -> Image.Image:
    width, height = image.size
    if height == target_height:
        return image.copy()
    scale = target_height / float(height)
    new_size = (max(1, int(round(width * scale))), target_height)
    return image.resize(new_size, Image.Resampling.BICUBIC)


def labeled_panel(image: Image.Image, label: str, target_height: int) -> Image.Image:
    display = resize_for_display(image.convert("RGB"), target_height)
    label_height = 24
    panel = Image.new("RGB", (display.width, display.height + label_height), (255, 255, 255))
    panel.paste(display, (0, label_height))
    draw = ImageDraw.Draw(panel)
    draw.text((6, 5), label, fill=(0, 0, 0))
    return panel


def make_comparison(
    original_template: Image.Image,
    degraded_template: Image.Image,
    original_search: Image.Image,
    degraded_search: Image.Image,
) -> Image.Image:
    target_height = min(260, max(original_template.height, degraded_template.height, original_search.height, degraded_search.height))
    panels = [
        labeled_panel(original_template, "original template", target_height),
        labeled_panel(degraded_template, "degraded template", target_height),
        labeled_panel(original_search, "original search", target_height),
        labeled_panel(degraded_search, "degraded search", target_height),
    ]
    gap = 8
    width = sum(panel.width for panel in panels) + gap * (len(panels) - 1)
    height = max(panel.height for panel in panels)
    canvas = Image.new("RGB", (width, height), (235, 235, 235))
    x = 0
    for panel in panels:
        canvas.paste(panel, (x, 0))
        x += panel.width + gap
    return canvas


def write_record(handle, record: dict[str, Any]) -> None:
    handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def build_cases() -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = []
    for severity in SEVERITIES:
        cases.append(
            {
                "mode": "clean",
                "label": "clean",
                "api_degradation_type": "clean",
                "severity": severity,
            }
        )
        for index, (label, api_type) in enumerate(DEGRADATION_LABELS):
            cases.append(
                {
                    "mode": "search_only",
                    "label": label,
                    "api_degradation_type": api_type,
                    "severity": severity,
                }
            )
            cases.append(
                {
                    "mode": "template_only",
                    "label": label,
                    "api_degradation_type": api_type,
                    "severity": severity,
                }
            )
            cases.append(
                {
                    "mode": "both_same",
                    "label": label,
                    "api_degradation_type": api_type,
                    "severity": severity,
                }
            )
            next_label, next_api_type = DEGRADATION_LABELS[(index + 1) % len(DEGRADATION_LABELS)]
            cases.append(
                {
                    "mode": "both_different",
                    "label": f"{label}_vs_{next_label}",
                    "api_degradation_type": (api_type, next_api_type),
                    "severity": severity,
                }
            )
    return cases


def main() -> int:
    parser = argparse.ArgumentParser(description="Test degradations on one template-search pair.")
    parser.add_argument("--template", required=True, help="Template image path.")
    parser.add_argument("--search", required=True, help="Search image path.")
    parser.add_argument("--output_dir", default="outputs/tracking_pair_degradation", help="Output folder.")
    parser.add_argument("--protocol", default="configs/degradation_protocol.json", help="Protocol JSON path.")
    parser.add_argument("--seed", type=int, default=123, help="Base random seed.")
    args = parser.parse_args()

    template_path = Path(args.template)
    search_path = Path(args.search)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if not template_path.exists():
        raise FileNotFoundError(f"Template image not found: {template_path}")
    if not search_path.exists():
        raise FileNotFoundError(f"Search image not found: {search_path}")

    protocol = load_protocol(args.protocol)
    original_template = Image.open(template_path).convert("RGB")
    original_search = Image.open(search_path).convert("RGB")

    metadata_path = output_dir / "metadata.jsonl"
    generated_cases = 0
    failures: list[dict[str, str]] = []

    with metadata_path.open("w", encoding="utf-8", newline="\n") as metadata_file:
        for index, case in enumerate(build_cases()):
            mode = case["mode"]
            label = safe_label(case["label"])
            severity = case["severity"]
            seed = args.seed + index
            prefix = f"{mode}__{label}__{severity}"
            template_output = output_dir / f"{prefix}__template.png"
            search_output = output_dir / f"{prefix}__search.png"
            comparison_output = output_dir / f"{prefix}__comparison.png"

            try:
                degraded_template, degraded_search, metadata = apply_pair_degradation(
                    original_template,
                    original_search,
                    mode=mode,
                    degradation_type=case["api_degradation_type"],
                    severity=severity,
                    seed=seed,
                )
                if degraded_template.size != original_template.size:
                    raise RuntimeError("template size changed")
                if degraded_search.size != original_search.size:
                    raise RuntimeError("search size changed")

                degraded_template.save(template_output)
                degraded_search.save(search_output)
                comparison = make_comparison(original_template, degraded_template, original_search, degraded_search)
                comparison.save(comparison_output)

                write_record(
                    metadata_file,
                    {
                        "template_input": str(template_path),
                        "search_input": str(search_path),
                        "template_output": str(template_output),
                        "search_output": str(search_output),
                        "comparison_output": str(comparison_output),
                        "mode": mode,
                        "label": label,
                        "severity": severity,
                        "template_original_size": list(original_template.size),
                        "search_original_size": list(original_search.size),
                        "template_output_size": list(degraded_template.size),
                        "search_output_size": list(degraded_search.size),
                        "metadata": metadata,
                    },
                )
                generated_cases += 1
            except Exception as exc:  # pragma: no cover - defensive for corrupt inputs
                failures.append({"case": prefix, "error": str(exc)})

    print(f"Template: {template_path}")
    print(f"Search: {search_path}")
    print(f"Protocol: {protocol.get('name', args.protocol)}")
    print(f"Generated cases: {generated_cases}")
    print(f"Images generated: {generated_cases * 3}")
    print(f"Output directory: {output_dir}")
    print(f"Metadata JSONL: {metadata_path}")
    print(f"Failures: {len(failures)}")
    if failures:
        for failure in failures[:10]:
            print(f"  - {failure}")
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
