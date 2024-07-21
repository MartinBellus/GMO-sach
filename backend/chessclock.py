from utility.enums import Colors
import time


class ChessClock:
    def __init__(self, starting_time):
        starting_time = float(starting_time)
        self.remaining_time: dict[Colors, int] = {
            Colors.WHITE: starting_time, Colors.BLACK: starting_time}
        self.current: Colors | None = None
        self.clock_start_time: float | None = None

    def start(self, color: Colors):
        self.current = color
        self.clock_start_time = time.monotonic()

    def update_remaining_time(self):
        if self.current is not None:
            self.remaining_time[self.current] -= time.monotonic() - \
                self.clock_start_time
            if self.remaining_time[self.current] < 0:
                self.remaining_time[self.current] = 0
            self.clock_start_time = time.monotonic()

    def pause(self):
        self.update_remaining_time()
        self.current = None
        self.clock_start_time = None

    def get_time(self, color: Colors):
        self.update_remaining_time()
        return self.remaining_time[color]

    def add_time(self, color: Colors, time: float):
        self.update_remaining_time()
        self.remaining_time[color] += time
