from abc import ABC, abstractmethod
from Vehicles.mining_truck import MiningTruck


class UnloadStation(ABC):
    def __init__(self, name, sim_time_unit):
        self._name = name
        self.calculate_unload_time_in_simulation(sim_time_unit)

    @abstractmethod
    def calculate_unload_time_in_simulation(self, sim_time_unit):
        pass

    @abstractmethod
    def unload(self, truck: MiningTruck):
        # Unload
        pass