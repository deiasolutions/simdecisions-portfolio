# Deployment Environment Variables — ShiftCenter Repoint Checklist

## Overview

Repointing two services from `deiasolutions/platform` to `deiasolutions/shiftcenter`:
- **Vercel** `simdecisions-2` → shiftcenter `browser/`
- **Railway** `merry-learning` → shiftcenter `hivenode/`

Two services stay on the old repo:
- **Railway** `beneficial-cooperation` (hodeia.me auth) — stays on `deiasolutions/platform`
- **Railway** `Ollama` — stays on `deiasolutions/platform`

---

## Vercel: `simdecisions-2` → ShiftCenter Browser

**Git repo:** `deiasolutions/shiftcenter`
**Root directory:** `browser/`
**Framework:** Vite
**Domain:** simdecisions.com (keep), shiftcenter.com (add when ready)

| Env Var | Source | Notes |
|---------|--------|-------|
| `VITE_API_URL` | Manual | URL of hivenode cloud service (e.g., `https://api.simdecisions.com` during transition, then `https://api.shiftcenter.com`) |
| `VITE_SD_GITHUB_CLIENT_ID` | GitHub OAuth App | SimDecisions GitHub OAuth app client ID. Rename to `VITE_GITHUB_CLIENT_ID` when ready. |
| `VITE_AUTH_API` | Manual | URL of hodeia.me auth service: `https://api.hodeia.me` (formerly `VITE_RA96IT_API`) |

---

## Railway: `merry-learning` → ShiftCenter Hivenode

**Git repo:** `deiasolutions/shiftcenter`
**Root directory:** (empty — run from repo root)
**Start command:** `uvicorn hivenode.main:app --host 0.0.0.0 --port $PORT`
**Domain:** api.simdecisions.com (keep), api.shiftcenter.com (add when ready)

**JWT Verification Strategy:**
Hivenode verifies JWTs from hodeia.me auth service using public key verification. During the rebrand transition, it must accept JWTs with either issuer:
- `iss: "ra96it"` (legacy)
- `iss: "hodeia"` (current)

Implementation uses the same public key for both issuers. After all clients migrate, remove support for `ra96it` issuer.

### Required — New

| Env Var | Source | Notes |
|---------|--------|-------|
| `HIVENODE_MODE` | Manual | Set to `cloud` |
<<<<<<< Updated upstream
| `HODEIA_PUBLIC_KEY` | From hodeia auth service | RS256 PEM public key. Export from `beneficial-cooperation` service's JWT config. Used to verify hodeia.me JWTs without importing auth service code. |
| `RA96IT_PUBLIC_KEY` | From hodeia auth service (legacy) | **DEPRECATED but still required during transition.** Same public key as `HODEIA_PUBLIC_KEY`. Support for dual-issuer JWT verification (accepts both `ra96it` and `hodeia` issuers). Remove after all clients migrated. |
=======
| `HODEIA_PUBLIC_KEY` | From hodeia service | RS256 PEM public key. Export from `beneficial-cooperation` service's JWT config. Used to verify hodeia JWTs without importing hodeia code. (formerly `RA96IT_PUBLIC_KEY`) |
>>>>>>> Stashed changes
| `FRONTEND_URL` | Manual | CORS origin. Set to `https://simdecisions.com` during transition, then `https://shiftcenter.com`. |

### Required — Carried Over

| Env Var | Source | Notes |
|---------|--------|-------|
| `DATABASE_URL` | Railway auto-inject | PostgreSQL connection string. Injected automatically by Railway from the shared Postgres service. Same DB as before. |
| `ANTHROPIC_API_KEY` | Infisical | Server-side LLM calls. Sync from Infisical, do NOT hardcode. |
| `VOYAGE_API_KEY` | Infisical | Embedding API (Voyage AI). Sync from Infisical. |

### Required — GitHub OAuth

