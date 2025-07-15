from Vehicles.mining_truck import MiningTruck


class H3MiningTruck(MiningTruck):
    # Mining time: 60 minutes to 300 minutes
    LEAST_TIME_TO_MINE = 60
    MOST_TIME_TO_MINE = 60 * 5
    # Travel time between a mining site and an unload station: 30 minutes
    TRAVEL_TIME = 30


    def go(self):
        # 1. Find a random travel time: randint(LEAST_TIME_TO_MINE, MOST_TIME_TO_MINE) + TRAVEL_TIME
        # 2. Report start
        # 3. wait for travel time
        # 4. Report arrival -> ready to unload
        # 5. Notify truck is ready to unload (Notify to Control Center??)
        # Note. A truck should go to the unload queue -> use FIFO
        pass