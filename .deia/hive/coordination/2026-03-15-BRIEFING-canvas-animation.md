# BRIEFING: Port Canvas Animation System

**From:** Q33NR
**To:** Q33N
**Date:** 2026-03-15
**Spec:** 2026-03-15-1036-SPEC-w1-07-canvas-animation.md
**Priority:** P0.35
**Model:** haiku

---

## Objective

Port 6 canvas animation components from platform repo to ShiftCenter browser. Total ~749 lines. Components: TokenAnimation, NodePulse, EdgeFlow, ResourceMeter, SimClock, AnimationController.

---

## Context

This is part of the Week 1 canvas work. Previous work completed:
- SPEC-w1-05: DES engine routes (22 tests passing)
- SPEC-w1-06: Canvas node types (just completed)

The animation system enables visual flow simulation on the canvas — tokens moving along edges, nodes pulsing on activity, resource meters updating, clock ticking. AnimationController manages playback state (play/pause/speed).

---

## Source Files (platform repo)

Locate in platform repo at:
```
platform/canvas/animation/
  TokenAnimation.tsx
  NodePulse.tsx
  EdgeFlow.tsx
  ResourceMeter.tsx
  SimClock.tsx
  AnimationController.ts
```

---

## Target Location

```
browser/src/apps/sim/components/flow-designer/animation/
  TokenAnimation.tsx
  NodePulse.tsx
  EdgeFlow.tsx
  ResourceMeter.tsx
  SimClock.tsx
  AnimationController.ts
```

---

## Acceptance Criteria (from spec)

- [ ] All 6 animation components ported
- [ ] Animation controller manages playback state
- [ ] Token animations follow edges
- [ ] Tests written and passing

---

## Constraints

- **TDD:** Tests first, implementation second
- **500 lines max per file**
- **No stubs:** Every function fully implemented
- **CSS:** `var(--sd-*)` only — NO hex, NO rgb(), NO named colors
- **Heartbeat:** POST to http://localhost:8420/build/heartbeat every 3 minutes:
  ```json
  {"task_id": "2026-03-15-1036-SPEC-w1-07-canvas-animation", "status": "running", "model": "haiku", "message": "working"}
  ```

---

## Smoke Test (from spec)

```bash
cd browser && npx vitest run src/apps/sim/components/flow-designer/animation/
```

No new test failures allowed.

---

## Task File Requirements

Write one task file per component OR logically group into 2-3 tasks (e.g., visual components vs controller). Each task MUST specify:

1. **Absolute paths** for all files (Windows format: `C:\Users\davee\OneDrive\...`)
2. **Test requirements:** How many tests, which scenarios (TDD)
3. **Edge cases:** Token path interpolation, playback state transitions, resource overflow, clock sync
4. **Dependencies:** Does TokenAnimation need EdgeFlow data? Does AnimationController coordinate all components?
5. **CSS verification:** No hardcoded colors anywhere
6. **Line count targets:** Each file should be <400 lines if possible (hard limit 500)

---

## What Q33N Must Deliver

- [ ] 1-3 task files written to `.deia/hive/tasks/`
- [ ] Task files reviewed by Q33NR BEFORE dispatch
- [ ] All 6 components accounted for across tasks
- [ ] Test plan covering playback, token flow, pulse triggers, meter updates, clock ticks
- [ ] Clear file paths (absolute)
- [ ] Response file template included in each task

---

## Model Assignment

haiku — good for porting with clear source files

---

## Q33N: Read These Files First

Before writing task files, read:

1. Source files in platform repo (list exact paths if you find them)
2. Existing canvas code in browser:
   - `browser/src/apps/sim/components/flow-designer/` (canvas, nodes, edges)
3. Test setup:
   - `browser/src/test/setup.ts` (vitest config, p5 mock)
4. CSS variables:
   - `browser/src/styles/` (find `--sd-*` color tokens)

---

## Success Criteria

When bees finish:
- All 6 components ported
- Tests written and passing (TDD)
- No stubs
- No hardcoded colors
- Smoke test passes
- Heartbeat logs confirm continuous work

Q33N will review bee responses and report to Q33NR.

---

**Q33N: Write task files, return for Q33NR review. Do NOT dispatch bees until Q33NR approves.**
