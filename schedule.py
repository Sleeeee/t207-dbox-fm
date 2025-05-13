import time
from machine import Timer

class Schedule:
    def __init__(self, schedule=None, display=None):
        self.next_song = None
        self._schedule = None
        self.display = display
        self.time = {"hours": None, "minutes": None}
        self.timer = Timer()
        self.timer.init(mode=Timer.PERIODIC, period=10000, callback=self.poll_time)
        self.poll_time(self.timer)

        self.schedule = schedule

    @property
    def hours(self):
        return self.time["hours"]

    @property
    def minutes(self):
        return self.time["minutes"]

    @property
    def schedule(self):
        return self._schedule

    def plan_next_song(self):
        if self.schedule:
            self.next_song = self._schedule.pop()
            print(f"Next in queue is song {self.next_song["publication"]}. It will be played at {self.next_song["time"]["hours"]}:{self.next_song["time"]["minutes"]}")
        else:
            print("Queue is now empty. You are free to exit once the last song is over")

    @schedule.setter
    def schedule(self, rest_schedule):
        if rest_schedule is not None:
            for scheduling in rest_schedule:
                scheduling_time = scheduling["time"].split("T")[1].split(":") # [HH, MM, SS+'Z']
                scheduling["time"] = {"hours": int(scheduling_time[0]), "minutes": int(scheduling_time[1])}

            # Filters the schedule to skip songs that would never be played
            rest_schedule = list(filter(lambda f: (f["time"]["hours"] > self.hours) or (f["time"]["hours"] == self.hours and f["time"]["minutes"] >= self.minutes), rest_schedule))
            # Stores the schedule in reverse in a stack-fashion for optimized complexity
            self._schedule = sorted(rest_schedule, key=lambda s: (s["time"]["hours"], s["time"]["minutes"]), reverse=True)
            self.plan_next_song()

    def poll_time(self, timer):
        time_values = time.gmtime(time.time())[3:5] # (hours, minutes)
        if (self.minutes != time_values[1]) or (self.hours != time_values[0]):
            time_string = ""
            for t in time_values:
                time_string += str(t) if t > 9 else "0" + str(t) # Force two digits with starting zero if needed
            if self.display is not None:
                self.display.digits = time_string
            self.time["hours"] = time_values[0]
            self.time["minutes"] = time_values[1]

            if self.next_song is not None and self.next_song["time"]["minutes"] == self.minutes and self.next_song["time"]["hours"] == self.hours:
                print(f"Time is {self.hours}:{self.minutes}. Playing song {self.next_song["publication"]}")
                self.plan_next_song()

    def deinit_timer(self):
        self.timer.deinit()
