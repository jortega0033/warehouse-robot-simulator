# Warehouse Robot Simulator

A planned offline project. Implementation has not started. The repository currently contains the product plan, technical specification and implementation backlog. A scaffold exists: `python -m unittest` runs the smoke tests and `python -m warehouse_sim --help` prints the planned commands.

## Program goal

Build a warehouse digital twin: thousands of robots with real motion, optimal and lifelong planning, order and stock decisions, failures and people, checked by an independent verifier and good enough to design a real site.

The program is planned ([#27](https://github.com/jortega0033/warehouse-robot-simulator/issues/27)). Phase 1 is the current epic [#1](https://github.com/jortega0033/warehouse-robot-simulator/issues/1) and the only phase with tickets.

**Score.** Throughput as a share of the proven upper bound on public multi-agent path finding benchmark maps, for a growing number of robots.

| Phase | Content | Hours (rough) | Issue |
|---|---|---|---|
| 1 | The current epic and its tickets | 54 to 84 | [#1](https://github.com/jortega0033/warehouse-robot-simulator/issues/1) |
| 2 | Optimal planning | 130 to 220 | [#28](https://github.com/jortega0033/warehouse-robot-simulator/issues/28) |
| 3 | Real motion | 110 to 180 | [#29](https://github.com/jortega0033/warehouse-robot-simulator/issues/29) |
| 4 | Operations | 110 to 180 | [#30](https://github.com/jortega0033/warehouse-robot-simulator/issues/30) |
| 5 | Layout design | 110 to 190 | [#31](https://github.com/jortega0033/warehouse-robot-simulator/issues/31) |
| 6 | Scale and view | 120 to 200 | [#32](https://github.com/jortega0033/warehouse-robot-simulator/issues/32) |

About 630 to 1050 engineer hours in total: rough estimates, not measurements. The numbers in the score and the finish lines are targets until a run shows them. Only phase 1 has tickets to work; the sub-issues of a later phase are written when it starts. No single session is expected to reach the end.

## Plan

- [Full product plan and acceptance criteria](docs/PRD.md)
- [Technical specification and verification fixtures](docs/TECHNICAL_SPEC.md)
- [Implementation epic](https://github.com/jortega0033/warehouse-robot-simulator/issues/1)

## Current status

The fixtures describe expected results for future checks. No working baseline or passing implementation tests are claimed. Required runtime versions and offline dependencies must be checked before the first build.

## Licensing

A license for this project has not been selected. Any upstream reference or adapted code must retain its applicable notices; see the plan.
