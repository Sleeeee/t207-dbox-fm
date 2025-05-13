from machine import Timer
import settings
from dfplayer import DFPlayer
from interface import Interface
from sdmodule import SDModule
from schedule import Schedule
from display import Display
from fmmodule import FmModule

def main():
    disp = None
    schedule = None
    try:
        disp = Display()
        schedule = Schedule(None, disp)
        inter = Interface()
        success = False
        while not success:
            try:
                swap = input("Do you want to download the scheduled songs ? If so, please enter the SD card inside the storage module [y/N]")
                if swap == "y":
                    sd = SDModule()
                    sd.wipe_drive()
                schedule.schedule = inter.download_schedule(swap == "y")
                success = True
            except Exception as e:
                retry = input(f"An error occured : {e}\nDo you want to retry ? [Y/n]")
                if retry == "n":
                    raise KeyboardInterrupt

        play = input("Do you want to start playing now ? If so, please place the SD card inside the DFPlayer Mini [Y/n]")
        if play == "n":
            raise KeyboardInterrupt
        df = DFPlayer()

        #df.resume()
        #fm = FmModule()
        while True:
            pass
    except KeyboardInterrupt:
        print("KeyboardInterrupt detected, collecting garbage...", end=' ')
        if disp is not None:
            disp.deinit()
        if schedule is not None:
            schedule.deinit_timer()
        print("Collected, exiting now")

main()
