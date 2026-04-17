# Refactor Layout Plan — shiftcenter → simdecisions

**Doc ID:** 20260411-REFACTOR-LAYOUT-PLAN
**Author:** Q33NR (Claude, acting under Q88N)
**Status:** DRAFT — authoritative target for code_move pass
**Parent:** SPEC-FACTORY-SELF-REFACTOR-001 (superseded by the framing below)

---

## Framing (Corrected)

This is a **full repo refactor**, not a per-item IRE cherry-pick.

- **All code** in shiftcenter gets refactored into a new monorepo layout
- **All non-code** conveys unchanged (docs, eggs, .deia, configs, secrets, logs, state)
- Target layout: **packages monorepo** under `simdecisions/packages/`
- Python namespace: **`simdecisions.*`** (brand-scoped, PEP 420 implicit namespace packages)
- `hodeia-auth` remains a **peer package** (own pyproject, own Railway service, own package name — NOT under `simdecisions.*`)
- `browser` is a TS/React package at `packages/browser/`, own Vite root
- Tests live at **root `tests/`**, mirror `packages/` structure

---

## Target Directory Structure

```
simdecisions/
├── packages/
│   ├── browser/                    (was shiftcenter/browser/)
│   │   ├── package.json
│   │   ├── vite.config.ts
│   │   ├── tsconfig.json
│   │   ├── app.html
│   │   ├── public/
│   │   ├── src/
│   │   │   ├── primitives/
│   │   │   ├── shell/
│   │   │   ├── apps/
│   │   │   ├── infrastructure/
│   │   │   ├── services/
│   │   │   ├── hooks/
│   │   │   └── pages/
│   │   └── e2e/
│   │
│   ├── engine/                     (was shiftcenter/engine/)
│   │   ├── pyproject.toml          → name = "simdecisions-engine"
│   │   └── src/
│   │       └── simdecisions/       (namespace package, NO __init__.py)
│   │           └── engine/
│   │               ├── __init__.py
│   │               ├── des/
│   │               └── phase_ir/
│   │
│   ├── core/                       (was shiftcenter/hivenode/)
│   │   ├── pyproject.toml          → name = "hivenode"
│   │   └── src/
│   │       └── simdecisions/       (namespace package, NO __init__.py)
│   │           └── core/
│   │               ├── __init__.py
│   │               ├── main.py     (was hivenode/main.py)
│   │               ├── routes/
│   │               ├── efemera/
│   │               ├── analytics/
│   │               ├── ledger/
│   │               ├── inventory/
│   │               ├── rag/
│   │               ├── shell/
│   │               ├── storage/
│   │               ├── governance/
│   │               ├── canvas/
│   │               ├── workspace/
│   │               ├── terminal/
│   │               ├── llm/
│   │               ├── hive_mcp/
│   │               └── factory/    (NEW — consolidated scheduler framework)
│   │                   ├── __init__.py
│   │                   ├── main.py         (single entrypoint)
│   │                   ├── queue.py        (was scheduler_daemon + run_queue --watch)
│   │                   ├── dispatcher.py   (was dispatcher_daemon)
│   │                   ├── triage.py       (was triage_daemon, now callback)
│   │                   ├── watchdog.py     (was _tools/watchdog.*)
│   │                   ├── state.py        (single state module)
│   │                   └── adapters/
│   │                       └── cli/
│   │                           ├── __init__.py
│   │                           ├── dispatch.py
│   │                           ├── run_queue.py
│   │                           ├── claude_cli_subprocess.py
│   │                           └── claude_code_cli_adapter.py
│   │
│   ├── hodeia-auth/                (was shiftcenter/hodeia_auth/)
│   │   ├── pyproject.toml          → name = "hodeia-auth" (NOT under simdecisions)
│   │   ├── Dockerfile              (moved from repo root)
│   │   └── src/
│   │       └── hodeia_auth/
│   │           ├── __init__.py
│   │           ├── main.py
│   │           ├── routes.py
│   │           ├── db.py
│   │           └── ...
│   │
│   └── tools/                      (was shiftcenter/_tools/)
│       ├── pyproject.toml          → name = "simdecisions-tools"
│       └── src/
│           └── simdecisions/       (namespace package, NO __init__.py)
│               └── tools/
│                   ├── __init__.py
│                   ├── inventory.py
│                   └── ... (plus any retained tool scripts)
│
├── docs/                           (conveyed unchanged)
├── eggs/                           (conveyed unchanged)
├── .deia/                          (conveyed unchanged)
├── .wiki/                          (conveyed unchanged)
├── .data/                          (conveyed unchanged)
├── .env                            (conveyed unchanged)
├── .gitignore                      (conveyed unchanged)
│
├── tests/                          (root — mirrors packages/)
│   ├── core/
│   ├── engine/
│   ├── tools/
│   ├── hodeia_auth/
│   ├── browser/                    (vitest/playwright — optional, or keep in packages/browser/)
│   └── integration/                (cross-package)
│
├── pyproject.toml                  (workspace root — uv workspace)
├── package.json                    (optional npm workspace root)
├── README.md
├── CLAUDE.md
├── Dockerfile                      (main app — runs hivenode.main)
├── railway.toml
├── vercel.json
├── nixpacks.toml
└── ecosystem.config.js
```

