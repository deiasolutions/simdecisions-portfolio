# BRIEFING: Wire DES events to canvas tokens move nodes light up

**From:** Q33NR
**To:** Q33N
**Date:** 2026-03-16
**Priority:** P1.05
**Model Assignment:** sonnet

---

## Objective

Wire DES simulation events to canvas visualization: tokens move along edges, active nodes light up, resource nodes show utilization colors. Uses animation system from w1-07.

---

## Context from Spec

**Spec ID:** 2026-03-16-1022-SPEC-w2-05-des-canvas-visual
**Queue file:** `.deia/hive/queue/2026-03-16-1022-SPEC-w2-05-des-canvas-visual.md`

The spec requires:
- Token animations follow simulation events
- Active nodes highlight during simulation
- Resource nodes show utilization colors
- Animation playback controls work
- Tests written and passing

**Constraints:**
- Max 500 lines per file
- TDD: tests first
- No stubs
- CSS: var(--sd-*) only
- File claim system (POST to localhost:8420/build/claim before modifying)
- Heartbeat every 3 minutes (POST to localhost:8420/build/heartbeat)

**Smoke test:** `cd browser && npx vitest run src/apps/sim/components/flow-designer/animation/`

---

## What Already Exists

Based on git status and memory:

1. **Animation system from w1-07** (TASK-147):
   - `browser/src/primitives/canvas/animation/__tests__/` (test directory exists)
   - `browser/src/apps/sim/components/flow-designer/animation/CheckpointFlash.tsx`
   - `browser/src/apps/sim/components/flow-designer/animation/NodePulse.tsx`
   - `browser/src/apps/sim/components/flow-designer/animation/QueueBadge.tsx`
   - `browser/src/apps/sim/components/flow-designer/animation/ResourceBar.tsx`
   - `browser/src/apps/sim/components/flow-designer/animation/SimClock.tsx`
   - `browser/src/apps/sim/components/flow-designer/animation/TokenAnimation.tsx`
   - Tests: `browser/src/apps/sim/components/flow-designer/__tests__/animation.test.tsx`

2. **DES routes** (TASK-146, R01):
   - `hivenode/routes/des_routes.py` — 4 endpoints (`/api/des/run`, `/api/des/validate`, `/api/des/replicate`, `/api/des/status`)
   - Tests: 22 passing

3. **Shell chrome** (BL-151):
   - Pane chrome components exist
   - Route targets include canvas

4. **Animation colors** (TASK-148):
   - Fixed to use `var(--sd-*)` CSS variables

---

## What Q33N Must Do

### Step 1: Read the codebase
Before writing task files, read:
- `browser/src/apps/sim/components/flow-designer/animation/` (all 6 components)
- `browser/src/apps/sim/components/flow-designer/__tests__/animation.test.tsx`
- `hivenode/routes/des_routes.py` (to understand event schema from `/api/des/run`)
- Any existing canvas/flow-designer integration files

### Step 2: Write task files

Break this into bee-sized tasks (max 500 lines per file, TDD):

**Suggested breakdown:**
1. **Event subscriber** — listen to DES simulation events from backend, parse them, emit to canvas
2. **Token movement** — wire TokenAnimation component to event subscriber, animate tokens along edges
3. **Node highlighting** — wire NodePulse component to event subscriber, highlight active nodes
4. **Resource utilization** — wire ResourceBar component to event subscriber, show color changes
5. **Playback controls** — wire SimClock component to event subscriber, control animation speed/pause
6. **Integration tests** — E2E test that verifies all animations respond to real DES events

**Each task file must include:**
- Objective (one sentence)
- Context (what the bee needs to know)
- Files to Read First (absolute paths)
- Deliverables (concrete outputs with checkboxes)
- Test Requirements (TDD, edge cases)
- Constraints (500 lines, CSS vars, no stubs, file claims, heartbeats)
- Response requirements (8-section template)

### Step 3: Return task files to Q33NR for review

Write a summary of task files created. Do NOT dispatch bees yet. Wait for Q33NR approval.

---

## Acceptance Criteria (from Spec)

- [ ] Token animations follow simulation events
- [ ] Active nodes highlight during simulation
- [ ] Resource nodes show utilization colors
- [ ] Animation playback controls work
- [ ] Tests written and passing

---

## Critical Reminders

1. **TDD:** Tests first, then implementation. No exceptions.
2. **No stubs:** Every function fully implemented. No `// TODO`, no empty bodies.
3. **File claims:** Before modifying any file, POST to `http://localhost:8420/build/claim` with `{"task_id": "...", "files": [...]}`. If conflicts, poll GET `/build/claims` every 30s. Release early with POST `/build/release`.
4. **Heartbeats:** POST to `http://localhost:8420/build/heartbeat` every 3 minutes with `{"task_id": "...", "status": "running", "model": "sonnet", "message": "working"}`.
5. **CSS:** Only `var(--sd-*)`. No hex, no rgb(), no named colors.
6. **500 line limit:** Modularize at 500. Hard limit: 1,000.
7. **Absolute paths:** All file paths in task files must be absolute (Windows format: `C:\Users\davee\OneDrive\...`).

---

## Expected Deliverables from Q33N

1. Task files written to `.deia/hive/tasks/` (one per bee unit of work)
2. Summary of task files (what each task does, which bee gets which task, dependencies)
3. Return to Q33NR for review before dispatching bees

---

## Model Assignment

**Sonnet** — complex wiring logic, event subscription, animation orchestration.

---

## Questions for Q33N to Investigate

1. What is the event schema from `/api/des/run`? (Read `hivenode/routes/des_routes.py` to see response format.)
2. How do the 6 animation components currently receive props? (Read their source files.)
3. Is there an existing event bus in the canvas/flow-designer? Or do we need to create one?
4. What are the edge cases for token movement (e.g., multiple tokens on same edge, token arrival at node, token destruction)?
5. What are the utilization thresholds for resource color changes (e.g., <50% green, 50-80% yellow, >80% red)?

Do NOT guess. Read the code. If the spec is unclear, write tasks that include "investigate" steps before implementation.

---

**End of Briefing.**
