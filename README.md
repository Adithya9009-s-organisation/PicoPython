# PicoPython

PicoPython is a conservative custom MicroPython firmware for the Raspberry Pi
Pico 2 (RP2350). It uses the MicroPython v1.29.0 RP2 port and keeps the normal
USB CDC REPL, core Python runtime, filesystem support, and selected RP2 hardware
APIs.
Display support is intentionally out of scope; the Pico remains usable over
USB serial without a display.

## Repository layout

- `board/PICO_PYTHON/`: custom board configuration based on upstream
  `RPI_PICO2` settings.
- `config/features.cmake`: feature decisions and current build notes.
- `config/stdlib_manifest.py`: prioritized compatibility module inventory;
  it does not freeze modules by itself.
- `docs/PICOPYTHON_V129_COMPATIBILITY.md`: compatibility scope, removal
  candidates, language audit, and acceptance rules.
- `tests/`: REPL, language, filesystem, hardware API, and memory checks.
- `micropython/`: upstream MicroPython pinned as a Git submodule.
- `patches/`: narrowly scoped MicroPython v1.29.0 build-compatibility patches.
- `builds/`: local build output; intentionally excluded from Git.
- `releases/v1.29.0/`: versioned RP2350 firmware candidates and comparison images.

## Source setup

```powershell
git submodule update --init micropython
git -C micropython submodule update --init --recursive
```

The `micropython` gitlink is pinned to the upstream `v1.29.0` commit. On
all hosts, apply the conditional module-table fix. The v1.29.0 generator
includes the `string` module registration even when `MICROPY_PY_TSTRINGS` is
disabled by the RP2 default; this fix omits that entry without enabling the
feature:

```sh
git -C micropython apply ../patches/micropython-v1.29.0-string-moduledefs.patch
git -C micropython apply ../patches/micropython-v1.29.0-pruned-features.patch
```

On Windows, also apply the qstr preprocessing adaptation:

```powershell
git -C micropython apply --ignore-space-change ../patches/windows-qstr-preprocess.patch
```

## Build and validation status

First build the source compiler, then the stock baseline and custom board in
separate directories, using low parallelism:

```sh
make -C micropython/mpy-cross -j2
make -C micropython/ports/rp2 BOARD=RPI_PICO2 BUILD="$PWD/builds/stock" -j2
make -C micropython/ports/rp2 BOARD_DIR="$PWD/board/PICO_PYTHON" BUILD="$PWD/builds/stripped" -j2
```

The custom board uses the RP2350 ARM platform, `PICO_BOARD=pico2`, the
upstream Pico 2 pin map, and the same 3 MiB flash-storage allocation. The
stock and custom builds now complete in the Linux Codespace. Their UF2 sizes
are 666,624 bytes and 661,504 bytes, respectively; see
[`docs/BUILD_RESULTS.md`](docs/BUILD_RESULTS.md) for hashes, tool versions,
and linker measurements. These are baseline measurements, not measurements
of the current removal candidate. The RP2 port still links mbedTLS.

The RP2350 wrapper-fix candidate retains asyncio/uasyncio, select, and
framebuf. Its versioned UF2 is
[`releases/v1.29.0/PicoPython-v1.29-wrapper-fix.uf2`](releases/v1.29.0/PicoPython-v1.29-wrapper-fix.uf2),
626,688 bytes, SHA-256
`2c610c7f061e0989dd80b849f4dfa5deb88392d1d78202897263468b171861a6`.
The earlier pre-wrapper-fix candidate is retained separately for comparison;
it has a reported `import rp2` failure and is not the recommended image.

The user reports that the wrapper-fix candidate passed Pico 2 boot/USB REPL,
filesystem read/write/delete, asyncio, and acceptance tests. Build, source,
and ELF checks were independently completed; the hardware results are
user-reported. See [`docs/BUILD_RESULTS.md`](docs/BUILD_RESULTS.md) and
[`docs/PR_REVIEW_REPORT.md`](docs/PR_REVIEW_REPORT.md) for details.

The Windows build remains subject to App Control blocking the locally built
`mpy-cross.exe`; use an approved Linux build environment rather than bypassing
that policy. Do not flash automatically; preserve the known-good firmware as
the rollback baseline.

For USB REPL testing, use:

```powershell
py -m serial.tools.miniterm COM8 115200
```

Filesystem persistence tests use a dedicated marker file and do not format
the filesystem. Hardware tests initially verify API availability and avoid
driving unverified pins or attached peripherals.
