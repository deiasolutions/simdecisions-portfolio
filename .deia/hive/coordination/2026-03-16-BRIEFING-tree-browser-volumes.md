# BRIEFING: Wire tree-browser to real volume storage

**Date:** 2026-03-16
**From:** Q33NR
**To:** Q33N
**Spec:** 2026-03-16-1032-SPEC-w2-07-tree-browser-volumes
**Model Assignment:** sonnet
**Priority:** P1.15

---

## Objective

Wire the tree-browser component to the real volume storage backend. The `home://` protocol should list actual directories and files from the volume system. When a user selects a file in the tree-browser, its contents should load in the text-pane. File metadata (size, date) should display correctly.

---

## Context from Q88N

This is part of Wave 2 frontend wiring. The volume storage backend already exists. The tree-browser UI exists. The missing piece is connecting them.

The spec requires:
- `home://` lists real directories from volume storage
- File contents load in text-pane when selected
- File metadata (size, date) displayed
- Tests written first (TDD)
- No stubs
- Max 500 lines per file
- CSS: `var(--sd-*)` only

---

## Relevant Components

### Backend (likely already exists)
- Volume storage system: `hivenode/volumes/` or similar
- Volume registry and routes
- File read endpoints

### Frontend (exists, needs wiring)
- Tree-browser component: `browser/src/primitives/tree-browser/`
- Volume adapter: `browser/src/primitives/tree-browser/adapters/volumeAdapter.ts` (may need creation)
- Text-pane component: `browser/src/primitives/text-pane/`
- Bus events for file selection

### Integration points
- Tree-browser emits `file:selected` bus event
- Text-pane listens for `file:selected` and fetches content
- Volume adapter fetches directory listings from backend API
- Volume adapter fetches file content from backend API

---

## Constraints

1. **TDD:** Tests first, implementation second
2. **No stubs:** Every function fully implemented
3. **Max 500 lines per file:** Modularize if approaching limit
4. **CSS variables only:** `var(--sd-*)` — no hardcoded colors
5. **File claims:** Use build monitor's file claim system to avoid conflicts with parallel bees
6. **Heartbeats:** POST to `http://localhost:8420/build/heartbeat` every 3 minutes with task status

---

## Files to Investigate First

Before writing task files, Q33N should read:

**Backend:**
- `hivenode/volumes/` (or wherever volume storage lives)
- Volume-related routes (search for `/api/volumes` or similar)
- Volume registry configuration

**Frontend:**
- `browser/src/primitives/tree-browser/TreeBrowser.tsx`
- `browser/src/primitives/tree-browser/adapters/` (existing adapters)
- `browser/src/primitives/tree-browser/types.ts`
- `browser/src/primitives/text-pane/` (file loading logic)
- `browser/src/infrastructure/relay_bus/` (bus event system)

**Tests:**
- `browser/src/primitives/tree-browser/__tests__/`
- Any existing volume adapter tests

---

## Acceptance Criteria (from spec)

- [ ] `home://` lists real directories
- [ ] File contents load in text-pane
- [ ] File metadata (size, date) displayed
- [ ] Tests written and passing

---

## Smoke Test

```bash
cd browser && npx vitest run src/primitives/tree-browser/
```

No new test failures.

---

## Your Task, Q33N

1. **Investigate the codebase** — read the files listed above
2. **Identify gaps** — what exists vs what needs to be built
3. **Write task files** — one per bee-sized unit of work
4. **Return to Q33NR for review** — do NOT dispatch bees yet

Each task file must include:
- Objective (one sentence)
- Context (relevant file paths, interfaces, contracts)
- Files to Read First (absolute paths)
- Deliverables (concrete, testable outputs)
- Test Requirements (TDD, edge cases, pass counts)
- Constraints (500 lines, CSS vars, no stubs)
- Response Requirements (8-section template)

---

## Notes

- The volume system likely already has backend routes. Don't rebuild what exists.
- The tree-browser likely already has adapter infrastructure. Follow the pattern.
- The text-pane likely already has file loading logic. Wire it to volume storage.
- The relay_bus likely already handles file selection events. Use existing bus events.

If anything is missing from the backend (unlikely), create a separate task for backend work.

---

**End of Briefing**
