"""Numerical correctness tests for smoothing filters."""

from __future__ import annotations

import pytest

from nami.mapping.smoothing import EMAFilter, OneEuroFilter, make_filter


def test_ema_initialises_to_first_value():
    f = EMAFilter(alpha=0.5)
    assert f(1.0) == pytest.approx(1.0)


def test_ema_converges():
    f = EMAFilter(alpha=0.5)
    val = 0.0
    for _ in range(50):
        val = f(1.0)
    assert val > 0.99


def test_ema_smooths():
    f = EMAFilter(alpha=0.1)
    f(0.0)
    result = f(1.0)
    # With alpha=0.1 a single step should move < 0.15
    assert result < 0.15


def test_one_euro_initialises_to_first_value():
    f = OneEuroFilter(freq=30.0)
    assert f(0.5) == pytest.approx(0.5)


def test_one_euro_converges():
    f = OneEuroFilter(freq=30.0, min_cutoff=5.0, beta=0.1)
    val = 0.0
    for _ in range(100):
        val = f(1.0)
    assert val > 0.99


def test_make_filter_ema():
    f = make_filter("ema", {"alpha": 0.3})
    assert isinstance(f, EMAFilter)


def test_make_filter_one_euro():
    f = make_filter("one_euro", {}, freq=60.0)
    assert isinstance(f, OneEuroFilter)


def test_make_filter_unknown():
    with pytest.raises(ValueError, match="Unknown smoothing filter"):
        make_filter("nonexistent", {})
