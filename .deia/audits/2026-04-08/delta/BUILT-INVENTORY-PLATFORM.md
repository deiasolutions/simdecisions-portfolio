# Built Inventory — Platform Repo

**Audit Date:** 2026-04-08
**Target:** `C:\Users\davee\OneDrive\Documents\GitHub\platform\`
**Audited By:** DELTA Queen (Watchdog Restart)
**Source Documents:**
- REPO-GROUND-TRUTH-2026-03-05.md (master inventory)
- PLATFORM-OVERVIEW.md (product spec)
- Direct filesystem scans

---

## Summary Statistics

| Category | Count | Notes |
|----------|-------|-------|
| Source files (Python) | ~850 (efemera) + 194 (src) | Excludes simdecisions-2 frontend |
| Source files (TS/TSX) | ~835 (simdecisions-2) | React/Vite frontend |
| ADR/Spec documents | 30+ | Implementation ADRs 001-013, speculative 014-023 |
| Test suites | 15+ | Event Ledger (42), DES (820+), Surrogates (252), Dialects (306), etc. |
| Legacy directories | 7 | flappy-*, simdecisions (v1), grandvision, hivemind, canonical |

---

## Core Simulation Engine — BUILT

### efemera/src/efemera/des/

**Type:** Python Module (Discrete Event Simulation Engine)
**Files:**
- engine.py (~800 LOC) — main DES loop, event queue, virtual time
- loader_v2.py (~400 LOC) — PHASE-IR v2.0 loader (nodes/edges as objects)
- checkpoints.py (~350 LOC) — Alterverse branching, fork/replay
- seeded_rng.py (~200 LOC) — reproducible randomness
- statistics.py (~250 LOC) — aggregate metrics, distributions

**Status:** WORKING
**Tests:** 820+ passing
**Description:** Discrete Event Simulation engine with virtual time, seeded RNG, checkpoint/replay, and Alterverse branching for counterfactual analysis.

**Dependencies:**
- numpy, scipy (statistical distributions)
- efemera.events (Event Ledger writer)
- efemera.phase_ir (process specification parser)

**Entry Point:** `efemera.execution.run_simulation()`, FastAPI `/simulation/run` endpoint

**Notes:** Core differentiator. Supports 10,000x speedup over wall-clock execution. Full reproducibility via seed capture.

---

### efemera/src/efemera/production/

**Type:** Python Module (Production Execution Engine)
**Files:**
- engine.py (~600 LOC) — wall-clock execution, restart survival
- task_queue.py (~300 LOC) — async task management
- integrations.py (~400 LOC) — external API adapters

**Status:** PARTIAL
**Tests:** 64 passing, 1 failing (restart survival edge case)
**Description:** Production mode engine for real-time execution against live integrations.

**Dependencies:**
- asyncio, aiohttp
- efemera.events (Event Ledger)
- efemera.oracle (decision routing)

**Entry Point:** `/production/execute` API endpoint

**Notes:** Production engine has restart survival logic, but one test fails on edge case (process dies mid-task). Needs bug fix before prod deployment.

---

### efemera/src/efemera/tabletop/

**Type:** Python Module (Tabletop Walkthrough Engine)
**Files:**
- engine.py (~450 LOC) — LLM-guided step-by-step execution
- prompts.py (~200 LOC) — prompt templates for walkthrough
- state_manager.py (~150 LOC) — interactive state snapshots

**Status:** WORKING
**Tests:** Yes (count not specified in ground truth)
**Description:** LLM-interpreted tabletop mode for interactive process walkthroughs without code.

**Dependencies:**
- efemera.llm_providers (unified LLM interface)
- efemera.events (Event Ledger)

**Entry Point:** `/tabletop/start` API endpoint

**Notes:** Onboarding mode. Cheapest way to test a process before coding it.

---

### efemera/src/efemera/optimization/

**Type:** Python Module (Constraint Optimization Engine)
**Files:**
- engine.py (~500 LOC) — OR-Tools integration, Pareto frontier
- translator.py (~400 LOC) — PHASE-IR → constraint model
- objectives.py (~250 LOC) — cost/time/carbon objective functions

**Status:** WORKING
**Tests:** Yes (count not specified)
**Description:** Optimization engine that translates process specs to constraint models and finds Pareto-optimal configurations.

**Dependencies:**
- ortools (Google OR-Tools)
- efemera.phase_ir

**Entry Point:** `/optimization/solve` API endpoint

**Notes:** Returns Pareto frontier (cost vs. speed vs. carbon). Proofs, not heuristics.

---

## Governance Runtime — BUILT

### efemera/src/efemera/events/

**Type:** Python Module (Event Ledger)
**Files:**
- ledger.py (~600 LOC) — 14-column append-only ledger, WAL mode, checksummed
- writer.py (~300 LOC) — async writer with batch flush
- query.py (~400 LOC) — temporal queries, aggregations

**Status:** WORKING
**Tests:** 42 passing
**Description:** Append-only Event Ledger (ADR-001). 14 columns: timestamp, event_type, entity_id, domain, action, cost_usd, cost_time, cost_carbon, seed, trace_id, parent_id, payload, checksum, ledger_version.

**Dependencies:**
- sqlite3 (WAL mode)
- hashlib (SHA-256 checksums)

**Entry Point:** All engines write to ledger via `ledger.write()`

**Notes:** Foundation of audit trail. Every action in every execution mode writes here. Checksummed for integrity.

---

### efemera/src/efemera/gate_enforcer/

**Type:** Python Module (5-Disposition Policy Engine)
**Files:**
- enforcer.py (~700 LOC) — main gate logic, disposition routing
- dispositions.py (~200 LOC) — PERMIT, DENY, GRACE, REVIEW, QUARANTINE
- ethics_loader.py (~150 LOC) — loads ethics rules from YAML

**Status:** WORKING
**Tests:** Yes (count not specified)
**Description:** GateEnforcer (ADR-014/GOV-001). Every decision passes through gate. 5 dispositions. Ethics rules loaded from config.

**Dependencies:**
- efemera.events (logs gate decisions)
- pydantic (rule schemas)

**Entry Point:** `gate_enforcer.check()` called by all engines before critical actions

**Notes:** Governance layer. No action bypasses the gate. Supports grace periods and mandatory review for high-stakes decisions.

---

### efemera/src/efemera/entities/

**Type:** Python Module (Four-Vector Profiling)
**Files:**
- profiles.py (~500 LOC) — α, σ, π, ρ computation per domain
- aggregator.py (~300 LOC) — compute profiles from Event Ledger
- scoring.py (~250 LOC) — weighted scoring for task assignment

**Status:** WORKING
**Tests:** Yes (count not specified)
**Description:** Four-Vector Entity Profiles (ADR-003). Every entity profiled on: Autonomy (α), Quality (σ), Preference (π), Reliability (ρ). Computed per-domain from ledger data.

**Dependencies:**
- efemera.events (reads ledger for profile computation)
- numpy (statistical aggregations)

**Entry Point:** `entities.get_profile(entity_id, domain)`, used by oracle routing and team composition

**Notes:** Profiles drive task assignment and oracle tier routing.

---

### efemera/src/efemera/oracle/

**Type:** Python Module (Oracle Tier System)
**Files:**
- router.py (~600 LOC) — tier routing (0-4), VoI calculation
- tribunal.py (~400 LOC) — Tier 3.5 (multi-LLM vote)
- tiers.py (~200 LOC) — tier definitions and cost models

**Status:** WORKING
**Tests:** Yes (count not specified)
**Description:** Oracle Tier System (ADR-004). 5 tiers: 0=cache/logic, 1=fast LLM, 2=capable LLM, 3=Tribunal (3.5=three models vote), 4=human. Routes by Value of Information.

**Dependencies:**
- efemera.llm_providers (multi-LLM support)
- efemera.entities (profiles for routing)

**Entry Point:** `oracle.route_decision(question, context)`, called by all engines for decisions

**Notes:** Tribunal (Tier 3.5) runs three models in parallel, majority vote wins. Tier 4 escalates to human.

---

### efemera/src/efemera/skills/

**Type:** Python Module (Agent Skills Governance)
**Files:**
- registry.py (~500 LOC) — skill certification tiers (-1 to 3)
- sandbox.py (~400 LOC) — skill sandboxing, resource limits
- certification.py (~300 LOC) — skill testing and promotion

**Status:** WORKING
**Tests:** Yes (count not specified)
**Description:** Agent Skills Governance (ADR-005). Skills certified on tiers: -1=quarantined, 0=experimental, 1=safe, 2=trusted, 3=core. Sandboxed execution.

**Dependencies:**
- efemera.events (logs skill invocations)
- subprocess (sandboxed skill execution)

**Entry Point:** `skills.invoke(skill_id, args)`, called by agents

**Notes:** Prevents untrusted skills from harming the system. Certification based on test coverage and audit.

---

### efemera/src/efemera/pheromones/

**Type:** Python Module (Pheromone Signals)
**Files:**
- signals.py (~400 LOC) — 7 signal types (REQUEST, OFFER, CLAIM, COMPLETE, REVIEW, BLOCKED, BROADCAST)
- transport.py (~300 LOC) — file/MCP/Efemera transport layers
- handlers.py (~350 LOC) — signal handlers, routing logic

**Status:** WORKING
**Tests:** Yes (count not specified)
**Description:** Pheromone Signals (ADR-006). 7 signal types for agent-to-agent coordination. Multi-transport (filesystem, MCP, Efemera relay).

**Dependencies:**
- watchdog (file-based transport)
- efemera.events (logs signals)

**Entry Point:** `pheromones.emit(signal_type, payload)`, called by agents for coordination

**Notes:** Enables agent swarms to coordinate without central orchestrator.

---

## Surrogate Models & ML — BUILT

### efemera/src/efemera/surrogates/

**Type:** Python Module (Surrogate Model Pipeline)
**Files:**
- pipeline.py (~600 LOC) — ML model training from Event Ledger
- drift_detector.py (~300 LOC) — model drift detection, retraining triggers
- models.py (~400 LOC) — regression, classification, time-series models

**Status:** WORKING
**Tests:** 252 passing
**Description:** Surrogate Model Pipeline (ADR-012). Trains ML models from Event Ledger data to predict outcomes without full simulation.

**Dependencies:**
- scikit-learn (ML models)
- efemera.events (training data source)

**Entry Point:** `/surrogates/train`, `/surrogates/predict` API endpoints

**Notes:** Enables fast approximations for high-fidelity simulations. Drift detection ensures models stay accurate.

---

## Domain Dialect Compilers — PARTIAL

### efemera/src/efemera/dialects/

**Type:** Python Module (Multi-Domain Compilers)
**Files:**
- bpmn_compiler.py (~500 LOC) — BPMN → PHASE-IR
- sbml_compiler.py (~400 LOC) — SBML (biology) → PHASE-IR
- workflow_yaml_compiler.py (~350 LOC) — Workflow YAML → PHASE-IR
- lsystems_compiler.py (~300 LOC) — L-systems (generative) → PHASE-IR

**Status:** PARTIAL (4/6 compilers built)
**Tests:** 306 passing
**Description:** Domain Dialect Compilers (ADR-013). Compiles external formats to PHASE-IR for simulation.

**Dependencies:**
- lxml (BPMN/SBML parsing)
- pyyaml (Workflow YAML)

**Entry Point:** `/dialects/compile` API endpoint

**Notes:** Terraform and Makefile compilers NOT BUILT. BPMN, SBML, L-systems, Workflow YAML all working.

---

## TASaaS (Terminal Anomaly Scanner) — BUILT BUT NOT WIRED

### efemera/src/efemera/tasaas/

**Type:** Python Module (Terminal Activity Scanning)
**Files:**
- scanner.py (~500 LOC) — terminal command scanning, risk scoring
- rules.py (~300 LOC) — risk rules (destructive commands, credential exposure)
- reporter.py (~200 LOC) — anomaly reports

**Status:** BUILT BUT NOT DEPLOYED
**Tests:** 49 passing
**Description:** Terminal-as-a-Service Anomaly Scanner. Scans terminal commands for risky patterns. NOT WIRED TO OUTPUT CHANNELS — logs to Event Ledger but no alerts sent.

**Dependencies:**
- efemera.events (logs scans)
- re (pattern matching)

**Entry Point:** Intended: terminal middleware. Actual: standalone CLI only.

**Notes:** Code is complete and tested, but not integrated into production terminal service. Requires wiring to notification system.

---

## Build Optimization Engine — BUILT

### efemera/src/efemera/builds/

**Type:** Python Module (Closed-Loop Build Instrumentation)
**Files:**
- optimizer.py (~600 LOC) — 3-currency optimization (CLOCK, COIN, CARBON)
- instrumentation.py (~400 LOC) — build tracing, cost attribution
- metrics.py (~300 LOC) — cost aggregation, reporting

**Status:** WORKING
**Tests:** Yes (count not specified)
**Description:** Build Optimization Engine (ADR-002). Instruments builds, tracks 3 currencies (CLOCK=time, COIN=USD, CARBON=CO2e), optimizes build graph.

**Dependencies:**
- efemera.events (logs build steps)
- networkx (build graph analysis)

**Entry Point:** Build hooks (pytest, npm, docker)

**Notes:** Closed-loop: measures actual build costs, suggests optimizations. Carbon field present but methodology TBD (ADR-015).

---

## Frontend (SimDecisions-2) — BUILT

### simdecisions-2/src/

**Type:** React/TypeScript (Vite)
**Files:** ~835 TS/TSX files
**Key Components:**
- components/canvas/ — ReactFlow node library, animation layer
- stores/ — 14 Zustand stores (scenario, graph, execution, history, etc.)
- pages/ — main UI pages (Designer, Dashboard, Ledger, Settings)
- hooks/ — custom React hooks (useSimulation, useProfile, etc.)

**Status:** WORKING
**Tests:** Multiple (exact count unknown)
**Description:** Full-featured React frontend for SimDecisions. Canvas-based process designer, real-time dashboard, Event Ledger viewer.

**Dependencies:**
- React, ReactFlow, Zustand, Tailwind CSS
- axios (API client)

**Entry Point:** Vite dev server, production build → `dist/`

**Notes:** Well-architected frontend. 14 Zustand stores cleanly separate concerns. Canvas supports drag-drop, annotation layer, node library.

---

## HiveHostShell — BUILT

### src/components/shell/HiveHostShell.jsx

**Type:** React Component (Recursive Pane Manager)
**Files:**
- HiveHostShell.jsx (~800 LOC) — binary split tree, tab system
- TabBar.jsx (~300 LOC) — tab types: hive, designer, browser, ledger
- SplitPane.jsx (~250 LOC) — draggable dividers, depth cap 2

**Status:** WORKING
**Tests:** Unknown
**Description:** Recursive pane manager for split/tabbed multi-app shell. Binary split tree with draggable dividers.

**Dependencies:**
- React
- react-split-pane (divider library)

**Entry Point:** Main app shell (integrated into simdecisions-2 or standalone)

**Notes:** Shell supports infinite recursion (depth cap 2 recommended). Tab types include iframe browser tabs (sandboxed).

---

## Legacy/Orphaned Code — DOCUMENTED

### simdecisions/ (v1)

**Type:** Superseded Python Backend
**Files:** 43 Python files
**Status:** ORPHANED (replaced by simdecisions-2)
**Description:** Original SimDecisions backend before pivot to React frontend + FastAPI.

**Recommendation:** ARCHIVE (historical reference only)

---

### flappy-001/, flappy-002/

**Type:** Experimental Projects
**Files:** 27 files (flappy-001), 13 files (flappy-002)
**Status:** LEGACY
**Description:** Early experiments, unclear purpose (possibly game physics or tutorial).

**Recommendation:** ARCHIVE or DELETE

---

### grandvision/

**Type:** Vision Document Archive
**Files:** 296 KB, markdown + drafts
**Status:** LEGACY
**Description:** Early vision documents and drafts, superseded by ADRs and current specs.

**Recommendation:** ARCHIVE (historical value)

---

### hivemind/

**Type:** Separate Project or Experiment
**Files:** 62 KB, 10 Python files
**Status:** UNKNOWN
**Description:** Unclear if this is intentional secondary repo or abandoned experiment.

**Recommendation:** REVIEW with Q88N before action

---

### canonical/

**Type:** Multi-Domain Archive
**Files:** 2,185 files (mostly .egg.md configs)
**Status:** MIXED (some active, many legacy)
**Description:** Massive archive of EGG configs, specs, and tools. Some actively used, many outdated.

**Recommendation:** REVIEW & MIGRATE (selective extraction to ShiftCenter)

---

## Missing/Speculative Components

These are referenced in ADRs or specs but NOT FOUND in codebase:

### ADR-015: Carbon Methodology

**Status:** SPEC ONLY
**Evidence:** `efemera/src/efemera/carbon/` directory exists, field present in Event Ledger, but no calculation logic found.

**Impact:** Carbon tracking infrastructure exists but methodology not defined.

---

### ADR-023: Efemera Relay

**Status:** SPEC ONLY
**Evidence:** ADR document exists in `.deia/hive/coordination/ADR-023-Efemera-Relay-Architecture.md`, no code found.

**Impact:** Relay architecture designed but not implemented. ShiftCenter hivenode may replace this.

---

### Hash Chain Integrity (EVT-003)

**Status:** NOT FOUND
**Evidence:** GAR-ALPHA spec references `src/simdecisions/runtime/ledger.py` as implemented, but path does not exist.

**Impact:** Event Ledger has checksums but not hash chain linkage between entries.

---

### Moon 1.1 Phases 4-5

**Status:** SPEC ONLY
**Evidence:** Moon 1.1 spec describes cross-pane comms (Phase 4) and Embed API (Phase 5), not implemented.

**Impact:** Cross-pane clipboard and embed API are design docs, not code.

---

## Summary Classification

| Category | Count | Status |
|----------|-------|--------|
| WORKING (complete, tested, wired) | 20+ modules | Core engines, governance, frontend |
| PARTIAL (substantial code, incomplete) | 3 modules | Production engine (1 test failing), Dialects (4/6), TASaaS (not wired) |
| ORPHANED (built but not wired) | 1 module | TASaaS |
| STUB | 0 | None found |
| LEGACY (superseded or abandoned) | 7 directories | simdecisions (v1), flappy-*, grandvision, etc. |
| SPEC ONLY (designed but not built) | 4 features | Carbon methodology, Efemera Relay, Hash Chain, Moon 1.1 P4-5 |

---

## End of Inventory
