"""Webcam capture running in a background thread."""

from __future__ import annotations

import threading
from typing import Optional

import cv2
import numpy as np


class CaptureThread:
    """Grabs frames from the webcam in a dedicated thread.

    The latest frame is always available via ``latest_frame``.
    Old frames are dropped if the consumer is slow.
    """

    def __init__(self, camera_index: int = 0) -> None:
        self._cap = cv2.VideoCapture(camera_index)
        if not self._cap.isOpened():
            raise RuntimeError(f"Cannot open camera {camera_index}")

        self._frame: Optional[np.ndarray] = None
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)

    @property
    def latest_frame(self) -> Optional[np.ndarray]:
        with self._lock:
            return self._frame

    def start(self) -> None:
        self._thread.start()

    def stop(self) -> None:
        self._stop_event.set()
        self._thread.join(timeout=2.0)
        self._cap.release()

    def _run(self) -> None:
        while not self._stop_event.is_set():
            ret, frame = self._cap.read()
            if ret:
                with self._lock:
                    self._frame = frame
