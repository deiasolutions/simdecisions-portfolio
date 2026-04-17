# BRIEFING: Pane Chrome Options — Pin, Collapse, Configurable Close

**From:** Q33NR (REGENT-QUEUE-TEMP-2026-03-15-1615-SPE)
**To:** Q33N (Queen Coordinator)
**Date:** 2026-03-15
**Spec:** SPEC-w2-04-pane-chrome-options
**Priority:** P0.74999
**Model Assignment:** Sonnet

---

## Objective

Add three new EGG-configurable pane chrome options to the shell primitive:
- `chromeClose` (boolean) — show/hide close X button on pane header
- `chromePin` (boolean) — show pin toggle button; when pinned, pane stays visible and sibling pane collapses
- `chromeCollapsible` (boolean) — pane can collapse to thin vertical icon strip (~34px wide) with expand button

These options are declared per-pane in EGG layout config and read by shell pane renderer.

---

## Context from Q88N

Backlog reference: BL-151 (supersedes BL-024 and BL-025)

This feature adds granular control over pane chrome behavior on a per-pane basis. Different panes need different affordances:
- Some panes should not have close buttons (e.g., primary terminal)
- Some panes can be pinned to take full width temporarily
- Some panes can collapse to a thin strip when not in use

All three options are configurable in the EGG layout config and passed to the shell pane renderer.

---

## Key Files (Likely Touched)

Based on codebase structure, these files will likely be involved:

### EGG Schema & Inflation
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\specs\SPEC-EGG-SCHEMA-v1.md` — schema docs
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\eggs\eggInflater.ts` — EGG inflation logic
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\eggToShell.ts` — EGG layout → shell config conversion

### Shell Components
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\Shell.tsx` — pane rendering
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\shell.css` — pane chrome styles

### New Files (likely needed)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\PaneChrome.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\__tests__\PaneChrome.test.tsx`

---

## Acceptance Criteria (from Spec)

- [ ] EGG schema supports `chromeClose`, `chromePin`, `chromeCollapsible` per pane
- [ ] eggInflater reads and passes chrome options to shell panes
- [ ] PaneChrome component renders optional close X, pin toggle, collapse toggle
- [ ] Pin toggle: when active, sibling pane collapses; pane gets full width
- [ ] Collapse: pane shrinks to ~34px vertical icon strip with expand button
- [ ] Collapsed strip shows pane icon (from EGG config) and expand arrow
- [ ] Expand button restores pane to previous size
- [ ] All chrome buttons use `var(--sd-*)` CSS variables only
- [ ] Tests written and passing (TDD)
- [ ] Existing browser tests still pass

---

## Constraints (Hard Rules)

- Max 500 lines per file
- TDD: tests first
- No stubs or TODOs
- CSS: `var(--sd-*)` only (Rule 3)
- All file paths must be absolute in task files
- POST heartbeats to http://localhost:8420/build/heartbeat every 3 minutes with JSON:
  `{"task_id": "2026-03-15-1615-SPEC-w2-04-pane-chrome-options", "status": "running", "model": "sonnet", "message": "working"}`
- File claim system: POST to http://localhost:8420/build/claim before modifying files

---

## Your Task (Q33N)

1. **Read the relevant files first** — examine existing shell structure, pane chrome, EGG schema
2. **Write task files** for bees to `.deia/hive/tasks/`
3. **Return task files to Q33NR for review** — do NOT dispatch bees yet
4. **After Q33NR approval**, dispatch bees using dispatch.py

Break this work into bee-sized chunks:
- Backend/schema changes (if needed for EGG schema extensions)
- Frontend component work (PaneChrome component)
- Integration work (eggInflater, eggToShell, Shell.tsx)
- Test coverage

Consider dependencies:
- Schema/type changes must happen before component work
- Components can be built in parallel if types are ready
- Integration tests depend on all components being complete

---

## Model Assignment

Assign based on complexity:
- **Haiku:** Simple, isolated, well-defined tasks (e.g., update schema docs)
- **Sonnet:** Medium complexity, multiple file changes, integration work
- **Opus:** Complex architectural changes (not expected for this spec)

---

## Notes

- The spec references "sibling pane" for pin behavior — this likely means the adjacent pane in a split layout
- Collapsed state is ~34px wide — verify this matches existing shell layout constraints
- Icon in collapsed strip comes from EGG config — ensure pane icon is accessible in collapse state
- Previous size restoration on expand — may need to track pane width state

---

**End of Briefing**
