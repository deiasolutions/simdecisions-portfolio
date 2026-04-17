# BRIEFING-BUG-031-REQUEUE: Task File Created -- READY FOR REVIEW

**Status:** READY FOR Q33NR REVIEW
**Model:** Sonnet
**Date:** 2026-03-18

## Files Modified

Created:
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\2026-03-18-TASK-BUG-031-REQUEUE-code-explorer-fix.md`

## What Was Done

- Read BOOT.md and HIVE.md to understand chain of command and workflows
- Read three previous failed attempt specs to understand the pattern of failure
- Read `browser/src/apps/treeBrowserAdapter.tsx` (current broken implementation)
- Read `browser/src/primitives/text-pane/SDEditor.tsx` (to see what it expects)
- Searched `hivenode/routes/storage_routes.py` to confirm URI format requirements
- Created comprehensive task file with:
  - **Explicit "MUST MODIFY SOURCE CODE" warning** (appears 4 times)
  - **Verification checklist** requiring source code modification before COMPLETE
  - **Example fixed code** showing exact changes needed
  - **Root cause analysis** from prior bee work
  - **7 specific test requirements** covering all edge cases
  - **Absolute file paths** throughout
  - **Smoke test commands** for all affected layers
  - **8-section response template** with emphasis on "Files Modified" section
  - **Notes from previous attempts** explaining why they failed

## Task File Structure

The task file includes:

1. **Objective** — Clear one-sentence goal emphasizing source modification
2. **Context** — Explains this is 4th attempt and WHY previous attempts failed
3. **Root Cause** — Documents missing `name` field and protocol prefix
4. **Current Broken Code** — Shows exact lines that are wrong
5. **What SDEditor Expects** — Shows what the consumer needs
6. **What Backend Expects** — Shows storage API requirements
7. **Files to Read First** — 4 absolute paths with line numbers
8. **Deliverables** — PRIMARY DELIVERABLE section in bold/caps
9. **Required Changes** — Step-by-step modification instructions
10. **Example Fixed Code** — Full corrected implementation
11. **Test Requirements** — 7 specific test cases
12. **Smoke Test Commands** — 4 test commands to verify no regressions
13. **Acceptance Criteria** — 7 checkboxes including source modification
14. **Constraints** — Standard rules (500 lines, TDD, no stubs)
15. **Critical Verification Checklist** — 7 yes/no questions before COMPLETE
16. **Notes from Previous Attempts** — Why they failed

## Key Design Decisions

### 1. Repetition of "MUST MODIFY SOURCE"

The phrase "MUST modify source code" or "CRITICAL: modify treeBrowserAdapter.tsx" appears in:
- Task title (Fourth Attempt)
- Objective
- Deliverables PRIMARY section (bold, caps, 3 sentences)
- Acceptance criteria (first two items)
- Verification checklist (first 3 items)

**Rationale:** Previous bees wrote perfect analysis but never modified the file. Making this impossible to miss.

### 2. Example Code Provided

The task includes the EXACT corrected code block with comments showing what changed.

**Rationale:** Removes any ambiguity about what needs to happen. Bee can copy-paste and verify.

### 3. Verification Checklist Before COMPLETE

7 yes/no questions that MUST be YES before marking task complete.

**Rationale:** Forces bee to verify source modification before writing response file.

### 4. Response File Must List Source Changes

Explicit requirement: "Files Modified" section MUST show treeBrowserAdapter.tsx with actual diff.

**Rationale:** Makes it impossible for bee to claim COMPLETE without actually making the change.

## Acceptance Criteria (for this briefing task)

- [x] Read BOOT.md, HIVE.md, briefing
- [x] Analyzed root cause from previous attempts
- [x] Read current source files
- [x] Created task file with absolute paths
- [x] Included explicit source modification warnings
- [x] Included example corrected code
- [x] Included 7 test requirements
- [x] Included smoke test commands
- [x] Included 8-section response template
- [x] Included verification checklist
- [x] Returned to Q33NR for review (DO NOT dispatch yet)

## Clock / Cost / Carbon

- **Clock:** ~15 minutes
- **Cost:** ~$0.05 (sonnet reads + writes)
- **Carbon:** ~2g CO2e

## Issues / Follow-ups

### Ready for Q33NR Review

The task file is ready for Q33NR to review. Key questions for review:

1. **Is the repetition of "MUST MODIFY SOURCE" excessive or appropriate?** (Given 3 failed attempts, I judged it necessary)
2. **Should we require manual smoke test in browser before COMPLETE?** (Currently only automated tests required)
3. **Should we add a requirement to log the bug fix in inventory.py?** (Not currently included)

### If Q33NR Approves

Next steps after approval:
1. Q33N dispatches bee (sonnet) with this task file
2. Bee reads task, modifies treeBrowserAdapter.tsx, writes tests, writes response
3. Q33N reviews bee response file
4. If source modification verified: task complete
5. If source modification missing: escalate to Q88N for manual intervention

### Alternative Approach (If This Fails Again)

If this 4th attempt also fails to modify source code despite explicit instructions, Q33NR should:
1. Report to Q88N
2. Q88N may choose to:
   - Make the fix directly (Q33NR-DIRECT)
   - Dispatch with different model (opus instead of sonnet)
   - Create a different task structure (split into "modify source" and "write tests" as separate tasks)
   - Investigate if there's a prompt injection or model limitation preventing source modification

---

**Task file location:** `.deia/hive/tasks/2026-03-18-TASK-BUG-031-REQUEUE-code-explorer-fix.md`

**Awaiting Q33NR review before dispatch.**
