import threading
from queue import Queue


class SimulationLogger:
    # SimulationLogger has to print a log at a time: use threading.Lock()
    _lock = threading.Lock()
    _instance = None
    _log_queue = Queue()

    _start_time_in_unix_tic = 0
    _sim_time_unit = 0

    def __init__(self, start_time_in_unix_timestamp, sim_time_unit):
        self._start_time_in_unix_tic = start_time_in_unix_timestamp
        self._sim_time_unit = sim_time_unit
        # TODO: init others.

    @classmethod
    def get_instance(cls) -> 'SimulationLogger':
        # TODO: Use singleton design to get a SimulationLogger instance.
        return cls._instance

    def log(self, unix_timsstamp, message: str):
        # Stores message to _log_queue
        self._log_queue.put((unix_timsstamp, message))
        pass

    def print_log(self):
        while True:
            # Print logs in _log_queue. One at a time.
            # TODO: convert from current time to simulation time. (Should I make a function?)
            pass
