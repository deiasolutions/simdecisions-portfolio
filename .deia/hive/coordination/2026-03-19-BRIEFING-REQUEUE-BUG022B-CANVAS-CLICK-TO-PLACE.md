# BRIEFING: BUG-022-B Canvas Click-to-Place Broken

**Date:** 2026-03-19
**From:** Q33NR (REGENT-QUEUE-TEMP-SPEC-REQUEUE-BUG022)
**To:** Q33N (Queen Coordinator)
**Priority:** P0

---

## Context from Q88N

Click-to-place was working yesterday. User confirms it stopped working. Multiple previous bees claimed COMPLETE or FALSE_POSITIVE but **the feature is broken at runtime**.

Clicking a component in the canvas palette/components panel does NOT place it on the canvas.

**Critical finding:** No palette component exists in `browser/src/primitives/canvas/` — there is no `Palette.tsx`, `ComponentsPanel.tsx`, or similar file.

---

## Objective

Fix the click-to-place flow so that clicking a component in the palette results in a node appearing on the canvas.

---

## Investigation Required

Before writing task files, Q33N MUST:

1. **Read the canvas EGG config** (`eggs/canvas.egg.md`) to understand how the palette pane is configured
2. **Read `browser/src/primitives/canvas/CanvasApp.tsx`** to understand how nodes are added
3. **Check for bus events** that handle node addition (e.g. `node:add`, `palette:select`, `component:place`)
4. **Check tree-browser adapters** — is there a palette adapter in `browser/src/primitives/tree-browser/adapters/`?
5. **Understand the current state** — what code exists, what's missing, what's broken

---

## Deliverables (for task files)

The task(s) you write must ensure:

- [ ] Clicking a palette item places a node on the canvas
- [ ] New node appears at a reasonable position (center of viewport or cursor)
- [ ] Tests for the click-to-place flow (TDD)
- [ ] No regressions in canvas tests
- [ ] All tests pass (backend and frontend)

---

## Files to Read First (Q33N must read these)

- `eggs/canvas.egg.md` (palette pane config)
- `browser/src/primitives/canvas/CanvasApp.tsx`
- `browser/src/primitives/canvas/canvasTypes.ts`
- `browser/src/primitives/tree-browser/adapters/` (look for palette adapter)
- `browser/src/infrastructure/relay_bus/` (bus event types)

---

## Constraints

- No file over 500 lines
- CSS: `var(--sd-*)` only (no hardcoded colors)
- No stubs
- **MUST verify the fix works** by checking bus event wiring end-to-end
- Tests MUST be written first (TDD)

---

## Test Commands (include in task files)

```bash
cd browser && npx vitest run --reporter=verbose src/primitives/canvas/
cd browser && npx vitest run
```

---

## Model Assignment

**Sonnet** — This is a P0 bug with cross-component investigation required.

---

## Next Steps

1. Read the files listed above
2. Determine root cause (missing component? broken event handler? disconnected bus subscriber?)
3. Write task file(s) with concrete deliverables
4. Return task files to Q33NR for review
5. **DO NOT dispatch bees until Q33NR approves**

---

## Response File Reminder

Every bee MUST write an 8-section response file to `.deia/hive/responses/YYYYMMDD-TASK-ID-RESPONSE.md`. No exceptions.

---

End of briefing.
