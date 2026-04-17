# TASK-137: Port AuthPage + authStore into Browser Primitives

## Objective
Port platform's AuthPage.tsx and auth.ts into browser as a reusable auth primitive with LoginPage component, shared authStore, and login EGG configuration.

## Context
The platform repo has a working React login page (`AuthPage.tsx`) with GitHub OAuth button, dev-login bypass button, and consent section. It also has a token store (`lib/auth.ts`) that manages localStorage token CRUD, expiry checking, and scope validation. This task ports both into `browser/src/primitives/auth/` as a shared primitive (not sim-specific) and creates a minimal login EGG.

**Key platform patterns to preserve:**
- Check `/dev-login/available` on mount to decide whether to show dev-login button
- GitHub OAuth flow: GET `/oauth/github/login` (fetch URL), redirect user to GitHub
- Dev-login flow: POST `/dev-login` (returns JWT)
- Token stored in localStorage with expiry + scope validation
- Consent section with terms/privacy/guidelines

**Key changes from platform:**
- Use `var(--sd-*)` CSS variables ONLY (no hardcoded colors) — Rule 3
- Storage key: `ra96it_token` (not `efemera_token`)
- API base URL: ra96it service (not efemera)
- Component name: `LoginPage` (not `AuthPage`)

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\frontend\src\pages\AuthPage.tsx` (138 lines: GitHub OAuth button, dev-login, consent)
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\frontend\src\lib\auth.ts` (57 lines: token store, expiry check, scope validation)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\lib\auth.ts` (existing sim-specific auth)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\TextPane.tsx` (example primitive structure)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\chat.egg.md` (example EGG structure)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\eggs\eggResolver.ts` (path resolution)

## Deliverables

### Primitive Component
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\auth\LoginPage.tsx` — Port from platform AuthPage.tsx:
  - Props: `onAuthSuccess: (token: string, user: {id: string, email: string, display_name: string}) => void`
  - State: `stage: "consent" | "loading"`, `devAvailable: boolean`, `devLoading: boolean`
  - On mount: fetch ra96it `/dev-login/available`, set `devAvailable`
  - GitHub button click: fetch ra96it `/oauth/github/login`, redirect to returned URL
  - Dev-login button click (if available): POST ra96it `/dev-login`, call `onAuthSuccess` with token + user
  - Consent section with 3 items: Terms, Privacy, Community Guidelines (keep same text)
  - Loading spinner when redirecting to GitHub
  - Use `var(--sd-text)`, `var(--sd-text-muted)`, `var(--sd-bg)`, `var(--sd-bg-card)`, `var(--sd-border)`, `var(--sd-purple)`, `var(--sd-green)` — NO hex colors
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\auth\LoginPage.css` — Styles using `var(--sd-*)` ONLY:
  - Container: center content, gradient background (using CSS variables)
  - Buttons: GitHub button (solid), dev-login button (outline)
  - Consent card: border, padding, list items with checkmarks
  - Loading spinner: rotate animation
  - NO hardcoded colors (Rule 3)
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\auth\authStore.ts` — Port from platform auth.ts:
  - Storage key: `ra96it_token` (not `efemera_token`)
  - `getToken(): string | null` — read from localStorage
  - `setToken(token: string): void` — write to localStorage
  - `clearToken(): void` — remove from localStorage
  - `getUser(): {id, email, display_name} | null` — parse from localStorage `ra96it_user`
  - `setUser(user): void` — write to localStorage `ra96it_user`
  - `getAuthHeaders(): {Authorization?: string}` — return `Bearer <token>` or empty object
  - `isAuthenticated(): boolean` — check token exists, not expired, scope="chat" (reject bot/api tokens)
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\auth\index.ts` — Barrel export:
  ```ts
  export { default as LoginPage } from './LoginPage';
  export * from './authStore';
  ```

