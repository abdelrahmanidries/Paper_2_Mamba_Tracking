"""Synthetic degradation tools for RGB tracking experiments."""

from .pipeline import (
    apply_degradation,
    apply_pair_degradation,
    degrade_tracking_pair,
    sample_degradation_pair,
)
from .protocols import (
    DEGRADATION_TYPES,
    PAIR_MODES,
    SEVERITIES,
    get_default_protocol,
    load_protocol,
    save_protocol,
    validate_protocol,
)

__all__ = [
    "DEGRADATION_TYPES",
    "PAIR_MODES",
    "SEVERITIES",
    "apply_degradation",
    "apply_pair_degradation",
    "degrade_tracking_pair",
    "get_default_protocol",
    "load_protocol",
    "sample_degradation_pair",
    "save_protocol",
    "validate_protocol",
]
