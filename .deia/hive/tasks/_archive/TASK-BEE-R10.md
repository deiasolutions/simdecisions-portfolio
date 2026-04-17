# TASK-BEE-R10: Port Checklist Refresh — Master Reconciliation

**Assigned to:** BEE (Sonnet)
**From:** Q33NR
**Date:** 2026-03-23
**Wave:** C (runs AFTER Wave A completes — depends on R01-R06 findings)

---

## Objective

This is the master port reconciliation. The highest-value deliverable of the entire night. Produce a fully refreshed port status by comparing old repos against shiftcenter AS IT EXISTS RIGHT NOW.

## Inputs — Read ALL of These First

1. **Wave A response files** (R01-R06 — these contain domain-by-domain findings):
   - `.deia/hive/responses/2026-03-23-BEE-R01-RESPONSE-shell-layout-dnd.md`
   - `.deia/hive/responses/2026-03-23-BEE-R02-RESPONSE-canvas-reactflow.md`
   - `.deia/hive/responses/2026-03-23-BEE-R03-RESPONSE-terminal-commands.md`
   - `.deia/hive/responses/2026-03-23-BEE-R04-RESPONSE-egg-system.md`
   - `.deia/hive/responses/2026-03-23-BEE-R05-RESPONSE-hivenode-backend.md`
   - `.deia/hive/responses/2026-03-23-BEE-R06-RESPONSE-channels-chat.md`
2. **Reference docs** (search `.deia/` and `docs/` if not found at expected path):
   - PORT-CHECKLIST.md (March 14)
   - 2026-02-22-MASTER-INVENTORY.md (138 features)
   - 2026-03-10-PRODUCT-SESSION-CANONICAL.docx (28 primitives, 16 composites, 23 services)
   - INVESTIGATION-REPO-COMPARISON-REPORT.md
   - UNIFIED-COMPONENT-REGISTRY.md

If a reference doc is missing, note it and proceed. Do NOT let a missing doc block you.

## Old Repos (READ-ONLY comparison source)

All three are subdirectories inside the platform repo:

| Repo | Path | What it had |
|------|------|-------------|
| efemera | `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\` | DES, PHASE-IR, RAG, dialects, surrogates, production, tabletop, optimization, pheromones, scenarios, builds, chat |
| efemera tests | `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\tests\` | Test suite for above |
| simdecisions-2 | `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\` | Canvas (22 node types), properties panel, shell chrome, flow designer, chat |
| simdecisions-2 engine | `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\engine\` | PHASE-IR v2 runtime |
| platform root | `C:\Users\davee\OneDrive\Documents\GitHub\platform\` | Server, store, flights, minder, router, task_files, KB |
| platform canonical | `C:\Users\davee\OneDrive\Documents\GitHub\platform\canonical\docs\` | Task registry, feature audit, bee ledger, readiness scorecard |

## Current Repo (what we're auditing)

| Area | Path |
|------|------|
| Browser frontend | `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\` |
| Hivenode backend | `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\` |
| Engine | `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\` |
| Auth | `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\ra96it\` |
| Eggs | `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\` |

## Output — Five Mandatory Sections

### Section 1: PORTED AND VERIFIED WORKING
For each: component name, old file path(s), new file path(s), line count old vs new, test count, confidence (HIGH/MEDIUM/LOW).

### Section 2: PORTED BUT BROKEN OR REGRESSED
Items ported but now broken. For each: what broke, when it likely broke, symptom, what test was skipped/removed.

Hunt specifically for:
- Tests that were `skip`ped or `xit`/`xdescribe`d after port
- Functions that exist but are empty or return hardcoded values
- Files that import from paths that no longer exist
- Components that render but have no functionality ("coming soon")
- Routes with stub handlers
- Event handlers registered as `() => {}`

### Section 3: NEVER PORTED (still only in old repos)
Items from old repos with no equivalent in shiftcenter. For each: what it did, line count, which old repo, whether still needed.

### Section 4: PARTIALLY PORTED
Code exists but incomplete. For each: what's present, what's missing, percentage estimate.

### Section 5: NEW — Built Fresh (audit for redundant rebuilds)
Items in shiftcenter with no old repo origin. CRITICAL: ~50% of "new" code is estimated to be redundant rebuilds. For each item answer:
1. Does an equivalent exist in old repos? If YES → redundant build.
2. Is the new version BETTER or WORSE? (NEW-BETTER / OLD-BETTER / EQUIVALENT)
3. If no old equivalent, is this genuinely new?

Per-item table:

| Field | Value |
|-------|-------|
| Component | [name] |
| New location | [path] |
| Line count (new) | [n] |
| Old equivalent? | YES / NO |
| Old location | [path if yes] |
| Line count (old) | [n if yes] |
| Test count new vs old | [n vs n] |
| Verdict | GENUINELY NEW / REDUNDANT-NEW-BETTER / REDUNDANT-OLD-BETTER / REDUNDANT-EQUIVALENT |
| Recommendation | KEEP NEW / REPLACE WITH PORT / MERGE BEST OF BOTH |

## Regression Patterns to Hunt

1. **"Summarized instead of ported"** — check process files, spec files, governance files
2. **"Ported then overwritten"** — check git blame for files ported before March 17 but modified after
3. **"Test existed, now doesn't"** — compare test file counts per directory old vs new
4. **"Import path broken by refactor"** — frank→prompt rename, HiveHostShell→HiveHostPanes rename
5. **Flow designer** — BL-129 claimed 29,174 lines / 121 files ported. Verify: do those files exist? Do imports resolve? Do tests pass?
6. **"Rebuilt from scratch instead of ported"** — for EVERY component in Section 5, check old repos

## Output

Write to: `.deia/hive/responses/2026-03-23-BEE-R10-RESPONSE-port-checklist-refresh.md`
Append to shared log: `.deia/hive/coordination/2026-03-23-RESEARCH-FINDINGS-LOG.md`
Format: "### [HH:MM] BEE-R10 | [SEVERITY] | CATEGORY\n\nOne-liner.\n\n---"

## IMPORTANT
- READ-ONLY research. Do NOT modify code. Do NOT commit.
- This bee runs AFTER R01-R06 complete. Their response files are your primary input.
- This is the highest-value deliverable of the entire night. Be thorough.
