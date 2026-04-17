# TASK-017: Dashboard Primitive (P-15) — Status Bar + Model Chooser

## Objective

Build a dashboard primitive at `browser/src/primitives/dashboard/` that provides a status/control bar for panes. MVP scope: model chooser dropdown, 3-currency display (Clock/Coin/Carbon), API key status indicator, and context status. This is the control surface that sits at the bottom or top of a pane and gives the user visibility into what model they're using, what it's costing, and whether their key is configured.

## Context

The terminal already has `TerminalStatusBar.tsx` which displays 3C metrics and model info. But that component is terminal-specific — it's tightly coupled to terminal state. The dashboard primitive extracts the universal parts into a reusable component that any pane can embed.

For the chat app MVP, the dashboard renders as a bottom bar in the terminal pane showing:
- Current model name + provider (e.g., "claude-sonnet-4-5 · Anthropic")
- 3-currency totals: Clock (wall time), Coin (USD cost), Carbon (CO₂)
- API key status: configured (green dot) or missing (yellow warning)
- A model chooser dropdown to switch models

### Integration with Shell

The dashboard is NOT a standalone pane — it's an **embeddable component** that other primitives import. It does not register in the app registry. Instead:

- Terminal imports `<DashboardBar />` and renders it in its status bar zone
- Any future pane that needs model/cost display imports the same component
- Communicates via props (not bus) — the parent pane owns the state

### Relation to Existing Code

- `TerminalStatusBar.tsx` — will be refactored in a follow-up task to use DashboardBar internally. Do NOT modify TerminalStatusBar in this task.
- `SessionLedger` interface (terminal/types.ts) — reuse this type for 3C metrics
- `hivenode/llm/config.py` — provider/model list reference (hardcode in frontend for MVP)
- `browser/src/services/frank/providers/` — provider implementations that use the selected model

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\TerminalStatusBar.tsx` — existing status bar (pattern reference, do NOT modify)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\types.ts` — SessionLedger, FrankMetrics types
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\frank\types.ts` — Frank service types
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\shell-themes.css` — CSS variables
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\llm\config.py` — provider/model list reference

## Type Definitions

### types.ts

```typescript
/** Provider and model configuration for the model chooser. */
export interface ProviderConfig {
  id: string;                       // 'anthropic' | 'openai' | 'groq' | 'ollama'
  label: string;                    // 'Anthropic' | 'OpenAI' | 'Groq' | 'Ollama'
  models: ModelOption[];
}

export interface ModelOption {
  id: string;                       // 'claude-sonnet-4-5-20250929'
  label: string;                    // 'Sonnet 4.5'
  provider: string;                 // 'anthropic'
}

/** 3-currency metrics. Matches SessionLedger from terminal types. */
export interface CurrencyMetrics {
  clock_ms: number;
  cost_usd: number;
  carbon_g: number;
}

/** Which currencies to display. */
export type CurrencyFilter = ('clock' | 'coin' | 'carbon')[];

export interface DashboardBarProps {
  /** Current model ID. */
  model: string;
  /** Called when user selects a different model. */
  onModelChange: (modelId: string) => void;
  /** Current session metrics. */
  metrics: CurrencyMetrics;
  /** Which currencies to show. Default: all three. */
  currencies?: CurrencyFilter;
  /** Whether an API key is configured for the current provider. */
  hasApiKey: boolean;
  /** Called when user clicks the API key status (to open settings). */
  onApiKeyClick?: () => void;
  /** Optional status text (e.g., "Streaming...", "Idle", "Error"). */
  statusText?: string;
  /** Compact mode — single line, smaller text. Default: false. */
  compact?: boolean;
}

export interface ModelChooserProps {
  /** Currently selected model ID. */
  value: string;
  /** Called when a model is selected. */
  onChange: (modelId: string) => void;
  /** Available providers and models. If omitted, uses DEFAULT_PROVIDERS. */
  providers?: ProviderConfig[];
  /** Compact mode. */
  compact?: boolean;
}

export interface CurrencyDisplayProps {
  /** Metrics to display. */
  metrics: CurrencyMetrics;
  /** Which currencies to show. */
  currencies?: CurrencyFilter;
  /** Compact mode. */
  compact?: boolean;
}
```

## Component Architecture

```
browser/src/primitives/dashboard/
├── types.ts                    — ProviderConfig, ModelOption, CurrencyMetrics, DashboardBarProps
├── constants.ts                — DEFAULT_PROVIDERS with hardcoded model lists
├── DashboardBar.tsx            — Main bar: model chooser + currencies + status
├── ModelChooser.tsx            — Dropdown: provider groups, model options
├── CurrencyDisplay.tsx         — 3C metric pills: clock, coin, carbon
├── ApiKeyBadge.tsx             — Key status indicator (configured/missing)
├── dashboard.css               — All styling (var(--sd-*) only)
├── index.ts                    — Public exports
└── __tests__/
    ├── DashboardBar.test.tsx   — Integration tests
    ├── ModelChooser.test.tsx   — Model selection tests
    ├── CurrencyDisplay.test.tsx — Currency formatting tests
    └── ApiKeyBadge.test.tsx    — Badge state tests
