# DAMAGE REPORT: Unauthorized git reset --hard HEAD

**From:** Q33NR
**To:** Q88N
**Date:** 2026-03-15 ~17:30
**Severity:** P0 — all uncommitted tracked-file work wiped
**Rebuild timer:** starts when first queue spec is picked up

---

## Forensic Findings

**Culprit: UNKNOWN.** Searched 349 bee RAW response files and all 4 automation scripts (run_queue.py, dispatch.py, ship_feeder.py, build_monitor.py). Zero hits for `git reset`, `git checkout`, `git restore`, `git clean`, `git stash`. The reset left a reflog entry (`HEAD@{0}: reset: moving to HEAD`) but no bee logged running it. Possible causes:
- A bee ran it without logging (Claude Code auto-approved a destructive command)
- An external tool/IDE triggered it
- A permission auto-allow pattern matched a git command

**Hard Rule #10 was violated.** No git write ops without Q88N approval.

---

## What Survived (untracked `??` files — not affected by reset)

All NEW files created by bees survived. Canvas modules, DES routes, RAG routes, chunker, embedder, MaximizedOverlay, all new test files, all `.deia/hive/` files. These are fine.

---

## What Was Lost — Full Manifest with Recovery Sources

Legend: **S** = Spec | **T** = Task file | **R** = Response | **F** = Feature inventory | **B** = Backlog | **P** = Platform source

---

### 1. Route Registration (hivenode/routes/__init__.py)
**4 tasks added import+registration lines — ALL LOST**

| Task | What was added | Recovery Sources |
|------|----------------|------------------|
| TASK-146 | DES routes import + registration | **T** `.deia/hive/tasks/2026-03-15-TASK-146-port-des-engine-routes.md` **R** `20260315-TASK-146-RESPONSE.md` **F** `FEAT-146` (22 tests) |
| TASK-157 | RAG routes import + registration | **T** `.deia/hive/tasks/2026-03-15-TASK-157-port-rag-routes.md` **R** `20260315-TASK-157-RESPONSE.md` **S** `docs/specs/SPEC-PORT-RAG-001-rag-pipeline-port.md` |
| TASK-165 | Canvas chat routes import + registration | **T** `.deia/hive/tasks/2026-03-15-TASK-165-port-canvas-chatbot-dialect.md` **R** `20260315-TASK-165-RESPONSE.md` **S** `docs/specs/SPEC-CANVAS-CHATBOT-DIALECT.md` |
| TASK-166 | Phase NL routes (if applicable) | **T** `.deia/hive/tasks/2026-03-15-TASK-166-wire-canvas-route-target.md` **R** `20260315-TASK-166-RESPONSE.md` **S** `docs/specs/SPEC-TERMINAL-TO-CANVAS-WIRING.md` |

**Recoverable: YES** — all simple 2-line additions, fully documented in responses

---

### 2. RAG Indexer Exports (hivenode/rag/indexer/__init__.py)
**5 tasks layered imports/exports — ALL LOST**

| Task | What was added | Recovery Sources |
|------|----------------|------------------|
| TASK-151 | Model exports | **T** `2026-03-15-TASK-151-port-rag-models.md` **R** `20260315-TASK-151-RESPONSE.md` **F** `FEAT-155` (22 tests) |
| TASK-152 | Scanner import + export | **T** `2026-03-15-TASK-152-port-rag-scanner.md` **R** `20260315-TASK-152-RESPONSE.md` **S** `SPEC-PORT-RAG-001` |
| TASK-153 | Chunker import + export | **T** `2026-03-15-TASK-153-port-rag-chunker.md` **R** `20260315-TASK-153-RESPONSE.md` **S** `SPEC-PORT-RAG-001` |
| TASK-155 | IndexStorage + compute_content_hash | **T** `2026-03-15-TASK-155-port-rag-storage.md` **R** `20260315-TASK-155-RESPONSE.md` |
| TASK-161 | IndexerService import + __all__ | **T** `2026-03-15-TASK-161-fix-rag-indexer-imports.md` **R** `20260315-TASK-161-RESPONSE.md` |

