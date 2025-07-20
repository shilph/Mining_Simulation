import pytest
import unittest
from unittest.mock import AsyncMock, MagicMock, call, patch

from UnloadStations.h3_unload_station import H3UnloadStation


class TestH3UnloadStation(unittest.IsolatedAsyncioTestCase):
    class DummyLogger:
        """Mock Logger for logging; Use this class instead of SimulationLogger."""

        def __init__(self, log_msgs):
            self._log_msgs = log_msgs

        def log(self, message):
            """Save log messages to log_msgs"""
            self._log_msgs.append(message)

    def setUp(self):
        # Mock: Add an Unload Station
        control_center = MagicMock()
        control_center.unload_complete = AsyncMock()
        self._station = H3UnloadStation(control_center=control_center, name="H3 Unload Station X", sim_time_unit=5)
        self._station._calculate_unload_time_in_simulation = MagicMock(return_value=1)
        self._log_msgs = []
        self._logger = self.DummyLogger(self._log_msgs)
        self._logger_patch = patch(
            target="simulation_logger.SimulationLogger.get_instance",
            return_value=self._logger,
        )
        self._logger_patch.start()

    def tearDown(self):
        """Clean up."""
        self._logger_patch.stop()

    @pytest.mark.asyncio
    @patch("asyncio.sleep", return_value=None)
    async def test_unload_single_truck(self, mock_sleep):
        """Test H3UnloadStation.unload"""
        # Mock: Add a Truck
        truck = MagicMock()
        truck.name = "Truck X"

        await self._station.unload(truck)

        # Verification: check log messages
        assert self._log_msgs[0] == "(+) H3 Unload Station X started unloading from Truck X."
        assert self._log_msgs[1] == "(-) H3 Unload Station X finished unloading from Truck X."

        # Verification: unload_complete should call it once.
        self._station._control_center.unload_complete.assert_awaited_once_with(
            truck=truck, station=self._station
        )

        assert 1 == self._station._unloads

    @pytest.mark.asyncio
    @patch("asyncio.sleep", return_value=None)
    async def test_unload_multiple_trucks(self, mock_sleep):
        """Test H3UnloadStation.unload"""

        # Mock: Add Trucks
        trucks = []
        for i in range(5):
            truck = MagicMock()
            truck.name = f"Truck {i}"
            trucks.append(truck)

        for truck in trucks:
            await self._station.unload(truck)

        # Verification: check log messages
        expected_messages = []
        for i in range(5):
            expected_messages.append(
                f"(+) H3 Unload Station X started unloading from Truck {i}."
            )
            expected_messages.append(
                f"(-) H3 Unload Station X finished unloading from Truck {i}."
            )
        assert self._log_msgs == expected_messages

        # Verification: unload_complete should call it 5 times.
        calls = [call(truck=trucks[i], station=self._station) for i in range(5)]
        self._station._control_center.unload_complete.assert_has_awaits(calls)

        assert 5 == self._station._unloads

    @pytest.mark.asyncio
    @patch("asyncio.sleep", return_value=None)
    async def test_unload_truck_name_not_defined(self, mock_sleep):
        """Test H3UnloadStation.unload"""

        # Mock: Add a Truck
        truck = MagicMock()
        truck.name = None

        await self._station.unload(truck)

        # Verification: check log messages
        assert (self._log_msgs[0] == "(+) H3 Unload Station X started unloading from Unknown Truck.")
        assert (self._log_msgs[1] == "(-) H3 Unload Station X finished unloading from Unknown Truck.")

        # Verification: unload_complete should call it once.
        self._station._control_center.unload_complete.assert_awaited_once_with(
            truck=truck, station=self._station
        )

        assert 1 == self._station._unloads

    @patch("asyncio.sleep", return_value=None)
    def test_verify_unload_time(self, mock_sleep):
        """Test: UnloadStation._calculate_unload_time_in_simulation."""
        # Verify Time unit: 1, 2, 5, 10
        for time_unit, expected in [[1, 5], [2, 2.5], [5, 1], [10, 0.5]]:
            self._test_verify_unload_time_for_time_unit_x(time_unit=time_unit, expected=expected)

    def _test_verify_unload_time_for_time_unit_x(self, time_unit: int, expected: float) -> None:
        """Check the calculated unload time is correct.

        :param time_unit: simulation time unit.
        :param expected: expected unload time.
        """
        control_center = MagicMock()
        station = H3UnloadStation(control_center=control_center, sim_time_unit=time_unit)
        assert expected == station._calculate_unload_time_in_simulation()
