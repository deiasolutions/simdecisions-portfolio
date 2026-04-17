# TASK-243: Global Commons Phase A — Static Content (W5 — 5.4)

## Objective
Create the static content for Global Commons at deiasolutions.org: the Federalist Papers (DEIA founding documents), design tokens reference, and ethics.yml defaults.

## Context
Wave 5 Ship. Global Commons is the public-facing documentation and governance reference for DEIA. Phase A is static content only — no dynamic features. This is what makes the constitutional framework visible and auditable by anyone.

## Source Spec
`docs/specs/WAVE-5-SHIP.md` — Task 5.4

## Files to Read First
- `.deia/config/ethics.yml` — Ethics configuration (the source of truth)
- `.deia/config/carbon.yml` — Carbon budget configuration
- `.deia/config/grace.yml` — Grace period configuration
- `browser/src/shell/shell-themes.css` — Design token definitions

## Deliverables
- [ ] Create `docs/global-commons/` directory with:
  - `index.md` — What is DEIA? What is Global Commons? Links to all documents
  - `ethics.md` — Ethics framework rendered from ethics.yml (human-readable version)
  - `design-tokens.md` — All `--sd-*` CSS variables documented with descriptions and default values
  - `carbon.md` — Carbon budget framework rendered from carbon.yml
  - `governance.md` — How the constitutional framework works: ethics → governance → execution
- [ ] Each document should be clean markdown, suitable for static site generation
- [ ] Include a `docs/global-commons/README.md` with build/deploy instructions
- [ ] Content must be factual — derived from actual config files, not invented

## Priority
P2

## Model
sonnet
