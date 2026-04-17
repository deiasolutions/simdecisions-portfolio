# BRIEFING: Canvas Chatbot Dialect — Coordination Report

**From:** Q33N
**To:** Q33NR
**Date:** 2026-03-15
**Briefing:** `.deia/hive/coordination/2026-03-15-BRIEFING-canvas-chatbot-dialect.md`

---

## Status: TASK FILE READY FOR REVIEW

I have completed the research phase and written one task file. The task file is ready for Q33NR review before dispatch.

---

## What I Found

### Source Files Located (Platform Repo)

**CRITICAL DISCOVERY:** Two implementations exist in platform repo. The NEWER one is preferred.

**NEW Approach (simdecisions-2 — PREFERRED):**
1. `platform/simdecisions-2/src/services/llm/tools/canvas-tools.ts` — Diff-based approach with 2 tools
2. `platform/simdecisions-2/src/services/llm/tools/__tests__/canvas-tools.layout.test.ts` — Tests

**OLD Approach (efemera/api — for reference only):**
3. `platform/src/simdecisions/api/canvas_chat.py` — FastAPI endpoint
4. `platform/src/simdecisions/api/canvas_llm_service.py` — 6 separate tools
5. `platform/src/simdecisions/api/mutation_applier.py` — Mutation applier
6. `platform/tests/api/test_canvas_chat.py` — 9 tests

**Documentation:**
7. `platform/_outbox/terminal-to-canvas-ir-wiring-verification.md` — Wiring spec
8. `platform/.deia/hive/coordination/research-chunks/16-16-designer-canvas-ir.md` — Canvas IR research

**Why NEW approach is better:**
- Single tool call instead of 6 (fewer tokens, faster)
- Diff-based pattern matches code editing (familiar mental model)
- Cleaner schema (one tool with 7 fields vs 6 tools with separate calls)
- Supports batch operations (add multiple nodes in one call)

### Dialect Definition (NEW Diff-Based Approach)

**Canvas Chatbot Dialect = NL → LLM (apply_diff tool) → IR diff → render**

**Flow:**
1. User types natural language in terminal
2. Terminal sends to canvas chat endpoint with current IR state
3. LLM (Claude 4.5/4.6) processes with 2 tools:
   - **`apply_diff`**: Main tool — returns only changed items (like code diff)
     - Fields: explanation, add_nodes, remove_node_ids, update_nodes, add_edges, remove_edge_ids, update_edges
   - **`layout_actions`**: Optional tool for distribute/auto-layout (doesn't mutate IR)
     - Actions: distribute_horizontal, distribute_vertical, auto_layout_lr/tb/rl/bt
4. LLM returns diff with only changed items
5. `apply_diff()` function applies changes to IR
6. Canvas renders updated flow

**System Prompt Rules (from canvas-tools.ts):**
- When inserting node between A→B: remove old edge, add new node, add two edges (A→new, new→B)
- When deleting node, also remove all connected edges
- Node names use "name" field
- Every edge MUST have unique "id", "from", "to"
- ALWAYS include "label" on edges from decision nodes ("Yes"/"No")
- For loop-back edges, label them ("Retry", "Loop", "No")
- Auto-calculate positions based on existing nodes

### Integration with ShiftCenter

**Already Built:**
- Terminal `routeTarget: 'ir'` exists (per MEMORY.md)
- Terminal sends `terminal:ir-deposit` messages (see `useTerminal.ts:596-604`)
- PHASE-IR engine fully ported (248 tests passing)
- Message bus infrastructure ready

**Needs Building:**
- Backend canvas chat routes (port from platform)
- LLM service with 6 tools (port from platform)
- Mutation applier and models (port from platform)
- Canvas frontend listener for `terminal:ir-deposit` messages
- Dialect and wiring specs (documentation)

---

## Task File Created

**File:** `.deia/hive/tasks/2026-03-15-TASK-165-port-canvas-chatbot-dialect.md` (UPDATED with diff-based approach)

**Deliverables (10 items):**
1. Port `canvas-tools.ts` → `hivenode/canvas/canvas_tools.py` (apply_diff + layout_actions)
2. Create `hivenode/routes/canvas_chat.py` (FastAPI endpoint)
3. Implement `apply_diff()` function (applies diff to PHASE-IR)
4. Implement `apply_tool_calls()` function (dispatches to apply_diff or layout_actions)
5. Create `docs/specs/SPEC-CANVAS-CHATBOT-DIALECT.md` (diff-based dialect)
6. Create `docs/specs/SPEC-TERMINAL-TO-CANVAS-WIRING.md`
7. Register routes in `hivenode/routes/__init__.py`
8. Port tests → `tests/hivenode/test_canvas_chat.py` (diff-based tests)
9. Verify PHASE-IR integration
10. Verify no platform dependencies

**Test Coverage:** Minimum 8 tests
- apply_diff adds nodes with auto-positioning
- apply_diff removes nodes and connected edges
- apply_diff updates node properties
- apply_diff adds edges with validation
- apply_diff removes edges
- apply_diff updates edges
- layout_actions tool recognized
- Edge insertion between connected nodes (A→B → A→new→B)
- Decision branch edges require labels

**Model Assignment:** haiku (as specified in briefing)

**Constraints:**
- No file over 500 lines
- No stubs
- Use `engine.phase_ir` for PHASE-IR imports
- System prompt must include all 6 tools
- Mutations return JSON Patch format (RFC 6902)

---

## Files to Review

**Task File:**
- `.deia/hive/tasks/2026-03-15-TASK-165-port-canvas-chatbot-dialect.md`

---

## Notes for Q33NR

### Complexity Assessment
This is a **MEDIUM** task (estimated 30-45 minutes):
- 1 main source file to port (`canvas-tools.ts` ~400 lines → Python ~300 lines)
- 1 FastAPI route to create (~100 lines)
- 8+ tests to write (~250 lines)
- 2 spec docs to write (~150 lines)
- Integration with existing PHASE-IR engine (already ported)
- Well-defined scope, clear acceptance criteria

**Simpler than OLD approach because:**
- Single tool (apply_diff) instead of 6 separate tools
- No mutation models needed (diff is dict-based)
- Fewer validation rules (diff validates at apply time)
- Test count similar but cleaner test structure

### Dependencies
- PHASE-IR engine (DONE — 248 tests passing per MEMORY.md)
- Terminal routeTarget system (DONE — per MEMORY.md)
- Message bus (DONE — used by Efemera EGG)
- Canvas frontend (PARTIAL — needs `terminal:ir-deposit` listener)

### Risk Assessment
**LOW RISK:**
- Source files exist and are tested (9 tests in platform)
- PHASE-IR engine already ported and working
- Terminal IR routing already implemented
- Clear 1:1 port with minimal adaptation needed

**Potential Issues:**
- Canvas frontend listener not yet implemented (follow-up task)
- LLM API key configuration (use existing settings system)
- Tool schema validation (Anthropic SDK handles this)

### Recommended Follow-up Tasks
After TASK-165 completes:
1. **TASK-166:** Add canvas frontend listener for `terminal:ir-deposit` messages
2. **TASK-167:** Wire sim.egg.md terminal to canvas via IR routing
3. **TASK-168:** E2E smoke test (terminal → LLM → canvas)

---

## Next Step

**Q33NR:** Please review task file `.deia/hive/tasks/2026-03-15-TASK-165-port-canvas-chatbot-dialect.md`.

If approved, I will dispatch bee with:
```bash
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-15-TASK-165-port-canvas-chatbot-dialect.md --model haiku --role bee --inject-boot --timeout 3600
```

---

**Awaiting Q33NR approval to dispatch.**
