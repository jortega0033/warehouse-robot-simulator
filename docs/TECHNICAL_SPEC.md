# Warehouse Robot Simulator: technical specification

Planning document. Implementation and verification remain future work.

## Technical design

### Simulation rules

- Coordinates are zero-based with x increasing east and y increasing south. A rectangular grid contains walkable cells and walls. Pick and drop cells are declared walkable cells. A walkable cell can hold one robot at an integer tick.
- Each job has a stable ID, integer release tick, pickup and drop cells, assigned robot if any, and status. Its normal states are queued, assigned, carrying, and complete. A robot carries one job at most. A blocked run retains unfinished jobs and reports why it stopped.
- At the start of tick t, release eligible orders and assign reachable jobs to free robots. Sort by release tick, then stable job ID. Pick the free robot with shortest static distance to the pickup, followed by stable robot ID. Compute the proposed action set from the same starting view. Each robot moves one cardinal step, waits, picks up, or drops off. Each service action occupies a full tick and leaves the robot in place. Validate and commit the whole action set together. Emit transitions in robot ID order. The resulting snapshot is tick t+1.
- At tick t+1, destinations must be unique. Forbid two robots from traversing the same edge in opposite directions in the same tick. Validate walls, movement distance, job ownership, and service state before committing.
- Use integer values. For path expansion use north, east, south, west, then wait. Break equal search scores by estimated arrival, elapsed ticks, y, x, and insertion order. Record scenario version, solver version, starting state, and seed.

### Scheduler

Use static reverse distances to flag unreachable pickups or drops. For multi-robot planning, search cell-and-tick states. Reserve future cell occupancy, edge traversals, and service ticks. Check planned destinations and reverse reservations. Plan robots in stable order by current job age and ID, then by robot ID. Treat nonmoving robots as occupied until a valid action set releases their cells. If one priority order stalls a lower-priority robot, try a bounded deterministic alternate order. Commit only action sets that pass validation. Record search limits and planner settings in the run.

Keep waiting reasons and queued age visible. Report static impossibility immediately. Count a no-progress tick only when at least one released order remains unfinished and all robots wait. Reset the counter on other ticks. Terminate after eight consecutive qualifying ticks with a blocked report. Emit idle waits while only future orders remain and let those orders release normally. Limit searches and total ticks to terminate moving cycles. Distinguish static unreachable, search budget exhausted, no legal progress found, and run limit reached. A blocked result describes the solver's result under its configured bounds.

### Replay and interface

- Define versioned JSON for scenarios and replays. Replays contain the original scenario, solver metadata, release and assignment events, one action per robot per tick, final status, and summary. Add optional checkpoints for seeking. Stable keys, stable arrays, integer ticks, and a canonical encoding make replays reproducible.
- An independent checker reconstructs occupancy and job state from the original scenario and events. It validates releases and assignments without running the scheduler's policy. Reject missing or duplicate robot actions. Return the first invalid tick, affected robot IDs, and reason. Compare reconstructed completion counts and job states with the recorded summary.
- Provide a scenario picker, run status, tick controls, grid, order table, and replay error panel. The text table shows the same order and robot state as the grid. Support keyboard operation and visible focus. Validate import schema and bounds before rendering inert data.
- Begin with caps of 16 by 16 cells, 12 robots, 100 orders, and 2,000 ticks. Cap input size and search expansions. Document defaults alongside the run commands. Raise specific limits in the scale experiment after measuring resources and observing replay checks.

## Hand-checked fixture

Use a 3 by 2 grid without walls. Robot A starts at (0,0) and B at (2,0). Both orders release at tick 0. J01 goes from (0,0) to (2,0) and J02 from (2,0) to (0,0). The distance-to-pick rule assigns J01 to A and J02 to B. Here is one valid replay. The automatic planner may find a different valid route.

| Snapshot | Robot A | Robot B | Event at end of preceding tick |
|---|---|---|---|
| 0 | (0,0) | (2,0) | Initial state |
| 1 | (0,0) | (2,0) | Both pick up following assignment at tick 0 |
| 2 | (1,0) | (2,1) | B leaves the shared aisle |
| 3 | (2,0) | (1,1) | Both move horizontally on different rows |
| 4 | (2,0) | (0,1) | A drops J01 |
| 5 | (2,0) | (0,0) | B reaches the drop cell |
| 6 | (2,0) | (0,0) | B drops J02 |

Consecutive positions are stays or cardinal moves. Positions differ at every snapshot, and simultaneous moves traverse distinct edges. Both orders complete by tick 6. For a failing copy, change B's action arriving at snapshot 2 to move west into (1,0). The checker should report a same-cell collision at tick 2. Test the edge-swap rule separately by starting two robots adjacent and proposing that they trade cells at tick 1. All timings here are expected outcomes for authored fixtures.
