import framebuf
import machine
import rp2

for name in ("Pin", "ADC", "PWM", "SPI", "I2C", "UART", "Timer"):
    assert hasattr(machine, name), "machine.%s is missing" % name

for name in ("PIO", "DMA"):
    assert hasattr(rp2, name), "rp2.%s is missing" % name

assert hasattr(framebuf, "FrameBuffer")
print("PicoPython hardware API surface tests: PASS")
