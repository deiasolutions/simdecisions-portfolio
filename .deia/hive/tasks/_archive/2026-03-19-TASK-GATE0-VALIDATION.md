# TASK-GATE0-VALIDATION: Implement Gate 0 Programmatic Validation for Queue Runner

## Objective

Implement **Gate 0 validation** from PROCESS-0013 as a programmatic validation step in the queue runner that runs BEFORE dispatch to catch incoherent specs (contradictory deliverables vs acceptance criteria, missing priorities, missing acceptance criteria, non-existent file paths, scope violations).

This is **pure Python validation** — no LLM calls, no network, no subprocess. Must run in < 1 second.

## Context

The queue runner currently dispatches specs directly to regent bot with zero validation. This allows incoherent specs (contradictory deliverables vs acceptance criteria) to reach bees and waste cycles.

Gate 0 is the first validation layer (disambiguation) from PROCESS-0013. It runs AFTER spec load, BEFORE `handler.call_dispatch()` in `spec_processor.py::process_spec()` at line 125.

Gate 0 catches:
1. Missing priority (P0/P1/P2/P3)
2. Missing acceptance criteria
3. Non-existent file paths in "Files to Read First" or "Files to Modify"
4. Contradictory deliverables vs acceptance criteria (e.g., spec says "fix X" in acceptance criteria but deliverables say "DO NOT modify X")
5. Scope violations (e.g., spec identifies bug location in source file but forbids editing that file)

If Gate 0 fails:
- Return `SpecResult(status="GATE0_FAIL", ...)`
- Do NOT dispatch
- `run_queue.py` moves spec to `_needs_review/`

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\processes\PROCESS-0013-BUILD-INTEGRITY-3PHASE.md` (lines 38-208) — Gate 0 requirements
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\spec_processor.py` (lines 85-321) — integration point
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\spec_parser.py` (lines 14-27) — SpecFile dataclass
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\run_queue.py` (lines 215-295) — status handling function `_handle_spec_result`

## Deliverables

### 1. New Module: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\gate0.py`

**Maximum 500 lines.**

Must define:

```python
from dataclasses import dataclass
from pathlib import Path
from .spec_parser import SpecFile

@dataclass
class CheckResult:
    """Result of a single validation check."""
    name: str           # e.g., "Priority Check"
    passed: bool
    message: str        # Details (success message or failure reason)

@dataclass
class Gate0Result:
    """Result of complete Gate 0 validation."""
    passed: bool
    checks: list[CheckResult]
    summary: str        # Human-readable summary for logs

def validate_spec(spec: SpecFile, repo_root: Path) -> Gate0Result:
    """Run all Gate 0 checks on a spec.

    Args:
        spec: The spec to validate
        repo_root: Repository root directory for file path resolution

    Returns:
        Gate0Result with validation outcome
    """
    pass

def check_priority(spec: SpecFile) -> CheckResult:
    """Check if spec has a valid priority (P0/P1/P2/P3)."""
    pass

def check_acceptance_criteria(spec: SpecFile) -> CheckResult:
    """Check if spec has at least one acceptance criterion."""
    pass

def check_file_paths_exist(spec: SpecFile, repo_root: Path) -> CheckResult:
    """Check that all referenced files exist on disk.

    Parses spec content for:
    - "Files to Read First" section
    - "Files to Modify" section

    Validates each path exists relative to repo_root.
    """
    pass

def check_deliverables_coherence(spec: SpecFile) -> CheckResult:
    """Check that deliverables don't contradict acceptance criteria.

    Example violations:
    - Acceptance: "Fix bug in foo.ts"
    - Deliverables: "DO NOT modify foo.ts"

    Uses heuristic keyword matching:
    - Extract file names from acceptance criteria
    - Check if deliverables forbid modifying those files
    """
    pass

def check_scope_sanity(spec: SpecFile) -> CheckResult:
    """Check that scope is coherent.

    Example violation:
    - Spec identifies bug location: "The error is in bar.ts line 45"
    - But forbids editing: "DO NOT modify bar.ts"

    Uses heuristic keyword matching:
    - Extract file references from objective/context
    - Check if constraints/deliverables forbid editing
    """
    pass
```

**Implementation Notes:**
- Use simple heuristics (regex, string matching) — NO LLM calls
- File path parsing: look for markdown sections "Files to Read First" and "Files to Modify"
- Extract file paths from bullet lists under those sections
- Coherence checks: keyword-based (look for "DO NOT", "forbidden", "out of scope" near file names)
- Keep it FAST — target < 1 second for typical spec

### 2. Integration: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\spec_processor.py`

At line 125 (BEFORE `handler.call_dispatch()` call), insert:

```python
# Run Gate 0 validation
from .gate0 import validate_spec

gate0_result = validate_spec(spec, repo_root)
if not gate0_result.passed:
    print(f"[QUEUE] GATE0 FAIL: {spec_id}", flush=True)
    print(f"[QUEUE] {gate0_result.summary}", flush=True)
    return SpecResult(
        spec_id=spec_id,
        status="GATE0_FAIL",
        cost_usd=0.0,
        duration_ms=0,
        error_msg=gate0_result.summary
    )
```

