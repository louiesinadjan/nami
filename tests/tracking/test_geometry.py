"""Unit tests for geometry.py — no hardware required."""

from __future__ import annotations

import numpy as np
import pytest

from nami.tracking.geometry import (
    wrist_elevation,
    finger_spread,
    palm_rotation,
    pinch_distance,
)


def test_wrist_elevation_range(default_landmarks):
    val = wrist_elevation(default_landmarks)
    assert 0.0 <= val <= 1.0


def test_wrist_elevation_top():
    lm = np.zeros((21, 3), dtype=np.float32)
    lm[0, 1] = 0.0  # y=0 means top of frame
    assert wrist_elevation(lm) == pytest.approx(1.0)


def test_wrist_elevation_bottom():
    lm = np.zeros((21, 3), dtype=np.float32)
    lm[0, 1] = 1.0  # y=1 means bottom of frame
    assert wrist_elevation(lm) == pytest.approx(0.0)


def test_finger_spread_range(default_landmarks):
    val = finger_spread(default_landmarks)
    assert 0.0 <= val <= 1.0


def test_finger_spread_zero_hand_size():
    lm = np.zeros((21, 3), dtype=np.float32)
    assert finger_spread(lm) == 0.0


def test_palm_rotation_range(default_landmarks):
    val = palm_rotation(default_landmarks)
    assert 0.0 <= val <= 1.0


def test_pinch_distance_range(default_landmarks):
    val = pinch_distance(default_landmarks)
    assert 0.0 <= val <= 1.0


def test_pinch_distance_zero_hand_size():
    lm = np.zeros((21, 3), dtype=np.float32)
    assert pinch_distance(lm) == 0.0
