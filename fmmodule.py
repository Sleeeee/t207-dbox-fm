from machine import Pin, I2C

class FmModule:
    def __init__(self, frequency=90.0, pin_scl=Pin(5), pin_sda=Pin(4)):
        self.frequency = frequency
        self.i2c = I2C(0, scl=pin_scl, sda=pin_sda, freq=400000)
        self.set_frequency(self.frequency)

    def set_frequency(self, freq):
        if((freq < 87) or (freq > 108)):
            return False
        return self.set_channel(round(freq * 20))

    def set_channel(self, channel):
        if((channel < 1740) or (channel > 2160)):
            return False
        buf1 = bytearray(1)
        buf1[0] = ((int(channel) & 0x1FE) >> 1)
        buf2 = bytearray(1)
        buf2[0] = ((int(channel) >> 9) | 0x68)
        buf3 = bytearray(1)
        buf3[0] = (((int(channel) & 0x001) << 7) | 0x01)
        buf4 = bytearray(1)
        buf4[0] = 0x34
        self.i2c.writeto_mem(0x3E, 0x00, buf1)
        self.i2c.writeto_mem(0x3E, 0x01, buf2)
        self.i2c.writeto_mem(0x3E, 0x02, buf3)
        self.i2c.writeto_mem(0x3E, 0x04, buf4)
        return True
