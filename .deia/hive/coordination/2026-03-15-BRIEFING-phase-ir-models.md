# Briefing: Port PHASE-IR models.py, schema_routes.py, validate_schema.py

**From:** Q33NR
**To:** Q33N
**Date:** 2026-03-15
**Priority:** P0.20
**Model Assignment:** haiku

---

## Objective

Port the remaining PHASE-IR files from platform repo to shiftcenter:
- `models.py` (~82 lines) → rewrite as SQLite store (follow `hivenode/efemera/store.py` pattern)
- `schema_routes.py` → port as-is, register in hivenode routes
- `validate_schema.py` (~140 lines) → port with correct schema path

Ensure jsonschema>=4.0 is in pyproject.toml.

---

## Context

**What was already done:**
- PHASE-IR core ported: 13 source files + 8 test files to `engine/phase_ir/`
- 248 tests passing
- 15 API endpoints under `/api/phase` + `/api/phase/traces`
- Database dependency ported: `engine/database.py` (SQLAlchemy Base)
- Routes registered in `hivenode/routes/__init__.py`

**What's left:**
- `models.py` was a SQLAlchemy ORM file in platform. In shiftcenter we use SQLite stores (see `hivenode/efemera/store.py` for pattern).
- `schema_routes.py` provides `/api/phase/schema` endpoint (GET schema JSON)
- `validate_schema.py` validates PHASE JSON against JSON Schema

**Platform source paths:**
- `platform/efemera/src/efemera/phase_ir/models.py`
- `platform/efemera/src/efemera/phase_ir/schema_routes.py`
- `platform/efemera/src/efemera/phase_ir/validate_schema.py`

**Target paths:**
- `engine/phase_ir/models.py` (rewrite as SQLite store)
- `engine/phase_ir/schema_routes.py` (port)
- `engine/phase_ir/validate_schema.py` (port, fix schema path)

**Schema file:**
- Already exists: `engine/phase_ir/phase.schema.json`
- `validate_schema.py` should load this file

**Dependency check:**
- jsonschema library required (add to pyproject.toml if missing)

---

## Acceptance Criteria (from spec)

- [ ] models.py ported as SQLite store (follow efemera/store.py pattern)
- [ ] validate_schema.py ported with correct schema path
- [ ] schema_routes.py registered in hivenode
- [ ] Tests written and passing
- [ ] Max 500 lines per file
- [ ] TDD: tests first
- [ ] No stubs
- [ ] CSS: var(--sd-*) only (not applicable for backend)
- [ ] POST heartbeats to http://localhost:8420/build/heartbeat every 3 minutes

**Smoke test:**
- [ ] `python -m pytest tests/engine/phase_ir/ -v`
- [ ] No new test failures

---

## Constraints

- No file over 500 lines
- TDD: tests first
- No stubs (every function fully implemented)
- Absolute file paths in task docs
- Response file MUST have all 8 sections

---

## What Q33N Must Deliver

**Task files** (to `.deia/hive/tasks/`) that specify:
1. Which bee writes which file
2. Test requirements (scenarios, edge cases, minimum test count)
3. File paths (absolute)
4. Acceptance criteria mapped to deliverables
5. Heartbeat requirement (every 3 minutes to build server)
6. Response file requirement (8 sections)

**After writing task files:**
- Return to Q33NR for review
- Do NOT dispatch bees until Q33NR approves

---

## Reference Files for Q33N

Read these before writing task files:
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\efemera\store.py` (SQLite store pattern)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\phase_ir\__init__.py` (current exports)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\phase_ir\phase.schema.json` (schema file)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\__init__.py` (route registration pattern)
- Platform source (if needed): `platform/efemera/src/efemera/phase_ir/models.py`, `schema_routes.py`, `validate_schema.py`

---

## Notes

- This is the final piece of PHASE-IR port (P0.20 in series w1-02, w1-03, w1-04)
- Previous PHASE-IR tasks: TASK-145, TASK-146, TASK-147 (check responses for context)
- models.py should NOT use SQLAlchemy ORM — rewrite as SQLite store with explicit SQL
- validate_schema.py loads schema from `engine/phase_ir/phase.schema.json` (not hardcoded path from platform)

---

**Q33N: Read the spec, read the codebase, write task files, return for review.**
