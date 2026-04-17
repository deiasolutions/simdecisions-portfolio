# BRIEFING: Wire Canvas Chatbot Terminal NL to LLM to PHASE-IR to Canvas

**To:** Q33N (Queen Coordinator)
**From:** Q33NR (Queen Regent)
**Date:** 2026-03-15
**Spec:** SPEC-w2-02-canvas-chatbot-wire
**Priority:** P0.90
**Model Assignment:** Sonnet

---

## Objective

Wire the end-to-end canvas chatbot flow: user types natural language in terminal → LLM converts to PHASE-IR → canvas receives and renders nodes. This connects three existing systems that are already built but not yet wired together.

---

## Context from Q88N

The spec requires:
1. Terminal NL input reaches LLM
2. LLM response parsed into PHASE-IR flow
3. Canvas receives and renders flow
4. End-to-end demo works
5. Tests written and passing

The terminal already has `routeTarget: 'canvas'` capability (added in Efemera work). PHASE-IR backend routes exist (ported in TASK-145). Canvas can render flows (from sim work). The missing piece is the **wiring layer** that connects them.

---

## Existing Systems to Wire Together

### 1. Terminal with routeTarget='canvas'
- Location: `browser/src/primitives/terminal/`
- Already handles `routeTarget` prop
- Sends input to backend or relay depending on target
- Needs: adapter to route canvas messages to LLM service

### 2. PHASE-IR Backend
- Routes: `hivenode/routes/phase_routes.py` (15 endpoints)
- Key endpoints: `/api/phase/flows` (create), `/api/phase/flows/{flow_id}` (get)
- Models: `engine/phase_ir/models.py` (Node, Edge, Flow, etc.)
- Schema: `engine/phase_ir/phase_ir_schema.json`
- Needs: endpoint for "NL to IR conversion" or use existing flow creation

### 3. Canvas (Flow Designer)
- Location: `browser/src/apps/sim/components/flow-designer/`
- Already renders nodes and edges from flow data
- Uses relay_bus events for updates
- Needs: listener for incoming flow data from chatbot

---

## Technical Approach

### Option A: New LLM Adapter Service (Recommended)
Create a new service in `browser/src/services/llm/` that:
1. Takes NL input from terminal
2. Calls backend LLM route (e.g., `/api/llm/nl-to-phase-ir`)
3. Backend calls Claude/GPT with PHASE-IR schema as context
4. Returns PHASE-IR JSON
5. Frontend sends to canvas via bus event

### Option B: Direct Canvas Adapter
Wire terminal directly to canvas adapter in `browser/src/apps/` that:
1. Handles `routeTarget='canvas'` messages
2. Calls backend LLM endpoint
3. Receives PHASE-IR
4. Publishes to bus for canvas to render

### Option C: Extend Existing simAdapter
The `simAdapter.tsx` already exists and handles sim-related logic. Could extend it to handle chatbot NL → PHASE-IR flow.

---

## Files to Review Before Writing Tasks

**Frontend:**
- `browser/src/primitives/terminal/useTerminal.tsx` (routeTarget handling)
- `browser/src/apps/simAdapter.tsx` (existing sim wiring)
- `browser/src/apps/sim/components/flow-designer/FlowDesigner.tsx` (canvas component)
- `browser/src/infrastructure/relay_bus/constants.ts` (bus event types)
- `browser/src/services/` (where LLM service would go)

**Backend:**
- `hivenode/routes/phase_routes.py` (PHASE-IR endpoints)
- `engine/phase_ir/models.py` (IR models)
- `engine/phase_ir/phase_ir_schema.json` (schema for LLM prompt)

**Tests:**
- `browser/src/primitives/terminal/__tests__/` (terminal tests)
- `browser/src/apps/sim/components/flow-designer/__tests__/` (canvas tests)
- `tests/hivenode/test_phase_routes.py` (backend PHASE-IR tests)

---

## Constraints

- **Max 500 lines per file** (modularize if needed)
- **TDD:** Tests first, then implementation
- **No stubs:** Every function fully implemented
- **CSS:** `var(--sd-*)` only (no hardcoded colors)
- **POST heartbeats** to `http://localhost:8420/build/heartbeat` every 3 minutes with JSON:
  ```json
  {"task_id": "2026-03-15-1536-SPEC-w2-02-canvas-chatbot-wire", "status": "running", "model": "sonnet", "message": "working"}
  ```

---

## Acceptance Criteria (from Spec)

- [ ] Terminal NL input reaches LLM
- [ ] LLM response parsed into PHASE-IR flow
- [ ] Canvas receives and renders flow
- [ ] End-to-end demo works
- [ ] Tests written and passing

---

## Smoke Test

After implementation:
```bash
cd browser && npx vitest run src/apps/sim/
```
No new test failures allowed.

---

## Your Task (Q33N)

1. **Read the files listed above** to understand current state
2. **Choose the best technical approach** (A, B, or C — or propose better)
3. **Write task files** breaking this into bee-sized units:
   - Backend: LLM endpoint for NL → PHASE-IR (if needed)
   - Frontend: LLM service or adapter (if needed)
   - Frontend: Wiring terminal → LLM → canvas
   - Tests: Unit tests for each layer
   - Tests: E2E test for full flow
4. **Return task files to me (Q33NR) for review** — DO NOT dispatch bees yet
5. **After I approve:** dispatch bees in correct order (backend first if needed, then frontend, then tests)

---

## Questions to Answer in Your Response

1. Does the existing PHASE-IR backend have everything needed, or do we need a new LLM endpoint?
2. Where should the LLM service live? New `browser/src/services/llm/` or extend existing adapter?
3. How many task files will this require? (Estimate 2-4 tasks)
4. What bus event types need to be added (if any)?
5. What test coverage is needed? (Unit + integration + E2E)

---

**END OF BRIEFING**