---

## Python Packaging Strategy

### PEP 420 Implicit Namespace Packages

The `simdecisions` top-level is an **implicit namespace package** across three wheels: `hivenode`, `simdecisions-engine`, `simdecisions-tools`. They all contribute submodules to the `simdecisions` namespace without ever having an `__init__.py` at the namespace root.

**Rule:** `packages/{core,engine,tools}/src/simdecisions/` has NO `__init__.py`. Only the next level down (`simdecisions/core/__init__.py`, etc.) gets an init file.

### Workspace Root (`pyproject.toml`)

Uses uv workspace:

```toml
[project]
name = "simdecisions-workspace"
version = "0.1.0"
requires-python = ">=3.13"

[tool.uv.workspace]
members = [
    "packages/core",
    "packages/engine",
    "packages/tools",
    "packages/hodeia-auth",
]

[tool.uv.sources]
hivenode = { workspace = true }
simdecisions-engine = { workspace = true }
simdecisions-tools = { workspace = true }
hodeia-auth = { workspace = true }
```

### Per-Package `pyproject.toml` Template

`packages/core/pyproject.toml`:
```toml
[project]
name = "hivenode"
version = "0.1.0"
requires-python = ">=3.13"
dependencies = [
    "fastapi>=0.109",
    "sqlalchemy>=2.0",
    "uvicorn",
    "simdecisions-engine",   # workspace dep
    # ... (copy from existing hivenode requirements)
]

[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[tool.setuptools.packages.find]
where = ["src"]
namespaces = true
```

Engine and tools use the same template pattern with their own names and dep lists.

`packages/hodeia-auth/pyproject.toml`:
```toml
[project]
name = "hodeia-auth"    # NOT namespaced under simdecisions
version = "0.1.0"
# ... (copy from existing hodeia_auth requirements)

[tool.setuptools.packages.find]
where = ["src"]
```

---

## Import Rewrite Rules

Apply these substitutions across all Python source and test files during the code_move pass:

| Old import | New import |
|-----------|-----------|
| `from hivenode.` | `from hivenode.` |
| `import hivenode.` | `import hivenode.` |
| `import hivenode` (bare) | `import hivenode as hivenode` (or refactor caller) |
| `from engine.` | `from simdecisions.` |
| `import engine.` | `import simdecisions.` |
| `from _tools.` | `from simdecisions.tools.` |
| `from hodeia_auth.` | `from hodeia_auth.` (unchanged) |

**Rewrite script:** `packages/tools/src/simdecisions/tools/rewrite_imports.py` — regex-based multi-file substitution with a dry-run mode. Applied to `packages/core/src/`, `packages/engine/src/`, `packages/tools/src/`, and `tests/`.

**Edge cases to watch:**
- String literals containing module paths (e.g., dynamic imports via `importlib`): grep for `"hivenode`, `'hivenode`, `"engine.`
- Mock patches: `@patch("hivenode.routes.x")` → `@patch("hivenode.routes.x")`
- Test fixtures referencing module paths
- Entrypoint strings in `pyproject.toml` `[project.scripts]` and Dockerfile `CMD`

---

## Scheduler Rationalization (factory/ package)

