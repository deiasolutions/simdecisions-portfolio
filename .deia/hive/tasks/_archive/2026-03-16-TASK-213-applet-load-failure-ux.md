# TASK-213: Applet Load Failure UX with Retry

## Objective
Enhance PaneContent.tsx to show a helpful error UI when an applet fails to load, with a retry button.

## Context
Currently, PaneContent.tsx shows a message when no renderer is registered for an appType:
```tsx
<div style={{ color: 'var(--sd-text-secondary)', fontSize: 'var(--sd-font-sm)' }}>
  No renderer registered for: <code style={{ color: 'var(--sd-orange)' }}>{node.appType}</code>
</div>
```

This is good for missing renderers, but we also need error handling for when:
- An applet module fails to load (import error)
- The applet registration throws an error
- The renderer returns null or crashes

This task extends the "no renderer" fallback to handle dynamic import failures and provide a retry mechanism.

**Note:** This task depends on TASK-186 (PaneErrorBoundary) for runtime errors. This task focuses on load-time failures.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\PaneContent.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\appRegistry.ts` (if exists, else check how apps are registered)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\index.ts`

## Deliverables
- [ ] Create `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\AppletLoadError.tsx`
  - Props: `{ appType: string, error?: Error, onRetry: () => void }`
  - UI: "Failed to load {appType}. Try refreshing." with retry button
  - Use var(--sd-red) for error icon, var(--sd-text-secondary) for message
  - Retry button with var(--sd-orange) hover
  - Optional: show error.message in collapsed details section (for debugging)
- [ ] Update PaneContent.tsx to detect applet load failures
  - If renderer is null/undefined but appType is valid → show AppletLoadError
  - Pass retry handler that clears cache and re-renders
  - Keep existing "no renderer registered" message for truly unknown appTypes
- [ ] Add CSS styles to `shell.css` for AppletLoadError component
  - `.applet-load-error` container with centered layout
  - `.applet-load-error-icon` with var(--sd-red) color
  - `.applet-load-error-message` with var(--sd-text-secondary)
  - `.applet-load-error-btn` with var(--sd-orange) hover
  - Optional: `.applet-load-error-details` collapsible section
- [ ] Export AppletLoadError from `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\index.ts`

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Edge cases:
  - Renderer returns null → AppletLoadError shown
  - Retry button click → onRetry called, error cleared
  - No error object → generic message shown
  - Error object with message → message shown in details (collapsed by default)
  - Valid appType but renderer missing → different message ("No renderer registered")

## Test File
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\__tests__\AppletLoadError.test.tsx`

Expected test count: **5+ tests**

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only (no hex, no rgb(), no named colors)
- No stubs
- Error message must be user-friendly
- Retry mechanism must actually attempt to reload (not just hide/show error)
- Distinguish between "renderer not registered" and "renderer failed to load"

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260316-TASK-213-RESPONSE.md`

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
