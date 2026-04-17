# Fix FLAPPY-100-self-learning-v2 -- NEEDS_DAVE

**Status:** NEEDS_DAVE (unfixable via automation — routing issue)
**Model:** Sonnet
**Date:** 2026-04-09
**Bot ID:** BEE-QUEUE-TEMP-2026-04-09-1749-SPE

## Files Modified
(none — issue is spec routing, not code)

## What Was Done
- Read original spec SPEC-FLAPPY-100-self-learning-v2.md
- Read bee response from first attempt (20260409-QUEUE-TEMP-SPEC-FLAPPY-100-self-learning-v2-RESPONSE.md)
- Read triage escalation history
- Diagnosed root cause: **queue routing issue, not code failure**

## Root Cause Analysis

### The Actual Problem
SPEC-FLAPPY-100 **requires Q33N coordinator role** but was **dispatched to worker bee (b33)**.

**Spec declares:**
```markdown
## Role
queen
```

**Worker bee constraints:**
- Cannot orchestrate or coordinate
- Cannot dispatch other bees
- Can only write code for assigned tasks

**Spec requires coordination tasks:**
- Dispatch research bee (SPEC-FLAPPY-R01)
- Synthesize design doc
- Create and queue build specs (SPEC-FLAPPY-1XX-*)
- Multi-phase build coordination

### Why This Happened
Queue runner does NOT route based on `Role:` field. It dispatches all specs to worker bees by default. The `Role: queen` field is **documentation only** — not enforced by the queue system.

### Secondary Issue (RESOLVED)
Spec references v1 files. Worker bee reported them as NOT FOUND, but they **DO exist**:
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\public\games\flappy-bird-ai-v1-20260407.html` — **EXISTS** (17K)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\public\games\flappy-bird-v1-20260407.html` — **EXISTS** (13K)

Worker bee likely used relative paths instead of absolute paths. Files are available for research phase.

## Resolution Options

### Option 1: Manual Q33N Dispatch (RECOMMENDED)
**Dave (Q88N) manually dispatches Q33N to handle this spec:**

1. Write briefing to `.deia/hive/coordination/20260409-FLAPPY-V2-BRIEFING.md`:
   ```markdown
   # Q33N Briefing: FLAPPY-100 Coordination

   You are coordinating SPEC-FLAPPY-100 (self-learning Flappy Bird v2).

   ## Phase 1: Locate or Skip v1
   Search for v1 files in `browser/public/games/*.html`. If not found, proceed without them.

   ## Phase 2: Dispatch Research
   Create SPEC-FLAPPY-R01 for research bee (NEAT best practices, visualization patterns).

   ## Phase 3: Design
   Synthesize research into design doc at `.deia/hive/responses/FLAPPY-V2-DESIGN-DOC.md`.

   ## Phase 4: Build Specs
   Create 5-6 build specs (game engine, NEAT engine, training loop, visualization, controls, polish).
   Queue to `.deia/hive/queue/backlog/SPEC-FLAPPY-1XX-*.md`.

   ## Phase 5: Coordinate Completion
   Write final coordination response when all build specs complete.
   ```

2. Dispatch Q33N via Task tool:
   ```
   Task(subagent_type="general-purpose", prompt="You are Q33N. Execute briefing at .deia/hive/coordination/20260409-FLAPPY-V2-BRIEFING.md")
   ```

3. Move SPEC-FLAPPY-100 to `_needs_review/` to prevent re-dispatch.

### Option 2: Convert to Direct Build Spec
**Rewrite SPEC-FLAPPY-100 as a single worker bee spec:**

Remove coordination phases, make it a direct "build self-learning Flappy Bird" task:
- Remove research phase (or inline research into constraints)
- Remove multi-phase coordination
- Single deliverable: `browser/public/games/flappy-bird-ai-v2.html`
- Worker bee writes entire game in one pass

**Pros:** Can be queued immediately
**Cons:** Loses research/design phases, higher risk of missing requirements

### Option 3: Fix Queue Router to Support Role Field
**Add role-based routing to queue runner:**

Modify `.deia/hive/scripts/queue/run_queue.py` to:
1. Parse `Role:` field from spec
2. If `Role: queen`, dispatch to Q33N via Task tool
3. If `Role: worker` or missing, dispatch to worker bee

**Pros:** Fixes systemic issue, future specs can declare roles
**Cons:** Requires queue runner changes (risky), not a quick fix

## Blockers

**CANNOT fix this via automation because:**
1. Queue runner doesn't support role-based routing
2. Worker bees cannot coordinate (by design)
3. Q33N dispatch requires human approval (Q88N decision)

**This is a design/routing issue, not a code failure.**

## Test Results
(no tests run — task is routing issue, not code)

## Cost Analysis
**Input tokens:** ~5,000
**Output tokens:** ~1,200
**Estimated cost:** ~$0.025

## Next Steps Required

**Requires Q88N (Dave) decision:**

1. **Which resolution option?**
   - Option 1: Manual Q33N dispatch (preserves multi-phase design)
   - Option 2: Convert to single worker spec (faster, less thorough)
   - Option 3: Fix queue router (long-term fix, high effort)

2. **v1 files confirmed available:**
   - Both v1 files exist and are ready for research phase
   - Path: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\public\games\`
   - No blocker on file availability

3. **Move SPEC-FLAPPY-100 to `_needs_review/`?**
   - Prevents re-dispatch while decision pending
   - Can be restored after routing fix

**Flagging NEEDS_DAVE per Fix Cycle Rule (unfixable via automation).**
