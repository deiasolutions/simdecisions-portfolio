# Platform Resurrection Candidates — Briefing for Mr. AI

**Date:** 2026-04-08
**Source:** Delta Queen audit of Platform repo, cross-referenced against ShiftCenter BRAVO catalog
**Purpose:** Identify features worth porting from Platform to ShiftCenter, with effort estimates

---

## Executive Summary

9 candidates identified. 6 recommended for port. 3 deferred (spec-only or low ROI).

**Recommended total effort:** 22-30 days across 4 waves
**Estimated new code:** ~12,000 lines (mostly Flow Designer)
**Risk:** All ports are additive — no breaking changes to existing ShiftCenter code

---

## Wave 1: Quick Wins (3-4 days)

### RC-001: LLM Metrics Database (Clock/Coin/Carbon)
- **Source:** `hivenode/llm-metrics/*.json` (5 files, ~500 LOC)
- **Effort:** SMALL (1 day)
- **What:** Copy 5 JSON cost files, add Python loader, REST endpoint, frontend hook
- **Why now:** Enables cost-aware LLM routing, task estimation, carbon tracking. Zero risk. Immediate value in build monitor.

### RC-006: Queue Approval UI
- **Source:** `efemera/frontend/src/components/QueueApproval.tsx` (~200 LOC)
- **Effort:** TRIVIAL (<1 day)
- **What:** Approval prompt in Efemera chat when bot requests task execution. Approve/Deny card. Backend adds `approval_status` field.
- **Why now:** Governance layer for bot actions. Simple modal, no new deps.

### RC-002: BPMN Importer (Backend Only)
- **Source:** `efemera/frontend/src/components/flow-designer/file-ops/dialect-importers/` (3 files, ~600 LOC)
- **Effort:** SMALL (1-2 days)
- **What:** Python BPMN → JSON converter. REST endpoint `POST /import/bpmn`. CLI tool.
- **Why now:** Industry-standard process import. Uses `lxml`, well-defined format.

---

## Wave 2: Flow Designer MVP (8-10 days)

### RC-004: Flow Designer Phase 1-2 (Core Canvas + Properties)
- **Source:** `efemera/frontend/src/components/flow-designer/` (122 files, ~10,000 LOC)
- **Effort:** LARGE (5-8 days for Phase 1-2 only)
- **What:** React Flow canvas, node palette, basic properties panel. Phase/Checkpoint nodes. Save/Load JSON.
- **Why now:** Core differentiator. Visual frontend for ShiftCenter's queue/spec system. Every SPEC-*.md could be visualized as an IR graph.
- **Risk:** Largest port. Mitigate with phased build — ship Phase 1-2 as MVP, iterate.

### RC-003: Efemera Flow Chat Integration
- **Source:** `efemera/frontend/src/pages/FlowDesignerPage.tsx` + chat integration
- **Effort:** SMALL (1-2 days)
- **What:** "Attach Flow" button in conversation pane. Flow picker. Message metadata with flow_id. Thumbnail cards in chat.
- **Depends on:** RC-004 Phase 1

---

## Wave 3: Advanced Features (7-8 days)

### RC-004 Phase 3: Simulation Mode (Local DES Engine)
- **Effort:** 4 days
- **What:** Copy LocalDESEngine.ts. Simulation config panel. Progress panel. Results preview.

### RC-005: Tabletop Engine (Standalone)
- **Source:** `efemera/frontend/src/components/flow-designer/tabletop/` (6 files, ~800 LOC)
- **Effort:** MEDIUM (3-4 days)
- **What:** Python graph walker. LLM-guided step-by-step process execution. CLI-first, no UI required.
- **Why:** Test specs in tabletop mode before dispatch. Educational tool.

---

## Wave 4: Collaboration (5-6 days)

### RC-004 Phase 4-5: Tabletop + Collaboration
- **Effort:** 5 days
- **What:** Live cursors (WebSocket), node comments, playback mode (session replay)

### RC-004 Phase 6: Compare Mode + Importers
- **Effort:** 3 days
- **What:** Split canvas (side-by-side diff), structural diff algorithm, BPMN importer integration

---

## Do Not Port

| Candidate | Why Not |
|-----------|---------|
| RC-007: Four-Vector Entity Profiling | Spec-only, no implementation exists in Platform |
| RC-008: Oracle Tier Routing | Spec-only, overcomplicated for current use cases |
| RC-009: Optimization Engine (OR-Tools) | Route stub only, no solver integration. Defer until optimization use cases emerge |

---

## Recommended Ship Sequence

```
Week 1:  RC-001 (LLM Metrics) + RC-006 (Approval UI) + RC-002 (BPMN)
Week 2-3: RC-004 Phase 1-2 (Flow Designer MVP)
Week 3:  RC-003 (Chat-Flow Integration)
Week 4-5: RC-004 Phase 3 (Simulation) + RC-005 (Tabletop)
Week 6:  RC-004 Phase 4-6 (Collab + Compare)
```

---

## Risk Matrix

| Candidate | Technical | Dependency | ROI |
|-----------|-----------|-----------|-----|
| RC-001 LLM Metrics | LOW | NONE | NONE — immediate value |
| RC-002 BPMN | LOW | LOW (lxml) | LOW |
| RC-003 Flow Link | LOW | MEDIUM (needs RC-004) | LOW |
| RC-004 Flow Designer | MEDIUM | HIGH (React Flow, DES) | MEDIUM |
| RC-005 Tabletop | LOW | LOW | MEDIUM |
| RC-006 Approval UI | LOW | NONE | LOW |

**Highest risk:** RC-004 due to size. Phased build mitigates.

---

## Alignment Check

All Tier 1-2 candidates align with ShiftCenter direction:
- **Chat-first UX** — Efemera connector active, Flow Designer extends it
- **HiveHostPanes** — Flow Designer is a natural pane (`primitives/flow-designer/`)
- **Multi-LLM routing** — LLM Metrics enables cost-aware model selection
- **Queue system** — BPMN + Tabletop extend queue capabilities
- **No conflicts.** All ports are additive.

---

## Decision Needed

1. **Approve Wave 1?** (3-4 days, all quick wins, zero risk)
2. **Approve Wave 2?** (8-10 days, Flow Designer MVP — biggest investment)
3. **Priority order within Wave 1?** (recommend RC-001 first — immediate build monitor value)
4. **Any candidates to cut or reprioritize?**
