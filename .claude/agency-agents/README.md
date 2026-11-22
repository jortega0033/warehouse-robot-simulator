# Agency Agents roles used in this repository

The Markdown files in `.claude/agents/` whose names start with `engineering-`, `security-` or `testing-` are copies of role definitions from Agency Agents. They are project-local Claude Code subagents. Loop Engineering files (see [`LOOP.md`](../../LOOP.md)) are not from Agency Agents.

## Source and licence

- Upstream: https://github.com/msitarzewski/agency-agents
- Pinned revision: `8ae6164602c95ca78828b148b9052460ee426885` (upstream `main`, committed 2026-11-09)
- Licence: MIT, "Copyright (c) 2025 AgentLand Contributors". The upstream licence text at the pinned revision is kept unchanged in [`LICENSE`](LICENSE) next to this file (SHA-256 `9a45258434d5cedf0af73c9ad4771373701225038d246c49219026c33677f66f`). It covers only the copied role files, not the rest of this repository.
- Fetched with `gh api -H "Accept: application/vnd.github.raw" "repos/msitarzewski/agency-agents/contents/<path>?ref=<revision>"`.

## Installed roles

"Upstream SHA-256" is the hash of the file as fetched at the pinned revision. Reviewer roles have one added frontmatter line, `tools: Read, Grep, Glob`, so they cannot edit files or run commands.

| File in `.claude/agents/` | `name:` | Upstream path | Upstream SHA-256 | Local change |
|---|---|---|---|---|
| `engineering-software-architect.md` | Software Architect | `engineering/engineering-software-architect.md` | `b85121691776147bacde26673e68fbbacd6a7f0816d1ca8e203c264d25ce1d30` | added `tools: Read, Grep, Glob` |
| `engineering-code-reviewer.md` | Code Reviewer | `engineering/engineering-code-reviewer.md` | `7509fcc3ea1dda46511b2801996305bf3d4a125576f9655ff0b63df25602f446` | added `tools: Read, Grep, Glob` |
| `security-appsec-engineer.md` | Application Security Engineer | `security/security-appsec-engineer.md` | `a19f0bda46f4adca5737365dbc3c7ed93e9d93b71349536d92ff055dcf4e3b83` | added `tools: Read, Grep, Glob` |
| `testing-accessibility-auditor.md` | Accessibility Auditor | `testing/testing-accessibility-auditor.md` | `362935907af23839775b9c6162f38c0c5a740542ab4350cb5c5b5a0d9f9a4268` | added `tools: Read, Grep, Glob` |
| `testing-performance-benchmarker.md` | Performance Benchmarker | `testing/testing-performance-benchmarker.md` | `16a841f67392d084b773c6d9f05341d093e9017f3e116f6df0de59a5a3f59c34` | added `tools: Read, Grep, Glob` |
| `testing-reality-checker.md` | Reality Checker | `testing/testing-reality-checker.md` | `6d32fcdb114233e13902ec6372d50293b120e85d490b5e81d372c29808f988a1` | added `tools: Read, Grep, Glob` |
| `engineering-backend-architect.md` | Backend Architect | `engineering/engineering-backend-architect.md` | `ac717bde4848d7663fff8a3c7edc711fd119256de6a7ce38c036619372f42c99` | none |
| `engineering-frontend-developer.md` | Frontend Developer | `engineering/engineering-frontend-developer.md` | `1ae4cc10b2e0163bd3ed921ad54080b865cd02e591becd8919b64b73fab06dad` | none |

## Why these roles

