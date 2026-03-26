"""Virtual MIDI port lifecycle.

Opens a virtual output port named "Nami" (or as configured).
Logic Pro will see this port in its MIDI controller list.
"""

from __future__ import annotations

import mido  # type: ignore[import-untyped]


class MidiPort:
    """Manages a virtual MIDI output port."""

    def __init__(self, name: str = "Nami") -> None:
        self._name = name
        self._port: mido.ports.BaseOutput | None = None

    @property
    def name(self) -> str:
        return self._name

    def open(self) -> None:
        self._port = mido.open_output(self._name, virtual=True)

    def close(self) -> None:
        if self._port is not None:
            self._port.close()
            self._port = None

    def send(self, message: mido.Message) -> None:
        if self._port is None:
            raise RuntimeError("MIDI port is not open")
        self._port.send(message)

    def __enter__(self) -> "MidiPort":
        self.open()
        return self

    def __exit__(self, *_: object) -> None:
        self.close()
