# TASK-MON-002: Monaco Named Volume I/O Adapter

**Status:** QUEUED
**Wave:** Wave B
**Assigned To:** BEE-001
**Date:** 2026-03-24
**Depends On:** TASK-MON-001 (component must exist)
**Blocks:** TASK-MON-004

---

## Context

TASK-MON-001 built the Monaco component shell with `getValue()` / `setValue()` stubs.
This task implements the file I/O adapter — wiring those stubs to the Named Volume System
so the editor can open and save files via `home://`, `mac://`, `vps://`, and `cloud://`
volume paths.

**Hard constraint (SPEC-MONACO-ADAPTER-001):** Zero direct filesystem access. No `fs`,
no `path`, no Node.js I/O in any Monaco-related file. All reads and writes go through
the hivenode storage API via the existing `filesystemAdapter`.

---

## Files to Read First

- C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\filesystemAdapter.ts
- C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\code-editor\MonacoApplet.tsx

---

## Scope

Build `browser/src/primitives/code-editor/monacoVolumeAdapter.ts` and wire it to `MonacoApplet`.

### What to build

1. **monacoVolumeAdapter.ts** — Volume I/O adapter
   ```ts
   interface MonacoVolumeAdapter {
     open(volumePath: string): Promise<string>   // returns file content
     save(volumePath: string, content: string): Promise<void>
     currentPath: string | null
   }
   ```
   - `open()` calls `/storage/read` on hivenode with the volume path
   - `save()` calls `/storage/write` on hivenode with the volume path + content
   - Follows exact pattern as `filesystemAdapter.ts` (audit it first)
   - Emits `FILE_OPENED` and `FILE_SAVED` events to Event Ledger after each operation
   - Three Currencies on every ledger event: CLOCK, COIN, CARBON

2. **Wire into MonacoApplet.tsx** (minimal addition)
   - Accept optional `volumePath` prop
   - On mount with `volumePath`: call `adapter.open()`, pass content to `setValue()`
   - Expose `saveFile()` method via ref that calls `adapter.save()`
   - Update `isDirty` to `false` after successful save

3. **File load bus event handler**
   - Listen for `file:selected` bus event (same event tree-browser emits)
   - On receipt: call `adapter.open(event.path)`, load content into editor
   - This is how the tree-browser → code-editor flow works

4. **Event Ledger emissions**
   ```ts
   // On FILE_OPENED
   { type: "FILE_OPENED", path: volumePath, size_bytes: content.length,
     clock: elapsed, coin: cost, carbon: co2e }

   // On FILE_SAVED
   { type: "FILE_SAVED", path: volumePath, size_bytes: content.length,
     clock: elapsed, coin: cost, carbon: co2e }
   ```

---

## File Locations

```
C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\code-editor\
  monacoVolumeAdapter.ts    ← new file (this task)
  MonacoApplet.tsx          ← minimal additions (volumePath prop, saveFile ref)
  __tests__\
    monacoVolumeAdapter.test.ts   ← vitest tests (TDD — write first)
```

---

## Constraints

- No file over 500 lines
- No direct filesystem access — `fs`, `path`, `require('fs')` are banned
- Follow `filesystemAdapter.ts` pattern exactly
- Mock the hivenode HTTP calls in tests (do NOT use real HTTP)
- CSS: `var(--sd-*)` only (no CSS expected in this task)
- TDD: write tests before implementation
- Do NOT change MonacoApplet.tsx beyond the minimal additions listed above

---

## Acceptance Criteria

- [ ] `adapter.open("home://projects/myfile.ts")` fetches content from hivenode and returns it
- [ ] `adapter.save("home://projects/myfile.ts", content)` writes content to hivenode
- [ ] `FILE_OPENED` and `FILE_SAVED` events appear in Event Ledger with all 3 currencies
- [ ] `file:selected` bus event loads file into editor automatically
- [ ] `isDirty` resets to `false` after successful save
- [ ] No `fs` or `path` imports present anywhere (grep check)
- [ ] All tests pass (minimum 10 tests)
- [ ] Existing MonacoApplet tests still pass (no regressions)

---

## Response Requirements -- MANDATORY

Write response file: `.deia/hive/responses/20260324-TASK-MON-002-RESPONSE.md`

Required sections (all 8):
1. **Header** — task ID, title, status, model, date
2. **Files Modified** — full absolute paths
3. **What Was Done** — concrete changes, not intent
4. **Test Results** — file names, pass/fail counts
5. **Build Verification** — last 5 lines of `vite build` output
6. **Acceptance Criteria** — each item marked [x] or [ ] with explanation
7. **Clock / Cost / Carbon** — all three, never omit
8. **Issues / Follow-ups** — blockers, edge cases, recommendations

YAML frontmatter required:
```yaml
features_delivered: [monaco-volume-adapter, file-selected-bus-handler]
features_modified: [code-editor-component]
features_broken: []
test_summary: "X/Y passing"
area_code: SHELL
```
