# TRIAGE ESCALATION: PHASE-IR

**Date:** 2026-04-16 15:19:55 UTC
**Reason:** 3 requeue attempts (max 3)
**Status:** NEEDS MANUAL REVIEW

## Summary

Spec `SPEC-PHASE-IR-ANALYSIS-001.md` has been requeued 3 times and failed each time.
Automated triage has moved it to `_escalated/` for manual review.

## Triage History

- 2026-04-16T14:49:55.196593Z — requeued (empty output)
- 2026-04-16T15:09:55.212633Z — requeued (empty output)
- 2026-04-16T15:14:55.244014Z — requeued (empty output)

## Next Steps

1. **Review spec file** in `queue/_escalated/SPEC-PHASE-IR-ANALYSIS-001.md`
2. **Diagnose root cause** — why is this spec failing repeatedly?
3. **Options:**
   - Fix spec and move back to backlog/
   - Archive spec if no longer needed
   - Break into smaller specs
   - Escalate to architect (Mr. AI) if systemic issue

## Original Spec

```markdown
## Clean Retry

**Previous attempt failed with no output.**

This is a clean retry — start from scratch. Check logs if available to
understand why the previous attempt failed.

---

## Clean Retry

**Previous attempt failed with no output.**

This is a clean retry — start from scratch. Check logs if available to
understand why the previous attempt failed.

---

## Clean Retry

**Previous attempt failed with no output.**

This is a clean retry — start from scratch. Check logs if available to
understand why the previous attempt failed.

---

# SPEC-PHASE-IR-ANALYSIS-001

**Title:** Add Petri net analysis tools  
**Priority:** P3  
**Status:** DRAFT  
**Date:** 2026-04-15  
**Author:** Q88N  
**Depends on:** None

---

## Problem

PRISM-IR flows compile to Petri net semantics internally (places, transitions, tokens, arcs). But from the audit (2026-04-14):
> "gap_004: No Petri net analysis tools (reachability, liveness, boundedness)"

Without analysis tools, you can't answer before running:
- "Can this flow deadlock?" (liveness)
- "Can tokens pile up unbounded?" (boundedness)
- "Can this state ever be reached?" (reachability)
- "Are there unreachable nodes?" (structural validation)

These are static analysis — no simulation needed.

---

## Solution

Add Petri net analysis functions to validate flows before execution.

---

## Requirements

### R1: Reachability graph

Compute all reachable markings from initial state:

```python
def reachability_graph(flow: Flow) -> ReachabilityGraph:
    """
    Compute reachability graph.
    
    Returns:
        ReachabilityGraph with:
        - markings: Set[Marking]  # All reachable states
        - transitions: Dict[Marking, List[(transition_id, Marking)]]
        - initial: Marking
        - terminal: Set[Marking]  # Markings with no outbound
    """
```

### R2: Liveness check

Determine if flow can complete or may deadlock:

```python
def is_live(flow: Flow) -> LivenessResult:
    """
    Check liveness properties.
    
    Returns:
        LivenessResult with:
        - is_live: bool  # All transitions can eventually fire
        - dead_transitions: List[str]  # Transitions that can never fire
        - potential_deadlocks: List[Marking]  # Non-terminal stuck states
    """
```

Liveness levels:
- **L0-live:** Transition can fire at least once
- **L1-live:** Transition can fire from any reachable marking
- **L4-live (live):** Transition can fire infinitely often

For workflow validation, L0 is usually sufficient.

### R3: Boundedness check

Determine if token counts are bounded:

```python
def is_bounded(flow: Flow, bound: int = None) -> BoundednessResult:
    """
    Check if flow is bounded.
    
    Args:
        bound: Optional max tokens per place. If None, check for any bound.
    
    Returns:
        BoundednessResult with:
        - is_bounded: bool
        - max_tokens_per_place: Dict[str, int]
        - unbounded_places: List[str]  # Places with no bound
    """
```

- **1-bounded (safe):** Each place has at most 1 token
- **k-bounded:** Each place has at most k tokens
- **Unbounded:** Token count can grow infinitely

### R4: Structural validation

Static checks without state space exploration:

```python
def structural_analysis(flow: Flow) -> StructuralResult:
    """
    Structural Petri net analysis.
    
    Returns:
        StructuralResult with:
        - is_connected: bool  # All nodes reachable from start
        - unreachable_nodes: List[str]
        - sink_nodes: List[str]  # Nodes with no outbound (should be end nodes)
        - source_nodes: List[str]  # Nodes with no inbound (should be start)
        - has_cycles: bool
        - cycle_nodes: List[str]  # Nodes participating in cycles
    """
