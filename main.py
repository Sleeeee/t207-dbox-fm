from storage import Storage
from interface import Interface
from sound import Sound

NETWORK_SSID = ""
NETWORK_PASSWORD = ""
SERVER_IP = ""

strg = Storage()
inter = Interface(NETWORK_SSID, NETWORK_PASSWORD)
inter.connect()
snd = Sound()

audio = inter.get_audio(SERVER_IP, 1)
strg.write("audio.mp3", audio)

snd.play("/sd/audio.mp3")
