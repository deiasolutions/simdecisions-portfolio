# TASK-159: Port Entity Archetype Management from Platform

**Date:** 2026-03-16
**Model:** sonnet
**Priority:** P0.75
**Estimated Time:** 90 minutes

---

## Objective

Port the complete entity archetype management system from platform/efemera to hivenode/entities. This includes ORM model, four consensus methods, management functions, API routes, LLM provider shim, and complete test suite (25 tests).

---

## Context

This is part of the platform rebuild effort. The entity archetype system provides:
1. **Tribunal consensus** — multiple LLM providers propose domain archetypes, system synthesizes
2. **Drift detection** — monitors when entity definitions deviate from established archetype
3. **Archetype history** — tracks evolution of domain definitions over time
4. **Four consensus methods:**
   - A: Majority (picks most representative candidate)
   - B: Weighted average (averages embeddings, picks closest text)
   - C: LLM synthesis (Claude synthesizes unified description)
   - D: Human select (user picks candidate by index)

This system is **ALREADY BUILT and TESTED** in platform. This is a PORT, not a design task.

**Key dependency:** Platform uses `llm_providers.py` with `call_provider()` and `extract_json_from_response()`. ShiftCenter does not have a unified provider interface. You will create a minimal LLM shim to bridge this gap.

---

## Files to Read First

**Platform source files (to port FROM):**
1. `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\entities\archetypes.py` (433 lines)
2. `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\entities\archetype_routes.py` (111 lines)
3. `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\tests\test_archetypes.py` (517 lines)
4. `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\llm_providers.py` (for shim reference)

**ShiftCenter target files (to port TO):**
5. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\database.py` (verify Base and get_db)
6. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\entities\__init__.py` (will add exports)
7. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\entities\routes.py` (will add archetype routes)
8. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\adapters\anthropic.py` (for LLM shim reference)

---

## Deliverables

### 1. Create `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\entities\archetypes.py` (433 lines)

Port from platform `archetypes.py` with these adjustments:

**Import changes:**
```python
# Platform:
from ..database import Base
from ..llm_providers import call_provider, extract_json_from_response

# ShiftCenter:
from engine.database import Base
from hivenode.entities.llm_shim import call_provider, extract_json_from_response
```

**Content to port (EXACTLY as-is, only change imports):**
- DomainArchetype ORM model (lines 36-48)
- ArchetypeCandidate, ConsensusResult dataclasses (lines 55-68)
- Pydantic schemas: ArchetypeCandidateSchema, ArchetypeResponse, DriftCheckRequest, DriftCheckResponse, RefreshRequest (lines 74-109)
- Embedding helpers: hash_embedding, cosine_similarity, serialize_embedding, deserialize_embedding (lines 114-151)
- Four consensus methods: consensus_method_a, consensus_method_b, consensus_method_c, consensus_method_d (lines 157-338)
- Management functions: generate_archetype, get_current_archetype, check_drift (lines 344-433)

**File must be under 500 lines** ✓ (433 lines, compliant)

---

### 2. Create `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\entities\archetype_routes.py` (111 lines)

Port from platform `archetype_routes.py` with these adjustments:

**Import changes:**
```python
# Platform:
from ..database import get_db
from .archetypes import (...)

# ShiftCenter:
from engine.database import get_db
from hivenode.entities.archetypes import (...)
```

**Content to port (EXACTLY as-is, only change imports):**
- router = APIRouter(prefix="/api/domains", tags=["archetypes"])
- _archetype_to_response helper (lines 34-46)
- POST /{domain}/archetype/refresh (lines 49-77)
- GET /{domain}/archetype (lines 80-86)
- GET /{domain}/archetype/history (lines 89-98)
- POST /{domain}/archetype/check-drift (lines 101-110)

**File must be under 500 lines** ✓ (111 lines, compliant)

---

### 3. Create `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\entities\llm_shim.py` (NEW, ~80 lines)

Create a minimal LLM provider shim to match platform's `llm_providers.py` interface.

**Required interface:**
```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class ProviderResponse:
    provider: str
    text: str           # Raw LLM response text
    cost_usd: float
    latency_ms: int
    model: str
    is_stub: bool = False   # True when stub fallback was used

def call_provider(
    provider: str,  # "claude" | "gemini" | "local"
    prompt: str,
    system: str = "",
    max_tokens: int = 512,
) -> ProviderResponse:
    """
    Call the specified LLM provider.

    Falls back to stub (is_stub=True, text="") when:
    - API key is not configured
    - Provider call fails

    This matches platform behavior: graceful degradation.
    """
    # Implementation:
    # 1. Try to import and use hivenode.adapters.anthropic/gemini
    # 2. If ANTHROPIC_API_KEY or GOOGLE_API_KEY not set, return stub
    # 3. If call fails, return stub
    # Always return ProviderResponse regardless of success/failure
    pass

def extract_json_from_response(text: str) -> Optional[dict]:
    """
    Extract first JSON object from LLM response text.

    Returns None if no JSON found or parse fails.
    """
    # Implementation:
    # 1. Use regex to find {...} blocks
    # 2. Try json.loads() on each
    # 3. Return first valid dict or None
    pass
```

