# TASK-EXPLORE-001: Productivity Suite Readiness Audit — COMPLETE

**Status:** COMPLETE
**Model:** Opus 4.6 (coordinating), Explore agents (research)
**Date:** 2026-04-05

---

## 1. ShiftCenter Shell and Panes

### Built and Functional (14 primitives)

| Primitive | Entry Point | Lines | Verdict |
|-----------|-------------|-------|---------|
| text-pane (SDEditor) | `browser/src/primitives/text-pane/SDEditor.tsx` | 917 | Full markdown editor, collaborative diff, speech synthesis |
| terminal (TerminalApp) | `browser/src/primitives/terminal/TerminalApp.tsx` | 245 | Chat interface, command routing, provider switching |
| tree-browser | `browser/src/primitives/tree-browser/TreeBrowser.tsx` | 185 | File explorer, context menus, lazy loading |
| efemera-connector | `browser/src/primitives/efemera-connector/EfemeraConnector.tsx` | 246 | Channels/Members tabs, WebSocket presence |
| kanban-pane | `browser/src/primitives/kanban-pane/KanbanPane.tsx` | Multi | Card boards, drag-drop, mobile sheet |
| canvas | `browser/src/primitives/canvas/CanvasApp.tsx` | Multi | BPMN editor, shapes, annotations, lasso |
| settings | `browser/src/primitives/settings/` | 3 files | API key manager, model selector, vault sync |
| dashboard | `browser/src/primitives/dashboard/DashboardBar.tsx` | Multi | Currency display, API badges, model chooser |
| progress-pane | `browser/src/primitives/progress-pane/ProgressPane.tsx` | 196 | Stage tracking, item rows, mobile view |
| top-bar | `browser/src/primitives/top-bar/` | Multi | App name, kebab menu, avatar |
| menu-bar | `browser/src/primitives/menu-bar/MenuBarPrimitive.tsx` | Multi | Dropdown menus (File, Edit, View, Help) |
| status-bar | `browser/src/primitives/status-bar/StatusBar.tsx` | Multi | Connection indicator, token info, hivenode URL |
| command-palette | `browser/src/primitives/command-palette/CommandPalette.tsx` | Multi | Fuzzy search, global commands, keybindings |
| code-editor | `browser/src/primitives/code-editor/MonacoApplet.tsx` | Multi | Monaco editor, syntax highlighting, volume support |

### Stubbed / Partially Wired

| Primitive | Entry Point | Lines | Gap |
|-----------|-------------|-------|-----|
| bottom-nav | `browser/src/primitives/bottom-nav/BottomNav.tsx` | ~100 | Renders nothing, no mobile nav |
| processing | `browser/src/primitives/processing/ProcessingCanvas.tsx` | ~100 | Layout only, no pipeline |
| keyboard (SCKeyboard) | `browser/src/primitives/keyboard/SCKeyboard.tsx` | Multi | Touch/physical keyboard exists, not wired to EGGs |
| drawing-canvas | `browser/src/primitives/drawing-canvas/DrawingCanvasApp.tsx` | ~150 | Canvas element, no drawing tools |
| auth (LoginPage) | `browser/src/primitives/auth/LoginPage.tsx` | ~200 | Works with hodeia_auth, offline session survival incomplete |

### Shell Infrastructure (all functional)

| Component | Path | Lines |
|-----------|------|-------|
| Shell.tsx | `browser/src/shell/components/Shell.tsx` | 405 |
| useEggInit.ts | `browser/src/shell/useEggInit.ts` | 195 |
| autosave.ts | `browser/src/shell/autosave.ts` | 160 |
| saveEgg.ts | `browser/src/shell/saveEgg.ts` | 70 |
| eggToShell.ts | `browser/src/shell/eggToShell.ts` | 456 |
| reducer.ts | `browser/src/shell/reducer.ts` | 407 |
| volumeStorage.ts | `browser/src/shell/volumeStorage.ts` | 138 |
| useViewport.ts | `browser/src/shell/useViewport.ts` | 101 |

