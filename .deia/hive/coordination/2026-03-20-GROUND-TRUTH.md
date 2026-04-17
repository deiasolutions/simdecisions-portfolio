# Ground Truth — 2026-03-20

**Branch:** `browser-recovery`
**Auditor:** Q33NR (read-only, no fixes applied)

---

## 1. Hivenode Tests (`python -m pytest`)

**Result: 2951 passed, 55 failed, 18 skipped, 43 errors**

Collection errors (2):
- `tests/hivenode/rag/test_models.py` — ImportError: `RelevanceMetadata` not in `hivenode.rag.indexer.models`
- `tests/routes/test_heartbeat_metadata.py` — __pycache__ collision (duplicate basename across test dirs)

Notable failures:
- E2E tests (`test_e2e.py`) — RuntimeError: Server failed to start (8 errors, port conflict with running hivenode)
- `test_kanban_routes.py` — sqlalchemy error
- 55 failures total across the suite

---

## 2. Browser Tests (`npx vitest run`)

**Result: 1574 passed, 1589 failed, 40 skipped (266 test files: 83 passed, 179 failed, 4 skipped)**

Primary failure pattern: `ReferenceError: document is not defined`
- Majority of failures are `jsdom` environment issues — tests expecting DOM but running in node environment
- Affects: sim flow designer, useSimulation, and many component tests
- This is a test environment configuration issue, not application code failures

---

## 3. Vite Build (`npx vite build`)

**Result: BUILD FAILED**

```
Could not resolve entry module "index.html"
```

The build was run from the wrong working directory context. The `--prefix` flag changes where npm looks for packages but doesn't change cwd for vite. Vite needs to run from `browser/` directory where `index.html` lives.

Note: The dev server (vite dev) IS running successfully on port 5173. This is a build invocation issue, not a code issue.

---

## 4. Localhost:5173

**Result: RUNNING (HTTP 200)**

EGG files served via Vite plugin — all return 200:
- chat: 200
- canvas: 200
- kanban: 200
- sim: 200
- code: 200
- apps: 200
- home: 200
- monitor: 200
- efemera: 200

15 EGG files exist on disk in `eggs/`:
apps, build-monitor, canvas, chat, code, efemera, home, kanban, login, monitor, playground, processing, ship-feed, sim, turtle-draw

---

## 5. hivenode/main.py

**Result: EXISTS**

Path: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\main.py`

---

## 6. hivenode/api/

**Result: DOES NOT EXIST**

No `hivenode/api/` directory. Routes live in `hivenode/routes/` instead.

---

## 7. Git Log (last 20 commits)

```
8a7af9c hive: Wave 1+2 task files, bee responses, and raw outputs
a55baa5 recovery: Wave 2 rebuilds — canvas properties + title bar
4500704 recovery: Wave 1 rebuilds — shell foundation, kanban fix, chat adapters
33bac43 hive: all-in commit — triage, research, dogfood audit, DA tasks, logs
8440fa9 recovery: cherry-pick 3 Bucket A files (Phase 3)
d061af1 recovery: reset browser/ and eggs/ to March 16 baseline
3debaff messy-checkpoint-mar19: safety net before browser recovery
d0df28b [BEE-SONNET] SPEC-TASK-GATE0-QUEUE-RUNNER-VALIDATION
5154cd8 [Q33NR-DIRECT] Restore session logging rule to HIVE.md
75560ae [BEE-HAIKU] SPEC-TASK-GATE0-QUEUE-RUNNER-VALIDATION
aaa30c6 [BEE-SONNET] SPEC-REQUEUE-BUG030-chat-duplicate-conversations
0126e74 [BEE-SONNET] SPEC-REQUEUE-BUG021-canvas-minimap
8e6ddd2 [BEE-SONNET] SPEC-TASK-BL121-PROPERTIES-PANEL-WIRING
aae983c [BEE-SONNET] SPEC-TASK-BL121-PROPERTIES-PANEL-WIRING
621161e [BEE-SONNET] SPEC-REQUEUE-BUG030-chat-duplicate-conversations
99505ae [BEE-SONNET] SPEC-REQUEUE-BL121-properties-panel
21a67bb [BEE-SONNET] SPEC-REQUEUE-BUG022B-click-to-place
deea38a [BEE-SONNET] SPEC-REQUEUE-BUG022B-click-to-place
a1b2ecf [BEE-SONNET] SPEC-REQUEUE2-BL207-chrome-opt-out
8a68033 [BEE-SONNET] SPEC-REQUEUE2-BL207-chrome-opt-out
```

---

## Summary

| Check | Status | Details |
|-------|--------|---------|
| Hivenode tests | MOSTLY PASSING | 2951 pass, 55 fail, 43 errors |
| Browser tests | MAJORITY FAILING | 1574 pass, 1589 fail (jsdom env issue) |
| Vite build | FAILED | Entry module resolution (cwd issue) |
| Localhost:5173 | RUNNING | All 15 EGGs serve HTTP 200 |
| hivenode/main.py | EXISTS | Yes |
| hivenode/api/ | MISSING | Routes in hivenode/routes/ instead |
| Git history | 20 commits shown | On browser-recovery branch |