Current sprawl across shiftcenter:
- `hivenode/scheduler/scheduler_daemon.py` (33 KB, process)
- `hivenode/scheduler/dispatcher_daemon.py` (process)
- `.deia/hive/scripts/queue/run_queue.py --watch` (37 KB, process)
- `hivenode/triage_daemon.py` or similar (process)
- `_tools/watchdog.py` (process)

**Target:** `hivenode.factory` — one package, one entrypoint, four coroutines:

```
hivenode.factory
├── main.py          — argparse + asyncio.run(run_all())
├── state.py         — QueueState, SlotPool, BeeRegistry (dataclasses + sqlite)
├── queue.py         — async def queue_watcher(state): scan backlog, enqueue
├── dispatcher.py    — async def dispatcher(state): pop work, launch bees
├── triage.py        — async def triage(state): react to response files
├── watchdog.py      — async def watchdog(state): kill stale bees
└── adapters/cli/    — unchanged wrappers around claude subprocess
```

`main.py`:
```python
async def run_all():
    state = State.load()
    await asyncio.gather(
        queue_watcher(state),
        dispatcher(state),
        triage(state),
        watchdog(state),
    )
```

Deployment: one systemd unit / one Railway worker, not four.

---

## Browser Package

`packages/browser/` — internal structure stays the same. Vite root is `packages/browser/`. Build outputs go to `packages/browser/dist/`.

**Vercel config update:** `vercel.json` (at repo root) must point `buildCommand` at `cd packages/browser && npm run build` and `outputDirectory` at `packages/browser/dist`.

**Deployment flag:** `packages/browser/` is published to Vercel as the shiftcenter project successor. No browser code moves into `simdecisions.*` — it's a peer TS package alongside the Python packages.

---

## Deployment Artifacts

### `Dockerfile` (root — main app)

Currently runs `hivenode.main:app`. After refactor:

```dockerfile
# Build stage
FROM python:3.13-slim AS base
WORKDIR /app
COPY pyproject.toml .
COPY packages/ packages/
RUN pip install uv && uv sync --frozen

# Runtime
CMD ["uvicorn", "hivenode.main:app", "--host", "0.0.0.0", "--port", "8420"]
```

### `Dockerfile.hivenode` (rename)

Rename to `packages/core/Dockerfile` and update CMD path. Keep the rename obvious in the commit so Railway config can be updated.

### `packages/hodeia-auth/Dockerfile`

Moved from repo root (was `Dockerfile.hodeia` or embedded in hodeia_auth/). CMD unchanged: `hodeia_auth.main:app`.

### `railway.toml`

Update service build contexts:
- `hivenode` service → builds `packages/core/Dockerfile`
- `beneficial-cooperation` (hodeia-auth) service → builds `packages/hodeia-auth/Dockerfile`

### `ecosystem.config.js` (PM2)

Update script paths:
- `hivenode/main.py` → `packages/core/src/simdecisions/core/main.py`
- `.deia/hive/scripts/queue/run_queue.py` → replaced by `python -m hivenode.factory.main`

---

## Tests Layout

Root `tests/` mirrors `packages/`:

```
tests/
├── core/           (was shiftcenter/tests/hivenode/)
├── engine/         (was shiftcenter/tests/engine/)
├── tools/          (was shiftcenter/tests/_tools/)
├── hodeia_auth/    (was shiftcenter/hodeia_auth/tests/)
└── integration/    (new — cross-package tests)
```

**pytest configuration** (root `pyproject.toml`):
```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = [
    "packages/core/src",
    "packages/engine/src",
    "packages/tools/src",
    "packages/hodeia-auth/src",
]
```

Inline tests co-located with source (e.g., `packages/core/src/simdecisions/core/inventory/tests/`) are still discoverable via standard pytest collection.

**Browser tests:** vitest stays in `packages/browser/`, playwright e2e stays in `packages/browser/e2e/`.

---

## Order of Operations for Code Move (#7)

