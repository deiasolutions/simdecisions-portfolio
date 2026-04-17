# TASK-181: Add file:selected bus event to TreeBrowserAdapter

## Objective
When user selects a file in filesystem adapter, emit `file:selected` bus event with file URI and metadata, following the same pattern as `channel:selected` for channels adapter.

## Context
TreeBrowserAdapter already handles onSelect for channels adapter and emits `channel:selected`. Add the same pattern for filesystem adapter to emit `file:selected` when a file node is clicked.

Existing pattern (from treeBrowserAdapter.tsx line 173-187):
```typescript
if (adapter === 'channels' && bus && node.meta?.channelId) {
  bus.send({
    type: 'channel:selected',
    sourcePane: paneId,
    target: '*',
    nonce: `${Date.now()}-${Math.random()}`,
    timestamp: new Date().toISOString(),
    data: { channelId, channelName, type },
  })
}
```

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\treeBrowserAdapter.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\types.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\filesystemAdapter.ts` (to see what meta fields are available)

## Deliverables
- [ ] In `handleSelect` callback (line ~170), add filesystem adapter case
- [ ] Check if `adapter === 'filesystem'` and node is a file (not directory)
- [ ] Emit `file:selected` bus event with data: `{uri, path, size, modified, created, extension}`
- [ ] Use same bus.send() pattern as channels adapter
- [ ] Only emit if node.meta.path exists (file selected, not directory)

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] Test that filesystem adapter emits `file:selected` on file click
- [ ] Test that filesystem adapter does NOT emit on directory click
- [ ] Test that bus event includes uri, path, size, modified, created
- [ ] Test that other adapters (channels, members) still work
- [ ] Minimum 4 new tests

## Constraints
- No file over 500 lines (treeBrowserAdapter.tsx is currently 235 lines)
- CSS: var(--sd-*) only (not applicable)
- No stubs
- Use existing bus interface (no type changes needed)
- Follow exact same pattern as channels adapter

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260316-TASK-181-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.
