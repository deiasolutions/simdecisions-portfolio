# DISPATCH INSTRUCTIONS: EXP-TREATMENT-B-Q33N-SWARM

**Date:** 2026-04-09
**Status:** Ready for Q33N dispatch
**Fix Cycle:** 1 of 2

---

## Quick Summary

The original spec was dispatched as a worker bee task, but it requires Q33N coordination. A proper briefing file has been created. Q33N needs to be dispatched with the correct role flag.

---

## What Happened

1. **Original spec:** `SPEC-EXP-TREATMENT-B-Q33N-SWARM.md` entered the queue
2. **Queue runner** dispatched it directly to a bee with `--role bee`
3. **Bee detected conflict:** Spec said "You are Q33N coordinator" but role injection said "You are worker bee"
4. **Bee correctly refused** citing Rule 7 (STAY IN YOUR LANE)
5. **Fix created:** Proper Q33N briefing file with coordinator instructions

---

## What Needs to Happen

**Option 1: Manual Q33N Dispatch (Recommended)**

```bash
cd C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter
python .deia/hive/scripts/dispatch/dispatch.py \
  .deia/hive/coordination/20260409-EXP-B-BRIEFING.md \
  --role queen \
  --model sonnet \
  --inject-boot
```

This dispatches Q33N (Sonnet, coordinator role) with the briefing file.

**Option 2: Queue Enhancement**

Enhance the queue runner to detect specs that require coordination:
- Add `Coordinator: Q33N` to spec frontmatter
- Or create `queue/coordination/` directory for Q33N-only specs
- Or parse spec content for "## Q33N Instructions" section

For now, **Option 1 is simpler and gets the experiment running.**

---

## Expected Q33N Workflow

1. Q33N reads briefing
2. Creates 2-3 task files (TASK-B-01, TASK-B-02, TASK-B-03)
3. Dispatches Sonnet bees to execute each task
4. Reviews bee outputs
5. Integrates results
6. Runs `pytest tests/test_spec_parser.py -v`
7. Reports experiment metrics to response file

---

## Experiment Metrics to Track

Q33N's response file should include:
- **CLOCK:** Total wall time (minutes) - includes coordination overhead
- **COIN:** Total cost (USD) - Q33N + all bee costs
- **CARBON:** CO2e estimate (grams)
- **Files created:** With line counts
- **Test results:** Pass/fail
- **Bee dispatch count:** How many bees used
- **Coordination overhead:** Q33N's token usage separate from bees

This allows direct comparison with Treatment A (single Opus).

---

## Files Created by This Fix

- `.deia/hive/coordination/20260409-EXP-B-BRIEFING.md` — Q33N briefing
- `.deia/hive/responses/20260409-QUEUE-TEMP-2026-04-09-2212-SPEC-fix-EXP-TREATMENT-B-Q33N-SWARM-RESPONSE.md` — Fix response
- This file — Dispatch instructions

---

## Status

✅ **FIX COMPLETE** — Ready for Q33N dispatch

**Next action:** Q88N decides whether to dispatch Q33N manually or enhance queue runner first.
