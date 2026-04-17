# TASK-227: LLM Triage Functions

## Objective

Create triage utility functions that classify incoming prompts by intent (simulation, query, design, chat) and route them to the correct handler with confidence scores.

## Context

**Current state:**
- Terminal sends prompts to hivenode backend
- No classification layer — everything goes to a single LLM call
- No routing logic to determine which handler to use

**What this task creates:**
A triage module that examines incoming prompts and returns:
- Intent classification (simulation, query, design, chat, unknown)
- Confidence score (0.0 to 1.0)
- Recommended handler route (e.g., `/api/des/run`, `/api/phase/validate`, `/shell/exec`)
- Extracted parameters (if pattern matches known command structures)

**How it will be used:**
- Terminal sends user prompt → triage classifies intent → routes to appropriate backend handler
- Reduces unnecessary LLM calls for structured commands
- Enables smart routing between simulation, design, and conversational modes

**Intent categories:**
1. **simulation** — "run 100 specs", "simulate pipeline with 5 bees", "test failure rate 0.2"
2. **query** — "show me the flow", "list active tasks", "what's in the queue?"
3. **design** — "create a node", "add edge from A to B", "define resource pool"
4. **chat** — "how does this work?", "explain bottlenecks", conversational questions
5. **unknown** — couldn't classify with confidence

## Files to Read First

**Existing routes (to understand what handlers exist):**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\shell.py` (shell command execution)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\des_routes.py` (DES simulation endpoints)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\pipeline_sim.py` (pipeline simulation)

**Schema references:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\shell\schemas.py` (ShellExecRequest)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\des\core.py` (SimConfig)

**Router registration (optional — if adding endpoint):**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\__init__.py`

## Files You May Modify

**Maximum 3 files:**

1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\triage.py` (NEW)
   - Create module with triage classification functions

2. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_triage.py` (NEW)
   - Create comprehensive test suite (minimum 10 tests)

3. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\__init__.py` (MODIFY — optional)
   - Register triage endpoint if adding HTTP route (only if needed)

## Files You Must NOT Modify

- **NO modifications to `browser/`** — frontend is protected (recovery work)
- **NO modifications to `engine/`** — engine modules are stable
- **NO modifications to existing routes** — shell.py, des_routes.py, pipeline_sim.py are complete
- **NO modifications to shell executor or schemas** — only triage logic

## Deliverables

- [ ] **Create `hivenode/triage.py`** with these functions:
  - `classify_intent(prompt: str) -> dict`
    - Returns: `{"intent": str, "confidence": float, "handler": str, "params": dict}`
    - Intent values: "simulation", "query", "design", "chat", "unknown"
    - Confidence: 0.0 to 1.0
    - Handler: recommended route (e.g., "/api/pipeline/simulate")
    - Params: extracted parameters (e.g., {"pool_size": 5, "num_specs": 100})

  - `extract_simulation_params(prompt: str) -> dict`
    - Parse prompts like "run 100 specs with 5 bees and 0.1 failure rate"
    - Returns: `{"num_specs": 100, "pool_size": 5, "failure_rate": 0.1}`

  - `is_simulation_request(prompt: str) -> bool`
    - Quick check if prompt requests simulation

  - `is_query_request(prompt: str) -> bool`
    - Quick check if prompt requests data query

  - `get_confidence_threshold() -> float`
    - Return minimum confidence for routing (default: 0.7)

- [ ] **All functions fully implemented** (no stubs, no TODO comments)

- [ ] **Type hints on all functions** (use Pydantic models or TypedDict as appropriate)

- [ ] **Docstrings with Args/Returns sections** for every public function

- [ ] **Pattern matching using regex or keyword matching** (no LLM calls — keep it fast)

- [ ] **Create comprehensive test file** (minimum 10 tests, TDD approach)

## Test Requirements

**Create:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_triage.py`

- [ ] **Tests written FIRST** (TDD)
- [ ] **Minimum 10 tests:**
  1. Test `classify_intent()` with simulation prompt (e.g., "run 50 specs")
  2. Test `classify_intent()` with query prompt (e.g., "show me the queue")
  3. Test `classify_intent()` with design prompt (e.g., "create a node")
  4. Test `classify_intent()` with chat prompt (e.g., "how does this work?")
  5. Test `classify_intent()` with ambiguous prompt (low confidence)
  6. Test `extract_simulation_params()` with valid prompt
  7. Test `extract_simulation_params()` with partial params (use defaults)
  8. Test `is_simulation_request()` returns True for sim keywords
  9. Test `is_query_request()` returns True for query keywords
  10. Test confidence scoring (verify 0.0 <= confidence <= 1.0)
