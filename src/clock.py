import math
import time

from src.flags import get_time_control


class Clock:
    def __init__(self):
        self.white = SubClock()
        self.black = SubClock()

    def __str__(self):
        return "CLOCK: w: " + str(self.white.time_left) + " b: " + str(self.black.time_left)


class SubClock:
    def __init__(self):
        self.time_started = -1
        self.time_left = get_time_control()
        self.running = False

    def start(self):
        if self.running:
            print("Clock already started")
            return
        self.running = True
        self.time_started = time.time() * 1000

    def stop(self):
        if not self.running:
            print("Clock already stopped")
            return
        self.running = False
        passed_time = math.ceil(time.time() * 1000 - self.time_started)
        self.time_left -= passed_time

    def is_out_of_time(self) -> bool:
        return self.time_left <= 0
