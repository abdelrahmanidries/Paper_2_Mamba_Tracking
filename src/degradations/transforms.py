"""Individual synthetic image degradations for RGB tracking experiments.

Each transform accepts a PIL image or numpy array and returns a PIL RGB image
plus metadata. All transforms preserve the input image size, so tracking
bounding boxes do not need geometric adjustment.
"""

from __future__ import annotations

from io import BytesIO
from typing import Any

import numpy as np
from PIL import Image, ImageEnhance, ImageFilter


SEVERITIES = ("mild", "medium", "severe")


def _check_severity(severity: str) -> str:
    severity = str(severity).lower()
    if severity not in SEVERITIES:
        raise ValueError(f"Unsupported severity {severity!r}; expected one of {SEVERITIES}")
    return severity


def _rng(seed: int | None) -> np.random.Generator:
    return np.random.default_rng(seed)


def _to_pil_rgb(image: Image.Image | np.ndarray) -> Image.Image:
    if isinstance(image, Image.Image):
        return image.convert("RGB")

    arr = np.asarray(image)
    if arr.ndim == 2:
        arr = np.stack([arr, arr, arr], axis=-1)
    if arr.ndim != 3 or arr.shape[2] not in (1, 3, 4):
        raise ValueError("Expected image array with shape HxW, HxWx1, HxWx3, or HxWx4")
    if arr.shape[2] == 1:
        arr = np.repeat(arr, 3, axis=2)
    if arr.shape[2] == 4:
        arr = arr[:, :, :3]

    if np.issubdtype(arr.dtype, np.floating):
        max_value = float(np.nanmax(arr)) if arr.size else 1.0
        if max_value <= 1.0:
            arr = arr * 255.0
    arr = np.clip(arr, 0, 255).astype(np.uint8)
    return Image.fromarray(arr, mode="RGB")


def _to_array(image: Image.Image) -> np.ndarray:
    return np.asarray(image.convert("RGB"), dtype=np.float32)


def _from_array(arr: np.ndarray) -> Image.Image:
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), mode="RGB")


def _metadata(
    degradation_type: str,
    severity: str,
    parameters: dict[str, Any],
    seed: int | None,
    **extra: Any,
) -> dict[str, Any]:
    metadata = {
        "degradation_type": degradation_type,
        "severity": severity,
        "parameters": parameters,
        "seed": seed,
    }
    metadata.update(extra)
    return metadata


def motion_blur(
    image: Image.Image | np.ndarray,
    severity: str,
    angle: float | None = None,
    seed: int | None = None,
) -> tuple[Image.Image, dict[str, Any]]:
    """Apply linear motion blur with an odd-size rotated kernel."""

    severity = _check_severity(severity)
    pil = _to_pil_rgb(image)
    kernel_sizes = {"mild": 7, "medium": 13, "severe": 21}
    kernel_size = kernel_sizes[severity]
    rng = _rng(seed)
    if angle is None:
        angle = float(rng.uniform(0.0, 180.0))

    radius = kernel_size // 2
    theta = np.deg2rad(angle)
    offsets = np.linspace(-radius, radius, kernel_size)
    dx = np.rint(np.cos(theta) * offsets).astype(int)
    dy = np.rint(np.sin(theta) * offsets).astype(int)

    arr = _to_array(pil)
    padded = np.pad(arr, ((radius, radius), (radius, radius), (0, 0)), mode="edge")
    height, width = arr.shape[:2]
    accum = np.zeros_like(arr, dtype=np.float32)
    for shift_x, shift_y in zip(dx, dy):
        y0 = radius + shift_y
        x0 = radius + shift_x
        accum += padded[y0 : y0 + height, x0 : x0 + width, :]
    blurred = _from_array(accum / float(kernel_size))
    params = {"kernel_size": kernel_size, "angle": angle}
    return blurred.convert("RGB"), _metadata("motion_blur", severity, params, seed)


def defocus_blur(
    image: Image.Image | np.ndarray,
    severity: str,
    seed: int | None = None,
) -> tuple[Image.Image, dict[str, Any]]:
    """Approximate defocus blur with Gaussian blur."""

    severity = _check_severity(severity)
    pil = _to_pil_rgb(image)
    radii = {"mild": 1.5, "medium": 3.5, "severe": 6.0}
    radius = radii[severity]
    blurred = pil.filter(ImageFilter.GaussianBlur(radius=radius))
    return blurred.convert("RGB"), _metadata("defocus_blur", severity, {"radius": radius}, seed)


def gaussian_noise(
    image: Image.Image | np.ndarray,
    severity: str,
    seed: int | None = None,
) -> tuple[Image.Image, dict[str, Any]]:
    """Add zero-mean Gaussian noise."""

    severity = _check_severity(severity)
    pil = _to_pil_rgb(image)
    sigmas = {"mild": 8.0, "medium": 20.0, "severe": 40.0}
    sigma = sigmas[severity]
    noise = _rng(seed).normal(0.0, sigma, size=_to_array(pil).shape)
    out = _to_array(pil) + noise
    return _from_array(out), _metadata("gaussian_noise", severity, {"sigma": sigma}, seed)


