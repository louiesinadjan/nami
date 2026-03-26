#!/usr/bin/env python
"""List available MIDI output ports."""

import mido  # type: ignore[import-untyped]

ports = mido.get_output_names()
if not ports:
    print("No MIDI output ports found.")
else:
    for p in ports:
        print(p)
