# Owner decisions

A dated record of every decision the owner made for this repository, so the rules do not depend on anyone's memory of a conversation. All entries are dated 2026-11-22. Changing any entry needs the owner; an agent that finds a decision blocking a ticket stops and says so.

| # | Decision | Date | Implemented in |
|---|---|---|---|
| 1 | The instructions, tooling and playbook live on the default branch. | 2026-11-22 | `CLAUDE.md`, `.claude/`, `.github/` on `main` |
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

Entry 11 (Rust verified in CI only) does not apply: this project has no Rust. Numbering follows the owner's list so entries match other repositories.

## Entry 10: decisions settled with the ticket's default

The default applies until the owner says otherwise. Ticket numbers are GitHub issues in this repository; WH-07 and WH-08 are new tickets whose issue numbers are assigned when they are created.

| ID | Decision | Ticket(s) | Default applied |
|---|---|---|---|
| D1 | Minimum Python version and package name | #2 | Python 3.12 or newer, package `warehouse_sim` |
| D2 | Canonical encoding | #2 | JSON with sorted keys, separators `,` and `:`, ASCII-escaped, UTF-8, no BOM, no trailing newline; hashes are SHA-256 of those bytes |
| D3 | Tick numbering in reports | #2, #3 | A fault in the actions of tick t is reported at snapshot t+1 |
| D4 | Default server port | #2 | `--port` default 8780; `--port 0` picks a free port |
| D5 | Where replays are written | #2 | `--out` is required; `runs/` is git-ignored; checks use a scratch directory |
| D6 | Numbers the plan leaves open | WH-07, #4, #5 | Scenario file 256 KiB, replay file 8 MiB, 50,000 expansions per planning call, at most 3 alternate priority orders, checkpoint every 50 ticks |
| D7 | Verifier reason codes | #3 | `same_cell_collision`, `edge_swap`, `wall_traversal`, `out_of_bounds`, `bad_move_distance`, `drop_without_pickup`, `missing_action`, `duplicate_action`, `summary_mismatch`, `checkpoint_mismatch` |
| D8 | How the blocked reason is chosen | WH-08 | Unreachable only gives static unreachable; search budget if any search hit the cap in the qualifying ticks, else no legal progress; tick cap gives run limit |
| D9 | Random numbers for workloads | #6 | A small own integer generator, not `random`, so seeds match on every Python version and OS |
| D10 | Scale steps and budget | #7 | 12, 25, 50, 100, 200 robots; 10 minutes per step; defaults unchanged, recommendation only |
| D11 | Browser checks | #2, #5, #7 | Manual and recorded; no automation dependency |
| D12 | Licence | none | Stay unselected; no `LICENSE` file is added |
| D13 | JavaScript tests | #2, #5 | None; the page renders server snapshots and logic stays in Python |
| D14 | Play interval | #5 | 500 ms per tick, Space toggles |
