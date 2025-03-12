from machine import Pin, I2C, UART, SPI
from time import sleep
import network
import socket
import urequests
import os
import sdcard

class DFPlayer:
    def __init__(self, pin_rx=1, pin_tx=0):
        self.uart = UART(0, 9600, rx=Pin(pin_rx), tx=Pin(pin_tx))

    def command(self, cmd, param=0x00):
        bytes_to_send = bytes([0x7e, 0xff, 0x06, cmd, 0x00, 0x00, param, 0xef])
        self.uart.write(bytes_to_send)

    def resume(self):
        self.command(0x0d)

NETWORK_SSID = ""
NETWORK_PASSWORD = ""
SERVER_IP = ""

def storage():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(NETWORK_SSID, NETWORK_PASSWORD)

    while not wlan.isconnected():
        pass
    print("Connected! IP:", wlan.ifconfig()[0])

    spi = SPI(0, baudrate=1000000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(19), miso=Pin(16))
    cs = Pin(17)
    sd = sdcard.SDCard(spi, cs)
    os.mount(sd, "/sd")

    for file in os.listdir("/sd"):
        try:
            print(file)
            os.remove(f"/sd/{file}")
            print(f"Removed /sd/{file}")
        except OSError as e:
            print(e)

    def stream_mp3(url, file_path):
        print(f"Downloading {url} to {file_path}...")

        response = urequests.get(url, stream=True)
        if response.status_code == 200:
            with open(file_path, "wb") as file:
                while True:
                    chunk = response.raw.read(1024)
                    if not chunk:
                        break
                    file.write(chunk)
                    print(f"Saved {len(chunk)} bytes...")
            print("Download complete.")
        else:
            print("Failed to fetch MP3")

    mp3_url = f"http://{SERVER_IP}:8000/api/audio/5/"
    stream_mp3(mp3_url, "/sd/music.mp3")

def play():
    df = DFPlayer()
    df.resume()
    print("Playing music...")
def waves():
    i2c = I2C(0, scl = Pin(5), sda = Pin(4), freq = 400000)
    frequency = 89.0
    def setFrequency(freq):
        if((freq < 87) or (freq > 108)):
            return False
        return setChannel(round(freq * 20))

    def setChannel(channel):
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
    
        i2c.writeto_mem(0x3E, 0x00, buf1)
        i2c.writeto_mem(0x3E, 0x01, buf2)
        i2c.writeto_mem(0x3E, 0x02, buf3)
        i2c.writeto_mem(0x3E, 0x04, buf4)
        return True

    setFrequency(frequency)
    while True:
        sleep(1)

def main():
    storage()
    input("Now place the SD card into the DFPlayer and press [ENTER]")
    play()
    waves()
