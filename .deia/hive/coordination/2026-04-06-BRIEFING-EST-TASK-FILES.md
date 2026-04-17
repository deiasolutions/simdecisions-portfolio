# BRIEFING: Create EST Task Files

**From:** Q33NR
**To:** Q33N
**Date:** 2026-04-06
**Priority:** P0

## Context

The estimation calibration ledger design is approved. The design doc is at:
`.deia/hive/responses/20260406-BRIEFING-ESTIMATION-CALIBRATION-LEDGER-RESPONSE.md`

The design defines 4 tasks (TASK-EST-01 through TASK-EST-04). The task FILES were not created. Create them now.

## Deliverables

Create these 4 task files in `.deia/hive/tasks/`:
1. `2026-04-06-TASK-EST-01-schema-migration.md`
2. `2026-04-06-TASK-EST-02-data-collection.md`
3. `2026-04-06-TASK-EST-03-calibration-engine.md`
4. `2026-04-06-TASK-EST-04-integration-tests.md`

Each task file must contain:
- Objective, Context, Files to Read First
- Deliverables with checkboxes
- Test Requirements
- Acceptance Criteria
- Smoke Test
- Constraints
- Response Requirements (8 mandatory sections)

Pull all content from the approved design doc. Include the schema definitions, algorithm code, CLI command specs, and file paths directly in the task files so bees have everything they need.

## Key Details from Design

- **EST-01:** Schema + migration. Tables: `inv_estimates` (19 cols), `inv_calibration` (7 cols). Haiku. No deps.
- **EST-02:** Data collection CLI (`_tools/estimates.py`). Commands: import-scheduler, import-actuals, import-responses, record, actual. Sonnet. Depends on EST-01.
- **EST-03:** Calibration engine + CLI commands: calibration, compare, budget, trend. Sonnet. Depends on EST-02.
- **EST-04:** Integration tests + docs. Haiku. Depends on EST-03.

## Constraints
- Each task file: 80-150 lines (enough detail for a bee to work independently)
- Include actual schema code, algorithm code, CLI specs from design doc
- Use absolute Windows paths for Files to Read First
- Follow standard task file format (same as TASK-MCP-QUEUE-* files)
