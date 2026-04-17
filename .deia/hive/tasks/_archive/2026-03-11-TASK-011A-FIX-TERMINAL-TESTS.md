# TASK-011A: Fix Terminal Primitive — Tests + Line Limits + Stripped Interfaces

## Objective

TASK-011 delivered source files but **zero tests** (violating Rule 5: TDD) and has a file over 500 lines (violating Rule 4). Fix all three problems:

1. **Write all 10 test files** with 80+ tests total
2. **Split terminalCommands.ts** (516 lines) under 500
3. **Restore stripped interfaces** in TerminalApp.tsx and useTerminal.ts so downstream consumers can wire to them

## Context

TASK-011 ported the terminal primitive to `browser/src/primitives/terminal/`. All 11 source files exist and compile. But:

- **No test files were written.** The bee deferred all 10 to a follow-up, which is a Rule 5 violation. Tests are not optional.
- **terminalCommands.ts is 516 lines** — over the 500-line limit (Rule 4).
- **TerminalApp.tsx was simplified from 523 to 160 lines** by stripping persistence hooks, feature registry, and mode engine interfaces. These need to be restored as real interfaces with correct signatures, not full implementations — but the seams must exist so TASK-009 (AppletShell) and future tasks can wire to them.

## Files to Read First

Read every source file in the terminal primitive to understand current state:

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\types.ts` (83 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\irRouting.ts` (85 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\terminalCommands.ts` (516 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\TerminalPrompt.tsx` (83 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\TerminalOutput.tsx` (194 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\TerminalResponsePane.tsx` (52 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\TerminalStatusBar.tsx` (101 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\useTerminal.ts` (356 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\TerminalApp.tsx` (160 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\terminal.css` (413 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\index.ts` (36 lines)

Also read the old test files for porting reference:

- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\shell\__tests__\useTerminal.test.ts` (302 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\services\terminal\__tests__\terminalCommands.test.ts` (392 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\services\terminal\__tests__\terminalCommands.telemetry.test.ts` (155 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\frank\__tests__\TerminalStatusBar.test.tsx` (242 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\frank\__tests__\TerminalStatusBar.currencies.test.tsx` (107 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\frank\__tests__\TerminalResponsePane.test.tsx` (238 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\frank\__tests__\TerminalButtonHover.test.tsx` (120 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\apps\__tests__\TerminalApp.paneNav.test.tsx` (297 lines)

## Fix 1: Write All 10 Test Files (80+ tests)

Create these test files in `browser/src/primitives/terminal/__tests__/`:

### useTerminal.test.ts (port from old repo, ~15 tests)
- [ ] Hook initializes with banner entry
- [ ] setInput updates input state
- [ ] handleSubmit adds input+response entries
- [ ] handleSubmit tracks command history
- [ ] handleSubmit clears input after submit
- [ ] /clear resets entries and ledger
- [ ] /help displays command list
- [ ] /ledger shows 3-currency session totals
- [ ] Tab completion matches slash commands
- [ ] localStorage persistence: entries saved on change
- [ ] localStorage persistence: ledger saved on change
- [ ] localStorage persistence: history saved on change
- [ ] localStorage persistence: loaded on mount
- [ ] copyToClipboard calls navigator.clipboard.writeText
- [ ] IR download creates blob and triggers download

### terminalCommands.test.ts (port from old repo, ~16 tests)
- [ ] SLASH_COMMANDS array has all 13 commands
- [ ] /clear clears entries and resets ledger
- [ ] /help displays command list with descriptions
- [ ] /ledger shows formatted session totals
- [ ] /save without conversation shows error
- [ ] /resume <code> calls resumeConversation API
- [ ] /history lists conversations with resume codes
- [ ] /settings in standalone navigates to /settings
- [ ] /settings in pane mode shows system message
- [ ] /designer in standalone navigates to /design/new
- [ ] /designer in pane mode dispatches bus message
- [ ] /logout in standalone navigates to /login
- [ ] /logout in pane mode shows system message
- [ ] /pane sets pane nickname via bus
- [ ] /github connect opens OAuth popup
- [ ] Unknown command shows error message

### terminalCommands.telemetry.test.ts (port from old repo, ~8 tests)
- [ ] /telemetry shows current tier
- [ ] /telemetry 0 switches to anonymous
- [ ] /telemetry 1 switches to UID-linked
- [ ] /telemetry 2 switches to full
- [ ] /telemetry shows "already on tier" if unchanged
- [ ] /telemetry delete shows not-implemented
- [ ] /telemetry export shows not-implemented
- [ ] Invalid subcommand shows usage

### TerminalOutput.test.tsx (port TerminalButtonHover tests + new, ~10 tests)
- [ ] Renders banner entries
- [ ] Renders input entries with prompt prefix
- [ ] Renders response entries with content
- [ ] Renders system entries in italic
- [ ] Renders IR entries with action buttons
- [ ] IR action buttons: Open in Designer, Copy IR, Save .ir.json
- [ ] Spinner displays during loading
- [ ] Auto-scrolls to bottom on new entry
- [ ] Metrics display below response entries
- [ ] CSS variables used (no hardcoded colors)

### TerminalPrompt.test.tsx (new, ~8 tests)
- [ ] Renders hive> prompt label
- [ ] ArrowUp navigates history backward
- [ ] ArrowDown navigates history forward
- [ ] ArrowDown at index 0 clears input
- [ ] Tab triggers onTabComplete callback
- [ ] Enter triggers onSubmit callback
- [ ] Disabled prop disables input field
- [ ] Input autofocuses when enabled

### TerminalResponsePane.test.tsx (port from old repo, ~8 tests)
- [ ] Renders with position=bottom
- [ ] Renders with position=top
- [ ] Renders with position=left
- [ ] Renders with position=right
- [ ] Returns null when position=hidden
- [ ] Returns null when defaultState=hidden
- [ ] Passes entries to TerminalOutput
- [ ] Shows loading indicator

### TerminalStatusBar.test.tsx (port from old repo, ~8 tests)
- [ ] Displays model name
- [ ] Shows BYOK badge with key
- [ ] Shows BYOK badge without key
- [ ] Shows efemera badge connected
- [ ] Shows efemera badge disconnected
- [ ] Displays resume code when present
- [ ] Component order: brand, model, metrics, badges
- [ ] Navigation buttons hidden in pane mode

### TerminalStatusBar.currencies.test.tsx (port from old repo, ~5 tests)
- [ ] Shows all three currencies by default
- [ ] Filters to clock only with statusBarCurrencies=["clock"]
- [ ] Filters to clock+carbon with statusBarCurrencies=["clock","carbon"]
- [ ] Shows cost only with statusBarCurrencies=["coin"]
- [ ] Hides all with statusBarCurrencies=[]

### TerminalApp.paneNav.test.tsx (port from old repo, ~7 tests)
- [ ] Standalone mode allows navigation
- [ ] Pane mode suppresses navigation with system message
- [ ] /settings pane vs standalone behavior
- [ ] /designer pane vs standalone behavior
- [ ] /logout pane vs standalone behavior
- [ ] Bus message dispatch in pane mode
- [ ] isPane detection from props

### irRouting.test.ts (new, ~5 tests)
- [ ] openInDesigner stores IR in sessionStorage (standalone)
- [ ] openInDesigner dispatches bus message (pane mode)
- [ ] copyToClipboard calls navigator.clipboard.writeText
- [ ] downloadIR creates blob and triggers download
- [ ] Shows system message when no canvas pane exists

**Total: 90+ tests across 10 files.**

## Fix 2: Split terminalCommands.ts (516 → under 500 each)

Split `terminalCommands.ts` into two files:

- `terminalCommands.ts` — `handleCommand()` dispatcher + core commands (/clear, /help, /ledger, /history, /save, /resume, /pane, unknown command handler). Keep `SLASH_COMMANDS` array and `TerminalCommandContext` here.
- `terminalCommands.nav.ts` — Navigation and integration commands (/settings, /designer, /logout, /github, /clipboard, /telemetry). These are the pane-aware commands that interact with external systems.

The dispatcher in `terminalCommands.ts` imports handlers from `terminalCommands.nav.ts`:

```typescript
import { handleNavCommand } from './terminalCommands.nav';

export async function handleCommand(cmd: string, context: TerminalCommandContext): Promise<void> {
  const [command, ...args] = cmd.trim().split(/\s+/);
  switch (command) {
    case '/clear': /* ... */ break;
    case '/help': /* ... */ break;
    // ... core commands
    case '/settings': case '/designer': case '/logout':
    case '/github': case '/clipboard': case '/telemetry':
      return handleNavCommand(command, args, context);
    default: /* unknown */ break;
  }
}
```

Both files must be under 500 lines.

## Fix 3: Restore Stripped Interfaces in TerminalApp.tsx and useTerminal.ts

The original TerminalApp.tsx had integration points that were stripped. Restore these as **real interfaces with correct signatures** that return stub values. These are NOT empty bodies — they're real functions with correct return types that downstream tasks wire to.

### TerminalApp.tsx — Add These Props/Hooks

```typescript
interface TerminalAppProps {
  nodeId?: string | null;
  isActive?: boolean;
  hideStatusBar?: boolean;
  onNavigate?: (path: string) => void;
  // Restored interfaces:
  initialEntries?: TerminalEntry[];          // For state restoration from shell reducer
  onStateChange?: (state: TerminalPaneState) => void;  // Debounced pane state persistence
  eggConfig?: TerminalEggConfig | null;      // EGG configuration for this pane
}

interface TerminalEggConfig {
  statusBarCurrencies?: string[];
  zone2Position?: 'top' | 'bottom' | 'left' | 'right' | 'hidden';
  zone2Default?: 'collapsed' | 'expanded' | 'hidden';
  promptPrefix?: string;
}

interface TerminalPaneState {
  entries: TerminalEntry[];
  ledger: SessionLedger;
  conversationId: string | null;
  commandHistory: string[];
}
```

### useTerminal.ts — Add These Parameters

```typescript
interface UseTerminalOptions {
  bus?: MessageBus | null;
  nodeId?: string | null;
  isPane?: boolean;
  initialEntries?: TerminalEntry[];
  onStateChange?: (state: TerminalPaneState) => void;
}
```

The hook should accept these options and:
- Use `initialEntries` if provided (pane state restoration), otherwise fall back to localStorage
- Call `onStateChange` (debounced 2s) whenever entries/ledger/history change
- These are real code paths, not stubs

Add `TerminalEggConfig` and `TerminalPaneState` to `types.ts`.

## Constraints

- TypeScript strict mode
- All files under 500 lines
- No stubs — every test actually tests real behavior
- Test with vitest + @testing-library/react
- All CSS references use var(--sd-*) if any CSS assertions exist
- Mock external dependencies (frank service, chatApi, relay_bus, shell utils)

## Deliverables

### Test Files (10)
- [ ] `browser/src/primitives/terminal/__tests__/useTerminal.test.ts`
- [ ] `browser/src/primitives/terminal/__tests__/terminalCommands.test.ts`
- [ ] `browser/src/primitives/terminal/__tests__/terminalCommands.telemetry.test.ts`
- [ ] `browser/src/primitives/terminal/__tests__/TerminalOutput.test.tsx`
- [ ] `browser/src/primitives/terminal/__tests__/TerminalPrompt.test.tsx`
- [ ] `browser/src/primitives/terminal/__tests__/TerminalResponsePane.test.tsx`
- [ ] `browser/src/primitives/terminal/__tests__/TerminalStatusBar.test.tsx`
- [ ] `browser/src/primitives/terminal/__tests__/TerminalStatusBar.currencies.test.tsx`
- [ ] `browser/src/primitives/terminal/__tests__/TerminalApp.paneNav.test.tsx`
- [ ] `browser/src/primitives/terminal/__tests__/irRouting.test.ts`

### Source File Modifications (4)
- [ ] `browser/src/primitives/terminal/terminalCommands.ts` — split, under 500 lines
- [ ] `browser/src/primitives/terminal/terminalCommands.nav.ts` — new file, nav commands
- [ ] `browser/src/primitives/terminal/TerminalApp.tsx` — restored interfaces
- [ ] `browser/src/primitives/terminal/useTerminal.ts` — restored options parameter
- [ ] `browser/src/primitives/terminal/types.ts` — add TerminalEggConfig, TerminalPaneState
- [ ] `browser/src/primitives/terminal/index.ts` — update exports

### Verification
- [ ] All 10 test files pass (80+ tests)
- [ ] No source file over 500 lines
- [ ] vitest runs clean with no errors

**16 deliverables total (10 test + 6 source modifications).**

## Response Requirements -- MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/YYYYMMDD-TASK-011A-RESPONSE.md`

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
