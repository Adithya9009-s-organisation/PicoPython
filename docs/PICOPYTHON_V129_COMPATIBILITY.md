# PicoPython v1.29 Compatibility Specification

## Goal

Make PicoPython a practical, CPython-like Python runtime on Raspberry Pi Pico
2 / RP2350 while staying within the RP2350's flash and RAM limits. MicroPython
v1.29.0 remains the interpreter and compiler. This project curates its
standard-library surface; it does not aim to reproduce desktop CPython or
implement a new VM.

The current stock and custom v1.29.0 UF2s are the size/build baseline. The
user reports that the current custom UF2 works. Preserve it as a known-good
rollback image. Record new device measurements before and after each
compatibility change; do not infer runtime heap or stability from a successful
cross-build.

## Target architecture

- USB CDC normal MicroPython REPL; no display is required.
- MicroPython parser, compiler, VM, builtins, exceptions, and GC.
- A curated, individually tested standard library.
- Minimal board-facing hardware API: `machine.Pin`, `UART`, `SPI`, and `I2C`.
- VFS with FAT and LittleFS on the existing 3 MiB flash partition.

The separate display Pico, GUI, editor, keyboard, and inter-Pico protocol are
out of scope.

## Modules and features proposed for removal

These are target decisions, but each removal must first be checked against
v1.29.0 dependencies, port build sources, startup, and required filesystem and
REPL behavior. Do not remove implementation files or hide imports as a
substitute for a verified build-time configuration change.

### v1.29.0 RP2 baseline audit

The pinned RP2 port sets `MICROPY_CONFIG_ROM_LEVEL_EXTRA_FEATURES`. As a
result, the MicroPython core defaults enable `cmath`, `select`, `asyncio`,
`heapq`, and `framebuf`; `errno` is enabled too and `io` is required by the
core. The RP2 board manifest freezes the asyncio library. Pico 2 board files
do not enable Wi-Fi, and the base Pico 2 configuration does not add Bluetooth.

The requested hardware removals are not all simple board-level switches:

- The RP2 port explicitly enables `machine.ADC`, `machine.PWM`, `machine.I2S`,
  and `machine.WDT` in `mpconfigport.h`.
- RP2-specific `machine.RTC` and `machine.Timer` are included in the port's
  machine module; the generic `MICROPY_PY_MACHINE_TIMER` default does not
  control that RP2 implementation.
- `rp2.PIO`, `rp2.StateMachine`, `rp2.DMA`, and `rp2.DMATimer` are registered
  by the RP2 module and their implementation sources are always listed in the
  RP2 CMake source sets.

Therefore module/API removal requires a verified port-source patch and a full
firmware build, not only definitions added to the custom board header. Check
the port's startup paths and shared SDK dependencies before excluding source
files. Keep these details synchronized with `config/stdlib_manifest.py`.

The source dependency check also found that MicroPython's frozen asyncio core
imports `select` and its stream module imports `errno`. This supports removing
`asyncio` and `select` together, while retaining `errno` as specified. The
RP2 uses its own FAT/LittleFS VFS paths; the generic POSIX VFS select
integration is not evidence that the RP2 filesystem depends on `select`.

### Current custom-board candidate

The custom board retains `framebuf`, `asyncio`, `uasyncio`, and `select`
and includes the frozen asyncio manifest. Async/await parser and VM support
remain enabled. `errno`, `io`, and the default RP2 frozen modules remain
included.

The custom board also disables the specified machine APIs and `rp2.PIO` /
`DMA` surfaces. A version-pinned RP2 source patch gates API registration,
startup/deinit calls, source/QSTR lists, and optional ADC/PWM/PIO SDK
components. The Pico SDK DMA driver remains linked because retained
`machine.SPI` depends on it; removing `rp2.DMA` does not remove that internal
dependency. Timer and watchdog clock/SDK support required internally by the
port remains available. These are source-level candidate changes only:
the candidate has not yet been rebuilt or device-tested, and the working UF2
remains the rollback baseline.

### Initial v1.29.0 parser probe

The test cases were compiled independently by the v1.29.0 `mpy-cross` built
from the pinned source:

- Supported: f-strings, decorators, generator expressions, set/dict
  comprehensions, keyword-only arguments, function annotations, async/await,
  assignment expressions, exception-chaining syntax, extended unpacking,
  keyword unpacking, `nonlocal`, and annotated assignments.
- Not supported: positional-only arguments (`/`) and structural pattern
  matching (`match`/`case`); both probes produce `SyntaxError`.

The supported cases are in `tests/language/syntax_compat.py`. Syntax support
does not guarantee identical CPython runtime semantics; for example,
exception-cause introspection and annotation storage still need device tests.
`tests/modules/compatibility.py` and `tests/hardware/api_surface.py` encode the
target's removal decisions. They should be run against the newly built
candidate; the existing working UF2 predates these removals and is not expected
to pass them.

| Candidate | Target | Audit constraint |
| --- | --- | --- |
| `framebuf` | Remove | Display is on the other Pico; check module build guard. |
| `asyncio` / `uasyncio` | Remove the library/runtime module | Keep async/await parser and VM syntax; this is a separate decision. Check frozen modules and scheduler dependencies. |
| `cmath` | Remove | Complex arithmetic is optional; check its feature guard and shared numeric dependencies. |
| `select` | Remove if safe | Check stream, VFS, socket, and other users before disabling. |
| `errno` | Keep unless proven safe to remove | Error constants are used by I/O, VFS, and exception paths. |
| `io` | Keep | Needed for file/stream interfaces and related builtins. |
| `collections` | Keep | Common Python compatibility. |
| `re` | Keep | Common Python compatibility. |
| `network` | Keep disabled | Pico 2 has no planned network hardware; do not expose a false API. |
| `bluetooth` | Keep disabled | No planned Bluetooth hardware; do not expose a false API. |

