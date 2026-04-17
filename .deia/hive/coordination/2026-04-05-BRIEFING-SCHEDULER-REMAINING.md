# BRIEFING: Scheduler Pipeline — Remaining Work

**From:** Q33NR
**To:** Q33N
**Date:** 2026-04-05
**Priority:** P0

## Context

The scheduler/dispatcher daemon pipeline is built and verified. First live run successfully moved 3 test specs (MW-S01, MW-S02, MW-S03) from backlog/ to queue/. Two issues remain before the pipeline can run unattended for the full 66-task Mobile Workdesk build.

## Issue 1: Dispatcher Slot Count Bug

**Problem:** The dispatcher counts ALL spec files in `_active/` as running bees, but `_active/` currently contains stale specs from old queue-runner sessions (not actually running). This causes negative slot counts:

```json
{"event": "cycle_start", "active": 13, "queued": 1, "slots": -4, "max_bees": 10}
```

**Root cause:** The dispatcher uses `_count_specs_in(queue_dir / "_active")` which just counts files. It doesn't check if those specs are actually being processed by running bees. Old specs sit in `_active/` indefinitely after queue-runner crashes or restarts.

**Fix needed in:** `hivenode/scheduler/dispatcher_daemon.py`

The dispatcher should either:
- (Option A) Only count specs modified within the last 30 minutes as "active" (stale files = not running)
- (Option B) Cross-reference with hivenode build monitor (`GET http://127.0.0.1:8420/build/status`) to get actual running bee count
- (Option C) Ignore `_active/` entirely and only use the build monitor's active count

**Recommendation:** Option A is simplest and doesn't require hivenode to be running. Use file mtime — if a spec in `_active/` hasn't been modified in 30 minutes, it's stale and shouldn't count toward slots.

**Current `_active/` contents:** Should be empty (Q33NR cleaned it). But the CHROME-F2 spec is in queue root and will land in `_active/` when queue-runner picks it up. The fix is needed so future stale specs don't block the dispatcher.

## Issue 2: Remaining 63 MW Spec Files

**Problem:** Only 3 of 66 MW task specs exist in backlog/. The dispatcher can't dispatch tasks without corresponding spec files.

**What's needed:** Generate spec files for all 63 remaining MW tasks and place them in `.deia/hive/queue/backlog/`.

**Task registry (from `scheduler_mobile_workdesk.py` TASKS list):**
The 3 already created: MW-S01, MW-S02, MW-S03
The remaining 63 need specs. Group them into batches for parallel bee dispatch.

**Spec format** (follow the 3 existing specs in backlog/ as templates):
```markdown
# SPEC-MW-{ID}: {description}

## Priority
P1

## Depends On
{list dependency task IDs, or "None"}

## Objective
{1-2 sentences describing what the bee must build}

## Model Assignment
sonnet

## Files to Read First
{relevant source files the bee needs to understand}

## Acceptance Criteria
- [ ] {concrete deliverable 1}
- [ ] {concrete deliverable 2}
- [ ] Tests written first (TDD)
- [ ] All tests pass

## Smoke Test
- {verification step 1}
- {verification step 2}

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs
- TDD required
```

**Important:** Each spec needs REAL content — not boilerplate. The bee reading the spec needs to know:
- What component/file to build or modify
- What the component does (behavior, not just name)
- Which existing files to read for context
- What tests to write

**Batch strategy:** Split the 63 specs across multiple bees:
- Batch 1 (sonnet): Phase 0.5 tests (MW-T01 through MW-T08) — 8 specs
- Batch 2 (sonnet): Phase 1-2 builds (MW-001 through MW-010, MW-V01 through MW-V04) — 14 specs
- Batch 3 (sonnet): Phase 3-4 builds (MW-011 through MW-022, MW-V05 through MW-V08) — 16 specs
- Batch 4 (sonnet): Phase 5 CSS builds (MW-023 through MW-033) — 11 specs
- Batch 5 (sonnet): Phase 6-7 builds + integration (MW-034 through MW-042) — 9 specs
- Batch 6 (haiku): Verify specs (MW-V01 through MW-V08) — already in batches above

Actually — the Q33N should determine the best batching. The key constraint is: each bee can write ~10-15 spec files in one session without hitting limits. Don't make bees write more than 15 specs each.

## Deliverables

### Task A: Fix dispatcher stale slot detection (sonnet bee)
- File: `hivenode/scheduler/dispatcher_daemon.py`
- Add stale detection (mtime > 30 min = not counted as active)
- Update tests
- Verify all existing dispatcher tests still pass

### Task B-F: Generate remaining 63 MW spec files (split across multiple bees)
- Each bee writes 10-15 spec files to `.deia/hive/queue/backlog/`
- Naming: `SPEC-MW-{ID}-{short-description}.md`
- Real content, not boilerplate
- Read existing 3 specs in backlog/ as format templates
- Read `scheduler_mobile_workdesk.py` TASKS list for task IDs, descriptions, dependencies, and hour estimates
- Read relevant source files to write accurate "Files to Read First" and "Acceptance Criteria" sections
- Model: sonnet (needs to understand codebase to write good specs)

## Constraints
- All tasks: TDD where applicable, no stubs, no file over 500 lines
- Spec files: 50-100 lines each, real content
- Use sonnet for all spec-writing bees (they need codebase understanding)
- Q33N determines exact batching and dispatch order
