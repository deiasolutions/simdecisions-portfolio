# SPEC: Estimation Calibration — Integration Tests + Documentation

## Priority
P1

## Depends On
EST-03

## Objective
Write end-to-end integration tests covering full estimation workflows (import -> calibrate -> budget), add CLI help text, and document the estimation calibration system.

## Context
Phase 4 (final) of the estimation calibration ledger. After EST-01/02/03 built the schema, data import, and calibration engine, this task validates the full system with integration tests and ensures documentation.

Design doc: `.deia/hive/responses/20260406-BRIEFING-ESTIMATION-CALIBRATION-LEDGER-RESPONSE.md`
Task file: `.deia/hive/tasks/2026-04-06-TASK-EST-04-integration-tests.md`

Files to read first:
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/_tools/estimates.py` — CLI (EST-02/03 created this)
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/tasks/2026-04-06-TASK-EST-04-integration-tests.md` — full task spec with test scenarios

## Acceptance Criteria
- [ ] End-to-end test: import scheduler -> simulate completed tasks -> calibration updates -> budget changes
- [ ] Validation test: compare response file Cs vs build monitor token-computed Cs (within 10%)
- [ ] Manual workflow test: record 10 tasks, compute calibration, verify factors
- [ ] Trend test: 3 weeks of data, verify weekly grouping and "Improving" trend
- [ ] Filter tests: --type, --model, --phase work on compare/budget/trend
- [ ] Edge case tests: no data, all complete, division by zero, missing files
- [ ] `--help` text exists for all 9 commands
- [ ] README.md has "Estimation Calibration" section (200-300 words)
- [ ] Smoke test passes: all commands execute without errors on test data
- [ ] 10+ integration tests
- [ ] All tests pass: `python -m pytest tests/hivenode/inventory/test_estimates_integration.py -v`

## Smoke Test
- [ ] `python _tools/estimates.py --help` shows all commands
- [ ] `python _tools/estimates.py import-scheduler --help` shows usage
- [ ] `python -m pytest tests/hivenode/inventory/test_estimates_integration.py -v` all pass

## Model Assignment
haiku

## Constraints
- No file over 500 lines
- No stubs — all tests fully implemented
- Use pytest fixtures for test database setup/teardown
- Mock httpx for build monitor API
- TDD
- Response file: `.deia/hive/responses/20260406-TASK-EST-04-RESPONSE.md`
