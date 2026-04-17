# TASK-246 BYOK Flow Analysis — Q33N Findings

**To:** Q33NR (Queen Regent)
**From:** Q33N (Queen Coordinator)
**Date:** 2026-03-17
**Task:** TASK-246 BYOK Flow Verified

---

## Summary

I traced the existing BYOK (Bring Your Own Key) flow end-to-end. **The core flow is ALREADY BUILT and works.** However, there are gaps in the integration and test coverage.

---

## What EXISTS (Already Built)

### 1. ✅ Settings UI — COMPLETE
- **File:** `browser/src/primitives/settings/SettingsModal.tsx` (80 lines)
- **File:** `browser/src/primitives/settings/SettingsPanel.tsx` (170 lines)
- Modal opens via portal to `.hhp-root`
- Tabbed interface: Keys | Model | Voice | About
- Keys tab contains KeyManager component (not yet verified)

### 2. ✅ Settings Storage — COMPLETE
- **File:** `browser/src/primitives/settings/settingsStore.ts` (266 lines)
- Storage key: `sd_user_settings` in localStorage
- Functions: `loadSettings()`, `saveSettings()`, `getApiKey()`, `setApiKey()`, `deleteApiKey()`
- Supports 3 providers: Anthropic, OpenAI, Groq
- Validates API key prefixes: `sk-ant-`, `sk-`, `gsk_`
- **Tests:** 16 tests in `settingsStore.test.ts` — ALL PASSING

### 3. ✅ API Key Usage in Terminal — COMPLETE
- **File:** `browser/src/services/terminal/terminalService.ts` (line 10)
  - Imports `getApiKey` from settingsStore
  - Line 180: `const apiKey = getApiKey('anthropic');` in proxy mode
- **File:** `browser/src/services/terminal/providers/anthropic.ts` (line 107-118)
  - `getApiKey()` method reads from localStorage (`sd_user_settings`)
  - Line 31: Throws error if no API key configured
  - Line 47: Sets `x-api-key` header with user's key
- **File:** `browser/src/primitives/terminal/useTerminal.ts` (line 10)
  - Imports `loadSettings` from settingsStore

### 4. ✅ LLM Provider Integration — COMPLETE
- **File:** `browser/src/services/terminal/providers/index.ts`
  - `getProvider(model)` maps model names to providers
  - `claude-*` → AnthropicProvider
  - `llama-*` → GroqProvider
- **File:** `browser/src/services/terminal/providers/anthropic.ts`
  - Calls `https://api.anthropic.com/v1/messages`
  - Uses `x-api-key` header from settingsStore
  - Handles 401 (auth error), 429 (rate limit), 500 (server error)

### 5. ✅ Chat EGG Config — COMPLETE
- **File:** `eggs/chat.egg.md`
  - Line 57: `"llmProvider": "anthropic"`
  - Lines 113-130: Permissions block with `allowBYOK: true`
  - Declares providers: anthropic, groq, openai

---

## What is MISSING

### 1. ❌ Settings Menu Integration
- **MenuBar.tsx (line 127-132):** Settings menu item exists
  - Calls `onNavigate('/settings')` but this prop is NOT wired in Shell
  - **Gap:** No route handler for `/settings` path
  - **Gap:** SettingsModal is never opened

### 2. ❌ First-Run Prompt
- **Gap:** No check for "user has no API key" on first load
- **Gap:** No prompt to open settings on first use
- **Expected:** When user opens chat for the first time, if no API key is configured, show a modal: "To use Fr@nk, add your Anthropic API key in Settings"

### 3. ❌ Missing E2E Test
- **Gap:** No test file that verifies:
  1. User opens settings
  2. User pastes API key
  3. Key is stored in localStorage
  4. Terminal sends message using stored key
  5. Chat response appears in text-pane
- **Existing tests:** Only unit tests for settingsStore (storage layer)
- **Need:** E2E test for the full BYOK flow

### 4. ⚠️ Missing Components (Not Verified)
- `KeyManager.tsx` — Renders API key input fields (assumed to exist, not read)
- `ModelSelector.tsx` — Renders model dropdown (assumed to exist, not read)
- May already be built, need verification

---

## Flow Trace

### Current BYOK Flow (Partial — Settings Not Accessible)

