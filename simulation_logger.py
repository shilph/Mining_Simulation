import threading
import time
from queue import Queue

from time_converter import convert_unix_time_to_sim_timestamp


class SimulationLogger:
    # SimulationLogger has to print a log at a time: use threading.Lock()
    _lock = threading.Lock()
    _log_queue = Queue()
    _instance = None
    _thread = None
    _instance_lock = threading.Lock()
    _start_time_in_unix_tic = 0
    _sim_time_unit = 0

    def __init__(self):
        self._instance = self

    def reset(self, start_time_in_unix_timestamp, sim_time_unit):
        self._start_time_in_unix_tic = start_time_in_unix_timestamp
        self._sim_time_unit = sim_time_unit
        if self._thread is None:
            self._thread = threading.Thread(target=self._print_log, daemon=True)
            self._thread.start()

    @classmethod
    def get_instance(cls):
        with cls._instance_lock:
            if cls._instance is None:
                cls._instance = SimulationLogger()
        return cls._instance

    def log(self, message: str):
        # Stores message to _log_queue
        with self._lock:
            self._log_queue.put((time.time(), message))

    def _print_log(self):
        while True:
            # Print logs in _log_queue. One at a time.
            # Wait until there is any message to pint
            msg = self._log_queue.get()
            sim_timestamp = convert_unix_time_to_sim_timestamp(
                unix_time_start=self._start_time_in_unix_tic,
                curr_unix_time=msg[0],
                sim_time_unit=self._sim_time_unit
            )
            print(f"[{sim_timestamp}] {msg[1]}")
