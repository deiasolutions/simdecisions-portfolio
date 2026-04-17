# Specification Inventory

**Generated:** 2026-04-08
**Audit:** BRAVO (Spec-to-Implementation Cross-Reference)
**Total Spec Documents:** 274

---

## Summary by Location

| Location | Count | Status | Notes |
|----------|-------|--------|-------|
| **docs/specs/** | 51 | Canonical specs | Long-term design documents, architecture decisions, feature specs |
| **.deia/hive/queue/_done/** | 183 | Completed | Specs processed by the build queue, implementation complete |
| **.deia/hive/queue/backlog/** | 13 | Queued | Awaiting scheduler pickup |
| **.deia/hive/queue/_active/** | 2 | In Progress | Currently being built by bees |
| **.deia/hive/queue/_needs_review/** | 19 | Review Needed | Queen review required before activation |
| **.deia/hive/responses/** | 6 | Design Docs | High-level design documents (EFEMERA-CONNECTOR, MCP-QUEUE, FLOW-DESIGNER) |

---

## Canonical Specs (docs/specs/)

These are long-lived specification documents that define architecture, major features, and design decisions.

### Architecture Decision Records (ADRs)
- `ADR-GC-APPLET-001-drawio-third-party-applet.md` (392 lines) — Third-party applet integration
- `ADR-SC-CHROME-001-v2.md` (557 lines) — Shell chrome architecture v2
- `ADR-SC-CHROME-001-v3.md` (917 lines) — Shell chrome architecture v3

### Feature Specifications
- `SPEC-BUILD-QUEUE-001.md` (531 lines) — Automated build queue pipeline
- `SPEC-CALENDAR-EGG-001-calendar-scheduling-agent.md` (302 lines) — Calendar EGG
- `SPEC-CANVAS-CHATBOT-DIALECT.md` (528 lines) — Canvas chatbot natural language interface
- `SPEC-CANVAS-SURFACE-001-infinite-canvas.md` (275 lines) — Infinite canvas primitive
- `SPEC-CHART-PRIMITIVE-001.md` (319 lines) — Chart visualization primitive
- `SPEC-CODE-EGG-001-code-shiftcenter-monaco-playwright.md` (310 lines) — Code editor EGG
- `SPEC-DATA-LAYER-001.md` (336 lines) — Data persistence layer
- `SPEC-DIALECT-PREFERENCE-001-user-vocabulary-and-shell-dialect.md` (152 lines) — User vocabulary preferences
- `SPEC-EGG-FORMAT-v0.3.1.md` (397 lines) — EGG file format v0.3.1
- `SPEC-EGG-SCHEMA-v1.md` (385 lines) — EGG JSON schema v1
- `SPEC-HAMBURGER-MENU-OVERFLOW.md` (102 lines) — Mobile hamburger menu
- `SPEC-HIVENODE-E2E-001.md` (666 lines) — End-to-end testing strategy
- `SPEC-IR-PRESENCE-TRIGGER-001-ir-presence-triggers.md` (302 lines) — IR presence triggers
- `SPEC-KB-EGG-001-kb-shiftcenter-knowledge-base.md` (277 lines) — Knowledge base EGG
- `SPEC-MONACO-BUS-001-monaco-relay-bus-feedback-loop.md` (231 lines) — Monaco editor relay bus integration
- `SPEC-PANE-MESSAGING-001-envelope-links-bus.md` (239 lines) — Pane messaging architecture (envelope/links/bus)
- `SPEC-PIPELINE-001-UNIFIED-BUILD-PIPELINE.md` (601 lines) — Unified build pipeline
- `SPEC-PORT-RAG-001-rag-pipeline-port.md` (515 lines) — RAG pipeline port from platform
- `SPEC-PORT-SHELL-001-shell-chrome-port.md` (349 lines) — Shell chrome port from platform
- `SPEC-PRESENCE-001-presence-service.md` (272 lines) — User presence service
- `SPEC-RAG-COMPARISON-001.md` (85 lines) — RAG implementation comparison
- `SPEC-REPO-INDEX-001.md` (455 lines) — Repository indexing system
- `SPEC-SCAFFOLD-001-scaffold-float-layout.md` (357 lines) — Float layout scaffolding
- `SPEC-SIM-CHAT-001-simulation-chat-channel.md` (261 lines) — Simulation chat channel
- `SPEC-STALENESS-GUARD.md` (151 lines) — Cache staleness guards
- `SPEC-TABLE-PRIMITIVE-001.md` (207 lines) — Table primitive
- `SPEC-TERMINAL-TO-CANVAS-WIRING.md` (472 lines) — Terminal↔Canvas IR wiring (Status: IMPLEMENTED)
- `SPEC-TSAAS-PROMPT-GOVERNANCE-001.md` (365 lines) — Prompt governance system
- `SPEC-YIJS-001-yjs-integration.md` (245 lines) — Yjs collaborative editing integration

### Planning Documents
- `SHIP-PLAN.md` (170 lines) — Product ship plan
- `WAVE-3-QUEUE-SPECS.md` (372 lines) — Wave 3 build queue specifications
- `WAVE-4-PRODUCT-POLISH.md` (30 lines) — Wave 4 product polish plan
- `WAVE-5-SHIP.md` (27 lines) — Wave 5 ship checklist

### Deployment Specifications (2026-03-13)
- `2026-03-13-1800-SPEC-sdeditor-multi-mode.md` (44 lines)
- `2026-03-13-1801-SPEC-shell-swap-delete-merge.md` (57 lines)
- `2026-03-13-1802-SPEC-wire-envelope-handlers.md` (56 lines)
- `2026-03-13-1803-SPEC-deployment-wiring.md` (82 lines)
- `2026-03-15-0100-SPEC-simdecisions-applet-wiring.md` (104 lines)

### Support Documents
- `PROMPT-BACKLOG-BATCH-INSERT.md` (254 lines) — Prompt for backlog batch inserts
- `RCA-001-backlog-db-wipe-2026-03-13.md` (130 lines) — Root cause analysis: backlog DB wipe
- `NOTE-DES-PORT-COMPARISON-2026-03-14.md` (106 lines) — DES port comparison notes
- `SDK-APP-BUILDER-v0.3.0.md` (1411 lines) — App builder SDK documentation

### Archived Specs (docs/specs/_archive/)
- `SHELL-FRAME-ARCHITECTURE-BRIEF.md` (234 lines)
- `PANE-BEHAVIOR-SPEC.md` (423 lines)
- `backlog-entries-from-memory.md` (33 lines)
- `backlog-pending-adds.md` (27 lines)
- `backlog-recalled-session3.md` (50 lines)
- `backlog-remembered.md` (25 lines)

---

## Queue Backlog (13 specs)

Specs waiting to be picked up by the scheduler:

- `SPEC-DISPATCH-QUEEN-FOXTROT.md` (351 lines) — Dispatch queen coordination
- `SPEC-MCP-002-heartbeat-upgrade.md` (46 lines) — MCP heartbeat upgrade
- `SPEC-MCP-003-queue-state-tool.md` (47 lines) — MCP queue state tool
- `SPEC-MCP-004-dispatch-mcp-json.md` (48 lines) — MCP dispatch JSON format
- `SPEC-MCP-005-telemetry-log-tool.md` (43 lines) — MCP telemetry log tool
- `SPEC-MCP-006-claim-release-tools.md` (51 lines) — MCP claim/release tools
- `SPEC-MCP-007-sync-queue-bridge.md` (46 lines) — MCP queue synchronization bridge
- `SPEC-MCP-008-advisory-heartbeat-ack.md` (44 lines) — MCP heartbeat acknowledgment
- `SPEC-WIKI-104-backlinks-query.md` (64 lines) — Wiki backlinks query
- `SPEC-WIKI-105-wikipane-primitive.md` (67 lines) — Wiki pane primitive
- `SPEC-WIKI-106-markdown-viewer.md` (78 lines) — Markdown viewer component
- `SPEC-WIKI-107-backlinks-panel.md` (77 lines) — Backlinks panel UI
- `SPEC-WIKI-108-egg-integration.md` (62 lines) — Wiki EGG integration

---

## Active Build (2 specs)

Currently being processed by bees:

- `SPEC-FACTORY-009-triage-daemon.md` (67 lines) — Factory triage daemon
- `SPEC-MCP-001-health-endpoint.md` (44 lines) — MCP health endpoint

---

## Needs Review (19 specs)

Queen-generated specs awaiting Q88N review:

- `SPEC-BL-146-BOT-ACTIVITY-PORT.md` (86 lines)
- `SPEC-CHROME-E2-save-derived-egg.md` (66 lines)
- `SPEC-DISPATCH-QUEEN-ALPHA.md` (192 lines)
- `SPEC-DISPATCH-QUEEN-BRAVO.md` (214 lines)
- `SPEC-DISPATCH-QUEEN-CHARLIE.md` (259 lines)
- `SPEC-DISPATCH-QUEEN-DELTA.md` (263 lines)
- `SPEC-DISPATCH-QUEEN-ECHO.md` (286 lines)
- `SPEC-EVENT-LEDGER-GAMIFICATION.md` (632 lines)
- `SPEC-FLAPPY-100-self-learning-v2.md` (129 lines)
- `SPEC-GAMIFICATION-V1.md` (882 lines)
- `SPEC-ML-TRAINING-V1.md` (1293 lines)
- `SPEC-MW-VERIFY-001-full-audit.md` (112 lines)
- `SPEC-OAUTH-FIX-01-verify-code.md` (39 lines)
- `SPEC-OAUTH-FIX-02-railway-deploy.md` (38 lines)
- `SPEC-RAIDEN-000-master-coordination.md` (161 lines)
- `SPEC-WIKI-101-database-schema-tables.md` (73 lines)
- `SPEC-WIKI-103-crud-api-routes.md` (80 lines)
- `SPEC-WIKI-SYSTEM.md` (2078 lines) — **LARGE comprehensive wiki system spec**
- `SPEC-WIKI-V1.md` (603 lines)

---

## Completed Specs (183 specs)

Specs that have been processed by the build queue. See `.deia/audits/2026-04-08/bravo/SPEC-INVENTORY-RAW.txt` for the full list. Key categories:

### Efemera Connector (12 specs) — COMPLETE
- SPEC-EFEMERA-CONN-01 through SPEC-EFEMERA-CONN-12 (all implemented)

### Mobile Workbench (42 specs) — COMPLETE
- SPEC-MW-001 through SPEC-MW-042 (full mobile UI implementation + tests + verification)

### Factory System (8 specs) — COMPLETE
- SPEC-FACTORY-001 through SPEC-FACTORY-008 (dependency resolution, TTL, telemetry, DAG support)

### MCP Integration (6 specs) — COMPLETE
- SPEC-MCP-QUEUE-01 through SPEC-MCP-QUEUE-06 (MCP server integration with queue system)

### Canvas/Keyboard/Voice (15 specs) — COMPLETE
- SPEC-CANVAS3-*, SPEC-KB-001A/B/C, SPEC-MW-001 through MW-005 (canvas polish, keyboard primitive, voice input)

### Wiki System (3 specs) — COMPLETE
- SPEC-WIKI-01, SPEC-WIKI-101, SPEC-WIKI-102 (wiki storage, schema, parser)

### Build Infrastructure (20+ specs) — COMPLETE
- SPEC-EXEC-*, SPEC-INFRA-*, SPEC-SCHED-*, SPEC-INJECT-*, SPEC-PERF-* (executor layer, scheduling, performance)

### Bug Fixes & Polish (50+ specs) — COMPLETE
- SPEC-BUG*, SPEC-REQUEUE*, SPEC-FIX-*, SPEC-VERIFY-* (bug fixes, re-queued tasks, verification)

---

## Design Documents (6 docs)

High-level architectural design documents in `.deia/hive/responses/`:

- `20260314-FLOW-DESIGNER-PORT-ENHANCEMENTS.md` (180 lines) — Flow designer port analysis
- `20260314-TASK-092-FLOW-DESIGNER-SURVEY.md` (647 lines) — Flow designer survey
- `20260314-TASK-092-FLOW-DESIGNER-SURVEY-RESPONSE.md` (114 lines) — Survey response
- `20260314-TASK-093-FLOW-DESIGNER-MAPPING.md` (583 lines) — Flow designer mapping
- `20260328-EFEMERA-CONNECTOR-DESIGN.md` (367 lines) — **Efemera Connector v2 design** (basis for CONN-01 through CONN-12)
- `20260406-MCP-QUEUE-NOTIFICATIONS-DESIGN.md` (544 lines) — MCP queue notifications design

---

## Classification Criteria

For gap analysis, specs are classified as:

- **BUILT** — Feature fully implemented, tests pass, matches spec
- **PARTIAL** — Core functionality exists, but incomplete (missing tests, edge cases, polish)
- **DIVERGED** — Implementation exists but deviates significantly from spec
- **NOT_BUILT** — Spec exists, no corresponding implementation found
- **UNKNOWN** — Insufficient information to determine status (spec too vague, implementation unclear)

---

## File Metadata

- **Total spec documents:** 274
- **Total spec lines:** ~32,000+ lines (estimated from line counts)
- **Largest spec:** SPEC-WIKI-SYSTEM.md (2,078 lines)
- **Oldest canonical spec:** PANE-BEHAVIOR-SPEC.md (archived)
- **Most recent completed:** SPEC-WIKI-102 (2026-03-28)

---

## Search Patterns Used

✓ `docs/specs/**/*.md` — 51 canonical specs
✓ `.deia/hive/queue/backlog/SPEC-*.md` — 13 queued specs
✓ `.deia/hive/queue/_done/SPEC-*.md` — 183 completed specs
✓ `.deia/hive/queue/_active/SPEC-*.md` — 2 active specs
✓ `.deia/hive/queue/_needs_review/SPEC-*.md` — 19 review-needed specs
✓ `.deia/hive/responses/*DESIGN*.md` — 6 design documents

---

**Next Step:** Cross-reference against IMPLEMENTATION-CATALOG.md to identify gaps (SPEC-IMPLEMENTATION-GAP.md)
