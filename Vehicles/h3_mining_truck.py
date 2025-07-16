import time
from random import randint

from Vehicles.mining_truck import MiningTruck
from simulation_logger import SimulationLogger
from time_converter import convert_sim_time_to_real_time_in_mil_sec


class H3MiningTruck(MiningTruck):
    """Mining Truck for Helium-3 class."""
    # Mining time: 60 minutes to 300 minutes
    LEAST_TIME_TO_MINE = 60
    MOST_TIME_TO_MINE = 60 * 5
    # Travel time between a mining site and an unload station: 30 minutes
    TRAVEL_TIME = 30

    def go(self) -> None:
        """Let the truck goes to a mining site and wait until arrive."""

        # 1. Find a random mining time: randint(LEAST_TIME_TO_MINE, MOST_TIME_TO_MINE) + TRAVEL_TIME
        mining_time_in_simulation = randint(self.LEAST_TIME_TO_MINE, self.MOST_TIME_TO_MINE)

        # 2. Report start
        SimulationLogger.get_instance().log(
            unix_timsstamp=time.time(),
            message=f"Truck {self.name} left the control center."
        )
        time.sleep(self._get_travel_time_in_real_time())
        SimulationLogger.get_instance().log(
            unix_timsstamp=time.time(),
            message=f"Truck {self.name} arrived at a mining site. Mining time: {mining_time_in_simulation}."
        )

        # 3. Wait for mining time
        time.sleep(
            convert_sim_time_to_real_time_in_mil_sec(
                sim_time_to_convert_in_minutes=mining_time_in_simulation,
                sim_time_unit=self._sim_time_unit
            )
        )
        SimulationLogger.get_instance().log(
            unix_timsstamp=time.time(),
            message=f"Truck {self.name} completed for mining. Leave the mining site."
        )

        # 4. Report arrival -> ready to unload
        time.sleep(self._get_travel_time_in_real_time())
        SimulationLogger.get_instance().log(
            unix_timsstamp=time.time(),
            message=f"Truck {self.name} arrived and ready to unload."
        )

        # 5. Notify truck is ready to unload (Notify to Control Center??)
        self._control_center.truck_arrived(truck=self)
