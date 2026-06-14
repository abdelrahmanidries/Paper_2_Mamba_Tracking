#!/usr/bin/env python3
"""Create a full UAV123-style root with one degraded target sequence."""

from __future__ import annotations

import argparse
import ast
import json
import shutil
import sys
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.degradations.pipeline import apply_degradation
from src.degradations.protocols import DEGRADATION_TYPES, SEVERITIES


UAV_DATASET_PY = ROOT / "external" / "OSTrack" / "lib" / "test" / "evaluation" / "uavdataset.py"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a degraded UAV123 root for one sequence.")
    parser.add_argument("--clean_uav_root", required=True, type=Path)
    parser.add_argument("--sequence", required=True)
    parser.add_argument("--degradation", required=True, choices=list(DEGRADATION_TYPES))
    parser.add_argument("--severity", required=True)
    parser.add_argument("--seed", required=True, type=int)
    parser.add_argument("--output_root", required=True, type=Path)
    return parser.parse_args()


def load_sequence_info() -> list[dict]:
    module = ast.parse(UAV_DATASET_PY.read_text(encoding="utf-8"))
    for node in ast.walk(module):
        if isinstance(node, ast.FunctionDef) and node.name == "_get_sequence_info_list":
            for child in ast.walk(node):
                if isinstance(child, ast.Assign):
                    for target in child.targets:
                        if isinstance(target, ast.Name) and target.id == "sequence_info_list":
                            return ast.literal_eval(child.value)
    raise RuntimeError(f"Could not parse sequence_info_list from {UAV_DATASET_PY}")


def get_sequence_info(sequence: str) -> dict:
    for info in load_sequence_info():
        if info["name"] == sequence:
            return info
    raise ValueError(f"Unknown UAV123 sequence: {sequence}")


def remove_path(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)


def link_or_copy(src: Path, dst: Path, directory: bool = False) -> str:
    if dst.exists() or dst.is_symlink():
        remove_path(dst)
    dst.parent.mkdir(parents=True, exist_ok=True)
    try:
        dst.symlink_to(src.resolve(), target_is_directory=directory)
        return "symlink"
    except OSError:
        if directory:
            shutil.copytree(src, dst, symlinks=True)
            return "copytree"
        shutil.copy2(src, dst)
        return "copy"


def count_nonempty_lines(path: Path) -> int:
    return sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip())


def mirror_uav_root(clean_root: Path, output_root: Path, target_rel_path: Path) -> int:
    output_root.mkdir(parents=True, exist_ok=True)
    mirrored = 0
    for entry in sorted(clean_root.iterdir()):
        if entry.name == "data_seq":
            continue
        link_or_copy(entry, output_root / entry.name, directory=entry.is_dir())
        mirrored += 1

    clean_seq_root = clean_root / "data_seq" / "UAV123"
    output_seq_root = output_root / "data_seq" / "UAV123"
    output_seq_root.mkdir(parents=True, exist_ok=True)
    target_name = target_rel_path.name
    for seq_dir in sorted(clean_seq_root.iterdir()):
        if not seq_dir.is_dir():
            continue
        if seq_dir.name == target_name:
            continue
        link_or_copy(seq_dir, output_seq_root / seq_dir.name, directory=True)
        mirrored += 1
    return mirrored


def frame_paths(root: Path, info: dict) -> list[Path]:
    start = int(info["startFrame"]) + int(info.get("initOmit", 0))
    end = int(info["endFrame"])
    nz = int(info["nz"])
    ext = str(info["ext"])
    seq_dir = root / info["path"]
    return [seq_dir / f"{frame:0{nz}}.{ext}" for frame in range(start, end + 1)]


def validate(args: argparse.Namespace, info: dict) -> None:
    if args.degradation != "clean" and args.severity not in SEVERITIES:
        raise ValueError(f"Unsupported severity {args.severity!r}; expected one of {SEVERITIES}")
    if not args.clean_uav_root.is_dir():
        raise FileNotFoundError(f"Clean UAV123 root not found: {args.clean_uav_root}")
    anno_path = args.clean_uav_root / info["anno_path"]
    if not anno_path.is_file():
        raise FileNotFoundError(f"Annotation file not found: {anno_path}")
    frames = frame_paths(args.clean_uav_root, info)
    if not frames:
        raise FileNotFoundError(f"No frames listed for sequence {args.sequence}")
    missing = [path for path in (frames[0], frames[-1]) if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"Missing first/last frame for {args.sequence}: {missing}")
    gt_lines = count_nonempty_lines(anno_path) - int(info.get("initOmit", 0))
    if gt_lines != len(frames):
        raise ValueError(f"Frame/annotation mismatch for {args.sequence}: frames={len(frames)} gt={gt_lines}")


def main() -> int:
    args = parse_args()
    info = get_sequence_info(args.sequence)
    validate(args, info)

    output_root = args.output_root / f"uav123_{args.sequence}_{args.degradation}_{args.severity}"
    clean_target_dir = args.clean_uav_root / info["path"]
    output_target_dir = output_root / info["path"]
    mirrored = mirror_uav_root(args.clean_uav_root, output_root, Path(info["path"]))
    if output_target_dir.exists() or output_target_dir.is_symlink():
        remove_path(output_target_dir)
    shutil.copytree(clean_target_dir, output_target_dir, symlinks=True)

    metadata_path = output_target_dir / "metadata.jsonl"
    frames = frame_paths(args.clean_uav_root, info)
    processed = 0
    with metadata_path.open("w", encoding="utf-8", newline="\n") as metadata_file:
        for index, frame_path in enumerate(frames):
            output_path = output_root / info["path"] / frame_path.name
            frame_seed = args.seed + index
            if args.degradation == "clean":
                with Image.open(frame_path) as image:
                    width, height = image.size
                metadata = {
                    "degradation_type": "clean",
                    "severity": args.severity,
                    "parameters": {},
                    "seed": frame_seed,
                    "copy_method": "preserved",
                }
            else:
                with Image.open(frame_path) as image:
                    image = image.convert("RGB")
                    width, height = image.size
                    degraded, metadata = apply_degradation(
                        image,
                        args.degradation,
                        args.severity,
                        seed=frame_seed,
                    )
                    if degraded.size != (width, height):
                        raise RuntimeError(f"Degradation changed image size for {frame_path}")
                    degraded.save(output_path)

            metadata_file.write(
                json.dumps(
                    {
                        "sequence": args.sequence,
                        "frame_index": index,
                        "input": str(frame_path),
                        "output": str(output_path),
                        "width": width,
                        "height": height,
                        "metadata": metadata,
                    },
                    sort_keys=True,
                )
                + "\n"
            )
            processed += 1

    anno_lines = count_nonempty_lines(args.clean_uav_root / info["anno_path"]) - int(info.get("initOmit", 0))
    print(f"Output root: {output_root}")
    print(f"Mirrored non-target entries: {mirrored}")
    print(f"Processed frames: {processed}")
    print(f"Annotation lines: {anno_lines}")
    print(f"Degradation type: {args.degradation}")
    print(f"Severity: {args.severity}")
    print(f"Seed: {args.seed}")
    print(f"Metadata JSONL: {metadata_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
