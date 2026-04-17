# Smoke Test Results

**Date:** 2026-04-08

**Total routes tested:** 64
**Success (2xx):** 11
**Client errors (4xx):** 53
**Server errors (5xx):** 0
**Connection failures:** 0

## Results by Route

| Method | Path | Status | Error | Preview |
|--------|------|--------|-------|--------|
| GET | / | 200 | - | {"service": "hivenode", "version": "0.1.0", "mode" |
| GET | /health | 200 | - | {"status": "ok", "mode": "local", "version": "0.1. |
| POST | /auth/register | 404 | - | {"detail": "Not Found"} |
| POST | /auth/login | 404 | - | {"detail": "Not Found"} |
| POST | /auth/refresh | 404 | - | {"detail": "Not Found"} |
| POST | /auth/logout | 404 | - | {"detail": "Not Found"} |
| GET | /auth/me | 404 | - | {"detail": "Not Found"} |
| POST | /ledger/write | 404 | - | {"detail": "Not Found"} |
| POST | /ledger/query | 404 | - | {"detail": "Not Found"} |
| GET | /ledger/tail | 404 | - | {"detail": "Not Found"} |
| POST | /storage/write | 422 | - | {"detail": [{"type": "missing", "loc": ["body", "u |
| POST | /storage/read | 405 | - | {"detail": "Method Not Allowed"} |
| POST | /storage/list | 405 | - | {"detail": "Method Not Allowed"} |
| POST | /storage/delete | 405 | - | {"detail": "Method Not Allowed"} |
| POST | /storage/info | 404 | - | {"detail": "Not Found"} |
| GET | /storage/volumes | 200 | - | {"volumes": [{"name": "home", "type": "local files |
| POST | /node/announce | 401 | - | {"detail": "Missing Authorization header"} |
| GET | /node/list | 404 | - | {"detail": "Not Found"} |
| POST | /node/heartbeat | 401 | - | {"detail": "Missing Authorization header"} |
| POST | /llm/chat | 200 | - | {"detail": {"error": "no_api_key", "message": "No  |
| GET | /llm/models | 404 | - | {"detail": "Not Found"} |
| POST | /shell/execute | 404 | - | {"detail": "Not Found"} |
| POST | /sync/push | 404 | - | {"detail": "Not Found"} |
| POST | /sync/pull | 405 | - | {"detail": "Method Not Allowed"} |
| GET | /sync/status | 200 | - | {"last_sync_at": "2026-03-25T18:00:30.485554+00:00 |
| POST | /repo/index | 405 | - | {"detail": "Method Not Allowed"} |
| POST | /repo/search | 404 | - | {"detail": "Not Found"} |
| GET | /repo/stats | 200 | - | {"total_files": 6708, "total_dirs": 424, "visible_ |
| POST | /rag/query | 404 | - | {"detail": "Not Found"} |
| POST | /rag/index | 405 | - | {"detail": "Method Not Allowed"} |
| POST | /rag/indexer/index | 404 | - | {"detail": "Not Found"} |
| GET | /rag/indexer/status | 404 | - | {"detail": "Not Found"} |
| POST | /rag/bok/add | 404 | - | {"detail": "Not Found"} |
| GET | /rag/bok/list | 404 | - | {"detail": "Not Found"} |
| GET | /relay/channels | 200 | - | [{"id": "announcements", "name": "announcements",  |
| POST | /relay/channels | 201 | - | {"id": "8fe8e170", "name": "test", "type": "channe |
| GET | /relay/channels/test-channel | 404 | - | {"detail": "Channel 'test-channel' not found"} |
| POST | /relay/messages | 404 | - | {"detail": "Not Found"} |
| GET | /relay/messages/test-channel | 405 | - | {"detail": "Method Not Allowed"} |
| GET | /api/kanban/boards | 404 | - | {"detail": "Not Found"} |
| POST | /api/kanban/boards | 404 | - | {"detail": "Not Found"} |
| GET | /api/progress/status | 404 | - | {"detail": "Not Found"} |
| GET | /build/status | 200 | - | {"total_cost_usd": 3252.546, "token_cost_usd": 324 |
| POST | /build/report | 404 | - | {"detail": "Not Found"} |
| GET | /build/notifications | 200 | - | {"notifications": [{"id": "notif-TASK-REVIEW-QUEEN |
| POST | /sim/run | 404 | - | {"detail": "Not Found"} |
| GET | /api/inventory/features | 200 | - | [] |
| POST | /api/inventory/features | 422 | - | {"detail": [{"type": "missing", "loc": ["body", "i |
| POST | /phase-ir/validate | 404 | - | {"detail": "Not Found"} |
| GET | /phase-ir/schema | 404 | - | {"detail": "Not Found"} |
| POST | /des/run | 404 | - | {"detail": "Not Found"} |
| POST | /optimize/run | 404 | - | {"detail": "Not Found"} |
| POST | /pipeline-sim/run | 404 | - | {"detail": "Not Found"} |
| GET | /entities | 404 | - | {"detail": "Not Found"} |
| POST | /entities | 404 | - | {"detail": "Not Found"} |
| GET | /tabletop/games | 404 | - | {"detail": "Not Found"} |
| GET | /playback/sessions | 404 | - | {"detail": "Not Found"} |
| GET | /compare/snapshots | 404 | - | {"detail": "Not Found"} |
| GET | /preferences | 404 | - | {"detail": "Not Found"} |
| PUT | /preferences | 404 | - | {"detail": "Not Found"} |
| GET | /early-access/features | 404 | - | {"detail": "Not Found"} |
| GET | /queue-events | 404 | - | {"detail": "Not Found"} |
| GET | /prism/status | 404 | - | {"detail": "Not Found"} |
| POST | /voice/transcribe | 404 | - | {"detail": "Not Found"} |
