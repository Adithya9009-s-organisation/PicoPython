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
stock and custom builds then completed without modifying the MicroPython
submodule's pinned commit.

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

The small size difference is from the custom board configuration and build
metadata; this is not evidence that the C implementation of TLS, USB classes,
or other libraries was stripped. The v1.29.0 RP2 port still links mbedTLS.
Keep the first firmware conservative until individual feature removals are
proven against the required APIs.

No firmware was flashed. USB CDC REPL operation, language tests on-device,
filesystem persistence, hardware APIs, and GC heap measurements remain
unverified. The Codespace has no access to the user's local COM8 device.
Flashing and device validation remain deferred pending separate
authorization.
