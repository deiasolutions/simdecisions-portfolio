# SPEC-SKILL-PRIMITIVE-001: Skill as a First-Class Primitive

**Version:** 1.0  
**Date:** 2026-04-12  
**Author:** Dave × Claude (Opus 4.6)  
**Status:** SPEC — Ready for review  
**Tags:** #skill #primitive #governance #agentskills #TASK-019

---

## 1. Problem Statement

The platform has governance infrastructure for skills (AGT-002, AGT-003, AGT-006/TASK-019) but no formal definition of what a Skill *is* in the DEIA stack. Meanwhile, the industry converged on an open standard (agentskills.io, adopted by 30+ platforms as of April 2026). Without a canonical Skill primitive:

1. Bee dispatch instructions are ad-hoc markdown — no standard structure, no progressive disclosure, no portability
2. The governance wrapper (TASK-019) has nothing formal to wrap
3. Third-party skills from Anthropic, OpenAI, Vercel, etc. have no ingestion path
4. Fr4nk's personas and show formats are implicit, not loadable skill packs

---

## 2. What a Skill Is — and Isn't

### 2.1 The Three Primitives (Hard Boundary)

| Primitive | What It Is | Consumer | Format | Lives On |
|-----------|-----------|----------|--------|----------|
| **Set** | Composition that plays on the stage. Libretto. | HiveHostPanes (the stage) | `.set.md` | Stage |
| **EGG** | Transport container. Encrypted, provenance-tracked, portable. | Any runtime that speaks .egg protocol | `.egg.md` | In transit |
| **Skill** | Instruction pack that teaches an agent how to perform a task | Bees, drones, LLM workers, Fr4nk | `SKILL.md` (agentskills.io format) | Agent context |

These are peers, not subsets of each other.

### 2.2 Relationship Rules

- A Skill talks to the **agent**, not the stage. It never touches HiveHostPanes.
- A Set talks to the **stage**, not the agent. It describes what renders.
- An EGG is the **envelope** for Sets, PHASE-IR, and other artifacts. It does not carry Skills.
- Skills live in the Global Commons as standard agentskills.io directories — the industry format, not a proprietary wrapper.
- A Skill is NOT a spec. Specs describe *what to build*. Skills describe *how to do a task repeatedly*.
- A Skill is NOT a task file. Task files are one-shot dispatches. Skills persist across sessions.

---

## 3. Skill Format — agentskills.io Alignment

DEIA Skills adopt the agentskills.io open standard as the base format. This is a deliberate #NOKINGS decision: write once, run on any agent platform.

### 3.1 Directory Structure

```
skill-name/
├── SKILL.md          # Required: YAML frontmatter + markdown instructions
├── scripts/          # Optional: executable code the agent can run
├── references/       # Optional: supplementary docs loaded on demand
├── assets/           # Optional: templates, resources
└── governance.yml    # DEIA EXTENSION: governance metadata (see §5)
```

### 3.2 SKILL.md Format

```yaml
---
name: tribunal-host
description: >-
  Host a structured multi-model debate using the Tribunal format.
  Use when preparing or running a Tribunal episode, casting models
  into roles, managing rounds, and producing episode artifacts.
license: Proprietary
compatibility: Requires Python 3.12+, Kokoro-82M TTS
metadata:
  author: Q88N
  version: "1.0"
  deia:
    cert_tier: 3
    carbon_class: heavy
    requires_human: false
---

# Tribunal Host

## Steps

### Step 1: Load Episode Workspace
[instructions...]

### Step 2: Cast Models into Roles
[instructions...]

## Output Format
[what the final result looks like]

## Gotchas
- Never let a model self-assign its role
- Always validate debate format before recording
```

### 3.3 Progressive Disclosure (Context Efficiency)

Adopted directly from the agentskills.io spec:

| Level | What Loads | When | Token Cost |
|-------|-----------|------|------------|
| **Catalog** | name + description only | Session start | ~50 tokens/skill |
| **Activation** | Full SKILL.md body | Task matches description | < 5,000 tokens recommended |
| **Execution** | Referenced files from scripts/, references/, assets/ | As needed during task | Variable |

