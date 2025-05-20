import network
import settings
import urequests
import json
from time import sleep

class Interface:
    def __init__(self):
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        self.wlan.connect(settings.NETWORK_SSID, settings.NETWORK_PASSWORD)
        print(f"Trying to connect to {settings.NETWORK_SSID}.", end='')
        while not self.wlan.isconnected():
            print(".", end='')
            sleep(1)
        print(" Connected! IP:", self.wlan.ifconfig()[0])

    def download_mp3(self, url, file_path):
        response = urequests.get(url, stream=True)
        if response.status_code == 200:
            print(f"Downloading {url} to {file_path}:")
            with open(file_path, "wb") as file:
                total_size = 0
                while True:
                    chunk = response.raw.read(1024)
                    total_size += len(chunk)
                    if not chunk:
                        break
                    file.write(chunk)
                    print(f"{total_size} bytes downloaded", end="\r")
            print(f"{url} successfully downloaded")
        else:
            print(f"Failed to fetch {url}")

    def download_schedule(self, download_songs, date=""):
        response = urequests.get(f"http://www.dbox-fm.be/api/schedule/{date}")
        response_text = json.loads(response.text)
        if response.status_code == 200:
                for i in range(len(response_text)):
                    response_text[i]["song_id"] = i + 1
                    if download_songs:
                        publication_id = response_text[i]["publication"]
                        self.download_mp3(f"http://www.dbox-fm.be/api/audio/{publication_id}/", f"/sd/{(i+1):03}.mp3")
        else:
            print("Failed to fetch schedule")
        return response_text