- [ ] **All tests pass**
- [ ] **No stubs** — every test fully implemented
- [ ] **Test file under 500 lines**

**Minimum: 10 tests**

## Constraints

- **No file over 500 lines** — modularize if needed
- **No stubs** — every function fully implemented
- **Absolute paths** in all file references
- **TDD** — write tests first
- **No LLM calls in triage** — use regex/keyword matching for speed
- **Fast execution** — triage must complete in <10ms (no blocking I/O)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260319-TASK-227-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy deliverables from above, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.

## Acceptance Criteria

- [ ] 10+ tests written and passing
- [ ] `triage.py` created with all 5 functions
- [ ] All functions have type hints and docstrings
- [ ] No stubs or TODO comments
- [ ] Pattern matching works for simulation, query, design, chat intents
- [ ] All existing hivenode tests still pass (no regressions)
- [ ] No file over 500 lines
- [ ] Triage executes in <10ms (no LLM calls)

## Build Verification Commands

```bash
# Run new triage tests
cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter && python -m pytest tests/hivenode/test_triage.py -v

# Regression check: all hivenode tests
cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter && python -m pytest tests/hivenode/ -v

# Full test suite
cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter && python -m pytest tests/ -v
```

## Dependencies

- **Depends on:** Existing routes (shell.py, des_routes.py, pipeline_sim.py) — already complete
- **Used by:** Terminal (future integration) — triage will be called before routing
- **Can run in parallel:** Yes — no conflicts with other tasks

## Notes for Bee

1. **Pattern matching approach (no LLM):**
   ```python
   import re

   SIMULATION_PATTERNS = [
       r'\brun\b.*\bspec',
       r'\bsimulate\b',
       r'\btest\b.*\bpipeline\b',
   ]

   def is_simulation_request(prompt: str) -> bool:
       prompt_lower = prompt.lower()
       return any(re.search(pat, prompt_lower) for pat in SIMULATION_PATTERNS)
   ```

2. **Parameter extraction example:**
   ```python
   def extract_simulation_params(prompt: str) -> dict:
       params = {"num_specs": 10, "pool_size": 5, "failure_rate": 0.1}  # defaults

       # Extract num_specs: "run 50 specs" → 50
       match = re.search(r'(\d+)\s+specs?', prompt.lower())
       if match:
           params["num_specs"] = int(match.group(1))

       # Extract pool_size: "with 7 bees" → 7
       match = re.search(r'(\d+)\s+bees?', prompt.lower())
       if match:
           params["pool_size"] = int(match.group(1))

       return params
   ```

3. **Confidence scoring heuristic:**
   ```python
   def calculate_confidence(prompt: str, patterns: list[str]) -> float:
       matches = sum(1 for pat in patterns if re.search(pat, prompt.lower()))
       return min(1.0, matches / len(patterns) * 1.5)  # scale to 0.0-1.0
   ```

4. **Classification logic:**
   - Check simulation patterns first (highest priority)
   - Then query patterns
   - Then design patterns
   - Default to chat if confidence < threshold
   - Return "unknown" if no patterns match

5. **Handler routing map:**
   ```python
   INTENT_HANDLERS = {
       "simulation": "/api/pipeline/simulate",
       "query": "/shell/exec",
       "design": "/api/phase/validate",
       "chat": "/chat/completions",
   }
   ```

6. **Test pattern:**
   ```python
   import pytest
   from hivenode.triage import classify_intent

   def test_classify_simulation_intent():
       prompt = "run 100 specs with 5 bees"
       result = classify_intent(prompt)
       assert result["intent"] == "simulation"
       assert result["confidence"] >= 0.7
       assert result["handler"] == "/api/pipeline/simulate"
       assert result["params"]["num_specs"] == 100
       assert result["params"]["pool_size"] == 5
   ```

7. **Performance note:** No LLM calls. No database queries. No file I/O. Pure regex + keyword matching. Should execute in <10ms.

8. **Future extension:** This module can be enhanced later with ML-based classification, but for now, regex patterns are sufficient and fast.

---

**End of Task File**
