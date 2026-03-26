"""MediaPipe Hands wrapper (Tasks API - MediaPipe 0.10+).

Exposes a clean ``HandResult`` dataclass with normalised landmark arrays
so the rest of the pipeline never touches MediaPipe internals directly.

On first use, downloads the hand_landmarker.task model (~8 MB) to
~/.config/nami/hand_landmarker.task automatically.
"""

from __future__ import annotations

import urllib.request
from dataclasses import dataclass
from pathlib import Path

import mediapipe as mp  # type: ignore[import-untyped]
import numpy as np
from mediapipe.tasks import python as _mp_python  # type: ignore[import-untyped]
from mediapipe.tasks.python import vision as _mp_vision  # type: ignore[import-untyped]

_MODEL_URL = (
    "https://storage.googleapis.com/mediapipe-models/"
    "hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"
)
_MODEL_PATH = Path.home() / ".nami" / "hand_landmarker.task"


def _ensure_model() -> Path:
    if not _MODEL_PATH.exists():
        _MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
        print(f"Downloading hand landmark model to {_MODEL_PATH} ...")
        urllib.request.urlretrieve(_MODEL_URL, _MODEL_PATH)
        print("Download complete.")
    return _MODEL_PATH


@dataclass
class HandResult:
    """Normalised landmarks for a single detected hand.

    ``landmarks`` is a (21, 3) float32 array with values in [0, 1] for x/y
    and the MediaPipe world-space z for depth.
    ``handedness``: "Left" or "Right".
    """

    landmarks: np.ndarray  # shape (21, 3)
    handedness: str


class HandTracker:
    """Wrapper around mediapipe.tasks.python.vision.HandLandmarker."""

    def __init__(
        self,
        max_num_hands: int = 2,
        min_detection_confidence: float = 0.7,
        min_tracking_confidence: float = 0.5,
    ) -> None:
        model_path = _ensure_model()
        options = _mp_vision.HandLandmarkerOptions(
            base_options=_mp_python.BaseOptions(model_asset_path=str(model_path)),
            num_hands=max_num_hands,
            min_hand_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
        )
        self._detector = _mp_vision.HandLandmarker.create_from_options(options)

    def process(self, bgr_frame: np.ndarray) -> list[HandResult]:
        """Return a list of HandResult, one per detected hand."""
        rgb = bgr_frame[:, :, ::-1]  # BGR -> RGB
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        result = self._detector.detect(mp_image)

        if not result.hand_landmarks:
            return []

        out: list[HandResult] = []
        for lm_list, handedness_list in zip(result.hand_landmarks, result.handedness):
            arr = np.array(
                [[lm.x, lm.y, lm.z] for lm in lm_list], dtype=np.float32
            )
            side = handedness_list[0].display_name  # "Left" or "Right"
            out.append(HandResult(landmarks=arr, handedness=side))
        return out

    def close(self) -> None:
        self._detector.close()
