"""Boundary and correctness tests for transfer curves."""

from __future__ import annotations

import pytest

from nami.mapping.curves import linear, exponential, s_curve, deadzone


@pytest.mark.parametrize("fn", [linear, exponential, s_curve])
def test_zero_maps_near_zero(fn):
    assert fn(0.0) == pytest.approx(0.0, abs=0.05)


@pytest.mark.parametrize("fn", [linear, exponential, s_curve])
def test_one_maps_near_one(fn):
    assert fn(1.0) == pytest.approx(1.0, abs=0.05)


def test_linear_midpoint():
    assert linear(0.5) == pytest.approx(0.5)


def test_exponential_concave():
    assert exponential(0.5, exponent=2.0) == pytest.approx(0.25)


def test_deadzone_clips_low():
    assert deadzone(0.05, low=0.1) == pytest.approx(0.0)


def test_deadzone_clips_high():
    assert deadzone(0.95, high=0.9) == pytest.approx(1.0)


def test_deadzone_interior():
    val = deadzone(0.5, low=0.0, high=1.0)
    assert val == pytest.approx(0.5)
