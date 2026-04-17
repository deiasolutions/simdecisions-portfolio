# TASK-BL-958: Update Build Monitor EGG to Standard MenuBar Config

## Objective

Replace the deprecated `hideMenuBar` pattern in `build-monitor.egg.md` with the standard `menuBar: true` format to ensure the menu bar renders correctly.

## Context

The Build Monitor EGG currently uses an older `ui` block format with negative properties (`hideMenuBar: false`) but the shell initialization code in `browser/src/shell/useEggInit.ts` (line 93) only reads `ui.menuBar` directly:

```typescript
menuBar: ui.menuBar !== false && ui.menuBar !== undefined ? !!ui.menuBar : false,
```

This means the Build Monitor's menu bar may not render correctly because the shell doesn't handle the old `hideMenuBar` format.

Other EGGs (canvas2, chat, efemera) already use the standard format with positive properties.

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\build-monitor.egg.md` (current file with old format)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\canvas2.egg.md` (reference for standard pattern)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\useEggInit.ts` (to understand how ui config is read)

## Deliverables

- [ ] Replace the old `ui` block (lines 114-122) in `build-monitor.egg.md` with the standard format
- [ ] Set `menuBar: true` (equivalent to old `hideMenuBar: false`)
- [ ] Add `displayName: "Build Monitor"` to the ui config
- [ ] Preserve all other existing behavior (status bar hidden, tab bar hidden, activity bar hidden)
- [ ] Follow the exact pattern from `canvas2.egg.md`

## Target Configuration

Replace the current `ui` block:

```json
{
  "hideMenuBar": false,
  "hideStatusBar": true,
  "hideTabBar": true,
  "hideActivityBar": true,
  "statusBarCurrencies": []
}
```

With the standard format:

```json
{
  "masterTitleBar": false,
  "workspaceBar": false,
  "menuBar": true,
  "shellTabBar": false,
  "statusBar": false,
  "commandPalette": true
}
```

## Test Requirements

This is a **configuration-only change** with no code logic modifications. Per Rule 5, no tests are required for pure CSS and docs. EGG configuration files fall under this exception.

However, verify that:
- [ ] Shell tests still pass (these verify EGG loading)
- [ ] Build completes successfully

## Smoke Test Commands

```bash
# Shell tests pass
cd browser && npx vitest run src/shell/

# Build passes
cd browser && npx vite build
```

## Constraints

- No file over 500 lines (build-monitor.egg.md is ~160 lines)
- No stubs (this is pure config, no code)
- All file paths must be absolute
- Configuration-only change — no TypeScript/React code modifications

## Acceptance Criteria

- [ ] build-monitor.egg.md has a `ui` JSON block with `menuBar: true`
- [ ] The old `ui` block with `hideMenuBar` is completely removed
- [ ] MenuBar renders when loading build-monitor EGG
- [ ] displayName shows "Build Monitor" in the MenuBar app name position
- [ ] No regressions in other EGGs (shell tests pass)
- [ ] Build completes successfully

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260325-TASK-BL-958-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts (or "N/A - config-only per Rule 5")
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.
