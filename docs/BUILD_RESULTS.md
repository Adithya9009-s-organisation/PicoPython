# PicoPython firmware build results

## Environment

- Source: MicroPython v1.29.0, commit `0fd6c573ea815774668bbb16b8e197c8822368b2`
- Host: GitHub Codespace, Ubuntu 26.04, x86_64
- CMake: 4.2.3
- ARM GNU toolchain: GCC 14.2.1
- Build parallelism: `-j2`
- Pico SDK: MicroPython submodule revision `98a542c1a62fb549ffb5d66a3e5892b06276b670`
- Compatibility patch: `patches/micropython-v1.29.0-string-moduledefs.patch`

The source compiler `mpy-cross` was built and run natively in Linux. The
stock and custom builds then completed without changing the MicroPython
submodule's pinned commit. The user reports the current custom UF2 works
on-device; exact device-side test results and runtime measurements have not
yet been recorded here.

## Artifacts

| Measurement | Stock `RPI_PICO2` | Custom `PICO_PYTHON` |
| --- | ---: | ---: |
| UF2 size | 666,624 bytes | 661,504 bytes |
| UF2 SHA-256 | `05ff1e18d1d179288abe45dad8f0c68f2ea1d535f55377c74ffb5427f5188e88` | `64da649663b4bd9a485fce24766d0479dc24684e2f16e4b23138b143e7f19fd8` |
| ELF text | 343,128 bytes | 340,664 bytes |
| ELF data | 0 bytes | 0 bytes |
| ELF bss | 4,696 bytes | 4,696 bytes |
| Linker-reported flash use | 332,892 bytes | 330,428 bytes |
| Linker-reported RAM use | 23,232 bytes | 23,232 bytes |

The custom UF2 is 5,120 bytes smaller than stock. Both builds reserve the
same 3 MiB flash filesystem partition and target `pico2` / `rp2350-arm-s`.
Both ELF files are ELF32 ARM images.

Artifacts and complete logs are in the Codespace worktree, outside the Git
repository's tracked files:

- `/workspaces/picopython-pr/builds/stock/firmware.uf2`
- `/workspaces/picopython-pr/builds/stripped/firmware.uf2`
- `/workspaces/picopython-pr/builds/stock-build.log`
- `/workspaces/picopython-pr/builds/stripped-build.log`

`picotool info` recognized both UF2s as RP2350 ARM Secure images and reported
USB REPL, the expected MicroPython frozen modules, a `pico2` board, and the
same `0x10100000-0x10400000` 3 MiB embedded drive. Their build metadata says
`v1.29.0-dirty`, as expected when the local module-table compatibility patch
is applied.

## Interpretation and remaining validation

The initial small size difference is from the custom board configuration and
build metadata; it is not evidence that the C implementation of TLS, USB
classes, or other libraries was stripped. The v1.29.0 RP2 port still links
mbedTLS.

The successful cross-build process did not flash the firmware. The user
reports that the current custom UF2 works, but this Codespace cannot
independently access the local COM8 device or verify the full acceptance
suite: language behavior, filesystem persistence, hardware APIs, and GC heap
measurements remain to be recorded. Do not overwrite or format the device's
filesystem during tests.

## v1.29 feature-removal candidate

The source-level removal candidate was built in an isolated worktree from the
same pinned source and Codespace toolchain as a stock `RPI_PICO2` comparison.
Both builds used `-j2`, CMake 4.2.3, and ARM GCC 14.2.1. The source patch
removes the selected Python modules and hardware APIs; the Pico SDK DMA driver
remains linked because the retained RP2 SPI implementation includes and uses
it.

| Measurement | Stock `RPI_PICO2` | Candidate `PICO_PYTHON` |
| --- | ---: | ---: |
| UF2 size | 661,504 bytes | 594,944 bytes |
| UF2 SHA-256 | `e5d5a99efeb8d594683c371afb842ddc8e3a7c7e44713890f47e3664b40001d9` | `4b09496ccd477c8b9c63c18fadba79e9985c42cb5d9886203b432a9c9f2b6aaa` |
| ELF text | 340,648 bytes | 307,372 bytes |
| ELF data | 0 bytes | 0 bytes |
| ELF bss | 4,696 bytes | 4,504 bytes |
| Linker-reported flash use | 330,412 bytes | 297,136 bytes |
| Linker-reported RAM use | 23,232 bytes | 22,608 bytes |

The candidate UF2 is 66,560 bytes smaller (10.06%) than this stock build.
`picotool` identifies both images as RP2350 ARM Secure firmware for `pico2`,
with USB REPL enabled and the same 3 MiB writable embedded drive. The stock
image lists `asyncio` and `uasyncio`; neither appears in the candidate's frozen
modules. The candidate also has no linked RP2 PIO/DMA API types or machine
ADC/PWM/RTC/Timer/WDT types. `mpy-cross` compiled the syntax, async/await,
module, and hardware acceptance scripts successfully.

These are build-time results only. No candidate firmware has been flashed;
device-side REPL, filesystem persistence, hardware behavior, and GC heap tests
remain pending. The existing user-confirmed working UF2 remains the rollback
baseline. Build artifacts are retained under the ignored Codespace
`builds/removal-test/` directory.
