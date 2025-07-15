from Vehicles.mining_truck import MiningTruck


class H3UnloadStation(MiningTruck):
    UNLOAD_TIME = 5

    def calculate_unload_time_in_simulation(self, sim_time_unit):
        # Calculate unload time
        self._unload_time = sim_time_unit * H3UnloadStation.UNLOAD_TIME

    def unload(self, truck: MiningTruck):
        # 1. Report to unload
        # 2. Wait until unload
        # 3. Report completion
        # 4. Notify the unloading is completed
        pass