# TASK-130: Ship Plan Queue Feeder

**Role:** Q33NR (regent)
**Model:** sonnet
**Priority:** P0

## Role Override
regent

## Objective

You are the Ship Plan Manager. Your job is to read `docs/specs/SHIP-PLAN.md` and feed the queue runner by creating spec files in `.deia/hive/queue/` in wave order.

## Instructions

### Step 1: Read the ship plan
Read `docs/specs/SHIP-PLAN.md` completely. Understand all 6 waves and their task order.

### Step 2: Read the briefing
Read `.deia/hive/coordination/2026-03-14-BRIEFING-ship-plan-feeder.md` for your operating rules.

### Step 3: Start with Wave 0
Wave 0 is "Clean the House." For each bee-dispatchable task in Wave 0:
- Create a spec file with proper frontmatter (Priority, Model Assignment, Objective, Acceptance Criteria, Constraints, Smoke Test)
- Write it to `.deia/hive/queue/`
- Max 3 specs at a time

Skip tasks marked as "Q33NR direct" or "Config" — those are not for bees.

For Q33NR-direct tasks in Wave 0, do them yourself:
- 0.1: Run test suites and report failures
- 0.3: Check for file conflicts from overnight bee work
- 0.5: Clean junk bug entries from DB
- 0.6: Move BL-043 from P0 to P2

### Step 4: Poll and wait
After adding specs to the queue, poll the queue directory every 60 seconds. When all specs have moved to `_done/` or `_needs_review/`, the batch is drained.

### Step 5: Proceed to next wave
Write a wave completion report, then create specs for Wave 1. Repeat for each wave.

### Step 6: Continue through all waves
Keep feeding specs wave by wave until the ship plan is complete or you run out of tasks to create.

## Acceptance Criteria
- [ ] Ship plan read and understood
- [ ] Wave 0 Q33NR-direct tasks completed (test report, conflict check, bug cleanup, BL-043 move)
- [ ] Wave 0 bee specs created and dropped in queue
- [ ] Polling loop monitors queue drain
- [ ] Wave completion reports written after each wave
- [ ] Proceeds to subsequent waves in order

## Constraints
- Max 3 specs in queue at once
- One wave at a time — do not start Wave N+1 until Wave N drains
- Skip "Config" and manual tasks
- Spec filenames: `2026-03-14-WAVE{N}-{NN}-SPEC-{description}.md`
- Use model assignments from the ship plan (haiku for small tasks, sonnet for complex)

## Smoke Test
- [ ] Queue directory receives spec files
- [ ] Specs have proper frontmatter (Priority, Model Assignment, Objective, etc.)
- [ ] Queue drains as queue runner processes specs
