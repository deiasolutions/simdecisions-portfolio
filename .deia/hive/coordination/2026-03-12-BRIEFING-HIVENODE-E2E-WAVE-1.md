# BRIEFING: SPEC-HIVENODE-E2E-001 — Wave 1

**From:** Q33NR
**To:** Q33N
**Date:** 2026-03-12
**Spec:** `docs/specs/SPEC-HIVENODE-E2E-001.md`
**Wave:** 1 of 4

---

## Objective

Deliver the foundation layer of SPEC-HIVENODE-E2E-001: the `8os` CLI tool (up/down/status commands only), the E2E route verification test suite for all 16 existing routes, and the new `/shell/exec` route with OS translation. These three are independent enough for parallel bees but must be separate task files.

---

## Wave 1 Scope — Three Task Files

### TASK-026: 8os CLI Tool (up/down/status)

**What:** Create `hivenode/cli.py` with `click` subcommands. Wire into `pyproject.toml` as a `[project.scripts]` entry point (`8os = "hivenode.cli:main"`). Only three commands this wave: `up`, `down`, `status`.

**Key details from spec (Section 2):**
- `8os up` → starts uvicorn on port 8420 as background process. PID stored at `~/.shiftcenter/hivenode.pid`.
- `8os down` → reads PID file, kills process, removes PID file.
- `8os status` → checks if PID is alive, prints running/stopped + port.
- Config location: `~/.shiftcenter/config.yml` — create on first `8os up` if it doesn't exist.
- Config schema defined in spec Section 2.3.
- `click` must be added to `[project.dependencies]` in pyproject.toml.

**Files to read first:**
- `docs/specs/SPEC-HIVENODE-E2E-001.md` (Sections 2.1–2.3)
- `hivenode/config.py` (existing settings — port 8420, modes)
- `hivenode/__main__.py` (existing entry point)
- `pyproject.toml` (existing scripts entry: `hive = "hivenode.__main__:main"`)

**Existing state:** There's already a `hive` script entry in pyproject.toml pointing to `__main__.py`. The new `8os` entry is ADDITIONAL (don't remove `hive`).

**Test requirements:** ~12 tests in `tests/hivenode/test_cli.py`. Test PID file creation/cleanup, config generation, status output. Use `click.testing.CliRunner` for CLI tests. Mock `subprocess.Popen` for uvicorn process management. Test Windows and Unix path handling.

**Model assignment:** Sonnet

---

### TASK-027: E2E Route Verification Test Suite

**What:** Create `tests/hivenode/test_e2e.py` — a test suite that starts a REAL hivenode instance on a random port, makes REAL httpx calls to every existing route, and tears down. This is NOT unit tests with mocks — it's integration tests with real HTTP.

**Key details from spec (Section 3.1):**
- All 16 routes tested (see table in spec Section 3.1)
- Test fixture starts a real hivenode via `uvicorn` on a random available port
- Uses `httpx.AsyncClient` for HTTP calls
- Each test writes real data, reads it back, verifies
- Tests need a temp directory for SQLite DBs and volume storage

**The 16 existing routes to verify:**
1. `GET /health` — 200 + `{"status": "ok"}`
2. `GET /status` — returns node_id, mode, uptime, volumes
3. `POST /auth/verify` — rejects invalid JWT (401), accepts valid/bypasses in local
4. `GET /auth/whoami` — returns user info
5. `GET /ledger/events` — returns list after writing test events
6. `GET /ledger/events/{id}` — returns specific event
7. `POST /ledger/query` — filters by event_type, actor, time range
8. `GET /ledger/cost` — returns cost aggregation
9. `POST /storage/read` — reads a file written to home://
10. `POST /storage/write` — writes file, verifies on disk
11. `POST /storage/list` — lists directory contents
12. `POST /storage/stat` — returns file metadata
13. `POST /storage/delete` — deletes file, verifies gone
14. `POST /node/announce` — registers node, returns ack
15. `GET /node/discover` — returns known nodes
16. `POST /node/heartbeat` — updates last_seen

**Files to read first:**
- `docs/specs/SPEC-HIVENODE-E2E-001.md` (Section 3.1)
- `hivenode/main.py` (app creation, lifespan, route mounting)
- `hivenode/routes/health.py`, `hivenode/routes/auth.py`, `hivenode/routes/ledger_routes.py`, `hivenode/routes/storage_routes.py`, `hivenode/routes/node.py` (all route handlers)
- `hivenode/config.py` (settings, mode, ports)
- `hivenode/dependencies.py` (dependency injection — verify_jwt_or_local)
- `hivenode/schemas.py` (request/response models)
- `tests/hivenode/conftest.py` (existing test fixtures)

**Critical pattern:** The existing tests use `TestClient` with mock transport to avoid SQLite thread issues. The E2E suite is DIFFERENT — it starts a real server process. Use `uvicorn.Config` + `uvicorn.Server` in a background thread, or `subprocess` to launch the server. The test must wait for the server to be ready (poll `/health`).

