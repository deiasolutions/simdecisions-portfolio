---
features_delivered: []
features_modified: []
features_broken: []
test_summary:
  total: 0
  passed: 0
  failed: 0
---

# RESEARCH: Menu Syndication, Command Registry Wiring, and Applet Bundle/Headless Patterns

| Field      | Value                                                     |
|------------|-----------------------------------------------------------|
| Task ID    | RESEARCH-MENU-SYNDICATION                                 |
| Title      | Menu Syndication, Command Registry & Headless Applet Audit|
| Status     | COMPLETE                                                  |
| Model      | claude-opus-4-6                                           |
| Date       | 2026-03-14                                                |

---

## 1. Files Modified

| Action  | File                                                                                      |
|---------|-------------------------------------------------------------------------------------------|
| Created | `.deia/hive/responses/20260314-RESEARCH-MENU-SYNDICATION-RESPONSE.md` (this file)         |

---

## 2. What Was Done

- Searched all `.ts`, `.tsx`, `.jsx`, `.js`, `.css` files for 10 term groups: MenuBar, commandRegistry, syndicateMenu/syndicate, appletMenu/category, headless, AppletShell, PaneMenu/hamburger, ChromeBtn, capabilities/addressable_as, shell.context.settings
- Read full source of `MenuBar.tsx`, `MenuBar.test.tsx`, `PaneMenu.tsx`, `PaneChrome.tsx`, `ChromeBtn.tsx`, `AppletShell.tsx`
- Read full source of `eggConfig.ts`, `defaultEggs.ts`, `eggResolver.ts`, `eggLoader.ts`, `eggInflater.ts`, `eggWiring.ts`, `parseEggMd.ts`, `types.ts`, `index.ts` (eggs barrel)
- Read commands blocks from `code.egg.md`, `chat.egg.md`, `efemera.egg.md`, `canvas.egg.md`
- Searched for `shell.context.settings` test files (none found)
- Searched for `CommandPalette`, `CommandRegistry`, `registerCommand` (zero matches)
- Searched for `category.*app` across all `.egg.md` files (found in code, efemera, canvas EGGs)
- Verified `eggWiring.ts` command wiring is entirely TODO/placeholder

---

## 3. Full Match Report

### MenuBar / menuBar / menu-bar

| File | Line(s) | Impl/Test | Summary |
|------|---------|-----------|---------|
| `browser/src/shell/components/MenuBar.tsx` | 1-423 | **Impl** | Full MenuBar component with hardcoded File/Edit/View/Help menus, layout presets, theme switcher, commands help modal, about modal |
| `browser/src/shell/components/__tests__/MenuBar.test.tsx` | 1-303 | **Test** | 20+ tests covering menu open/close, keyboard shortcuts, dispatch actions, modals |
| `browser/src/shell/components/Shell.tsx` | 12, 67 | **Impl** | Imports and conditionally renders `<MenuBar />` based on `uiConfig.menuBar` |
| `browser/src/shell/components/__tests__/Shell.test.tsx` | 68-70 | **Test** | Tests that menu-bar renders when `menuBar: true` |
| `browser/src/shell/components/__tests__/ShellChromeIntegration.test.tsx` | 50-78 | **Test** | Tests MenuBar visibility based on uiConfig |
| `browser/src/shell/useEggInit.ts` | 16, 37, 70 | **Impl** | `menuBar` field in `EggUiConfig`, defaults to `false`, read from EGG ui block |
| `browser/src/shell/components/shell.css` | 185 | **Impl** | `.menu-bar` CSS class definition |

### command_registry / commandRegistry / registerCommand / CommandRegistry

**Zero matches.** No command registry implementation exists in the codebase.

### syndicateMenu / syndicate / menuSyndication

| File | Line(s) | Impl/Test | Summary |
|------|---------|-----------|---------|
| `browser/src/eggs/eggConfig.ts` | 27-28 | **Impl** | `EggAppletProtocol` interface declares `syndicatesMenu?: boolean` and `syndicatesSettings?: boolean` |
| `browser/src/eggs/defaultEggs.ts` | 35-36 | **Impl** | `DEFAULT_TERMINAL_CLI_EGG` sets `syndicatesMenu: true, syndicatesSettings: true` |
| `browser/src/eggs/defaultEggs.ts` | 69-70 | **Impl** | `DEFAULT_TERMINAL_APP_EGG` sets `syndicatesMenu: false, syndicatesSettings: true` |
| `browser/src/eggs/defaultEggs.ts` | 103-104 | **Impl** | `DEFAULT_DESIGNER_APP_EGG` sets `syndicatesMenu: true, syndicatesSettings: true` |

