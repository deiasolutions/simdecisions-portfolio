# Phase 1 Triage Report — SPEC-BUGFIX-PALOOZA-001

**Date:** 2026-04-10
**Author:** Q33NR (Claude Opus 4.6)
**Target:** simdecisions (canonical, NOT shiftcenter)
**Stash:** `stash@{0}` — "palooza-001: stash escalation cleanup work before diagnostics"
**Spec:** `C:\Users\davee\Downloads\SPEC-BUGFIX-PALOOZA-001.md`

---

## Summary

Phase 1 diagnostic survey complete. Findings materially exceed single-session capacity.
Recommendation: hand off phases 2–4 to Q33N queen with this report as source of truth.

| Area | Status | Scope |
|------|--------|-------|
| Frontend build (`vite build`) | **BLOCKED** | 1 blocking bug — vite config `serve-eggs` plugin |
| Frontend dev server (`vite`) | **WORKS** | Vite ready in ~1s on :5173 (dev is lazy, only `build` triggers eggs dir) |
| Frontend typecheck (`tsc --noEmit`) | **BROKEN** | 2,728 error lines across 241 files |
| Frontend tests (`vitest --run`) | **BROKEN** | 527 failures + V8 OOM crash at end |
| Backend startup (uvicorn) | **BLOCKED** | Editable-install namespace shadow |
| Backend tests (pytest) | **BLOCKED** | Same shadow — `ModuleNotFoundError: hivenode` |

---

## BLOCKING Errors (prevent basic operation)

### B1. Vite config `[serve-eggs]` plugin — wrong path
- **File:** `packages/browser/vite.config.ts`
- **Error:**
  ```
  [serve-eggs] ENOENT: no such file or directory, scandir
    'C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\packages\eggs'
  ```
- **Root cause:** Custom dev plugin hardcoded to read `packages/eggs`. After the simdecisions monorepo cutover, the real eggs dir is at the repo root (`./eggs`, i.e. `../../eggs` from `packages/browser`).
- **Impact:** `npm run build` fails immediately. Dev server survives only because the plugin is invoked lazily on route hit.
- **Fix estimate:** 2 lines. Change the plugin's `scandir` target to `path.resolve(__dirname, '../../eggs')`.

### B2. Editable-install namespace shadow on `simdecisions`
- **File:** `C:\Users\davee\AppData\Roaming\Python\Python312\site-packages\__editable__.simdecisions-0.1.0.pth`
- **Contents:** `C:\Users\davee\OneDrive\Documents\GitHub\platform\src`
- **Effect:** When Python imports `simdecisions`, it resolves to the OLD `platform/src/simdecisions` package, which does NOT contain a `core/` sub-package. Site-packages is ordered before `PYTHONPATH`, so even `PYTHONPATH="packages/core/src"` cannot override it.
- **Proof:**
  ```python
  simdecisions.__path__ → ['C:\\Users\\davee\\...\\platform\\src\\simdecisions']
  ```
- **Error when starting backend:**
  ```
  ModuleNotFoundError: No module named 'hivenode'
  ```
- **Error running pytest:**
  ```
  tests/core/conftest.py:16: ModuleNotFoundError: No module named 'hivenode'
  ```
- **Fix:** `python -m pip uninstall -y simdecisions` then `python -m pip install -e packages/core` from repo root. Verify with `python -c "import hivenode.main; print(hivenode.__path__)"`. Must resolve to `simdecisions/packages/core/src/simdecisions/core`.

---

## NON-BLOCKING but severe (app runs, features broken)

### N1. TypeScript errors — 2,728 lines across 241 files
Top error codes:
```
639  TS2322  Type assignment mismatches
345  TS2304  Cannot find name (missing `global`, `require`, etc.)
273  TS2339  Property does not exist on type
109  TS2345  Argument of type X not assignable
 82  TS2741  Missing property in type (e.g., isActive in AppRendererProps)
 70  TS2353  Unknown object literal property
 48  TS2739  Missing type members
 48  TS2683  'this' implicitly has type 'any'
 32  TS2591  Cannot find name 'require' (test files — missing @types/node)
 29  TS2740  Missing type members
```
Top files by error count:
```
 79  src/shell/__tests__/reducer.layout.test.ts
 48  src/primitives/text-pane/__tests__/SDEditor.test.tsx
 48  src/primitives/conversation-pane/__tests__/ConversationPane.test.tsx
 46  src/primitives/canvas/CanvasApp.tsx             ← NON-TEST FILE
 44  src/shell/__tests__/utils.test.ts
 41  src/primitives/notification-pane/__tests__/NotificationPane.test.tsx
 40  src/primitives/conversation-pane/useLLMRouter.test.ts
 36  src/primitives/code-editor/__tests__/monacoVolumeAdapter.test.ts
 31  src/shell/actions/layout.ts                     ← NON-TEST FILE
 30  src/apps/__tests__/efemera.channels.integration.test.tsx
 29  src/primitives/text-pane/__tests__/SDEditor.openInNewTab.test.tsx
 29  src/primitives/canvas/__tests__/AnnotationNodes.test.tsx
 ...
```
**Pattern observations:**
- Majority are in test files — tests drifted from source types during the shiftcenter→simdecisions cutover.
- `AppRendererProps` changed shape: tests use `_paneId`/`_isActive`/`_config` but current type requires `paneId`/`isActive`/`config`.
- `smoke.test.tsx` uses `mode: "home"` which no longer exists on the mode enum (now `"both" | "home-only" | "cloud-only"`).
- Non-test files with errors: `CanvasApp.tsx` (46), `layout.ts` (31), `MenuBarPrimitive.tsx` (24) — these touch production code and likely block runtime.

