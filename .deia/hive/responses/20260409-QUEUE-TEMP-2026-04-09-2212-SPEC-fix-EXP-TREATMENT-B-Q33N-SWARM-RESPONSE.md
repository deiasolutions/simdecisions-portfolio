# QUEUE-TEMP-2026-04-09-2212-SPEC-fix-EXP-TREATMENT-B-Q33N-SWARM -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-04-09

## Files Modified

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\coordination\20260409-EXP-B-BRIEFING.md` (created, 147 lines)

## What Was Done

**Root Cause Analysis:**

The original SPEC-EXP-TREATMENT-B-Q33N-SWARM was dispatched directly to a worker bee, but the spec contains explicit Q33N coordinator instructions. This caused a role conflict:

1. Dispatch role injection: "You are **b33 (worker bee)**"
2. Spec content: "## Q33N Instructions - You are the coordinator"

The bee correctly refused to proceed, citing Rule 7 (STAY IN YOUR LANE).

**Fix Applied:**

Created a proper briefing file for Q33N coordination:
- File: `.deia/hive/coordination/20260409-EXP-B-BRIEFING.md`
- Contains Q33N-specific instructions to coordinate the spec parser build
- Explicitly states: "DO NOT write code yourself. You coordinate bees who write code."
- Includes all acceptance criteria and experiment metrics

**Next Steps Required:**

This spec needs to be dispatched to Q33N with the `--role queen` flag, not directly to a bee:

```bash
python .deia/hive/scripts/dispatch/dispatch.py \
  .deia/hive/coordination/20260409-EXP-B-BRIEFING.md \
  --role queen \
  --model sonnet \
  --inject-boot
```

Q33N will then:
1. Decompose the work into 2-3 bee tasks
2. Dispatch Sonnet bees to execute each task
3. Integrate results
4. Report experiment metrics

## Architectural Note

The queue runner currently treats all specs uniformly - it dispatches them as worker bee tasks. Specs that require Q33N coordination need explicit routing logic or a different queue pathway.

**Recommendation:** Add a frontmatter field to specs like `Coordinator: Q33N` to signal routing needs, or create a separate `queue/coordination/` directory that triggers Q33N dispatch instead of direct bee dispatch.

## Tests Run

None - this is a dispatch configuration fix, not a code change.

## Blockers

None. Briefing file created and ready for Q33N dispatch.

## Notes

The experiment design is sound - Treatment A (single Opus) vs Treatment B (Q33N swarm) will generate valuable comparison data. The issue was purely in the dispatch routing.

The briefing file is complete and Q33N-ready. It includes:
- Clear coordinator role assignment
- Decomposition guidance (2-3 tasks)
- All acceptance criteria from original spec
- Experiment metrics requirements
- Smoke test commands
- Cost/time tracking requirements

**Awaiting Q88N decision on how to proceed with Q33N dispatch.**