| Env Var | Source | Notes |
|---------|--------|-------|
| `GITHUB_CLIENT_ID` | GitHub OAuth App | Was `SD_GITHUB_CLIENT_ID` on old service. Drop the `SD_` prefix. |
| `GITHUB_CLIENT_SECRET` | GitHub OAuth App | Was `SD_GITHUB_CLIENT_SECRET` on old service. Drop the `SD_` prefix. |

### Optional — Future

| Env Var | Source | Notes |
|---------|--------|-------|
| `OLLAMA_URL` | Railway auto-inject | Internal URL to Ollama service for local LLM inference. Railway provides as `RAILWAY_SERVICE_OLLAMA_URL`. |
| `ENCRYPTION_KEY` | Infisical | For BYOK encrypted key storage (backend). Not needed until BYOK backend integration task. |
| `RESEND_API_KEY` | Infisical | For email notifications. Not needed for MVP. |

### Migration Mapping — Auth Rebrand (ra96it → hodeia.me)

| Old Env Var | New Env Var | Notes |
|-------------|-------------|-------|
| `VITE_RA96IT_API` | `VITE_AUTH_API` | Frontend auth service URL. New value: `https://api.hodeia.me` |
| `RA96IT_PUBLIC_KEY` | `HODEIA_PUBLIC_KEY` | JWT verification public key. **Both keys required during transition** for dual-issuer support. |
| (none) | `VITE_GITHUB_CLIENT_ID` | GitHub OAuth client ID for frontend. Replaces `VITE_SD_GITHUB_CLIENT_ID`. |

### Drop — No Longer Needed

| Old Env Var | Reason |
|-------------|--------|
| `SD_JWT_SECRET` | Replaced by `HODEIA_PUBLIC_KEY` (asymmetric verification). |
<<<<<<< Updated upstream
=======
| `RA96IT_PUBLIC_KEY` | Renamed to `HODEIA_PUBLIC_KEY`. |
| `VITE_RA96IT_API` | Renamed to `VITE_AUTH_API`. |
>>>>>>> Stashed changes
| `SD_FRONTEND_URL` | Replaced by `FRONTEND_URL`. |
| `SD_GITHUB_CLIENT_ID` | Renamed to `GITHUB_CLIENT_ID`. |
| `SD_GITHUB_CLIENT_SECRET` | Renamed to `GITHUB_CLIENT_SECRET`. |
| `VITE_SD_GITHUB_CLIENT_ID` | Renamed to `VITE_GITHUB_CLIENT_ID`. |
| `VITE_RA96IT_API` | Renamed to `VITE_AUTH_API`. |
| `SD_ADMIN_GITHUB_LOGINS` | Move to hivenode config or keep if needed. |
| `OAUTH_CALLBACK_URL` | Will be reconfigured to new service URL. |
| `GITHUB_TOKEN` | Old GitHub API token. Replace if needed. |

---

## Auth Rebrand Migration: ra96it → hodeia

### Environment Variable Migration Mapping

| Old Name | New Name | Notes |
|----------|----------|-------|
| `VITE_RA96IT_API` | `VITE_AUTH_API` | Frontend: URL of auth service (now `https://api.hodeia.me`) |
| `RA96IT_PUBLIC_KEY` | `HODEIA_PUBLIC_KEY` | Backend: RS256 public key for JWT verification |

### Dual-Issuer JWT Strategy (Transition Period)

During the transition from ra96it to hodeia branding, hivenode MUST accept JWTs from **both** issuers:

- **Old issuer:** `https://api.ra96it.com`
- **New issuer:** `https://api.hodeia.me`

**Implementation:**

1. Backend (`hivenode/auth/jwt.py`) checks `iss` claim in incoming JWT
2. If `iss == "https://api.ra96it.com"` → verify with `HODEIA_PUBLIC_KEY` (same key, old domain)
3. If `iss == "https://api.hodeia.me"` → verify with `HODEIA_PUBLIC_KEY` (same key, new domain)
4. Both issuers use the same RS256 key pair during transition
5. Frontend (`browser/`) only requests tokens from new issuer (`https://api.hodeia.me`)
6. Old tokens (ra96it issuer) remain valid until expiry (typically 24 hours)

