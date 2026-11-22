# AGENTS.md

The full repository instructions are in [CLAUDE.md](CLAUDE.md). This file repeats only what an agent needs before it reads that.

## Status

Planning only. There is no application code yet, so no build, run or test command works at this commit. The planned commands are listed in [CLAUDE.md](CLAUDE.md), each with the ticket that introduces it. The first one, `python -m unittest`, appears with ticket #2.

## Stack

Planned: Python standard library and plain JavaScript, no pip or npm dependency, loopback only. See [CLAUDE.md](CLAUDE.md), "Stack and constraints".

## Ticket work

To implement a GitHub issue, follow the steps in [.claude/skills/implement-ticket/SKILL.md](.claude/skills/implement-ticket/SKILL.md) and the section "Ticket implementation: agent roles run automatically" in [CLAUDE.md](CLAUDE.md). The role files in `.claude/agents/` each start with a section "In this repository" that holds the project rules for that role. An agent that cannot delegate to those roles does the before-coding, while-coding and specialist steps itself and says so in the pull request. The agent that wrote the change cannot pass the review and acceptance gates: if the gates could not run, do not push or open the pull request; report that in the issue comment and leave the run for the owner.

## Loop conventions

- The loop runs at L1: report-only, started by hand. It proposes; it does not label, comment, close, edit source, push or merge.
- No scheduler and no loop workflow is installed. Do not add one without the owner's approval.
- See [LOOP.md](LOOP.md) for the manual command and the human gates.
