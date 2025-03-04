import wifi
from socketpool import SocketPool
import adafruit_requests as requests

class Interface:
    def __init__(self, ssid: str, password: str):
        self.ssid = ssid
        self.password = password
        self.pool, self.session = None, None

    def connect(self):
        print("Connecting WLAN interface...")
        wifi.radio.connect(ssid, password)
        print("Connected with IP address", wifi.radio.ipv4_address)

        self.pool = SocketPool(wifi.radio)
        self.session = requests.Session(self.pool)

    def get(self, url: str):
        if not self.session:
            raise RuntimeError("The WiFi interface is not connected !")
        return self.session.get(url)

    def get_audio(self, ip: str, n: int):
        return self.get(f"http://{ip}:8000/api/audio/{n}/")

