import threading
from collections import deque
from enum import Enum



class MiningType(Enum):
    # What if there are different resources and required different truck or unload station?
    HELIUM_3 = 0


class MiningControlCenter:
    def __init__(self, n: int, m: int, sim_time_unit):
        """
        :param n: number of mining trucks
        :param m: number of mining unload stations
        :param sim_time_unit: simulation time unit
        """
        # TODO: Add Trucks and Unload Stations
        self.trucks = deque()
        # Instead of use a single queue, separates to available and in_use to reduce time to search.
        self.available_unload_stations = deque()
        self.unload_stations_in_use = deque()

        self.trucks_to_unload = deque()

        # Use semaphore to control unload stations
        # NOTE: Can be done with a simple queue. May need to find a cheaper solution.
        self.unload_semaphore = threading.Semaphore(m)

    def run(self, duration: int):
        # 1. Report the simulation starts. Initiate the Logger
        # 2. Use thread to let trucks go -> set daemon True to terminate threads
        # 3. Loop until timeout. Use simulation time
        # TODO: Replace True -> duration (in simulation time)
        while True:
            # 4. Check there is any truck to unload. (trucks_to_unload) If not, wait.
            # 4-1. If there is an available unload station, unload.
            # NOTE: Unload: remove the unload station to the in_use queue -> Use thread to wait while unloading.
            ## NOTE: If the main loop assign a truck to an unload station, it could lead a minor bottleneck.
            ##       Should truck_arrived() function do similar job?
            pass

    def truck_arrived(self, truck):
        self.trucks_to_unload.append(truck)

    def unload_complete(self, station):
        self.unload_stations_in_use.remove(station)
        self.available_unload_stations.append(station)
        # If I use unload_semaphore, self.unload_semaphore.release()