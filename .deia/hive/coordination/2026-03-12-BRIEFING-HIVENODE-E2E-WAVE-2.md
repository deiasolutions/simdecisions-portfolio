# BRIEFING: SPEC-HIVENODE-E2E-001 — Wave 2

**From:** Q33NR
**To:** Q33N
**Date:** 2026-03-12
**Spec:** `docs/specs/SPEC-HIVENODE-E2E-001.md`
**Wave:** 2 of 4

---

## Objective

Deliver Wave 2 of SPEC-HIVENODE-E2E-001: browser terminal shell parsing (smart input detection, mode switching, shell command routing to `/shell/exec`), the cloud storage adapter (wiring `cloud://` to call a remote hivenode over HTTPS), and the token tracking schema migration (tokens up/down as first-class ledger columns).

---

## Wave 2 Scope — Three Task Files

### TASK-029: Browser Terminal Shell Parsing

**What:** Add smart input parsing to the browser terminal so it can detect shell commands vs natural language, route shell commands to the hivenode `/shell/exec` endpoint, and support mode switching.

**Key details from spec (Section 4):**

**Smart parsing rules (Section 4.1) — NO LLM needed:**
1. Starts with `!` → force shell. Strip `!`, parse as shell command, send IR to `/shell/exec`.
2. Starts with `/` → slash command (already implemented in `terminalCommands.ts`).
3. Starts with `//` → IPC (existing behavior).
4. Starts with `>` → command palette mode.
5. First token matches known shell command → shell. Parse as IR, send to `/shell/exec`.
6. Natural language → route to LLM (existing behavior).
7. Ambiguous → route to LLM (default safe path).

**Known shell command detection (Section 4.2):**
```typescript
const SHELL_COMMANDS = new Set([
  // Unix
  'ls', 'cd', 'pwd', 'mkdir', 'rmdir', 'cp', 'mv', 'rm', 'cat',
  'grep', 'find', 'chmod', 'chown', 'touch', 'head', 'tail', 'wc',
  'sort', 'uniq', 'tar', 'curl', 'wget',
  // DOS
  'dir', 'copy', 'move', 'del', 'ren', 'type', 'findstr', 'cls',
  // Cross-platform tools
  'git', 'npm', 'npx', 'node', 'python', 'pip', 'pytest', 'docker',
  'ssh', 'scp',
]);
```

**Mode override (Section 4.3):**
| Command | Effect |
|---------|--------|
| `/mode shell` | Everything treated as shell. `!` prefix added automatically. No LLM calls. |
| `/mode chat` | Everything treated as natural language. Shell commands sent to LLM. |
| `/mode hybrid` | Default. Smart parsing decides. |

Mode persists for the session. Resets on page reload or EGG switch.

**Shell command execution flow:**
1. Parse input → detect shell command
2. Split into command + args (first token = command, rest = args)
3. POST to hivenode `/shell/exec` with `{ command, args, working_dir: "home://", os_hint: "auto" }`
4. Display result in terminal (stdout/stderr/exit_code)
5. If denied, show denial reason

**Efemera shell toggle (Section 4.5):**
In Efemera (headless chat EGG), shell is hidden by default. EGG config controls:
```yaml
terminal:
  allow_shell: false    # Efemera default
```
When disabled, `!` prefix and `/mode shell` are not available.

**Files to read first:**
- `docs/specs/SPEC-HIVENODE-E2E-001.md` (Section 4)
- `browser/src/primitives/terminal/useTerminal.ts` (main input handler — handleSubmit)
- `browser/src/primitives/terminal/TerminalPrompt.tsx` (input component)
- `browser/src/services/terminal/terminalCommands.ts` (existing slash commands)
- `browser/src/services/terminal/terminalService.ts` (sendMessage flow)
- `browser/src/services/terminal/index.ts` (exports)
- `eggs/*.egg.md` (check EGG config format for terminal.allow_shell)

**Architecture — new files:**
- `browser/src/services/terminal/shellParser.ts` — `parseInput()` function: classifies input as shell/slash/ipc/palette/chat. Returns `{ type: 'shell'|'slash'|'ipc'|'palette'|'chat', command?, args? }`
- `browser/src/services/terminal/shellCommands.ts` — `SHELL_COMMANDS` set + `isShellCommand(token)` function
- `browser/src/services/terminal/shellExecutor.ts` — `executeShellCommand(command, args, nodeUrl)` function: calls `/shell/exec`, returns formatted result