1. **Create empty src-layout skeletons** in each `packages/*/src/simdecisions/*/`
2. **Copy hivenode → core:** `shiftcenter/hivenode/**` → `simdecisions/packages/core/src/simdecisions/core/**`
3. **Copy engine → engine:** `shiftcenter/engine/**` → `simdecisions/packages/engine/src/simdecisions/engine/**`
4. **Copy _tools → tools:** `shiftcenter/_tools/**` → `simdecisions/packages/tools/src/simdecisions/tools/**`
5. **Copy hodeia_auth:** `shiftcenter/hodeia_auth/**` → `simdecisions/packages/hodeia-auth/src/hodeia_auth/**`
6. **Copy browser:** `shiftcenter/browser/**` → `simdecisions/packages/browser/**`
7. **Copy tests with rename:** `shiftcenter/tests/hivenode/` → `simdecisions/tests/core/`, etc.
8. **Apply import rewrites** across all `.py` files in `packages/core/`, `packages/engine/`, `packages/tools/`, `tests/`
9. **Write per-package pyproject.toml** files
10. **Write workspace root pyproject.toml**
11. **Update Dockerfile, railway.toml, ecosystem.config.js** with new paths and module names
12. **Update vercel.json** browser build paths
13. **Create factory/ package stub** under `packages/core/src/simdecisions/core/factory/` (full consolidation happens in a follow-up task, not this refactor)
14. **Run `uv sync`** at root — must succeed
15. **Run `pytest tests/ --collect-only`** — must collect without errors

---

## Deferred to Follow-Up (Not Part of Initial Refactor)

1. **Full scheduler consolidation** — factory/ package gets stubs now; the actual merging of 4 daemons into 1 process with 4 coroutines is a separate task after the refactor lands green
2. **Test failure triage** — any shiftcenter test currently failing stays failing; not this refactor's job to fix
3. **Feature inventory migration** — `_tools/inventory.py` still points at Railway PG; no schema changes
4. **Namespace collapse** — if we later decide `hivenode.*` is too long, we can rename to just `simdecisions.*` (dropping the `core`). Defer that call.
5. **Hodeia-auth folding** — if at some point we decide to fold hodeia-auth under `simdecisions.auth`, it's a one-file move. Not now.

---

## Rollback Plan

`simdecisions/` is a fresh directory at peer level. Shiftcenter is untouched. If the refactor fails:

1. `rm -rf simdecisions/`
2. shiftcenter is unchanged, still deploys from Railway, still builds on Vercel
3. No data loss, no downtime

Rollback cost: zero. This is a forward experiment, not a destructive migration.

---

## Smoke Tests After Code Move

Run in order. Halt on first failure:

```bash
cd simdecisions/

# 1. Workspace resolution
uv sync

# 2. Python import collection
python -c "import hivenode.main"
python -c "import simdecisions.des"
python -c "import hodeia_auth.main"

# 3. Test collection
pytest tests/ --collect-only -q

# 4. Fast unit subset
pytest tests/core/inventory/ -q
pytest tests/engine/phase_ir/ -q

# 5. Browser build
cd packages/browser && npm install && npm run build
```

All five must pass before cutover declared.

---

## Files to Create During #7

| Path | Purpose |
|------|---------|
| `simdecisions/pyproject.toml` | Workspace root |
| `simdecisions/packages/core/pyproject.toml` | Core package |
| `simdecisions/packages/engine/pyproject.toml` | Engine package |
| `simdecisions/packages/tools/pyproject.toml` | Tools package |
| `simdecisions/packages/hodeia-auth/pyproject.toml` | Hodeia-auth package |
| `simdecisions/Dockerfile` | Main app (runs `hivenode.main:app`) |
| `simdecisions/packages/core/Dockerfile` | Core-only dockerfile |
| `simdecisions/packages/hodeia-auth/Dockerfile` | Hodeia-auth dockerfile |

---

## Open Calls Made (No Q88N Override Pending)

| Decision | Call |
|----------|------|
| Python import namespace | `hivenode.*`, `simdecisions.*`, `simdecisions.tools.*` |
| Tests location | Root `tests/` mirrors `packages/` |
| Hodeia-auth namespace | Own `hodeia_auth.*` (NOT under `simdecisions.*`) |
| Browser location | Peer `packages/browser/` with own Vite root |
| Monorepo layout | `packages/` with uv workspace |
| Scheduler consolidation | Stub in #7, full merge in follow-up |

---

*20260411-REFACTOR-LAYOUT-PLAN — Q33NR — 2026-04-11*
