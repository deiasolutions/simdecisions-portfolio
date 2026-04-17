# Wave 3 Queue Specs — Deploy + Harden

Drop these in .deia/hive/queue/ after Wave 2 completes. Each section is one spec file.

---

## FILE: 2026-03-16-3000-SPEC-vercel-railway-repoint.md

# SPEC: Repoint Vercel + Railway to ShiftCenter Repo

## Priority
P0

## Objective
Repoint existing Vercel project to shiftcenter/browser/ and Railway service to shiftcenter/hivenode/. Set up dev.shiftcenter.com as dev branch preview.

## Context
Files to read first:
- `docs/DEPLOYMENT-WIRING-NOTES.md`
- `.deia/config/deployment-env.md`
- `browser/vite.config.ts`
- `hivenode/main.py`
- `pyproject.toml`

Old deploy: Vercel from simdecisions-2/, Railway from simdecisions-2/api/
New deploy: Vercel from browser/, Railway from hivenode/

## Acceptance Criteria
- [ ] Vercel project linked to deiasolutions/shiftcenter, root dir browser/
- [ ] Production branch: main. Preview: dev + PR branches.
- [ ] vercel.json in browser/ with SPA fallback rewrites
- [ ] Railway service linked to deiasolutions/shiftcenter, root dir hivenode/
- [ ] Start command: uvicorn hivenode.main:app --host 0.0.0.0 --port $PORT
- [ ] Env vars set per .deia/config/deployment-env.md
- [ ] Health check: GET /health returns 200
- [ ] Do NOT delete old Vercel/Railway projects
- [ ] Do NOT change production DNS yet

## Smoke Test
- [ ] Push to dev → Vercel builds
- [ ] Push to dev → Railway builds
- [ ] Staging URL loads chat app in browser
- [ ] Staging API /health returns 200

## Model Assignment
sonnet

---

## FILE: 2026-03-16-3001-SPEC-dev-shiftcenter-dns.md

# SPEC: dev.shiftcenter.com DNS

## Priority
P0

## Objective
Add dev.shiftcenter.com CNAME in Cloudflare pointing to Vercel preview deployment. Verify api staging URL.

## Context
Cloudflare manages DNS for shiftcenter.com. Vercel assigns preview URLs automatically. We need a custom domain for the dev branch.

## Acceptance Criteria
- [ ] dev.shiftcenter.com CNAME → Vercel (cname.vercel-dns.com or similar)
- [ ] Vercel custom domain dev.shiftcenter.com assigned to dev branch
- [ ] SSL works (Cloudflare flex or full)
- [ ] api.shiftcenter.com CNAME verified or updated for Railway
- [ ] Both resolve and load correctly

## Smoke Test
- [ ] https://dev.shiftcenter.com loads the chat app
- [ ] https://api.shiftcenter.com/health returns 200 (or staging equivalent)

## Model Assignment
haiku

## Constraints
This may require manual Cloudflare + Vercel dashboard work. If the bee can't access these services via CLI, document the exact steps for Dave to execute manually.

---

## FILE: 2026-03-16-3002-SPEC-subdomain-egg-routing.md

# SPEC: Subdomain → EGG Routing

## Priority
P0

## Objective
Add hostname → EGG mapping so different subdomains load different products from the same deploy.

## Context
Files to read first:
- `browser/src/App.tsx` or `browser/src/main.tsx`
- `browser/src/shell/useEggInit.ts`
- `eggs/` directory for available EGGs

## Acceptance Criteria
- [ ] Mapping in App.tsx or useEggInit.ts:
  - chat.efemera.live → chat.egg.md
  - code.shiftcenter.com → code.egg.md (when it exists, fallback to chat)
  - pm.shiftcenter.com → pm.egg.md (when it exists, fallback to chat)
  - canvas.shiftcenter.com → canvas.egg.md
  - dev.shiftcenter.com → chat.egg.md (default)
  - localhost:5173 → chat.egg.md (dev default)
- [ ] ?egg=name query param overrides hostname mapping
- [ ] Unknown hostname falls back to chat.egg.md
- [ ] 5+ tests

## Smoke Test
- [ ] dev.shiftcenter.com loads chat app
- [ ] dev.shiftcenter.com?egg=canvas loads canvas app
- [ ] localhost:5173?egg=monitor loads build monitor

## Model Assignment
haiku

---

## FILE: 2026-03-16-3003-SPEC-rate-limiting.md