This means hundreds of skills can be registered without burning context. ZORTZI manages the catalog level; activation happens on match.

---

## 4. Skill Categories in the DEIA Stack

### 4.1 Internal Skills (authored by Dave / hive)

| Skill | Description | Cert Tier |
|-------|-------------|-----------|
| tribunal-host | Multi-model debate orchestration | 3 |
| tribunal-judge | Scoring and verdict production | 3 |
| bee-dispatch | Format and send task files to Mr. Code | 3 |
| spec-writer | Produce specs in DEIA format | 3 |
| task-file-writer | Write properly formatted task files with all required sections | 3 |
| response-file-writer | Write properly formatted bee response files (8-section format) | 3 |
| three-phase-validation | Run PROCESS-0013 Gate 0 + Phase 0/1/2 build integrity checks | 3 |
| wave-planner | Organize work into Wave 0/A/B/C/D/E with dependency + parallelization assessment | 3 |
| process-writer | Write PROCESS-XXXX docs in standard format | 3 |
| coordination-briefing-writer | Write sprint coordination briefings for all bees in a session | 3 |
| prism-ir-author | Write PRISM-IR process definitions | 3 |
| egg-packager | Bundle payloads into .egg.md transport format | 3 |
| set-composer | Compose .set.md stage configurations | 3 |
| hive-diagnostics | Survey repo, run grep audits, produce gap reports | 3 |
| fr4nk-persona-dave | Fr4nk as Dave's working assistant | 3 |
| fr4nk-persona-demo | Fr4nk in demo/portfolio mode | 3 |
| fr4nk-persona-stage | Fr4nk as Center Stage host | 3 |

### 4.2 Imported Skills (third-party, governed)

Skills from external catalogs (Anthropic, OpenAI, Vercel, community) that enter the platform through the governance wrapper. Default cert tier: **-1** (untrusted, maximum sandboxing) until promoted.

### 4.3 Resolved Design Decisions

- **Operator-authored skills:** Yes. Operators (Tier 1-4) can author their own skills. The same governance pipeline applies — operator skills enter at cert tier -1 and promote through the same certification path as any other skill. No special treatment.
- **Global Commons participation:** Yes. Skills are hosted in the Global Commons in standard agentskills.io format (SKILL.md directories) — NOT as EGG payloads. Skills are skills. EGGs are transport. The Global Commons speaks the industry standard.
- **Skill activation model:** No switching policy. A skill loads at the time it's needed, in the context it's needed, at the level it needs to be played out. A skill is a script for an actor to follow — the actor carries their repertoire and performs the right script when the cue comes. Progressive disclosure handles the mechanics: catalog at session start, activation on description match, execution on demand.

---

## 5. Governance Layer — TASK-019 Realized

This is the product. The agentskills.io format is open. The governance wrapper is proprietary.

### 5.1 governance.yml (DEIA Extension)

Every skill in the DEIA stack gets a `governance.yml` sidecar, either authored (internal) or generated (imported):

```yaml
# governance.yml — DEIA governance metadata for this skill
cert_tier: -1          # Current certification level (-1 to 3)
promoted_from: null    # Previous tier (audit trail)
promoted_at: null      # ISO timestamp of last promotion
promoted_by: null      # Entity ID that approved promotion

# Capability grants (what this skill is allowed to do)
capabilities:
  filesystem_read: false
  filesystem_write: false
  network_access: false
  shell_exec: false
  user_data_access: false
  model_invocation: false
  event_ledger_write: false

# Blast radius classification
blast_radius: contained    # contained | local | platform | external

# Three currencies — budget caps per invocation
budget:
  clock_max_seconds: 60
  coin_max_usd: 0.10
  carbon_max_grams: 5.0

# TASaaS scan results
last_scan:
  timestamp: null
  threats_detected: []
  prompt_injection_risk: unknown   # none | low | medium | high
  pii_exposure_risk: unknown       # none | low | medium | high

# Audit
event_ledger_id: null    # Ledger entry for this skill's registration
```

### 5.2 Certification Tiers (AGT-003, unchanged)

