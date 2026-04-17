# TASK-BUG-031-REQUEUE: Fix Code Explorer File Selection (Fourth Attempt)

## Objective
Modify `browser/src/apps/treeBrowserAdapter.tsx` to send complete `file:selected` events with proper `name` field and protocol-prefixed URIs so that clicking files in the Code EGG loads their content instead of showing "Error loading file Bad Request URI".

## Context

**This is the FOURTH attempt at fixing BUG-031. Three previous attempts failed because bees wrote tests but NEVER modified the source code.**

### Root Cause (Confirmed)

When a user clicks a file in the Code EGG's tree-browser (filesystem adapter), the `file:selected` bus event is missing:

1. **`name` field** — SDEditor expects `message.data.name` to display in the tab label
2. **Protocol prefix on URI** — Backend `/storage/read` expects URIs like `home://path/to/file.md`, not just `path/to/file.md`

### Current Broken Code

In `browser/src/apps/treeBrowserAdapter.tsx` lines 189-206, the filesystem adapter sends:

```typescript
bus.send({
  type: 'file:selected',
  sourcePane: paneId,
  target: '*',
  nonce: `${Date.now()}-${Math.random()}`,
  timestamp: new Date().toISOString(),
  data: {
    uri: node.meta.path as string,           // ❌ Missing protocol prefix
    path: node.meta.path as string,
    // ❌ Missing name field
    size: node.meta.size as number | undefined,
    extension: node.meta.extension as string | undefined,
    created: node.meta.created as string | undefined,
    modified: node.meta.modified as string | undefined,
  },
})
```

### What SDEditor Expects

`browser/src/primitives/text-pane/SDEditor.tsx` lines 312-353:

```typescript
if (message.type === 'file:selected') {
  const { uri, name } = message.data || {}  // ✅ Expects both uri AND name
  if (uri) {
    setLabel(`Loading ${name || 'file'}...`)  // ✅ Uses name for display
    // ... fetches from /storage/read?uri=${encodedUri}
```

### What Backend Expects

`hivenode/routes/storage_routes.py` line 58-66:

```python
@router.get("/read")
async def read_file(
    uri: str = Query(...),  # ✅ Expects protocol-prefixed URI like home://path
    ...
):
    content = transport.read(uri)  # ✅ FileTransport requires protocol
```

## Files to Read First

1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\treeBrowserAdapter.tsx` (lines 189-206)
2. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\SDEditor.tsx` (lines 312-353)
3. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\storage_routes.py` (lines 57-68)
4. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\code.egg.md` (to understand paneConfig)

## Deliverables

### PRIMARY DELIVERABLE — SOURCE CODE MODIFICATION

**CRITICAL: You MUST modify `browser/src/apps/treeBrowserAdapter.tsx`. This is the PRIMARY deliverable. Writing tests alone is NOT sufficient.**

**The source code change MUST appear in your response file under "Files Modified" with the actual diff/changes shown.**

### Required Changes to `treeBrowserAdapter.tsx`

In the `handleSelect` callback, modify the `adapter === 'filesystem'` block (currently lines 189-206):

1. **Add `name` field** to `data` object using `node.label`
2. **Add protocol prefix** to `uri` field:
   - Extract protocol from `paneConfig.protocol` OR default to `'home://'`
   - Prepend protocol to path: `const uri = \`\${protocol}\${path}\``
3. **Ensure directory clicks don't send `file:selected`** (already correct: checks `!node.children`)

### Example Fixed Code

```typescript
// Filesystem adapter: broadcast file:selected via bus (only for files, not directories)
if (adapter === 'filesystem' && bus && node.meta?.path && !node.children) {
  const path = node.meta.path as string
  const protocol = (paneConfig as any).protocol || 'home://'
  const uri = `${protocol}${path}`

  bus.send({
    type: 'file:selected',
    sourcePane: paneId,
    target: '*',
    nonce: `${Date.now()}-${Math.random()}`,
    timestamp: new Date().toISOString(),
    data: {
      uri,                                    // ✅ Protocol-prefixed
      path,                                   // ✅ Original path
      name: node.label,                       // ✅ ADDED: Display name
      size: node.meta.size as number | undefined,
      extension: node.meta.extension as string | undefined,
      created: node.meta.created as string | undefined,
      modified: node.meta.modified as string | undefined,
    },
  })
}
```

