# Multi-Agent Warehouse Robot Coordination System

A real-time multi-agent warehouse simulation implementing A* search, dynamic task allocation, collision avoidance, priority scheduling, and battery-aware replanning.

---

## Features

- A* Path Planning with Manhattan Heuristic
- Dynamic Task Allocation (Nearest Task Strategy)
- Priority-Based Conflict Resolution
- Deadlock Prevention
- Dynamic Obstacle Addition (Mouse Click)
- Automatic Replanning
- Battery Simulation with Charging Station
- Real-Time Performance Metrics
- Makespan Tracking

---

## Algorithms Used

- A* Search
- Heuristic Optimization
- Greedy Task Assignment
- Constraint-Based Collision Avoidance
- Priority Scheduling

---

## How to Run

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Simulation

```bash
python main.py
```

---

## Controls

- Left Click → Add obstacle dynamically
- Robots automatically replan paths
- Charging station is shown in Green

---

## Metrics Displayed

- Nodes Expanded
- Path Cost
- Planning Time
- Battery Level
- Current Task
- Makespan
