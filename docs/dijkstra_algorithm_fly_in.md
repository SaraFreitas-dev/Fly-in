# Dijkstra Algorithm
> Weighted shortest path algorithm used to find the cheapest valid route between zones.

---

# Table of Contents

1. What is Dijkstra?
2. Why Dijkstra fits Fly-in
3. BFS vs Dijkstra
4. Weighted Graphs
5. Core Idea
6. How Dijkstra Thinks
7. Main Structures
8. Step-by-Step Example
9. Visual Simulation
10. Path Reconstruction
11. Complexity
12. Fly-in Integration
13. Common Mistakes
14. Suggested Project Architecture
15. Mental Model

---

# 1️⃣ What is Dijkstra?

Dijkstra is a graph algorithm used to find:

```text
The cheapest path between two points.
```

NOT:

```text
The shortest path in number of steps.
```

This difference is EXTREMELY important.

---

# 2️⃣ Why Dijkstra fits Fly-in

In Fly-in:

```text
normal      = 1 turn
priority    = 1 turn
restricted  = 2 turns
blocked     = impossible
```

Some zones are:

- faster
- slower
- impossible to enter

This means:

```text
NOT ALL MOVEMENTS COST THE SAME
```

That is exactly the kind of problem Dijkstra was created for.

---

# 3️⃣ BFS vs Dijkstra

# BFS

BFS thinks:

```text
"How many steps?"
```

Example:

```text
start -> A -> goal
```

BFS says:

```text
2 movements
```

---

# Dijkstra

Dijkstra thinks:

```text
"What is the total cost?"
```

Example:

```text
start -> restricted -> goal
```

Cost:

```text
1 + 2 = 3 turns
```

Another path:

```text
start -> priority -> normal -> goal
```

Cost:

```text
1 + 1 + 1 = 3 turns
```

Dijkstra compares COSTS.

---

# 4️⃣ Weighted Graphs

Fly-in is a:

# Weighted Graph

Because each movement has a different cost.

---

# Visual Example

```text
              (2)
start ---------------- roof1
  |                     |
  |                     |
 (1)                   (1)
  |                     |
  |                     |
corridorA ----------- goal
         (1)
```

The numbers represent movement costs.

---

# 5️⃣ Core Idea

Dijkstra constantly asks:

```text
"What is the cheapest known path so far?"
```

The algorithm:

- explores zones
- calculates costs
- updates cheaper routes
- remembers best paths

---

# 6️⃣ How Dijkstra Thinks

Imagine this graph:

```text
start
 ├── roof1 (cost 2)
 └── corridorA (cost 1)
```

The algorithm says:

```text
corridorA is currently cheaper
```

So it explores:

```text
corridorA first
```

---

# IMPORTANT

Dijkstra always explores:

# The cheapest known possibility

NOT:
- closest visually
- shortest in nodes
- random

---

# 7️⃣ Main Structures

Dijkstra usually needs:

---

# A️⃣ Costs Dictionary

Stores:

```text
best known cost to each zone
```

Example:

```python
{
    "start": 0,
    "roof1": 2,
    "corridorA": 1,
}
```

---

# B️⃣ Parent Dictionary

Stores:

```text
Where each zone came from
```

Example:

```python
{
    "roof1": "start",
    "goal": "corridorA"
}
```

Used later to rebuild the final path.

---

# C️⃣ Visited Zones

Prevents:
- infinite loops
- unnecessary recalculations

---

# D️⃣ Priority Queue Mindset

This is the MOST important part mentally.

The algorithm constantly selects:

```text
the zone with the lowest current cost
```

---

# 8️⃣ Step-by-Step Example

Imagine:

```text
start
 ├── roof1 (2)
 └── corridorA (1)

roof1
 └── goal (1)

corridorA
 └── goal (1)
```

---

# STEP 1

Start here:

```text
start
```

Current cost:

```text
0
```

---

# STEP 2

Explore neighbors:

```text
roof1      = 2
corridorA  = 1
```

Store:

```python
{
    "roof1": 2,
    "corridorA": 1
}
```

---

# STEP 3

Choose cheapest zone:

```text
corridorA
```

because:

```text
1 < 2
```

---

# STEP 4

Explore corridorA neighbors:

```text
goal = 1 + 1 = 2
```

Store:

```python
{
    "goal": 2
}
```

---

# STEP 5

Algorithm continues until:

```text
goal reached
```

---

# Final Result

```text
start -> corridorA -> goal
```

---

# 9️⃣ Visual Simulation

Think of Dijkstra like water spreading:

```text
start
  ↓
cheapest zones first
  ↓
more expensive zones later
```

---

# Another Visualization

```text
          [roof1]
             ↑
             |
             |
[start] → [corridorA] → [goal]
```

The algorithm gradually discovers:
- routes
- costs
- better alternatives

---

# 🔟 Path Reconstruction

The algorithm usually does NOT build the path immediately.

Instead it stores:

```text
parent relationships
```

Example:

```python
{
    "roof1": "start",
    "goal": "corridorA",
    "corridorA": "start"
}
```

---

# Rebuilding

Start from:

```text
goal
```

Then go backwards:

```text
goal
↑
corridorA
↑
start
```

Reverse result:

```text
start -> corridorA -> goal
```

---

# 1️⃣1️⃣ Complexity

Dijkstra is more expensive than BFS.

---

# BFS

Usually:

```text
O(V + E)
```

---

# Dijkstra

Usually:

```text
O((V + E) log V)
```

depending on implementation.

---

# 1️⃣2️⃣ Fly-in Integration

# PathFinder Responsibility

Dijkstra should ONLY answer:

```text
"What is the cheapest valid path?"
```

NOT:
- occupancy
- waiting
- congestion
- collisions

---

# Simulator Responsibility

Simulator handles:
- turns
- drone movement
- occupancy
- capacities
- simultaneous movement

---

# VERY IMPORTANT

Do NOT mix:
- pathfinding
- simulation logic

Too early.

---

# 1️⃣3️⃣ Common Mistakes

# ❌ Mistake 1

Mixing occupancy into Dijkstra immediately.

This explodes complexity.

---

# ❌ Mistake 2

Treating restricted as blocked.

Restricted means:

```text
higher cost
```

NOT impossible.

---

# ❌ Mistake 3

Trying to optimize before simulation works.

First:
- valid routes
- valid movement

Later:
- optimization
- rerouting
- congestion management

---

# ❌ Mistake 4

Thinking Dijkstra is "magic".

It is simply:

```text
constant comparison of costs
```

---

# 1️⃣4️⃣ Suggested Fly-in Architecture

```text
MapParser
    ↓

build_connected_zones_map()
    ↓

calculate_movement_cost()
    ↓

dijkstra_shortest_path()
    ↓

reconstruct_path()
    ↓

Simulator
```

---

# 1️⃣5️⃣ Mental Model

This is the MOST important thing to remember:

# BFS thinks:

```text
"What is the shortest route?"
```

---

# Dijkstra thinks:

```text
"What is the cheapest route?"
```

---

# Final Mental Image

Imagine a drone constantly asking:

```text
"If I continue this way,
will it cost me fewer turns?"
```

That is Dijkstra.

---

# Suggested Next Learning Steps

After understanding Dijkstra:

1. adjacency graphs
2. priority queues
3. path reconstruction
4. weighted graphs
5. simulator scheduling
6. occupancy systems
7. multi-agent routing

---

# Fly-in Connection

Your project is essentially:

```text
Weighted Graph Pathfinding
+
Turn-Based Scheduling
+
Multi-Drone Simulation
```

And Dijkstra is one of the best foundations for that.
