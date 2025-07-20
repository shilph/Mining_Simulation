from random import randint
import asyncio
from typing import Any, Dict

from Vehicles.mining_truck import MiningTruck
from simulation_logger import SimulationLogger
from time_converter import convert_sim_time_to_real_time_in_sec
from const import (
    TRAVELING_TIME_FOR_H3_MINING_TRUCK,
    SHORTEST_TIME_FOR_MINING_H3,
    LONGEST_TIME_FOR_MINING_H3,
)


class H3MiningTruck(MiningTruck):
    """Mining Truck for Helium-3."""

    # Travel time between a mining site and an unload station: 30 minutes
    TRAVEL_TIME = TRAVELING_TIME_FOR_H3_MINING_TRUCK

    async def go(self) -> None:
        """Let the truck goes to a mining site and start to mining."""

        # Report move
        SimulationLogger.get_instance().log(
            message=f"<-- {self.name} left the control center."
        )
        await asyncio.sleep(self._get_travel_time_in_real_time())
        SimulationLogger.get_instance().log(
            message=f"<++ {self.name} arrived at a mining site."
        )

        await self.start_to_mining()

    async def start_to_mining(self) -> None:
        """Start to mining.
        When the simulation starts, each truck starts at a mining site.
        """
        # Find a random mining time: randint(shortest time, longest time) + TRAVEL_TIME
        mining_time_in_simulation = randint(
            SHORTEST_TIME_FOR_MINING_H3, LONGEST_TIME_FOR_MINING_H3
        )
        SimulationLogger.get_instance().log(
            message=f"+++ Mining time: {mining_time_in_simulation} minutes."
        )

        # Wait for mining time
        await asyncio.sleep(
            convert_sim_time_to_real_time_in_sec(
                sim_time_to_convert_in_minutes=mining_time_in_simulation,
                sim_time_unit=self._sim_time_unit,
            )
        )
        SimulationLogger.get_instance().log(
            message=f"++> {self.name} completed for mining. Leave the mining site."
        )

        # Report arrival -> ready to unload
        await asyncio.sleep(self._get_travel_time_in_real_time())
        SimulationLogger.get_instance().log(
            message=f"--> {self.name} arrived and ready to unload."
        )

        # Save mining time when the truck arrived only.
        self.total_mining_time += mining_time_in_simulation
        self.total_mining += 1

        # Notify truck is ready to unload (Notify to Control Center??)
        await self._control_center.truck_arrived(truck=self)

    def report(self) -> Dict[str, Any]:
        """Reports simulation statistics.

        :return: simulation statistics
        """
        return {
            "Total mining time": self.total_mining_time,
            "Total mining": self.total_mining,
            "Total wait time": self.total_wait_time
        }
