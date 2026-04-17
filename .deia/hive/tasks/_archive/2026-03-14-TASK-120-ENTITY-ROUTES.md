# TASK-120: Entity Embedding Routes

**Wave:** 4
**Model:** haiku
**Role:** bee
**Depends on:** TASK-118, TASK-119

---

## Objective

Build FastAPI routes for bot embedding registration, pi computation, and drift detection.

## Source Spec

Port from: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\specs\SPEC-PORT-RAG-001-rag-pipeline-port.md`
Decomposition: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260314-Q33N-BRIEFING-PORT-RAG-PIPELINE-TASK-DECOMPOSITION.md`

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\entities\embeddings.py` (bot embedding functions)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\entities\vectors_compute.py` (pi computation)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\auth.py` (verify_jwt_or_local function)

## Files to Create

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\entities\routes.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\entities\test_routes.py`

## Files to Modify

None

## Deliverables

### routes.py (129 lines)

**Router setup:**
```python
from fastapi import APIRouter, Depends, HTTPException
from hivenode.auth import verify_jwt_or_local
from hivenode.entities.embeddings import register_bot_profile, compute_pi_bot_full, check_bot_drift
from hivenode.database import get_db
from pydantic import BaseModel

router = APIRouter(prefix="/api/bots", tags=["bot-embeddings"])
```

**Request/Response schemas:**

```python
class RegisterRequest(BaseModel):
    system_prompt: str
    model_id: Optional[str] = None

class RegisterResponse(BaseModel):
    entity_id: str
    prompt_hash: str
    model_version: str
    cached: bool

class PiResponse(BaseModel):
    pi: float
    domain_sim: float
    task_sim: Optional[float]

class CheckDriftRequest(BaseModel):
    new_system_prompt: str
    threshold: float = 0.3

class DriftResponse(BaseModel):
    drifted: bool
    similarity: Optional[float]
    threshold: float
    current_hash: Optional[str]
    new_hash: str
    reason: Optional[str]
```

**Endpoints:**

1. **`POST /api/bots/{entity_id}/register`**
   - Auth: `verify_jwt_or_local()` (local bypasses auth, cloud requires JWT)
   - Body: RegisterRequest
   - Call: `register_bot_profile(entity_id, request.system_prompt, request.model_id, db)`
   - Return: RegisterResponse

2. **`GET /api/bots/{entity_id}/pi/{domain}`**
   - Auth: `verify_jwt_or_local()`
   - Query param: `task_text: Optional[str] = None`
   - Fetch system_prompt from DB (EntityComponent table)
   - If not found: raise HTTPException(404, "Bot profile not found")
   - Call: `compute_pi_bot_full(entity_id, domain, system_prompt, task_text, db)`
   - Return: PiResponse

3. **`POST /api/bots/{entity_id}/check-drift`**
   - Auth: `verify_jwt_or_local()`
   - Body: CheckDriftRequest
   - Call: `check_bot_drift(entity_id, request.new_system_prompt, request.threshold, db)`
   - Return: DriftResponse

**Error handling:**
- 404: Bot profile not found (no system_prompt in DB)
- 401: Unauthorized (cloud mode + missing JWT)
- 500: Internal server error (Voyage API failure, DB error)

### test_routes.py (6+ tests)

**Test setup:**
- Use FastAPI TestClient
- Mock `verify_jwt_or_local()` to bypass auth
- Mock DB session (use in-memory SQLite or mock)

**Test cases:**
- Test `POST /api/bots/{entity_id}/register` creates bot profile
- Test `GET /api/bots/{entity_id}/pi/{domain}` returns pi value
- Test `GET /api/bots/{entity_id}/pi/{domain}?task_text=...` includes task_sim
- Test `POST /api/bots/{entity_id}/check-drift` returns drifted=True when threshold exceeded
- Test `POST /api/bots/{entity_id}/check-drift` returns drifted=False when similar
- Test 404 error when bot profile not found (GET pi endpoint)
- Test 401 error when JWT missing in cloud mode (mock verify_jwt_or_local to raise)

## Acceptance Criteria

- [ ] All listed files created
- [ ] All tests pass (`python -m pytest tests/hivenode/entities/test_routes.py -v`)
- [ ] No file exceeds 500 lines
- [ ] PORT not rewrite — same 3 endpoints, same auth bypass for local mode as platform/efemera
- [ ] TDD: tests written first
- [ ] 6+ tests covering all 3 endpoints, auth bypass, 401 on missing JWT (cloud mode)
- [ ] Router prefix: `/api/bots`, tags: `["bot-embeddings"]`

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260314-TASK-120-RESPONSE.md`

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
