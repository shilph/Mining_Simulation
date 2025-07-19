import time
from collections import deque

import asyncio

from const import MiningType
from UnloadStations.unload_station import UnloadStation
from UnloadStations.h3_unload_station import H3UnloadStation

from Vehicles.h3_mining_truck import H3MiningTruck
from Vehicles.mining_truck import MiningTruck
from simulation_logger import SimulationLogger
from time_converter import convert_sim_time_to_real_time_in_mil_sec


class MiningControlCenter:
    def __init__(self, n: int, m: int, sim_time_unit: int):
        """
        :param n: number of mining trucks
        :param m: number of mining unload stations
        :param sim_time_unit: simulation time unit
        """
        self._num_trucks = n
        # Add n number of trucks and m number of stations
        self._trucks = deque()
        for i in range(1, n + 1):
            self._trucks.append(
                H3MiningTruck(
                    control_center=self,
                    name=f"H3 Truck #{i}",
                    mining_type=MiningType.HELIUM_3,
                    sim_time_unit=sim_time_unit
                )
            )
        self._trucks_to_unload = deque()

        # Instead of use a single queue, separates to available and in_use to reduce time to search.
        self._available_unload_stations = deque()
        for i in range(1, m + 1):
            self._available_unload_stations.append(
                H3UnloadStation(
                    control_center=self,
                    name=f"H3 Unload Station #{i}",
                    mining_type=MiningType.HELIUM_3,
                    sim_time_unit=sim_time_unit
                )
            )

        self._sim_time_unit = sim_time_unit
        self._unloads = 0

    async def run(self, duration: int) -> None:
        """Start the simulation.

        :param duration: test duration in simulation hours
        """
        duration_in_real_time = convert_sim_time_to_real_time_in_mil_sec(
            sim_time_to_convert_in_minutes=duration*60,      # Need to convert hours to minutes
            sim_time_unit=self._sim_time_unit
        )

        # Initialize the Logger
        SimulationLogger.get_instance().reset(
            start_time_in_unix_timestamp=time.time(),
            sim_time_unit=self._sim_time_unit
        )

        # 1. Report the simulation starts. Initiate the Logger
        SimulationLogger.get_instance().log(
            message=f"Start the simulation for {duration} hours."
        )

        # 2. Use thread to let trucks go -> set daemon True to terminate threads
        for truck in self._trucks:
            await self._send_truck(truck)

        # 3. Wait until finish: Give a quick report every 30 minutes
        # TODO: Instead of a hard value (30 min), use a variable to customize.
        tic = convert_sim_time_to_real_time_in_mil_sec(
            sim_time_to_convert_in_minutes=30,
            sim_time_unit=self._sim_time_unit
        )
        timeleft = duration_in_real_time
        SimulationLogger.get_instance().log(f"Wait for {duration_in_real_time} minutes...")
        while timeleft > 0:
            await asyncio.sleep(tic)
            SimulationLogger.get_instance().log(
                message=f"-- Notify every 30 minutes. --"
            )
            timeleft -= tic

        # 4. Report completion
        SimulationLogger.get_instance().log(
            message=f"Finish the simulation for {duration} hours. Total unloads: {self._unloads}\n"
        )

    async def _send_truck(self, truck: MiningTruck) -> None:
        """Send the truck to a mining site.

        :param truck: Truck to send.
        """
        # Send a truck
        asyncio.create_task(truck.go())

    async def _unload(self, truck: MiningTruck, station: UnloadStation) -> None:
        """Unload the truck at the given Unload Station.

        :param truck: Truck to unload.
        :param station: Unload Station to unload.
        """
        # Start to unload
        asyncio.create_task(station.unload(truck))

    async def truck_arrived(self, truck: MiningTruck) -> None:
        """Event: When a truck arrives.

        :param truck: Truck to arrive to unload.
        """
        if self._available_unload_stations:
            # Get an available Unload Station and store the thread.
            station = self._available_unload_stations.popleft()
            await self._unload(truck=truck, station=station)
        else:
            # If there is no available unload station, put the truck into queue
            self._trucks_to_unload.append(truck)

    async def unload_complete(self, truck: MiningTruck, station: UnloadStation) -> None:
        """Event: When a truck is completed unloads.

        :param truck: Truck which is completed to unload.
        :param station: Unload Station
        """
        self._unloads += 1
        # Send the truck again
        await self._send_truck(truck=truck)

        if self._trucks_to_unload:
            # Get a truck on queue
            truck = self._trucks_to_unload.popleft()
            await self._unload(truck=truck, station=station)
        else:
            self._available_unload_stations.append(station)