```

### R5: Invariant computation

Compute place and transition invariants:

```python
def compute_invariants(flow: Flow) -> InvariantResult:
    """
    Compute Petri net invariants.
    
    Returns:
        InvariantResult with:
        - place_invariants: List[Dict[str, int]]  # Token conservation laws
        - transition_invariants: List[Dict[str, int]]  # Firing sequences returning to initial
    """
```

Place invariants: weighted sums of tokens that remain constant.
Transition invariants: firing sequences that return to original marking.

### R6: Deadlock detection

Specific check for deadlock states:

```python
def find_deadlocks(flow: Flow) -> List[DeadlockInfo]:
    """
    Find potential deadlock states.
    
    Returns:
        List of DeadlockInfo with:
        - marking: Marking  # The stuck state
        - path_to_deadlock: List[str]  # Transition sequence to reach it
        - stuck_tokens: Dict[str, int]  # Where tokens are stuck
    """
```

### R7: Flow validation summary

Combined validation for pre-flight check:

```python
def validate_flow(flow: Flow) -> ValidationReport:
    """
    Run all structural and behavioral checks.
    
    Returns:
        ValidationReport with:
        - is_valid: bool
        - errors: List[ValidationError]  # Must fix
        - warnings: List[ValidationWarning]  # Should review
        - info: AnalysisInfo  # Structural properties
    """
```

Errors:
- Unreachable nodes (except isolated subflows)
- No path from start to any end
- Deadlock states reachable

Warnings:
- Unbounded places
- Dead transitions
- Cycles without exit conditions

---

## Implementation Location

| File | Change |
|------|--------|
| `simdecisions/phase_ir/analysis.py` | New file with all analysis functions |
| `simdecisions/phase_ir/petri.py` | Petri net representation (may exist in formalism.py) |
| `simdecisions/phase_ir/cli_commands.py` | Add `validate --analysis` command |
| `simdecisions/phase_ir/schema_routes.py` | Add `/validate` endpoint with analysis |

---

## Test Cases

### T1: Simple valid flow

```
start → task → end
```

- `is_live`: True
- `is_bounded`: True (1-bounded)
- `find_deadlocks`: []
- `validate_flow`: is_valid=True

### T2: Deadlock-prone flow

```
start → fork → [task_a, task_b] → join → end
```

If join requires both but task_b can fail:
- `find_deadlocks`: Returns marking where token stuck at join

### T3: Unbounded flow

```
start → loop_body → [exit | loop_body]  (no exit condition)
```

- `is_bounded`: False
- Warning: unbounded accumulation possible

### T4: Unreachable node

```
start → task_a → end
orphan_node (no edges to it)
```

- `structural_analysis`: unreachable_nodes = ["orphan_node"]
- `validate_flow`: error

---

## Acceptance Criteria

- [ ] `reachability_graph()` computes all reachable markings
- [ ] `is_live()` detects dead transitions
- [ ] `is_bounded()` detects unbounded places
- [ ] `structural_analysis()` finds unreachable/sink/source nodes
- [ ] `find_deadlocks()` returns path to deadlock states
- [ ] `validate_flow()` provides pre-flight validation report
- [ ] CLI command `validate --analysis` runs full check
- [ ] API endpoint `/validate` includes analysis results

---

## Limitations

- State space explosion for large flows (mitigate with partial exploration)
- Timed/stochastic properties not analyzed (that's simulation)
- Resource constraints not modeled in Petri analysis (future extension)

---

## Estimated Effort

6-8 hours. Standard Petri net algorithms, but careful implementation needed.

---

## Notes

This is static analysis — runs in milliseconds, catches design errors before simulation burns compute. Every flow should pass `validate_flow()` before going to DES.

## Triage History
- 2026-04-16T14:49:55.196593Z — requeued (empty output)
- 2026-04-16T15:09:55.212633Z — requeued (empty output)
- 2026-04-16T15:14:55.244014Z — requeued (empty output)

```

---

**Automated escalation by triage daemon**
