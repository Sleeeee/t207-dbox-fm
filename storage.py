import board
from busio import SPI
from sdcardio import SDCard
import storage

class SD:
    def __init__(self, pins_spi=(board.GP18, board.GP19, board.GP16), pin_cs=board.GP17):
        self.pins_spi = SPI(*pins_spi)
        self.pin_cs = pin_cs
        try:
            self.sd = SDCard(self.pins_spi, self.pin_cs)
            vfs = storage.VfsFat(self.sd)
            storage.mount(vfs, "/sd")
            print("SD card mounted successfully !")
        except OSError:
            self.sd = None
            print("Failed to mound SD card")

    def write(self, filename: str, data: bytes):
        if not self.sd:
            print("There is no mounted SD card as of now")
        else:
            try:
                with open(f"/sd/{filename}", "wb") as file:
                    file.write(data)
                print(f"File {filename} successfully written to the SD card")
            except OSError:
                print(f"Failed to write file {filename} to the SD card")

