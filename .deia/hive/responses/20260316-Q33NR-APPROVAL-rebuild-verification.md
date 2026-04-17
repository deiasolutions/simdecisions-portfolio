# Q33N Response: TASK-R13 Task File Overwritten

**From:** Q33N
**To:** Q33NR
**Date:** 2026-03-16
**Re:** TASK-R13 task file correction per your approval

---

## Action Taken

**Overwrote** `.deia/hive/tasks/2026-03-15-TASK-R13-full-integration-verify.md` to match your briefing requirements.

---

## Key Changes from Old Task File

| Aspect | Old Task | New Task (Per Briefing) |
|--------|----------|-------------------------|
| **Code changes** | Allowed ("Fix Cross-Task Regressions" section) | **FORBIDDEN** (verification only) |
| **Deliverable 3** | "Fix Cross-Task Regressions" | "Regression Documentation" (document, don't fix) |
| **Constraints** | "Fix only regressions caused by rebuild" | "NO CODE CHANGES. Do NOT fix anything." |
| **Response section 8** | List remaining failures | GREEN LIGHT or BLOCKING ISSUES LIST |

---

## What the Task Now Requires

### The bee MUST:
1. Run both test suites (`pytest tests/hivenode/` + `vitest run`)
2. Capture full output with pass/fail counts by module
3. Document any failures with full tracebacks
4. Report final status as:
   - **GREEN LIGHT** if all tests pass (969+ hivenode, 1122+ browser)
   - **BLOCKING ISSUES LIST** if any fail (with module, error, traceback, recommended fix)

### The bee MUST NOT:
- Write any code changes
- Fix any regressions
- Skip any tests
- Implement any recommended fixes

---

## Task File Ready for Review

The corrected task file is now at:
- `.deia/hive/tasks/2026-03-15-TASK-R13-full-integration-verify.md`

**All 8 mandatory response sections are specified.**

**Constraint "NO CODE CHANGES" is explicit in 3 places:**
1. Objective section
2. Constraints section
3. Deliverable 4 (document, don't fix)

---

## Next Step Options

If you approve this task file:
1. I will dispatch the bee (Sonnet model as specified in briefing)
2. Bee will run tests and write response file
3. I will review bee's response
4. If failures found: I will create targeted fix tasks for each blocking issue
5. If all pass: Green light for commit

**Awaiting your approval to dispatch.**

---

**Q33N**
