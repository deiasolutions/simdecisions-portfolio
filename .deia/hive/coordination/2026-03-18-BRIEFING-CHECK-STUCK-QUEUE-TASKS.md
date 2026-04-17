# BRIEFING: Check 3 Stuck Queue Tasks

## Objective

Three tasks show as "running" in hivenode but their bee processes are long dead (from a previous session). Determine whether each task was actually completed (response file exists, code was written) or genuinely incomplete.

## The 3 Tasks

1. **QUEUE-TEMP-2026-03-16-SPEC-TASK-246-byok-flow-verified**
   - Spec file: `.deia/hive/queue/2026-03-16-SPEC-TASK-246-byok-flow-verified.md`
   - Check for response files matching `*TASK-246*` or `*byok*` in `.deia/hive/responses/`

2. **QUEUE-TEMP-2026-03-17-SPEC-TASK-BUG025-sim-egg-fails**
   - Spec file: `.deia/hive/queue/2026-03-17-SPEC-TASK-BUG025-sim-egg-fails.md`
   - Check for response files matching `*BUG-025*` or `*BUG025*` or `*sim-egg*` in `.deia/hive/responses/`

3. **QUEUE-TEMP-2026-03-17-SPEC-TASK-BL209-processing-primitive-layout**
   - Spec file: `.deia/hive/queue/2026-03-17-SPEC-TASK-BL209-processing-primitive-layout.md`
   - Check for response files matching `*BL-209*` or `*BL209*` or `*processing-primitive*` in `.deia/hive/responses/`

## What To Do

For each of the 3 tasks:

1. Read the spec file to understand what was assigned.
2. Search `.deia/hive/responses/` for any matching response file (completed or RAW).
3. If a response file exists, read it and determine:
   - Did the bee report COMPLETE or FAILED?
   - Were files actually modified? (Check git status or read the listed files)
   - Did tests pass?
4. If NO response file exists, check if the code changes described in the spec were made anyway (bee may have finished code but crashed before writing the response).

## Deliverables

Write a single report to `.deia/hive/responses/20260318-CHECK-STUCK-TASKS-REPORT.md` with:

- For each task: status assessment (COMPLETED-UNMARKED / INCOMPLETE / UNKNOWN)
- Evidence: what response files exist, what code changes were found
- Recommendation: mark as done, re-dispatch, or discard

## Constraints

- Do NOT write code. Do NOT modify any source files.
- Do NOT run git write operations.
- Do NOT dispatch any bees.
- Read-only investigation.
