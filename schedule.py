import time

class Schedule:
    def __init__(self, schedule):
        self.schedule = schedule
        print(schedule)

    def poll_time(self, timer):
        date = time.gmtime(time.time())
        print(date)
