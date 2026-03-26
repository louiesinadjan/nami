# Nami

Real-time gesture-controlled audio modulation. Move your hands in front of a webcam; Nami maps the motion to MIDI CC messages that control knobs, effects, and VST parameters in your DAW.

## How it works

```
Webcam → MediaPipe hand tracking → gesture values → smoothing + curves → MIDI CC → Logic Pro (or any DAW)
```

Nami opens a virtual MIDI port named **"Nami"**. In Logic, go to *Controller Assignments* and map any CC number to any parameter — filter cutoff, reverb send, compressor threshold, a VST knob, anything.

## Gestures

| Gesture | Description |
|---|---|
| `wrist_elevation` | Vertical position of the wrist (low → high) |
| `pinch_distance` | Distance between thumb tip and index tip |
| `finger_spread` | Spread of index-to-pinky fingers |
| `palm_rotation` | In-plane rotation of the palm |

Each gesture maps to a configurable MIDI CC number with independent smoothing and transfer curve settings.

## Install

```bash
conda env create -f environment.yml
conda activate nami
pip install -e ".[dev]"
```

## Usage

```bash
# Start with default config (~/.config/nami/config.yaml, created on first run)
nami run

# Show camera window with hand skeleton + CC value HUD
nami run --debug

# Use a custom config
nami run --config configs/examples/filter_sweep.yaml

# List available MIDI ports
nami list-ports
```

## Configuration

On first run, `~/.config/nami/config.yaml` is created from `configs/default.yaml`. Edit it to change the gesture-to-CC mapping, smoothing parameters, and transfer curves.

```yaml
mappings:
  - gesture: wrist_elevation
    cc: 74            # MIDI CC number — map this in Logic
    smoothing: one_euro
    curve: linear
```

Example configs are in `configs/examples/`.

## Development

```bash
pytest tests/          # run all tests (no hardware required)
ruff check src/        # lint
```

## Future / Protocol Support

Currently outputs MIDI CC only, targeting Logic Pro. The output layer (`src/nami/midi/`) is designed behind a simple `send(cc, value)` interface so alternative protocols (OSC, etc.) can be added later without changing the tracking or mapping pipeline.

## Tech stack

- [MediaPipe](https://mediapipe.dev/) — hand landmark detection
- [OpenCV](https://opencv.org/) — webcam capture and debug window
- [mido](https://mido.readthedocs.io/) + [rtmidi](https://github.com/thestk/rtmidi) — MIDI output
- [NumPy](https://numpy.org/) — signal processing
- [Click](https://click.palletsprojects.com/) — CLI
