# BRIEFING: EXP-GAM-B-Q33N-SWARM

**To:** Q33N (Coordinator)
**From:** Q88NR (Regent)
**Date:** 2026-04-09 23:50
**Spec:** SPEC-EXP-GAM-B-Q33N-SWARM
**Treatment:** Experiment B — Q33N Swarm

---

## Mission

You are the coordinator for **Experiment Treatment B**. Your mission: decompose the gamification design doc into task files, dispatch a swarm of Sonnet/Haiku bees, and deliver a working gamification module.

This is being compared to **Treatment A** (single Opus model). You need to demonstrate that coordinated swarm intelligence can match or beat single-model performance.

---

## Context

**Input document:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\queue\_stage\SPEC-GAMIFICATION-V1.md` (882 lines)

This is an ambiguous design doc describing a gamification system. Your job is to turn it into working code.

---

## Build Target

Deliver a working gamification module at `primitives/gamification/` with:

### Required Components (MVP)

1. **XP Calculator** — `xp_calculator.py`
   - Function: `calculate_xp(event, user_progression) -> XPEvent`
   - Base XP table from Section 3.1
   - Multipliers from Section 3.2 (streak, first-of-day, night owl, weekend)

2. **Level System** — `levels.py`
   - Function: `calculate_level(xp) -> int`
   - Level thresholds from Section 4.1 (10 levels: 0 → 26,000 XP)
   - Function: `xp_to_next_level(xp) -> int`

3. **Badge Engine** — `badges.py`
   - `BadgeDefinition` dataclass
   - Function: `check_badges(user_id, event_history) -> list[Badge]`
   - Implement at least 5 badges from Section 5

4. **Streak Tracker** — `streaks.py`
   - Function: `update_streak(user_id, event_date) -> StreakState`
   - Consecutive day logic from Section 10.2

5. **Data Models** — `models.py`
   - `UserProgression` dataclass
   - `XPEvent` dataclass
   - `BadgeAward` dataclass

6. **Tests** — `tests/test_gamification.py`
   - Test XP calculation with multipliers
   - Test level thresholds
   - Test streak increment/reset
   - Test badge award logic
   - **Minimum 15 test cases**

### Not Required (skip for MVP)

- React components
- Database migrations
- API endpoints
- Wiki page generation
- Morning report integration

---

## Your Workflow

### Phase 1: Decompose (15-30 min)

1. **Read the design doc completely**
   - Path: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\queue\_stage\SPEC-GAMIFICATION-V1.md`

2. **Identify buildable units**
   - Aim for 4-6 task files
   - Each task should be independently buildable

3. **Decide bee assignments**
   - **Haiku** for simple, well-defined units (models, level thresholds, simple calculations)
   - **Sonnet** for complex logic (XP calculator with multipliers, badge engine, tests)

4. **Write task files**
   - Save to: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\`
   - Format: `TASK-GAM-B-01.md`, `TASK-GAM-B-02.md`, etc.
   - Each task file must include:
     - Objective
     - Deliverables (absolute file paths)
     - Acceptance criteria
     - Test requirements
     - Constraints (file size < 200 lines per file)

### Phase 2: Dispatch

5. **Dispatch bees via dispatch.py**
   ```bash
   python .deia/hive/scripts/dispatch/dispatch.py \
     --task TASK-GAM-B-01 \
     --model haiku \
     --bot-id BEE-GAM-B-01
   ```
   - Bees may run in parallel if no dependencies
   - Max 5 bees in parallel (cost control)

### Phase 3: Integrate (30-60 min)

6. **Review each bee's output**
   - Check response files in `.deia/hive/responses/`
   - Verify acceptance criteria met

7. **Request fixes if needed**
   - Create fix task if acceptance criteria not met
   - Max 2 fix cycles per task

8. **Integrate all pieces**
   - Ensure `primitives/gamification/__init__.py` exports all required functions
   - Ensure all files work together

9. **Run full test suite**
   ```bash
   pytest primitives/tests/test_gamification.py -v
   ```

10. **Fix integration issues**
    - You may code small glue (imports, exports, wiring)
    - NO full implementations — delegate to bees

### Phase 4: Report

11. **File response**
    - Path: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260409-EXP-GAM-B-SWARM-RESPONSE.md`
    - Include all metrics (see below)

---

## Suggested Task Decomposition

(You may deviate based on judgment)

| Task | Bee | Description | Est Lines |
|------|-----|-------------|-----------|
| TASK-GAM-B-01 | Haiku | `models.py` — dataclasses only | ~50 |
| TASK-GAM-B-02 | Haiku | `levels.py` — threshold table + calculation | ~40 |
| TASK-GAM-B-03 | Sonnet | `xp_calculator.py` — full multiplier logic | ~120 |
| TASK-GAM-B-04 | Sonnet | `badges.py` — engine + 5 badge definitions | ~150 |
| TASK-GAM-B-05 | Sonnet | `streaks.py` — consecutive day logic | ~60 |
| TASK-GAM-B-06 | Sonnet | `tests/test_gamification.py` — 15+ tests | ~200 |

**Total estimated code:** ~420 lines (excluding tests)

---

## Acceptance Criteria (from spec)

