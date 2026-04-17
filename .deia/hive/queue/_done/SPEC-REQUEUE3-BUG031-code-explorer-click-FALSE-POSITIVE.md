# BUG-031 (RE-QUEUE 3): Code explorer click returns "Error loading file Bad Request URI"

## Background — Why Re-Queued
Attempted 4 times total. Fix cycle on attempt 3 failed due to _active/ path reference bug (now fixed). The fix is KNOWN — just needs to be applied to source code.

## Objective
Fix the Code EGG file explorer so clicking a file loads its content instead of showing "Error loading file Bad Request URI".

## Root Cause (confirmed across prior attempts)
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

## Files to Modify
- `browser/src/apps/treeBrowserAdapter.tsx` — add name field + protocol prefix to file:selected event

## Files to Read First
- `browser/src/apps/treeBrowserAdapter.tsx`
- `browser/src/primitives/text-pane/SDEditor.tsx` (to see what fields it expects)
- `hivenode/routes/storage_routes.py` (to confirm URI format expected)

## Deliverables
- [ ] treeBrowserAdapter.tsx sends `name` field in file:selected events
- [ ] treeBrowserAdapter.tsx constructs URI with protocol prefix (e.g. `home://path`)
- [ ] Directory clicks do NOT trigger file:selected
- [ ] Tests for file:selected event data (name, uri format)

## Acceptance Criteria
- [ ] Clicking a file in Code explorer loads its content
- [ ] No "Error loading file" or "Bad Request URI" message
- [ ] All new tests pass
- [ ] No regressions in existing tree-browser tests

## Smoke Test
- [ ] `cd browser && npx vitest run --reporter=verbose src/apps/__tests__/`
- [ ] `cd browser && npx vitest run --reporter=verbose src/primitives/tree-browser/`
- [ ] `cd browser && npx vitest run --reporter=verbose src/primitives/text-pane/`

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs
- MUST modify source code (treeBrowserAdapter.tsx), not just tests

## Model Assignment
sonnet

## Priority
P0
