# Q33N Task Files Summary — Canvas Full Port

**Date:** 2026-03-23
**From:** Q33N (Coordinator)
**To:** Q33NR (Regent)
**Briefing:** 2026-03-23-BRIEFING-CANVAS-FULL-PORT.md

## Summary

I have broken down the Canvas Full Port briefing into **9 bee-sized task files** covering all 5 tiers. All task files are written and ready for your review.

## Task Files Created

### TIER 1 — Core Pipeline (1 task)
1. **TASK-CANVAS-001: Wire Terminal → IR → Canvas Pipeline**
   - File: `.deia/hive/tasks/2026-03-23-TASK-CANVAS-001-IR-PIPELINE.md`
   - Scope: Add bus subscription for `terminal:ir-deposit`, parse PHASE-IR, add nodes to canvas
   - Model: Sonnet (requires understanding full pipeline + bus routing)
   - Est. effort: Medium (needs IR parser, bus integration, intelligent positioning)

### TIER 2 — Missing Node Types (2 tasks)
2. **TASK-CANVAS-002: Port Process Flow Nodes (Split, Join, Queue)**
   - File: `.deia/hive/tasks/2026-03-23-TASK-CANVAS-002-PROCESS-FLOW-NODES.md`
   - Scope: Port 3 node types from old platform, register in canvas, add to palette
   - Model: Sonnet (porting work, requires reading old code)
   - Est. effort: Medium (3 nodes × ~150 lines each = ~450 lines + tests)

3. **TASK-CANVAS-003: Port All 7 Annotation Node Types**
   - File: `.deia/hive/tasks/2026-03-23-TASK-CANVAS-003-ANNOTATION-NODES.md`
   - Scope: Port 7 annotation nodes (Line, Image, Text, Rect, Ellipse, Callout, Sticky)
   - Model: Sonnet (porting work, some are complex like AnnotationLine)
   - Est. effort: Large (7 nodes × ~120 lines each = ~840 lines + tests)

### TIER 3 — Missing Modes (2 tasks)
4. **TASK-CANVAS-004: Port Configure Mode**
   - File: `.deia/hive/tasks/2026-03-23-TASK-CANVAS-004-CONFIGURE-MODE.md`
   - Scope: Port ConfigureView (validation panel + sim config + read-only canvas)
   - Model: Sonnet (requires understanding mode engine + validation logic)
   - Est. effort: Medium (~200 lines mode file + integration)

5. **TASK-CANVAS-005: Port Optimize Mode**
   - File: `.deia/hive/tasks/2026-03-23-TASK-CANVAS-005-OPTIMIZE-MODE.md`
   - Scope: Port OptimizeView (parameter sweep + Pareto viz + backend API)
   - Model: Sonnet (complex, may need backend API implementation)
   - Est. effort: Large (~500 lines UI + backend API + Pareto chart)

### TIER 4 — Wire Shell Modes to Backends (3 tasks)
6. **TASK-CANVAS-006: Wire Playback Mode to Backend API**
   - File: `.deia/hive/tasks/2026-03-23-TASK-CANVAS-006-PLAYBACK-BACKEND.md`
   - Scope: Backend API for playback events, SQLite table, frontend integration
   - Model: Sonnet (backend + frontend integration)
   - Est. effort: Medium (backend routes + table + frontend wiring)

7. **TASK-CANVAS-007: Wire Tabletop Mode to Backend API**
   - File: `.deia/hive/tasks/2026-03-23-TASK-CANVAS-007-TABLETOP-BACKEND.md`
   - Scope: Backend API for tabletop sessions, graph walker logic, frontend integration
   - Model: Sonnet (requires porting graph walk logic to Python)
   - Est. effort: Medium-Large (backend routes + graph walker + frontend wiring)

8. **TASK-CANVAS-008: Wire Compare Mode to Backend API**
   - File: `.deia/hive/tasks/2026-03-23-TASK-CANVAS-008-COMPARE-BACKEND.md`
   - Scope: Backend API for diff computation + snapshot storage, frontend integration
   - Model: Sonnet (diff logic porting decision)
   - Est. effort: Medium (backend routes + snapshot storage + frontend wiring)

### TIER 5 — Missing Features (1 mega-task)
9. **TASK-CANVAS-009: Port Missing Features (Lasso, BroadcastChannel, Smart Handles, Properties)**
   - File: `.deia/hive/tasks/2026-03-23-TASK-CANVAS-009-LASSO-AND-FEATURES.md`
   - Scope: 4 features — (1) Lasso selection, (2) BroadcastChannel sync, (3) Smart edge handles, (4) 6 missing property tabs
   - Model: Sonnet (multi-feature port, some complex like BroadcastChannel)
   - Est. effort: Large (4 distinct features, ~800 lines total)

