[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/NdAim9o4)
# CourierGraph: Multi-Agent Routing and Scheduling Simulator


### Summary
This project simulates multiple couriers operating on a map represented as a weighted graph.

Couriers start from a shared depot, receive delivery assignments, compute routes using shortest-path logic, and simulate completing deliveries while accumulating travel time.

The focus of the project is algorithmic reasoning, scheduling heuristics, and modular program design using various data structures.

### Background:
No essential finance knowledge since it is not a finance-oriented project.
Key concepts:

1. A graph is a set of nodes connected by weighted edges.

2. Edge weights represent travel time between locations.

3. Dijkstra’s algorithm computes the shortest-path distance between nodes.

4. Scheduling assigns deliveries across couriers fairly or efficiently.

5. A simulation engine replays couriers’ actions step-by-step, recording completion time.

### File Structure:
The project is organized into several Python modules to keep responsibilities separate and readable. 

graph_algos.py
Defines the Graph class and implements shortest-path functionality using Dijkstra’s algorithm.

scenario.py
Parses scenario input files, validates correctness, and optionally prints a text-based map overview.

scheduler.py
Assigns deliveries to couriers and builds delivery routes using different ordering strategies.

simulator.py
Simulates courier movement along routes and records delivery completion times.

main.py
Serves as the entry point. Supports both command-line execution and an interactive text-based UI.

test_cases.py
Contains automated tests that run multiple scenarios and verify correctness of routing and simulation output.

scenario.txt / scenario_UCLA.txt
Example input files defining maps, depots, deliveries, and number of couriers.

### Running the Project
To run the simulator, ensure you are inside the project directory with Python 3.9+ installed. The main entry point is main.py, which takes a scenario file and an ordering strategy as arguments. For example, running python main.py scenario.txt nearest_2swap loads the map, assigns deliveries, computes routes, and prints simulation output. The ordering argument may be given, nearest, or nearest_2swap, depending on whether you want the deliveries performed in listed order, closest-first, or optimized using a local 2-swap improvement heuristic.

### Output:

For each run, the program prints:

Courier routes

Delivery completion logs with timestamps

Total number of deliveries

Completion time per courier

Overall makespan (maximum delivery time)