**Implementation notes:**
- Use `os.getenv("ANTHROPIC_API_KEY")` to check for API keys
- Use `requests.post()` for HTTP calls (matching platform pattern)
- Anthropic endpoint: `https://api.anthropic.com/v1/messages`
- Default model: `claude-haiku-4-5-20251001`
- Timeout: 60 seconds
- Log warnings when falling back to stub
- Return `ProviderResponse(provider="claude", text="", cost_usd=0.0, latency_ms=0, model="...", is_stub=True)` on failure

**File must be under 500 lines** ✓ (~80 lines, compliant)

---

### 4. Update `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\entities\__init__.py`

Add exports for archetype module:

```python
# Existing imports...

from hivenode.entities.archetypes import (
    # ORM
    DomainArchetype,
    # Dataclasses
    ArchetypeCandidate,
    ConsensusResult,
    # Schemas
    ArchetypeResponse,
    DriftCheckRequest,
    DriftCheckResponse,
    RefreshRequest,
    # Helpers
    hash_embedding,
    cosine_similarity,
    serialize_embedding,
    deserialize_embedding,
    # Consensus methods
    consensus_method_a,
    consensus_method_b,
    consensus_method_c,
    consensus_method_d,
    # Management
    generate_archetype,
    get_current_archetype,
    check_drift,
)

__all__ = [
    # Existing exports...
    # Archetype exports
    "DomainArchetype",
    "ArchetypeCandidate",
    "ConsensusResult",
    "ArchetypeResponse",
    "DriftCheckRequest",
    "DriftCheckResponse",
    "RefreshRequest",
    "hash_embedding",
    "cosine_similarity",
    "serialize_embedding",
    "deserialize_embedding",
    "consensus_method_a",
    "consensus_method_b",
    "consensus_method_c",
    "consensus_method_d",
    "generate_archetype",
    "get_current_archetype",
    "check_drift",
]
```

---

### 5. Update `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\entities\routes.py`

Add archetype routes to existing router:

```python
# At top of file, add import:
from hivenode.entities.archetype_routes import (
    refresh_archetype,
    get_archetype,
    get_archetype_history,
    check_archetype_drift,
)

# In the router setup section, add routes:
router.post("/api/domains/{domain}/archetype/refresh", status_code=201)(refresh_archetype)
router.get("/api/domains/{domain}/archetype")(get_archetype)
router.get("/api/domains/{domain}/archetype/history")(get_archetype_history)
router.post("/api/domains/{domain}/archetype/check-drift")(check_archetype_drift)
```

**OR** (if simpler):
```python
from hivenode.entities import archetype_routes

# In router setup:
router.include_router(archetype_routes.router)
```

Choose whichever approach is cleaner based on existing route.py structure.

---

### 6. Create `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\entities\test_archetypes.py` (517 lines)

Port from platform `test_archetypes.py` with these adjustments:

**Import changes:**
```python
# Platform:
from src.efemera.main import app
from src.efemera.database import SessionLocal
from src.efemera.entities.archetypes import (...)

# ShiftCenter:
from hivenode.main import app  # (verify correct path to FastAPI app)
from engine.database import SessionLocal
from hivenode.entities.archetypes import (...)
```

**Content to port (EXACTLY as-is, only change imports):**
- All 25 tests (lines 98-517)
- Fixtures: db_session, client, _make_candidates (lines 48-96)

**File must be under 1,000 lines** ✓ (517 lines, compliant for tests)

---

## Test Requirements

### TDD Approach
1. **Port tests FIRST** (before implementation)
2. **Run tests** (they will fail on missing imports)
3. **Create implementation files** (archetypes.py, archetype_routes.py, llm_shim.py)
4. **Run tests again** (should pass)

### All 25 tests must pass:

**Unit tests (17):**
- test_domain_archetype_crud
- test_hash_embedding_consistent
- test_cosine_similarity_identical
- test_cosine_similarity_orthogonal
- test_consensus_method_a_picks_most_representative
- test_consensus_method_a_single_candidate
- test_consensus_method_b_averages_embeddings
- test_consensus_method_b_single_candidate
- test_consensus_method_d_selects_by_index
- test_consensus_method_d_out_of_range
- test_generate_archetype_saves_to_db
- test_generate_archetype_marks_previous_non_current
- test_get_current_archetype
- test_check_drift_detects_deviation
- test_check_drift_same_embedding
- test_check_drift_no_archetype
- test_serialize_deserialize_roundtrip
- test_serialize_deserialize_hash_embedding
- test_consensus_method_c_concatenates (bonus)

**API tests (8):**
- test_api_refresh_archetype
- test_api_refresh_archetype_no_candidates
- test_api_get_current_archetype
- test_api_get_current_archetype_not_found
- test_api_get_archetype_history
- test_api_get_archetype_history_empty
- test_api_check_drift

