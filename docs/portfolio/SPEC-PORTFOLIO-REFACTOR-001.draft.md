# SPEC-PORTFOLIO-REFACTOR-001: Portfolio Refactoring Recommendations

## Priority
P2 — Optional improvements, defer until interview stage

## Model
sonnet

## Depends On
SPEC-PORTFOLIO-NUGGET-HUNT-001 (complete)

## Objective

Address structural and cosmetic refactoring opportunities identified during portfolio nugget hunt. These improvements strengthen 1000bulbs JD signal alignment by demonstrating architectural discipline and ability to evolve legacy code. Grouped into dispatchable units (≤4 hrs each).

**Note:** This is NOT required before job application. Use this spec if/when interview is scheduled and you want to polish the private repos before granting access.

---

## Sandbox Strategy

**CRITICAL:** The live `simdecisions/` repo is actively being used as a portfolio demonstration piece for a job interview. All refactoring MUST happen in an isolated sandbox directory to avoid disrupting the live codebase.

**Setup step (run FIRST, before any refactoring):**
```bash
cd C:\Users\davee\OneDrive\Documents\GitHub\simdecisions
mkdir simdecisions-refactor
# Copy only the source trees being modified (not .git, not .deia, not node_modules)
cp -r hivenode simdecisions-refactor/hivenode
cp -r browser/src simdecisions-refactor/browser-src
cp -r tests simdecisions-refactor/tests
cp vercel.json simdecisions-refactor/vercel.json
cp docs/DEPLOYMENT.md simdecisions-refactor/DEPLOYMENT.md
```

**All file modifications in this spec target `simdecisions-refactor/`** — never the live repo root. After Q88N reviews and approves, the refactored files replace their live counterparts manually.

**Paths in this spec use the prefix:**
`C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\simdecisions-refactor\`

---

## Context

Portfolio nugget hunt (SPEC-PORTFOLIO-NUGGET-HUNT-001) identified 6 refactor opportunities across platform architecture and AI correction infrastructure. All map to JD criteria 1-2 (multi-tier architecture, clean separation, config management, API design).

**Severity breakdown:**
- **Blockers:** 0 (nothing prevents deployment)
- **Structural:** 4 (architectural improvements)
- **Cosmetic:** 2 (naming conventions, readability)

**Total estimated effort:** 21 hours (grouped into 6 work units of 1-8 hours each)

---

## Refactor Opportunities Summary

### RO-1: Lifespan Manager Decomposition (Structural, 8 hrs)
**File:** `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\simdecisions-refactor\hivenode\main.py`
**Issue:** 640-line lifespan manager violates single responsibility (orchestrates 15+ subsystems)
**JD Relevance:** Criterion 1 (demonstrates ability to refactor monolithic initialization)
**Current state:** All subsystems initialized in one function (ledger, storage, sync, RAG, relay, scheduler, wiki, inventory, shell, build monitor, LLM router, etc.)
**Recommendation:** Extract subsystem initialization into composable modules with dependency injection

### RO-2: Mode-Based Config Separation (Structural, 3 hrs)
**File:** `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\simdecisions-refactor\hivenode\config.py`
**Issue:** Mode-specific defaults in `_set_defaults()` mix config with business logic
**JD Relevance:** Criterion 1 (12-factor principle: config separation)
**Current state:** Python function sets defaults based on `HIVENODE_MODE` env var
**Recommendation:** Move mode defaults to YAML config files (config/local.yml, config/cloud.yml), load via pydantic-settings ConfigDict

### RO-3: CI/CD Pipeline Documentation (Structural, 4 hrs)
**File:** `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\simdecisions-refactor\DEPLOYMENT.md`
**Issue:** No CI/CD pipeline documentation (manual build verification steps)
**JD Relevance:** Criterion 3 (DevOps maturity)
**Current state:** Deployment doc covers Railway/Vercel manual deploy, health checks, env vars
**Recommendation:** Add GitHub Actions workflows for automated build verification, Railway deploy-on-merge, Vercel preview deployments

### RO-4: Vercel Routing Config (Cosmetic, 1 hr)
**File:** `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\simdecisions-refactor\vercel.json`
**Issue:** Hardcoded Railway service URLs in routing config (no env var substitution)
**JD Relevance:** Criterion 1 (12-factor config)
**Current state:** `"destination": "https://hivenode-production.up.railway.app/:path*"`
**Recommendation:** Switch to Vercel env vars + rewrites.source pattern for dynamic service URLs

### RO-5: Volume Naming Rules (Cosmetic, 2 hrs)
**File:** `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\simdecisions-refactor\hivenode\storage\registry.py`
**Issue:** Volume naming rules enforced via string length check (system ≤7, user ≥8) — fragile
**JD Relevance:** Criterion 2 (API design)
**Current state:** `if len(name) <= 7: type = "system" else: type = "user"`
**Recommendation:** Replace length-based distinction with explicit volume type enum (SystemVolume vs UserVolume)

### RO-6: OAuth Token Interceptor Lifecycle (Structural, 3 hrs)
**File:** `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\simdecisions-refactor\browser-src\App.tsx`
**Issue:** OAuth token interceptor runs on module load (side effect before React renders)
**JD Relevance:** Criterion 2 (frontend architecture)
**Current state:** Token extraction logic runs at top-level of module
**Recommendation:** Move token extraction into React hook (useOAuthRedirect) with proper lifecycle management

---

## Work Units (Dispatchable)

### Unit 1: Lifespan Manager Decomposition (RO-1)
**Effort:** 8 hours
**Severity:** Structural
**Priority:** P2

**Files to modify:**
- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\simdecisions-refactor\hivenode\main.py` (reduce from 640 to <300 lines)
- Create: `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\simdecisions-refactor\hivenode\init\ledger.py`
- Create: `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\simdecisions-refactor\hivenode\init\storage.py`
- Create: `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\simdecisions-refactor\hivenode\init\sync.py`
- Create: `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\simdecisions-refactor\hivenode\init\rag.py`
- Create: `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\simdecisions-refactor\hivenode\init\relay.py`
- Create: `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\simdecisions-refactor\hivenode\init\scheduler.py`
- Create: `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\simdecisions-refactor\hivenode\init\__init__.py`

