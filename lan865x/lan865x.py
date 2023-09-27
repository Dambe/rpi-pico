from machine import Pin, SPI

HIGH = 1
LOW = 0

LED = Pin("LED", Pin.OUT)


# MicroPython SPI documentation:
# https://docs.micropython.org/en/latest/library/machine.SPI.html
def spi_write(spi_inst: SPI, cs_pin: Pin, spi_write_buf: bytearray):
    LED.toggle()
    cs_pin.value(LOW)
    spi_inst.write(spi_write_buf)
    cs_pin.value(HIGH)
    LED.toggle()


def spi_read(spi_inst: SPI, cs_pin: Pin, r_len=0):
    if r_len == 0:
        return bytearray()

    LED.toggle()
    cs_pin.value(LOW)
    spi_read_data = spi_inst.read(r_len)
    cs_pin.value(HIGH)
    LED.toggle()

    return spi_read_data


def spi_read_write(spi_inst: SPI, cs_pin: Pin, spi_write_buf: bytearray):
    buf_len = len(spi_write_buf)

    if buf_len == 0:
        return bytearray()

    spi_read_buf = bytearray(buf_len)

    # fill spi_write_buf with dummy data
    # can be used to test MISO-MOSI-loopback
    for i in range(buf_len):
        spi_write_buf[i] = i

    LED.toggle()
    cs_pin.value(LOW)
    spi_inst.write_readinto(spi_write_buf, spi_read_buf)
    cs_pin.value(HIGH)
    LED.toggle()

    return spi_read_buf


if __name__ == "__main__":
    # assign Chip Select (CS) pin and set it high
    spi_cs = Pin(7, Pin.OUT, value=HIGH)
    # initialize SPI
    spi = SPI(
        0, baudrate=100000, polarity=0, phase=0, sck=Pin(2), mosi=Pin(3), miso=Pin(4)
    )

    test_buf = bytearray(8)
    data = spi_read(spi, spi_cs, 4)
    print(data)
    data = spi_read_write(spi, spi_cs, test_buf)
    print(data)