### N2. Frontend test failures — 527 failing expectations, V8 crash
Vitest ran to completion logically but crashed the node process at the end:
```
# Fatal JavaScript invalid size error 169220804 (see crbug.com/1201626)
```
Characteristic failure clusters:
- **paletteAdapter** (`Resources` category missing, `draggable` false, `nodeType` undefined)
- **paletteAdapter.canvasInternal** (`canvasInternal` marker undefined)
- **simEgg / simEgg.minimal** (chrome flag, sim app type registration)
- **QuickActions FAB integration** (keyboard flow empty strings, perf threshold 56.94ms > 50ms budget)
- **canvasDragIsolation** (canvas/internal vs hhs/node-id)
- **SDEditor integration** (Mode Switching — mode dropdown null, `'3w'` word count, co-author toggles)
- **ConversationPane e2e** — mostly missing-null text assertions

The V8 OOM crash suggests an unbounded subscription or retained module state. Possibly related to Vitest isolation being off or a leak in the QuickActions animation/perf test.

### N3. Backend tests — collection error (blocked on B2)
Same `ModuleNotFoundError: No module named 'hivenode'`. Once B2 is fixed, re-run `python -m pytest --collect-only` to reveal true state.

---

## Environment notes

- **Monorepo layout (simdecisions):**
  - `packages/browser/` (vite, vitest, playwright, typescript) — has `package.json` with `dev`, `build`, `test`, `typecheck` (NO hyphen).
  - `packages/core/src/simdecisions/core/` — FastAPI backend; entry `hivenode.main:app`.
  - `packages/engine/`, `packages/tools/`, `packages/hodeia-auth/` — uv workspace members.
  - `eggs/` — at repo root (NOT under `packages/`).
  - `ecosystem.config.js` — PM2, backend cmd: `python -m uvicorn hivenode.main:app --host 0.0.0.0 --port 8420`.
- **Node modules:** were absent — `npm install` in `packages/browser` installed 445 pkgs in 24s (10 vulns: 7 moderate, 3 high).
- **Stash state:** `stash@{0}` holds the pre-palooza working tree (escalation cleanup artifacts).

---

## Diagnostic artifacts (absolute paths)

| File | Size | Purpose |
|------|------|---------|
| `/tmp/sd-build.txt` | small | Vite build fail output |
| `/tmp/sd-dev.txt` | small | Vite dev server start (success) |
| `/tmp/sd-npm-install.txt` | medium | npm install output |
| `/tmp/sd-typecheck.txt` | 2728 lines | tsc --noEmit output |
| `/tmp/sd-typecheck-clean.txt` | 2728 lines | Same, ANSI stripped |
| `/tmp/sd-test.txt` | 25068 lines | Vitest output (crashed at end) |
| `/tmp/sd-test-clean.txt` | 25068 lines | Same, ANSI stripped |
| `/tmp/sd-backend.txt` | 0 bytes | Backend startup attempt 1 (silent hang) |
| `/tmp/sd-backend2.txt` | small | Backend startup attempt 2 with PYTHONPATH (still shadowed) |
| `/tmp/sd-pytest.txt` | 48 lines | pytest collect error |

All `/tmp/*` paths are Git Bash / MSYS paths, i.e. real location `C:\Users\davee\AppData\Local\Temp\...` or similar. These files are ephemeral — promote essential excerpts into this report before they vanish.

---

## Recommended Phase 2 ordering (for Q33N)

1. **B2 first** — uninstall the editable `simdecisions` install, `pip install -e packages/core`, verify `python -c "import hivenode.main"`.
2. **Run `pytest --collect-only`** — see real backend state.
3. **B1** — fix `vite.config.ts` `serve-eggs` path to `../../eggs`. Re-run `npm run build`.
4. **Backend smoke** — `python -m uvicorn hivenode.main:app --port 8420`, curl `/health`, record outcome.
5. **Scope-bound TS fix batch** — focus only on non-test production code with errors first: `CanvasApp.tsx`, `layout.ts`, `MenuBarPrimitive.tsx`. Defer the test-file drift (79 files' worth) into a separate follow-up spec.
6. **Commit `fix(palooza): phase 2 complete`** only when build passes and backend starts clean.

Phase 3 and Phase 4 should be attempted ONLY after Phase 2 closes cleanly.

---

## Blocker for Q33N

Do not try to fix all 2728 TS errors in this spec. That is a multi-day project. The palooza spec explicitly says:
> "If a fix would require >20 lines, document it and move on."

Interpret this as: if a file has >20 errors, document the file and defer it unless it's on the runtime path.

---

**End of Phase 1 triage.**
