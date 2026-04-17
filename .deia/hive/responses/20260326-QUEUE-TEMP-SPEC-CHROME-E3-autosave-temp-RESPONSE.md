# SPEC-CHROME-E3: Autosave to Temp Storage -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-03-26

## Files Modified
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\autosave.ts` — NEW: autosave logic (timer, structural trigger, localStorage, cloud)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\__tests__\autosave.test.ts` — NEW: 11 tests for autosave functionality
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\temp_cleanup.py` — NEW: background cleanup job (boot + 24h schedule)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_temp_cleanup.py` — NEW: 9 tests for cleanup job
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\main.py` — MODIFIED: integrated cleanup task into lifespan

## What Was Done
- Created browser-side autosave module with 60-second timer and immediate structural change trigger
- Implemented synchronous localStorage saves to `local://temp/eggs/{eggId}/{userId}/layout.json`
- Implemented async cloud saves to avoid blocking main thread
- Added 7-day TTL to all temp files (layout + per-pane content)
- Created cleanup function that scans temp directory for expired files and deletes them
- Integrated cleanup task into hivenode lifespan: runs immediately on boot + every 24 hours
- Wrote 11 browser tests: timer trigger, structural trigger, TTL handling, localStorage cleanup, per-pane content serialization
- Wrote 9 backend tests: expired file deletion, valid file preservation, corrupt data handling, empty directory cleanup, scheduler functionality
- All 20 tests pass

## Deliverables Met
- [x] Autosave timer: 60 seconds, saves layout + per-pane content
- [x] Structural change trigger: saves immediately on split/merge/dock/etc
- [x] localStorage save: `local://temp/eggs/{eggId}/{userId}/layout.json`
- [x] Cloud save: async via fetch (non-blocking)
- [x] 7-day TTL on all temp files
- [x] Hivenode cleanup: runs on boot + every 24h, deletes expired temp files
- [x] Browser cleanup: `cleanupExpiredLocalStorage()` deletes expired localStorage entries on app load
- [x] All acceptance criteria met

## Test Results
**Browser tests (11/11 passing):**
```
✓ should save layout to localStorage after 60 seconds
✓ should include 7-day TTL in saved layout
✓ should save to cloud asynchronously
✓ should not crash if cloud save fails
✓ should save immediately on structural change
✓ should not wait for timer when saveNow is called
✓ should delete expired localStorage entries
✓ should handle missing TTL gracefully
✓ should handle corrupt data gracefully
✓ should clear interval when stopAutosave is called
✓ should save per-pane content to separate keys
```

**Backend tests (9/9 passing):**
```
✓ test_cleanup_deletes_expired_files
✓ test_cleanup_skips_files_without_ttl
✓ test_cleanup_handles_corrupt_json
✓ test_cleanup_deletes_content_files
✓ test_cleanup_empty_directory
✓ test_cleanup_removes_empty_parent_dirs
✓ test_schedule_cleanup_task_runs_immediately
✓ test_schedule_cleanup_task_runs_periodically
✓ test_cleanup_handles_permission_errors
```

## Smoke Test
```bash
cd browser && npx vitest run src/shell/__tests__/autosave — 11 tests pass
python -m pytest tests/hivenode/test_temp_cleanup.py -v — 9 tests pass
```

## Constraints Met
- No file over 500 lines (autosave.ts: 150 lines, temp_cleanup.py: 100 lines)
- No stubs (all functions fully implemented)
- localStorage saves are synchronous (reliability)
- Cloud saves are async (non-blocking)
- TDD approach: tests written first, then implementation

## Architecture Notes
- Browser autosave uses `volumeStorage` abstraction (existing pattern)
- Cloud save uses standard fetch API, fails gracefully without blocking localStorage
- Backend cleanup uses asyncio.create_task for background scheduling
- Cleanup task integrated into FastAPI lifespan (runs on boot, cancelled on shutdown)
- TTL format: ISO 8601 timestamp, checked via datetime comparison
- Empty parent directories are removed after file deletion to avoid clutter
