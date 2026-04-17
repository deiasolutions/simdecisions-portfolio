# TASK-025B: Fix Cycle Logic

**From:** Q33N
**To:** BEE (Sonnet)
**Date:** 2026-03-12
**Depends On:** TASK-025A (real dispatch integration)

---

## Objective

Implement the fix cycle logic in `run_queue.py` so that when a spec fails (response success=False), the queue runner generates a fix spec and re-queues it as P0 for retry. After max fix cycles (default 2), flag the spec as NEEDS_DAVE and move to `_needs_review/`.

---

## Context

Phase 1 built the queue skeleton. TASK-025A wires real dispatch. Now we need the auto-retry mechanism.

### Current Behavior (after TASK-025A)

When `process_spec()` returns `status="NEEDS_DAVE"`, the main loop in `run_queue()` moves the spec to `_needs_review/` immediately. This happens at line 341-346 in run_queue.py.

### Desired Behavior (this task)

1. Track fix cycle count per spec ID
2. When status != "CLEAN":
   - If fix_cycles < max (default 2): generate fix spec, insert at front of queue, increment counter
   - If fix_cycles >= max: move to `_needs_review/`, log QUEUE_NEEDS_DAVE event
3. Fix spec format: P0 priority, references original spec, includes error details
4. Fix spec naming: `YYYY-MM-DD-HHMM-SPEC-fix-<original-spec-name>.md`

### Fix Cycle Tracking

Use a dict to track: `fix_cycles: dict[str, int]` keyed by original spec ID (the root spec, not fix specs).

When creating a fix spec for `SPEC-foo`, the fix spec ID is `SPEC-fix-foo`. If that fix spec also fails, we still count against `SPEC-foo`'s fix cycle limit.

### Fix Spec Template (from briefing)

```markdown
# SPEC: Fix failures from <original-spec-name>

## Priority
P0

## Objective
Fix the errors reported after processing <original-spec-name>. See error details below.

## Context
Original spec: <path to original spec>
Fix cycle: <N> of <max>

### Error Details
<paste from response file: test failures, stderr, etc.>

## Acceptance Criteria
- [ ] All original acceptance criteria still pass
- [ ] Reported errors are resolved
- [ ] No new test regressions

## Model Assignment
<same model as original spec>

## Constraints
- Do not break existing tests
- Fix the reported errors, do not refactor
```

---

## Files to Read

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\run_queue.py` — modify run_queue() main loop
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\morning_report.py` — QueueEvent dataclass
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\config\queue.yml` — config["budget"]["max_fix_cycles_per_spec"]
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\specs\SPEC-BUILD-QUEUE-001.md` — sections 7, 8 for fix cycle rules

---

## Deliverables

### 1. generate_fix_spec() Function

Add to run_queue.py (or new module if over 500 lines):

```python
def generate_fix_spec(
    original_spec: SpecFile,
    error_details: str,
    fix_cycle: int,
    max_cycles: int,
    queue_dir: Path
) -> Path:
    """Generate a fix spec and write it to the queue directory.

    Args:
        original_spec: The spec that failed
        error_details: Error message from the response file or subprocess
        fix_cycle: Current fix cycle number (1-based)
        max_cycles: Max fix cycles allowed (from config)
        queue_dir: Path to queue directory

    Returns:
        Path to the generated fix spec file
    """
```

**Implementation:**

1. Extract original spec ID (strip "fix-" prefix if present to find root spec)
2. Format timestamp: `datetime.now().strftime("%Y-%m-%d-%H%M")`
3. Create fix spec filename: `{timestamp}-SPEC-fix-{original_id}.md`
4. Build fix spec content from template (see above)
5. Write to queue_dir
6. Return Path to fix spec

### 2. Modify run_queue() Main Loop

Current code (lines 296-347):

```python
for spec in specs:
    # Check budget...
    # Process spec
    result = process_spec(spec, config, session_events, repo_root)
    session_cost += result.cost_usd

    # Move spec based on result
    if result.status == "CLEAN":
        # Move to _done/
    elif result.status == "NEEDS_DAVE":
        # Move to _needs_review/
```

**New logic:**

**IMPORTANT:** Do NOT use `for spec in specs:` with `specs.insert()` — mutating a list during `for` iteration is unsafe in Python (shifts indices, skips items). Use a `while` loop with an explicit index instead:

