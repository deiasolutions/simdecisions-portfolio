# TASK-011: Terminal Primitive (P-04) — Port to browser/src/primitives/terminal/

## Objective

Port the Fr@nk terminal pane primitive from simdecisions-2 to `browser/src/primitives/terminal/`. This is the interactive terminal component: `hive>` prompt, scrolling output, slash commands, IR routing, Zone 2 response pane, 3-currency session ledger, and 3-mode deployment (standalone / pane / bus-connected). All files convert to TypeScript during port.

## Dependencies

- **TASK-005 (Relay Bus)** — must be complete. Bus dispatch for inter-pane messaging, clipboard bridge, IR routing.
- **TASK-008 (Shell Core)** — must be complete. Reducer types (`ShellState`, `ShellTreeNode`, `AppNode`) and utils (`findNode`) for pane-aware navigation and shell context.
- **TASK-007 (EGG System)** — must be complete. EGG config loading for pane configuration (`statusBarCurrencies`, `frankBehavior`).

## Source Files

Port from simdecisions-2:

| Source Path | Lines | Dest Path | What It Does |
|-------------|-------|-----------|-------------|
| `components/shell/useTerminal.ts` | 612 | `useTerminal.ts` | Main terminal hook: state, history, LLM calls, slash dispatch |
| `services/terminal/terminalCommands.ts` | 414 | `terminalCommands.ts` | Slash command dispatcher (13 commands, pane-aware) |
| `services/terminal/irRouting.ts` | 69 | `irRouting.ts` | IR → Designer routing (bus + sessionStorage) |
| `components/apps/TerminalApp.tsx` | 523 | `TerminalApp.tsx` | Reusable terminal in 3 modes (standalone/pane/bus) |
| `components/frank/TerminalOutput.tsx` | 214 | `TerminalOutput.tsx` | Scrolling output: banner/input/response/system/ir entries |
| `components/frank/TerminalPrompt.tsx` | 81 | `TerminalPrompt.tsx` | `hive>` prompt with arrow-key history + tab complete |
| `components/frank/TerminalResponsePane.tsx` | 52 | `TerminalResponsePane.tsx` | Zone 2: collapsible response pane (top/bottom/left/right/hidden) |
| `components/frank/TerminalStatusBar.tsx` | 99 | `TerminalStatusBar.tsx` | Model + 3-currency ledger + BYOK badge + efemera badge |
| `components/frank/frank-terminal.css` | 413 | `terminal.css` | All terminal styling (CSS variables only) |

**All source paths relative to:** `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\`

**Total source: ~2,477 lines across 9 files.**

## Port Rules

### 1. File Organization

All files go into `browser/src/primitives/terminal/`:

```
browser/src/primitives/terminal/
├── index.ts                    -- Public exports
├── types.ts                    -- TerminalEntry, SessionLedger, UseTerminalReturn, TerminalCommandContext, IRRoutingContext
├── useTerminal.ts              -- Main terminal hook
├── terminalCommands.ts         -- Slash command dispatcher
├── irRouting.ts                -- IR → Designer routing
├── TerminalApp.tsx             -- Reusable terminal component (3 modes)
├── TerminalOutput.tsx          -- Scrolling output display
├── TerminalPrompt.tsx          -- hive> prompt input
├── TerminalResponsePane.tsx    -- Zone 2 response pane
├── TerminalStatusBar.tsx       -- Status bar + 3-currency ledger
├── terminal.css                -- All styling
└── __tests__/
    ├── useTerminal.test.ts
    ├── terminalCommands.test.ts
    ├── terminalCommands.telemetry.test.ts
    ├── TerminalOutput.test.tsx
    ├── TerminalPrompt.test.tsx
    ├── TerminalResponsePane.test.tsx
    ├── TerminalStatusBar.test.tsx
    ├── TerminalStatusBar.currencies.test.tsx
    ├── TerminalApp.paneNav.test.tsx
    └── irRouting.test.ts
```

### 2. Extract Shared Types to types.ts

Create `types.ts` as the canonical type source for the terminal primitive:

```typescript
/** Terminal output entry types. */
export type TerminalEntry =
  | { type: 'banner'; content: string }
  | { type: 'input'; content: string }
  | { type: 'response'; content: string; metrics?: FrankMetrics }
  | { type: 'system'; content: string }
  | { type: 'ir'; content: string; ir: Record<string, unknown> };

