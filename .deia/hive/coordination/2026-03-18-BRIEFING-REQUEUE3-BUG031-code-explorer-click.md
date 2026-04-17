# BRIEFING: BUG-031 (REQUEUE 3) — Code Explorer Click Returns Bad Request

**To:** Q33N (Queen Coordinator)
**From:** Q33NR (Regent)
**Date:** 2026-03-18
**Priority:** P0

## Objective

Fix the Code EGG file explorer so clicking a file loads its content instead of showing "Error loading file Bad Request URI".

## Background

This bug has been attempted 4 times total. Fix cycle on attempt 3 failed due to `_active/` path reference bug (now fixed by separate spec). **The fix is KNOWN** — just needs to be applied to source code.

## Root Cause (Confirmed Across Prior Attempts)

`treeBrowserAdapter.tsx` sends `file:selected` bus events without:
1. A `name` field (SDEditor expects `message.data.name`)
2. A protocol prefix on the URI (backend `/storage/read` expects `home://path` format)

## Exact Fix Required

In `browser/src/apps/treeBrowserAdapter.tsx`, find where `file:selected` events are sent and change:

```typescript
// BEFORE (broken):
bus.send({
  type: 'file:selected',
  data: { uri: 'README.md', path: 'README.md', size: 1024 }
})

// AFTER (fixed):
const protocol = (paneConfig as any).protocol || 'home://'
const uri = `${protocol}${path}`
bus.send({
  type: 'file:selected',
  data: { uri, path, name: node.label, size: 1024 }
})
```

## Files to Read First

- `browser/src/apps/treeBrowserAdapter.tsx` — the file that needs modification
- `browser/src/primitives/text-pane/SDEditor.tsx` — to verify what fields it expects from `file:selected`
- `hivenode/routes/storage_routes.py` — to confirm URI format expected by backend

## Deliverables

- [ ] treeBrowserAdapter.tsx sends `name` field in file:selected events
- [ ] treeBrowserAdapter.tsx constructs URI with protocol prefix (e.g. `home://path`)
- [ ] Directory clicks do NOT trigger file:selected (only files)
- [ ] Tests for file:selected event data (name, uri format)

## Acceptance Criteria

- [ ] Clicking a file in Code explorer loads its content
- [ ] No "Error loading file" or "Bad Request URI" message
- [ ] All new tests pass
- [ ] No regressions in existing tree-browser tests

## Smoke Test Commands

```bash
cd browser && npx vitest run --reporter=verbose src/apps/__tests__/
cd browser && npx vitest run --reporter=verbose src/primitives/tree-browser/
cd browser && npx vitest run --reporter=verbose src/primitives/text-pane/
```

## Constraints (10 Hard Rules Apply)

- No file over 500 lines
- CSS: var(--sd-*) only (no hardcoded colors)
- No stubs or TODOs
- TDD: tests first, then implementation
- MUST modify source code (treeBrowserAdapter.tsx), not just tests
- All file paths must be absolute in task files

## Model Assignment

**Sonnet** — This is a known fix that needs precision implementation.

## Task File Requirements

Write ONE task file to `.deia/hive/tasks/` with:
- Absolute file paths in "Files to Read First"
- Specific test scenarios to implement
- Clear acceptance criteria from the spec
- The 8-section response file requirement

Return the task file to me for review BEFORE dispatching any bees.
