# Q33N Briefing — Finish SPEC-BUGFIX-PALOOZA-001 (Phases 2–4)

**Date:** 2026-04-10
**From:** Q33NR (Claude Opus 4.6)
**To:** Q33N (you, Claude Sonnet 4.5)
**Target repo:** `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions` (canonical)
**NOT the target:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter` (frozen-legacy)

---

## Context (read in order)

1. **Source spec:** `C:\Users\davee\Downloads\SPEC-BUGFIX-PALOOZA-001.md`
   - Spec's header says "shiftcenter (frozen main branch)". **IGNORE THAT.** Q88N (Dave) explicitly re-targeted the spec at simdecisions because shiftcenter is frozen-legacy. Execute against simdecisions only.
2. **Phase 1 triage report:** `.deia/hive/coordination/2026-04-10-PHASE1-TRIAGE-BUGFIX-PALOOZA.md`
   - Contains every diagnostic finding Q33NR captured. Treat it as the source of truth. Do NOT re-run all of Phase 1 — just verify state, then proceed to Phase 2.

## State handed off

- Phase 0 complete: simdecisions monorepo layout understood, shell commands mapped, pre-palooza working tree stashed.
  - **Stash:** `stash@{0}` — "palooza-001: stash escalation cleanup work before diagnostics"
  - Do NOT `git stash pop` this until all four phases are complete. After Phase 4, pop it and see if anything still needs attention.
- Phase 1 complete: diagnostics gathered and triaged.
- Phase 2: **not started** — your job.
- Phase 3: not started — your job.
- Phase 4: not started — your job.

## Monorepo shell command crib sheet

```bash
# Frontend (from repo root)
cd packages/browser && npm run build       # ← currently failing on B1
cd packages/browser && npm run dev          # ← works, only blocked by timeout
cd packages/browser && npm run typecheck    # NO hyphen
cd packages/browser && npm test -- --run

# Backend (from repo root)
python -m uvicorn hivenode.main:app --port 8420   # ← currently failing on B2
python -m pytest                                            # ← currently failing on B2
```

---

## Your mission

Finish phases 2, 3, and 4 of SPEC-BUGFIX-PALOOZA-001. Commit after each phase with message exactly `fix(palooza): phase N complete`. Stay in simdecisions, not shiftcenter.

Do **not** pop the stash. Do **not** reset anything. Do **not** delete files you don't understand.

## Phase 2 — fix blocking errors (in this strict order)

### Step 1 — Resolve editable-install shadow (B2)

```bash
# From any cwd
python -m pip uninstall -y simdecisions

# Then from repo root of simdecisions
cd C:/Users/davee/OneDrive/Documents/GitHub/simdecisions
python -m pip install -e packages/core
python -c "import hivenode.main as m; print('OK:', m.__file__)"
```
Expected: import succeeds and path contains `simdecisions\packages\core\src\simdecisions\core\main.py`.

If the path is still `platform\src\simdecisions`, look for another `.pth` file in `C:\Users\davee\AppData\Roaming\Python\Python312\site-packages\*.pth`. The offending file is `__editable__.simdecisions-0.1.0.pth` pointing at `platform/src`. Remove it and reinstall.

Also ensure the install targets the right interpreter — `python -m site` should show `AppData\Roaming\Python\Python312\site-packages`.

### Step 2 — Fix Vite `[serve-eggs]` plugin (B1)

Edit `packages/browser/vite.config.ts`. Find the `serve-eggs` plugin (search for `serve-eggs` or `scandir`). It hardcodes a path that resolves to `packages/eggs`. Change it so it resolves to the repo-root `eggs/` directory:

```ts
// before (approx)
const eggsDir = path.resolve(__dirname, '../eggs');   // or similar wrong path

// after
const eggsDir = path.resolve(__dirname, '../../eggs');
```

Re-run `cd packages/browser && npm run build`. If it now fails on a DIFFERENT error, that's progress — fix only blocking errors, document non-blocking, move on.

**Hard rule:** If a fix would require >20 lines, DOCUMENT in your response and MOVE ON. Don't try to drain all 2728 TS errors in Phase 2.

### Step 3 — Backend smoke

```bash
python -m uvicorn hivenode.main:app --port 8420 &
sleep 5
curl -s http://localhost:8420/health
```
Record the outcome (success / error). If the backend fails, fix the one specific import error it reports, then retry. Do not hand-fix every Python error — only the ones on the startup path.

### Step 4 — Commit

```bash
git add -A
git commit -m "fix(palooza): phase 2 complete"
```

Only commit if at minimum:
- `npm run build` succeeds OR you've documented the next remaining blocker
- Backend imports (`python -c "import hivenode.main"`) succeed

If neither can pass, STOP and report. Do not force through.

## Phase 3 — validate startup

```bash
cd packages/browser && npm run dev &
sleep 10
curl -s http://localhost:5173 | head -20

# Backend (separate shell, from repo root)
python -m uvicorn hivenode.main:app --port 8420 &
sleep 5
curl -s http://localhost:8420/health
```

Success criteria (per spec):
- [ ] `npm run dev` starts without crash
- [ ] Browser shows SOMETHING (even broken UI)
- [ ] Backend `/health` returns 200

Commit: `git commit -m "fix(palooza): phase 3 complete"` — only if above criteria pass.

## Phase 4 — fix visible runtime breaks

With both services running, check for:
1. Console errors on initial page load
2. Error boundaries
3. Failed API calls (network tab 4xx/5xx)

Fix only these, and only if each fix is <20 lines. Do NOT:
- Fix styling
- Add missing features
- Refactor code you don't need to touch

Commit: `git commit -m "fix(palooza): phase 4 complete"`.

## Exit criteria (reminder from spec)

Task is COMPLETE when:
1. `npm run dev` starts without crash
2. Browser renders HiveHostPanes (even empty)
3. Backend health check passes
4. Zero console errors on initial load

If blocked, STOP and write a response doc naming the blocker. Do NOT invent solutions.

---

## Deliverable (your response doc)

Write to `.deia/hive/responses/2026-04-10-RESPONSE-PALOOZA-PHASES-2-4.md` with sections:

```
## Phase 2 fixes applied
| File | Lines changed | What | Result |

## Phase 2 deferrals (>20 lines or out of scope)
- File path — reason — follow-up spec id

## Phase 3 startup state
- Frontend: PASS/FAIL + evidence
- Backend: PASS/FAIL + evidence

## Phase 4 runtime fixes
| Component | Error | Fix |

## Commits
- sha: fix(palooza): phase 2 complete — N files
- sha: fix(palooza): phase 3 complete — N files
- sha: fix(palooza): phase 4 complete — N files

## Final state
- App running? YES/NO/PARTIAL
- Console errors? N
- Remaining blockers?

## Next steps
1. ...
```

---

## Constraints (lifted from spec)

- CSS: `var(--sd-*)` only — no hex, rgb, or named colors
- No file over 500 lines (split first if a fix would push past)
- No stubs
- No algorithm changes — fix wiring, not logic
- Absolute paths in all reports
- Minimal changes only

---

## Hard boundaries

1. **Do not commit anything to shiftcenter.** You are in simdecisions.
2. **Do not pop stash@{0}.** Q33NR will pop it after you finish.
3. **Do not exceed 20-line fixes** without documenting and deferring.
4. **Do not drain all TS errors** — that's a multi-day project outside this spec.
5. **Do not create a Phase 5.** If stuck after Phase 4, write the blocker and stop.
6. **Commit exactly** `fix(palooza): phase N complete` — no variations, no extra text.

---

**End of briefing. Execute autonomously. Respond when done.**
