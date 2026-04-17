# BRIEFING: Find and Port Kanban Board Component (BL-071)

**From:** Q33NR
**To:** Q33N
**Date:** 2026-03-15
**Priority:** P0.80
**Model Assignment:** Sonnet

---

## Objective

Find the kanban board component in the platform repo and port it to shiftcenter. The kanban should be a pane-compatible applet that renders columns (To Do, In Progress, Done) with draggable cards.

---

## Context from Q88N

This is spec `2026-03-15-1519-SPEC-w1-16-kanban-board.md` from the queue. BL-071. The kanban board should follow the same pattern as other pane applets in shiftcenter.

---

## Source and Target

**Source:** Platform repo (`platform/` directory)
**Target:** `browser/src/apps/kanban/`

The kanban board must:
- Render columns (To Do, In Progress, Done)
- Support drag and drop between columns
- Be registered as a pane applet (like sim, efemera, etc.)
- Follow TDD with tests written first
- Use only CSS variables (`var(--sd-*)`)

---

## Acceptance Criteria (from spec)

- [ ] Kanban board component ported
- [ ] Columns render with cards
- [ ] Drag and drop between columns works
- [ ] Registered as a pane applet
- [ ] Tests written and passing

---

## Constraints

- Max 500 lines per file
- TDD: tests first
- No stubs
- CSS: `var(--sd-*)` only
- Heartbeat required: POST to `http://localhost:8420/build/heartbeat` every 3 minutes with JSON:
  ```json
  {"task_id": "2026-03-15-1519-SPEC-w1-16-kanban-board", "status": "running", "model": "sonnet", "message": "working"}
  ```

---

## Smoke Test

```bash
cd browser && npx vitest run src/apps/kanban/
```

No new test failures allowed.

---

## Your Task

1. **Search the platform repo** for the kanban board component
2. **Read the source files** to understand the implementation
3. **Write task files** for porting (likely 2-3 tasks):
   - TASK-XXX: Port kanban board component (core component)
   - TASK-YYY: Wire kanban board to pane system (adapter + registration)
   - TASK-ZZZ: Port kanban board tests
4. **Return task files to Q33NR for review** before dispatching bees
5. **Include absolute paths** in all task files
6. **Specify test requirements** (how many tests, which scenarios)
7. **Verify no hardcoded colors** in source before porting
8. **Break into bee-sized tasks** (each task < 500 lines of code to write)

---

## Files to Reference

Before writing task files, check these existing patterns:
- `browser/src/apps/sim/` (sim applet structure)
- `browser/src/apps/treeBrowserAdapter.tsx` (adapter pattern)
- `browser/src/apps/simAdapter.tsx` (another adapter example)
- `browser/src/apps/index.ts` (applet registration)
- `browser/src/eggs/` (EGG loader/inflater patterns)

---

## Questions for Q33NR

If you cannot find the kanban board component in the platform repo, report this to Q33NR before writing task files.

If the source uses hardcoded colors, flag this in your task files and specify that bees must convert to CSS variables during the port.

---

## Remember

- You do NOT code unless Q88N explicitly approves
- You write task files, return to Q33NR for review, THEN dispatch bees
- Every task file must include all 8 response file sections in requirements
- No `_outbox/` directory
- Use dispatch.py for all dispatches (no per-batch scripts)
