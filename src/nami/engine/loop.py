"""Main engine loop: webcam -> tracking -> mapping -> MIDI."""

from __future__ import annotations

import time

from nami.config import NamiConfig
from nami.mapping.mapper import Mapper
from nami.midi.port import MidiPort
from nami.midi.sender import MidiSender
from nami.tracking.capture import CaptureThread
from nami.tracking.geometry import GESTURE_REGISTRY
from nami.tracking.hands import HandTracker


class Engine:
    """Ties all subsystems together and runs the main loop."""

    def __init__(self, config: NamiConfig, debug: bool = False) -> None:
        self._config = config
        self._debug = debug
        self._running = False

        self._capture = CaptureThread(config.camera_index)
        self._tracker = HandTracker()
        self._mapper = Mapper(config)
        self._port = MidiPort(config.port_name)
        self._sender: MidiSender | None = None
        self._debug_window = None

    def start(self) -> None:
        self._capture.start()
        self._port.open()
        self._sender = MidiSender(self._port)

        if self._debug:
            from nami.engine.diagnostics import DebugWindow
            self._debug_window = DebugWindow()

        self._running = True
        self._loop()

    def stop(self) -> None:
        self._running = False
        self._capture.stop()
        self._tracker.close()
        self._port.close()
        if self._debug_window is not None:
            self._debug_window.close()

    def _loop(self) -> None:
        target_dt = 1.0 / self._config.target_fps

        while self._running:
            t0 = time.perf_counter()

            frame = self._capture.latest_frame
            if frame is None:
                time.sleep(0.001)
                continue

            # Track hands
            hand_results = self._tracker.process(frame)

            # Extract gesture values from the first detected hand
            gesture_values: dict[str, float] = {}
            if hand_results:
                lm = hand_results[0].landmarks
                for name, fn in GESTURE_REGISTRY.items():
                    gesture_values[name] = fn(lm)  # type: ignore[operator]

            # Map to CC values and send
            cc_values = self._mapper.process(gesture_values)
            if self._sender is not None:
                self._sender.send(cc_values)

            # Debug window
            if self._debug_window is not None:
                keep_open = self._debug_window.draw(frame, hand_results, cc_values)
                if not keep_open:
                    break

            # Frame pacing
            elapsed = time.perf_counter() - t0
            sleep = target_dt - elapsed
            if sleep > 0:
                time.sleep(sleep)
