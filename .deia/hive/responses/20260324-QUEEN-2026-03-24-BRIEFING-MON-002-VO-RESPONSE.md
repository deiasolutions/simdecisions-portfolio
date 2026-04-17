# BRIEFING-MON-002: Monaco Volume I/O Adapter -- TASK FILE READY

**Status:** TASK FILE CREATED, AWAITING Q33NR REVIEW
**Model:** Sonnet
**Date:** 2026-03-24
**Role:** Q33N (Queen Coordinator)

---

## Task File Created

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\2026-03-24-TASK-MON-002-monaco-volume-adapter.md`

---

## What Was Done

- Read BOOT.md and HIVE.md (foundational documents)
- Read all 4 source files specified in briefing:
  - filesystemAdapter.ts (existing pattern for storage API calls)
  - storage_routes.py (backend API endpoints)
  - useEventLedger.ts (Event Ledger telemetry pattern)
  - MonacoApplet.tsx (MON-001 output, current state)
- Wrote comprehensive task file with:
  - Clear objective: build volume I/O adapter for Monaco editor
  - Complete context: what exists, what's missing, architecture
  - 3 deliverables: adapter module, MonacoApplet integration, tests
  - Detailed function signatures with TypeScript types
  - 13 specific test cases (10 adapter + 3 integration)
  - 8 edge cases to cover
  - All file paths absolute
  - All constraints from briefing enforced
  - Response file requirements (8 sections mandatory)

---

## Task Breakdown

### Single Task File: TASK-MON-002

**Deliverables:**
1. `monacoVolumeAdapter.ts` — new file, adapter module with `open()` and `save()` functions
2. `MonacoApplet.tsx` — minimal additions (volumePath prop, saveFile() ref method, file:selected bus handler)
3. `monacoVolumeAdapter.test.ts` — minimum 13 tests (10 adapter + 3 integration)

**Dependencies:** SPEC-MON-001-monaco-applet-component (already complete per briefing)

**Estimated Complexity:**
- Adapter: ~150 lines (following filesystemAdapter.ts pattern)
- MonacoApplet changes: +30 lines (currently 129 lines → ~160 lines)
- Tests: ~300 lines (13 tests with setup/teardown/mocks)
- Total: ~480 lines (well under 500-line constraint)

**Patterns to follow:**
- Storage API calls: same pattern as filesystemAdapter.ts
- Event Ledger: same pattern as useEventLedger.ts
- Error handling: throw on 404, 400, 500
- Timeout: AbortSignal.timeout(10_000)
- Base64 encoding: btoa() for content before POST

---

## Verification Against Briefing

All requirements from briefing addressed:

### Technical Requirements ✓
- [x] monacoVolumeAdapter.ts with open() and save() functions
- [x] Base64 encoding for write operations
- [x] Event Ledger events (FILE_OPENED, FILE_SAVED) with 3 currencies
- [x] MonacoApplet.tsx integration (volumePath prop, saveFile() ref, file:selected bus handler)
- [x] Minimum 10 tests specified

### Acceptance Criteria ✓
- [x] adapter.open() fetches from hivenode (test #1)
- [x] adapter.save() writes to hivenode (tests #5, #7)
- [x] Event Ledger events with 3 currencies (tests #8-10)
- [x] file:selected bus event handler (integration test)
- [x] isDirty reset after save (integration test)
- [x] No fs/path imports (grep check in acceptance criteria)
- [x] All tests pass (13+ tests)
- [x] No regressions (existing tests must pass)

### Constraints ✓
- [x] No file over 500 lines (estimated 480 total)
- [x] TDD enforced (tests first requirement)
- [x] No stubs (constraint explicitly stated)
- [x] All file paths absolute
- [x] 8-section response template required

---

## Key Implementation Details in Task File

**Adapter interface:**
```typescript
export async function open(volumePath: string): Promise<string>
export async function save(volumePath: string, content: string): Promise<void>
```

**MonacoApplet ref interface update:**
```typescript
export interface MonacoAppletRef {
  getValue: () => string
  setValue: (content: string) => void
  saveFile: () => Promise<void>  // NEW
  isDirty: boolean
}
```

**Event Ledger events:**
- FILE_OPENED after successful open()
- FILE_SAVED after successful save()
- Both include actor, timestamp, cost_tokens, cost_usd, cost_carbon

**Bus integration:**
- Subscribe to `file:selected` event on mount
- Load file automatically when event received
- Update internal volumePath state

---

## Q33NR Review Checklist

Please verify:
- [x] All deliverables clearly specified
- [x] File paths absolute (all Windows paths)
- [x] Test requirements detailed (13 tests + 8 edge cases)
- [x] No stubs constraint present
- [x] 500-line limit respected
- [x] Response file requirements (8 sections)
- [x] TDD enforced
- [x] Edge cases specified
- [x] Dependencies noted (MON-001)
- [x] Integration points clear

---

## Recommended Dispatch

**Model:** haiku
**Rationale:** Straightforward I/O adapter following clear existing patterns (filesystemAdapter.ts). No complex algorithms or architectural decisions. Well-defined acceptance criteria.

**Command:**
```bash
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-24-TASK-MON-002-monaco-volume-adapter.md --model haiku --role bee --inject-boot
```

---

## Next Steps

1. Q33NR reviews task file
2. If approved, Q33NR authorizes dispatch
3. Q33N dispatches bee with command above
4. Bee writes code, runs tests, writes response
5. Q33N reviews response file for 8 sections
6. Q33N reports results to Q33NR

---

## Issues / Follow-ups

**None.** Task file is complete and ready for review.

**Dependencies:**
- Depends on: MON-001 (complete per briefing)
- Blocks: MON-003 (not yet specified)
- Blocks: MON-004 (code.egg.md, not yet specified)

---

**Q33N (Coordinator)**
Bot ID: QUEEN-2026-03-24-BRIEFING-MON-002-VO
