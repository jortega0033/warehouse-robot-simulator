# CLAUDE.md

Working instructions for this repository. Read this file first, then the documents it links to. It does not repeat them.

## What this is

A planned offline warehouse robot simulator. A person runs a fictional order scenario on a grid, watches robots share aisle space in a local browser, inspects why an order completed or stalled, and checks a saved replay with an independent verifier. **Nothing is implemented yet.** The repository holds the product plan, the technical specification and the backlog. No command in this file runs today; every command below is marked "planned" with the ticket that introduces it.

## Sources of truth

| Topic | Document |
|---|---|
| Product scope, requirements, ticket scopes, hand-checked fixture | [docs/PRD.md](docs/PRD.md) |
| Simulation rules, scheduler, replay and interface, same fixture | [docs/TECHNICAL_SPEC.md](docs/TECHNICAL_SPEC.md) |
| Planned module map, tick convention, schema freeze rule, differences between the documents | [docs/architecture.md](docs/architecture.md) (planned, not implemented) |
| Backlog | Epic issue #1 and its sub-issues on GitHub. The epic's table is authoritative for dependency order, parallel tracks and estimates. |
| Loop setup and its limits | [LOOP.md](LOOP.md), [loop-constraints.md](loop-constraints.md) |
| Project subagents, their origin and local changes | [.claude/agency-agents/README.md](.claude/agency-agents/README.md) |
| Ticket workflow and the step at which each agent role runs | [.claude/skills/implement-ticket/SKILL.md](.claude/skills/implement-ticket/SKILL.md), section "Ticket implementation: agent roles run automatically" below |
| Decisions the owner made, dated, with where each is implemented | [docs/owner-decisions.md](docs/owner-decisions.md) |
| UI rules and writing quality (binding) | [docs/ui-quality.md](docs/ui-quality.md) |
| Releases | [docs/RELEASING.md](docs/RELEASING.md) |

When a document and the code disagree once code exists, the code is the baseline and [docs/architecture.md](docs/architecture.md) records the difference. A ticket that changes a contract (scenario schema, replay schema, command line, caps) updates the document that states it in the same pull request.

## Stack and constraints (planned)

The PRD names the stack: "standard-library Python and plain JavaScript served from the same local origin" ([docs/PRD.md](docs/PRD.md), Scope). Neither document names a Python version or a package name; the defaults are Python 3.12 or newer and the package `warehouse_sim`, and ticket #2 confirms or changes them.

- Standard library only, in the application and in the tests (`unittest`). No pip or npm dependency, no build step, no framework, no CDN, font, image or script from another host.
- Local browser and CPU process only. The server binds `127.0.0.1`. No outgoing request from the server, the page or the tests. Browser checks run with external requests blocked ([docs/PRD.md](docs/PRD.md), WH-06).
- Deterministic: identical input, solver version and seed give identical canonical replay bytes. Integer ticks and coordinates, stable keys, stable arrays, canonical encoding ([docs/TECHNICAL_SPEC.md](docs/TECHNICAL_SPEC.md), "Replay and interface").
- Starting caps: 16 by 16 cells, 12 robots, 100 orders, 2,000 ticks, plus input-size and search-expansion caps whose numbers the tickets set. Raise a specific cap only in the scale experiment (WH-06), after measuring.
- Imported replay and scenario JSON is untrusted data. Validate schema and bounds before anything is rendered or run; show values through `textContent` or DOM nodes, never `innerHTML`, `eval` or inline script.
- Keyboard operation and visible focus for every control ([docs/TECHNICAL_SPEC.md](docs/TECHNICAL_SPEC.md), "Replay and interface").
- Synthetic data only: no physical devices, live inventory or customer data.
- Licence not selected ([README.md](README.md)). Do not add a `LICENSE` file or change licence wording without the owner.

## Setup, run and test commands (all planned)

Nothing below exists at this commit. Each command is introduced by the ticket named; until that ticket is merged, running it fails. Interpreter: `python` on Windows, `python3` on Linux.

