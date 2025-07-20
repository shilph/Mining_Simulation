import pytest
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from Vehicles.h3_mining_truck import H3MiningTruck


class TestH3MiningTruck(unittest.IsolatedAsyncioTestCase):
    """Tests the H3MiningTruck class."""

    class DummyLogger:
        """Mock Logger for logging; Use this class instead of SimulationLogger."""

        def __init__(self, log_msgs):
            self._log_msgs = log_msgs

        def log(self, message):
            self._log_msgs.append(message)

    def setUp(self):
        """Prepare tests."""
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
    @patch("Vehicles.h3_mining_truck.randint", return_value=150)  # Use patch to return 150 min for mining time
    @patch("asyncio.sleep", return_value=None)  # Skip wait time
    async def test_go(self, mock_sleep, mock_randint):
        control_center = MagicMock()
        control_center.truck_arrived = AsyncMock()

        # Execute Truck.go
        truck_name = "Truck X"
        truck = H3MiningTruck(control_center=control_center, name=truck_name, sim_time_unit=5)
        await truck.go()

        # Verification: log messages and truck_arrived function was called once.
        assert self._log_msgs == [
            f"<-- {truck_name} left the control center.",
            f"<++ {truck_name} arrived at a mining site.",
            "+++ Mining time: 150 minutes.",
            f"++> {truck_name} completed for mining. Leave the mining site.",
            f"--> {truck_name} arrived and ready to unload.",
        ]

        assert control_center.truck_arrived.call_count == 1
        control_center.truck_arrived.assert_awaited_once_with(truck=truck)

        # Verification: mining time and mining count are increased
        assert 150 == truck.total_mining_time
        assert 1 == truck.total_mining
