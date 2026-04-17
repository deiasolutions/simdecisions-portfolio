# Fix FLAPPY-100-self-learning-v2 (Cycle 2) -- NEEDS_DAVE

**Status:** NEEDS_DAVE (unfixable via automation — role mismatch cannot be resolved by worker bees)
**Model:** Sonnet
**Date:** 2026-04-09
**Bot ID:** BEE-QUEUE-TEMP-2026-04-09-1752-SPE
**Fix Cycle:** 2 of 2 (MAX REACHED)

## Files Modified
(none — issue is systemic routing, not fixable by worker bee)

## What Was Done
- Read original spec SPEC-FLAPPY-100-self-learning-v2.md
- Read previous fix attempt response (cycle 1)
- Verified root cause analysis from cycle 1
- Confirmed v1 files exist (previous bee was correct)
- Confirmed this is fix cycle 2 of 2 (max reached per Fix Cycle Rule)

## Root Cause Confirmed

**SPEC-FLAPPY-100 requires `Role: queen` but was dispatched to worker bee.**

**Spec declares:**
```markdown
## Role
queen
```

**Worker bee (b33) cannot:**
- Orchestrate or coordinate
- Dispatch other bees (research bee, build bees)
- Create sub-specs and queue them
- Synthesize research into design docs
- Perform multi-phase coordination

**Spec requires coordination tasks:**
- Phase 1: Dispatch research bee (SPEC-FLAPPY-R01)
- Phase 2: Synthesize design doc
- Phase 3: Create and queue build specs (SPEC-FLAPPY-1XX-*)
- Phase 4: Coordinate verification across all phases

**This is a fundamental role mismatch that cannot be fixed by a worker bee.**

## Why Previous Fix Failed

Cycle 1 correctly diagnosed the issue and flagged NEEDS_DAVE. The queue runner re-dispatched to another worker bee (me) for cycle 2, but **no worker bee can fix a queen-level spec**.

## v1 Files Status (RESOLVED)

Previous bee reported v1 files as missing, but they **DO exist**:
- `browser/public/games/flappy-bird-ai-v1-20260407.html` — EXISTS (17K, verified)
- `browser/public/games/flappy-bird-v1-20260407.html` — EXISTS (13K, verified)

The "missing files" blocker was a false positive (likely path resolution issue). Files are available for research phase.

## Resolution Requires Q88N Decision

**Three options (from previous analysis):**

### Option 1: Manual Q33N Dispatch (RECOMMENDED)
Dave (Q88N) manually dispatches Q33N to handle this spec:
1. Write briefing to `.deia/hive/coordination/`
2. Dispatch Q33N via Task tool
3. Move SPEC-FLAPPY-100 to `_done/` after Q33N completes

### Option 2: Convert to Direct Build Spec
Rewrite SPEC-FLAPPY-100 to remove coordination phases:
- Make it a single "build self-learning Flappy Bird" worker spec
- Remove research/design phases (or inline into constraints)
- Single deliverable: worker bee writes entire game in one pass

### Option 3: Add Role-Based Routing to Queue Runner
Modify `.deia/hive/scripts/queue/run_queue.py`:
- Parse `Role:` field from specs
- If `Role: queen`, dispatch to Q33N via Task tool
- If `Role: worker` or missing, dispatch to worker bee
- This fixes the systemic issue for all future specs

## Why This Cannot Be Auto-Fixed

1. **Worker bees cannot coordinate** (by design, enforced in HIVE.md)
2. **Queue runner doesn't route by role** (dispatches all specs to worker bees)
3. **Q33N dispatch requires Q88N approval** (chain of command)
4. **Fix cycle 2 of 2 reached** (per Fix Cycle Rule in system prompt)

## Blockers

**CRITICAL:** This spec cannot be executed by any worker bee, regardless of how many fix cycles are attempted. The queue runner is dispatching a queen-level spec to worker bees, which is a routing misconfiguration.

**FLAGGING NEEDS_DAVE PER FIX CYCLE RULE:**
- Max 2 fix cycles per original spec (REACHED)
- After 2 failed cycles, flag NEEDS_DAVE and stop processing
- Move spec to `_needs_review/` to prevent further re-dispatch

## Test Results
(no tests run — task is routing issue, not code implementation)

## Cost Analysis
**Input tokens:** ~6,000
**Output tokens:** ~1,000
**Estimated cost:** ~$0.025

## Recommended Next Steps for Q88N

1. **Choose resolution option** (1, 2, or 3 above)
2. **Move SPEC-FLAPPY-100** to `_needs_review/` to prevent re-dispatch loop
3. **If Option 1:** Manually write Q33N briefing and dispatch
4. **If Option 2:** Rewrite spec and re-queue as worker spec
5. **If Option 3:** Upgrade queue runner to support role-based routing (long-term fix)

**This requires human decision — cannot be resolved by automated fix cycles.**
