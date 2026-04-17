# Briefing: Write Quick Specs for P0 Test Failures → Drop in Queue

## Objective
Write lightweight spec files for the 3 P0 test failures and drop them directly in `.deia/hive/queue/`. These don't need to be exhaustive — a Q33NR will pick them up and flesh them out. Just point to the test sweep report and describe what's broken.

## Context
The full test sweep report is at `.deia/hive/responses/20260318-FULL-TEST-SWEEP-REPORT.md`. Read it.

## P0 Items to Write Specs For

### 1. BUS class signature change (58+ tests broken)
- `BUS.__init__()` now requires `ledger_publisher` argument
- Breaks: governance (16), dispositions (17), heartbeat (15), cloud storage E2E (13), gate enforcer (2)
- Fix: Either make `ledger_publisher` optional with a default, OR update all test instantiations to pass it
- Making it optional is probably the right call — less churn, backward compatible

### 2. E2E server startup failure (28 tests timing out)
- All tests in `tests/hivenode/test_e2e.py` — httpx.ConnectTimeout
- Server fails to start during test setup
- Likely cause: startup crash or port conflict
- Fix: Debug server init, check if BUS signature change broke startup too
- Reference: test sweep report section "E2E integration tests (28)"

### 3. ReliabilityMetadata missing (RAG module blocked)
- `ImportError: cannot import name 'ReliabilityMetadata' from 'hivenode.rag.indexer.models'`
- Blocks ALL RAG tests
- Fix: Either add the class to `hivenode/rag/indexer/models.py` or remove/update the import
- Reference: test sweep report section "Hivenode RAG Module"

## What To Do
For each P0 item:
1. Write a short spec file (objective, what's broken, pointer to test sweep report, suggested fix approach)
2. Set priority P0
3. Set model to sonnet
4. Drop it in `.deia/hive/queue/`
5. Use naming convention: `2026-03-18-SPEC-TASK-BUG0XX-<short-name>.md`

Use the next available BUG IDs. Run `python _tools/inventory.py bug list` to see what's taken, then use the next ones.

## Constraints
- Do NOT write full implementation specs — just enough for a Q33NR to understand the problem and dispatch a bee
- Point to `.deia/hive/responses/20260318-FULL-TEST-SWEEP-REPORT.md` as the reference
- Keep each spec under 50 lines

## Model: sonnet

## Response
Write response to: `.deia/hive/responses/20260318-P0-TEST-FIX-SPECS.md`
