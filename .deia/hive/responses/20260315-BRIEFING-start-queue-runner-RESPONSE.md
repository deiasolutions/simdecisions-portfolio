# BRIEFING: Start Queue Runner -- FAILED

**Status:** FAILED (Unicode encoding error in subprocess)
**Model:** Sonnet
**Date:** 2026-03-15

## Files Modified
None (queue runner crashed before completing any work)

## What Was Done
- Verified hivenode is running on port 8420 (status: OK, uptime 3584s)
- Listed pending specs in queue (2 SPEC files found: BL-126, ra96it)
- Moved orphaned fix-cycle spec to _done/ as instructed
- Started queue runner via `python .deia/hive/scripts/queue/run_queue.py`
- Runner initialized and began processing BL-126 spec
- Runner crashed with Unicode encoding error in subprocess pipe reader

## Test Results
N/A — runner crashed before reaching test phase

## Build Verification
N/A — runner crashed before completing any work

## Acceptance Criteria
From briefing:
- [ ] **NOT DONE** — Verify hivenode running (✓ completed)
- [ ] **NOT DONE** — List pending specs (✓ completed)
- [ ] **NOT DONE** — Move orphaned spec to _done (✓ completed)
- [ ] **NOT DONE** — Start queue runner (❌ crashed)
- [ ] **NOT DONE** — Process pending specs (❌ never reached)

## Clock / Cost / Carbon
- **Clock:** ~5 minutes (runner stuck, then killed)
- **Cost:** ~$0.00 (no LLM calls completed)
- **Carbon:** negligible

## Issues / Follow-ups

### Root Cause
The queue runner's dispatch handler (`C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\dispatch_handler.py:121`) calls `subprocess.Popen` with `text=True` but no explicit encoding:

```python
proc = subprocess.Popen(
    cmd,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,        # ← uses system default encoding
    cwd=str(self.repo_root),
)
```

On Windows, this defaults to `cp1252`, which cannot decode UTF-8 characters from Claude's output (specifically byte `0x9d` at multiple positions). The pipe reader threads crash with:

```
UnicodeDecodeError: 'charmap' codec can't decode byte 0x9d in position 762: character maps to <undefined>
```

### Fix Required
Add explicit UTF-8 encoding to the Popen call:

```python
proc = subprocess.Popen(
    cmd,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    encoding='utf-8',  # ← ADD THIS
    cwd=str(self.repo_root),
)
```

Location: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\dispatch_handler.py:121`

### Queue State
The queue runner did not complete any specs. The queue directory still contains:
- `2026-03-14-2100-SPEC-BL-126-kanban-backlog-db.md` (priority P1)
- `2026-03-14-2200-SPEC-ra96it-sso-federation.md` (priority P1)
- Morning reports (ignored by runner)
- Event log (ignored by runner)

### Recommended Next Steps
1. Q88N decides: should Q33NR make the encoding fix directly (emergency override), or dispatch a bee?
2. After fix is deployed, restart the queue runner
3. Monitor the first spec (BL-126) to confirm the encoding issue is resolved

### Note on Role Boundaries
Per HIVE.md, Q33NR (regent) does NOT write code unless Q88N explicitly approves it for emergency fixes. This is a one-line fix in a critical infrastructure script, but I'm waiting for Q88N's direction.
