# TASK-054: SDEditor Process-Intake Mode

## Objective
Implement process-intake mode for SDEditor — renders like document mode but routes co-author rewrites to `to_ir` instead of `to_text`.

## Context
Process-intake mode is for structured data entry. It looks like document mode (markdown rendering, co-author overlay) but the LLM rewrite goes through a different routing path.

Current co-author flow:
1. User presses Enter
2. Paragraph sent to `bus.request('llm:rewrite', ...)`
3. Result rendered as text

Process-intake flow:
1. User presses Enter
2. Paragraph sent to `bus.request('llm:to_ir', ...)` instead
3. Result rendered as text (for now — IR generation is not built yet)

This is a **routing flag change**, not a visual change.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\SDEditor.tsx` (see handleTextareaKeyDown line 395)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\types.ts`

## Deliverables
- [ ] Update handleTextareaKeyDown in SDEditor.tsx — check `mode === 'process-intake'`
- [ ] If process-intake mode, call `bus.request('llm:to_ir', ...)` instead of `bus.request('llm:rewrite', ...)`
- [ ] For now, `llm:to_ir` returns text (same as rewrite) — IR generation is future work
- [ ] Add visual indicator in header when in process-intake mode (e.g., label shows "Process Intake" instead of "Text")
- [ ] Process-intake mode renders exactly like document mode otherwise

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All existing tests pass
- [ ] 4+ new tests in SDEditor.test.tsx:
  - Process-intake mode renders like document mode
  - Co-author in process-intake mode calls `llm:to_ir`
  - Document mode calls `llm:rewrite`
  - Header shows "Process Intake" label when in process-intake mode

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs
- Changes should be < 50 lines total

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia\hive\responses\20260313-TASK-054-RESPONSE.md`

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

## Dependencies
- Depends on TASK-050 (mode refactor)

## Notes for Bee
- This is a minimal change — just routing logic, no new UI
- The `llm:to_ir` handler doesn't exist yet — that's fine, it will be added later
- For testing, mock bus.request to handle `llm:to_ir` and return text
