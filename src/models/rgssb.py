"""Minimal Restoration-Guided State Space Block.

This module is a standalone proof-of-concept block for feature-level
restoration in template-search tracking. The state branch is a lightweight
SSM-style proxy implemented with dependency-free gated depthwise 1D
convolution; it is not a full Mamba implementation.
"""

from __future__ import annotations

from typing import Optional, Tuple

import torch
from torch import nn


class RestorationGuidedSSB(nn.Module):
    """Minimal RG-SSB block with shape-preserving token input/output.

    Args:
        dim: Token channel dimension.
        spatial_size: Optional default spatial size used to reshape tokens
            from ``[B, N, C]`` to ``[B, C, H, W]`` for the local branch.
        local_kernel_size: Kernel size for the local depthwise convolution.
        channel_reduction: Reduction ratio for channel attention.
        use_local_branch: Enable local enhancement branch.
        use_channel_attention: Enable squeeze-excitation channel attention.
        use_state_branch: Enable lightweight SSM-style sequence branch.
        dropout: Dropout probability before residual addition.
    """

    def __init__(
        self,
        dim: int,
        spatial_size: Optional[Tuple[int, int]] = None,
        local_kernel_size: int = 3,
        channel_reduction: int = 4,
        use_local_branch: bool = True,
        use_channel_attention: bool = True,
        use_state_branch: bool = True,
        dropout: float = 0.0,
    ) -> None:
        super().__init__()
        if dim <= 0:
            raise ValueError("dim must be a positive integer")
        if local_kernel_size <= 0 or local_kernel_size % 2 == 0:
            raise ValueError("local_kernel_size must be a positive odd integer")
        if channel_reduction <= 0:
            raise ValueError("channel_reduction must be a positive integer")

        self.dim = int(dim)
        self.spatial_size = spatial_size
        self.use_local_branch = bool(use_local_branch)
        self.use_channel_attention = bool(use_channel_attention)
        self.use_state_branch = bool(use_state_branch)

        self.norm = nn.LayerNorm(dim)

        padding = local_kernel_size // 2
        self.local_depthwise = nn.Conv2d(
            dim,
            dim,
            kernel_size=local_kernel_size,
            padding=padding,
            groups=dim,
        )
        self.local_pointwise = nn.Conv2d(dim, dim, kernel_size=1)

        hidden_dim = max(1, dim // channel_reduction)
        self.channel_mlp = nn.Sequential(
            nn.Linear(dim, hidden_dim),
            nn.GELU(),
            nn.Linear(hidden_dim, dim),
            nn.Sigmoid(),
        )

        self.state_depthwise = nn.Conv1d(
            dim,
            dim,
            kernel_size=3,
            padding=1,
            groups=dim,
        )
        self.state_gate = nn.Linear(dim, dim)

        self.activation = nn.GELU()
        self.out_proj = nn.Linear(dim, dim)
        self.dropout = nn.Dropout(dropout)

    def _resolve_spatial_size(
        self,
        token_count: int,
        spatial_size: Optional[Tuple[int, int]],
    ) -> Tuple[int, int]:
        size = spatial_size if spatial_size is not None else self.spatial_size
        if size is None:
            raise ValueError("spatial_size is required when the local branch is enabled")

        height, width = int(size[0]), int(size[1])
        if height <= 0 or width <= 0:
            raise ValueError("spatial_size values must be positive")
        if height * width != token_count:
            raise ValueError(
                f"spatial_size {size} is incompatible with token count {token_count}; "
                f"expected H*W == N"
            )
        return height, width

    def _local_branch(self, x: torch.Tensor, spatial_size: Optional[Tuple[int, int]]) -> torch.Tensor:
        batch, token_count, channels = x.shape
        height, width = self._resolve_spatial_size(token_count, spatial_size)
        feature_map = x.transpose(1, 2).reshape(batch, channels, height, width)
        feature_map = self.local_depthwise(feature_map)
        feature_map = self.local_pointwise(feature_map)
        feature_map = self.activation(feature_map)
        return feature_map.flatten(2).transpose(1, 2)

    def _channel_attention_branch(self, x: torch.Tensor) -> torch.Tensor:
        weights = self.channel_mlp(x.mean(dim=1)).unsqueeze(1)
        return x * weights

    def _state_branch(self, x: torch.Tensor) -> torch.Tensor:
        sequence_features = self.state_depthwise(x.transpose(1, 2)).transpose(1, 2)
        gate = torch.sigmoid(self.state_gate(x))
        return self.activation(sequence_features) * gate

    def forward(
        self,
        x: torch.Tensor,
        template_len: Optional[int] = None,
        search_len: Optional[int] = None,
        spatial_size: Optional[Tuple[int, int]] = None,
    ) -> torch.Tensor:
        """Apply RG-SSB to token features.

        Args:
            x: Token tensor with shape ``[B, N, C]``.
            template_len: Reserved for future template/search split support.
            search_len: Optional expected search token count.
            spatial_size: Optional runtime spatial size override.

        Returns:
            Tensor with the same shape as ``x``.
        """

        if x.ndim != 3:
            raise ValueError(f"Expected x with shape [B, N, C], got {tuple(x.shape)}")
        if x.shape[-1] != self.dim:
            raise ValueError(f"Expected token dim {self.dim}, got {x.shape[-1]}")
        if search_len is not None and int(search_len) != x.shape[1]:
            raise ValueError(f"search_len {search_len} does not match token count {x.shape[1]}")
        if template_len is not None and int(template_len) < 0:
            raise ValueError("template_len must be non-negative when provided")

        residual = x
        x_norm = self.norm(x)

        branches = []
        if self.use_local_branch:
            branches.append(self._local_branch(x_norm, spatial_size))
        if self.use_channel_attention:
            branches.append(self._channel_attention_branch(x_norm))
        if self.use_state_branch:
            branches.append(self._state_branch(x_norm))

        if branches:
            fused = torch.stack(branches, dim=0).mean(dim=0)
        else:
            fused = x_norm

        out = self.out_proj(fused)
        out = self.dropout(out)
        return residual + out
