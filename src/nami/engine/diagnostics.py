"""Optional OpenCV debug window with hand skeleton and HUD overlay.

Only active when the engine is started with ``debug=True``.
Renders current CC values, FPS, and hand landmarks on the camera frame.
"""

from __future__ import annotations

import time

import cv2
import numpy as np

_FONT = cv2.FONT_HERSHEY_SIMPLEX
_GREEN = (0, 255, 80)
_WHITE = (255, 255, 255)
_CYAN = (255, 220, 0)

# MediaPipe hand landmark connections (fixed 21-point graph)
_HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),        # thumb
    (0, 5), (5, 6), (6, 7), (7, 8),         # index
    (0, 9), (9, 10), (10, 11), (11, 12),    # middle
    (0, 13), (13, 14), (14, 15), (15, 16),  # ring
    (0, 17), (17, 18), (18, 19), (19, 20),  # pinky
    (5, 9), (9, 13), (13, 17),              # palm knuckles
]


class DebugWindow:
    """Manages the OpenCV preview window."""

    def __init__(self, window_name: str = "Nami - debug") -> None:
        self._name = window_name
        self._fps_times: list[float] = []

    def draw(
        self,
        frame: np.ndarray,
        hand_results: list,  # list[HandResult] - avoid circular import
        cc_values: dict[int, float],
    ) -> bool:
        """Draw overlay and show frame. Returns False if window was closed."""
        now = time.perf_counter()
        self._fps_times.append(now)
        self._fps_times = [t for t in self._fps_times if now - t < 1.0]
        fps = len(self._fps_times)

        display = frame.copy()
        h, w = display.shape[:2]

        # Draw hand landmarks
        for hand in hand_results:
            pts = [(int(lm[0] * w), int(lm[1] * h)) for lm in hand.landmarks]
            for a, b in _HAND_CONNECTIONS:
                cv2.line(display, pts[a], pts[b], _GREEN, 2)
            for pt in pts:
                cv2.circle(display, pt, 4, _CYAN, -1)

        # HUD: FPS
        cv2.putText(display, f"FPS: {fps}", (10, 25), _FONT, 0.7, _GREEN, 2)

        # HUD: CC values
        y = 55
        for cc, val in sorted(cc_values.items()):
            text = f"CC{cc:03d}: {int(val * 127):3d}  ({val:.2f})"
            cv2.putText(display, text, (10, y), _FONT, 0.6, _WHITE, 1)
            y += 22

        cv2.imshow(self._name, display)
        return cv2.waitKey(1) != ord("q")

    def close(self) -> None:
        cv2.destroyAllWindows()
