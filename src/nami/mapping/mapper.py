"""Config-driven router: gesture values -> {cc_number: float}."""

from __future__ import annotations

from typing import Callable

from nami.config import NamiConfig, GestureMapping
from nami.mapping.curves import CURVE_REGISTRY
from nami.mapping.smoothing import make_filter, EMAFilter, OneEuroFilter
from nami.tracking.geometry import GESTURE_REGISTRY


class Mapper:
    """Instantiated once at startup from a NamiConfig.

    Each call to ``process`` takes a dict of raw gesture values
    (keyed by gesture name) and returns a dict of {cc_number: float 0-1}.
    """

    def __init__(self, config: NamiConfig) -> None:
        self._mappings: list[GestureMapping] = config.mappings
        self._filters: list[EMAFilter | OneEuroFilter] = [
            make_filter(m.smoothing, m.smoothing_params, freq=config.target_fps)
            for m in config.mappings
        ]
        self._curves: list[Callable[..., float]] = [
            CURVE_REGISTRY[m.curve]  # type: ignore[index]
            for m in config.mappings
        ]

    def process(self, gesture_values: dict[str, float]) -> dict[int, float]:
        """Map raw gesture values to CC output values.

        Args:
            gesture_values: {gesture_name: raw_float_0_to_1}

        Returns:
            {cc_number: float_0_to_1}
        """
        output: dict[int, float] = {}
        for mapping, filt, curve in zip(self._mappings, self._filters, self._curves):
            raw = gesture_values.get(mapping.gesture)
            if raw is None:
                continue
            # Remap to [min_val, max_val] window
            windowed = mapping.min_val + raw * (mapping.max_val - mapping.min_val)
            # Apply transfer curve
            curved = curve(windowed, **mapping.curve_params)
            # Smooth
            smoothed = filt(curved)
            output[mapping.cc] = float(smoothed)
        return output