**Note:** These flags are declared in the type system and set in default EGG configs, but **nothing reads or acts on them**. There is no code that checks `syndicatesMenu` to decide whether to surface menu items.

### appletMenu / appletsMenu / category "app"

| File | Line(s) | Impl/Test | Summary |
|------|---------|-----------|---------|
| `eggs/code.egg.md` | 278, 289, 300, 311, 322 | **Data** | 5 commands with `"category": "app"` (git.commit, git.push, git.branch.new, code.run, code.format) |
| `eggs/efemera.egg.md` | 117, 128, 150 | **Data** | 3 commands with `"category": "app"` (new-channel, new-dm, search) |
| `eggs/canvas.egg.md` | 143, 154, 165 | **Data** | 3 commands with `"category": "app"` (new-diagram, save, export-ir) |

**Note:** These commands are defined in `.egg.md` files and parsed by `parseEggMd()`, but **no code reads the `category` field or surfaces these commands in any menu or palette**. There is no CommandPalette component.

### headless / headlessApplet / bundlePane / parentPane

| File | Line(s) | Impl/Test | Summary |
|------|---------|-----------|---------|
| `browser/src/eggs/eggConfig.ts` | 48, 103 | **Impl** | `EggConfig` interface declares `headless: boolean`; validator checks `typeof cfg.headless !== 'boolean'` |
| `browser/src/eggs/defaultEggs.ts` | 13, 47, 81 | **Impl** | All three default EGGs set `headless: false` |
| `browser/src/eggs/__tests__/eggConfig.test.ts` | 14, 35, 46, 69, 116 | **Test** | Tests validate headless field parsing; confirms `DEFAULT_TERMINAL_CLI_EGG.headless === false` |

**Note:** The `headless` flag exists in the JSON-format `EggConfig` type (legacy). No code path checks this flag to run an applet without a visible pane. No `bundlePane` or `parentPane` concepts exist. The newer `.egg.md` format (`ParsedEgg`/`EggIR` types) does not include a `headless` field.

### AppletShell / appletShell / useApplet

| File | Line(s) | Impl/Test | Summary |
|------|---------|-----------|---------|
| `browser/src/shell/components/AppletShell.tsx` | 1-91 | **Impl** | Lifecycle wrapper providing notification modal and keyboard shortcuts popup. Exposes `notify()` and `showShortcuts()` on applet handle. |
| `browser/src/shell/components/__tests__/AppletShell.test.tsx` | 1-77 | **Test** | Tests rendering children, CSS class, lifecycle hook calls, notifications, shortcuts display |

**Note:** `AppletShell` does not interact with any command registry or menu syndication system. It manages notifications and feature listing via `applet.registry.listFeatures()`, but that registry is a simple feature/shortcut list, not a command registry.

### PaneMenu / paneMenu / hamburger

| File | Line(s) | Impl/Test | Summary |
|------|---------|-----------|---------|
| `browser/src/shell/components/PaneMenu.tsx` | 1-171 | **Impl** | Hamburger menu rendered via portal with layout actions: Add Tab, Split, Flip, Maximize, Swap, Lock, Close |
| `browser/src/shell/components/PaneChrome.tsx` | 14, 129 | **Impl** | Imports and renders `<PaneMenu>` in every pane title bar |
| `browser/src/shell/components/__tests__/PaneMenu.test.tsx` | 1-295 | **Test** | Extensive tests for all menu items, hamburger button, portal rendering, swap state |

**Note:** PaneMenu is purely shell layout actions. It does not source items from any command registry or applet. Items are hardcoded in the component.

### ChromeBtn / chrome-btn

| File | Line(s) | Impl/Test | Summary |
|------|---------|-----------|---------|
| `browser/src/shell/components/ChromeBtn.tsx` | 1-43 | **Impl** | Atomic icon button with hover/active states, used in PaneChrome and PaneMenu |
| `browser/src/shell/components/PaneChrome.tsx` | 13, 159-182 | **Impl** | Uses ChromeBtn for audio mute, bus mute, maximize/close controls |
| `browser/src/shell/components/PaneMenu.tsx` | 12, 126 | **Impl** | Uses ChromeBtn for hamburger toggle button |

