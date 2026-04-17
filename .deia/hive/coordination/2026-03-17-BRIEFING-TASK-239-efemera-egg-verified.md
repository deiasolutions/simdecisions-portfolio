# BRIEFING: TASK-239 — Efemera EGG Verified

**From:** Q33NR
**To:** Q33N
**Date:** 2026-03-17
**Source:** Wave 4 Product Polish (4.11)

## Objective

Verify that the Efemera EGG (`eggs/efemera.egg.md`) renders correctly in the browser with all components working: channels sidebar, messages pane, compose terminal, and members list.

## Context

Efemera is the team chat product built on ShiftCenter's pane system. The backend and frontend are already implemented:

- **Backend:** `hivenode/efemera/store.py` (SQLite store) + `hivenode/efemera/routes.py` (8 API endpoints)
- **Frontend:**
  - `browser/src/primitives/tree-browser/adapters/channelsAdapter.ts` (channels tree)
  - `browser/src/primitives/tree-browser/adapters/membersAdapter.ts` (members tree)
  - `browser/src/services/efemera/relayPoller.ts` (relay poller for real-time updates)
- **EGG config:** `eggs/efemera.egg.md` (209 lines, defines the 4-pane layout)

The memory file confirms:
> "Efemera EGG (BL-101) — IMPLEMENTED"
> Tests: 29 backend (store + API), 7 frontend (channelsAdapter)

## What Q33N Must Do

1. **Write one task file** for a BEE to:
   - Load `?egg=efemera` in browser (manual or automated test)
   - Verify the 4-pane layout renders correctly per EGG spec
   - Verify channel selection → messages load in text-pane
   - Verify compose terminal sends via relay
   - Verify presence indicators show status
   - Fix any layout, data loading, or bus event issues
   - Run: `cd browser && npx vitest run` (confirm tests still pass)

2. **Task file requirements:**
   - Model: haiku (as specified in original task)
   - Deliverables: verification checklist + any fixes + test results
   - Test requirements: existing tests must continue passing, add tests if gaps found
   - Constraints: Rule 3 (CSS vars only), Rule 4 (500 line limit), Rule 6 (no stubs)

3. **Return task file to Q33NR** for review before dispatching the bee.

## Key Files for Q33N to Read

- `eggs/efemera.egg.md` — the EGG layout config
- `hivenode/efemera/store.py` — backend data store
- `hivenode/efemera/routes.py` — API endpoints
- `browser/src/primitives/tree-browser/adapters/channelsAdapter.ts` — channels tree adapter
- `browser/src/primitives/tree-browser/adapters/membersAdapter.ts` — members tree adapter
- `browser/src/services/efemera/relayPoller.ts` — relay poller

## Priority

P1 (Wave 4 product polish)

## Expected Outcome

One task file ready for Q33NR review, then dispatch to BEE (haiku).
