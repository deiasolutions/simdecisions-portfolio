# Platform → ShiftCenter Gap Analysis

**Generated:** 2026-04-08
**Method:** Cross-reference Platform implementations against ShiftCenter catalog (BRAVO)
**Platform Source:** C:\Users\davee\OneDrive\Documents\GitHub\platform
**ShiftCenter Catalog:** .deia/audits/2026-04-08/bravo/IMPLEMENTATION-CATALOG.md

---

## Executive Summary

| Metric | Count |
|--------|-------|
| **Platform Major Features** | 11 |
| **Implemented in Platform** | 9 |
| **Present in ShiftCenter** | 2 (Efemera chat, partial Hive system) |
| **Gap Features (not in ShiftCenter)** | 7 |
| **Resurrection Candidates** | 5 (high-value subset) |

---

## Platform Major Features — Implementation Status

### 1. Flow Designer (PHASE-IR Canvas)
**Platform Location:** `efemera/frontend/src/components/flow-designer/` (122 TypeScript files, ~10,000 LOC)
**Spec:** ADR-007 PHASE IR Specification, 2026-03-03-IR-CANONICAL-SPEC.md
**Implementation Status:** ✅ **FULLY IMPLEMENTED** in Platform
**ShiftCenter Status:** ❌ **NOT PRESENT**

**What it is:**
- Visual workflow designer for process modeling (BPMN-like)
- 5 execution modes: Design, Simulate (DES), Tabletop (LLM-guided), Playback, Compare
- Node types: Phase (task), Checkpoint, Resource, Group
- Property panel with 7 tabs: General, Timing, Resources, Actions, Guards, Oracle, Metadata
- File operations: Save/Load JSON, Import BPMN/SBML/L-Systems, Export PNG/SVG/JSON
- Collaboration layer: Live cursors, node comments, design flight (session playback)
- Animation: Token flow, resource bars, queue badges, checkpoint flashes
- Local DES engine (discrete event simulation) runs in browser
- Local Graph Walker (tabletop mode) walks IR step-by-step with LLM decisions
- Checkpoints: Save/restore flow state at any point
- Diff/Compare: Side-by-side comparison of two flow versions with visual diff highlighting

**Key Dependencies:**
- React Flow (node graph library)
- Zustand (state management)
- Backend: SimDecisions DES engine API, IR validation API

**Files:** 122 TypeScript files organized into:
- `/animation/` (7 files) — visual effects
- `/checkpoints/` (3 files) — state save/restore
- `/collaboration/` (5 files) — multiplayer features
- `/compare/` (6 files) — diff visualization
- `/edges/` (3 files) — edge rendering
- `/file-ops/` (8 files + 3 dialect importers) — serialization, import/export
- `/modes/` (5 files) — mode switching (design/sim/tabletop/playback/compare)
- `/nodes/` (4 files) — node type components
- `/overlays/` (3 files) — badges, tooltips, pills
- `/playback/` (7 files) — session replay
- `/properties/` (7 files) — property panel tabs
- `/responsive/` (7 files) — mobile/tablet layout
- `/simulation/` (10 files) — local DES engine + config
- `/tabletop/` (6 files) — LLM-guided step execution
- `/telemetry/` (2 files) — event ledger integration
- Root: FlowDesigner.tsx, FlowCanvas.tsx, FlowToolbar.tsx, NodePalette.tsx, etc.

---

### 2. SimDecisions DES Engine (Discrete Event Simulation)
**Platform Location:** Backend (not fully visible in repo scan, likely in `services/` or external package)
**Spec:** ADR-008 DES Execution Engine, SPEC-V1-SHIP-2026-02-26
**Implementation Status:** ⚠️ **PARTIALLY VISIBLE** (API routes exist, core engine location unclear)
**ShiftCenter Status:** ❌ **NOT PRESENT**

**What it is:**
- Discrete Event Simulation engine (10,000x real-time speedup)
- Statistical Monte Carlo ensembles with seeded randomness (reproducibility)
- Three-currency fitness measurement: Clock (time), Coin (cost), Carbon (CO2e)
- Alterverse branching (counterfactual simulation)
- Event ledger integration (all events logged for audit)

**Evidence in Platform:**
- Backend routes: `hivenode/routes/sim.py`, `hivenode/routes/des_routes.py`, `hivenode/routes/pipeline_sim.py`
- Frontend calls DES API from Flow Designer simulation mode
- LLM metrics files in `hivenode/llm-metrics/` (cost/latency/carbon data for model selection)