/** Session ledger — 3-currency totals. */
export interface SessionLedger {
  total_clock_ms: number;
  total_cost_usd: number;
  total_carbon_g: number;
  total_input_tokens: number;
  total_output_tokens: number;
  message_count: number;
}

/** Context for slash command execution. */
export interface TerminalCommandContext {
  entries: TerminalEntry[];
  setEntries: (entries: TerminalEntry[]) => void;
  ledger: SessionLedger;
  setLedger: (ledger: SessionLedger) => void;
  isPane: boolean;
  bus: MessageBus | null;
  nodeId: string | null;
  navigate: (path: string) => void;
  user: { id: string; token: string } | null;
  conversationId: string | null;
  setConversationId: (id: string | null) => void;
  setGithubMcpConnected: (connected: boolean) => void;
}

/** Context for IR routing. */
export interface IRRoutingContext {
  bus: MessageBus | null;
  nodeId: string | null;
  setEntries: (fn: (prev: TerminalEntry[]) => TerminalEntry[]) => void;
  isPane: boolean;
}
```

Import `FrankMetrics` from `../../services/frank` (TASK-012). If TASK-012 is not yet complete, define a minimal `FrankMetrics` interface locally and mark it for replacement.

Import `MessageBus` from `../../infrastructure/relay_bus` (TASK-005).

### 3. Import Updates

| Old Import | New Import |
|------------|-----------|
| `stores/settingsStore` | `../../infrastructure/relay_bus` (settings via bus context) |
| `stores/authStore` | `../../infrastructure/relay_bus` (auth via bus context) |
| `services/llm/providers/*` | `../../services/frank` (TASK-012 provides sendMessage) |
| `components/frank/TerminalOutput` | `./TerminalOutput` |
| `components/frank/TerminalStatusBar` | `./TerminalStatusBar` |
| `components/frank/TerminalPrompt` | `./TerminalPrompt` |
| `components/frank/TerminalResponsePane` | `./TerminalResponsePane` |
| `hooks/usePaneContext` | `../../infrastructure/relay_bus` |
| `components/shell/shell.context` (useShell) | `../../infrastructure/relay_bus` |
| `components/shell/shell.utils` (findNode) | `../../shell/utils` (TASK-008) |
| `services/egg/eggConfig` | `../../eggs` (TASK-007) |
| `services/egg/defaultEggs` | `../../eggs` (TASK-007) |
| `services/terminal/terminalCommands` | `./terminalCommands` |
| `services/terminal/irRouting` | `./irRouting` |
| `services/frank/frankService` | `../../services/frank` (TASK-012) |
| `services/frank/chatApi` | `../../services/frank` (TASK-012) |
| `services/clipboardBridge` | Inline or stub — clipboard bridge is a future task |
| `hooks/useEfemeraSync` | Stub — efemera sync is a future task |
| `hooks/useTerminalPersistence` | Inline in useTerminal (localStorage read/write) |
| `hooks/useTerminalSession` | Inline in useTerminal (session state management) |
| `hooks/useTerminalAttachments` | Stub — file attachments are a future task |
| `hooks/useApplet` | Stub or import from shell if AppletShell is available (TASK-009) |

### 4. Stub Strategy for Missing Dependencies

These features depend on systems not yet ported. Stub them with no-op implementations:

| Feature | Old Module | Stub |
|---------|-----------|------|
| Efemera sync | `useEfemeraSync` | Return `{ connected: false, messages: [] }` |
| File attachments | `useTerminalAttachments` | Return `{ files: [], attach: noop, remove: noop }` |
| Clipboard bridge | `clipboardBridge` | Use `navigator.clipboard` directly (no cross-pane) |
| Telemetry service | `telemetryService` | Log to console, no persistence |
| Mode engine | `useModeEngine` | Return `{ currentMode: null }` |

Each stub must be a real function (not `// TODO`), return correct types, and be clearly marked with a `// STUB: <feature> — wire when <dependency> is ported` comment.

### 5. TerminalApp.tsx — Modularize if Over 500 Lines

The old TerminalApp.tsx is 523 lines. After port it may exceed 500. If so, extract:
- State restoration logic → `useTerminalRestore.ts` (~80 lines)
- Bus subscription setup → into useTerminal hook
- Feature registry → `terminalFeatures.ts` (~40 lines)

Each extracted file must be fully functional, not a stub.

### 6. CSS Rules

- All colors use `var(--sd-*)` — no hex, no rgb, no named colors
- Rename `frank-terminal.css` → `terminal.css`
- Keep all class names (`.frank-terminal`, `.terminal-*`) — renaming is cosmetic and out of scope
- Verify responsive breakpoint at 768px is preserved
- No emoji in CSS — emoji rendering (🔑, ⚠, 🟢, 🔴) stays in JSX

### 7. Slash Commands

Port all 13 commands from `terminalCommands.ts`:

| Command | Behavior | Notes |
|---------|----------|-------|
| `/clear` | Reset entries + ledger + localStorage | Creates new conversation if chatApi available |
| `/clipboard` | list/copy/paste via bus | Stub: use navigator.clipboard for now |
| `/designer` | Route IR to canvas pane | Pane: bus message. Standalone: sessionStorage + navigate |
| `/github` | GitHub MCP connect/disconnect/status | OAuth popup with 5-min timeout |
| `/help` | Show command list | Static text |
| `/history` | List conversations with resume codes | Calls chatApi.listConversations() |
| `/ledger` | Show 3-currency session totals | Formats clock/cost/carbon |
| `/logout` | Clear auth + navigate | Pane: system message. Standalone: navigate to /login |
| `/resume <code>` | Resume conversation by code | Calls chatApi.resumeConversation() |
| `/save` | Save current conversation | Calls chatApi.addMessage() |
| `/settings` | Open settings | Pane: system message. Standalone: navigate to /settings |
| `/telemetry` | View/set telemetry tier (0/1/2) | Stub: console.log for now |
| `/pane` | Set pane nickname | Bus dispatch |

### 8. Three-Mode Deployment

The terminal works in 3 modes. All must be preserved:

1. **Standalone** — full page at a route. Navigation via `window.location.href`. Full status bar with settings/close buttons.
2. **Pane** — inside HiveHostPanes. Navigation suppressed (system messages instead). Status bar respects `hideStatusBar` prop. Flex:1 layout.
3. **Bus-connected** — pane mode with bus integration. Publishes `terminal:open-in-designer`, subscribes to clipboard requests. Uses `usePaneContext()` for bus access.

### 9. Persistence Hierarchy

State restoration order (highest priority first):
1. `node.appState` — shell reducer pane state (if in pane mode)
2. localStorage — `sd:frank_entries`, `sd:frank_ledger`, `sd:frank_command_history`
3. Defaults — empty entries + banner, zero ledger, empty history

Efemera sync is stubbed (future task). When wired, it slots between 1 and 2.

## Test Requirements

### Port Existing Tests

Port these test files, updating imports:

| Old Test File | Lines | New Test File | What It Tests |
|---------------|-------|---------------|---------------|
| `useTerminal.test.ts` | 302 | `useTerminal.test.ts` | Hook init, state, slash commands, localStorage, clipboard, IR |
| `terminalCommands.test.ts` | 392 | `terminalCommands.test.ts` | All 13 slash commands, pane-aware nav, bus dispatch |
| `terminalCommands.telemetry.test.ts` | 155 | `terminalCommands.telemetry.test.ts` | /telemetry tier switching |
| `TerminalStatusBar.test.tsx` | 242 | `TerminalStatusBar.test.tsx` | BYOK badge, efemera badge, component order |
| `TerminalStatusBar.currencies.test.tsx` | 107 | `TerminalStatusBar.currencies.test.tsx` | statusBarCurrencies filtering |
| `TerminalResponsePane.test.tsx` | 238 | `TerminalResponsePane.test.tsx` | Position modes, collapse/expand, auto-scroll |
| `TerminalButtonHover.test.tsx` | 120 | `TerminalOutput.test.tsx` | IR buttons, CSS variable usage |
| `TerminalApp.paneNav.test.tsx` | 297 | `TerminalApp.paneNav.test.tsx` | Pane vs standalone command routing |

### New Tests

**TerminalPrompt.test.tsx:**
- [ ] Renders hive> prompt
- [ ] ArrowUp navigates history backward
- [ ] ArrowDown navigates history forward
- [ ] ArrowDown at index 0 clears input
- [ ] Tab triggers onTabComplete
- [ ] Enter triggers onSubmit
- [ ] Disabled prop disables input
- [ ] Autofocus when enabled

**irRouting.test.ts:**
- [ ] openInDesigner stores IR in sessionStorage (standalone)
- [ ] openInDesigner dispatches bus message (pane mode)
- [ ] copyToClipboard calls navigator.clipboard.writeText
- [ ] downloadIR creates blob + triggers download
- [ ] openInDesigner shows system message when no canvas pane

### Coverage Requirements

- [ ] All 13 slash commands tested with pane vs standalone behavior
- [ ] SessionLedger accumulation (clock, cost, carbon)
- [ ] TerminalEntry rendering for all 5 types (banner, input, response, system, ir)
- [ ] Tab completion for slash commands
- [ ] Command history (ArrowUp/Down, 100-item limit)
- [ ] localStorage persistence (save/load/clear)
- [ ] 3-currency display filtering via statusBarCurrencies
- [ ] Zone 2 position modes (top/bottom/left/right/hidden)
- [ ] IR action buttons (Open in Designer, Copy, Download)
- [ ] Spinner animation during loading

**Minimum: 80+ tests.**

## Source Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\shell\useTerminal.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\services\terminal\terminalCommands.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\services\terminal\irRouting.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\apps\TerminalApp.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\frank\TerminalOutput.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\frank\TerminalPrompt.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\frank\TerminalResponsePane.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\frank\TerminalStatusBar.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\frank\frank-terminal.css`

Test files to port:
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\shell\__tests__\useTerminal.test.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\services\terminal\__tests__\terminalCommands.test.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\services\terminal\__tests__\terminalCommands.telemetry.test.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\frank\__tests__\TerminalStatusBar.test.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\frank\__tests__\TerminalStatusBar.currencies.test.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\frank\__tests__\TerminalResponsePane.test.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\frank\__tests__\TerminalButtonHover.test.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\apps\__tests__\TerminalApp.paneNav.test.tsx`

Also check TASK-005, TASK-007, TASK-008 outputs for:
- `MessageBus` import path from relay_bus
- `usePaneContext()` / `useShell()` from relay_bus
- `findNode()` from shell/utils
- `NodeType` from eggs/types.ts
- EGG config loading functions

## What NOT to Build

- No Frank service / LLM interaction (TASK-012)
- No envelope parsing or dialect composition (TASK-012)
- No chatApi conversation persistence (TASK-012)
- No RAG EGG loader (future task)
- No Efemera sync (future task — stub only)
- No file attachments / paperclip (future task — stub only)
- No clipboard bridge cross-pane (future task — use navigator.clipboard)
- No shell reducer (TASK-008)
- No shell components (TASK-009)

## Constraints

- TypeScript strict mode
- All files under 500 lines (modularize TerminalApp if needed)
- No stubs meaning empty bodies — stubs for missing deps must be real functions with correct return types
- All CSS uses `var(--sd-*)` — no hex, no rgb, no named colors
- Test with vitest + @testing-library/react
- All state updates immutable

## Deliverables

### Source Files
- [ ] `browser/src/primitives/terminal/index.ts`
- [ ] `browser/src/primitives/terminal/types.ts`
- [ ] `browser/src/primitives/terminal/useTerminal.ts`
- [ ] `browser/src/primitives/terminal/terminalCommands.ts`
- [ ] `browser/src/primitives/terminal/irRouting.ts`
- [ ] `browser/src/primitives/terminal/TerminalApp.tsx`
- [ ] `browser/src/primitives/terminal/TerminalOutput.tsx`
- [ ] `browser/src/primitives/terminal/TerminalPrompt.tsx`
- [ ] `browser/src/primitives/terminal/TerminalResponsePane.tsx`
- [ ] `browser/src/primitives/terminal/TerminalStatusBar.tsx`
- [ ] `browser/src/primitives/terminal/terminal.css`

### Test Files
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

**21 deliverables total (11 source + 10 test).**

## Response Requirements -- MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/YYYYMMDD-TASK-011-RESPONSE.md`

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