# SPEC: Rate Limiting on Auth Routes

## Priority
P0

## Objective
Add sliding window rate limiting middleware to all /auth/ routes. Prevent brute force attacks.

## Context
Files to read first:
- `hivenode/routes/auth.py`
- `hivenode/dependencies.py`
- `hivenode/main.py` (middleware setup)

## Acceptance Criteria
- [ ] Sliding window rate limiter: 10 requests per minute per IP on all /auth/ routes
- [ ] Rate limit headers in response: X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset
- [ ] 429 Too Many Requests response when limit exceeded, with Retry-After header
- [ ] In-memory storage (dict with TTL cleanup) — no Redis dependency
- [ ] Configurable via environment variable: RATE_LIMIT_AUTH (default 10)
- [ ] Does NOT apply to non-auth routes (other hivenode routes unaffected)
- [ ] 5+ tests: under limit passes, at limit passes, over limit returns 429, different IPs have separate limits, reset after window

## Smoke Test
- [ ] Hit /auth/verify 11 times in 60 seconds → 11th returns 429

## Model Assignment
haiku

---

## FILE: 2026-03-16-3004-SPEC-cost-storage-rate-lookup.md

# SPEC: Cost Storage Format + Model Rate Lookup Table

## Priority
P1

## Objective
Define how three currencies (CLOCK, COIN, CARBON) are stored per operation, and add a model rate lookup table so COIN can be computed from token counts.

## Context
Files to read first:
- `docs/specs/SPEC-COST-STORAGE-RATE-LOOKUP.docx` (existing spec)
- `hivenode/ledger/writer.py` (Event Ledger)
- `hivenode/ledger/schemas.py` (event schemas)

## Acceptance Criteria
- [ ] Cost stored as three fields on every Event Ledger entry: clock_ms (int), coin_usd (float, stored as scientific notation e.g. 3.0e-4), carbon_grams (float)
- [ ] Model rate lookup table in hivenode/config/model_rates.yml:
  ```yaml
  rates:
    claude-opus-4-6: { input_per_million: 15.00, output_per_million: 75.00 }
    claude-sonnet-4-6: { input_per_million: 3.00, output_per_million: 15.00 }
    claude-haiku-4-5: { input_per_million: 0.80, output_per_million: 4.00 }
    gpt-4o: { input_per_million: 2.50, output_per_million: 10.00 }
  ```
- [ ] compute_coin(model, input_tokens, output_tokens) → float USD
- [ ] compute_carbon(model, input_tokens, output_tokens) → float grams (estimate based on published data center PUE)
- [ ] LLM Router auto-attaches cost to every Event Ledger entry after an LLM call
- [ ] Build monitor shows cumulative cost from these real values (not hardcoded $0.00)
- [ ] 8+ tests

## Smoke Test
- [ ] Send a chat message → Event Ledger entry has non-zero coin_usd and carbon_grams
- [ ] Build monitor header shows real cost for bee dispatches

## Model Assignment
sonnet

---

## FILE: 2026-03-16-3005-SPEC-cloud-adapter-e2e.md

# SPEC: Cloud Storage Adapter End-to-End on Railway

## Priority
P0

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
- [ ] From browser: save a chat → cloud hivenode writes file → refresh page → chat loads from cloud

## Model Assignment
sonnet

## Constraints
This requires the Railway deployment from SPEC-3000 to be live. If Railway isn't deployed yet, write the tests against a local hivenode in cloud mode with a temp directory simulating the Railway volume.

---

## FILE: 2026-03-16-3006-SPEC-volume-sync-e2e.md

# SPEC: Volume Sync home:// ↔ cloud:// End-to-End

## Priority
P0