**Cutover:**

- After 48 hours with zero ra96it-issuer tokens observed in logs, remove ra96it issuer from accepted list
- Auth service (`beneficial-cooperation`) updated to issue only `https://api.hodeia.me` tokens

### URL Migration

All references to `api.ra96it.com` updated to `api.hodeia.me`:

- Frontend env var: `VITE_AUTH_API=https://api.hodeia.me`
- Frontend localStorage key prefix: `hodeia_` (migrated from `ra96it_` via SPEC-AUTH-B)
- Backend public key source: `beneficial-cooperation` Railway service (domain unchanged in Railway config, but issues hodeia-branded JWTs)

---

## Services That Stay on Old Repo

### Railway: `beneficial-cooperation` (hodeia.me auth)

**Git repo:** `deiasolutions/platform` (no change)
**Domain:** api.hodeia.me (formerly api.ra96it.com)
**Notes:** Independent auth service. Issues JWTs that hivenode verifies via public key.

**Dual-Issuer JWT Strategy (Transition Period):**
During the rebrand transition, this service accepts both old and new JWT issuers:
- `iss: "ra96it"` — legacy tokens from old clients
- `iss: "hodeia"` — new tokens from updated clients

Hivenode must verify both issuers during this period. Once all clients migrate to `hodeia` issuer, the `ra96it` issuer support can be removed. Both issuers use the same RS256 public key.

### Railway: `Ollama`

**Git repo:** `deiasolutions/platform` (no change)
**Domain:** ollama-production-3568.up.railway.app (no change)
**Notes:** Self-contained LLM inference service. Hivenode calls it via `OLLAMA_URL` for sensitive prompts routed by the sensitivity gate.

### Railway: `platform` (Efemera)

**Git repo:** `deiasolutions/platform` (no change)
**Domain:** api.efemera.live (no change)
**Notes:** Separate product. Shares PostgreSQL but independent codebase.

### Railway: `github-mcp-server`

**Git repo:** `deiasolutions/platform` (no change)
**Domain:** github-mcp.simdecisions.com (no change)
**Notes:** GitHub MCP proxy. May repoint to shiftcenter in a future task.

### Railway: `Postgres`

**No change.** Shared by all services. Connection string auto-injected by Railway.

---

## Domain Strategy

### Dev Branch: `dev.shiftcenter.com`

Single domain serves the `dev` branch. EGG selected via `?egg=name` query param (default: `code`).

- **DNS:** Cloudflare CNAME `dev.shiftcenter.com` → Vercel
- **Vercel branch:** `dev`
- **URL examples:**
  - `dev.shiftcenter.com` → code EGG (default)
  - `dev.shiftcenter.com?egg=chat` → chat EGG
  - `dev.shiftcenter.com?egg=centerstage` → broadcast EGG
- **API:** Points to same Railway hivenode (or a dev Railway environment if needed later)

### Production: `main` branch — one subdomain per product

Each product gets its own subdomain on the `main` branch. Domains unchanged during transition:

| Product | Domain | EGG |
|---------|--------|-----|
| SimDecisions (chat) | simdecisions.com | `chat` |
| (future products) | *.shiftcenter.com | per-product EGG |

Production domains are NOT consolidated into a single `?egg=` param — each product has its own branded entry point.

---

## Repoint Procedure (When Ready)

### Vercel
1. Dashboard → `simdecisions-2` → Settings → Git
2. Disconnect `deiasolutions/platform`
3. Connect `deiasolutions/shiftcenter`
4. Set Root Directory: `browser/`
5. Verify env vars (above)
6. Trigger redeploy

