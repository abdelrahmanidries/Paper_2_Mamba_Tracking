"""Shared NFS annotation normalization and alignment helpers.

The raw NFS archives store boxes as XYXY. OSTrack expects one XYWH row
per evaluated frame, so project-side NFS code should use this module
instead of ad hoc row-count or first-four-column parsing.
"""

from __future__ import annotations

import ast
import io
import json
import re
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping

import numpy as np
from PIL import Image


PROJECT_ROOT = Path(__file__).resolve().parents[2]
NFS_DATASET_PY = PROJECT_ROOT / "external" / "OSTrack" / "lib" / "test" / "evaluation" / "nfsdataset.py"


@dataclass(frozen=True)
class NFSSequenceInfo:
    name: str
    path: str
    start_frame: int
    end_frame: int
    nz: int
    ext: str
    anno_path: str
    object_class: str
    init_omit: int = 0

    @property
    def target_name(self) -> str:
        return Path(self.path).name

    @property
    def frame_count(self) -> int:
        return self.end_frame - (self.start_frame + self.init_omit) + 1


@dataclass(frozen=True)
class NFSAnnotationBundle:
    sequence: NFSSequenceInfo
    frame_paths: list[Path]
    gt_xywh: np.ndarray
    raw_xyxy: np.ndarray
    selected_raw_indices: list[int]
    raw_annotation_count: int
    aligned_annotation_count: int
    image_count: int
    sampling_stride: int
    coordinate_format: str
    raw_annotation_path: Path


def load_sequence_metadata(nfs_dataset_py: Path = NFS_DATASET_PY) -> list[NFSSequenceInfo]:
    module = ast.parse(nfs_dataset_py.read_text(encoding="utf-8"))
    raw_list = None
    for node in ast.walk(module):
        if isinstance(node, ast.FunctionDef) and node.name == "_get_sequence_info_list":
            for child in ast.walk(node):
                if isinstance(child, ast.Assign):
                    for target in child.targets:
                        if isinstance(target, ast.Name) and target.id == "sequence_info_list":
                            raw_list = ast.literal_eval(child.value)
                            break
    if raw_list is None:
        raise RuntimeError(f"Could not parse sequence_info_list from {nfs_dataset_py}")
    return [
        NFSSequenceInfo(
            name=str(item["name"]),
            path=str(item["path"]),
            start_frame=int(item["startFrame"]),
            end_frame=int(item["endFrame"]),
            nz=int(item["nz"]),
            ext=str(item["ext"]),
            anno_path=str(item["anno_path"]),
            object_class=str(item.get("object_class", "")),
            init_omit=int(item.get("initOmit", 0)),
        )
        for item in raw_list
    ]


def get_sequence_info(sequence: str, nfs_dataset_py: Path = NFS_DATASET_PY) -> NFSSequenceInfo:
    for info in load_sequence_metadata(nfs_dataset_py):
        if info.name == sequence:
            return info
    raise ValueError(f"Unknown NFS sequence: {sequence}")


def _mapped_value(mapping: Mapping[str, Any], aliases: tuple[str, ...], field_name: str) -> Any:
    for alias in aliases:
        if alias in mapping:
            return mapping[alias]
    raise ValueError(f"Missing required NFS sequence metadata field '{field_name}' (aliases: {', '.join(aliases)})")


def canonical_sequence_info(info: NFSSequenceInfo | Mapping[str, Any]) -> NFSSequenceInfo:
    """Return canonical NFS metadata from either dataclass or OSTrack-style dict.

    Some project-side scripts historically expose OSTrack-style dictionaries
    with keys like startFrame/endFrame/initOmit. Shared helpers use the
    canonical NFSSequenceInfo dataclass. This adapter keeps the conversion
    explicit without duplicating frame-list or alignment logic.
    """

    if isinstance(info, NFSSequenceInfo):
        return info
    if not isinstance(info, Mapping):
        raise TypeError(f"Expected NFSSequenceInfo or mapping metadata, got {type(info).__name__}")
    return NFSSequenceInfo(
        name=str(_mapped_value(info, ("name", "sequence", "sequence_name"), "name")),
        path=str(_mapped_value(info, ("path", "sequence_path"), "path")),
        start_frame=int(_mapped_value(info, ("start_frame", "startFrame"), "start_frame")),
        end_frame=int(_mapped_value(info, ("end_frame", "endFrame"), "end_frame")),
        nz=int(_mapped_value(info, ("nz", "zero_padding"), "nz")),
        ext=str(_mapped_value(info, ("ext", "extension"), "ext")),
        anno_path=str(_mapped_value(info, ("anno_path", "annotation_path"), "anno_path")),
        object_class=str(info.get("object_class", "")),
        init_omit=int(info.get("init_omit", info.get("initOmit", 0))),
    )


