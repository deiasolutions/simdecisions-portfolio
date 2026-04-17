# TASK-CLOUD-STORAGE-D: Cloud Storage Documentation

## Objective

Document cloud storage architecture, encryption policy, deployment requirements, quota limits, and user responsibilities for custom volumes.

---

## Context

TASK-A, TASK-B, and TASK-C implemented cloud storage. This task documents:

1. **Cloud storage architecture** — PostgreSQL on Railway, 10 MB quota per user
2. **Encryption at rest** — Railway PostgreSQL only (not user-added volumes)
3. **Namespace isolation** — users cannot access other users' files
4. **Quota enforcement** — 10 MB per user (free tier)
5. **Deployment requirements** — `DATABASE_URL` env var, cloud mode detection
6. **User-added volumes** — user's security responsibility (no encryption guarantees)
7. **Visitor export** — client-side download, no cloud writes

---

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\storage\cloud_store.py` — store implementation
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\cloud_storage_routes.py` — routes
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\main.py` — cloud route registration
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\` — existing docs (if any)

---

## Deliverables

- [ ] File created: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\CLOUD-STORAGE.md`
- [ ] File updated: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\DEPLOYMENT.md` (create if doesn't exist)
- [ ] Documentation covers all acceptance criteria
- [ ] Markdown format, clear sections, code examples

---

## Content Requirements

### File: `docs/CLOUD-STORAGE.md`

Create comprehensive documentation with these sections:

#### 1. Overview

- What is cloud storage in ShiftCenter?
- How it differs from local storage (`home://`, `local://`)
- URI format: `cloud://{user_id}/path/to/file`

#### 2. Architecture

- **Backend:** Railway hivenode with PostgreSQL
- **Tables:** `cloud_files` (file content as BYTEA), `cloud_quotas` (per-user usage)
- **Client:** `CloudAdapter` (HTTP client in `hivenode/storage/adapters/cloud.py`)
- **Routes:** `/storage/write`, `/storage/read`, `/storage/list`, `/storage/stat`, `/storage/delete`, `/storage/quota`
- **Auth:** JWT required (ra96it/hodeia identity service)
- **Namespace isolation:** `user_id` from JWT `sub` claim

#### 3. Quota Limits

- **Free tier:** 10 MB per user (10,485,760 bytes)
- **Enforcement:** Writes rejected with 400 error when quota exceeded
- **Tracking:** Real-time quota updates on write/delete
- **Quota check:** `GET /storage/quota` returns `{"bytes_used": X, "quota_bytes": 10485760}`

#### 4. Encryption at Rest

**IMPORTANT:** Clearly document security boundaries.

- **Railway PostgreSQL:** Encrypted at rest by Railway infrastructure
- **Server-side storage:** Cloud files stored in PostgreSQL on Railway (encrypted)
- **User-added custom volumes:** NOT encrypted by ShiftCenter — user's responsibility
- **In-transit:** HTTPS for all cloud storage requests

Example text:
```markdown
## Encryption and Security

### What ShiftCenter Encrypts

- **Cloud storage (Railway PostgreSQL):** Encrypted at rest by Railway infrastructure. File content stored as BYTEA in `cloud_files` table is protected by Railway's encryption-at-rest policy.
- **In-transit:** All cloud storage requests use HTTPS.

### What ShiftCenter Does NOT Encrypt

- **User-added custom volumes:** If you configure custom volume endpoints (e.g., `work://` pointing to your own storage backend), ShiftCenter makes NO security guarantees. Encryption, access control, and data protection are YOUR responsibility.
- **Local filesystem volumes:** `home://` and `local://` volumes store files on local disk without encryption. If you need encrypted local storage, use OS-level disk encryption (BitLocker, FileVault, LUKS).

### Your Responsibility

If you add custom volume adapters or endpoints to your hivenode configuration, YOU are responsible for:
- Access control
- Encryption (at rest and in transit)
- Data backup
- Compliance with data protection regulations
```

#### 5. Namespace Isolation

- Users can only access `cloud://{user_id}/...` where `user_id` matches their JWT `sub` claim
- Attempts to access other users' namespaces return 403 Forbidden
- No shared storage between users (by design)

#### 6. Visitor Export

- **Visitors (no auth):** Can export (download) files created locally
- **No cloud writes without JWT:** Visitors get 401 on cloud storage write attempts
- **Export mechanism:** Client-side browser download, NOT cloud storage

