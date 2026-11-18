import machine
import rp2

for name in ("Pin", "SPI", "I2C", "UART"):
    assert hasattr(machine, name), "machine.%s is missing" % name

for name in ("ADC", "PWM", "I2S", "RTC", "WDT", "Timer"):
    assert not hasattr(machine, name), "machine.%s should be removed" % name

for name in ("PIO", "StateMachine", "DMA", "DMATimer"):
    assert not hasattr(rp2, name), "rp2.%s should be removed" % name

print("PicoPython hardware API surface tests: PASS")
