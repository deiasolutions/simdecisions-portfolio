# INVESTIGATION REPORT: Full Repo Comparison Diagnostic

**Prepared by:** Q33N (Claude)
**Date:** 2026-03-14
**Scope:** Compare shiftcenter (new) against platform/efemera + platform/simdecisions-2 (old)
**Mode:** READ ONLY — no files were modified

---

## Area 1: PHASE-IR Primitives

**Old:** `platform/efemera/src/efemera/phase_ir/` — 23 files, 6,499 lines
**New:** `shiftcenter/engine/phase_ir/` — 15 files, 4,956 lines

| Old file | Old lines | New file | New lines | Verdict | What's missing |
|---|---|---|---|---|---|
| `__init__.py` | 1 | `__init__.py` | 29 | CHANGED | New exports all 11 primitives |
| `primitives.py` | 146 | `primitives.py` | 146 | IDENTICAL | All 11 core primitives |
| `expressions/__init__.py` | 72 | `expressions/__init__.py` | 72 | IDENTICAL | — |
| `expressions/evaluator.py` | 350 | `expressions/evaluator.py` | 350 | IDENTICAL | — |
| `expressions/lexer.py` | 250 | `expressions/lexer.py` | 250 | IDENTICAL | — |
| `expressions/parser.py` | 355 | `expressions/parser.py` | 355 | IDENTICAL | — |
| `expressions/types.py` | 163 | `expressions/types.py` | 163 | IDENTICAL | — |
| `bpmn_compiler.py` | 536 | `bpmn_compiler.py` | ~536 | PORTED | — |
| `formalism.py` | 399 | `formalism.py` | ~399 | PORTED | — |
| `mermaid.py` | 423 | `mermaid.py` | ~416 | PORTED | Minor diff (-7 lines) |
| `node_types.py` | 705 | `node_types.py` | ~705 | PORTED | — |
| `pie.py` | 546 | `pie.py` | ~546 | PORTED | — |
| `schema.py` | 243 | `schema.py` | ~243 | PORTED | — |
| `validation.py` | 614 | `validation.py` | ~607 | PORTED | Minor diff (-7 lines) |
| `validate_schema.py` | 140 | — | — | NOT PORTED | JSON Schema validator (Draft 2020-12) |
| `cli.py` | 578 | — | — | NOT PORTED | 13-subcommand CLI toolchain |
| `__main__.py` | 4 | — | — | NOT PORTED | CLI entry point |
| `expressions.py` | 61 | — | — | NOT PORTED | Re-export shim (redundant) |
| `models.py` | 82 | — | — | NOT PORTED | SQLAlchemy ORM (FlowRecord, FlowVersion) |
| `schema_routes.py` | 187 | — | — | NOT PORTED | FastAPI CRUD routes for flows |
| `trace.py` | 420 | — | — | NOT PORTED | 25 trace event types, JSONL export |
| `trace_routes.py` | 128 | — | — | NOT PORTED | FastAPI routes for trace queries |
| `validation_routes.py` | 96 | — | — | NOT PORTED | FastAPI route for validation |

**NOT ported: 8 files, ~1,543 lines** (CLI, DB models, FastAPI routes, trace system, JSON Schema validator)
**Domain vocabulary YAML files** (biology.vocab.yaml, etc.) also NOT ported.
**Porting: ~76% by lines**

---

## Area 2: DES Engine

**Old:** `platform/efemera/src/efemera/des/` — 18 files, 7,806 lines
**New:** `shiftcenter/engine/des/` — 18 files, 7,710 lines

