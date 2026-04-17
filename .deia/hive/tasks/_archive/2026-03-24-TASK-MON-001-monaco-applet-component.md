# TASK-MON-001: Monaco Applet Component

## Objective
Build the core Monaco editor React component as a ShiftCenter applet with `appType: "code-editor"`. This delivers the component shell ONLY — no filesystem I/O, no volume integration. All file operations and bus routing are separate tasks (MON-002, MON-003, MON-004).

## Context
Monaco editor is the VS Code editor component. We're wrapping it as a ShiftCenter primitive applet. The adapter pattern is identical to `terminalAdapter.tsx`. The component exposes getValue/setValue/isDirty via ref for external control. Feature registry declares keyboard shortcuts for AppletShell's shortcuts popup. NO direct filesystem access — all I/O comes later via volume adapter (MON-002).

## Files to Read First
1. **C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\terminalAdapter.tsx**
   - Shows adapter pattern: maps AppRendererProps → primitive component props
   - Uses ShellCtx for bus access
   - Manages settings modal

2. **C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\useTerminal.ts**
   - Shows ref-based external control pattern
   - Bus integration patterns (subscribe, send)
   - State management hook patterns

3. **C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\FlowDesigner.tsx**
   - Shows AppletShell usage patterns (lines 336-355: toolbar actions syndication)
   - Feature registry implementation (lines 381-431: menu items syndication)
   - Bus message handling (lines 358-371, 434-485)

## Deliverables
All files under `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\code-editor\`:

### 1. MonacoApplet.tsx (300-400 lines estimated)
- AppletShell-wrapped React component
- Mounts `@monaco-editor/react` (already in package.json)
- Props interface:
  ```typescript
  interface MonacoAppletProps {
    paneId: string;
    isActive: boolean;
    config: Record<string, unknown>;
    bus?: MessageBus | null;
  }
  ```
- Extract config values:
  - `language` (default: "typescript")
  - `theme` (default: "vs-dark")
  - `minimap` (default: { enabled: false })
  - `fontSize` (default: 14)
  - `wordWrap` (default: "off")
  - `lineNumbers` (default: "on")
- Use `useRef` for editor instance access
- Expose ref interface:
  ```typescript
  interface MonacoAppletRef {
    getValue: () => string;
    setValue: (content: string) => void;
    isDirty: boolean;
  }
  ```
- Track `isDirty` state: set true on content change, provide method to reset
- Capability advertisement on mount: send bus message `capability:advertise` with `{ type: 'code-editor', features: [...] }`
- Feature registry (for AppletShell shortcuts popup):
  ```typescript
  {
    'format-document': { label: 'Format Document', shortcut: 'Shift+Alt+F' },
    'toggle-minimap': { label: 'Toggle Minimap', shortcut: 'Ctrl+M' },
    'goto-line': { label: 'Go to Line', shortcut: 'Ctrl+G' },
    'find': { label: 'Find', shortcut: 'Ctrl+F' }
  }
  ```
- NO imports of `fs`, `path`, `require`, or any Node.js I/O modules
- File must stay under 500 lines (hard limit: 1,000)

### 2. MonacoApplet.css (50-100 lines estimated)
- Scoped class: `.monaco-applet-wrapper`
- NO hex colors (e.g., `#fff`)
- NO rgb/rgba (e.g., `rgb(255, 255, 255)`)
- NO named colors (e.g., `red`, `white`, `black`)
- ONLY `var(--sd-*)` CSS variables
- Example valid styles:
  ```css
  .monaco-applet-wrapper {
    background: var(--sd-bg-primary);
    color: var(--sd-text-primary);
    border: 1px solid var(--sd-border-muted);
  }
  ```

### 3. monacoAppletAdapter.ts (30-50 lines estimated)
- Follow terminalAdapter.tsx pattern
- Extract config from `AppRendererProps`
- Pass paneId, isActive, bus, config to MonacoApplet
- Register in applet registry:
  ```typescript
  export const monacoAppletAdapter = {
    appType: "code-editor",
    component: MonacoAppletAdapterComponent,
    defaultConfig: {
      language: "typescript",
      theme: "vs-dark",
      minimap: { enabled: false },
      fontSize: 14,
      wordWrap: "off",
      lineNumbers: "on"
    }
  };
  ```

