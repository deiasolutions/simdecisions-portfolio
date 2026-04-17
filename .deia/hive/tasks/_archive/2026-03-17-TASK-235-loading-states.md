# TASK-235: Pane Loading States (W4 — 4.7)

## Objective

Add a loading spinner to panes while their applet content is loading. Users should see visual feedback during component mount, not a blank pane followed by sudden content pop-in.

## Context

**Wave 4 Product Polish** — Task 4.7.

Terminal already has a loading spinner (`TerminalOutput.tsx` lines 23-43 with `spinnerChars = ['/', '-', '\\', '|']` rotating every 150ms). This task adds **pane-level** loading state — shown when an appType is assigned but the applet component hasn't finished mounting yet.

The shell uses a `LoadState` enum: COLD (not instantiated), WARM (invisible), HOT (visible). This task adds a **mounting state indicator** that shows between when HOT state is set and when the applet component actually renders.

**Key architectural insight:**
- `ShellNodeRenderer.tsx` checks `appNode.loadState` and decides what to render
- `AppFrame.tsx` loads the app component from the registry via `getAppRenderer(node.appType)`
- When `appType !== 'empty'` and component hasn't mounted yet, we need to show a loading indicator
- Reference spinner: `TerminalOutput.tsx` lines 23-43, 86-92

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\ShellNodeRenderer.tsx` — where AppNodes are rendered (279-285: HOT state rendering)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\AppFrame.tsx` — where applet components are loaded
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\TerminalOutput.tsx` — reference spinner implementation (lines 23-43, 86-92)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\types.ts` — LoadState enum definition

## Deliverables

### 1. PaneLoader Component

Create: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\PaneLoader.tsx`

**Requirements:**
- Centered spinner animation (reuse terminal spinner pattern: `['/', '-', '\\', '|']` cycling every 150ms)
- Text: "Loading..." in `var(--sd-text-muted)`
- Spinner color: `var(--sd-purple)`
- Centered vertically and horizontally in pane
- Only CSS variables for colors (no hex, no rgb())
- Component structure:
  ```tsx
  export function PaneLoader(): React.ReactElement
  ```

### 2. Mounting State Detection in AppFrame

Modify: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\AppFrame.tsx`

**Requirements:**
- Track mounting state with `useState` + `useEffect`
- Show `<PaneLoader />` if component is not mounted yet AND appType is not 'empty'
- Add a delay (100ms) before showing loader to prevent flash on fast mounts
- When `Renderer` is found, wrap in mounting detection:
  ```tsx
  const [isMounted, setIsMounted] = useState(false);
  const [showLoader, setShowLoader] = useState(false);

  useEffect(() => {
    const delayTimer = setTimeout(() => setShowLoader(true), 100);
    const mountTimer = setTimeout(() => setIsMounted(true), 0);
    return () => { clearTimeout(delayTimer); clearTimeout(mountTimer); };
  }, [node.appType]);

  if (!isMounted && showLoader) return <PaneLoader />;
  ```
- Loader should disappear when component renders
- Errors should be handled by existing `PaneErrorBoundary` (no changes needed there)

### 3. CSS for Spinner

Add to: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\PaneLoader.tsx`

**Requirements:**
- All styles inline (no separate CSS file)
- Spinner character: monospace font, large size (24px)
- Text: `fontSize: 'var(--sd-font-sm)'`, `color: 'var(--sd-text-muted)'`
- Spinner color: `color: 'var(--sd-purple)'`
- Layout: centered container using flexbox
- No hardcoded colors anywhere

### 4. Tests

Create: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\__tests__\PaneLoader.test.tsx`

**Test coverage:**
1. Renders spinner with rotating animation
2. Renders "Loading..." text
3. Uses correct CSS variables for colors
4. Spinner cycles through all 4 characters
5. Component is centered in container

Create: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\__tests__\AppFrame.loading.test.tsx`

**Test coverage:**
1. Shows loading state when component is mounting
2. Hides loading state after component renders
3. No flash on fast loads (<100ms)
4. Loading disappears when appType changes
5. Error boundary still works during mount

**Test command:**
```bash
cd browser && npx vitest run src/shell/components/__tests__/PaneLoader.test.tsx src/shell/components/__tests__/AppFrame.loading.test.tsx
```

## Test Requirements

- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Edge cases covered:
  - Fast mount (<100ms) — no loader flash
  - Slow mount (>100ms) — loader appears
  - Component error during mount — error boundary catches it
  - appType changes mid-mount — loader resets

## Constraints

- **No file over 500 lines** — PaneLoader.tsx should be ~60 lines, AppFrame.tsx is currently 59 lines (will be ~90 after changes)
- **CSS: var(--sd-*) only** — No hex, no rgb(), no named colors
- **No stubs** — Every function fully implemented
- **Reuse terminal spinner pattern** — Same chars, same interval (150ms)
- **No new dependencies** — Use existing React hooks only

## Acceptance Criteria

- [ ] PaneLoader component renders centered spinner + "Loading..." text
- [ ] AppFrame shows PaneLoader during mount if appType is not 'empty'
- [ ] No flash on fast loads (<100ms delay before showing loader)
- [ ] Loader disappears when component renders
- [ ] All CSS uses `var(--sd-*)` variables only
- [ ] All tests pass: `cd browser && npx vitest run src/shell/components/__tests__/PaneLoader.test.tsx src/shell/components/__tests__/AppFrame.loading.test.tsx`
- [ ] No hardcoded colors anywhere in code
- [ ] Spinner animation cycles correctly (150ms interval)
- [ ] Error boundary still catches mount errors

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260317-TASK-235-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.
