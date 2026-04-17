# SPEC-MON-001: Monaco Applet Component

## Priority
P1

## Objective
Build the core Monaco editor React component as a ShiftCenter applet with appType "code-editor", following the terminalAdapter pattern for registration. Monaco has zero direct filesystem access — all I/O is a separate concern (MON-002). This task builds the component shell only: AppletShell-wrapped editor, adapter registration, getValue/setValue via ref, dirty state tracking, and feature registry declaration.

## Files to Read First
- C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\terminalAdapter.tsx
- C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\useTerminal.ts
- C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\FlowDesigner.tsx

## Scope

Build these files under `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\code-editor\`:

1. **MonacoApplet.tsx** — AppletShell-wrapped React component
   - Mounts `@monaco-editor/react` (npm package)
   - Props: `language`, `theme`, `nodeId`, `config`
   - Forwards `onMount` ref for external control
   - Registers capability advertisement on mount
   - Declares feature registry (format document, toggle minimap, goto line, find)
   - Exposes `getValue()` / `setValue()` via ref for bus integration (MON-003)
   - No direct `fs`, `path`, or Node.js I/O anywhere

2. **MonacoApplet.css** — Scoped styles using `var(--sd-*)` only

3. **monacoAppletAdapter.ts** — Adapter registration following terminalAdapter.tsx pattern
   - Registers `appType: "code-editor"` in applet registry
   - Exports `{ appType, component, defaultConfig }`

4. **index.ts** — Barrel export

5. **Dirty state tracking** — `isDirty` boolean via ref, true on content change, false after save

6. **defaultConfig**: language typescript, theme vs-dark, minimap disabled, fontSize 14, wordWrap off, lineNumbers on

## Deliverables
1. C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\code-editor\MonacoApplet.tsx
2. C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\code-editor\MonacoApplet.css
3. C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\code-editor\monacoAppletAdapter.ts
4. C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\code-editor\index.ts
5. C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\code-editor\__tests__\MonacoApplet.test.tsx

## Acceptance Criteria
- [ ] MonacoApplet renders without errors in Vite dev server
- [ ] appType "code-editor" resolves correctly from adapter registry
- [ ] Feature registry populates AppletShell shortcuts popup
- [ ] isDirty toggles correctly on edit
- [ ] getValue() returns current editor content
- [ ] setValue(content) sets editor content without losing cursor position
- [ ] No direct filesystem imports present (grep check: no fs, path, require)
- [ ] All CSS uses var(--sd-*) only — no hex, no rgb(), no named colors
- [ ] All tests pass (minimum 8 tests)
- [ ] Build passes with npx vite build

## Response File
20260324-TASK-MON-001-RESPONSE.md
