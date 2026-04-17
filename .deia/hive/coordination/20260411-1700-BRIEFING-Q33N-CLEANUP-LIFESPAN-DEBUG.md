# BRIEFING — Q33N CLEANUP LIFESPAN DEBUG CODE

**Date:** 2026-04-11 17:00
**From:** Q33NR (Opus 4.6)
**To:** Q33N (Sonnet 4.5)
**Repo:** `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions` (canonical)
**Task file:** `.deia/hive/tasks/20260411-1700-TASK-Q33N-CLEANUP-LIFESPAN-DEBUG.md`
**Response target:** `.deia/hive/responses/20260411-RESPONSE-CLEANUP-LIFESPAN-DEBUG.md`

---

## Context

During today's Railway cutover debugging, I added several diagnostic prints and log lines to `packages/core/src/simdecisions/core/main.py` to figure out why the app wasn't completing the ASGI startup handshake. The real root cause turned out to be a Dockerfile CMD form issue (exec-form not substituting `$PORT`), which was fixed in commit `5140475`.

The debug code is no longer needed. It's producing noise in Railway logs (the `[DEBUG] lifespan...` prints and the `[lifespan] starting/startup complete` INFO logs). Time to clean it up.

## What Got Added (and needs to come out)

Four commits added noise; one commit has the real fix that stays:

| Commit | Kept or removed |
|---|---|
| `4616061 fix(ledger): run migration before creating event_hash index` | **KEEP** — real bug fix |
| `ce2d639 fix(docker): install workspace members via --all-packages` | **KEEP** — real bug fix |
| `c44803f debug: add lifespan start/yield log lines` | **REVERT content** (the log lines) |
| `46fd3d4 debug: add PYTHONUNBUFFERED and explicit log-level` | **PARTIAL** — keep `PYTHONUNBUFFERED=1` (useful in prod), keep explicit `--log-level info` |
| `db415b0 debug: add unbuffered stderr prints around yield` | **REVERT content** (the `print()` + `import sys`) |
| `014583a fix(cloud): skip nested MCP uvicorn in cloud mode` | **KEEP** — this is the CORRECT design (MCP is local/remote only, not cloud). Not a precaution; the original unconditional MCP start was an oversight. |
| `5140475 fix(docker): use shell-form CMD so Railway PORT env var is honored` | **KEEP** — the fix that actually worked |

## Specific Code to Remove

In `packages/core/src/simdecisions/core/main.py`, the `lifespan()` context manager currently has:

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan - initialize services on startup."""
    import sys                                                                              # REMOVE
    print(f"[DEBUG] lifespan entered mode={settings.mode}", file=sys.stderr, flush=True)    # REMOVE
    logger.info(f"[lifespan] starting (mode={settings.mode}, ledger={settings.ledger_db_path})")  # REMOVE
    ...
    logger.info("[lifespan] startup complete, yielding to app")                             # REMOVE
    print("[DEBUG] lifespan yielding NOW", file=sys.stderr, flush=True)                     # REMOVE
    yield
    print("[DEBUG] lifespan resumed after yield (shutdown)", file=sys.stderr, flush=True)   # REMOVE
```

All six of those lines are debug noise. Remove them. The surrounding production logging (`MCP server started on http://...`, `Temp file cleanup task started`, etc.) stays as-is.

## MCP Cloud Gate — DO NOT REVERT

The `if settings.mode != "cloud":` check around MCP server startup (commit `014583a`) is **correct behavior**, not a debug artifact. MCP is a local dev tool for bees to talk to the factory loop via MCP protocol. Railway runs in cloud mode serving end-user API traffic; there are no bees and no factory loop on Railway, so MCP has no purpose there.

The comment in the code already explains this:

```python
# Start MCP server on port 8421 (background task) — local/remote only.
# On Railway (cloud mode), nested uvicorn prevents the outer server from
# completing its ASGI startup handshake, which leaves /health unreachable.
```

You MAY update that second sentence of the comment to be more accurate (it was written during debugging when we weren't sure why). The correct rationale is simpler: **MCP is a local dev tool; Railway serves production API traffic and has no need for it.** Rewrite the comment to reflect that.

## Success Criteria

1. Six debug lines removed from `main.py` `lifespan()`.
2. `import sys` removed (it's only there for the print calls).
3. MCP cloud gate kept, comment tightened.
4. Commit with clean message (no "fix the fix" chain).
5. Deploy to Railway hivenode — `MSYS_NO_PATHCONV=1 railway up --detach`.
6. Verify `/health` still returns 200 and runtime logs are clean (no `[DEBUG]` lines, no `[lifespan] ...` lines).

## Out of Scope

- Do NOT touch hodeia-auth (another Q33N is handling that).
- Do NOT squash/rewrite the earlier debug commits; they're already in `main` history and that's fine.
- Do NOT remove `PYTHONUNBUFFERED=1` from Dockerfile — it's useful in prod.
- Do NOT remove `--log-level info` from Dockerfile CMD — it's useful in prod.

## Constraints

- One commit. Focused.
- Test locally if you can (`python -c "import packages.core.src.hivenode.main"` or similar import-level check) before deploying.
- After deploy, pull runtime logs via `railway logs --deployment <ID>` and verify none of the debug lines appear.
