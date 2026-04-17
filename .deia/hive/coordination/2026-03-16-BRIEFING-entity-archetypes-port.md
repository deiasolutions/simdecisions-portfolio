# BRIEFING: Port Entity Archetype Management from Platform

**Date:** 2026-03-16
**From:** Q33NR (Regent)
**To:** Q33N (Queen Coordinator)
**Priority:** P0.75
**Model Assignment:** sonnet

---

## Objective

Port the complete entity archetype management system from platform/efemera to hivenode. This includes:
- Domain archetype ORM model (SQLAlchemy)
- Four consensus methods (A: majority, B: weighted avg, C: LLM synthesis, D: human select)
- Archetype management functions (generate, get_current, check_drift)
- API routes (4 endpoints under `/api/domains/{domain}/archetype/...`)
- Complete test suite (17 unit tests + 8 API tests)

---

## Context from Q88N

This is part of the platform rebuild effort. The entity archetype system provides:
1. **Tribunal consensus** — multiple LLM providers propose domain archetypes, system synthesizes
2. **Drift detection** — monitors when entity definitions deviate from established archetype
3. **Archetype history** — tracks evolution of domain definitions over time
4. **Four consensus methods:**
   - A: Majority (picks most representative candidate)
   - B: Weighted average (averages embeddings, picks closest text)
   - C: LLM synthesis (Claude synthesizes unified description)
   - D: Human select (user picks candidate by index)

This system is ALREADY BUILT and TESTED in platform. This is a PORT, not a design task.

---

## Source Files (Platform Repo)

**Core module:**
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\entities\archetypes.py` (433 lines)
  - DomainArchetype ORM model
  - ArchetypeCandidate, ConsensusResult dataclasses
  - Pydantic schemas (ArchetypeResponse, DriftCheckRequest, etc.)
  - Embedding helpers (hash_embedding, cosine_similarity, serialize/deserialize)
  - Four consensus methods
  - Management functions (generate_archetype, get_current_archetype, check_drift)

**API routes:**
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\entities\archetype_routes.py` (111 lines)
  - POST `/api/domains/{domain}/archetype/refresh` — generate new archetype
  - GET `/api/domains/{domain}/archetype` — get current archetype
  - GET `/api/domains/{domain}/archetype/history` — get archetype history
  - POST `/api/domains/{domain}/archetype/check-drift` — check embedding drift

**Tests:**
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\tests\test_archetypes.py` (517 lines)
  - 17 unit tests (ORM CRUD, consensus methods, drift detection)
  - 8 API tests (all endpoints, edge cases)
  - 100% coverage of core functionality

---

## Target Location (ShiftCenter Repo)

**Create new module:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\entities\` (new directory)
  - `__init__.py` — exports
  - `archetypes.py` — core module (port from platform)
  - `archetype_routes.py` — API routes (port from platform)

**Tests:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\entities\` (new directory)
  - `__init__.py`
  - `test_archetypes.py` — port all tests from platform

**Route registration:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\__init__.py` — register archetype_routes router

---

## Dependencies to Verify

1. **SQLAlchemy Base** — `hivenode.database.Base` (already exists, used by other modules)
2. **Database session** — `hivenode.database.get_db` (already exists)
3. **LLM providers** — `hivenode.adapters.llm_providers.call_provider` (needs verification)
4. **JSON extraction** — `hivenode.adapters.llm_providers.extract_json_from_response` (needs verification)

If LLM provider functions are missing or incompatible, create stubs that return mock responses (to keep archetype system functional without external API calls).

---

## Key Implementation Notes

1. **Port, don't rewrite.** The platform code is tested and working. Copy structure, adapt imports.

2. **Embedding strategy:** Platform uses `hash_embedding` (deterministic SHA-256 hashing) for tests. This is CORRECT. Do not introduce external embedding dependencies.

3. **SQLite compatibility:** The `DomainArchetype` model uses `LargeBinary` for embeddings and `Integer` for booleans (0/1). This is SQLite-compatible. Keep it.

4. **Consensus method C (LLM synthesis):** Falls back to stub concatenation when no API key configured. This is intentional. Keep the fallback.

5. **is_current flag:** When generating new archetype, mark all previous archetypes for that domain as `is_current=0`. This ensures only one current archetype per domain.

6. **Route prefix:** Routes use `/api/domains/{domain}/archetype/...` — this is the CORRECT pattern. Do not change.

7. **Test fixtures:** Platform uses `db_session` and `client` fixtures that clean the table before/after. Port these exactly.

---

## Acceptance Criteria (from Spec)

- [ ] Entity archetype models ported
- [ ] CRUD operations implemented
- [ ] Schema validation working
- [ ] All archetype tests pass

**Expanded criteria:**
- [ ] `hivenode/entities/archetypes.py` created (433 lines, all functions ported)
- [ ] `hivenode/entities/archetype_routes.py` created (111 lines, 4 endpoints)
- [ ] `hivenode/entities/__init__.py` created with exports
- [ ] `tests/hivenode/entities/test_archetypes.py` created (517 lines, 25 tests)
- [ ] Routes registered in `hivenode/routes/__init__.py`
- [ ] All 25 tests pass (17 unit + 8 API)
- [ ] No files exceed 500 lines
- [ ] No hardcoded colors (N/A for backend)
- [ ] No stubs in implementation (consensus_method_c stub fallback is INTENTIONAL, not a violation)

---

## Constraints

- **TDD:** Tests MUST be ported and passing. All 25 tests from platform.
- **No file over 500 lines:** All source files are under 500 lines. Tests are 517 lines — allowed (tests can go to 1,000).
- **No stubs:** Full implementation required. The stub fallback in consensus_method_c is a FEATURE (graceful degradation when no API key), not a violation.
- **Absolute paths:** All task file paths must be absolute.
- **Response file:** 8-section response MANDATORY.

---

## Model Assignment

**sonnet** — This is a straightforward port with clear source and clear target. Sonnet can handle the file reads, import adjustments, and test verification.

---

## Task Decomposition Guidance

This should be **one task** (not multiple):
- Port all three files (archetypes.py, archetype_routes.py, test_archetypes.py)
- Register routes
- Verify all tests pass

Rationale: The three files are tightly coupled. Porting them separately would create broken intermediate states. One bee can port all three in sequence, run tests, and deliver a working system.

---

## Expected Deliverables

1. **Three new source files** (under `hivenode/entities/`)
2. **One new test file** (under `tests/hivenode/entities/`)
3. **Route registration** (one line in `hivenode/routes/__init__.py`)
4. **Test pass confirmation** (all 25 tests green)
5. **Response file** (8 sections, includes test output)

---

## Timeline Estimate

- **File reads:** 10 minutes
- **Port archetypes.py:** 20 minutes
- **Port archetype_routes.py:** 10 minutes
- **Port test_archetypes.py:** 20 minutes
- **Register routes:** 2 minutes
- **Run tests, fix imports:** 15 minutes
- **Write response file:** 5 minutes

**Total:** ~80 minutes (well within sonnet timeout)

---

## Q33N: Next Steps

1. **Read this briefing** and the three platform source files
2. **Verify dependencies** (check if LLM provider functions exist in hivenode)
3. **Write one task file** for porting all three files + tests
4. **Return task file to Q33NR for review** (do NOT dispatch yet)
5. **After Q33NR approval, dispatch sonnet bee**
6. **Review bee response** (verify all tests pass, no stubs shipped)
7. **Report results to Q33NR**

---

**END BRIEFING**