- [ ] `primitives/gamification/__init__.py` exports: `calculate_xp`, `calculate_level`, `check_badges`, `update_streak`
- [ ] `primitives/gamification/xp_calculator.py` implements full multiplier logic
- [ ] `primitives/gamification/levels.py` implements 10-level threshold table
- [ ] `primitives/gamification/badges.py` implements at least 5 badge definitions
- [ ] `primitives/gamification/streaks.py` implements consecutive-day logic
- [ ] `primitives/gamification/models.py` defines all required dataclasses
- [ ] `primitives/tests/test_gamification.py` has 15+ test cases
- [ ] All tests pass: `pytest primitives/tests/test_gamification.py -v`
- [ ] No stubs — all functions fully implemented
- [ ] Total Python lines < 800 (excluding tests)
- [ ] Each file < 200 lines

---

## Constraints

- **Q33N coordinates, bees execute** — you do NOT write implementation code
- **Bees:** Sonnet for complex tasks, Haiku for simple tasks
- **Branch:** `exp/gamification-swarm` (already created)
- **Commit prefix:** `[EXP-GAM-B]`
- **Max 6 hours wall clock** (including coordination overhead)
- **You decide final decomposition** — the suggested breakdown is just guidance

---

## Response File Requirements

File: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260409-EXP-GAM-B-SWARM-RESPONSE.md`

Must include:

### Section 1: Summary
- Status: COMPLETE | FAILED (reason)
- Wall time in minutes (total, including coordination)
- Total cost in USD (Q33N + all bees, itemized)
- Test results (pass/fail counts)

### Section 2: Files Created
- List all files with absolute paths and line counts
- Total lines of code (excluding tests)

### Section 3: Bee Dispatch Log

| Task ID | Bee Model | Duration (min) | Cost (USD) | Status |
|---------|-----------|----------------|------------|--------|
| TASK-GAM-B-01 | haiku | ... | ... | PASS/FAIL |
| ... | ... | ... | ... | ... |

### Section 4: Coordination Metrics
- Q33N tokens used (input + output)
- Q33N cost estimate
- Number of task files created
- Number of rework cycles needed

### Section 5: Test Results
```
PASSED: 15/15
FAILED: 0/15
```

### Section 6: Integration Issues
- List any integration problems encountered
- How they were resolved

### Section 7: Experiment Metadata
```yaml
experiment_id: HIVE-VS-OPUS-GAMIFICATION
treatment: B
treatment_name: q33n-swarm
coordinator_model: sonnet
bee_models: [sonnet, haiku]
coordination: q33n
branch: exp/gamification-swarm
run_number: 1
wall_time_minutes: ...
total_cost_usd: ...
```

### Section 8: Observations
- What worked well
- What didn't work
- Coordination overhead insights
- Comparison insights (if any)

---

## Key Design Details (from design doc)

### XP Base Values (Section 3.1)

```python
XP_TABLE = {
    'TASK_APPROVED': 10,
    'TASK_REJECTED': 5,
    'TASK_COMPLETED': 25,
    'TASK_DISPATCHED': 2,
    'PAGE_CREATED': 15,
    'PAGE_UPDATED': 5,
    'PAGE_LINKED': 5,
    'NOTEBOOK_RUN': 2,
    'NOTEBOOK_EXPORTED': 10,
    'EGG_PACKED': 25,
    'EGG_INFLATED': 5,
    'REVIEW_COMPLETED': 15,
    'BUG_CAUGHT': 50,
    'SPEC_WRITTEN': 30,
    'SPEC_SHIPPED': 100,
    'DEPLOY_COMPLETED': 20,
    'ROLLBACK_EXECUTED': 10,
    'UNDER_BUDGET_CLOCK': 15,
    'UNDER_BUDGET_COIN': 15,
    'UNDER_BUDGET_CARBON': 15,
}
```

### Multipliers (Section 3.2)

| Condition | Multiplier | Stacks |
|-----------|------------|--------|
| First action of the day | 2.0x | No |
| Streak active (3+ days) | 1.25x | Yes |
| Streak active (7+ days) | 1.5x | Yes |
| Streak active (30+ days) | 2.0x | Yes |
| Night shift (10pm-6am) | 1.25x | Yes |
| Weekend | 1.1x | Yes |

### Level Thresholds (Section 4.1)

```python
LEVEL_THRESHOLDS = [0, 100, 400, 1000, 2000, 3500, 6000, 10000, 16000, 26000]
```

### Minimum 5 Badges Required

Examples from Section 5:
- `first_blood`: First task approved (+25 XP)
- `streak_3`: 3-day streak (+25 XP)
- `streak_7`: 7-day streak (+50 XP)
- `tasks_10`: 10 tasks approved (+25 XP)
- `wiki_10`: 10 wiki pages (+50 XP)

---

## Success Criteria

This experiment succeeds if:

1. **All acceptance criteria met** (see checklist above)
2. **All tests pass** (15+)
3. **Total cost < $5.00** (for comparison with Treatment A)
4. **Wall time < 6 hours**
5. **No stubs** — everything fully implemented

---

## Questions?

If you need clarification:
- Read the design doc completely first
- Check sections 3, 4, 5 for XP rules, levels, badges
- If still unclear, make a reasonable judgment call and document it

---

## GO

You are cleared for dispatch. Begin Phase 1: Decompose.

**Q88NR**
