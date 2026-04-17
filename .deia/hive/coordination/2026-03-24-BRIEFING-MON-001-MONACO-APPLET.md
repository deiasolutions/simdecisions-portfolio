# BRIEFING: MON-001 Monaco Applet Component

**Date:** 2026-03-24
**From:** Q33NR
**To:** Q33N
**Model:** Sonnet
**Priority:** P1

---

## Objective

Build the core Monaco editor React component as a ShiftCenter applet with `appType: "code-editor"`. This is the first of four tasks (MON-001 through MON-004) to build a complete Code Editor EGG. This task builds ONLY the applet component shell — no filesystem I/O, no volume integration, no bus routing. Those are separate concerns.

---

## Context from Spec

**Spec ID:** SPEC-MON-001
**Deliverable:** Monaco editor React component registered as applet with `appType: "code-editor"`

The spec explicitly states:
- "Monaco has zero direct filesystem access — all I/O is a separate concern (MON-002)"
- "This task builds the component shell only"
- Follow the `terminalAdapter` pattern for registration
- Feature registry declaration (format document, toggle minimap, goto line, find)
- Dirty state tracking via ref
- getValue/setValue via ref for bus integration

---

## Reference Files (Absolute Paths)

These files demonstrate the patterns to follow:

1. **C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\terminalAdapter.tsx**
   - Shows adapter pattern: maps AppRendererProps → primitive component props
   - Uses ShellCtx for bus access
   - Manages settings modal
   - Exports adapter for registry

2. **C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\useTerminal.ts**
   - Shows ref-based external control pattern
   - Bus integration patterns
   - State management hook patterns

3. **C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\FlowDesigner.tsx**
   - Shows AppletShell usage patterns
   - Feature registry implementation
   - Bus message handling

---

## Scope — What Q33N Must Deliver

### File Structure

Create these files under `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\code-editor\`:

1. **MonacoApplet.tsx** (300-400 lines estimated)
   - AppletShell-wrapped React component
   - Mounts `@monaco-editor/react` (npm package already in dependencies)
   - Props: `language`, `theme`, `nodeId`, `config`
   - Forwards `onMount` ref for external control
   - Registers capability advertisement on mount
   - Declares feature registry (format document, toggle minimap, goto line, find)
   - Exposes `getValue()` / `setValue()` via ref
   - Dirty state tracking (`isDirty` boolean via ref)
   - NO direct `fs`, `path`, or Node.js I/O anywhere

2. **MonacoApplet.css** (50-100 lines estimated)
   - Scoped styles using `var(--sd-*)` ONLY
   - NO hex, NO rgb(), NO named colors (Rule 3)

3. **monacoAppletAdapter.ts** (30-50 lines estimated)
   - Adapter registration following terminalAdapter.tsx pattern
   - Registers `appType: "code-editor"` in applet registry
   - Exports `{ appType, component, defaultConfig }`

4. **index.ts** (10 lines)
   - Barrel export

5. **__tests__/MonacoApplet.test.tsx** (200-300 lines, minimum 8 tests)
   - Test render without errors
   - Test adapter registration
   - Test feature registry population
   - Test isDirty toggle on edit
   - Test getValue() returns content
   - Test setValue() sets content
   - Test no filesystem imports (grep check)
   - Test CSS variable usage only

---

## defaultConfig Values

```typescript
{
  language: "typescript",
  theme: "vs-dark",
  minimap: { enabled: false },
  fontSize: 14,
  wordWrap: "off",
  lineNumbers: "on"
}
```

---

## Acceptance Criteria (from Spec)

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

---

## Constraints (10 Hard Rules)

- **Rule 3:** NO HARDCODED COLORS. Only CSS variables (`var(--sd-*)`). No hex, no rgb(), no named colors.
- **Rule 4:** No file over 500 lines. Hard limit: 1,000.
- **Rule 5:** TDD. Tests first, then implementation.
- **Rule 6:** NO STUBS. Every function fully implemented.

---

## Task File Requirements

When you write the task file for the bee, ensure:

1. **Absolute file paths** for all deliverables
2. **Test requirements section** with specific scenarios:
   - Render test
   - Adapter registration test
   - Feature registry test
   - Dirty state test
   - getValue/setValue tests
   - CSS variable validation test
   - No filesystem imports test
   - Build verification test

3. **Response file requirement** — bee must write:
   `.deia/hive/responses/20260324-TASK-MON-001-RESPONSE.md`
   with all 8 sections

4. **CSS constraint explicitly called out** — no hex, no rgb(), no named colors

5. **No filesystem I/O constraint** — grep check for fs, path, require imports

6. **Ref interface specification** — getValue(), setValue(), isDirty exposed via ref

---

## Dependencies

- `@monaco-editor/react` (already in package.json)
- `monaco-editor` (peer dependency, already in package.json)
- React, AppletShell (existing primitives)

---

## Q33N: Your Next Steps

1. Read the three reference files (absolute paths above)
2. Write task file: `.deia/hive/tasks/2026-03-24-TASK-MON-001-monaco-applet-component.md`
3. Return to Q33NR for review
4. After approval, dispatch bee with:
   ```bash
   python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-24-TASK-MON-001-monaco-applet-component.md --model haiku --role bee --inject-boot
   ```

---

## Expected Bee: Haiku (cost-efficient for focused implementation task)

This is a well-defined, focused implementation task with clear patterns to follow. Haiku is appropriate.

---

**END BRIEFING**
