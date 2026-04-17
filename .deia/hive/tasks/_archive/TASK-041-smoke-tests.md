# TASK-041: Smoke Tests — Backend Integration + Browser Integration

**Assigned to:** BEE-SONNET
**Model:** Sonnet
**Date:** 2026-03-13
**Parent:** SPEC-HIVENODE-E2E-001 (all waves)

---

## Objective

Write smoke tests that verify the major integrated flows across all 4 waves of SPEC-HIVENODE-E2E-001. These tests exercise real code paths (not mocks) to catch integration bugs that unit tests miss.

Two test suites:
1. **Backend smoke tests** — FastAPI TestClient against the real app with temp storage
2. **Browser smoke tests** — Component integration tests that mock the hivenode API but test real component wiring

---

## What Already Exists

**Backend test infrastructure:**
- `tests/hivenode/conftest.py` — shared fixtures: `mock_settings`, `mock_verify_jwt_fixture`, `mock_ledger_reader`, `mock_volume_registry`, `mock_file_transport`, `mock_node_store`
- `tests/hivenode/test_e2e.py` — real subprocess E2E tests (need running hivenode, not for CI)
- TestClient pattern: `TestClient(app)` with dependency overrides
- `hivenode/main.py` — singleton app with lifespan context manager

**Browser test infrastructure:**
- Vitest with jsdom environment
- `@testing-library/react` for component testing
- `vi.mock()` for API mocking
- Relay bus available for integration testing

---

## Backend Smoke Tests

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_smoke.py`

Use `TestClient(app)` with patched settings pointing to temp directories. These run without a subprocess server — TestClient handles the ASGI lifecycle in-process.

### Test Setup

```python
import pytest
from fastapi.testclient import TestClient
from hivenode.main import app
from hivenode.config import HivenodeConfig
from hivenode import dependencies

@pytest.fixture
def smoke_client(tmp_path, monkeypatch):
    """TestClient with real services pointing to temp storage."""
    storage_root = tmp_path / "storage"
    storage_root.mkdir()
    (storage_root / "home").mkdir()

    config = HivenodeConfig(
        mode="local",
        storage_root=str(storage_root),
        ledger_db_path=str(tmp_path / "ledger.db"),
        node_db_path=str(tmp_path / "nodes.db"),
    )
    monkeypatch.setattr("hivenode.config.settings", config)
    monkeypatch.setattr("hivenode.dependencies.settings", config)

    # Let TestClient trigger the lifespan with temp config
    with TestClient(app) as client:
        yield client
```

### Tests (~15)

**Health + Status (2 tests):**
1. `test_smoke_health()` — GET /health returns 200
2. `test_smoke_status()` — GET /status returns node_id, mode, uptime

**Storage round-trip (3 tests):**
3. `test_smoke_storage_write_read()` — POST /storage/write → POST /storage/read → content matches
4. `test_smoke_storage_list_after_write()` — Write file → POST /storage/list → file in listing
5. `test_smoke_storage_stat_after_write()` — Write file → POST /storage/stat → size, hash, modified

**Ledger integration (3 tests):**
6. `test_smoke_ledger_write_query()` — Write event → GET /ledger/events → event in list
7. `test_smoke_ledger_cost_with_tokens()` — Write LLM_CALL event with cost_tokens_up + cost_tokens_down → GET /ledger/cost → verify tokens_up, tokens_down in response
8. `test_smoke_ledger_query_by_type()` — Write 3 events with different types → POST /ledger/query with filter → only matching events returned

**Shell exec (2 tests):**
9. `test_smoke_shell_exec_allowed()` — POST /shell/exec with `echo hello` → status: success, stdout contains "hello"
10. `test_smoke_shell_exec_denied()` — POST /shell/exec with denied command → status: denied

**Sync routes (2 tests):**
11. `test_smoke_sync_status()` — GET /sync/status → returns last_sync, pending, conflicts
12. `test_smoke_sync_trigger()` — POST /sync/trigger → returns sync result (even if no files to sync)

**Volumes + Node (3 tests):**
13. `test_smoke_volumes_list()` — GET /storage/volumes → returns list with home:// volume
14. `test_smoke_node_status_local()` — GET /node/status → returns node info in local mode
15. `test_smoke_full_flow()` — Write file → write ledger event → query ledger → read file back → all consistent (full integration)

### Important Implementation Notes

- Use the existing `conftest.py` fixtures where possible (don't duplicate)
- The smoke_client fixture must properly trigger the app's lifespan so all services initialize
- For shell exec tests: use `echo` which is allowed on all platforms
- For ledger tests: use the routes directly (POST body), don't call writer.py directly
- All tests must clean up (tmp_path fixture handles this)
- Use `monkeypatch` to override settings, NOT `unittest.mock.patch` (avoids thread issues)

---

## Browser Smoke Tests

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\__tests__\smoke.test.tsx`

