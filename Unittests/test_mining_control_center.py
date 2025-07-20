import unittest

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from collections import deque

from Vehicles.h3_mining_truck import H3MiningTruck
from mining_control_center import MiningControlCenter


class TestMiningControlCenter(unittest.IsolatedAsyncioTestCase):
    """Test the MiningControlCenter class."""

    class DummyLogger:
        """Mock Logger for logging; Use this class instead of SimulationLogger."""

        def __init__(self, log_msgs):
            self._log_msgs = log_msgs
            self.thread = AsyncMock()

        def log(self, message):
            """Save log messages to log_msgs"""
            self._log_msgs.append(message)

        def reset(self, start_time_in_unix_timestamp, sim_time_unit):
            """Mocking reset function. Do nothing."""
            pass

    def _make_unload_stations(self) -> deque:
        """Create unload station mock queue."""
        unload_station = MagicMock(name="Unload Station X")
        unload_station._control_center = self._control_center
        unload_station.unload = AsyncMock()
        return deque([unload_station])

    def _make_truck(self, name: str = "Truck X") -> H3MiningTruck:
        """Create a Trcuk mock"""
        truck = MagicMock()
        truck.name = name
        truck.start_to_mining = AsyncMock()
        return truck

    def setUp(self):
        """Prepare for tests."""
        self._control_center = MiningControlCenter(n=5, m=2, sim_time_unit=10)
        self._control_center._trucks = deque(
            [self._make_truck(name=f"Truck {i}") for i in range(5)]
        )
        self._control_center._unload = AsyncMock()
        self._control_center._send_truck = AsyncMock()
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
    async def test_truck_arrived_and_unload_station_available(self):
        """Test: When a Truck arrived and there is an unload station available."""
        unload_stations = self._make_unload_stations()
        unload_station = unload_stations[0]
        self._control_center._available_unload_stations = unload_stations

        truck = self._make_truck()
        await self._control_center.truck_arrived(truck)

        # If there is available unload station, _unload should be called
        self._control_center._unload.assert_awaited_once_with(
            truck=truck, station=unload_station
        )
        self.assertEqual(self._control_center._unload.call_count, 1)

    @pytest.mark.asyncio
    async def test_truck_arrived_and_no_unload_station_available(self):
        """Test: When a Truck arrived and there is no unload station available."""
        unload_stations = deque()
        self._control_center._available_unload_stations = unload_stations

        truck = self._make_truck()
        self._control_center._trucks_to_unload = deque()
        await self._control_center.truck_arrived(truck)

        # If there is no available unload station, truck will be added to _trucks_to_unload
        assert 1 == len(self._control_center._trucks_to_unload)
        assert truck == self._control_center._trucks_to_unload[0]

    @pytest.mark.asyncio
    async def test_unload_completed_and_trucks_wait(self):
        """Test: If there is a truck waits for unloading when the unloading is complete."""
        unload_stations = self._make_unload_stations()
        unload_station = unload_stations[0]
        self._control_center._available_unload_stations = unload_stations

        truck = self._make_truck()
        truck.start_to_wait = 1
        self._control_center._trucks_to_unload = deque()

        truck_wait = self._make_truck("Truck Wait")
        self._control_center._trucks_to_unload = deque([truck_wait])

        await self._control_center.unload_complete(truck=truck, station=unload_station)

        # Verify that the truck in waitlist is removed and call for unloading.
        assert 0 == len(self._control_center._trucks_to_unload)
        self.assertEqual(self._control_center._unload.call_count, 1)

    @pytest.mark.asyncio
    @patch("asyncio.sleep", return_value=None)  # Skip wait time
    @patch("time_converter.convert_sim_time_to_real_time_in_sec", side_effect=(15, 5))
    async def test_run(self, mock_covert_time, mock_sleep):
        """Test run function."""
        # TODO: Verify testing reports too
        self._control_center.report = AsyncMock(return_value=None)

        await self._control_center.run(duration=3)

        # Verify messages: This unit test runs for 3 simulation hours and reports 6 notifications.
        expected_messages = [
            "Start the simulation for 3 hours.",
            "** Wait for 18.0 seconds in the real world time. **",
            "-- Notify every 30 minutes. --",
            "-- Notify every 30 minutes. --",
            "-- Notify every 30 minutes. --",
            "-- Notify every 30 minutes. --",
            "-- Notify every 30 minutes. --",
            "-- Notify every 30 minutes. --",
            "Finish the simulation for 3 hours. Total unloads: 0 times.",
        ]
        assert expected_messages == self._log_msgs

        # Verify all 5 trucks start to mining
        for truck in self._control_center._trucks:
            assert truck.start_to_mining.called