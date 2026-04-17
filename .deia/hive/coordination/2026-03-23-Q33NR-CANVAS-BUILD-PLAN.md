# Q33NR Canvas Build Plan — Full Execution Runbook

**Date:** 2026-03-23
**Session:** Canvas Full Port (14 bees, 3 waves)
**Status:** Wave 1 dispatched, Waves 2+3 briefed

---

## What We're Building

Full canvas capability port from old platform (simdecisions-2) to shiftcenter. The overnight research audit (11 bees, BEE-R00 through R10) revealed:
- 2 missing modes (Configure, Optimize)
- 10 missing node types (7 annotation + split/join/queue)
- 3 shell modes (Playback, Tabletop, Compare — UI only, no backend)
- No auto-layout (old had dagre, we need ELK)
- No LLM → IR → Canvas pipeline (the core use case)
- All floating panels built as custom absolute-positioned divs instead of shell panes

**Audit reports:**
- `.deia/hive/coordination/2026-03-23-CANVAS-COMPARISON-REPORT.md` (final comparison)
- `.deia/hive/responses/20260323-TASK-BEE-CA1-RESPONSE.md` (old platform)
- `.deia/hive/responses/20260323-TASK-BEE-CA2-RESPONSE.md` (new shiftcenter)

---

## Wave 1 — Foundation (6 bees, DISPATCHED)

