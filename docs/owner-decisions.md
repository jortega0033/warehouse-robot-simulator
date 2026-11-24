# Owner decisions

A dated record of every decision the owner made for this repository, so the rules do not depend on anyone's memory of a conversation. Entries are dated 2026-11-22 unless the date column says otherwise. Changing any entry needs the owner; an agent that finds a decision blocking a ticket stops and says so.

| # | Decision | Date | Implemented in |
|---|---|---|---|
| 1 | The instructions, tooling and playbook live on the default branch. | 2026-11-22 | `CLAUDE.md`, `.claude/`, `.github/`; on the default branch (`main`) once the owner merges the preparation pull request |
| 2 | Persona agents run automatically during ticket work and carry instructions tailored to this project. | 2026-11-22 | `.claude/agents/` ("In this repository" sections and "Use proactively" descriptions), `.claude/skills/implement-ticket/SKILL.md`, `.claude/agency-agents/README.md` |
| 3 | Every open ticket is about app implementation; tooling is installed, not ticketed. | 2026-11-22 | Epic #1 and its sub-issues; tooling files listed in this table |
| 4 | Agents may take a ticket up to a ready pull request. Only the owner merges and releases. | 2026-11-22 | `.claude/skills/next-ticket/SKILL.md`, `.claude/settings.json` (deny rules), `CLAUDE.md` "Git workflow", `docs/RELEASING.md` |
| 5 | No scheduler. Ticket work starts only on the owner's go signal (`/next-ticket`), because the repository is used to train AI models. | 2026-11-22 | `.claude/skills/next-ticket/SKILL.md` (`disable-model-invocation: true`), `LOOP.md` |
| 6 | A review gate hook blocks opening or readying a pull request until the gate roles have run after the last code edit. | 2026-11-22 | `.claude/hooks/role_gate.py`, `.claude/settings.json` (`hooks`) |
| 7 | Loop Engineering stays at L1, report-only and unscheduled. | 2026-11-22 | `LOOP.md`, `loop-constraints.md`, `loop-budget.md` |
| 8 | Continuous integration runs on Linux and Windows; the default branch requires a pull request and green checks. | 2026-11-22 | `.github/workflows/ci.yml`; branch protection is set on GitHub by the owner's orchestration, not in a file |
| 9 | Permission rules: documented commands are allowed; force pushes, pushes to the default branch, merges, releases and reads of secrets are denied; edits to CI, agent configuration and Loop files ask first. | 2026-11-22 | `.claude/settings.json` (`permissions`) |
| 10 | Open decisions on tickets are settled with the ticket's stated default. The list is below. | 2026-11-22 | The tickets named below |
| 12 | The ten UI rules in `docs/ui-quality.md` are binding, and the `ui-ux-pro-max` and `unslop` skills are installed in the repository and used for UI work and for copy. | 2026-11-22 | `docs/ui-quality.md`, `.claude/skills/ui-ux-pro-max/`, `.claude/skills/unslop/`, `.claude/skills/implement-ticket/SKILL.md` |
| 13 | Visual system: Pipenzo Flow look tokens (docs/design-tokens.md). SDLC kit version: jortega0033/sdlc-kit v1.0.0. | 2026-11-23 | `docs/design-tokens.md`, `warehouse_sim/static/tokens.css` |
| 14 | UI token rules, decided 2026-11-23. The labels 14-D1 to 14-D5 are separate from the D1 to D16 of entry 10. 14-D1 Current selection: the yellow accent is used for the primary action, the current-step marker and the current selection (UI rule 8); decided by the owner. How (recommended by the orchestrator, adopted under the owner's delegation of the same day): a selection uses a solid `--primary` fill with `--on-primary` text (not only a yellow border, which has about 1.5:1 against white on light), plus a second sign that is not colour (weight, icon or text) and the existing aria attribute; never a tint with a same-hue border and never a thick one-sided border. 14-D2 Focus ring: `--focus` is a focus indicator, exempt from the accent limit, including where it is yellow in dark; a ticket that says the focus style stays unchanged means the rule on main after the token pull request (recommended by the orchestrator, adopted under the owner's delegation of 2026-11-23). 14-D3 Themes: contrast and no-colour-alone checks cover both the light and the dark block of `tokens.css` (same source). 14-D4 Linking: a ticket that creates a page or its static allowlist links `tokens.css` before any other stylesheet and serves it (allowlist and its test) (same source). 14-D5 release-dependency-planner: while a plan is open only one yellow primary button shows; "New plan" (`#new-plan`) becomes neutral, in ticket `jortega0033/release-dependency-planner#11` (same source; applies to that repository, recorded here for the shared rule set). | 2026-11-23 | `docs/design-tokens.md`, `docs/ui-quality.md` |

