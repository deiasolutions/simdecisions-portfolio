# TASK-133: ra96it SSO Phase 1 — LoginPage + authStore (Browser-Only)

## Objective

Build the login page UI and auth store for ShiftCenter as a standalone browser primitive. This ships independently before ra96it backend exists. Uses dev-login bypass on localhost (no GitHub account needed for dev). Styled with ShiftCenter theme (CSS variables only).

## Context

This is Phase 1 of the ra96it SSO federation system. The spec calls for a 3-phase approach:
1. **Phase 1 (this task):** Login page + auth store + EGG + routing (browser-only, can ship independently)
2. **Phase 2 (TASK-134):** ra96it service (backend, separate repo)
3. **Phase 3 (TASK-135):** Wire ShiftCenter to ra96it (backend + frontend integration)

Phase 1 must work with dev-login bypass on localhost even before ra96it backend exists. The login page will be a pane primitive that can be rendered via EGG config.

## Dependencies

None. This task is standalone and does not depend on any other tasks. It prepares the infrastructure for future ra96it integration.

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\settings\settingsStore.ts` — localStorage wrapper pattern (uses `sd_user_settings` key)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\settings\SettingsPanel.tsx` — UI component pattern with CSS variables
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\chat.egg.md` — EGG config format example
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\eggs\eggResolver.ts` — routing resolution (pathname + hostname + URL param)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\index.ts` — app registration pattern
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\queue\2026-03-14-2200-SPEC-ra96it-sso-federation.md` — full spec

## Deliverables

### Browser Primitives

- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\auth\LoginPage.tsx` — login UI component
  - GitHub OAuth button (future — links to ra96it.com/authorize)
  - Dev-login bypass button (localhost only)
  - Status display (logged in / not logged in)
  - All colors use `var(--sd-*)` CSS variables
  - No inline styles, no hardcoded colors
  - Clean, minimal UI (similar to SettingsPanel style)
  - Displays "Dev Mode — Auth bypassed" message on localhost
  - Displays "Authentication required" message when not authenticated
  - Shows user display_name when authenticated

- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\auth\authStore.ts` — JWT storage + auth state
  - `loadAuthToken()` — read JWT from localStorage (key: `sd_auth_token`)
  - `saveAuthToken(token: string)` — save JWT to localStorage
  - `deleteAuthToken()` — remove JWT from localStorage
  - `isAuthenticated()` — check if valid token exists (basic check, no verification yet)
  - `getAuthClaims()` — decode JWT and return claims (no verification, just decode)
  - `isLocalMode()` — check if running on localhost (bypasses auth)
  - `getDevToken()` — return stub dev token for localhost (mock JWT claims)
  - No network calls in this task — just localStorage wrapper

- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\auth\LoginPage.css` — styles
  - Use CSS variables exclusively (`var(--sd-*)`)
  - Match SettingsPanel style (`.sd-auth-*` class prefix)
  - Layout: centered card, 400px wide, auto height
  - Button styles: primary button for GitHub OAuth, secondary for dev-login
  - Clean spacing, readable typography

- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\auth\types.ts` — TypeScript types
  - `AuthToken` interface (JWT string wrapper)
  - `AuthClaims` interface (matches ra96it JWT claims from spec)
  - `LoginPageProps` interface (onLogin callback, onClose callback)
  - Export all types

- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\auth\index.ts` — barrel export
  - Export LoginPage component
  - Export authStore functions
  - Export types

### EGG Config

- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\login.egg.md` — login EGG
  - Minimal chrome (no sidebar, no toolbar)
  - Single pane layout with LoginPage component
  - `appType: "login"` in layout
  - `defaultRoute: /login`
  - Match chat.egg.md format (schema_version: 3)

### App Registration

- [ ] Update `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\index.ts`
  - Add `import { LoginAdapter } from './loginAdapter'`
  - Register: `registerApp('login', LoginAdapter)`

- [ ] Create `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\loginAdapter.tsx`
  - Implement `LoginAdapter` component
  - Renders `LoginPage` from primitives/auth
  - Follows same pattern as TerminalAdapter, TextPaneAdapter

### Routing

- [ ] Update `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\eggs\eggResolver.ts`
  - Add pathname `/login` → `'login'` mapping in `resolveCurrentEgg()`
  - Ensure localhost:5174/login resolves to login EGG

