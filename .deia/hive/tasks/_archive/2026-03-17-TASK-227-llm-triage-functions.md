# TASK-227: LLM Triage Functions — 3 Integration Points (W3-B)

**Objective:** Implement three LLM triage functions that add intelligence to the directory state machine: crash recovery triage, failure diagnosis, and completion validation.

**Model:** Sonnet
**Priority:** P1
**Estimated Size:** ~100 lines code + ~80 lines tests
**Cost:** ~$0.50 (Sonnet for implementation, Haiku for testing)

---

## Context

This task is part of **SPEC-PIPELINE-001** (Unified Build Pipeline), Section 5 — LLM Triage Layer.

These functions use cheap Haiku calls (~$0.01-0.03 per call) to make smart routing decisions instead of blind retries. They integrate into the queue runner's state machine at three critical decision points:

1. **Crash recovery** — when runner finds orphaned work in `_active/` on startup
2. **Failure diagnosis** — when a bee returns error/timeout
3. **Completion validation** — before moving spec to `_done/` (advisory only in Phase 1)

**The holdout principle is critical:** The reviewing LLM must NEVER be the same model/session that did the work.

---

## Dependencies

**TASK-224** (directory state machine) — COMPLETE (in `_done/`)
- The state machine transitions exist in `run_queue.py`
- Orphan scan logic exists
- `_active/`, `_done/`, `_failed/`, `_needs_review/` directories in use

**Dependency Status:** ✅ SATISFIED

---

## Files to Read First

Read these files before writing any code:

1. **`C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\specs\SPEC-PIPELINE-001-UNIFIED-BUILD-PIPELINE.md`**
   - Lines 272-318 (Section 5: LLM Triage Layer)
   - Describes the three triage points, inputs, outputs, verdicts, routing logic

2. **`C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\run_queue.py`**
   - Lines 1-250 minimum
   - Understand where triage will be called (orphan scan, failure handling, completion)

3. **`C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\dispatch_handler.py`**
   - Lines 1-200 minimum
   - Bee dispatch/completion handling, where results come back

4. **`C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\filesystem_store.py`**
   - Full file (303 lines)
   - Understand the PipelineStore interface (already implemented per TASK-222)

5. **`C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\ledger_events.py`**
   - Full file (196 lines)
   - Understand how to emit events (already implemented per TASK-223)

6. **`C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\adapters\anthropic.py`**
   - Lines 1-79 (full file)
   - Pattern for calling Anthropic API with token tracking

7. **`C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\llm\proxy.py`**
   - Lines 1-100
   - Pattern for async Anthropic API calls

---

## Deliverables

### 1. Create `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\triage.py`

Implement three triage functions with these exact signatures:

```python
from dataclasses import dataclass
from enum import Enum
from typing import Optional

# Verdict types
class CrashVerdict(str, Enum):
    """Verdict for crash recovery triage."""
    COMPLETE_ENOUGH = "complete_enough"  # Commit diff, move to _done/
    PARTIAL_SAFE = "partial_safe"        # Keep diff, generate continuation spec
    REVERT = "revert"                    # Discard changes, retry from scratch

class FailureClassification(str, Enum):
    """Classification for failure diagnosis."""
    AMBIGUOUS_SPEC = "ambiguous_spec"         # Spec unclear → _needs_review/
    CODING_ERROR = "coding_error"             # Bug in bee's code → generate fix spec
    DEPENDENCY_ISSUE = "dependency_issue"     # Upstream broken → block until fixed
    ENVIRONMENT_ISSUE = "environment_issue"   # Setup/config → _needs_review/

@dataclass
class CompletionReview:
    """Review result for completion validation."""
    passed: bool
    confidence: float  # 0.0-1.0
    missing_criteria: list[str]
    suspicious_changes: list[str]
    recommendation: str  # "ACCEPT" | "REVIEW" | "REJECT"

# Triage functions
def triage_crash_recovery(
    spec_content: str,
    git_diff: str,
    test_output: Optional[str],
    started_at: str,
) -> tuple[CrashVerdict, str, dict]:
    """Triage a crashed bee session.

    Args:
        spec_content: Full spec markdown
        git_diff: Output of `git diff HEAD` since session started
        test_output: Pytest output if available (may be None)
        started_at: ISO datetime when session started

    Returns:
        Tuple of (verdict, reasoning, metadata)
        - verdict: CrashVerdict enum
        - reasoning: Plain English explanation
        - metadata: Dict with tokens_in, tokens_out, cost_usd, model
    """

def triage_failure(
    spec_content: str,
    response_file: Optional[str],
    error_output: str,
    test_results: Optional[str],
) -> tuple[FailureClassification, str, dict]:
    """Diagnose why a bee failed.

    Args:
        spec_content: Full spec markdown
        response_file: Path to bee's response file (may not exist)
        error_output: Error messages from bee or dispatch
        test_results: Test output if available

    Returns:
        Tuple of (classification, reasoning, metadata)
        - classification: FailureClassification enum
        - reasoning: Plain English explanation
        - metadata: Dict with tokens_in, tokens_out, cost_usd, model
    """

def validate_completion(
    spec_content: str,
    git_diff: str,
    test_results: str,
    acceptance_criteria: list[str],
) -> tuple[CompletionReview, dict]:
    """Validate that bee completed all acceptance criteria.

    Args:
        spec_content: Full spec markdown
        git_diff: Output of `git diff HEAD` for committed changes
        test_results: Pytest output showing new tests
        acceptance_criteria: Extracted from spec's ## Acceptance Criteria section

    Returns:
        Tuple of (review, metadata)
        - review: CompletionReview dataclass
        - metadata: Dict with tokens_in, tokens_out, cost_usd, model

    Note:
        Phase 1: Advisory only. Always returns passed=True, but logs concerns.
        Phase 2 (future): Will gate on review.passed.
    """
```

