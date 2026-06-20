import numpy as np

from scripts.analyze_nfs_drift_onset import classify_failure, recovery_after


def test_bowling_specific_divergence_is_not_labeled_shared_failure():
    classification = classify_failure(
        divergence_idx=88,
        shared_idx=95,
        jump_idx=None,
        scale_idx=None,
        recovery=False,
    )

    assert classification == "persistent RG-SSB-specific target loss"


def test_gymnastics_specific_divergence_is_not_labeled_shared_failure():
    classification = classify_failure(
        divergence_idx=130,
        shared_idx=150,
        jump_idx=131,
        scale_idx=None,
        recovery=False,
    )

    assert classification == "persistent RG-SSB-specific target loss"


def test_shared_failure_when_both_trackers_fail_first():
    classification = classify_failure(
        divergence_idx=40,
        shared_idx=35,
        jump_idx=None,
        scale_idx=None,
        recovery=False,
    )

    assert classification == "shared tracker failure"


def test_recovery_is_measured_after_rgssb_specific_divergence():
    iou = np.array([0.5] * 10 + [0.0] * 5 + [0.45] * 5)

    recovered, frame_index = recovery_after(iou, start_idx=10, run_length=5)

    assert recovered is True
    assert frame_index == 15


def test_specific_divergence_with_recovery_gets_temporary_label():
    classification = classify_failure(
        divergence_idx=10,
        shared_idx=None,
        jump_idx=None,
        scale_idx=None,
        recovery=True,
    )

    assert classification == "temporary RG-SSB-specific failure with recovery"