Example text:
```markdown
## Visitor Access

Visitors (users who haven't signed in) can:
- **Export files:** Download files they created locally via browser download (client-side)
- **No cloud writes:** Visitors cannot write to cloud storage (401 Unauthorized)

Cloud storage is ONLY available to authenticated users with valid JWT tokens.
```

#### 7. API Reference

Document all 6 endpoints with request/response examples:

```markdown
### POST /storage/write

Write file to cloud storage.

**Auth:** Required (JWT)

**Request:**
```json
{
  "uri": "cloud://user123/docs/report.pdf",
  "content_base64": "SGVsbG8gd29ybGQ="
}
```

**Response (200 OK):**
```json
{
  "ok": true,
  "uri": "cloud://user123/docs/report.pdf"
}
```

**Error (400 - Quota Exceeded):**
```json
{
  "error": "quota_exceeded",
  "bytes_used": 10000000,
  "quota_bytes": 10485760
}
```

... (repeat for all 6 endpoints)
```

---

### File: `docs/DEPLOYMENT.md`

Create or update deployment documentation with cloud storage section:

#### Section: Cloud Storage Deployment (Railway)

```markdown
## Cloud Storage (Railway Deployment)

### Prerequisites

1. **Railway account** with PostgreSQL database provisioned
2. **DATABASE_URL** environment variable set in Railway project

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `DATABASE_URL` | Yes | PostgreSQL connection string (Railway provides this) |
| `HIVENODE_MODE` | Yes | Set to `"cloud"` for Railway deployment |
| `PORT` | Auto | Railway sets this automatically |

### Database Migration

Cloud storage tables (`cloud_files`, `cloud_quotas`) are created automatically via SQLAlchemy `Base.metadata.create_all()` on hivenode startup.

No manual migration required.

### Route Registration

Cloud storage routes are registered ONLY in cloud mode:

- **Cloud mode:** Uses `/storage/*` routes backed by PostgreSQL (from `cloud_storage_routes.py`)
- **Local/remote mode:** Uses `/storage/*` routes backed by local filesystem (from `storage_routes.py`)

This is handled automatically in `hivenode/main.py` based on `settings.mode`.

### Verification

After deployment:

1. Check health endpoint: `curl https://your-app.railway.app/`
2. Verify cloud storage routes: `curl -H "Authorization: Bearer <jwt>" https://your-app.railway.app/storage/quota`
3. Expected response: `{"bytes_used": 0, "quota_bytes": 10485760}`

### Troubleshooting

- **Error: "Database not initialized"** → Check `DATABASE_URL` env var
- **Error: 401 on all requests** → Verify JWT token from ra96it/hodeia
- **Error: 400 quota exceeded** → User has reached 10 MB limit (free tier)
```

---

## Constraints

- **Markdown format:** All docs in `.md` format
- **No stubs:** Complete documentation, no placeholders
- **Clear security boundaries:** Explicitly state what ShiftCenter encrypts vs. user responsibility
- **API examples:** Include request/response JSON for all 6 endpoints
- **Deployment checklist:** Step-by-step Railway deployment instructions

---

## Acceptance Criteria

- [ ] `docs/CLOUD-STORAGE.md` created with 7 sections: Overview, Architecture, Quota Limits, Encryption, Namespace Isolation, Visitor Export, API Reference
- [ ] `docs/DEPLOYMENT.md` updated with Cloud Storage Deployment section
- [ ] Encryption policy documented: Railway PostgreSQL encrypted, user-added volumes NOT encrypted
- [ ] User responsibility clearly stated for custom volumes
- [ ] Quota limits documented: 10 MB per user
- [ ] Namespace isolation documented: users cannot access other users' files
- [ ] Visitor export documented: client-side download, no cloud writes
- [ ] API reference with all 6 endpoints (request/response examples)
- [ ] Deployment checklist for Railway
- [ ] No stubs, no placeholders

---

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260325-TASK-CLOUD-STORAGE-D-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — N/A (documentation task, no tests)
5. **Build Verification** — N/A (documentation task)
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — any gaps, links to verify, next tasks

DO NOT skip any section.

---

## Dependencies

None. Can be done in parallel with other tasks (but should read completed code for accurate docs).

---

## Test Command

No tests (documentation task). Verify by reading generated docs.
