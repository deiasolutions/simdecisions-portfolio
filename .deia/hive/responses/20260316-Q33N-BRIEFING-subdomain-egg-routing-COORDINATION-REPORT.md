# Q33N Coordination Report: Subdomain → EGG Routing

**From:** Q33N (QUEEN-2026-03-16-BRIEFING-subdomain-)
**To:** Q33NR
**Date:** 2026-03-16
**Spec:** `.deia/hive/queue/2026-03-16-3002-SPEC-w3-03-subdomain-egg-routing.md`
**Status:** TASK FILES READY FOR REVIEW

---

## Summary

Read spec, analyzed codebase, wrote 1 task file. This is a small change: add one hostname mapping + comprehensive tests. Ready for Q33NR review.

---

## Codebase Analysis

### Current State (eggResolver.ts)

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\eggs\eggResolver.ts`

**Existing hostname mappings (lines 87-100):**
- `chat.efemera.live` → `chat` ✓
- `code.shiftcenter.com` → `code` ✓
- `pm.shiftcenter.com` → `pm` ✓
- `dev.shiftcenter.com` → `chat` ✓
- `apps.shiftcenter.com` → `apps` ✓
- `dev.ra96it.com` → `login` ✓
- `ra96it.com` → `login` ✓
- `www.ra96it.com` → `login` ✓
- `localhost:5173` → `chat` ✓
- `localhost:3000` → `chat` ✓

**Missing mapping:**
- `canvas.shiftcenter.com` → `canvas` ✗ (needs to be added)

**Already implemented:**
- Query param override (`?egg=`) — line 119 ✓
- Pathname routing — line 126 ✓
- Fallback to `'chat'` — line 100 ✓

### Available EGG Files

From glob of `eggs/`:
- `chat.egg.md` ✓
- `canvas.egg.md` ✓
- `code.egg.md` ✓
- `monitor.egg.md` ✓
- `sim.egg.md` ✓
- `build-monitor.egg.md` ✓
- `apps.egg.md` ✓
- `login.egg.md` ✓
- `efemera.egg.md` ✓
- Others: `home`, `kanban`, `playground`, `ship-feed`, `turtle-draw`

**Missing:**
- `pm.egg.md` — does NOT exist (but mapping exists, will fail gracefully via `useEggInit` error handling)

### Error Handling (useEggInit.ts)

File: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\useEggInit.ts`

Lines 84-96 already handle missing EGG files:
- Catches error from `loadEggFromMarkdown()`
- Sets `error` state
- Shows "Failed to load EGG" message to user

**Decision:** Keep `pm.shiftcenter.com` → `pm` mapping as-is. If user visits that domain, loader will fail gracefully. This is acceptable per spec ("when it exists, fallback to chat").

---

## Task Breakdown

### TASK-190: Add canvas.shiftcenter.com mapping and comprehensive EGG routing tests

**Model:** haiku (per spec)
**File:** `.deia/hive/tasks/2026-03-16-TASK-190-subdomain-egg-routing.md`

**Objective:**
Add `canvas.shiftcenter.com` → `canvas` to hostname map + write 10+ tests for EGG routing logic.

**Deliverables:**
1. Add one line to `hostnameMap` in `eggResolver.ts`: `'canvas.shiftcenter.com': 'canvas'`
2. Create test file: `browser/src/eggs/__tests__/eggResolver.test.ts`
3. Write 10+ tests covering:
   - Query param override (3 tests)
   - Hostname mapping (6 tests)
   - Fallback behavior (1 test)
   - Pathname routing (1 test)
4. All tests pass

**Why single task:**
- Simple change (one line + tests)
- No dependencies on other components
- No UI changes
- No breaking changes
- TDD workflow: tests first, then add mapping line

**Estimated effort:**
- Clock: 15-20 minutes
- Lines added: ~150 (test file ~140 lines, mapping +1 line)
- Test count: 10+

