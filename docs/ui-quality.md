# UI quality rules

Binding rules for every screen and every piece of user-facing copy in this repository. The owner stated rules 1 and 2 and approved rules 3 to 10 on 2026-11-22 ([docs/owner-decisions.md](owner-decisions.md), entry 12). They are enforced by the review gate: Code Reviewer checks every ticket against this file. Rule 1 can be linted; rule 2 cannot be detected reliably from CSS, so a reviewer reads the screen.

1. No thick accent border on one side of a card, callout, alert, list item or quote (for example `border-left: 4px solid <accent>`). Use spacing, type weight, an icon or a full hairline border instead.
2. No soft tinted background with a thin border of the same hue as the default way to mark a status, tag, callout or card. One neutral surface and one clear signal (text, icon or a solid chip) is enough.
3. No gradient text and no purple-to-blue gradient as a default accent.
4. No blur or glass panels, and no drop shadow plus large radius on every card.
5. No emoji used as icons or bullets, and no sparkle marks.
6. No pill or badge on things that are not states. No all-caps, letter-spaced micro labels as section decoration.
7. No centred hero with a slogan in an application screen. Screens open on the user's task.
8. One accent colour, used for the primary action and the current selection. Status colours only for status.
9. Dense, aligned layouts on a consistent spacing scale. No card grid where a table or a list is the right form.
10. User-facing copy is plain and specific: no filler, no exclamation marks, and the same word for the same thing everywhere.

## How the rules are applied

- A UI ticket starts with the `ui-ux-pro-max` skill (design-system search for the product type: `python .claude/skills/ui-ux-pro-max/scripts/search.py "<query>" --design-system`) and ends with a check of the changed screens against this file.
- User-facing copy, documentation and pull request text go through the `unslop` skill before the pull request is opened.
- The project's own constraints still apply: plain HTML, CSS and JavaScript from the local server, no framework, no external font, image or script, keyboard operation and visible focus ([CLAUDE.md](../CLAUDE.md), "Stack and constraints"). Where a skill suggests a framework, CDN or web font, this repository's rules win.
- This product is a simulator view: a grid, a robot table, an order table, run status, timeline controls and an error panel. A table is the right form for the order and robot state; do not turn it into cards.
- Colours, type, radii and motion come from the design tokens in [docs/design-tokens.md](design-tokens.md); do not add colour literals.
