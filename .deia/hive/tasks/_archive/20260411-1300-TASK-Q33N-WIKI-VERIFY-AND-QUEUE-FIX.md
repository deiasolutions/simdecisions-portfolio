# TASK — Q33N WIKI VERIFY + QUEUE RUNNER DIAGNOSIS

**ID:** 20260411-1300-TASK-Q33N-WIKI-VERIFY-AND-QUEUE-FIX
**Assignee:** Q33N (Sonnet 4.5, role=queen)
**Repo:** `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions`
**Briefing:** `.deia/hive/coordination/20260411-1300-BRIEFING-Q33N-WIKI-VERIFY-AND-QUEUE-FIX.md`
**Response target:** `.deia/hive/responses/20260411-RESPONSE-WIKI-VERIFY-AND-QUEUE-FIX.md`

---

## Read First

1. `.deia/BOOT.md` — hard rules + response template
2. `.deia/HIVE.md` — your chain of command
3. `.deia/hive/coordination/20260411-1300-BRIEFING-Q33N-WIKI-VERIFY-AND-QUEUE-FIX.md` — full context

---

## What to Do

### Task 1 — Verify wiki works end-to-end (READ ONLY)

```bash
# Backend probes
curl -s http://localhost:8420/api/wiki/pages
curl -s http://localhost:8420/api/wiki/pages/core/backlinks
curl -s http://localhost:8420/api/wiki/pages/intro/backlinks

# Frontend verification
grep -n "wiki" packages/browser/src/apps/index.ts
ls packages/browser/src/primitives/wiki/

# Run wiki tests only
cd packages/browser
npx vitest run src/primitives/wiki/ --reporter=verbose
cd ../..
```

**Do NOT run:** `npm run build`, `npm run typecheck`, full vitest (all hang or OOM).

### Task 2 — Inventory marking

Try in order:
1. `python _tools/inventory.py feature list | grep -i wiki`
2. `find . -name "inventory*" -path "*simdecisions*"`
3. `grep -rn "inv_features" packages/core/src/`

If CLI works: add/update features WIKI-103, 104, 105, 106, 107, 109 with status=done.
If CLI unreachable: write stub report listing what should be marked.

Commit: `chore(wiki): mark WIKI-103..109 as done in inventory` (only if actual DB changes made)

### Task 3 — Queue runner phantom diagnosis

The queue runner logs show it processes 1 phantom spec (`2026-03-18-SPEC-REQUEUE-TASK228-des-pipeline-runner.md`) that doesn't exist on disk anywhere in `.deia/hive/queue/`.

Find the source:
```bash
# Find queue runner code
grep -rn "Watch: processing" packages/
grep -rn "REQUEUE-TASK228" packages/
grep -rn "TASK-226" packages/

# Find state cache
cat .deia/hive/queue/monitor-state.json 2>/dev/null | head -20
cat .deia/hive/schedule.json 2>/dev/null | head -20
ls .deia/hive/dispatched.jsonl .deia/hive/dispatcher_log.jsonl 2>/dev/null
```

**Root cause hypothesis to verify:** The queue runner loaded this spec on backend startup and cached its presence in memory. When the spec was moved/deleted, the in-memory list wasn't refreshed because the dep check never resolves so it never completes and never re-scans. (This would be a real bug — report it, don't fix it.)

---

## Hard Rules

1. simdecisions ONLY — do not touch shiftcenter
2. No dependency installs
3. No refactors
4. Do NOT stop the queue runner or backend
5. Response doc at `.deia/hive/responses/20260411-RESPONSE-WIKI-VERIFY-AND-QUEUE-FIX.md`
6. Follow the BOOT.md response template exactly

## Acceptance Criteria

- [ ] Wiki API 3 endpoints probed (show curl output)
- [ ] Wiki vitest run and pass/fail reported
- [ ] Wiki app registration confirmed in apps/index.ts
- [ ] Inventory marking attempted + result documented
- [ ] Queue runner phantom root cause identified in response doc
- [ ] Response doc follows BOOT.md template
- [ ] Clock / cost / carbon reported at bottom
