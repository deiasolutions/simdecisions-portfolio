# BRIEFING: TASK-245 — ra96it Sign-Up Flow Verified

**From:** Q33NR (Queen Regent)
**To:** Q33N (Queen Coordinator)
**Date:** 2026-03-17
**Source:** `.deia/hive/queue/2026-03-16-SPEC-TASK-245-ra96it-signup-flow.md`
**Wave:** 5 (Ship)
**Model:** haiku

---

## Objective

Verify the ra96it sign-up flow works end-to-end for new users: visit ShiftCenter → click "Continue with GitHub" → authenticate → redirected back with JWT → session active → can use app.

If anything is broken, fix it. This is a **verification task** with repair authority.

---

## Context

Wave 5 Ship (Task 5.7 in `docs/specs/WAVE-5-SHIP.md`). The goal: a stranger can find the product, sign up, and use it.

**"Sign-up" means GitHub OAuth.** ShiftCenter does not have traditional username/password registration. New users authenticate via GitHub, which creates a user record in ra96it's PostgreSQL database and issues a JWT.

The flow was implemented in **TASK-136, TASK-137, TASK-138** (2026-03-15). It exists but has never been smoke-tested end-to-end from a new user's perspective.

---

## The Expected Flow

1. **User visits ShiftCenter** (localhost:5173 or production URL)
   - Not logged in → sees `LoginPage.tsx` component
2. **User clicks "Continue with GitHub"** button
   - Frontend calls: `GET ${API_BASE}/auth/github/login?origin=<origin>`
   - Backend (`ra96it/routes/oauth.py`) returns: `{url: "https://github.com/login/oauth/authorize?..."}`
   - Frontend redirects to GitHub
3. **User authorizes on GitHub**
   - GitHub redirects to ra96it callback: `/auth/github/callback?code=<code>`
   - Backend (`ra96it/routes/oauth.py`) exchanges code for GitHub access token
   - Backend fetches GitHub user profile
   - Backend creates or updates User record in PostgreSQL
   - Backend creates JWT with claims: `{sub: user_id, email, display_name, scope: "chat", ...}`
   - Backend redirects to frontend: `${origin}?token=<jwt>`
4. **User lands on ShiftCenter with token in URL**
   - `LoginPage.tsx` `useEffect` extracts token from `?token=` query param
   - Decodes JWT payload to get user info
   - Calls `onAuthSuccess(token, user)`
   - Parent component (`AppFrame.tsx` or similar) stores token in localStorage via `authStore.ts`
   - App loads requested EGG (e.g., chat.egg.md)
5. **User is now authenticated**
   - Token stored in `localStorage` under key `ra96it_token`
   - User object stored under key `ra96it_user`
   - App can make authenticated requests with `Authorization: Bearer <token>` header

---

## Files to Review

### Frontend (browser/)
- `browser/src/primitives/auth/LoginPage.tsx` — OAuth UI and redirect handler
- `browser/src/primitives/auth/authStore.ts` — Token storage and validation
- `browser/src/shell/components/AppFrame.tsx` — Likely parent component handling `onAuthSuccess`

### Backend (ra96it/)
- `ra96it/routes/oauth.py` — GitHub OAuth endpoints (`/auth/github/login`, `/auth/github/callback`)
- `ra96it/services/github.py` — GitHub API integration
- `ra96it/services/jwt.py` — JWT creation
- `ra96it/models.py` — User model
- `ra96it/db.py` — Database session

### Tests (if exist)
- `tests/ra96it/test_oauth.py` — OAuth flow tests
- `browser/src/primitives/auth/__tests__/LoginPage.test.tsx` — LoginPage tests

---

## What Q33N Must Do

### Step 1: Trace the Flow
Read the files listed above. Document each step of the flow:
1. User sees LoginPage
2. Clicks GitHub button → what happens?
3. Backend receives callback → what happens?
4. JWT created → what claims?
5. Redirect back to frontend → what URL format?
6. Frontend extracts token → how?
7. Token stored → where? how?

### Step 2: Verify or Fix
For each step, check:
- **Does it work?** (read tests, read code logic)
- **Is there a gap?** (e.g., missing redirect_uri config, wrong environment variable, broken callback route)
- **Can it fail silently?** (e.g., malformed JWT, missing error handling)

If you find a broken step, create a task to fix it.

### Step 3: Add E2E Test
The spec requires: **"Add E2E test: sign-up flow redirects correctly (mock ra96it for CI)"**

This means:
- Write a browser-side test that simulates the full flow
- Mock the backend responses (e.g., `/auth/github/login` returns mock URL, token callback returns mock JWT)
- Verify:
  - LoginPage renders
  - Click GitHub button triggers redirect
  - Token in URL gets extracted
  - `onAuthSuccess` gets called with correct token and user
  - Token stored in localStorage

File location: `browser/src/primitives/auth/__tests__/LoginPage.integration.test.tsx` (or similar)

Run: `cd browser && npx vitest run`

### Step 4: Write Task Files
Break the work into bee-sized tasks:
- **TASK-245A:** Trace and document the flow (Q33N can do this — no code)
- **TASK-245B:** Fix any broken steps (if found)
- **TASK-245C:** Add E2E test for sign-up flow (mock backend)

If no fixes are needed, skip TASK-245B. Document that the flow is already working.

---

## Acceptance Criteria (from Spec)

- [ ] Trace the full sign-up flow and document each step
- [ ] Verify each step works (or identify what's broken)
- [ ] Fix any broken steps found during verification
- [ ] Add E2E test: sign-up flow redirects correctly (mock ra96it for CI)
- [ ] Run: `cd browser && npx vitest run` — all tests pass

---

## Constraints

- **Rule 2:** Q33N does NOT code unless Q88N explicitly approves it for a specific task
- **Rule 5:** TDD — tests first, then implementation
- **Rule 3:** No hardcoded colors (CSS variables only)
- **Rule 4:** No file over 500 lines
- **Rule 6:** No stubs or TODOs
- **Rule 10:** No git operations without Q88N approval

---

## Environment Variables to Check

`LoginPage.tsx` uses: `import.meta.env.VITE_RA96IT_API`

Verify this is set correctly:
- **Local:** Should point to local ra96it server (e.g., `http://localhost:8001` or empty string for same-origin)
- **Production:** Should point to production ra96it (e.g., `https://ra96it.com`)

---

## Questions for Q33N

Before writing task files, answer these:
1. **Does the flow already work?** (based on code review)
2. **Is there a gap?** (e.g., missing redirect_uri handling, wrong env var, broken callback)
3. **Do E2E tests exist?** (check `browser/src/primitives/auth/__tests__/`)
4. **What needs to be built?** (list specific fixes or tests)

---

## Deliverables for Q33NR

Return to me with:
1. **Flow documentation** — 6-step trace of the sign-up flow (what happens at each step)
2. **Status report** — does it work? what's broken?
3. **Task files** (if work is needed) — written to `.deia/hive/tasks/`
4. **Test plan** — what E2E test needs to be added?

Do NOT dispatch bees yet. I will review your task files before approval.

---

## References

- Source spec: `docs/specs/WAVE-5-SHIP.md` (Task 5.7)
- Related tasks: TASK-136 (ra96it GitHub OAuth + JWKS), TASK-137 (browser auth primitive), TASK-138 (hivenode JWKS cache)
- BOOT.md: 10 hard rules
- HIVE.md: Q33N workflow

---

**Next Step:** Q33N reads this briefing, traces the flow, identifies gaps, writes task files, returns for Q33NR review.
