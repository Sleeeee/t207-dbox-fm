from machine import Timer
import settings
from dfplayer import DFPlayer
from interface import Interface
from sdmodule import SDModule
from schedule import Schedule
from fmmodule import FmModule

def main():
    inter = Interface()
    success = False
    while not success:
        try:
            swap = input("Do you want to download the schedule ? If so, please enter the SD card inside the storage module [y/N]")
            if swap == "y":
                sd = SDModule()
                sd.wipe_drive()
            schedule = Schedule(inter.download_schedule(swap == "y"))
            success = True
        except Exception as e:
            retry = input(f"An error occured : {e}\nDo you want to retry ? [Y/n]")
            if retry == "n":
                return

    play = input("Do you want to start playing now ? If so, please place the SD card inside the DFPlayer Mini [Y/n]")
    if play == "n":
        return
    df = DFPlayer()
    timer = Timer()
    timer.init(mode=Timer.PERIODIC, period=10000, callback=schedule.poll_time)
    schedule.poll_time(timer)

    #df.resume()
    #fm = FmModule()
    while True:
        pass

main()
