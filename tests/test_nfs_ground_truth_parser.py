import ast
from pathlib import Path

import numpy as np

from scripts.audit_nfs_ground_truth_format import (
    aligned_annotation_indices,
    candidate_boxes,
    parse_numeric_prefix,
    plausibility,
)


def test_parse_raw_nfs_annotation_row_detects_numeric_prefix_and_label():
    row = '0 525 286 945 516 1 0 0 1 "animal"'
    numeric, token_count, delimiter = parse_numeric_prefix(row)

    assert delimiter == "whitespace"
    assert token_count == 10
    assert numeric == [0.0, 525.0, 286.0, 945.0, 516.0, 1.0, 0.0, 0.0, 1.0]


def test_raw_nfs_columns_1_to_4_convert_from_xyxy_to_xywh():
    row = '0 525 286 945 516 1 0 0 1 "animal"'
    numeric, _, _ = parse_numeric_prefix(row)
    boxes = candidate_boxes(numeric)

    assert boxes["candidate_a_direct_c0_c3_xywh"] == [0.0, 525.0, 286.0, 945.0]
    assert boxes["candidate_c_raw_nfs_c1_c4_xyxy_to_xywh"] == [525.0, 286.0, 420.0, 230.0]


def test_plausibility_rejects_direct_first_four_columns_for_cheetah_like_row():
    row = '0 525 286 945 516 1 0 0 1 "animal"'
    numeric, _, _ = parse_numeric_prefix(row)
    boxes = candidate_boxes(numeric)

    direct_ok, _ = plausibility(boxes["candidate_a_direct_c0_c3_xywh"], 1280, 720)
    raw_ok, _ = plausibility(boxes["candidate_c_raw_nfs_c1_c4_xyxy_to_xywh"], 1280, 720)

    assert not direct_ok
    assert raw_ok


def test_aligned_annotation_indices_sample_dense_raw_rows_to_expected_frames():
    indices, stride = aligned_annotation_indices(raw_count=4433, expected_frames=555, init_omit=0)

    assert stride == 8
    assert len(indices) == 555
    assert indices[:3] == [0, 8, 16]