| Role | Use in this repository |
|---|---|
| Software Architect (read-only) | Check a ticket's design against the module boundaries in [`CLAUDE.md`](../../CLAUDE.md): engine, independent verifier, scheduler, replay schema, server and browser page. Planned, not implemented. |
| Code Reviewer (read-only) | Review a diff for correctness, determinism, verifier independence and the dependency policy. |
| Application Security Engineer (read-only) | Review the parts where untrusted JSON (imported replays and scenarios) and the local server meet: schema and bounds validation, size caps, no HTML sinks, loopback binding. |
| Accessibility Auditor (read-only) | Review keyboard operation, visible focus and the text table that mirrors the grid. The plan makes these requirements. |
| Performance Benchmarker (read-only) | Review the scale measurements and caps (16x16, 12 robots, 100 orders, 2,000 ticks, scale experiment to 200 robots): that they were measured on a stated machine and fixture, not asserted. |
| Reality Checker (read-only) | Compare claimed evidence with what was actually run before a ticket or the epic is called done. |
| Backend Architect | Implement the Python engine, scheduler, verifier, replay schema and local server. |
| Frontend Developer | Implement the plain JavaScript browser page. |

Most of these roles are written for larger stacks. Backend Architect, Frontend Developer and Performance Benchmarker mention frameworks, cloud services and load-testing tools; Application Security Engineer describes scanners and pipelines. In this repository the rules in [`CLAUDE.md`](../../CLAUDE.md) win: Python standard library only, plain JavaScript, no network.

Roles that were considered and left out: Test Automation Engineer (written for Playwright and Cypress, which the dependency policy rules out), Database Optimizer and Backend roles for storage (the product has no database), UI Designer and UX Architect (a single plain grid page; the UI rules are in `docs/ui-quality.md`).

## Name collision with user-level agents

A developer who has installed Agency Agents in `~/.claude/agents/` already has agents with the same `name:` values. Claude Code gives the project-level definition precedence, so inside this repository the copies here are used, including the read-only tool limits. The upstream names were kept on purpose so that the roles stay recognisable and can be compared with upstream.

A Claude Code session that was already running when these files were added keeps the definitions it loaded at start. Start a new session to pick up the project copies.

## Check that the roles load

From the repository root, in a new session:

```text
claude -p "List the project-level subagents defined in .claude/agents with the tools each one may use."
```

The six reviewer roles must report exactly `Read, Grep, Glob`.

## Updating

Fetch the same paths at a newer revision, re-apply the `tools:` line to the six reviewer roles, and update the revision and hashes in this file in the same commit.

## Local change: automatic delegation (2026-11-22)

One sentence beginning "Use proactively" was appended to the `description:` line of every Agency Agents role in `.claude/agents/` (not to `loop-verifier`). Claude Code uses that field to decide when to delegate, so the roles now run during ticket work without being named. Nothing else in the role files changed in that step.

This supersedes any statement above that a role file is unmodified or that the `tools:` line is the only local change. To compare a role with the pinned upstream file, remove that sentence (and the `tools:` line where one was added) first.

The steps at which each role runs are in `.claude/skills/implement-ticket/SKILL.md`.

A section headed "In this repository" was then inserted directly after the frontmatter of every Agency Agents role (not into `loop-verifier`), before the upstream text. It is project-specific text written for this repository, not upstream text. Because no application code exists yet, it describes the planned stack, modules and commands and says they are planned: the dependency policy that binds the role, what the role does here, its planned commands (or the output a read-only role must be given), a checklist of this project's rules with their sources, the parts of the generic text that do not apply, and what the role hands back. It ends with the sentence "This section and CLAUDE.md override the generic text below wherever they differ." The upstream text below it and the rest of the frontmatter are unchanged.

To compare a role with the pinned upstream file, remove three things first: the "Use proactively" sentence (in Backend Architect, Frontend Developer, Performance Benchmarker and Reality Checker also the full stop that was added in front of it, where the upstream description has none), the section "In this repository" together with the blank line after it, and the `tools:` line where one was added. Checked on 2026-11-22: with these three removed, each of the eight files has the upstream SHA-256 listed in the table above. Check the sections against the code once code exists; until then they describe a plan.

Verification, 2026-11-22: the headless `claude -p` loading check was not run in this preparation stage and is still to be done after the delivery tooling is installed. File structure was checked by reading the files: eight Agency Agents roles, each starting with "In this repository" after valid frontmatter, six with `tools: Read, Grep, Glob`.