| Purpose | Planned command | Introduced by |
|---|---|---|
| Run all tests | `python -m unittest` | planned: introduced by ticket WH-01a (sub-issue of #2) |
| Run one scenario and write a replay | `python -m warehouse_sim run <scenario.json> --out <replay.json>` | planned: introduced by ticket WH-01a (sub-issue of #2) |
| Fresh start: run a scenario and open the local browser view | `python -m warehouse_sim serve [scenario] [--port N] [--no-open]` (default scenario `scenarios/single-order.json`, default port 8780, `--port 0` picks a free port; runs the scenario, prints the URL and opens the browser unless `--no-open` is given; tests and checks use `--no-open`) | planned: introduced by ticket WH-01b (sub-issue of #2) |
| Validate a scenario against the schema and caps | `python -m warehouse_sim validate <scenario.json>` (exit 0 valid, 2 invalid) | planned: introduced by ticket WH-07 (new; issue number assigned when created) |
| Verify a replay independently | `python -m warehouse_sim.verify <replay.json>` (exit 0 accepted, 1 rejected with the first invalid tick) | planned: introduced by ticket #3 (WH-02) |
| Compare two assignment policies on a seeded workload | `python -m warehouse_sim compare --seed <n> ...` | planned: introduced by ticket #6 (WH-05) |
| Scale report | `python -m warehouse_sim scale ...` | planned: introduced by ticket #7 (WH-06) |

The exact flags are fixed by the ticket that introduces the command, then recorded here and in the README in the same pull request. Generated replays, run output and scale reports go to a scratch directory outside the repository (or under `runs/`, which ticket #2 adds to `.gitignore`); never commit them.

On Windows use `python` only. To hash a file: `python -c "import hashlib,sys;print(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest())" <file>` (instead of `sha256sum`). To read an exit code: `echo $?` in bash, `$LASTEXITCODE` in PowerShell.

## Architecture boundaries (planned)

Short form of the module map in [docs/architecture.md](docs/architecture.md). Package `warehouse_sim` (default name):

- `schema`, `canonical` and `limits`: versioned scenario and replay JSON, validation, canonical encoding, and every input cap in one place. No simulation logic.
- `engine`: tick loop, state, action-set validation and atomic commit, event emission in robot ID order. It does not plan routes.
- `scheduler`: job assignment, static reverse distances, time-expanded search, reservations, bounded replanning, blockage reasons. It proposes actions; only the engine commits them.
- `verify`: the independent checker. It reconstructs occupancy and job state from the scenario and the recorded events with its own rules and must not import `engine` or `scheduler`. A rule that changes in one is written again in the other on purpose; a shared helper would defeat the check.
- `workload`: seeded scenario generation. `server`: loopback HTTP and a fixed static allowlist, no simulation logic. `static/`: plain JavaScript page that talks to the server through documented routes only.
- `tests/` with `unittest`; fixtures under `tests/fixtures/` and included scenarios under `scenarios/`.

Rules every change must keep:

- A rejected action set changes nothing: the whole set is validated and committed together, or the previous snapshot stays.
- Tie-breaks are the ones in the technical specification (jobs by release tick then ID; robot by static distance then ID; search expansion order north, east, south, west, wait). No unordered iteration, wall-clock time or unseeded randomness in a run.
- Schema changes after ticket WH-01a bump the schema version and update the schema document, the verifier and the fixtures in the same pull request.
- A blocked run reports one of four reasons (static unreachable, search budget exhausted, no legal progress found, run limit reached) and the unfinished order IDs.

## Git workflow

- `main` is the default branch. Branch per ticket (`<issue-number>-<short-slug>`), pull request to `main`, small commits with a type prefix (`feat:`, `fix:`, `test:`, `docs:`, `chore:`).
- Only the owner merges and releases. Do not push to `main`, force-push or merge your own pull request. Do not push or open a pull request unless the owner asked in the current session; starting `/next-ticket` is that request for one ticket.
- Order for every ticket: local checks, Code Reviewer, Reality Checker, then a draft pull request that names the issue (`Part of #1`, `Closes #n`), then CI on that draft, then ready only when CI is green.
- Never commit `.env*`, generated replays or run output, or `.claude/state/`.
- Do not change `.claude/agents/`, `LOOP.md`, `loop-constraints.md` or `loop-budget.md` as part of a feature ticket.

## Evidence before a ticket is called done

Paste real output into the pull request description; do not summarise a run you did not make. None of this can be run before ticket WH-01a exists, and WH-01a creates the test command itself.

1. The output tail of `python -m unittest` from a clean checkout, with the Python version and the operating system, and the test count before and after.
2. For each acceptance criterion of the issue: the name of the test that proves it, or the exact command and what it printed. Fixtures in [docs/TECHNICAL_SPEC.md](docs/TECHNICAL_SPEC.md) are acceptance targets until a test reproduces them.
3. For a change to a replay: `python -m warehouse_sim.verify` on a replay produced by the change (after ticket #3), and the canonical hash of two runs with the same seed.
4. For a change under `static/`: a browser run on the local URL with the browser name and version, keyboard-only operation of the changed controls, and the console and network log free of errors and external requests. Browser automation is excluded by the dependency policy; the step is manual and listed under "Owner checks" in the pull request.
5. For a performance claim: the machine, the fixture size and the measured numbers, not an assertion.
6. `git status` free of stray files, and confirmation that no dependency, external URL or non-loopback listener was added.
7. Green CI on the pull request (Linux and Windows) with the run link. CI cannot be judged before the draft pull request exists, so the order is: local checks, Code Reviewer, Reality Checker, draft pull request, CI, then ready.
8. Anything not verified, said plainly.

## Ticket implementation: agent roles run automatically

When asked to implement, continue or finish a GitHub issue, follow the playbook in [`.claude/skills/implement-ticket/SKILL.md`](.claude/skills/implement-ticket/SKILL.md). Claude Code loads it on its own for ticket work; `/implement-ticket <issue number>` starts it by hand.

Delegate to the project subagents in `.claude/agents/` without waiting to be asked:

- **Before coding:** Software Architect, as their descriptions say.
- **While coding:** the implementing role that matches the files being changed.
- **After coding:** each specialist reviewer whose trigger matches the change.
- **On every ticket, before it is called done:** Code Reviewer, then Reality Checker.
- The session that wrote a change does not count as its reviewer.
- List the roles that ran and their verdicts in the pull request description under "Agent roles run".

Each role's `description` ends with a "Use proactively ..." sentence, which is what makes Claude Code delegate to it without being told.

## Delivery workflow

How a ticket gets from the backlog to a ready pull request. The files below hold the details; this part only points to them.

- **Start:** only the owner, with `/next-ticket [issue number]` ([`.claude/skills/next-ticket/SKILL.md`](.claude/skills/next-ticket/SKILL.md)). It is the go signal for one ticket, because the repository is used to train AI models. There is no scheduler. A `tracking` parent is never picked; only leaf sub-issues are work.
- **Playbook:** [`.claude/skills/implement-ticket/SKILL.md`](.claude/skills/implement-ticket/SKILL.md).
- **Review gate hook:** [`.claude/hooks/role_gate.py`](.claude/hooks/role_gate.py) blocks `gh pr create` and `gh pr ready` until Code Reviewer and Reality Checker ran after the last code edit; documentation-only changes pass. `ROLE_GATE=off` in the environment Claude Code is started from switches it off for that session. Self-test: `python .claude/hooks/role_gate.py --self-test`.
- **Permission rules:** [`.claude/settings.json`](.claude/settings.json). Documented commands are allowed; force pushes, pushes to `main`, `gh pr merge`, releases and reads of `.env` are denied; edits to `.github/`, agent configuration, `CLAUDE.md`, `AGENTS.md` and the Loop files ask first.
- **CI:** [`.github/workflows/ci.yml`](.github/workflows/ci.yml) runs on Linux and Windows. It must be green before a pull request is marked ready. Until ticket WH-01a creates the package, the test step is guarded by the existence of `warehouse_sim/__init__.py`; WH-01a removes the guard.
- **Pull request template:** [`.github/pull_request_template.md`](.github/pull_request_template.md). **Ticket template:** [`.github/ISSUE_TEMPLATE/implementation-ticket.md`](.github/ISSUE_TEMPLATE/implementation-ticket.md).
- **Labels:** `status:ready`, `status:blocked`, `status:in-progress`, `needs-decision`, `tracking`.
- **Changelog:** every ticket pull request adds a line under `Unreleased` in [CHANGELOG.md](CHANGELOG.md).
- **UI and copy:** UI tickets start with the `ui-ux-pro-max` skill and end with a check against [docs/ui-quality.md](docs/ui-quality.md); user-facing copy, docs and pull request text go through the `unslop` skill.
- **Merging and releasing:** only the owner. See [docs/RELEASING.md](docs/RELEASING.md) and [SECURITY.md](SECURITY.md).
- **Decisions:** [docs/owner-decisions.md](docs/owner-decisions.md). An agent that finds a recorded decision blocking a ticket stops and says so.