def sensor_noise(
    image: Image.Image | np.ndarray,
    severity: str,
    seed: int | None = None,
) -> tuple[Image.Image, dict[str, Any]]:
    """Simulate signal-dependent shot noise plus additive read noise."""

    severity = _check_severity(severity)
    pil = _to_pil_rgb(image)
    presets = {
        "mild": {"peak_photons": 80.0, "read_sigma": 0.01},
        "medium": {"peak_photons": 35.0, "read_sigma": 0.025},
        "severe": {"peak_photons": 15.0, "read_sigma": 0.05},
    }
    params = presets[severity]
    rng = _rng(seed)
    arr = _to_array(pil) / 255.0
    shot = rng.poisson(arr * params["peak_photons"]) / params["peak_photons"]
    read = rng.normal(0.0, params["read_sigma"], size=arr.shape)
    out = (shot + read) * 255.0
    return _from_array(out), _metadata("sensor_noise", severity, dict(params), seed)


def low_resolution(
    image: Image.Image | np.ndarray,
    severity: str,
    seed: int | None = None,
) -> tuple[Image.Image, dict[str, Any]]:
    """Downsample then upsample to the original size."""

    severity = _check_severity(severity)
    pil = _to_pil_rgb(image)
    width, height = pil.size
    scales = {"mild": 0.75, "medium": 0.5, "severe": 0.25}
    scale = scales[severity]
    low_size = (max(1, int(round(width * scale))), max(1, int(round(height * scale))))
    down = pil.resize(low_size, Image.Resampling.BICUBIC)
    up = down.resize((width, height), Image.Resampling.BICUBIC)
    params = {"scale": scale, "low_size": list(low_size)}
    return up.convert("RGB"), _metadata("low_resolution", severity, params, seed)


def jpeg_compression(
    image: Image.Image | np.ndarray,
    severity: str,
    seed: int | None = None,
) -> tuple[Image.Image, dict[str, Any]]:
    """Apply in-memory JPEG compression."""

    severity = _check_severity(severity)
    pil = _to_pil_rgb(image)
    qualities = {"mild": 70, "medium": 40, "severe": 18}
    quality = qualities[severity]
    buffer = BytesIO()
    pil.save(buffer, format="JPEG", quality=quality)
    buffer.seek(0)
    out = Image.open(buffer).convert("RGB")
    return out, _metadata("jpeg_compression", severity, {"quality": quality}, seed)


def low_light(
    image: Image.Image | np.ndarray,
    severity: str,
    seed: int | None = None,
) -> tuple[Image.Image, dict[str, Any]]:
    """Reduce brightness/contrast and add mild noise."""

    severity = _check_severity(severity)
    pil = _to_pil_rgb(image)
    presets = {
        "mild": {"brightness": 0.75, "contrast": 0.85, "noise_sigma": 2.0},
        "medium": {"brightness": 0.5, "contrast": 0.75, "noise_sigma": 5.0},
        "severe": {"brightness": 0.3, "contrast": 0.65, "noise_sigma": 9.0},
    }
    params = presets[severity]
    out = ImageEnhance.Brightness(pil).enhance(params["brightness"])
    out = ImageEnhance.Contrast(out).enhance(params["contrast"])
    arr = _to_array(out)
    noise = _rng(seed).normal(0.0, params["noise_sigma"], size=arr.shape)
    return _from_array(arr + noise), _metadata("low_light", severity, dict(params), seed)


def mixed_degradation(
    image: Image.Image | np.ndarray,
    severity: str,
    seed: int | None = None,
) -> tuple[Image.Image, dict[str, Any]]:
    """Randomly combine two or three degradations."""

    severity = _check_severity(severity)
    rng = _rng(seed)
    available = [
        "motion_blur",
        "defocus_blur",
        "gaussian_noise",
        "sensor_noise",
        "low_resolution",
        "jpeg_compression",
        "low_light",
    ]
    count_probs = {"mild": (2, 2), "medium": (2, 3), "severe": (3, 3)}
    low_count, high_count = count_probs[severity]
    count = int(rng.integers(low_count, high_count + 1))
    chosen = rng.choice(available, size=count, replace=False).tolist()

    out = _to_pil_rgb(image)
    applied: list[dict[str, Any]] = []
    for degradation_type in chosen:
        sub_seed = int(rng.integers(0, 2**31 - 1))
        out, sub_meta = TRANSFORM_REGISTRY[degradation_type](out, severity, seed=sub_seed)
        applied.append(sub_meta)

    params = {"count": count, "order": chosen}
    return out.convert("RGB"), _metadata(
        "mixed",
        severity,
        params,
        seed,
        applied_degradations=applied,
    )


TRANSFORM_REGISTRY = {
    "motion_blur": motion_blur,
    "defocus_blur": defocus_blur,
    "gaussian_noise": gaussian_noise,
    "sensor_noise": sensor_noise,
    "low_resolution": low_resolution,
    "jpeg_compression": jpeg_compression,
    "low_light": low_light,
    "mixed": mixed_degradation,
}
