# SPEC-WAVE0-A: Directory Structure + Task Template Update

## Priority
P0

## Model Assignment
haiku

## Depends On
None

## Intent

Create the directory structure required by PROCESS-DOC-DRIVEN-DEVELOPMENT and update the task file template to require IMPL doc generation.

## Files to Read First

.deia/processes/PROCESS-DOC-DRIVEN-DEVELOPMENT.md
.deia/hive/scripts/dispatch/dispatch.py

## Work Required

### 1. Create directories

Create the following directories. Add a .gitkeep to each so they commit:

  .deia/docs/spec/
  .deia/docs/impl/
  .deia/docs/test/
  .deia/docs/ir/
  .deia/hive/_code_complete/
  .deia/hive/_qa_review/
  .deia/hive/_q33n_review/
  .deia/hive/_needs_revision/

### 2. Update task file template

Find the canonical task file template used by Q33N and the dispatcher. Add the following section to the footer of every task file template:

---
## REQUIRED OUTPUT

In addition to code changes, produce:

1. IMPL-{task_id}.md in .deia/docs/impl/
   - YAML frontmatter: id, type, status, created, task_id, task_title,
     files_created, files_modified, clock_actual_minutes, coin_actual_usd,
     model, tokens_in, tokens_out
   - Sections: Summary, Deltas from Spec, Files Created, Files Modified,
     Key Decisions, Known Issues, Verification
   - If no deltas from spec: state "None - implementation matches spec exactly"

This is a DRAFT. A QA bee will review it.
Your task moves to _code_complete/ when finished, not _done/.
---

### 3. Create IMPL doc schema reference

Write .deia/docs/impl/SCHEMA.md containing the full IMPL document schema from PROCESS-DOC-DRIVEN-DEVELOPMENT section "IMPL Document Structure". This is the reference bees use when writing IMPL docs.

## Acceptance Criteria

- [ ] All 8 directories exist with .gitkeep
- [ ] Task file template contains REQUIRED OUTPUT section
- [ ] .deia/docs/impl/SCHEMA.md exists and matches the process spec schema
- [ ] No existing task files modified (template only, not instances)

## Constraints

- No file over 500 lines
- No stubs
- No git operations
- 8-section response file on completion

## Smoke Test

After completion:
```bash
# Verify directories exist
ls -la .deia/docs/spec/.gitkeep
ls -la .deia/docs/impl/.gitkeep
ls -la .deia/docs/test/.gitkeep
ls -la .deia/docs/ir/.gitkeep
ls -la .deia/hive/_code_complete/.gitkeep
ls -la .deia/hive/_qa_review/.gitkeep
ls -la .deia/hive/_q33n_review/.gitkeep
ls -la .deia/hive/_needs_revision/.gitkeep

# Verify IMPL schema exists
cat .deia/docs/impl/SCHEMA.md | head -20
```
