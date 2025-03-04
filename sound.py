import board
from audiomp3 import MP3Decoder

class Sound:
    def __init__(self, pin=board.GP0):
        self.pin = pin

    def play(self, path: str):
        if self.pin.playing:
            print("Audio is currently playing !")
        else:
            try:
                with open(path, "rb") as file:
                    print(f"Playing {path}...")
                    decoder = MP3Decoder(file)
                    self.pin.play(decoder)
            except OSError as e:
                print(f"An error occured while trying to open {path} : {e}")