| Tier | Label | Capabilities | Entry Condition |
|------|-------|-------------|-----------------|
| **-1** | Untrusted | Maximum sandboxing. No filesystem, no network, no shell. | Default for all imported skills |
| **0** | Verified | Basic verification passed. Read-only filesystem. | TASaaS scan clean, no prompt injection risk |
| **1** | Audited | Security audit passed. Standard capabilities. | Manual review by Q33NR or Q88N |
| **2** | Tested | Extensive testing. Elevated capabilities including network. | BAT holdout-set validation passed |
| **3** | Certified | Fully certified. Unrestricted within policy bounds. | Q88N approval. Internal skills only (initially). |

Certification is revocable. Tier changes log to Event Ledger.

### 5.3 Ingestion Pipeline (third-party skills)

```
External Skill Catalog
       │
       ▼
   Download / Clone
       │
       ▼
   TASaaS Scan ──────────────────┐
   (prompt injection,            │
    PII exposure,                │
    malicious scripts,           │
    network calls,               │
    dependency audit)            │
       │                         │
       ▼                         ▼
   Generate governance.yml    BLOCK if critical threats
   cert_tier: -1
       │
       ▼
   Register in Skill Catalog
   (name + description only)
       │
       ▼
   Event Ledger: SKILL_REGISTERED
       │
       ▼
   Available for sandboxed execution
       │
       ▼
   Promotion path: -1 → 0 → 1 → 2 → 3
   (each step requires higher authority)
```

### 5.4 Runtime Enforcement (GovernanceProxy integration)

When an agent activates a skill:

1. GovernanceProxy checks cert_tier against requested capabilities
2. If capability exceeds tier grant → GateEnforcer disposition (BLOCK / ESCALATE / REQUIRE_HUMAN)
3. If permitted → skill loads into agent context
4. Every skill invocation logs to Event Ledger: `SKILL_ACTIVATED`, `SKILL_COMPLETED`, `SKILL_FAILED`
5. Three currencies metered per invocation
6. Four-vector profile of the skill entity updated (yes, skills get profiles too)

---

## 6. Skill Profiles — Skills as Entities

Skills are entities in the four-vector system. They earn reputation just like agents do.

| Vector | What It Measures for a Skill |
|--------|------------------------------|
| **σ (sigma)** | Quality — does the skill produce correct, useful output? |
| **π (pi)** | Predictability — does it behave consistently across invocations? |
| **ρ (rho)** | Reliability — does it complete without errors? |
| **α (alpha)** | Autonomy — does it require human intervention? |

A skill with degrading σ/ρ scores gets flagged for review. A skill with consistent high scores across all vectors is a candidate for tier promotion.

---

## 7. Relationship to Existing Components

| Component | Relationship to Skill |
|-----------|----------------------|
| **AGT-002** (Agent Skills Governance) | The enforcement layer. Every skill passes through it. |
| **AGT-003** (Certification Tiers) | The trust hierarchy. Determines what a skill can do. |
| **AGT-006 / TASK-019** (Skills Wrapper) | The product wrapper. Makes any third-party skill governed. |
| **Event Ledger** (EVT-001) | Logs all skill lifecycle events. |
| **Four-Vector Profiles** (ENT-001) | Skills are profiled entities. |
| **GateEnforcer** (GOV-001) | Enforces capability grants at runtime. |
| **TASaaS** (EPH-012) | Scans skills on ingestion and monitors at runtime. |
| **GovernanceProxy** | Orchestrates the full governed skill execution flow. |
| **ZORTZI** | Manages skill catalog in context (progressive disclosure). |
| **EGG** | Transport mechanism. Skills do NOT travel as EGG payloads — they use standard agentskills.io format in the Global Commons. EGGs carry Sets, PHASE-IR, and other artifacts. |
| **Set** | No direct relationship. Skills and Sets are separate primitives. |
| **PRISM-IR** | A skill can teach an agent how to write PRISM-IR, but a skill is not IR. |

---

## 8. Fr4nk Skill Loading

Fr4nk's personas are skills in the repertoire — not modes to switch between. A skill loads when the work calls for it, scoped to what's needed, released when done. Fr4nk doesn't "become" a different persona; Fr4nk performs the right script when the cue comes.