**Verdict:** 14+ primitives battle-tested. Shell reducer, autosave, EGG inflation solid. Bottom-nav, drawing, and processing are stubbed.

---

## 2. Named Volume System

### Backend (hivenode)

| Component | Path | Lines | Status |
|-----------|------|-------|--------|
| VolumeRegistry | `hivenode/storage/registry.py` | 245 | Built |
| LocalFilesystemAdapter | `hivenode/storage/adapters/local.py` | ~100 | Built |
| CloudAdapter | `hivenode/storage/adapters/cloud.py` | ~180 | Built |
| SyncQueueAdapter | `hivenode/storage/adapters/sync_queue.py` | ~150 | Built |
| BaseVolumeAdapter | `hivenode/storage/adapters/base.py` | ~100 | Built |

### Protocol Support

- **local://** — Direct filesystem ✓
- **home://** — User home directory ✓
- **cloud://** — Remote cloud hivenode (HTTP) ✓
- **session://** — localStorage (browser only) ✓
- **vps://** — NOT FOUND

### Operations: read ✓, write ✓, list ✓, delete ✓ (local), exists ✓

**Verdict:** Built but not fully wired. Cloud writes queue to sync_queue but no UI for conflict resolution. No `vps://` protocol. No bidirectional sync UI.

---

## 3. hivenode Sync

### Sync Infrastructure

| Component | Path | Lines | Status |
|-----------|------|-------|--------|
| SyncQueueWriter | `hivenode/hive_mcp/sync.py` | 218 | Built |
| SyncEngine | `hivenode/sync/engine.py` | 338 | Built |
| SyncWorker | `hivenode/sync/worker.py` | ~200 | Built |
| SyncWatcher | `hivenode/sync/watcher.py` | ~150 | Built |
| SyncOutbox | `hivenode/sync/outbox.py` | ~200 | Built |
| SyncLog | `hivenode/sync/sync_log.py` | ~120 | Built |

### Endpoints

| Endpoint | Status |
|----------|--------|
| `POST /sync/trigger` | Built |
| `GET /sync/status` | Built |
| `GET /sync/conflicts` | Built |
| `POST /sync/resolve` | Built (manual, choose winner) |

**Verdict:** Partially built. Sync queue works, conflict detection exists, manual resolution endpoint implemented. No conflict resolution UI. No three-way merge. No auto-retry on network restoration. Settings sync works (via vault), file-level sync UI missing.

---

## 4. EGG System

### Pipeline (all functional)

| Stage | Path | Lines |
|-------|------|-------|
| parseEggMd | `browser/src/eggs/parseEggMd.ts` | 191 |
| eggInflater | `browser/src/eggs/eggInflater.ts` | 392 |
| eggResolver | `browser/src/eggs/eggResolver.ts` | 193 |
| eggLoader | `browser/src/eggs/eggLoader.ts` | 83 |
| eggWiring | `browser/src/eggs/eggWiring.ts` | 55 |
| eggToShell | `browser/src/shell/eggToShell.ts` | 456 |
| useEggInit | `browser/src/shell/useEggInit.ts` | 195 |

**23 canonical .egg.md files** in `eggs/` — chat, efemera, canvas (3 variants), code, kanban, sim, playground, turtle-draw, build-monitor, monitor, ship-feed, and more.

**30+ app types** registered in `browser/src/apps/index.ts`.

**Verdict:** Fully functional. Write a `.egg.md`, push to `eggs/`, reload → app inflates and renders. No EGG editor UI (manual file edit only). No EGG versioning.

---

## 5. Efemera Notification Layer

### Frontend

