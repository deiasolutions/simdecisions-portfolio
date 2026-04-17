# TASK-021: Wire Chat Persistence to Local Hivenode

**Date:** 2026-03-11
**Priority:** P1 (Alpha — after TASK-020)
**Assigned to:** BEE (Sonnet)
**Estimated turns:** 30-40

---

## Objective

Replace `chatApi.ts` (currently pointing at `api.simdecisions.com`) with local hivenode storage. Chat history persists at `home://chat/` via hivenode's `/storage/read` and `/storage/write` routes. localStorage stays as fallback when hivenode isn't reachable.

This gives the user `home://` chat history that persists across browser sessions and (eventually) syncs to cloud.

---

## Architecture

```
Browser (chatApi.ts)
  │
  ├─ hivenode available: fetch('http://localhost:8420/storage/...')
  │   └─ Persists to: ~/.shiftcenter/storage/home/chat/
  │
  └─ hivenode unavailable: localStorage fallback
      └─ Persists to: sd:frank_entries, sd:frank_ledger
```

### Storage layout (home:// volume)

```
home://chat/
  ├── conversations.json           # Index: [{id, title, created_at, updated_at}]
  └── conversations/
      ├── {conv-id-1}.json         # Full conversation with messages
      ├── {conv-id-2}.json
      └── ...
```

---

## Pre-requisite: Local Mode Auth Bypass

**BLOCKER:** Storage routes currently require JWT (`Depends(verify_jwt)`). Local mode has no ra96it running.

**Fix (part of this task):** Add auth bypass for local mode:

```python
# In hivenode/dependencies.py or a new middleware
async def verify_jwt_or_local(request: Request):
    """Skip JWT verification in local mode — it's the user's own machine."""
    if settings.mode == "local":
        return {"sub": "local-user", "mode": "local"}
    return await verify_jwt(request)
```

Update storage routes to use `verify_jwt_or_local` instead of `verify_jwt`.

---

## Browser changes

### Modified files

| File | Change |
|------|--------|
| `browser/src/services/frank/chatApi.ts` | Rewrite to call hivenode storage, localStorage fallback |
| `browser/src/primitives/terminal/useTerminal.ts` | Use new chatApi for persistence instead of raw localStorage |

### chatApi.ts rewrite

```typescript
const HIVENODE_URL = import.meta.env.VITE_HIVENODE_URL || 'http://localhost:8420';

async function isHivenodeAvailable(): Promise<boolean> {
  try {
    const res = await fetch(`${HIVENODE_URL}/health`, { signal: AbortSignal.timeout(2000) });
    return res.ok;
  } catch { return false; }
}

// Cache availability check for 30 seconds
let _available: boolean | null = null;
let _checkedAt = 0;

async function getBackend(): Promise<'hivenode' | 'localStorage'> {
  if (_available !== null && Date.now() - _checkedAt < 30000) {
    return _available ? 'hivenode' : 'localStorage';
  }
  _available = await isHivenodeAvailable();
  _checkedAt = Date.now();
  return _available ? 'hivenode' : 'localStorage';
}
```

### Conversation operations

| Operation | hivenode path | localStorage fallback |
|-----------|--------------|----------------------|
| Create conversation | `POST /storage/write` → `home://chat/conversations/{id}.json` + update index | Create in `sd:frank_conversations` |
| List conversations | `GET /storage/read?uri=home://chat/conversations.json` | Read `sd:frank_conversations` |
| Get conversation | `GET /storage/read?uri=home://chat/conversations/{id}.json` | Read `sd:frank_conv_{id}` |
| Add message | `POST /storage/write` → append to `home://chat/conversations/{id}.json` | Append to `sd:frank_conv_{id}` |
| Delete conversation | `DELETE /storage/delete?uri=home://chat/conversations/{id}.json` + update index | Remove from `sd:frank_conversations` |

---

## Backend changes

### Modified files

| File | Change |
|------|--------|
| `hivenode/dependencies.py` | Add `verify_jwt_or_local()` that bypasses JWT in local mode |
| `hivenode/routes/storage_routes.py` | Use `verify_jwt_or_local` instead of `verify_jwt` |

---

## Tests

### New test files

| File | Tests |
|------|-------|
| `tests/hivenode/test_storage_local_auth.py` | Local mode bypasses JWT, cloud mode requires it |
| `browser/src/services/frank/__tests__/chatApi.test.ts` | Update: hivenode backend, localStorage fallback, availability probe |

### Test scenarios

1. Local mode: storage routes accessible without JWT
2. Cloud mode: storage routes still require JWT (no regression)
3. chatApi creates conversation in hivenode when available
4. chatApi falls back to localStorage when hivenode unreachable
5. Availability check caches for 30 seconds
6. Conversation CRUD round-trip through hivenode storage

---

## Acceptance Criteria

- [ ] `python -m hivenode` starts on port 8420
- [ ] Storage routes work in local mode without JWT
- [ ] Storage routes still require JWT in cloud mode (no regression)
- [ ] `chatApi.ts` probes hivenode health and uses it when available
- [ ] Chat conversations persist at `home://chat/conversations/` on disk
- [ ] Falls back to localStorage when hivenode is not running
- [ ] Tree-browser sidebar loads conversation list from hivenode storage
- [ ] All tests pass

---

## NOT in scope

- Cloud sync (home:// → cloud://) — needs TASK-019 cloud mode
- Real-time sync via WebSocket — HTTP polling only
- Conversation search/indexing — just JSON files for now
- Migration tool (localStorage → hivenode) — manual for Alpha

---

## Dependencies

- **TASK-019** (Hivenode FastAPI server) — DONE
- **TASK-003** (Named volume storage) — DONE
- **TASK-016** (Tree browser primitive) — DONE
- **TASK-020** (LLM proxy route) — concurrent, no hard dependency
