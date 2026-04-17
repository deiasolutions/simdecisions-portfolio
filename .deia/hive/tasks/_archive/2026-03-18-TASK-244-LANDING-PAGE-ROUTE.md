# TASK-244: Wire LandingPage route into App.tsx

## Objective
Modify `App.tsx` to conditionally render the LandingPage component when visiting `/` without an `?egg=` parameter, instead of always loading a Shell with an EGG.

## Context

### What Already Exists (DO NOT recreate)
- `browser/src/pages/LandingPage.tsx` — full landing page component (57 lines)
- `browser/src/pages/LandingPage.css` — styles (all CSS variables, no hardcoded colors)
- `browser/src/pages/__tests__/LandingPage.test.tsx` — tests

### The Problem
Currently, `App.tsx` always calls `useEggInit()` on mount. The `useEggInit()` hook:
1. Calls `resolveCurrentEgg()` from `eggResolver.ts`
2. This function checks for `?egg=` param, then pathname, then hostname mapping
3. When visiting `/` with no params, it falls back to hostname mapping (returns 'chat' for localhost)
4. Shell loads with the fallback EGG instead of showing the LandingPage

### The Solution
Modify `App.tsx` to:
1. Check if the URL condition requires the landing page (no `?egg=` param AND empty pathname)
2. If YES → render `LandingPage` directly (skip `useEggInit()` entirely)
3. If NO → use existing flow (call `useEggInit()` and render Shell as before)

### Landing Page Condition
The landing page should show when:
- URL pathname is exactly `/` (no segments like `/chat` or `/canvas`)
- AND no `?egg=` parameter exists in the URL
- (Hostname doesn't matter — any hostname with these conditions shows landing)

### Examples
- `http://localhost:5173/` → LandingPage ✓
- `http://localhost:5173/?egg=canvas` → Shell with Canvas EGG ✓
- `http://localhost:5173/chat` → Shell with Chat EGG ✓
- `http://chat.efemera.live/` → LandingPage ✓
- `http://chat.efemera.live/?egg=code` → Shell with Code EGG ✓

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\App.tsx` (current routing logic, 102 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\pages\LandingPage.tsx` (already exists, 57 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\useEggInit.ts` (how useEggInit works)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\eggs\eggResolver.ts` (how egg param is parsed)

## Files to Modify
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\App.tsx` — add LandingPage import + conditional routing logic

## Deliverables

1. **App.tsx changes:**
   - [ ] Import `LandingPage` from `'./pages/LandingPage'`
   - [ ] Add function to check landing page condition (no egg param, empty pathname)
   - [ ] Conditionally render LandingPage OR existing Shell flow
   - [ ] Preserve all existing Shell rendering logic (no changes to loading/error states)
   - [ ] Preserve existing `extractTokenFromUrl()` logic (must still run)

2. **No regressions:**
   - [ ] `/` with `?egg=canvas` → still loads Shell with Canvas EGG
   - [ ] `/chat` → still loads Shell with Chat EGG
   - [ ] Any hostname with `?egg=xxx` → still loads Shell with that EGG
   - [ ] OAuth token extraction still works (extractTokenFromUrl runs before routing)

3. **Tests:**
   - [ ] `browser/src/pages/__tests__/LandingPage.test.tsx` still passes
   - [ ] Full frontend test suite passes: `cd browser && npx vitest run`
   - [ ] No new test failures introduced

## Test Requirements

Run these commands in order:

```bash
# Test LandingPage component
cd browser && npx vitest run --reporter=verbose src/pages/__tests__/LandingPage.test.tsx

# Run full frontend test suite
cd browser && npx vitest run --reporter=verbose
```

Expected results:
- LandingPage tests: all passing (no regressions)
- Full test suite: all passing (no new failures)

## Implementation Notes

### Routing Logic Pseudocode
```typescript
function shouldShowLandingPage(): boolean {
  const params = new URLSearchParams(window.location.search)
  const hasEggParam = params.has('egg')
  const pathname = window.location.pathname.replace(/^\/+/, '').split('/')[0]
  return !hasEggParam && !pathname
}

function App() {
  // OAuth token extraction (runs first, always)
  // ... existing extractTokenFromUrl() ...

  // Check for landing page condition
  if (shouldShowLandingPage()) {
    return <LandingPage />
  }

  // Existing Shell flow (no changes)
  const { loading, error, shellRoot, uiConfig } = useEggInit()
  // ... rest of existing code ...
}
```

### Key Constraints
- **Do NOT modify `useEggInit()`, `eggResolver.ts`, or any egg loading logic**
- **Do NOT recreate LandingPage.tsx or LandingPage.css** — they already exist
- **Do NOT change existing Shell, loading, or error rendering logic**
- App.tsx must stay under 150 lines (currently 102 lines)
- Preserve all existing imports and exports

## Constraints
- No file over 500 lines (App.tsx will stay under 150)
- CSS: var(--sd-*) only (already satisfied by existing LandingPage.css)
- No stubs — full implementation
- MUST modify App.tsx and ONLY App.tsx
- Do NOT recreate LandingPage component or its CSS

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260318-TASK-244-RESPONSE.md`

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

## Model Assignment
sonnet

## Priority
P2
