from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest
from PIL import Image

from src.degradations.pipeline import apply_degradation, apply_pair_degradation, degrade_tracking_pair
from src.degradations.protocols import DEGRADATION_TYPES, PAIR_MODES, load_protocol, validate_protocol


DEGRADATIONS = [d for d in DEGRADATION_TYPES if d != "clean"]


def make_image(size: tuple[int, int] = (96, 64)) -> Image.Image:
    width, height = size
    x = np.linspace(0, 255, width, dtype=np.float32)
    y = np.linspace(0, 255, height, dtype=np.float32)[:, None]
    arr = np.zeros((height, width, 3), dtype=np.uint8)
    arr[:, :, 0] = x[None, :]
    arr[:, :, 1] = y
    arr[:, :, 2] = ((x[None, :] + y) / 2).astype(np.uint8)
    arr[18:44, 25:67, :] = np.array([220, 40, 40], dtype=np.uint8)
    return Image.fromarray(arr, mode="RGB")


def assert_valid_rgb_image(image: Image.Image, size: tuple[int, int]) -> None:
    assert isinstance(image, Image.Image)
    assert image.size == size
    assert image.mode == "RGB"
    arr = np.asarray(image)
    assert arr.dtype == np.uint8
    assert int(arr.min()) >= 0
    assert int(arr.max()) <= 255


@pytest.mark.parametrize("degradation_type", DEGRADATIONS)
def test_every_degradation_runs_without_error(degradation_type: str) -> None:
    image = make_image()
    degraded, metadata = apply_degradation(image, degradation_type, "medium", seed=7)
    assert_valid_rgb_image(degraded, image.size)
    assert isinstance(metadata, dict)
    assert metadata["degradation_type"] == degradation_type
    assert metadata["severity"] == "medium"
    assert "parameters" in metadata
    assert "seed" in metadata


def test_numpy_array_input_is_supported() -> None:
    image = np.asarray(make_image())
    degraded, metadata = apply_degradation(image, "gaussian_noise", "mild", seed=1)
    assert_valid_rgb_image(degraded, (96, 64))
    assert metadata["degradation_type"] == "gaussian_noise"


@pytest.mark.parametrize("mode", PAIR_MODES)
def test_pair_modes_work(mode: str) -> None:
    template = make_image((80, 60))
    search = make_image((120, 90))
    degradation_type: str | tuple[str, str] = "motion_blur"
    if mode == "both_different":
        degradation_type = ("motion_blur", "gaussian_noise")

    out_template, out_search, metadata = apply_pair_degradation(
        template,
        search,
        mode=mode,
        degradation_type=degradation_type,
        severity="medium",
        seed=11,
    )
    assert_valid_rgb_image(out_template, template.size)
    assert_valid_rgb_image(out_search, search.size)
    assert metadata["mode"] == mode
    assert "template" in metadata
    assert "search" in metadata
    assert metadata["bbox_note"].startswith("image size is preserved")


def test_same_seed_is_deterministic_for_stochastic_degradation() -> None:
    image = make_image()
    first, first_meta = apply_degradation(image, "gaussian_noise", "severe", seed=123)
    second, second_meta = apply_degradation(image, "gaussian_noise", "severe", seed=123)
    assert np.array_equal(np.asarray(first), np.asarray(second))
    assert first_meta == second_meta


def test_different_seeds_can_change_stochastic_degradation() -> None:
    image = make_image()
    first, _ = apply_degradation(image, "gaussian_noise", "severe", seed=123)
    second, _ = apply_degradation(image, "gaussian_noise", "severe", seed=124)
    assert not np.array_equal(np.asarray(first), np.asarray(second))


def test_low_resolution_returns_original_size() -> None:
    image = make_image((111, 77))
    degraded, metadata = apply_degradation(image, "low_resolution", "severe", seed=3)
    assert_valid_rgb_image(degraded, image.size)
    assert metadata["parameters"]["low_size"][0] < image.size[0]
    assert metadata["parameters"]["low_size"][1] < image.size[1]


def test_jpeg_compression_returns_valid_image() -> None:
    image = make_image()
    degraded, metadata = apply_degradation(image, "jpeg_compression", "medium", seed=3)
    assert_valid_rgb_image(degraded, image.size)
    assert metadata["parameters"]["quality"] == 40


def test_protocol_config_is_valid_json() -> None:
    path = Path("configs/degradation_protocol.json")
    data = json.loads(path.read_text(encoding="utf-8"))
    assert validate_protocol(data) is True
    assert load_protocol(path)["name"] == "minimal_rgb_tracking_degradation_protocol"


def test_degrade_tracking_pair_samples_protocol_deterministically() -> None:
    template = make_image((80, 60))
    search = make_image((120, 90))
    first_template, first_search, first_meta = degrade_tracking_pair(template, search, seed=99)
    second_template, second_search, second_meta = degrade_tracking_pair(template, search, seed=99)

    assert_valid_rgb_image(first_template, template.size)
    assert_valid_rgb_image(first_search, search.size)
    assert np.array_equal(np.asarray(first_template), np.asarray(second_template))
    assert np.array_equal(np.asarray(first_search), np.asarray(second_search))
    assert first_meta == second_meta
