# BRIEFING: BL-958 Build Monitor MenuBar Standard

**Date:** 2026-03-25
**From:** Q33NR (Regent)
**To:** Q33N (Queen Coordinator)
**Spec:** SPEC-BL-958-build-monitor-menubar
**Model:** Haiku
**Priority:** P1

---

## Objective

Update `build-monitor.egg.md` to use the standard `ui` block format with `menuBar: true` instead of the deprecated `hideMenuBar: false` pattern.

---

## Context

### Problem

The Build Monitor EGG currently uses an older `ui` block format:

```json
{
  "hideMenuBar": false,
  "hideStatusBar": true,
  "hideTabBar": true,
  "hideActivityBar": true,
  "statusBarCurrencies": []
}
```

Other EGGs (canvas2, chat, efemera) use the standard format:

```json
{
  "masterTitleBar": false,
  "workspaceBar": false,
  "menuBar": true,
  "shellTabBar": false,
  "statusBar": true,
  "commandPalette": true
}
```

### Why This Matters

The shell initialization code in `browser/src/shell/useEggInit.ts` (line 93) reads `ui.menuBar` directly:

```typescript
menuBar: ui.menuBar !== false && ui.menuBar !== undefined ? !!ui.menuBar : false,
```

It does NOT handle the old `hideMenuBar` format. This means the Build Monitor's menu bar may not render correctly.

---

## Files to Read

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\build-monitor.egg.md` (file to modify)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\canvas2.egg.md` (reference for standard pattern)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\useEggInit.ts` (to understand how ui config is read)

---

## Task Requirements

Create ONE task file for a Haiku bee to:

1. Replace the old `ui` block in `build-monitor.egg.md` with the standard format
2. Set `menuBar: true` (equivalent to old `hideMenuBar: false`)
3. Set `displayName` to "Build Monitor" in the ui config
4. Preserve all other existing configuration (status bar hidden, tab bar hidden, etc.)
5. Follow the exact pattern from `canvas2.egg.md` or `chat.egg.md`

---

## Deliverables

- [ ] One task file: `YYYY-MM-DD-TASK-BL-958-BUILD-MONITOR-MENUBAR.md`
- [ ] Task specifies exact file path (absolute)
- [ ] Task includes the target `ui` block structure
- [ ] Task specifies the smoke test commands

---

## Acceptance Criteria (from spec)

- [ ] build-monitor.egg.md has a `ui` JSON block with menuBar: true
- [ ] The old `ui` block with `hideMenuBar` is removed
- [ ] MenuBar renders when loading build-monitor EGG
- [ ] displayName shows "Build Monitor" in the MenuBar app name position
- [ ] No regressions in other EGGs

---

## Smoke Test

```bash
# Shell tests pass
cd browser && npx vitest run src/shell/

# Build passes
cd browser && npx vite build
```

---

## Constraints

- No file over 500 lines (build-monitor.egg.md is ~160 lines)
- No stubs (this is pure config, no code)
- No tests required (config-only change, like CSS/docs)
- Follow Rule 3: CSS variables only (not applicable here - no CSS changes)

---

## Notes

This is a **configuration-only change**. No code logic. No tests required per Rule 5 exception for pure CSS and docs. The EGG file is configuration, similar to documentation.

The old `ui` block uses negative properties (`hideMenuBar: false`). The new standard uses positive properties (`menuBar: true`). They are semantically equivalent but the shell code only reads the new format.

---

## Next Steps

1. Q33N: Read the three files listed above
2. Q33N: Write one task file for Haiku bee
3. Q33N: Return to Q33NR for review (do NOT dispatch yet)
