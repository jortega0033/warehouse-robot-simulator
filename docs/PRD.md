# Warehouse Robot Simulator

## Product requirements

A developer or warehouse-layout planner can run a fictional order scenario, see how robots share aisle space, and inspect why an order completed or stalled. A saved run must replay the same decisions and pass a separate collision check. The browser shows a virtual grid and robot history. All scenarios use generated or locally authored data.

**First working slice.** Load a small included grid, assign one order to one robot, move one cell per tick, take one tick each to pick up and drop off, and replay the resulting history in a local browser. The user can step forward and back, inspect positions and order state, and verify completion.

**Target workflow.** Choose a scenario, validate it, start a run, and inspect the order queue alongside the grid. Pause or step to examine a reroute or an aging order. Load an exported replay and see its validation result, including the first offending tick if the data are invalid. Compare two scheduling policies over the same generated workload using completed orders, makespan, wait time, and blocked runs.

**Success checks.** An independent replay checker accepts the authored crossing fixture and detects a same-cell collision, an edge swap, a route through a wall, and a drop without pickup. Identical input, solver version, and seed produce the same canonical replay bytes. In a reachable fixture with continuing arrivals, an older reachable order wins the next assignment opportunity over later work. A run that stalls returns diagnostics and unfinished order IDs. Record performance on stated machine and fixture sizes. Two hundred robots is a scale experiment. Use the smaller seeded loads as the integration gate.

**Scope.** Local browser and CPU process, synthetic orders, cardinal movement, virtual pick and drop points, and replay import and export. Start with standard-library Python and plain JavaScript served from the same local origin. Use generated files in a scratch directory for checks. Physical devices, live inventory, and customer data are out of scope.

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

## Epic

**Deliver a deterministic warehouse simulator with independently verified multi-robot replay.** Finish when a user can run the small crossing and a larger seeded queue in the browser, inspect why robots detoured or stopped, and verify exported history with the independent checker. Reopen a completed run and confirm identical reconstructed positions and order states.

**Plan.** Agree the replay schema first. WH-01 and WH-02 can then run in parallel. WH-03 and WH-04 can run in parallel after both establish the contract. WH-05 follows WH-03. WH-06 integrates all lanes.

**Effort.** 16–25 hours of remaining engineering work including testing and integration. Parallel lanes change elapsed time. This is a prospective estimate.

### WH-01 · Build a one-order vertical slice · 2–3 hours

Define scenario and tick contracts. Build the local run entry point, deterministic order assignment, single-robot movement, service actions, and a minimal browser step view.

**Acceptance and verification.** A fixture with a robot already at the pickup and an adjacent drop produces pick, move, drop in three ticks. A wall blocks movement. A malformed coordinate produces a specific error. A documented fresh-start command opens the local browser, loads the fixture, and displays completion from recorded events.

### WH-02 · Implement independent replay verification · 2–3 hours

Depends only on freezing the WH-01 schema. This ticket can then run in parallel with the vertical slice. Build a standalone verifier and authored legal and illegal traces. Reconstruct the state independently of the simulation engine.

**Acceptance and verification.** The 3 by 2 trace reconstructs both completed jobs at tick 6. Same-cell collision, edge swap, wall traversal, and drop-without-pickup variants fail with the expected first tick and reason. An altered final summary fails on otherwise legal actions. Repeating verification produces the same result.

### WH-03 · Plan and commit multi-robot routes · 4–6 hours

Depends on WH-01 and WH-02. Add time-expanded search, cell and edge reservations, atomic tick validation, bounded replanning, and explicit completion and blockage states.

**Acceptance and verification.** The open 3 by 2 fixture produces a verifier-approved route completing both orders. An adjacent swap in a corridor with no bypass ends with a blocked result. Injecting an invalid action set leaves positions and order states at the previous snapshot. Two runs with the same inputs and settings produce identical event order.

### WH-04 · Add accessible browser replay and error inspection · 2–3 hours

Depends on WH-01 and WH-02. Add timeline controls, per-tick robot and order details, keyboard operation, and bounded local replay import and export.

**Acceptance and verification.** Keyboard users can advance from tick 0 to 6 and back. Tick 4 shows J01 complete and J02 carrying in both grid and text. Reopening the exported history reproduces the selected states after restart. Importing the collision fixture displays tick 2 and leaves the last valid replay usable.

### WH-05 · Report waiting, progress, and workload measurements · 3–5 hours

Depends on WH-02 and WH-03. Add deterministic workload generation, oldest-reachable job selection, waiting and no-progress reasons, and a same-input comparison of two assignment policies.

**Acceptance and verification.** Under the default policy, an older reachable job gets the next assignment even if a newer pickup is closer. The comparison policy chooses the nearest reachable robot and pickup pair first. An unreachable job stays visible while a younger reachable one proceeds. The all-wait fixture with released orders ends after eight no-progress ticks with unfinished IDs. With one order released at tick 10 and a robot at its pickup next to the drop, the first ten idle ticks leave the counter at zero and the order completes at snapshot 13. A seeded 12-robot, 50-order run reports its inputs, verifier results, and unfinished work. Report queued time as ticks from release to assignment. Completed runs contribute makespan. Blocked runs are counted separately.

### WH-06 · Integrate and measure the offline workflow · 3–5 hours

Depends on WH-03, WH-04, and WH-05. Add repeatable verification for seeded runs, browser checks with external network requests blocked, and a scale report using gradually larger scenarios up to 200 simulated robots.

**Acceptance and verification.** Run the documented offline browser flow with the integration scenario and confirm the checker result. Repeat a seeded run and match canonical hashes. Record completed orders, ticks, conflicts, planner expansions, elapsed time, and any cap reached per scale. Confirm keyboard replay and first-fault reporting.

[Official project inspiration](https://docs.google.com/document/d/1R5MyfVvn033KoXZXgXP65qRAXnhcjtVvO_VF7IxUZaA/edit?tab=t.ef9a30wzb1z5)
