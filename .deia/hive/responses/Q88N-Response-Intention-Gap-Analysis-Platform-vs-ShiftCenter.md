# Intention Gap Analysis: Platform → ShiftCenter

**Date:** 2026-03-19
**Source Data:** `.deia/intention-engine/{shiftcenter,platform}/intentions.json`
**Scan Date:** 2026-03-18
**Tool:** `_tools/compare_intentions.py`

---

## Summary

| Metric | Count |
|--------|-------|
| Platform intentions (filtered) | 11,902 |
| ShiftCenter intentions (filtered) | 6,523 |
| Covered (matched) | 9,744 |
| **Gaps (platform-only)** | **2,139** |

---

## Category Distribution Comparison

| Category | Platform | ShiftCenter | Gap Ratio | Description |
|----------|----------|-------------|-----------|-------------|
| GP | 395 | 14 | **28x** | Governance patterns |
| AD | 1,242 | 224 | **5.5x** | Architectural decisions |
| QA | 134 | 30 | **4.5x** | Quality assurance |
| TMP | 226 | 29 | **7.8x** | Temporal / milestone |
| OR | 203 | 99 | **2x** | Operational rules |
| PAT | 140 | 59 | **2.4x** | Patterns |
| CON | 1,347 | 695 | **1.9x** | Constraints |
| IC | 733 | 413 | **1.8x** | Implementation concerns |
| AP | 421 | 339 | **1.2x** | Anti-patterns |
| UC | 7,415 | 4,810 | **1.5x** | Use cases |

---

## Tag-Level Gaps (Platform vs ShiftCenter)

| Tag | Platform | ShiftCenter | Gap Ratio |
|-----|----------|-------------|-----------|
| `knowledge` / `bok` | 126 | 0 | **missing entirely** |
| `agents` | 147 | 14 | **10x** |
| `governance` | 556 | 70 | **8x** |
| `security` | 52 | 7 | **7x** |
| `human` | 119 | 20 | **6x** |
| `coordination` | 54 | 8 | **7x** |
| `scope` | 67 | 25 | **2.7x** |
| `protocol` | 74 | 21 | **3.5x** |
| `validation` | 143 | 50 | **2.9x** |
| `config` | 186 | 103 | **1.8x** |

---

## Entire Functional Systems Missing from ShiftCenter

### Tier 1: Core Engine (Simulation Ecosystem) — NOT PORTED

These are the computational heart of the platform. None have been ported to shiftcenter.