**Gap:** Core Python DES engine implementation not found in repo scan (may be in external package or not committed).

---

### 3. Tabletop Engine (LLM-Guided Walkthrough)
**Platform Location:** `efemera/frontend/src/components/flow-designer/tabletop/` (6 TypeScript files)
**Spec:** ADR-010 Tabletop Engine
**Implementation Status:** ✅ **FULLY IMPLEMENTED** in Platform (frontend + backend integration)
**ShiftCenter Status:** ❌ **NOT PRESENT**

**What it is:**
- Interactive step-by-step process walkthrough
- LLM interprets natural language commands and walks IR graph
- Decision prompts at each node (user chooses path or delegates to LLM)
- Frank (LLM assistant) suggests next steps based on context
- Produces same Event Ledger trace as other execution modes
- Onboarding tool + cheap testing (no simulation cost, just LLM inference)

**Files:**
- `LocalGraphWalker.ts` — client-side IR graph traversal logic
- `TabletopChat.tsx` — chat interface for LLM interaction
- `DecisionPanel.tsx`, `DecisionPrompt.tsx` — user decision UI
- `FrankSuggestion.tsx` — LLM-generated guidance
- `StepProgress.tsx` — visual progress through flow
- `useTabletop.ts` — React hook for tabletop state management

---

### 4. Four-Vector Entity Profiling (α, σ, π, ρ)
**Platform Location:** Not visible in repo scan (backend logic, likely in `services/` or ML pipeline)
**Spec:** ADR-003 Four-Vector Entity Profiles
**Implementation Status:** ⚠️ **SPEC COMPLETE, IMPLEMENTATION UNCLEAR**
**ShiftCenter Status:** ❌ **NOT PRESENT**

**What it is:**
- Every entity (agent, human, bot, machine) profiled on 4 dimensions:
  - **α (Autonomy):** How much it can decide on its own (0-1)
  - **σ (Quality):** How well it performs (0-1)
  - **π (Preference):** Task affinity vector (multi-dimensional)
  - **ρ (Reliability):** Consistency of delivery (0-1)
- Profiles computed from Event Ledger data (actual performance, not declared)
- Used for: task assignment, team composition, oracle tier routing

**Evidence:** ADR-003 is fully specified. No code found in repo scan.

---

### 5. Oracle Tier System (Tier 0-4 Decision Routing)
**Platform Location:** Not visible in repo scan (backend routing logic)
**Spec:** ADR-004 Oracle Tier System
**Implementation Status:** ⚠️ **SPEC COMPLETE, IMPLEMENTATION UNCLEAR**
**ShiftCenter Status:** ❌ **NOT PRESENT**

**What it is:**
- 5-tier decision routing based on Value of Information (VoI):
  - **Tier 0:** Free lookups (cache, logic, deterministic)
  - **Tier 1:** Fast LLM (Haiku, Gemini Flash)
  - **Tier 2:** Capable LLM (Sonnet, GPT-4o)
  - **Tier 3:** Multi-LLM Tribunal (3 models vote, Tier 3.5 specifically)
  - **Tier 4:** Human judgment
- System routes each decision by VoI: spend minimum required for trustworthy answer
- Tier 3.5 Tribunal: 3 LLMs independently answer, majority vote wins, consensus logged

**Evidence:** ADR-004 is fully specified. No routing code found in repo scan.

---

### 6. Efemera Chat (Message/Channel System)
**Platform Location:** `efemera/frontend/src/` (15+ React components, WebSocket client)
**Spec:** ADR-023 Efemera Relay Architecture, efemera-build-spec-v2.egg.md
**Implementation Status:** ✅ **FULLY IMPLEMENTED** in Platform
**ShiftCenter Status:** ✅ **PARTIAL** — Chat UI exists (`primitives/conversation-pane/`, `primitives/efemera-connector/`), backend routes exist (`hivenode/efemera/`), but Platform's Flow Designer integration is NOT present

**What it is:**
- Multi-channel chat system (public/private channels, DMs)
- WebSocket-based real-time messaging
- Bot integration (Claude, GPT, Gemini via message commands)
- Queue approval flow (bots request permission before executing tasks)
- RAG integration (retrieval-augmented generation for document Q&A)
- Terminal execution (run shell commands via chat)
- File attachments, markdown rendering, code syntax highlighting

