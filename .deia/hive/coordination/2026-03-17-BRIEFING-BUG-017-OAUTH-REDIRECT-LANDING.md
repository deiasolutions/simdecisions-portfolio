# BRIEFING: BUG-017 — OAuth Redirect Shows LandingPage Instead of Logged-In State

**From:** Q33NR
**To:** Q33N
**Date:** 2026-03-17
**Priority:** P0 — blocks ra96it.com auth flow entirely
**Model assignment:** Haiku (small, surgical fix)

---

## Problem

When a user completes GitHub OAuth on ra96it.com, they are redirected back to `https://ra96it.com/?token=eyJhbGciOiJSU...`. The token IS correctly saved to localStorage by `extractTokenFromUrl()`. But the user then sees the ShiftCenter LandingPage (marketing page) instead of the LoginPage's "You are logged in" state.

The auth flow is **silently succeeding but visually failing**. The user thinks login didn't work.

## Root Cause

Three interacting bugs in `browser/src/App.tsx`:

### Bug A (Primary): `shouldShowLanding()` ignores auth state

After `extractTokenFromUrl()` (line 25-47) saves the token and strips `?token=` from the URL (line 46), the URL becomes `ra96it.com/` — clean root path, no query params.

`shouldShowLanding()` (line 58-63) then checks:
- Is path root? YES (`/`)
- Has `?egg=` param? NO (URL was just cleaned)
- Result: returns `true` → renders `<LandingPage />`

It never checks whether the user just authenticated.

### Bug B: `shouldShowLanding()` ignores hostname

`ra96it.com` is mapped to the `login` EGG in `eggResolver.ts` (lines 94-96). But `shouldShowLanding()` runs BEFORE the EGG system and short-circuits it. Users visiting `ra96it.com/` see the ShiftCenter marketing page, not the login page — even on first visit without any OAuth flow.

### Bug C: `LandingPage` has zero auth awareness

`browser/src/pages/LandingPage.tsx` is a static marketing page. No `isAuthenticated()` check. No redirect. No fallback for authenticated users.

## The Fix

Modify `shouldShowLanding()` in `App.tsx` to:

1. **Check hostname** — ra96it.com domains should NEVER show LandingPage. They have their own `login` EGG via `eggResolver.ts`.
2. **Check auth state** — if `isAuthenticated()` returns true, don't show LandingPage (let the EGG system handle routing to an appropriate post-login state).

Approximate fix (~10 lines):

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

This requires importing `isAuthenticated` from `authStore` (already imported partially — `setToken`, `setUser`, `base64UrlDecode` are there).

## Files to Modify

| File | Change |
|------|--------|
| `browser/src/App.tsx` (lines 58-63) | Fix `shouldShowLanding()` — add hostname + auth checks |
| `browser/src/App.tsx` (line 16) | Add `isAuthenticated` to import from authStore |

## Files to Read First

- `browser/src/App.tsx` — the bug lives here
- `browser/src/primitives/auth/authStore.ts` — `isAuthenticated()` implementation
- `browser/src/eggs/eggResolver.ts` — hostname → EGG mapping (lines 94-96)
- `browser/src/pages/LandingPage.tsx` — the static page that incorrectly renders

## Test Requirements

- Test: `shouldShowLanding()` returns `false` when hostname is `ra96it.com`
- Test: `shouldShowLanding()` returns `false` when hostname is `www.ra96it.com`
- Test: `shouldShowLanding()` returns `false` when hostname is `dev.ra96it.com`
- Test: `shouldShowLanding()` returns `false` when `isAuthenticated()` returns true
- Test: `shouldShowLanding()` returns `true` on root path with no EGG param on non-ra96it hostname when not authenticated (existing behavior preserved)
- Test: `shouldShowLanding()` returns `false` when `?egg=` param present (existing behavior preserved)

## Constraints

- CSS: `var(--sd-*)` only (no CSS changes expected)
- No file over 500 lines
- TDD — tests first
- No stubs
- `isAuthenticated()` is already implemented and tested in `authStore.ts`

## Acceptance Criteria

- [ ] Visiting `ra96it.com/` shows LoginPage (login EGG), NOT LandingPage
- [ ] OAuth redirect `ra96it.com/?token=eyJ...` results in logged-in state visible to user
- [ ] Visiting `shiftcenter.com/` (or localhost without params) still shows LandingPage
- [ ] Authenticated users on any domain enter the EGG system, not LandingPage
- [ ] All existing App.tsx tests still pass
- [ ] 6+ new tests for `shouldShowLanding()` logic
