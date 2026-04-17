# BUG: Fix cycle specs reference _active/ path that no longer exists

## Objective
Fix the queue runner so fix cycle specs reference the spec's _done/ path (where it ends up) instead of _active/ path (where it was during dispatch).

## Root Cause
`fix_cycle.py` line 89 writes `f"Original spec: {original_spec.path}"` into the fix spec. Since the _active/ directory change, `spec.path` points to `_active/foo.md`. But by the time the fix spec is processed, the original has been moved to `_done/` or `_needs_review/`. So the fix spec references a file that doesn't exist.

## The Fix
Two options (pick the simpler one):

### Option A: Fix in fix_cycle.py (preferred)
Line 89 in `fix_cycle.py` — instead of using `original_spec.path`, compute the `_done/` path:

```python
# Line 89 — change from:
f"Original spec: {original_spec.path}",

# To:
f"Original spec: {original_spec.path.parent.parent / '_done' / original_spec.path.name}",
```

### Option B: Fix in run_queue.py
Before calling `generate_fix_spec()`, update `spec.path` to point to where it was moved (the `_done/` destination).

## Files to Modify
- `.deia/hive/scripts/queue/fix_cycle.py` — line 89 (and line ~155 in generate_q33n_fix_spec if same pattern)

## Files to Read First
- `.deia/hive/scripts/queue/fix_cycle.py` (the two generate functions)
- `.deia/hive/scripts/queue/run_queue.py` (where generate_fix_spec is called — search for "generate_fix_spec")

## Acceptance Criteria
- [ ] Fix specs reference _done/ path, not _active/ path
- [ ] Fix cycle still works end-to-end (fix spec can find the original)
- [ ] No regressions in queue runner tests

## Smoke Test
- [ ] `python -m pytest tests/ -k "fix_cycle" -v`
- [ ] `python -m pytest .deia/hive/scripts/queue/tests/ -v`

## Constraints
- Minimal change — just fix the path reference
- Do NOT refactor fix_cycle.py or run_queue.py beyond this fix

## Model Assignment
sonnet

## Priority
P0