### Test command:
```bash
cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter
python -m pytest tests/hivenode/entities/test_archetypes.py -v
```

**Expected result:** 25 passed, 0 failed

---

## Edge Cases to Verify

1. **Empty candidates list** → 400 error on refresh endpoint
2. **Single candidate** → All consensus methods return it with confidence=1.0
3. **Out-of-range index for method D** → IndexError
4. **No current archetype** → 404 on GET /archetype
5. **Drift check with no archetype** → returns (True, 0.0)
6. **Identical embedding** → no drift (similarity=1.0)
7. **Multiple archetype generations** → previous marked is_current=0
8. **Stub fallback** → consensus_method_c returns concatenation with confidence=0.7 when no API key

---

## Constraints

1. **No file over 500 lines** (Rule 4) — all source files comply
2. **TDD** (Rule 5) — port tests first, then implementation
3. **NO STUBS** (Rule 6) — full implementation required. Note: consensus_method_c stub fallback is a FEATURE (graceful degradation), not a violation.
4. **Absolute paths** (Rule 8) — all paths in this task file are absolute
5. **CSS variables** (Rule 3) — N/A (backend only)
6. **Response file** — 8 sections MANDATORY (see template below)

---

## Acceptance Criteria

- [ ] `hivenode/entities/archetypes.py` created (433 lines, all functions ported)
- [ ] `hivenode/entities/archetype_routes.py` created (111 lines, 4 endpoints)
- [ ] `hivenode/entities/llm_shim.py` created (~80 lines, ProviderResponse + call_provider + extract_json)
- [ ] `hivenode/entities/__init__.py` updated with archetype exports
- [ ] `hivenode/entities/routes.py` updated with archetype route registration
- [ ] `tests/hivenode/entities/test_archetypes.py` created (517 lines, 25 tests)
- [ ] All 25 tests pass (17 unit + 8 API)
- [ ] Routes accessible under `/api/domains/{domain}/archetype/...`
- [ ] No files exceed 500 lines (tests allowed to 1,000)
- [ ] No hardcoded colors (N/A for backend)
- [ ] No stubs in implementation (stub fallback in consensus_method_c is intentional)
- [ ] Database table `domain_archetypes` created automatically on first run
- [ ] Import adjustments correct (engine.database, hivenode.entities.llm_shim)

---

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260316-TASK-159-RESPONSE.md`

The response MUST contain these 8 sections:

1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full absolute paths
3. **What Was Done** — bullet list of concrete changes (not intent)
4. **Test Results** — test files run, pass/fail counts, actual pytest output
5. **Build Verification** — test pass summary, build output if applicable
6. **Acceptance Criteria** — copy from above, mark [x] or [ ] with explanation
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.

---

## Implementation Notes

1. **Port, don't rewrite.** The platform code is tested and working. Copy structure, adapt imports only.

2. **Embedding strategy:** Platform uses `hash_embedding` (deterministic SHA-256 hashing) for tests. This is CORRECT. Do not introduce external embedding dependencies.

3. **SQLite compatibility:** The `DomainArchetype` model uses `LargeBinary` for embeddings and `Integer` for booleans (0/1). This is SQLite-compatible. Keep it.

4. **Consensus method C (LLM synthesis):** Falls back to stub concatenation when no API key configured. This is intentional. Keep the fallback.

5. **is_current flag:** When generating new archetype, mark all previous archetypes for that domain as `is_current=0`. This ensures only one current archetype per domain.

6. **Route prefix:** Routes use `/api/domains/{domain}/archetype/...` — this is the CORRECT pattern. Do not change.

7. **Test fixtures:** Platform uses `db_session` and `client` fixtures that clean the table before/after. Port these exactly.

8. **LLM shim:** The shim should match platform's ProviderResponse interface exactly. When API key is missing, return stub with `is_stub=True` and empty text. This allows consensus_method_c to fall back gracefully.

---

## Build Verification

After implementation, verify:

1. **Run tests:**
   ```bash
   cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter
   python -m pytest tests/hivenode/entities/test_archetypes.py -v
   ```
   Expected: `25 passed`

2. **Check table creation:**
   ```bash
   sqlite3 .deia/efemera.db "SELECT name FROM sqlite_master WHERE type='table' AND name='domain_archetypes';"
   ```
   Expected: `domain_archetypes`

3. **Check route registration:**
   ```bash
   curl http://localhost:3301/docs | grep archetype
   ```
   Expected: 4 endpoints visible in OpenAPI docs

---

## Timeline Estimate

- **File reads:** 10 minutes
- **Port archetypes.py:** 20 minutes
- **Port archetype_routes.py:** 10 minutes
- **Create llm_shim.py:** 15 minutes
- **Update __init__.py + routes.py:** 5 minutes
- **Port test_archetypes.py:** 20 minutes
- **Run tests, fix imports:** 15 minutes
- **Write response file:** 5 minutes

**Total:** ~100 minutes (within timeout)

---

**END TASK FILE**
