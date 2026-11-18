"""Compatibility inventory for PicoPython on MicroPython v1.29.0.

This is a planning/test manifest, not a MicroPython freeze manifest. It does
not include modules in firmware by itself. Each entry must be audited,
implemented/reused, tested, and measured before being frozen.
"""

BASELINE = {
    "source": "MicroPython v1.29.0 RP2 port",
    "rom_level": "MICROPY_CONFIG_ROM_LEVEL_EXTRA_FEATURES",
    "modules_to_keep": (
        "io",
        "collections",
        "re",
        "errno",
        "json",
        "struct",
        "array",
        "math",
        "random",
        "binascii",
        "hashlib",
    ),
    "modules_disabled_by_target": ("network", "bluetooth"),
    "hardware_to_keep": ("machine.Pin", "machine.SPI", "machine.I2C", "machine.UART"),
    "filesystem_to_keep": ("VFS", "FAT", "LittleFS"),
}

CURRENT_MODULES = {
    "enabled_by_rp2_defaults": (
        "cmath",
        "select",
        "asyncio",
        "heapq",
        "framebuf",
        "errno",
        "io",
    ),
    "provided_by_rp2_frozen_manifest": ("asyncio", "uasyncio"),
    "disabled_or_unconfigured_on_pico2": ("network", "bluetooth"),
    "implementation_exists_but_disabled_by_default": ("weakref",),
}

MODULE_DEPENDENCIES = {
    "asyncio": ("imports select in extmod/asyncio/core.py",),
    "errno": (
        "imported by extmod/asyncio/stream.py",
        "retain error constants and errno mapping for I/O/VFS compatibility",
    ),
    "select": (
        "used by frozen asyncio; remove both together",
        "generic POSIX VFS integration is not used as RP2 VFS evidence",
    ),
    "io": ("used by builtins and sys standard streams",),
}

REMOVALS = {
    "modules": {
        "framebuf": "disabled in custom board; build/device validation pending",
        "asyncio": "disabled and omitted from custom frozen manifest; keep async/await syntax",
        "uasyncio": "omitted with asyncio from the custom frozen manifest",
        "cmath": "disabled in custom board; ordinary math support remains",
        "select": "disabled with asyncio; no RP2 VFS dependency was found",
        "errno": "review only; preserve until error-path dependencies are verified",
    },
    "machine_apis": {
        "machine.ADC": "disabled in custom board; ADC SDK component omitted",
        "machine.PWM": "disabled in custom board; PWM SDK component omitted",
        "machine.I2S": "disabled; no I2S startup/deinit is performed",
        "machine.RTC": "registration and RP2 implementation omitted; port time init remains",
        "machine.WDT": "Python API disabled; watchdog SDK remains for reset support",
        "machine.Timer": "registration and RP2 implementation omitted; port soft timers remain",
        "rp2.PIO": "registration, startup, source, and PIO SDK component omitted",
        "rp2.StateMachine": "omitted with rp2.PIO",
        "rp2.DMA": "API and source omitted; SDK DMA remains for retained machine.SPI",
        "rp2.DMATimer": "omitted with rp2.DMA",
    },
}

CANDIDATE_REMOVALS = {
    "modules_configured_off": (
        "framebuf",
        "asyncio",
        "uasyncio",
        "cmath",
        "select",
    ),
    "machine_apis_configured_off": (
        "machine.ADC",
        "machine.PWM",
        "machine.I2S",
        "machine.RTC",
        "machine.WDT",
        "machine.Timer",
        "rp2.PIO",
        "rp2.StateMachine",
        "rp2.DMA",
        "rp2.DMATimer",
    ),
    "validation_status": "candidate firmware builds; device tests pending",
    "retained": ("errno", "io", "async/await syntax", "Pin", "SPI", "I2C", "UART"),
}

ADDITIONS = {
    1: {
        "functools": ("partial", "wraps", "reduce", "lru_cache"),
        "itertools": ("chain", "cycle", "repeat", "product", "islice"),
        "operator": ("standard operator functions",),
        "copy": ("copy", "deepcopy"),
        "enum": ("Enum", "IntEnum", "Flag"),
        "dataclasses": ("dataclass", "field", "asdict"),
        "contextlib": ("contextmanager", "suppress"),
        "abc": ("ABC", "abstractmethod"),
        "typing": ("common typing definitions",),
        "traceback": ("traceback formatting",),
        "inspect": ("function and object introspection",),
    },
    2: {
        "pathlib": ("Path", "path operations"),
        "datetime": ("date", "time", "datetime", "timedelta"),
        "logging": ("loggers", "handlers", "formatters"),
        "pprint": ("pprint", "pformat"),
        "textwrap": ("wrap", "fill", "dedent"),
        "difflib": ("SequenceMatcher", "unified diffs"),
        "heapq": ("heap operations",),
        "bisect": ("binary search",),
        "statistics": ("basic statistical functions",),
        "csv": ("readers", "writers"),
        "configparser": ("INI configuration",),
        "unittest": ("basic test framework",),
    },
    3: {
        "decimal": ("decimal arithmetic",),
        "fractions": ("rational arithmetic",),
        "uuid": ("UUID creation and parsing",),
        "calendar": ("calendar helpers",),
        "base64": ("base64 encode/decode",),
        "hmac": ("HMAC",),
        "pickle": ("compatible serialization subset",),
        "weakref": ("weak references",),
        "zlib": ("compression APIs",),
    },
}

EXISTING_MODULE_AUDIT = {
    "binascii": "verify import and API surface before extending",
    "hashlib": "verify current algorithms; add only justified gaps",
    "json": "extend only for demonstrated compatibility gaps",
    "struct": "extend only for demonstrated compatibility gaps",
    "array": "extend only for demonstrated compatibility gaps",
    "math": "extend only for demonstrated compatibility gaps",
    "random": "extend only for demonstrated compatibility gaps",
    "re": "extend only for demonstrated compatibility gaps",
    "collections": "extend only for demonstrated compatibility gaps",
    "heapq": "check whether the port already provides it; do not duplicate",
}

LANGUAGE_AUDIT = {
    "supported_by_v1_29_mpy_cross_probe": (
        "f-strings",
        "decorators",
        "generator expressions",
        "set comprehensions",
        "dict comprehensions",
        "keyword-only arguments",
        "function annotations",
        "async/await syntax",
        "assignment expressions",
        "exception chaining syntax",
        "extended unpacking",
        "keyword unpacking",
        "nonlocal",
        "annotated assignments",
    ),
    "not_supported_by_v1_29_mpy_cross_probe": (
        "positional-only arguments",
        "structural pattern matching",
    ),
}

EXCLUDED = (
    "tkinter",
    "turtle",
    "multiprocessing",
    "subprocess",
    "ctypes",
    "curses",
    "sqlite3",
    "venv",
    "ensurepip",
    "idlelib",
    "mailbox",
    "socketserver",
    "http.server",
)
