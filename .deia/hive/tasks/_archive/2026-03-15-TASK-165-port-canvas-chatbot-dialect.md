# TASK-165: Port Canvas Chatbot Dialect

## Objective
Port the canvas chatbot dialect files from platform repo and create dialect documentation that defines how the terminal talks to the canvas (NL → LLM → to_ir → render).

## Context
The canvas chatbot dialect is a key integration piece that allows users to chat naturally with their process flows. The dialect processes natural language through Claude LLM with a diff-based tool approach, converts to PHASE-IR mutations, and applies changes to the canvas.

**Flow:** User types in terminal → LLM with apply_diff tool → IR diff → Apply to canvas → Render

**IMPORTANT:** Two implementations exist in platform repo:
1. **OLD (efemera/api):** 6 separate tools (add_node, add_edge, update_node, remove_node, remove_edge, clarify)
2. **NEW (simdecisions-2):** Single `apply_diff` tool + `layout_actions` tool (PREFERRED)

The NEW approach is more efficient (fewer tokens, single tool call) and matches the "code diff" pattern. Port the NEW approach.

### Source Files (platform repo — NEW approach)
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\services\llm\tools\canvas-tools.ts` (apply_diff + layout_actions tools)
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\services\llm\tools\__tests__\canvas-tools.layout.test.ts` (tests)
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\_outbox\terminal-to-canvas-ir-wiring-verification.md` (wiring spec)

### Source Files (platform repo — OLD approach, for reference only)
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\src\simdecisions\api\canvas_chat.py` (FastAPI endpoint)
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\src\simdecisions\api\canvas_llm_service.py` (6 tools)
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\tests\api\test_canvas_chat.py` (9 tests)

### Target Structure (shiftcenter)
- Backend routes: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\canvas_chat.py`
- Canvas tools (apply_diff logic): `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\canvas\canvas_tools.py`
- Dialect spec: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\specs\SPEC-CANVAS-CHATBOT-DIALECT.md`
- Wiring spec: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\specs\SPEC-TERMINAL-TO-CANVAS-WIRING.md`
- Tests: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_canvas_chat.py`

### Integration Points
- Terminal `routeTarget: 'ir'` already exists (per MEMORY.md)
- Terminal sends `terminal:ir-deposit` messages to canvas (see `useTerminal.ts:596-604`)
- Canvas must listen for these messages and apply mutations
- Text-pane gets chat text, canvas gets IR JSON

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\services\llm\tools\canvas-tools.ts` (NEW diff-based approach)
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\services\llm\tools\__tests__\canvas-tools.layout.test.ts` (tests)
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\_outbox\terminal-to-canvas-ir-wiring-verification.md`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\useTerminal.ts` (lines 576-604, IR mode)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\phase_ir\__init__.py` (PHASE-IR exports)

## Deliverables
- [ ] Port `canvas-tools.ts` to `hivenode/canvas/canvas_tools.py` (apply_diff + layout_actions tools in Python)
- [ ] Create `hivenode/routes/canvas_chat.py` (FastAPI endpoint for chat)
- [ ] Implement `apply_diff()` function (applies diff to PHASE-IR)
- [ ] Implement `apply_tool_calls()` function (handles tool call dispatch)
- [ ] Create `docs/specs/SPEC-CANVAS-CHATBOT-DIALECT.md` (diff-based dialect definition)
- [ ] Create `docs/specs/SPEC-TERMINAL-TO-CANVAS-WIRING.md` (port wiring spec)
- [ ] Register routes in `hivenode/routes/__init__.py`
- [ ] Port tests to `tests/hivenode/test_canvas_chat.py` (diff-based tests)
- [ ] Verify integration with PHASE-IR engine (use `engine.phase_ir` imports)
- [ ] Verify no dependencies on platform-specific modules

## Test Requirements
- [ ] Tests written FIRST (TDD) — adapt tests from platform canvas-tools.layout.test.ts
- [ ] Core test scenarios:
  - `apply_diff` adds nodes with auto-positioning
  - `apply_diff` removes nodes and connected edges
  - `apply_diff` updates node properties
  - `apply_diff` adds edges with validation (source/target must exist)
  - `apply_diff` removes edges
  - `apply_diff` updates edges
  - `layout_actions` tool recognized (positions handled separately)
  - Edge insertion between connected nodes (A→B becomes A→new→B)
  - Decision branch edges require labels ("Yes"/"No")
- [ ] All tests pass (minimum 8 tests)
- [ ] No new test failures in hivenode or browser test suites

## Constraints
- No file over 500 lines (split if needed)
- CSS: `var(--sd-*)` only (N/A for backend)
- No stubs — all functions fully implemented
- Use `engine.phase_ir` for PHASE-IR imports (not platform modules)
- LLM service must use Claude 4.5/4.6 model (latest)
- Tool definition must include 2 tools: `apply_diff` (main) and `layout_actions` (optional)
- Apply_diff schema must include: explanation, add_nodes, remove_node_ids, update_nodes, add_edges, remove_edge_ids, update_edges
- Edge labels required for decision branches ("Yes"/"No") and loop-backs ("Retry"/"Loop")

## Acceptance Criteria
- [ ] Canvas chat endpoint accepts POST with `flow_id`, `message`, `history`, `current_ir`
- [ ] Canvas tools module exports 2 tools: `apply_diff` and `layout_actions`
- [ ] `apply_diff` tool schema includes all 7 fields (explanation, add_nodes, remove_node_ids, update_nodes, add_edges, remove_edge_ids, update_edges)
- [ ] `apply_diff()` function applies diff to IR and returns DiffResult with change tracking
- [ ] System prompt enforces: node insertion rules, edge deletion with nodes, edge labels for decisions/loops, position auto-calculation
- [ ] `apply_tool_calls()` function dispatches to apply_diff or layout_actions
- [ ] All tests pass (minimum 8 tests covering add/remove/update nodes/edges)
- [ ] Routes registered and accessible at `/api/canvas/chat`
- [ ] Dialect spec documents NL → LLM → apply_diff → IR flow
- [ ] Wiring spec documents terminal:ir-deposit message format
- [ ] No regressions in existing hivenode or browser tests

## Heartbeat Requirement
POST to `http://localhost:8420/build/heartbeat` every 3 minutes:
```json
{
  "task_id": "2026-03-15-TASK-165-port-canvas-chatbot-dialect",
  "status": "running",
  "model": "haiku",
  "message": "working"
}
```

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260315-TASK-165-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.
