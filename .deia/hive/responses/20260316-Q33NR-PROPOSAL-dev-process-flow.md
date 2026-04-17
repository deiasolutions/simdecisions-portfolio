# Dev Process Flow: Q88N Direction → Shipped Code

**Author:** Q33NR
**Date:** 2026-03-16
**Status:** AWAITING Q88N REVIEW

---

## Overview

This documents the full development process from the moment Q88N gives direction through to shipped, tested, archived code. Two paths exist: the **manual chain** (Q33NR → Q33N → BEEs) for complex work, and the **queue runner** for batch/overnight processing. Both converge at the same quality gates.

---

## PATH A: Manual Chain (Live Session)

Used when Q88N is actively directing work in a Claude Code session.

### Step 1: Q88N Gives Direction
Q88N (Dave) tells Q33NR what needs to happen. Could be:
- "Build feature X"
- "Fix bug Y"
- "Port Z from platform"
- "Here's a spec, make it happen"

### Step 2: Q33NR Writes Briefing
Q33NR creates a briefing file in `.deia/hive/coordination/`:

```
.deia/hive/coordination/YYYY-MM-DD-BRIEFING-<short-name>.md
```

Contains:
- Objective (what)
- Context (why, from Q88N)
- File paths and code references
- Constraints (max lines, CSS rules, TDD)
- Model assignment (haiku/sonnet/opus)

### Step 3: Q33NR Dispatches Q33N
```bash
python .deia/hive/scripts/dispatch/dispatch.py \
  .deia/hive/coordination/YYYY-MM-DD-BRIEFING-<name>.md \
  --model sonnet --role queen --inject-boot
```

Q33N receives the briefing + BOOT.md + HIVE.md context.

### Step 4: Q33N Reads Codebase + Writes Task Files
Q33N:
1. Reads every file referenced in the briefing
2. Understands what exists vs. what needs building
3. Splits work into bee-sized units
4. Writes task files to `.deia/hive/tasks/`:

```
.deia/hive/tasks/YYYY-MM-DD-TASK-XXX-<short-name>.md
```

Each task file has 7 mandatory sections:
- Objective
- Context
- Files to Read First
- Deliverables (checklist)
- Test Requirements (TDD)
- Constraints
- Response Requirements (8-section template)

**Q33N STOPS HERE.** Does NOT dispatch bees. Returns task files to Q33NR for review.

### Step 5: Q33NR Reviews Task Files
Q33NR checks every task file for:
- [ ] Missing deliverables
- [ ] Stubs or vague acceptance criteria
- [ ] Hardcoded colors (must use var(--sd-*))
- [ ] Files that would exceed 500 lines
- [ ] Missing test requirements
- [ ] Imprecise file paths
- [ ] Gaps vs. the original briefing

If corrections needed → Q33NR tells Q33N what to fix → Q33N fixes → repeat.

### Step 6: Q33NR Approves → Q33N Dispatches BEEs
Q33NR says "approved, dispatch." Q33N runs:

```bash
python .deia/hive/scripts/dispatch/dispatch.py \
  .deia/hive/tasks/TASK-XXX.md \
  --model haiku --role bee --inject-boot
```

Rules:
- Independent tasks → parallel (max 5 bees)
- Dependent tasks → sequential
- Always background execution
- Always `--inject-boot` (bee gets BOOT.md rules)

### Step 7: BEEs Execute
Each bee:
1. Reads task file + referenced source files
2. Writes tests FIRST (TDD)
3. Writes code to pass tests
4. Runs all tests, fixes failures
5. Verifies no file >500 lines, no hardcoded colors
6. Writes response file to `.deia/hive/responses/`:

```
.deia/hive/responses/YYYYMMDD-TASK-XXX-RESPONSE.md
```

Response has 8 mandatory sections:
1. Header (task ID, status, model, date)
2. Files Modified (full paths)
3. What Was Done (bullet list)
4. Test Results (pass/fail counts)
5. Build Verification (output summary)
6. Acceptance Criteria (marked [x] or [ ])
7. Clock / Cost / Carbon (all three, never omit)
8. Issues / Follow-ups

### Step 8: Q33N Reviews Bee Responses
For each response:
- All 8 sections present? → if not, re-dispatch bee
- Tests pass? → if not, dispatch fix task
- Stubs shipped? → if so, re-dispatch bee
- Regressions? → if so, dispatch fix task

Q33N writes completion report, returns to Q33NR.

### Step 9: Q33NR Reviews Results → Reports to Q88N
Q33NR checks:
- All bees completed?
- Test counts match requirements?
- Any stubs or regressions?
- Response files complete?

If issues → tell Q33N to fix → repeat steps 6-8.
If clean → report to Q88N with summary.

### Step 10: Archive + Inventory
Q33N (on Q33NR direction):
1. Moves task files to `.deia/hive/tasks/_archive/`
2. Registers features: `python _tools/inventory.py add --id FE-XXX ...`
3. Exports: `python _tools/inventory.py export-md`
4. Logs bugs if any: `python _tools/inventory.py bug add ...`
5. Updates backlog: `python _tools/inventory.py backlog update ...`

---

## PATH B: Queue Runner (Batch/Overnight)

Used for batch processing when Q88N is not actively watching. Specs go through the queue runner instead of the manual Q33NR → Q33N → BEE chain.

### Queue Directory State Machine

