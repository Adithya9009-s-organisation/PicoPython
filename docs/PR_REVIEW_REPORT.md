# PicoPython RP2 Wrapper-Fix Candidate Report

## Candidate

The wrapper-fix candidate is built for MicroPython v1.29.0 on RP2350 and
retains:
asyncio/uasyncio, select, framebuf, USB CDC REPL, VFS/FAT/LittleFS, GC,
Pin, SPI, I2C, UART, errno, io, collections, re, and existing core modules.

The candidate removes cmath and the explicitly scoped machine/rp2 APIs:
ADC, PWM, I2S, RTC, WDT, Timer, PIO, StateMachine, DMA, and DMATimer.
The Pico SDK DMA component remains linked because the retained SPI
implementation depends on it.

It removes cmath and the scoped machine/RP2 APIs: ADC, PWM, I2S, RTC, WDT,
Timer, PIO, StateMachine, DMA, and DMATimer. The Pico SDK DMA component
remains linked because the retained SPI implementation depends on it.

## Build and artifact

- Pinned MicroPython source: `0fd6c573ea815774668bbb16b8e197c8822368b2`
- Toolchain: CMake 4.2.3, ARM GCC 14.2.1, `-j2`
- UF2: `releases/v1.29.0/PicoPython-v1.29-wrapper-fix.uf2`
- UF2 size: 626,688 bytes
- UF2 SHA-256: `2c610c7f061e0989dd80b849f4dfa5deb88392d1d78202897263468b171861a6`
- ELF: text 323,280 bytes, data 0 bytes, BSS 4,508 bytes
- Linker-reported flash use: 313,044 bytes; RAM use: 22,612 bytes
- `picotool` identifies RP2350 ARM Secure firmware with USB REPL enabled.

The earlier pre-wrapper-fix UF2 is preserved separately as
`releases/v1.29.0/PicoPython-v1.29-reviewed-pre-wrapper-fix.uf2` (626,688
bytes, SHA-256
`7c03974c6ac6066253f86756bf089ccfe0f1b454516dbcdc303c747eb68ec158`). It is
kept for comparison only; the user reported that it fails during `import rp2`.

## Patch review

The feature patch retains the earlier conditional CMake/source/QSTR/SDK and
machine/RP2 registration changes, and now also guards the PIO-dependent Python
wrapper:

- `PIOASMError` and `PIOASMEmit`
- `_pio_funcs`, `_pio_directives`, and `_pio_instructions`
- `asm_pio` and `asm_pio_encode`

These definitions exist only when `PIO` is exported by `_rp2`; no placeholder
PIO API or C registration is added. `rp2.py` remains in the frozen manifest.
The source patch applies and reverse-checks cleanly against the pinned source.

`tests/hardware/api_surface.py` now asserts that the removed PIO wrapper names
are absent while `machine.Pin`, `SPI`, `I2C`, and `UART` remain available.

## Validation status

- Build-verified: clean RP2350 build, UF2 hash, and ELF API-symbol audit.
- Source-audited: PIO wrapper helpers are guarded; retained C APIs remain
  registered and removed API types are absent.
- Runtime-tested on the MicroPython Unix VM: the actual `rp2.py` imports with
  PIO both absent and present, using a test `_rp2` shim.
- Acceptance scripts: all ten compile with `mpy-cross`; portable language,
  async, filesystem, REPL, and memory tests pass on the Unix VM.
- Hardware-tested (user-reported): Pico 2 boot/REPL, filesystem
  read/write/delete, asyncio, and the acceptance tests passed. These device
  results were reported by the user and were not independently captured here.
- No CPython standard-library implementation has been added.

Network and Bluetooth remain unconfigured. The former pre-wrapper-fix UF2 is
not the recommended image. Preserve the known-good firmware as the rollback
baseline; do not format the filesystem.

The candidate is prepared as a versioned artifact for this release branch.
Future CPython module additions remain a separate phase.
