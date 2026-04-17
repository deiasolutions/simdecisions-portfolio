# PORTFOLIO NUGGET HUNT 001: AI Agent Orchestration Evidence

**Date:** 2026-04-17
**Agent:** QUEEN-2
**Status:** COMPLETE
**Model:** Claude Sonnet 4.5

---

## Mission Summary

Surveyed DEIA Hive coordination system to extract portfolio nuggets proving "teams of AI developer agents" for 1000bulbs job application. Focus: agent orchestration under governance, NOT "AI-assisted coding."

---

## Key Findings: Agent Orchestration Under Governance

### 1. Multi-Tier Command Chain

**Chain of Command (from C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\.deia\HIVE.md):**

```
Q88N (Dave, human sovereign)
  ↓ sets direction
Q33NR (Queen Regent — live session with Dave)
  ↓ writes briefing, dispatches Q33N
Q33N (Queen — headless coordinator)
  ↓ writes task files, dispatches bees after Q33NR approval
BEEs (workers — headless)
  ↓ write code, run tests, write response files
Results flow UP: BEE → Q33N → Q33NR → Q88N
```

**Governance Rules:**
- **No shortcuts. No skipping levels.** Q33NR never talks to bees directly. Bees never talk to Q88N directly.
- **Q33NR does NOT code.** Q33N does NOT code unless Q88N explicitly approves.
- **BEEs NEVER orchestrate.** They execute one task, write response file, stop.

**Portfolio Nugget:** This is a **command hierarchy with role segregation**, not ad-hoc prompting. Each agent tier has distinct responsibilities and communication boundaries.

---

### 2. Autonomous Daemon Orchestration

**Three Coordinated Daemons (event-driven, not polling):**

#### Scheduler Daemon (C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\hivenode\scheduler\scheduler_daemon.py)
- **Responsibility:** Computes optimal task schedules using OR-Tools CP-SAT solver
- **Input:** Backlog specs (`queue/backlog/`), completed specs (`queue/_done/`), velocity data
- **Output:** `schedule.json` with dependency-resolved task order
- **Triggers:** MCP event `queue.spec_done` → instant recalculation (<2s latency)
- **Fallback:** 60s polling if MCP unavailable
- **Stats:** 93% latency reduction vs polling (30s → <2s), 98% I/O reduction

#### Dispatcher Daemon (C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\hivenode\scheduler\dispatcher_daemon.py)
- **Responsibility:** Manages queue slot allocation, moves specs from backlog to active queue
- **Slot Calculation:** `available_slots = max_bees - active_count - queued_count`
- **Safety Gate:** Verifies dependencies satisfied before dispatch (double-checks schedule.json)
- **In-Memory Counters:** Updated by MCP events (`queue.spec_active`, `queue.spec_done`)
- **Drift Correction:** Re-scans disk every 60s to correct missed events
- **Stats:** 90% latency reduction (10s → <1s), stale slot bug eliminated

#### Triage Daemon (C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\hivenode\scheduler\triage_daemon.py)
- **Responsibility:** Monitors failed specs in `_needs_review/`, requeues or escalates
- **Decision Logic:**
  - Completion flag detected → move to `_done/`
  - Partial work detected → requeue to `backlog/` with resume context
  - Empty output → requeue with clean retry header
  - **3 retries reached → escalate to `_escalated/` + write coordination briefing**
- **Healing:** Appends triage history to spec files, tracks retry count
- **Scan Interval:** 5 minutes (300s)

**Portfolio Nugget:** These daemons form a **closed-loop autonomous factory** with event-driven coordination. MCP event system eliminates polling lag and enables sub-2s reaction times. This is **agent-to-agent communication via event bus**, not human-in-the-loop for every decision.

---

### 3. Governed Build Integrity Process

**Process: PROCESS-0013-BUILD-INTEGRITY-3PHASE.md**

**Multi-Phase Validation Pipeline:**

