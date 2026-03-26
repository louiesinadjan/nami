"""Transfer curve functions.

All functions map a float in [0, 1] -> [0, 1].
Used to shape the gesture -> CC relationship before scaling to 0-127.
"""

from __future__ import annotations

import math


def linear(x: float, **_: float) -> float:
    return float(x)


def exponential(x: float, exponent: float = 2.0, **_: float) -> float:
    """Power curve. exponent > 1 = more response at high end."""
    return float(x ** exponent)


def s_curve(x: float, steepness: float = 10.0, **_: float) -> float:
    """Sigmoid-shaped S-curve centred at 0.5."""
    return 1.0 / (1.0 + math.exp(-steepness * (x - 0.5)))


def deadzone(x: float, low: float = 0.1, high: float = 0.9, **_: float) -> float:
    """Clamp values outside [low, high] to 0 and 1 respectively,
    then rescale the interior to [0, 1]."""
    if x <= low:
        return 0.0
    if x >= high:
        return 1.0
    return (x - low) / (high - low)


CURVE_REGISTRY: dict[str, object] = {
    "linear": linear,
    "exponential": exponential,
    "s_curve": s_curve,
    "deadzone": deadzone,
}