**Platform-specific features NOT in ShiftCenter:**
- Flow Designer integration (attach flows to messages, run simulations from chat)
- QueueApproval component (approve/deny bot task execution)
- Dashboard widgets (chat activity, bot status)
- Settings page (API key management, theme selection)

---

### 7. LLM Metrics Database (Clock/Coin/Carbon)
**Platform Location:** `hivenode/llm-metrics/*.json` (5 provider files)
**Spec:** SPEC-V1-SHIP-2026-02-26 (Section 2.2)
**Implementation Status:** ✅ **FULLY IMPLEMENTED** — JSON files with per-model metrics
**ShiftCenter Status:** ❌ **NOT PRESENT**

**What it is:**
- JSON files for each provider (Anthropic, OpenAI, Google, Meta, Voyage AI)
- Per-model metrics:
  - **Clock:** TTFT (ms), tokens/sec, latency p50/p95
  - **Coin:** input cost/million, output cost/million (USD)
  - **Carbon:** grams CO2e per 1000 tokens
  - **Capabilities:** context window, max output, vision, function calling, tier
- Used by: DES engine (cost estimation), Oracle router (tier selection), optimization engine (Pareto frontier)

**Files:**
- `hivenode/llm-metrics/anthropic.json`
- `hivenode/llm-metrics/openai.json`
- `hivenode/llm-metrics/google.json`
- `hivenode/llm-metrics/meta.json`
- `hivenode/llm-metrics/voyageai.json`

---

### 8. Hive Multi-Agent System
**Platform Location:** Spec-heavy, implementation unclear (telemetry logging exists)
**Spec:** SPEC-HIVE-DISPATCH-GOVERNANCE-001-v3, HIVE-BUILD-SPEC-2026-02-17, docs/PLATFORM-OPERATIONS.md
**Implementation Status:** ⚠️ **PARTIAL** — Telemetry/logging exists (`docs/hive-telemetry/`, `docs/bee-telemetry/`), but full scheduler/dispatcher not visible
**ShiftCenter Status:** ✅ **FULLY IMPLEMENTED** — Scheduler daemon, dispatcher daemon, queue runner, spec parser, all exist in `hivenode/scheduler/` and `.deia/hive/scripts/`

**What it is (Platform version):**
- Q33N orchestrator (Opus 4.6) coordinates tasks
- 9 bee types (TDD-1, TDD-2, CODE-G, CODEX-DOC, SONNET-1/2, OPUS, BEE-SONNET, BEE-GEMINI)
- File-based messaging (no direct bee-to-bee communication)
- Telemetry: Every bee action logged to JSONL
- Multi-vendor LLM routing (Anthropic, Google, OpenAI)

**Gap:** Platform's Hive is orchestration-focused (Q33N writes tasks, bees execute). ShiftCenter's Hive is automation-focused (scheduler scans queue, dispatcher assigns work, runner monitors progress). Platform has better telemetry. ShiftCenter has better automation.

---

### 9. Event Ledger (Immutable Audit Trail)
**Platform Location:** Backend (not visible in scan, likely in `services/` or database)
**Spec:** ADR-001 Event Ledger Foundation
**Implementation Status:** ⚠️ **SPEC COMPLETE, IMPLEMENTATION UNCLEAR**
**ShiftCenter Status:** ✅ **PARTIAL** — `hivenode/ledger/ledger.py` exists (1,303 LOC), but not integrated across all surfaces

**What it is:**
- Append-only log of every action (message sent, decision made, simulation run, file changed)
- Schema: `{ timestamp, actor, action, target, metadata, hash }`
- Immutable (no updates, no deletes)
- Reproducibility: Every simulation run captures seed, can replay exactly
- Governance: If not in ledger, it didn't happen

**Evidence:** ADR-001 is canonical spec. ShiftCenter has `ledger.py` module. Platform implementation not found in scan.

---

### 10. Optimization Engine (OR-Tools Integration)
**Platform Location:** Backend (not visible in scan)
**Spec:** ADR-011 Optimization Engine
**Implementation Status:** ⚠️ **SPEC COMPLETE, IMPLEMENTATION UNCLEAR**
**ShiftCenter Status:** ❌ **NOT PRESENT**

**What it is:**
- Translates IR flow to constraint model
- Uses Google OR-Tools solver
- Returns Pareto frontier: cost vs. speed vs. carbon
- Not a heuristic — mathematical proof of optimality
- Execution mode #3 (alongside Production, Simulation, Tabletop)

