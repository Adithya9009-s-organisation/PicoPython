# PicoPython development handoff

## Purpose

Continue the PicoPython stripped-firmware development in the GitHub Codespace associated with this repository.

Target Codespace: `humble-train-9qjw4q6g6pwcpx4q`  
Repository: `adithya9009/picopython`  
Target board: Raspberry Pi Pico 2 (RP2350)  
MicroPython baseline: v1.29.0  
Port: `rp2`

## Current project decisions

- Preserve the real MicroPython VM, parser/compiler, GC, exceptions, import system and USB CDC REPL.
- Keep FAT and LittleFS support initially.
- Preserve `machine`, `rp2`, GPIO, ADC, PWM, SPI, I2C, UART, timers, PIO and DMA.
- Keep the display out of the main PicoPython firmware. A second Pico running ordinary MicroPython will drive the 2.4-inch SPI ILI9341 display.
- The main Pico remains independently usable through its USB serial REPL.
- Do not flash hardware until a build is verified and the user explicitly authorizes flashing.

## Previous Windows build blocker

The isolated Windows workspace was `C:\Users\adith\PicoPython`. Its stock build reached MicroPython's frozen-module step but Windows App Control blocked `mpy-cross.exe` with WinError 4551. The same policy blocked the executable in the old checkout.

Do not bypass or weaken Windows App Control. No UF2 was produced and nothing was flashed.

The provided ARM GCC toolchain could compile without its blocked optional LTO plugin. A local Windows qstr-preprocessing issue was fixed. A redundant D: download was removed to restore disk space.

## Codespace migration approach

The Windows process itself, local uncommitted files, installed tools and terminal state do not automatically move into a Codespace. Treat this document as the project handoff and inspect the Codespace checkout before making changes.

In the Codespace:

1. Confirm the repository, branch, working tree and current files before modifying anything.
2. Preserve any existing Codespace changes; do not reset, clean or overwrite them.
3. Check available disk space, RAM, Python, CMake, Make/Ninja, compiler and Git versions.
4. Use a clean MicroPython v1.29.0 source checkout (or verify an existing one is exactly that revision).
5. Initialize only the submodules required by the RP2 port after auditing the v1.29.0 build requirements.
6. Build the unmodified `RPI_PICO2` stock baseline first.
7. On Linux, build the matching `mpy-cross` from the same MicroPython source revision if needed; do not substitute an incompatible version.
8. Audit exact v1.29.0 feature options and dependencies before changing any build configuration.
9. Create a separate `PICO_PYTHON` board configuration. Do not modify upstream `RPI_PICO2`.
10. Build the conservative custom firmware and compare it with the stock baseline.

## Candidate workspace layout

```text
picopython/
├── docs/
│   └── DEVELOPMENT_HANDOFF.md
├── micropython/                 # pinned upstream source, preferably a submodule
├── board/
│   └── PICO_PYTHON/
├── config/
├── tests/
│   ├── repl/
│   ├── language/
│   ├── filesystem/
│   ├── hardware/
│   └── memory/
└── builds/
    ├── stock/
    └── stripped/
```

Do not assume this layout already exists. Inspect the repository and Codespace first. Decide whether upstream MicroPython should be a Git submodule or a separately cloned checkout before adding it.

## Required audit before implementation

Record verified facts, unknowns and exact source paths for:

- RP2 board configuration and CMake options in MicroPython v1.29.0
- frozen-module manifest and `mpy-cross` build requirements
- network, Bluetooth, TLS and USB feature gates and linked dependencies
- FAT and LittleFS configuration
- flash layout and filesystem compatibility
- RP2350 hardware APIs and their build dependencies
- minimum required RP2 submodules

Do not infer that a feature is absent merely because its Python import fails.

## Validation

### Stock and custom firmware

- USB CDC REPL starts and accepts commands.
- Core syntax, functions, classes, generators, comprehensions and exceptions work.
- Ctrl+C and soft reset work.
- Required modules import.
- Filesystem mounts and supports create/read/write/delete.
- FAT and LittleFS support remain compiled in.
- GPIO, ADC, PWM, SPI, I2C, UART, timers, PIO and DMA APIs remain available.
- Files persist across soft reset and power cycling (power-cycle test requires physical hardware).

Record UF2 size, flash usage, GC heap total/free/allocated, and test outcomes for both builds.

### Hardware safety

- Do not format or remount the Pico filesystem.
- Do not perform destructive GPIO or peripheral tests.
- Do not flash the Pico without explicit user approval.
- Keep USB serial REPL as the first hardware validation path.

## Display architecture (later phase)

The second Pico runs pure MicroPython and owns the ILI9341 SPI display and graphics. The main PicoPython board sends terminal/UI data over a dedicated inter-Pico connection (UART is the current preferred candidate, not yet finalized). Display rendering and input forwarding are later milestones, not part of the stripped firmware baseline.

## Immediate next action

Inspect the existing Codespace and repository state, then produce a read-only environment/source audit. Do not start a build or change files until that audit is complete.
