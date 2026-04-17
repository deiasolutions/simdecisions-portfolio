# BRIEFING: PHASE-IR Runtime + DES Engine Port

**Date:** 2026-03-14
**From:** Q88NR (Queue Regent)
**To:** Q33N (Queen Coordinator)
**Spec:** `.deia/hive/queue/2026-03-14-0100-SPEC-phase-ir-port.md`
**Priority:** P0

---

## Objective

Port the PHASE-IR specification (v1.0) and DES execution engine from the legacy `platform/efemera` repository into the shiftcenter `engine/` directory. Write hivenode sim routes and ledger adapter to integrate the simulation engine with the existing Event Ledger and FastAPI infrastructure.

---

## Context

### What Exists Now

**Old Repo:** `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\`
- `phase_ir/primitives.py` — 11 IR types (Flow, Node, Edge, Port, Token, Resource, Variable, Distribution, Timing, Group, Checkpoint)
- `des/` directory with 16 files total:
  - Core engine files: `core.py`, `engine.py`, `tokens.py`, `resources.py`, `statistics.py`, `variables.py`, `replay.py`, `sweep.py`, `replication.py`
  - Additional files noted: `checkpoints.py`, `dispatch.py`, `distributions.py`, `edges.py`, `generators.py`, `pools.py`, `loader_v2.py`, `engine_routes.py`
  - `__init__.py`
- Tests: `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\tests\des\` (270+ tests)

**New Repo:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\`
- `engine/` directory exists but contains only `__init__.py` (1 byte)
- `hivenode/ledger/writer.py` — existing Event Ledger writer
- `hivenode/routes/__init__.py` — existing route registry
- `hivenode/main.py` — existing FastAPI app with lifespan

**Full Spec:** `C:\Users\davee\Downloads\SPEC-PHASE-IR-PORT-001.md` (267 lines, detailed technical spec)

---

## What Q33N Must Deliver

Q33N will write **TWO task files** for parallel bee execution:

### Task 1: Engine Port (Bee 1 — Sonnet)
**Deliverables:**
- Copy `efemera/src/efemera/phase_ir/primitives.py` → `engine/phase_ir/primitives.py`
- Copy ALL relevant DES files from `efemera/src/efemera/des/` → `engine/des/`
  - Core files listed in spec section 3.1: `core.py`, `engine.py`, `tokens.py`, `resources.py`, `statistics.py`, `variables.py`, `replay.py`, `sweep.py`, `replication.py`
  - **DO NOT copy** `engine_routes.py` (will be rewritten as hivenode routes)
  - **Survey other files** in old repo's `des/` directory to determine if they should be ported (e.g., `checkpoints.py`, `distributions.py`, `edges.py`, `generators.py`, etc.)
- Fix ALL imports: `from efemera.` → `from engine.`
- Write `engine/__init__.py`, `engine/phase_ir/__init__.py`, `engine/des/__init__.py`
- Copy tests from `efemera/tests/des/` → `tests/engine/des/`
- Fix test imports
- Run: `cd tests/engine && python -m pytest des/ -v`
- **Target:** 270+ tests passing

### Task 2: Hivenode Sim Routes + Ledger Adapter (Bee 2 — Sonnet)
**Deliverables:**
- Write `engine/des/ledger_adapter.py` — bridges DES events to hivenode Event Ledger
  - Must call `hivenode.ledger.writer.LedgerWriter.write_event()`
  - Map DES events to `SIM_*` event types (see spec section 6)
  - Include all three currencies: `CLOCK` (sim_time), `COIN` (0 for sim), `CARBON` (compute estimate)
- Write `hivenode/routes/sim.py` — 16 FastAPI routes:
  - `/sim/load` (POST) — load PHASE-IR flow
  - `/sim/start` (POST) — start simulation
  - `/sim/pause` (POST) — pause simulation
  - `/sim/resume` (POST) — resume simulation
  - `/sim/step` (POST) — advance one event
  - `/sim/step/{n}` (POST) — advance N events
  - `/sim/status` (GET) — current state
  - `/sim/inject` (POST) — inject token
  - `/sim/checkpoint` (POST) — save checkpoint
  - `/sim/restore` (POST) — restore from checkpoint
  - `/sim/fork` (POST) — fork simulation (Alterverse)
  - `/sim/tokens` (GET) — list active tokens
  - `/sim/resources` (GET) — resource utilization
  - `/sim/statistics` (GET) — stats snapshot
  - `/sim/events` (GET) — recent sim events
  - `/sim/sweep` (POST) — parameter sweep
- Write `hivenode/schemas_sim.py` — Pydantic models for sim API
- Register routes in `hivenode/routes/__init__.py`
- Write tests:
  - `tests/engine/des/test_ledger_adapter.py` (10+ tests)
  - `tests/hivenode/test_sim_routes.py` (10+ E2E tests)
- **Target:** 20+ new tests passing

---

## Files Q33N Must Read Before Writing Tasks

**Required reads:**
1. `C:\Users\davee\Downloads\SPEC-PHASE-IR-PORT-001.md` — full technical spec (267 lines)
2. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\ledger\writer.py` — existing ledger interface
3. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\__init__.py` — route registration pattern
4. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\main.py` — app structure
5. Survey old repo DES directory: `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\des\` — identify all files to port
6. Survey old repo tests: `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\tests\des\` — count tests, identify structure

---

## Acceptance Criteria (from Spec)

When Q33N writes task files, ensure ALL these criteria are distributed across the two tasks:

- [ ] `from engine.des import SimulationEngine` works
- [ ] `from engine.phase_ir.primitives import Flow, Node, Edge` works
- [ ] 270+ existing DES tests pass in new location
- [ ] Sim can load a simple IR flow (3 nodes, 2 edges), run to completion
- [ ] Event Ledger receives `SIM_*` events during simulation
- [ ] All 16 hivenode sim routes respond correctly
- [ ] `/sim/load` + `/sim/start` + `/sim/status` E2E test passes
- [ ] No file over 500 lines (split if needed)
- [ ] 20+ new tests for ledger adapter and sim routes

---

## Critical Constraints

1. **PHASE-IR v1.0 ONLY** — do NOT implement v2.0 features (no state_refs, no implicit_termination, etc.)
2. **Do NOT port:**
   - Production engine (`efemera/production/`)
   - Tabletop engine (`efemera/tabletop/`)
   - Optimization/OR-Tools (`efemera/optimization/`)
   - Surrogate pipeline (`efemera/surrogates/`)
3. **Import paths:** All `from efemera.` → `from engine.` or `from hivenode.`
4. **File size:** No file over 500 lines (hard limit: 1,000)
5. **Parallel bees:** Two independent tasks, can run simultaneously
6. **Model assignment:** Both tasks use `sonnet`
7. **TDD:** Tests first, then implementation (except for pure copy-paste port of existing code)
8. **No stubs:** Every function fully implemented

---

## Model Assignment

**Both bees: sonnet**

Engine port is mechanical (copy + fix imports) but large. Routes/adapter are new code, require design. Sonnet handles both.

---

## Q33N Next Steps

1. **Read all 6 required files** listed above
2. **Survey old repo** to identify exact file list for port
3. **Write Task File 1:** `2026-03-14-TASK-071-engine-port-phase-ir-des.md`
4. **Write Task File 2:** `2026-03-14-TASK-072-hivenode-sim-routes-adapter.md`
5. **Return task files to Q88NR for review** (do NOT dispatch yet)
6. **After Q88NR approval:** dispatch both bees in parallel

---

## Expected Timeline

- Q33N reads + writes task files: ~30 min
- Q88NR review: ~15 min
- Bee 1 (engine port): ~2 hours (mechanical, large file count)
- Bee 2 (routes/adapter): ~1.5 hours (design + tests)
- **Total:** ~4 hours wall time (parallel execution)

---

## Event Log

```
QUEUE_SPEC_STARTED: 2026-03-14-0100-SPEC-phase-ir-port
QUEUE_BRIEFING_WRITTEN: 2026-03-14-BRIEFING-phase-ir-port.md
```

---

**Q88NR will dispatch Q33N with this briefing. Q33N: read, survey, write tasks, return for review.**