**Briefing:** None (I dispatched directly — violation, noted, won't repeat)

| Bee ID | Task | What | Background ID |
|--------|------|------|---------------|
| — | CANVAS-000 | Convert floating panels to shell panes | ba9c6c1 |
| — | CANVAS-001 | LLM → IR → Canvas pipeline | b55d000 |
| — | CANVAS-002 | Port Split/Join/Queue nodes | bf9e1ec |
| — | CANVAS-003A | Basic annotation nodes (text, rect, ellipse, sticky) | b5bd78c |
| — | CANVAS-003B | Rich annotation nodes (line, image, callout) | bd1044b |
| — | CANVAS-010 | ELK auto-layout (replacing dagre) | b4f4821 |

### When Wave 1 bees return, Q33NR must:

1. Read each response file in `.deia/hive/responses/`:
   - `20260323-TASK-CANVAS-000-RESPONSE.md`
   - `20260323-TASK-CANVAS-001-RESPONSE.md`
   - `20260323-TASK-CANVAS-002-RESPONSE.md`
   - `20260323-TASK-CANVAS-003A-RESPONSE.md`
   - `20260323-TASK-CANVAS-003B-RESPONSE.md`
   - `20260323-TASK-CANVAS-010-RESPONSE.md`

2. Check for:
   - All 8 response sections present?
   - Tests pass?
   - Stubs shipped?
   - File conflicts (FlowCanvas.tsx, types.ts, NodePalette.tsx, canvas.egg.md all touched by multiple bees)?

3. If conflicts exist: dispatch a merge/fix bee before Wave 2.

4. If all clean: dispatch Q33N with Wave 2 briefing.

---

## Wave 2 — Modes + Features (5 bees, BRIEFED)

**Briefing:** `.deia/hive/coordination/2026-03-23-BRIEFING-CANVAS-WAVE-2.md`

| Task | What | Depends On |
|------|------|------------|
| CANVAS-004 | Port Configure mode | CANVAS-000 (pane architecture) |
| CANVAS-005 | Port Optimize mode | CANVAS-000 (pane architecture) |
| CANVAS-009A | Lasso selection + BroadcastChannel sync | Nothing |
| CANVAS-009B | Smart edge handles | Nothing |
| CANVAS-009C | 6 missing property tabs | CANVAS-002 (new node types) |

### Dispatch procedure:

1. **Dispatch Q33N** with Wave 2 briefing (NOT bees directly):
   ```
   python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/coordination/2026-03-23-BRIEFING-CANVAS-WAVE-2.md --model sonnet --role queen --inject-boot
   ```

2. Q33N reads Wave 1 responses, verifies dependencies are met, then dispatches 5 bees.

3. Q33NR reviews results when Q33N reports back.

### Wave 2 risk flags:
- CANVAS-005 (Optimize) was flagged as potentially too large — watch for partial completion
- CANVAS-009C (property tabs, 6 tabs in one bee) is aggressive — may need a fix task
- Multiple bees edit canvas.egg.md — conflict risk

---

## Wave 3 — Backend Wiring (3 bees, BRIEFED)

**Briefing:** `.deia/hive/coordination/2026-03-23-BRIEFING-CANVAS-WAVE-3.md`

| Task | What | Depends On |
|------|------|------------|
| CANVAS-006 | Playback backend + pane adapter | CANVAS-000 |
| CANVAS-007 | Tabletop backend + pane adapter | CANVAS-000 |
| CANVAS-008 | Compare backend + pane adapter | CANVAS-000 |

### Dispatch procedure:

1. **Dispatch Q33N** with Wave 3 briefing (NOT bees directly):
   ```
   python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/coordination/2026-03-23-BRIEFING-CANVAS-WAVE-3.md --model sonnet --role queen --inject-boot
   ```

2. Q33N reads Wave 1+2 responses, verifies pane architecture is solid, then dispatches 3 bees.

3. Q33NR reviews final results.

### Wave 3 risk flags:
- All 3 add routes to `hivenode/routes/__init__.py` — merge conflict risk
- All 3 add pane layouts to `canvas.egg.md` — merge conflict risk
- If CANVAS-000 pane architecture had issues, all 3 will fail the same way

---

## Post-Build Verification (After All 3 Waves)

### Run full test suites:
```bash
cd browser && npx vitest run src/apps/sim/
cd hivenode && python -m pytest tests/ -v
```

### Verify end-to-end functionality:
- [ ] Design mode: drag nodes from palette, edit properties, undo/redo
- [ ] Configure mode: validation pane (left), sim config pane (right), read-only canvas
- [ ] Simulate mode: backend DES run, progress pane, results pane — all as shell panes
- [ ] Playback mode: backend replay, playback controls pane
- [ ] Tabletop mode: backend session, chat pane, graph walk
- [ ] Compare mode: backend diff, dual canvas panes, snapshot storage
- [ ] Optimize mode: parameter sweep, Pareto chart, results pane
- [ ] IR pipeline: terminal command → LLM → IR → nodes appear on canvas
- [ ] ELK layout: toolbar button auto-arranges (click=TB, shift+click=LR)
- [ ] All 16 node types: 9 process + 7 annotation
- [ ] Lasso selection, BroadcastChannel sync, smart handles
- [ ] 12 property tabs total (6 existing + 6 new)

### Report to Q88N:
- Total bees: 14
- Total waves: 3
- Total cost: sum all response file costs
- Pass/fail count
- Remaining gaps
- Recommended follow-ups (group drill-down deferred to separate batch)

---

## Task Files Location

All task files in `.deia/hive/tasks/`:
- `2026-03-23-TASK-CANVAS-000-PANE-ARCHITECTURE.md`
- `2026-03-23-TASK-CANVAS-001-IR-PIPELINE.md`
- `2026-03-23-TASK-CANVAS-002-PROCESS-FLOW-NODES.md`
- `2026-03-23-TASK-CANVAS-003A-ANNOTATION-NODES-BASIC.md`
- `2026-03-23-TASK-CANVAS-003B-ANNOTATION-NODES-RICH.md`
- `2026-03-23-TASK-CANVAS-004-CONFIGURE-MODE.md`
- `2026-03-23-TASK-CANVAS-005-OPTIMIZE-MODE.md`
- `2026-03-23-TASK-CANVAS-006-PLAYBACK-BACKEND.md`
- `2026-03-23-TASK-CANVAS-007-TABLETOP-BACKEND.md`
- `2026-03-23-TASK-CANVAS-008-COMPARE-BACKEND.md`
- `2026-03-23-TASK-CANVAS-009A-LASSO-AND-BROADCAST.md`
- `2026-03-23-TASK-CANVAS-009B-SMART-HANDLES.md`
- `2026-03-23-TASK-CANVAS-009C-PROPERTY-TABS.md`
- `2026-03-23-TASK-CANVAS-010-ELK-LAYOUT.md`

**Obsolete (replaced by splits, do not dispatch):**
- `2026-03-23-TASK-CANVAS-003-ANNOTATION-NODES.md` → replaced by 003A + 003B
- `2026-03-23-TASK-CANVAS-009-LASSO-AND-FEATURES.md` → replaced by 009A + 009B + 009C

---

## Deferred Work (Not in This Build)

- **Group drill-down:** Hierarchical sub-flow composition where a group node opens a separate pane showing the detailed sub-process. Neither old nor new platform had this. Genuinely new feature. Q88N approved deferral.
- **Old canvas node types that were renamed:** Old "task" → new "phase-node", old "decision" → new "checkpoint-node". These are at parity, not regressions.
- **Collaboration stubs:** LiveCursors, DesignFlight, NodeComments — shell stubs with no backend. Not in scope for this build. Separate decision needed.

---

## Key Decisions Made This Session

1. **Pane architecture first:** Q88N directed that ALL floating panels must be shell panes defined in EGG, not custom position:absolute divs. CANVAS-000 establishes this pattern.
2. **ELK over dagre:** Old platform used dagre. Q88N wants ELK (better hierarchical layout, future group drill-down support).
3. **Port from old, don't reinvent:** Take the lead from old canvas on anything that worked. Read old source files, port the patterns.
4. **Group drill-down deferred:** Can wait for a separate batch after this build completes.
5. **Q33NR does not dispatch bees directly:** Wave 1 was a violation (noted). Waves 2+3 go through Q33N via briefings.
