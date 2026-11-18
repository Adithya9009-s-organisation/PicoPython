import collections
import errno
import io
import json
import re
import struct

for name in ("framebuf", "asyncio", "uasyncio", "select"):
    __import__(name)

for name in ("cmath",):
    try:
        __import__(name)
    except ImportError:
        pass
    else:
        raise AssertionError("%s should be unavailable" % name)

for name in ("network", "bluetooth"):
    try:
        __import__(name)
    except ImportError:
        pass
    else:
        raise AssertionError("%s should be disabled on Pico 2" % name)

print("PicoPython module compatibility tests: PASS")