### Test Requirements

Write test file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\__tests__\treeBrowserAdapter-file-selection.test.tsx`

Tests MUST verify:

1. **`file:selected` event includes `name` field** (set to `node.label`)
2. **`file:selected` event includes protocol-prefixed `uri`** (e.g., `home://README.md`)
3. **`file:selected` event includes original `path`** (without protocol)
4. **Directory clicks do NOT send `file:selected`** (only files)
5. **File clicks DO send `file:selected`** (when node has no children)
6. **Protocol defaults to `home://`** when not in paneConfig
7. **Protocol can be overridden** via `paneConfig.protocol`

## Smoke Test Commands

After implementation, run:

```bash
# Test the modified adapter
cd browser && npx vitest run src/apps/__tests__/treeBrowserAdapter-file-selection.test.tsx

# Test tree-browser primitive (no regressions)
cd browser && npx vitest run src/primitives/tree-browser/

# Test SDEditor (should still work with new event structure)
cd browser && npx vitest run src/primitives/text-pane/

# Full browser test suite
cd browser && npx vitest run
```

## Acceptance Criteria

- [x] `browser/src/apps/treeBrowserAdapter.tsx` **MODIFIED** to add `name` field to `file:selected` events
- [x] `browser/src/apps/treeBrowserAdapter.tsx` **MODIFIED** to add protocol prefix to `uri` field
- [x] Directory clicks do NOT trigger `file:selected` (verify existing `!node.children` check)
- [x] Test file created with 7+ tests covering all requirements
- [x] All new tests pass
- [x] No regressions in existing tests (`tree-browser/`, `text-pane/`, `apps/`)
- [x] Manual verification: Clicking a file in Code EGG loads its content (no "Error loading file Bad Request URI")

## Constraints

- No file over 500 lines (treeBrowserAdapter.tsx is currently 253 lines)
- CSS: `var(--sd-*)` only (not applicable for this task)
- No stubs (all functions fully implemented)
- TDD: Write tests FIRST, then apply the fix
- Model: sonnet

## Priority

P0 — This blocks Code EGG functionality

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260318-TASK-BUG-031-REQUEUE-RESPONSE.md`

The response MUST contain these 8 sections:

1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — MUST list `treeBrowserAdapter.tsx` with actual changes made
3. **What Was Done** — bullet list including "Modified treeBrowserAdapter.tsx to add name field and protocol prefix"
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy from above, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

## CRITICAL VERIFICATION CHECKLIST

Before marking this task COMPLETE, verify:

- [ ] Did you modify `treeBrowserAdapter.tsx`? (Not just tests — the actual source file?)
- [ ] Does your response file list `treeBrowserAdapter.tsx` under "Files Modified"?
- [ ] Does your response file show the actual changes made to `treeBrowserAdapter.tsx`?
- [ ] Did you add the `name` field to the `data` object?
- [ ] Did you add the protocol prefix to the `uri` field?
- [ ] Did you write and run tests?
- [ ] Do all tests pass?

**If you answer NO to ANY of these questions, the task has FAILED and must be restarted.**

## Notes from Previous Attempts

1. **BUG-031 (haiku)** — Bee wrote tests but NEVER modified `treeBrowserAdapter.tsx`
2. **BUG-031-SONNET** — Bee wrote tests but NEVER modified `treeBrowserAdapter.tsx`
3. **BUG-039 fix-spec** — Failed due to spec file path error in queue runner

**This time, the PRIMARY deliverable is the SOURCE CODE CHANGE. Tests are secondary verification.**

---

**End of task file.**
