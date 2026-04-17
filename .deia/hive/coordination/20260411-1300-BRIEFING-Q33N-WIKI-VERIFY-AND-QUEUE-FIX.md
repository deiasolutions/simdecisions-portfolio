# BRIEFING — Q33N WIKI VERIFY + QUEUE RUNNER FIX

**Date:** 2026-04-11 13:00
**From:** Q33NR (Opus 4.6)
**To:** Q33N (Sonnet 4.5)
**Repo:** `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions` (NOT shiftcenter)
**Task file:** `.deia/hive/tasks/20260411-1300-TASK-Q33N-WIKI-VERIFY-AND-QUEUE-FIX.md`

---

## Context

Q88N asked to "kick off the 5 WIKI-104→109 specs through the scheduler". Q33NR surveyed and discovered:

1. **All 5 wiki specs (104, 105, 106, 107, 109) are ALREADY DONE in code.**
   - `/api/wiki/pages` returns real page data
   - `/api/wiki/pages/{path}/backlinks` returns valid JSON (WIKI-104 done)
   - `packages/browser/src/primitives/wiki/WikiPane.tsx` exists with tests (WIKI-105)
   - `packages/browser/src/primitives/wiki/MarkdownViewer.tsx` exists (WIKI-106)
   - `packages/browser/src/primitives/wiki/BacklinksPanel.tsx` exists (WIKI-107)
   - `packages/browser/src/apps/wikiPaneAdapter.tsx` exists
   - `packages/browser/src/apps/index.ts:80` has `registerApp('wiki', WikiPaneAdapter)`

2. **Queue dir cleanup already done by Q33NR:**
   - Moved `SPEC-WIKI-104-backlinks-query.md` → `_done/`
   - Moved `SPEC-WIKI-105-wikipane-primitive.md` → `_done/`
   - Deleted duplicate zombies: WIKI-106, WIKI-107, WIKI-109 (byte-identical to _done versions)
   - Moved `SPEC-WIKI-103-crud-api-routes.md` from `_escalated/` and `_needs_review/` → `_done/`
   - Deleted `REJ-WIKI-103-crud-api-routes.md` from `_needs_review/`
   - Deleted 55 rejection garbage files from `backlog/`
   - Backlog now: 10 real specs (6 utility + 4 Raiden)

3. **Queue runner is broken — only processing 1 phantom spec:**
   - Log shows `[QUEUE] Watch: processing 1 spec(s)` every 60s
   - Stuck spec: `2026-03-18-SPEC-REQUEUE-TASK228-des-pipeline-runner.md`
   - **This file does NOT exist anywhere in `.deia/hive/queue/`** (find returns empty)
   - Queue runner is scanning phantom state from an earlier run
   - Real 10 specs in `backlog/` are never scanned
   - Must be embedded queue runner inside hivenode backend caching stale state

---

## Mission

Three things, in order:

### Task 1 — Verify wiki UI works end-to-end

1. Frontend dev server is running on `http://[::1]:5173` (IPv6 localhost).
   - Backend on `http://localhost:8420`.
2. Write a Playwright test OR manual curl probes that verify:
   - (a) `/api/wiki/pages` returns the 3 seeded pages (intro, core, advanced)
   - (b) `/api/wiki/pages/intro/backlinks` returns valid shape `{path, backlinks, total}`
   - (c) The wiki app is registered — confirm by reading `packages/browser/src/apps/index.ts` and checking WikiPaneAdapter is imported + `registerApp('wiki', WikiPaneAdapter)` is called
   - (d) Run the existing wiki tests: `cd packages/browser && npx vitest run src/primitives/wiki/` — report pass/fail
3. **Do NOT run `npm run build` or `npm run typecheck`** — they hang on Windows with 2728 TS errors. This is known; do not attempt.

### Task 2 — Mark wiki features in inventory

Use the inventory CLI at `_tools/inventory.py` (likely still at that path — check first, may be under `packages/` in the monorepo).

1. Locate the inventory CLI. Try in this order:
   - `_tools/inventory.py` (legacy location)
   - `packages/core/src/simdecisions/inventory/cli.py`
   - `grep -r "inventory" _tools/` and `find packages -name "inventory*"`
2. Add or update features for: WIKI-103, WIKI-104, WIKI-105, WIKI-106, WIKI-107, WIKI-109
3. Each entry: status=done, owner=bee, stage=complete
4. If inventory CLI is unreachable, write a stub report at `.deia/hive/responses/20260411-WIKI-INVENTORY-STATUS.md` listing what SHOULD be marked and why it couldn't be done

### Task 3 — Diagnose queue runner phantom spec

1. Find the code for the embedded queue runner inside the backend:
   - Search `packages/core/src/simdecisions/` and `packages/browser/` for queue runner code
   - Grep for `"Watch: processing"` and `"REQUEUE-TASK228"` strings to find source
2. Find where the phantom spec list is cached. Candidates:
   - `.deia/hive/queue/monitor-state.json`
   - `.deia/hive/schedule.json`
   - Backend in-memory state (check uvicorn /routes endpoint for any queue endpoints)
   - `.deia/hive/dispatched.jsonl` / `.deia/hive/dispatcher_log.jsonl`
3. Document root cause in response doc. **Do NOT fix yet** — report + recommend.

---

## Hard Rules

1. **Target is simdecisions ONLY.** Do not touch `../shiftcenter/` for any reason.
2. **No new dependencies.** Do not `pip install` or `npm install` anything.
3. **No refactors.** Read-only investigation + inventory marking + possibly small fix scripts.
4. **Do not stop the queue runner.** Do not kill the backend. Q88N prohibited this.
5. **Use dispatch.py only** — you don't dispatch anyone, you are the top of this chain.
6. **Commit discipline:**
   - Task 1 findings: no commit (just response doc)
   - Task 2 inventory changes: commit `chore(wiki): mark WIKI-103..109 as done in inventory`
   - Task 3 diagnosis: no commit (just response doc)
7. **No >20 line code changes.** This is verify + mark + diagnose, not rebuild.
8. **Response doc at:** `.deia/hive/responses/20260411-RESPONSE-WIKI-VERIFY-AND-QUEUE-FIX.md`

---

## Acceptance Criteria

- [ ] Wiki API endpoints verified (curl evidence in response doc)
- [ ] Wiki vitest results reported (pass/fail per test file)
- [ ] WiKi registration verified in apps/index.ts
- [ ] Inventory marking done (or documented if unreachable)
- [ ] Queue runner phantom spec root cause documented
- [ ] Response doc complete with clock/cost/commit SHAs

---

## Notes

- Wiki seed data: 3 pages (intro, core, advanced) with `[[core]]` wikilink from intro/advanced
- Expected backlinks for "core": `[intro, advanced]` (2 backlinks)
- If WIKI-104 is truly done, `GET /api/wiki/pages/core/backlinks` should return `{"path":"core","backlinks":[{path:"intro",...},{path:"advanced",...}],"total":2}`
- The wiki work was done in a previous session — commit history should show it

Good hunting.
