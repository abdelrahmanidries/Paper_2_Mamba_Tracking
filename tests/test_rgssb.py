from __future__ import annotations

import pytest
import torch

from src.models.rgssb import RestorationGuidedSSB


def count_params(module: torch.nn.Module) -> int:
    return sum(param.numel() for param in module.parameters())


def test_import_works() -> None:
    from src.models import RestorationGuidedSSB as ExportedRGSSB

    assert ExportedRGSSB is RestorationGuidedSSB


def test_rgssb_preserves_ostrack_search_shape() -> None:
    model = RestorationGuidedSSB(dim=768, spatial_size=(16, 16))
    x = torch.randn(2, 256, 768)
    y = model(x)
    assert y.shape == x.shape


def test_gradient_flows_through_block() -> None:
    model = RestorationGuidedSSB(dim=32, spatial_size=(4, 4))
    x = torch.randn(2, 16, 32, requires_grad=True)
    loss = model(x).mean()
    loss.backward()

    assert x.grad is not None
    assert torch.isfinite(x.grad).all()
    assert any(param.grad is not None for param in model.parameters() if param.requires_grad)


@pytest.mark.parametrize(
    "kwargs",
    [
        {"use_local_branch": True, "use_channel_attention": False, "use_state_branch": False},
        {"use_local_branch": False, "use_channel_attention": True, "use_state_branch": False},
        {"use_local_branch": False, "use_channel_attention": False, "use_state_branch": True},
        {"use_local_branch": False, "use_channel_attention": False, "use_state_branch": False},
    ],
)
def test_branch_disable_modes_work(kwargs: dict[str, bool]) -> None:
    model = RestorationGuidedSSB(dim=64, spatial_size=(8, 8), **kwargs)
    x = torch.randn(2, 64, 64)
    y = model(x)
    assert y.shape == x.shape
    assert torch.isfinite(y).all()


def test_wrong_spatial_size_raises_value_error() -> None:
    model = RestorationGuidedSSB(dim=32, spatial_size=(3, 5))
    x = torch.randn(2, 16, 32)
    with pytest.raises(ValueError, match="H\\*W == N"):
        model(x)


def test_eval_mode_is_deterministic_with_fixed_seed() -> None:
    torch.manual_seed(123)
    model = RestorationGuidedSSB(dim=48, spatial_size=(4, 4), dropout=0.2)
    model.eval()
    x = torch.randn(2, 16, 48)

    with torch.no_grad():
        first = model(x)
        second = model(x)

    assert torch.allclose(first, second)


def test_parameter_count_is_positive_and_not_huge() -> None:
    model = RestorationGuidedSSB(dim=768, spatial_size=(16, 16))
    params = count_params(model)
    assert params > 0
    assert params < 5_000_000


def test_cuda_if_available_otherwise_cpu() -> None:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = RestorationGuidedSSB(dim=64, spatial_size=(8, 8)).to(device)
    x = torch.randn(2, 64, 64, device=device)
    y = model(x)
    assert y.shape == x.shape
    assert y.device == device