**Constraints:**
- Add import at top of file
- Preserve all existing code
- Do NOT modify dispatch logic — only add validation before it

### 3. Status Handling: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\run_queue.py`

In `_handle_spec_result` function (around line 264), add handling for `GATE0_FAIL` status:

```python
if result.status == "GATE0_FAIL":
    # Gate 0 validation failed — move to _needs_review
    needs_review_dir = queue_dir / "_needs_review"
    needs_review_dir.mkdir(exist_ok=True)
    dest = needs_review_dir / spec.path.name

    if not _safe_move_spec(spec.path, dest):
        print(
            f"[QUEUE] ERROR: Failed to move {spec.path.name} to _needs_review/",
            flush=True,
        )
    else:
        print(
            f"[QUEUE] GATE0_FAIL: {spec.path.name} -> _needs_review/\n"
            f"[QUEUE] Reason: {result.error_msg}",
            flush=True,
        )

    return []  # No fix specs generated
```

**Placement:** Add this block BEFORE the `if result.status == "CLEAN":` check (around line 264).

### 4. Test File: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\queue\test_gate0.py`

**Minimum 12 tests, all must pass.**

Test structure:

```python
import pytest
from pathlib import Path
from datetime import datetime
from .deia.hive.scripts.queue.gate0 import (
    validate_spec,
    check_priority,
    check_acceptance_criteria,
    check_file_paths_exist,
    check_deliverables_coherence,
    check_scope_sanity,
    CheckResult,
    Gate0Result,
)
from .deia.hive.scripts.queue.spec_parser import SpecFile


class TestGate0Validation:
    """Test Gate 0 validation checks."""

    def test_check_priority_valid(self):
        """Valid priority passes."""
        pass

    def test_check_priority_missing(self):
        """Missing priority fails."""
        pass

    def test_check_acceptance_criteria_present(self):
        """Spec with acceptance criteria passes."""
        pass

    def test_check_acceptance_criteria_missing(self):
        """Spec without acceptance criteria fails."""
        pass

    def test_check_file_paths_all_exist(self, tmp_path):
        """All referenced files exist — passes."""
        pass

    def test_check_file_paths_missing(self, tmp_path):
        """Referenced file missing — fails."""
        pass

    def test_check_deliverables_coherence_pass(self):
        """Coherent deliverables vs acceptance criteria — passes."""
        pass

    def test_check_deliverables_coherence_fail(self):
        """Contradictory deliverables vs acceptance criteria — fails."""
        pass

    def test_check_scope_sanity_pass(self):
        """Coherent scope — passes."""
        pass

    def test_check_scope_sanity_fail(self):
        """Scope violation (identifies bug but forbids fix) — fails."""
        pass

    def test_validate_spec_all_pass(self, tmp_path):
        """Valid spec passes all checks."""
        pass

    def test_validate_spec_multiple_failures(self, tmp_path):
        """Invalid spec fails multiple checks."""
        pass
```

**Test Requirements:**
- Use pytest fixtures for `tmp_path` (temporary directory)
- Create minimal SpecFile objects for testing
- Create temporary files in `tmp_path` for file existence tests
- Use realistic spec content fragments for coherence tests
- All tests must pass — no skips, no xfail

### 5. Test Fixtures: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\queue\fixtures\`

Create 6 fixture spec files (plain text, not Python):

**`valid-spec.md`** — Passes all checks:
```markdown
# TASK-XXX: Valid Spec

Priority: P1

## Objective
Fix the login bug.

## Files to Read First
- C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\auth\login.ts

## Acceptance Criteria
- [ ] Login form submits correctly
- [ ] Tests pass

## Deliverables
- [ ] Fix login.ts
- [ ] Add tests
```

**`missing-priority-spec.md`** — No priority section:
```markdown
# TASK-XXX: Missing Priority

## Objective
Fix something.

## Acceptance Criteria
- [ ] It works
```

**`missing-criteria-spec.md`** — No acceptance criteria:
```markdown
# TASK-XXX: Missing Criteria

Priority: P1

## Objective
Fix something.
```

**`missing-files-spec.md`** — References non-existent files:
```markdown
# TASK-XXX: Missing Files

Priority: P1

## Files to Read First
- C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\DOES_NOT_EXIST.ts

## Acceptance Criteria
- [ ] It works
```

**`incoherent-spec.md`** — Contradictory deliverables vs acceptance criteria:
```markdown
# TASK-XXX: Incoherent Spec

Priority: P1

## Acceptance Criteria
- [ ] Fix bug in foo.ts

## Deliverables
- [ ] DO NOT modify foo.ts
```

**`scope-violation-spec.md`** — Identifies bug but forbids fix:
```markdown
# TASK-XXX: Scope Violation

Priority: P1

## Objective
The bug is in bar.ts line 45.

## Acceptance Criteria
- [ ] Bug fixed

## Constraints
- DO NOT modify bar.ts
```

## Test Requirements