### Shell Integration (Optional — Nice to Have)

- [ ] Add login status indicator to shell (if time permits)
  - Small indicator in shell header showing "Logged in as: [name]" or "Not authenticated"
  - Reads from authStore.getAuthClaims()
  - Only shows on non-localhost (dev mode doesn't need it)

## Test Requirements

- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Minimum 12 tests across all test files

### Test Files

- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\auth\__tests__\authStore.test.ts`
  - Test loadAuthToken() with empty localStorage
  - Test saveAuthToken() and loadAuthToken() round-trip
  - Test deleteAuthToken() clears storage
  - Test isAuthenticated() returns true/false correctly
  - Test getAuthClaims() decodes valid JWT
  - Test getAuthClaims() returns null for invalid JWT
  - Test isLocalMode() detects localhost correctly
  - Test getDevToken() returns stub token on localhost
  - Edge cases: malformed JWT, expired token (just decode, no verification)

- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\auth\__tests__\LoginPage.test.tsx`
  - Test component renders without crashing
  - Test dev mode message shows on localhost
  - Test GitHub OAuth button is disabled (no backend yet)
  - Test dev-login button works (calls onLogin with dev token)
  - Test authenticated state shows user display_name
  - Test unauthenticated state shows "Authentication required" message

## Acceptance Criteria

- [ ] `localhost:5174/login` renders the LoginPage component
- [ ] Dev mode message "Dev Mode — Auth bypassed" shows on localhost
- [ ] Dev-login button works — sets stub token in localStorage
- [ ] After dev-login, page shows "Logged in as: local-user" (or similar)
- [ ] GitHub OAuth button is present but disabled/placeholder (no backend yet)
- [ ] All colors use `var(--sd-*)` CSS variables — ZERO hardcoded colors
- [ ] No file over 500 lines
- [ ] authStore functions work with localStorage (save, load, delete, check)
- [ ] JWT decode works (no verification, just decode base64)
- [ ] All 12 tests pass
- [ ] Vitest output shows 0 failures

## Constraints

- **NO HARDCODED COLORS.** Only CSS variables (`var(--sd-*)`). No hex, no rgb(), no named colors.
- **No file over 500 lines.** Modularize at 500. Hard limit: 1,000.
- **TDD.** Tests first, then implementation. No exceptions.
- **NO STUBS.** Every function fully implemented. No `// TODO`, no empty bodies.
- **No network calls in this task.** This is browser-only. No API calls to ra96it or hivenode.
- **No external dependencies.** Use existing packages in package.json. jwt-decode is allowed if needed for base64 decoding.

## Implementation Notes

### JWT Decode (No Verification)

For Phase 1, we just need to decode the JWT payload (base64 decode). No signature verification. Use:
- `jwt-decode` package (likely already in dependencies) OR
- Manual base64 decode (split on `.`, decode middle part, JSON.parse)

No need to verify signature or expiry in this task. That comes in Phase 3 when we wire to ra96it backend.

### Dev Token Format

The dev token should be a mock JWT with these claims:
```json
{
  "sub": "local-user",
  "email": "local@shiftcenter.local",
  "display_name": "Local Dev User",
  "iss": "localhost",
  "aud": "shiftcenter",
  "mode": "local",
  "tier": "local"
}
```

Encode this as a JWT (header.payload.signature) but with a fake signature (just `"dev-signature"`). The decode function will just extract the payload.

### localStorage Key

Use `sd_auth_token` as the key (consistent with `sd_user_settings` pattern).

### EGG Layout

The login EGG should be a single pane with no sidebar. Minimal chrome. Example:

```layout
{
  "type": "pane",
  "nodeId": "login-main",
  "appType": "login",
  "label": "Login",
  "config": {}
}
```

### CSS Variables Reference

Check existing files for CSS variable names. Common ones:
- `--sd-bg-primary` — background color
- `--sd-text-primary` — text color
- `--sd-border` — border color
- `--sd-accent` — accent color
- `--sd-button-bg` — button background
- `--sd-button-text` — button text

If a variable doesn't exist, add it to the global CSS file (but prefer using existing ones).

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260315-TASK-133-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — vitest output summary
6. **Acceptance Criteria** — copy from above, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, recommended next tasks

DO NOT skip any section. A response without all 8 sections is incomplete.
