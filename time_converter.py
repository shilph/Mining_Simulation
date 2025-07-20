def convert_sim_time_to_real_time_in_sec(
    sim_time_to_convert_in_minutes: int, sim_time_unit: int
) -> float:
    """Converts simulation time (minutes) to real time in seconds.

    :param sim_time_to_convert_in_minutes: simulation time in minutes
    :param sim_time_unit: simulation time unit
    :return: real time in mil seconds
    """

    if sim_time_unit <= 0:
        # sim_time_unit has to be one of main.SIM_TIME_UNIT. But add a quick check just in case.
        raise ValueError("sim_time_unit must be positive integer")
    return sim_time_to_convert_in_minutes / sim_time_unit


def convert_real_time_to_sim_time(
    real_time: float, sim_time_unit: int
) -> int:
    """Converts simulation time (minutes) to real time in seconds.

    :param real_time: real time in seconds
    :param sim_time_unit: simulation time unit
    :return: simulation time in minutes
    """

    if sim_time_unit <= 0:
        # sim_time_unit has to be one of main.SIM_TIME_UNIT. But add a quick check just in case.
        raise ValueError("sim_time_unit must be positive integer")
    return round(real_time * sim_time_unit)


def convert_unix_time_to_sim_timestamp(
    unix_time_start: float, curr_unix_time: float, sim_time_unit: int
) -> str:
    """Converts unix time to simulation timestamp in string

    :param unix_time_start: unix timestamp when the simulation starts
    :param curr_unix_time: current unix timestamp
    :param sim_time_unit: simulation time unit
    :return: simulation timestamp in string
    """

    if sim_time_unit <= 0:
        # sim_time_unit has to be one of main.SIM_TIME_UNIT. But add a quick check just in case.
        raise ValueError("sim_time_unit must be positive integer")
    elif curr_unix_time < unix_time_start:
        # This should not happen. The current time is always larger than the start time.
        raise ValueError("curr_unix_time must be greater than unix_time_start")
    minutes = int((curr_unix_time - unix_time_start) * sim_time_unit)
    return f"{minutes // 60:02d}:{minutes % 60:02d}"
