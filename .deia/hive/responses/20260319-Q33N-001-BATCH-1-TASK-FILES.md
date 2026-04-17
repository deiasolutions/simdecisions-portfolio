# Q33N-001: Batch 1 Task Files — COMPLETE

**Status:** COMPLETE
**Model:** Sonnet 4.5
**Date:** 2026-03-19

---

## Task Files Created

I have written 3 task files for Batch 1 (backend-first, low-risk items):

1. **TASK-BL203**: Split Heartbeat into Liveness Ping + State Transition Log
   - File: `.deia/hive/tasks/2026-03-19-TASK-BL203-SPLIT-HEARTBEAT.md`
   - Model: haiku
   - Priority: P0
   - Scope: Pure backend (build_monitor.py + run_queue.py)
   - Risk: LOW — isolated changes, no browser/ files touched

2. **TASK-243**: Global Commons Phase A — Static Content Documentation
   - File: `.deia/hive/tasks/2026-03-19-TASK-243-GLOBAL-COMMONS-PHASE-A.md`
   - Model: sonnet
   - Priority: P2
   - Scope: Documentation only (new files in docs/global-commons/)
   - Risk: ZERO — no code changes, only documentation

3. **TASK-228**: DES Pipeline Runner for Build Pipeline Simulation
   - File: `.deia/hive/tasks/2026-03-19-TASK-228-DES-PIPELINE-RUNNER.md`
   - Model: sonnet
   - Priority: P1
   - Scope: New backend route (pipeline_sim.py + tests)
   - Risk: LOW — dependencies satisfied, follows existing pattern

---

## Why These 3 Tasks for Batch 1

**Backend-first strategy:** All three tasks are backend or documentation — zero browser/ modifications. This reduces risk of breaking the stable browser/ code recovered on March 19.

**Dependencies satisfied:**
- TASK-228 depends on TASK-225 (inmemory_store.py ✓ exists) and TASK-226 (pipeline.ir.json ✓ exists)
- TASK-243 has no code dependencies (reads config files only)
- BL-203 has no dependencies

**Isolated scope:**
- Each task modifies maximum 3 files (per briefing constraint)
- Each task has explicit "Files You May Modify" and "Files You Must NOT Modify" sections
- No cross-primitive modifications
- No browser/ files touched

**Skipped items:**
- BL-070 (envelope handlers) — This is a BROWSER task (touches terminal/, relay_bus/), not backend. Moved to future batch.
- BL-110 (status system alignment) — Complex cross-layer task (touches backend + browser + kanban). Too risky for Batch 1. Moved to future batch.

---

## Task File Quality Checklist

Each task file includes:
- ✅ Explicit "Files You May Modify" section (absolute paths)
- ✅ Explicit "Files You Must NOT Modify" section
- ✅ Maximum 3 source files modified per task
- ✅ Test requirements (TDD, minimum test count)
- ✅ Build verification commands (absolute paths)
- ✅ No stubs allowed
- ✅ 8-section response template requirement
- ✅ Model assignment (haiku or sonnet)
- ✅ Priority level

---

## Batch 1 Dispatch Order Recommendation

**Sequential execution recommended:**

1. **TASK-243** (Global Commons docs) — Zero code risk, can run first
2. **BL-203** (Heartbeat split) — Backend only, no dependencies
3. **TASK-228** (DES pipeline runner) — Backend only, all dependencies satisfied

**Rationale:** Run lowest-risk first (docs), then isolated backend features. If any task fails, it won't block the others.

---

## Next Steps

**Waiting for Q33NR review:**
1. Review task file quality (file boundaries, test requirements, acceptance criteria)
2. Approve or request corrections
3. If approved, authorize dispatch

**After Batch 1 completes:**
- Review bee response files (all 8 sections present?)
- Verify tests pass
- Check for stubs/regressions
- Plan Batch 2 (next 3-5 items from remaining 17)

---

## Remaining Items for Future Batches

**Backend (2 remaining):**
- BL-110 (status system alignment) — complex cross-layer, needs careful planning

**Browser UI Polish (6 remaining):**
- TASK-230 (terminal command history)
- TASK-231 (seamless pane borders)
- TASK-232 (expandable terminal input)
- TASK-235 (loading states)
- BL-023 (shell swap/merge)
- BL-208 (app directory sort order)
- BL-209 (processing primitive layout)

**Browser Canvas/Bugs (8 remaining):**
- BL-070 (envelope handlers) — moved from Batch 1
- BUG-015 (drag pane into stage)
- BUG-018 (canvas IR wrong pane)
- BUG-019 (canvas drag captured)
- BUG-020 (canvas IR terminal hides response)
- BUG-025 (sim EGG failures)
- BUG-027 (turtle draw unregistered)
- BUG-028 (efemera channels not wired)
- BUG-029 (stage app add warning)
- BUG-031 (code explorer click error)

**Infra/Auth (6 remaining):**
- TASK-239 (efemera EGG verified)
- TASK-240 (keyboard shortcuts)
- TASK-241 (production URL smoke test)
- TASK-242 (full smoke test suite)
- TASK-244 (landing page)
- TASK-245 (ra96it signup flow)

---

## File Boundary Enforcement

All three task files enforce strict file boundaries:

**TASK-BL203:**
- ✅ May modify: `build_monitor.py`, `run_queue.py`, `test_build_monitor_integration.py`
- ❌ Must NOT modify: Any browser/, engine/, other routes, database schemas

**TASK-243:**
- ✅ May create: 6 new files in `docs/global-commons/`
- ❌ Must NOT modify: Any existing docs/, any browser/, hivenode/, engine/, config files

**TASK-228:**
- ✅ May modify: `pipeline_sim.py` (new), `__init__.py`, `test_pipeline_sim.py` (new)
- ❌ Must NOT modify: Any browser/, engine/ (read only), queue scripts, other routes

---

**Q33N-001 awaiting Q33NR review and dispatch authorization.**