**Modify:**
- `browser/src/primitives/terminal/useTerminal.ts` — integrate shellParser into handleSubmit
- `browser/src/services/terminal/terminalCommands.ts` — add `/mode` command
- `browser/src/services/terminal/index.ts` — export new modules

**Test requirements:** ~18 tests in `browser/src/services/terminal/__tests__/shellParser.test.ts` and `shellExecutor.test.ts`. Test each parsing rule, mode switching, EGG config check, `/shell/exec` HTTP call.

**Model assignment:** Sonnet

---

### TASK-030: Cloud Storage Adapter

**What:** Wire the `cloud://` volume adapter to call a remote hivenode's `/storage/*` routes over HTTPS. Currently all 8 methods in `hivenode/storage/adapters/cloud.py` raise `NotImplementedError`. Replace them with real HTTPS calls using `httpx`.

**Key details from spec (Section 5):**

**Architecture (Section 5.1):**
```
Browser → local hivenode (home://) → writes to local disk
Browser → cloud hivenode (cloud://) → writes to Railway volume
Local hivenode → cloud hivenode → sync (Wave 3)
```

The cloud adapter on the LOCAL hivenode is an HTTP client that calls the CLOUD hivenode's `/storage/*` routes. It is NOT direct S3/volume access.

**Cloud adapter interface (Section 5.2):**
```python
class CloudStorageAdapter(BaseVolumeAdapter):
    def __init__(self, cloud_url: str, auth_token: str):
        self.cloud_url = cloud_url    # https://api.shiftcenter.com
        self.auth_token = auth_token  # ra96it JWT

    def read(self, path: str) -> bytes:
        # POST cloud_url/storage/read with path + JWT
    def write(self, path: str, content: bytes, actor: str, intent: str) -> dict:
        # POST cloud_url/storage/write with path, content, provenance + JWT
    def list(self, path: str) -> list:
        # POST cloud_url/storage/list + JWT
    def stat(self, path: str) -> dict:
        # POST cloud_url/storage/stat + JWT
    def delete(self, path: str) -> dict:
        # POST cloud_url/storage/delete + JWT
    def exists(self, path: str) -> bool:
        # stat() and check for 404
    def move(self, src: str, dest: str) -> dict:
        # read + write + delete (no native move over HTTP)
```

Every operation includes the ra96it JWT in the `Authorization: Bearer <token>` header.

**Offline behavior (Section 5.3):**
- If cloud:// is unreachable (network down, timeout, connection refused):
  - Reads → return `VOLUME_OFFLINE` error
  - Writes → queue in `~/.shiftcenter/sync_queue/` (one file per queued write, JSON format with path + content_base64 + metadata)
  - Queue flushes when cloud:// comes back online (checked on next operation or periodic sync)

**Files to read first:**
- `docs/specs/SPEC-HIVENODE-E2E-001.md` (Section 5)
- `hivenode/storage/adapters/base.py` (BaseVolumeAdapter abstract interface — 8 methods)
- `hivenode/storage/adapters/cloud.py` (current stub — all NotImplementedError)
- `hivenode/storage/adapters/local.py` (reference implementation — LocalFilesystemAdapter)
- `hivenode/storage/registry.py` (VolumeRegistry — how adapters are registered)
- `hivenode/storage/transport.py` (FileTransport — how storage routes use adapters)
- `hivenode/routes/storage_routes.py` (storage route handlers — request/response format)
- `hivenode/config.py` (settings — cloud_url, mode)
- `hivenode/dependencies.py` (how to get auth token)

**Architecture — modify:**
- `hivenode/storage/adapters/cloud.py` — replace NotImplementedError with real httpx calls

**Architecture — new files:**
- `hivenode/storage/adapters/sync_queue.py` — offline write queue: `SyncQueue` class with `enqueue(path, content, metadata)` and `flush(cloud_adapter)` methods. Stores queued writes as JSON files in `~/.shiftcenter/sync_queue/`.