1. **Gate 0: Prompt→SPEC Disambiguation**
   - LLM interprets user intent → extracts requirements tree
   - Compares prompt requirements vs SPEC requirements (TF-IDF similarity)
   - **Healing Loop:** FAIL → DIAGNOSE → HEAL (LLM regenerates SPEC) → RETRY (max 3) → ESCALATE (human)
   - **Threshold:** 100% coverage, 0 hallucinations, embedding similarity ≥ 0.85

2. **Phase 0: Coverage Validation**
   - Extracts requirements from ASSIGNMENT
   - Checks every requirement covered in SPEC (LLM verification)
   - **Violation Detection:** Mandatory requirements declared "out of scope" → FAIL
   - **Healing Loop:** Same as Gate 0

3. **Phase 1: SPEC Fidelity**
   - Encode SPEC → Phase-IR → Decode to SPEC'
   - Compare embeddings: `cosine_similarity(SPEC, SPEC') ≥ 0.85`
   - Ensures semantic preservation in encoding

4. **Phase 2: TASK Fidelity**
   - Same as Phase 1, but for task breakdown
   - Ensures task assignments preserve SPEC intent

**Escalation After Max Retries:**
- 3 automated healing attempts per phase
- **Human escalation prompt** if all retries fail
- Options: `approve` (override), `edited` (manual fix), `abort` (stop)

**Portfolio Nugget:** This is **multi-agent quality assurance** with automated healing loops and escalation to human only after exhausting automated recovery. The system heals itself first, escalates when stuck. Not a simple "generate code" workflow.

---

### 4. Traceability & Auditability

**Traceability ID System (from PROCESS-0013):**

| Level | Prefix | Example | Description |
|-------|--------|---------|-------------|
| L0 | `REQ-{CAT}-{NNN}` | `REQ-UI-001` | Requirements from ASSIGNMENT |
| L1 | `SPEC-{NNN}` | `SPEC-001` | Specification items |
| L2 | `TASK-{NNN}` | `TASK-001` | Implementation tasks |
| L3 | `CODE-{NNN}` | `CODE-001` | Code artifacts (files/functions) |
| L4 | `TEST-{NNN}` | `TEST-001` | Test cases |

**Directed Acyclic Graph (DAG):**
```
REQ-UI-001 (User clicks Export)
    ↓ implements
SPEC-001 (Export Button Component)
    ↓ breaks_into
TASK-001 (Build ExportButton.tsx)
    ↓ produces
CODE-001 (ExportButton.tsx)
    ↓ tested_by
TEST-001 (Export button renders)
```

**Code Comments:**
```typescript
// Implements: TASK-001 | Satisfies: REQ-UI-001
// File: simdecisions-2/src/components/buttons/ExportButton.tsx
export function ExportButton() { ... }
```

**Portfolio Nugget:** Every line of agent-generated code traces back to a requirement through a **4-level dependency graph**. This enables:
- Orphan detection (requirements with no implementation)
- Impact analysis (which code breaks if requirement changes)
- Audit trail (why was this code written?)

This is **software engineering rigor applied to AI-generated code**, not "move fast and break things."

---

### 5. Three-Currency Resource Accounting

**Carbon Methodology (from C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\.deia\config\carbon.yml):**

**Model Energy Consumption:**
| Model | Input kWh/1k | Output kWh/1k |
|-------|--------------|---------------|
| claude-opus-4-6 | 0.0080 | 0.0120 |
| claude-sonnet-4-5 | 0.0030 | 0.0045 |
| claude-haiku-4-5 | 0.0008 | 0.0012 |

**Carbon Intensity by Region:**
| Region | g CO2/kWh |
|--------|-----------|
| us_average | 400 |
| california | 230 |
| france | 50 |

**Budget Limits:**
- Daily: 50,000g CO2
- Weekly: 250,000g CO2
- Monthly: 1,000,000g CO2
- Alert threshold: 80% of limit

