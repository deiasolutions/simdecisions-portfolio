# TASK-GAM-B-Q33N-COORDINATE

**Task ID:** TASK-GAM-B-Q33N-COORDINATE
**Assigned To:** Q33N (Coordinator)
**From:** Q88NR
**Date:** 2026-04-09
**Model:** Sonnet
**Role:** Queen (Coordinator)

---

## Objective

Coordinate the gamification module build for Experiment Treatment B. Decompose design doc, create task files, dispatch bees, integrate results, and deliver working MVP.

---

## Briefing

Read: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\coordination\20260409-2350-BRIEFING-EXP-GAM-B-Q33N-SWARM.md`

This briefing contains full context, constraints, acceptance criteria, and suggested task decomposition.

---

## Deliverables

1. **Task files** (4-6 files)
   - Location: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\`
   - Format: `TASK-GAM-B-01.md`, `TASK-GAM-B-02.md`, etc.
   - Each must include: objective, deliverables (absolute paths), acceptance criteria, test requirements

2. **Bee dispatches**
   - Dispatch via: `python .deia/hive/scripts/dispatch/dispatch.py`
   - Track all bee IDs and costs

3. **Working gamification module**
   - Location: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\primitives\gamification\`
   - Must pass all acceptance criteria from briefing

4. **Test suite**
   - Location: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\primitives\tests\test_gamification.py`
   - Minimum 15 test cases
   - All tests must pass

5. **Response file**
   - Location: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260409-EXP-GAM-B-SWARM-RESPONSE.md`
   - Must include all 8 sections from briefing

---

## Acceptance Criteria

- [ ] All components from briefing implemented (models.py, levels.py, xp_calculator.py, badges.py, streaks.py)
- [ ] Tests pass: `pytest primitives/tests/test_gamification.py -v` shows 15+ passing
- [ ] No stubs — all functions fully implemented
- [ ] Total Python code < 800 lines (excluding tests)
- [ ] Each file < 200 lines
- [ ] `primitives/gamification/__init__.py` exports: `calculate_xp`, `calculate_level`, `check_badges`, `update_streak`
- [ ] Response file complete with all metrics (wall time, costs, bee dispatch log)

---

## Constraints

- Max 6 hours wall clock
- Max 5 bees in parallel (cost control)
- Branch: `exp/gamification-swarm` (already created)
- Commit prefix: `[EXP-GAM-B]`
- You coordinate — you do NOT write implementation code
- Bees: Sonnet for complex, Haiku for simple

---

## Workflow

1. Read briefing completely
2. Read design doc: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\queue\_stage\SPEC-GAMIFICATION-V1.md`
3. Decompose into 4-6 tasks
4. Write task files to `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\`
5. Dispatch bees via dispatch.py
6. Review bee outputs
7. Request fixes if needed (max 2 cycles)
8. Integrate results
9. Run full test suite
10. Fix integration issues (small glue only)
11. File response with metrics

---

## Success Metrics

- Wall time < 6 hours
- Total cost < $5.00
- All tests pass (15+)
- Zero stubs
- Clean integration

---

## GO

You are cleared for execution. Start with Phase 1: Decompose.

**Q88NR**