### capabilities / registerCapabilities / addressable_as

| File | Line(s) | Impl/Test | Summary |
|------|---------|-----------|---------|
| `browser/src/eggs/eggConfig.ts` | 29-32 | **Impl** | `EggAppletProtocol.capabilities` with `produces?: string[]` and `consumes?: string[]` |
| `browser/src/eggs/defaultEggs.ts` | 37-40, 71-74, 105-108 | **Impl** | Default EGGs declare produces/consumes arrays (e.g., `['ir', 'to_user', 'to_markdown']`) |
| `browser/src/infrastructure/relay_bus/permissionsResolver.ts` | 9 | **Impl** | Comment mentions "no new capabilities" in intersection logic |
| `browser/src/infrastructure/relay_bus/__tests__/permissionsResolver.test.ts` | 229 | **Test** | Test section header about node permissions not widening capabilities |

**Note:** `capabilities` are declared in the EggAppletProtocol type but **no runtime code reads produces/consumes to route bus messages or filter subscriptions**. `addressable_as` does not appear anywhere. `registerCapabilities` does not appear anywhere.

### shell.context.settings

**Zero matches.** No file named `shell.context.settings` or containing this pattern exists in the codebase. The old simdecisions-2 `shell.context.js` was ported to `messageBus.ts` (line 3 reference comment), but there is no settings sub-module.

---

## 4. Test Results

| Test File | Exists? | Notes |
|-----------|---------|-------|
| `browser/src/shell/components/__tests__/MenuBar.test.tsx` | **YES** | 20+ tests, covers menu rendering, keyboard shortcuts, dispatch, modals, terminal integration |
| `shell.context.settings.test.jsx` | **NO** | Does not exist anywhere in the repo. No file matching `*settings*test*` in the shell directory. |

Tests were not executed as part of this research task. Existence was verified by glob search.

---

## 5. Build Verification

N/A -- research-only task. No code was created or modified (only this response file).

---

## 6. Acceptance Criteria -- Six Questions Answered

### Q1: Does MenuBar.tsx render items from the command registry, or is it hardcoded?

**Hardcoded.** `MenuBar.tsx` (lines 180-376) renders four static top-level menus (File, Edit, View, Help) with entirely hardcoded items. File has "New Tab > Hive/Designer/Browser", "Close Tab", "Settings". Edit has Cut/Copy/Paste/Clear Terminal. View has Layout presets and Theme picker. Help has Commands and About. There is no import of any command registry, no dynamic item generation, and no reading of the EGG `commands` block. The component sources its actions directly from inline handler functions and `useShell()` dispatch.

### Q2: Do commands with category "app" appear anywhere in a menu surface, or only in Command Palette?

**Neither.** Commands with `"category": "app"` are defined in `.egg.md` files (code, efemera, canvas EGGs) and parsed into the `commands` array by `parseEggMd()`. They are carried through inflation into `EggIR.commands`. However:
- There is **no CommandPalette component** in the codebase (zero search matches).
- There is **no code that reads `EggIR.commands`** to populate any UI.
- `eggWiring.ts` line 39-46 has a TODO placeholder: `if (egg.commands && bus) { console.log(...) }` -- the wiring is unimplemented.
- Commands with `category: "app"` are **dead data** -- parsed, inflated, never rendered.

### Q3: Is there any code path where an applet registers menu items that bubble up to a parent pane?

**No.** There are two menu syndication signals in the type system:
1. `EggAppletProtocol.syndicatesMenu` (boolean flag in `eggConfig.ts` line 27) -- set on default EGGs but never read by any rendering code.
2. `AppletShell.tsx` exposes `applet.registry.listFeatures()` for a shortcuts popup, but this is a flat feature/shortcut list, not menu items, and it does not propagate upward.

No code path exists where an applet's commands or menu entries flow up to `MenuBar`, `PaneMenu`, `PaneChrome`, or any other parent container. The `syndicatesMenu: true` flag on `DEFAULT_TERMINAL_CLI_EGG` and `DEFAULT_DESIGNER_APP_EGG` is a declaration of intent with no implementation behind it.

### Q4: Does any applet run headless (no visible pane) while participating on the bus?

