## Lunar Helium-3 Mining Simulation

This project is a simulation of a lunar Helium-3 space mining operation for over 72 hours.

### Overview
* Goal: Simulate and analyze the continuous movement and efficiency of mining trucks and unload stations during Helium-3 extraction on the moon.
* Key Features:
  * Configurable number of mining trucks and unload stations
  * Configurable total operation hours and ratio between simulation time and real world time
  * Detailed logging and reporting of operational statistics

### How it works

#### Components
* Mining Trucks
  * Travel between mining sites and unload stations.
  * Each truck operates independently.
  * Mining time: between 1 and 5 hours
  * Travel time: 30 minutes
* Mining Sites 
  * Infinite number of sites: each mining truck always finds an available mining site immediately.
* Unload Stations
  * Each station can serve only one truck at a time to unload Helium-3. 
  * If all stations are busy, trucks queue and wait their turn. (FIFO)

#### Simulation Flow
1. Each truck starts empty at a mining site.
2. It spends 1–5 hours mining Helium-3.
3. The truck travels 30 minutes to the nearest available unload station.
4. If all stations are busy, the truck queues until a station is free.
5. Unloading lasts 5 minutes.
6. The truck proceeds directly back to a mining site to repeat the cycle.

### Running the Simulation

* Prerequisites
  * Python 3.8+
    * pytest
    * asyncio

* Running
  * `python main.py`
  * You will be prompted to enter:
    * Number of mining trucks
    * Number of unload stations
    * Simulation time unit: 1, 2, 5, or 10 simulation minutes per real second
    * Test duration in simulation hours: enter 72 for a full operation

### Project Structure
* main.py
  * CLI entry point
* mining_control_center.py
  * Simulation engine
* simulation_logger.py	
  * Logging for the simulation
  * Use thread + Singleton
* time_converter.py
  * Simulation/real-time conversion functions
* /UnloadStations/unload_station
  * Abstraction class for all unload stations
  * For this project, there is only one type: Helium-3
* /UnloadStations/h3_unload_station
  * Unload station for Helium-3
* /Vehicles/mining_truck
  * Abstraction class for all mining truck.
  * For this project, there is only one type of vehicle: Truck for Helium-3
* /Vehicles/h3_mining_truck
  * Mining truck for Helium-3
  
### Note

* asyncio is used throughout most modules instead of threading for asynchronous event handling.
This is because almost all simulation agents (e.g., mining trucks, unload stations) spend most of their lifecycle 
in a waiting state (e.g., mining, traveling, unloading) rather than doing heavy parallel computation or real-time I/O.
* This design fits the goals of the simulation, allowing scalable, logical, and easy-to-test event-driven concurrency.

* Additionally, both mining trucks and unload stations are implemented as abstract base classes (MiningTruck, UnloadStation).
Each specific resource—for example, Helium-3 trucks (H3MiningTruck) or unload stations (H3UnloadStation); simply inherits and specializes these base classes.
While the current simulation models only Helium-3 operations, the codebase is structured so you can easily add 
additional mining types by making a new class for each resource type and tweaking constants or logic as needed.
To support this, an enumeration (MiningType) and appropriate abstract class patterns have been prepared; 
offering a buffer for future growth and making the simulation extensible and maintainable as real life projects.