Integration tests that render real components and verify wiring between them. Mock the hivenode API (fetch/httpx calls) but let everything else run real — relay bus, state management, adapters.

### Test Setup

```typescript
import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor, act } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

// Mock the hivenode API at the fetch level
const mockFetch = vi.fn();
global.fetch = mockFetch;

beforeEach(() => {
    vi.clearAllMocks();
    localStorage.clear();
});
```

### Tests (~10)

**Chat persistence flow (3 tests):**
1. `test_smoke_create_conversation_stores_markdown()` — Create conversation via chatApi → verify markdown format with frontmatter
2. `test_smoke_add_message_updates_conversation()` — Create conversation → add message → read back → message present in markdown
3. `test_smoke_dual_write_both_volumes()` — Create conversation with volume_preference='both' → verify write called for both home:// and cloud://

**Shell parser integration (3 tests):**
4. `test_smoke_shell_command_detected_and_routed()` — Input `ls -la` in hybrid mode → parseInput returns type:'shell' → executeShellCommand called with correct args
5. `test_smoke_chat_message_routed_to_llm()` — Input "how do I deploy?" → parseInput returns type:'chat' → LLM service called
6. `test_smoke_mode_switch_affects_parsing()` — Set mode to 'shell' → input "hello" → treated as shell, not chat

**Tree-browser + relay bus (2 tests):**
7. `test_smoke_conversation_select_publishes_bus_event()` — Render ChatNavigatorPane → click conversation → verify `conversation:selected` message published on bus
8. `test_smoke_tree_refreshes_on_conversation_created()` — Render ChatNavigatorPane → publish `conversation:created` on bus → verify tree reloads

**Chat markdown round-trip (2 tests):**
9. `test_smoke_markdown_serialize_parse_roundtrip()` — Create conversation with messages → serialize to markdown → parse back → all data preserved
10. `test_smoke_markdown_preserves_frontmatter()` — Serialize conversation with volume_preference, model, timestamps → parse → all metadata intact

### Important Implementation Notes

- Mock `fetch` at the global level, not individual modules — this tests real code paths
- For chatApi tests: mock the hivenode `/storage/read` and `/storage/write` responses
- For shell parser tests: mock the `/shell/exec` endpoint response
- For tree-browser tests: use `@testing-library/react` `render()` with real components
- The relay bus should be real (not mocked) — that's the integration we're testing
- Use `waitFor()` for async operations (fetch, bus message delivery)

---

## Files to Read First

**Backend:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\conftest.py` (shared fixtures)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_e2e.py` (E2E pattern reference)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_storage_local_auth.py` (TestClient + settings pattern)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\main.py` (app + lifespan)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\dependencies.py` (service injection)

**Browser:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\terminal\chatApi.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\terminal\chatMarkdown.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\terminal\shellParser.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\terminal\shellExecutor.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\ChatNavigatorPane.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\messageBus.ts`

---

## Constraints

- No file over 500 lines
- TDD — tests first (but these ARE the tests, so write them and verify they pass)
- No stubs in the smoke tests themselves — the point is testing real integration
- Mock only external boundaries (HTTP calls to hivenode API in browser, filesystem in backend via tmp_path)
- Tests must run in CI (no real server needed, no network, no Docker)
- Each test should be independent (no shared state between tests)

---

## Definition of Done

- [x] `tests/hivenode/test_smoke.py` written (~15 backend smoke tests)
- [x] `browser/src/__tests__/smoke.test.tsx` written (~10 browser smoke tests)
- [x] All smoke tests pass: `python -m pytest tests/hivenode/test_smoke.py -v`
- [x] All smoke tests pass: `npx vitest run browser/src/__tests__/smoke.test.tsx` (from browser/ dir)
- [x] No existing tests broken
- [x] Tests verify real integration paths, not just mocked behavior

---

## Response File

Write your response to:
`C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260313-TASK-041-RESPONSE.md`

Use the standard 8-section format from BOOT.md Rule 10.

---

**End of TASK-041.**
