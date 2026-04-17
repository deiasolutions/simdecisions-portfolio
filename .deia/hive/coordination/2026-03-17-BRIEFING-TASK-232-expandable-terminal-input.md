# BRIEFING: TASK-232 — Expandable Terminal Input Verification

**From:** Q33NR
**To:** Q33N
**Date:** 2026-03-17
**Priority:** P1
**Model Assignment:** Haiku

---

## Objective

Verify that the expandable terminal input feature works correctly. The textarea should:
- Grow vertically as user types multiple lines
- Expand upward when content exceeds 3 lines (input lifts above prompt area)
- Show proper shadow (`--sd-shadow-lg`) in expand-up mode
- Collapse back to normal when content is cleared or submitted
- Support Shift+Enter for newlines, Enter for submit
- Show scrollbar when content exceeds max-height (50vh)

Fix any visual issues (jumpy resize, clipped text, focus loss) and add tests to verify the behavior.

---

## Context

This is Wave 4 Product Polish (BL-003), Task 4.4 from `docs/specs/WAVE-4-PRODUCT-POLISH.md`.

According to the spec:
- TerminalPrompt.tsx already has auto-resize logic (min 22px, max 200px) at lines 59-88
- Expand-up mode triggers at >3 lines
- CSS support exists in terminal.css with absolute positioning, max-height 50vh, and box shadow (lines 268-278)

The task is to VERIFY everything works smoothly and FIX any issues found.

---

## Source Spec

`docs/specs/WAVE-4-PRODUCT-POLISH.md` — Task 4.4

---

## Files to Reference

**Primary files:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\TerminalPrompt.tsx` — Auto-resize logic (lines 59-88)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\terminal.css` — Expand-up CSS (lines 268-278)

**Test location:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\__tests__\` — Add test file here

---

## Deliverables

Q33N should create a task file for a BEE to:

1. **Manual verification:**
   - [ ] Verify textarea grows vertically as user types multiple lines
   - [ ] Verify expand-up mode triggers at >3 lines (input lifts above prompt area)
   - [ ] Verify expand-up has proper shadow (`--sd-shadow-lg`) to separate from content
   - [ ] Verify collapsing back to normal when content is cleared or submitted
   - [ ] Verify Shift+Enter creates newlines, Enter submits
   - [ ] Verify scrollbar appears when content exceeds max-height (50vh)

2. **Bug fixes (if any):**
   - [ ] Fix any visual issues found: jumpy resize, clipped text, focus loss
   - [ ] Ensure all CSS uses `var(--sd-*)` only (Rule 3)

3. **Tests:**
   - [ ] Add test: expand triggers at correct line count (>3 lines)
   - [ ] Add test: collapse on clear/submit
   - [ ] Run: `cd browser && npx vitest run src/primitives/terminal/`

---

## Constraints

- **Rule 3:** NO HARDCODED COLORS. Only CSS variables (`var(--sd-*)`). Verify this in any CSS changes.
- **Rule 4:** No file over 500 lines.
- **Rule 5:** TDD. Tests first, then implementation (but verification tasks may discover issues that need fixing).
- **Rule 6:** NO STUBS. If something can't be fixed, report it clearly.

---

## Test Requirements

- New tests must be added to verify:
  - Expand-up triggers at correct threshold (>3 lines)
  - Collapse on clear/submit
- All existing terminal tests must still pass
- Test command: `cd browser && npx vitest run src/primitives/terminal/`

---

## Q33N Instructions

1. Read the source spec: `docs/specs/WAVE-4-PRODUCT-POLISH.md` (Task 4.4)
2. Read the implementation files listed above
3. Create ONE task file for a BEE (haiku model)
4. Task file should include:
   - Objective (verify + fix)
   - Files to read first (absolute paths)
   - Deliverables (verification steps + bug fixes + tests)
   - Test requirements
   - Response requirements (8 sections)
5. Return to Q33NR for review BEFORE dispatching the BEE

---

## Expected Outcome

After BEE completes:
- Terminal input expands/collapses smoothly
- No visual glitches
- Tests verify the behavior
- All terminal tests pass
- Response file documents what was verified and what (if anything) was fixed