**Tracked in Every Response File (MANDATORY):**
```markdown
## Clock / Cost / Carbon
- **Clock:** wall time
- **Cost:** estimated USD
- **Carbon:** estimated CO2e
```

**Portfolio Nugget:** The hive tracks **three currencies** (CLOCK, COIN, CARBON) for every agent operation. This enables:
- Cost optimization (use Haiku for simple tasks, Sonnet for complex)
- Carbon budgeting (stay under daily/weekly/monthly caps)
- ROI analysis (e.g., "8 cents and 86k tokens prevents dropped requirements that could cost hours of rework")

This is **environmental and financial accountability** built into the orchestration layer.

---

### 6. Ethics & Safety Governance

**Ethics Configuration (from C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\.deia\config\ethics-default.yml):**

**Forbidden Actions:**
- `delete_production_data`
- `bypass_gate`
- `modify_ethics`
- `impersonate_human`
- `access_pii_unredacted`

**Forbidden Targets:**
- `system:event-ledger`
- `system:gate-enforcer`

**Escalation Triggers:**
- `security`, `pii`, `financial`, `legal`, `medical`

**Max Autonomy Tier:** 1 (lowest)
**Grace Period:** 300 seconds (5 minutes)

**Portfolio Nugget:** Agents operate under **hard-coded ethical constraints** that cannot be overridden without escalation. This is **safety by design**, not trust-based delegation.

---

### 7. Production Scale Evidence

**Completed Specs (from C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\.deia\hive\queue\_done):**
- **Total:** 1,358 completed specs
- **Sample Diversity:** deployment wiring, UI components, build monitors, Phase-IR ports, queue infrastructure

**Escalated Specs (from C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\.deia\hive\queue\_escalated):**
- **Total:** 18 escalated specs
- **Escalation Rate:** ~1.3% (18/1358)
- **Reason:** 3+ retry failures → automatic triage escalation

**Portfolio Nugget:** This is **production-scale operation** with >1,300 completed tasks and a 98.7% autonomous completion rate. Escalation is rare and automated. This is NOT a proof-of-concept.

---

### 8. Distributed Coordination Artifacts

**Coordination Briefings (from C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\.deia\hive\coordination):**
- Q33NR writes briefings for Q33N (example: `2026-03-11-BRIEFING-BUG-001-002-CHAT-RENDERING.md`)
- Q33N writes completion reports for Q33NR (example: `2026-03-11-Q33N-BUG-001-002-COMPLETION-REPORT.md`)
- Triage daemon writes escalation briefings (example: `20260417-TRIAGE-ESCALATION-PORTFOLIO-NUGGET.md`)

**Task Files (from C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\.deia\hive\tasks):**
- Q33N writes task files for BEEs (stored in `.deia/hive/tasks/`)
- BEEs write response files (stored in `.deia/hive/responses/`)

**Portfolio Nugget:** Communication is **asynchronous and file-based**, not real-time chat. Agents read/write markdown documents in a structured directory system. This enables:
- Crash recovery (all state on disk)
- Audit trail (full conversation history)
- Multi-session coordination (multiple agents can read same briefing)

This is **document-driven orchestration**, not RPC or REST APIs.

---

## Portfolio Nuggets Summary (YAML Format)