| Skill | What It Teaches Fr4nk | Loads When |
|-------|----------------------|------------|
| fr4nk-persona-dave | Direct, technical, dispatch-ready working style | Task matches working session patterns |
| fr4nk-persona-demo | Polished, explains the stack, audience-aware | Task matches demonstration/portfolio patterns |
| tribunal-host | Debate format, role assignment, scoring | Task involves Tribunal episode production |
| fr4nk-persona-stage | Production host, audience interaction | Task involves Center Stage broadcast |

Multiple skills can be active simultaneously (e.g., tribunal-host + fr4nk-persona-stage for a live broadcast episode). No switching policy exists because none is needed — the progressive disclosure mechanism (§3.3) handles activation via description match.

---

## 9. Open Standard Boundary (Red Hat Model)

| Layer | Open / Proprietary |
|-------|-------------------|
| SKILL.md format (agentskills.io) | **Open** — adopted as-is |
| Directory structure (scripts/, references/, assets/) | **Open** — adopted as-is |
| Global Commons skill hosting | **Open** — standard agentskills.io format, not EGG-wrapped |
| governance.yml sidecar | **Proprietary** — DEIA extension |
| TASaaS scan pipeline | **Proprietary** |
| Certification tier enforcement | **Proprietary** |
| GovernanceProxy skill execution flow | **Proprietary** |
| Four-vector skill profiling | **Proprietary** |
| Event Ledger skill event types | **Proprietary** |

Anyone can write a SKILL.md. Only DEIA governs it.

---

## 10. Implementation Priority

| Phase | Deliverable | Depends On |
|-------|------------|------------|
| **1** | Formal Skill directory structure in repo (`.deia/skills/`) | This spec |
| **2a** | Convert 3 internal workflows to SKILL.md format (bee-dispatch, spec-writer, hive-diagnostics) | Phase 1 |
| **2b** | Convert 6 hive process workflows to SKILL.md format (task-file-writer, response-file-writer, three-phase-validation, wave-planner, process-writer, coordination-briefing-writer) | Phase 1 |
| **3** | governance.yml generator from TASaaS scan | TASaaS pipeline |
| **4** | Skill catalog registry (name + description index) | Phase 2a |
| **5** | Third-party skill ingestion pipeline | Phases 3 + 4 |
| **6** | Fr4nk persona skills | Phase 2a |
| **7** | Runtime enforcement via GovernanceProxy | Phase 5 + GateEnforcer |
| **8** | Four-vector profiling for skills | Phase 7 + Event Ledger |
| **9** | Skill publishing to Global Commons (agentskills.io format) | GC infrastructure |

---

## 11. ADR Cross-References

- **ADR-005:** Agent Skills Governance — this spec formalizes the artifact that ADR governs
- **ADR-001:** Event Ledger — skill events are a new event category
- **ADR-003:** Four-Vector Profiles — skills become profiled entities
- **ADR-004:** Oracle Tier System — skill tier decisions can route through oracle
- **ADR-009:** Scenario Management — skills and scenarios are separate distribution paths in the Global Commons
- **TASK-019:** Skills Wrapper — this spec defines what gets wrapped

---

## 12. Key Decisions Locked by This Spec

1. **Skill adopts the agentskills.io open standard as base format.** No proprietary fork.
2. **governance.yml is the DEIA extension.** Sidecar, not embedded in SKILL.md.
3. **Skills are entities.** They get four-vector profiles and event ledger entries.
4. **Default cert tier for imported skills is -1.** Guilty until proven innocent.
5. **Fr4nk personas are skills.** Loadable via description match, not mode-switched.
6. **Skill ≠ Spec ≠ Task file.** Three distinct artifacts with different lifecycles.
7. **Skills live in the Global Commons as standard agentskills.io directories.** NOT as EGG payloads. EGGs carry other things.
8. **Operators can author skills.** Same governance applies — no special treatment.
9. **Skill activation is demand-driven.** A skill loads at the time, in the context, and at the level it needs to be played out. No switching policy.
