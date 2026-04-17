# BRIEFING: Port 13 Missing Canvas Node Types

**To:** Q33N (Queen Coordinator)
**From:** Q33NR (Regent)
**Date:** 2026-03-15
**Spec ID:** 2026-03-15-1016-SPEC-w1-06-canvas-node-types
**Priority:** P0.30
**Model Assignment:** Sonnet

---

## Objective

Port 13 missing BPMN and annotation node type components from the platform repo to ShiftCenter. Total ~1,110 lines. All components must render correctly in the flow designer canvas.

---

## Context

The flow designer canvas (sim EGG) currently has basic node types but is missing advanced BPMN gateway and event types, plus annotation nodes. These exist in the platform repo and need to be ported.

### Missing Node Types (13 total)

**BPMN Gateways (5):**
- Exclusive gateway
- Parallel gateway
- Inclusive gateway
- Event-based gateway
- Complex gateway

**BPMN Events (7):**
- Intermediate event
- Boundary event
- Signal event
- Timer event
- Error event
- Compensation event
- Escalation event

**Annotation (1):**
- Annotation node

---

## Source and Target

**Source:** `platform` repo (exact path TBD — search for canvas/nodes/ or similar)
**Target:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\nodes\`

---

## Constraints

- **TDD:** Tests first, then implementation (BOOT.md Rule 5)
- **No stubs:** Every function fully implemented (BOOT.md Rule 6)
- **Max 500 lines per file** (BOOT.md Rule 4)
- **CSS: var(--sd-*) only** — no hex, rgb(), or named colors (BOOT.md Rule 3)
- **POST heartbeats** every 3 minutes to `http://localhost:8420/build/heartbeat` with:
  ```json
  {
    "task_id": "2026-03-15-1016-SPEC-w1-06-canvas-node-types",
    "status": "running",
    "model": "sonnet",
    "message": "working"
  }
  ```

---

## Acceptance Criteria (from spec)

- [ ] All 13 node type components ported
- [ ] Each node renders correctly in canvas
- [ ] Node type registry updated
- [ ] Tests written and passing

---

## Smoke Test (from spec)

```bash
cd browser && npx vitest run src/apps/sim/components/flow-designer/
```

No new test failures allowed.

---

## Your Task

1. **Locate the source files** in the platform repo
2. **Break down into bee-sized tasks** (likely 1-3 tasks depending on component coupling)
3. **Write task files** with:
   - Absolute file paths
   - Specific test scenarios (render, props, interaction)
   - Explicit line count limits per file
   - CSS variable usage enforcement
   - Registry update instructions
4. **Return task files to me (Q33NR) for review** — DO NOT dispatch bees yet
5. **After I approve:** dispatch bees

---

## Notes

- Check existing node registry structure before writing tasks
- Look for shared utilities or base classes in existing node types
- If components share common patterns, consider grouping by pattern (e.g., all gateways in one task, all events in another)
- Update any TypeScript types/interfaces for the node registry

---

**Next step:** Write task files and return them to me for review.
