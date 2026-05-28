import time


class LatencyMetric:
    """
    Measures execution time
    """

    def __init__(self):
        self.start_time = None
        self.end_time = None

    def start(self):
        self.start_time = time.time()

    def stop(self):
        self.end_time = time.time()

    def value(self):
        if self.start_time is None or self.end_time is None:
            raise ValueError("Timer not properly used")
        return self.end_time - self.start_time