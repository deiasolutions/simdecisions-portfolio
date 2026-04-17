# Dispatch Instruction: TASK-227 LLM Triage Functions

**To:** Q33N (Queen Coordinator)
**From:** Q33NR (Regent)
**Date:** 2026-03-17
**Task:** 2026-03-17-TASK-227-llm-triage-functions.md
**Status:** ✅ APPROVED FOR DISPATCH

---

## Review Complete — All Checks Pass

**Cycle 2 Review Result:** ✅ APPROVED

Both corrections from Cycle 1 have been successfully applied:
- Line 73: Absolute path ✅
- Line 182: Absolute path ✅

All mechanical review checklist items pass:
- ✅ Deliverables match spec
- ✅ File paths absolute (corrected)
- ✅ Test requirements present (12+ tests, mocks, TDD)
- ✅ CSS uses var(--sd-*) (N/A for Python)
- ✅ No files over 500 lines (~100 + ~80)
- ✅ No stubs or TODOs (explicit criteria)
- ✅ Response file template present (8 sections)

---

## Dispatch Authorization

Q33N, you are **AUTHORIZED** to dispatch the Sonnet bee for TASK-227.

**Command:**
```bash
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-17-TASK-227-llm-triage-functions.md --model sonnet --role bee --inject-boot
```

**Expectations:**
- Model: Sonnet
- Estimated cost: ~$0.50
- Estimated time: 45-60 minutes
- Deliverables: `triage.py`, `test_triage.py`, `triage_integration_plan.md`
- Tests: ≥12 tests, all passing

---

## Q33N Instructions (HIVE.md Step 6-9)

### Step 6: Dispatch the bee ✅

Run the dispatch command above.

### Step 7: Monitor and review — STAY ALIVE

After dispatching, **DO NOT EXIT.** Stay alive and poll for completion.

**Monitoring cadence:**
- Poll `.deia/hive/responses/` every 60 seconds for new response file matching `YYYYMMDD-TASK-227-RESPONSE.md` or `YYYYMMDD-*-TASK-227-*-RAW.txt`
- Do not spin (no sub-second loops)
- Do not over-sleep (no 5+ minute gaps)

**When response file appears, immediately review it inline:**
- Are all 8 sections present? If not, dispatch the bee again.
- Did tests pass? If not, write a fix task and dispatch it.
- Were stubs shipped? If so, dispatch the bee again.
- Any regressions on other tests? If so, write a fix task and dispatch it.
- If PASS: mark task as verified in the completion report.

### Step 8: Backfill freed slots

This is the only task in this batch, so no backfill needed.

### Step 9: Report to Q33NR

After the bee completes and you've reviewed the response:
- Write a single completion report to `.deia/hive/responses/`
- Include: task completed, task failed (if any), total tests passed, any issues or follow-ups
- Report to Q33NR (this session)

---

## Cost Tracking

- Briefing + corrections: $2.03 + $0.80 = $2.83
- Estimated bee cost: ~$0.50
- **Total estimated: ~$3.33**

---

**Q33N, proceed with dispatch and monitoring. Q33NR awaits your completion report.**
