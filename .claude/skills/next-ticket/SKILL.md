---
name: next-ticket
description: Take the next ready ticket of epic #1 up to a ready pull request. Only the owner starts it; starting it is the go signal for one ticket.
argument-hint: "[issue number]"
disable-model-invocation: true
---

# Next ticket

The owner starts this driver with `/next-ticket` or `/next-ticket <issue number>`. Starting it is the go signal: this repository is used to train AI models, so no ticket work happens without it. There is no scheduler. One ticket per run. The driver never merges, never releases and never starts another run by itself. Only the owner merges.

The ticket itself is done with the playbook [`implement-ticket`](../implement-ticket/SKILL.md). `CLAUDE.md` holds the commands, boundaries, Git workflow and evidence rules; where this file and `CLAUDE.md` differ, `CLAUDE.md` wins. Decisions already made are in `docs/owner-decisions.md`.

Labels: `status:ready`, `status:blocked`, `status:in-progress`, `needs-decision`, `tracking`. The epic is issue #1. Its table is authoritative for dependency order.

## Which ticket is work

- Big tickets are split into sub-issues of 1 to 4 hours, one pull request each. A ticket labelled `tracking`, or with open sub-issues, is a container: this driver never picks it.
- Only a leaf ticket is work. The order is the order of the parents in the epic's table, then the order of the sub-issues inside each parent.
- An explicit issue number that is a `tracking` parent is refused. Print the list of its open sub-issues and stop.

## Steps

1. **Refresh the queue.** `gh issue list` for the epic's children.
   - A `status:blocked` ticket whose blockers are all closed becomes `status:ready` (remove `status:blocked`).
   - A parent whose sub-issues are all closed is closed with a comment that names the last sub-issue. A ticket with no sub-issues is never closed by this step.
2. **Pick.** With an issue number, use it, after checking that it is a leaf, open, `status:ready` and not `needs-decision`. Without one, take the first `status:ready` leaf ticket in the epic's order that is not `status:in-progress` and not `needs-decision`. If none qualifies, say why (blocked, decision open, queue empty) and stop.
3. **Claim.** Label it `status:in-progress` and remove `status:ready`.
4. **Worktree.** `git fetch origin`, then create a fresh worktree and a branch named `<issue-number>-<short-slug>` from `origin/main`. All work happens there. Never work on `main`.
5. **Implement.** Run the `implement-ticket` playbook for the ticket, delegating to the project subagents at its steps. Settle an open owner decision with the ticket's stated default and say so in the pull request; where a ticket states none, take the conservative option and flag it in the issue. An agent that finds a decision in `docs/owner-decisions.md` blocking the ticket stops and says so. Do not change agent configuration (`.claude/agents/`, `.claude/skills/`, `.claude/hooks/`, `.claude/settings.json`, `.claude/agency-agents/`), `LOOP.md` or the Loop files in a ticket. CI changes only where the ticket names them (ticket #2 removes the guard in `.github/workflows/ci.yml`); that edit asks first.
6. **Gates, in this order** (CI cannot be judged before it exists):
   1. Local checks pass (the documented test command and every other documented check). Record each command and its output.
   2. Write the review files (below), then run Code Reviewer, then Reality Checker, on the full diff and the recorded evidence. Reality Checker checks that the documented checks were run locally and passed and that CI is configured to run them; it does not need a CI result.
   3. Only then `git push -u origin <branch>` and `gh pr create --draft`. The gate hook allows it because both roles ran after the last code edit.
7. **Wait for CI without polling.** After the push and the draft pull request, bind the pull request to this session when the app offers it (the desktop app's pull request tools) and end the turn with the line "Draft pull request #N is waiting for CI". Do not loop, sleep or watch. When the session is woken (a CI event from the app, or the owner says "continue"), read `gh pr checks <n>` once:
   - green: go to step 8;
   - red: fix, re-run the local checks and both gates, push, and end the turn with the same line;
   - still running: end the turn with the same line again.
8. **Ready.** When CI is green, `gh pr ready <n>` (the hook checks the gates again) and comment on the issue with the CI run link and the pull request link. Green CI is a condition checked here, not by Reality Checker.
9. **Close parents.** If this ticket is the last open sub-issue of a parent, its pull request body says `Closes #<sub-issue>` and `Closes #<parent>`, so the owner's merge closes both. Otherwise it says `Part of #<parent>` and `Closes #<sub-issue>`. Every pull request also says `Part of #1`.
10. **Stop.** Report the pull request link, the evidence, the "Owner checks" list and anything not verified. Do not merge and do not start the next ticket.

## Diff files for the read-only reviewers

Code Reviewer and Reality Checker have no shell. Before calling them, write these files in the ticket worktree's `.claude/state/review/` (that folder is git-ignored) and name them in the request:

- `git diff --stat origin/main...HEAD` as `diff-stat.txt`
- `git diff origin/main...HEAD` as `diff.patch`
- the output of every check you ran, as `checks.txt`, with the command, Python version and operating system

## Steps that need a person

A criterion that needs a person ("by hand in a normal browser", "manual, recorded") is done as far as an agent can (a scripted run with its evidence), and the rest is listed under "Owner checks" in the pull request. Reality Checker accepts that only when the ticket marks the step as manual. Browser automation is excluded by the dependency policy, so the browser steps of this project are manual.

## Ask rules at any depth

Edits to agent configuration, skills, hooks, `.claude/settings.json` and `.claude/agency-agents/` ask first at any depth, so also in a ticket worktree. Edits to `.github/`, `CLAUDE.md`, `AGENTS.md`, `LOOP.md`, `loop-constraints.md` and `loop-budget.md` ask first only at the project root (the rules in `.claude/settings.json` anchor them there), so in a ticket worktree they may not ask: a ticket that edits one of them (WH-01a edits the CI guard, README and `CLAUDE.md`) says so in the pull request and the owner reviews those files. Edits made through a shell command are not covered by that rule, so the playbook forbids changing agent configuration in a ticket.
