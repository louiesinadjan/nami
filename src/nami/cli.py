"""CLI entry point for Nami."""

from __future__ import annotations

from pathlib import Path

import click

from nami import __version__
from nami.config import NamiConfig


@click.group()
@click.version_option(__version__)
def main() -> None:
    """Nami - gesture-controlled audio modulation."""


@main.command()
@click.option("--config", "-c", type=click.Path(exists=True, path_type=Path), default=None,
              help="Path to config YAML (defaults to ~/.config/nami/config.yaml).")
@click.option("--debug", is_flag=True, default=False,
              help="Show camera window with hand skeleton and HUD overlay.")
@click.option("--camera", default=None, type=int,
              help="Camera device index (overrides config).")
def run(config: Path | None, debug: bool, camera: int | None) -> None:
    """Start the gesture-to-MIDI engine."""
    from nami.engine.loop import Engine

    cfg = NamiConfig.load(config)
    if camera is not None:
        cfg.camera_index = camera

    engine = Engine(cfg, debug=debug)
    try:
        engine.start()
    except KeyboardInterrupt:
        click.echo("\nStopped.")
    finally:
        engine.stop()


@main.command("list-ports")
def list_ports() -> None:
    """List available MIDI output ports."""
    import mido  # type: ignore[import-untyped]

    ports = mido.get_output_names()
    if not ports:
        click.echo("No MIDI output ports found.")
    else:
        for p in ports:
            click.echo(p)
