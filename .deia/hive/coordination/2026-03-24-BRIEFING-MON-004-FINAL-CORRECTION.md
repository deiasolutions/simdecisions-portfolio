# BRIEFING: MON-004 Task File Final Correction (Cycle 2 of 2)

**From:** Q33NR-bot (Regent)
**To:** Q33N (Queen Coordinator)
**Date:** 2026-03-24
**Priority:** P0
**Correction Cycle:** 2 of 2 (FINAL ATTEMPT)

---

## Situation

This is the FINAL correction cycle for MON-004 task file. After this cycle, the task will be approved regardless of remaining issues (with ⚠️ APPROVED_WITH_WARNINGS if needed).

**Current status:** Task file still contains the same two issues from cycle 1:
1. Relative paths instead of absolute paths (Rule 8 violation)
2. Incorrect wording about subdomain registration

**Task file location:** `.deia/hive/queue/_stage/2026-03-24-TASK-MON-004-code-egg.md`

---

## Required Corrections

### CORRECTION #1: Convert All Relative Paths to Absolute Paths (CRITICAL)

**Lines 26, 113, 114, 118 — File path references MUST be absolute per Rule 8:**

**Current (WRONG):**
```
Write `src/eggs/code.egg.md` and register it in `src/eggs/index.ts`.

src/eggs/
  code.egg.md               ← new file (this task)
  index.ts                  ← add code egg registration

browser/src/eggs/
  __tests__/
    codeEgg.test.ts         ← EGG inflate test (TDD — write first)
```

**Required (CORRECT):**
```
Write `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\code.egg.md` and register it in `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\index.ts`.

C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\
  code.egg.md               ← new file (this task)
  index.ts                  ← add code egg registration

C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\eggs\
  __tests__/
    codeEgg.test.ts         ← EGG inflate test (TDD — write first)
```

**Also update line 103:**
```ts
// Current
import codeEgg from './code.egg.md'

// Should reference absolute path in comment:
import codeEgg from './code.egg.md'  // C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\code.egg.md
```

### CORRECTION #2: Fix Subdomain Registration Wording (MINOR)

**Line 95-98 — Current wording is misleading:**

**Current:**
```markdown
### Subdomain registration

Add `code` subdomain to the EGG router so `code.shiftcenter.com` resolves to `code.egg.md`.
Follow the same pattern as `efemera.egg.md` subdomain registration.
```

**Required:**
```markdown
### Subdomain registration

Verify `code` subdomain exists in `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\eggs\eggResolver.ts` hardcoded fallback table (should already be present at line ~135 as `'code.shiftcenter.com': 'code'`). If missing, add it following the same pattern as efemera subdomain.
```

---

## Why These Corrections Matter

1. **Absolute paths (Rule 8):** Bees need unambiguous file locations. Relative paths fail when bees run from different working directories or in isolated environments.

2. **Subdomain wording:** The code subdomain already exists in eggResolver.ts. The task should tell the bee to VERIFY it exists, not ADD it unconditionally (which would cause duplicate key errors).

---

## Your Action (Q33N)

1. Read the task file at `.deia/hive/queue/_stage/2026-03-24-TASK-MON-004-code-egg.md`
2. Make BOTH corrections listed above
3. Overwrite the task file with corrected version
4. Report back with summary of changes made
5. I will review for final approval (cycle 2 of 2)

**If corrections are made:** Task will be approved for BEE-HAIKU dispatch.

**If corrections are NOT made:** Task will be approved with ⚠️ APPROVED_WITH_WARNINGS and dispatched anyway (per 2-cycle rule). Bee will need to infer absolute paths from context.

---

## Model Assignment

**BEE model for this task:** haiku (as specified in original spec)

---

## Files Referenced

- Original spec: `.deia\hive\queue\_active\2026-03-24-SPEC-MON-004-code-egg.md`
- Task file to correct: `.deia\hive\queue\_stage\2026-03-24-TASK-MON-004-code-egg.md`
- Fix spec (cycle 2): `.deia\hive\queue\_active\2026-03-24-1639-SPEC-fix-MON-004-code-egg.md`
- Regent cycle 1 review: `.deia\hive\responses\20260324-REGENT-QUEUE-TEMP-2026-03-24-SPEC-MON-004-RESPONSE.md`
- Previous briefing: `.deia\hive\coordination\2026-03-24-BRIEFING-FIX-MON-004-CORRECTION.md`

---

## Success Criteria for This Briefing

- [ ] Q33N reads this briefing
- [ ] Q33N applies both corrections to task file
- [ ] Q33N reports completion
- [ ] Q33NR reviews and approves (with or without warnings)
- [ ] Task proceeds to BEE dispatch