```python
# At start of run_queue():
fix_cycles: dict[str, int] = {}  # Track fix cycles per root spec ID
spec_index = 0

while spec_index < len(specs):
    spec = specs[spec_index]
    # Check budget (unchanged)...

    # Process spec
    result = process_spec(spec, config, session_events, repo_root)
    session_cost += result.cost_usd

    # Determine root spec ID (strip "fix-" prefix)
    root_spec_id = _get_root_spec_id(spec.path.stem)

    # Move/retry based on result
    if result.status == "CLEAN":
        # Move to _done/ (unchanged)
        done_dir = queue_dir / "_done"
        done_dir.mkdir(exist_ok=True)
        dest = done_dir / spec.path.name
        spec.path.rename(dest)
        print(f"[QUEUE] ✅ CLEAN: {spec.path.name} → _done/")

    else:  # NEEDS_DAVE or other failure
        current_cycle = fix_cycles.get(root_spec_id, 0)
        max_cycles = config["budget"]["max_fix_cycles_per_spec"]

        if current_cycle < max_cycles:
            # Generate fix spec
            fix_spec_path = generate_fix_spec(
                spec,
                result.error_msg or "Unknown error",
                current_cycle + 1,
                max_cycles,
                queue_dir
            )

            # Increment fix cycle counter
            fix_cycles[root_spec_id] = current_cycle + 1

            # Log QUEUE_FIX_CYCLE event
            session_events.append(QueueEvent(
                event_type="QUEUE_FIX_CYCLE",
                timestamp=datetime.now().isoformat(),
                spec_id=spec.path.stem,
                cost_usd=result.cost_usd,
                duration_ms=result.duration_ms,
                model_used=spec.model,
                details={
                    "fix_cycle": current_cycle + 1,
                    "max_cycles": max_cycles,
                    "fix_spec": fix_spec_path.name
                }
            ))

            # Move original spec to _done (processed, even if failed)
            done_dir = queue_dir / "_done"
            done_dir.mkdir(exist_ok=True)
            dest = done_dir / spec.path.name
            spec.path.rename(dest)

            # Load the fix spec and insert right after current position (processes next)
            fix_spec = parse_spec(fix_spec_path)
            specs.insert(spec_index + 1, fix_spec)

            print(f"[QUEUE] 🔄 FIX_CYCLE {current_cycle + 1}/{max_cycles}: {spec.path.name} → fix spec generated")

        else:
            # Max cycles reached, flag for Dave
            needs_review_dir = queue_dir / "_needs_review"
            needs_review_dir.mkdir(exist_ok=True)
            dest = needs_review_dir / spec.path.name
            spec.path.rename(dest)

            # Log QUEUE_NEEDS_DAVE event
            session_events.append(QueueEvent(
                event_type="QUEUE_NEEDS_DAVE",
                timestamp=datetime.now().isoformat(),
                spec_id=spec.path.stem,
                cost_usd=result.cost_usd,
                duration_ms=result.duration_ms,
                model_used=spec.model,
                details={
                    "issue": result.error_msg or "Unknown error",
                    "fix_attempts": current_cycle
                }
            ))

            print(f"[QUEUE] ⚠️ NEEDS_DAVE: {spec.path.name} → _needs_review/ (max fix cycles reached)")

    spec_index += 1
```

### 3. Helper Function: _get_root_spec_id()

Extract root spec ID from spec filename:

```python
def _get_root_spec_id(spec_filename: str) -> str:
    """Extract root spec ID from a spec filename.

    For fix specs like "2026-03-12-1234-SPEC-fix-foo", returns "foo".
    For original specs like "2026-03-12-1234-SPEC-foo", returns "foo".

    Args:
        spec_filename: Spec file stem (no extension)

    Returns:
        Root spec ID (without date, time, "SPEC-" prefix, or "fix-" prefix)
    """
    # Strip date prefix (YYYY-MM-DD-HHMM-)
    parts = spec_filename.split('-')

    # Find "SPEC" marker
    if "SPEC" in parts:
        spec_index = parts.index("SPEC")
        remaining = parts[spec_index + 1:]

        # If starts with "fix", strip it
        if remaining and remaining[0] == "fix":
            remaining = remaining[1:]

        return "-".join(remaining)

    # Fallback: return as-is
    return spec_filename
```

---