| Component | Path | Lines | Status |
|-----------|------|-------|--------|
| WsTransport | `browser/src/primitives/efemera-connector/wsTransport.ts` | 237 | Built |
| useEfemeraConnector | `browser/src/primitives/efemera-connector/useEfemeraConnector.ts` | 514 | Built |
| channelService | `browser/src/primitives/efemera-connector/channelService.ts` | 95 | Built |
| messageService | `browser/src/primitives/efemera-connector/messageService.ts` | 203 | Built |
| presenceService | `browser/src/primitives/efemera-connector/presenceService.ts` | 159 | Built |
| memberService | `browser/src/primitives/efemera-connector/memberService.ts` | 29 | Stub |

### Backend

| Component | Path | Lines | Status |
|-----------|------|-------|--------|
| RelayStore | `hivenode/relay/store.py` | 529 | Built |
| ConnectionManager | `hivenode/relay/ws.py` | 255 | Built |
| Relay Routes | `hivenode/relay/routes.py` | 150+ | Built |

### Notification Surfaces

| Surface | Status |
|---------|--------|
| WebSocket | Built (localhost only, Vercel doesn't proxy WS) |
| Polling fallback | Built (3000ms interval) |
| Push notifications | Missing |
| Email | Missing |
| SMS | Missing |
| Browser Notification API | Missing |
| In-app toast | Missing |

**Verdict:** WebSocket + polling work. Presence, channels, messages flow. No push, email, SMS, toast, or typing indicators.

---

## 6. Auth and Identity

### Frontend

| Component | Path | Lines | Status |
|-----------|------|-------|--------|
| authStore.ts | `browser/src/primitives/auth/authStore.ts` | 150+ | Built |
| LoginPage.tsx | `browser/src/primitives/auth/LoginPage.tsx` | ~200 | Built |
| SetupWizard.tsx | `browser/src/primitives/auth/SetupWizard.tsx` | ~300 | Built |

### hodeia_auth Service

| Component | Path | Lines | Status |
|-----------|------|-------|--------|
| main.py | `hodeia_auth/main.py` | 98 | Built |
| db.py | `hodeia_auth/db.py` | 142 | Built |
| models.py | `hodeia_auth/models.py` | 294 | Built |
| schemas.py | `hodeia_auth/schemas.py` | 315 | Built |
| oauth.py | `hodeia_auth/routes/oauth.py` | 369 | Built |
| token.py | `hodeia_auth/routes/token.py` | 148 | Built |

### Session Persistence

- Token survives reload ✓ (localStorage)
- Token survives hivenode restart ✓ (JWT signed, valid until expiry)
- Token refresh on offline→online ✓ (tryRefreshToken in useEggInit)
- Google OAuth ✓, Microsoft OAuth ✓, Local dev mock ✓

**Verdict:** Mostly functional. No rate limiting, no password reset, no MFA, no session management UI, hardcoded admin secret.

---

## 7. Volume Sync Conflict Handling

### What Exists

- `hivenode/sync/engine.py` — Detects file mod time conflicts
- `hivenode/routes/sync_routes.py` — Conflict tracking API
- SyncLog table — Tracks conflicts with path, source, target, error
- Manual resolution — `POST /sync/resolve` with conflict_id + winner

### What Is Missing

- No conflict viewer UI
- No diff/merge visualization
- No three-way merge
- No conflict notification to user
- No automatic merge strategies

**Verdict:** Backend detects and logs conflicts. Resolution is manual-only (POST request, no UI). Zero frontend components for viewing or resolving conflicts.

---

## 8. Mobile Readiness

### What Exists

| Component | Path | Lines | Status |
|-----------|------|-------|--------|
| useViewport.ts | `browser/src/shell/useViewport.ts` | 101 | Built — breakpoint detection |
| MobileNav.css | `browser/src/shell/components/MobileNav.css` | — | Built — mobile nav styles |
| KanbanMobileSheet | `browser/src/primitives/kanban-pane/KanbanMobileSheet.tsx` | 119 | Built — mobile card view |
| MobileStageView | `browser/src/primitives/progress-pane/MobileStageView.tsx` | 196 | Built — mobile progress |
| ImmersiveNavigator | `browser/src/shell/components/ImmersiveNavigator.tsx` | — | Built — fullscreen mobile nav |
| manifest.json | `browser/public/manifest.json` | 26 | Built — PWA manifest |
| sw.js | `browser/public/sw.js` | 62 | Built — cache-first, network-first |
| SW registration | `browser/src/main.tsx` | — | Wired |
| Viewport meta | `browser/app.html` | — | Set |

### What Is Missing

- Only 16 `@media` queries in entire codebase — most primitives have no mobile breakpoints
- No touch gesture support (except keyboard primitive)
- Bottom-nav renders nothing
- Not tested on real mobile devices

**Verdict:** PWA shell exists. Viewport detection works. Two mobile-specific components exist (kanban, progress). Everything else is desktop-only. A phone user would see a broken layout.

---

## 9. Research Track Readiness

**Research track intent:** We are setting aside a portion of factory capacity for structured experiments. The first experiment is cost modeling — breaking a spec into many small tasks dispatched to Haiku vs fewer larger tasks dispatched to Sonnet, measuring total Three Currencies for equivalent output.

### The DES Engine IS the Experiment Runner

The factory already has a full discrete event simulation engine with parameter sweeps, multi-run replication, confidence intervals, and three-currency ledger integration. It does not need to be built — it needs to be pointed at the factory itself.

### DES Engine Inventory (~4,700 lines)

| Component | Path | Lines | What It Does |
|-----------|------|-------|-------------|
| core.py | `engine/des/core.py` | 708 | Event queue, simulation clock, main loop, process_event() |
| engine.py | `engine/des/engine.py` | 491 | Unified SimulationEngine: load, run, step, checkpoint, fork |
| sweep.py | `engine/des/sweep.py` | 542 | Full factorial parameter sweeps, sensitivity analysis, elasticity |
| replication.py | `engine/des/replication.py` | 585 | Multi-run with CIs, CRN variance reduction, MSER-5 warm-up, paired comparison |
| resources.py | `engine/des/resources.py` | 600 | Capacity-limited resources, 6 queue disciplines, preemption |
| tokens.py | `engine/des/tokens.py` | 578 | Token lifecycle (12 states), registry, batch ops, fork/join |
| distributions.py | `engine/des/distributions.py` | 749 | 14 statistical distributions, pure Python (no numpy/scipy) |
| statistics.py | `engine/des/statistics.py` | 481 | Welford's algorithm, time-weighted metrics, running stats |
| ledger_adapter.py | `engine/des/ledger_adapter.py` | 147 | Maps DES events to Event Ledger with CLOCK/COIN/CARBON |

### API Routes Already Exposed

| Endpoint | Path | Status |
|----------|------|--------|
| `POST /api/des/run` | `hivenode/routes/des_routes.py` | Built — single simulation run |
| `POST /api/des/replicate` | `hivenode/routes/des_routes.py` | Built — multi-run with aggregate CIs |
| `POST /api/des/validate` | `hivenode/routes/des_routes.py` | Built — pre-flight flow check |
| `GET /api/des/status` | `hivenode/routes/des_routes.py` | Built — engine health |

### Experiment Capabilities Already Built

| Capability | Module | Status |
|-----------|--------|--------|
| Full factorial parameter sweep | `sweep.py` → `parameter_sweep()` | Built (Python-only, no API route yet) |
| Paired comparison with CRN | `replication.py` → `compare_configs_paired()` | Built (Python-only) |
| Sensitivity analysis (OAT) | `sweep.py` → `sensitivity_analysis()` | Built (Python-only) |
| Confidence intervals (95%) | `replication.py` → Cornish-Fisher + Welford | Built |
| Deterministic reproducibility | `engine.py` → seeded RNG, explicit event ordering | Built |
| Checkpoint/fork/what-if | `engine.py` → `checkpoint()`, `fork()`, `restore()` | Built |
| Pareto frontier analysis | `engine/optimization/core.py` | Built (430 lines) |

### Per-Task Cost Tracking (Live Dispatch) — HOW IT ACTUALLY WORKS

**The telemetry pipeline captures real API token counts, not estimates.** Here is the verified data path:

```
Anthropic API → response.usage (real token counts)
    ↓
Claude Code CLI (--output-format json)
    ↓ JSON: { "usage": { "input_tokens", "output_tokens", "cache_*" } }
claude_cli_subprocess.py:389-442 → json.loads() → extract usage_data
    ↓ real tokens × rate_loader prices
_estimate_cost() → model_rates.yml pricing
    ↓
dispatch.py → send_heartbeat(input_tokens=N, output_tokens=M, cost_usd=$X)
    ↓ POST /build/heartbeat
build_monitor.py:223-348 → accumulates per-task
    ↓
.deia/hive/queue/monitor-state.json (persisted on every heartbeat)
```

**Key code locations:**

| Stage | File | Lines | What Happens |
|-------|------|-------|-------------|
| CLI spawned with JSON mode | `hivenode/adapters/cli/claude_cli_subprocess.py` | 236-237 | `--output-format json` flag set |
| Token extraction from JSON | `hivenode/adapters/cli/claude_cli_subprocess.py` | 389-442 | Parses `usage.input_tokens`, `usage.output_tokens`, `usage.cache_*` |
| Cost calculation | `hivenode/adapters/cli/claude_cli_subprocess.py` | 793-824 | Real tokens × `rate_loader/model_rates.yml` rates |
| Mid-build heartbeat callback | `.deia/hive/scripts/dispatch/dispatch.py` | 608-613 | Fires during execution with real counts |
| Completion heartbeat | `.deia/hive/scripts/dispatch/dispatch.py` | 636-677 | Final token counts + cost emitted |
| Accumulation + persistence | `hivenode/routes/build_monitor.py` | 223-348 | Per-task accumulation, persists to `monitor-state.json` |
| Test coverage | `tests/hivenode/adapters/cli/test_claude_cli_token_tracking.py` | 471 lines | Verifies extraction, cost calc, edge cases |

**Three input buckets tracked separately:** `input_tokens`, `cache_creation_tokens`, `cache_read_tokens`, `output_tokens`

**Cache multipliers:** input=1.0, cache_creation=1.25, cache_read=0.1

**Current totals (from monitor-state.json):**
- $1,515.86 total cost across all dispatches
- 500.8M input tokens
- 3.7M output tokens

### Where the Data Lives — and Where It Doesn't

| Storage | What's there | Queryable? |
|---------|-------------|-----------|
| `monitor-state.json` | Per-task: model, cost_usd, input_tokens, output_tokens, timestamps | NO — flat JSON, full rewrite on every heartbeat, 6,600 lines |
| Event Ledger (`hivenode/ledger/`) | Schema exists with 26 columns (clock_ms, coin_usd, carbon_g, model_id) | YES — SQLAlchemy, but **NOT connected** to heartbeat pipeline |
| Response files (`.deia/hive/responses/`) | Bee self-reported `## Clock / Cost / Carbon` in markdown | NO — bee estimates, not authoritative |

**Critical gap:** The heartbeat pipeline writes to `monitor-state.json` only. The Event Ledger has the right schema but `build_monitor.py` and `dispatch.py` never call `write_event()`. Real data goes to a flat file; the queryable database sits empty.

### What Needs Wiring

1. **Connect heartbeat → ledger** (~50 lines) — `build_monitor.py` calls `LedgerWriter.write_event()` on each heartbeat with real token counts, model_id, cost_usd, carbon_g
2. **Expose sweep/sensitivity as API routes** (~50 lines) — Add `POST /api/des/sweep` wrapping `parameter_sweep()`, `POST /api/des/sensitivity` wrapping `sensitivity_analysis()`
3. **Model bee dispatch as a PHASE-IR Resource** (~100 lines) — Define Haiku and Sonnet as resources with `cost_per_use`, model token consumption as a distribution parameter
4. **Build the factory flow** (~50 lines) — A PHASE-IR flow representing: spec_source → dispatch_node (resource=haiku|sonnet) → response_sink

### Research Track Verdict

**The DES engine can run the cost experiment today** with minor adaptation. The telemetry pipeline captures real data. The critical missing link is that real data goes to a flat JSON file instead of the queryable Event Ledger.

**Priority zero for research track:** Wire `build_monitor.py` → `LedgerWriter` so every heartbeat becomes a queryable ledger event. Then the DES engine can be calibrated against real factory data.

---

## Gap Priority List — Top 10

Ordered by dependency (what must be built first for anything else to work):

| # | Gap | Impact | Effort | Blocks |
|---|-----|--------|--------|--------|
| 1 | **Conflict resolution UI** | Can't safely edit files offline | 20-30h | Daily use |
| 2 | **Mobile CSS breakpoints** | Phone renders broken | 40-60h | Mobile use |
| 3 | **Notification toast/push** | Users miss messages, presence invisible | 15-25h | Real-time collab |
| 4 | **DES sweep API route + factory flow model** | DES engine exists but sweep not exposed as HTTP endpoint | 2-4h | Research track |
| 5 | **Sync status indicator** | Silent sync failures | 8-12h | Daily use confidence |
| 6 | **EGG editor UI** | Non-technical users can't customize | 30-50h | Self-service |
| 7 | **Rate limiting + session mgmt** | Login brute-force risk, no device revocation | 10-15h | Security |
| 8 | **Three-way merge** | Simultaneous edits lose one person's work | 20-30h | Multi-device |
| 9 | **Typing indicators** | Stubbed, no real-time feedback | 5-8h | Chat UX |
| 10 | **vps:// protocol** | No volume protocol for VPS-hosted storage | 10-15h | Infrastructure |

---

## Files Modified

None. Research only.

## Test Results

N/A — no code written.

## Build Verification

N/A — no code written.

## Acceptance Criteria

- [x] Survey shell and panes — 14 functional, 5 stubbed/partial
- [x] Survey named volume system — 4 protocols, read/write/list/delete, no vps://
- [x] Survey hivenode sync — engine built, conflict detection built, no resolution UI
- [x] Survey EGG system — fully functional pipeline, 23 EGGs, 30+ app types
- [x] Survey efemera notifications — WS + polling work, no push/email/SMS/toast
- [x] Survey auth and identity — JWT + OAuth functional, no MFA/rate limiting
- [x] Survey conflict handling — detection built, reconciliation missing
- [x] Survey mobile readiness — PWA shell exists, 16 @media queries, not usable
- [x] Survey research track readiness — DES engine IS the experiment runner, ~200 lines of glue to wire sweep API + factory flow model

## Clock / Cost / Carbon

(Platform-populated from build monitor telemetry. Do not estimate manually.)

## Issues / Follow-ups

1. **Wire heartbeat → ledger (priority zero for research track)** — Real token counts from the API are captured and stored in `monitor-state.json`, but never written to the queryable Event Ledger. One call to `LedgerWriter.write_event()` in `build_monitor.py` fixes this. Without it, $1,515.86 of real cost data is trapped in a flat JSON file.
2. **DES sweep API route + factory PHASE-IR flow model** — Turns the existing 4,700-line DES engine into a factory cost simulator with ~200 lines of glue
3. Conflict resolution UI is the highest-impact gap for daily use
4. Mobile is a large surface area — consider mobile-specific EGG variants rather than retrofitting all 14 primitives
5. Response file `## Clock / Cost / Carbon` sections are bee self-reports (estimates). The authoritative data is in the heartbeat pipeline → `monitor-state.json`. These are two separate data streams and should not be confused.
