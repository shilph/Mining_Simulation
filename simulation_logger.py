import threading
import time
from queue import Queue

from time_converter import convert_unix_time_to_sim_timestamp


class SimulationLogger:
    """Logger class for Simulation."""

    # SimulationLogger has to print a log at a time: use threading.Lock()
    _lock = threading.Lock()
    _log_queue = Queue()
    _instance = None
    thread = None
    _instance_lock = threading.Lock()
    _start_time_in_unix_tic = 0
    _sim_time_unit = 0

    def __init__(self):
        self._instance = self

    def reset(self, start_time_in_unix_timestamp: float, sim_time_unit: int) -> None:
        """Reset the simulation starting time.

        :param start_time_in_unix_timestamp: starting time in unix timestamp
        :param sim_time_unit: simulation time unit
        """
        self._start_time_in_unix_tic = start_time_in_unix_timestamp
        self._sim_time_unit = sim_time_unit
        if self.thread is None:
            self.thread = threading.Thread(target=self._print_log, daemon=True)
            self.thread.start()

    @classmethod
    def get_instance(cls) -> "SimulationLogger":
        """Use singleton instance for this class."""
        with cls._instance_lock:
            if cls._instance is None:
                cls._instance = SimulationLogger()
        return cls._instance

    def log(self, message: str|None, log_with_timestamp: bool = True) -> None:
        """Store message in log queue.

        :param message: message to log; None to notify the end of the queue.
        :param log_with_timestamp: whether to log message with timestamp.
        """
        # Stores message to _log_queue
        with self._lock:
            self._log_queue.put(
                (
                    time.time() if log_with_timestamp else 0,
                    message
                )
            )

    def _print_log(self):
        """Print log message one at a time."""
        while True:
            # Print logs in _log_queue. One at a time.
            # Wait until there is any message to pint
            msg = self._log_queue.get()
            if msg[1] is None:
                # If end notification is shown, stop the thread
                break
            if msg[0] > 0:
                sim_timestamp = convert_unix_time_to_sim_timestamp(
                    unix_time_start=self._start_time_in_unix_tic,
                    curr_unix_time=msg[0],
                    sim_time_unit=self._sim_time_unit,
                )
                print(f"[{sim_timestamp}] {msg[1]}")
            else:
                print(msg[1])