## Test Requirements

Write tests in `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\tests\test_fix_cycle.py`

### Test Cases (minimum 8)

1. **test_generate_fix_spec_creates_valid_markdown** — verify output format matches template
2. **test_generate_fix_spec_has_p0_priority** — verify priority in output
3. **test_generate_fix_spec_references_original_spec** — verify original spec path included
4. **test_generate_fix_spec_includes_error_details** — verify error_details in output
5. **test_fix_cycle_count_tracked_correctly** — first failure → fix_cycles["foo"] = 1
6. **test_fix_spec_inserted_at_front_of_queue** — verify fix spec processes next
7. **test_max_cycles_moves_to_needs_review** — 2 failures → _needs_review/
8. **test_queue_fix_cycle_event_logged** — verify QUEUE_FIX_CYCLE event appended
9. **test_queue_needs_dave_event_logged** — verify QUEUE_NEEDS_DAVE event after max cycles
10. **test_get_root_spec_id_strips_fix_prefix** — "SPEC-fix-foo" → "foo"
11. **test_get_root_spec_id_handles_original_spec** — "SPEC-foo" → "foo"

### Mocking Strategy

Use `unittest.mock.patch` to:
- Mock `process_spec()` to return SpecResult with status="NEEDS_DAVE"
- Mock file system operations (mkdir, rename) with temporary directories
- Use real `parse_spec()` on generated fix spec to verify format

Example:

```python
import tempfile
from pathlib import Path
from unittest.mock import patch

def test_generate_fix_spec_creates_valid_markdown():
    # Setup
    with tempfile.TemporaryDirectory() as tmpdir:
        queue_dir = Path(tmpdir)

        original_spec = SpecFile(
            path=Path("/fake/SPEC-foo.md"),
            priority="P1",
            objective="Test objective",
            acceptance_criteria=["Criterion 1"],
            model="haiku",
            smoke_test=[],
            constraints=[]
        )

        # Execute
        fix_path = generate_fix_spec(
            original_spec,
            "Error: test failed",
            1,
            2,
            queue_dir
        )

        # Assert
        assert fix_path.exists()
        content = fix_path.read_text()
        assert "# SPEC: Fix failures from foo" in content
        assert "## Priority\nP0" in content
        assert "Error: test failed" in content
```

---

## Constraints

- **No changes to morning_report.py** — use existing QueueEvent dataclass
- **No changes to queue.yml** — read config only
- **Keep run_queue.py under 500 lines** — if adding fix cycle logic pushes over, extract to `fix_cycle.py` module
- **No stubs** — every function fully implemented
- **All tests use mocks or temp files** — no real dispatch during testing

---

## Model Assignment

**Sonnet** — control flow logic, state tracking, markdown generation require precision

---

## Acceptance Criteria

- [ ] generate_fix_spec() creates markdown matching the template format
- [ ] generate_fix_spec() writes file to queue directory with correct naming
- [ ] Fix spec has P0 priority
- [ ] Fix spec references original spec path
- [ ] Fix spec includes error details from response
- [ ] Fix cycle count tracked in dict keyed by root spec ID
- [ ] First failure generates fix spec, increments counter to 1
- [ ] Second failure generates fix spec, increments counter to 2
- [ ] Third failure (counter >= max) moves to _needs_review/, no fix spec generated
- [ ] QUEUE_FIX_CYCLE event logged when fix spec created
- [ ] QUEUE_NEEDS_DAVE event logged when max cycles reached
- [ ] Fix spec inserted at front of remaining queue (processes next)
- [ ] _get_root_spec_id() correctly strips "fix-" prefix
- [ ] All 11 test cases pass
- [ ] run_queue.py total line count ≤ 500 (modularize if needed)
- [ ] No stubs or TODOs in implementation

---

## Response File — MANDATORY

When done, write: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260312-TASK-025B-RESPONSE.md`

Must include all 8 sections:
1. **Status:** COMPLETE | FAILED (reason)
2. **Files Modified** (absolute paths)
3. **What Was Done** (bullet list of concrete changes)
4. **Tests Added/Modified** (file paths + counts)
5. **Test Results** (pass count, any failures)
6. **Clock** (start time, end time, duration)
7. **Cost** (model, turns, estimated USD)
8. **Next Steps** (if any blockers or follow-up needed)

---

**End of TASK-025B**
