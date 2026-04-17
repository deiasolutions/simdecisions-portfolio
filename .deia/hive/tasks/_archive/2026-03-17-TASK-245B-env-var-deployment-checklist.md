# TASK-245B: Document Environment Variable Deployment Checklist

**Parent:** TASK-245 (ra96it Sign-Up Flow Verified)
**Wave:** 5 (Ship)
**Model:** haiku
**Est:** 15 minutes

---

## Objective

Create a deployment checklist that documents all required environment variables for the ra96it sign-up flow to work in local and production environments. This checklist will be used by Q88N to verify deployment config before going live.

---

## Context

The ra96it sign-up flow depends on multiple environment variables:
- Frontend: `VITE_RA96IT_API` (points to ra96it backend)
- Backend: GitHub OAuth credentials, JWT keys, CORS origins, etc.

These are already configured in code (`ra96it/config.py`) but not documented in a single place. Before production deploy, we need a checklist to verify all vars are set correctly.

---

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\ra96it\config.py` — Settings class with all env vars
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\ra96it\routes\oauth.py` — OAuth routes (uses GitHub OAuth vars)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\auth\LoginPage.tsx` — Uses `VITE_RA96IT_API`
- Flow trace: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260317-TASK-245-FLOW-TRACE.md` (env var section)

---

## Deliverables

- [ ] Create new file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\DEPLOYMENT-CHECKLIST-RA96IT.md`
- [ ] Document all required environment variables for ra96it sign-up flow
- [ ] For each variable, specify:
  - Name
  - Description
  - Required? (yes/no)
  - Local value (example)
  - Production value (example or instruction)
  - How to test if set correctly
- [ ] Add checklist section: pre-deploy verification steps
- [ ] Add troubleshooting section: common errors and fixes

---

## Test Requirements

N/A — This is a documentation task. No tests required.

---

## Constraints

- No file over 500 lines
- Markdown format
- Clear, concise language
- Use tables for environment variable list
- Include code examples for testing

---

## Acceptance Criteria

- [ ] New file created: `docs/DEPLOYMENT-CHECKLIST-RA96IT.md`
- [ ] All environment variables documented (minimum 12 vars: see list below)
- [ ] Local vs production values specified
- [ ] Test commands provided for each var
- [ ] Pre-deploy checklist included (5+ steps)
- [ ] Troubleshooting section included (3+ common errors)

---

## Environment Variables to Document

### Frontend (Vite)
1. `VITE_RA96IT_API` — ra96it backend URL

### Backend (FastAPI / Railway)
2. `GITHUB_CLIENT_ID` — GitHub OAuth app client ID
3. `GITHUB_CLIENT_SECRET` — GitHub OAuth app client secret
4. `GITHUB_REDIRECT_URI` — OAuth callback URL
5. `ALLOWED_ORIGINS` — Comma-separated list of allowed frontend origins
6. `FRONTEND_URL` — Default frontend URL for redirects
7. `JWT_PRIVATE_KEY` — RS256 private key (PEM format)
8. `JWT_PUBLIC_KEY` — RS256 public key (PEM format)
9. `JWT_ISSUER` — JWT issuer claim
10. `JWT_AUDIENCE` — JWT audience claim
11. `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` — Token expiry in minutes
12. `DATABASE_URL` — PostgreSQL connection string (for user storage)

**Optional:**
13. `ADMIN_GITHUB_LOGINS` — Comma-separated list of GitHub usernames to auto-elevate to admin
14. `DEV_LOGIN_ENABLED` — Enable dev-login endpoint (local only)

---

## Test Commands to Include

For each variable, provide a test command. Examples:

**Frontend:**
```bash
# Verify VITE_RA96IT_API is set correctly
cd browser
echo $VITE_RA96IT_API  # Should print: (empty) for local, https://ra96it.com for production
```

**Backend:**
```bash
# Verify GitHub OAuth credentials
curl http://localhost:8001/auth/github/login?origin=http://localhost:5173
# Should return: {"url": "https://github.com/login/oauth/authorize?..."}
# If not configured: {"detail": "GitHub OAuth not configured"}

# Verify JWKS endpoint
curl http://localhost:8001/.well-known/jwks.json
# Should return: {"keys": [{"kty": "RSA", "kid": "...", ...}]}

