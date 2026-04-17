# BRIEFING: Fix BUS.__init__() ledger_publisher signature breaking 58 tests

**From:** Q33NR (Regent)
**To:** Q33N (Queen Coordinator)
**Date:** 2026-03-18
**Priority:** P0
**Model:** sonnet

---

## Objective

Fix BUS class signature change that broke 58+ tests across governance, dispositions, heartbeat, and cloud storage modules.

## Problem

The `BUS.__init__()` constructor now requires a `ledger_publisher` argument, but 58+ test files instantiate `BUS()` without providing it.

**Error pattern:**
```
TypeError: BUS.__init__() missing 1 required positional argument: 'ledger_publisher'
```

**Affected test files (58+ total):**
- `tests/hivenode/governance/test_gate_enforcer_integration.py` (16 tests)
- `tests/hivenode/governance/test_dispositions.py` (17 tests)
- `tests/hivenode/governance/test_heartbeat.py` (15+ tests)
- `tests/hivenode/governance/test_heartbeat_metadata.py` (additional tests)
- `tests/hivenode/cloud/test_cloud_adapter_e2e.py` (13 tests)
- `tests/hivenode/governance/test_enforcer.py` (2 errors)

## Context

From full test sweep report: `.deia\hive\responses\20260318-FULL-TEST-SWEEP-REPORT.md`

The BUS class signature was changed recently (likely during BL-203 or related work). The `ledger_publisher` parameter was added as a required argument, but the test suite was not updated.

This is blocking **58+ tests** and is classified as **P0 Critical**.

## Fix Approaches

**Option A (RECOMMENDED):** Make `ledger_publisher` parameter optional with a default value
- Less churn, backward compatible
- Tests that don't care about ledger can pass `None` or use default
- Minimal test file modifications
- Pattern: `def __init__(self, ledger_publisher=None):`

**Option B:** Update all 58+ test files to pass `ledger_publisher`
- More invasive
- Only if `ledger_publisher` is truly required for all BUS operations
- Higher risk of introducing new issues

**Recommendation:** Choose Option A unless you discover during investigation that `ledger_publisher` must be non-optional for BUS to function.

## Files to Investigate

**Source file (BUS class):**
- Find and read the BUS class definition (likely in `hivenode/governance/` or `hivenode/infrastructure/`)
- Check: grep -r "class BUS" hivenode to locate it

**Test files to verify after fix:**
- `tests/hivenode/governance/test_gate_enforcer_integration.py`
- `tests/hivenode/governance/test_dispositions.py`
- `tests/hivenode/governance/test_heartbeat.py`
- `tests/hivenode/governance/test_heartbeat_metadata.py`
- `tests/hivenode/cloud/test_cloud_adapter_e2e.py`
- `tests/hivenode/governance/test_enforcer.py`

## Acceptance Criteria

- [ ] BUS class constructor allows instantiation without `ledger_publisher` (Option A) OR all test files updated (Option B)
- [ ] All 58+ affected tests pass
- [ ] No regressions in governance/dispositions/heartbeat/cloud modules
- [ ] Test command: `python -m pytest tests/hivenode/governance/ tests/hivenode/cloud/test_cloud_adapter_e2e.py -v`

## Task Breakdown Instructions for Q33N

**Your job:**
1. **Locate the BUS class** — search hivenode/ for "class BUS", determine exact file path
2. **Read the BUS class** — understand current signature, why ledger_publisher was added
3. **Choose fix approach** — Option A (default value) vs Option B (update all tests)
4. **Write task file(s)** for bee(s):
   - If Option A: Single task to modify BUS.__init__() signature
   - If Option B: May need multiple tasks (one per test module or one for all tests)
5. **Include test verification** — Task must specify running all affected tests
6. **Return to Q33NR** for review before dispatching bees

## Constraints

- **Rule 5 (TDD):** If modifying BUS class, write/update tests first
- **Rule 6 (NO STUBS):** Fix must be complete, no placeholders
- **Rule 10 (NO GIT OPS):** Bee cannot commit without Q88N approval
- **Response file required:** 8 sections, to `.deia\hive\responses\`

## Notes

- This is part of post-30-item-build cleanup
- E2E tests are also failing due to server startup timeout, but that's a separate issue (BUG-043)
- The BUS class is likely part of the governance/event ledger system added in recent work

---

**Next Step:** Q33N reads this briefing, investigates BUS class, writes task file(s), returns for Q33NR review.
