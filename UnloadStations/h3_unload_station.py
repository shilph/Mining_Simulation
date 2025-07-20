import asyncio
from typing import Dict, Any

from UnloadStations.unload_station import UnloadStation
from Vehicles.mining_truck import MiningTruck
from simulation_logger import SimulationLogger
from const import UNLOADING_TIME_FOR_H3_UNLOAD_STATION


class H3UnloadStation(UnloadStation):
    """Unload Station for Helium-3."""

    UNLOADING_TIME = UNLOADING_TIME_FOR_H3_UNLOAD_STATION

    async def unload(self, truck: MiningTruck) -> None:
        """Unload a mining truck.

        :param truck: MiningTruck to unload.
        """

        # Just in case if truck does not have name...
        truck_name = truck.name if truck.name else "Unknown Truck"

        # Unloading
        SimulationLogger.get_instance().log(
            message=f"(+) {self.name} started unloading from {truck_name}."
        )
        await asyncio.sleep(self._calculate_unload_time_in_simulation())
        SimulationLogger.get_instance().log(
            message=f"(-) {self.name} finished unloading from {truck_name}."
        )

        # Notify unloading is completed
        self._unloads += 1
        await self._control_center.unload_complete(truck=truck, station=self)

    def report(self) -> Dict[str, Any]:
        return {
            "Total unloads": self._unloads,
            "Total unloading time": self._unloads * self.UNLOADING_TIME
        }