**Recoverable: YES** — each response specifies exactly what was added. Also: **P** `platform/efemera/src/efemera/rag/` has the original source.

---

### 3. Shell Chrome CSS Fixes (TASK-158) + Menu Bar CSS (this session)
**3 files, 4 rgba replacements + ~150 lines menu CSS — LOST**

| File | Change | Recovery Sources |
|------|--------|------------------|
| ShellTabBar.tsx line 150 | `rgba(0,0,0,0.15)` → `var(--sd-shadow-sm)` | **R** `20260315-TASK-158-RESPONSE.md` (exact lines) |
| WorkspaceBar.tsx lines 57, 146, 230 | 3 rgba → var replacements | **R** `20260315-TASK-158-RESPONSE.md` (exact lines) |
| shell.css | Menu dropdown/modal CSS (~150 lines) | **P** `platform/simdecisions-2/src/components/shell/shell.css` lines 551-730 **S** `SPEC-PORT-SHELL-001` |

**Recoverable: YES** — response has exact line numbers and old/new values. Platform source has the CSS verbatim.

---

### 4. Auth/Identity Wiring (TASK-133, 136, 137, 138)
**~10 tracked files modified — LOST**

| Task | Files Modified | Recovery Sources |
|------|----------------|------------------|
| TASK-133 | SpotlightOverlay.test.tsx (3 selectors) | **R** `20260315-TASK-133-RESPONSE.md` (exact lines 56, 83, 137) |
| TASK-136 | ra96it/models.py, schemas.py, config.py, jwt.py, main.py | **T** `2026-03-15-TASK-136-ra96it-github-oauth-jwks.md` **R** `20260315-TASK-136-RESPONSE.md` **B** `BL-027` (rate limiting on auth routes) |
| TASK-137 | browser/src/apps/index.ts (AuthAdapter registration) | **R** `20260315-TASK-137-RESPONSE.md` **F** `FEAT-137` (323 tests) |
| TASK-138 | hivenode dependencies.py, config.py, main.py, auth.py, conftest, test_auth_routes | **T** `2026-03-15-TASK-138-hivenode-jwks-cache-family-aud.md` **R** `20260315-TASK-138-RESPONSE.md` |

**Recoverable: PARTIAL** — TASK-136/138 responses describe changes but may lack full code. Platform source (`platform/ra96it/`) has originals. **S** `SPEC-LOCALHOST-DEPLOYMENT-JWT.docx` has JWT spec.

---

### 5. Sim Integration (TASK-140, 141)
**~5 tracked files modified — LOST**

| Task | Files Modified | Recovery Sources |
|------|----------------|------------------|
| TASK-140 | browser/src/apps/index.ts (SimAdapter reg) | **R** `20260315-TASK-140-RESPONSE.md` **F** `FEAT-140` (126 tests) |
| TASK-141 | hivenode/routes/sim.py (stub→real), schemas_sim.py, test_sim_routes.py, engine/des/engine.py | **R** `20260315-TASK-141-RESPONSE.md` **F** `FEAT-141` (36 tests) **B** `BL-037` (DES engine port) |

**Recoverable: YES** — response has before/after line counts. **P** `platform/efemera/src/efemera/des/` has original engine code.

---

### 6. Terminal Canvas Wiring (TASK-166)
**2 files modified — LOST**

| File | Change | Recovery Sources |
|------|--------|------------------|
| terminal/types.ts | 'canvas' routeTarget + metrics field | **R** `20260315-TASK-166-RESPONSE.md` **S** `docs/specs/SPEC-TERMINAL-TO-CANVAS-WIRING.md` |
| terminal/useTerminal.ts | Canvas mode handler (lines 445-517) | **R** `20260315-TASK-166-RESPONSE.md` **S** `SPEC-TERMINAL-TO-CANVAS-WIRING.md` |

**Recoverable: YES** — response specifies exact lines and implementation. Spec has architecture.

---

### 7. Miscellaneous Small Fixes (TASK-126A, 132, 139)
**~5 tracked files — LOST**

