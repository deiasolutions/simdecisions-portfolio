# BRIEFING: BL-065 SDEditor Multi-Mode Verify and Fix

**To:** Q33N (Queen Coordinator)
**From:** Q88NR-bot (Regent)
**Date:** 2026-03-18
**Spec:** `2026-03-17-SPEC-TASK-BL065-sdeditor-multi-mode.md`

---

## Objective
Verify and fix the SDEditor (text-pane) multi-mode system: raw, preview, diff, code, and process-intake modes all work correctly.

---

## Context

The SDEditor component at `browser/src/primitives/text-pane/SDEditor.tsx` supports 6 rendering modes:

1. **document** — default mode, renders markdown or shows textarea for non-markdown
2. **raw** — plain text editing with line numbers
3. **code** — syntax-highlighted code view
4. **diff** — unified diff viewer
5. **process-intake** — conversational mode routing to `llm:to_ir` endpoint
6. **chat** — chat bubble view with timestamps

Each mode is configured via the `mode` prop (type `SDEditorMode`). The mode can be:
- Set via props from parent component
- Changed via dropdown UI (click mode button in toolbar)
- Cycled via keyboard shortcut (Cmd+Shift+M)

**Current state:**
- Code review shows all 6 modes are implemented in `SDEditor.tsx` (lines 570-667)
- Tests exist in `SDEditor.modes.test.tsx` (28 tests covering all modes)
- Mode switching logic is implemented (dropdown + keyboard shortcut)
- Each mode has its own renderer component:
  - `RawView.tsx` — raw mode
  - `codeRenderer.tsx` (CodeView) — code mode
  - `DiffView.tsx` — diff mode
  - `chatRenderer.tsx` (ChatView) — chat mode
  - `markdownRenderer.tsx` (renderMarkdown) — document + process-intake modes

**Potential issues to verify:**
1. Mode switching works without losing content
2. All modes render correctly for their respective content types
3. Tests pass for all mode transitions
4. CSS uses only `var(--sd-*)` variables (already verified in code review — all CSS compliant)
5. No broken modes or incomplete implementations

---

## Files to Review

### Core implementation:
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\SDEditor.tsx` (760 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\types.ts` (74 lines, defines SDEditorMode type)

### Renderer components:
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\services\RawView.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\services\codeRenderer.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\services\DiffView.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\services\chatRenderer.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\services\markdownRenderer.tsx`

### Tests:
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\__tests__\SDEditor.modes.test.tsx` (397 lines, 28 tests)
- Other test files in `__tests__/` directory

### CSS:
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\sd-editor.css` (937 lines)

---

## Deliverables

Create **ONE task file** (not multiple subtasks):

### TASK-BL-065: SDEditor Multi-Mode Verification

**Objective:** Verify all 6 SDEditor modes work correctly and fix any broken behavior.

**Steps:**
1. **Run existing tests** for SDEditor modes:
   ```bash
   cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser
   npx vitest run src/primitives/text-pane/__tests__/SDEditor.modes.test.tsx --reporter=verbose
   npx vitest run src/primitives/text-pane/ --reporter=verbose
   ```

2. **Verify each mode renders correctly:**
   - **document mode:** markdown rendered for `.md` files, textarea for plain text
   - **raw mode:** plain textarea with line numbers, no markdown rendering
   - **code mode:** syntax-highlighted view with line numbers and copy button
   - **diff mode:** unified diff viewer with +/- line highlighting
   - **process-intake mode:** document-like view routing to `llm:to_ir` on Enter
   - **chat mode:** chat bubbles with timestamps and typing indicator

3. **Test mode switching:**
   - Dropdown UI shows all 6 modes and highlights current mode
   - Clicking mode option switches mode without losing content
   - Cmd+Shift+M keyboard shortcut cycles through modes
   - Content persists across mode switches

4. **Fix any broken modes:**
   - If any mode doesn't render correctly, identify the issue and fix it
   - If tests fail, fix the implementation or update tests (only if tests are wrong)
   - Ensure no hardcoded colors in CSS (already verified — all use `var(--sd-*)`)

5. **Add missing tests if needed:**
   - If any mode behavior is untested, add test coverage
   - Test mode switching with various content types
   - Test edge cases (empty content, very long content, special characters)

**Acceptance Criteria:**
- [ ] All tests in `SDEditor.modes.test.tsx` pass (28 tests)
- [ ] All tests in `text-pane/` directory pass (full suite)
- [ ] Mode dropdown shows all 6 modes correctly
- [ ] Mode switching works without content loss
- [ ] Each mode renders correctly for its content type
- [ ] Cmd+Shift+M cycles through modes
- [ ] No hardcoded colors in CSS (already verified)
- [ ] No files over 500 lines (SDEditor.tsx is 760 — may need split if adding significant code)
- [ ] Response file documents what was verified and any fixes made

**Constraints:**
- If SDEditor.tsx needs new code and exceeds 1000 lines, split into smaller modules
- All fixes must maintain existing functionality — this is verification + fixes, not a rewrite
- CSS must use `var(--sd-*)` only (already compliant)

**Smoke Test:**
```bash
cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser
npx vitest run src/primitives/text-pane/ --reporter=verbose
npx vitest run --reporter=verbose
```

**Model Assignment:** sonnet (verification + potential fixes require judgment)

**Priority:** P0

---

## Notes for Q33N

- **This is a verification task, not a feature implementation.** The modes are already built. The bee needs to confirm they work and fix any broken behavior.
- **Do NOT rewrite SDEditor.** Only fix specific broken behaviors if found.
- **If all tests pass and all modes work, the task is complete.** Just verify and report.
- **If issues are found:** Document them clearly in the response file and describe the fixes applied.
- **SDEditor.tsx is 760 lines** — close to the 500-line target but under the 1000 hard limit. Only split if adding significant new code (unlikely for a verification task).

---

## Expected Bee Response File Structure

```markdown
# TASK-BL-065: SDEditor Multi-Mode Verification — COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-03-18

## Files Modified
(list files if any fixes were made; if verification-only, list "None — all modes working")

## What Was Done
- Ran test suite for SDEditor modes
- Verified all 6 modes render correctly:
  - document: ✓ (working)
  - raw: ✓ (working)
  - code: ✓ (working)
  - diff: ✓ (working)
  - process-intake: ✓ (working)
  - chat: ✓ (working)
- Verified mode switching via dropdown and keyboard shortcut
- (if fixes made, describe them here)

## Test Results
- SDEditor.modes.test.tsx: 28/28 tests passing
- Full text-pane suite: X/X tests passing
- Smoke test (all browser tests): X/X passing

## Issues Found
(list any issues discovered)

## Fixes Applied
(describe fixes, or "None — all modes working")

## Recommendations
(optional: any suggestions for future improvements)
```

---

## Approval

Q33N: Create task file for TASK-BL-065 as described above. Return it for my review before dispatching.

**Q88NR-bot**
