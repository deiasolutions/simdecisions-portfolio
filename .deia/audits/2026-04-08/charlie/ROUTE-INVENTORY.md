# Hivenode Route Inventory

**Total routes:** 64

## Routes by Module

### auth

| Method | Path | Auth Required |
|--------|------|---------------|
| POST | /auth/register | No |
| POST | /auth/login | No |
| POST | /auth/refresh | Yes |
| POST | /auth/logout | Yes |
| GET | /auth/me | Yes |

### bok

| Method | Path | Auth Required |
|--------|------|---------------|
| POST | /rag/bok/add | Yes |
| GET | /rag/bok/list | Yes |

### bot-embeddings

| Method | Path | Auth Required |
|--------|------|---------------|
| GET | /entities | Yes |
| POST | /entities | Yes |

### build-monitor

| Method | Path | Auth Required |
|--------|------|---------------|
| GET | /build/status | No |
| POST | /build/report | No |

### compare

| Method | Path | Auth Required |
|--------|------|---------------|
| GET | /compare/snapshots | Yes |

### des-engine

| Method | Path | Auth Required |
|--------|------|---------------|
| POST | /des/run | Yes |

### early-access

| Method | Path | Auth Required |
|--------|------|---------------|
| GET | /early-access/features | Yes |

### health

| Method | Path | Auth Required |
|--------|------|---------------|
| GET | /health | No |

### indexer

| Method | Path | Auth Required |
|--------|------|---------------|
| POST | /rag/indexer/index | Yes |
| GET | /rag/indexer/status | Yes |

### inventory

| Method | Path | Auth Required |
|--------|------|---------------|
| GET | /api/inventory/features | Yes |
| POST | /api/inventory/features | Yes |

### kanban

| Method | Path | Auth Required |
|--------|------|---------------|
| GET | /api/kanban/boards | Yes |
| POST | /api/kanban/boards | Yes |

### ledger

| Method | Path | Auth Required |
|--------|------|---------------|
| POST | /ledger/write | Yes |
| POST | /ledger/query | Yes |
| GET | /ledger/tail | Yes |

### llm

| Method | Path | Auth Required |
|--------|------|---------------|
| POST | /llm/chat | Yes |
| GET | /llm/models | Yes |

### node

| Method | Path | Auth Required |
|--------|------|---------------|
| POST | /node/announce | No |
| GET | /node/list | Yes |
| POST | /node/heartbeat | No |

### notifications

| Method | Path | Auth Required |
|--------|------|---------------|
| GET | /build/notifications | Yes |

### optimize

| Method | Path | Auth Required |
|--------|------|---------------|
| POST | /optimize/run | Yes |

### phase-ir

| Method | Path | Auth Required |
|--------|------|---------------|
| POST | /phase-ir/validate | Yes |
| GET | /phase-ir/schema | Yes |

### pipeline-sim

| Method | Path | Auth Required |
|--------|------|---------------|
| POST | /pipeline-sim/run | Yes |

### playback

| Method | Path | Auth Required |
|--------|------|---------------|
| GET | /playback/sessions | Yes |

### preferences

| Method | Path | Auth Required |
|--------|------|---------------|
| GET | /preferences | Yes |
| PUT | /preferences | Yes |

### prism

| Method | Path | Auth Required |
|--------|------|---------------|
| GET | /prism/status | Yes |

### progress

| Method | Path | Auth Required |
|--------|------|---------------|
| GET | /api/progress/status | Yes |

### queue-events

| Method | Path | Auth Required |
|--------|------|---------------|
| GET | /queue-events | Yes |

### rag

| Method | Path | Auth Required |
|--------|------|---------------|
| POST | /rag/query | Yes |
| POST | /rag/index | Yes |

### relay

| Method | Path | Auth Required |
|--------|------|---------------|
| GET | /relay/channels | Yes |
| POST | /relay/channels | Yes |
| GET | /relay/channels/test-channel | Yes |

### relay-messages

| Method | Path | Auth Required |
|--------|------|---------------|
| POST | /relay/messages | Yes |
| GET | /relay/messages/test-channel | Yes |

### repo

| Method | Path | Auth Required |
|--------|------|---------------|
| POST | /repo/index | Yes |
| POST | /repo/search | Yes |
| GET | /repo/stats | Yes |

### root

| Method | Path | Auth Required |
|--------|------|---------------|
| GET | / | No |

### shell

| Method | Path | Auth Required |
|--------|------|---------------|
| POST | /shell/execute | Yes |

### simulation

| Method | Path | Auth Required |
|--------|------|---------------|
| POST | /sim/run | Yes |

### storage

| Method | Path | Auth Required |
|--------|------|---------------|
| POST | /storage/write | Yes |
| POST | /storage/read | Yes |
| POST | /storage/list | Yes |
| POST | /storage/delete | Yes |
| POST | /storage/info | Yes |
| GET | /storage/volumes | Yes |

### sync

| Method | Path | Auth Required |
|--------|------|---------------|
| POST | /sync/push | Yes |
| POST | /sync/pull | Yes |
| GET | /sync/status | Yes |

### tabletop

| Method | Path | Auth Required |
|--------|------|---------------|
| GET | /tabletop/games | Yes |

### voice

| Method | Path | Auth Required |
|--------|------|---------------|
| POST | /voice/transcribe | Yes |

