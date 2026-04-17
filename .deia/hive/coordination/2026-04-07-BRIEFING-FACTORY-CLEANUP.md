# BRIEFING: FACTORY Pipeline — Cleanup & Integration Finish

## Objective

The FACTORY pipeline built 8 modules (173 tests) implementing PRISM-IR v1.1. The modules exist and have tests, but there are loose ends: unwired integrations, a known scheduler bug, and tests that may not all run cleanly from a single pytest invocation. Your job is to tie everything together — zero failing tests, no orphan code, all modules properly importable, and the 4 unwired modules connected to the pipeline.

## Scope

### 1. Fix the Scheduler done_ids Bug

**File:** `hivenode/scheduler/scheduler_daemon.py`, line ~630

**Bug:** `done_ids = {t.id for t in self.tasks if t.id in done_specs}` only includes tasks that are in BOTH `self.tasks` AND `_done/`. If a spec was never in the workdesk task list (i.e., it came purely from backlog), it won't appear in `done_ids` even when it's in `_done/`.

**Fix:** Change to `done_ids = done_specs` — the `_done/` directory is ground truth. The set `done_specs` is already built correctly from scanning `_done/` at lines 591-596.

**Test:** Write a test that verifies: when FACTORY-001 is in `_done/` and FACTORY-002 depends on it, FACTORY-002 gets `status: "ready"` even if FACTORY-001 was never in the workdesk task list.

### 2. Wire dependency_resolver.py into the Scheduler

**Module:** `.deia/hive/scripts/queue/dependency_resolver.py`

The scheduler currently has inline dependency checking at line ~635. Replace that inline check with a call to `dependency_resolver.check_dependencies()`. This gives us circular dependency detection for free.

**Integration point:** `compute_schedule()` in `scheduler_daemon.py` — where it determines `deps_met` for each task.

**Also:** Add a circular dependency check during `scan_backlog()` — if circular deps are detected, log a warning and mark affected specs as `status: "error"`.

### 3. Wire acceptance_criteria.py into spec_processor.py

**Module:** `.deia/hive/scripts/queue/acceptance_criteria.py`

Currently bees finish and specs go straight to `_done/`. The acceptance criteria module should run AFTER the bee completes but BEFORE the spec moves to `_done/`.

**Integration point:** In `spec_processor.py` (or wherever the queue runner handles bee completion), after the bee's response is received:
1. Read the spec's `content_type` field
2. Call `evaluate_acceptance(spec, output_path)`
3. If all checks pass → move to `_done/`
4. If any check fails → move to `_needs_review/` with failure details logged
5. If `content_type` is null/missing → skip acceptance (backward compat)

**Important:** Checks marked as "skipped" (like `renders_without_crash`) should NOT cause failure. Only checks that actively fail should block.

### 4. Wire bundle_formation.py into the Dispatcher

**Module:** `hivenode/scheduler/bundle_formation.py`

This is lower priority than 1-3. If time permits, wire it into the dispatcher daemon so that when multiple specs are ready simultaneously, they can be bundled for cost optimization.

**Integration point:** In `dispatcher_daemon.py`'s `_dispatch_cycle()`, after filtering to `ready_tasks`:
1. Load model capabilities for the target model
2. Call `form_bundles(ready_specs, operator, token_buffer_ratio)`
3. Dispatch bundles instead of individual specs

**If this is too complex for this cleanup pass:** Skip it. Document what's needed in a follow-up spec and move on. The pipeline works without bundling.

### 5. Wire dag_traversal.py into spec_parser

**Module:** `.deia/hive/scripts/queue/dag_traversal.py`

Same as bundling — lower priority. If SHARED_REF nodes aren't being used yet, this can wait. But if there's a clean integration point (e.g., `load_queue()` could call `resolve_shared_refs()` after loading), wire it in.

**If too complex:** Skip. Document and move on.

### 6. Run ALL Tests — Fix Any Failures

Run the full test suite for all FACTORY modules:
```bash
python -m pytest tests/hive/ tests/hivenode/ -v --tb=short 2>&1
```

Fix any:
- Import errors (modules in wrong paths, missing `__init__.py`)
- Test files that can't find their modules
- Tests that pass individually but fail when run together (state leaks)
- Stale test fixtures referencing old interfaces

The goal is: `pytest tests/hive/ tests/hivenode/ -v` runs clean with 0 failures.

### 7. Verify All Module Imports Work

From the repo root, verify each module is importable:
```python
from spec_parser import parse_spec, SpecFile
from dependency_resolver import check_dependencies, detect_circular_dependencies
from acceptance_criteria import evaluate_acceptance
from telemetry_logger import log_build_attempt
from policy_recommender import generate_policy_recommendations
from dag_traversal import topological_sort_specs, check_circular_dependencies
```

And from hivenode:
```python
from hivenode.scheduler.ttl_enforcement import scan_and_handle_stale_specs
from hivenode.scheduler.bundle_formation import form_bundles
from hivenode.scheduler.model_capabilities import load_model_capabilities
from hivenode.scheduler.integrity_check import find_orphaned_nodes
```

Fix any import issues.

## Files to Read First

- `hivenode/scheduler/scheduler_daemon.py` — lines 560-640 (compute_schedule, done_ids bug)
- `.deia/hive/scripts/queue/spec_processor.py` — bee completion handling
- `.deia/hive/scripts/queue/run_queue.py` — queue runner flow
- `hivenode/scheduler/dispatcher_daemon.py` — dispatch cycle
- `.deia/hive/scripts/queue/dependency_resolver.py` — the module to wire in
- `.deia/hive/scripts/queue/acceptance_criteria.py` — the module to wire in

## Priority Order

1. Fix done_ids bug (blocker — scheduler doesn't work correctly without this)
2. Run all tests, fix failures (hygiene)
3. Wire dependency_resolver (replaces buggy inline code)
4. Wire acceptance_criteria (enables quality gates)
5. Wire bundle_formation (nice to have — skip if complex)
6. Wire dag_traversal (nice to have — skip if complex)
7. Final test run — zero failures

## Constraints

- No file over 500 lines (split if needed)
- TDD: write/update tests for any integration changes
- Do NOT break existing tests — run the full suite before AND after changes
- Do NOT modify the dispatcher's dep gate safety net (the `_verify_deps_satisfied` method)
- Backward compatible: specs without `content_type` should still work (skip acceptance)
- If items 4-5 are too complex, write a follow-up spec to `.deia/hive/queue/backlog/` and move on

## Response Requirements

Write your response to `.deia/hive/responses/20260407-FACTORY-CLEANUP-RESPONSE.md` with:
- What was fixed/wired
- What was skipped and why
- Full test results (command + output summary)
- Any new specs written for deferred work
