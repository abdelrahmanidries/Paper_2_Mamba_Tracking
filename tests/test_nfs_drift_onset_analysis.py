import numpy as np

from scripts.analyze_nfs_drift_onset import classify_event_sequence, classify_failure, recovery_after


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


def test_bowling_multistage_shared_then_persistent_rgssb_loss():
    result = classify_event_sequence(
        divergence_idx=88,
        shared_idx=79,
        jump_idx=None,
        scale_idx=None,
        rgssb_recovered_after_divergence=False,
        baseline_recovered_after_shared=True,
        rgssb_recovered_after_shared=False,
    )

    assert result["initial_failure_mode"] == "shared tracker failure"
    assert result["subsequent_failure_mode"] == "RG-SSB-specific divergence"
    assert result["terminal_failure_mode"] == "persistent RG-SSB-specific target loss"
    assert result["event_sequence"] == "shared tracker failure -> baseline recovery -> persistent RG-SSB target loss"
    assert result["persistent_rgssb_loss_after_shared_failure"] is True


def test_gymnastics_low_resolution_multistage_shared_then_persistent_rgssb_loss():
    result = classify_event_sequence(
        divergence_idx=130,
        shared_idx=118,
        jump_idx=None,
        scale_idx=None,
        rgssb_recovered_after_divergence=False,
        baseline_recovered_after_shared=True,
        rgssb_recovered_after_shared=False,
    )

    assert result["initial_failure_mode"] == "shared tracker failure"
    assert result["subsequent_failure_mode"] == "RG-SSB-specific divergence"
    assert result["terminal_failure_mode"] == "persistent RG-SSB-specific target loss"


def test_gymnastics_gaussian_noise_multistage_shared_then_persistent_rgssb_loss():
    result = classify_event_sequence(
        divergence_idx=287,
        shared_idx=119,
        jump_idx=None,
        scale_idx=None,
        rgssb_recovered_after_divergence=False,
        baseline_recovered_after_shared=True,
        rgssb_recovered_after_shared=False,
    )

    assert result["initial_failure_mode"] == "shared tracker failure"
    assert result["subsequent_failure_mode"] == "RG-SSB-specific divergence"
    assert result["terminal_failure_mode"] == "persistent RG-SSB-specific target loss"


def test_basketball_player_2_multistage_shared_then_persistent_rgssb_loss():
    result = classify_event_sequence(
        divergence_idx=375,
        shared_idx=196,
        jump_idx=None,
        scale_idx=None,
        rgssb_recovered_after_divergence=False,
        baseline_recovered_after_shared=True,
        rgssb_recovered_after_shared=False,
    )

    assert result["initial_failure_mode"] == "shared tracker failure"
    assert result["subsequent_failure_mode"] == "RG-SSB-specific divergence"
    assert result["terminal_failure_mode"] == "persistent RG-SSB-specific target loss"


def test_parkour_rgssb_specific_divergence_without_shared_failure():
    result = classify_event_sequence(
        divergence_idx=44,
        shared_idx=None,
        jump_idx=None,
        scale_idx=None,
        rgssb_recovered_after_divergence=False,
        baseline_recovered_after_shared=False,
        rgssb_recovered_after_shared=False,
    )

    assert result["initial_failure_mode"] == "RG-SSB-specific divergence"
    assert result["subsequent_failure_mode"] == ""
    assert result["terminal_failure_mode"] == "persistent RG-SSB-specific target loss"
    assert result["event_sequence"] == "persistent RG-SSB target loss"


def test_car_rc_rolling_center_jump_before_shared_failure():
    result = classify_event_sequence(
        divergence_idx=None,
        shared_idx=39,
        jump_idx=35,
        scale_idx=None,
        rgssb_recovered_after_divergence=False,
        baseline_recovered_after_shared=False,
        rgssb_recovered_after_shared=False,
    )

    assert result["initial_failure_mode"] == "sudden center jump"
    assert result["subsequent_failure_mode"] == "shared tracker failure"
    assert result["terminal_failure_mode"] == "sudden center jump"


def test_footbal_skill_center_jump_before_shared_failure():
    result = classify_event_sequence(
        divergence_idx=None,
        shared_idx=87,
        jump_idx=35,
        scale_idx=None,
        rgssb_recovered_after_divergence=False,
        baseline_recovered_after_shared=False,
        rgssb_recovered_after_shared=False,
    )

    assert result["initial_failure_mode"] == "sudden center jump"
    assert result["subsequent_failure_mode"] == "shared tracker failure"
    assert result["terminal_failure_mode"] == "sudden center jump"
