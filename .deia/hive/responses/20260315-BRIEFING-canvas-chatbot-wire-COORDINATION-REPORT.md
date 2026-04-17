# Canvas Chatbot Wire — Q33N Coordination Report

**To:** Q33NR (Queen Regent)
**From:** Q33N (Queen Coordinator)
**Date:** 2026-03-15
**Briefing:** BRIEFING-canvas-chatbot-wire
**Status:** TASK FILES READY FOR REVIEW

---

## Answers to Q33NR's Questions

### 1. Does the existing PHASE-IR backend have everything needed, or do we need a new LLM endpoint?

**Answer:** We DO need a new backend LLM endpoint. The existing PHASE-IR backend (`engine/phase_ir/schema_routes.py`) provides CRUD operations for flows, but it does NOT provide NL-to-IR conversion via LLM.

**What's needed:**
- New route: `POST /api/phase/nl-to-ir` that:
  - Takes NL text + PHASE-IR schema context
  - Calls Claude/GPT API
  - Parses response into PHASE-IR JSON
  - Returns structured flow data

### 2. Where should the LLM service live? New browser/src/services/llm/ or extend existing adapter?

**Answer:** Extend the existing `canvasAdapter.tsx` + create new backend route.

**Rationale:**
- The terminal already has `routeTarget='ir'` logic (lines 575-604 in useTerminal.ts)
- It extracts IR blocks from LLM response via `extractIRBlocks()`
- It sends `terminal:ir-deposit` bus messages to canvas
- Canvas already listens for these messages (CanvasApp.tsx line 194)
- **The missing piece:** routeTarget='canvas' is NOT implemented (only 'ai', 'shell', 'relay', 'ir' exist)

**Therefore:** We need to add `routeTarget='canvas'` handling that:
1. Calls new backend `/api/phase/nl-to-ir` endpoint
2. Receives PHASE-IR flow JSON
3. Sends to canvas via `terminal:ir-deposit` bus event

### 3. How many task files will this require?

**Answer:** 3 tasks (backend + frontend + tests)

1. **TASK-165**: Backend — NL-to-IR endpoint (sonnet)
2. **TASK-166**: Frontend — routeTarget='canvas' wiring (haiku)
3. **TASK-167**: E2E test — terminal → LLM → canvas flow (haiku)

### 4. What bus event types need to be added (if any)?

**Answer:** NONE. All required bus events already exist:
- `terminal:ir-deposit` — already defined in constants.ts (implicitly via TERMINAL_IR_GENERATED)
- `terminal:typing-start` / `terminal:typing-end` — already used
- Canvas listens for `terminal:ir-deposit` — already implemented (CanvasApp.tsx line 194)

### 5. What test coverage is needed?

**Answer:**
- Backend: Unit tests for `/api/phase/nl-to-ir` endpoint (mock LLM call, verify JSON schema)
- Frontend: Unit test for `routeTarget='canvas'` handler in useTerminal
- E2E: Full flow test (terminal input → backend → canvas render)

---

## Technical Approach (Selected)

**Hybrid of Option A and Option B:**

1. **Backend:** New `/api/phase/nl-to-ir` endpoint in `hivenode/routes/phase_nl_routes.py`
   - Accepts `{"text": str, "model": str, "api_key": str}`
   - Calls LLM with PHASE-IR schema context
   - Returns `{"flow_data": {...}, "metadata": {...}}`

2. **Frontend:** Extend `useTerminal.ts` to handle `routeTarget='canvas'`
   - When `routeTarget === 'canvas'`, call `/api/phase/nl-to-ir`
   - Parse response flow data
   - Send via `terminal:ir-deposit` bus event to canvas

3. **Canvas:** No changes needed — already listens for `terminal:ir-deposit`

---

## Task Files Written

I have written 3 task files to `.deia/hive/tasks/`:

1. **2026-03-15-TASK-165-phase-nl-to-ir-endpoint.md** (backend, sonnet)
   - Create `/api/phase/nl-to-ir` route
   - LLM integration with PHASE-IR schema context
   - 15+ unit tests (mock LLM, validate schema, error cases)

2. **2026-03-15-TASK-166-wire-canvas-route-target.md** (frontend, haiku)
   - Add `routeTarget='canvas'` handling to useTerminal
   - Call backend endpoint
   - Send IR to canvas via bus
   - 8 unit tests

3. **2026-03-15-TASK-167-canvas-chatbot-e2e-test.md** (e2e, haiku)
   - Full flow integration test
   - Terminal → backend → canvas
   - Verify nodes rendered correctly

---

## Dispatch Order (Pending Your Approval)

1. **Sequential:**
   - TASK-165 (backend) → TASK-166 (frontend) → TASK-167 (e2e)
   - Backend must complete first (dependency)
   - Frontend can't be tested without backend endpoint
   - E2E test validates full integration

**Estimated time:** ~90 minutes total (30 + 30 + 30)

---

## Next Steps

1. **Q33NR:** Review the 3 task files in `.deia/hive/tasks/`
2. **Q33NR:** Approve or request corrections
3. **Q33N:** Dispatch bees in sequence after approval
4. **Q33N:** Monitor responses, write completion report

---

**Awaiting your approval to dispatch.**

— Q33N
