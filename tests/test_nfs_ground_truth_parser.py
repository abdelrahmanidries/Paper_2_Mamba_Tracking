from pathlib import Path

import numpy as np
import pytest

from src.evaluation.nfs_annotations import (
    alignment_indices,
    load_canonical_nfs_ground_truth,
    load_raw_nfs_annotations,
    validate_raw_xyxy,
    xyxy_to_xywh,
)


def test_xyxy_to_xywh_cheetah_representative_row():
    raw = np.array([[525.0, 286.0, 945.0, 516.0]])

    out = xyxy_to_xywh(raw)

    assert out.tolist() == [[525.0, 286.0, 420.0, 230.0]]


def test_xyxy_to_xywh_walking_representative_row():
    raw = np.array([[270.0, 457.0, 362.0, 735.0]])

    out = xyxy_to_xywh(raw)

    assert out.tolist() == [[270.0, 457.0, 92.0, 278.0]]


def test_exact_aligned_row_selection_for_dense_240fps_rows():
    indices, stride = alignment_indices(raw_count=1329, image_count=167, init_omit=0)

    assert stride == 8
    assert len(indices) == 167
    assert indices[:5] == [0, 8, 16, 24, 32]
    assert indices[-1] == 1328


def test_aligned_count_equals_image_count_for_walking():
    indices, stride = alignment_indices(raw_count=4433, image_count=555, init_omit=0)

    assert stride == 8
    assert len(indices) == 555
    assert indices[-1] == 4432


def test_invalid_negative_dimensions_rejected():
    raw = np.array([[525.0, 286.0, 500.0, 516.0]])

    with pytest.raises(ValueError):
        validate_raw_xyxy(raw)


def test_raw_xyxy_is_not_returned_as_canonical_xywh():
    raw = np.array([[525.0, 286.0, 945.0, 516.0]])

    out = xyxy_to_xywh(raw)

    assert out.tolist() != raw.tolist()
    assert out[0, 2] == 420.0
    assert out[0, 3] == 230.0


def test_load_raw_four_column_file_as_xyxy_then_convert(tmp_path: Path):
    anno = tmp_path / "nfs_cheetah.txt"
    anno.write_text("525 286 945 516\n", encoding="utf-8")

    raw = load_raw_nfs_annotations(anno)
    out = xyxy_to_xywh(raw)

    assert raw.tolist() == [[525.0, 286.0, 945.0, 516.0]]
    assert out.tolist() == [[525.0, 286.0, 420.0, 230.0]]


def test_load_raw_ten_column_file_extracts_xyxy_columns(tmp_path: Path):
    anno = tmp_path / "nfs_cheetah.txt"
    anno.write_text('0 525 286 945 516 1 0 0 1 "animal"\n', encoding="utf-8")

    raw = load_raw_nfs_annotations(anno)
    out = xyxy_to_xywh(raw)

    assert raw.tolist() == [[525.0, 286.0, 945.0, 516.0]]
    assert out.tolist() == [[525.0, 286.0, 420.0, 230.0]]


def test_normalized_loader_output_shape_matches_frame_count(tmp_path: Path):
    root = tmp_path / "nfs_norm"
    seq_dir = root / "sequences" / "cheetah"
    anno_dir = root / "anno"
    seq_dir.mkdir(parents=True)
    anno_dir.mkdir(parents=True)
    (root / "normalization_manifest.json").write_text('{"sequences": []}\n', encoding="utf-8")
    for frame in range(1, 168):
        (seq_dir / f"{frame:05d}.jpg").write_bytes(b"placeholder")
    rows = ["525.000000\t286.000000\t420.000000\t230.000000" for _ in range(167)]
    (anno_dir / "nfs_cheetah.txt").write_text("\n".join(rows) + "\n", encoding="utf-8")

    bundle = load_canonical_nfs_ground_truth(root, "nfs_cheetah")

    assert bundle.gt_xywh.shape == (167, 4)
    assert bundle.coordinate_format == "canonical_xywh"
