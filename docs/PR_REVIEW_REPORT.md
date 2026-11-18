# PR #3 Review Report

## Reviewed candidate

The compatibility candidate is build-verified but not device-validated.
It retains the general-purpose features most relevant to PicoPython:
asyncio/uasyncio, select, framebuf, USB CDC REPL, VFS/FAT/LittleFS, GC,
Pin, SPI, I2C, UART, errno, io, collections, re, and existing core modules.

The candidate removes cmath and the explicitly scoped machine/rp2 APIs:
ADC, PWM, I2S, RTC, WDT, Timer, PIO, StateMachine, DMA, and DMATimer.
The Pico SDK DMA component remains linked because the retained SPI
implementation depends on it.

## Build evidence

- Pinned source: MicroPython `0fd6c573ea815774668bbb16b8e197c8822368b2`
- Toolchain: CMake 4.2.3, ARM GCC 14.2.1, parallelism `-j2`
- Reviewed candidate UF2: 626,688 bytes
- Reviewed candidate SHA256:
  `7c03974c6ac6066253f86756bf089ccfe0f1b454516dbcdc303c747eb68ec158`
- Stock comparison UF2: 661,504 bytes
- Clean-build stock SHA256:
  `fe5902a62eb79f76ff9d7d526b4de5b1f3873ab35f1a5fb2fcf065c9218c691b`
- Reviewed candidate reduction: 34,816 bytes / 5.26%

Asyncio-only review: 615,936 bytes. Framebuf-only incremental cost: 10,752 bytes.
The earlier asyncio/framebuf-stripped image measured 594,944 bytes but is not
the reviewed candidate.

## Patch review

The 293-line RP2 patch is limited to:

1. Conditional RP2 CMake source, QSTR, and SDK component lists.
2. Conditional PIO/DMA startup and soft-reset calls.
3. Conditional machine RTC/Timer module registration.
4. Conditional RP2 PIO/DMA module registration and declarations.
5. Conditional ADC/PWM/I2S/WDT/Timer/RTC macros.

The patch applies and reverses cleanly on the exact pinned source.
Trailing whitespace and patch line endings have been normalized.

## Risks and pending validation

- No candidate has been flashed.
- USB REPL behavior and startup stability are unverified on hardware.
- SPI/I2C/UART runtime behavior is unverified.
- Pin behavior is unverified.
- FAT/LittleFS persistence is unverified across soft reset and power cycle.
- GC heap measurements are unverified.
- Network and Bluetooth remain unconfigured, but this has not been
  device-audited.
- No CPython standard-library implementation has been added.

## Decision

Do not merge or flash. Retain this configuration for hardware-acceptance
review. Any further change should remain separate from the display Pico,
CPython module work, or filesystem-formatting tests.