| Old file | Old lines | New file | New lines | Verdict | What's missing |
|---|---|---|---|---|---|
| `__init__.py` | 8 | `__init__.py` | 31 | CHANGED | Expanded exports |
| `core.py` | 673 | `core.py` | 673 | IDENTICAL* | EventQueue, SimClock, EngineState, load_flow, 4 handlers |
| `engine.py` | 481 | `engine.py` | 481 | IDENTICAL* | Full SimulationEngine API |
| `tokens.py` | 578 | `tokens.py` | 578 | IDENTICAL* | 12-state FSM, TokenRegistry |
| `resources.py` | 600 | `resources.py` | 600 | IDENTICAL* | ResourceManager, 6 queue disciplines, preemption |
| `statistics.py` | 481 | `statistics.py` | 481 | IDENTICAL* | Welford, time-weighted, Little's Law |
| `dispatch.py` | 445 | `dispatch.py` | 445 | IDENTICAL* | Event dispatch logic |
| `distributions.py` | 749 | `distributions.py` | 749 | IDENTICAL* | RNGManager, 8 distribution types |
| `edges.py` | 420 | `edges.py` | 420 | IDENTICAL* | Edge evaluation, JoinTracker |
| `generators.py` | 276 | `generators.py` | 276 | IDENTICAL* | Token generators |
| `checkpoints.py` | 430 | `checkpoints.py` | 430 | IDENTICAL* | Save/restore/list/delete |
| `pools.py` | 432 | `pools.py` | 432 | IDENTICAL* | Resource pools |
| `replay.py` | 289 | `replay.py` | 289 | IDENTICAL* | Event replay |
| `replication.py` | 585 | `replication.py` | 585 | IDENTICAL* | Multi-run with CI aggregation |
| `sweep.py` | 542 | `sweep.py` | 542 | IDENTICAL* | Parameter sweep |
| `trace_writer.py` | 350 | `trace_writer.py` | 350 | IDENTICAL* | Trace buffer |
| `loader_v2.py` | 202 | `loader_v2.py` | 202 | IDENTICAL* | Flow loader v2 |
| `engine_routes.py` | 265 | — | — | NOT PORTED | FastAPI routes for DES |
| — | — | `ledger_adapter.py` | 146 | NEW | 3-currency ledger bridge |

*"IDENTICAL" = same line count, same logic. Only change is import paths (`..des` → `engine.des`).

**NOT ported: 1 file, 265 lines** (engine_routes.py — FastAPI routes)
**Porting: ~97% by lines**

---

## Area 3: Other Efemera Engines (NOT expected to be ported)

| Engine | Directory | Files | Lines | Notes |
|---|---|---|---|---|
| Production | `efemera/production/` | 20 | 5,234 | Production scheduling engine |
| Tabletop | `efemera/tabletop/` | 12 | 6,200 | Tabletop simulation engine |
| Optimization | `efemera/optimization/` | 10 | 6,785 | OR-Tools optimization |
| Surrogates | `efemera/surrogates/` | 28 | 8,999 | Surrogate model pipeline |
| Pheromones | `efemera/pheromones/` | 15 | 6,624 | Pheromone load balancing |
| **TOTAL** | | **85** | **33,842** | **None ported (by design)** |

These are future-phase engines. Not expected in shiftcenter yet.

---

## Area 4: Canvas / SimDecisions UI

**Old:** `simdecisions-2/src/components/canvas/` — 50 files, 6,300 lines
**New:** `shiftcenter/browser/src/primitives/canvas/` — 18 files, 2,658 lines

All 18 new files created 2026-03-14 17:33–17:54 (single-session port by another Claude instance).
Same React Flow version (`@xyflow/react ^12.10.1`) in both repos.

**Ported (9 node types + core):**
CanvasApp.tsx (392), canvas.css (198), canvasTypes.ts (80), edgeHandles.ts (82), CustomEdge.tsx (124), nodes.css (619), StartNode, EndNode, TaskNode, DecisionNode, CheckpointNode, ParallelSplitNode, ParallelJoinNode, QueueNode, GroupNode, BadgeStrip.tsx, plus 2 test files (526 lines)

**NOT ported (13 node types + subsystems, ~3,642 lines):**
- **BPMN nodes** (6 types): BPMNNode.tsx (189) + bpmn-styles.css (353) — Start, End, Task, Gateway, Subprocess, Event
- **Annotation nodes** (5 types + 2 tests, ~568 lines): Ellipse, Image, Line, Rect, Text, Callout, StickyNote
- **Animation system** (6 components, 749 lines): CheckpointFlash, NodePulse, QueueBadge, ResourceBar, SimClock, TokenAnimation
- **Lasso selection** (107 lines) + BroadcastChannel sync (213 line test)
- **Custom ZoomControls** (96 + 53 CSS) — new uses React Flow built-in Controls
- **AnnotationBadge** (58 + 121 CSS)
- **Edge glow filters** for playback states (drop-shadow)
- **10 old test files** not ported (2,348 lines → 2 new test files, 526 lines)

**Also related (not in canvas/ scope):** Properties panel at `panels/properties/` — 16 files, 2,669 lines. NOT ported.

**Porting: ~42% by lines (PORTED TODAY, partial)**

---

## Area 5: Shell Components