**No.** The `headless: boolean` field exists in the legacy JSON `EggConfig` type (line 48). All three default EGGs set it to `false`. The newer `ParsedEgg`/`EggIR` types do not include a `headless` field at all. No code path checks `headless` to instantiate an applet without a pane. There is no mechanism for a bus-connected applet to exist without being mounted in the layout tree.

### Q5: Do MenuBar.test.tsx and shell.context.settings.test.jsx pass, fail, or exist at all?

- **MenuBar.test.tsx EXISTS** at `browser/src/shell/components/__tests__/MenuBar.test.tsx` (303 lines, 20+ test cases). Tests were not executed in this research session, but the file is present, well-structured, and consistent with the implementation. Per the session memory, browser tests are reported as "87 files, 1122 passed, 0 failures" as of the latest run.
- **shell.context.settings.test.jsx DOES NOT EXIST.** No file with this name or any similar pattern was found. The `shell.context.js` from simdecisions-2 was ported to `messageBus.ts`, but no settings sub-module or test exists.

### Q6: Is there a commands block parser in the EGG loader that feeds the command registry?

**Partially.** The **parser exists** but the **registry does not**.

The pipeline:
1. `parseEggMd.ts` (line 136): Lists `'commands'` as a recognized JSON block tag. Parses it into `ParsedEgg.commands: unknown[]`.
2. `eggInflater.ts` (line 229): Passes `commands` through to `EggIR.commands` unchanged.
3. `eggWiring.ts` (lines 39-46): **TODO placeholder.** Contains `if (egg.commands && bus) { console.log(...) }` with commented-out `bus.emit('command:register', command)`. The comment on line 33 says "Command Registry (future task)".

So: parsing works, inflation works, but the terminal step -- registering commands into a registry and making them available to UI surfaces -- is unimplemented.

---

## 7. Clock / Cost / Carbon

| Metric  | Value         |
|---------|---------------|
| Clock   | ~15 min       |
| Cost    | Research task  |
| Carbon  | Minimal       |

---

## 8. Issues / Follow-ups

### Gaps Found

1. **No Command Registry exists.** Zero matches for `CommandRegistry`, `commandRegistry`, `registerCommand` anywhere in the codebase. The EGG wiring explicitly lists "Command Registry (future task)" as a dependency. This is the critical missing piece.

2. **No Command Palette exists.** Zero matches for `CommandPalette`. Commands defined in `.egg.md` files have no UI surface to appear in.

3. **`syndicatesMenu` flag is dead.** Declared in `EggAppletProtocol`, set on default EGGs, but nothing reads it. No menu syndication pipeline exists.

4. **`capabilities.produces/consumes` are dead.** Declared in EGG configs but no runtime code uses them for bus routing or filtering.

5. **`headless` flag is dead (legacy only).** Present in the old JSON `EggConfig` type but not in the newer `ParsedEgg`/`EggIR` types. No runtime check exists.

6. **MenuBar is entirely hardcoded.** Four static menus with no extensibility. Cannot receive items from EGG commands, applet syndication, or a command registry.

7. **`shell.context.settings` does not exist.** The old simdecisions-2 module was partially ported to `messageBus.ts` but no settings sub-context was created.

### Recommended Next Tasks

| Priority | Task | Description |
|----------|------|-------------|
| P1 | **Create CommandRegistry service** | Central registry that holds command definitions from EGG `commands` blocks. Must support register/unregister/query by category/scope/tag. |
| P1 | **Wire eggWiring.ts commands to CommandRegistry** | Replace the TODO in `wireEgg()` with actual command registration calls. |
| P2 | **Create CommandPalette component** | Ctrl+Shift+P surface that queries CommandRegistry and displays filtered commands. |
| P2 | **Implement menu syndication pipeline** | When `syndicatesMenu: true`, commands with `category: "app"` should appear in a dynamic section of MenuBar or PaneMenu. |
| P3 | **Make MenuBar data-driven** | Refactor MenuBar to source items from CommandRegistry (filtered by `category: "view"`, `category: "file"`, etc.) instead of hardcoding. |
| P3 | **Implement headless applet support** | Allow EGGs to declare panes that participate on the bus without rendering. Requires changes to layout tree and shell reducer. |
| P3 | **Wire capabilities produces/consumes** | Use the declared capabilities for bus message routing and permission checks. |
