from abc import ABC, abstractmethod
from Vehicles.mining_truck import MiningTruck
from mining_control_center import MiningControlCenter, MiningType
from time_converter import convert_sim_time_to_real_time_in_mil_sec


class UnloadStation(ABC):
    """Abstract class for unload stations."""

    UNLOAD_TIME = 0

    def __init__(
            self,
            control_center: MiningControlCenter,
            name: str = "Unload Station",
            mining_type: MiningType = MiningType.HELIUM_3,
            sim_time_unit: int = 1):
        """Initialise a mining truck.

        :param control_center: MiningControlCenter instance
        :param name: Name of the mining truck
        :param mining_type: Mining type of the mining truck
        :param sim_time_unit: Simulation time unit
        """
        self.control_center = control_center
        self.name = name
        self._mining_type = mining_type
        self._unload_time = -1
        self._sim_time_unit = sim_time_unit

    def _calculate_unload_time_in_simulation(self) -> int:
        """Calculate the unload time in simulation to real time in real world miliseconds.

        :return: Unload time in real world miliseconds
        """
        if self._unload_time < 0:
            self._travel_time = convert_sim_time_to_real_time_in_mil_sec(
                sim_time_to_convert_in_minutes=self.UNLOAD_TIME,
                sim_time_unit=self._sim_time_unit
            )
        return self._travel_time

    @abstractmethod
    def unload(self, truck: MiningTruck) -> None:
        """Unload a mining truck.

        :param truck: MiningTruck to unload.
        """
        # Unload
        pass