**Changes:**
1. Extract ledger initialization logic into `init/ledger.py`:
   ```python
   # hivenode/init/ledger.py
   from hivenode.ledger import EventLedger

   async def init_ledger(cfg):
       """Initialize event ledger with config-based writer."""
       writer = await setup_ledger_writer(cfg.ledger_mode)
       return EventLedger(writer=writer)
   ```

2. Extract storage initialization into `init/storage.py`:
   ```python
   # hivenode/init/storage.py
   from hivenode.storage import VolumeRegistry

   async def init_storage(cfg):
       """Initialize volume registry with adapters."""
       registry = VolumeRegistry()
       await registry.mount_volumes(cfg.volumes)
       return registry
   ```

3. Refactor `main.py` lifespan to call init modules:
   ```python
   # hivenode/main.py
   from hivenode.init import (
       init_ledger, init_storage, init_sync,
       init_rag, init_relay, init_scheduler
   )

   @asynccontextmanager
   async def lifespan(app: FastAPI):
       cfg = get_config()

       # Initialize subsystems via composable modules
       app.state.ledger = await init_ledger(cfg)
       app.state.storage = await init_storage(cfg)
       app.state.sync_engine = await init_sync(cfg)
       app.state.rag = await init_rag(cfg)
       app.state.relay = await init_relay(cfg)
       app.state.scheduler = await init_scheduler(cfg)

       yield

       # Cleanup
       await shutdown_all(app.state)
   ```

**Tests to create:**
- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\simdecisions-refactor\tests\hivenode\init\test_ledger_init.py` (verify ledger initialization with mock config)
- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\simdecisions-refactor\tests\hivenode\init\test_storage_init.py` (verify volume mounting)
- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\simdecisions-refactor\tests\hivenode\init\test_integration.py` (verify all inits compose correctly)

**Acceptance Criteria:**
- [ ] `hivenode/main.py` reduced to <300 lines
- [ ] 7 init modules created in `hivenode/init/`
- [ ] Each init module has single responsibility (one subsystem)
- [ ] All existing routes and subsystems work unchanged
- [ ] 12+ tests added for init modules
- [ ] No regression in health check endpoint

**JD Signal Strengthened:** Criterion 1 (demonstrates refactoring monolithic code into composable modules with dependency injection)

---

### Unit 2: Mode-Based Config Separation (RO-2)
**Effort:** 3 hours
**Severity:** Structural
**Priority:** P2

**Files to modify:**
- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\simdecisions-refactor\hivenode\config.py` (remove `_set_defaults()` function)
- Create: `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\simdecisions-refactor\hivenode\config\local.yml`
- Create: `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\simdecisions-refactor\hivenode\config\cloud.yml`
- Create: `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\simdecisions-refactor\hivenode\config\remote.yml`