### Railway
1. Dashboard → `merry-learning` → Settings → Source
2. Disconnect current repo
3. Connect `deiasolutions/shiftcenter`
4. Set Root Directory: (empty)
5. Set Start Command: `uvicorn hivenode.main:app --host 0.0.0.0 --port $PORT`
<<<<<<< Updated upstream
6. Add new env vars:
   - `HIVENODE_MODE=cloud`
   - `HODEIA_PUBLIC_KEY` (from hodeia auth service)
   - `RA96IT_PUBLIC_KEY` (same value as HODEIA_PUBLIC_KEY during transition)
   - `FRONTEND_URL=https://simdecisions.com` (update to shiftcenter.com when ready)
7. Rename:
   - `SD_GITHUB_CLIENT_ID` → `GITHUB_CLIENT_ID`
   - `SD_GITHUB_CLIENT_SECRET` → `GITHUB_CLIENT_SECRET`
8. Drop:
   - `SD_JWT_SECRET`
   - `SD_FRONTEND_URL`
   - `VITE_RA96IT_API` (frontend only, not needed in hivenode)
=======
6. Add new env vars: `HIVENODE_MODE`, `HODEIA_PUBLIC_KEY`, `FRONTEND_URL`
7. Rename: `SD_GITHUB_CLIENT_ID` → `GITHUB_CLIENT_ID`, `SD_GITHUB_CLIENT_SECRET` → `GITHUB_CLIENT_SECRET`
8. Drop: `SD_JWT_SECRET`, `SD_FRONTEND_URL`, `RA96IT_PUBLIC_KEY`, `VITE_RA96IT_API`
>>>>>>> Stashed changes
9. Verify deployment

---

## Auth Rebrand Migration Checklist

### Phase 1: Dual-Issuer Support (CURRENT)

**Frontend (Vercel):**
- [x] Add `VITE_AUTH_API=https://api.hodeia.me`
- [x] Keep `VITE_RA96IT_API` for backwards compatibility (if needed)
- [x] Update code to use `VITE_AUTH_API` as primary
- [x] Update localStorage key from `ra96it_*` to `hodeia_*` with migration

**Backend (Railway):**
- [x] Add `HODEIA_PUBLIC_KEY` env var
- [x] Keep `RA96IT_PUBLIC_KEY` env var (same value)
- [x] Update JWT verification to accept both issuers (`ra96it` and `hodeia`)
- [x] Keep dual-issuer support for transition period

**Auth Service (beneficial-cooperation):**
- [x] Update domain from api.ra96it.com to api.hodeia.me
- [x] Issue JWTs with `iss: "hodeia"`
- [x] Maintain backwards compatibility for `iss: "ra96it"` during transition

### Phase 2: Deprecate Legacy (FUTURE)

**After all clients confirm migration:**
- [ ] Remove `VITE_RA96IT_API` from frontend env vars
- [ ] Remove `RA96IT_PUBLIC_KEY` from backend env vars
- [ ] Remove `iss: "ra96it"` support from JWT verification
- [ ] Update all localStorage references to use `hodeia_*` exclusively
- [ ] Remove dual-issuer verification code from hivenode

### URL Updates

| Service | Old URL | New URL | Status |
|---------|---------|---------|--------|
| Auth API | api.ra96it.com | api.hodeia.me | ✅ Migrated |
| Frontend | simdecisions.com | (unchanged) | Production domain |
| Hivenode | api.simdecisions.com | (unchanged) | Production domain |

### localStorage Migration

Frontend code must migrate existing keys on load:

| Old Key | New Key | Migration Strategy |
|---------|---------|-------------------|
| `ra96it_token` | `hodeia_token` | Copy value, keep both during transition |
| `ra96it_user` | `hodeia_user` | Copy value, keep both during transition |
| `ra96it_refresh` | `hodeia_refresh` | Copy value, keep both during transition |

After migration period: remove all `ra96it_*` keys from localStorage.
