# C++ Smoothing Extension (placeholder)

This directory is reserved for a future pybind11 extension implementing
performance-critical signal processing in C++.

Candidates for migration here if sub-10ms latency becomes a requirement:
- One-Euro filter (currently in `src/nami/mapping/smoothing.py`)
- Savitzky-Golay filter
- Custom gesture feature extraction from raw landmark arrays

## Build setup (when needed)

Add a `CMakeLists.txt` here and a `[tool.hatch.build.hooks.custom]` entry
in `pyproject.toml` to compile the extension as part of `pip install`.
