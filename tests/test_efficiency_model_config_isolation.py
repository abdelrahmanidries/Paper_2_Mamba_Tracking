import json
import sys
from pathlib import Path

import pytest

from scripts import benchmark_ostrack_efficiency as bench


def load_benchmark_config():
    return json.loads(Path("configs/paper_efficiency_benchmark.json").read_text(encoding="utf-8"))


def test_explicit_baseline_checkpoint_resolution():
    cfg = load_benchmark_config()
    path = bench.checkpoint_path(Path.cwd(), cfg["baseline"])
    assert str(path).endswith(
        "external/OSTrack/output/checkpoints/train/ostrack/"
        "vitb_256_mae_ce_32x4_ep300/OSTrack_ep0300.pth.tar"
    )


def test_explicit_final_checkpoint_resolution():
    cfg = load_benchmark_config()
    path = bench.checkpoint_path(Path.cwd(), cfg["final_method"])
    assert str(path).endswith(
        "external/OSTrack/output/checkpoints/train/ostrack/"
        "vitb_256_mae_ce_32x4_ep300_rgssb_head_train_lasot_degraded_hpc_featcons_lam002/"
        "OSTrack_ep0010.pth.tar"
    )
    assert "ep0300" not in path.name


def test_baseline_epoch_300_final_epoch_10_and_rgssb_states():
    cfg = load_benchmark_config()
    assert cfg["baseline"]["expected_test_epoch"] == 300
    assert cfg["final_method"]["expected_test_epoch"] == 10
    assert cfg["baseline"]["expected_rgssb_enabled"] is False
    assert cfg["final_method"]["expected_rgssb_enabled"] is True


def test_static_provenance_accepts_distinct_model_states_without_checkpoint_requirement():
    cfg = load_benchmark_config()
    baseline = bench.validate_model_static_provenance(
        Path.cwd(),
        cfg,
        "baseline",
        actual_epoch=300,
        actual_rgssb_enabled=False,
        total_params=92518533,
        rgssb_params=0,
        has_active_rgssb=False,
        require_checkpoint=False,
    )
    final = bench.validate_model_static_provenance(
        Path.cwd(),
        cfg,
        "final_method",
        actual_epoch=10,
        actual_rgssb_enabled=True,
        total_params=94598469,
        rgssb_params=2079936,
        has_active_rgssb=True,
        require_checkpoint=False,
    )
    assert baseline["rgssb_enabled"] is False
    assert final["rgssb_enabled"] is True
    assert baseline["total_params"] != final["total_params"]


def test_mutable_config_state_cannot_make_final_look_like_baseline():
    cfg = load_benchmark_config()
    with pytest.raises(RuntimeError, match="TEST.EPOCH mismatch"):
        bench.validate_model_static_provenance(
            Path.cwd(),
            cfg,
            "final_method",
            actual_epoch=300,
            actual_rgssb_enabled=False,
            total_params=92518533,
            rgssb_params=0,
            has_active_rgssb=False,
            require_checkpoint=False,
        )


def test_parameter_count_mismatch_fails():
    cfg = load_benchmark_config()
    with pytest.raises(RuntimeError, match="parameter-count mismatch"):
        bench.validate_model_static_provenance(
            Path.cwd(),
            cfg,
            "baseline",
            actual_epoch=300,
            actual_rgssb_enabled=False,
            total_params=1,
            rgssb_params=0,
            has_active_rgssb=False,
            require_checkpoint=False,
        )


def test_missing_checkpoint_fails_when_required():
    cfg = load_benchmark_config()
    with pytest.raises(FileNotFoundError, match="Missing explicit checkpoint"):
        bench.validate_model_static_provenance(
            Path.cwd(),
            cfg,
            "final_method",
            actual_epoch=10,
            actual_rgssb_enabled=True,
            total_params=94598469,
            rgssb_params=2079936,
            has_active_rgssb=True,
            require_checkpoint=True,
        )


def test_final_model_ep0300_checkpoint_fails():
    cfg = load_benchmark_config()
    cfg["final_method"] = dict(cfg["final_method"])
    cfg["final_method"]["checkpoint"] = (
        "external/OSTrack/output/checkpoints/train/ostrack/"
        "vitb_256_mae_ce_32x4_ep300_rgssb_head_train_lasot_degraded_hpc_featcons_lam002/"
        "OSTrack_ep0300.pth.tar"
    )
    with pytest.raises(RuntimeError, match="invalid final checkpoint"):
        bench.validate_model_static_provenance(
            Path.cwd(),
            cfg,
            "final_method",
            actual_epoch=10,
            actual_rgssb_enabled=True,
            total_params=94598469,
            rgssb_params=2079936,
            has_active_rgssb=True,
            require_checkpoint=False,
        )


def test_partial_worker_failure_does_not_modify_final_csv(tmp_path, monkeypatch):
    cfg_dir = tmp_path / "configs"
    cfg_dir.mkdir()
    output_csv = tmp_path / "experiments" / "paper_efficiency_results.csv"
    output_csv.parent.mkdir()
    original = "model_label,config\nold,row\n"
    output_csv.write_text(original, encoding="utf-8")

    cfg = load_benchmark_config()
    cfg["output_csv"] = str(output_csv.relative_to(tmp_path))
    cfg_path = cfg_dir / "paper_efficiency_benchmark.json"
    cfg_path.write_text(json.dumps(cfg), encoding="utf-8")

    def fail_worker(*args, **kwargs):
        raise RuntimeError("worker failed")

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(bench, "run_benchmark_workers", fail_worker)
    monkeypatch.setattr(sys, "argv", ["benchmark", "--benchmark_config", str(cfg_path.relative_to(tmp_path))])
    with pytest.raises(RuntimeError, match="worker failed"):
        bench.main()
    assert output_csv.read_text(encoding="utf-8") == original