# Verify ALLOWED_ORIGINS includes frontend URL
# Try to trigger CORS error with unauthorized origin — should fail
curl -X OPTIONS http://localhost:8001/auth/github/login \
  -H "Origin: https://evil.com" \
  -H "Access-Control-Request-Method: GET"
# Should NOT have Access-Control-Allow-Origin header for evil.com
```

---

## Pre-Deploy Checklist to Include

- [ ] All environment variables set in Railway dashboard
- [ ] `GITHUB_CLIENT_ID` and `GITHUB_CLIENT_SECRET` match GitHub OAuth app
- [ ] `GITHUB_REDIRECT_URI` matches Railway deployment URL (e.g., `https://ra96it.up.railway.app/auth/github/callback`)
- [ ] `ALLOWED_ORIGINS` includes production frontend URL (e.g., `https://shiftcenter.com`)
- [ ] `FRONTEND_URL` set to production frontend (e.g., `https://shiftcenter.com`)
- [ ] JWT keys generated (RS256, 2048-bit) and stored securely
- [ ] Test OAuth flow in production: visit frontend → click GitHub → callback works
- [ ] Verify JWT issued has correct claims (sub, email, scope, exp, iss, aud)
- [ ] Verify token stored in localStorage after successful login
- [ ] Verify `isAuthenticated()` returns true after login

---

## Troubleshooting Section to Include

### Error: "GitHub OAuth not configured"
**Cause:** `GITHUB_CLIENT_ID` or `GITHUB_CLIENT_SECRET` not set.
**Fix:** Set both environment variables in Railway dashboard. Restart service.

### Error: "Unauthorized origin"
**Cause:** Frontend origin not in `ALLOWED_ORIGINS` list.
**Fix:** Add frontend URL to `ALLOWED_ORIGINS` (comma-separated, no spaces). Example: `http://localhost:5173,https://shiftcenter.com`

### Error: Token not stored in localStorage
**Cause:** CORS error, or `?token=` not in callback URL.
**Fix:**
1. Check browser console for CORS errors. Verify `ALLOWED_ORIGINS` includes frontend URL.
2. Check callback URL — should be `${FRONTEND_URL}?token=<jwt>`. Verify `FRONTEND_URL` is set.

### Error: "Invalid signature" when decoding JWT
**Cause:** `JWT_PRIVATE_KEY` and `JWT_PUBLIC_KEY` mismatch, or wrong algorithm.
**Fix:** Regenerate RS256 key pair. Verify keys are in PEM format. Ensure both keys from same pair.

---

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260317-TASK-245B-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — N/A (documentation task)
5. **Build Verification** — N/A (documentation task)
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.

---

## Example Document Structure

```markdown
# ra96it Deployment Checklist

## Overview
This checklist verifies all environment variables for the ra96it sign-up flow are configured correctly before production deploy.

## Environment Variables

### Frontend (Vite)
| Variable | Description | Required | Local Value | Production Value | Test Command |
|----------|-------------|----------|-------------|------------------|--------------|
| `VITE_RA96IT_API` | ra96it backend URL | No | (empty string) | `https://ra96it.com` | `echo $VITE_RA96IT_API` |

### Backend (FastAPI / Railway)
| Variable | Description | Required | Local Value | Production Value | Test Command |
|----------|-------------|----------|-------------|------------------|--------------|
| `GITHUB_CLIENT_ID` | GitHub OAuth app client ID | Yes | `abc123` | (from GitHub OAuth app) | `curl .../auth/github/login` |
| `GITHUB_CLIENT_SECRET` | GitHub OAuth app client secret | Yes | `secret123` | (from GitHub OAuth app) | (verify callback works) |
| ... | ... | ... | ... | ... | ... |

## Pre-Deploy Checklist
- [ ] Step 1
- [ ] Step 2
...

## Troubleshooting
### Error: "..."
**Cause:** ...
**Fix:** ...
```

---

## References

- ra96it config: `ra96it/config.py`
- Flow trace: `.deia/hive/responses/20260317-TASK-245-FLOW-TRACE.md`
- BOOT.md: 10 hard rules (no hardcoded values in docs)
