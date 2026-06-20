from pathlib import Path
import subprocess
import sys
import types
from types import SimpleNamespace

import numpy as np
import pytest
from PIL import Image

from src.evaluation.nfs_annotations import (
    alignment_indices,
    load_canonical_nfs_ground_truth,
    load_raw_nfs_annotations,
    load_sequence_metadata,
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


def test_degraded_nfs_root_preserves_complete_annotation_tree_and_loader_constructs(monkeypatch, tmp_path: Path):
    clean = tmp_path / "normalized_nfs"
    output_root = tmp_path / "degraded"
    (clean / "sequences").mkdir(parents=True)
    (clean / "anno").mkdir(parents=True)
    (clean / "normalization_manifest.json").write_text('{"sequences": []}\n', encoding="utf-8")

    target = "nfs_basketball_player"
    for info in load_sequence_metadata():
        seq_dir = clean / info.path
        seq_dir.mkdir(parents=True)
        rows = ["10.000000\t20.000000\t30.000000\t40.000000" for _ in range(info.frame_count)]
        (clean / info.anno_path).write_text("\n".join(rows) + "\n", encoding="utf-8")
        if info.name == target:
            for frame in range(info.start_frame + info.init_omit, info.end_frame + 1):
                Image.new("RGB", (64, 64), color=(frame % 255, 32, 64)).save(seq_dir / f"{frame:0{info.nz}}.{info.ext}")

    subprocess.run(
        [
            sys.executable,
            "scripts/create_degraded_nfs_sequence.py",
            "--clean_nfs_root",
            str(clean),
            "--sequence",
            target,
            "--degradation",
            "motion_blur",
            "--severity",
            "medium",
            "--seed",
            "42",
            "--output_root",
            str(output_root),
        ],
        check=True,
    )

    degraded = output_root / "nfs_nfs_basketball_player_motion_blur_medium"
    assert (degraded / "anno" / "nfs_Gymnastics.txt").is_file()
    assert (degraded / "anno" / "nfs_basketball_player.txt").is_file()
    assert len(list((degraded / "anno").glob("*.txt"))) == len(load_sequence_metadata())
    assert len([p for p in (degraded / "sequences").iterdir() if p.is_dir() or p.is_symlink()]) == len(load_sequence_metadata())

    ostrack_root = Path("external/OSTrack").resolve()
    sys.path.insert(0, str(ostrack_root))
    fake_train = types.ModuleType("lib.train")
    fake_train_data = types.ModuleType("lib.train.data")
    fake_image_loader = types.ModuleType("lib.train.data.image_loader")
    fake_image_loader.imread_indexed = lambda path: None
    fake_test_utils = types.ModuleType("lib.test.utils")
    fake_load_text = types.ModuleType("lib.test.utils.load_text")
    fake_load_text.load_text = lambda path, delimiter="\t", dtype=np.float64: np.loadtxt(path, delimiter=delimiter, dtype=dtype)
    monkeypatch.setitem(sys.modules, "lib.train", fake_train)
    monkeypatch.setitem(sys.modules, "lib.train.data", fake_train_data)
    monkeypatch.setitem(sys.modules, "lib.train.data.image_loader", fake_image_loader)
    monkeypatch.setitem(sys.modules, "lib.test.utils", fake_test_utils)
    monkeypatch.setitem(sys.modules, "lib.test.utils.load_text", fake_load_text)
    from lib.test.evaluation import data as eval_data
    from lib.test.evaluation.nfsdataset import NFSDataset

    monkeypatch.setattr(eval_data, "env_settings", lambda: SimpleNamespace(nfs_path=str(degraded)))
    dataset = NFSDataset()
    sequence_list = dataset.get_sequence_list()
    selected = sequence_list[target]

    assert len(sequence_list) == len(load_sequence_metadata())
    assert selected.ground_truth_rect.shape == (369, 4)