**Old:** `simdecisions-2/src/components/shell/` — 47 source files (excl. tests), ~7,932 lines
**New:** `shiftcenter/browser/src/shell/` — 28 source files, ~5,850 lines

**Ported (JS→TS rewrite, 23 files):**
- Core reducer split into 4 files (reducer.ts + actions/layout.ts + actions/branch.ts + actions/lifecycle.ts = 970 lines). All 47 old actions present + 2 new (DELETE_CELL, UPDATE_LAYOUT_DIMENSIONS).
- shell.utils.js (435) → utils.ts (541) — expanded
- shell.constants.js (245) → constants.ts (62) + shell-themes.css (670) — CSS extracted
- shell.css (850) → split across 4 CSS files (1,109 total)
- 17 UI components ported: Shell, AppFrame, AppletShell, ChromeBtn, ContextMenu (merged PaneContextMenu), EmptyPane, FloatPaneWrapper, PaneChrome, PaneContent, ShellNodeRenderer, SplitContainer, SplitDivider, SplitTree, TabbedContainer, TripleSplitContainer, DropZone, SwapTarget

**NOT ported (13+ files, ~2,450 lines):**
- `MenuBar.tsx` (430) — top menu bar with dropdowns
- `ShellTabBar.tsx` (233) — workspace tab bar
- `WorkspaceBar.jsx` (243) — workspace switcher
- `GovernanceProxy.tsx` (159) — governance gate UI
- `useTerminal.ts` (611) — old xterm.js integration (replaced by new terminal primitive)
- `HiveHostPanes.jsx` (541) — decomposed into smaller components
- `shell.context.js` (186) — replaced by hook-based approach
- `shell.import.js` (109) — dynamic import orchestrator
- `PaneMenu.jsx` (110), `ScrollToBottom.tsx` (33), `NotificationModal.tsx` (63)
- `HighlightOverlay.tsx` (15), `ShortcutsPopup.tsx` (26), `LayoutSwitcher.tsx` (33)
- `PinnedPaneWrapper.jsx` (72), `SpotlightOverlay.jsx` (92), `dragDropUtils.ts` (61)
- `MaximizedOverlay.jsx` (26)

**7 new files added** (types.ts, merge-helpers.ts, eggToShell.ts, useEggInit.ts, volumeStorage.ts, ThemePicker.tsx, appRegistry.ts)

**Porting: ~74% by lines (PORT + ENHANCE)**

---

## Area 6: Efemera Chat / Frontend

**Old:** `platform/efemera/frontend/src/` — ~130 source files, ~35,463 lines (Vite + React + TypeScript)
**New:** ZERO files ported

Two major subsystems in the old frontend:

**Chat/Communication (~6,800 lines, ~40 files):**
- `pages/ChatPage.tsx` (617) — main chat page
- `components/ChatMessage.tsx` (248) — message rendering
- `components/MessageInput.tsx` (163) — compose input
- `components/ChannelSidebar.tsx` (70) — channel list
- `components/MembersPanel.tsx` (47) — online members
- `components/CommandPopup.tsx` (85) — slash command popup
- `components/Sidebar.tsx` (283) — full sidebar
- `adapters/api-client.ts` (727) — typed REST client
- `lib/ws.ts` (149) — WebSocket client
- Plus 9 pages (Auth, Dashboard, Docs, Landing, Onboarding, Settings, SimDecisions, FlowDesigner)
- Plus libs (commands.ts, auth.ts, theme.ts, icons.tsx)

**Flow Designer (~17,000 lines, ~80 files):**
- React Flow-based visual simulation editor
- Animation, playback, collaboration, tabletop, checkpoints
- Comparison view, file import/export, responsive modes
- Would become a pane applet if ported

ShiftCenter's chat is being **built from scratch** using existing primitives (terminal + text-pane + tree-browser) rather than porting the old monolithic frontend.

**Porting: 0% — REBUILT using different architecture**

---

## Area 7: RAG / Embeddings / Context

**Old:** 4 separate subsystems in `platform/efemera/src/efemera/` — ~5,195 lines total

**Module 1: `rag/`** — Core RAG (783 lines):
engine.py (181), routes.py (153), indexer.py (136), synthesizer.py (121), search.py (72), embedder.py (58), models.py (55)

