# TASK-232: Expandable Terminal Input Verification

**Model:** Haiku
**Date:** 2026-03-17
**Priority:** P1
**Source Spec:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\specs\WAVE-4-PRODUCT-POLISH.md` (Task 4.4)

---

## Objective

Verify that the expandable terminal input feature works correctly and fix any visual issues found. The textarea should grow vertically, expand upward when content exceeds 3 lines, show proper shadow, and collapse on clear/submit.

---

## Context

This is Wave 4 Product Polish (BL-003), Task 4.4. The feature is already implemented:

- **TerminalPrompt.tsx** has auto-resize logic (lines 59-88) and expand-up mode tracking (lines 72-88)
- **TerminalApp.tsx** manages `inputExpanded` state (line 92) and passes it to TerminalPrompt (lines 213-215)
- **terminal.css** has expand-up CSS with absolute positioning and shadow (lines 268-278)
- **Existing tests** verify expand triggers at >3 lines and collapses on clear

**Known Issue:**
Line 277 of terminal.css uses `box-shadow: 0 -4px 12px var(--sd-shadow-lg);` which is INCORRECT. The variable `--sd-shadow-lg` already contains the full shadow definition (`0 8px 24px rgba(...)`), so the line should be just `box-shadow: var(--sd-shadow-lg);` with a negative offset if needed, or a custom value using the variable's color only.

---

## Files to Read First

1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\TerminalPrompt.tsx` — Auto-resize + expand-up logic
2. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\TerminalApp.tsx` — State management
3. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\terminal.css` — Expand-up CSS (lines 268-278)
4. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\__tests__\TerminalPrompt.expand.test.tsx` — Existing tests
5. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\__tests__\TerminalApp.expand.test.tsx` — Integration tests
6. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\shell-themes.css` — Shadow variable definitions (lines 113-117, 215-219, 326-330, etc.)

---

## Deliverables

### 1. Manual Verification
- [ ] Read the implementation files and existing tests
- [ ] Verify the logic matches the spec requirements:
  - Textarea grows vertically as user types multiple lines
  - Expand-up mode triggers at >3 lines (input lifts above prompt area)
  - Expand-up has proper shadow to separate from content
  - Collapses back to normal when content is cleared or submitted
  - Shift+Enter creates newlines, Enter submits
  - Scrollbar appears when content exceeds max-height (50vh)

### 2. Bug Fixes
- [ ] **Fix CSS shadow bug:** Change line 277 in `terminal.css` from `box-shadow: 0 -4px 12px var(--sd-shadow-lg);` to use the variable correctly (e.g., `box-shadow: var(--sd-shadow-lg);` or define a proper upward shadow)
- [ ] Fix any other visual issues found: jumpy resize, clipped text, focus loss
- [ ] Ensure all CSS uses `var(--sd-*)` only (Rule 3) — no hardcoded colors

### 3. Tests
- [ ] Review existing tests in `TerminalPrompt.expand.test.tsx` (8 tests already exist)
- [ ] Review existing tests in `TerminalApp.expand.test.tsx` (8 tests already exist)
- [ ] If the shadow fix changes behavior, add a new test verifying the CSS class is applied correctly
- [ ] Run: `cd browser && npx vitest run src/primitives/terminal/` — all tests must pass

---

## Test Requirements

- All 16 existing expand mode tests must still pass
- If new tests are added, they must verify:
  - CSS class `data-input-expanded="true"` is applied when expanded
  - Shadow styling is correct (no hardcoded colors)
- Test command: `cd browser && npx vitest run src/primitives/terminal/`

---

## Constraints

- **Rule 3:** NO HARDCODED COLORS. Only CSS variables (`var(--sd-*)`). Verify this in any CSS changes.
- **Rule 4:** No file over 500 lines.
- **Rule 5:** TDD. Tests first, then implementation (but verification tasks may discover issues that need fixing).
- **Rule 6:** NO STUBS. If something can't be fixed, report it clearly.

---

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260317-TASK-232-RESPONSE.md`

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

---

## Acceptance Criteria

From the briefing:

- [ ] Verify textarea grows vertically as user types multiple lines
- [ ] Verify expand-up mode triggers at >3 lines (input lifts above prompt area)
- [ ] Verify expand-up has proper shadow (`--sd-shadow-lg`) to separate from content
- [ ] Verify collapsing back to normal when content is cleared or submitted
- [ ] Verify Shift+Enter creates newlines, Enter submits
- [ ] Verify scrollbar appears when content exceeds max-height (50vh)
- [ ] Fix CSS shadow bug on line 277 of terminal.css
- [ ] Fix any other visual issues found
- [ ] Ensure all CSS uses `var(--sd-*)` only (Rule 3)
- [ ] All terminal tests pass

---

## Expected Outcome

After you complete:
- Terminal input expands/collapses smoothly
- Shadow uses CSS variables correctly (no hardcoded values)
- No visual glitches
- Tests verify the behavior
- All terminal tests pass (16+ expand tests + all other terminal tests)
- Response file documents what was verified and what (if anything) was fixed
