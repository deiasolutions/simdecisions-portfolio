# TASK-018: BYOK Settings UI — API Key Management + Model Selection

## Objective

Build a settings panel at `browser/src/primitives/settings/` that lets users paste their API keys, select a default model, and manage provider preferences. This is the component that unblocks the actual LLM round-trip — without it, the chat app shows "No API key configured" and can't call any provider.

## Context

The backend BYOK system exists (`hivenode/llm/byok.py`) with encrypted storage, but the chat app runs entirely in the browser for MVP. API keys are stored in `localStorage` under `sd_user_settings`. The Frank service providers (`browser/src/services/frank/providers/`) already read from this key:

```typescript
// Current pattern in providers/anthropic.ts:
const settings = localStorage.getItem('sd_user_settings');
const apiKey = state.apiKey || null;
```

The settings UI needs to:
1. Let users paste API keys for each provider (Anthropic, OpenAI, Groq)
2. Store keys in localStorage (encrypted backend storage is a future task)
3. Let users pick a default model from the selected provider
4. Show which providers have keys configured
5. Register as appType `'settings'` in the app registry (for standalone settings pane)
6. Also export a `<SettingsModal />` that can be opened from any pane via bus message

### Interaction Flow

1. User clicks "No key" badge in DashboardBar (TASK-017) → publishes `settings:open` on bus
2. Shell opens settings as a spotlight pane (or modal overlay)
3. User selects provider tab → pastes API key → clicks Save
4. Key stored in localStorage → badge updates to green → model chooser unlocks
5. User selects model → saved to localStorage → Frank service uses it on next message

### Security Considerations

- Keys stored in localStorage are NOT encrypted (browser limitation for MVP)
- Display key as masked (`sk-ant-••••••••••••ABCD`) — show only first 7 + last 4 chars
- Warn user: "Keys are stored in your browser. Do not use on shared computers."
- Delete key clears from localStorage immediately
- Never log keys to console

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\frank\providers\anthropic.ts` — how keys are currently read
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\useTerminal.ts` — currentModel state, localStorage patterns
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\appRegistry.ts` — AppRendererProps for pane registration
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\shell-themes.css` — CSS variables
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\llm\config.py` — provider/model list reference
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\llm\byok.py` — backend BYOK reference (future integration)

## Type Definitions

### types.ts

```typescript
/** User settings stored in localStorage. */
export interface UserSettings {
  /** API keys by provider ID. */
  apiKeys: Record<string, string>;
  /** Default provider. */
  defaultProvider: string;
  /** Default model ID. */
  defaultModel: string;
  /** Timestamp of last settings change. */
  updatedAt: string;
}

/** Props for the settings panel. */
export interface SettingsPanelProps {
  /** Called when settings are saved. */
  onSave?: (settings: UserSettings) => void;
  /** Called when panel is closed. */
  onClose?: () => void;
  /** Initial tab to show. */
  initialTab?: 'keys' | 'model' | 'about';
}

/** Props for the settings modal wrapper. */
export interface SettingsModalProps extends SettingsPanelProps {
  /** Whether the modal is open. */
  open: boolean;
}

/** Provider key status for display. */
export interface ProviderKeyStatus {
  provider: string;
  label: string;
  hasKey: boolean;
  maskedKey?: string;          // 'sk-ant-••••ABCD'
  lastUsed?: string;           // ISO timestamp
}
```

## Component Architecture

```
browser/src/primitives/settings/
├── types.ts                    — UserSettings, SettingsPanelProps, ProviderKeyStatus
├── settingsStore.ts            — localStorage read/write for UserSettings (single source of truth)
├── SettingsPanel.tsx           — Main panel: tab bar (Keys | Model | About) + tab content
├── KeyManager.tsx              — API key management: provider list, paste input, save/delete, masked display
├── ModelSelector.tsx           — Model selection: provider dropdown → model dropdown, save default
├── SettingsModal.tsx           — Modal wrapper: backdrop, centered card, close button
├── settings.css                — All styling (var(--sd-*) only)
├── index.ts                    — Public exports + app registry registration
└── __tests__/
    ├── settingsStore.test.ts   — Store read/write/mask tests
    ├── KeyManager.test.tsx     — Key management UI tests
    ├── ModelSelector.test.tsx  — Model selection tests
    ├── SettingsPanel.test.tsx  — Tab navigation tests
    └── SettingsModal.test.tsx  — Modal open/close tests
```

## Component Details

### settingsStore.ts (localStorage wrapper)
- `loadSettings(): UserSettings` — reads from `sd_user_settings`, returns defaults if missing
- `saveSettings(settings: UserSettings): void` — writes to `sd_user_settings` with updatedAt
- `getApiKey(provider: string): string | null` — reads key for provider
- `setApiKey(provider: string, key: string): void` — saves key, updates timestamp
- `deleteApiKey(provider: string): void` — removes key for provider
- `maskApiKey(key: string): string` — returns masked version (first 7 + "••••" + last 4)
- `getProviderStatuses(): ProviderKeyStatus[]` — returns status for all providers
- `getDefaultModel(): string` — returns default model ID
- `setDefaultModel(provider: string, model: string): void` — saves default

### SettingsPanel.tsx (main panel)
- Tab bar: Keys | Model | About
- Keys tab: renders KeyManager
- Model tab: renders ModelSelector
- About tab: version info, links, security notice
- 400px wide, auto height, max 600px
- Renders as standalone content (no chrome of its own — parent provides frame)