**Evidence:** ADR-011 is fully specified. Backend route `hivenode/routes/optimize_routes.py` exists in ShiftCenter (330 LOC). Core solver integration not visible.

---

### 11. Domain Dialect Compilers (BPMN, SBML, L-Systems)
**Platform Location:** `efemera/frontend/src/components/flow-designer/file-ops/dialect-importers/` (3 TypeScript files)
**Spec:** ADR-013 Domain Dialect Compilers
**Implementation Status:** ✅ **PARTIALLY IMPLEMENTED** — Import logic exists for BPMN, SBML, L-Systems
**ShiftCenter Status:** ❌ **NOT PRESENT**

**What it is:**
- Import external process definitions into PHASE-IR format
- **BPMN:** Business Process Model and Notation (XML)
- **SBML:** Systems Biology Markup Language (XML)
- **L-Systems:** Lindenmayer systems (rewrite grammar)
- One-way translation: external format → IR (not bidirectional)

**Files:**
- `bpmn-importer.ts` — BPMN XML → IR JSON
- `sbml-importer.ts` — SBML XML → IR JSON
- `lsys-importer.ts` — L-System grammar → IR JSON

---

## Summary Table: Platform Features vs. ShiftCenter

| Feature | Platform Status | ShiftCenter Status | Gap? |
|---------|----------------|-------------------|------|
| Flow Designer (PHASE-IR Canvas) | ✅ Fully implemented (10K LOC) | ❌ Not present | **YES** |
| DES Engine (Simulation) | ⚠️ Partial (API exists, core unclear) | ❌ Not present | **YES** |
| Tabletop Engine (LLM Walkthrough) | ✅ Fully implemented | ❌ Not present | **YES** |
| Four-Vector Profiling | ⚠️ Spec only (no code found) | ❌ Not present | **YES** |
| Oracle Tier Routing | ⚠️ Spec only (no code found) | ❌ Not present | **YES** |
| Efemera Chat | ✅ Fully implemented | ✅ Partial (no Flow Designer link) | **PARTIAL** |
| LLM Metrics DB (Clock/Coin/Carbon) | ✅ Fully implemented (JSON files) | ❌ Not present | **YES** |
| Hive System | ⚠️ Partial (telemetry) | ✅ Full automation (scheduler/dispatcher) | **DIVERGENT** |
| Event Ledger | ⚠️ Spec only (no code found) | ✅ Partial (`ledger.py`) | **DIVERGENT** |
| Optimization Engine | ⚠️ Spec only (route exists) | ✅ Partial (route exists, solver unclear) | **DIVERGENT** |
| Dialect Importers (BPMN/SBML/L-Sys) | ✅ Fully implemented | ❌ Not present | **YES** |

---

## Gap Analysis: What ShiftCenter is Missing

### High-Value Gaps (Worth Porting)
1. **Flow Designer** — 10,000 LOC visual workflow builder with 5 execution modes
2. **LLM Metrics DB** — Clock/Coin/Carbon cost modeling for all major LLM providers
3. **Tabletop Engine** — LLM-guided step-by-step process walkthrough
4. **Dialect Importers** — BPMN/SBML/L-Systems → IR translation
5. **Flow Designer Collaboration Features** — Live cursors, comments, playback, diff/compare

### Medium-Value Gaps (Context-Dependent)
6. **DES Engine** — If ShiftCenter wants simulation capabilities
7. **Oracle Tier Routing** — If ShiftCenter wants multi-tier LLM decision routing

### Low-Value Gaps (Spec-Only, No Code)
8. Four-Vector Profiling (no implementation found)
9. Optimization Engine (spec + route stub, no solver integration found)

---

## Divergent Features (Both Have, Different Approaches)

### Hive System
- **Platform:** Orchestration + telemetry (Q33N coordinates, bees log to JSONL)
- **ShiftCenter:** Automation + scheduling (scheduler scans queue, dispatcher assigns, runner monitors)
- **Recommendation:** Keep both. Platform's telemetry is superior. ShiftCenter's automation is superior.

### Event Ledger
- **Platform:** Spec-driven, immutable audit (no code found)
- **ShiftCenter:** Working implementation (`ledger.py`), partial integration
- **Recommendation:** ShiftCenter's implementation is ahead. No need to port.

---

## Files Modified/Created if Gaps Were Closed

**None.** This is a read-only audit. No modifications made to either repo.
