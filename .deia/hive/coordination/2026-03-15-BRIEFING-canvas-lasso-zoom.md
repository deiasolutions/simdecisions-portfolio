# BRIEFING: Port canvas lasso selection + zoom controls + annotation badge

**From:** Q33NR
**To:** Q33N
**Date:** 2026-03-15
**Spec ID:** 2026-03-15-1124-SPEC-w1-08-canvas-lasso-zoom
**Model Assignment:** haiku
**Priority:** P0.40

---

## Objective

Port 3 canvas interaction components from platform to browser:
1. **LassoSelection** — multi-select by drawing rectangle
2. **ZoomControls** — fit, zoom in/out, reset
3. **AnnotationBadge** — comment count indicator on nodes

**Source:** `platform/.../canvas/` (exact path TBD — you need to locate it)
**Target:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\`

Total ~435 lines to port.

---

## Context

This is part of the canvas/sim work (w1 week). Other canvas specs have already been processed:
- SPEC-w1-06 (canvas node types) — DONE
- SPEC-w1-07 (canvas animation) — DONE

This spec adds **user interaction** components to the flow-designer canvas.

---

## Constraints from Spec

- **Max 500 lines per file** (hard rule #4)
- **TDD: tests first** (hard rule #5)
- **No stubs** (hard rule #6)
- **CSS: var(--sd-*) only** (hard rule #3)
- **Heartbeats:** POST to `http://localhost:8420/build/heartbeat` every 3 minutes with:
  ```json
  {"task_id": "2026-03-15-1124-SPEC-w1-08-canvas-lasso-zoom", "status": "running", "model": "haiku", "message": "working"}
  ```

---

## Acceptance Criteria (from spec)

- [ ] Lasso selection component ported
- [ ] Zoom controls component ported
- [ ] Annotation badge component ported
- [ ] Tests written and passing

---

## Smoke Test (from spec)

```bash
cd browser && npx vitest run src/apps/sim/components/flow-designer/
```

No new test failures.

---

## Your Tasks (Q33N)

1. **Locate the source files** in the platform repo. Find:
   - LassoSelection component
   - ZoomControls component
   - AnnotationBadge component

2. **Read existing flow-designer structure** in browser to understand where these fit.

3. **Write ONE task file** for the haiku bee:
   - Task file must include:
     - Absolute paths to source files (platform)
     - Absolute paths to target files (browser)
     - Specific test requirements (how many tests, which scenarios)
     - Specific constraints (500-line limit, CSS vars, no stubs)
     - 8-section response file requirement

4. **Return the task file to me (Q33NR) for review.** Do NOT dispatch the bee yet.

---

## What I (Q33NR) Will Review

When you return the task file, I will check:
- [ ] Deliverables match spec acceptance criteria
- [ ] File paths are absolute
- [ ] Test requirements are specific (count, scenarios)
- [ ] CSS uses var(--sd-*) only
- [ ] No file over 500 lines
- [ ] No stubs allowed
- [ ] Response file template present

---

## Notes

- This is a PORT, not a rewrite. The haiku bee should copy/adapt existing code from platform, not create from scratch.
- If the source files don't exist or are incomplete, the bee should report that in the response file and mark the task as FAILED.
- If the total line count exceeds 500 per file, the bee must split into multiple files.

---

**Next step:** Q33N reads this briefing, locates source files, writes task file, returns to Q33NR for review.
