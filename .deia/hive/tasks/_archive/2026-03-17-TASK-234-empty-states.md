# TASK-234: Empty States — Helpful Text in Empty Panes

## Objective

Add helpful guidance text to empty panes so new users understand what to do when they see a blank pane with just a FAB (+) button.

## Context

This is Wave 4 Product Polish (Task 4.6 from `docs/specs/WAVE-4-PRODUCT-POLISH.md`).

Currently, `EmptyPane.tsx` shows a centered FAB (+) button, but new users see a blank dark box with a small + button and have no idea what to do. We need to add contextual help text that explains the user can click + or right-click to add content.

The help text should:
- Be subtle and understated (not compete with the FAB)
- Use theme variables for all colors
- Appear below the FAB button
- Show in two lines: "Empty pane" (primary) and "Click + or right-click to add content" (secondary)

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\EmptyPane.tsx` — Current empty pane implementation (~200 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\__tests__\PaneContent.test.tsx` — Example test pattern for shell components

## Deliverables

- [ ] Add help text below the FAB button in `EmptyPane.tsx`:
  - Primary text: "Empty pane" (subtle, using `var(--sd-text-muted)`)
  - Secondary text: "Click + or right-click to add content" (smaller, using `var(--sd-text-dimmer)`)
  - Text should be centered below the FAB
  - Text should not be shown when an applet is loading (defer to loading state)
- [ ] Create test file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\__tests__\EmptyPane.test.tsx`
- [ ] Tests must include:
  - Empty pane renders help text
  - Help text uses correct CSS variables
  - FAB button is present and clickable
  - Right-click opens context menu
  - Help text is properly styled (centered, correct spacing)
- [ ] Run: `cd browser && npx vitest run src/shell/components/__tests__/EmptyPane.test.tsx`
- [ ] Verify no hardcoded colors (only `var(--sd-*)`)

## Test Requirements

- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Edge cases:
  - Empty pane with no tabs
  - Empty pane with tabs but active tab is empty (future — skip for now)
  - Help text doesn't interfere with FAB hover/click behavior

## Constraints

- Rule 3: **NO HARDCODED COLORS.** Only CSS variables (`var(--sd-*)`). No hex, no rgb(), no named colors.
- Rule 4: **No file over 500 lines.** `EmptyPane.tsx` is currently ~200 lines. Adding help text should not push it over 500.
- Rule 5: **TDD.** Tests first, then implementation.
- Rule 6: **NO STUBS.** Every function fully implemented.

## Acceptance Criteria

- [ ] Help text appears below FAB in empty panes
- [ ] Help text uses `var(--sd-text-muted)` for primary line
- [ ] Help text uses `var(--sd-text-dimmer)` for secondary line
- [ ] Help text is centered and properly spaced
- [ ] FAB button remains functional (click opens menu)
- [ ] Right-click still opens context menu
- [ ] All tests pass (minimum 5 tests)
- [ ] No hardcoded colors in the implementation
- [ ] `EmptyPane.tsx` remains under 500 lines

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260317-TASK-234-RESPONSE.md`

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
