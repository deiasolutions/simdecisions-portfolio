# BRIEFING: Ship Plan Queue Feeder

**Date:** 2026-03-14
**From:** Q33NR
**To:** Q33NR (Ship Plan Manager)
**Priority:** P0

## Context

We have a 6-wave ship plan at `docs/specs/SHIP-PLAN.md` and a queue runner at `.deia/hive/scripts/queue/run_queue.py` that processes specs sequentially from `.deia/hive/queue/`.

The queue runner processes whatever is in the queue directory. YOUR job is to be the external manager that controls WHAT goes in and WHEN, following the wave order in the ship plan.

## Your Role

You are a **queue feeder**. You:

1. Read `docs/specs/SHIP-PLAN.md` to know the wave order
2. For the current wave, create spec files for each task
3. Drop them into `.deia/hive/queue/`
4. Poll until the queue drains (all specs moved to `_done/` or `_needs_review/`)
5. Move to the next wave
6. Repeat until all waves are complete

## How Spec Files Work

Each spec is a markdown file in `.deia/hive/queue/` with these sections:

```markdown
## Priority
P0

## Model Assignment
sonnet

## Objective
What the bee should do

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Constraints
- Max 500 lines per file
- TDD: tests first

## Smoke Test
- [ ] All tests pass
- [ ] No regressions
```

The queue runner parses these sections. Priority and Model Assignment are required.

## Wave Execution Rules

1. **Wave 0 first.** Nothing else starts until Wave 0 exits clean.
2. **One wave at a time.** Do not add Wave N+1 specs until Wave N is fully drained.
3. **Max 3 specs in queue at once.** Don't flood the queue. Add 3, wait for drain, add 3 more.
4. **Check `_needs_review/` after each wave.** If specs failed, report them but continue to next wave unless they're blockers.
5. **Skip items marked "Q33NR direct" or "Config" in the ship plan.** Those are manual. Only create specs for bee-dispatchable work.

## Polling Method

Check the queue directory every 60 seconds:

```python
import time
from pathlib import Path

queue_dir = Path(".deia/hive/queue")
done_dir = queue_dir / "_done"
needs_review_dir = queue_dir / "_needs_review"

# Check if all specs from current batch are processed
pending = list(queue_dir.glob("*.md"))
# Filter out MORNING-REPORT and other non-spec files
pending = [p for p in pending if "MORNING-REPORT" not in p.name]
```

When `len(pending) == 0`, the wave batch is drained. Add the next batch.

## Reporting

After each wave completes, write a wave completion report to `.deia/hive/responses/20260314-WAVE-{N}-COMPLETION.md` with:
- Which specs completed (moved to `_done/`)
- Which specs failed (moved to `_needs_review/`)
- Any blockers for the next wave

## Important

- The queue runner must be started separately. Your job is ONLY to feed specs.
- Read SHIP-PLAN.md carefully — some tasks are Q33NR-direct (you do them yourself), some are config (skip), some are bee work (create specs).
- The ship plan has estimated models per task (haiku/sonnet). Use those in the `## Model Assignment`.
- Create spec filenames like: `2026-03-14-WAVE0-01-SPEC-test-suite-fixes.md`