- [ ] **Tests written FIRST (TDD)** — Write all 12+ tests before implementing functions
- [ ] All tests pass: `cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter && python -m pytest tests/queue/test_gate0.py -v`
- [ ] Edge cases covered:
  - Empty spec content
  - Malformed priority strings (e.g., "Priority: HIGH" instead of "P1")
  - Relative vs absolute file paths
  - Case sensitivity in keyword matching
  - Multiple file references in same spec
- [ ] No test skips or xfail markers

## Constraints

- **No file over 500 lines** (gate0.py must be < 500 lines)
- **TDD** — Tests written FIRST
- **NO STUBS** — Every function fully implemented, no `# TODO` comments
- **NO LLM CALLS** — Pure Python heuristics only
- **FAST** — Gate 0 must run in < 1 second
- **NO NETWORK** — No HTTP requests, no subprocess calls
- **Python 3.10+** — Use modern Python features (dataclasses, Path, type hints)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260319-GATE0-QUEUE-RUNNER-VALIDATION-SONNET-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full absolute paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.

## Acceptance Criteria

- [ ] New file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\gate0.py` with all required functions
- [ ] Integration in `spec_processor.py` at line 125 (before dispatch call)
- [ ] New status `GATE0_FAIL` handled in `run_queue.py::_handle_spec_result`
- [ ] Test file `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\queue\test_gate0.py` with minimum 12 tests
- [ ] All tests pass (100% pass rate)
- [ ] Gate 0 rejects incoherent specs (contradictory deliverables vs acceptance criteria)
- [ ] Gate 0 rejects specs with missing file paths
- [ ] Gate 0 rejects specs with no acceptance criteria
- [ ] Gate 0 rejects specs with no priority
- [ ] Gate 0 passes valid, coherent specs
- [ ] Gate 0 runs in < 1 second (no subprocess, no network, no LLM)
- [ ] Fixture specs in `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\queue\fixtures\` for test cases (6 files)
- [ ] No stubs, no TODOs, no placeholder implementations
- [ ] gate0.py file is under 500 lines

## Expected Behavior

### Valid Spec Flow
```
1. Queue runner loads spec from .deia/hive/queue/
2. spec_processor.py calls validate_spec(spec, repo_root)
3. Gate 0 runs 5 checks (priority, criteria, files, coherence, scope)
4. All checks pass → Gate0Result(passed=True)
5. Dispatch proceeds normally
6. Bee processes spec
7. Spec moves to _done/
```

### Invalid Spec Flow
```
1. Queue runner loads spec from .deia/hive/queue/
2. spec_processor.py calls validate_spec(spec, repo_root)
3. Gate 0 runs 5 checks
4. One or more checks fail → Gate0Result(passed=False, summary="...")
5. spec_processor.py returns SpecResult(status="GATE0_FAIL", error_msg=summary)
6. run_queue.py calls _handle_spec_result
7. Status is "GATE0_FAIL" → spec moves to _needs_review/
8. Queue runner logs failure reason
9. Human reviews spec, fixes issues, moves back to queue/
```

## Performance Requirements

- `validate_spec()` must complete in < 1 second for typical specs (50-200 lines)
- No subprocess calls (no dispatch.py, no Claude Code, no git)
- No network requests (no HTTP, no LLM APIs)
- Pure Python heuristics only

## Implementation Hints

### Priority Check
Look for lines matching: `Priority: P[0-3]` or `priority: P[0-3]` (case insensitive)

### Acceptance Criteria Check
Look for markdown section: `## Acceptance Criteria` followed by checkbox list items `- [ ]`

### File Paths Check
1. Find sections: `## Files to Read First` and `## Files to Modify`
2. Extract bullet list items under those sections
3. Parse paths (handle Windows/Unix separators)
4. Resolve relative to repo_root
5. Check `Path(file).exists()`

### Coherence Check
1. Extract file names from acceptance criteria (e.g., "foo.ts" from "Fix bug in foo.ts")
2. Look for negative keywords in deliverables: "DO NOT", "forbidden", "out of scope"
3. Check if negative keywords appear near file names
4. Fail if contradiction detected

### Scope Sanity Check
1. Extract file names from objective/context sections
2. Check if constraints/deliverables forbid editing those files
3. Fail if scope violation detected

## Build Commands

```bash
# Run Gate 0 tests
cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter
python -m pytest tests/queue/test_gate0.py -v

# Run all queue tests
python -m pytest tests/queue/ -v
```

## Success Metrics

- 12+ tests written
- 100% test pass rate
- Gate 0 validation runs in < 1 second
- Invalid specs caught before dispatch (0 wasted bee cycles on incoherent specs)
- Valid specs pass through unchanged
- No false positives (valid specs rejected)
- No false negatives (invalid specs accepted)

## Notes

- Gate 0 is NOT an LLM-based validation — it's a fast heuristic check
- False positives are acceptable (human reviews _needs_review/)
- False negatives are NOT acceptable (invalid specs must be caught)
- Err on the side of strictness — better to over-reject than under-reject
- This is Phase 0 of PROCESS-0013 — Phases 1 & 2 (fidelity checks) come later

---

**Assigned Model:** Sonnet
**Complexity:** Medium (integration + validation logic + comprehensive tests)
**Estimated Duration:** 45-60 minutes
