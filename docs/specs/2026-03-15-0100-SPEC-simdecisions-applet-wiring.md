# SPEC: SimDecisions Applet Wiring — Last-Mile Integration

## Priority
P1

## Objective
Wire up the existing SimDecisions flow designer (121 frontend files, 818-line FlowDesigner component) into the ShiftCenter shell as a launchable applet. All major components exist — this spec connects the pieces: app adapter, EGG config, APP_REGISTRY entry, and engine integration so `/sim` loads a working flow designer with live DES simulation.

## Context

### What already exists
- **FlowDesigner component:** `browser/src/apps/sim/components/flow-designer/FlowDesigner.tsx` (818 lines) — 5 modes (Design, Simulate, Playback, Tabletop, Compare), full toolbar, property panels, file ops, animation, collaboration
- **API client adapter:** `browser/src/apps/sim/adapters/api-client.ts` — CloudAPIClient with all fetch calls
- **API client context:** `browser/src/apps/sim/adapters/ApiClientContext.tsx` — React context provider for DI
- **LocalDESEngine:** `browser/src/apps/sim/components/flow-designer/simulation/LocalDESEngine.ts` (281 lines) — Client-side fallback engine
- **Sim API routes:** `hivenode/routes/sim.py` (479 lines) — All endpoints defined, returns 503 pending engine integration
- **Sim schemas:** `hivenode/schemas_sim.py` (215 lines) — Pydantic models for all request/response types
- **DES engine:** `engine/des/engine.py` — SimulationEngine class with load, run, pause, step, checkpoint, fork
- **DES core:** `engine/des/core.py` — EngineState, SimConfig, load_flow, process_event, run
- **PHASE-IR:** `engine/phase_ir/` — Schema, validation, BPMN compiler
- **Ledger adapter:** `engine/des/ledger_adapter.py` — Bridges DES events to hivenode ledger

### What's missing
1. No `simAdapter.tsx` — FlowDesigner is not registered with the shell
2. No `sim.egg.md` — No EGG product config
3. No entry in `browser/src/apps/index.ts` APP_REGISTRY
4. `hivenode/routes/sim.py` endpoint `/sim/load` returns 503 — SimulationEngine.load() not wired
5. No WebSocket endpoint for streaming sim events to frontend

### Existing patterns to follow
- **Adapter pattern:** `browser/src/apps/canvasAdapter.tsx` (32 lines) — wraps component, passes bus from ShellCtx
- **EGG pattern:** `eggs/code.egg.md` — schema_version 3, JSON layout block, YAML frontmatter
- **Registration:** `browser/src/apps/index.ts` — `registerApp('name', Adapter)` call

## Deliverables

### Phase 1: Shell Integration (browser-only, no backend changes)
- [ ] Create `browser/src/apps/simAdapter.tsx` — Wrap FlowDesigner in AppRendererProps interface, pass bus from ShellCtx, pass paneId. Follow canvasAdapter.tsx pattern.
- [ ] Create `eggs/sim.egg.md` — EGG config with schema_version 3, single pane layout (`appType: "sim"`), defaultRoute `/sim`, displayName "SimDecisions Flow Designer"
- [ ] Add `registerApp('sim', SimAdapter)` to `browser/src/apps/index.ts`
- [ ] Verify: `localhost:5174/?egg=sim` loads FlowDesigner with demo flow visible

### Phase 2: Engine Integration (backend wiring)
- [ ] Wire `SimulationEngine` into `hivenode/routes/sim.py` — replace 503 stubs with real engine calls:
  - `POST /sim/load` → `SimulationEngine().load(flow_data)` → return run_id
  - `POST /sim/start` → engine.run() in background task
  - `POST /sim/pause` → engine.pause()
  - `POST /sim/resume` → engine.resume()
  - `POST /sim/step` → engine.step()
  - `GET /sim/status` → engine.status()
  - `GET /sim/tokens` → engine.tokens()
  - `GET /sim/resources` → engine.resources()
  - `GET /sim/statistics` → engine.statistics()
  - `POST /sim/checkpoint` → engine.checkpoint()
  - `POST /sim/restore` → engine.restore()
  - `POST /sim/fork` → engine.fork()
  - `POST /sim/sweep` → engine.sweep()
  - `GET /sim/events` → read from ledger
- [ ] Connect LedgerAdapter so sim events write to hivenode's event ledger
- [ ] Verify: `POST /sim/load` with a valid PHASE-IR flow returns 200 + run_id

### Phase 3: Tests
- [ ] Test `simAdapter.tsx` renders FlowDesigner (mount test, verify canvas present)
- [ ] Test EGG resolves: `resolveCurrentEgg()` returns sim EGG for `?egg=sim` and `/sim` path
- [ ] Test engine integration: `POST /sim/load` → `POST /sim/start` → `GET /sim/status` returns running
- [ ] Test pause/resume cycle: start → pause → status=paused → resume → status=running
- [ ] Unskip existing tests in `tests/hivenode/test_sim_routes.py` that were blocked on TASK-071
- [ ] All existing sim frontend tests still pass (`browser/src/apps/sim/__tests__/`)

## Key Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\FlowDesigner.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\adapters\api-client.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\adapters\ApiClientContext.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\canvasAdapter.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\index.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\code.egg.md`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\sim.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\schemas_sim.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\des\engine.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\des\core.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\des\ledger_adapter.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_sim_routes.py`

## Smoke Test
- [ ] `localhost:5174/?egg=sim` renders flow designer with toolbar, canvas, node palette
- [ ] Can drag a TASK node onto the canvas
- [ ] `POST http://localhost:8420/sim/load` with demo PHASE-IR flow returns 200 + run_id
- [ ] `POST http://localhost:8420/sim/start` returns 200, status shows "running"
- [ ] Click "Simulate" mode button in flow designer → simulation starts (uses LocalDESEngine as fallback if backend unreachable)

## Model Assignment
sonnet

## Constraints
- Do not rewrite FlowDesigner.tsx or any existing sim component — wrap and wire only
- No file over 500 lines
- CSS: `var(--sd-*)` only
- No stubs — every function fully implemented
- Phase 1 must work independently of Phase 2 (frontend loads even if backend is down, uses LocalDESEngine)
- Keep `_engines` dict in sim.py for now (production state manager is future work)
- Do not modify `engine/des/` core files — only import and call them from routes

## Source
Q88N-direct, 2026-03-15
