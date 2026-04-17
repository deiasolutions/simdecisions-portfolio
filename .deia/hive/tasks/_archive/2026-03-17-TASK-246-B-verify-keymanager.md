# TASK-246-B: Verify KeyManager + ModelSelector Components

## Objective
Read KeyManager.tsx and ModelSelector.tsx to verify they exist and are fully implemented. If either is missing or incomplete, implement them to support BYOK flow.

## Context
SettingsPanel.tsx (line 72-73) references KeyManager and ModelSelector components, but we have not verified they exist or are complete. These components are required for users to paste API keys and select models.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\settings\KeyManager.tsx` (may not exist)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\settings\ModelSelector.tsx` (may not exist)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\settings\SettingsPanel.tsx` (lines 72-73)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\settings\settingsStore.ts` (PROVIDERS constant, setApiKey, validateApiKey)

## Deliverables

### If KeyManager DOES NOT EXIST, implement it:
- [ ] Create `browser/src/primitives/settings/KeyManager.tsx`
- [ ] Features:
  - Provider dropdown (Anthropic, OpenAI, Groq) from `PROVIDERS` constant in settingsStore
  - API key input field (type=password, placeholder="Paste your API key")
  - Show/hide toggle for API key (eye icon)
  - Save button → calls `setApiKey(provider, key)`
  - Validation: calls `validateApiKey(provider, key)` before saving
  - Error message if validation fails (wrong prefix, too short, empty)
  - Success message after save: "API key saved"
  - Display current key status: "No key configured" or "Key configured: sk-ant-••••CDEF"
- [ ] All CSS uses var(--sd-*), no hardcoded colors
- [ ] File under 500 lines

### If ModelSelector DOES NOT EXIST, implement it:
- [ ] Create `browser/src/primitives/settings/ModelSelector.tsx`
- [ ] Features:
  - Provider dropdown (Anthropic, OpenAI, Groq)
  - Model dropdown (filtered by selected provider, from PROVIDERS[].models)
  - Save button → calls `setDefaultModel(provider, model)`
  - Display current default: "Current: claude-sonnet-4-5-20250929"
  - Success message after save: "Default model updated"
- [ ] All CSS uses var(--sd-*), no hardcoded colors
- [ ] File under 500 lines

### If components EXIST, verify they meet requirements:
- [ ] Read KeyManager.tsx and verify all features above
- [ ] Read ModelSelector.tsx and verify all features above
- [ ] If incomplete, add missing features
- [ ] Write tests for KeyManager: paste key → save → key stored in localStorage
- [ ] Write tests for ModelSelector: select model → save → default model updated

## Test Requirements
- [ ] Tests written FIRST (TDD) if creating new components
- [ ] Test file: `browser/src/primitives/settings/__tests__/KeyManager.test.tsx`
- [ ] Test file: `browser/src/primitives/settings/__tests__/ModelSelector.test.tsx`
- [ ] All tests pass: `cd browser && npx vitest run`
- [ ] Edge cases for KeyManager:
  - Invalid API key (wrong prefix) → error message shown
  - Empty API key → error message shown
  - Valid API key → saves to localStorage
  - Delete key → key removed from localStorage
- [ ] Edge cases for ModelSelector:
  - Select provider → model list updates
  - Save → localStorage updated with new default

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs
- Use existing types from `browser/src/primitives/settings/types.ts` if they exist

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260317-TASK-246-B-RESPONSE.md`

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
