from abc import ABC, abstractmethod
from mining_control_center import MiningType, MiningControlCenter
from time_converter import convert_sim_time_to_real_time_in_mil_sec


class MiningTruck(ABC):
    """Abstract class for mining trucks.
    It may inherit from a Vehicle class, which has not been implemented for purpose.
    """

    TRAVEL_TIME = 0

    def __init__(
            self,
            control_center: MiningControlCenter,
            name: str = "Truck",
            mining_type: MiningType = MiningType.HELIUM_3,
            sim_time_unit: int = 1):
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

    def _get_travel_time_in_real_time(self):
        if self._travel_time < 0:
            self._travel_time = convert_sim_time_to_real_time_in_mil_sec(
                sim_time_to_convert_in_minutes=self.TRAVEL_TIME,
                sim_time_unit=self._sim_time_unit
            )
        return self._travel_time

    @abstractmethod
    def go(self):
        # Go to a mining site and mining
        pass