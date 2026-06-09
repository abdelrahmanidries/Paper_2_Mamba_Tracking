from pathlib import Path
import argparse
import numpy as np


def load_boxes(path: Path) -> np.ndarray:
    rows = []
    for line in path.read_text().strip().splitlines():
        line = line.replace(",", " ").replace("\t", " ")
        vals = [float(x) for x in line.split()[:4]]
        rows.append(vals)
    return np.array(rows, dtype=np.float32)


def box_iou_xywh(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    ax1, ay1, aw, ah = a.T
    bx1, by1, bw, bh = b.T

    ax2, ay2 = ax1 + aw, ay1 + ah
    bx2, by2 = bx1 + bw, by1 + bh

    ix1 = np.maximum(ax1, bx1)
    iy1 = np.maximum(ay1, by1)
    ix2 = np.minimum(ax2, bx2)
    iy2 = np.minimum(ay2, by2)

    iw = np.maximum(0, ix2 - ix1)
    ih = np.maximum(0, iy2 - iy1)

    inter = iw * ih
    area_a = aw * ah
    area_b = bw * bh
    union = area_a + area_b - inter

    return inter / np.maximum(union, 1e-6)


def center_error(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    acx = a[:, 0] + a[:, 2] / 2
    acy = a[:, 1] + a[:, 3] / 2
    bcx = b[:, 0] + b[:, 2] / 2
    bcy = b[:, 1] + b[:, 3] / 2
    return np.sqrt((acx - bcx) ** 2 + (acy - bcy) ** 2)


def compute_metrics(gt: np.ndarray, pred: np.ndarray) -> dict:
    n = min(len(gt), len(pred))
    gt = gt[:n]
    pred = pred[:n]

    ious = box_iou_xywh(gt, pred)
    errors = center_error(gt, pred)

    thresholds = np.linspace(0, 1, 101)
    success_curve = [(ious >= t).mean() for t in thresholds]

    return {
        "frames": n,
        "mean_iou": float(ious.mean()),
        "success_auc": float(np.mean(success_curve)),
        "precision_20": float((errors <= 20).mean()),
        "mean_center_error": float(errors.mean()),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--gt", required=True, type=Path)
    parser.add_argument("--pred", required=True, type=Path)
    parser.add_argument("--name", default="sequence")
    args = parser.parse_args()

    gt = load_boxes(args.gt)
    pred = load_boxes(args.pred)
    metrics = compute_metrics(gt, pred)

    print(f"Sequence: {args.name}")
    print(f"Frames evaluated: {metrics['frames']}")
    print(f"Mean IoU: {metrics['mean_iou']:.4f}")
    print(f"Success AUC: {metrics['success_auc']:.4f}")
    print(f"Precision @20px: {metrics['precision_20']:.4f}")
    print(f"Mean center error: {metrics['mean_center_error']:.2f} px")


if __name__ == "__main__":
    main()
