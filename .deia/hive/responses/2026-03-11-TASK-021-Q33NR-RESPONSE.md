# RESPONSE: TASK-021 — Wire Chat Persistence to Local Hivenode

**Date:** 2026-03-11
**Respondent:** Q33NR (regent) + BEE (sonnet, partial)
**Status:** COMPLETE

---

## Summary

Chat persistence now uses hivenode `/storage/` routes when available, with localStorage as automatic fallback. Local mode auth bypass implemented so storage routes work without JWT on the user's own machine.

## Work Completed

### Backend (Python)

1. **`hivenode/dependencies.py`** — Added `verify_jwt_or_local()`:
   - Local mode returns stub claims `{"sub": "local-user", ...}` — no JWT needed
   - Cloud/remote modes delegate to full `verify_jwt()` — no regression

2. **`hivenode/routes/storage_routes.py`** — All 5 routes (`read`, `write`, `list`, `stat`, `delete`) now use `Depends(verify_jwt_or_local)` instead of `Depends(verify_jwt)`

### Frontend (TypeScript)

3. **`browser/src/services/frank/chatApi.ts`** — Complete rewrite:
   - Backend detection: probes `localhost:8420/health` with 2s timeout
   - Caches result for 30 seconds (avoids health-check spam)
   - Storage layout: `home://chat/conversations.json` (index) + `home://chat/conversations/{id}.json`
   - Full CRUD: `createConversation`, `listConversations`, `getConversation`, `addMessage`, `deleteConversation`, `resumeConversation`
   - localStorage fallback with `sd:frank_conversations` / `sd:frank_conv_{id}` keys

### Tests

4. **`tests/hivenode/test_storage_local_auth.py`** — 10 tests:
   - 6 local mode tests (all storage routes work without JWT, write→read round-trip)
   - 4 cloud mode tests (all routes still require JWT)
   - Uses mock transport to avoid SQLite thread-safety issues with TestClient

5. **`browser/src/services/frank/__tests__/chatApi.test.ts`** — 14 tests:
   - Backend detection (hivenode vs localStorage, caching)
   - localStorage fallback CRUD (create, list, get, add message, delete)
   - Resume codes, unique IDs, metrics tracking

## Test Results

- Python local auth tests: **10/10 PASSING**
- Browser chatApi tests: **14/14 PASSING**

## Bee Note

Sonnet bee completed the Python changes but was blocked on TypeScript file writes due to permission system. Q33NR completed the browser work directly.

## Files Changed

| File | Action |
|------|--------|
| `hivenode/dependencies.py` | Modified — added `verify_jwt_or_local()` |
| `hivenode/routes/storage_routes.py` | Modified — switched to `verify_jwt_or_local` |
| `browser/src/services/frank/chatApi.ts` | Rewritten — hivenode + localStorage fallback |
| `browser/src/services/frank/__tests__/chatApi.test.ts` | Rewritten — 14 tests |
| `tests/hivenode/test_storage_local_auth.py` | Created — 10 tests |
