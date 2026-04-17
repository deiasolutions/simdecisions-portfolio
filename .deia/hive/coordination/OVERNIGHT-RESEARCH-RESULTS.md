# OVERNIGHT RESEARCH RESULTS — 2026-03-23

**Bees dispatched:** 11 (R00-R10)
**Total cost:** ~$27.74
**Total turns:** 363
**Duration:** ~2 hours (parallel dispatch)
**Model:** Sonnet (all bees)

---

## READ FIRST: PORT-CHECKLIST-REFRESH

`.deia/hive/responses/2026-03-23-BEE-R10-RESPONSE-port-checklist-refresh.md`

---

## EXECUTIVE SUMMARY

**Port status: ~48% by line count, ~75% by MVP-critical functionality.**

The gap is intentional: simplified EGG system, dropped efemera features (threading, WebSocket, moderation), future-phase exclusions (optimization, surrogates, production).

### What's Working (12 systems)

| System | Status | Tests |
|--------|--------|-------|
| Shell | Rewritten, SUPERIOR (48 actions vs old 15) | 413 |
| Terminal | 100% ported + 140% enhanced (14 commands, 5 modes) | ~400 |
| PHASE-IR | 76% ported, core working (identical port) | 248 |
| DES Engine | 97% ported (identical port) | ~356 |
| Event Ledger | 100% ported | 39 |
| Governance | 100% ported + enhanced | 153 |
| EGG System | Rewritten in TS, better for MVP | 94 |
| Canvas Animation | 100% direct port (7 files) | 23 |
| FlowDesigner | 7.2x expansion (35K lines, NOT a port) | 400+ |
| Efemera | Simplified MVP (polling > WebSocket) | 78 |
| Queue Runner | Genuinely new | 69 |
| Inventory | Genuinely new | 35 |

**Total tests passing: 9,012+**

### What's Broken (3 items)

