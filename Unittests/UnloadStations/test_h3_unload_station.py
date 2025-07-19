import pytest
from unittest.mock import AsyncMock, MagicMock, call, patch

from UnloadStations.h3_unload_station import H3UnloadStation
import simulation_logger


@pytest.mark.asyncio
@patch("asyncio.sleep", return_value=None)
async def test_unload_single_truck(mock_sleep, monkeypatch):
    """Test H3UnloadStation.unload"""

    # Mock: Add an Unload Station
    control_center = MagicMock()
    control_center.unload_complete = AsyncMock()
    station = H3UnloadStation(control_center=control_center, name="H3 Unload Station X", sim_time_unit=5)
    station._calculate_unload_time_in_simulation = MagicMock(return_value=1)

    # Mock: Add a Truck
    truck = MagicMock()
    truck.name = "Truck X"

    # Mock: Add a SimulationLogger. (Use monkeypatch)
    log_msgs = []
    class DummyLogger:
        def log(self, message):
            log_msgs.append(message)
    monkeypatch.setattr(
        target=simulation_logger.SimulationLogger,
        name="get_instance",
        value=staticmethod(lambda: DummyLogger())
    )

    await station.unload(truck)

    # Verification: check log messages
    assert log_msgs[0] == "(+) H3 Unload Station X started unloading from Truck X."
    assert log_msgs[1] == "(-) H3 Unload Station X finished unloading from Truck X."

    # Verification: unload_complete should call it once.
    station._control_center.unload_complete.assert_awaited_once_with(truck=truck, station=station)


@pytest.mark.asyncio
@patch("asyncio.sleep", return_value=None)
async def test_unload_multiple_trucks(mock_sleep, monkeypatch):
    """Test H3UnloadStation.unload"""

    # Mock: Add an Unload Station
    control_center = MagicMock()
    control_center.unload_complete = AsyncMock()
    station = H3UnloadStation(control_center=control_center, name="H3 Unload Station X", sim_time_unit=5)
    station._calculate_unload_time_in_simulation = MagicMock(return_value=1)

    # Mock: Add a SimulationLogger. (Use monkeypatch)
    log_msgs = []
    class DummyLogger:
        def log(self, message):
            log_msgs.append(message)
    monkeypatch.setattr(
        target=simulation_logger.SimulationLogger,
        name="get_instance",
        value=staticmethod(lambda: DummyLogger())
    )

    # Mock: Add Trucks
    trucks = []
    for i in range(5):
        truck = MagicMock()
        truck.name = f"Truck {i}"
        trucks.append(truck)

    for truck in trucks:
        await station.unload(truck)

    # Verification: check log messages
    expected_messages = []
    for i in range(5):
        expected_messages.append(f"(+) H3 Unload Station X started unloading from Truck {i}.")
        expected_messages.append(f"(-) H3 Unload Station X finished unloading from Truck {i}.")
    assert log_msgs == expected_messages

    # Verification: unload_complete should call it 5 times.
    calls = [call(truck=trucks[i], station=station) for i in range(5)]
    station._control_center.unload_complete.assert_has_awaits(calls)


@pytest.mark.asyncio
@patch("asyncio.sleep", return_value=None)
async def test_unload_truck_name_not_defined(mock_sleep, monkeypatch):
    """Test H3UnloadStation.unload"""

    # Mock: Add an Unload Station
    control_center = MagicMock()
    control_center.unload_complete = AsyncMock()
    station = H3UnloadStation(control_center=control_center, name="H3 Unload Station X", sim_time_unit=5)
    station._calculate_unload_time_in_simulation = MagicMock(return_value=1)

    # Mock: Add a Truck
    truck = MagicMock()
    truck.name = None

    # Mock: Add a SimulationLogger. (Use monkeypatch)
    log_msgs = []
    class DummyLogger:
        def log(self, message):
            log_msgs.append(message)
    monkeypatch.setattr(
        target=simulation_logger.SimulationLogger,
        name="get_instance",
        value=staticmethod(lambda: DummyLogger())
    )

    await station.unload(truck)

    # Verification: check log messages
    assert log_msgs[0] == "(+) H3 Unload Station X started unloading from Unknown Truck."
    assert log_msgs[1] == "(-) H3 Unload Station X finished unloading from Unknown Truck."

    # Verification: unload_complete should call it once.
    station._control_center.unload_complete.assert_awaited_once_with(truck=truck, station=station)


@patch("asyncio.sleep", return_value=None)
def test_verify_unload_time(mock_sleep):
    # Note: Instead of adding a unit test file for unload_station, I just added to here...
    # Verify Time unit: 1, 2, 5, 10
    for time_unit, expected in [[1, 5], [2, 2.5], [5, 1], [10, 0.5]]:
        _test_verify_unload_time_for_time_unit_x(time_unit=time_unit, expected=expected)


def _test_verify_unload_time_for_time_unit_x(time_unit: int, expected: float):
    control_center = MagicMock()
    station = H3UnloadStation(control_center=control_center, sim_time_unit=time_unit)
    assert expected == station._calculate_unload_time_in_simulation()
