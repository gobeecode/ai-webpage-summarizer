import time
from collections import defaultdict
from contextlib import contextmanager



class TimeHelper:

    _start_times = {}
    _elapsed_times = defaultdict(float)

    @staticmethod
    def get_elapsed(label: str):
        return TimeHelper._elapsed_times[label]

    @staticmethod
    @contextmanager
    def measure(label: str):
        TimeHelper._start_times[label] = time.perf_counter()
        try:
            yield
        finally:
            elapsed = time.perf_counter() - TimeHelper._start_times.pop(label)
            TimeHelper._elapsed_times[label] += elapsed