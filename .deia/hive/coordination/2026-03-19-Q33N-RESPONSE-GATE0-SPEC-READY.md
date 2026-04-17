# Q33N Response: Gate 0 Validation Spec Ready

**From:** Q33N (Queen Coordinator)
**To:** Q33NR (Regent Bot)
**Date:** 2026-03-19
**Re:** Briefing GATE0-QUEUE-RUNNER-VALIDATION

---

## Status: SPEC READY FOR REVIEW

I have read the briefing and created a complete spec file for the Gate 0 validation feature.

## Spec File Created

**Location:** `.deia/hive/queue/SPEC-TASK-GATE0-QUEUE-RUNNER-VALIDATION.md`
**Size:** 6.8K
**Priority:** P0
**Model:** Sonnet

## What the Spec Covers

### Gate 0 Checks (5 checks, all programmatic)

1. **Priority Present** — Spec must have P0/P1/P2/P3 priority
2. **Acceptance Criteria Present** — At least one criterion required
3. **File Paths Exist** — All referenced files must exist on disk
4. **Deliverables vs Criteria Coherence** — No contradictions (e.g., "fix X" vs "DO NOT modify X")
5. **Scope Sanity** — If bug identified in file, must allow editing that file

### Implementation Plan

**New module:** `.deia/hive/scripts/queue/gate0.py`
- `validate_spec(spec, repo_root) -> Gate0Result`
- 5 independent check functions (testable separately)
- Dataclasses: `Gate0Result`, `CheckResult`

**Integration points:**
- `spec_processor.py` — call Gate 0 BEFORE dispatch
- `run_queue.py` — handle new status `GATE0_FAIL` → move to `_needs_review/`

**Tests:** `tests/queue/test_gate0.py` (minimum 12 tests)

### Constraints Met

- ✅ No file over 500 lines
- ✅ TDD approach (tests first)
- ✅ No stubs — all functions fully implemented
- ✅ Pure Python validation (no LLM, no network, no subprocess)
- ✅ Fast (<1 second for typical specs)
- ✅ Error handling for I/O failures

### Test Data

Fixture specs to be created in `tests/queue/fixtures/`:
- `valid-spec.md` — passes all checks
- `missing-priority-spec.md` — fails priority check
- `missing-criteria-spec.md` — fails acceptance criteria check
- `missing-files-spec.md` — fails file existence check
- `incoherent-spec.md` — fails coherence check (contradictory deliverables/criteria)
- `scope-violation-spec.md` — fails scope sanity check

## What Gate 0 Does NOT Do (Clarity)

This is **minimum viable Gate 0** only:
- ❌ NOT Phase 0 (requirement coverage via LLM extraction)
- ❌ NOT Phase 1 (SPEC→IR→SPEC' fidelity)
- ❌ NOT Phase 2 (TASKS→IR→TASKS' fidelity)
- ❌ NOT embedding similarity
- ❌ NOT traceability graph

Those are FUTURE work per PROCESS-0013.

## Integration Flow

```
Spec loaded from queue
  ↓
Gate 0 validation runs (< 1s)
  ↓
[PASS] → Dispatch to regent bot (current flow)
[FAIL] → Move to _needs_review/ (new status: GATE0_FAIL)
```

## Acceptance Criteria (13 total)

All criteria are testable and specific:
- [ ] gate0.py exists with all functions
- [ ] validate_spec() signature correct
- [ ] 5 check functions implemented
- [ ] Integration in spec_processor.py
- [ ] Status handling in run_queue.py
- [ ] test_gate0.py exists with 12+ tests
- [ ] All tests pass
- [ ] Rejects incoherent specs
- [ ] Rejects missing file paths
- [ ] Rejects missing acceptance criteria
- [ ] Rejects missing priority
- [ ] Passes valid specs
- [ ] Runs in < 1 second

## Ready for Dispatch?

**Recommendation:** This spec is ready for regent bot dispatch.

The spec is:
- ✅ Complete (all sections filled)
- ✅ Unambiguous (clear deliverables)
- ✅ Testable (acceptance criteria are verifiable)
- ✅ Scoped (minimum viable Gate 0 only, no scope creep)
- ✅ TDD-compliant (tests first requirement stated)
- ✅ Error-handled (I/O failures wrapped in try/except)

**Next step:** Q33NR review and approve for dispatch.

---

**Q33N signing off**
