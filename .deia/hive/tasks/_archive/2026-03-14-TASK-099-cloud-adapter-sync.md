# TASK-099: Convert CloudAdapter to Synchronous

## Objective
Convert CloudAdapter from async (httpx.AsyncClient) to sync (httpx.Client) so it matches the BaseVolumeAdapter synchronous interface.

## Context
CloudAdapter (`hivenode/storage/adapters/cloud.py`) currently uses `httpx.AsyncClient` and `async def` methods. But `BaseVolumeAdapter` defines a sync interface (`def read()` returns bytes, not coroutine). The VolumeRegistry assumes sync. Any code calling `adapter.read()` gets a coroutine instead of bytes.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\storage\adapters\cloud.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\storage\adapters\base.py` (BaseVolumeAdapter interface)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\storage\test_cloud_adapter.py`

## Deliverables
- [ ] Modify `hivenode/storage/adapters/cloud.py`:
  - Replace `httpx.AsyncClient` with `httpx.Client`
  - Remove `async` from all method signatures
  - Replace `await self._client.get(...)` with `self._client.get(...)`
  - Replace `await self._client.put(...)` with `self._client.put(...)`
  - Replace `await self._client.delete(...)` with `self._client.delete(...)`
  - Keep the same error handling (VolumeOfflineError on connection failure)
  - Keep the same SyncQueue integration
- [ ] Modify `tests/hivenode/storage/test_cloud_adapter.py`:
  - Remove `@pytest.mark.asyncio` decorators
  - Remove `async def` from test functions
  - Remove `await` from all adapter calls
  - Replace `respx` async mocking with sync httpx mocking (respx supports both)
  - All 15 existing tests must pass
- [ ] Verify: `adapter.read("path")` returns `bytes`, not coroutine

## Constraints
- No file over 500 lines
- Do NOT change the public API (method names, parameters, return types stay the same)
- Do NOT modify `base.py` or `sync_queue.py`
- Keep all existing functionality (offline detection, write queueing)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia\hive\responses\20260314-TASK-099-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.

## Model Assignment
haiku
