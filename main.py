import asyncio
import sys

from mining_control_center import MiningControlCenter
from typing import List, Optional


def get_integer(prompt: str, selections: Optional[List[int]] = None) -> int:
    """Get an integer value from the user.
    If the input is not a positive integer, or is not in the selection list (if a selection list is provided),
        prompt the user to enter a value again.

    :param prompt: Prompt message to be displayed
    :param selections: list of integers which the user can select; None for default
    :return: An integer value from the user
    """
    while True:
        try:
            val = int(input(prompt))
            if val > 0:
                if selections:
                    # If
                    if val in selections:
                        return val
                    else:
                        raise ValueError
                else:
                    return val
            else:
                raise ValueError
        except ValueError:
            print("Invalid input. Please enter a valid integer.")


# only allows 1, 2, 5, or 10 for simulation time unit
SIM_TIME_UNIT = [1, 2, 5, 10]

if __name__ == '__main__':
    """Main function of the program. It simply executes the MiningControlCenter simulation."""

    # Get number of trucks and unload stations, simulation time unit & test duration from the user.
    num_trucks = get_integer("Please enter the number of trucks: ")
    num_unload_stations = get_integer("Please enter the number of unload stations: ")
    msg = ("Please enter the number of simulation MINUTES that will advance for every 1 SECOND of real-world time "
           "during the simulation run (1, 2, 5, or 10):")
    sim_time_unit = get_integer(msg, selections=SIM_TIME_UNIT)
    test_duration = get_integer("Please enter the test duration in simulation HOURS: ")

    # Run simulation.
    mining_control_center = MiningControlCenter(n=num_trucks,
                                                m=num_unload_stations,
                                                sim_time_unit=sim_time_unit)
    mining_control_center.run(test_duration)
