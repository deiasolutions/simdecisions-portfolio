# Triage Integration Plan

## Overview

This document describes how to integrate the three LLM triage functions into the queue runner's state machine. These functions are implemented in `triage.py` but are NOT yet wired into `run_queue.py`.

**Integration will be done in a separate task** after this implementation is reviewed and approved.

---

## Integration Point 1: Crash Recovery (Orphan Scan on Startup)

**Location:** `run_queue.py` — startup orphan scan loop (around line 172-206)
**Trigger:** Spec found in `_active/` with no running process

**Current Code (lines ~296-302 in get_orphans):**
```python
def get_orphans(self) -> list[SpecFile]:
    """Return specs in _active/ (for crash recovery).

    Returns:
        List of SpecFile objects currently in _active/
    """
    return self.list_specs("active")
```

**Integration Pseudocode:**
```python
from .triage import triage_crash_recovery, CrashVerdict

# In main run_queue loop, after loading specs
orphans = store.get_orphans()

for spec in orphans:
    print(f"🔍 Orphan detected: {spec.id}")

    # Capture current state
    git_diff = subprocess.run(
        ["git", "diff", "HEAD"],
        capture_output=True,
        cwd=repo_root
    ).stdout.decode()

    # Try to read test output from responses/
    test_output = None
    test_output_pattern = responses_dir / f"*{spec.id}*test*.txt"
    test_files = list(responses_dir.glob(test_output_pattern.name))
    if test_files:
        test_output = test_files[0].read_text(encoding='utf-8')

    # Get start time from manifest
    started_at = spec.manifest.get('started_at', datetime.now().isoformat())

    # Triage the orphan
    verdict, reasoning, metadata = triage_crash_recovery(
        spec.content, git_diff, test_output, started_at
    )

    # Emit triage event
    emit_triage_event("crash_recovery", spec.id, verdict.value, metadata)

    # Route based on verdict
    if verdict == CrashVerdict.COMPLETE_ENOUGH:
        print(f"✅ {spec.id}: Complete enough — committing and closing")
        subprocess.run(["git", "add", "."], cwd=repo_root)
        subprocess.run([
            "git", "commit", "-m",
            f"Recovered: {spec.id}\n\n{reasoning}"
        ], cwd=repo_root)
        store.move_spec(spec.id, "active", "done", {
            "section": "Recovery",
            "content": f"Crash recovery verdict: {verdict.value}\n{reasoning}"
        })

    elif verdict == CrashVerdict.PARTIAL_SAFE:
        print(f"⚠️  {spec.id}: Partial work safe — generating continuation spec")
        # Generate continuation spec (use fix_cycle.py pattern)
        continuation_spec = generate_continuation_spec(spec, reasoning, metadata)
        continuation_path = queue_dir / continuation_spec.filename
        continuation_path.write_text(continuation_spec.content, encoding='utf-8')

        # Move original to done with partial flag
        store.move_spec(spec.id, "active", "done", {
            "section": "Partial Completion",
            "content": f"Partial work saved. Continuation: {continuation_spec.filename}\n{reasoning}"
        })

    elif verdict == CrashVerdict.REVERT:
        print(f"❌ {spec.id}: Reverting changes — retrying from scratch")
        subprocess.run(["git", "checkout", "."], cwd=repo_root)
        store.move_spec(spec.id, "active", "queue")

    print(f"💰 Triage cost: ${metadata['cost_usd']:.4f} ({metadata['tokens_in']}+{metadata['tokens_out']} tokens)")
```

**Helper Function to Add:**
```python
def generate_continuation_spec(original_spec: SpecFile, reasoning: str, metadata: dict) -> dict:
    """Generate continuation spec for partial work.

    Args:
        original_spec: The partially-completed spec
        reasoning: Triage reasoning explaining what's done and what's left
        metadata: Triage metadata dict

    Returns:
        Dict with 'filename' and 'content' for new spec
    """
    timestamp = datetime.now().strftime("%Y-%m-%d-%H%M")
    continuation_id = f"{timestamp}-CONT-{original_spec.id}"

    content = f"""# {continuation_id}: Continue {original_spec.id}

## Context

Previous bee partially completed {original_spec.id} before crashing.
The work done so far has been committed and is safe to build on.

## What Was Completed

{reasoning}

## What Remains

Review the original spec and complete the remaining deliverables:

{original_spec.content}

## Triage Metadata

- Model: {metadata['model']}
- Cost: ${metadata['cost_usd']:.4f}
- Tokens: {metadata['tokens_in']} + {metadata['tokens_out']}

## Acceptance Criteria

- [ ] Complete all remaining deliverables from original spec
- [ ] All tests pass
- [ ] No regressions introduced
"""

    return {
        "filename": f"{continuation_id}.md",
        "content": content
    }
```

---

## Integration Point 2: Failure Diagnosis (After Bee Returns Error)

