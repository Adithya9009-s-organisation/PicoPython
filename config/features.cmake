# Compatibility target for MicroPython v1.29.0.
#
# The current working UF2 is the rollback baseline. The custom board retains
# framebuf, asyncio/uasyncio, and select as useful general-purpose features.
# cmath and the specified hardware APIs are removed. Async/await parser/VM
# support remains available. The candidate builds successfully; device
# validation is still pending.
#
# Preserve the VM, USB CDC, VFS, FAT, LittleFS, errno, io, collections, re,
# and machine.Pin/SPI/I2C/UART. The Pico 2 board does not enable Wi-Fi or
# Bluetooth; those modules remain unavailable by design.
#
# WebREPL is part of the network feature group and is not needed for USB REPL.
# USB CDC is enabled by the RP2 port; USB MSC defaults off.
#
# The RP2 port unconditionally enables and links mbedTLS in this source
# revision. Leave it unchanged until a separately verified source-level
# change can demonstrate that removing it preserves the required features.
#
# MicroPython v1.29.0's generated extensible-module table includes the
# string module even when MICROPY_PY_TSTRINGS is disabled. Apply the
# version-specific patch in patches/ to omit that unavailable module without
# enabling template strings.
#
# For Windows builds, use -fno-use-linker-plugin: the host policy blocks the
# provided compiler's optional LTO plugin, and this source has no LTO flags.
# The qstr preprocessing rule uses a local Python equivalent of its POSIX
# cat/sed pipeline so the pinned source can build under the Windows command
# processor without changing generated firmware features.
#
# The user reports that the current custom UF2 works on-device. Preserve it as
# the known-good rollback image while evaluating compatibility changes.