**Implementation Requirements:**

- **Use Haiku model** (`claude-haiku-4-5-20251001`) for all three functions
- **Call Anthropic API directly** using the pattern from `hivenode/adapters/anthropic.py`
- **Structured prompts** with clear instructions and examples
- **Token tracking** — return tokens_in, tokens_out, cost_usd in metadata dict
- **Error handling** — if LLM call fails, return safe default (REVERT for crash, AMBIGUOUS_SPEC for failure, passed=True for completion)
- **Mock-friendly design** — all LLM calls should go through a single `_call_haiku()` helper function for easy mocking in tests

### 2. Create `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\tests\test_triage.py`

Write comprehensive tests with these requirements:

**Minimum 12 tests:**

1. **`test_triage_crash_recovery_complete_enough`** — diff shows all deliverables done, tests pass
2. **`test_triage_crash_recovery_partial_safe`** — 50% done, safe to keep, generate continuation
3. **`test_triage_crash_recovery_revert`** — broken code, bad changes, start over
4. **`test_triage_crash_recovery_no_diff`** — no changes made, REVERT verdict
5. **`test_triage_failure_ambiguous_spec`** — bee says "unclear requirements"
6. **`test_triage_failure_coding_error`** — test failures, syntax errors
7. **`test_triage_failure_dependency_issue`** — import errors, missing upstream
8. **`test_triage_failure_environment_issue`** — missing tools, config errors
9. **`test_validate_completion_all_criteria_met`** — passed=True, all checkboxes ticked
10. **`test_validate_completion_missing_criteria`** — passed=True (advisory), but flags gaps
11. **`test_validate_completion_suspicious_changes`** — passed=True, but flags hardcoded colors
12. **`test_llm_call_failure_safe_defaults`** — network error → REVERT, AMBIGUOUS_SPEC, passed=True

**Test Requirements:**
- **Mock all LLM calls** — use `unittest.mock.patch` to mock `_call_haiku()` helper
- **No real API calls** — tests must pass offline with $0 cost
- **Test verdict routing logic** — verify correct return types and values
- **Test token/cost tracking** — verify metadata dict has correct fields
- **TDD approach** — write tests FIRST, then implement functions to pass them

### 3. Integration (Documentation Only — Do NOT Modify run_queue.py)

**Do NOT wire triage functions into `run_queue.py` in this task.** That will be done in a separate integration task after review.

Instead, document the three integration points in a new file:

**`C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\triage_integration_plan.md`**

