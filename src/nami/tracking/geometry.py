"""Stateless geometry functions: landmark arrays -> scalar gesture values.

All functions accept a (21, 3) float32 landmark array (x, y, z normalised
to [0,1]) and return a float in [0, 1] unless documented otherwise.

MediaPipe hand landmark indices:
  0  WRIST
  4  THUMB_TIP
  5  INDEX_FINGER_MCP
  8  INDEX_FINGER_TIP
  9  MIDDLE_FINGER_MCP
  12 MIDDLE_FINGER_TIP
  13 RING_FINGER_MCP
  16 RING_FINGER_TIP
  17 PINKY_MCP
  20 PINKY_TIP
"""

from __future__ import annotations

import math

import numpy as np

# Landmark indices
WRIST = 0
THUMB_TIP = 4
INDEX_MCP = 5
INDEX_TIP = 8
MIDDLE_MCP = 9
MIDDLE_TIP = 12
RING_MCP = 13
RING_TIP = 16
PINKY_MCP = 17
PINKY_TIP = 20


def wrist_elevation(landmarks: np.ndarray) -> float:
    """Vertical position of the wrist normalised to [0, 1].

    0 = bottom of frame, 1 = top of frame (y axis is inverted in image coords).
    """
    return float(np.clip(1.0 - landmarks[WRIST, 1], 0.0, 1.0))


def finger_spread(landmarks: np.ndarray) -> float:
    """Spread of the four fingers (index to pinky) normalised to [0, 1].

    Measured as the distance between the index MCP and pinky MCP,
    scaled by the hand size (wrist-to-middle-MCP distance).
    """
    hand_size = float(np.linalg.norm(landmarks[MIDDLE_MCP, :2] - landmarks[WRIST, :2]))
    if hand_size < 1e-6:
        return 0.0
    spread = float(np.linalg.norm(landmarks[PINKY_MCP, :2] - landmarks[INDEX_MCP, :2]))
    return float(np.clip(spread / hand_size, 0.0, 1.0))


def palm_rotation(landmarks: np.ndarray) -> float:
    """In-plane rotation of the palm in [0, 1] (mapped from -π to π).

    Angle of the vector from wrist to middle-finger MCP relative to vertical.
    """
    vec = landmarks[MIDDLE_MCP, :2] - landmarks[WRIST, :2]
    angle = math.atan2(float(vec[0]), float(-vec[1]))  # 0 = pointing up
    return float(np.clip((angle + math.pi) / (2 * math.pi), 0.0, 1.0))


def pinch_distance(landmarks: np.ndarray) -> float:
    """Distance between thumb tip and index tip normalised to [0, 1].

    Scaled by hand size. 0 = fully pinched, 1 = fully open.
    """
    hand_size = float(np.linalg.norm(landmarks[MIDDLE_MCP, :2] - landmarks[WRIST, :2]))
    if hand_size < 1e-6:
        return 0.0
    dist = float(np.linalg.norm(landmarks[THUMB_TIP, :2] - landmarks[INDEX_TIP, :2]))
    return float(np.clip(dist / hand_size, 0.0, 1.0))


# Registry used by mapper.py to look up gesture functions by name
GESTURE_REGISTRY: dict[str, object] = {
    "wrist_elevation": wrist_elevation,
    "finger_spread": finger_spread,
    "palm_rotation": palm_rotation,
    "pinch_distance": pinch_distance,
}
