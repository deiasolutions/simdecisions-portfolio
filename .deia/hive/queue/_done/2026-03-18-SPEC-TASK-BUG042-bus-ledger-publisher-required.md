# SPEC-TASK-BUG042: Fix BUS.__init__() ledger_publisher signature breaking 58 tests

**Priority:** P0
**Model:** sonnet
**Component:** governance/bus

## Objective
Fix BUS class signature change that broke 58+ tests across governance, dispositions, heartbeat, and cloud storage modules.

## Problem
`BUS.__init__()` now requires `ledger_publisher` argument, but 58+ test files instantiate BUS() without it.

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

## Reference
Full test sweep report: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260318-FULL-TEST-SWEEP-REPORT.md`

See section: "Governance (16)", "Dispositions (17)", "Heartbeat (15)", "Cloud storage E2E (13)"

## Suggested Fix Approach
**Option A (recommended):** Make `ledger_publisher` optional with a default value
- Less churn, backward compatible
- Tests that don't care about ledger can pass None or use default

**Option B:** Update all 58 test files to pass ledger_publisher
- More invasive
- Only if ledger_publisher is truly required for all BUS operations

## Files to Check
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\governance\bus.py` (BUS class)
- All test files listed above

## Success Criteria
- [ ] BUS class constructor allows instantiation without ledger_publisher (or all tests updated)
- [ ] All 58+ affected tests pass
- [ ] No regressions in governance/dispositions/heartbeat/cloud modules

## Response File
Write to: `.deia\hive\responses\20260318-BUG-042-RESPONSE.md`
