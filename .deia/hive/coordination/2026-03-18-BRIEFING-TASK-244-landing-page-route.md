# BRIEFING: Wire LandingPage route into App.tsx

**To:** Q33N (Queen Coordinator)
**From:** Q33NR (Regent)
**Date:** 2026-03-18
**Spec:** `.deia/hive/queue/2026-03-18-SPEC-REQUEUE-TASK244-landing-page-route.md`

---

## Objective

Wire the existing `LandingPage` component into `App.tsx` so that visiting `/` without an `?egg=` param shows the landing page instead of loading a Shell with an EGG.

## Context

### What Already Exists (DO NOT recreate)
- `browser/src/pages/LandingPage.tsx` — full component (57 lines)
- `browser/src/pages/LandingPage.css` — styles
- `browser/src/pages/__tests__/LandingPage.test.tsx` — tests

### The Problem
Currently, `App.tsx` always calls `useEggInit()`, which:
1. Calls `resolveCurrentEgg()` from `eggResolver.ts`
2. This function checks for `?egg=` param, then pathname, then hostname mapping
3. When visiting `/` with no params, it falls back to hostname mapping (returns 'chat' for localhost)
4. Shell loads with the fallback EGG instead of showing the LandingPage

### The Solution
Modify `App.tsx` to:
1. Check if URL has `?egg=` parameter OR non-empty pathname
2. If YES → use existing flow (call `useEggInit()` and render Shell)
3. If NO → render `LandingPage` directly (skip `useEggInit()` entirely)

### Key Insight
The landing page should show when:
- URL is exactly `/` (no pathname segments)
- AND no `?egg=` parameter exists
- (Hostname doesn't matter — any hostname with `/` and no params shows landing)

### Files to Read First
- `browser/src/App.tsx` (current routing logic)
- `browser/src/pages/LandingPage.tsx` (already exists)
- `browser/src/eggs/eggResolver.ts` (how egg param is parsed)
- `browser/src/shell/useEggInit.ts` (what happens when EGG is loaded)

### Files to Modify
- `browser/src/App.tsx` — add LandingPage import + conditional routing logic

## Deliverables

1. **App.tsx changes:**
   - Import `LandingPage` from `./pages/LandingPage`
   - Add logic to detect landing page condition (no egg param, no pathname)
   - Conditionally render LandingPage OR existing Shell flow
   - NO changes to existing Shell rendering logic (preserve all current behavior)

2. **Tests:**
   - Existing `LandingPage.test.tsx` must still pass
   - If `App.test.tsx` exists, it must still pass
   - Full frontend test suite must pass (`cd browser && npx vitest run`)

3. **No regressions:**
   - `/` with `?egg=canvas` → still loads Shell with Canvas EGG
   - `/chat` → still loads Shell with Chat EGG
   - Any hostname with `?egg=xxx` → still loads Shell with that EGG

## Constraints

- **Rule 3:** CSS uses `var(--sd-*)` only (already satisfied by LandingPage.css)
- **Rule 4:** No file over 500 lines (App.tsx is ~102 lines, will stay under 150)
- **Rule 6:** NO STUBS — full implementation
- **DO NOT recreate LandingPage.tsx or its CSS** — they already exist and work

## Model Assignment

**Model:** sonnet (routing logic requires careful testing)

## Priority

P2

---

## What Q33N Should Do

1. **Write ONE task file** for a bee to:
   - Read App.tsx, LandingPage.tsx, eggResolver.ts
   - Modify App.tsx to conditionally render LandingPage
   - Run all frontend tests
   - Write response file with test results

2. **Return task file to Q33NR for review** (do NOT dispatch yet)

3. **After Q33NR approval:** Dispatch ONE bee (sonnet) with the task

4. **After bee completes:** Review response file, verify tests pass, report to Q33NR

---

## Expected Bee Response Checklist

When reviewing the bee's response file, verify:
- [ ] App.tsx imports LandingPage
- [ ] Conditional logic checks for egg param AND pathname
- [ ] Landing page renders when both are absent
- [ ] Shell renders when either is present
- [ ] All existing tests still pass
- [ ] No new test failures
- [ ] No regressions on Shell loading
- [ ] Response file has all 8 sections

---

## Reference: Original Spec Location

- **Original spec:** `.deia/hive/queue/_done/2026-03-16-SPEC-TASK-244-landing-page.md`
- **Previous bee response:** `.deia/hive/responses/20260317-TASK-244-RESPONSE.md`
- **Failure reason:** Bee created LandingPage component but never wired the route in App.tsx

---

**END BRIEFING**
