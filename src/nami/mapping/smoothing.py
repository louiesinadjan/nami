"""Signal smoothing filters for gesture values.

Each filter is a stateful object with a single ``__call__(value) -> float`` interface.

Available filters:
- ``EMAFilter``      - exponential moving average, simple and low-overhead
- ``OneEuroFilter``  - velocity-adaptive, best feel for hand tracking data
"""

from __future__ import annotations

import math
from typing import Optional


class EMAFilter:
    """Exponential moving average filter.

    ``alpha`` in (0, 1]: higher = more responsive, lower = smoother.
    """

    def __init__(self, alpha: float = 0.2) -> None:
        self._alpha = alpha
        self._value: Optional[float] = None

    def __call__(self, value: float) -> float:
        if self._value is None:
            self._value = value
        else:
            self._value = self._alpha * value + (1.0 - self._alpha) * self._value
        return self._value


class OneEuroFilter:
    """One-Euro filter (Casiez et al. 2012).

    Adapts cutoff frequency based on signal velocity - smooth when slow,
    responsive when fast. Ideal for hand tracking.

    Args:
        freq:      Sampling frequency in Hz (e.g. 30).
        min_cutoff: Minimum cutoff frequency in Hz. Lower = smoother at rest.
        beta:      Speed coefficient. Higher = less lag when moving fast.
        d_cutoff:  Cutoff for the derivative filter.
    """

    def __init__(
        self,
        freq: float = 30.0,
        min_cutoff: float = 1.0,
        beta: float = 0.007,
        d_cutoff: float = 1.0,
    ) -> None:
        self._freq = freq
        self._min_cutoff = min_cutoff
        self._beta = beta
        self._d_cutoff = d_cutoff

        self._x: Optional[float] = None
        self._dx: float = 0.0

    @staticmethod
    def _alpha(cutoff: float, freq: float) -> float:
        te = 1.0 / freq
        tau = 1.0 / (2 * math.pi * cutoff)
        return 1.0 / (1.0 + tau / te)

    def __call__(self, value: float) -> float:
        if self._x is None:
            self._x = value
            return value

        # Derivative
        dx = (value - self._x) * self._freq
        a_d = self._alpha(self._d_cutoff, self._freq)
        self._dx = a_d * dx + (1.0 - a_d) * self._dx

        # Adaptive cutoff
        cutoff = self._min_cutoff + self._beta * abs(self._dx)
        a = self._alpha(cutoff, self._freq)
        self._x = a * value + (1.0 - a) * self._x
        return self._x


def make_filter(name: str, params: dict[str, float], freq: float = 30.0) -> EMAFilter | OneEuroFilter:
    """Factory: returns a configured filter by name."""
    if name == "ema":
        return EMAFilter(alpha=params.get("alpha", 0.2))
    if name == "one_euro":
        return OneEuroFilter(
            freq=freq,
            min_cutoff=params.get("min_cutoff", 1.0),
            beta=params.get("beta", 0.007),
            d_cutoff=params.get("d_cutoff", 1.0),
        )
    raise ValueError(f"Unknown smoothing filter: {name!r}")
