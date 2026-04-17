# COORDINATION REPORT: Animation Event Wiring Briefing (UPDATED)

**From:** Q33N (coordinator)
**To:** Q33NR
**Date:** 2026-03-16
**Spec:** `.deia/hive/queue/2026-03-16-1500-SPEC-w2-05-animation-event-wiring.md`

---

## STATUS: TASK FILES ALREADY EXIST

I've analyzed the briefing and discovered that **task files for this spec were already created in a previous session**. They are well-structured and cover all spec requirements.

### Discovery

All 6 animation components (NodePulse, TokenAnimation, ResourceBar, SimClock, QueueBadge, CheckpointFlash) were ported in TASK-147 and are ready to use. The `useSimulation` hook already emits events and updates state. FlowDesigner already receives simulation state via `useSimulationLayer`.

**What's missing:** FlowDesigner doesn't yet RENDER the animation components. We need an overlay layer that maps simulation state to animation component props.

**The required tasks already exist:**

---

## Task Files Created

### TASK-186: Add Animation Overlay Layer to FlowDesigner
**File:** `.deia/hive/tasks/2026-03-16-TASK-186-animation-overlay-layer.md`
**Model:** Sonnet
**Deliverables:**
- Create `AnimationOverlay.tsx` component that:
  - Takes simulation state as props (simState, stats, nodeStates, edgeTokenCounts, viewport)
  - Renders NodePulse for active nodes
  - Renders TokenAnimation for edges with tokens
  - Renders ResourceBar on resource nodes
  - Renders SimClock in top-right corner
  - Renders QueueBadge on nodes with queues
  - Renders CheckpointFlash when checkpoints fire
- Integrate AnimationOverlay into FlowDesigner.tsx (inside FlowCanvas overlay section, after line 700)
- All animations reset to idle when simulation stops

### TASK-187: Animation Event Mapping Tests
**File:** `.deia/hive/tasks/2026-03-16-TASK-187-animation-event-mapping-tests.md`
**Model:** Haiku (tests only, straightforward assertions)
**Deliverables:**
- Create `AnimationOverlay.test.tsx` with 8+ tests covering:
  - node_activate → NodePulse appears
  - token_move → TokenAnimation appears
  - resource_claim → ResourceBar updates
  - checkpoint_reached → CheckpointFlash fires
  - sim_stats → SimClock + ResourceBar update
  - node queue → QueueBadge appears
  - simulation stop → animations reset
  - simulation pause → SimClock shows PAUSED

---

## Dependency Order

1. **TASK-187 (tests) FIRST** — TDD requirement
2. **TASK-186 (implementation)** — uses tests from TASK-187

---

## Files Modified (Expected)

**New files:**
- `browser/src/apps/sim/components/flow-designer/animation/AnimationOverlay.tsx`
- `browser/src/apps/sim/components/flow-designer/animation/__tests__/AnimationOverlay.test.tsx`

**Modified files:**
- `browser/src/apps/sim/components/flow-designer/FlowDesigner.tsx` (add AnimationOverlay import + render)

---

## Acceptance Criteria Mapping (from spec)

| Spec AC | Task |
|---------|------|
| FlowDesigner has event subscriber listening to useSimulation state | TASK-186 (AnimationOverlay receives simState props) |
| NodePulse highlights active nodes | TASK-186 + TASK-187 |
| TokenAnimation shows tokens moving | TASK-186 + TASK-187 |
| ResourceBar updates fill level | TASK-186 + TASK-187 |
| SimClock displays current time | TASK-186 + TASK-187 |
| QueueBadge shows queue length | TASK-186 + TASK-187 |
| Animation state resets on stop | TASK-186 + TASK-187 |
| CSS uses var(--sd-*) only | Both tasks |
| 5+ tests for event → animation mapping | TASK-187 (8 tests planned) |
| No file over 500 lines | Both tasks |

---

## Constraints & Smoke Test

All constraints from spec are copied into task files:
- Max 500 lines per file ✓
- TDD: tests first ✓
- No stubs ✓
- CSS: var(--sd-*) only ✓
- Heartbeats every 3 minutes ✓
- File claims before modification ✓

Smoke test:
- Run simulation → animations appear
- Stop simulation → animations reset
- `cd browser && npx vitest run src/apps/sim/components/flow-designer/animation/`

---

## Why Only 2 Tasks?

The work naturally splits into:
1. **Component creation + integration** (TASK-186)
2. **Test coverage** (TASK-187)

