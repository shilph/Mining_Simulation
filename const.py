"""This is a file to store all const values."""

from enum import Enum


class MiningType(Enum):
    """Mining type Enum.
    There is only one MiningType, Helium-3 for this project; but I added for possible extension.
    """

    HELIUM_3 = 0


# Unload Station
UNLOADING_TIME_FOR_H3_UNLOAD_STATION = 5

# Mining Truck
TRAVELING_TIME_FOR_H3_MINING_TRUCK = 30
SHORTEST_TIME_FOR_MINING_H3 = 60
LONGEST_TIME_FOR_MINING_H3 = 300