```

## Component Details

### DashboardBar.tsx (main bar)
- Horizontal flex bar, fixed height (32px default, 24px compact)
- Left section: ModelChooser dropdown
- Center section: CurrencyDisplay (3C pills)
- Right section: ApiKeyBadge + optional status text
- All sections collapse gracefully at narrow widths (currency labels hide, model shows short name)

### ModelChooser.tsx (dropdown)
- Custom select-like dropdown (not native `<select>` — needs styling)
- Shows current model label + provider name when closed
- When open: grouped by provider, each provider is a section header
- Click outside or Escape closes
- Keyboard: ArrowUp/Down to navigate, Enter to select
- Disabled state when no API key (grayed out with tooltip)

### CurrencyDisplay.tsx (3C pills)
- Three inline pills, each showing icon + value
- Clock: stopwatch icon + `(ms / 1000).toFixed(1)` + "s"
- Coin: dollar icon + `cost_usd.toFixed(4)` (or .toFixed(2) in compact)
- Carbon: leaf icon + `carbon_g.toFixed(2)` + "g"
- Icons are CSS-only (Unicode or var(--sd-icon-*))
- Respects `currencies` filter — only shows requested ones
- Zero values shown as "0.0s", "$0.00", "0.00g" (never hidden)

### ApiKeyBadge.tsx (key status)
- Green dot + "Key" when hasApiKey is true
- Yellow warning + "No key" when false
- Clickable — calls onApiKeyClick to open settings
- Tooltip on hover with provider name

### constants.ts (default providers)
- Hardcoded provider/model list for MVP (matches hivenode/llm/config.py):
  - Anthropic: claude-opus-4-6, claude-sonnet-4-5, claude-haiku-4-5
  - OpenAI: gpt-4o, gpt-4o-mini
  - Groq: llama-3.3-70b, mixtral-8x7b
- This will be replaced by dynamic loading from hivenode API in a future task

## Deliverables

### Source Files (8)
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\dashboard\types.ts`
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\dashboard\constants.ts`
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\dashboard\DashboardBar.tsx`
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\dashboard\ModelChooser.tsx`
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\dashboard\CurrencyDisplay.tsx`
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\dashboard\ApiKeyBadge.tsx`
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\dashboard\dashboard.css`
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\dashboard\index.ts`

### Test Files (4)
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\dashboard\__tests__\DashboardBar.test.tsx` — 10 tests
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\dashboard\__tests__\ModelChooser.test.tsx` — 8 tests
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\dashboard\__tests__\CurrencyDisplay.test.tsx` — 8 tests
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\dashboard\__tests__\ApiKeyBadge.test.tsx` — 5 tests

**Total: 12 deliverables (8 source + 4 test), 31+ tests**

## Test Requirements (~31 tests minimum)

### DashboardBar.test.tsx (~10 tests)
- [ ] Renders model chooser, currency display, and API key badge
- [ ] Passes model prop to ModelChooser
- [ ] Passes metrics to CurrencyDisplay
- [ ] Passes hasApiKey to ApiKeyBadge
- [ ] Calls onModelChange when model is selected
- [ ] Calls onApiKeyClick when badge is clicked
- [ ] Renders status text when provided
- [ ] Compact mode reduces height
- [ ] Currency filter is passed through
- [ ] All sections render at minimum width without overflow

### ModelChooser.test.tsx (~8 tests)
- [ ] Shows current model label when closed
- [ ] Opens dropdown on click
- [ ] Groups models by provider
- [ ] Calls onChange when model clicked
- [ ] Closes on click outside
- [ ] Closes on Escape key
- [ ] ArrowDown moves to next option
- [ ] Enter selects focused option

### CurrencyDisplay.test.tsx (~8 tests)
- [ ] Renders all three currencies by default
- [ ] Formats clock as seconds with 1 decimal
- [ ] Formats coin as USD with 4 decimals
- [ ] Formats carbon as grams with 2 decimals
- [ ] Respects currency filter — hides filtered currencies
- [ ] Shows zero values (never hidden)
- [ ] Compact mode uses shorter format
- [ ] Updates when metrics change

### ApiKeyBadge.test.tsx (~5 tests)
- [ ] Shows green indicator when hasApiKey is true
- [ ] Shows warning indicator when hasApiKey is false
- [ ] Calls onApiKeyClick when clicked
- [ ] Shows "Key" text when configured
- [ ] Shows "No key" text when not configured

## Constraints

- TypeScript strict mode
- All files under 500 lines
- CSS: `var(--sd-*)` only — no hex, no rgb(), no named colors
- vitest + @testing-library/react
- No external UI library dependencies
- No stubs — every function fully implemented
- Keyboard accessible (dropdown navigation)
- Do NOT modify TerminalStatusBar.tsx

## Response Requirements -- MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/YYYYMMDD-TASK-017-RESPONSE.md`

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