AnimationOverlay is a single integration point — all 6 animation components are already built and tested individually. We just need to orchestrate them based on simulation state.

---

---

## Verification of Existing Tasks

I read both task files in detail:

**TASK-186 (`2026-03-16-TASK-186-animation-overlay-layer.md`):**
- ✓ Creates `AnimationOverlay.tsx` component
- ✓ Maps simulation state to all 6 animation components
- ✓ Integrates into FlowDesigner (line 700+ overlay section)
- ✓ Resets animations when simulation stops
- ✓ All constraints present (500 lines, CSS vars, no stubs, TDD)
- ✓ File paths are absolute
- ✓ Response file requirements included

**TASK-187 (`2026-03-16-TASK-187-animation-event-mapping-tests.md`):**
- ✓ Creates `AnimationOverlay.test.tsx`
- ✓ Tests all event types (node_activate, token_move, resource_claim, checkpoint_reached, sim_stats, queue)
- ✓ Tests simulation lifecycle (start, pause, stop, reset)
- ✓ Edge cases covered (queue overflow, utilization > 0.8, pause state)
- ✓ 8+ tests planned (exceeds spec's 5+ requirement)
- ✓ All constraints present
- ✓ Response file requirements included

**Both tasks are complete, unambiguous, and ready for dispatch.**

---

## Proposed Dispatch Plan

### Sequential Dispatch (TASK-186 depends on TASK-187)

Per TDD requirement, tests should be written FIRST, then implementation. However, the task file for TASK-186 creates the component, and TASK-187 tests it. This is backwards from TDD.

**Corrected sequence:**

```bash
# Step 1: Write tests FIRST (TDD)
python .deia/hive/scripts/dispatch/dispatch.py \
  .deia/hive/tasks/2026-03-16-TASK-187-animation-event-mapping-tests.md \
  --model haiku \
  --role bee \
  --inject-boot \
  --timeout 900

# Step 2: Implement component to pass tests
python .deia/hive/scripts/dispatch/dispatch.py \
  .deia/hive/tasks/2026-03-16-TASK-186-animation-overlay-layer.md \
  --model sonnet \
  --role bee \
  --inject-boot \
  --timeout 1200
```

**WAIT — TDD Issue:**

TASK-187 says "Tests written FIRST (TDD)" but it cannot write tests for a component that doesn't exist yet. The component interface (props, types) is not defined until TASK-186 creates it.

**Revised approach:**
- TASK-186 should write the component skeleton + types + tests together (TDD internally within the task)
- TASK-187 becomes redundant OR should be renamed to "integration tests"

**OR:**
- Combine both tasks into one Sonnet task that does: write AnimationOverlay interface → write tests → implement component to pass tests

---

## Recommendation to Q33NR

**Option 1: Dispatch TASK-186 Only (Component + Tests Together)**
- TASK-186 creates both the component AND its tests in TDD fashion
- TASK-187 becomes redundant
- One Sonnet bee handles everything
- Estimated time: 20-25 minutes

**Option 2: Revise TASK-187 to Define Interface First**
- Add a TASK-186-PREREQ that defines AnimationOverlay props interface
- TASK-187 writes tests against that interface
- TASK-186 implements the component
- More granular but adds overhead

**Option 3: Accept the Existing Tasks As-Is**
- Dispatch TASK-186 first (creates component with internal TDD)
- Dispatch TASK-187 second (adds extra integration tests)
- Not true TDD but pragmatic
- Total time: 30-35 minutes

I recommend **Option 1** for efficiency. TASK-186 is well-scoped for one Sonnet bee to do TDD internally.

---

## Awaiting Q33NR Direction

Please advise:
1. **Dispatch TASK-186 only** (merge 186+187 into one TDD workflow)?
2. **Dispatch both tasks** (Option 3 — accept as-is)?
3. **Revise tasks** to fix TDD ordering issue?

Once you confirm, I'll execute the dispatch.

---

## Notes

- All animation components were ported in TASK-147 (completed earlier today)
- FlowDesigner already has simulation state via `useSimulationLayer` hook (line 102)
- The overlay rendering pattern already exists for LiveCursors (line 704), NodeComments (line 707), and PlaybackMode (line 722) — we're adding AnimationOverlay in the same style
- Viewport transform is already available (line 710) for positioning overlays in flow coordinates

---

**Q33N (coordinator)**
Bot ID: QUEEN-2026-03-16-BRIEFING-animation-
