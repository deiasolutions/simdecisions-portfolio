# TASK-R17: Register or port Phase NL routes

## Objective
Fix the 15 test failures in `tests/hivenode/test_phase_nl_routes.py` where `/api/phase/nl-to-ir` returns 404.

## Context
R13 verification found 15 failures. The NL-to-IR route translates natural language to intermediate representation flows. This endpoint was likely created during a wave-2 task and lost in the git reset. The test file survived but the route module may be missing or unregistered.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_phase_nl_routes.py` (what the tests expect)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\__init__.py` (current registrations)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\phase_ir\` (check for nl_routes module)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260316-TASK-R13-RESPONSE.md`

## Deliverables
- [ ] Check if route module exists (hivenode/routes/phase_nl_routes.py or engine/phase_ir/nl_routes.py)
- [ ] If exists but unregistered: register it in __init__.py
- [ ] If missing: check platform repo for source, port it
- [ ] If no platform source: implement based on test expectations (tests define the contract)
- [ ] Run: `python -m pytest tests/hivenode/test_phase_nl_routes.py -v`
- [ ] All 15 tests must pass

## Constraints
- Do NOT modify test files
- If porting from platform, follow existing patterns in hivenode/routes/
- Route must accept POST with {text, model, api_key} and return {flow_data, metadata, validation_result}

## Acceptance Criteria
- [ ] `/api/phase/nl-to-ir` endpoint responds (not 404)
- [ ] All 15 Phase NL route tests pass
- [ ] No regressions in other phase_ir tests
- [ ] Route registered in __init__.py

## Response Requirements — MANDATORY
Write response to: `.deia/hive/responses/20260316-TASK-R17-RESPONSE.md`
All 8 sections required.