## Objective
Verify bidirectional sync between local hivenode (home://) and cloud hivenode (cloud://) works.

## Context
Files to read first:
- SPEC-HIVENODE-E2E-001.md Section 6 (Volume Sync)
- `hivenode/storage/sync/` (if it exists from overnight build)
- `hivenode/storage/adapters/`

## Acceptance Criteria
- [ ] On file write to home://, change queued for push to cloud://
- [ ] On file write to cloud://, change queued for push to home:// on next connect
- [ ] Periodic sync every 5 minutes (configurable)
- [ ] Manual sync via 8os sync CLI command
- [ ] On hivenode startup, pull changes from cloud since last sync
- [ ] Conflict resolution: last-write-wins, both versions preserved (.conflict file)
- [ ] sync_log.db tracks all sync operations
- [ ] Event Ledger logs SYNC_STARTED, SYNC_COMPLETED, SYNC_CONFLICT events
- [ ] Offline queue: writes to offline volume queued, flushed on reconnect
- [ ] 10+ tests including conflict scenarios

## Smoke Test
- [ ] Write file on local hivenode → appears on cloud after sync
- [ ] Write file on cloud → appears on local after sync
- [ ] Write same file on both before sync → conflict file created, latest wins

## Model Assignment
sonnet

---

## FILE: 2026-03-16-3007-SPEC-smoke-test-suite.md

# SPEC: Automated Smoke Test Suite for Deployed URLs

## Priority
P1

## Objective
Playwright test suite that verifies the deployed app works after every push. Runs as part of the build queue's deploy verification step.

## Context
Files to read first:
- `browser/playwright.config.ts` (if exists)
- `tests/e2e/` (existing Playwright tests from TASK-015)

## Acceptance Criteria
- [ ] Playwright config points to dev.shiftcenter.com (configurable via env var)
- [ ] Test: homepage loads, contains #root div
- [ ] Test: API /health returns 200
- [ ] Test: chat.egg.md renders 3 panes (tree-browser, text-pane, terminal)
- [ ] Test: canvas.egg.md renders 5 panes (via ?egg=canvas)
- [ ] Test: monitor.egg.md renders build monitor (via ?egg=monitor)
- [ ] Test: type message in terminal → response appears in text-pane
- [ ] Test: page load time < 3 seconds
- [ ] Test: no console errors
- [ ] Screenshot saved per test to .deia/hive/smoke/
- [ ] 8+ tests total

## Smoke Test
- [ ] Run: npx playwright test --config=tests/e2e/playwright.config.ts
- [ ] All tests pass against dev.shiftcenter.com (or localhost:5173 for local verification)

## Model Assignment
sonnet

---

## FILE: 2026-03-16-3008-SPEC-https-cors.md

# SPEC: HTTPS + CORS Configuration

## Priority
P0

## Objective
Ensure browser can talk to API without CORS errors. Verify HTTPS works on all deployed URLs.

## Context
Files to read first:
- `hivenode/main.py` (CORSMiddleware setup)
- `browser/vite.config.ts` (proxy settings for dev)

## Acceptance Criteria
- [ ] CORSMiddleware allows: dev.shiftcenter.com, chat.efemera.live, code.shiftcenter.com, localhost:5173
- [ ] Wildcard NOT used in production (security)
- [ ] Allowed methods: GET, POST, DELETE, OPTIONS
- [ ] Allowed headers: Authorization, Content-Type
- [ ] Credentials: true (for JWT cookies if used)
- [ ] CORS origins configurable via ALLOWED_ORIGINS env var (comma-separated)
- [ ] HTTPS verified on all custom domains (Cloudflare handles SSL)
- [ ] 3+ tests: allowed origin passes, disallowed origin blocked, preflight OPTIONS works

## Smoke Test
- [ ] Browser at dev.shiftcenter.com can call API at api.shiftcenter.com without CORS error

## Model Assignment
haiku

---

## FILE: 2026-03-16-3009-SPEC-error-handling-ux.md

# SPEC: User-Facing Error Handling

## Priority
P1

## Objective
Users see helpful error messages, not stack traces or blank screens. Every failure state has a UI.

## Context
Files to read first:
- `browser/src/shell/components/PaneContent.tsx`
- `browser/src/shell/components/AppletShell.tsx`
- `browser/src/primitives/terminal/`

## Acceptance Criteria
- [ ] Applet load failure: pane shows "Failed to load [applet name]. Try refreshing." with retry button
- [ ] API unreachable: terminal shows "Cannot reach server. Check your connection." (not a stack trace)
- [ ] LLM error (bad API key, rate limit, model down): terminal shows human-readable message with suggestion ("Check your API key in Settings")
- [ ] 500 error from hivenode: user sees "Something went wrong. Error logged." (not the raw JSON error)
- [ ] Network timeout: terminal shows "Request timed out. Try again."
- [ ] React error boundary wraps every pane — one crashing pane doesn't take down the whole app
- [ ] All error messages use var(--sd-*) colors (red accent for errors, yellow for warnings)
- [ ] 5+ tests

## Smoke Test
- [ ] Remove API key → send message → terminal shows "No API key configured" with link to settings
- [ ] Kill hivenode → send message → terminal shows connection error, not crash

## Model Assignment
haiku
