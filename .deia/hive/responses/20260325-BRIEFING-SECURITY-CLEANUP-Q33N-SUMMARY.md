# BRIEFING-SECURITY-CLEANUP: Task File Summary -- AWAITING Q33NR REVIEW

**Status:** Task files written, awaiting Q33NR review and approval
**Model:** Sonnet (Q33N)
**Date:** 2026-03-25

## Task Files Created

Created 10 task files covering all phases of the security cleanup runbook (excluding Phase 2 git history scrubbing and TASK 1.3 CORS changes as instructed):

### PHASE 1: Remove Hardcoded Credentials

1. **TASK-SEC-1: Clean Hardcoded Credentials from config.py**
   - Remove hardcoded Railway URLs from config.py
   - Replace inventory_database_url fallback with clean env-var logic
   - Verify no postgresql:// strings remain
   - Model: Sonnet

2. **TASK-SEC-2: Verify .env and .gitignore Configuration**
   - Verify .env is in .gitignore
   - Verify .env is not tracked by git
   - Read-only verification task
   - Model: Haiku

3. **TASK-SEC-3: Add Rate Limiting to LLM Routes**
   - Install slowapi dependency
   - Add limiter setup to main.py
   - Apply rate limiting to LLM-facing routes (10/minute)
   - Write tests for rate limit behavior
   - Model: Sonnet

### PHASE 3: Repo Hygiene

4. **TASK-SEC-4: Identify Junk Files in Repository Root**
   - Identify files starting with {, nul, C..., etc.
   - List them for Q88N review (no deletion)
   - Read-only verification
   - Model: Haiku

5. **TASK-SEC-5: Review and Update .gitignore Patterns**
   - Check for recommended patterns ({*, nul, *.tmp, etc.)
   - Add missing patterns (additive only)
   - Model: Haiku

### PHASE 4: Fix Test Environment

6. **TASK-SEC-6: Fix Windows tmp_path PermissionError in Tests**
   - Override tempfile.tempdir in conftest.py for Windows
   - Run backend tests and record baseline
   - Model: Haiku

7. **TASK-SEC-7: Fix Frontend Tests - Vitest esbuild EPERM**
   - Clean reinstall node_modules if esbuild spawn fails
   - Run frontend tests and record baseline
   - Model: Haiku

8. **TASK-SEC-8: Verify Frontend Build**
   - Run npm run build and verify success
   - Document build output
   - Model: Haiku

9. **TASK-SEC-9: Record Test Baseline**
   - Create comprehensive test baseline document
   - Consolidate backend + frontend test counts
   - Document known failures
   - Model: Haiku

### PHASE 5: Fix Import-Time Side Effects

10. **TASK-SEC-10: Defer config.py Initialization with Lazy Proxy**
    - Replace module-level settings instantiation with lazy proxy
    - Verify import has no side effects
    - Verify all existing tests pass
    - Model: Sonnet

## Task Dependencies

Sequential execution recommended:
1. TASK-SEC-1, SEC-2, SEC-4, SEC-5 can run in parallel (independent)
2. TASK-SEC-3 depends on SEC-1 (needs clean config)
3. TASK-SEC-6, SEC-7, SEC-8 can run in parallel (test infrastructure)
4. TASK-SEC-9 depends on SEC-6, SEC-7, SEC-8 (consolidates their results)
5. TASK-SEC-10 can run after SEC-6 (requires working backend tests)

## Execution Plan

**Batch 1 (parallel):**
- TASK-SEC-1 (Sonnet)
- TASK-SEC-2 (Haiku)
- TASK-SEC-4 (Haiku)
- TASK-SEC-5 (Haiku)

**Batch 2 (after Batch 1):**
- TASK-SEC-3 (Sonnet)
- TASK-SEC-6 (Haiku)
- TASK-SEC-7 (Haiku)
- TASK-SEC-8 (Haiku)

**Batch 3 (after Batch 2):**
- TASK-SEC-9 (Haiku)
- TASK-SEC-10 (Sonnet)

## Excluded Items

As instructed in the briefing:
- ❌ TASK 1.3: CORS changes (explicitly skipped)
- ❌ Phase 2: Git history scrubbing (Q88N will handle separately)
- ❌ File deletions (only identification, no deletion without Q88N approval)
- ❌ Git write operations (no commits, no pushes)

## Current Findings (from investigation)

1. **config.py:** No hardcoded Railway URLs found in current version. The code already uses environment variables. TASK-SEC-1 will verify this and ensure proper fallback logic.

2. **Junk files:** Found `nul` file in repo root (0 bytes, created 2026-03-25 14:16).

3. **.gitignore:** Already contains `.env`, `.env.local`, `nul` patterns. TASK-SEC-5 will verify all recommended patterns.

4. **pyproject.toml:** Does NOT currently have `slowapi` dependency. TASK-SEC-3 will add it.

5. **main.py:** Currently has RateLimiterMiddleware but not slowapi. May need to verify approach.

## Issues for Q33NR Review

1. **main.py already has RateLimiterMiddleware** (line 18). TASK-SEC-3 adds slowapi which may conflict or duplicate. Should we:
   - Replace existing RateLimiterMiddleware with slowapi?
   - Keep both and apply slowapi only to LLM routes?
   - Verify existing middleware and skip slowapi?

2. **config.py appears clean** — no hardcoded Railway URLs found in grep. TASK-SEC-1 may find the code is already correct.

## Awaiting Q33NR Approval

Q33N has completed task file writing. Awaiting Q33NR review of:
- Task file completeness
- Deliverable clarity
- Test requirements
- Model assignments
- Execution plan

Once approved, Q33N will dispatch bees according to the 3-batch execution plan.

## All Task Files

All 10 task files written to:
- `.deia/hive/tasks/2026-03-25-TASK-SEC-1-CONFIG-CLEANUP.md`
- `.deia/hive/tasks/2026-03-25-TASK-SEC-2-VERIFY-ENV-GITIGNORE.md`
- `.deia/hive/tasks/2026-03-25-TASK-SEC-3-ADD-RATE-LIMITING.md`
- `.deia/hive/tasks/2026-03-25-TASK-SEC-4-IDENTIFY-JUNK-FILES.md`
- `.deia/hive/tasks/2026-03-25-TASK-SEC-5-REVIEW-GITIGNORE.md`
- `.deia/hive/tasks/2026-03-25-TASK-SEC-6-FIX-WINDOWS-TMP-PATH.md`
- `.deia/hive/tasks/2026-03-25-TASK-SEC-7-FIX-VITEST-ESBUILD.md`
- `.deia/hive/tasks/2026-03-25-TASK-SEC-8-VERIFY-BUILD.md`
- `.deia/hive/tasks/2026-03-25-TASK-SEC-9-TEST-BASELINE.md`
- `.deia/hive/tasks/2026-03-25-TASK-SEC-10-LAZY-CONFIG.md`

---

**Q33N awaiting Q33NR review and dispatch approval.**
