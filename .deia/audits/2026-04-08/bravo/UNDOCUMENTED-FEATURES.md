# Undocumented Features

**Generated:** 2026-04-08
**Audit:** BRAVO (Implementation-to-Spec Reverse Mapping)
**Method:** Identify substantial code (>500 LOC or full features) without corresponding specifications

---

## Executive Summary

| Category | Count | Notes |
|----------|-------|-------|
| **Fully Documented** | 115 | Features with clear spec references |
| **Undocumented** | 18 | Substantial code without specs |
| **Organically Evolved** | 12 | Features that grew incrementally without formal design |
| **Infrastructure** | 8 | Operational tools without formal specs |

**Documentation Rate:** 86% (115/133) of implemented features have specifications

---

## Fully Documented Features (115)

These features exist in code AND have clear corresponding specs. See SPEC-IMPLEMENTATION-GAP.md for details.

**Examples:**
- ✓ Terminal primitive (13,698 LOC) → SPEC-MW-024-terminal-mobile-css, SPEC-TERMINAL-TO-CANVAS-WIRING
- ✓ Efemera Connector (3,631 LOC) → SPEC-EFEMERA-CONN-01 through SPEC-EFEMERA-CONN-12
- ✓ RAG module (6,105 LOC) → SPEC-PORT-RAG-001
- ✓ Build Monitor routes (818 LOC) → SPEC-BMON-01-pipeline-dashboard
- ✓ Inventory system (1,050 LOC) → SPEC-LEDGER-01, inventory CLI usage

---

## Undocumented Features (18)

These features exist in the codebase with significant code volume (>500 LOC or complete functionality) but have NO corresponding specification documents.

### Frontend — Undocumented Primitives (0)
**All 27 primitives are documented.** ✓

### Frontend — Undocumented Apps (2)

1. **Build Monitor Adapter** (`apps/buildMonitorAdapter.tsx`, 484 LOC)
   - **Description:** Adapter for build monitor dashboard
   - **Gap:** SPEC-BMON-01 exists for backend routes, but frontend adapter not specified
   - **Severity:** LOW (adapter pattern is standard, no unique logic)

2. **Primitive Preview Adapter** (`apps/primitivePreviewAdapter.tsx`, 185 LOC)
   - **Description:** Dev tool for previewing primitives in isolation
   - **Gap:** No spec for this dev tool
   - **Severity:** LOW (internal dev tool)

### Backend — Undocumented Modules (7)

3. **Playback Module** (`hivenode/playback/`, 390 LOC)
   - **Description:** Session playback/replay functionality
   - **Gap:** No spec found for playback feature
   - **Severity:** MEDIUM (significant feature, 390 LOC)

