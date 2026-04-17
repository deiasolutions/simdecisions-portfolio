# SPEC-CLOUD-STORAGE-RAILWAY: Cloud Storage Backend on Railway

## Objective

Wire up cloud-side storage on Railway so signed-in users get persistent cloud storage through the named volume system. Visitors get export-only (download what they build, no cloud persistence).

Storage tiers:
- Visitor (no auth): Export only -- download/save-as from the tool. No cloud storage.
- Signed-in (free): cloud:// volume mounted, 10 MB quota.

Encryption at rest applies to our database on the server only (Railway PostgreSQL encrypted at rest). User-added endpoints (custom volumes) are the user's responsibility -- we do not encrypt, audit, or guarantee security on user-declared volumes pointing to external storage.

## Files to Read First

- hivenode/storage/adapters/cloud.py
- hivenode/routes/storage_routes.py
- hivenode/storage/config.py
- hivenode/sync/engine.py
- hivenode/storage/adapters/base.py
- hivenode/main.py
- hivenode/routes/__init__.py

## Files to Modify

- hivenode/routes/storage_routes.py
- hivenode/storage/adapters/cloud.py
- hivenode/storage/config.py
- hivenode/main.py
- hivenode/routes/__init__.py

## Deliverables

- [ ] Cloud storage routes: /storage/write, /storage/read, /storage/list, /storage/stat, /storage/delete on cloud hivenode
- [ ] Quota tracking table and enforcement (10 MB per user)
- [ ] GET /storage/quota endpoint for authenticated user
- [ ] Visitor export support (no cloud writes without JWT)
- [ ] Wire existing CloudAdapter to new server-side routes
- [ ] Tests for quota enforcement, namespace isolation, auth rejection

## Acceptance Criteria

- [ ] Cloud hivenode serves /storage/* routes backed by PostgreSQL
- [ ] Per-user namespace isolation (users cannot access other users' files)
- [ ] 10 MB quota enforced per user
- [ ] Quota check returns structured error on exceed
- [ ] GET /storage/quota returns usage for authenticated user
- [ ] Visitors get no cloud storage (401 on cloud writes without JWT)
- [ ] Visitor export (download) works without auth
- [ ] Encryption at rest on server DB only -- documented
- [ ] User-added endpoints security is user's responsibility -- documented
- [ ] SyncQueue flushes to cloud storage
- [ ] Tests for quota enforcement, namespace isolation, auth rejection

## Smoke Test

- [ ] cd hivenode && python -m pytest tests/hivenode/ -v -k storage -- tests pass
- [ ] cd hivenode && python -m pytest tests/ -v -- no regressions

## Constraints

- TDD, 500-line limit per file, Python 3.13
- JWT auth via ra96it/hodeia
- PostgreSQL on Railway
- No encryption on user-declared custom volumes
- Per-user namespace: cloud://{user_id}/path/to/file
- Storage backed by Railway PostgreSQL (file content as bytea or linked to Railway object storage)

## Model Assignment

sonnet

## Priority

P1