**Test requirements:** 16+ tests (one per route minimum). All use real HTTP calls.

**Model assignment:** Sonnet

---

### TASK-028: /shell/exec Route + OS Translation

**What:** Create `hivenode/routes/shell.py` with `POST /shell/exec` route. Create `hivenode/shell/executor.py` with the OS translation engine. Create `hivenode/shell/allowlist.py` for command allow/deny list.

**Key details from spec (Sections 3.2.1–3.2.3):**

**Request/Response format:**
```json
// Request
{
  "command": "mkdir",
  "args": ["foo/bar"],
  "working_dir": "home://projects/myapp",
  "os_hint": "auto"
}
// Response
{
  "status": "success",
  "exit_code": 0,
  "stdout": "",
  "stderr": "",
  "os_used": "windows",
  "command_executed": "mkdir foo\\bar",
  "duration_ms": 12
}
```

**OS translation table (spec Section 3.2.1):**
| IR command | Windows | Unix/Mac |
|-----------|---------|----------|
| `mkdir foo/bar` | `mkdir foo\bar` | `mkdir -p foo/bar` |
| `ls -la` | `dir /a` | `ls -la` |
| `cp file1 file2` | `copy file1 file2` | `cp file1 file2` |
| `rm file` | `del file` | `rm file` |
| `cat file` | `type file` | `cat file` |
| `grep pattern file` | `findstr pattern file` | `grep pattern file` |
| `pwd` | `cd` | `pwd` |
| `mv file1 file2` | `move file1 file2` | `mv file1 file2` |
| `touch file` | `type nul > file` | `touch file` |

Path separator normalization: `/` → `\` on Windows, `\` → `/` on Unix.

**Security (spec Section 3.2.3):**
- LOCAL MODE ONLY by default. Cloud hivenode does NOT expose `/shell/exec` unless config allows.
- Default allowlist defined in spec Section 3.2.2 (mkdir, ls, dir, cp, copy, etc.)
- Denylist: `rm -rf /`, `del /s /q C:\`, `format`, `mkfs`, fork bomb
- Commands not in allowlist → reject with error
- Commands matching denylist → reject + log `SHELL_DENIED` to Event Ledger
- Every execution → log `SHELL_EXEC` to Event Ledger
- 30-second timeout default
- Working directory resolved through volume system (`home://projects/myapp` → actual disk path)

**Files to read first:**
- `docs/specs/SPEC-HIVENODE-E2E-001.md` (Sections 3.2.1–3.2.3)
- `hivenode/routes/__init__.py` (how routes are mounted)
- `hivenode/storage/resolver.py` (volume path resolution — `home://` → disk path)
- `hivenode/storage/registry.py` (VolumeRegistry for volume lookups)
- `hivenode/dependencies.py` (dependency injection pattern)
- `hivenode/ledger/writer.py` (how to log events)
- `hivenode/config.py` (settings.mode for local/cloud check)
- `hivenode/schemas.py` (existing Pydantic models — follow same pattern)

**Architecture:**
- `hivenode/shell/__init__.py` — empty
- `hivenode/shell/executor.py` — `ShellExecutor` class: detects OS, translates IR→native, runs subprocess, returns result
- `hivenode/shell/allowlist.py` — default allow/deny lists, validation function
- `hivenode/routes/shell.py` — FastAPI route, depends on executor + allowlist + ledger writer
- Mount the shell router in `hivenode/routes/__init__.py`
- Add `hivenode.shell` to `[tool.setuptools] packages` in pyproject.toml

**Test requirements:** ~15 tests in `tests/hivenode/shell/` (test_executor.py, test_allowlist.py) + route tests in `tests/hivenode/test_shell_routes.py`. Test OS translation for each command pair. Test allowlist/denylist rejection. Test volume path resolution. Test cloud mode rejection. Test timeout. Test Event Ledger logging.

**Model assignment:** Sonnet

---

## Dependencies Between Tasks

- TASK-026 (CLI) and TASK-028 (shell exec) are **independent** — can dispatch in parallel.
- TASK-027 (E2E tests) tests existing routes, so it's also independent. BUT if we want it to also test `/shell/exec`, it should run AFTER TASK-028. **Solution:** dispatch TASK-027 for the 16 existing routes only. A follow-up task in Wave 2 can add shell exec E2E tests.
- All three can dispatch in parallel.

## Constraints

- No file over 500 lines. If `executor.py` is large, split translation table into a separate module.
- TDD — tests first.
- No stubs.
- CSS rule N/A (backend only).
- All paths in task files must be absolute.
- `click` dependency must be added to pyproject.toml.
- `hivenode.shell` package must be added to setuptools packages list.

## Waves 2–4 (Preview — NOT this briefing)

- **Wave 2:** Browser terminal shell parsing + cloud storage adapter
- **Wave 3:** Volume sync engine + chat persistence rewrite
- **Wave 4:** Tree-browser conversation navigator + node announcement

---

**Q33N:** Write three task files for TASK-026, TASK-027, TASK-028. Return them for review before dispatching. Use Sonnet for all three bees.