4. **Services Module** (`hivenode/services/`, 379 LOC)
   - **Description:** Miscellaneous services (unclear scope)
   - **Gap:** No spec for services layer
   - **Severity:** MEDIUM (unclear what's in here)

5. **Node Module** (`hivenode/node/`, 355 LOC)
   - **Description:** Node/tree data structures
   - **Gap:** No spec for node data model
   - **Severity:** LOW (utility module)

6. **Middleware Module** (`hivenode/middleware/`, 235 LOC)
   - **Description:** FastAPI middleware (CORS, auth, etc.)
   - **Gap:** No spec for middleware layer
   - **Severity:** LOW (standard FastAPI patterns)

7. **Rate Loader Module** (`hivenode/rate_loader/`, 96 LOC)
   - **Description:** Rate data loading (pricing? bandwidth?)
   - **Gap:** No spec for rate loader
   - **Severity:** LOW (small module, unclear purpose)

8. **Compare Module** (`hivenode/compare/`, 825 LOC)
   - **Description:** Diff/comparison engine
   - **Gap:** No spec for compare feature
   - **Severity:** MEDIUM (significant feature, 825 LOC)

9. **Adapters Module** (`hivenode/adapters/`, 3,996 LOC)
   - **Description:** Protocol adapters (Slack, etc.)
   - **Gap:** Spec mentions "adapters" but no formal SPEC-ADAPTERS-* document
   - **Severity:** HIGH (largest undocumented module, 3,996 LOC)
   - **Note:** May be organically evolved from platform port

### Backend — Undocumented Routes (5)

10. **Phase NL Routes** (`hivenode/routes/phase_nl_routes.py`, 450 LOC)
    - **Description:** /phase/*, natural language interface for PHASE-IR
    - **Gap:** No SPEC-PHASE-NL-* document found
    - **Severity:** MEDIUM (450 LOC, substantial feature)

11. **Optimization Routes** (`hivenode/routes/optimize_routes.py`, 330 LOC)
    - **Description:** /optimize/*, planning optimization
    - **Gap:** No SPEC-OPTIMIZE-* document found
    - **Severity:** MEDIUM (330 LOC)

12. **Pipeline Sim Routes** (`hivenode/routes/pipeline_sim.py`, 253 LOC)
    - **Description:** /pipeline-sim/*, build timing simulation
    - **Gap:** SPEC-BUILD-QUEUE-001 mentions pipeline, but no detailed spec for simulator
    - **Severity:** LOW (likely supporting feature for build monitor)

13. **Tabletop Routes** (`hivenode/routes/tabletop_routes.py`, 178 LOC)
    - **Description:** /tabletop/*, game simulation
    - **Gap:** No SPEC-TABLETOP-* document found
    - **Severity:** LOW (178 LOC, niche feature)

14. **Build Slots Routes** (`hivenode/routes/build_slots.py`, 18 LOC)
    - **Description:** /build/slots/raw, legacy endpoint
    - **Gap:** Marked as "legacy", likely superseded
    - **Severity:** NEGLIGIBLE (18 LOC, legacy)

### CLI Tools — Undocumented (4)

15. **Service Watchdog** (`_tools/service_watchdog.py`, 294 LOC)
    - **Description:** Health monitoring daemon for services
    - **Gap:** No spec for watchdog
    - **Severity:** LOW (operational tool)

16. **Hivenode Service** (`_tools/hivenode-service.py`, 277 LOC)
    - **Description:** Windows service wrapper for hivenode
    - **Gap:** No spec for Windows service integration
    - **Severity:** LOW (platform-specific wrapper)

17. **Smoke Test DNS** (`_tools/smoke_test_dns.py`, 250 LOC)
    - **Description:** DNS/domain verification tool
    - **Gap:** No spec for DNS smoke tests
    - **Severity:** LOW (operational tool)

18. **Query Index** (`_tools/query_index.py`, 254 LOC)
    - **Description:** Codebase query tool (uses index built by build_index.py)
    - **Gap:** SPEC-REPO-INDEX-001 exists (455 lines), but unclear if query_index is covered
    - **Severity:** LOW (supporting tool for repo index)

---

## Organically Evolved Features (12)

These features likely grew incrementally without formal specs, through iterative development or ports from the platform repo.

### Governance System (Likely Evolved)
- **Governance Module** (`hivenode/governance/`, 1,111 LOC)
- **Gap:** No SPEC-GOVERNANCE-* or SPEC-RBAC-* document found
- **Evidence:** SPEC-EFEMERA-CONN-09 mentions "RBAC system", suggesting governance exists but wasn't formally specified
- **Hypothesis:** Ported from platform repo, no spec written during port

### Privacy System (Likely Evolved)
- **Privacy Module** (`hivenode/privacy/`, 1,063 LOC)
- **Gap:** No SPEC-PRIVACY-* document found
- **Hypothesis:** Compliance/filtering layer added organically

### Sync System (Likely Evolved)
- **Sync Module** (`hivenode/sync/`, 1,152 LOC)
- **Gap:** No SPEC-SYNC-* document found
- **Evidence:** Sync routes exist (233 LOC), but no formal sync spec
- **Hypothesis:** State synchronization layer evolved with real-time features

### Storage System (Likely Evolved)
- **Storage Module** (`hivenode/storage/`, 1,826 LOC)
- **Gap:** No SPEC-STORAGE-* document found
- **Evidence:** SPEC-CLOUD-STORAGE-RAILWAY exists (74 lines), but only covers Railway deployment, not storage architecture
- **Hypothesis:** File/blob storage evolved from S3/cloud integration

### Terminal Backend (Likely Evolved)
- **Terminal Module** (`hivenode/terminal/`, 703 LOC)
- **Gap:** SPEC-TERMINAL-TO-CANVAS-WIRING exists (472 lines), but no SPEC-TERMINAL-BACKEND-*
- **Evidence:** Terminal primitive has spec, backend state management undocumented
- **Hypothesis:** Backend evolved to support frontend primitive

### Canvas Backend (Likely Evolved)
- **Canvas Module** (`hivenode/canvas/`, 653 LOC)
- **Gap:** SPEC-CANVAS-SURFACE-001 exists (275 lines), but no SPEC-CANVAS-BACKEND-*
- **Evidence:** Canvas primitive has spec, backend persistence layer undocumented
- **Hypothesis:** Backend evolved to persist canvas state

### Prism Color System (Likely Evolved)
- **Prism Module** (`hivenode/prism/`, 110 LOC)
- **Gap:** No SPEC-PRISM-* document found
- **Evidence:** Hard rule #3 is "NO HARDCODED COLORS. Only CSS variables (`var(--sd-*)`)"
- **Hypothesis:** Color system evolved organically to enforce CSS variable usage

### Early Access Flags (Likely Evolved)
- **Early Access Module** (`hivenode/early_access/`, 103 LOC)
- **Gap:** No SPEC-EARLY-ACCESS-* or SPEC-FEATURE-FLAGS-* document found
- **Evidence:** Early access routes exist (56 LOC), but no formal spec
- **Hypothesis:** Feature flag system added for gradual rollout

### Preferences System (Likely Evolved)
- **Preferences Module** (`hivenode/preferences/`, 75 LOC)
- **Gap:** No SPEC-PREFERENCES-* document found
- **Evidence:** SPEC-DIALECT-PREFERENCE-001 exists (152 lines), but describes "dialect preference", not generic preferences store
- **Hypothesis:** Generic preferences store evolved beyond dialect-specific storage

### Build Monitor Liveness (Likely Evolved)
- **Build Monitor Liveness Routes** (`hivenode/routes/build_monitor_liveness.py`, 66 LOC)
- **Gap:** SPEC-BMON-01 exists (103 lines), but no mention of liveness endpoints
- **Evidence:** Build monitor has claims/slots routes (148/80 LOC), liveness added later
- **Hypothesis:** Liveness health checks added to support build monitoring

### Build Monitor Claims (Likely Evolved)
- **Build Monitor Claims Routes** (`hivenode/routes/build_monitor_claims.py`, 148 LOC)
- **Gap:** SPEC-BMON-01 exists (103 lines), but claims detail unclear
- **Hypothesis:** Claims system evolved to manage slot reservations

### Build Monitor Slots (Likely Evolved)
- **Build Monitor Slots Routes** (`hivenode/routes/build_monitor_slots.py`, 80 LOC)
- **Gap:** SPEC-BMON-01 exists (103 lines), but slots detail unclear
- **Hypothesis:** Slots system evolved to manage worker pools

---

## Infrastructure Without Specs (8)

These are operational tools or supporting scripts that typically don't require formal specifications.

### CLI Tools (8)
1. **Retrofit Eggs** (`_tools/retrofit_eggs.py`, 69 LOC) — EGG format migration (supporting)
2. **Queue Monitor Timer** (`_tools/queue_monitor_timer.py`, 65 LOC) — Queue monitoring loop (supporting)
3. **Perf Find Loop** (`_tools/perf_find_loop.py`, 64 LOC) — Loop detection tool (supporting)
4. **Inventory DB** (`_tools/inventory_db.py`, 64 LOC) — Database utilities (supporting)
5. **Cloudflare Update DNS** (`_tools/cf_update_dns.py`, 63 LOC) — DNS record updater (supporting)
6. **Count Color Violations** (`_tools/count_color_violations.py`, 51 LOC) — CSS color validator (supporting)
7. **Migrate Inventory to PG** (`_tools/migrate_inventory_to_pg.py`, 139 LOC) — Database migration utility (one-time)
8. **Generate Policy Recommendations** (`_tools/generate_policy_recommendations.py`, 102 LOC) — Policy suggestion engine (experimental?)

**Note:** These tools are operational utilities. Formal specs are not typically required.

---

## Gap Analysis by Severity

### HIGH Severity (1 feature)
- **Adapters Module** (3,996 LOC) — Largest undocumented module

### MEDIUM Severity (5 features)
- **Playback Module** (390 LOC)
- **Services Module** (379 LOC)
- **Compare Module** (825 LOC)
- **Phase NL Routes** (450 LOC)
- **Optimization Routes** (330 LOC)

### LOW Severity (12 features)
- Various CLI tools, small modules, dev tools

---

## Recommendations

### Immediate Actions (HIGH/MEDIUM severity)
1. **Document Adapters Module** — 3,996 LOC, largest gap
   - Write SPEC-ADAPTERS-001-protocol-adapters.md
   - Document Slack, Discord, email, webhook adapters

2. **Document Compare Module** — 825 LOC, diff engine
   - Write SPEC-COMPARE-001-diff-engine.md
   - Clarify use cases (file diff, IR diff, etc.)

3. **Document Phase NL Routes** — 450 LOC, natural language interface
   - Write SPEC-PHASE-NL-001-natural-language-interface.md
   - Clarify how it differs from canvas chat

4. **Document Playback Module** — 390 LOC, session replay
   - Write SPEC-PLAYBACK-001-session-replay.md
   - Clarify use cases (debugging, audit, training?)

5. **Document Optimization Routes** — 330 LOC, planning optimization
   - Write SPEC-OPTIMIZE-001-planning-optimization.md
   - Clarify what's being optimized (schedules, resources, IR?)

### Secondary Actions (Organically Evolved)
6. **Governance Module** — 1,111 LOC
   - Write SPEC-GOVERNANCE-001-rbac-system.md
   - Document roles, permissions, policy enforcement

7. **Storage Module** — 1,826 LOC
   - Expand SPEC-CLOUD-STORAGE-RAILWAY beyond deployment
   - Write SPEC-STORAGE-001-file-blob-storage.md

8. **Sync Module** — 1,152 LOC
   - Write SPEC-SYNC-001-state-synchronization.md
   - Document conflict resolution, optimistic updates

9. **Privacy Module** — 1,063 LOC
   - Write SPEC-PRIVACY-001-data-filtering.md
   - Document PII handling, compliance

### Low Priority (Infrastructure)
10. **Document remaining CLI tools** — As needed for onboarding/handoff

---

## Key Findings

1. **86% documentation rate** — 115/133 features have specs
2. **Adapters module is the largest gap** — 3,996 LOC undocumented
3. **Most primitives are documented** — 27/27 primitives have specs
4. **Backend modules have gaps** — 7 modules (7/28 = 25%) undocumented
5. **Routes mostly documented** — 5 route groups (5/32 = 16%) undocumented
6. **Organic evolution common** — 12 features evolved without formal design
7. **Infrastructure appropriately unspecified** — 8 CLI tools are operational utilities

---

## Conclusion

The ShiftCenter codebase has **strong specification coverage** (86%), especially for frontend primitives (100% documented). The main gaps are:

- **Backend service modules** — governance, storage, sync, privacy evolved without specs
- **Protocol adapters** — 3,996 LOC module with no spec
- **Natural language interfaces** — phase_nl, optimize routes lack formal design
- **Supporting features** — compare, playback, services modules undocumented

These gaps are typical for:
- **Ported code** (from platform repo, specs left behind)
- **Organic growth** (features added incrementally without formal design)
- **Infrastructure** (operational tools that don't need specs)

**Recommendation:** Prioritize specs for high-LOC modules (adapters, storage, sync, governance) and customer-facing features (phase_nl, optimize, playback). Infrastructure tools can remain unspecified.