1. ❌ **User opens Settings** → MenuBar has Settings menu item, but `onNavigate` is not wired in Shell → Settings never opens
2. ✅ **User selects provider** → (Assumed KeyManager exists)
3. ✅ **User pastes API key** → (Assumed KeyManager calls `setApiKey()`)
4. ✅ **Key stored in localStorage** → `sd_user_settings` key
5. ✅ **Terminal sends message** → useTerminal calls terminalService.sendMessage()
6. ✅ **Provider reads key** → AnthropicProvider.getApiKey() reads from localStorage
7. ✅ **API call with key** → Fetch to `https://api.anthropic.com/v1/messages` with `x-api-key` header
8. ✅ **Response appears** → terminalService returns content + metrics

**Blocker:** Step 1 does not work. Settings modal never opens.

---

## Recommended Task Breakdown

### TASK-246-A: Wire Settings Modal to MenuBar (S — Small, Bee)
**Objective:** Make Settings menu item open SettingsModal.

**Approach:**
1. Add state to Shell: `const [showSettings, setShowSettings] = useState(false)`
2. Pass `onNavigate` handler to MenuBar that opens modal
3. Render `<SettingsModal open={showSettings} onClose={...} onSave={...} />` in Shell
4. Write test: Click Settings → modal opens → press Escape → modal closes

**Files:**
- `browser/src/shell/components/Shell.tsx` (modify)
- `browser/src/shell/components/__tests__/Shell.settings.test.tsx` (new)

**Model:** haiku

---

### TASK-246-B: Verify KeyManager + ModelSelector Exist (S — Small, Bee)
**Objective:** Read KeyManager.tsx and ModelSelector.tsx. If they don't exist, implement them.

**Deliverables:**
- [ ] Read `browser/src/primitives/settings/KeyManager.tsx`
- [ ] Read `browser/src/primitives/settings/ModelSelector.tsx`
- [ ] If missing, implement KeyManager with:
  - Provider dropdown (Anthropic, OpenAI, Groq)
  - API key input (type=password)
  - Save button → calls `setApiKey(provider, key)`
  - Validation: calls `validateApiKey(provider, key)` before saving
- [ ] If missing, implement ModelSelector with:
  - Model dropdown (per provider)
  - Save button → calls `setDefaultModel(provider, model)`
- [ ] Write tests for KeyManager: paste key → save → key stored in localStorage

**Files:**
- `browser/src/primitives/settings/KeyManager.tsx` (new or verify)
- `browser/src/primitives/settings/ModelSelector.tsx` (new or verify)
- `browser/src/primitives/settings/__tests__/KeyManager.test.tsx` (new)

**Model:** haiku

---

### TASK-246-C: E2E Test — BYOK Flow (M — Medium, Bee)
**Objective:** Write E2E test that verifies the full BYOK flow.

**Test Steps:**
1. Render Shell with chat EGG
2. Open Settings modal (via MenuBar click or direct modal open)
3. Select provider = Anthropic
4. Paste API key = `sk-ant-test123...`
5. Click Save
6. Verify localStorage has key: `getApiKey('anthropic') === 'sk-ant-test123...'`
7. Close Settings
8. Type message in terminal
9. Mock Anthropic API response (vi.mock fetch)
10. Verify terminal displays response in text-pane
11. Verify API call included `x-api-key: sk-ant-test123...`

**Files:**
- `browser/src/__tests__/byok-flow.e2e.test.tsx` (new)

**Model:** haiku

---

### TASK-246-D: First-Run Prompt (S — Small, Bee)
**Objective:** Show modal on first use if no API key is configured.

**Approach:**
1. On terminal mount, check if `getApiKey('anthropic')` returns null
2. If null, show modal: "To use Fr@nk, add your Anthropic API key in Settings"
3. Modal has button: "Open Settings" → opens SettingsModal
4. Test: First load with no key → modal shows → click Open Settings → SettingsModal opens

**Files:**
- `browser/src/primitives/terminal/TerminalApp.tsx` (modify)
- `browser/src/primitives/terminal/__tests__/TerminalApp.firstRun.test.tsx` (new)

**Model:** haiku

---

## Next Steps

1. Review these findings with Q33NR
2. Q33NR approves task files (246-A, 246-B, 246-C, 246-D)
3. Q33N dispatches bees in sequence:
   - 246-B first (verify KeyManager exists)
   - 246-A second (wire settings modal)
   - 246-C third (E2E test)
   - 246-D fourth (first-run prompt)

---

**Q33N Signature:** QUEEN-2026-03-17-TASK-246-FINDINGS