### KeyManager.tsx (API key management)
- Lists all providers (Anthropic, OpenAI, Groq) as cards
- Each card shows: provider name, status (configured/not), masked key if set
- "Add Key" button → expands to show paste input + Save button
- "Delete Key" button → confirmation prompt → removes from localStorage
- Input type="password" with toggle visibility button
- Validation: non-empty, trims whitespace
- Security warning banner at top: "Keys are stored in your browser only."

### ModelSelector.tsx (model selection)
- Provider dropdown (only providers with configured keys are selectable)
- Model dropdown (models for selected provider)
- "Set as default" button
- Shows current default with checkmark
- Disabled providers (no key) shown grayed out with "Add key first" message
- Model list hardcoded for MVP (same as TASK-017 constants.ts)

### SettingsModal.tsx (modal wrapper)
- Backdrop (semi-transparent overlay, click to close)
- Centered card with SettingsPanel inside
- Close button (× in top-right)
- Escape key closes
- Rendered via React portal (appended to document.body)
- Transition: fade in/out (CSS transition, not JS animation)

### index.ts (exports + registration)
- Exports all components and types
- Exports `registerSettingsApp()` function that calls `registerApp('settings', SettingsAdapter)`
- SettingsAdapter maps AppRendererProps → SettingsPanel props

## Deliverables

### Source Files (8)
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\settings\types.ts`
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\settings\settingsStore.ts`
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\settings\SettingsPanel.tsx`
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\settings\KeyManager.tsx`
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\settings\ModelSelector.tsx`
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\settings\SettingsModal.tsx`
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\settings\settings.css`
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\settings\index.ts`

### Test Files (5)
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\settings\__tests__\settingsStore.test.ts` — 10 tests
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\settings\__tests__\KeyManager.test.tsx` — 10 tests
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\settings\__tests__\ModelSelector.test.tsx` — 8 tests
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\settings\__tests__\SettingsPanel.test.tsx` — 6 tests
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\settings\__tests__\SettingsModal.test.tsx` — 6 tests

**Total: 13 deliverables (8 source + 5 test), 40+ tests**

## Test Requirements (~40 tests minimum)

### settingsStore.test.ts (~10 tests)
- [ ] loadSettings returns defaults when localStorage empty
- [ ] saveSettings writes to localStorage with updatedAt
- [ ] getApiKey returns null when no key set
- [ ] setApiKey stores key and updates timestamp
- [ ] deleteApiKey removes key from settings
- [ ] maskApiKey masks middle of key (first 7 + •••• + last 4)
- [ ] maskApiKey handles short keys gracefully
- [ ] getProviderStatuses returns all providers with correct hasKey
- [ ] getDefaultModel returns stored default
- [ ] setDefaultModel updates provider and model

### KeyManager.test.tsx (~10 tests)
- [ ] Renders all provider cards
- [ ] Shows "Not configured" for providers without keys
- [ ] Shows masked key for configured providers
- [ ] Add Key button shows input field
- [ ] Save button stores key via settingsStore
- [ ] Delete button removes key after confirmation
- [ ] Input validation rejects empty strings
- [ ] Security warning banner is visible
- [ ] Password input toggles visibility
- [ ] Calls onSave after key is saved

### ModelSelector.test.tsx (~8 tests)
- [ ] Shows provider dropdown
- [ ] Only providers with keys are selectable
- [ ] Shows models for selected provider
- [ ] Calls onChange when model is selected
- [ ] Shows current default with indicator
- [ ] Disabled providers show "Add key first"
- [ ] Set as default button calls setDefaultModel
- [ ] Updates when provider keys change

### SettingsPanel.test.tsx (~6 tests)
- [ ] Renders tab bar with Keys, Model, About tabs
- [ ] Keys tab is default
- [ ] Clicking Model tab shows ModelSelector
- [ ] Clicking About tab shows version info
- [ ] initialTab prop selects starting tab
- [ ] onClose is called when close action triggers

### SettingsModal.test.tsx (~6 tests)
- [ ] Renders nothing when open is false
- [ ] Renders backdrop and panel when open is true
- [ ] Clicking backdrop calls onClose
- [ ] Escape key calls onClose
- [ ] Close button calls onClose
- [ ] Modal renders via portal (not in parent DOM)

## Constraints

- TypeScript strict mode
- All files under 500 lines
- CSS: `var(--sd-*)` only — no hex, no rgb(), no named colors
- vitest + @testing-library/react
- No external UI library dependencies
- No stubs — every function fully implemented
- localStorage only for MVP (no backend API calls)
- NEVER log API keys to console
- Keyboard accessible (tab navigation, Escape to close)

## Response Requirements -- MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/YYYYMMDD-TASK-018-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** -- task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** -- every file created/modified/deleted, full paths
3. **What Was Done** -- bullet list of concrete changes
4. **Test Results** -- test files run, pass/fail counts
5. **Build Verification** -- vitest output summary
6. **Acceptance Criteria** -- copy deliverables above, mark [x] or [ ]
7. **Clock / Cost / Carbon** -- all three, never omit any
8. **Issues / Follow-ups** -- edge cases, dependencies, recommended next tasks

DO NOT skip any section. A response without all 8 sections is incomplete.