**Module 2: `indexer/`** — Document Indexer Service (3,060 lines):
storage.py (462), metrics_updater.py (354), chunker.py (323), cloud_sync.py (318), indexer_service.py (300), reliability.py (295), sync_daemon.py (266), markdown_exporter.py (194), embedder.py (180), models.py (178), scanner.py (163)

**Module 3: `entities/`** — Entity Embeddings (1,234 lines):
vectors.py (685), embeddings.py (280), voyage_embedding.py (141), embedding_routes.py (128)

**Module 4: `bok/`** — BOK Services (142 lines):
embedding_service.py (78), rag_service.py (64)

**New:** `shiftcenter/hivenode/rag/` — 1,098 lines (EXISTS)

| Old (rag/) | Old lines | New (hivenode/rag/) | New lines | Verdict |
|---|---|---|---|---|
| engine.py | 181 | engine.py | 430 | PORTED, EXPANDED |
| routes.py | 153 | routes.py | 164 | PORTED |
| indexer.py | 136 | chunkers.py | 279 | PORTED, RENAMED |
| embedder.py | 58 | embedder.py | 80 | PORTED |
| models.py | 55 | schemas.py | 115 | PORTED, RENAMED |
| search.py | 72 | (in engine.py) | — | MERGED |
| synthesizer.py | 121 | — | — | NOT PORTED |

**NOT ported (~4,470 lines):**
- Full indexer service (3,060) — cloud sync, reliability, metrics, daemon
- Entity vector/embedding system (1,234) — vectors, Voyage AI
- BOK services (142), LLM synthesizer (121)

**Porting: ~21% by lines (core pipeline ported, advanced features not)**

---

## Area 8: Auth / ra96it

**Old:** Auth code scattered in platform/ (basic JWT, SHA-256 passwords)
**New:** `shiftcenter/ra96it/` — 17 files, 1,327 lines

| Component | Old | New | Notes |
|---|---|---|---|
| Password hashing | SHA-256 | bcrypt | UPGRADED |
| JWT algorithm | HS256 | RS256 | UPGRADED |
| MFA | None | TOTP-based | NEW |
| Refresh tokens | None | Yes | NEW |
| Audit logging | None | Yes | NEW |
| Cross-app SSO | None | Yes | NEW |

**Verdict: REWRITE as standalone microservice.** Not a port — completely redesigned with modern security practices.

---

## Area 9: Privacy / PII / Governance

**New (built from scratch in shiftcenter):**

| Module | Files | Lines | Source |
|---|---|---|---|
| `hivenode/governance/gate_enforcer/` | 5 | 1,070 | gate_enforcer concept PORTED from old, implementation ENHANCED |
| `hivenode/privacy/` | 7 | 1,029 | Entirely NEW |
| `browser/src/infrastructure/` | TS files | — | Frontend governance integration |
| **Total** | **12+** | **2,099** | |

Old repo had GateEnforcer concept + ethics.yml. New repo has full implementation with:
- 4-level enforcement (models, ethics_loader, grace, overrides, enforcer)
- Privacy pipeline (hasher, purger, consent, training_store, pipeline, redactor, audit_trail)
- TASaaS content moderation from old: NOT ported

---

## Area 10: Hivenode / Backend Services

**New:** `shiftcenter/hivenode/` — 114 Python files, 18,716 lines

**NOT a port** of efemera backend. ShiftCenter hivenode is a new application shell backend with:
- FastAPI application server
- Shell command execution (allowlisted)
- AI chat routing (multi-provider)
- File/volume management
- Queue system
- RAG pipeline (hivenode/rag/ — core ported, advanced features pending)
- Governance enforcement
- Privacy pipeline

The old efemera backend was Express.js + PostgreSQL for chat/messaging. Zero overlap with hivenode's architecture.

---

## Area 11: Tests

| Repo | Python test files | TypeScript test files | Total |
|---|---|---|---|
| **Old (efemera)** | 272 | — | 272 |
| **Old (simdecisions-2)** | — | not counted | — |
| **New (shiftcenter)** | 120 | 126 | 246 |

**All new tests.** The shiftcenter tests are written for new code, not ports of old tests. Test methodology differs:
- Old: pytest for Python backend
- New: pytest for Python + Vitest for TypeScript, with E2E integration tests

---

## Final Summary

