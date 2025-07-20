from abc import ABC, abstractmethod
from typing import Dict, Any

from const import MiningType
from time_converter import convert_sim_time_to_real_time_in_sec


class MiningTruck(ABC):
    """Abstract class for mining trucks.
    It may inherit from a Vehicle class, which has not been implemented for purpose.
    """

    # Each Truck type has its own travel time between a mining site and an unload station,
    TRAVEL_TIME = -1

    def __init__(
        self,
        control_center: "MiningControlCenter",
        name: str = "Truck",
        mining_type: MiningType = MiningType.HELIUM_3,
        sim_time_unit: int = 1,
    ):
        """Initialise a mining truck.

        :param control_center: MiningControlCenter instance
        :param name: Name of the mining truck
        :param mining_type: Mining type of the mining truck
        :param sim_time_unit: Simulation time unit
        """

        self._control_center = control_center
        self.name = name
        self._mining_type = mining_type
        self._sim_time_unit = sim_time_unit
        self._travel_time = -1

        # For statistics
        self.total_mining = 0
        self.total_mining_time = 0
        self.total_wait_time = 0
        self.start_to_wait = 0

    def _get_travel_time_in_real_time(self) -> float:
        """Get the travel time between a mining site and an unloading station.

        :return: travel time in real time.
        """
        if self._travel_time < 0:
            self._travel_time = convert_sim_time_to_real_time_in_sec(
                sim_time_to_convert_in_minutes=self.TRAVEL_TIME,
                sim_time_unit=self._sim_time_unit,
            )
        return self._travel_time

    @abstractmethod
    def go(self):
        """Send a mining truck to a mining site."""
        # Go to a mining site and mining
        pass

    def start_to_mining(self) -> None:
        """Start to mining."""
        pass

    @abstractmethod
    def report(self) -> Dict[str, Any]:
        """Reports simulation statistics.

        :return: simulation statistics
        """
        pass