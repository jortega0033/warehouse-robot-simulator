# Architecture: implementer map

Planned, not implemented. This page adds only what [PRD.md](PRD.md) and [TECHNICAL_SPEC.md](TECHNICAL_SPEC.md) leave open for an implementer: where the pieces live, how data flows, and the points where the two documents disagree. Module boundaries are in [CLAUDE.md](../CLAUDE.md), "Architecture boundaries". Simulation rules, scheduler rules and the fixture are in the technical specification and are not repeated here.

## Data flow (planned)

1. A scenario (versioned JSON, caps checked) is loaded by `schema`.
2. `scheduler` assigns jobs and proposes one action per robot for the tick; `engine` validates the whole set and commits it, or keeps the previous snapshot. The result of every tick is appended to the replay.
3. The replay (scenario copy, solver version, seed, search settings, events, one action per robot per tick, final status, summary, optional checkpoints) is written in canonical encoding.
4. `verify` reads only the replay file. It rebuilds occupancy and job state from the scenario and the events, and returns accepted, or the first invalid tick, the robot IDs and the reason.
5. The browser page loads a replay through the local server, validates schema and bounds, and shows the grid and a text table of the same state. Import of an exported replay takes the same path.

Replay and scenario files are the only interface between steps 2 and 4: the verifier never calls the engine or scheduler.

## Tick and snapshot convention

The technical specification says the actions of tick t produce snapshot t+1, and the fixture table counts snapshots. This repository uses these words one way: **tick t** is the decision step starting from snapshot t; **snapshot n** is the state after n ticks. A fault found when validating the actions of tick t is reported at snapshot t+1, which is how the PRD reads "same-cell collision at tick 2" for the fixture. Ticket WH-01a (a sub-issue of #2) states this in the schema document and every error message uses it.

## Schema freeze

The epic says "agree the replay schema first" but no ticket owned it. Ticket WH-01a (a sub-issue of #2) defines schema version 1 in a schema document, reserves every field the later tickets use (blocked reason, unfinished IDs, search statistics, solver policy, checkpoints, wait reason, detour) and freezes it by merging. After that, a change bumps the version and updates the document, the verifier and the fixtures in the same pull request.

## Differences between the documents (to resolve in the tickets)

- Epic: "WH-01 and WH-02 can run in parallel". Issue for WH-02 lists WH-01 as a dependency. Resolution: WH-02 starts after WH-01a merges, because WH-01a now owns the schema.
- PRD: WH-05 depends on WH-02 and WH-03. The epic says "follows WH-03". Resolution: both, as in the PRD.
- The "continuing arrivals" fixture for oldest-first assignment is named in the success checks but not authored. Ticket WH-05 authors it.
- No runtime version, package name, command line, file layout or numeric input-size and search-expansion cap exists in either document. The tickets set defaults and record them in `CLAUDE.md`.

## PRD drift recorded here

- The PRD says the fresh-start command "opens the local browser, loads the fixture, and displays completion from recorded events". Ticket WH-01b implements it as `python -m warehouse_sim serve [scenario] [--port N] [--no-open]`: the default scenario is `scenarios/single-order.json`, the browser opens unless `--no-open` is given, and tests always pass `--no-open`.
- The PRD epic says the user can "inspect why robots detoured or stopped". Detours are recorded as a per-move `detour` annotation (extra ticks over the static route and the robot that caused it) by WH-08a and shown by WH-08b; waits and blocked runs have reasons from the same tickets.
- No planning horizon is defined in either document. Ticket #4 defines one (static distance plus 20 ticks) so that a goal held by a robot that cannot move ends a search at once and is never counted as search-budget exhaustion (D8, D15 in `docs/owner-decisions.md`).
- The technical design says to "treat nonmoving robots as occupied" without saying when a robot is non-moving. Ticket #4 defines it (D15): no job, plan ended, or `no_route`/`cap_hit` in the current planning round. A lower-priority robot that is not yet planned in the round is not non-moving and is ignored by higher-priority searches (standard prioritized planning); without that rule the hand-checked 3 by 2 crossing would end blocked. When a robot that ends `no_route` sits on a cell an earlier plan of the round enters, the round is repeated with it non-moving, and a bounded alternate priority order is tried afterwards. The two fixtures differ as a result: `crossing-3x2` completes, `corridor-swap` ends `no_legal_progress` with zero cap hits and with `horizon_hits` of two per planning round.
