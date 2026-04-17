# TASK-AUTH-A: LoginPage Rebrand from ra96it to hodeia

**Model:** Haiku
**Priority:** P1
**Date:** 2026-03-24

---

## Objective

Rebrand LoginPage.tsx from ra96it branding to hodeia branding. Replace environment variable `VITE_RA96IT_API` with `VITE_AUTH_API` (generic) and replace all UI text references to "ra96it" with "hodeia" or neutral language. This is a pure branding change — OAuth flow logic and localStorage keys remain unchanged.

---

## Context

The LoginPage currently uses:
- Environment variable: `VITE_RA96IT_API` (line 23)
- UI branding: "ra96it" appears 4 times in the UI (lines 158, 178, 194)
- GitHub branding (logo, badge, consent) remains unchanged

**IMPORTANT:** This task is ONLY for LoginPage.tsx changes. The localStorage keys (`ra96it_token`, `ra96it_user`) will be handled in a separate task (AUTH-B). Do NOT change localStorage keys or authStore.ts in this task.

---

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\auth\LoginPage.tsx` (275 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\auth\__tests__\authStore.test.ts` (136 lines, for reference only)

---

## Deliverables

### 1. LoginPage.tsx Changes

**Environment Variable (Line 23):**
- Replace: `const API_BASE = import.meta.env.VITE_RA96IT_API || ''`
- With: `const API_BASE = import.meta.env.VITE_AUTH_API || ''`

**UI Branding Changes:**
- Line 158: Replace `<span className="auth-logo-text">ra96it</span>` with `<span className="auth-logo-text">hodeia</span>`
- Line 178: Replace `You can now use ra96it.` with `You can now use hodeia.`
- Line 194: Replace `<span className="auth-logo-text">ra96it</span>` with `<span className="auth-logo-text">hodeia</span>`

**Leave Unchanged:**
- GitHub branding (logo, badge, consent flow)
- OAuth flow logic (GitHub redirect, token extraction, JWT decoding)
- All CSS classes and styling
- Dev-login button and logic
- All other component behavior

### 2. Test Coverage

Create `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\auth\__tests__\LoginPage.test.tsx`

**Required Test Cases:**

1. **test_env_var_uses_VITE_AUTH_API**: Verify that LoginPage uses `VITE_AUTH_API` environment variable for API_BASE
2. **test_ui_displays_hodeia_branding_in_header**: Verify that the header displays "hodeia" instead of "ra96it" (line 194)
3. **test_ui_displays_hodeia_branding_when_logged_in**: Verify that logged-in state displays "hodeia" instead of "ra96it" (lines 158, 178)
4. **test_github_branding_unchanged**: Verify that GitHub logo, badge, and consent flow remain intact

**Test Coverage Requirements:**
- All 4 test cases must pass
- Use Vitest + React Testing Library
- Mock `import.meta.env.VITE_AUTH_API` in tests
- Mock fetch API for OAuth and dev-login endpoints
- Tests must verify actual rendered text, not just component props

---

## Test Requirements

- [ ] Write tests FIRST (TDD approach)
- [ ] All tests pass (`cd browser && npx vitest run --reporter=verbose src/primitives/auth/__tests__/LoginPage.test.tsx`)
- [ ] Minimum 4 test cases (all passing)
- [ ] Edge cases covered:
  - Environment variable correctly referenced
  - All 3 instances of "hodeia" branding rendered correctly
  - GitHub branding unchanged (logo SVG, badge text, consent list)
  - OAuth flow logic unchanged (no regression)

---

## Constraints (10 Hard Rules Apply)

- **No file over 500 lines**: LoginPage.tsx is 275 lines (safe)
- **CSS: var(--sd-*) only**: Already compliant — no changes to CSS
- **No stubs**: Full implementation required
- **TDD**: Tests first, then implementation
- **Do NOT change OAuth flow logic**: Only env var name and UI text
- **Do NOT change localStorage keys**: Separate task (AUTH-B)
- **Do NOT modify authStore.ts**: Out of scope for this task
- **Do NOT modify LoginPage.css**: CSS file unchanged
- **Stay in your lane**: Only modify LoginPage.tsx and create LoginPage.test.tsx

---

## Acceptance Criteria

- [ ] `VITE_RA96IT_API` replaced with `VITE_AUTH_API` in LoginPage.tsx (line 23)
- [ ] All 4 instances of "ra96it" UI text replaced with "hodeia" (lines 158, 178, 194)
- [ ] GitHub branding unchanged (logo, badge, consent flow)
- [ ] OAuth flow logic unchanged (redirect, token extraction, JWT decode)
- [ ] Dev-login logic unchanged
- [ ] LoginPage.test.tsx created with 4+ passing tests
- [ ] All tests pass (`npx vitest run`)
- [ ] No changes to authStore.ts or localStorage key names
- [ ] No changes to LoginPage.css
- [ ] File length under 500 lines (LoginPage.tsx will remain ~275 lines)

---

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260324-TASK-AUTH-A-RESPONSE.md`

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

---

## Test Commands

```bash
# Run LoginPage tests only
cd browser && npx vitest run --reporter=verbose src/primitives/auth/__tests__/LoginPage.test.tsx

# Run all auth tests
cd browser && npx vitest run --reporter=verbose src/primitives/auth/__tests__/

# Run full frontend test suite
cd browser && npx vitest run
```
