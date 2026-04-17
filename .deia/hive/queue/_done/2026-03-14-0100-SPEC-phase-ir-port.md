# SPEC: PHASE-IR Runtime + DES Engine Port

## Priority
P0

## Objective
Port the PHASE-IR specification and DES execution engine from the old `platform/efemera` repo into the shiftcenter `engine/` directory, and write hivenode sim routes + ledger adapter.

## Context
Full spec at `C:\Users\davee\Downloads\SPEC-PHASE-IR-PORT-001.md`. Read it first.

Old repo source: `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\`
- `phase_ir/primitives.py` — 11 core IR types (Flow, Node, Edge, Port, Token, Resource, Variable, Distribution, Timing, Group, Checkpoint)
- `des/` — 14 source files (core.py, engine.py, tokens.py, resources.py, statistics.py, variables.py, ledger.py, replay.py, sweep.py, replication.py, routes.py, schemas.py, __init__.py, conftest.py)
- `tests/des/` — 270+ tests

New repo destination: `engine/` (currently empty)

Two parallel bee tasks:

### Bee 1 (sonnet): Engine Port
- Copy `efemera/src/efemera/phase_ir/` → `engine/phase_ir/`
- Copy `efemera/src/efemera/des/` → `engine/des/` (all 10 core files, NOT routes.py or schemas.py)
- Fix ALL imports: `from efemera.` → `from engine.`
- Copy `efemera/tests/des/` → `tests/engine/des/`, fix imports
- Write `engine/__init__.py`, `engine/phase_ir/__init__.py`, `engine/des/__init__.py`
- Run tests: `cd engine && python -m pytest tests/ -v`
- Target: 270+ tests passing

### Bee 2 (sonnet): Hivenode Sim Routes + Ledger Adapter
- Write `engine/des/ledger_adapter.py` — bridges DES events to hivenode Event Ledger (`hivenode/ledger/writer.py`)
- Write `hivenode/routes/sim.py` — 16 FastAPI routes (load, start, pause, resume, step, status, inject, checkpoint, restore, fork, tokens, resources, statistics, events, sweep)
- Write `hivenode/schemas_sim.py` — Pydantic models for sim API
- Register sim routes in `hivenode/routes/__init__.py`
- Write tests: `tests/engine/des/test_ledger_adapter.py`, `tests/hivenode/test_sim_routes.py`
- Target: 20+ new tests

Files to read first:
- `C:\Users\davee\Downloads\SPEC-PHASE-IR-PORT-001.md` — full spec
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\ledger\writer.py` — existing ledger writer
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\__init__.py` — route registration
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\main.py` — app entry point

## Acceptance Criteria
- [ ] `from engine.des import SimulationEngine` works
- [ ] `from engine.phase_ir.primitives import Flow, Node, Edge` works
- [ ] 270+ existing DES tests pass in new location
- [ ] Sim can load a 3-node IR flow, run to completion
- [ ] Event Ledger receives SIM_* events during simulation
- [ ] All 16 hivenode sim routes respond correctly
- [ ] `/sim/load` + `/sim/start` + `/sim/status` E2E test passes
- [ ] No file over 500 lines (split if needed)
- [ ] 20+ new tests for ledger adapter and sim routes

## Model Assignment
sonnet

## Constraints
- Two parallel bees: one for engine port, one for routes/adapter
- Do NOT port production engine, tabletop engine, optimization, or surrogates
- Do NOT implement PHASE-IR v2.0 — v1.0 only
- Import paths: `from engine.` not `from efemera.`
