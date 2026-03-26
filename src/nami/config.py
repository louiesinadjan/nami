"""Load and validate Nami configuration from YAML."""

from __future__ import annotations

import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

_USER_CONFIG_DIR = Path.home() / ".nami"
_DEFAULT_CONFIG = Path(__file__).parent.parent.parent / "configs" / "default.yaml"


@dataclass
class GestureMapping:
    gesture: str
    cc: int
    smoothing: str = "one_euro"
    smoothing_params: dict[str, float] = field(default_factory=dict)
    curve: str = "linear"
    curve_params: dict[str, float] = field(default_factory=dict)
    min_val: float = 0.0
    max_val: float = 1.0


@dataclass
class NamiConfig:
    port_name: str
    camera_index: int
    target_fps: int
    mappings: list[GestureMapping]

    @classmethod
    def load(cls, path: Path | None = None) -> "NamiConfig":
        """Load config from path, falling back to user config then default."""
        if path is None:
            user_cfg = _USER_CONFIG_DIR / "config.yaml"
            if not user_cfg.exists():
                _USER_CONFIG_DIR.mkdir(parents=True, exist_ok=True)
                shutil.copy(_DEFAULT_CONFIG, user_cfg)
            path = user_cfg

        raw: dict[str, Any] = yaml.safe_load(path.read_text())
        mappings = [GestureMapping(**m) for m in raw.get("mappings", [])]
        return cls(
            port_name=raw.get("port_name", "Nami"),
            camera_index=raw.get("camera_index", 0),
            target_fps=raw.get("target_fps", 30),
            mappings=mappings,
        )
