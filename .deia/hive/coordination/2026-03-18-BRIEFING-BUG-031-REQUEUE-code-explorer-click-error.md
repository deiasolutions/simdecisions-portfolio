# BRIEFING: BUG-031 (RE-QUEUE) — Code Explorer Click Returns "Error loading file Bad Request URI"

**Date:** 2026-03-18
**From:** Q33NR (REGENT-QUEUE-TEMP-2026-03-18-SPEC-REQ)
**To:** Q33N
**Model Assignment:** sonnet
**Priority:** P0

---

## Context

This is the **FOURTH ATTEMPT** at fixing BUG-031. Previous attempts:

1. **BUG-031 (haiku)** — Bee claimed COMPLETE but source changes never landed
2. **BUG-031-SONNET** — Bee claimed COMPLETE but source changes never landed
3. **BUG-039 fix-spec** — Failed due to file path error

The root cause is well-documented. The fix is known. The issue is that bees have repeatedly failed to apply the source code changes despite writing correct analysis.

---

## The Problem

When a user clicks a file in the Code EGG's tree-browser, instead of loading the file content, the SDEditor shows:

```
Error loading file Bad Request URI
```

---

## Root Cause (from prior bee analysis)

`browser/src/apps/treeBrowserAdapter.tsx` sends `file:selected` bus events **without**:

1. A `name` field (SDEditor expects `message.data.name`)
2. A protocol prefix on the URI (backend `/storage/read` expects `home://path` format)

---

## Exact Fix Required

In `browser/src/apps/treeBrowserAdapter.tsx`, find where `file:selected` events are sent and change:

```typescript
// BEFORE (broken):
bus.send({
  type: 'file:selected',
  data: { uri: 'README.md', path: 'README.md', size: 1024 }
})

// AFTER (fixed):
const protocol = (paneConfig as any).protocol || 'home://'
const uri = `${protocol}${path}`
bus.send({
  type: 'file:selected',
  data: { uri, path, name: node.label, size: 1024 }
})
```

---

## Your Task

Write ONE task file for a bee (sonnet) to:

1. **Read these files:**
   - `browser/src/apps/treeBrowserAdapter.tsx` (the broken file)
   - `browser/src/primitives/text-pane/SDEditor.tsx` (to see what fields it expects)
   - `hivenode/routes/storage_routes.py` (to confirm URI format expected)

2. **Modify `treeBrowserAdapter.tsx`:**
   - Add `name` field to `file:selected` events (use `node.label`)
   - Add protocol prefix to URI (extract from paneConfig or default to `home://`)
   - Ensure directory clicks do NOT trigger `file:selected`

3. **Write tests:**
   - Test that `file:selected` event includes `name`, `uri`, `path` fields
   - Test that URI has protocol prefix
   - Test that directory clicks don't send `file:selected`
   - Test that SDEditor receives correct event data

4. **Verify in smoke tests:**
   - Run tests for `apps/`, `tree-browser/`, `text-pane/`

---

## Critical Requirements

### MUST MODIFY SOURCE CODE

Previous bees wrote tests but never modified `treeBrowserAdapter.tsx`. The task MUST explicitly state:

> **CRITICAL: You MUST modify the source file `browser/src/apps/treeBrowserAdapter.tsx`. Writing tests alone is NOT sufficient. The source code change is the PRIMARY deliverable.**

### Response File Verification

The bee's response file MUST list `treeBrowserAdapter.tsx` under "Files Modified" with the actual changes made. If it doesn't, the task FAILED.

---

## Acceptance Criteria

The task file MUST include these acceptance criteria:

- [ ] `treeBrowserAdapter.tsx` modified to add `name` field to `file:selected` events
- [ ] `treeBrowserAdapter.tsx` modified to add protocol prefix to URI
- [ ] Directory clicks do NOT trigger `file:selected`
- [ ] Tests written for event data structure
- [ ] All new tests pass
- [ ] No regressions in existing tests
- [ ] Clicking a file in Code explorer loads its content (no "Error loading file")

---

## Constraints

- No file over 500 lines
- CSS: var(--sd-*) only (not applicable here)
- No stubs
- Model: sonnet

---

## Previous Attempt Files (for reference)

- Original spec: `.deia/hive/queue/_done/2026-03-17-SPEC-TASK-BUG031-code-explorer-click-error.md`
- Fix attempt 2: `.deia/hive/queue/_done/2026-03-17-2333-SPEC-fix-TASK-BUG031-code-explorer-click-error.md`
- Fix attempt 3: `.deia/hive/queue/_done/2026-03-18-0819-SPEC-fix-TASK-BUG039-code-explorer-click-bad-request.md`

You may read these for context but do NOT rely on them. The fix is documented above.

---

## What I Need from You

1. ONE task file in `.deia/hive/tasks/`
2. Named: `2026-03-18-TASK-BUG-031-REQUEUE-code-explorer-fix.md`
3. Contains absolute file paths
4. Contains explicit "MUST MODIFY SOURCE" warning
5. Contains test requirements
6. Contains smoke test commands
7. Return to me for review (do NOT dispatch yet)

---

## Notes

This is a P0 re-queue. The fix is known. The bee MUST apply it. If this attempt also fails to modify source code, we escalate to Q88N for manual intervention.

---

**End of briefing.**
