# TASK — Q33N CLEANUP LIFESPAN DEBUG CODE

**ID:** 20260411-1700-TASK-Q33N-CLEANUP-LIFESPAN-DEBUG
**Assignee:** Q33N (Sonnet 4.5, role=queen)
**Repo:** `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions`
**Briefing:** `.deia/hive/coordination/20260411-1700-BRIEFING-Q33N-CLEANUP-LIFESPAN-DEBUG.md`
**Response target:** `.deia/hive/responses/20260411-RESPONSE-CLEANUP-LIFESPAN-DEBUG.md`

---

## Read First

1. `.deia/BOOT.md` — hard rules + response template
2. `.deia/HIVE.md` — your chain of command
3. `.deia/hive/coordination/20260411-1700-BRIEFING-Q33N-CLEANUP-LIFESPAN-DEBUG.md` — full context

---

## What to Do

### Step 1 — Read current state

```bash
cd /c/Users/davee/OneDrive/Documents/GitHub/simdecisions
git log --oneline -10
# See the lifespan() function
grep -n "lifespan\|DEBUG\|import sys" packages/core/src/simdecisions/core/main.py
```

### Step 2 — Edit main.py

Open `packages/core/src/simdecisions/core/main.py`, locate `async def lifespan(app: FastAPI):`, and remove exactly these six lines:

1. `import sys` (inside the function)
2. `print(f"[DEBUG] lifespan entered mode={settings.mode}", file=sys.stderr, flush=True)`
3. `logger.info(f"[lifespan] starting (mode={settings.mode}, ledger={settings.ledger_db_path})")`
4. `logger.info("[lifespan] startup complete, yielding to app")`
5. `print("[DEBUG] lifespan yielding NOW", file=sys.stderr, flush=True)`
6. `print("[DEBUG] lifespan resumed after yield (shutdown)", file=sys.stderr, flush=True)`

Keep everything else in the function: MCP start block, temp cleanup task, sync worker, etc.

### Step 3 — Tighten MCP comment

Find the comment above the `if settings.mode != "cloud":` MCP block. Replace the debugging-era rationale with the correct architectural rationale:

```python
# Start MCP server on port 8421 (background task).
# MCP is a local developer tool: it exposes the factory loop so local bees
# can drive the hivenode via MCP protocol. Railway runs in cloud mode
# serving end-user API traffic — no bees, no factory loop — so MCP is not
# started there.
```

### Step 4 — Commit

```bash
git add packages/core/src/simdecisions/core/main.py
git commit -m "chore: remove lifespan debug prints after Railway cutover"
```

One commit. Focused.

### Step 5 — Deploy to Railway hivenode

```bash
cd /c/Users/davee/OneDrive/Documents/GitHub/simdecisions
MSYS_NO_PATHCONV=1 railway link -s hivenode -p peaceful-integrity -e production
MSYS_NO_PATHCONV=1 railway up --detach
# Note build URL + deploy ID
```

### Step 6 — Verify

Wait ~90s, then:

```bash
MSYS_NO_PATHCONV=1 railway deployment list 2>&1 | head -5
curl -s -o /dev/null -w "health: %{http_code}\n" https://hivenode-production.up.railway.app/health
curl -s https://hivenode-production.up.railway.app/health
MSYS_NO_PATHCONV=1 railway logs --deployment <new-deploy-id> 2>&1 > /tmp/clean-deploy.log
grep -c DEBUG /tmp/clean-deploy.log   # Must be 0
grep -c '\[lifespan\]' /tmp/clean-deploy.log   # Must be 0
grep 'Application startup complete' /tmp/clean-deploy.log   # Must still be present
```

Success: deploy SUCCESS, /health 200, 0 hits on `DEBUG` and `[lifespan]`, `Application startup complete.` still appears.

## Done Criteria

- [ ] Six debug lines removed from `main.py` `lifespan()`
- [ ] `import sys` inside the function removed
- [ ] MCP comment tightened to reflect architectural intent (not debug rationale)
- [ ] One commit on `main`
- [ ] Railway `hivenode` deployment SUCCESS
- [ ] `/health` still returns 200
- [ ] Runtime logs are clean (no `DEBUG`, no `[lifespan]`, still has `Application startup complete.`)
- [ ] Response file written with commit hash + deploy ID + log grep results

## Out of Scope

- Do NOT touch hodeia-auth. Another Q33N is on that.
- Do NOT revert the MCP cloud gate. It's correct.
- Do NOT remove `PYTHONUNBUFFERED=1` or `--log-level info` from Dockerfile.
- Do NOT rewrite history or squash.
