"""Tests for MidiSender: CC scaling and redundant-send suppression."""

from __future__ import annotations

from unittest.mock import MagicMock, call

import pytest

from nami.midi.sender import MidiSender


@pytest.fixture
def mock_port():
    return MagicMock()


@pytest.fixture
def sender(mock_port):
    return MidiSender(mock_port, channel=0)


def test_send_scales_to_127(sender, mock_port):
    sender.send({74: 1.0})
    msg = mock_port.send.call_args[0][0]
    assert msg.value == 127


def test_send_scales_to_0(sender, mock_port):
    sender.send({74: 0.0})
    msg = mock_port.send.call_args[0][0]
    assert msg.value == 0


def test_send_midpoint(sender, mock_port):
    sender.send({74: 0.5})
    msg = mock_port.send.call_args[0][0]
    assert msg.value == 64


def test_redundant_send_suppressed(sender, mock_port):
    sender.send({74: 0.5})
    sender.send({74: 0.5})
    assert mock_port.send.call_count == 1


def test_changed_value_sent(sender, mock_port):
    sender.send({74: 0.0})
    sender.send({74: 1.0})
    assert mock_port.send.call_count == 2


def test_clamps_above_127(sender, mock_port):
    sender.send({74: 1.5})
    msg = mock_port.send.call_args[0][0]
    assert msg.value == 127


def test_clamps_below_0(sender, mock_port):
    sender.send({74: -0.5})
    msg = mock_port.send.call_args[0][0]
    assert msg.value == 0