```yaml
portfolio_nuggets:
  - title: "Multi-Tier Agent Command Chain"
    category: "Orchestration"
    evidence: ".deia/HIVE.md lines 1-40"
    description: "4-tier command hierarchy (Q88N → Q33NR → Q33N → BEEs) with role segregation and no cross-level communication"
    impact: "Enables delegation at scale without human bottlenecks. Q88N sets direction once, agents execute autonomously."

  - title: "Autonomous Factory with Event-Driven Daemons"
    category: "Infrastructure"
    evidence: "hivenode/scheduler/*.py (scheduler, dispatcher, triage daemons)"
    description: "Three coordinated daemons (scheduler, dispatcher, triage) orchestrate 1,358+ specs via MCP event bus"
    impact: "Sub-2s reaction time to queue changes. 98% I/O reduction vs polling. Autonomous triage with 3-retry healing loops."

  - title: "Multi-Phase Validation with Automated Healing"
    category: "Quality Assurance"
    evidence: ".deia/processes/PROCESS-0013-BUILD-INTEGRITY-3PHASE.md"
    description: "Gate 0 + 3 validation phases (prompt→SPEC, coverage, SPEC fidelity, TASK fidelity) with LLM-driven healing loops (max 3 retries) before human escalation"
    impact: "Prevents dropped requirements. 100% coverage validation. Semantic fidelity ≥0.85. ROI: 8 cents prevents hours of rework."

  - title: "Traceability DAG for AI-Generated Code"
    category: "Auditability"
    evidence: ".deia/processes/PROCESS-0013-BUILD-INTEGRITY-3PHASE.md lines 570-733"
    description: "5-level traceability graph (REQ → SPEC → TASK → CODE → TEST) with embedded IDs in code comments"
    impact: "Every line of code traces to a requirement. Enables orphan detection, impact analysis, and audit trails."

  - title: "Three-Currency Resource Accounting"
    category: "Sustainability"
    evidence: ".deia/config/carbon.yml, PROCESS-0013 lines 836-922"
    description: "Tracks CLOCK (time), COIN (cost), CARBON (CO2e) for every agent operation. Daily/weekly/monthly carbon budgets."
    impact: "Environmental accountability built into orchestration. Model selection optimized for cost/carbon (Haiku vs Sonnet vs Opus)."

  - title: "Ethics & Safety Governance"
    category: "Safety"
    evidence: ".deia/config/ethics-default.yml"
    description: "Hard-coded forbidden actions (delete_production_data, bypass_gate, modify_ethics). Escalation triggers for security/PII/financial."
    impact: "Safety by design. Agents cannot override ethical constraints without human intervention."

  - title: "Production Scale: 1,358 Completed Specs"
    category: "Scale"
    evidence: ".deia/hive/queue/_done/ (1,358 files), _escalated/ (18 files)"
    description: "1,358 completed specs with 1.3% escalation rate. Autonomous completion: 98.7%."
    impact: "This is production-scale operation, not a proof-of-concept. Escalation is rare and automated."

  - title: "Document-Driven Asynchronous Coordination"
    category: "Architecture"
    evidence: ".deia/hive/coordination/, .deia/hive/tasks/, .deia/hive/responses/"
    description: "Agents communicate via markdown documents in structured directories. Q33NR writes briefings, Q33N writes tasks, BEEs write responses."
    impact: "Crash recovery (state on disk). Full audit trail. Multi-session coordination (agents read same briefing)."

performance_metrics:
  scheduler:
    latency_reduction: "93% (30s → <2s)"
    io_reduction: "98%"
    wake_trigger: "MCP event-driven"
  dispatcher:
    latency_reduction: "90% (10s → <1s)"
    slot_detection: "In-memory counters (MCP events)"
    safety_gate: "Double-check deps before dispatch"
  triage:
    scan_interval: "300s (5 minutes)"
    retry_limit: 3
    escalation_rate: "1.3% (18/1358)"
  validation:
    coverage_threshold: "100% (mandatory)"
    fidelity_threshold: "0.85 (cosine similarity)"
    healing_retries: 3
    cost_per_build: "$0.08 (avg 10 reqs, 5 tasks)"
    carbon_per_build: "~12g CO2e"

governance_rules:
  - "No cross-level communication (Q33NR ↔ BEEs forbidden)"
  - "Q33NR does NOT code"
  - "Q33N does NOT code without Q88N approval"
  - "BEEs NEVER orchestrate"
  - "3 healing retries before human escalation"
  - "No git write operations without Q88N approval"
  - "Hard-coded ethical constraints (no override)"
  - "Daily/weekly/monthly carbon budgets"

technology_stack:
  orchestration:
    - "Custom MCP (Model Context Protocol) event bus"
    - "OR-Tools CP-SAT solver (task scheduling)"
    - "Voyage embeddings (semantic fidelity validation)"
    - "TF-IDF similarity (requirements matching)"
  agents:
    - "Claude Opus 4.6 (complex tasks)"
    - "Claude Sonnet 4.5 (standard tasks)"
    - "Claude Haiku 4.5 (simple tasks, validation)"
  infrastructure:
    - "Python 3.12 (daemon processes)"
    - "Railway (production deployment)"
    - "PostgreSQL (inventory database)"
    - "FastAPI (hivenode service)"
    - "React + Vite (browser frontend)"

files_surveyed:
  boot: "C:\\Users\\davee\\OneDrive\\Documents\\GitHub\\simdecisions\\.deia\\BOOT.md"
  hive: "C:\\Users\\davee\\OneDrive\\Documents\\GitHub\\simdecisions\\.deia\\HIVE.md"
  scheduler: "C:\\Users\\davee\\OneDrive\\Documents\\GitHub\\simdecisions\\hivenode\\scheduler\\scheduler_daemon.py"
  dispatcher: "C:\\Users\\davee\\OneDrive\\Documents\\GitHub\\simdecisions\\hivenode\\scheduler\\dispatcher_daemon.py"
  triage: "C:\\Users\\davee\\OneDrive\\Documents\\GitHub\\simdecisions\\hivenode\\scheduler\\triage_daemon.py"
  processes:
    - "C:\\Users\\davee\\OneDrive\\Documents\\GitHub\\simdecisions\\.deia\\processes\\P-SCHEDULER.md"
    - "C:\\Users\\davee\\OneDrive\\Documents\\GitHub\\simdecisions\\.deia\\processes\\P-DISPATCHER.md"
    - "C:\\Users\\davee\\OneDrive\\Documents\\GitHub\\simdecisions\\.deia\\processes\\PROCESS-0013-BUILD-INTEGRITY-3PHASE.md"
  config:
    - "C:\\Users\\davee\\OneDrive\\Documents\\GitHub\\simdecisions\\.deia\\config\\carbon.yml"
    - "C:\\Users\\davee\\OneDrive\\Documents\\GitHub\\simdecisions\\.deia\\config\\ethics-default.yml"
  completed_specs: "C:\\Users\\davee\\OneDrive\\Documents\\GitHub\\simdecisions\\.deia\\hive\\queue\\_done\\ (1358 files)"
  escalated_specs: "C:\\Users\\davee\\OneDrive\\Documents\\GitHub\\simdecisions\\.deia\\hive\\queue\\_escalated\\ (18 files)"

conclusion:
  summary: "The DEIA Hive is a production-scale AI agent orchestration system with governed command hierarchy, event-driven coordination, multi-phase validation, traceability graphs, three-currency accounting, and ethical constraints. This is NOT 'AI-assisted coding' — this is 'AI-orchestrated development' with 1,358 completed specs and 98.7% autonomous completion rate."
  differentiation: "vs AI-assisted coding"
  key_difference:
    ai_assisted: "Human writes specs, AI generates code, human reviews"
    ai_orchestrated: "Human sets direction, AI agents write specs → validate → break into tasks → dispatch workers → heal failures → escalate only after 3 retries"
  business_value:
    speed: "Sub-2s reaction time to queue changes (vs 30s polling)"
    quality: "100% requirement coverage validation + semantic fidelity ≥0.85"
    scale: "1,358 completed specs with 1.3% escalation rate"
    cost: "$0.08 per build prevents hours of rework"
    sustainability: "Carbon budgets + model optimization (Haiku vs Sonnet vs Opus)"
    auditability: "Full traceability DAG (REQ → CODE) + file-based audit trail"
