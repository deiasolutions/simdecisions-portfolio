# Zombie Failures — RCA Pending

**Created:** 2026-04-06
**Purpose:** Failed pipeline items parked for root cause analysis

These 8 items appear as "failed" in the build monitor. Most are not real spec failures — they're briefings or tasks that were incorrectly fed to the queue runner, or edge cases in completion detection.

## Items

| # | Task ID | Date | Cost | Category | Notes |
|---|---------|------|------|----------|-------|
| 1 | MW-T06 (test-notification-pane) | Apr 6 | $4.15 | FALSE POSITIVE | Bee found tests already existed (MW-S06 built them). Reported ALREADY_COMPLETE. Queue runner didn't recognize that status → marked as failed → spawned useless fix cycle. **Spec is in _done/, work is complete.** |
| 2 | BRIEFING-ANONYMOUS-MODE-CORRECTIONS | Apr 2 | $2.29 | WRONG INPUT | Briefing doc fed to queue runner. Not a spec. |
| 3 | TASK-EFE3B-inbox-models | Mar 31 | $3.33 | SUPERSEDED | Old efemera task, superseded by CONN rebuild specs |
| 4 | BRIEFING-PHASE3-EFEMERA-REBUILD-v2 | Mar 31 | $0.00 | WRONG INPUT | Briefing doc fed to queue runner. Not a spec. |
| 5 | BRIEFING-PHASE3-EFEMERA-REBUILD | Mar 31 | $2.73 | WRONG INPUT | Briefing doc fed to queue runner. Not a spec. |
| 6 | TASK-EFEMERA-LIVE-404 | Mar 29 | $4.02 | SUPERSEDED | Old efemera task, superseded by CONN rebuild |
| 7 | BRIEFING-EGG-LAYOUT-AUDIT | Mar 27 | $2.69 | WRONG INPUT | Briefing doc fed to queue runner. Not a spec. |
| 8 | FLOW-B | Mar 26 | $0.00 | NEVER RAN | No model assigned, never executed |
| 9 | MW-V04 (verify-conversation-pane) | Apr 6 | $0.00 | STALE — bee died or never completed | Spec was stuck in _active/ for 3+ hours with only "Processing..." heartbeats. Moved to _zombies/ on 2026-04-06 for RCA. **Action:** Bee never completed; likely crashed mid-execution or dispatcher killed it. Consider requeuing with fresh dispatch if conversation-pane verification still needed. |

## Root Causes (preliminary)

1. **WRONG INPUT (4 items):** Briefing docs placed in queue/ and the queue runner accepted them because the filename filter wasn't strict enough. Fix: queue runner should reject files that don't match `SPEC-*.md` pattern.

2. **FALSE POSITIVE (1 item):** Queue runner doesn't recognize `ALREADY_COMPLETE` as a valid success status. Fix: SPEC-QUEUE-FIX-ALREADY-COMPLETE.

3. **SUPERSEDED (2 items):** Old efemera tasks that the CONN rebuild made irrelevant. No fix needed — just cleanup.

4. **NEVER RAN (1 item):** FLOW-B had no model assignment. Early pipeline artifact.

## Wasted Cost

$17.21 total across all 8 failures. $9.44 on wrong-input briefings alone.

## Action Items

- [ ] Fix queue runner filename filter (reject non-SPEC files)
- [ ] Fix queue runner ALREADY_COMPLETE status handling
- [ ] Clear these from build monitor failed list (or add "dismiss" to BMON UI)