**Test requirements:** ~15 tests. Mock httpx responses for all 8 adapter methods. Test offline behavior (connection refused → queue). Test JWT header inclusion. Test sync queue flush. Tests go in `tests/hivenode/storage/test_cloud_adapter.py` (already exists, update with real tests).

**Model assignment:** Sonnet

---

### TASK-031: Token Tracking Schema Migration (tokens up/down)

**What:** Add `cost_tokens_up` and `cost_tokens_down` columns to the Event Ledger schema. Update LLM_CALL event emission to populate them. Update cost aggregation to report directional costs.

**Key details from spec (Section 10.1 — new amendment):**

**Schema migration:**
```sql
ALTER TABLE events ADD COLUMN cost_tokens_up INTEGER;    -- input/prompt tokens
ALTER TABLE events ADD COLUMN cost_tokens_down INTEGER;  -- output/completion tokens
```

The existing `cost_tokens` column remains as total (up + down) for backward compatibility.

**What to change:**

1. **`hivenode/ledger/schema.py`** — Add the two new columns to `CREATE TABLE IF NOT EXISTS events`. Also add a migration function that ALTERs existing DBs.

2. **`hivenode/llm/cost.py`** — Update `emit_llm_event()` to pass `cost_tokens_up=input_tokens` and `cost_tokens_down=output_tokens` to `ledger_writer.write_event()`.

3. **`hivenode/ledger/writer.py`** — Update `write_event()` to accept and store `cost_tokens_up` and `cost_tokens_down` parameters.

4. **`hivenode/ledger/aggregation.py`** — Update `get_total_cost()` and all `aggregate_cost_by_*` functions to return directional token counts:
   ```python
   {
     "tokens": total,
     "tokens_up": total_up,
     "tokens_down": total_down,
     "usd": total_usd,
     "carbon": total_carbon,
   }
   ```

5. **`hivenode/ledger/reader.py`** — Ensure event read-back includes the new columns.

6. **`hivenode/routes/ledger_routes.py`** — Update the `/ledger/cost` response model to include `tokens_up`, `tokens_down`, `cost_up_usd`, `cost_down_usd`.

**Files to read first:**
- `docs/specs/SPEC-HIVENODE-E2E-001.md` (Section 10.1)
- `hivenode/ledger/schema.py` (current schema — 14 columns, needs 2 more)
- `hivenode/ledger/writer.py` (write_event function signature)
- `hivenode/ledger/reader.py` (event read-back)
- `hivenode/ledger/aggregation.py` (cost aggregation — get_total_cost, aggregate_cost_by_*)
- `hivenode/llm/cost.py` (emit_llm_event — already has input_tokens/output_tokens)
- `hivenode/routes/ledger_routes.py` (/ledger/cost endpoint)
- `hivenode/schemas.py` (response models)
- `tests/hivenode/ledger/test_schema.py` (existing schema tests)
- `tests/hivenode/ledger/test_writer.py` (existing writer tests)
- `tests/hivenode/ledger/test_aggregation.py` (existing aggregation tests)
- `tests/hivenode/llm/test_cost.py` (existing cost tests)

**Test requirements:** ~12 tests. Test schema has new columns. Test writer stores them. Test aggregation returns directional data. Test emit_llm_event populates them. Test backward compatibility (old events with NULL tokens_up/down). Update existing tests that check column counts.

**Model assignment:** Sonnet

---

## Dependencies Between Tasks

- **TASK-029 (shell parsing)** depends on Wave 1's `/shell/exec` route being deployed (it is — committed and pushed). Independent of TASK-030 and TASK-031.
- **TASK-030 (cloud adapter)** is independent. No dependency on shell parsing or token tracking.
- **TASK-031 (token tracking)** is independent. Touches ledger schema only, no dependency on shell or cloud.
- **All three can dispatch in parallel.**

## Constraints

- No file over 500 lines.
- TDD — tests first.
- No stubs.
- Browser tests use vitest (`npx vitest run`).
- Hivenode tests use pytest (`python -m pytest tests/hivenode/ -v`).
- CSS: `var(--sd-*)` only (relevant for TASK-029 if any visual changes).
- TASK-031 must not break existing ledger tests — backward compatibility required.

---

**Q33N:** Write three task files for TASK-029, TASK-030, TASK-031. Return them for review before dispatching. Use Sonnet for all three bees.
