# PicoPython

PicoPython is a conservative custom MicroPython firmware for the Raspberry Pi
Pico 2 (RP2350). It uses the MicroPython v1.29.0 RP2 port and keeps the normal
USB CDC REPL, core Python runtime, filesystem support, and RP2 hardware APIs.
Display support is intentionally out of scope; the Pico remains usable over
USB serial without a display.

## Repository layout

- `board/PICO_PYTHON/`: custom board configuration based on upstream
  `RPI_PICO2` settings.
- `config/features.cmake`: feature decisions and current build notes.
- `tests/`: REPL, language, filesystem, hardware API, and memory checks.
- `micropython/`: upstream MicroPython pinned as a Git submodule.
- `patches/`: host-build compatibility patches; the Windows patch only adapts
  qstr preprocessing and does not change firmware features.
- `builds/`: local build output; intentionally excluded from Git.

## Source setup

```powershell
git submodule update --init micropython
git -C micropython submodule update --init --recursive
```

The `micropython` gitlink is pinned to the upstream `v1.29.0` commit. On
Windows, apply the host compatibility patch before building:

```powershell
git -C micropython apply --ignore-space-change ../patches/windows-qstr-preprocess.patch
```

## Build and validation status

Build the unchanged `RPI_PICO2` baseline before the custom board, using
separate directories under `builds/stock` and `builds/stripped`. The custom
board uses the RP2350 ARM platform, `PICO_BOARD=pico2`, the upstream Pico 2
pin map, and the same 3 MiB flash-storage allocation.

No firmware image has been produced or flashed yet. In the current Windows
environment, App Control blocks the generated `mpy-cross.exe`; a
policy-approved MicroPython v1.29.0-compatible executable is needed to
complete frozen-module builds. Do not bypass App Control. Flashing remains
deferred until the stock and custom builds pass validation and is explicitly
authorized.

For USB REPL testing, use:

```powershell
py -m serial.tools.miniterm COM8 115200
```

Filesystem persistence tests use a dedicated marker file and do not format
the filesystem. Hardware tests initially verify API availability and avoid
driving unverified pins or attached peripherals.
