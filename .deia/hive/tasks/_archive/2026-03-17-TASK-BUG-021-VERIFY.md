# TASK-BUG-021-VERIFY: Verify Canvas Minimap Fix and Close BUG-021

## Objective

Verify that BUG-021 (canvas minimap white visible zone and corner misalignment) is already fixed in the current codebase through manual testing, document when the fix occurred, and close the bug.

## Context

BUG-021 reported two issues:
1. **White visible zone on dark background** — minimap viewport indicator showing white instead of theme colors
2. **Corner outline misalignment** — minimap outline corners not aligning correctly

Code analysis by Q33N shows:
- All minimap colors use CSS variables (`var(--sd-*)`) — no hardcoded white/hex/rgb
- CSS explicitly references BUG-021 fix: `/* Minimap viewport indicator — use theme-aware stroke (BUG-021) */`
- Component props use theme-appropriate variables
- Test coverage exists (7 tests, 4 passing due to jsdom limitations)

**Your task:** Verify the fix via manual testing and document closure.

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\canvas.css` (lines 35-39, 101-107)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\CanvasApp.tsx` (lines 499-506)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\__tests__\minimap.styles.test.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260317-2314-BEE-SONNET-2026-03-17-BRIEFING-BUG-021-CANVAS-MINIMAP-WHITE-ZONE-RAW.txt` (investigation report)

## Deliverables

### Manual Verification
- [ ] Manual test: Canvas minimap in dark theme (visible zone = purple dashed outline, NOT white)
- [ ] Manual test: Canvas minimap in light theme (visible zone = purple dashed outline)
- [ ] Manual test: Corner outline alignment (clean, no gaps/misalignment)
- [ ] Screenshots documenting correct behavior (optional, but recommended)

### Documentation
- [ ] Identify when BUG-021 was fixed (search git history for canvas.css changes, look for commit with BUG-021 comment)
- [ ] Document fix commit hash and date in response file

### Test Results
- [ ] Run existing test file: `browser/src/primitives/canvas/__tests__/minimap.styles.test.tsx`
- [ ] Confirm no hardcoded color tests still pass (4 tests expected)
- [ ] No new test failures introduced

### Response File
- [ ] Write response file: `.deia/hive/responses/20260317-TASK-BUG-021-VERIFY-RESPONSE.md`
- [ ] Include all 8 mandatory sections
- [ ] Add **BUG-021 Status** section:
  - Status: VERIFIED_FIXED | STILL_EXISTS
  - Fix date: (commit date when BUG-021 was addressed)
  - Fix commit: (hash)
  - Recommendation: CLOSE_BUG or RE-OPEN

## Test Requirements

- [ ] Run test file: `cd "C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser" && npx vitest run --reporter=verbose src/primitives/canvas/__tests__/minimap.styles.test.tsx`
- [ ] Expected result: 4 tests pass (no hardcoded colors assertions)
- [ ] 3 tests may fail due to jsdom DOM style limitations (not actual bugs)
- [ ] No new test failures introduced

## Constraints

- No file over 500 lines
- CSS: `var(--sd-*)` only (already compliant, verify only)
- No stubs
- **NO CODE CHANGES** — This is verification only
- If you discover the bug STILL EXISTS, document it and return immediately (do NOT attempt fixes)

## Files Referenced

| File | Absolute Path | Purpose |
|------|---------------|---------|
| CSS styles | `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\canvas.css` | Minimap styles (lines 35-39, 101-107) |
| Component | `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\CanvasApp.tsx` | MiniMap component config (lines 499-506) |
| Tests | `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\__tests__\minimap.styles.test.tsx` | Minimap style tests (7 tests) |
| Investigation | `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260317-2314-BEE-SONNET-2026-03-17-BRIEFING-BUG-021-CANVAS-MINIMAP-WHITE-ZONE-RAW.txt` | Q33N investigation report |

## Manual Test Instructions

### How to Test:

1. **Start dev server:** `cd "C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter" && python run_dev.py` (or use existing dev server)
2. **Open browser:** Navigate to Canvas EGG (likely `http://localhost:5174` with canvas.egg.md loaded)
3. **Test dark theme:**
   - Verify minimap visible zone (viewport indicator) is **purple dashed outline**
   - Verify it is **NOT white**
   - Verify corners are clean (no gaps or misalignment)
4. **Test light theme:**
   - Switch to light theme (via settings or CSS variable override)
   - Verify minimap visible zone is **purple dashed outline**
   - Verify corners are clean
5. **Document findings** in response file

### Expected Behavior:

- **Minimap container:** Uses `var(--sd-surface)` background and `var(--sd-border)` border
- **Viewport mask:** Uses `var(--sd-purple)` stroke with 2px width and 4px dash pattern
- **No white color** anywhere in minimap rendering
- **Corners:** Clean alignment, no gaps

## Smoke Test

```bash
cd "C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser" && npx vitest run --reporter=verbose src/primitives/canvas/__tests__/minimap.styles.test.tsx
```

**Expected output:** 4-7 tests pass (depending on jsdom environment)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260317-TASK-BUG-021-VERIFY-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — (should be NONE for verification task)
3. **What Was Done** — manual testing steps performed, test runs
4. **Test Results** — minimap.styles.test.tsx pass/fail counts
5. **Build Verification** — test output summary
6. **Acceptance Criteria** — copy from deliverables, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — any remaining issues or next steps

**ADDITIONAL SECTION:**
9. **BUG-021 Status** — MUST INCLUDE:
   - Status: VERIFIED_FIXED or STILL_EXISTS
   - Fix date: (commit date when BUG-021 was addressed, if found)
   - Fix commit: (hash, if found)
   - Evidence: (screenshots, test results, code snippets)
   - Recommendation: CLOSE_BUG or RE-OPEN (with reasons)

DO NOT skip any section.

## Model Assignment

**Model:** haiku

## Priority

**Priority:** P0 (verification task)

---

**Task Author:** Q33N
**Approved by:** Q88NR
**Date:** 2026-03-17T23:25:00Z
