# timer.py
class Timer:
    def __init__(self, seconds):
        self.start_time = seconds
        self.time_left = seconds

    def update(self, dt):
        self.time_left = max(0.0, self.time_left - dt)

    def reset(self, seconds=None):
        if seconds is not None:
            self.start_time = seconds
        self.time_left = self.start_time

    def is_time_up(self):
        return self.time_left <= 0
