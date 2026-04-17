# BRIEFING: Dispatcher False-Completion Diagnosis

**From:** Q33NR
**To:** Q33N
**Date:** 2026-04-06
**Model:** sonnet
**Priority:** P0 — blocking all pipeline work

---

## Objective

Diagnose why the dispatcher daemon is moving brand-new specs from `backlog/` directly to `_done/` without them ever being executed by a bee. This is a false-completion bug. Do NOT fix it — just find the root cause and report back.

---

## Symptoms

1. Four specs were created at 15:49 today (SPEC-WAVE0-A, B, C and SPEC-INFRA-01)
2. Within one scheduler cycle, the dispatcher moved WAVE0-A, B, C to `_done/` — they were never built
3. INFRA-01 was moved to `_active/` despite the embedded queue runner being dead
4. This matches a previously observed pattern where specs get ALREADY_COMPLETE status falsely

## Files to Read

- hivenode/scheduler/dispatcher_daemon.py
- hivenode/scheduler/scheduler_daemon.py
- .deia/hive/queue/monitor-state.json
- .deia/hive/queue/_done/

## Questions to Answer

1. What logic in the dispatcher decides a spec is "already complete"? Find the exact code path.
2. Is it matching on task ID prefix, filename substring, or something else? The old March 15 WAVE0 specs (different tasks entirely) are in `_done/` — is the dispatcher matching "WAVE0" and concluding the new ones are duplicates?
3. What triggers the move to `_active/` vs `_done/`? Why did INFRA-01 go to `_active/` but WAVE0-A/B/C went to `_done/`?
4. Is monitor-state.json caching old completion records that poison new specs?
5. What's the dispatcher's decision log? Check `dispatched.jsonl` or `dispatcher_log.jsonl` for entries about these specs.

## Deliverable

Response file: `.deia/hive/responses/20260406-DISPATCHER-DX-RESPONSE.md`

Sections:
1. Root cause (the exact code path and condition that triggers false completion)
2. Evidence (log entries, file matches, or state that proves it)
3. Recommended fix (describe what SHOULD change, but do NOT make the change)
4. Blast radius (what else might break if we fix this)

## Constraints

- DIAGNOSIS ONLY. Do NOT modify any code or config files.
- Do NOT move any spec files.
- Do NOT restart any services.
