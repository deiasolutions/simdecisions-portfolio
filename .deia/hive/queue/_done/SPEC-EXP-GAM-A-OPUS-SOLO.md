# SPEC-EXP-GAM-A-OPUS-SOLO

**Spec ID:** SPEC-EXP-GAM-A-OPUS-SOLO
**Created:** 2026-04-09
**Author:** Q88N + Mr. AI
**Type:** EXPERIMENT-BUILD
**Status:** READY
**Gate0-Exempt:** true
**Experiment:** HIVE-VS-OPUS-GAMIFICATION / Treatment A

---

## Priority

P1

## Depends On

None

## Model Assignment

opus

## Purpose

**Experiment Treatment A** — Single Opus bee receives `SPEC-GAMIFICATION-V1` (880-line design doc), self-decomposes the work, and builds a working gamification module solo. No Q33N coordination, no swarm.

This tests whether Opus's deep reasoning can match or beat a coordinated Sonnet/Haiku swarm when both start from the same ambiguous design document.

---

## Branch Setup

**FIRST ACTION — before any code:**

```bash
git checkout main
git pull origin main
git checkout -b exp/gamification-opus
```

All work happens on `exp/gamification-opus`. Do NOT merge to main.

---

## Input Document

Read this design doc completely before planning:

- `docs/specs/SPEC-GAMIFICATION-V1.md` (or use the copy in project knowledge)

This is your only input. You decide how to decompose and build.

---

## Build Target

Deliver a working gamification module at `primitives/gamification/` that implements:

### Required (MVP)

1. **XP Calculator** — `xp_calculator.py`
   - `calculate_xp(event, user_progression) -> XPEvent`
   - Base XP table from Section 3.1
   - Multipliers from Section 3.2 (streak, first-of-day, night owl, weekend)

2. **Level System** — `levels.py`
   - `calculate_level(xp) -> int`
   - Level thresholds from Section 4.1
   - `xp_to_next_level(xp) -> int`

3. **Badge Engine** — `badges.py`
   - `BadgeDefinition` dataclass
   - `check_badges(user_id, event_history) -> list[Badge]`
   - Implement at least 5 badges from Section 5

4. **Streak Tracker** — `streaks.py`
   - `update_streak(user_id, event_date) -> StreakState`
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
   - Minimum 15 test cases

### Not Required (skip for MVP)

- React components (PathMap, ProgressionWidget, etc.)
- Database migrations
- API endpoints
- Wiki page generation
- Morning report integration

---

## Acceptance Criteria

- [ ] `primitives/gamification/__init__.py` exports: `calculate_xp`, `calculate_level`, `check_badges`, `update_streak`
- [ ] `primitives/gamification/xp_calculator.py` implements full multiplier logic
- [ ] `primitives/gamification/levels.py` implements 10-level threshold table
- [ ] `primitives/gamification/badges.py` implements at least 5 badge definitions
- [ ] `primitives/gamification/streaks.py` implements consecutive-day logic
- [ ] `primitives/gamification/models.py` defines all required dataclasses
- [ ] `tests/test_gamification.py` has 15+ test cases
- [ ] All tests pass: `pytest tests/test_gamification.py -v`
- [ ] No stubs — all functions fully implemented
- [ ] Total Python lines < 800 (excluding tests)
- [ ] Each file < 200 lines

---

## Smoke Test

```bash
cd primitives/gamification
pytest ../tests/test_gamification.py -v
python -c "from primitives.gamification import calculate_xp, calculate_level; print('imports OK')"
```

---

## Constraints

- Single bee, single session — no sub-agents, no coordination layer
- Model: Opus only
- Branch: `exp/gamification-opus`
- Commit prefix: `[EXP-GAM-A]`
- Max 6 hours wall clock
- You decide the decomposition — spec does not prescribe order

---

## Experiment Metadata

```yaml
experiment_id: HIVE-VS-OPUS-GAMIFICATION
treatment: A
treatment_name: opus-solo
model: opus
coordination: none
branch: exp/gamification-opus
run_number: 1
```

---

## Response File

`.deia/hive/responses/20260409-EXP-GAM-A-OPUS-RESPONSE.md`

Report at end:
- CLOCK: wall time in minutes
- COIN: estimated cost in USD
- CARBON: estimated CO2e in grams
- Files created (with line counts)
- Test results (pass/fail counts)
- Self-decomposition plan (what order you chose and why)
- Challenges encountered

---

*SPEC-EXP-GAM-A-OPUS-SOLO — 2026-04-09*
