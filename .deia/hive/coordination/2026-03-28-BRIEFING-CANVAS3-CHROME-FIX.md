# BRIEFING: Fix canvas3 Chrome Primitives

**From:** Q33NR
**To:** Q33N
**Date:** 2026-03-28
**Priority:** P0

## Context

canvas3.egg.md loads but has three chrome issues:

1. **TopBar shows redundant currencies** — the currency chip displays clock/coin/carbon which are already in the status-bar. Fix: set `showCurrencyChip: false` in canvas3.egg.md config. Also the TopBar layout is squished left — everything piles up on the left side instead of spreading across the bar. The spacer comes AFTER the currency chip, but with currencies gone, check if the layout is correct: hamburger | brand | spacer | kebab | avatar. Brand should be left, kebab+avatar should be right.

2. **MenuBarPrimitive is the old MenuBar ported** — it was literally copy-pasted from the legacy MenuBar.tsx (the file says "Ported from MenuBar.tsx (594 lines)"). It has unicode emoji buttons, the dropdown z-index is wrong (menus pop up BEHIND the main stage content), and it looks/behaves like the old component. We need to find if there's a NEWER version anywhere — check git history, stash, branches, the platform repo. If no newer version exists, the current one needs z-index fixes at minimum.

3. **TopBar CSS** — read TopBar.css and check if the layout is using flexbox correctly. The bar should stretch full width with items spaced properly.

## Your Mission

### Part 1: Fix canvas3.egg.md

Edit `eggs/canvas3.egg.md`:
- Set `showCurrencyChip: false` in the top-bar config
- Set `appName: "SimDecisions Canvas"` in the top-bar config (keep this)
- Set `showBreadcrumb: true` in the top-bar config (keep this)

### Part 2: Investigate MenuBarPrimitive

Search for a newer/better version of the menu bar:

1. **Check git log** for any commits that touched `browser/src/primitives/menu-bar/` — is there a newer version that was written and then lost/overwritten?
2. **Check git stash** — `git stash list` then check if any stash has a different MenuBarPrimitive
3. **Check the platform repo** — look in `C:\Users\davee\OneDrive\Documents\GitHub\platform\` for any menu-bar component that's different from this one
4. **Check other branches** — `git branch -a` and look for any chrome-related branches
5. **Read the ADR** — `docs/specs/ADR-SC-CHROME-001-v3.md` — what does it say the menu-bar should look like?

Report what you find. If there's no newer version, report that clearly.

### Part 3: Fix MenuBar z-index

Regardless of whether a newer version exists, fix the dropdown z-index issue:

1. Read `browser/src/primitives/menu-bar/MenuBarPrimitive.css`
2. The menu dropdowns need `z-index` high enough to render ABOVE all pane content. Pane content renders in `.shell-body`. The menu dropdown needs to be above that.
3. Look at what z-index values are used elsewhere — check `browser/src/shell/components/Shell.tsx` or any constants file for Z_LAYERS
4. Set the menu dropdown z-index to be above pane content (at least 100, probably higher)

### Part 4: Fix TopBar CSS

1. Read `browser/src/primitives/top-bar/TopBar.css`
2. Verify the bar uses `display: flex` with proper spacing
3. The layout should be: `[hamburger] [brand] ---- spacer ---- [kebab] [avatar]`
4. If the CSS is wrong, fix it

### Part 5: Run tests and verify

1. Run `npx vitest run menu-bar` from browser/
2. Run `npx vitest run top-bar` from browser/
3. Run `npx vitest run eggToShell` from browser/
4. Report all results

## Deliverable

Write to: `.deia/hive/responses/20260328-CANVAS3-CHROME-FIX.md`

Include:
1. canvas3.egg.md changes made
2. MenuBar investigation results — is there a newer version anywhere?
3. MenuBar z-index fix details
4. TopBar CSS fix details (if needed)
5. Test results
6. What the ADR says about menu-bar design

## Constraints

- You MAY edit: `eggs/canvas3.egg.md`, `browser/src/primitives/menu-bar/MenuBarPrimitive.css`, `browser/src/primitives/top-bar/TopBar.css`
- You MAY edit: `browser/src/primitives/menu-bar/MenuBarPrimitive.tsx` ONLY for z-index fixes (inline styles)
- You MUST NOT rewrite MenuBarPrimitive.tsx from scratch — just fix z-index
- You MUST NOT edit any other source files
- Read the ADR before making changes

## Model Assignment

Sonnet — investigation + CSS fixes + egg edit.
