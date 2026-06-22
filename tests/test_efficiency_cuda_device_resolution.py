from types import SimpleNamespace

import pytest

from scripts.benchmark_ostrack_efficiency import resolve_cuda_device


class FakeCuda:
    def __init__(self, available=True, count=1, property_error=None):
        self._available = available
        self._count = count
        self.property_error = property_error
        self.selected = None

    def is_available(self):
        return self._available

    def device_count(self):
        return self._count

    def set_device(self, index):
        self.selected = index

    def get_device_properties(self, index):
        if self.property_error is not None:
            raise self.property_error
        return SimpleNamespace(name=f"fake-gpu-{index}")


class FakeTorch:
    def __init__(self, cuda):
        self.cuda = cuda

    def device(self, kind, index):
        return f"{kind}:{index}"


def test_one_visible_logical_gpu_selects_zero():
    cuda = FakeCuda(available=True, count=1)
    result = resolve_cuda_device(torch_module=FakeTorch(cuda), env={})
    assert result.device == "cuda:0"
    assert result.logical_index == 0
    assert result.gpu_name == "fake-gpu-0"
    assert cuda.selected == 0


def test_multiple_visible_gpus_default_to_logical_zero():
    cuda = FakeCuda(available=True, count=4)
    result = resolve_cuda_device(torch_module=FakeTorch(cuda), env={"CUDA_VISIBLE_DEVICES": "0,1,2,3"})
    assert result.logical_index == 0
    assert result.device_count == 4


def test_remapped_cuda_visible_devices_does_not_become_torch_index():
    cuda = FakeCuda(available=True, count=1)
    result = resolve_cuda_device(torch_module=FakeTorch(cuda), env={"CUDA_VISIBLE_DEVICES": "7"})
    assert result.logical_index == 0
    assert result.cuda_visible_devices == "7"
    assert cuda.selected == 0


def test_mig_uuid_visible_device_selects_logical_zero():
    mig_uuid = "MIG-GPU-12345678-1234-5678-9abc-def012345678/1/0"
    cuda = FakeCuda(available=True, count=1)
    result = resolve_cuda_device(torch_module=FakeTorch(cuda), env={"CUDA_VISIBLE_DEVICES": mig_uuid})
    assert result.logical_index == 0
    assert result.cuda_visible_devices == mig_uuid


def test_cuda_available_but_device_count_zero_raises():
    cuda = FakeCuda(available=True, count=0)
    with pytest.raises(RuntimeError, match="zero usable logical devices"):
        resolve_cuda_device(torch_module=FakeTorch(cuda), env={"CUDA_VISIBLE_DEVICES": "0"})


def test_invalid_requested_logical_index_raises():
    cuda = FakeCuda(available=True, count=1)
    with pytest.raises(RuntimeError, match="Requested logical CUDA device 1 is invalid"):
        resolve_cuda_device(requested_index=1, torch_module=FakeTorch(cuda), env={})


def test_get_device_properties_failure_raises_clear_error():
    cuda = FakeCuda(available=True, count=1, property_error=AssertionError("Invalid device id"))
    with pytest.raises(RuntimeError, match="Could not initialize logical CUDA device 0"):
        resolve_cuda_device(torch_module=FakeTorch(cuda), env={"SLURM_LOCALID": "0"})


def test_cuda_unavailable_can_be_nonfatal_for_check_only():
    cuda = FakeCuda(available=False, count=0)
    result = resolve_cuda_device(require_cuda=False, torch_module=FakeTorch(cuda), env={})
    assert result.device is None
    assert result.logical_index is None
    assert result.gpu_name == "cuda_unavailable"


def test_cuda_unavailable_raises_when_required():
    cuda = FakeCuda(available=False, count=0)
    with pytest.raises(RuntimeError, match="CUDA is unavailable"):
        resolve_cuda_device(require_cuda=True, torch_module=FakeTorch(cuda), env={})
