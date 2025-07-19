import unittest

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from collections import deque

from Vehicles.h3_mining_truck import H3MiningTruck
from mining_control_center import MiningControlCenter


class TestMiningControlCenter(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self._control_center = MiningControlCenter(n=5, m=2, sim_time_unit=1)
        self._control_center._trucks = deque()
        self._control_center._unload = AsyncMock()
        self._control_center._send_truck = AsyncMock()



    def _get_unload_stations(self) -> deque:
        unload_station = MagicMock(name="Unload Station X")
        unload_station._control_center = self._control_center
        unload_station.unload = AsyncMock()
        return deque([unload_station])


    def _get_truck(self) -> H3MiningTruck:
        truck = MagicMock()
        truck.name = "Truck X"
        return truck

    @pytest.mark.asyncio
    async def test_truck_arrived_and_unload_station_available(self):
        unload_stations = self._get_unload_stations()
        unload_station = unload_stations[0]
        self._control_center._available_unload_stations = unload_stations

        truck = self._get_truck()
        await self._control_center.truck_arrived(truck)

        # If there is available unload station, _unload should be called
        self._control_center._unload.assert_awaited_once_with(truck=truck, station=unload_station)

    @pytest.mark.asyncio
    async def test_truck_arrived_and_no_unload_station_available(self):
        unload_stations = deque()
        self._control_center._available_unload_stations = unload_stations

        truck = self._get_truck()
        self._control_center._trucks_to_unload = deque()
        await self._control_center.truck_arrived(truck)

        # If there is no available unload station, truck will be added to _trucks_to_unload
        assert 1 == len(self._control_center._trucks_to_unload)
        assert truck == self._control_center._trucks_to_unload[0]


