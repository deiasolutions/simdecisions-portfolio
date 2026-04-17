# TASK-159: Port entity archetypes

## Objective
Port entity archetype management from platform to shiftcenter. Domain archetype generation via tribunal consensus, archetype CRUD, drift detection.

## Context
Entity archetypes represent the "ideal" profile for a given domain (e.g., "customer_support_bot", "sales_assistant"). The archetype is generated via a tribunal consensus process where multiple bots contribute their embeddings and a consensus method (majority, weighted average, LLM synthesis, or human selection) produces the final archetype.

**Platform source:** `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\entities\archetypes.py` (432 lines)

**Target file:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\entities\archetypes.py` (NEW)

**Key features to port:**
- `DomainArchetype` ORM model (SQLAlchemy)
- `ArchetypeCandidate`, `ConsensusResult` dataclasses
- Four consensus methods: `majority_vote`, `weighted_average`, `llm_synthesis`, `human_select`
- `generate_archetype()` — creates new archetype via tribunal
- `get_current_archetype()` — fetches active archetype for domain
- `check_drift()` — compares entity embedding vs current archetype
- Helper functions: `hash_embedding()`, `cosine_similarity()`

**Dependencies:**
- `engine.database` (Base, get_db) — already ported
- `hivenode.entities.voyage_embedding` (generate_embedding) — already ported
- LLM provider integration for `llm_synthesis` method (use OpenAI/Anthropic client, similar to existing hivenode LLM calls)

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\entities\archetypes.py` (source file)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\database.py` (Base, get_db)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\entities\voyage_embedding.py` (embedding adapter)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\entities\vectors_core.py` (for pattern reference)

## Deliverables
- [ ] `hivenode\entities\archetypes.py` created with full implementation (no stubs)
- [ ] `DomainArchetype` ORM model (table: `domain_archetypes`, columns: id, domain, embedding, consensus_method, created_at, is_active)
- [ ] `ArchetypeCandidate`, `ConsensusResult` dataclasses
- [ ] Four consensus methods implemented (majority, weighted avg, LLM synthesis, human select)
- [ ] `generate_archetype()` function fully implemented
- [ ] `get_current_archetype()` function fully implemented
- [ ] `check_drift()` function fully implemented (returns similarity score 0.0-1.0)
- [ ] Helper functions: `hash_embedding()`, `cosine_similarity()`
- [ ] All functions return proper types (no `Any`, no placeholders)
- [ ] File size under 500 lines (platform source is 432, should fit comfortably)

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] Test file: `tests\hivenode\entities\test_archetypes.py`
- [ ] All tests pass
- [ ] Test count target: 15-20 tests minimum
- [ ] Edge cases:
  - Empty candidate list → raise ValueError
  - Single candidate → returns that candidate as archetype
  - Drift detection with missing archetype → returns None or 0.0
  - Consensus with equal votes → deterministic tiebreaker
  - Invalid embedding dimension → raise ValueError
  - LLM synthesis with API failure → fallback to weighted average
  - Database constraint violations (duplicate active archetypes for same domain)
- [ ] Test consensus methods in isolation (unit tests for each)
- [ ] Test archetype CRUD operations (create, read, check for active archetype)
- [ ] Mock LLM API calls for `llm_synthesis` tests
- [ ] Mock Voyage AI API calls for embedding generation

## Constraints
- No file over 500 lines (platform source is 432, port should be similar)
- CSS: var(--sd-*) only (not applicable, backend only)
- No stubs — every function fully implemented
- TDD: tests first, then implementation
- Use SQLAlchemy ORM for `DomainArchetype` model (inherit from `engine.database.Base`)
- Use dataclasses for request/response schemas (not Pydantic, those go in routes)
- All imports must use absolute paths (`from hivenode.entities.voyage_embedding import ...`)
- Follow existing entity file patterns (see `vectors_core.py`, `embeddings.py`)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260315-TASK-159-RESPONSE.md`

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

## Test Commands

```bash
# Run archetype tests only
python -m pytest tests/hivenode/entities/test_archetypes.py -v

# Run all entity tests (verify no regressions)
python -m pytest tests/hivenode/entities/ -v
```

## Model Assignment
Haiku (straightforward port, no complex logic)

## Priority
P0.55 (critical path for entity vectors MVP)
