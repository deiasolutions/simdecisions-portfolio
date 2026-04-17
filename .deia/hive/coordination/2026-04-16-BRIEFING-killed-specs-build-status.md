# BRIEFING: Audit Build Status of Killed-Spec Intentions

**From:** Q33NR
**Date:** 2026-04-16
**Model:** Sonnet
**Role:** Queen
**Mode:** INVESTIGATE + REPORT ONLY — NO CODE, NO ACTION

---

## Objective

On 2026-04-10, 7 spec families were killed as structurally unrecoverable.
The intent of each was preserved in
`docs/killed-specs-2026-04-10-intent.md` so the underlying ideas would
not be lost.

Six days have passed since then. Some of that work may have been built
under different spec IDs, may have been partially built, or may still
be entirely missing. This investigation answers: **for each killed
intent, what has actually been built in the current repo, and what is
still missing?**

Do NOT act. Do not write code, move files, dispatch bees, or run long
test suites. Produce a single report.

---

## Specs Under Review

Per `docs/killed-specs-2026-04-10-intent.md`:

1. **SPEC-BL-146** — Bot tokens + bot settings UI
   (backend: `hivenode/efemera/bot_store.py`, `bot_routes.py`,
   `keeper.py`; DB tables `sd_bot_tokens`, `sd_bot_mutations`;
   SHA-256 token hashing, 60/hr rate limit, one active bot per user)

2. **SPEC-FLAPPY-100** — Self-learning Flappy Bird NEAT v2
   (target file: `browser/public/games/flappy-bird-ai-v2-20260407.html`,
   50+ birds per generation, live neural net viz, single HTML file,
   Canvas API, vanilla JS)

3. **SPEC-MW-VERIFY-001** — Mobile Workdesk audit of 66 SPEC-MW-* specs
   (8 new primitives to verify: command-interpreter, voice-input,
   quick-actions, conversation-pane, mobile-nav, notification-pane,
   queue-pane, diff-viewer; plus 11 existing primitives for mobile CSS)

4. **SPEC-TRIAGE-ESCALATED-001** — Superseded by ESC-001/ESC-002.
   Skip this one — intent doc explicitly says "do not rewrite."

5. **SPEC-WIKI-V1.1** — LLM Wiki pattern (3-layer: `raw/`, `wiki/`,
   `SCHEMA.md`; Ingest/Query/Lint operations; `log.md` audit log;
   AI Solutions tool taxonomy with ~28 categories; ONET integration
   tables `onet_occupations`, `onet_skills`, `onet_occupation_skills`,
   `bls_wages`, `ai_exposure`)

6. **SPEC-GITHUB-005** — Federalist Papers reference corpus
   (Gutenberg IDs 1404, 18; individual papers, not a monolithic
   `complete-collection.md`)

7. **SPEC-WIKI-SURVEY-000** — Pure phantom, no content ever written.
   Skip this one — intent doc says no rewrite.

Focus on #1, #2, #3, #5, #6. Skip #4 and #7.

---

## Context

- Killed-spec intent doc is the source of truth:
  `docs/killed-specs-2026-04-10-intent.md`
- Commit b22995c7 landed DES-CURRENCY-001 (cost computation)
- Commit 00de470b landed DES-CURRENCY-002 (cost aggregation)
- Commit 9a51bcad landed MW-VERIFY-001-full-audit (possibly covers #3?)
- Commit 5bd55c83 landed WIKI-110-status-survey (possibly covers #7?
  But #7 is a skip anyway)
- Various WIKI-* commits landed (75bd945c WIKI-V1, de237b2d WIKI-SYSTEM)
- Backlog has SPEC-WIKI-ONET-READVIEW-001 (blocked on
  OPERATOR-PROFILE-SEED-001) — partial overlap with WIKI-V1.1 ONET work
- Responses dir contains ONET-INGEST-001, AI-EXPOSURE-SCORES-001,
  BLS-WAGE-INGEST-001 response files — check if those covered parts of
  WIKI-V1.1 intent

---

## Files To Read First

- `docs/killed-specs-2026-04-10-intent.md` (the source of truth)
- `hivenode/` directory — check for `efemera/`, bot-related files
- `browser/public/games/` — check for flappy-bird-ai-v2 HTML
- `browser/src/primitives/` — check for the 8 new MW primitives
- `hivenode/wiki/` — check for wiki backend
- `hivenode/inventory/` — check for ONET / BLS tables
- Git log (search: efemera, bot, flappy, NEAT, wiki, onet, bls,
  federalist, ingest, query, lint, mobile-workdesk, mw-verify)

---

## Deliverable

Single report file at:
`.deia/hive/responses/2026-04-16-Q33N-KILLED-SPECS-BUILD-STATUS.md`

For each of the 5 in-scope killed specs, answer:

### Per-spec template

```markdown
### N. SPEC-XXXXX-NNN — <title>

**Intent summary (one sentence):**

**Build status:** BUILT | PARTIAL | NOT BUILT | OBSOLETE
**Confidence:** low | medium | high

**Evidence:**
- <file/commit/route/test that exists and covers intent>
- <what is missing>

**Gaps (if PARTIAL or NOT BUILT):**
- <concrete missing pieces>

**Recommended next step:**
- <write fresh spec with scope X / mark as intentionally abandoned /
  deprioritize because superseded by Y / etc.>
```

### Overall section

- **Coverage matrix** — table: Spec | % built | % missing
- **Newly-built overlapping work** — what got built under different spec
  IDs that satisfies some of the killed intent (e.g., did
  ONET-INGEST-001 land the ONET tables from WIKI-V1.1?)
- **True gaps** — things in killed-specs-intent that no current spec
  or commit addresses
- **Recommendations** — for Q88N: which gaps are worth filling with
  a new spec, and which should be explicitly dropped

---

## Constraints

- NO code changes.
- NO file moves.
- NO queue state changes.
- NO dispatching bees.
- NO git writes.
- Do not run long tests. A `pytest --co` collection-only check is
  acceptable to verify tests exist, but do not run the suite.
- Report file is the only deliverable.

---

## Response Requirements

Standard 8-section response format per BOOT.md, written to
`.deia/hive/responses/2026-04-16-Q33N-KILLED-SPECS-BUILD-STATUS-RESPONSE.md`
IN ADDITION to the main report file.