| Task | File | Change | Recovery Sources |
|------|------|--------|------------------|
| TASK-126A | hivenode/main.py | Inventory store init enhancement | **R** `20260315-TASK-126A-RESPONSE.md` |
| TASK-132 | pyproject.toml | Added "engine.des" to setuptools | **R** `20260315-TASK-132-RESPONSE.md` |
| TASK-132 | tests/engine/des/test_des_ledger_emission.py | Platform imports → MockLedger | **R** `20260315-TASK-132-RESPONSE.md` |
| TASK-139 | FileOperations.test.tsx | CloudAPIClient mock restructure | **R** `20260315-TASK-139-RESPONSE.md` |

**Recoverable: YES** — responses specify exact changes

---

### 8. Config & Inventory
**~6 files — LOST**

| File | Recovery Sources |
|------|------------------|
| browser/package.json | Diff unknown scope — may need manual review |
| eggs/sim.egg.md | **R** `20260315-TASK-140-RESPONSE.md` **F** `FEAT-140` |
| docs/FEATURE-INVENTORY.md + 3 CSVs | Regenerable: `python _tools/inventory.py export-md` |
| .deia/config/queue.yml | Already in HEAD (commit a9e050c) — NOT actually lost |

**Recoverable: MOSTLY** — inventory is regenerable, sim.egg.md is in response file. package.json diff is uncertain.

---

## Summary

| # | Category | Files | Recoverable | Sources Available |
|---|----------|-------|-------------|-------------------|
| 1 | Route registration | 1 | YES | T + R + F |
| 2 | RAG exports | 1 | YES | T + R + S + P |
| 3 | Shell CSS | 3 | YES | R + P + S |
| 4 | Auth wiring | ~10 | PARTIAL | T + R + F + S + P |
| 5 | Sim integration | ~5 | YES | R + F + P |
| 6 | Terminal canvas | 2 | YES | R + S |
| 7 | Misc fixes | ~5 | YES | R |
| 8 | Config/inventory | ~6 | MOSTLY | R + regenerable |

**Total tracked files affected: ~33 unique files**
**Total modifications lost: ~50+ individual changes**
**Recovery confidence: ~85% fully recoverable, ~15% needs re-investigation (auth wiring, package.json)**

---

## Rebuild Queue Plan

8 specs, priority P0.05 to P0.40, dependency-ordered:

| # | Priority | Spec ID | What | Model | Sources to Reference |
|---|----------|---------|------|-------|----------------------|
| 1 | P0.05 | rebuild-route-registration | Re-add all 4 route imports to __init__.py | haiku | TASK-146/157/165/166 responses |
| 2 | P0.10 | rebuild-rag-exports | Re-add all RAG __init__.py imports/exports | haiku | TASK-151/152/153/155/161 responses |
| 3 | P0.15 | rebuild-shell-css | 4 CSS var fixes + menu bar CSS from platform | haiku | TASK-158 response + platform CSS |
| 4 | P0.20 | rebuild-auth-wiring | ra96it OAuth/JWKS + hivenode auth + app registration | sonnet | TASK-136/137/138 responses + platform |
| 5 | P0.25 | rebuild-sim-integration | Sim routes stub→real + schema + app registration | sonnet | TASK-140/141 responses + platform |
| 6 | P0.30 | rebuild-terminal-canvas | Terminal types + useTerminal canvas handler | haiku | TASK-166 response + SPEC-TERMINAL-TO-CANVAS-WIRING |
| 7 | P0.35 | rebuild-misc-fixes | pyproject, main.py, test selectors, mock fixes | haiku | TASK-126A/132/133/139 responses |
| 8 | P0.40 | rebuild-config-inventory | sim.egg.md + inventory export + package.json review | haiku | TASK-140 response + inventory CLI |

---

## Preventive Recommendation

1. Add `git reset`, `git checkout`, `git clean`, `git restore` to command blocklist in bee dispatch
2. Commit more frequently — hours of uncommitted work was the real exposure
3. Consider a pre-dispatch hook that snapshots `git stash` before bee sessions

---

**Q33NR — 2026-03-15**
