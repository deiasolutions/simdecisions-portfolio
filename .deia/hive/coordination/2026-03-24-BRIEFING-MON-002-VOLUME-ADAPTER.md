# BRIEFING: MON-002 — Monaco Volume I/O Adapter

**Date:** 2026-03-24
**From:** Q33NR (Regent)
**To:** Q33N (Queen Coordinator)
**Model:** sonnet
**Priority:** P1
**Depends On:** SPEC-MON-001-monaco-applet-component

---

## Objective

Build the volume I/O adapter that connects the Monaco editor to the Named Volume System. MON-001 built the Monaco component shell with getValue()/setValue(). This task implements the file I/O adapter that connects those methods to hivenode storage API endpoints (home://, mac://, vps://, cloud://). Zero direct filesystem access — all reads and writes go through `/storage/read` and `/storage/write` endpoints.

---

## Context

### What Exists
1. **Storage API endpoints** (hivenode/routes/storage_routes.py):
   - `GET /storage/read?uri=<volume-path>` → returns file content as octet-stream
   - `POST /storage/write` → takes `{ uri, content_base64 }`, writes file
   - Both endpoints support all volume protocols: home://, mac://, vps://, cloud://

2. **Existing adapter pattern** (filesystemAdapter.ts):
   - Calls `/storage/list` and `/storage/stat` for tree-browser
   - Pattern: async functions, fetch with AbortSignal.timeout, error handling
   - Returns typed responses

3. **Event Ledger pattern** (useEventLedger.ts):
   - `emit(eventType, payload, extra)` with 3 currencies: CLOCK, COIN, CARBON
   - Used in FlowDesigner for tracking user actions
   - Batches events and flushes periodically

### What's Missing
- **monacoVolumeAdapter.ts** — the I/O adapter for Monaco editor
- **Integration into MonacoApplet.tsx** — minimal additions to wire adapter
- **Bus event handler** — listen for `file:selected` from tree-browser
- **Tests** — minimum 10 tests for adapter, ensure no regressions on MonacoApplet

---

## Technical Requirements

### File 1: monacoVolumeAdapter.ts
Location: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\code-editor\monacoVolumeAdapter.ts`

Functions:
```typescript
/**
 * Opens a file from a volume path and returns its content.
 * @param volumePath - e.g., "home://projects/myfile.ts"
 * @returns file content as string
 * @throws if file not found or network error
 */
export async function open(volumePath: string): Promise<string>

/**
 * Saves content to a volume path.
 * @param volumePath - e.g., "home://projects/myfile.ts"
 * @param content - file content to write
 * @throws if write fails
 */
export async function save(volumePath: string, content: string): Promise<void>
```

Pattern to follow (from filesystemAdapter.ts):
- Use `import.meta.env.VITE_HIVENODE_URL` or default to `http://localhost:8420`
- Use `fetch()` with `AbortSignal.timeout(10_000)`
- For `/storage/read`: `GET /storage/read?uri=${encodeURIComponent(volumePath)}`
- For `/storage/write`: `POST /storage/write` with body `{ uri: volumePath, content_base64: btoa(content) }`
- Handle errors: 404 → FileNotFoundError, 400 → validation error, 500 → server error
- Emit Event Ledger events: `FILE_OPENED` and `FILE_SAVED` with all 3 currencies

### File 2: MonacoApplet.tsx (minimal additions)
Location: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\code-editor\MonacoApplet.tsx`

Changes:
1. Accept optional `volumePath` prop
2. On mount with volumePath: call `adapter.open(volumePath)`, pass content to `setValue()`
3. Expose `saveFile()` method via ref that calls `adapter.save()`
4. Update `isDirty` to false after successful save
5. Listen for `file:selected` bus event (same event tree-browser emits)
6. On receipt: call `adapter.open(event.path)`, load content into editor

### File 3: Tests
Location: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\code-editor\__tests__\monacoVolumeAdapter.test.ts`

Minimum 10 tests:
1. `open()` fetches content from hivenode and returns it
2. `open()` throws on 404 (file not found)
3. `open()` throws on 400 (invalid path)
4. `save()` writes content to hivenode
5. `save()` sends base64-encoded content
6. `save()` throws on network error
7. FILE_OPENED event appears in Event Ledger
8. FILE_SAVED event appears in Event Ledger
9. Event Ledger events include all 3 currencies (CLOCK, COIN, CARBON)
10. `file:selected` bus event loads file into editor

Additionally: ensure existing MonacoApplet tests still pass (no regressions).

---

## Acceptance Criteria
- [ ] adapter.open("home://projects/myfile.ts") fetches content from hivenode and returns it
- [ ] adapter.save("home://projects/myfile.ts", content) writes content to hivenode
- [ ] FILE_OPENED and FILE_SAVED events appear in Event Ledger with all 3 currencies
- [ ] file:selected bus event loads file into editor automatically
- [ ] isDirty resets to false after successful save
- [ ] No fs or path imports present anywhere (grep check)
- [ ] All tests pass (minimum 10 tests)
- [ ] Existing MonacoApplet tests still pass (no regressions)

---

## Files to Read First
- C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\filesystemAdapter.ts
- C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\storage_routes.py
- C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\telemetry\useEventLedger.ts
- C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\code-editor\MonacoApplet.tsx (MON-001 output)

---

## Constraints
- No file over 500 lines (modularize if needed)
- TDD: tests first, then implementation
- No stubs (every function fully implemented)
- All 8 sections required in response file
- CSS: var(--sd-*) only (not applicable here, but good to remember)

---

## Response File
`.deia/hive/responses/20260324-REGENT-QUEUE-TEMP-2026-03-24-SPEC-MON-002-RESPONSE.md`

---

## Next Steps for Q33N

1. Read the spec (already in your context)
2. Read the "Files to Read First" listed above
3. Write a single task file to `.deia/hive/tasks/`:
   - `2026-03-24-TASK-MON-002-monaco-volume-adapter.md`
4. Return to me (Q33NR) for review
5. After approval, dispatch a BEE (haiku or sonnet, your call based on complexity)

---

**Q33NR (Regent)**