| Area | Old total lines | New total lines | % Ported | % Built New | % Missing | Critical gaps |
|---|---|---|---|---|---|---|
| 1. PHASE-IR | 6,499 | 4,956 | 76% | 0% | 24% | CLI, trace, DB models, routes, JSON Schema validator |
| 2. DES Engine | 7,806 | 7,710 | 97% | 2% | 3% | engine_routes.py only |
| 3. Other Engines | 33,842 | 0 | 0% | 0% | N/A | Not expected to be ported yet |
| 4. Canvas | 6,300 | 2,658 | 42% | 0% | 58% | 13 node types, animations, BPMN nodes, lasso, annotations |
| 5. Shell | ~7,932 | ~5,850 | 74% | 0% | 26% | MenuBar, ShellTabBar, WorkspaceBar, GovernanceProxy |
| 6. Efemera Frontend | ~35,463 | 0 | 0% | 0% | 100% | Entire chat app (rebuilt from scratch with primitives) |
| 7. RAG | ~5,195 | 1,098 | 21% | 0% | 79% | Indexer service, entity vectors, Voyage AI, BOK, synthesizer |
| 8. Auth | ~500 | 1,327 | 0% | 100% | 0% | Rewrite — all features present + enhanced |
| 9. Privacy/Gov | ~300 | 2,099 | partial | 90% | 0% | gate_enforcer concept ported, rest is new |
| 10. Hivenode | 0 | 18,716 | N/A | 100% | N/A | New backend, not a port |
| 11. Tests | ~272 files | 246 files | 0% | 100% | N/A | All new tests for new code |

---

## Three Key Questions

### 1. Total line count of code in old repos that SHOULD have been ported but WASN'T?

| Area | Lines not ported | Notes |
|---|---|---|
| PHASE-IR | ~1,543 | CLI, models, routes, trace, validator |
| DES Engine | 265 | engine_routes.py |
| Canvas | ~3,642 | BPMN nodes, annotations, animations, lasso, zoom controls |
| Shell | ~2,450 | MenuBar, tabs, workspace, governance proxy, overlays |
| Efemera Frontend | ~35,463 | Entire chat UI (being rebuilt differently) |
| RAG | ~4,470 | Indexer service, entity vectors, Voyage AI, BOK, synthesizer |
| **TOTAL** | **~47,833** | |

**However:** ~35,463 of that (efemera frontend) is being intentionally rebuilt using ShiftCenter primitives rather than ported. If you exclude that, **~12,370 lines** of backend/engine code should have been ported but wasn't.

### 2. Total line count of code in new repo that was BUILT NEW when a port existed?

| Area | New lines built fresh | Port existed? |
|---|---|---|
| Canvas | 2,658 | Yes (6,300 lines in old — 42% ported today) |
| Auth (ra96it) | 1,327 | Partial (old auth was simpler) |
| Privacy pipeline | 1,029 | No (new concept) |
| Hivenode backend | 18,716 | No (new architecture) |
| **TOTAL with port available** | **~3,985** | Canvas + Auth |

### 3. Top 5 most critical missing pieces

1. **RAG advanced pipeline (~4,470 lines not ported)** — Core RAG is ported (hivenode/rag/, 1,098 lines), but the full indexer service (3,060 lines — cloud sync, reliability, metrics, daemon), entity vector system (1,234 lines — Voyage AI, entity embeddings), BOK services (142 lines), and LLM synthesizer (121 lines) are all missing. Critical for production-grade AI-assisted features.

2. **Canvas node types + animations (~3,642 lines not ported)** — 9 of 22 node types ported today. Missing: 6 BPMN nodes (189 + 353 CSS), 5 annotation nodes (~568 lines), animation system (6 components, 749 lines), lasso selection (107), zoom controls (149). Plus properties panel (2,669 lines) as a companion concern. Critical for the SimDecisions visual designer.

3. **Shell chrome components (~2,450 lines)** — MenuBar (430), ShellTabBar (233), WorkspaceBar (243), GovernanceProxy (159), useTerminal/xterm (611), PaneMenu (110), SpotlightOverlay (92), plus notification, shortcuts, layout switcher, pinned pane, and drag-drop utilities. These provide the application chrome that makes ShiftCenter feel like a complete application.

4. **PHASE-IR CLI toolchain (578 lines)** — 13 subcommands (validate, lint, export, compile, decompile, pack, unpack, inspect, rules, node-types, eval, formalism, init). Critical for developer workflow and CI/CD pipeline validation.

5. **PHASE-IR trace system (548 lines)** — 25 trace event types, execution tracing, JSONL export/import, trace API routes. Critical for simulation debugging and analysis.

---

**END OF REPORT**
