# Design tokens

The visual system for this repository is the Pipenzo "Flow look" token file: a black page, Flow-style alpha layers, one accent (Pipenzo yellow `#FECE02`), and red only for danger. Yellow marks the primary action, the current step and the current selection. The owner chose it for every repository ([docs/owner-decisions.md](owner-decisions.md)).

## Source

`warehouse_sim/static/tokens.css` is a byte-for-byte copy of `extension/sidepanel/tokens.css` in `jortega0033/clip-to-reel-studio`, commit `a13378ce73e5b27213c9a200fc960ec93afef054` (2026-11-21). The header comment of the file holds the contrast checks and the yellow rule. That comment is narrower than the rules below: it lists yellow uses of the source product and does not name the current selection or the focus ring. The copy must stay identical to the source, so the comment cannot be changed here. Where this document differs from any comment in `tokens.css`, including the inline comments on `--primary` and `--state-selected`, this document takes precedence.

## Resync

Copy the file over `warehouse_sim/static/tokens.css` (the source commits LF line endings; git handles the working-copy endings, so the committed blob must equal the source blob). Nothing else. Never edit the copy here; a change belongs in the source repository.

## Token names by role

- Surfaces: `--bg`, `--bg-raised`, `--surface`, `--bg-sunken`
- Text: `--fg`, `--muted`, `--faint`
- Lines and focus: `--border`, `--hairline`, `--control-border`, `--input-border`, `--focus`, `--ring-accent`
- Hero and ink panels: `--hero-bg`, `--on-hero`, `--on-hero-muted`, `--hero-chip-border`, `--hero-border`, `--hero-shadow`, `--ink`, `--on-ink`, `--on-ink-muted`, `--ink-border`
- Accent: `--primary`, `--primary-press`, `--primary-edge`, `--on-primary`
- Status: `--success`, `--ok`, `--ok-bg`, `--warn-fg`, `--warn-bg`, `--danger`, `--danger-bg`, `--info`
- Interaction layers: `--state-hover`, `--state-selected`, `--btn-secondary`, `--btn-secondary-border`, `--ink-hover`. `--state-selected` does not mark the current selection; that is a solid `--primary` fill with `--on-primary` text (see "Current selection").
- Overlays and media: `--glass*`, `--scrim`, `--on-media`, `--grad-*`, `--blur`, `--shadow-*`
- Type: `--font`, `--font-display`, `--mono`
- Shape, spacing and motion: `--space-1`, `--radius-*`, `--dur-1`, `--ease-out`, `--ease-in-out`

Some tokens (glass, blur, gradients, large shadows) exist in the source file but conflict with [docs/ui-quality.md](ui-quality.md) rules 3 and 4. Do not use them in this repository.

## Rule

New UI uses these tokens. No new colour literals in CSS or JavaScript. Canvas or inline colours are read with `getComputedStyle(document.documentElement).getPropertyValue('--token')`. Yellow is only for the primary action, the current step and the current selection (UI rule 8 in [docs/ui-quality.md](ui-quality.md)); red only for danger. The focus ring is covered under "Focus ring" below.

## Current selection

The owner decided on 2026-11-23 that the yellow accent is used for the primary action, the current-step marker and the current selection. How it is drawn is a recommendation by the orchestrator, adopted under the owner's delegation of the same day:

- A selection uses a solid `--primary` fill with `--on-primary` text. A yellow border alone is not enough: it has about 1.5:1 against white on light.
- A second sign that is not colour: weight, an icon or text.
- The existing aria attribute (for example `aria-selected`, `aria-current` or `aria-pressed`). A new control needs the matching aria attribute.
- Never a tint with a same-hue border, and never a thick one-sided border (UI rules 1 and 2).

Status: there is no page yet (`warehouse_sim/static/` holds only `tokens.css`), so nothing marks a selection today. The rule applies when ticket work (#9 and later UI tickets) adds one.

## Focus ring

`--focus` is a focus indicator and is exempt from the accent limit, including where it is yellow in dark. A ticket that says the focus style stays unchanged means the rule on main after the token pull request. Recommended by the orchestrator, adopted under the owner's delegation of 2026-11-23.

## Light and dark

Dark is the primary design. The `:root` block is the matching light theme. The dark values apply through the operating system colour scheme (`prefers-color-scheme`), with `color-scheme: light dark` set. There is no manual switch.

Contrast checks and no-colour-alone checks cover both the light block and the dark block of `tokens.css`; a pair that passes in one theme is not assumed to pass in the other. Recommended by the orchestrator, adopted under the owner's delegation of 2026-11-23.

## Linking

Link `tokens.css` before any other stylesheet. A ticket that creates a page or the static allowlist links `tokens.css` before any other stylesheet and serves it: the allowlist includes it and the allowlist test lists it (ticket #9, WH-01b, is the first such ticket). Recommended by the orchestrator, adopted under the owner's delegation of 2026-11-23. The page ships from `warehouse_sim/static/`.
