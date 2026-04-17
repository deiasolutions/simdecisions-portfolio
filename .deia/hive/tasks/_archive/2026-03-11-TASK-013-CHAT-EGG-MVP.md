# TASK-013: chat.egg.md — First Product MVP

## Objective

Wire everything together into a running application. Create the chat.egg.md product definition, the app entry point (Vite + React), app registration, and EGG-to-shell initialization. This is the first product — an AI chat interface powered by the terminal primitive and Frank service.

## Context

All building blocks are built and tested:

| Component | Task | Tests | Location |
|-----------|------|-------|----------|
| Terminal Primitive | TASK-011 | 49 passing | `browser/src/primitives/terminal/` |
| Frank Service (LLM + Envelope) | TASK-012 | 82 passing | `browser/src/services/frank/` |
| SDEditor (Text Pane) | TASK-010 | 65 passing | `browser/src/primitives/text-pane/` |
| EGG System (Parser, Inflater) | TASK-007 | 105 passing | `browser/src/eggs/` |
| Shell Core (Reducer, Utils) | TASK-008 | 231 passing | `browser/src/shell/` |
| Shell Renderer (Components) | TASK-009 | 79 passing | `browser/src/shell/components/` |
| Relay Bus | TASK-005 | 115 passing | `browser/src/infrastructure/relay_bus/` |
| Gate Enforcer (Browser) | TASK-006 | 17 passing | `browser/src/infrastructure/gate_enforcer/` |

**What's missing:** The product composition layer — the .egg.md file, the app entry point, and the wiring code that snaps these Lego blocks together.

## Files to Read First

Read these to understand the integration points:

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\Shell.tsx` (89 lines) — root shell frame
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\appRegistry.ts` (33 lines) — registerApp/getAppRenderer
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\PaneContent.tsx` (49 lines) — routes appType to renderer
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\types.ts` (243 lines) — ShellState, ShellAction, AppNode
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\eggs\eggLoader.ts` (30 lines) — loadEggFromMarkdown/loadEggFromString
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\eggs\eggInflater.ts` (273 lines) — inflateEgg
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\eggs\eggResolver.ts` (112 lines) — resolveCurrentEgg
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\eggs\eggWiring.ts` — wireEgg side effects
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\eggs\types.ts` (130 lines) — EggIR, ParsedEgg, EggLayoutNode
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\index.ts` (36 lines) — terminal exports
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\TerminalApp.tsx` (~160 lines) — terminal component props
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\frank\index.ts` — frank service exports
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\shell-themes.css` — CSS custom properties (--sd-*)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\package.json` — current dependencies
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\tsconfig.json` — TypeScript config

## Architecture

### Key Insight: TerminalApp IS the Chat UI

TerminalApp already has:
- `hive>` prompt with history and tab completion
- LLM calls via Frank service (direct mode, BYOK)
- Scrolling output with response rendering
- 3-currency metrics in status bar
- Slash commands (/clear, /help, /ledger, /save, /resume, /history, etc.)
- Zone 2 response pane
- localStorage persistence

**There is no separate ChatApp needed.** The terminal primitive IS the chat component. The chat product is: TerminalApp registered as appType `'terminal'` in the shell's app registry, composed via chat.egg.md into a layout.

### Initialization Flow

```
1. browser/index.html loads browser/src/main.tsx
2. main.tsx:
   a. Import and call registerApps() — registers terminal + text-pane in appRegistry
   b. Import global CSS (shell-themes.css)
   c. Render <App /> into #root
3. App.tsx:
   a. Call resolveCurrentEgg() to get egg ID (from ?egg= param or hostname)
   b. Call loadEggFromMarkdown(`/eggs/${eggId}.egg.md`) to get EggIR
   c. Convert EggIR.layout to ShellState (inflate layout tree into shell reducer initial state)
   d. Render <Shell /> with the inflated state
4. Shell.tsx renders the layout tree:
   a. ShellNodeRenderer routes split → SplitContainer, app → PaneChrome+AppFrame
   b. PaneContent calls getAppRenderer('terminal') → TerminalApp
   c. TerminalApp renders with config from AppNode.appConfig
```

### App Registry Bridge

The bridge between EGG layout and shell components is the **AppRendererProps** interface:

```typescript
// From appRegistry.ts
interface AppRendererProps {
  paneId: string;
  isActive: boolean;
  config: Record<string, unknown>;
}
```

Each primitive must export a wrapper that accepts AppRendererProps and maps to its own props. Create thin adapter components:

```typescript
// browser/src/apps/terminalAdapter.ts
function TerminalAdapter({ paneId, isActive, config }: AppRendererProps) {
  const { bus } = useShell(); // or from ShellCtx
  return (
    <TerminalApp
      nodeId={paneId}
      isActive={isActive}
      bus={bus}
      llmProvider={config.llmProvider as string}
      apiKey={localStorage.getItem('sd-api-key') || undefined}
      statusBarCurrencies={config.statusBarCurrencies as string[]}
      promptLabel={config.promptLabel as { text: string; cssClass?: string }}
      eggConfig={config as TerminalEggConfig}
    />
  );
}
registerApp('terminal', TerminalAdapter);
```

### EGG Layout → Shell State

The EGG layout tree uses `EggLayoutNode` types (pane, split, tab-group). The shell reducer expects `ShellTreeNode` types (app, split, tabbed). Need a function to convert:

```typescript
function eggLayoutToShellTree(eggLayout: EggLayoutNode): ShellTreeNode {
  // Recursively convert EGG nodes to shell nodes
  // EGG 'pane' → Shell AppNode (with appType, appConfig from EGG config)
  // EGG 'split' → Shell SplitNode (with direction, ratio, children)
}
```

The shell types.ts already has `eggNodeToShellNode()` helper for type mapping.

## Deliverables

### Product Definition (1 file)

- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\chat.egg.md`