```markdown
# Triage Integration Plan

## Integration Point 1: Crash Recovery (Orphan Scan on Startup)

**Location:** `run_queue.py` — startup orphan scan loop
**Trigger:** Spec found in `_active/` with no running process

**Pseudocode:**
```python
for spec in store.get_orphans():
    manifest = parse_manifest(spec)
    git_diff = subprocess.run(["git", "diff", "HEAD"], capture_output=True).stdout.decode()
    test_output = read_test_output_if_exists(spec.id)

    verdict, reasoning, metadata = triage_crash_recovery(
        spec.content, git_diff, test_output, manifest['started_at']
    )

    if verdict == CrashVerdict.COMPLETE_ENOUGH:
        subprocess.run(["git", "add", "."])
        subprocess.run(["git", "commit", "-m", f"Recovered: {spec.id}"])
        store.move_spec(spec.id, "active", "done", {"section": "Recovery", "content": reasoning})
    elif verdict == CrashVerdict.PARTIAL_SAFE:
        continuation_spec = generate_continuation_spec(spec, reasoning)
        write_spec_to_queue(continuation_spec)
        store.move_spec(spec.id, "active", "done", {"section": "Partial", "content": reasoning})
    elif verdict == CrashVerdict.REVERT:
        subprocess.run(["git", "checkout", "."])
        store.move_spec(spec.id, "active", "queue")

    emit_triage_event("crash_recovery", spec.id, verdict, metadata)
```

## Integration Point 2: Failure Diagnosis (After Bee Returns Error)

**Location:** `run_queue.py` — after dispatch returns error/timeout
**Trigger:** Bee returns NEEDS_DAVE, TIMEOUT, or CRASH

**Pseudocode:**
```python
if result.status in ("NEEDS_DAVE", "TIMEOUT", "CRASH"):
    response_file = find_response_file(spec.id)

    classification, reasoning, metadata = triage_failure(
        spec.content, response_file, result.error_output, result.test_results
    )

    if classification == FailureClassification.AMBIGUOUS_SPEC:
        store.move_spec(spec.id, "active", "needs_review", {"section": "Triage", "content": reasoning})
    elif classification == FailureClassification.CODING_ERROR:
        fix_spec = generate_fix_spec(spec, reasoning)
        write_spec_to_queue(fix_spec)
        store.move_spec(spec.id, "active", "failed")
    elif classification == FailureClassification.DEPENDENCY_ISSUE:
        # Extract dep ID from reasoning, add to spec's ## Depends On
        store.move_spec(spec.id, "active", "queue")  # will block until dep done
    elif classification == FailureClassification.ENVIRONMENT_ISSUE:
        store.move_spec(spec.id, "active", "needs_review", {"section": "Env Issue", "content": reasoning})

    emit_triage_event("failure_diagnosis", spec.id, classification, metadata)
```

## Integration Point 3: Completion Validation (Before Moving to _done/)

**Location:** `run_queue.py` — after bee reports CLEAN, before moving to `_done/`
**Trigger:** Bee returns CLEAN status

**Pseudocode:**
```python
if result.status == "CLEAN":
    acceptance_criteria = extract_acceptance_criteria(spec.content)
    git_diff = subprocess.run(["git", "diff", "HEAD~1"], capture_output=True).stdout.decode()
    test_results = result.test_results

    review, metadata = validate_completion(
        spec.content, git_diff, test_results, acceptance_criteria
    )

    # Phase 1: Advisory only — log but don't gate
    if not review.passed or review.confidence < 0.8:
        print(f"⚠️  Completion review flagged concerns for {spec.id}:")
        print(f"  Missing: {', '.join(review.missing_criteria)}")
        print(f"  Suspicious: {', '.join(review.suspicious_changes)}")
        print(f"  Recommendation: {review.recommendation}")

    # Always move to _done/ in Phase 1 (advisory mode)
    store.move_spec(spec.id, "active", "done", {"section": "Review", "content": review.recommendation})
    emit_triage_event("completion_validation", spec.id, review.recommendation, metadata)

    # Phase 2 (future): Gate on review.passed
    # if review.recommendation == "REJECT":
    #     store.move_spec(spec.id, "active", "needs_review")
```

## Event Emission

All three triage calls emit to ledger via `ledger_events.py`:

```python
def emit_triage_event(triage_type: str, spec_id: str, verdict: str, metadata: dict):
    from ledger_events import emit_validation_event

    emit_validation_event(
        spec_id=spec_id,
        phase=f"triage_{triage_type}",
        fidelity_score=None,  # N/A for triage
        tokens_in=metadata['tokens_in'],
        tokens_out=metadata['tokens_out'],
        model=metadata['model'],
        cost_usd=metadata['cost_usd'],
        attempt=1,
        result=verdict,
        healing_attempts=0,
        wall_time_seconds=metadata.get('wall_time_seconds', 0),
    )
```
```

---

## Technical Decisions

### 1. LLM Dispatch Mechanism

**Decision:** Use Anthropic Python SDK directly (synchronous calls)

