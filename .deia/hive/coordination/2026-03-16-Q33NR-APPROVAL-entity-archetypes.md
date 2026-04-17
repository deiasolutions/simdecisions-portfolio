# Q33N Coordination Report: Entity Archetype Port

**Date:** 2026-03-16
**From:** Q33N (Bot ID: QUEEN-2026-03-16-BRIEFING-entity-arc)
**To:** Q33NR (Regent)
**Re:** Briefing "Port Entity Archetype Management from Platform"

---

## Briefing Analysis

I have read the briefing, reviewed the three platform source files (archetypes.py: 433 lines, archetype_routes.py: 111 lines, test_archetypes.py: 517 lines), and analyzed the ShiftCenter target location.

**Key findings:**

1. **Target directory exists:** `hivenode/entities/` already exists with bot embedding infrastructure
2. **Routes already registered:** Line 9 of `hivenode/routes/__init__.py` imports `entity_routes` and line 42 registers it
3. **Database infrastructure ready:** `engine/database.py` provides `Base` and `get_db` (exact match to platform pattern)
4. **LLM provider gap:** Platform uses `llm_providers.py` with `call_provider()` and `extract_json_from_response()`. ShiftCenter has adapters but no unified `call_provider()` function.

---

## Dependency Resolution Strategy

The briefing correctly identifies the LLM provider functions as the key dependency. Here's my assessment:

### What exists in ShiftCenter:
- `hivenode/adapters/anthropic.py`, `gemini.py`, etc. (individual adapters)
- `hivenode/adapters/base.py` (BaseAdapter interface with `.call()` method)
- No unified `call_provider("claude", prompt, system)` function

### What platform archetypes.py expects:
```python
from ..llm_providers import call_provider, extract_json_from_response
# ...
response = call_provider("claude", prompt, system=system, max_tokens=512)
```

### Proposed solution (per briefing guidance):
Create a minimal **adapter shim** at `hivenode/entities/llm_shim.py` that:
1. Implements `call_provider()` wrapper (returns ProviderResponse dataclass)
2. Implements `extract_json_from_response()` helper
3. Falls back to stub when no API key configured (matching platform behavior)

This keeps the archetype system functional without external API dependency, exactly as the briefing instructs.

**File count: +1** (llm_shim.py, ~80 lines)

---

## Task Structure

Per briefing guidance, this should be **ONE task** (not multiple) because the three files are tightly coupled. Breaking them apart creates broken intermediate states.

### Task TASK-159: Port Entity Archetype Management

**Deliverables:**
1. `hivenode/entities/archetypes.py` (433 lines) — ORM model, consensus methods, management functions
2. `hivenode/entities/archetype_routes.py` (111 lines) — 4 API endpoints
3. `hivenode/entities/llm_shim.py` (NEW, ~80 lines) — adapter wrapper for platform compatibility
4. `hivenode/entities/__init__.py` — add archetype exports
5. `hivenode/entities/routes.py` — add archetype routes to existing router
6. `tests/hivenode/entities/test_archetypes.py` (517 lines) — port all 25 tests

**Total files:** 6 (3 new source files, 2 modified, 1 new test file)

**Model assignment:** sonnet (per briefing)

**Acceptance criteria:**
- [ ] All 25 tests pass (17 unit + 8 API)
- [ ] All source files under 500 lines
- [ ] Routes accessible under `/api/domains/{domain}/archetype/...`
- [ ] No stubs (consensus_method_c fallback is INTENTIONAL feature)
- [ ] Full TDD coverage

**Estimated timeline:** ~90 minutes (briefing estimated 80 minutes, adding 10 for llm_shim)

---

## Import Path Adjustments

Platform uses relative imports:
```python
from ..database import Base
from ..llm_providers import call_provider
```

ShiftCenter equivalent:
```python
from engine.database import Base
from hivenode.entities.llm_shim import call_provider
```

All other imports remain identical (SQLAlchemy, FastAPI, Pydantic, etc.).

---

## Route Integration

Current `hivenode/entities/routes.py` has router at `/api/bots`. The archetype routes should be added to the **existing router** (not a new router) to avoid duplication.

**Modification strategy:**
```python
# In hivenode/entities/routes.py
from hivenode.entities.archetype_routes import router as archetype_router

# Add to existing router setup
router.include_router(archetype_router)  # Brings in /api/domains/... prefix
```

Routes will be accessible under `/api/domains/{domain}/archetype/...` (matching platform pattern).

---

## Test Fixture Adjustments

Platform test fixtures reference:
```python
from src.efemera.main import app
from src.efemera.database import SessionLocal
```

ShiftCenter equivalent:
```python
from hivenode.main import app  # (or wherever the FastAPI app is)
from engine.database import SessionLocal
```

All test logic remains identical.

---

## File Line Counts (Compliance Check)

| File | Lines | Limit | Status |
|------|-------|-------|--------|
| archetypes.py | 433 | 500 | ✓ PASS |
| archetype_routes.py | 111 | 500 | ✓ PASS |
| llm_shim.py | ~80 | 500 | ✓ PASS |
| test_archetypes.py | 517 | 1,000 (tests) | ✓ PASS |

All files comply with Rule 4 (no file over 500 lines, tests allowed up to 1,000).

---

## Risk Assessment

**Low risk.** This is a straightforward port with:
- Clear source files (all tested and working in platform)
- Clear target location (hivenode/entities already exists)
- Clear acceptance criteria (25 tests must pass)
- No architectural changes (pure port)

**Mitigation for LLM dependency gap:** The llm_shim.py adapter ensures the archetype system works with stub responses when no API key is configured, matching platform's graceful degradation behavior.

---

## Task File Ready for Review

I have analyzed the briefing and am ready to write the task file for TASK-159. The task will include:
- Absolute file paths for all source and test files
- Full context on import adjustments
- Explicit llm_shim.py spec (to resolve dependency gap)
- All 25 test criteria enumerated
- 8-section response template requirement

**Awaiting Q33NR approval to proceed with task file creation.**

---

## Questions / Clarifications

None. The briefing is comprehensive and all dependencies are resolvable.

---

**END COORDINATION REPORT**
