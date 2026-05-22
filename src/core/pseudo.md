
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