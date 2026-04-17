# TASK-100: Port Shell Chrome — Wave 1 (Standalone Components)

## Objective
Port 6 standalone shell chrome components from old repo to shiftcenter: HighlightOverlay, ScrollToBottom, ShortcutsPopup, NotificationModal, LayoutSwitcher, dragDropUtils. These have no shell context dependencies.

## Context
Wave 1 of a 3-wave shell chrome port. These components are small, independent, and have minimal dependencies. The spec is at `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\specs\SPEC-PORT-SHELL-001-shell-chrome-port.md`.

**Rule:** PORT, NOT REWRITE. Same props, same logic, same CSS classes. TypeScript conversion + `var(--sd-*)` theming only.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\specs\SPEC-PORT-SHELL-001-shell-chrome-port.md` (lines 271–310 for these 6 components)
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\shell\HighlightOverlay.tsx` (16 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\shell\ScrollToBottom.tsx` (34 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\shell\ShortcutsPopup.tsx` (27 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\shell\NotificationModal.tsx` (64 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\shell\LayoutSwitcher.tsx` (33 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\shell\dragDropUtils.ts` (62 lines)

## Deliverables
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\HighlightOverlay.tsx` (port from old)
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\ScrollToBottom.tsx` (port from old)
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\ShortcutsPopup.tsx` (port from old)
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\NotificationModal.tsx` (port from old)
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\LayoutSwitcher.tsx` (port from old)
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\dragDropUtils.ts` (port from old, note: in `shell/` not `shell/components/`)
- [ ] Vitest unit tests for all 6 components (`__tests__/HighlightOverlay.test.tsx`, etc.)

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Edge cases:
  - HighlightOverlay: renders null when not visible
  - ScrollToBottom: threshold logic (40px), returns null when at bottom
  - ShortcutsPopup: backdrop click closes, filters features with shortcuts
  - NotificationModal: 5 types, visual mute suppresses info/reject-feedback (NOT alert/confirmation), keyboard Enter/Escape, reject-feedback text input
  - LayoutSwitcher: 8 layout presets dispatch SET_LAYOUT
  - dragDropUtils: wildcard matching (`image/*`), special IR/BPMN extensions, fallback logic

## Constraints
- No file over 500 lines (none of these are close)
- CSS: `var(--sd-*)` only
- No stubs
- Props interfaces MUST match spec exactly
- CSS class names MUST match spec
- Portal target for modals: `.hhp-root`

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260314-TASK-100-RESPONSE.md`

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