```
_hold/ ──→ queue/ ──→ _active/ ──→ _done/
                         │
                         ├──→ _failed/ ──→ queue/ (retry)
                         │                  │
                         │                  ├──→ _dead/ (give up)
                         │                  │
                         │                  └──→ _needs_review/ (human)
                         │
                         └──→ _needs_review/ (regression)
```

| Directory | State | Who Acts |
|-----------|-------|----------|
| `_hold/` | Not yet released | Q88N/Q33NR moves to queue/ |
| `queue/` | Pending, eligible for pickup | Queue runner selects next |
| `_active/` | Bee working right now | Queue runner monitors |
| `_done/` | Completed successfully | Archive when ready |
| `_failed/` | Failed, may retry | Queue runner or human |
| `_needs_review/` | Needs human decision | Q88N/Q33NR reviews |
| `_dead/` | Permanently cancelled | No further action |

### Queue Runner Pickup Logic

```
for each spec in queue/, sorted by (priority_int, added_at):
    if hold_until is in the future → skip
    if any dependency not in _done/ → skip (BLOCKED)
    if slots available (< max_parallel) → move to _active/, dispatch bee
```

### Priority (P0–P3 integer only)

| P | Meaning | Example |
|---|---------|---------|
| P0 | Emergency hotfix | Broken production, blocking bug |
| P1 | Current wave work | Normal feature/port tasks |
| P2 | Next wave, not urgent | Staged but not blocking |
| P3 | Backlog, do when idle | Nice-to-have improvements |

Within same priority: FIFO by file modification time.

### Dependencies

Specs declare what must complete first:

```markdown
## Depends On
- w2-04-flow-des-wire
- w2-05-des-canvas-visual
```

Queue runner checks: does `_done/` contain a file with each dep ID as substring? If all satisfied → eligible. If any missing → BLOCKED (stays in queue/, logged).

After each completion, blocked specs are re-checked — a newly satisfied dependency can unblock waiting work.

### Failure Handling

| Result | Action | Retry? |
|--------|--------|--------|
| CLEAN | Move `_active/` → `_done/` | — |
| TIMEOUT | Move `_active/` → `_failed/`, generate resume spec in `queue/` | Yes, up to 2x |
| NEEDS_DAVE | Move `_active/` → `_failed/`, generate fix spec in `queue/` | Yes, up to 2x |
| Max retries | Move `_failed/` → `_needs_review/` | No, human decides |
| Regression | Move `_active/` → `_needs_review/` | No, human decides |
| Process crash | Orphan in `_active/`, recovered on restart → back to `queue/` | Yes |

### Crash Recovery

On queue runner startup:
1. Scan `_active/` for orphaned specs
2. Check each orphan's failure log (if any)
3. If retries remain → move back to `queue/`
4. If max retries exhausted → move to `_needs_review/`
5. Log: `[QUEUE] RECOVERY: spec-name.md was in-flight, moved back to queue/`

### Budget Enforcement

- Session ceiling: $20 USD (configurable in queue.yml)
- Warning at 80% consumed
- Hard stop at 100% — remaining specs stay in queue for next session
- Max 2 fix cycles per spec
- Max 50 specs per session

---

## Where Both Paths Converge

Regardless of manual chain or queue runner, the outputs are the same:

1. **Code written** with tests (TDD)
2. **Response file** in `.deia/hive/responses/` with 8 sections
3. **Task archived** to `.deia/hive/tasks/_archive/`
4. **Feature registered** in inventory DB (Railway PostgreSQL)
5. **Backlog updated** (item moved to done)
6. **FEATURE-INVENTORY.md** exported

---

## Spec Lifecycle (Upstream)

How work enters the system:

```
Q88N idea
  → Q33NR writes spec (docs/specs/SPEC-*.md)
  → Spec reviewed and approved
  → Individual queue spec created (queue/*.md) with:
      - Priority (P0–P3)
      - Depends On (optional)
      - Objective, Acceptance Criteria, Model Assignment
      - Smoke Test, Constraints
  → Enters queue runner pipeline (Path B)
  OR
  → Q33NR writes briefing for manual chain (Path A)
```

### Backlog → Queue Connection

Backlog items (in inventory DB) track:
- `kanban_column`: icebox → backlog → in_progress → review → done
- `stage`: SPEC → IR → VAL → BUILD → TEST
- `stage_status`: pending → active → done / failed / blocked

When a backlog item reaches `stage=BUILD, stage_status=active`, a queue spec should exist for it. On completion, the backlog item advances to `stage=TEST` then `done`.

---

## Quality Gates (From P-04 Build Integrity)

Every piece of work passes through:

1. **Gate 1: Spec Validation** — spec has all required sections, model assigned, acceptance criteria concrete
2. **Gate 2: Pre-dispatch Baseline** — capture current test counts before bee runs
3. **Gate 3: Post-dispatch Verification** — compare test counts after bee, flag regressions
4. **Gate 4: Response Review** — all 8 sections present, no stubs, tests pass
5. **Gate 5: Archive** — feature registered, inventory updated, backlog closed

---

## Roles Summary

| Role | Does | Never Does |
|------|------|-----------|
| **Q88N** | Sets direction, approves results, approves git ops | Writes code, dispatches |
| **Q33NR** | Writes briefings, reviews tasks, reviews results, reports to Q88N | Writes code, dispatches bees, runs git write ops without approval |
| **Q33N** | Writes task files, dispatches bees (after approval), reviews responses, archives | Writes code (unless approved), talks to Q88N, dispatches before review |
| **BEE** | Writes code, runs tests, writes response | Dispatches other bees, modifies files outside scope, runs inventory CLI |