def metadata_frame_paths(nfs_root: Path, info: NFSSequenceInfo | Mapping[str, Any]) -> list[Path]:
    info = canonical_sequence_info(info)
    start = info.start_frame + info.init_omit
    return [nfs_root / info.path / f"{frame:0{info.nz}}.{info.ext}" for frame in range(start, info.end_frame + 1)]


def existing_metadata_frame_paths(nfs_root: Path, info: NFSSequenceInfo | Mapping[str, Any]) -> list[Path]:
    info = canonical_sequence_info(info)
    frames = metadata_frame_paths(nfs_root, info)
    missing = [path for path in frames if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"Missing NFS frame for {info.name}: {missing[0]}")
    return frames


def count_nonempty_lines(path: Path) -> int:
    return sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip())


def _numeric_prefix(line: str) -> list[float]:
    values: list[float] = []
    for token in re.split(r"[\s,\t]+", line.strip()):
        if not token:
            continue
        try:
            values.append(float(token))
        except ValueError:
            break
    return values


def load_raw_nfs_annotations(path: Path) -> np.ndarray:
    rows = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        values = _numeric_prefix(line)
        if len(values) == 4:
            rows.append(values)
        elif len(values) >= 5:
            # Raw NFS archive rows use: track_id x1 y1 x2 y2 frame ...
            rows.append(values[1:5])
        else:
            raise ValueError(f"Annotation row {line_number} has too few numeric columns in {path}: {line!r}")
    if not rows:
        raise ValueError(f"No annotation rows found: {path}")
    raw = np.asarray(rows, dtype=np.float64)
    validate_raw_xyxy(raw, path)
    return raw


def load_xywh_annotations(path: Path) -> np.ndarray:
    rows = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        values = _numeric_prefix(line)
        if len(values) < 4:
            raise ValueError(f"Annotation row {line_number} has too few numeric columns in {path}: {line!r}")
        rows.append(values[:4])
    boxes = np.asarray(rows, dtype=np.float64)
    validate_xywh(boxes, source=str(path))
    return boxes


def validate_raw_xyxy(raw_xyxy: np.ndarray, source: Path | str = "annotations") -> None:
    if raw_xyxy.ndim != 2 or raw_xyxy.shape[1] != 4:
        raise ValueError(f"Expected raw XYXY shape [N,4] for {source}, got {raw_xyxy.shape}")
    widths = raw_xyxy[:, 2] - raw_xyxy[:, 0]
    heights = raw_xyxy[:, 3] - raw_xyxy[:, 1]
    if np.any(widths <= 0) or np.any(heights <= 0):
        bad = int(np.where((widths <= 0) | (heights <= 0))[0][0])
        raise ValueError(f"Invalid raw XYXY box at row {bad + 1} in {source}: {raw_xyxy[bad].tolist()}")


def xyxy_to_xywh(raw_xyxy: np.ndarray) -> np.ndarray:
    validate_raw_xyxy(raw_xyxy)
    out = raw_xyxy.astype(np.float64, copy=True)
    out[:, 2] = raw_xyxy[:, 2] - raw_xyxy[:, 0]
    out[:, 3] = raw_xyxy[:, 3] - raw_xyxy[:, 1]
    return out


def validate_xywh(boxes: np.ndarray, image_sizes: list[tuple[int, int]] | None = None, source: str = "boxes") -> None:
    if boxes.ndim != 2 or boxes.shape[1] != 4:
        raise ValueError(f"Expected XYWH shape [N,4] for {source}, got {boxes.shape}")
    if np.any(boxes[:, 2] <= 0) or np.any(boxes[:, 3] <= 0):
        bad = int(np.where((boxes[:, 2] <= 0) | (boxes[:, 3] <= 0))[0][0])
        raise ValueError(f"Invalid XYWH size at row {bad + 1} in {source}: {boxes[bad].tolist()}")
    if image_sizes is not None:
        if len(image_sizes) != len(boxes):
            raise ValueError(f"Image-size count mismatch for {source}: sizes={len(image_sizes)} boxes={len(boxes)}")
        for index, ((width, height), box) in enumerate(zip(image_sizes, boxes), start=1):
            x, y, w, h = box
            if x + w < -2 or y + h < -2 or x > width + 2 or y > height + 2:
                raise ValueError(f"Box row {index} in {source} is geometrically implausible for image {width}x{height}: {box.tolist()}")


