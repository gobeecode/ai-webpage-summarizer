import time
from contextlib import contextmanager
from typing import Dict


class TimeHelper:
    """Utility to measure elapsed time of code blocks by label."""

    _start_times: Dict[str, float] = {}
    _elapsed_times: Dict[str, float] = {}

    @staticmethod
    @contextmanager
    def measure(label: str):
        """
        Context manager to measure elapsed time for a code block.
        Usage:
            with TimeHelper.measure("my_task"):
                # code here
        """
        start_time = time.perf_counter()
        TimeHelper._start_times[label] = start_time
        try:
            yield
        finally:
            # always try to pop to avoid leaking start_times
            start = TimeHelper._start_times.pop(label, None)
            if start is not None:
                elapsed = time.perf_counter() - start
                TimeHelper._elapsed_times[label] = (
                    TimeHelper._elapsed_times.get(label, 0.0) + elapsed
                )

    @staticmethod
    def get_elapsed(label: str) -> float:
        """Return the total elapsed time recorded for a label (seconds)."""
        return TimeHelper._elapsed_times.get(label, 0.0)

    @staticmethod
    def clear(label: str = None):
        """
        Clear recorded times.
        - If label provided, clear only that label's elapsed time.
        - If label is None, clear all elapsed times and any active start times.
        """
        if label is None:
            TimeHelper._start_times.clear()
            TimeHelper._elapsed_times.clear()
        else:
            TimeHelper._start_times.pop(label, None)
            TimeHelper._elapsed_times.pop(label, None)