**Changes:**
1. Create YAML config files for each mode:
   ```yaml
   # hivenode/config/local.yml
   ledger_mode: file
   storage_mode: local
   sync_enabled: false
   rag_enabled: true
   scheduler_enabled: true

   # hivenode/config/cloud.yml
   ledger_mode: postgres
   storage_mode: railway
   sync_enabled: true
   rag_enabled: true
   scheduler_enabled: true

   # hivenode/config/remote.yml
   ledger_mode: postgres
   storage_mode: cloud
   sync_enabled: true
   rag_enabled: false
   scheduler_enabled: false
   ```

2. Update `config.py` to load from YAML:
   ```python
   # hivenode/config.py
   import yaml
   from pydantic_settings import BaseSettings, SettingsConfigDict

   class HivenodeSettings(BaseSettings):
       model_config = SettingsConfigDict(
           env_prefix="HIVENODE_",
           case_sensitive=False
       )

       mode: str = "local"
       ledger_mode: str
       storage_mode: str
       sync_enabled: bool
       rag_enabled: bool
       scheduler_enabled: bool

       def __init__(self, **data):
           # Load mode-specific defaults from YAML
           mode = os.getenv("HIVENODE_MODE", "local")
           config_path = Path(__file__).parent / "config" / f"{mode}.yml"

           with open(config_path) as f:
               defaults = yaml.safe_load(f)

           # Merge YAML defaults with env overrides
           merged = {**defaults, **data}
           super().__init__(**merged)
   ```

**Tests to modify:**
- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\simdecisions-refactor\tests\hivenode\test_config.py` (verify YAML loading, env override behavior)

**Acceptance Criteria:**
- [ ] 3 YAML config files created (local.yml, cloud.yml, remote.yml)
- [ ] `_set_defaults()` function removed from `config.py`
- [ ] `HivenodeSettings` loads defaults from YAML based on `HIVENODE_MODE`
- [ ] Env vars still override YAML defaults (12-factor compliance)
- [ ] All existing tests pass with no regression
- [ ] 5+ new tests for YAML loading logic

**JD Signal Strengthened:** Criterion 1 (demonstrates 12-factor config separation via YAML + env vars)

---

### Unit 3: CI/CD Pipeline Documentation (RO-3)
**Effort:** 4 hours
**Severity:** Structural
**Priority:** P2

**Files to create:**
- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\simdecisions-refactor\.github\workflows\test.yml`
- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\simdecisions-refactor\.github\workflows\deploy-railway.yml`
- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\simdecisions-refactor\.github\workflows\deploy-vercel.yml`