1. **171 hardcoded color violations** — 11 in shell, 160 in flow-designer (BOOT.md Rule #3)
2. **3 files exceed 1,000-line limit** — FlowDesigner.tsx (1,123), utils.test.ts (732+), test files
3. **Gemini adapter** — `cannot import name 'genai' from 'google'` (library deprecation)

### What's Missing (4 items)

1. **RAG query engine** — Indexer works, query/embed/search NOT ported (40% complete)
2. **11 canvas node types** — Annotations, sticky notes, parallel split/join, queue
3. **Terminal IR deposit wiring** — Terminal → canvas node creation not connected
4. **E2E drag-drop tests** — Old repo had desktop-drag-in.test.tsx, new doesn't

### Inaccurate Claims Debunked

1. **"121-file, 29,174-line flow designer PORT"** — INACCURATE. Old repo had 0 flow-designer files. New is 133 files, 35,625 lines of GENUINELY NEW code.
2. **"2,669-line properties panel PORT"** — INACCURATE. Old repo has NO PropertyPanel.tsx. New is 336 lines of new code.
3. **BUG-028 (Efemera channels don't work)** — INACCURATE. Bug report was wrong. Channels work correctly.

---

## FINDINGS BY SEVERITY

### CRITICAL (8 findings)

| Bee | Finding |
|-----|---------|
| R00 | Missing Python dependencies: `respx`, `google.generativeai` — 9 pytest errors |
| R00 | npm build fails at copy-eggs step |
| R01 | 11 hardcoded rgba() colors in shell chrome components |
| R02 | 11/17 old node types missing from flow-designer |
| R02 | 160 hardcoded rgba() shadows in 44 flow-designer files |
| R04 | 404.egg.md does not exist |
| R07 | ChromeBtn + SplitDivider have hardcoded colors in every pane |
| R09 | BUG-017 OAuth fix LOST in recovery commit d061af1 (2026-03-19) |

### WARNING (12 findings)

| Bee | Finding |
|-----|---------|
| R00 | vitest 50% failure rate — `document is not defined` in hook tests |
| R01 | 4 files exceed 500-line limit (MenuBar, utils, test files) |
| R01 | E2E drag-drop tests missing |
| R02 | Terminal IR deposit → canvas NOT implemented |
| R03 | useTerminal.ts at 956 lines (500-line limit violation) |
| R04 | hodeia-landing adapter not registered |
| R04 | code.egg.md references 3 unregistered apps |
| R05 | Gemini adapter import error blocks test suite |
| R06 | Channel creation UI commands not wired |
| R07 | 790 lines with hardcoded colors across 55 files |
| R08 | 11 console.log() calls in production code |
| R09 | BUG-049 (turtle pen up) STILL BROKEN |

### NOTE (15 findings)

| Bee | Finding |
|-----|---------|
| R01 | Shell swap/delete/merge all WORKING |
| R01 | Pin/collapse/maximize all WORKING |
| R02 | "flow designer port" claim is INACCURATE — it's new code |
| R03 | Terminal 100% ported + 140% enhanced, zero regressions |
| R04 | Platform scenario system never ported (intentional) |
| R05 | LLM adapters minimal — Anthropic works, Ollama works, rest broken/untested |
| R05 | ~48% backend ported by line count |
| R06 | Old efemera-compose never existed — new design is cleaner |
| R06 | Channel system is simplified MVP, architecture sound |
| R08 | _outbox/ pattern is DEAD — zero instances, full compliance |
| R08 | No circular dependencies detected |
| R09 | 4 P0 bugs verified FIXED (BUG-018, 019, 028, 051) |
| R09 | BUG-023 canvas collapse 95% implemented |
| R09 | 3 P0 backlog items NOT implemented (BL-203, 206, 214) |
| R10 | Port status: 70-80% of MVP-critical features ported or rebuilt better |

---

## BUGS TO CLOSE (verified fixed)

| Bug | Title | Status | Evidence |
|-----|-------|--------|----------|
| BUG-018 | Canvas IR routing | FIXED | R09: canvas IR routing code verified working |
| BUG-019 | Drag isolation | FIXED | R09: drag isolation code verified |
| BUG-028 | Efemera channels | FIXED (bug was inaccurate) | R09: channels work correctly |
| BUG-051 | Channel selection | FIXED (duplicate of BUG-028) | R09: same as BUG-028 |

## BUGS STILL OPEN (verified broken)

| Bug | Title | Status | Fix Location |
|-----|-------|--------|-------------|
| BUG-017 | OAuth redirect | REGRESSED (fix lost in recovery) | Need re-implementation |
| BUG-049 | Turtle pen up | STILL BROKEN | DrawingCanvasApp.tsx:242-253 |
| BUG-058 | Canvas to_ir | WIRED but needs live debug | Needs runtime testing |

## BUGS NEEDING MANUAL TEST (14 items)

BUG-050, 052, 054-057, 059-064, 066-067 — Cannot determine from code inspection alone.

---

## RECOMMENDED BUILD PRIORITIES

### Tier 1: Fix Quality Violations (blocks alpha)

1. Fix 171 hardcoded colors (define --sd-shadow-* vars, replace inline rgba)
2. Modularize FlowDesigner.tsx (1,123 → 4 files, <300 each)
3. Fix Gemini adapter import (google.generativeai → google.genai)
4. Fix vitest DOM environment setup (jsdom config for hook tests)
5. Re-implement BUG-017 OAuth fix (lost in recovery)

### Tier 2: Complete Missing Features (needed for MVP)

6. Complete RAG engine (port embed + query modules)
7. Wire terminal IR deposit → canvas node creation
8. Register hodeia-landing adapter
9. Create 404.egg.md
10. Fix BUG-049 (turtle pen up — add penDown check to circle/rect)

### Tier 3: Modularize + Test Coverage

11. Split useTerminal.ts (956 → 5 modules)
12. Split MenuBar.tsx (602 → sections)
13. Split utils.ts (568 → tree/merge/node utils)
14. Add drag-drop E2E tests
15. Add auth + inventory route tests
16. Remove 11 console.log() calls

### Tier 4: Future Decisions Required

17. Port 11 missing canvas node types (or document removal)
18. Port PHASE-IR CLI (or keep API-only)
19. Add efemera features back (threading, roles, versioning)
20. Consider WebSocket upgrade (if 3s polling becomes bottleneck)

---

## COST BREAKDOWN

| Bee | Domain | Cost | Turns |
|-----|--------|------|-------|
| R00 | Environment Baseline | $0.02 | — |
| R01 | Shell + Layout + DnD | $2.20 | 36 |
| R02 | Canvas + ReactFlow | $3.34 | 60 |
| R03 | Terminal + Commands | $4.36 | 43 |
| R04 | EGG System | $2.76 | 41 |
| R05 | Hivenode Backend | $3.51 | 44 |
| R06 | Channels + Chat | $2.47 | 35 |
| R07 | CSS Audit | $1.96 | 20 |
| R08 | Dead Code | $3.10 | 36 |
| R09 | Bug Triage | $1.93 | 25 |
| R10 | Port Checklist | $2.09 | 23 |
| **Total** | | **$27.74** | **363** |

---

## RESPONSE FILES

All in `.deia/hive/responses/`:

| Bee | Response File |
|-----|--------------|
| R00 | `20260323-TASK-BEE-R00-RESPONSE-environment-baseline.md` |
| R01 | `20260323-BEE-R01-RESPONSE-shell-layout-dnd.md` |
| R02 | `20260323-2056-BEE-SONNET-TASK-BEE-R02-RAW.txt` |
| R03 | `20260323-2056-BEE-SONNET-TASK-BEE-R03-RAW.txt` |
| R04 | `20260323-TASK-BEE-R04-RESPONSE-egg-system.md` |
| R05 | `20260323-2057-BEE-SONNET-TASK-BEE-R05-RAW.txt` |
| R06 | `20260323-2057-BEE-SONNET-TASK-BEE-R06-RAW.txt` |
| R07 | `20260323-2057-BEE-SONNET-TASK-BEE-R07-RAW.txt` |
| R08 | `20260323-TASK-BEE-R08-RESPONSE-code-quality.md` |
| R09 | `20260323-2057-BEE-SONNET-TASK-BEE-R09-RAW.txt` |
| R10 | `2026-03-23-BEE-R10-RESPONSE-port-checklist-refresh.md` |

**Findings log:** `.deia/hive/coordination/2026-03-23-RESEARCH-FINDINGS-LOG.md` (58 entries)

---

END OF OVERNIGHT RESEARCH RESULTS
