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

REMOVALS = {
    "modules": {
        "framebuf": "remove",
        "asyncio": "remove library; retain async/await language syntax",
        "uasyncio": "remove frozen library with asyncio",
        "cmath": "remove after checking shared numeric dependencies",
        "select": "remove only if VFS, stream, socket, and port dependencies permit",
        "errno": "review only; preserve until error-path dependencies are verified",
    },
    "machine_apis": {
        "machine.ADC": "explicitly enabled in RP2 port config; audit init/users",
        "machine.PWM": "explicitly enabled in RP2 port config; audit init/users",
        "machine.I2S": "enabled by RP2 defaults; audit init/users",
        "machine.RTC": "RP2-specific implementation; audit clock/time init",
        "machine.WDT": "explicitly enabled; audit startup/reset behavior",
        "machine.Timer": "RP2-specific implementation; audit internal alarms",
        "rp2.PIO": "registered unconditionally; audit source and peripheral users",
        "rp2.StateMachine": "registered unconditionally with PIO",
        "rp2.DMA": "registered unconditionally; audit shared DMA users",
        "rp2.DMATimer": "registered unconditionally with DMA",
    },
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
