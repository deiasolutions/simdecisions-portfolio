# BRIEFING: BL-956 — FAB EGG Discovery

**From:** Q33NR (regent)
**To:** Q33N (coordinator)
**Date:** 2026-03-25
**Model Assignment:** sonnet
**Priority:** P1

---

## Objective

EmptyPane FAB currently uses a hardcoded `APP_REGISTRY` array (6 apps in `constants.ts`). Replace this with dynamic EGG discovery from the `eggs/` directory. When a user selects a full app EGG, show a 3-choice prompt: load into this pane, fill the entire screen, or add to a new tab. Applets and primitives spawn directly without prompting.

---

## Context

### Current State

**EmptyPane.tsx** (lines 42-66):
- Filters `APP_REGISTRY` by category ('app', 'applet', 'primitive')
- Checks `listRegisteredApps()` to filter runtime-registered renderers
- For category='app' in single-pane mode: shows `window.confirm()` then navigates to `?egg=<eggId>`
- For all other cases: dispatches `SPAWN_APP` directly

**APP_REGISTRY** (constants.ts lines 65-91):
- Hardcoded array of 6 apps, 2 applets, 5 primitives
- Each entry: `{ appType, label?, category, eggId?, accepts? }`
- Apps have `eggId` field (e.g., `eggId: 'chat'`)

**EGG Discovery Infrastructure:**
- 20+ EGG files exist in `eggs/` directory (chat.egg.md, code.egg.md, sim.egg.md, etc.)
- `getEggRegistry()` in `browser/src/eggs/index.ts` returns `EggRegistry` (currently empty with TODO comments)
- `useEggManifest()` in `browser/src/eggs/useEggManifest.ts` extracts apps from EGG layout
- EGG files have YAML front-matter with `egg`, `displayName`, `description`, `defaultRoute`
- Vite plugin `serveEggs()` serves `*.egg.md` from repo-level `eggs/` directory

### What Needs to Change

1. **Populate getEggRegistry()** — Import all `*.egg.md` files and inflate them into the registry. Remove TODO comments.

2. **FAB Dynamic Discovery** — Replace `APP_REGISTRY.filter()` with a query to the EGG registry. Derive category from EGG metadata or layout structure:
   - **category='app'**: full EGG layouts (multi-pane apps like chat, code, sim)
   - **category='applet'**: multi-primitive bundles (kanban, apps-home)
   - **category='primitive'**: single primitives (terminal, text-pane, tree-browser)

3. **App Load Prompt** — When user clicks an app (category='app'), show a dialog:
   > "[DisplayName] is a full screen app. Do you want to load it into this pane, fill the entire screen, or add it to a new tab?"

   Three buttons:
   - **This pane** — dispatch `SPAWN_APP` with the app's primary appType
   - **Full screen** — navigate to EGG URL (`?egg=<eggId>`)
   - **New tab** — dispatch `ADD_TAB` then `SPAWN_APP`

4. **Keep applets/primitives as-is** — They spawn directly via `SPAWN_APP`, no prompt.

---

## Files to Review

**Key files (absolute paths):**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\EmptyPane.tsx` (206 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\constants.ts` (lines 65-91, APP_REGISTRY)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\eggs\index.ts` (119 lines, getEggRegistry)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\eggs\useEggManifest.ts` (80 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\eggs\parseEggMd.ts` (EGG parser)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\eggs\eggInflater.ts` (inflation logic)

**EGG files to import (20 total):**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\*.egg.md`

**Related:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\reducer.ts` (SPAWN_APP, ADD_TAB actions)

---

## Constraints

1. **Do NOT remove APP_REGISTRY** — Keep it as a fallback for category/label metadata if needed
2. **CSS variables only** — `var(--sd-*)`, no hardcoded colors (Rule 3)
3. **Dialog via portal** — Render to `.hhp-root` (same as ContextMenu)
4. **TDD** — Write tests first (Rule 5)
5. **File size limit** — 500 lines, hard limit 1,000 (Rule 4)
6. **No stubs** — Fully implement (Rule 6)
7. **Absolute paths** — All file paths in task files must be absolute (Rule 8)

---

## Test Requirements (minimum 9 tests)

1. FAB menu shows all EGGs from registry, not just hardcoded 6
2. Clicking an app shows 3-choice prompt dialog
3. "This pane" dispatches `SPAWN_APP` with correct appType
4. "Full screen" navigates to correct EGG URL
5. "New tab" dispatches `ADD_TAB` then `SPAWN_APP`
6. Clicking an applet spawns directly without prompt
7. Clicking a primitive spawns directly without prompt
8. Dialog closes on Escape key
9. Dialog renders via portal to `.hhp-root`

---

## Acceptance Criteria

- [ ] `getEggRegistry()` imports all 20+ EGG files and returns populated registry
- [ ] FAB discovers available EGGs dynamically from the EGG registry
- [ ] App selection shows a 3-choice prompt: this pane, full screen, new tab
- [ ] Prompt dialog text includes the app's display name
- [ ] "This pane" option dispatches `SPAWN_APP` into current pane
- [ ] "Full screen" option navigates to EGG URL (`?egg=<eggId>`)
- [ ] "New tab" option creates a tab and spawns the app there
- [ ] Applets and primitives still spawn directly without prompt
- [ ] All 9+ tests passing
- [ ] No hardcoded colors — CSS variables only
- [ ] No file exceeds 500 lines

---

## Deliverables

Q33N should produce:

1. **Task file(s)** for bee(s) to implement this feature
2. **Test plan** specifying which test files, how many tests, edge cases
3. **File modularization plan** if any file would exceed 500 lines
4. **Response file requirements** — all 8 sections per P-07

---

## Next Steps

1. Q33N reads this briefing
2. Q33N reads the key files listed above
3. Q33N writes task file(s) to `.deia/hive/tasks/`
4. Q33N returns to Q33NR for review
5. Q33NR reviews task files against mechanical checklist
6. Q33NR approves dispatch
7. Q33N dispatches bee(s)

---

## Notes

- The EGG infrastructure already exists — just needs wiring
- 20+ EGG files already exist in `eggs/` directory
- Vite plugin already serves `*.egg.md` files
- `parseEggMd()` and `inflateEgg()` already exist
- The main work: import EGGs into registry + wire FAB to use it + add prompt dialog
- This is a medium-sized task — likely 1-2 bees (registry population + FAB update)

---

**Q33N: Read the files above, write task file(s), return for review. Do NOT dispatch bees yet.**