**Files to modify:**
- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\simdecisions-refactor\DEPLOYMENT.md` (add CI/CD section)

**Changes:**
1. Create GitHub Actions workflow for automated testing:
   ```yaml
   # .github/workflows/test.yml
   name: Test Suite
   on: [push, pull_request]
   jobs:
     test-python:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         - uses: actions/setup-python@v5
           with:
             python-version: '3.12'
         - run: pip install uv
         - run: uv pip install -r requirements.txt
         - run: pytest tests/ -v --cov=hivenode --cov=simdecisions

     test-typescript:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         - uses: actions/setup-node@v4
           with:
             node-version: '20'
         - run: cd browser && npm ci
         - run: cd browser && npx vitest run
   ```

2. Create Railway auto-deploy workflow:
   ```yaml
   # .github/workflows/deploy-railway.yml
   name: Deploy to Railway
   on:
     push:
       branches: [main]
   jobs:
     deploy:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         - run: curl -fsSL https://railway.app/install.sh | sh
         - run: railway up
           env:
             RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
   ```

3. Create Vercel preview deployment workflow:
   ```yaml
   # .github/workflows/deploy-vercel.yml
   name: Vercel Preview
   on: [pull_request]
   jobs:
     deploy:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         - uses: amondnet/vercel-action@v25
           with:
             vercel-token: ${{ secrets.VERCEL_TOKEN }}
             vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
             vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
   ```

4. Update DEPLOYMENT.md with CI/CD section:
   ```markdown
   ## CI/CD Pipeline

   ### Automated Testing
   - **Trigger:** Every push and pull request
   - **Python:** pytest with coverage reports
   - **TypeScript:** vitest with coverage reports
   - **Status:** See GitHub Actions tab

   ### Railway Deployment
   - **Trigger:** Push to `main` branch
   - **Build:** Docker image via Dockerfile
   - **Health Check:** /health endpoint (120s timeout)
   - **Status:** See Railway dashboard

   ### Vercel Deployment
   - **Trigger:** Push to `main` (production), pull request (preview)
   - **Build:** `cd browser && npm run build`
   - **Status:** See Vercel dashboard
   ```

**Tests to create:**
- None (workflow validation via GitHub Actions UI)

**Acceptance Criteria:**
- [ ] 3 GitHub Actions workflows created (.github/workflows/)
- [ ] Test workflow runs pytest + vitest on every push
- [ ] Railway deploy workflow triggers on main branch push
- [ ] Vercel preview workflow triggers on pull request
- [ ] DEPLOYMENT.md updated with CI/CD section
- [ ] Workflows execute successfully (verified in GitHub Actions tab)

**JD Signal Strengthened:** Criterion 3 (demonstrates automated CI/CD pipelines with testing + deployment)

---

### Unit 4: Vercel Routing Config (RO-4)
**Effort:** 1 hour
**Severity:** Cosmetic
**Priority:** P2

**Files to modify:**
- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\simdecisions-refactor\vercel.json`

**Changes:**
1. Replace hardcoded Railway URLs with env vars:
   ```json
   {
     "rewrites": [
       {
         "source": "/health",
         "destination": "$HIVENODE_SERVICE_URL/health"
       },
       {
         "source": "/auth/:path*",
         "destination": "$AUTH_SERVICE_URL/:path*"
       }
     ]
   }
   ```

2. Add env vars in Vercel dashboard:
   - `HIVENODE_SERVICE_URL=https://hivenode-production.up.railway.app`
   - `AUTH_SERVICE_URL=https://beneficial-cooperation-production.up.railway.app`

**Tests to create:**
- Manual verification: deploy to Vercel, test /health endpoint

**Acceptance Criteria:**
- [ ] `vercel.json` uses env var placeholders (`$HIVENODE_SERVICE_URL`)
- [ ] Vercel env vars configured in dashboard
- [ ] /health endpoint responds HTTP 200 after deploy
- [ ] All proxy routes work unchanged

**JD Signal Strengthened:** Criterion 1 (demonstrates 12-factor config via env vars)

---

### Unit 5: Volume Naming Rules (RO-5)
**Effort:** 2 hours
**Severity:** Cosmetic
**Priority:** P2

**Files to modify:**
- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\simdecisions-refactor\hivenode\storage\registry.py`

**Changes:**
1. Replace string length check with explicit enum:
   ```python
   # hivenode/storage/registry.py
   from enum import Enum

   class VolumeType(Enum):
       SYSTEM = "system"
       USER = "user"

   class VolumeDeclaration:
       name: str
       type: VolumeType  # Explicit, not inferred from length
       adapter: str

   def declare_volume(name: str, type: VolumeType, adapter: str):
       """Declare a volume with explicit type (system or user)."""
       return VolumeDeclaration(name=name, type=type, adapter=adapter)
   ```

2. Update all call sites to use explicit type:
   ```python
   # Before
   registry.declare("home", adapter="local")  # type inferred from len("home") <= 7

   # After
   registry.declare("home", type=VolumeType.SYSTEM, adapter="local")
   ```

**Tests to modify:**
- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\simdecisions-refactor\tests\hivenode\storage\test_registry.py` (update to use VolumeType enum)

**Acceptance Criteria:**
- [ ] `VolumeType` enum created (SYSTEM, USER)
- [ ] String length check removed from registry.py
- [ ] All volume declarations use explicit `type` parameter
- [ ] All existing tests pass with enum-based logic
- [ ] 3+ new tests for VolumeType validation