**Location:** `run_queue.py` — after dispatch returns error/timeout (around line 350-400)
**Trigger:** Bee returns NEEDS_DAVE, TIMEOUT, or CRASH

**Current Code Pattern:**
```python
# After process_spec() returns SpecResult
if result.status in ("NEEDS_DAVE", "TIMEOUT", "CRASH"):
    # Currently just moves to _failed/ or _needs_review/
    pass
```

**Integration Pseudocode:**
```python
from .triage import triage_failure, FailureClassification

if result.status in ("NEEDS_DAVE", "TIMEOUT", "CRASH"):
    print(f"🩺 Diagnosing failure for {spec.id}")

    # Find response file
    response_file = None
    response_pattern = responses_dir / f"*{spec.id}*RESPONSE.md"
    response_files = list(responses_dir.glob(response_pattern.name))
    if response_files:
        response_file = str(response_files[0])

    # Triage the failure
    classification, reasoning, metadata = triage_failure(
        spec.content,
        response_file,
        result.error_output,
        result.test_results
    )

    # Emit triage event
    emit_triage_event("failure_diagnosis", spec.id, classification.value, metadata)

    # Route based on classification
    if classification == FailureClassification.AMBIGUOUS_SPEC:
        print(f"📝 {spec.id}: Ambiguous spec — needs human rewrite")
        store.move_spec(spec.id, "active", "needs_review", {
            "section": "Triage: Ambiguous Spec",
            "content": reasoning
        })

    elif classification == FailureClassification.CODING_ERROR:
        print(f"🐛 {spec.id}: Coding error — generating fix spec")
        fix_spec = generate_fix_spec(spec, reasoning, result)
        fix_path = queue_dir / fix_spec.filename
        fix_path.write_text(fix_spec.content, encoding='utf-8')

        store.move_spec(spec.id, "active", "failed", {
            "section": "Triage: Coding Error",
            "content": f"Fix spec generated: {fix_spec.filename}\n{reasoning}"
        })

    elif classification == FailureClassification.DEPENDENCY_ISSUE:
        print(f"⛓️  {spec.id}: Dependency issue — blocking until upstream fixed")

        # Extract dependency ID from reasoning (LLM should mention it)
        # Simple pattern: look for TASK-XXX or SPEC-XXX in reasoning
        dep_match = re.search(r'(TASK-\d+|SPEC-\w+-\d+)', reasoning)
        if dep_match:
            dep_id = dep_match.group(1)
            # Append to spec's ## Depends On section
            updated_content = spec.content + f"\n\n## Depends On\n- {dep_id}\n"
            spec_path = store._find_spec_path(spec.id, "active")
            spec_path.write_text(updated_content, encoding='utf-8')

        # Move back to queue (will block until dep done)
        store.move_spec(spec.id, "active", "queue")

    elif classification == FailureClassification.ENVIRONMENT_ISSUE:
        print(f"⚙️  {spec.id}: Environment issue — needs human intervention")
        store.move_spec(spec.id, "active", "needs_review", {
            "section": "Triage: Environment Issue",
            "content": reasoning
        })

    print(f"💰 Triage cost: ${metadata['cost_usd']:.4f}")
```

---

## Integration Point 3: Completion Validation (Before Moving to _done/)

**Location:** `run_queue.py` — after bee reports CLEAN, before moving to `_done/` (around line 400-450)
**Trigger:** Bee returns CLEAN status

**Current Code Pattern:**
```python
if result.status == "CLEAN":
    store.move_spec(spec.id, "active", "done")
```

**Integration Pseudocode:**
```python
from .triage import validate_completion

if result.status == "CLEAN":
    print(f"🔬 Validating completion for {spec.id}")

    # Extract acceptance criteria from spec
    acceptance_criteria = extract_acceptance_criteria(spec.content)

    # Get git diff (last commit, which should be the bee's commit)
    git_diff = subprocess.run(
        ["git", "diff", "HEAD~1"],
        capture_output=True,
        cwd=repo_root
    ).stdout.decode()

    # Validate completion
    review, metadata = validate_completion(
        spec.content,
        git_diff,
        result.test_results or "",
        acceptance_criteria
    )

    # Emit triage event
    emit_triage_event(
        "completion_validation",
        spec.id,
        review.recommendation,
        metadata
    )

    # Phase 1: Advisory only — log but don't gate
    if not review.passed or review.confidence < 0.8:
        print(f"⚠️  Completion review flagged concerns for {spec.id}:")
        print(f"  Confidence: {review.confidence:.0%}")
        if review.missing_criteria:
            print(f"  Missing: {', '.join(review.missing_criteria)}")
        if review.suspicious_changes:
            print(f"  Suspicious: {', '.join(review.suspicious_changes)}")
        print(f"  Recommendation: {review.recommendation}")

    # Always move to _done/ in Phase 1 (advisory mode)
    store.move_spec(spec.id, "active", "done", {
        "section": "Completion Review",
        "content": f"""Validation: {review.recommendation}
Confidence: {review.confidence:.0%}
Missing: {', '.join(review.missing_criteria) if review.missing_criteria else 'none'}
Suspicious: {', '.join(review.suspicious_changes) if review.suspicious_changes else 'none'}
"""
    })

    print(f"💰 Triage cost: ${metadata['cost_usd']:.4f}")

    # Phase 2 (future): Gate on review.passed
    # if review.recommendation == "REJECT":
    #     print(f"❌ {spec.id}: Rejected by completion review")
    #     store.move_spec(spec.id, "active", "needs_review", {
    #         "section": "Completion Review: Rejected",
    #         "content": f"Confidence: {review.confidence:.0%}\n{review.recommendation}"
    #     })
    # elif review.recommendation == "REVIEW":
    #     print(f"⚠️  {spec.id}: Flagged for human review")
    #     store.move_spec(spec.id, "active", "needs_review", {
    #         "section": "Completion Review: Manual Check Required",
    #         "content": f"Confidence: {review.confidence:.0%}\n{review.recommendation}"
    #     })
    # else:
    #     store.move_spec(spec.id, "active", "done", ...)
```

