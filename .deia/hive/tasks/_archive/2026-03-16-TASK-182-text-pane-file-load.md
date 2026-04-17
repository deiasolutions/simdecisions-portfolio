# TASK-182: Wire text-pane to load file content on file:selected bus event

## Objective
When text-pane receives `file:selected` bus event, fetch file content from `/storage/read?uri=${uri}` and load it into the editor, following the same pattern as `channel:selected` for chat mode.

## Context
Text-pane (SDEditor.tsx) already listens for `channel:selected` bus events when in chat mode. Add similar handling for `file:selected` to load file content when user clicks a file in tree-browser.

Existing pattern (SDEditor.tsx line 283):
```typescript
if (message.type === 'channel:selected' && mode === 'chat') {
  // Handle channel selection
}
```

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\SDEditor.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\__tests__\SDEditor.test.tsx` (for test patterns)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\storage_routes.py` (for /storage/read endpoint contract)

## Deliverables
- [ ] Add bus subscription for `file:selected` event in SDEditor
- [ ] When `file:selected` received, fetch content from `/storage/read?uri=${event.data.uri}`
- [ ] Load content into editor (update value state)
- [ ] Show loading indicator while fetching
- [ ] Handle errors (404, 500) gracefully with error message in editor
- [ ] Auto-detect language from file extension (use existing logic if present)
- [ ] Update read-only status based on mode (files are editable unless mode='markdown-readonly')

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] Test that `file:selected` event triggers fetch to `/storage/read`
- [ ] Test that file content loads into editor value
- [ ] Test that 404 shows error message
- [ ] Test that loading indicator appears during fetch
- [ ] Test that language is auto-detected from extension (.ts → typescript, .md → markdown, etc.)
- [ ] Test that existing `channel:selected` still works (no regression)
- [ ] Minimum 6 new tests

## Constraints
- No file over 500 lines (SDEditor.tsx is currently ~450 lines)
- CSS: var(--sd-*) only
- No stubs
- Use HIVENODE_URL from import.meta.env.VITE_HIVENODE_URL
- Reuse existing fetch patterns from codebase
- Error messages should be user-friendly (not raw HTTP errors)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260316-TASK-182-RESPONSE.md`

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
