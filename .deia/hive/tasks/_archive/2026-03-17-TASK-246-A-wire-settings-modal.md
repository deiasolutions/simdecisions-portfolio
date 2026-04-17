# TASK-246-A: Wire Settings Modal to MenuBar

## Objective
Make the Settings menu item in MenuBar open the SettingsModal. Currently, MenuBar has a Settings item that calls `onNavigate('/settings')`, but this prop is not wired in Shell, so the modal never opens.

## Context
BYOK flow exists end-to-end (SettingsModal, settingsStore, API key usage in terminal), but the Settings modal is not accessible from the UI. The MenuBar Settings item (line 127-132 in MenuBar.tsx) calls `onNavigate('/settings')`, but Shell does not provide this handler.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\Shell.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\MenuBar.tsx` (lines 127-132)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\settings\SettingsModal.tsx`

## Deliverables
- [ ] Modify Shell.tsx to add state: `const [showSettings, setShowSettings] = useState(false)`
- [ ] Pass `onNavigate` handler to MenuBar that sets `showSettings` to true when path === '/settings'
- [ ] Render `<SettingsModal open={showSettings} onClose={() => setShowSettings(false)} onSave={() => setShowSettings(false)} />` in Shell
- [ ] Write test file: `browser/src/shell/components/__tests__/Shell.settings.test.tsx`
  - Test: Click Settings menu item → modal opens
  - Test: Press Escape → modal closes
  - Test: Click backdrop → modal closes
  - Test: Save settings → modal closes

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass: `cd browser && npx vitest run`
- [ ] Edge cases:
  - Settings already open → clicking Settings again does nothing
  - Modal closes when Escape is pressed
  - Modal closes when backdrop is clicked

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260317-TASK-246-A-RESPONSE.md`

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