def alignment_indices(raw_count: int, image_count: int, init_omit: int = 0) -> tuple[list[int], int]:
    """Map evaluated frame positions to raw annotation rows.

    NFS 30fps image folders are sequentially renamed, while raw annotations
    can retain dense 240fps rows. The mapping is by frame position using a
    verified stride derived from counts, not by image filename number.
    """

    available = raw_count - init_omit
    if image_count <= 0:
        raise ValueError("image_count must be positive")
    if available <= 0:
        raise ValueError(f"No available annotations after init_omit={init_omit}")
    if available == image_count:
        return list(range(init_omit, init_omit + image_count)), 1
    if available < image_count:
        raise ValueError(f"Raw annotations fewer than images: raw_available={available} images={image_count}")
    stride = round(available / image_count)
    if stride <= 1:
        raise ValueError(f"Ambiguous NFS annotation stride: raw_available={available} images={image_count} stride={stride}")
    indices = [init_omit + i * stride for i in range(image_count)]
    if indices[-1] >= raw_count:
        raise ValueError(
            f"Alignment exceeds raw annotations: last_index={indices[-1]} raw_count={raw_count} "
            f"image_count={image_count} stride={stride}"
        )
    expected_len = len(range(init_omit, raw_count, stride))
    if expected_len < image_count:
        raise ValueError(f"Stride does not provide enough rows: stride={stride} expected_len={expected_len} images={image_count}")
    return indices, stride


def load_canonical_nfs_ground_truth(nfs_root: Path, sequence: str) -> NFSAnnotationBundle:
    info = get_sequence_info(sequence)
    frames = existing_metadata_frame_paths(nfs_root, info)
    raw_path = nfs_root / info.anno_path
    if not raw_path.is_file():
        raise FileNotFoundError(f"NFS annotation file not found: {raw_path}")
    if (nfs_root / "normalization_manifest.json").is_file():
        gt_xywh = load_xywh_annotations(raw_path)
        if len(gt_xywh) != len(frames):
            raise ValueError(f"Normalized annotation/frame mismatch for {sequence}: gt={len(gt_xywh)} frames={len(frames)}")
        return NFSAnnotationBundle(
            sequence=info,
            frame_paths=frames,
            gt_xywh=gt_xywh,
            raw_xyxy=np.empty((0, 4), dtype=np.float64),
            selected_raw_indices=list(range(len(gt_xywh))),
            raw_annotation_count=len(gt_xywh),
            aligned_annotation_count=len(gt_xywh),
            image_count=len(frames),
            sampling_stride=1,
            coordinate_format="canonical_xywh",
            raw_annotation_path=raw_path,
        )
    raw_xyxy = load_raw_nfs_annotations(raw_path)
    indices, stride = alignment_indices(len(raw_xyxy), len(frames), info.init_omit)
    aligned_xyxy = raw_xyxy[indices, :]
    gt_xywh = xyxy_to_xywh(aligned_xyxy)
    validate_xywh(gt_xywh, source=f"{sequence} canonical GT")
    if len(gt_xywh) != len(frames):
        raise ValueError(f"Aligned annotation count mismatch for {sequence}: gt={len(gt_xywh)} frames={len(frames)}")
    return NFSAnnotationBundle(
        sequence=info,
        frame_paths=frames,
        gt_xywh=gt_xywh,
        raw_xyxy=raw_xyxy,
        selected_raw_indices=indices,
        raw_annotation_count=len(raw_xyxy),
        aligned_annotation_count=len(gt_xywh),
        image_count=len(frames),
        sampling_stride=stride,
        coordinate_format="raw_xyxy_to_canonical_xywh",
        raw_annotation_path=raw_path,
    )


def format_xywh_row(row: Iterable[float]) -> str:
    return "\t".join(f"{float(value):.6f}" for value in row)


def write_xywh_annotations(path: Path, boxes: np.ndarray) -> None:
    validate_xywh(boxes, source=str(path))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(format_xywh_row(row) for row in boxes) + "\n", encoding="utf-8")


def read_image_sizes(paths: list[Path]) -> list[tuple[int, int]]:
    sizes = []
    for path in paths:
        with Image.open(path) as image:
            sizes.append((image.width, image.height))
    return sizes


def manifest_record(bundle: NFSAnnotationBundle, output_anno_path: Path | None = None) -> dict[str, object]:
    indices = bundle.selected_raw_indices
    mapping_preview = {
        "first_10": indices[:10],
        "last_10": indices[-10:],
    }
    return {
        "sequence": bundle.sequence.name,
        "raw_annotation_path": str(bundle.raw_annotation_path),
        "image_path": str(Path(bundle.sequence.path)),
        "output_annotation_path": str(output_anno_path) if output_anno_path is not None else None,
        "raw_annotation_count": bundle.raw_annotation_count,
        "image_count": bundle.image_count,
        "aligned_count": bundle.aligned_annotation_count,
        "sampling_stride": bundle.sampling_stride,
        "selected_raw_indices": mapping_preview,
        "coordinate_conversion": "xyxy_to_xywh",
        "coordinate_format": bundle.coordinate_format,
        "validation_status": "passed",
    }


def dump_manifest(path: Path, records: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"sequences": records}, indent=2) + "\n", encoding="utf-8")