### Hardware API reduction

| API | Target | Audit constraint |
| --- | --- | --- |
| `rp2.PIO`, `rp2.StateMachine` | Remove | Check their sources and PIO program registration dependencies. |
| `rp2.DMA`, `rp2.DMATimer` | Remove | Check DMA users in the port and required peripherals. |
| `machine.ADC`, `machine.PWM`, `machine.I2S` | Remove | Verify source guards, board initialization, and shared SDK dependencies. |
| `machine.RTC`, `machine.WDT`, `machine.Timer` | Remove | Verify timer/alarm/watchdog uses needed internally by the port. |
| `machine.Pin`, `machine.SPI`, `machine.I2C`, `machine.UART` | Keep | Required minimal hardware surface. |

Removing a Python API does not automatically mean removing the underlying SDK
driver: a driver can still be required by another retained component.

## Standard-library additions

`config/stdlib_manifest.py` is the authoritative inventory of proposed
additions, priority, APIs, source, and implementation status. Additions are
not enabled simply by appearing in that inventory. For each module:

1. Check the existing MicroPython built-in/frozen modules and
   `micropython-lib` before writing or freezing code.
2. Select only the requested API subset and document MicroPython-specific
   limitations.
3. Add focused behavioral tests for that module.
4. Include it in a separate candidate frozen manifest and measure flash,
   static RAM, and post-GC free heap before accepting it.

### Priority 1 — core compatibility

`functools` (`partial`, `wraps`, `reduce`, `lru_cache`), `itertools`
(`chain`, `cycle`, `repeat`, `product`, `islice`), `operator` (standard
operator functions), `copy` (`copy`, `deepcopy`), `enum` (`Enum`, `IntEnum`,
`Flag`), `dataclasses` (`dataclass`, `field`, `asdict`), `contextlib`
(`contextmanager`, `suppress`), `abc` (`ABC`, `abstractmethod`), `typing`
(common definitions), `traceback` (formatting), and `inspect` (function/object
introspection).

### Priority 2 — extended compatibility

`pathlib` (`Path` and path operations), `datetime` (`date`, `time`,
`datetime`, `timedelta`), `logging` (loggers, handlers, formatters), `pprint`
(`pprint`, `pformat`), `textwrap` (`wrap`, `fill`, `dedent`), `difflib`
(`SequenceMatcher`, unified diffs), `heapq` (heap operations), `bisect`
(binary search), `statistics` (basic functions), `csv` (readers/writers),
`configparser` (INI), and `unittest` (basic framework).

If a module such as `heapq` is already built in, extend/test that implementation
instead of adding a duplicate.

### Priority 3 — additional compatibility, subject to measurements

`decimal`, `fractions`, `uuid`, `calendar`, `base64`, `hmac`, `pickle`,
`weakref`, and `zlib`. Check whether `binascii` is already available; extend
`hashlib` only for justified missing algorithms. Do not duplicate or replace
existing `json`, `struct`, `array`, `math`, `random`, `re`, or `collections`;
test and extend them only where a specific compatibility gap is demonstrated.

## Python syntax and language behavior

Keep the existing parser/compiler features unless tests against v1.29.0 show a
gap. `async`/`await` syntax is independent of retaining the `asyncio` library.
Compile the audit cases with the v1.29.0 `mpy-cross`, then run supported
behavioral cases on the board:

| Feature | Required audit |
| --- | --- |
| F-strings | Keep and verify interpolation. |
| Decorators | Keep and verify application/order. |
| Generator expressions | Keep and verify iteration. |
| Set/dict comprehensions | Keep and verify results. |
| Keyword-only arguments | Keep and verify argument errors and binding. |
| Positional-only arguments (`/`) | Current v1.29.0 parser probe rejects this syntax; a compiler/runtime change is needed to meet the target. |
| Function annotations | Keep syntax; document annotation introspection differences. |
| Async / await | Keep syntax and VM support, even if the `asyncio` library is removed. |
| Assignment expressions (`:=`) | Parser probe passes; run runtime behavior test. |
| Structural pattern matching (`match` / `case`) | Current v1.29.0 parser rejects this syntax; leave as an explicit gap unless implemented and tested. |
| Exception chaining (`raise X from err`) | Parser probe passes; test exception-cause behavior separately. |
| Extended unpacking | Keep and verify assignment and call unpacking. |
| Keyword unpacking (`**kwargs`) | Keep and verify. |
| `nonlocal` | Keep and verify closure updates. |
| Type-annotated assignments | Parser probe passes; test runtime behavior and annotation storage. |

## Explicit exclusions

Do not add `tkinter`, `turtle`, `multiprocessing`, `subprocess`, `ctypes`,
`curses`, `sqlite3`, `venv`, `ensurepip`, `idlelib`, `mailbox`,
`socketserver`, or `http.server`.

## Acceptance and change discipline

The current working UF2 is the rollback baseline. For each subsequent change,
record the source/configuration delta, build both the relevant baseline and
candidate with the same toolchain, and compare UF2/flash size and static RAM.
The user reports the current UF2 works; preserve it as the rollback image.
For each new image, run focused module/syntax tests and the retained REPL,
filesystem, hardware, and heap checks. Preserve the 3 MiB filesystem and
never format it during tests.
