import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from Vehicles.h3_mining_truck import H3MiningTruck
import simulation_logger


@pytest.mark.asyncio
@patch("Vehicles.h3_mining_truck.randint", return_value=150)
@patch("asyncio.sleep", return_value=None)
async def test_go(mock_sleep, mock_randint, monkeypatch):
    control_center = MagicMock()
    control_center.truck_arrived = AsyncMock()

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

    # Execute Truck.go
    truck_name = "Truck X"
    truck = H3MiningTruck(control_center=control_center, name=truck_name, sim_time_unit=5)
    await truck.go()

    assert log_msgs == [
        f"<- {truck_name} left the control center.",
        f"<+ {truck_name} arrived at a mining site. Mining time: 150 minutes.",
        f"+> {truck_name} completed for mining. Leave the mining site.",
        f"-> {truck_name} arrived and ready to unload."
    ]

    control_center.truck_arrived.assert_awaited_once_with(truck=truck)
