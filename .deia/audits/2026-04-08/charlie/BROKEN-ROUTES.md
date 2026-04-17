# Broken Routes Summary

**Date:** 2026-04-08
**Total routes with issues:** 53

## Issue Categories

### 1. Routes Returning 404 (Not Found) - 50 routes

These routes are referenced in code but not properly mounted or path is incorrect:

| Route | Expected Module | Status | Issue |
|-------|----------------|--------|-------|
| POST /auth/register | auth | 404 | Not mounted or wrong path |
| POST /auth/login | auth | 404 | Not mounted or wrong path |
| POST /auth/refresh | auth | 404 | Not mounted or wrong path |
| POST /auth/logout | auth | 404 | Not mounted or wrong path |
| GET /auth/me | auth | 404 | Not mounted or wrong path |
| POST /ledger/write | ledger | 404 | Not mounted or wrong path |
| POST /ledger/query | ledger | 404 | Not mounted or wrong path |
| GET /ledger/tail | ledger | 404 | Not mounted or wrong path |
| POST /storage/info | storage | 404 | Not mounted or wrong path |
| GET /node/list | node | 404 | Not mounted or wrong path |
| GET /llm/models | llm | 404 | Not mounted or wrong path |
| POST /shell/execute | shell | 404 | Not mounted or wrong path |
| POST /sync/push | sync | 404 | Not mounted or wrong path |
| POST /repo/search | repo | 404 | Not mounted or wrong path |
| POST /rag/query | rag | 404 | Not mounted or wrong path |
| POST /rag/indexer/index | indexer | 404 | Not mounted or wrong path |
| GET /rag/indexer/status | indexer | 404 | Not mounted or wrong path |
| POST /rag/bok/add | bok | 404 | Not mounted or wrong path |
| GET /rag/bok/list | bok | 404 | Not mounted or wrong path |
| GET /relay/channels/test-channel | relay | 404 | Channel not found (expected) |
| POST /relay/messages | relay-messages | 404 | Not mounted or wrong path |
| GET /api/kanban/boards | kanban | 404 | Not mounted or wrong path |
| POST /api/kanban/boards | kanban | 404 | Not mounted or wrong path |
| GET /api/progress/status | progress | 404 | Not mounted or wrong path |
| POST /build/report | build-monitor | 404 | Not mounted or wrong path |
| POST /sim/run | simulation | 404 | Not mounted or wrong path |
| POST /phase-ir/validate | phase-ir | 404 | Not mounted or wrong path |
| GET /phase-ir/schema | phase-ir | 404 | Not mounted or wrong path |
| POST /des/run | des-engine | 404 | Not mounted or wrong path |
| POST /optimize/run | optimize | 404 | Not mounted or wrong path |
| POST /pipeline-sim/run | pipeline-sim | 404 | Not mounted or wrong path |
| GET /entities | bot-embeddings | 404 | Not mounted or wrong path |
| POST /entities | bot-embeddings | 404 | Not mounted or wrong path |
| GET /tabletop/games | tabletop | 404 | Not mounted or wrong path |
| GET /playback/sessions | playback | 404 | Not mounted or wrong path |
| GET /compare/snapshots | compare | 404 | Not mounted or wrong path |
| GET /preferences | preferences | 404 | Not mounted or wrong path |
| PUT /preferences | preferences | 404 | Not mounted or wrong path |
| GET /early-access/features | early-access | 404 | Not mounted or wrong path |
| GET /queue-events | queue-events | 404 | Not mounted or wrong path |
| GET /prism/status | prism | 404 | Not mounted or wrong path |
| POST /voice/transcribe | voice | 404 | Not mounted or wrong path |

### 2. Routes Returning 405 (Method Not Allowed) - 5 routes

These routes exist but don't support the tested HTTP method:

| Route | Tested Method | Status | Issue |
|-------|--------------|--------|-------|
| POST /storage/read | POST | 405 | Likely expects GET |
| POST /storage/list | POST | 405 | Likely expects GET |
| POST /storage/delete | POST | 405 | Likely expects DELETE |
| POST /sync/pull | POST | 405 | Check actual method |
| POST /repo/index | POST | 405 | Check actual method |
| POST /rag/index | POST | 405 | Check actual method |
| GET /relay/messages/test-channel | GET | 405 | Check actual method |

### 3. Routes Returning 422 (Validation Error) - 2 routes

These routes work but test body was invalid:

| Route | Status | Issue |
|-------|--------|-------|
| POST /storage/write | 422 | Missing required fields in body |
| POST /api/inventory/features | 422 | Missing required fields in body |

### 4. Routes Requiring Auth (401) - Expected Behavior

| Route | Status | Note |
|-------|--------|------|
| POST /node/announce | 401 | Auth required (should be no-auth) |
| POST /node/heartbeat | 401 | Auth required (should be no-auth) |

## Routes That Work (11 total)

- GET / (root)
- GET /health
- GET /storage/volumes
- POST /llm/chat (returns error but route works)
- GET /sync/status
- GET /repo/stats
- GET /relay/channels
- POST /relay/channels
- GET /build/status
- GET /build/notifications
- GET /api/inventory/features

## Recommendations

1. **Audit routes/__init__.py** - Many modules imported but routes may not be properly registered
2. **Check route decorators** - Verify @router.get/@router.post match expected methods
3. **Fix auth decorators** - Node announce/heartbeat should not require auth
4. **Verify path prefixes** - Many 404s suggest path prefix mismatches
5. **Review storage routes** - Methods don't align with REST conventions
6. **Test with auth tokens** - Many 404s might actually be auth failures

## High Priority Fixes

1. Auth routes (login, register, logout) - core functionality
2. Ledger routes (write, query, tail) - event logging broken
3. Storage routes (read, list, delete, info) - file system access broken
4. Relay messages routes - messaging system incomplete
5. Node routes - distributed features broken
