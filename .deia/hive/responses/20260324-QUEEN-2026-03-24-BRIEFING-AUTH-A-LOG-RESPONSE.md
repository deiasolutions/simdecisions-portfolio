# Q33N Response: AUTH-A LoginPage Rebrand Task File

**Status:** TASK FILE READY FOR Q33NR REVIEW
**Model:** Sonnet
**Date:** 2026-03-24

---

## Task File Created

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\2026-03-24-TASK-AUTH-A-LOGIN-REBRAND.md`

---

## What Was Prepared

1. **Read foundational files:**
   - `.deia/BOOT.md` — 10 Hard Rules, response template, test commands
   - `.deia/HIVE.md` — Q33N workflow, dispatch commands, inventory process

2. **Read referenced files:**
   - `browser/src/primitives/auth/LoginPage.tsx` (275 lines)
   - `browser/src/primitives/auth/__tests__/authStore.test.ts` (136 lines, for reference)

3. **Analyzed current state:**
   - Environment variable: `VITE_RA96IT_API` (line 23)
   - UI branding: "ra96it" appears at lines 158, 178, 194
   - localStorage keys: `ra96it_token` and `ra96it_user` (out of scope — AUTH-B task)
   - GitHub branding: logo SVG, badge, consent flow (unchanged)

4. **Wrote task file** with:
   - Objective: Pure branding change (env var + UI text)
   - Context: Scope limited to LoginPage.tsx only
   - Deliverables: 4 specific code changes + 4 test cases
   - Test requirements: TDD approach, 4+ passing tests
   - Constraints: 10 Hard Rules compliance
   - Acceptance criteria: 10 specific checkboxes
   - Response requirements: 8-section mandatory format
   - Test commands: 3 levels (file, directory, full suite)

---

## Task Scope Summary

**In Scope:**
- Replace `VITE_RA96IT_API` with `VITE_AUTH_API` (line 23)
- Replace "ra96it" with "hodeia" in UI text (lines 158, 178, 194)
- Create LoginPage.test.tsx with 4+ passing tests
- Verify GitHub branding unchanged
- Verify OAuth flow logic unchanged

**Out of Scope (Explicitly Excluded):**
- localStorage keys (`ra96it_token`, `ra96it_user`) — handled in AUTH-B
- authStore.ts modifications
- LoginPage.css modifications
- OAuth flow logic changes
- Dev-login logic changes

---

## Test Requirements

**Minimum 4 Test Cases:**
1. Env var uses `VITE_AUTH_API`
2. UI displays "hodeia" in header (line 194)
3. UI displays "hodeia" when logged in (lines 158, 178)
4. GitHub branding unchanged (logo, badge, consent)

**Test Approach:**
- TDD (tests first, then implementation)
- Vitest + React Testing Library
- Mock `import.meta.env.VITE_AUTH_API`
- Mock fetch API for OAuth/dev-login
- Verify actual rendered text, not props

---

## Acceptance Criteria (10 Total)

- [ ] `VITE_RA96IT_API` → `VITE_AUTH_API` (line 23)
- [ ] "ra96it" → "hodeia" (line 158)
- [ ] "ra96it" → "hodeia" (line 178)
- [ ] "ra96it" → "hodeia" (line 194)
- [ ] GitHub branding unchanged
- [ ] OAuth flow logic unchanged
- [ ] LoginPage.test.tsx created with 4+ tests
- [ ] All tests pass
- [ ] No authStore.ts changes
- [ ] File length under 500 lines

---

## 10 Hard Rules Compliance

✅ **Rule 0:** No "take a break" suggestions
✅ **Rule 1:** Q88N is sovereign
✅ **Rule 2:** Q33N does NOT code (waits for Q33NR approval before dispatch)
✅ **Rule 3:** No hardcoded colors (task specifies no CSS changes)
✅ **Rule 4:** No file over 500 lines (LoginPage.tsx is 275 lines, safe)
✅ **Rule 5:** TDD (tests first, explicitly required)
✅ **Rule 6:** No stubs (full implementation required)
✅ **Rule 7:** Stay in lane (only LoginPage.tsx + LoginPage.test.tsx)
✅ **Rule 8:** Absolute file paths (all paths absolute in task file)
✅ **Rule 9:** Archive after completion (Q33N will archive after bee completes)
✅ **Rule 10:** No git operations (not required for this task)

---

## Model Assignment

**Haiku** — Briefing specifies haiku. This is a straightforward find-replace + test task:
- 4 string replacements (env var + 3 UI text changes)
- 4 test cases (env var check + 3 branding checks)
- No complex logic changes
- No architectural decisions
- TDD approach fits haiku's capabilities

---

## Next Steps (Awaiting Q33NR Approval)

1. **Q33NR reviews** this task file for:
   - Missing deliverables
   - Vague acceptance criteria
   - Gaps vs briefing
   - Hard rules compliance

2. **If Q33NR approves:**
   - Q33N dispatches bee with haiku model
   - Dispatch command: `python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-24-TASK-AUTH-A-LOGIN-REBRAND.md --model haiku --role bee --inject-boot`

3. **After bee completes:**
   - Q33N reads response file
   - Q33N verifies 8 sections present
   - Q33N reports results to Q33NR

---

## Q33NR: Task File Ready for Review

The task file is complete and awaits your review. Please check for:
- [ ] All deliverables specified (code changes + tests)
- [ ] Acceptance criteria precise and measurable
- [ ] Test requirements clear (TDD, 4+ tests, edge cases)
- [ ] Constraints match 10 Hard Rules
- [ ] Scope boundaries clear (no localStorage, no authStore.ts)
- [ ] Model assignment appropriate (haiku)
- [ ] Response requirements (8 sections mandatory)

If approved, ready to dispatch bee.
