import threading
import time
from collections import deque
from enum import Enum

from UnloadStations.h3_unload_station import H3UnloadStation
from UnloadStations.unload_station import UnloadStation
from Vehicles.h3_mining_truck import H3MiningTruck
from Vehicles.mining_truck import MiningTruck
from simulation_logger import SimulationLogger
from time_converter import convert_sim_time_to_real_time_in_mil_sec


class MiningType(Enum):
    """Mining type Enum.
    There is only one MiningType, Helium-3 for this project; but I added for possible extension.
    """

    HELIUM_3 = 0


class MiningControlCenter:
    def __init__(self, n: int, m: int, sim_time_unit: int):
        """
        :param n: number of mining trucks
        :param m: number of mining unload stations
        :param sim_time_unit: simulation time unit
        """
        # Add n number of trucks and m number of stations
        self._trucks = deque(
            [
                H3MiningTruck(
                    control_center=self,
                    name=f"H3 Truck #{i}",
                    mining_type=MiningType.HELIUM_3,
                    sim_time_unit=sim_time_unit
                )
                for i in range(1, n + 1)
            ]
        )
        self._trucks_to_unload = deque()

        # Instead of use a single queue, separates to available and in_use to reduce time to search.
        self._available_unload_stations = deque(
            [
                H3UnloadStation(
                    control_center=self,
                    name=f"H3 Unload Station #{i}",
                    mining_type=MiningType.HELIUM_3,
                    sim_time_unit=sim_time_unit
                )
                for i in range(1, m + 1)
            ]
        )

        self._sim_time_unit = sim_time_unit
        self._unloads = 0
        self._is_complete = False

        self._lock = threading.Lock()
        # Store individual threads which send trucks
        self._truck_threads = {}
        self._unload_threads = {}


    def run(self, duration: int) -> None:
        """Start the simulation.

        :param duration: test duration in simulation hours
        """
        duration_in_real_time = convert_sim_time_to_real_time_in_mil_sec(
            sim_time_to_convert_in_minutes=duration*60,      # Need to convert hours to minutes
            sim_time_unit=self._sim_time_unit
        )

        # Initialize the Logger
        logger = SimulationLogger(
            start_time_in_unix_timestamp=time.time(), sim_time_unit=self._sim_time_unit
        ).get_instance()

        # 1. Report the simulation starts. Initiate the Logger
        logger.log(
            unix_timsstamp=time.time(),
            message=f"Start the simulation for {duration} hours."
        )

        # 2. Use thread to let trucks go -> set daemon True to terminate threads
        for truck in self._trucks:
            self._send_truck(truck)

        # 3. Wait until finish
        time.sleep(duration_in_real_time)

        # 4. Report completion
        num_trucks_went = len(self._truck_threads)
        num_unloading = len(self._unload_threads)
        logger.log(
            unix_timsstamp=time.time(),
            message=f"Finish the simulation for {duration} hours.\n"
                    f"* Total unloads: {self._unloads}\n"
                    f"* Number of trucks went to mining sites: {num_trucks_went}\n"
                    f"* Number of unloading stations in use: {num_unloading}\n"
        )
        self._is_complete = True

        # 4. Let the user chooses to terminate or wait the simulation
        if num_trucks_went > 0 or num_unloading > 0:
            terminate = input("Do you want to terminate the simulation? (Y/n) ")
            if terminate in ("N", "n"):
                for truck_name in self._truck_threads:
                    logger.log(
                        unix_timsstamp=time.time(),
                        message=f"Wait until Truck {truck_name} comes back.\n"
                    )
                    self._truck_threads[truck_name].join()
                for station_name in self._unload_threads:
                    logger.log(
                        unix_timsstamp=time.time(),
                        message=f"Wait until Unload Station {station_name} finishes.\n"
                    )
                    self._unload_threads[station_name].join()

    def _send_truck(self, truck: MiningTruck) -> None:
        """Send the truck to a mining site.

        :param truck: Truck to send.
        """
        # Truck will not be sent if the simulation is completed
        if not self._is_complete:
            thr = threading.Thread(target=truck.go, daemon=True)
            thr.start()
            self._truck_threads[truck.name] = thr

    def _unload(self, truck: MiningTruck, station: UnloadStation) -> None:
        """Unload the truck at the given Unload Station.

        :param truck: Truck to unload.
        :param station: Unload Station to unload.
        """
        # Unload Station will not be unloaded if the simulation is completed
        if not self._is_complete:
            thr = threading.Thread(target=station.unload, args=(truck,), daemon=True)
            thr.start()
            self._unload_threads[station.name] = thr

    def truck_arrived(self, truck: MiningTruck) -> None:
        """Event: When a truck arrives.

        :param truck: Truck to arrive to unload.
        """
        with self._lock:
            if self._available_unload_stations:
                # Get an available Unload Station and store the thread.
                station = self._available_unload_stations.popleft()
                self._unload(truck=truck, station=station)
            else:
                # If there is no available unload station, put the truck into queue
                self._trucks_to_unload.append(truck)

    def unload_complete(self, truck: MiningTruck, station: UnloadStation) -> None:
        """Event: When a truck is completed unloads.

        :param truck: Truck which is completed to unload.
        :param station: Unload Station
        """
        with self._lock:
            self._unloads += 1
            # Send the truck again
            self._send_truck(truck=truck)

            if self._trucks_to_unload:
                # Get a truck on queue
                truck = self._trucks_to_unload.popleft()
                self._unload(truck=truck, station=station)
            else:
                self._available_unload_stations.append(station)
                self._unload_threads.pop(station.name)
