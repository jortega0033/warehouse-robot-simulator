# Design tokens

The visual system for this repository is the Pipenzo "Flow look" token file: a black page, Flow-style alpha layers, one accent (Pipenzo yellow `#FECE02`), and red only for danger. The owner chose it for every repository ([docs/owner-decisions.md](owner-decisions.md)).

## Source

`warehouse_sim/static/tokens.css` is a byte-for-byte copy of `extension/sidepanel/tokens.css` in `jortega0033/clip-to-reel-studio`, commit `a13378ce73e5b27213c9a200fc960ec93afef054` (2026-11-21). The header comment of the file holds the contrast checks and the yellow rule.

## Resync

Copy the file over `warehouse_sim/static/tokens.css`. Nothing else. Never edit the copy here; a change belongs in the source repository.

## Token names by role

- Surfaces: `--bg`, `--bg-raised`, `--surface`, `--bg-sunken`
- Text: `--fg`, `--muted`, `--faint`
- Lines and focus: `--border`, `--hairline`, `--control-border`, `--input-border`, `--focus`, `--ring-accent`
- Hero and ink panels: `--hero-bg`, `--on-hero`, `--on-hero-muted`, `--hero-chip-border`, `--hero-border`, `--hero-shadow`, `--ink`, `--on-ink`, `--on-ink-muted`, `--ink-border`
- Accent: `--primary`, `--primary-press`, `--primary-edge`, `--on-primary`
- Status: `--success`, `--ok`, `--ok-bg`, `--warn-fg`, `--warn-bg`, `--danger`, `--danger-bg`, `--info`
- Interaction layers: `--state-hover`, `--state-selected`, `--btn-secondary`, `--btn-secondary-border`, `--ink-hover`
- Overlays and media: `--glass*`, `--scrim`, `--on-media`, `--grad-*`, `--blur`, `--shadow-*`
- Type: `--font`, `--font-display`, `--mono`
- Shape, spacing and motion: `--space-1`, `--radius-*`, `--dur-1`, `--ease-out`, `--ease-in-out`

Some tokens (glass, blur, gradients, large shadows) exist in the source file but conflict with [docs/ui-quality.md](ui-quality.md) rules 3 and 4. Do not use them in this repository.

## Rule

New UI uses these tokens. No new colour literals in CSS or JavaScript. Canvas or inline colours are read with `getComputedStyle(document.documentElement).getPropertyValue('--token')`. Yellow is only for the primary action and the current step; red only for danger.

## Light and dark

Dark is the primary design. The `:root` block is the matching light theme. The dark values apply through the operating system colour scheme (`prefers-color-scheme`), with `color-scheme: light dark` set. There is no manual switch.

## Linking

Link `tokens.css` before any other stylesheet. The server's static allowlist (ticket #9, WH-01b) must include it, and its test must list it. The page ships from `warehouse_sim/static/`.
