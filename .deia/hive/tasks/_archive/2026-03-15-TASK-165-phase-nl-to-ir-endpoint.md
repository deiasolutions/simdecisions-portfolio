# TASK-165: Create /api/phase/nl-to-ir endpoint for NL-to-PHASE-IR conversion

## Objective
Build a backend FastAPI endpoint that accepts natural language input, calls an LLM (Claude/GPT) with PHASE-IR schema context, and returns structured PHASE-IR flow JSON. This enables the canvas chatbot to convert user descriptions into executable process flows.

## Context
The terminal has `routeTarget='ir'` logic that extracts IR blocks from LLM responses, but no endpoint exists to perform NL → PHASE-IR conversion. The canvas already listens for `terminal:ir-deposit` events with PHASE-IR flow data. This task creates the missing backend service.

**PHASE-IR schema location:** The schema exists in `engine/phase_ir/` modules but may need to be exported as JSON for LLM context. Check `engine/phase_ir/schema.py` for schema generation utilities.

**Existing routes:** `engine/phase_ir/schema_routes.py` handles CRUD operations. This new route handles LLM-based IR generation.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\phase_ir\schema.py` (schema utilities)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\phase_ir\models.py` (flow models)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\phase_ir\schema_routes.py` (existing routes structure)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\phase_routes.py` (if it exists, else check engine/phase_ir/)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\useTerminal.ts` (lines 575-604 for IR mode)

## Deliverables
- [ ] New file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\phase_nl_routes.py` (max 500 lines)
- [ ] Route: `POST /api/phase/nl-to-ir` with request/response schemas
- [ ] LLM integration: Call Claude or GPT API with PHASE-IR schema as context
- [ ] Response validation: Ensure returned JSON matches PHASE-IR schema
- [ ] Error handling: Invalid NL, LLM timeout, malformed IR, missing API key
- [ ] Register route in `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\__init__.py`
- [ ] Test file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_phase_nl_routes.py`

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass (`cd hivenode && python -m pytest tests/hivenode/test_phase_nl_routes.py -v`)
- [ ] Edge cases:
  - [ ] Valid NL → valid PHASE-IR flow
  - [ ] Empty text → 400 error
  - [ ] Invalid LLM response → 500 error with details
  - [ ] Missing API key → 401 error
  - [ ] LLM timeout → 504 error
  - [ ] Malformed IR (LLM hallucination) → validation error response
  - [ ] Multiple nodes/edges in description
  - [ ] BPMN-specific requests
  - [ ] Annotation requests (sticky notes, callouts)
- [ ] Minimum 15 tests

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only (N/A for backend)
- No stubs — full implementation required
- Use environment variable for LLM API key (not hardcoded)
- Support both Anthropic and OpenAI models via config
- Return PHASE-IR flow data (not raw LLM response text)
- POST heartbeats to http://localhost:8420/build/heartbeat every 3 minutes:
  ```json
  {"task_id": "2026-03-15-TASK-165-phase-nl-to-ir-endpoint", "status": "running", "model": "sonnet", "message": "working"}
  ```

## API Specification

### Request Schema (Pydantic)
```python
class NLToIRRequest(BaseModel):
    text: str  # Natural language description
    model: str = "claude-sonnet-4-5"  # LLM model to use
    api_key: str | None = None  # Optional override (else use env)
    intent: str | None = None  # Optional flow intent/description
```

### Response Schema (Pydantic)
```python
class NLToIRResponse(BaseModel):
    flow_data: dict  # PHASE-IR flow JSON
    metadata: dict  # LLM model, tokens, cost, etc.
    validation_result: dict  # {valid: bool, errors: list}
```

### Example Flow
**Request:**
```json
{
  "text": "Create a flow that starts with a task called 'Review Document', then a decision 'Is Approved?', leading to either 'Archive' or 'Reject'",
  "model": "claude-sonnet-4-5"
}
```

**Response:**
```json
{
  "flow_data": {
    "id": "flow-generated-123",
    "name": "Document Review Flow",
    "phase_ir_version": "1.0.0",
    "nodes": [
      {"id": "start", "type": "start", "name": "Start", "position": {"x": 0, "y": 0}},
      {"id": "review", "type": "task", "name": "Review Document", "position": {"x": 200, "y": 0}},
      {"id": "decision", "type": "decision", "name": "Is Approved?", "position": {"x": 400, "y": 0}},
      {"id": "archive", "type": "task", "name": "Archive", "position": {"x": 600, "y": -100}},
      {"id": "reject", "type": "task", "name": "Reject", "position": {"x": 600, "y": 100}},
      {"id": "end", "type": "end", "name": "End", "position": {"x": 800, "y": 0}}
    ],
    "edges": [
      {"id": "e1", "source": "start", "target": "review"},
      {"id": "e2", "source": "review", "target": "decision"},
      {"id": "e3", "source": "decision", "target": "archive", "label": "yes"},
      {"id": "e4", "source": "decision", "target": "reject", "label": "no"},
      {"id": "e5", "source": "archive", "target": "end"},
      {"id": "e6", "source": "reject", "target": "end"}
    ]
  },
  "metadata": {
    "model": "claude-sonnet-4-5",
    "input_tokens": 250,
    "output_tokens": 180,
    "cost_usd": 0.0025,
    "clock_ms": 1200
  },
  "validation_result": {
    "valid": true,
    "errors": []
  }
}
```

## Implementation Notes

1. **LLM Prompt Engineering:**
   - System prompt: Include PHASE-IR schema JSON
   - User prompt: Natural language description
   - Instruct LLM to return ONLY JSON (no markdown fences)
   - Include examples of valid flows

2. **Schema Context:**
   - Load PHASE-IR schema from `engine/phase_ir/schema.py` or JSON file
   - Include node types, edge types, required fields
   - Include examples for each node type

3. **Validation:**
   - Use existing `engine/phase_ir/validation.py` functions
   - Validate returned flow structure before sending response
   - Return validation errors in response if invalid

4. **Position Calculation:**
   - Auto-generate node positions (simple left-to-right or dagre)
   - Frontend canvas will re-layout if all positions are (0,0)

5. **Error Recovery:**
   - If LLM returns invalid JSON, attempt to extract JSON from markdown fence
   - If still invalid, return 422 with error details

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
