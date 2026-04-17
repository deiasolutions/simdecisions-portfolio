# QUEUE-TEMP-SPEC-ML-TRAINING-V1: ML Training System -- BLOCKED

**Status:** BLOCKED (dependency not met)
**Model:** Sonnet 4.5
**Date:** 2026-04-13
**Bot ID:** BEE-QUEUE-TEMP-SPEC-ML-TRAINING-V1

## Blocker Report

**Cannot proceed with SPEC-ML-TRAINING-V1 due to unmet dependencies.**

### Dependencies Required

This spec declares:
```
Depends On: SPEC-EVENT-LEDGER-GAMIFICATION, SPEC-GAMIFICATION-V1
```

### Current Dependency Status

1. **SPEC-EVENT-LEDGER-GAMIFICATION**
   - Location: `.deia/hive/queue/_needs_review/SPEC-EVENT-LEDGER-GAMIFICATION.md`
   - Status: NOT COMPLETE (in review, not implemented)

2. **SPEC-GAMIFICATION-V1**
   - Location: `.deia/hive/queue/_active/SPEC-GAMIFICATION-V1.md`
   - Status: NOT COMPLETE (in active queue, not implemented)
   - Also depends on: SPEC-EVENT-LEDGER-GAMIFICATION

### Why This Blocks ML Training

The ML Training spec requires:
- Event Ledger infrastructure to exist (for collecting training data)
- Gamification events to be emitted (as training signals)
- Database schema from both dependencies (for user factors, XP events)

From the spec:
> "Every event in ShiftCenter is training data."
> "The Event Ledger is the single source of truth."

Without the Event Ledger and Gamification systems implemented, there is:
- No event collection infrastructure
- No user_progression table
- No xp_events table
- No user_factors table (ρ-π-σ-τ)
- No training data to work with

### Recommended Action

**Move SPEC-ML-TRAINING-V1 to `.deia/hive/queue/_parked/`** with a note that it requires:
1. SPEC-EVENT-LEDGER-GAMIFICATION to be completed
2. SPEC-GAMIFICATION-V1 to be completed

Then process those dependencies first, in order:
1. SPEC-EVENT-LEDGER-GAMIFICATION (P2, foundational)
2. SPEC-GAMIFICATION-V1 (P3, builds on ledger)
3. SPEC-ML-TRAINING-V1 (P3, builds on both)

### Queue Processing Guidance

The queue runner should:
- Detect dependency declarations in spec frontmatter
- Check if dependencies are in `_done/` before dispatching
- Auto-park specs with unmet dependencies
- Re-evaluate parked specs when dependencies complete

This prevents wasted dispatch cycles on blocked work.

## Files Modified

None (blocked before work started)

## What Was Done

- Read spec SPEC-ML-TRAINING-V1
- Identified dependency declarations
- Checked queue status for dependencies
- Confirmed dependencies are not complete
- Wrote blocker report

## Tests Run

None (blocked before implementation)

## Lessons Learned

**Dependency checking should happen at queue triage, not at bee dispatch.**

The dispatcher should validate:
```python
def can_dispatch(spec):
    if "depends_on" in spec.frontmatter:
        for dep in spec.frontmatter["depends_on"]:
            dep_path = queue_dir / "_done" / f"{dep}.md"
            if not dep_path.exists():
                return False, f"Dependency {dep} not complete"
    return True, None
```

This saves:
- Bee dispatch cost (avoided wasted LLM calls)
- Queue runner time
- Session budget

## Blockers

**Primary Blocker:** SPEC-EVENT-LEDGER-GAMIFICATION not implemented
**Secondary Blocker:** SPEC-GAMIFICATION-V1 not implemented

## Next Steps (for Q33NR)

1. Move `SPEC-ML-TRAINING-V1.md` from `_active/` to `_parked/`
2. Add dependency check to dispatcher (`dispatch_handler.py`)
3. Process SPEC-EVENT-LEDGER-GAMIFICATION next
4. Then process SPEC-GAMIFICATION-V1
5. Finally return to SPEC-ML-TRAINING-V1

---

**Completion Time:** 0 ms (blocked immediately)
**Cost:** ~$0.02 (read spec, detect blocker, write report)
