---
id: FACTORY-002
priority: P0
model: sonnet
role: bee
depends_on:
  - FACTORY-001
---
# SPEC-FACTORY-002: Dependency Resolution

## Priority
P0

## Model Assignment
sonnet

## Depends On
- FACTORY-001

## Intent
Implement non-parent dependency checking so the scheduler blocks specs whose `depends_on` list has unmet dependencies. When a dependency completes, blocked specs re-evaluate and promote if ready.

## Files to Read First
- `.deia/hive/backlog/PRISM-IR-FACTORY-DUAL-LOOP-v1.1.prism.md` — Sections 4.1 (check_dependencies, unblock_dependents), 7.1
- `hivenode/scheduler/scheduler_daemon.py` — scan_backlog(), compute_schedule()
- `.deia/hive/scripts/queue/run_queue.py` — _deps_satisfied()
- `.deia/hive/scripts/queue/spec_parser.py` — SpecFile with depends_on field (from FACTORY-001)

## Acceptance Criteria
- [ ] Scheduler checks `depends_on` list before promoting spec to ready
- [ ] A spec is BLOCKED if any ID in `depends_on` is not in `_done/` (BUILT or INTEGRATED)
- [ ] `find_blocked_specs()` function: returns all specs with unmet depends_on
- [ ] `check_unblocked()` function: given a completed spec ID, finds specs that were blocked on it and re-evaluates
- [ ] When dependency completes and moves to `_done/`, blocked specs re-evaluate automatically on next scheduler cycle
- [ ] Circular dependency detection at spec parse time — reject with clear error message
- [ ] Tests: spec with unmet dep stays blocked, dep completes then spec unblocks, circular dep rejected

## Constraints
- Dependency IDs match the `id` field from YAML frontmatter (not filenames)
- Both `depends_on` from frontmatter and `## Depends On` from markdown body are checked
- No file over 500 lines
- TDD: tests first