**Rationale:**
- Queue runner already uses subprocess for dispatch — adding SDK dependency is fine
- Simpler than HTTP to hivenode LLM proxy (no server dependency)
- Synchronous calls are fine — triage is quick (~3-5s per call)
- Pattern exists in `hivenode/adapters/anthropic.py`

**Implementation:**
```python
from anthropic import Anthropic

def _call_haiku(prompt: str, system: str = "") -> tuple[str, int, int]:
    """Call Haiku model via Anthropic SDK.

    Returns:
        Tuple of (response_text, tokens_in, tokens_out)
    """
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=2048,
        temperature=0.3,  # Low temp for deterministic triage
        system=system if system else None,
        messages=[{"role": "user", "content": prompt}]
    )
    return (
        response.content[0].text,
        response.usage.input_tokens,
        response.usage.output_tokens,
    )
```

### 2. Git Diff Capture

**Decision:** Use `git diff HEAD` for crash recovery, `git diff HEAD~1` for completion validation

**Rationale:**
- Crash recovery: diff since last commit (bee's uncommitted changes)
- Completion validation: diff from last commit (bee's committed changes)
- No need for timestamp-based diff (`git diff HEAD@{timestamp}`) — simpler is better

### 3. Test Output Access

**Decision:** Read from `.deia/hive/responses/` if pytest output file exists, else pass `None`

**Rationale:**
- Queue runner may not always capture test output to file
- Triage functions must work with partial data
- Prompts explicitly say "test data may be unavailable"

### 4. Return Types

**Decision:** Use Enums for verdicts, dataclass for CompletionReview, dict for metadata

**Rationale:**
- Enums are type-safe and serializable
- Dataclass provides structure + type hints
- Dict for metadata allows flexibility (can add fields later)

---

## Constraints

1. **TDD** — Tests first, then implementation (Rule 5)
2. **No files over 500 lines** — `triage.py` should be ~100 lines, tests ~80 lines
3. **No stubs** — Every function fully implemented (Rule 6)
4. **Holdout principle** — Triage LLM (Haiku) must NOT be same session as bee being reviewed
5. **Phase 1 advisory mode** — `validate_completion` logs review but does NOT gate
6. **Mock LLM calls in tests** — No real API calls during test runs (Rule 5)
7. **Absolute paths** in this task file (Rule 8) — ✅ Done
8. **No git operations** in implementation — only documentation (Rule 10)

---

## Acceptance Criteria

- [ ] **`triage.py` exists** with all three functions fully implemented
  - `triage_crash_recovery(spec, diff, tests, started_at)` returns `(CrashVerdict, str, dict)`
  - `triage_failure(spec, response, errors, tests)` returns `(FailureClassification, str, dict)`
  - `validate_completion(spec, diff, tests, criteria)` returns `(CompletionReview, dict)`
  - All functions use Haiku model via Anthropic SDK
  - All functions return token counts and cost in metadata dict
  - Safe error handling — LLM failure returns safe defaults

- [ ] **`test_triage.py` exists** with ≥12 tests, all passing
  - All LLM calls are mocked (no real API calls)
  - Tests verify correct verdict types returned
  - Tests verify token/cost metadata structure
  - Tests verify safe defaults on LLM error
  - `pytest .deia/hive/scripts/queue/tests/test_triage.py -v` shows 12+ passed

- [ ] **`triage_integration_plan.md` exists** with documented integration points
  - Three integration points clearly described
  - Pseudocode for each integration point
  - Event emission pattern documented

- [ ] **No stubs** — every code path has real logic
  - No `# TODO`, no `pass`, no `raise NotImplementedError`
  - Prompts are complete with examples
  - Verdict parsing logic is complete

- [ ] **All existing queue tests still pass** (no regressions)
  - `pytest .deia/hive/scripts/queue/tests/ -v` — all tests pass
  - No imports broken, no side effects

- [ ] **Cost estimate accurate**
  - Implementation used ≤$0.60 in LLM calls (Sonnet for coding, Haiku for testing)
  - Document actual cost in response file

---

## Response Requirements — MANDATORY

When you finish your work, write a response file:

**`C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260317-TASK-227-RESPONSE.md`**

The response MUST contain these 8 sections:

1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full absolute paths
3. **What Was Done** — bullet list of concrete changes (not intent)
4. **Test Results** — test files run, pass/fail counts, output summary
5. **Build Verification** — all existing queue tests still pass
6. **Acceptance Criteria** — copy from above, mark [x] done or [ ] not done with explanation
7. **Clock / Cost / Carbon** — wall time, estimated USD cost, estimated CO2e
8. **Issues / Follow-ups** — anything that didn't work, edge cases, recommended next tasks

DO NOT skip any section.

---

## Example Prompt Structures

To guide your implementation, here are example prompts for each triage function:

### Crash Recovery Prompt Template

```
You are a code reviewer analyzing a crashed development session.

## Task
A bee (AI worker) was working on this spec when it crashed:

{spec_content}

The session started at: {started_at}

## Changes Made
{git_diff}

## Test Output
{test_output or "No test output available"}

## Your Job
Analyze the changes and determine:
1. What % of the spec's deliverables are complete?
2. Are the changes safe to keep or should we revert?
3. If partial, what's left to do?

## Response Format
Return a JSON object with:
{
  "verdict": "COMPLETE_ENOUGH" | "PARTIAL_SAFE" | "REVERT",
  "confidence": 0.0-1.0,
  "completion_pct": 0-100,
  "reasoning": "1-2 sentence explanation",
  "missing": ["deliverable 1", "deliverable 2"],
  "risks": ["risk 1", "risk 2"]
}

## Verdicts
- COMPLETE_ENOUGH: ≥80% done, all critical tests pass, safe to commit and close
- PARTIAL_SAFE: 40-80% done, changes are correct but incomplete, keep diff and generate continuation spec
- REVERT: <40% done OR broken code OR bad changes, discard and start over
```

### Failure Diagnosis Prompt Template

```
You are diagnosing why a development task failed.

## Spec
{spec_content}

## Error Output
{error_output}

## Response File
{response_file_content or "No response file written"}

## Test Results
{test_results or "No test results available"}

## Your Job
Classify the failure into one of these categories:

1. **AMBIGUOUS_SPEC** — The spec was unclear, incomplete, or contradictory. The bee did its best but had no clear direction.
2. **CODING_ERROR** — The spec was clear but the bee wrote buggy code (syntax errors, test failures, wrong logic).
3. **DEPENDENCY_ISSUE** — Upstream dependency is broken or missing (import errors, missing files, blocking issue).
4. **ENVIRONMENT_ISSUE** — Setup/config problem (missing tools, wrong Python version, permissions, etc.).

## Response Format
Return a JSON object with:
{
  "classification": "AMBIGUOUS_SPEC" | "CODING_ERROR" | "DEPENDENCY_ISSUE" | "ENVIRONMENT_ISSUE",
  "confidence": 0.0-1.0,
  "reasoning": "1-2 sentence explanation",
  "suggested_fix": "What should happen next?"
}
```

### Completion Validation Prompt Template

```
You are reviewing completed work against acceptance criteria.

## Spec Acceptance Criteria
{acceptance_criteria}

## Changes Made
{git_diff}

## Test Results
{test_results}

## Your Job
Check if ALL acceptance criteria are met. Flag:
- Missing deliverables
- Suspicious changes (hardcoded colors, stubs, TODOs)
- Test coverage gaps

## Response Format
Return a JSON object with:
{
  "passed": true | false,
  "confidence": 0.0-1.0,
  "missing_criteria": ["criterion 1", "criterion 2"],
  "suspicious_changes": ["issue 1", "issue 2"],
  "recommendation": "ACCEPT" | "REVIEW" | "REJECT"
}

## Notes
- In Phase 1, you are advisory only. Always return passed=true but flag concerns.
- Check for hardcoded colors (hex/rgb/named instead of CSS variables).
- Check for stubs (TODO, NotImplementedError, empty functions).
- Check for test files matching acceptance criteria.
```

---

## Notes for Implementation

1. **Cost Model:** Each triage call costs ~$0.01-0.03 (Haiku). At 10% failure rate on 50 specs/day = 5 calls = $0.05-0.15/day. Trivial vs. cost of re-running full Sonnet bee.

2. **Existing Patterns:** Check `ledger_events.py` for event emission patterns. Check `filesystem_store.py` for how queue runner interacts with state.

3. **TASK-224 Fix Pending:** The fix spec for TASK-224 is P0 in queue, but it's about dispatch role detection, not state machine logic. This work can proceed in parallel.

4. **Integration Task:** After this task is complete and reviewed, a separate task (TASK-228 or similar) will wire these functions into `run_queue.py`. Do NOT do that integration in this task.

5. **Holdout Enforcement:** The triage functions themselves don't need to enforce holdout — the queue runner will ensure different model/session is used for triage vs. original work.

---

**End of Task File**