| Platform Area | Gap Count | What It Is |
|---|---|---|
| **optimization/** | ~30 | Solver, objectives, constraints, Pareto frontiers, sensitivity analysis, warm start, variables |
| **surrogates/** | ~25 | Surrogate model training, serving, drift detection, uncertainty, time series, online learning |
| **tabletop/** | ~20 | Tabletop simulation engine — branching, history, interpreter, assumptions, traces, decision points |
| **pheromones/** | ~15 | Trust/coordination pheromone system — scope, transport, trust, anti-gaming, decay, vectors |
| **oracle/** | ~10 | LLM oracle — graduation, peer review, human-in-the-loop |
| **skills/** | ~8 | Skill registry, revocation, skill tribunal |
| **lineage/** | ~3 | Data lineage integrity tracking |
| **production/** | ~5 | Production metrics, webhook routes, actors |
| **scenarios/** | ~3 | Scenario binding and routes |

**Source files not ported:**

| Module | Files |
|---|---|
| optimization/ | `solver.py`, `objectives.py`, `constraints.py`, `infeasibility.py` |
| surrogates/ | `training.py`, `serving.py`, `drift.py`, `uncertainty.py`, `time_series.py` |
| tabletop/ | `branching.py`, `history.py`, `interpreter.py`, `assumptions.py`, `trace.py` |
| pheromones/ | `trust.py`, `scope.py`, `models.py`, `decay.py`, `anti_gaming.py`, `file_transport.py` |
| oracle/ | `graduation.py`, `peer_review.py`, `human.py` |
| skills/ | `registry.py`, `revocation.py`, `skill_tribunal.py` |
| lineage/ | `integrity.py` |
| production/ | `metrics.py`, `webhook_routes.py` |

### Tier 2: Canonical Knowledge & Governance — NOT PORTED

The entire knowledge management and governance layer.

| Platform Area | Gap Count | What It Is |
|---|---|---|
| **canonical/kb** | 232 | Knowledge base — goals, principles, constraints, contracts, patterns. The entire canonical KB system with `.egg.md` knowledge articles. |
| **canonical/docs** | 169 | Business model, architecture vision, domain verticals, strategic analysis, service portfolio, implementation plans |
| **canonical/projects** | 124 | Project management canonical data |
| **canonical/governance** | 120 | Ostrom principles, constitutional amendments, DEIA governance framework, human knowledge sovereignty |
| **canonical/simulation** | 10 | Simulation engine canonical specs |
| **canonical/tools** | 11 | LLH builder specs, tool definitions |
| **canonical/federalist** | 9 | Federalist papers / requirements extraction methodology |
| **canonical/ephemera** | 22 | Ephemeral messaging canonical data |
| **canonical/hivemind** | 5 | Hivemind coordination canonical |
| **canonical/services** | 4 | Service definitions |

### Tier 3: Frontend Functionality — NOT PORTED

| Platform Area | Gap Count | What It Is |
|---|---|---|
| **services/execution** | 2 | Execution service layer |
| **services/ir** | 1 | IR service layer |
| **components/mode-views** | 2 | Mode view components |
| **components/apps** | 1 | App components |
| **components/bridge** | 1 | Bridge components |
| **stores/optimizationStore** | 2 | Optimization state management |
| **hooks/useCanvasChatBrowser** | 1 | Canvas chat browser hook |
| **utils/bpmn-export** | 1 | BPMN export utility |
| **utils/colors** | 1 | Color utilities |
| **tests/fidelity** | 1 | IR fidelity tests |
| **tests/governance** | 1 | Governance tests |

### Tier 4: Infrastructure & Integration — NOT PORTED

| Platform Area | What It Is |
|---|---|
| **discord/** | Discord integration (frank_handler.py) |
| **builds/** | Build routes (commons_routes.py, routes.py) |
| **entities/** | Entity vectors |
| **global_commons/** | Global commons processes |

---

## Hive/Coordination Gaps (679 items)

The largest gap area (679) is `.deia/hive/` — but this is mostly **historical task/coordination documents** from platform's hive lifecycle. These include:

- Completed task files, dispatch scripts, and response files from platform-era work
- Chrysalis extraction outputs (intention scanner development)
- Research reports (LLM validation, industry analysis)
- Architecture briefings that informed platform but aren't shiftcenter-specific

**Actionable items from this area:**
- LEAN waste analysis for PHASE-IR (TIMWOOD auto-detection)
- IR JSON compression for LLM prompts (40-60% token savings)
- Translation gate architecture (LLM bootstraps its replacement)
- Governed Agent Runtime (GAR) spec — threat scanning, platform adapters
- Live memory system (Phase 1 — don't bake memory into compiled code)
- Telemetry consent prompt system
- Pane registry and advertisement protocol

---

## High-Confidence Platform-Only Intentions (Top 20)

| Conf. | Category | Area | Intention |
|-------|----------|------|-----------|
| 0.90 | GP | canonical/governance | DEIA's foundational principle: Human knowledge sovereignty in the AI era |
| 0.90 | GP | canonical/governance | Users collectively own and govern the knowledge created with AI assistance |
| 0.88 | GP | canonical/governance | Deferred Constitutional Amendments (Ostrom Principles 2, 4, 5, 6, 7) |
| 0.85 | CON | canonical/simulation | Simulation engine canonical constraints |
| 0.85 | GP | .deia/hive | Human knowledge sovereignty — SPECCED in canonical/governance |
| 0.82 | AD | .deia/hive | Every decision: Why you chose that approach |
| 0.82 | CON | .deia/hive | STRONG_KEYWORDS — High-confidence keyword detection |
| 0.81 | AD | .deia/hive | Architecture Decision: Hybrid Approach |
| 0.79 | IC | canonical/kb | Controller contract: returns { aimX, aimY, fire, thrusters } |
| 0.79 | AP | .deia/hive | Avoid pattern detection keywords |
| 0.78 | CON | canonical/kb | Core Principle: Coordination must never outrun conscience |
| 0.78 | CON | canonical/kb | Design principle: "FUCK MY COMPUTER CRASHED" should never mean lost work |
| 0.78 | CON | canonical/kb | Constraint: This is a solo project with AI assistance. Scope accordingly |
| 0.78 | IC | canonical/kb | Purpose: Define the contract for hatching, validating, and emitting LLHs |
| 0.78 | TMP | canonical/kb | Goal: Make DEIA installable and usable (Phase 1 success criteria) |
| 0.77 | AD | .deia/hive | Decision: Service architecture (CLI vs daemon vs hybrid) |
| 0.76 | IC | canonical/kb | Guarantee: Encrypted content can't be censored |
| 0.76 | UC | canonical/kb | Goal: Document the Master Librarian role and workflows |
| 0.76 | UC | .deia/hive | GOAL: Analyze IR to auto-detect 7 Lean wastes (TIMWOOD) |
| 0.76 | UC | .deia/hive | GOAL: Compress PHASE-IR JSON for LLM prompts — 40-60% savings |

---

## Prioritization Notes

### Already Ported to ShiftCenter (complete or partial)
- PHASE-IR engine (248 tests passing)
- DES routes (22 tests passing)
- Efemera EGG (channels, messages, relay)
- Fr@nk terminal concept (terminal primitive)
- EGG system (28 primitives, .egg.md format)
- Event Ledger (append-only)
- Gate Enforcer (five dispositions)
- Shell chrome (partial — Wave 1 recovery in progress)
- Chat system (bubbles, persistence, LLM proxy)

### Port Priority Suggestion

**P0 — Needed for alpha product:**
- None of the Tier 1 engine modules are needed for alpha. The shell, primitives, and EGG system are the alpha deliverable.

**P1 — Needed for beta / demo capability:**
- Dialect/vocabulary theme packs (user-selectable terminology)
- Canonical governance docs (Ostrom principles, human sovereignty)
- Optimization store + basic solver (for simulation demos)
- Skill registry (for EGG-loaded capabilities)

**P2 — Full platform parity:**
- Full optimization engine (Pareto, sensitivity, surrogates)
- Tabletop simulation engine
- Pheromone trust system
- Oracle (LLM peer review, graduation)
- Domain dialect compilers (BPMN, SBML, Terraform)
- Canonical KB system
- Discord integration
- Production metrics/webhooks

**P3 — Future / speculative:**
- Federalist requirements extraction
- LEAN waste auto-detection
- IR compression for LLM prompts
- Governed Agent Runtime (GAR)
- Lineage integrity

---

## Files Reference

| Artifact | Path |
|----------|------|
| Gap report (full) | `.deia/intention-engine/gap-report.md` |
| Comparison tool | `_tools/compare_intentions.py` |
| ShiftCenter intentions | `.deia/intention-engine/shiftcenter/intentions.json` |
| Platform intentions | `.deia/intention-engine/platform/intentions.json` |
| ShiftCenter scan summary | `.deia/intention-engine/shiftcenter/scan_summary.json` |
| Platform scan summary | `.deia/intention-engine/platform/scan_summary.json` |
| Extract tool | `_tools/extract_intentions.py` |
| Dialect spec (draft) | `docs/specs/SPEC-DIALECT-PREFERENCE-001-user-vocabulary-and-shell-dialect.md` |
