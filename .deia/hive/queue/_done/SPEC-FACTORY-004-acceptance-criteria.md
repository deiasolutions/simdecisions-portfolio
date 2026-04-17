---
id: FACTORY-004
priority: P1
model: sonnet
role: bee
depends_on:
  - FACTORY-001
---
# SPEC-FACTORY-004: Acceptance Criteria Evaluation

## Priority
P1

## Model Assignment
sonnet

## Depends On
- FACTORY-001

## Intent
Implement typed acceptance gates per node. After a bee completes, the executor evaluates output against the spec's `acceptance_criteria` before marking it BUILT.

## Files to Read First
- `.deia/hive/backlog/PRISM-IR-FACTORY-DUAL-LOOP-v1.1.prism.md` — Section 1.2 (AcceptanceCriteria variants)
- `.deia/hive/scripts/queue/spec_processor.py` — where bee output is evaluated
- `.deia/hive/scripts/queue/run_queue.py` — post-build validation
- `.deia/hive/scripts/queue/spec_parser.py` — SpecFile with acceptance_criteria field

## Acceptance Criteria
- [ ] Acceptance criteria schemas defined per content_type:
  - `python_file`: syntax_valid, imports_resolve, tests_pass, linting_clean
  - `react_component`: syntax_valid, builds_clean, renders_without_crash
  - `architecture_doc`: sections_present, round_trip_valid
  - `task_decomposition`: children_defined, no_orphan_refs, coverage_complete
  - `null` (fallback): human_approved
- [ ] `evaluate_acceptance(spec, output_path)` function:
  - Reads acceptance_criteria from spec
  - Runs each check
  - Returns result object: {passed: bool, checks: [{name, passed, detail}]}
- [ ] All criteria must pass for BUILT status
- [ ] Any failure produces FAILED with specific `failure_reason` listing which checks failed
- [ ] Acceptance results logged (which passed, which failed, timing)
- [ ] Tests: python_file passes all checks, python_file fails syntax, fallback requires human_approved

## Constraints
- `python_file` checks: use `py_compile` for syntax, `ast` for imports, subprocess for tests
- `react_component` checks: use `npx tsc --noEmit` for syntax, `npx vite build` for builds
- For checks that can't run locally (e.g., renders_without_crash), mark as `skipped` not `failed`
- No file over 500 lines
- TDD: tests first
