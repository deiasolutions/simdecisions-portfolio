# SPEC-Q33N-ASSESS-UNARCHIVED-TASKS-001: Assess Unarchived Hive Tasks Post-Cutover

**MODE: EXECUTE**

## Priority
P1

## Acceptance Criteria

- [ ] Every *.md in .deia/hive/tasks/ (excluding _archive/) enumerated
- [ ] Each classified as KEEP-AS-IS, KEEP-REWRITE, OBSOLETE-COMPLETED, OBSOLETE-SUPERSEDED, or UNCLEAR
- [ ] Recommendation report produced with per-file rationale
- [ ] Report delivered to .deia/hive/responses/

## Model Assignment
sonnet

## Role
queen

## Objective

Assess every uncompleted task file currently sitting in `.deia/hive/tasks/` (not under `_archive/`). For each one, determine whether it is (a) still relevant under the post-cutover monorepo layout, (b) obsolete because the work was superseded or already completed elsewhere, or (c) relevant but needs a rewrite because its file references point at the dead shiftcenter flat layout. Produce a single recommendation report for Q33NR.

**Do not write code. Do not move or delete any task files.** This is a read-and-recommend job. Q33NR will make the archive/rewrite/keep decisions after reviewing the report.

## Context

- On 2026-04-11 the shiftcenter -> simdecisions cutover completed (see `.deia/hive/responses/20260411-CUTOVER-COMPLETE.md`). The repo was subsequently flattened back to a flat layout: `hivenode/`, `browser/`, `engine/`, `_tools/`, `hodeia_auth/`, `browser/sets/` (was `eggs/`).
- The unarchived task files pre-date the flatten and may reference paths like `packages/core/src/simdecisions/core/...` or `packages/browser/src/...` that no longer exist.
- Most of these tasks were written for the monorepo layout; some may duplicate work already completed.

## Files to Read First

- `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/.deia/BOOT.md` — hard rules
- `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/.deia/HIVE.md` — Q33N workflow (you are Q33N)
- `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/.deia/hive/responses/20260411-CUTOVER-COMPLETE.md` — what the cutover actually produced
- `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/.deia/hive/responses/20260411-Q33NR-HANDOFF-REPORT.md` — the pre-cutover state

Note: In Step 1, enumerate and read all .md files under .deia/hive/tasks/ (excluding _archive/).

## Steps

1. **Enumerate.** List every `.md` file directly under `.deia/hive/tasks/` (not recursively into `_archive/`). Expect ~23 files.

2. **For each task file:**
   - Read it in full.
   - Record: `task_id`, `title`, `date` (from filename or header), `priority` if set, `intended model`, `intended role`.
   - Extract every file path referenced in "Files to Read First", "Deliverables", "Context", or inline.
   - For each referenced path, verify whether it exists in the current flat layout. Check both the dead monorepo layout (`packages/core/...`, `packages/tools/...`) and the current flat layout (`hivenode/...`, `_tools/...`, `browser/...`, `browser/sets/...`).
   - Check `.deia/hive/responses/` for any response file matching the task ID. If a response exists, note its path and status (COMPLETE / FAILED / other).
   - Check whether the subject matter was already addressed by the cutover (search cutover response for overlap).

3. **Classify each task into exactly one of:**
   - **KEEP-AS-IS** — still relevant, file refs still resolve (or are path-agnostic), not superseded. Can be dispatched as written.
   - **KEEP-REWRITE** — still relevant but file references point at the dead shiftcenter layout. Needs a path-fix rewrite before dispatch. Record which paths need updating.
   - **OBSOLETE-COMPLETED** — a response file exists with status COMPLETE, or the cutover itself absorbed the work. Safe to archive.
   - **OBSOLETE-SUPERSEDED** — the underlying requirement is no longer valid (spec changed, feature cancelled, replaced by a newer task). Safe to delete or archive with note.
   - **UNCLEAR** — cannot determine without human input. Describe what Q33NR/Q88N needs to clarify.

4. **Write the recommendation report** to:
   `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/.deia/hive/responses/YYYYMMDD-Q33N-ASSESS-UNARCHIVED-TASKS-RESPONSE.md`
   (use today's date)

## Deliverables

Response file with these sections (8-section response template from BOOT.md, plus an extra per-task table):

1. **Header** — task ID, status, model, date
2. **Files Modified** — should be empty except for the response file itself
3. **What Was Done** — enumeration and classification summary
4. **Test Results** — N/A (state why: read-only assessment task)
5. **Build Verification** — N/A
6. **Acceptance Criteria** — copy from this spec, check off
7. **Clock / Cost / Carbon** — all three
8. **Issues / Follow-ups** — anything unclear, recommended next tasks

Plus, embedded in section 3, a **per-task table** with columns:

| Task File | Classification | Response File (if any) | Broken Paths | Recommendation |
|-----------|---------------|------------------------|--------------|----------------|

And a **summary count**:
```
Total tasks assessed:   N
KEEP-AS-IS:             N
KEEP-REWRITE:           N  (list them explicitly — Q33NR will decide whether to rewrite)
OBSOLETE-COMPLETED:     N  (list them explicitly — Q33NR will archive)
OBSOLETE-SUPERSEDED:    N  (list them explicitly — Q33NR will archive or delete)
UNCLEAR:                N  (list them explicitly — needs Q88N input)
```

## Acceptance Criteria

- [ ] Every unarchived `.md` file under `.deia/hive/tasks/` is accounted for in the table
- [ ] Every task has a classification from the fixed list above
- [ ] For KEEP-REWRITE tasks, the specific broken paths are listed
- [ ] For OBSOLETE-COMPLETED tasks, the matching response file path is cited
- [ ] Summary counts are consistent with the table
- [ ] No task files were moved, renamed, or deleted by this spec
- [ ] Response file exists at the documented path with all 8 mandatory sections

## Constraints

- Read-only. Do not move, rename, or delete any task files.
- Do not run `inventory.py` or touch `FEATURE-INVENTORY.md`.
- Do not dispatch any bees.
- Do not write code.
- If you find more than 30 unarchived tasks, still assess all of them. If fewer than 15, also assess all of them. The approximate count is ~23.
- If a task file is itself malformed or unreadable, note it in UNCLEAR with a reason.

## Response File

`.deia/hive/responses/YYYYMMDD-Q33N-ASSESS-UNARCHIVED-TASKS-RESPONSE.md` (use today's date)

## Triage History
- 2026-04-12T18:52:40.091926Z — requeued (empty output)
- 2026-04-12T18:57:40.150450Z — requeued (empty output)
- 2026-04-12T19:02:40.236897Z — requeued (empty output)