Entry 11 (Rust verified in CI only) does not apply: this project has no Rust. Numbering follows the owner's list so entries match other repositories.

## Entry 10: decisions settled with the ticket's default

The default applies until the owner says otherwise. Ticket numbers are GitHub issues in this repository; the new tickets are WH-01a #8, WH-01b #9, WH-07 #10, WH-03a #11, WH-03b #12, WH-04a #13, WH-04b #14, WH-08a #15, WH-08b #16 and WH-09 #17; the older ones are WH-01 #2, WH-02 #3, WH-03 #4, WH-04 #5, WH-05 #6 and WH-06 #7; the epic is #1 (#2, #4 and #5 become `tracking` parents of the sub-issues that carry their names).

| ID | Decision | Ticket(s) | Default applied |
|---|---|---|---|
| D1 | Minimum Python version and package name | WH-01a | Python 3.12 or newer, package `warehouse_sim` |
| D2 | Canonical encoding | WH-01a | JSON with sorted keys, separators `,` and `:`, ASCII-escaped, UTF-8, no BOM, no trailing newline; hashes are SHA-256 of those bytes |
| D3 | Tick numbering in reports | WH-01a, #3 | A fault in the actions of tick t is reported at snapshot t+1 (the PRD's "collision at tick 2") |
| D4 | Default server port | WH-01b | `--port` default 8780; `--port 0` picks a free port |
| D5 | Where replays are written | WH-01a (`run`), WH-01b (`serve` keeps the replay in memory) | `--out` is required; `runs/` is git-ignored; checks use a scratch directory |
| D6 | Numbers the plan leaves open | WH-01a (constants), WH-07, WH-03b, WH-09 | Scenario file 256 KiB, replay file 8 MiB, 50,000 expansions per planning call, at most 3 alternate priority orders, checkpoint every 50 ticks |
| D7 | Verifier reason codes | #3, WH-09 (`checkpoint_mismatch`) | `same_cell_collision`, `edge_swap`, `wall_traversal`, `out_of_bounds`, `bad_move_distance`, `drop_without_pickup`, `missing_action`, `duplicate_action`, `summary_mismatch`, `checkpoint_mismatch` |
| D8 | How the blocked reason is chosen | WH-08a | Planning calls end `route`, `no_route` or `cap_hit`; a goal held by a non-moving robot (defined in D15) or an exhausted planning horizon is `no_route`, never budget exhaustion. At termination: tick cap gives `run_limit_reached`; at the no-progress termination `search_budget_exhausted` if any planning call in the qualifying ticks ended `cap_hit`, else `no_legal_progress`; when only statically unreachable jobs remain, `static_unreachable` |
| D9 | Random numbers for workloads | #6 | A small own integer generator, not `random`, so seeds match on every Python version and OS |
| D10 | Scale steps and budget | #7 | 12, 25, 50, 100, 200 robots; 10 minutes per step; defaults unchanged, recommendation only |
| D11 | Browser checks | WH-01b, WH-04b, WH-08b, #7 | Manual and recorded; no automation dependency (it would break the dependency policy) |
| D12 | Licence | none | Stay unselected; no `LICENSE` file is added |
| D13 | JavaScript tests | WH-01b, WH-04b | None; the page renders server snapshots and logic stays in Python |
| D14 | Play interval | WH-04b | 500 ms per tick, Space toggles |
| D15 | Planning horizon and non-moving robots | #4 (WH-03a, WH-03b) | Horizon: static distance from start to goal plus 20 ticks (`horizon_slack` 20), recorded in the replay search settings. A robot is non-moving when it has no job, its plan has ended, or it ended `no_route` or `cap_hit` in the current planning round; a lower-priority robot that is not yet planned in the round is not non-moving and is ignored by higher-priority searches. When a robot ends `no_route` or `cap_hit` and an earlier plan of the same round enters its cell, the round is repeated with that robot non-moving, until no earlier plan enters the cell of a non-moving robot; then at most `alternate_bound` (default 3) alternate priority orders are tried and the result with strictly fewer stalled robots is kept |
| D16 | `serve` launch behaviour | WH-01b | `serve [scenario] [--port N] [--no-open]`; default scenario `scenarios/single-order.json`; opens the browser unless `--no-open`; replay kept in memory |

## Program decisions (owner, 2026-11-24)

The owner accepted the goal and each suggestion below. They apply from the phase they name; the rules of `CLAUDE.md` hold for phase 1 as written.

| Decision | Implemented in |
|---|---|
| The repository has a program goal above phase 1: a warehouse digital twin, in six phases. | Program issue #27 |
| The rule standard-library Python limits 1,000-robot planning. Suggested: allow a compiled planner core from the optimal planning phase. | Program issue #27 |
| Benchmark maps have their own licences. Suggested: fetch at a pinned version, commit none. | Program issue #27 |
