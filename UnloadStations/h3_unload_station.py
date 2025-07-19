import asyncio

from UnloadStations.unload_station import UnloadStation
from Vehicles.mining_truck import MiningTruck
from simulation_logger import SimulationLogger


class H3UnloadStation(UnloadStation):
    async def unload(self, truck: MiningTruck) -> None:
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
        await self._control_center.unload_complete(truck=truck, station=self)
