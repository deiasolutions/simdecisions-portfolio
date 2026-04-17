# SPEC: Cloud Storage Adapter End-to-End on Railway

## Priority
P1

## Objective
Verify the cloud:// storage adapter works end-to-end on the deployed Railway hivenode. Write a file from the browser, read it back from another session.

## Context
Cloud adapter was built overnight (TASK-099 through TASK-102). Needs verification on the actual Railway deployment, not just local tests.

Files to read first:
- `hivenode/storage/adapters/cloud.py`
- `hivenode/storage/registry.py`
- `hivenode/routes/storage_routes.py`
- `hivenode/config.py` (HIVENODE_MODE=cloud settings)

## Acceptance Criteria
- [ ] POST /storage/write with volume=cloud:// writes to Railway persistent volume
- [ ] POST /storage/read with volume=cloud:// reads the file back
- [ ] POST /storage/list with volume=cloud:// lists the directory
- [ ] POST /storage/delete with volume=cloud:// deletes the file
- [ ] JWT required on all storage routes when HIVENODE_MODE=cloud
- [ ] Offline behavior: if cloud unreachable, return VOLUME_OFFLINE error (not crash)
- [ ] 6+ integration tests using real HTTP calls

## Smoke Test
- [ ] From browser: save a chat -> cloud hivenode writes file -> refresh page -> chat loads from cloud

## Depends On
- w3-01-vercel-railway-repoint

## Model Assignment
sonnet

## Constraints
This requires the Railway deployment from SPEC-3000 to be live. If Railway isn't deployed yet, write the tests against a local hivenode in cloud mode with a temp directory simulating the Railway volume.