## Total Breakdown

- **Tasks:** 9
- **Model:** All Sonnet (porting work requires reading + understanding old code)
- **Est. total lines:** ~3,500 lines of new code + ~1,500 lines of tests = ~5,000 lines
- **Dependencies:**
  - TASK-001 (IR pipeline) has no blockers — can start immediately
  - TASK-002, TASK-003 (node types) can run in parallel with TASK-001
  - TASK-004, TASK-005 (modes) can run after node types exist (may reference new nodes)
  - TASK-006, TASK-007, TASK-008 (backend wiring) can run after modes exist
  - TASK-009 (features) can run in parallel with TASK-004/005/006/007/008

## Dispatch Strategy

### Option A: Serial (low parallelism, safer)
1. Dispatch TASK-001 (IR pipeline) → wait for completion
2. Dispatch TASK-002 + TASK-003 (node types) in parallel → wait
3. Dispatch TASK-004 + TASK-005 (modes) in parallel → wait
4. Dispatch TASK-006 + TASK-007 + TASK-008 (backends) in parallel → wait
5. Dispatch TASK-009 (features) → wait

**Timeline:** ~5-6 sequential batches, ~8-12 hours total (assuming 1-2 hours per task)

### Option B: Parallel (high parallelism, faster but riskier)
1. Dispatch TASK-001, TASK-002, TASK-003 in parallel (all independent) → wait
2. Dispatch TASK-004, TASK-005, TASK-006, TASK-007, TASK-008 in parallel → wait
3. Dispatch TASK-009 → wait

**Timeline:** ~3 sequential batches, ~4-6 hours total

### Option C: Hybrid (recommended)
1. Dispatch TASK-001 + TASK-002 in parallel → wait
2. Dispatch TASK-003 + TASK-004 in parallel → wait
3. Dispatch TASK-005 + TASK-006 + TASK-007 in parallel → wait
4. Dispatch TASK-008 + TASK-009 in parallel → wait

**Timeline:** ~4 sequential batches, ~6-8 hours total

## Cost Estimate

- **Model:** Sonnet 4.5 ($3 per 1M input tokens, $15 per 1M output tokens)
- **Est. input per task:** ~50K tokens (reading old code + new code + tests) × 9 tasks = 450K tokens
- **Est. output per task:** ~20K tokens (writing code + tests + response) × 9 tasks = 180K tokens
- **Cost:** (450K × $3/1M) + (180K × $15/1M) = $1.35 + $2.70 = **~$4.05 total**
- **Clock:** ~8-12 hours (depends on dispatch strategy)
- **Carbon:** ~120g CO2e (Sonnet 4.5, 9 tasks)

## Review Checklist for Q33NR

Please review each task file for:
- [ ] Missing deliverables vs briefing
- [ ] Stubs or vague acceptance criteria
- [ ] Hardcoded colors mentioned
- [ ] Files that would exceed 500 lines
- [ ] Missing test requirements
- [ ] Imprecise file paths (all paths are absolute)
- [ ] Gaps vs the briefing requirements

If corrections needed, I will revise and return for re-review.

## Notes

- All tasks include mandatory 8-section response file requirements
- All tasks specify TDD (tests first)
- All tasks specify no hardcoded colors, no files over 500 lines, no stubs
- All tasks reference old platform source files for porting
- TASK-003 (7 annotation nodes) and TASK-009 (4 features) are the largest tasks — consider splitting if too large
- TASK-005 (Optimize mode) may require backend API implementation — flagged in task as decision point
- TASK-007 (Tabletop backend) requires porting graph walker logic to Python — most complex backend task

## Questions for Q33NR

1. **Parallelism preference:** Option A (serial), Option B (parallel), or Option C (hybrid)?
2. **TASK-003 size:** 7 annotation nodes in one task is large. Split into 2 bees (4 + 3 nodes)?
3. **TASK-009 size:** 4 features in one task is large. Split into 2-3 bees (lasso+broadcast, handles+properties)?
4. **Optimize mode backend:** Should bee implement full backend API or client-side multi-run? Task flags this as decision.

Awaiting your review and approval to dispatch.

---

**Q33N (Coordinator)**
Bot ID: QUEEN-2026-03-23-BRIEFING-CANVAS-FULL-PORT
