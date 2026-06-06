"""Protocol configuration for tracking-pair degradations."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


SEVERITIES = ("mild", "medium", "severe")
DEGRADATION_TYPES = (
    "clean",
    "motion_blur",
    "defocus_blur",
    "gaussian_noise",
    "sensor_noise",
    "low_resolution",
    "jpeg_compression",
    "low_light",
    "mixed",
)
PAIR_MODES = ("clean", "search_only", "template_only", "both_same", "both_different")


def get_default_protocol() -> dict[str, Any]:
    """Return the default degradation protocol used for minimal POC tests."""

    return {
        "name": "minimal_rgb_tracking_degradation_protocol",
        "default_seed": 123,
        "enabled_degradations": [
            "motion_blur",
            "defocus_blur",
            "gaussian_noise",
            "sensor_noise",
            "low_resolution",
            "jpeg_compression",
            "low_light",
            "mixed",
        ],
        "degradation_probabilities": {
            "motion_blur": 0.16,
            "defocus_blur": 0.10,
            "gaussian_noise": 0.16,
            "sensor_noise": 0.10,
            "low_resolution": 0.16,
            "jpeg_compression": 0.16,
            "low_light": 0.08,
            "mixed": 0.08,
        },
        "severity_probabilities": {
            "mild": 0.4,
            "medium": 0.4,
            "severe": 0.2,
        },
        "pair_mode_probabilities": {
            "search_only": 0.4,
            "template_only": 0.15,
            "both_same": 0.2,
            "both_different": 0.2,
            "clean": 0.05,
        },
        "mixed_degradation_rules": {
            "mild": {"min_count": 2, "max_count": 2},
            "medium": {"min_count": 2, "max_count": 3},
            "severe": {"min_count": 3, "max_count": 3},
        },
    }


def _validate_probability_map(name: str, values: dict[str, Any], allowed: tuple[str, ...]) -> None:
    if not isinstance(values, dict) or not values:
        raise ValueError(f"{name} must be a non-empty dictionary")
    unknown = sorted(set(values) - set(allowed))
    if unknown:
        raise ValueError(f"{name} contains unknown keys: {unknown}")
    total = 0.0
    for key, value in values.items():
        if not isinstance(value, (int, float)):
            raise ValueError(f"{name}.{key} must be numeric")
        if value < 0:
            raise ValueError(f"{name}.{key} must be non-negative")
        total += float(value)
    if total <= 0:
        raise ValueError(f"{name} must have positive total probability")


def validate_protocol(protocol: dict[str, Any]) -> bool:
    """Validate a protocol dictionary.

    Raises ValueError for invalid protocols and returns True otherwise.
    """

    if not isinstance(protocol, dict):
        raise ValueError("Protocol must be a dictionary")

    enabled = protocol.get("enabled_degradations")
    if not isinstance(enabled, list) or not enabled:
        raise ValueError("enabled_degradations must be a non-empty list")
    unknown = sorted(set(enabled) - set(DEGRADATION_TYPES))
    if unknown:
        raise ValueError(f"Unknown enabled degradations: {unknown}")
    if "clean" in enabled:
        raise ValueError("clean should be controlled by pair mode, not enabled_degradations")

    _validate_probability_map(
        "severity_probabilities",
        protocol.get("severity_probabilities", {}),
        SEVERITIES,
    )
    _validate_probability_map(
        "pair_mode_probabilities",
        protocol.get("pair_mode_probabilities", {}),
        PAIR_MODES,
    )

    degradation_probs = protocol.get("degradation_probabilities")
    if degradation_probs is not None:
        _validate_probability_map("degradation_probabilities", degradation_probs, DEGRADATION_TYPES)
        missing = sorted(set(enabled) - set(degradation_probs))
        if missing:
            raise ValueError(f"degradation_probabilities missing enabled degradations: {missing}")

    rules = protocol.get("mixed_degradation_rules", {})
    if rules:
        if not isinstance(rules, dict):
            raise ValueError("mixed_degradation_rules must be a dictionary")
        for severity in SEVERITIES:
            if severity not in rules:
                raise ValueError(f"mixed_degradation_rules missing {severity}")
            item = rules[severity]
            if item.get("min_count", 0) < 1 or item.get("max_count", 0) < item.get("min_count", 0):
                raise ValueError(f"Invalid mixed_degradation_rules for {severity}")

    return True


def load_protocol(path: str | Path) -> dict[str, Any]:
    path = Path(path)
    with path.open("r", encoding="utf-8") as f:
        protocol = json.load(f)
    validate_protocol(protocol)
    return protocol


def save_protocol(protocol: dict[str, Any], path: str | Path) -> None:
    validate_protocol(protocol)
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as f:
        json.dump(protocol, f, indent=2)
        f.write("\n")
