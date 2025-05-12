from machine import Pin, SPI
from sdcard import SDCard
import urequests
import os

class SDModule:
    def __init__(self, pin_sck=Pin(18), pin_mosi=Pin(19), pin_miso=Pin(16), pin_cs=Pin(17)):
        self.spi = SPI(0, baudrate=1000000, polarity=0, phase=0, sck=pin_sck, mosi=pin_mosi, miso=pin_miso)
        self.sd = SDCard(self.spi, pin_cs)
        os.mount(self.sd, "/sd")
        print("SD card mounted successfully")

    def wipe_drive(self):
        for file in os.listdir("/sd"):
            try:
                os.remove(f"/sd/{file}")
                print(f"Removed /sd/{file}")
            except OSError as e:
                print(e)
