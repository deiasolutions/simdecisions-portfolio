# BUG-043: E2E Server Startup Timeout — TASK FILE READY FOR REVIEW

**Status:** TASK FILE WRITTEN (awaiting Q33NR review)
**Model:** Sonnet (Q33N coordinator)
**Date:** 2026-03-18

---

## Summary

Q33N has completed investigation and written task file for BUG-043 (E2E server startup timeout).

**Task file location:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\2026-03-18-TASK-BUG-043-E2E-SERVER-STARTUP-TIMEOUT.md`

**Recommended model:** Sonnet (investigation + debugging required)

---

## Investigation Findings

### What Q33N discovered:

1. **BUG-042 is NOT the blocker here**
   - BUG-042 (BUS signature) is still in progress but affects different tests
   - BUG-042 affects: governance, dispositions, heartbeat test modules
   - Those modules import/instantiate BUS class
   - E2E server startup doesn't import BUS (verified: `from hivenode.main import app` succeeds)

2. **The E2E timeout is real but cause unknown**
   - Confirmed: All 28 E2E tests fail with `httpx.ConnectTimeout`
   - Server never responds to `/health` within 10 seconds
   - Test fixture tries to capture stderr/stdout but they appear empty

3. **Manual import works fine**
   - `python -c "from hivenode.main import app"` succeeds
   - No BUS errors, no import errors
   - Only fails in subprocess with E2E fixture environment variables

4. **Root cause hypothesis:**
   - Subprocess environment variables may trigger startup issues
   - OR: Database/storage initialization missing in tmp directories
   - OR: Logs are buffered and not flushed (hiding the real error)

### What the task will do:

**Phase 1:** Actually capture server startup logs
- Modify fixture or create standalone reproducer
- See the REAL error message (currently hidden)

**Phase 2:** Fix root cause
- Based on Phase 1 findings
- Could be fixture fix OR server startup fix

**Phase 3:** Verify all 28 E2E tests pass

---

## Task File Review Points

**Deliverables:**
- [ ] Clear and specific (capture logs, fix root cause, verify 28 tests)

**Test requirements:**
- [ ] Primary test suite specified (test_e2e.py -v)
- [ ] Verification suite specified (test_routes.py, test_storage.py)
- [ ] Success criteria: 28 tests pass, 0 timeouts

**File paths:**
- [ ] All absolute Windows paths (test_e2e.py, main.py, config.py)

**Constraints:**
- [ ] No file over 500 lines (N/A - only fixing fixture or small startup code)
- [ ] No hardcoded colors (N/A - backend code)
- [ ] No stubs (explicit requirement)
- [ ] TDD (if modifying server code, tests first)

**Response file:**
- [ ] Template present (8 sections required)
- [ ] Path specified (20260318-BUG-043-RESPONSE.md)

**Approach clarity:**
- [ ] Investigation phases clear (Phase 1: logs, Phase 2: reproduce, Phase 3: fix)
- [ ] Example fix patterns provided (buffering issue, startup dependency issue)

---

## Recommended Dispatch

**Command:**
```bash
python .deia/hive/scripts/dispatch/dispatch.py \
  .deia/hive/tasks/2026-03-18-TASK-BUG-043-E2E-SERVER-STARTUP-TIMEOUT.md \
  --model sonnet \
  --role bee \
  --inject-boot
```

**Reasoning:**
- Sonnet: Investigation + debugging complexity (need to capture logs, diagnose, fix)
- No timeout needed: Should complete within default limits (log capture is fast)
- Independent of BUG-042: Can dispatch in parallel

---

## Coordination Note

**BUG-042 status:** Still in progress (Q33N dispatched, not returned yet)

**Relationship:**
- Test sweep report hypothesized E2E timeout was caused by BUS signature issue
- Q33N investigation determined they are INDEPENDENT issues
- BUG-042 affects test modules that import BUS class
- BUG-043 affects E2E subprocess startup (no BUS imports)

**Recommendation:** Proceed with BUG-043 dispatch even if BUG-042 incomplete

---

## Files Modified

None (investigation + task file creation only)

---

## Clock / Cost / Carbon

**Q33N work:**
- **Clock:** ~25 minutes (read briefing, spec, test code, manual verification, investigation, task file writing)
- **Cost:** ~$0.08 (reading + grep searches + file reads + task file generation)
- **Carbon:** <1g CO2e

---

## Next Steps (for Q33NR)

1. **Review task file** for:
   - Completeness (all deliverables clear?)
   - File paths (all absolute?)
   - Test requirements (specific commands?)
   - Example fix patterns (helpful for bee?)

2. **If approved:** Dispatch bee with Sonnet model

3. **If corrections needed:** Tell Q33N what to fix

---

**READY FOR Q33NR REVIEW**
