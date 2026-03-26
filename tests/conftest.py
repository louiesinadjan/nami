"""Shared test fixtures."""

from __future__ import annotations

import numpy as np
import pytest


@pytest.fixture
def flat_landmarks() -> np.ndarray:
    """A (21, 3) landmark array with all points at the origin."""
    return np.zeros((21, 3), dtype=np.float32)


@pytest.fixture
def default_landmarks() -> np.ndarray:
    """A (21, 3) landmark array representing a rough open-palm pose."""
    lm = np.zeros((21, 3), dtype=np.float32)
    # Wrist at bottom centre
    lm[0] = [0.5, 0.8, 0.0]
    # Middle finger MCP roughly above wrist
    lm[9] = [0.5, 0.5, 0.0]
    # Index MCP / Pinky MCP spread apart
    lm[5] = [0.4, 0.55, 0.0]
    lm[17] = [0.6, 0.55, 0.0]
    # Fingertips
    lm[8] = [0.38, 0.2, 0.0]   # index tip
    lm[4] = [0.35, 0.45, 0.0]  # thumb tip
    return lm
