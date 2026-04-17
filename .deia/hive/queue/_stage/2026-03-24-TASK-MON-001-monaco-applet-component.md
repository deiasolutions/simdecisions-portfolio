# TASK-MON-001: Monaco Applet Component

**Status:** QUEUED
**Wave:** Wave A
**Assigned To:** BEE-001
**Date:** 2026-03-24
**Depends On:** None
**Blocks:** TASK-MON-002, TASK-MON-003

---

## Context

Monaco Editor (MIT-licensed) is being added to the ShiftCenter Global Commons Applet Registry
as `appType: "code-editor"`. This task builds the core React component — the sandboxed,
AppletShell-wrapped Monaco editor primitive.

Reference specs:
- SPEC-MONACO-ADAPTER-001 (Monaco as standalone applet, zero direct filesystem access)
- SPEC-MONACO-BUS-001 (relay bus feedback loop)
- SDK-APP-BUILDER-v0.2.0 (AppletShell contract)

**Hard constraint:** Monaco has zero direct filesystem access. All I/O is through the Named
Volume System adapter (TASK-MON-002). This task wires the component shell only — file load/save
stubs are left for MON-002 to implement.

---

## Scope

Build `browser/src/primitives/code-editor/MonacoApplet.tsx` and supporting files.

### What to build

1. **MonacoApplet.tsx** — AppletShell-wrapped React component
   - Mounts `@monaco-editor/react` (already available via npm)
   - Props: `language`, `theme`, `nodeId`, `config`
   - Forwards `onMount` ref for external control
   - Registers capability advertisement on mount
   - Declares feature registry (keyboard shortcuts, toolbar actions)
   - Exposes `getValue()` / `setValue()` via ref for bus integration (MON-003)
   - No direct `fs`, `path`, or Node.js I/O anywhere in this file

2. **MonacoApplet.css** — Scoped styles
   - CSS variables: `var(--sd-*)` only. No hex, no rgb(), no named colors.
   - Editor fills pane 100% height minus AppletShell chrome

3. **monacoAppletAdapter.ts** — Adapter registration
   - Follows exact pattern of `terminalAdapter.tsx`
   - Registers `appType: "code-editor"` in the GC Applet Registry
   - Exports `{ appType, component, defaultConfig }`

4. **defaultConfig** shape:
   ```ts
   {
     language: "typescript",
     theme: "vs-dark",
     minimap: { enabled: false },
     fontSize: 14,
     wordWrap: "off",
     lineNumbers: "on"
   }
   ```

5. **Feature registry declaration** (for AppletShell shortcuts popup):
   ```ts
   [
     { id: "format-document", label: "Format Document", shortcut: "Shift+Alt+F" },
     { id: "toggle-minimap",  label: "Toggle Minimap",  shortcut: "Ctrl+Shift+M" },
     { id: "goto-line",       label: "Go to Line",      shortcut: "Ctrl+G" },
     { id: "find",            label: "Find",             shortcut: "Ctrl+F" }
   ]
   ```

6. **Dirty state tracking**
   - `isDirty` boolean exposed via ref
   - Set to `true` on any content change, `false` after save
   - AppletShell dirty indicator wired to this state

---

## File Locations

```
browser/src/primitives/code-editor/
  MonacoApplet.tsx          ← main component
  MonacoApplet.css          ← scoped styles
  monacoAppletAdapter.ts    ← registration
  index.ts                  ← barrel export
  __tests__/
    MonacoApplet.test.tsx   ← vitest tests (TDD — write first)
```

---

## Constraints

- No file over 500 lines
- CSS: `var(--sd-*)` only
- TypeScript strict mode
- No direct filesystem access (no `fs`, `path`, `require('fs')`)
- No `localStorage` or `sessionStorage`
- Follow `terminalAdapter.tsx` pattern exactly for registration
- TDD: write tests before implementation

---

## Acceptance Criteria

- [ ] MonacoApplet renders without errors in Vite dev server
- [ ] `appType: "code-editor"` resolves correctly from GC Applet Registry
- [ ] Feature registry populates AppletShell shortcuts popup
- [ ] `isDirty` toggles correctly on edit
- [ ] `getValue()` returns current editor content
- [ ] `setValue(content)` sets editor content without losing cursor position
- [ ] No direct filesystem imports present (grep check)
- [ ] All tests pass (minimum 8 tests)
- [ ] Build passes: `npx vite build`

---

## Response Requirements -- MANDATORY

Write response file: `.deia/hive/responses/20260324-TASK-MON-001-RESPONSE.md`

Required sections (all 8):
1. **Header** — task ID, title, status, model, date
2. **Files Modified** — full absolute paths
3. **What Was Done** — concrete changes, not intent
4. **Test Results** — file names, pass/fail counts
5. **Build Verification** — last 5 lines of `vite build` output
6. **Acceptance Criteria** — each item marked [x] or [ ] with explanation
7. **Clock / Cost / Carbon** — all three, never omit
8. **Issues / Follow-ups** — blockers, edge cases, recommendations

YAML frontmatter required:
```yaml
features_delivered: [code-editor-component, monaco-adapter-registration]
features_modified: []
features_broken: []
test_summary: "X/Y passing"
area_code: SHELL
```
