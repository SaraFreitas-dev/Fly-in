
PathFinder.py
    ✅ build_connected_zones_map()
    ✅ get_connected_zones()
    ✅ get_zone_cost()
    ❌ dijkstra_shortest_path()
    ❌ reconstruct_path()

Simulator.py
    ✅ create_drones()
    ❌ simulate_turn()
    ❌ run_simulation()
    ❌ occupancy system

# =========================================================
# dijkstra_shortest_path()
# =========================================================
FUNCTION dijkstra_shortest_path(start, goal):

↓

CREATE queue

CREATE costs dictionary

CREATE parent dictionary

CREATE visited set

↓

SET all costs = infinity

SET start cost = 0

ADD start to queue

↓

WHILE queue not empty:

↓

GET cheapest current zone

↓

IF current == goal:

    reconstruct path

    RETURN path

↓

FOR each neighbor:

↓

IF blocked:
    skip

↓

new_cost =
current_cost
+
movement_cost

↓

IF new_cost better:

    UPDATE costs

    UPDATE parent

    ADD neighbor to queue
# =========================================================
# reconstruct_path()
# =========================================================
FUNCTION reconstruct_path(parent, goal):

↓

CREATE empty path list

SET current = goal

↓

WHILE current exists:

    ADD current to path

    current = parent[current]

↓

REVERSE path

RETURN path




Simulator.py

# =========================================================
# simulate_turn()
# =========================================================
FOR each drone:

↓

IF delivered:
    continue

↓

GET current_zone

↓

GET next_zone

↓

IF occupied:
    wait

↓

ELSE:
    move drone

↓

current_step += 1
# =========================================================
# run_simulation()
# =========================================================
WHILE not all drones delivered:

    simulate_turn()