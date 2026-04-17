# TASK-043A: Extract useAttachment.ts from useTerminal.ts (File Size Fix)

## Objective
Extract all file attachment logic from `useTerminal.ts` (707 lines) into a new `useAttachment.ts` hook. This is a Rule 4 violation fix — no file over 500 lines.

## Context
TASK-043 added typing indicator + attachment button features. The bee was explicitly told to extract attachment logic to `useAttachment.ts` but ignored the instruction and added everything to `useTerminal.ts`, pushing it from 588 → 707 lines. The attachment features work correctly — this task only extracts them to a separate file.

**DO NOT change any behavior.** This is a pure refactor. All 18 TASK-043 tests must continue to pass.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\useTerminal.ts` (707 lines — target: ≤620 after extraction)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\types.ts` (FileAttachment interface)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\__tests__\fileAttachment.test.ts` (7 tests)

## Deliverables

- [ ] Create `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\useAttachment.ts`:
  - Move `MAX_FILE_SIZE`, `ALLOWED_EXTENSIONS` constants from useTerminal.ts
  - Move `handleFileSelect()` function
  - Move `removeAttachment()` function
  - Move `formatPromptWithAttachment()` logic (the code that prepends file content to prompt text)
  - Move `attachment` and `attachmentError` state
  - Export as `useAttachment()` hook returning `{ attachment, attachmentError, handleFileSelect, removeAttachment, formatPromptWithAttachment }`
- [ ] Modify `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\useTerminal.ts`:
  - Import `useAttachment` from `./useAttachment`
  - Call `const { attachment, attachmentError, handleFileSelect, removeAttachment, formatPromptWithAttachment } = useAttachment()`
  - In `handleSubmit()`: use `formatPromptWithAttachment(text)` instead of inline attachment logic
  - Remove the extracted constants, functions, and state
  - **Target: ≤620 lines after extraction**
- [ ] Update `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\__tests__\fileAttachment.test.ts` if imports change

## Test Requirements
- [ ] All 7 fileAttachment tests pass
- [ ] All 5 typingIndicator tests pass
- [ ] All 15 useTerminal tests pass
- [ ] All 16 TerminalOutput tests pass
- [ ] Full browser suite: no regressions
- [ ] **Zero behavioral changes** — this is extraction only

## Constraints
- No file over 500 lines
- No behavioral changes — pure refactor
- No new features
- All existing tests must pass unchanged (import path changes allowed)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260313-TASK-043A-RESPONSE.md`

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
