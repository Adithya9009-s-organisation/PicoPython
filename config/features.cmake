# Conservative first build for MicroPython v1.29.0.
#
# Keep the RP2 port defaults for the VM, USB CDC, VFS, FAT, LittleFS,
# machine/rp2 peripherals, framebuf, and asyncio. The Pico 2 board does not
# enable the Wi-Fi or Bluetooth drivers; its current firmware also lacks
# importable network and bluetooth modules.
#
# WebREPL is part of the network feature group and is not needed for USB REPL.
# USB CDC is enabled by the RP2 port; USB MSC defaults off.
#
# The RP2 port unconditionally enables and links mbedTLS in this source
# revision. Leave it unchanged until a separately verified source-level
# change can demonstrate that removing it preserves the required features.
#
# For Windows builds, use -fno-use-linker-plugin: the host policy blocks the
# provided compiler's optional LTO plugin, and this source has no LTO flags.
# The qstr preprocessing rule uses a local Python equivalent of its POSIX
# cat/sed pipeline so the pinned source can build under the Windows command
# processor without changing generated firmware features.
#
# Current blocker: Windows App Control also blocks executing the newly built
# mpy-cross.exe (WinError 4551). Do not bypass that policy; a policy-approved,
# v1.29-compatible mpy-cross executable is needed to freeze Python modules.
