class Stopwatch:
    def __init__(self):
        self.time = 0

    def add(self, delta_time: float):
        self.time += delta_time

    def reset(self):
        self.time = 0

    def check(self, interval: float) -> bool:
        return self.time >= interval

    def check_reset(self, interval: float) -> bool:
        if self.check(interval):
            self.time = 0
            return True

        return False


class GameObject:
    def __init__(self):
        self.stopwatches = []

    def new_stopwatch(self) -> Stopwatch:
        stopwatch = Stopwatch()
        self.stopwatches.append(stopwatch)

        return stopwatch

    def add_all(self, delta_time: float):
        for stopwatch in self.stopwatches:
            stopwatch.add(delta_time)

    def reset_all(self):
        for stopwatch in self.stopwatches:
            stopwatch.reset()