The chat.egg.md should define:
- **Frontmatter:** egg: chat, version: 1.0.0, displayName: "Chat", description, defaultRoute: /chat
- **Layout block:** Single terminal pane (full screen, no split for MVP). The terminal already has Zone 2 built in.
- **UI block:** Theme: default (dark purple from shell-themes.css)
- **Commands block:** /new (new conversation), plus all terminal slash commands are built-in
- **Startup block:** sessionRestore: true, sessionRestoreScope: perUser
- **Permissions block:** basic chat permissions

### App Entry Point (4 files)

- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\index.html` — HTML with `<div id="root">`, loads main.tsx via Vite
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\main.tsx` — Registers apps, imports CSS, renders App
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\App.tsx` — Root component: resolves EGG, inflates layout, renders Shell
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\vite.config.ts` — Vite config with React plugin, dev server

### App Adapters + Registration (3 files)

- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\terminalAdapter.tsx` — Maps AppRendererProps → TerminalApp props
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\textPaneAdapter.tsx` — Maps AppRendererProps → SDEditor props
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\index.ts` — Calls registerApp for both

### EGG → Shell Bridge (2 files)

- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\eggToShell.ts` — Converts EggIR.layout → ShellState initial state (inflate EGG layout tree into shell reducer's BranchesRoot)
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\useEggInit.ts` — React hook: resolves EGG, loads .egg.md, inflates, returns ShellState (used by App.tsx)

### Test Files (5 files)

- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\__tests__\terminalAdapter.test.tsx` — 6 tests
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\__tests__\textPaneAdapter.test.tsx` — 4 tests
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\__tests__\eggToShell.test.ts` — 10 tests
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\__tests__\useEggInit.test.ts` — 6 tests
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\__tests__\App.test.tsx` — 5 tests

### Package Updates (1 file)

- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\package.json` — Add vite, @vitejs/plugin-react, add dev/build/preview scripts

**Total: 16 deliverables (1 egg + 4 entry + 3 adapters + 2 bridge + 5 tests + 1 package update)**

## Test Requirements (~31 tests minimum)

### eggToShell.test.ts (~10 tests)
- [ ] Converts single pane EGG layout to AppNode
- [ ] Converts horizontal split with 2 panes to SplitNode with 2 AppNode children
- [ ] Converts vertical split to SplitNode with correct direction
- [ ] Preserves ratio from EGG split node
- [ ] Maps EGG pane appType to AppNode appType
- [ ] Maps EGG pane config to AppNode appConfig
- [ ] Generates unique IDs for shell nodes
- [ ] Sets default LoadState.HOT for all app nodes
- [ ] Handles nested splits (split inside split)
- [ ] Returns valid BranchesRoot with layout, empty float/pinned/spotlight

### useEggInit.test.ts (~6 tests)
- [ ] Returns loading state initially
- [ ] Returns ShellState after EGG loads
- [ ] Falls back to 'home' egg if resolution fails
- [ ] Handles fetch failure gracefully (renders error state)
- [ ] Passes egg ID from URL param ?egg=chat
- [ ] Calls loadEggFromMarkdown with correct path

### terminalAdapter.test.tsx (~6 tests)
- [ ] Renders TerminalApp with paneId passed as nodeId
- [ ] Passes isActive to TerminalApp
- [ ] Maps config.llmProvider to TerminalApp llmProvider prop
- [ ] Maps config.statusBarCurrencies to TerminalApp prop
- [ ] Reads API key from localStorage
- [ ] Passes bus from ShellCtx

### textPaneAdapter.test.tsx (~4 tests)
- [ ] Renders SDEditor with paneId
- [ ] Passes config.format to SDEditor
- [ ] Passes isActive to SDEditor
- [ ] Renders without errors when config is empty

### App.test.tsx (~5 tests)
- [ ] Renders without crashing
- [ ] Shows loading state while EGG loads
- [ ] Renders Shell after EGG loads
- [ ] Applies hhp-root class for theme variables
- [ ] Shows error message if EGG fails to load

## Constraints

- TypeScript strict mode
- All files under 500 lines
- CSS: var(--sd-*) only — no hex/rgb/named colors in new files
- vitest + @testing-library/react
- No stubs — every function fully implemented
- Mock external dependencies (fetch for EGG loading)
- Do NOT modify any existing source files except browser/package.json
- Vite config: React plugin, dev server on port 5173
- API key read from localStorage key `'sd-api-key'` (user sets it via /settings command in terminal)

## Response Requirements -- MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/YYYYMMDD-TASK-013-RESPONSE.md`

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
