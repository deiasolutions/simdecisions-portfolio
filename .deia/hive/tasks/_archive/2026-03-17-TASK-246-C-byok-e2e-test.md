# TASK-246-C: E2E Test — BYOK Flow

## Objective
Write an end-to-end test that verifies the full BYOK (Bring Your Own Key) flow: user opens settings, pastes API key, saves, sends message, terminal uses the key to call LLM API, response appears.

## Context
All BYOK components exist (SettingsModal, settingsStore, AnthropicProvider), but there is no E2E test that proves the flow works end-to-end. This test is required for Wave 5 Ship confidence.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\settings\SettingsModal.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\settings\settingsStore.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\terminal\providers\anthropic.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\useTerminal.ts`

## Deliverables
- [ ] Create test file: `browser/src/__tests__/byok-flow.e2e.test.tsx`
- [ ] Test Steps:
  1. Mock localStorage with no API key initially
  2. Render Shell component with chat EGG layout
  3. Open Settings modal (simulate click on MenuBar Settings item or direct modal open)
  4. Select provider = Anthropic in KeyManager
  5. Paste API key = `sk-ant-test1234567890ABCDEF` into key input
  6. Click Save button
  7. Verify localStorage now has key: `getApiKey('anthropic') === 'sk-ant-test1234567890ABCDEF'`
  8. Close Settings modal
  9. Type message "Hello" in terminal input
  10. Submit message (Enter key or submit button)
  11. Mock fetch to `https://api.anthropic.com/v1/messages` using vi.mock
  12. Verify fetch was called with:
      - Header: `x-api-key: sk-ant-test1234567890ABCDEF`
      - Body: `messages: [{ role: 'user', content: 'Hello' }]`
  13. Mock response: `{ content: [{ type: 'text', text: 'Hi there!' }], usage: { input_tokens: 10, output_tokens: 5 }, model: 'claude-sonnet-4-5-20250929' }`
  14. Verify terminal displays response "Hi there!" in text-pane
  15. Verify metrics displayed: clock, cost, carbon

## Test Requirements
- [ ] Test file written using vitest + @testing-library/react
- [ ] Mock fetch globally: `vi.stubGlobal('fetch', vi.fn())`
- [ ] Mock localStorage: `Storage.prototype.getItem`, `Storage.prototype.setItem`
- [ ] All tests pass: `cd browser && npx vitest run`
- [ ] Edge cases:
  - No API key configured → terminal shows error "No API key configured"
  - Invalid API key (401 from Anthropic) → terminal shows auth error
  - Network error → terminal shows network error

## Constraints
- No file over 500 lines
- Test file must not duplicate existing unit tests (settingsStore.test.ts, useTerminal.test.ts)
- Focus on integration: Settings UI → Storage → Terminal → API Call → Response Display

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260317-TASK-246-C-RESPONSE.md`

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
