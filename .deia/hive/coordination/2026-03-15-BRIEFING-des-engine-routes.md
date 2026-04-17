# BRIEFING: Port DES Engine Routes

**To:** Q33N (Queen Coordinator)
**From:** Q33NR (Regent)
**Date:** 2026-03-15
**Spec:** `.deia/hive/queue/2026-03-15-1005-SPEC-w1-05-des-engine-routes.md`

---

## Objective

Port DES engine routes from platform repo (~265 lines). Create API endpoints for simulation execution in hivenode.

## Context from Q88N

This is part of W1 (Week 1) sprint to port DES simulation engine components. Previous specs completed:
- W1-02: phase-ir CLI ✓
- W1-03: phase-ir trace ✓
- W1-04: phase-ir models ✓

Now we need the HTTP routes that expose simulation control endpoints.

## Source Material

**Source file:** `platform/efemera/src/efemera/engine_routes.py` (~265 lines)

The platform file contains FastAPI routes for:
- `/sim/start` - initiate a simulation run
- `/sim/step` - execute one simulation step
- `/sim/status` - query simulation state
- `/sim/results` - retrieve simulation output

## Target Implementation

**Target file:** `hivenode/routes/des_routes.py`

**Registration:** Add to `hivenode/routes/__init__.py` (already has phase_ir routes registered)

## Model Assignment

**Haiku** — this is a straightforward port with established patterns.

## Constraints from Spec

- Max 500 lines per file
- TDD: tests first
- No stubs
- CSS: var(--sd-*) only (not applicable for backend routes)
- Heartbeat: POST to `http://localhost:8420/build/heartbeat` every 3 minutes with task status

## Acceptance Criteria (from spec)

- [ ] DES engine routes ported from platform
- [ ] Endpoints: `/sim/start`, `/sim/step`, `/sim/status`, `/sim/results`
- [ ] Routes registered in `hivenode/routes/__init__.py`
- [ ] Tests written and passing

## Smoke Test

```bash
python -m pytest tests/hivenode/test_des_routes.py -v
```

No new test failures allowed.

## What Q33N Must Do

1. **Read source file:** `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\engine_routes.py` (or equivalent path)
2. **Read existing hivenode patterns:**
   - `hivenode/routes/phase_ir.py` (recently ported, similar pattern)
   - `hivenode/routes/__init__.py` (registration pattern)
3. **Write ONE task file** for a haiku bee:
   - Port routes
   - Write tests first (TDD)
   - Register in routes/__init__.py
   - Full test coverage for all 4 endpoints
4. **Return task file to Q33NR for review**
5. **After approval:** Dispatch haiku bee with task file

## Success Criteria

- All tests green
- No stubs
- No file over 500 lines
- Response file complete (8 sections)
- Routes callable via HTTP

---

**Q33N: Read this briefing, then write the task file. Return for review before dispatching.**
