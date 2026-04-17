# TASK-023: BUG-023 — Palette Collapse to Icon-Only Mode

## Objective

Fix BUG-023: Verify and complete the palette collapse-to-icon-only behavior when the canvas components panel (TreeBrowser) is resized below 120px width. The collapse mechanism exists but needs comprehensive testing and validation to ensure it works correctly in production.

## Context

The canvas palette (TreeBrowser with palette adapter) should automatically collapse to show only component icons when the containing pane is resized below 120px width. Currently:

- ✅ ResizeObserver monitors container width and triggers state change
- ✅ `collapsed` class applied to root div when width < 120px
- ✅ CSS rules hide labels, badges, chevrons; center icons
- ✅ Header and search hidden via JSX conditional rendering
- ⚠️ **No integration tests verify this works in pane context**
- ⚠️ **CSS robustness not verified for edge cases**

The bug is that while unit tests pass, there's no confidence this works correctly in the actual shell/pane environment where TreeBrowser is mounted inside a resizable pane container.

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\TreeBrowser.tsx` (lines 26-50, ResizeObserver setup)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\tree-browser.css` (lines 200-225, collapsed CSS)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\__tests__\collapse.test.tsx` (existing ResizeObserver mock tests)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\treeBrowserAdapter.tsx` (lines 48-419, how TreeBrowser is mounted)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\canvas.egg.md` (to verify palette pane config exists)

## Deliverables

- [ ] **Integration test file:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\__tests__\TreeBrowser.palette-collapse.integration.test.tsx` (or similar name)
  - Tests that mimic TreeBrowserAdapter mounting TreeBrowser with palette adapter
  - Verifies collapse behavior triggers correctly at 120px threshold
  - Verifies all text content (labels, badges) is hidden in collapsed mode
  - Verifies icons remain visible and centered
  - Tests smooth transitions between expanded/collapsed states
  - No hardcoded colors; only CSS variables used

- [ ] **CSS robustness check:** Verify `tree-browser.css` (lines 200-225) correctly handles:
  - Hidden labels don't break layout (display: none, not visibility: hidden)
  - Badges hidden (currently done)
  - Chevrons hidden (currently done)
  - Icons centered (justify-content: center applied to rows)
  - No margin/padding changes that could break centering

- [ ] **Optional: TreeBrowserAdapter enhancement** (if needed after testing):
  - Add `collapseThreshold` prop to `TreeBrowserPaneConfig` so panes can customize the threshold
  - Pass `collapseThreshold` to TreeBrowser in adapter (line 417)
  - This is OPTIONAL—only if tests reveal a need for it

## Test Requirements

- [ ] **Unit tests:** Write tests FIRST (TDD)
  - Simulate pane resizing from 200px → 80px → 200px
  - Verify `collapsed` class toggled at correct threshold
  - Verify labels hidden and icons visible in collapsed mode
  - Verify header/search hidden (JSX conditional rendering—already tested elsewhere)
  - Verify smooth transitions (no flickering, no intermediate states)

- [ ] **Edge case tests:**
  - Width exactly at threshold (120px) — should NOT collapse (requires width < 120, not <=)
  - Very narrow widths (< 50px) — should not break layout
  - Width oscillating around threshold (test debouncing, if needed)
  - ResizeObserver not available (graceful fallback)

- [ ] **All tests pass:**
  - Run: `cd browser && npx vitest run 'src/primitives/tree-browser/__tests__/TreeBrowser.palette-collapse.integration.test.tsx'`
  - All assertions pass
  - No console errors or warnings

- [ ] **No file exceeds 500 lines:**
  - Integration test file should be ≤ 400 lines
  - If larger, split into multiple test files

## Constraints

- **No file over 500 lines** (hard limit: 1,000)
- **CSS variables only:** No hardcoded colors, hex, rgb(), or named colors. Only `var(--sd-*)`
- **TDD:** Tests written first, then implementation
- **No stubs:** Every function fully implemented. No `// TODO`, no empty bodies
- **Node icons must remain centered and visible** when collapsed
- **Smooth transitions:** No jarring class application/removal

## Response Requirements — MANDATORY

When you finish, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260324-TASK-023-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test file, pass/fail counts
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three metrics
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.

## Acceptance Criteria

- [ ] Integration test file created and tests pass (≥ 8 tests)
- [ ] Tests verify collapse behavior at 120px threshold
- [ ] Tests verify labels hidden, icons visible when collapsed
- [ ] Tests verify header/search hidden when collapsed
- [ ] Tests verify smooth transitions between states
- [ ] All CSS uses variables only (`var(--sd-*)`)
- [ ] No file exceeds 500 lines
- [ ] No console errors or warnings in test runs
- [ ] Response file written with all 8 sections

## Background / Notes

- The unit tests in `collapse.test.tsx` already verify the ResizeObserver mock. This task is about **integration testing** in a more realistic context.
- The CSS is already in place (lines 200-225 of tree-browser.css). This task verifies it works as intended.
- **Do not modify the CSS** unless tests reveal a bug. The CSS looks correct.
- **Do not modify TreeBrowser.tsx** unless tests reveal a bug. The ResizeObserver logic looks correct.
- **Focus:** Write comprehensive integration tests that give confidence the feature works end-to-end.
- **P0 Bug:** This is a priority fix. Keep it focused and tight. Don't add extra features.
