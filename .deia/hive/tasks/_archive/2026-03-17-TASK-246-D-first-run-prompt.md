# TASK-246-D: First-Run Prompt — No API Key Configured

## Objective
Show a modal on first use if no API key is configured, prompting the user to add their Anthropic API key in Settings. This is the critical onboarding moment for BYOK users.

## Context
New users who open the chat terminal for the first time have no API key configured. Instead of showing a generic error when they try to send a message, we should proactively prompt them to configure their key on first load.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\TerminalApp.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\settings\settingsStore.ts` (getApiKey function)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\settings\SettingsModal.tsx`

## Deliverables
- [ ] Add first-run check in TerminalApp.tsx (or useTerminal.ts):
  - On mount, check if `getApiKey('anthropic') === null`
  - If null, show modal: "Welcome to Fr@nk. To get started, add your Anthropic API key in Settings."
  - Modal has two buttons:
    - "Open Settings" → opens SettingsModal with initialTab='keys'
    - "Dismiss" → closes modal (user can open settings later via menu)
- [ ] Track dismissed state in localStorage: `sd_first_run_dismissed`
  - If user clicks Dismiss, set `localStorage.setItem('sd_first_run_dismissed', 'true')`
  - On next mount, if `sd_first_run_dismissed === 'true'`, do NOT show modal again
  - Reset logic: If user DOES add an API key, clear the dismissed flag (so if they delete it later, prompt shows again)
- [ ] Render modal ONLY if:
  - No API key is configured AND
  - First-run has not been dismissed
- [ ] Modal styling:
  - Use CSS variables (var(--sd-*))
  - Portal to `.hhp-root`
  - Centered card, semi-transparent backdrop
  - Close on Escape key

## Test Requirements
- [ ] Test file: `browser/src/primitives/terminal/__tests__/TerminalApp.firstRun.test.tsx`
- [ ] Test cases:
  - First load with no API key → modal shows
  - Click "Open Settings" → SettingsModal opens with Keys tab active
  - Click "Dismiss" → modal closes, localStorage flag set
  - Reload page after dismiss → modal does NOT show
  - User adds API key → reload → modal does NOT show (even if dismissed flag was set)
  - User deletes API key → reload → modal shows again
- [ ] All tests pass: `cd browser && npx vitest run`

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs
- Modal should NOT block terminal usage (user can dismiss and try to send a message, which will fail with "No API key configured" error)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260317-TASK-246-D-RESPONSE.md`

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
