import time
from collections import deque
import asyncio

from const import MiningType
from UnloadStations.unload_station import UnloadStation
from UnloadStations.h3_unload_station import H3UnloadStation
from Vehicles.h3_mining_truck import H3MiningTruck
from Vehicles.mining_truck import MiningTruck
from simulation_logger import SimulationLogger
from time_converter import convert_sim_time_to_real_time_in_sec, convert_real_time_to_sim_time


class MiningControlCenter:
    """Mining Control Center class. The main class for the simulation."""

    def __init__(self, n: int, m: int, sim_time_unit: int):
        """
        :param n: number of mining trucks
        :param m: number of mining unload stations
        :param sim_time_unit: simulation time unit
        """

        # Add n number of trucks and m number of stations
        self._trucks = deque()
        for i in range(1, n + 1):
            self._trucks.append(
                H3MiningTruck(
                    control_center=self,
                    name=f"H3 Truck #{i}",
                    mining_type=MiningType.HELIUM_3,
                    sim_time_unit=sim_time_unit,
                )
            )
        self._trucks_to_unload = deque()

        # Instead of use a single queue, separates to available and in_use to reduce time to search.
        self._unload_stations = []
        self._available_unload_stations = deque()
        for i in range(1, m + 1):
            unload_station = H3UnloadStation(
                control_center=self,
                name=f"H3 Unload Station #{i}",
                mining_type=MiningType.HELIUM_3,
                sim_time_unit=sim_time_unit,
            )
            self._available_unload_stations.append(unload_station)
            self._unload_stations.append(unload_station)


        self._sim_time_unit = sim_time_unit
        self.unloads = 0

    async def run(self, duration: int) -> None:
        """Start the simulation.

        :param duration: test duration in simulation hours
        """
        duration_in_real_time = convert_sim_time_to_real_time_in_sec(
            sim_time_to_convert_in_minutes=duration * 60,  # Need to convert hours to minutes
            sim_time_unit=self._sim_time_unit,
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
            asyncio.create_task(truck.start_to_mining())

        # 3. Wait until finish: Give a quick report every 30 minutes
        tic = convert_sim_time_to_real_time_in_sec(
            sim_time_to_convert_in_minutes=30, sim_time_unit=self._sim_time_unit
        )
        timeleft = duration_in_real_time
        SimulationLogger.get_instance().log(
            f"** Wait for {duration_in_real_time} seconds in the real world time. **"
        )
        while timeleft > 0:
            await asyncio.sleep(tic)
            SimulationLogger.get_instance().log(
                message=f"-- Notify every 30 minutes. --"
            )
            timeleft -= tic

        # 4. Report completion
        SimulationLogger.get_instance().log(
            message=f"Finish the simulation for {duration} hours. Total unloads: {self.unloads} times."
        )

        self.report(duration=duration * 60)

        SimulationLogger.get_instance().thread.join()

    def report(self, duration: int) -> None:
        """Reports simulation statistics."""
        SimulationLogger.get_instance().log(
            message="## Simulation Statistics Report",
            log_with_timestamp=False
        )
        SimulationLogger.get_instance().log(
            message="\n#### Simulation Statistics: Trucks",
            log_with_timestamp=False
        )
        self.report_trucks(duration=duration)
        SimulationLogger.get_instance().log(
            message="\n#### Simulation Statistics: Unload Stations",
            log_with_timestamp=False
        )
        self.report_unload_stations(duration=duration)
        SimulationLogger.get_instance().log(message=None)

    def report_trucks(self, duration: int) -> None:
        # Get results
        reports_trucks = {}
        for truck in self._trucks:
            reports_trucks[truck.name] = truck.report()

        # To make a table
        headers = [
            "Truck Name",
            "Total mining",
            "Total mining time (min)",
            "Mining utilization (%)",
            "Total wait time (min)",
        ]
        rows = []
        for truck_name, report in reports_trucks.items():
            total_mining_time = report.get("Total mining time", 0)
            rows.append([
                truck_name,
                str(report.get("Total mining", 0)),
                str(total_mining_time),
                f"{(total_mining_time / duration) * 100:.1f} %",
                str(report.get("Total wait time", 0)),
            ])

        # Find the longest value per column
        col_widths = [
            max(len(header), max((len(row[i]) for row in rows), default=0))
            for i, header in enumerate(headers)
        ]

        sep = " | "
        line = " -" + "-+-".join("-" * w for w in col_widths) + "-"
        header_row = sep.join(header.ljust(col_widths[i]) for i, header in enumerate(headers))

        SimulationLogger.get_instance().log(line, log_with_timestamp=False)
        SimulationLogger.get_instance().log(f"| {header_row} |", log_with_timestamp=False)
        SimulationLogger.get_instance().log(line, log_with_timestamp=False)
        for row in rows:
            SimulationLogger.get_instance().log(
                "| " +  sep.join(row[i].ljust(col_widths[i]) for i in range(len(headers))) + " |",
                log_with_timestamp=False
            )
        SimulationLogger.get_instance().log(line, log_with_timestamp=False)

    def report_unload_stations(self, duration: int) -> None:
        # Get results
        reports_unloads = {}
        for unload_station in self._unload_stations:
            reports_unloads[unload_station.name] = unload_station.report()

        # To make a table
        headers = [
            "Unload Station Name",
            "Total unloads",
            "Total unloading time",
            "Unloading utilization (%)"
        ]
        rows = []
        for unload_station_name, report in reports_unloads.items():
            total_unloading_time = report.get("Total unloading time", 0)
            rows.append([
                unload_station_name,
                str(report.get("Total unloads", 0)),
                str(total_unloading_time),
                f"{(total_unloading_time / duration) * 100:.1f} %",
            ])

        # Find the longest value per column
        col_widths = [
            max(len(header), max((len(row[i]) for row in rows), default=0))
            for i, header in enumerate(headers)
        ]

        sep = " | "
        line = " -" + "-+-".join("-" * w for w in col_widths) + "-"
        header_row = sep.join(header.ljust(col_widths[i]) for i, header in enumerate(headers))

        SimulationLogger.get_instance().log(line, log_with_timestamp=False)
        SimulationLogger.get_instance().log(f"| {header_row} |", log_with_timestamp=False)
        SimulationLogger.get_instance().log(line, log_with_timestamp=False)
        for row in rows:
            SimulationLogger.get_instance().log(
                "| " + sep.join(row[i].ljust(col_widths[i]) for i in range(len(headers))) + " |",
                log_with_timestamp=False
            )
        SimulationLogger.get_instance().log(line, log_with_timestamp=False)

    async def _send_truck(self, truck: MiningTruck) -> None:
        """Send the truck to a mining site.

        :param truck: Truck to send.
        """
        asyncio.create_task(truck.go())

    async def _unload(self, truck: MiningTruck, station: UnloadStation) -> None:
        """Unload the truck at the given Unload Station.

        :param truck: Truck to unload.
        :param station: Unload Station to unload.
        """
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
            SimulationLogger.get_instance().log(
                message=f"{truck.name} is waiting for next available unload stations.",
            )
            truck.start_to_wait = time.time()
            self._trucks_to_unload.append(truck)

    async def unload_complete(self, truck: MiningTruck, station: UnloadStation) -> None:
        """Event: When a truck is completed unloads.

        :param truck: Truck which is completed to unload.
        :param station: Unload Station
        """

        self.unloads += 1
        # Send the truck again
        if truck.start_to_wait > 0:
            truck.total_wait_time += convert_real_time_to_sim_time(
                time.time() - truck.start_to_wait, self._sim_time_unit
            )
            truck.start_to_wait = 0
        await self._send_truck(truck=truck)

        if self._trucks_to_unload:
            # Get a truck on queue
            truck = self._trucks_to_unload.popleft()
            await self._unload(truck=truck, station=station)
        else:
            self._available_unload_stations.append(station)