### 4. index.ts (10 lines)
- Barrel export:
  ```typescript
  export { MonacoApplet } from './MonacoApplet';
  export { monacoAppletAdapter } from './monacoAppletAdapter';
  export type { MonacoAppletProps, MonacoAppletRef } from './MonacoApplet';
  ```

### 5. __tests__/MonacoApplet.test.tsx (200-300 lines, minimum 8 tests)
Test scenarios:
1. **Render test** — MonacoApplet renders without errors
2. **Adapter registration test** — appType "code-editor" resolves correctly
3. **Feature registry test** — feature list populates correctly
4. **isDirty toggle test** — isDirty = false initially, true after edit
5. **getValue test** — getValue() returns current editor content
6. **setValue test** — setValue(content) updates editor content
7. **CSS variable test** — MonacoApplet.css contains NO hex, rgb, or named colors (grep check)
8. **No filesystem imports test** — MonacoApplet.tsx contains NO fs, path, require imports (grep check)

Mock `@monaco-editor/react` in tests:
```typescript
vi.mock('@monaco-editor/react', () => ({
  default: ({ value, onChange }: any) => (
    <textarea
      data-testid="monaco-mock"
      value={value}
      onChange={(e) => onChange?.(e.target.value)}
    />
  )
}));
```

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All 8 tests pass
- [ ] Build passes: `cd browser && npx vite build`
- [ ] No regressions in existing tests: `cd browser && npx vitest run`

## Constraints
- **NO HARDCODED COLORS** — Rule 3 applies strictly. Only `var(--sd-*)` in CSS.
- **No file over 500 lines** — Modularize if approaching limit.
- **NO STUBS** — Every function fully implemented.
- **NO FILESYSTEM I/O** — No fs, path, require, or Node.js I/O anywhere in MonacoApplet.tsx. File operations come later in MON-002.
- **TDD required** — Write tests first, then implementation.

## Dependencies
- `@monaco-editor/react` (already in package.json)
- `monaco-editor` (peer dependency, already in package.json)
- React, AppletShell (existing primitives)
- MessageBus types from `infrastructure/relay_bus`

## Response Requirements — MANDATORY

When you finish your work, write a response file:
**C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260324-TASK-MON-001-RESPONSE.md**

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full absolute paths
3. **What Was Done** — bullet list of concrete changes (not intent)
4. **Test Results** — test files run, pass/fail counts, output summary
5. **Build Verification** — `npx vite build` output (last 5 lines), pass/fail
6. **Acceptance Criteria** — copy from task, mark [x] done or [ ] not done with explanation
7. **Clock / Cost / Carbon** — wall time (minutes), estimated USD, estimated CO2e (never omit any)
8. **Issues / Follow-ups** — edge cases, dependencies, recommended next tasks

DO NOT skip any section. If a section doesn't apply, write "N/A" with explanation.

## Acceptance Criteria
- [ ] MonacoApplet renders without errors in Vite dev server
- [ ] appType "code-editor" resolves correctly from adapter registry
- [ ] Feature registry populates AppletShell shortcuts popup (feature list declared and accessible)
- [ ] isDirty toggles correctly on edit (false initially, true after edit, resetable)
- [ ] getValue() returns current editor content
- [ ] setValue(content) sets editor content without losing cursor position
- [ ] No direct filesystem imports present (grep check: no fs, path, require in MonacoApplet.tsx)
- [ ] All CSS uses var(--sd-*) only — no hex, no rgb(), no named colors (grep check on MonacoApplet.css)
- [ ] All tests pass (minimum 8 tests)
- [ ] Build passes with `npx vite build`

## Notes
- Monaco editor already configured in Vite (if not, minimal config needed in vite.config.ts)
- This task is isolated — no integration with file system or volume adapter yet
- Follow terminalAdapter.tsx patterns exactly for consistency
- AppletShell will provide shortcuts popup automatically when features are declared
- Bus integration is minimal here — just capability advertisement on mount
- Full bus routing (text-patch messages, IR routing) comes later in MON-003

---

**Estimated Complexity:** Medium (M)
**Estimated Time:** 90-120 minutes
**Model Recommendation:** Haiku (well-defined patterns, focused scope)
