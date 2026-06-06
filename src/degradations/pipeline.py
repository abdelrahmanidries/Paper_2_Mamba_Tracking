"""Tracking-pair degradation pipeline."""

from __future__ import annotations

from typing import Any

import numpy as np
from PIL import Image

from .protocols import DEGRADATION_TYPES, PAIR_MODES, SEVERITIES, get_default_protocol, validate_protocol
from .transforms import TRANSFORM_REGISTRY, _to_pil_rgb


def _rng(seed: int | None) -> np.random.Generator:
    return np.random.default_rng(seed)


def _choice_from_probs(rng: np.random.Generator, probabilities: dict[str, float]) -> str:
    keys = list(probabilities.keys())
    weights = np.asarray([float(probabilities[k]) for k in keys], dtype=np.float64)
    if np.any(weights < 0) or float(weights.sum()) <= 0:
        raise ValueError("Probabilities must be non-negative with positive total")
    weights = weights / weights.sum()
    return str(rng.choice(keys, p=weights))


def _derive_seeds(seed: int | None, count: int) -> list[int | None]:
    if seed is None:
        return [None] * count
    rng = _rng(seed)
    return [int(rng.integers(0, 2**31 - 1)) for _ in range(count)]


def apply_degradation(
    image: Image.Image | np.ndarray,
    degradation_type: str,
    severity: str,
    seed: int | None = None,
) -> tuple[Image.Image, dict[str, Any]]:
    """Apply one degradation type to one RGB image."""

    degradation_type = str(degradation_type).lower()
    severity = str(severity).lower()
    if degradation_type not in DEGRADATION_TYPES:
        raise ValueError(f"Unsupported degradation_type {degradation_type!r}")
    if severity not in SEVERITIES:
        raise ValueError(f"Unsupported severity {severity!r}")

    pil = _to_pil_rgb(image)
    if degradation_type == "clean":
        return pil.copy(), {
            "degradation_type": "clean",
            "severity": severity,
            "parameters": {},
            "seed": seed,
        }

    return TRANSFORM_REGISTRY[degradation_type](pil, severity, seed=seed)


def apply_pair_degradation(
    template: Image.Image | np.ndarray,
    search: Image.Image | np.ndarray,
    mode: str,
    degradation_type: str | tuple[str, str] | list[str],
    severity: str | tuple[str, str] | list[str],
    seed: int | None = None,
) -> tuple[Image.Image, Image.Image, dict[str, Any]]:
    """Apply degradation to a template/search pair while preserving sizes."""

    mode = str(mode).lower()
    if mode not in PAIR_MODES:
        raise ValueError(f"Unsupported pair mode {mode!r}")

    template_pil = _to_pil_rgb(template)
    search_pil = _to_pil_rgb(search)
    template_seed, search_seed = _derive_seeds(seed, 2)

    if isinstance(severity, (list, tuple)):
        template_severity, search_severity = str(severity[0]).lower(), str(severity[1]).lower()
    else:
        template_severity = search_severity = str(severity).lower()

    if mode == "clean":
        clean_template, template_meta = apply_degradation(template_pil, "clean", template_severity, template_seed)
        clean_search, search_meta = apply_degradation(search_pil, "clean", search_severity, search_seed)
    elif mode == "search_only":
        clean_template, template_meta = apply_degradation(template_pil, "clean", template_severity, template_seed)
        clean_search, search_meta = apply_degradation(search_pil, str(degradation_type), search_severity, search_seed)
    elif mode == "template_only":
        clean_template, template_meta = apply_degradation(template_pil, str(degradation_type), template_severity, template_seed)
        clean_search, search_meta = apply_degradation(search_pil, "clean", search_severity, search_seed)
    elif mode == "both_same":
        clean_template, template_meta = apply_degradation(template_pil, str(degradation_type), template_severity, template_seed)
        clean_search, search_meta = apply_degradation(search_pil, str(degradation_type), search_severity, search_seed)
    else:
        if isinstance(degradation_type, (list, tuple)):
            template_type, search_type = str(degradation_type[0]).lower(), str(degradation_type[1]).lower()
        else:
            template_type = str(degradation_type).lower()
            candidates = [d for d in DEGRADATION_TYPES if d not in ("clean", template_type)]
            search_type = str(_rng(seed).choice(candidates))
        clean_template, template_meta = apply_degradation(template_pil, template_type, template_severity, template_seed)
        clean_search, search_meta = apply_degradation(search_pil, search_type, search_severity, search_seed)

    metadata = {
        "mode": mode,
        "seed": seed,
        "template": template_meta,
        "search": search_meta,
        "bbox_note": "image size is preserved; bounding boxes are unchanged",
    }
    return clean_template, clean_search, metadata


def sample_degradation_pair(protocol: dict[str, Any] | None = None, seed: int | None = None) -> dict[str, Any]:
    """Sample a tracking-pair degradation setting from a protocol."""

    protocol = get_default_protocol() if protocol is None else protocol
    validate_protocol(protocol)
    rng = _rng(seed if seed is not None else protocol.get("default_seed"))

    mode = _choice_from_probs(rng, protocol["pair_mode_probabilities"])
    severity = _choice_from_probs(rng, protocol["severity_probabilities"])

    enabled = list(protocol["enabled_degradations"])
    degradation_probs = protocol.get("degradation_probabilities")
    if degradation_probs:
        filtered = {k: float(v) for k, v in degradation_probs.items() if k in enabled}
        degradation_type = _choice_from_probs(rng, filtered)
    else:
        degradation_type = str(rng.choice(enabled))

    template_type = "clean"
    search_type = "clean"
    if mode == "search_only":
        search_type = degradation_type
    elif mode == "template_only":
        template_type = degradation_type
    elif mode == "both_same":
        template_type = search_type = degradation_type
    elif mode == "both_different":
        template_type = degradation_type
        candidates = [d for d in enabled if d != template_type]
        if not candidates:
            raise ValueError("both_different requires at least two enabled degradations")
        search_type = str(rng.choice(candidates))

    return {
        "mode": mode,
        "degradation_type": degradation_type,
        "severity": severity,
        "template_degradation_type": template_type,
        "search_degradation_type": search_type,
        "seed": seed,
    }


def degrade_tracking_pair(
    template: Image.Image | np.ndarray,
    search: Image.Image | np.ndarray,
    protocol: dict[str, Any] | None = None,
    seed: int | None = None,
) -> tuple[Image.Image, Image.Image, dict[str, Any]]:
    """Sample and apply a degradation protocol to a template/search pair."""

    sampled = sample_degradation_pair(protocol, seed=seed)
    mode = sampled["mode"]
    severity = sampled["severity"]
    if mode == "both_different":
        degradation_type: str | tuple[str, str] = (
            sampled["template_degradation_type"],
            sampled["search_degradation_type"],
        )
    else:
        degradation_type = sampled["degradation_type"]

    template_out, search_out, metadata = apply_pair_degradation(
        template,
        search,
        mode=mode,
        degradation_type=degradation_type,
        severity=severity,
        seed=seed,
    )
    metadata["sampled_protocol"] = sampled
    return template_out, search_out, metadata