**JD Signal Strengthened:** Criterion 2 (demonstrates API design improvement via explicit types)

---

### Unit 6: OAuth Token Interceptor Lifecycle (RO-6)
**Effort:** 3 hours
**Severity:** Structural
**Priority:** P2

**Files to modify:**
- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\simdecisions-refactor\browser-src\App.tsx`
- Create: `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\simdecisions-refactor\browser-src\infrastructure\auth\useOAuthRedirect.ts`

**Changes:**
1. Create React hook for OAuth token extraction:
   ```typescript
   // browser/src/infrastructure/auth/useOAuthRedirect.ts
   import { useEffect } from 'react';

   export function useOAuthRedirect() {
     useEffect(() => {
       const params = new URLSearchParams(window.location.search);
       const token = params.get('token');

       if (token) {
         localStorage.setItem('auth_token', token);
         // Remove token from URL
         window.history.replaceState({}, '', window.location.pathname);
       }
     }, []);
   }
   ```

2. Update App.tsx to use hook:
   ```typescript
   // browser/src/App.tsx
   import { useOAuthRedirect } from './infrastructure/auth/useOAuthRedirect';

   function App() {
     useOAuthRedirect();  // Runs in React lifecycle, not module load

     // Rest of App logic...
   }
   ```

**Tests to create:**
- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\simdecisions-refactor\browser-src\infrastructure\auth\__tests__\useOAuthRedirect.test.ts`

**Acceptance Criteria:**
- [ ] `useOAuthRedirect` hook created in `infrastructure/auth/`
- [ ] OAuth token extraction removed from module-level code in App.tsx
- [ ] Hook runs in React useEffect lifecycle
- [ ] Token still extracted from URL and stored correctly
- [ ] 5+ tests for hook behavior (token present, token absent, cleanup)

**JD Signal Strengthened:** Criterion 2 (demonstrates frontend architecture improvement via React hooks)

---

## Summary Table

| Unit | RO ID | Severity | Effort (hrs) | JD Criterion | Files Modified | Tests Added |
|------|-------|----------|--------------|--------------|----------------|-------------|
| 1 | RO-1 | Structural | 8 | 1 (refactoring) | 8 | 12+ |
| 2 | RO-2 | Structural | 3 | 1 (12-factor) | 4 | 5+ |
| 3 | RO-3 | Structural | 4 | 3 (CI/CD) | 4 | 0 (workflow validation) |
| 4 | RO-4 | Cosmetic | 1 | 1 (12-factor) | 1 | 0 (manual verification) |
| 5 | RO-5 | Cosmetic | 2 | 2 (API design) | 2 | 3+ |
| 6 | RO-6 | Structural | 3 | 2 (frontend arch) | 2 | 5+ |
| **Total** | — | — | **21** | — | **21** | **25+** |

---

## Prioritization Guidance

**If you have 1-4 hours:**
- Do Unit 4 (Vercel routing config) — highest ROI, demonstrates 12-factor config

**If you have 4-8 hours:**
- Do Unit 3 (CI/CD pipeline) — directly hits JD criterion 3

**If you have 8-12 hours:**
- Do Unit 1 (lifespan manager decomposition) — strongest architectural signal

**If you have 12+ hours:**
- Do Units 1, 3, 6 in order (lifespan → CI/CD → OAuth hook)

**If interview is NOT scheduled:**
- Defer all units. Focus on SPEC-PORTFOLIO-CURATE-001 instead.

---

## Constraints

- **No git operations.** This spec creates/modifies files only. Q88N will review before commit.
- **TDD enforced.** Write tests before implementation for all structural changes.
- **No breaking changes.** All refactors must preserve existing API contracts and route behavior.
- **12-factor compliance.** Any config changes must maintain env-based overrides.

---

## Success Criteria

Refactoring complete if:
1. ✅ All selected work units pass their acceptance criteria
2. ✅ No regression in existing tests
3. ✅ Health check endpoint responds HTTP 200
4. ✅ Railway/Vercel deployments work unchanged
5. ✅ 25+ new tests added across all units

**Next step:** Deploy to Railway/Vercel, verify health checks, grant 1000bulbs interviewer access to private repos.

---

**END OF SPEC**
