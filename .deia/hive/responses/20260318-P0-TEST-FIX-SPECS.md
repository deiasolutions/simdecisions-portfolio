# P0 Test Fix Specs Written -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-03-18

## Files Modified
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\queue\2026-03-18-SPEC-TASK-BUG042-bus-ledger-publisher-required.md` (created)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\queue\2026-03-18-SPEC-TASK-BUG043-e2e-server-startup-timeout.md` (created)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\queue\2026-03-18-SPEC-TASK-BUG044-rag-reliability-metadata-missing.md` (created)

## What Was Done
- Read `.deia/BOOT.md`, `.deia/HIVE.md`, and full test sweep report
- Ran `python _tools/inventory.py bug list` to identify next available BUG IDs (042, 043, 044)
- Wrote 3 lightweight spec files for P0 test failures:
  - **BUG-042:** BUS.__init__() ledger_publisher signature breaking 58 tests (governance, dispositions, heartbeat, cloud storage)
  - **BUG-043:** E2E server startup timeout blocking 28 integration tests
  - **BUG-044:** ReliabilityMetadata missing from RAG module (blocks all RAG tests)
- Each spec includes:
  - Objective (one sentence)
  - Problem description with error pattern
  - Affected test count and file paths
  - Reference to full test sweep report
  - Suggested fix approach (Option A/B where applicable)
  - Files to check (absolute paths)
  - Success criteria
  - Response file path
- Specs set to priority P0 and model sonnet
- Dropped all 3 specs directly into `.deia/hive/queue/` for queue runner pickup

## Test Results
No tests run (spec writing only).

## Build Verification
Not applicable (spec writing only).

## Acceptance Criteria
- [x] Read full test sweep report
- [x] Identify 3 P0 test failures (BUS signature, E2E startup, RAG collection error)
- [x] Check existing BUG IDs to assign next available (042, 043, 044)
- [x] Write 3 lightweight spec files (under 50 lines each)
- [x] Point to test sweep report as reference
- [x] Include suggested fix approach for each
- [x] Drop specs in `.deia/hive/queue/` directory
- [x] Use naming convention: `2026-03-18-SPEC-TASK-BUG0XX-<short-name>.md`

## Clock / Cost / Carbon
- **Clock:** ~5 minutes
- **Cost:** $0.00 (spec writing only)
- **Carbon:** ~0g (local file operations)

## Issues / Follow-ups
**Queue Runner Status:** Specs written to queue directory. Queue runner should pick them up automatically if running.

**Priority Order:** All 3 specs are P0. Suggested execution order:
1. **BUG-042 (BUS signature)** — Unblocks 58 tests immediately, may also fix E2E startup (BUG-043)
2. **BUG-043 (E2E startup)** — If not fixed by BUG-042, debug separately
3. **BUG-044 (RAG collection)** — Independent, can run in parallel

**Spec Quality:** Kept specs lightweight per briefing instructions (under 50 lines each). Q33NR will flesh out task files if needed.

**Bug ID Assignment:** Next available after these: BUG-045, BUG-046, BUG-047...