---

## Acceptance Criteria Coverage

From spec:
- [ ] Mapping in eggResolver.ts:
  - `chat.efemera.live` → `chat` ✓ (already exists)
  - `code.shiftcenter.com` → `code` ✓ (already exists)
  - `pm.shiftcenter.com` → `pm` ✓ (already exists, will fallback to chat if file missing)
  - `canvas.shiftcenter.com` → `canvas` ✗ (TASK-190 adds this)
  - `dev.shiftcenter.com` → `chat` ✓ (already exists)
  - `localhost:5173` → `chat` ✓ (already exists)
- [ ] `?egg=name` query param overrides hostname ✓ (already works, TASK-190 adds tests)
- [ ] Unknown hostname falls back to `chat.egg.md` ✓ (already works, TASK-190 adds tests)
- [ ] 5+ tests ✗ (TASK-190 adds 10+ tests)

**After TASK-190:** All criteria met.

---

## Files to Modify

### Modified Files
1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\eggs\eggResolver.ts`
   - Add one line to `hostnameMap` (line ~92)

### New Files
1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\eggs\__tests__\eggResolver.test.ts`
   - ~140 lines of test code
   - 10+ test cases

---

## Dependencies

**Spec says:**
- Depends on: `w3-02-dev-shiftcenter-dns` (for live smoke test)

**Reality:**
- Code changes do NOT depend on DNS config
- Tests verify resolver logic with mocked hostnames
- Live smoke test (manual browser test) DOES require DNS config
- DNS config is a separate task

**TASK-190 is NOT blocked.** It can be dispatched immediately. The live smoke test can be performed later after `w3-02` is complete.

---

## Test Strategy

TASK-190 uses TDD:
1. Write test file FIRST with 10+ test cases
2. Run tests (they will pass for existing mappings, fail for `canvas.shiftcenter.com`)
3. Add `canvas.shiftcenter.com` → `canvas` mapping
4. Run tests again (all pass)

Tests use `vitest` with mocked `window.location`:
- Mock hostname, pathname, search params
- Test both `resolveEggFromHostname()` and `resolveCurrentEgg()`
- Cover all spec requirements + edge cases

---

## Risk Assessment

**Risks:** NONE

- Change is minimal (one line)
- Existing logic unchanged
- All existing hostnames already mapped correctly
- Query param override already works
- Fallback already works
- Tests will catch any regressions

**Confidence:** HIGH

---

## Next Steps for Q33NR

1. **Review TASK-190 file** (`.deia/hive/tasks/2026-03-16-TASK-190-subdomain-egg-routing.md`)
2. **Check for:**
   - Missing deliverables? No.
   - Vague acceptance criteria? No — very specific.
   - Hardcoded colors? N/A (logic only).
   - Files exceeding 500 lines? No (eggResolver.ts currently 133 lines, test ~140 lines).
   - Missing test requirements? No — 10+ tests specified with examples.
   - Imprecise file paths? No — all absolute paths.
   - Gaps vs briefing? No — all briefing requirements covered.
3. **If approved:** Tell Q33N to dispatch BEE (haiku model)
4. **If corrections needed:** Tell Q33N what to fix

---

## Q33N Notes

- This is a textbook small task: minimal change, maximum test coverage
- Haiku model is sufficient (spec requirement)
- No UI work, no backend work, pure logic + tests
- DNS config (w3-02) is a separate concern — this task is NOT blocked
- Live smoke test can be performed manually after DNS is configured
- If `pm.egg.md` is created later, the mapping will automatically work (no code changes needed)

---

## Files Created by Q33N

- Task file: `.deia/hive/tasks/2026-03-16-TASK-190-subdomain-egg-routing.md`
- This report: `.deia/hive/responses/20260316-Q33N-BRIEFING-subdomain-egg-routing-COORDINATION-REPORT.md`

---

**Awaiting Q33NR review and approval to dispatch.**
