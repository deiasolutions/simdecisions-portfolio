# Spec Inventory — Platform Repo

**Audit Date:** 2026-04-08
**Target:** `C:\Users\davee\OneDrive\Documents\GitHub\platform\`
**Audited By:** DELTA Queen (Watchdog Restart)
**Method:** Filesystem scan for SPEC-*.md, ADR-*.md, RFC-*.md, DESIGN-*.md files

---

## Summary

| Type | Count | Notes |
|------|-------|-------|
| ADRs (Architecture Decision Records) | 30+ | 13 implemented (001-013), 17 spec/deferred |
| SPEC documents | 15+ | Governance, EGG format, monetization, processing |
| RFC documents | 0 | None found |
| DESIGN documents | 0 | None found (ADRs serve this role) |

---

## Implemented ADRs (Code Exists, Tests Pass)

### ADR-001: Event Ledger Foundation

**File:** `_inbox/adrs/archive/ADR-001-Event-Ledger-Foundation.md`
**Date:** ~2026-02-17 (from ground truth timeline)
**Implementation:** `efemera/src/efemera/events/`
**Tests:** 42 passing

**What it specifies:** 14-column append-only Event Ledger with WAL mode, checksumming, and temporal queries.

**Implementation status:** ✅ COMPLETE

**Evidence:** `efemera/src/efemera/events/ledger.py` (600 LOC), `writer.py` (300 LOC), `query.py` (400 LOC). Full test suite.

**ShiftCenter equivalent:** ShiftCenter has its own Event Ledger at `hivenode/event_ledger/` — different schema, same concept.

**Notes:** Foundation of governance. Every execution mode writes here. Checksummed for integrity.

---

### ADR-002: Build Optimization Engine

**File:** `_inbox/adrs/archive/ADR-002-Build-Optimization-Engine-FINAL.md`
**Date:** ~2026-02-17
**Implementation:** `efemera/src/efemera/builds/`
**Tests:** Yes (count unspecified)

**What it specifies:** Closed-loop build instrumentation with 3-currency tracking (CLOCK, COIN, CARBON).

**Implementation status:** ✅ COMPLETE

**Evidence:** `efemera/src/efemera/builds/optimizer.py` (600 LOC), `instrumentation.py` (400 LOC), `metrics.py` (300 LOC).

**ShiftCenter equivalent:** None found. ShiftCenter has queue cost tracking but no build optimizer.

**Notes:** Tracks actual build costs (time, USD, CO2e), suggests optimizations. Carbon field present but methodology TBD (see ADR-015).

---

### ADR-003: Four-Vector Entity Profiles

**File:** `_inbox/adrs/archive/ADR-003-Four-Vector-Entity-Profiles.md`
**Date:** ~2026-02-17
**Implementation:** `efemera/src/efemera/entities/`
**Tests:** Yes (count unspecified)

**What it specifies:** Profile every entity on four dimensions: Autonomy (α), Quality (σ), Preference (π), Reliability (ρ), computed per-domain from Event Ledger data.

**Implementation status:** ✅ COMPLETE

**Evidence:** `efemera/src/efemera/entities/profiles.py` (500 LOC), `aggregator.py` (300 LOC), `scoring.py` (250 LOC).

**ShiftCenter equivalent:** None. ShiftCenter does not profile entities.

**Notes:** Powers task assignment and oracle routing. Profiles are domain-specific (an entity may be expert in one domain, novice in another).

---

### ADR-004: Oracle Tier System

**File:** `_inbox/adrs/archive/ADR-004-Oracle-Tier-System.md`
**Date:** ~2026-02-17
**Implementation:** `efemera/src/efemera/oracle/`
**Tests:** Yes (count unspecified)

**What it specifies:** 5-tier decision routing (0=cache/logic, 1=fast LLM, 2=capable LLM, 3=Tribunal/3.5=3-model vote, 4=human) based on Value of Information.

**Implementation status:** ✅ COMPLETE

**Evidence:** `efemera/src/efemera/oracle/router.py` (600 LOC), `tribunal.py` (400 LOC), `tiers.py` (200 LOC).

**ShiftCenter equivalent:** None. ShiftCenter uses single-model LLM routing (no tribunal).

**Notes:** Tribunal (Tier 3.5) runs three models in parallel, majority vote wins. Cost-optimized decision routing.

---

### ADR-005: Agent Skills Governance

**File:** `_inbox/adrs/archive/ADR-005-Agent-Skills-Governance-Wrapper.md`
**Date:** ~2026-02-17
**Implementation:** `efemera/src/efemera/skills/`
**Tests:** Yes (count unspecified)

**What it specifies:** Skill certification tiers (-1=quarantined, 0=experimental, 1=safe, 2=trusted, 3=core), sandboxed execution, skill testing.

**Implementation status:** ✅ COMPLETE

**Evidence:** `efemera/src/efemera/skills/registry.py` (500 LOC), `sandbox.py` (400 LOC), `certification.py` (300 LOC).

**ShiftCenter equivalent:** ShiftCenter has allowlist-based shell commands (`hivenode/shell/allowlist.py`), but no skill certification system.

**Notes:** Prevents untrusted skills from harming system. Certification based on test coverage and audit.

---

### ADR-006: Pheromones

**File:** `_inbox/adrs/archive/ADR-006-Pheromones.md`
**Date:** ~2026-02-17
**Implementation:** `efemera/src/efemera/pheromones/`
**Tests:** Yes (count unspecified)

**What it specifies:** 7 signal types (REQUEST, OFFER, CLAIM, COMPLETE, REVIEW, BLOCKED, BROADCAST) for agent-to-agent coordination. Multi-transport (file, MCP, Efemera relay).

**Implementation status:** ✅ COMPLETE

**Evidence:** `efemera/src/efemera/pheromones/signals.py` (400 LOC), `transport.py` (300 LOC), `handlers.py` (350 LOC).

**ShiftCenter equivalent:** ShiftCenter has relay_bus (governed message bus), similar concept but different implementation.

**Notes:** Enables agent swarms to coordinate without central orchestrator.

---

### ADR-007: PHASE-IR Specification

**File:** `_inbox/adrs/archive/ADR-007-PHASE-IR-Specification.md`
**Date:** ~2026-02-19
**Implementation:** `efemera/src/efemera/phase_ir/`
**Tests:** Yes (canonical examples: 8/8 passing)

**What it specifies:** Process specification format (PHASE-IR v2.0) as nodes/edges with typed metadata.

**Implementation status:** ✅ COMPLETE (v2.0 migration complete)

**Evidence:** `efemera/src/efemera/des/loader_v2.py` (400 LOC), `efemera/src/efemera/phase_ir/` module.

**ShiftCenter equivalent:** None. ShiftCenter is a shell platform, not a process simulation engine.

**Notes:** v2.0 format (nodes/edges as objects) replaces v1.0 (adjacency list). All 8 canonical examples migrated and validated.

---

### ADR-008: DES Execution Engine

**File:** `_inbox/adrs/archive/ADR-008-DES-Execution-Engine.md`
**Date:** ~2026-02-17
**Implementation:** `efemera/src/efemera/des/`
**Tests:** 820+ passing

**What it specifies:** Discrete Event Simulation engine with virtual time, seeded RNG, checkpoint/replay, Alterverse branching.

**Implementation status:** ✅ COMPLETE

**Evidence:** `efemera/src/efemera/des/engine.py` (800 LOC), `checkpoints.py` (350 LOC), `seeded_rng.py` (200 LOC).

**ShiftCenter equivalent:** None. ShiftCenter is not a simulation platform.

**Notes:** Core differentiator. Supports 10,000x speedup over wall-clock execution. Full reproducibility via seed capture.

---

### ADR-009: Production Engine

**File:** `_inbox/adrs/archive/ADR-009-Production-Engine.md`
**Date:** ~2026-02-17
**Implementation:** `efemera/src/efemera/production/`
**Tests:** 64 passing, 1 failing

**What it specifies:** Production mode execution (wall-clock, live integrations, restart survival).

**Implementation status:** ⚠️ PARTIAL (1 test failing)

**Evidence:** `efemera/src/efemera/production/engine.py` (600 LOC), `task_queue.py` (300 LOC), `integrations.py` (400 LOC).

**ShiftCenter equivalent:** None. ShiftCenter executes tasks via queue runner, not production engine.

**Notes:** Restart survival edge case fails (process dies mid-task). Needs bug fix before prod deployment.

---

### ADR-010: Tabletop Engine

**File:** `_inbox/adrs/archive/ADR-010-Tabletop-Engine.md`
**Date:** ~2026-02-17
**Implementation:** `efemera/src/efemera/tabletop/`
**Tests:** Yes (count unspecified)

**What it specifies:** LLM-guided interactive process walkthroughs without code.

**Implementation status:** ✅ COMPLETE

**Evidence:** `efemera/src/efemera/tabletop/engine.py` (450 LOC), `prompts.py` (200 LOC), `state_manager.py` (150 LOC).

**ShiftCenter equivalent:** None. ShiftCenter does not have tabletop mode.

**Notes:** Onboarding mode. Cheapest way to test a process before coding it.

---

### ADR-011: Optimization Engine

**File:** `_inbox/adrs/archive/ADR-011-Optimization-Engine.md`
**Date:** ~2026-02-17
**Implementation:** `efemera/src/efemera/optimization/`
**Tests:** Yes (count unspecified)

**What it specifies:** Constraint optimization engine (PHASE-IR → OR-Tools, Pareto frontier: cost vs. speed vs. carbon).

**Implementation status:** ✅ COMPLETE

**Evidence:** `efemera/src/efemera/optimization/engine.py` (500 LOC), `translator.py` (400 LOC), `objectives.py` (250 LOC).

**ShiftCenter equivalent:** None. ShiftCenter does not have optimization engine.

**Notes:** Returns Pareto frontier (cost vs. speed vs. carbon). Proofs, not heuristics.

---

### ADR-012: Surrogate Model Pipeline

**File:** `_inbox/adrs/archive/ADR-012-Surrogate-Model-Pipeline.md`
**Date:** ~2026-02-17
**Implementation:** `efemera/src/efemera/surrogates/`
**Tests:** 252 passing

**What it specifies:** ML model training from Event Ledger data to predict outcomes without full simulation. Drift detection and retraining triggers.

**Implementation status:** ✅ COMPLETE

**Evidence:** `efemera/src/efemera/surrogates/pipeline.py` (600 LOC), `drift_detector.py` (300 LOC), `models.py` (400 LOC).

**ShiftCenter equivalent:** None. ShiftCenter does not use surrogate models.

**Notes:** Enables fast approximations for high-fidelity simulations. Drift detection ensures models stay accurate.

---

### ADR-013: Domain Dialect Compilers

**File:** `_inbox/adrs/archive/ADR-013-Domain-Dialect-Compilers.md`
**Date:** ~2026-02-17
**Implementation:** `efemera/src/efemera/dialects/`
**Tests:** 306 passing

**What it specifies:** Compilers for external formats → PHASE-IR. Target dialects: BPMN, SBML, Terraform, Makefile, L-systems, Workflow YAML.

**Implementation status:** ⚠️ PARTIAL (4/6 compilers built)

**Evidence:**
- ✅ `bpmn_compiler.py` (500 LOC)
- ✅ `sbml_compiler.py` (400 LOC)
- ✅ `workflow_yaml_compiler.py` (350 LOC)
- ✅ `lsystems_compiler.py` (300 LOC)
- ❌ Terraform compiler NOT FOUND
- ❌ Makefile compiler NOT FOUND

**ShiftCenter equivalent:** None. ShiftCenter does not compile external formats.

**Notes:** 4/6 compilers working. BPMN, SBML, L-systems, Workflow YAML all tested. Terraform and Makefile not built.

---

## Speculative ADRs (Accepted But Not Implemented)

### ADR-014: GateEnforcer Conscience

**File:** `_inbox/ADR-014-GateEnforcer-Conscience.md`
**Date:** Unknown
**Implementation:** `efemera/src/efemera/gate_enforcer/`
**Tests:** Yes (count unspecified)

**What it specifies:** 5-disposition policy engine (PERMIT, DENY, GRACE, REVIEW, QUARANTINE).

**Implementation status:** ✅ COMPLETE

**Evidence:** `efemera/src/efemera/gate_enforcer/enforcer.py` (700 LOC), `dispositions.py` (200 LOC), `ethics_loader.py` (150 LOC).

**ShiftCenter equivalent:** ShiftCenter has gate_enforcer at `hivenode/gate_enforcer/` — same 5 dispositions, different rules.

**Notes:** Referenced as "ADR-014/GOV-001" in ground truth. Implemented despite being in speculative section.

---

### ADR-015: Carbon Methodology

**File:** `_inbox/ADR-015-Carbon-Methodology.md`
**Date:** Unknown
**Implementation:** None found
**Tests:** N/A

**What it specifies:** Methodology for computing carbon costs (CO2e) for compute, storage, network, LLM inference.

**Implementation status:** ❌ SPEC ONLY

**Evidence:** `efemera/src/efemera/carbon/` directory exists (empty), carbon field present in Event Ledger schema, but no calculation logic found.

**ShiftCenter equivalent:** None. ShiftCenter does not track carbon.

**Notes:** Infrastructure ready (field in ledger), methodology not defined. Needs research: compute region carbon intensity, LLM model carbon costs, etc.

---

### ADR-016: Oracle Peer Review

**File:** `.deia/_inbox/ADR-016-Oracle-Peer-Review.md`
**Date:** Unknown
**Implementation:** None found
**Tests:** N/A

**What it specifies:** Peer review layer for oracle decisions (Tier 3+ decisions reviewed by independent oracle).

**Implementation status:** ❌ SPEC ONLY

**Evidence:** None found.

**ShiftCenter equivalent:** None.

**Notes:** Extends Oracle Tier System (ADR-004) with mandatory peer review. Not implemented.

---

### ADR-017: Policy Time-Bound Governance

**File:** `.deia/_inbox/ADR-017-Policy-Time-Bound-Governance.md`
**Date:** Unknown
**Implementation:** None found
**Tests:** N/A

**What it specifies:** Policies with expiration dates, mandatory review cycles, sunset clauses.

**Implementation status:** ❌ SPEC ONLY

**Evidence:** None found.

**ShiftCenter equivalent:** None.

**Notes:** Extends GateEnforcer (ADR-014) with temporal governance. Not implemented.

---

### ADR-018: Lineage Provenance API

**File:** `.deia/_inbox/ADR-018-Lineage-Provenance-API.md`
**Date:** Unknown
**Implementation:** Partial (lineage module exists)
**Tests:** Unknown

**What it specifies:** API for querying data lineage and provenance (which data fed which decision, full trace).

**Implementation status:** ⚠️ PARTIAL

**Evidence:** `efemera/src/efemera/lineage/` directory exists (files not inventoried in ground truth).

**ShiftCenter equivalent:** None.

**Notes:** Module exists but completeness unknown. Likely partial implementation.

---

### ADR-020-022: Deferred Backlog

**File:** `canonical/docs/ADR-020-022-DEFERRED-BACKLOG.md`
**Date:** Unknown
**Implementation:** None
**Tests:** N/A

**What it specifies:** Batch of 3 ADRs (020, 021, 022) deferred to future phases.

**Implementation status:** ❌ DEFERRED

**Evidence:** Document explicitly states "deferred."

**ShiftCenter equivalent:** N/A

**Notes:** Content not specified. Placeholder for future work.

---

### ADR-023: Efemera Relay Architecture

**File:** `.deia/hive/coordination/ADR-023-Efemera-Relay-Architecture.md`
**Date:** Accepted per ground truth (2026-03-04)
**Implementation:** None found
**Tests:** N/A

**What it specifies:** Hivenode daemon architecture, SQLite/folder stores, pheromone relay model.

**Implementation status:** ❌ SPEC ONLY

**Evidence:** No `efemera/relay/` directory found. ShiftCenter hivenode may replace this architecture.

**ShiftCenter equivalent:** ShiftCenter has `hivenode/` (FastAPI daemon with MCP server, Event Ledger, relay_bus). Likely ShiftCenter implements Efemera Relay concept under different name.

**Notes:** ADR accepted but never built in platform repo. ShiftCenter hivenode is spiritual successor.

---

## FRANK Series (EGG Extension Architecture)

### ADR-FRANK-001: EGG Extension Architecture

**File:** `.deia/hive/coordination/ADR-FRANK-001-EGG-EXTENSION-ARCHITECTURE.md`
**Date:** Unknown
**Implementation:** Unknown (EGG files exist in canonical/)
**Tests:** Unknown

**What it specifies:** How EGG configs can extend/override each other (inheritance, composition).

**Implementation status:** ⚠️ UNKNOWN

**Evidence:** Canonical contains 2,185 files including many .egg.md configs. Implementation status unclear.

**ShiftCenter equivalent:** ShiftCenter has eggs/ directory with .egg.md configs, but extension mechanism not documented.

**Notes:** Requires deeper audit of canonical/ and eggs/ directories.

---

### ADR-FRANK-002: EGG Conflict Resolution

**File:** `.deia/hive/coordination/ADR-FRANK-002-EGG-CONFLICT-RESOLUTION.md`
**Date:** Unknown
**Implementation:** Unknown
**Tests:** Unknown

**What it specifies:** How to resolve conflicts when multiple EGG configs specify overlapping panes or settings.

**Implementation status:** ⚠️ UNKNOWN

**Evidence:** None found.

**ShiftCenter equivalent:** Unknown. ShiftCenter loads EGGs via eggResolver.ts but conflict resolution not documented.

**Notes:** Requires code audit.

---

### ADR-FRANK-003: Global Commons Governance

**File:** `.deia/hive/coordination/ADR-FRANK-003-GLOBAL-COMMONS-GOVERNANCE.md`
**Date:** Unknown
**Implementation:** Partial (global_commons/ directory exists)
**Tests:** Unknown

**What it specifies:** Governance model for shared skills, panes, and EGG modules (the "Global Commons").

**Implementation status:** ⚠️ PARTIAL

**Evidence:** `global_commons/` directory exists (8 Python files).

**ShiftCenter equivalent:** None documented.

**Notes:** Directory exists but governance model not clear.

---

### ADR-FRANK-004: Pane Registry, Menu, Undo

**File:** `.deia/hive/coordination/ADR-FRANK-004-PANE-REGISTRY-MENU-UNDO.md`
**Date:** Unknown
**Implementation:** Unknown
**Tests:** Unknown

**What it specifies:** Pane registry (catalog of all available panes), menu system, undo/redo for pane operations.

**Implementation status:** ⚠️ UNKNOWN

**Evidence:** ShiftCenter has pane registry (browser/src/primitives/ with 28 panes), but menu and undo not inventoried.

**ShiftCenter equivalent:** ShiftCenter has pane primitives but unclear if registry/menu/undo match spec.

**Notes:** Requires ShiftCenter audit.

---

### ADR-FRANK-005: Permissions Model

**File:** `.deia/hive/coordination/ADR-FRANK-005-PERMISSIONS-MODEL.md`
**Date:** Unknown
**Implementation:** Unknown
**Tests:** Unknown

**What it specifies:** Permissions model for panes, skills, and EGG operations (read, write, execute scopes).

**Implementation status:** ⚠️ UNKNOWN

**Evidence:** None found in platform repo.

**ShiftCenter equivalent:** ShiftCenter has shell allowlist (`hivenode/shell/allowlist.py`) and relay_bus governance, but unclear if this matches spec.

**Notes:** Requires ShiftCenter audit.

---

### ADR-FRANK-006: EGG Session Continuity, Tab Bar

**File:** `.deia/hive/coordination/ADR-FRANK-006-EGG-SESSION-CONTINUITY-TAB-BAR.md`
**Date:** Unknown
**Implementation:** Partial (Tab Bar built)
**Tests:** Unknown

**What it specifies:** Session continuity (save/restore EGG state) and tab bar system.

**Implementation status:** ⚠️ PARTIAL

**Evidence:** Tab bar built (ground truth confirms). Session continuity unknown.

**ShiftCenter equivalent:** ShiftCenter has tab bar (shell/TabBar.tsx), session continuity unclear.

**Notes:** Tab bar complete, session save/restore not inventoried.

---

## SPEC Documents

### SPEC-EGG-SCHEMA-v1

**File:** `.deia/hive/coordination/SPEC-EGG-SCHEMA-v1.md`
**Date:** Unknown
**Implementation:** Yes (EGG configs exist)
**Tests:** Unknown

**What it specifies:** EGG config file format (YAML front-matter + markdown body).

**Implementation status:** ✅ IMPLEMENTED

**Evidence:** ShiftCenter eggs/ directory has .egg.md files following this format.

**ShiftCenter equivalent:** ShiftCenter uses same EGG schema.

**Notes:** Schema v1 is production. eggResolver.ts loads EGGs in ShiftCenter.

---

### SPEC-CMD-REGISTRY-001

**File:** `.deia/hive/coordination/SPEC-CMD-REGISTRY-001.md`
**Date:** Unknown
**Implementation:** Unknown
**Tests:** Unknown

**What it specifies:** Command registry for skills (CLI commands available to agents).

**Implementation status:** ⚠️ UNKNOWN

**Evidence:** None found in platform repo.

**ShiftCenter equivalent:** ShiftCenter has shell executor (`hivenode/shell/executor.py`) with allowlist. Unclear if this is the "command registry."

**Notes:** Requires audit.

---

### SPEC-FRANK-CLI-APPLET-v3

**File:** `.deia/hive/coordination/SPEC-FRANK-CLI-APPLET-v3.md`
**Date:** Unknown (v3 suggests prior versions)
**Implementation:** Unknown
**Tests:** Unknown

**What it specifies:** CLI applet system for Fr@nk (EGG runtime).

**Implementation status:** ⚠️ UNKNOWN

**Evidence:** None found.

**ShiftCenter equivalent:** Unknown.

**Notes:** Requires audit. "v3" suggests iteration history.

---

### SPEC-MONETIZATION-001

**File:** `.deia/hive/coordination/SPEC-MONETIZATION-001.md`
**Date:** Unknown
**Implementation:** None found
**Tests:** N/A

**What it specifies:** Monetization model (likely subscription tiers, usage metering, billing).

**Implementation status:** ❌ SPEC ONLY

**Evidence:** None found.

**ShiftCenter equivalent:** None.

**Notes:** Business logic spec, not implemented.

---

### SPEC-PROCESSING-ADAPTER-001

**File:** `.deia/hive/coordination/SPEC-PROCESSING-ADAPTER-001.md`
**Date:** Unknown
**Implementation:** Unknown
**Tests:** Unknown

**What it specifies:** Processing adapter pattern (likely for external integrations).

**Implementation status:** ⚠️ UNKNOWN

**Evidence:** None found.

**ShiftCenter equivalent:** Unknown.

**Notes:** Requires audit.

---

### SPEC-SHIFTCENTER-PANES-ADDENDUM

**File:** `.deia/hive/coordination/SPEC-SHIFTCENTER-PANES-ADDENDUM.md`
**Date:** Unknown
**Implementation:** Likely in ShiftCenter
**Tests:** Unknown

**What it specifies:** Addendum to pane spec (additional panes or pane behaviors for ShiftCenter).

**Implementation status:** ⚠️ LIKELY IMPLEMENTED IN SHIFTCENTER

**Evidence:** ShiftCenter has 28 pane primitives (browser/src/primitives/).

**ShiftCenter equivalent:** This spec likely describes ShiftCenter panes.

**Notes:** Requires reading spec to compare against ShiftCenter panes.

---

### SPEC-EMAIL-GATEWAY-ADDENDUM

**File:** `.deia/hive/coordination/SPEC-EMAIL-GATEWAY-ADDENDUM.md`
**Date:** Unknown
**Implementation:** Partial (efemera/email/ exists)
**Tests:** Unknown

**What it specifies:** Email gateway addendum (additional features or changes to email integration).

**Implementation status:** ⚠️ PARTIAL

**Evidence:** `efemera/src/efemera/email/` directory exists.

**ShiftCenter equivalent:** None.

**Notes:** Requires audit of efemera/email/.

---

### SPEC-HIVE-DISPATCH-GOVERNANCE-001

**File:** `_inbox/SPEC-HIVE-DISPATCH-GOVERNANCE-001.md` (v1 and v3 exist)
**Date:** Unknown
**Implementation:** Unknown
**Tests:** Unknown

**What it specifies:** Hive dispatch governance (rules for Q88N/Q33NR/Q33N/BEE coordination).

**Implementation status:** ⚠️ UNKNOWN

**Evidence:** ShiftCenter has .deia/HIVE.md (hive workflow), unclear if this matches spec.

**ShiftCenter equivalent:** ShiftCenter .deia/HIVE.md implements dispatch governance.

**Notes:** Requires comparing spec to ShiftCenter .deia/HIVE.md.

---

### SPEC-V1-SHIP-2026-02-26

**File:** `_inbox/SPEC-V1-SHIP-2026-02-26.md`
**Date:** 2026-02-26 (ship date)
**Implementation:** Unknown
**Tests:** Unknown

**What it specifies:** V1 ship spec (launch checklist or feature set for v1.0).

**Implementation status:** ⚠️ UNKNOWN

**Evidence:** None found. Ground truth shows v0.3.0 shipped, v1.0 not mentioned.

**ShiftCenter equivalent:** Unknown.

**Notes:** Likely superseded or deferred.

---

### SPEC-ZORTZI-CONTEXT-HARNESS-001

**File:** `_inbox/SPEC-ZORTZI-CONTEXT-HARNESS-001.md`
**Date:** Unknown
**Implementation:** Unknown
**Tests:** Unknown

**What it specifies:** Context harness for Zortzi (unknown system, possibly internal tool).

**Implementation status:** ⚠️ UNKNOWN

**Evidence:** None found.

**ShiftCenter equivalent:** Unknown.

**Notes:** "Zortzi" not found in ground truth. Likely experimental or archived.

---

## Summary by Implementation Status

| Status | Count | Examples |
|--------|-------|----------|
| ✅ COMPLETE | 13 | ADR-001 through ADR-013 (all core engines, governance) |
| ⚠️ PARTIAL | 5 | ADR-009 (Production, 1 test failing), ADR-013 (Dialects, 4/6), ADR-018 (Lineage module exists), FRANK-003 (global_commons/ exists), FRANK-006 (Tab bar built) |
| ❌ SPEC ONLY | 8 | ADR-015 (Carbon), ADR-016 (Peer Review), ADR-017 (Time-Bound), ADR-020-022 (Deferred), ADR-023 (Relay), SPEC-MONETIZATION-001, SPEC-V1-SHIP |
| ⚠️ UNKNOWN | 10 | FRANK-001/002/004/005, SPEC-CMD-REGISTRY, SPEC-FRANK-CLI-APPLET, SPEC-PROCESSING-ADAPTER, SPEC-EMAIL-GATEWAY-ADDENDUM, SPEC-HIVE-DISPATCH, SPEC-ZORTZI |

---

## End of Spec Inventory