### EGG Configuration
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\login.egg.md` — Minimal login EGG (no chrome, single pane):
  ```yaml
  name: "Login"
  slug: "login"
  description: "Authentication page for GitHub OAuth and dev-login"
  layout:
    - type: "pane"
      id: "auth-pane"
      primitive: "auth"
      props:
        onAuthSuccess: "handleAuthSuccess"
      chrome: false
  ```
- [ ] Update `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\eggs\eggResolver.ts`:
  - Add `/login` path → resolves to `eggs/login.egg.md`
- [ ] Update `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\index.ts`:
  - Register `auth` adapter that maps `primitive: "auth"` → `<LoginPage onAuthSuccess={...} />`

### Tests (TDD — write tests FIRST)
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\auth\__tests__\LoginPage.test.tsx`:
  - `test_renders_github_button` — mounts component, finds GitHub OAuth button
  - `test_renders_consent_section` — finds 3 consent items (Terms, Privacy, Community)
  - `test_dev_login_button_shown_when_available` — mock `/dev-login/available` → true, button visible
  - `test_dev_login_button_hidden_when_unavailable` — mock `/dev-login/available` → false, button hidden
  - `test_github_login_fetches_url_and_redirects` — mock `/oauth/github/login`, click button, verify redirect
  - `test_dev_login_posts_and_calls_onAuthSuccess` — mock `/dev-login`, click button, verify callback
  - `test_loading_spinner_shown_during_github_redirect` — verify spinner when stage=loading
  - `test_no_hardcoded_colors` — scan rendered output for hex colors, fail if found
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\auth\__tests__\authStore.test.ts`:
  - `test_getToken_returns_null_when_empty` — localStorage empty → null
  - `test_setToken_and_getToken` — write token, read back, verify match
  - `test_clearToken_removes_token_and_user` — write token + user, clear, verify both gone
  - `test_getUser_and_setUser` — write user object, read back, verify match
  - `test_getAuthHeaders_with_token` — token exists → returns `{Authorization: "Bearer <token>"}`
  - `test_getAuthHeaders_without_token` — no token → returns `{}`
  - `test_isAuthenticated_false_when_no_token` — no token → false
  - `test_isAuthenticated_false_when_expired` — expired token → false
  - `test_isAuthenticated_false_when_scope_not_chat` — scope=bot → false (auto-clears token)
  - `test_isAuthenticated_true_when_valid_chat_token` — valid token, scope=chat → true

### Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All 17+ tests pass (8 component + 9 store)
- [ ] Use Vitest + React Testing Library
- [ ] Mock fetch calls (use vi.fn())
- [ ] Test token expiry edge cases (expired, missing exp, malformed)
- [ ] Test scope rejection (bot/api tokens auto-clear)
- [ ] Verify NO hardcoded colors in rendered output

## Constraints
- No file over 500 lines (Rule 4)
- NO STUBS (Rule 6) — every function fully implemented
- TDD (Rule 5) — tests first, then implementation
- All file paths must be absolute (Rule 8)
- NO HARDCODED COLORS (Rule 3) — only `var(--sd-*)` CSS variables
- Port existing code — do NOT rewrite UI from scratch
- Keep consent section text (terms, privacy, community guidelines)
- Storage key: `ra96it_token` (not `efemera_token`)

## Acceptance Criteria
- [ ] `localhost:5174/login` renders GitHub OAuth login page
- [ ] Login page styled with `var(--sd-*)` CSS variables ONLY (no hex, no rgb(), no named colors)
- [ ] Dev-login button shown when ra96it returns `{available: true}` from `/dev-login/available`
- [ ] Dev-login button hidden when unavailable (cloud mode or GitHub OAuth configured)
- [ ] GitHub button fetches `/oauth/github/login`, redirects to returned GitHub URL
- [ ] Dev-login button POSTs `/dev-login`, calls `onAuthSuccess` with token + user
- [ ] JWT stored in localStorage as `ra96it_token`, survives page refresh
- [ ] User stored in localStorage as `ra96it_user`
- [ ] `isAuthenticated()` returns false for expired tokens, bot/api tokens, missing tokens
- [ ] `isAuthenticated()` returns true for valid chat-scoped tokens
- [ ] All 17+ tests pass
- [ ] No file over 500 lines

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260315-TASK-137-RESPONSE.md`

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
