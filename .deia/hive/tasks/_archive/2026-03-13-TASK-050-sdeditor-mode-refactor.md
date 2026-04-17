# TASK-050: SDEditor Mode System Refactor

## Objective
Refactor SDEditor's mode system to consolidate the dual mode/renderMode props into a single `mode` prop with 5 values, laying foundation for multi-mode editing.

## Context
SDEditor currently has two overlapping mode concepts:
- `renderMode?: 'chat' | 'code'` (external prop)
- `mode: RenderMode = 'rendered' | 'raw'` (internal state)

This causes confusion. The spec requires a single `mode` prop with 5 values:
- `document` (default, replaces "rendered")
- `raw` (plain text)
- `code` (syntax highlighting)
- `diff` (diff view)
- `process-intake` (document mode but routes to `to_ir`)

**This task:** Refactor the type system and state management to support the new mode structure. Do NOT implement the new visual modes yet — just prepare the types and routing logic.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\SDEditor.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\types.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\__tests__\SDEditor.test.tsx`

## Deliverables
- [ ] Update `SDEditorProps` in `types.ts` — replace `renderMode?: 'chat' | 'code'` with `mode?: 'document' | 'raw' | 'code' | 'diff' | 'process-intake' | 'chat'`
- [ ] Add `defaultMode?: 'document' | 'raw' | 'code' | 'diff' | 'process-intake' | 'chat'` prop (defaults to `'document'`)
- [ ] Remove internal `RenderMode` type — use the single mode string
- [ ] Update all internal `renderMode === 'chat'` checks to `mode === 'chat'`
- [ ] Update all internal `mode === 'rendered'` checks to `mode === 'document'`
- [ ] Add toolbar mode toggle dropdown (replaces current Raw/Preview button) — shows all 6 modes, highlights current mode
- [ ] Update keyboard shortcut Cmd+Shift+M to cycle through modes instead of toggle rendered/raw
- [ ] Preserve all existing functionality — chat mode, code mode, co-author, undo/redo

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All existing SDEditor tests pass
- [ ] 8+ new tests:
  - Mode prop defaults to 'document'
  - Mode toggle dropdown shows all 6 modes
  - Switching mode updates state
  - Chat mode still works
  - Code mode still works
  - Keyboard shortcut cycles modes
  - Process-intake mode renders like document
  - Diff mode renders (even if placeholder for now)

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs — if a mode doesn't have visual rendering yet, render as document mode with a warning label

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia\hive\responses\20260313-TASK-050-RESPONSE.md`

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

## Model Assignment
haiku

## Notes for Bee
- This is a refactor, not a feature add. Visual modes come in TASK-051.
- Focus on type safety and state management.
- All 6 modes should be selectable, but raw/diff/process-intake can render as document mode with a label until TASK-051.