**Helper Function to Add:**
```python
def extract_acceptance_criteria(spec_content: str) -> list[str]:
    """Extract acceptance criteria from spec markdown.

    Args:
        spec_content: Full spec markdown content

    Returns:
        List of criteria strings (without checkboxes)
    """
    import re

    criteria = []
    in_criteria_section = False

    for line in spec_content.split('\n'):
        # Check if we're entering the acceptance criteria section
        if re.match(r'^##\s+Acceptance Criteria', line, re.IGNORECASE):
            in_criteria_section = True
            continue

        # Check if we've left the section (next ## heading)
        if in_criteria_section and re.match(r'^##\s+', line):
            break

        # Extract checkbox items
        if in_criteria_section:
            match = re.match(r'^\s*-\s+\[[ x]\]\s+(.+)$', line)
            if match:
                criteria.append(match.group(1).strip())

    return criteria
```

---

## Event Emission

All three triage calls emit events to the ledger via `ledger_events.py`:

```python
def emit_triage_event(
    triage_type: str,
    spec_id: str,
    verdict: str,
    metadata: dict
):
    """Emit triage event to Event Ledger.

    Args:
        triage_type: "crash_recovery" | "failure_diagnosis" | "completion_validation"
        spec_id: SPEC-XXX identifier
        verdict: Verdict/classification/recommendation string
        metadata: Dict with tokens_in, tokens_out, cost_usd, model
    """
    from .ledger_events import emit_validation_event

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

**Add this helper to `run_queue.py` imports section:**
```python
from .triage import (
    triage_crash_recovery,
    triage_failure,
    validate_completion,
    CrashVerdict,
    FailureClassification,
)
```

---

## Cost Tracking

All triage costs should be tracked in the queue runner's cost accumulator:

```python
# After each triage call
total_cost_usd += metadata['cost_usd']
```

This ensures triage costs are included in the morning report and budget calculations.

---

## Testing Integration

Before integrating, ensure:

1. **Unit tests pass:** `pytest .deia/hive/scripts/queue/tests/test_triage.py -v`
2. **Queue runner tests still pass:** `pytest .deia/hive/scripts/queue/tests/ -v`
3. **No import errors:** `python -c "from .deia.hive.scripts.queue.triage import *"`

After integrating:

1. **Test orphan recovery:** Manually create an orphan in `_active/` and run queue
2. **Test failure diagnosis:** Trigger a NEEDS_DAVE failure and verify triage routing
3. **Test completion validation:** Complete a spec with CLEAN and verify review logging

---

## Rollout Plan

**Phase 1 (Current):** Advisory mode
- Completion validation logs concerns but always returns passed=True
- No blocking, no gating, just logging and learning

**Phase 2 (Future — after 2+ weeks of validation data):**
- Enable gating on completion review (REJECT → _needs_review/)
- Tune confidence thresholds based on false positive/negative rates
- Add metrics dashboard for triage accuracy

**Phase 3 (Future):**
- Add self-healing: if triage confidence < 0.5, ask second LLM (Sonnet) for opinion
- Add human feedback loop: tag triage decisions, track accuracy over time
- Add cost/benefit analysis: measure time saved vs. triage cost

---

## Open Questions

1. **Continuation spec priority:** Should continuation specs inherit priority from original, or use P1 default?
   - Recommendation: Inherit priority + add urgency flag

2. **Fix spec vs. continuation spec:** When coding error detected, should we generate fix spec or continuation spec?
   - Recommendation: Fix spec (narrower scope, targeted fix)

3. **Dependency extraction:** Should LLM explicitly return dependency IDs in structured format?
   - Recommendation: Yes — add `"dependency_id"` field to FailureClassification response

4. **Triage retry:** If triage LLM call fails (network, etc.), should we retry or use safe default?
   - Recommendation: Use safe default (current behavior), log retry-worthy errors

---

## End of Integration Plan
