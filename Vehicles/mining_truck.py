from abc import ABC, abstractmethod

from mining_control_center import MiningType


class MiningTruck(ABC):
    def __init__(self, name, mining_type: MiningType, sim_time_unit):
        self._name = name
        self._mining_type = mining_type
        self._sim_time_unit = sim_time_unit

    @abstractmethod
    def go(self):
        # Go to a mining site and mining
        pass