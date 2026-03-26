"""Converts mapped parameter values to MIDI CC messages.

Suppresses redundant sends: if a CC value hasn't changed since the last
frame, no message is sent, preventing MIDI spam to the DAW.
"""

from __future__ import annotations

import mido  # type: ignore[import-untyped]

from nami.midi.port import MidiPort

_CHANNEL = 0  # MIDI channel 1 (0-indexed)


class MidiSender:
    """Sends CC messages via a MidiPort, with redundant-send suppression."""

    def __init__(self, port: MidiPort, channel: int = _CHANNEL) -> None:
        self._port = port
        self._channel = channel
        self._last: dict[int, int] = {}

    def send(self, cc_values: dict[int, float]) -> None:
        """Send CC messages for values that have changed.

        Args:
            cc_values: {cc_number: float_0_to_1}
        """
        for cc, value in cc_values.items():
            scaled = int(round(value * 127))
            scaled = max(0, min(127, scaled))
            if self._last.get(cc) == scaled:
                continue
            self._last[cc] = scaled
            msg = mido.Message(
                "control_change",
                channel=self._channel,
                control=cc,
                value=scaled,
            )
            self._port.send(msg)
