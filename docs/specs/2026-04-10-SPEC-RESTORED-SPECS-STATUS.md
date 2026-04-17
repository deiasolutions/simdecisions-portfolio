# SPEC: Restored Specs — Status & Remaining Work

**Date:** 2026-04-10
**Author:** Q33NR (post-ESC-002 analysis)
**Status:** Status document (not a build spec — this is the work definition for what follows)
**Scope:** The 8 specs restored from shiftcenter git history during ESC-001/ESC-002 escalation cleanup

---

## Context

On 2026-04-10, the escalation cleanup arc (ESC-001 survey → ESC-002 restore) pulled 8 clean specs out of shiftcenter git history and placed them in `simdecisions/.deia/hive/queue/_needs_review/` as uncommitted working-tree changes.

After an automated gap survey against the simdecisions codebase, **4 of the 8 are already done or obsolete**. Only **4 have real work remaining**, and of those, only **1 is a small self-contained task**. The other 3 are large epics that need decomposition before dispatch.

This document captures:
1. Current state of all 8 restored specs
2. Real work remaining (4 specs)
3. Dependency graph
4. Recommended build sequence
5. Housekeeping actions before build starts

---

## 1. Restored Spec Status Matrix

| Spec | File Size | Status | Disposition |
|------|-----------|--------|-------------|
| SPEC-WIKI-V1 | 17 KB | **DONE** | Archive to `_done/` |
| SPEC-WIKI-103-crud-api-routes | 3.2 KB | **DONE** | Archive to `_done/` |
| SPEC-RAIDEN-000-master-coordination | 6.6 KB | **DONE** | Archive to `_done/` |
| SPEC-WIKI-SYSTEM | 63 KB | **OBSOLETE** | Archive to `_wrong-product/` (it's for FamilyBondBot, not shiftcenter/simdecisions) |
| SPEC-WIKI-108-egg-integration | 2.1 KB | **NOT_STARTED** | Dispatch as single bee task |
| SPEC-EVENT-LEDGER-GAMIFICATION | 17 KB | **PARTIAL** | Decompose into 1-2 sub-specs |
| SPEC-GAMIFICATION-V1 | 26 KB | **NOT_STARTED** | Decompose into 5-7 sub-specs |
| SPEC-ML-TRAINING-V1 | 36 KB | **NOT_STARTED** | Decompose into 8+ sub-specs |

---

## 2. Evidence for DONE/OBSOLETE Classifications

### SPEC-WIKI-V1 — DONE
**Backend** (`packages/core/src/simdecisions/core/wiki/`):
- `store.py` — wiki_pages table with path, title, content, version, is_current, previous_version_id, is_deleted, frontmatter (JSONB), outbound_links (JSONB); wiki_edit_log table for audit
- `parser.py` — parse_wikilinks(), parse_frontmatter()
- `routes.py` — mounted CRUD routes
- `schemas.py` — Pydantic request/response models
- `tests/test_routes.py`, `tests/test_parser.py`

**Frontend** (`packages/browser/src/primitives/wiki/`):
- `WikiPane.tsx` — layout with tree browser + markdown viewer + backlinks panel
- `BacklinksPanel.tsx`
- `MarkdownViewer.tsx` — renders markdown with wikilink navigation
- `wikiAdapter.ts` — loads pages from API, structures tree
- `__tests__/WikiPane.integration.test.tsx`, `BacklinksPanel.test.tsx`, `wikiAdapter.test.tsx`

**Conclusion:** Fully functional. No work needed.

### SPEC-WIKI-103-crud-api-routes — DONE
All 6 routes implemented in `packages/core/src/simdecisions/core/wiki/routes.py`:
- `POST /api/wiki/pages`
- `GET /api/wiki/pages`
- `GET /api/wiki/pages/{path}`
- `PUT /api/wiki/pages/{path}`
- `DELETE /api/wiki/pages/{path}`
- `GET /api/wiki/pages/{path}/history`
- `GET /api/wiki/pages/{path}/backlinks` (bonus, beyond spec)

Features working: automatic frontmatter + wikilink parsing on save, versioning via previous_version_id, soft delete, history retrieval, backlinks query. 8+ integration tests present.

**Conclusion:** All acceptance criteria met.

### SPEC-RAIDEN-000-master-coordination — DONE
This is a **meta-coordination spec** (role: queen) that decomposed into RAIDEN-101 through RAIDEN-109, which were executed separately. The final deliverable is at:
- `packages/browser/public/games/raiden-v1-20260408.html`
- Backup: `raiden-v1-20260408.html.backup`

Game implementation includes:
- 10-level vertical shmup, boss fights, weapon progression
- Canvas-based 60fps game loop with entity pooling
- PC keyboard + mobile touch controls (joystick + bomb button)
- Multiple enemy types (GRUNT, FIGHTER, INTERCEPTOR, TRACTOR, CHARGER, TANK, HEAVY, BOSS, MINI_BOSS)
- Score system with combo multiplier
- Synthesized sound effects via Web Audio API
- Single-file HTML (no build step)

**Conclusion:** Coordination executed, build delivered, game playable. The meta-spec's job is done.

### SPEC-WIKI-SYSTEM — OBSOLETE
**Red flag:** This spec references **FamilyBondBot (FBB)**, a family-support product with clinical concepts like `loyalty_binds`, `coercive_control`, `parental_alienation`, family member tokens (DS001, DD001, CP001), and guardrails like "never diagnose, crisis response."

This is not a shiftcenter/simdecisions spec. It was apparently misfiled into the shiftcenter `_stage/` directory and survived the escalation loop. The entire concept (clinical wiki + family wiki + trainer-maintained knowledge base) is inapplicable to this project.

**Conclusion:** Wrong product. Archive to `docs/specs/_wrong-product/` or similar. Do NOT build.

---

## 3. Real Work Remaining (4 Specs)

### 3.1 SPEC-WIKI-108 — Wiki EGG Integration ⭐ QUICK WIN

**Status:** NOT_STARTED
**Size:** Small, ~2 hours, single bee dispatch
**Dependencies:** None (WIKI-107 backlinks already done)
**Priority:** P1 (unblocks wiki discoverability)

**What's required:**
1. Create `eggs/wiki.set.md` — EGG definition registering wiki as a discoverable app
   - Metadata: `egg: wiki`, `version: 1.0.0`, `displayName: Wiki`
   - Layout: tree-browser + wiki primitive panes
   - Config for wikiAdapter (API endpoint, workspace_id)
2. Create `packages/browser/e2e/wiki.spec.ts` — Playwright E2E test
   - Start backend server
   - Create test pages via API (with wikilinks)
   - Load wiki via `?egg=wiki`
   - Verify tree renders pages
   - Click page, verify content renders
   - Click wikilink, verify navigation
   - Verify backlinks panel shows correct pages
   - Clean up test pages

**Blocker impact:** Without `wiki.set.md`, the wiki exists in code but cannot be mounted as a standalone egg. This is a 2-hour blocker on wiki discoverability.

**Recommended dispatch:** Single Sonnet bee, standard `.deia/hive/tasks/` task file, 2-hour cap.

**Acceptance criteria:**
- [ ] `eggs/wiki.set.md` exists and parses as valid EGG config
- [ ] Loading `http://localhost:5173/?egg=wiki` renders the wiki UI
- [ ] `wiki.spec.ts` passes on clean database
- [ ] E2E test is idempotent (can run multiple times)
- [ ] No file over 500 lines

---

### 3.2 SPEC-EVENT-LEDGER-GAMIFICATION — Event Kinds + Scoring Rules

**Status:** PARTIAL (ledger core is done, gamification consumer layer is not)
**Size:** Medium, ~1 focused spec
**Dependencies:** Event ledger core (already built)
**Priority:** P0 (prerequisite for all gamification work)

**What exists:**
- `packages/core/src/simdecisions/core/ledger/`
  - `schema.py` — event table with event_type, actor, target, payload, hash chain
  - `emitter.py` — `emit_event()` API
  - `writer.py` — hash chain integrity
  - `reader.py`, `aggregation.py`, `export.py`
- Tests for hash chain integrity, canonical JSON normalization, event emission
- Currency fields present in schema (clock, coin, carbon) but not populated in event emission

**What's missing:**
1. **Canonical event kinds enum** — define the gamification-relevant event types:
   - `TASK_APPROVED`, `TASK_REJECTED`
   - `WIKI_PAGE_CREATED`, `WIKI_PAGE_UPDATED`, `WIKI_PAGE_LINKED`
   - `NOTEBOOK_RUN`
   - `EGG_PACKED`, `EGG_LOADED`
   - `REVIEW_STARTED`, `REVIEW_COMPLETED`
   - `BUG_CAUGHT`, `BUG_FIXED`
   - `DEPLOY_STARTED`, `DEPLOY_COMPLETED`
2. **Actor type enforcement** — schema-level validation that actor is one of `human`, `bee`, `system`
3. **Currency tracking in emission** — update `emit_event()` callers to populate `clock_ms`, `coin_usd`, `carbon_kg` where applicable
4. **Scoring rules registry** — storage for rules like:
   - `TASK_APPROVED → +100 XP`
   - `WIKI_PAGE_CREATED → +50 XP`
   - `BUG_CAUGHT → +25 XP`
   - Storage options: JSONB config table, `.md` file in `.deia/config/`, or Python module
5. **Replayability guarantee** — scoring rules must be versioned so historic events can be re-scored deterministically

**Recommended dispatch:** Sonnet bee, single spec with schema migration + event kind enum + scoring rules file + replay test. Or have Q33N decompose into 2 sub-specs if it balloons past 500 lines.

---

### 3.3 SPEC-GAMIFICATION-V1 — User Progression System

**Status:** NOT_STARTED
**Size:** Large, ~5-7 sub-specs
**Dependencies:** SPEC-EVENT-LEDGER-GAMIFICATION (must complete first)
**Priority:** P0

**What's required (high-level):**
1. **Database schema** — `user_progression` table with:
   - `xp` (int), `level` (int)
   - Streak tracking (consecutive days active, last active date)
   - `badges` (JSONB array)
   - `stats` (JSONB for per-category counts)
2. **XP Calculator** — module that reads events from ledger, applies scoring rules, computes xp_delta. Must be **replayable** (given event history + rules version, produces same result).
3. **Badge Engine** — pattern matching on event history to award badges retroactively. Badges should be addable without re-writing history (new badge rule → scan history → award).
4. **Progression Routes** — FastAPI routes:
   - `GET /api/progression/{user_id}` — current state
   - `POST /api/progression/{user_id}/recompute` — force recalculation from event history
   - `GET /api/progression/leaderboard` — top users by xp
5. **Progression State Wiki Page** — auto-maintained wiki page at `user/progression.md` per user, updated on xp changes (uses WIKI-V1 subsystem)
6. **Dashboard Widget** — React primitive showing:
   - XP bar with level progress
   - Current level
   - Recent badges (last 5)
   - Streak counter with flame icon
   - Integrated into morning report
7. **Integration tests** — end-to-end: emit event → calculator runs → progression updates → widget reflects

**Recommended decomposition (Q33N task):**
- `SPEC-GAM-01-progression-schema` — DB table + migration
- `SPEC-GAM-02-xp-calculator` — scoring engine with replay
- `SPEC-GAM-03-badge-engine` — pattern matcher with retroactive award
- `SPEC-GAM-04-progression-routes` — FastAPI endpoints
- `SPEC-GAM-05-progression-widget` — React primitive
- `SPEC-GAM-06-progression-wiki-integration` — auto-maintained wiki page
- `SPEC-GAM-07-morning-report-hook` — morning report integration + E2E test

**Estimated dispatch budget:** 7 bee dispatches, mix of Sonnet (02, 03, 05) and Haiku (01, 04, 06, 07).

---

### 3.4 SPEC-ML-TRAINING-V1 — ML Surrogate + Preference Pair System

**Status:** NOT_STARTED
**Size:** Very large, ~8+ sub-specs
**Dependencies:** SPEC-GAMIFICATION-V1, SPEC-EVENT-LEDGER-GAMIFICATION
**Priority:** P1 (defer until gamification is solid)

**What's required (high-level):**
1. **Surrogate model system** — stored model artifacts, versioning, loading
2. **Preference pair system** — `@ml_feature` and `@ml_label` decorators for tagging code outputs
3. **Training data collection framework** — automatic harvesting from event ledger + pref pairs
4. **Embedding generation** — convert text/code/events into vectors
5. **Calibration system** — model confidence calibration
6. **RLHF pipeline** — reward model training loop
7. **Surrogate inference routes** — serve model predictions via API
8. **Monitoring / drift detection** — production model health

**Recommended decomposition:** 8+ sub-specs. This should not be attempted until:
- GAMIFICATION-V1 is fully built and producing stable XP/badge data
- Event ledger has at least 30 days of production events for training data
- A clear product use case for the surrogate model is defined

**Recommended action right now:** Park this spec. Do NOT decompose or dispatch. Revisit after gamification is in production for 30+ days.

---

## 4. Dependency Graph

```
SPEC-EVENT-LEDGER-GAMIFICATION (P0)
         │
         ├──▶ SPEC-GAMIFICATION-V1 (P0)
         │            │
         │            ├──▶ SPEC-ML-TRAINING-V1 (P1, deferred)
         │            │
         │            └──▶ (dashboards, leaderboards, reports)
         │
         └──▶ (other event consumers: audit, billing, analytics)

SPEC-WIKI-108 (P1)  ← INDEPENDENT, can dispatch anytime
```

**Critical path:** EVENT-LEDGER-GAMIFICATION → GAMIFICATION-V1 → ML-TRAINING-V1
**Parallel work:** WIKI-108 can be dispatched independently at any time.

---

## 5. Recommended Build Sequence

### Phase 0 — Housekeeping (no dispatch, direct file ops)
1. Archive the 3 DONE specs to `.deia/hive/queue/_done/`:
   - `SPEC-WIKI-V1.md`
   - `SPEC-WIKI-103-crud-api-routes.md`
   - `SPEC-RAIDEN-000-master-coordination.md`
2. Move the 1 OBSOLETE spec to `docs/specs/_wrong-product/`:
   - `SPEC-WIKI-SYSTEM.md` (with a README explaining it's FamilyBondBot, not shiftcenter)
3. Leave the 4 real-work specs in `_needs_review/` until they're ready to dispatch
4. Commit the cleanup as a single atomic commit in simdecisions

### Phase 1 — Quick Win (1 bee dispatch)
5. Write task file for WIKI-108 (convert the spec to a task file with concrete simdecisions paths)
6. Dispatch WIKI-108 as a single Sonnet bee (~2 hours)
7. Review output, verify wiki loads at `?egg=wiki`, commit

### Phase 2 — Event Ledger Gamification Layer (Q33N decompose + dispatch)
8. Dispatch Q33N to decompose SPEC-EVENT-LEDGER-GAMIFICATION into 1-2 sub-specs (event kinds + scoring rules registry)
9. Dispatch each sub-spec as a bee
10. Review + commit

### Phase 3 — Gamification Build (Q33N decompose + 5-7 bee dispatches)
11. Dispatch Q33N to decompose SPEC-GAMIFICATION-V1 into ~7 sub-specs (see proposed IDs in §3.3)
12. Dispatch each sub-spec, respecting dependencies (GAM-01 schema first, then GAM-02/03 in parallel, then GAM-04/05/06/07)
13. Review, E2E test, commit
14. Deploy to production
15. Let it bake for 30+ days to collect event data

### Phase 4 — ML Training (deferred, review before starting)
16. After 30+ days of production gamification, reassess SPEC-ML-TRAINING-V1
17. Only decompose + dispatch if there is a clear product use case for the surrogate model
18. If yes, Q33N decomposition → 8+ bee dispatches
19. If no, archive ML-TRAINING-V1 with a note

---

## 6. Success Criteria (for this status spec)

- [ ] The 3 DONE specs are moved to `_done/` and no longer visible in `_needs_review/`
- [ ] The 1 OBSOLETE spec is moved to `_wrong-product/` with an explanatory README
- [ ] `_needs_review/` contains only the 4 real-work specs (WIKI-108, EVENT-LEDGER-GAM, GAMIFICATION-V1, ML-TRAINING-V1)
- [ ] A single atomic commit captures the housekeeping
- [ ] Phase 1 (WIKI-108) is ready to dispatch with a concrete task file
- [ ] Phase 2 and Phase 3 decomposition plans are documented (this spec §3.2 and §3.3)
- [ ] Phase 4 (ML) is explicitly deferred with a 30-day review trigger

---

## 7. Notes

### Why the restored specs are "ghosts"
Several of the restored specs were already built in shiftcenter before the simdecisions cutover. The simdecisions codebase inherited the code but not the spec files (which had been polluted by the triage daemon's escalation loop). The ESC-001/002 cleanup restored the clean specs from shiftcenter git history, but didn't check whether the work itself was already complete in simdecisions. This status spec closes that gap.

### Why SPEC-WIKI-SYSTEM is a wrong-product spec
The spec appears to have been drafted for a separate project called **FamilyBondBot (FBB)** — possibly by the same author using the same DEIA hive scaffolding. It got filed into the shiftcenter `_stage/` directory, survived the escalation loop, and was restored by ESC-002. It has no business being in this repo. The correct action is to preserve it (the work is presumably valuable to whoever owns FBB) but move it out of the shiftcenter/simdecisions spec queue.

### Costs so far (escalation cleanup arc)
- ESC-001 survey: $2.65
- ESC-002 scope update (Q33N): $1.43
- ESC-002 restore (Haiku bee): $0.48
- Intent preservation doc: negligible (direct write)
- Gap matrix survey (Explore agent): negligible
- **Total cleanup cost: ~$4.56**

### Expected costs for real work
- **Phase 1 (WIKI-108):** ~$1.50 (single Sonnet bee, ~2 hours)
- **Phase 2 (Event Ledger Gam):** ~$3-5 (Q33N + 1-2 bees)
- **Phase 3 (Gamification):** ~$15-25 (Q33N + 7 bees, Sonnet/Haiku mix)
- **Phase 4 (ML):** deferred, unknown
- **Estimated total through Phase 3:** ~$20-35

---

**END OF STATUS SPEC**
