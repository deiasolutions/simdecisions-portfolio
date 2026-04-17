# TASK-BUG-017: Fix OAuth Redirect Landing Page Bug

## Objective
Fix the bug where ra96it.com OAuth redirect shows LandingPage instead of the logged-in state (login EGG). Modify `shouldShowLanding()` to check hostname and auth state before rendering LandingPage.

## Context
After OAuth completes on ra96it.com, the user is redirected to `https://ra96it.com/?token=eyJ...`. The token IS saved to localStorage by `extractTokenFromUrl()` (line 25-47 of App.tsx), and the URL is cleaned to `ra96it.com/`. But then `shouldShowLanding()` returns `true` because:
- Path is root (`/`)
- No `?egg=` param (URL was just cleaned)
- It never checks hostname or auth state

Result: User sees ShiftCenter LandingPage instead of the login EGG's "You are logged in" state.

**Root Cause:**
`shouldShowLanding()` (lines 58-63) short-circuits the EGG system without checking:
1. Hostname — ra96it.com domains should NEVER show LandingPage (they use the `login` EGG via eggResolver.ts)
2. Auth state — authenticated users should enter the EGG system, not see LandingPage

**Additional hostname bug:** Even on first visit to `ra96it.com/` (no OAuth flow), users see ShiftCenter landing instead of the login page.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\App.tsx` — the bug lives here (lines 58-63)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\auth\authStore.ts` — `isAuthenticated()` implementation (lines 94-118)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\eggs\eggResolver.ts` — hostname → EGG mapping (lines 94-96: ra96it domains map to `login` EGG)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\__tests__\App.test.tsx` — existing test patterns

## Deliverables
- [ ] Add `isAuthenticated` to imports from `authStore` (line 16 of App.tsx)
- [ ] Modify `shouldShowLanding()` to check hostname and auth state
- [ ] ra96it domains (`ra96it.com`, `www.ra96it.com`, `dev.ra96it.com`) return `false`
- [ ] Authenticated users return `false` (let EGG system handle routing)
- [ ] Root path with no `?egg=` on non-ra96it hostname when NOT authenticated returns `true` (preserve existing behavior)
- [ ] Existing behavior preserved: `?egg=` param present returns `false`
- [ ] Write TDD tests FIRST in `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\__tests__\App.shouldShowLanding.test.tsx`
- [ ] All existing App.tsx tests still pass

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Edge cases:
  - `shouldShowLanding()` returns `false` when hostname is `ra96it.com`
  - `shouldShowLanding()` returns `false` when hostname is `www.ra96it.com`
  - `shouldShowLanding()` returns `false` when hostname is `dev.ra96it.com`
  - `shouldShowLanding()` returns `false` when `isAuthenticated()` returns `true`
  - `shouldShowLanding()` returns `true` on root path with no `?egg=` param on `localhost:5173` when NOT authenticated (existing behavior)
  - `shouldShowLanding()` returns `false` when `?egg=` param present (existing behavior)

Create a new test file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\__tests__\App.shouldShowLanding.test.tsx`

The test file should:
- Mock `window.location.hostname`, `window.location.pathname`, `window.location.search`
- Mock `authStore.isAuthenticated()`
- Test all 6 edge cases above
- Use vitest patterns from existing App.test.tsx

## Constraints
- No file over 500 lines
- CSS: `var(--sd-*)` only (no CSS changes expected in this task)
- TDD — tests first, then implementation
- No stubs
- `isAuthenticated()` is already implemented and tested in authStore.ts — use it directly
- Do NOT modify eggResolver.ts, authStore.ts, or LandingPage.tsx — the bug is in App.tsx only

## Approximate Implementation (10 lines)
Replace `shouldShowLanding()` (lines 58-63) with:

```typescript
function shouldShowLanding(): boolean {
  const params = new URLSearchParams(window.location.search)
  const hasEggParam = params.has('egg')
  const isRootPath = window.location.pathname === '/' || window.location.pathname === ''

  // ra96it domains use the login EGG — never show ShiftCenter landing
  const hostname = window.location.hostname
  if (hostname === 'ra96it.com' || hostname === 'www.ra96it.com' || hostname === 'dev.ra96it.com') {
    return false
  }

  // Authenticated users should enter the EGG system, not see landing
  if (isAuthenticated()) {
    return false
  }

  return isRootPath && !hasEggParam
}
```

And add `isAuthenticated` to the import at line 16:
```typescript
import { setToken, setUser, base64UrlDecode, isAuthenticated } from './primitives/auth/authStore'
```

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260317-TASK-BUG-017-RESPONSE.md`

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
