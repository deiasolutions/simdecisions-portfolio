# TASK-MON-002: Monaco Volume I/O Adapter

## Objective
Build the volume I/O adapter that connects Monaco editor to hivenode storage API endpoints for file read/write operations. Implement `open()` and `save()` functions, Event Ledger telemetry, and bus integration for `file:selected` events.

## Context

### What Exists
1. **Storage API** (hivenode/routes/storage_routes.py):
   - `GET /storage/read?uri=<volume-path>` → returns file content as octet-stream
   - `POST /storage/write` → takes `{ uri, content_base64 }`, writes file
   - Supports all volume protocols: home://, mac://, vps://, cloud://

2. **MonacoApplet.tsx** (MON-001 output):
   - React component with `forwardRef` exposing `getValue()`, `setValue()`, `isDirty`
   - Accepts `config` prop, `bus` prop for message routing
   - Currently no file I/O — content is static from `config.defaultValue`

3. **Event Ledger pattern** (useEventLedger.ts):
   - `emit(eventType, payload, extra)` with 3 currencies: CLOCK, COIN, CARBON
   - Used in FlowDesigner for tracking user actions
   - Batches events and flushes periodically

4. **Adapter pattern** (filesystemAdapter.ts):
   - `fetch()` with `AbortSignal.timeout(10_000)`
   - `import.meta.env.VITE_HIVENODE_URL` or default `http://localhost:8420`
   - Type-safe response interfaces

### What's Missing
- `monacoVolumeAdapter.ts` — the I/O adapter for file read/write
- Integration into `MonacoApplet.tsx` — wire adapter, handle `file:selected` bus event
- Event Ledger telemetry — track FILE_OPENED and FILE_SAVED events
- Tests — minimum 10 tests for adapter, ensure no regressions on MonacoApplet

### Architecture
- **Zero direct filesystem access** — all reads/writes go through hivenode storage API
- **Volume URIs** — all paths use volume protocol format (e.g., "home://projects/myfile.ts")
- **Base64 encoding** — `/storage/write` expects `content_base64` field
- **Bus events** — `file:selected` event from tree-browser triggers file load

---

## Files to Read First
- C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\filesystemAdapter.ts
- C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\storage_routes.py
- C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\telemetry\useEventLedger.ts
- C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\code-editor\MonacoApplet.tsx

---

## Deliverables

### File 1: monacoVolumeAdapter.ts
**Path:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\code-editor\monacoVolumeAdapter.ts`

**Functions:**

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

**Requirements:**
- Use `import.meta.env.VITE_HIVENODE_URL` or default to `http://localhost:8420`
- Use `fetch()` with `AbortSignal.timeout(10_000)` for all requests
- For `open()`: `GET /storage/read?uri=${encodeURIComponent(volumePath)}`
  - Response is octet-stream, use `.text()` to decode
  - Throw on 404 (FileNotFoundError), 400 (validation error), 500 (server error)
- For `save()`: `POST /storage/write` with body `{ uri: volumePath, content_base64: btoa(content) }`
  - Throw on network error or non-200 response
- Emit Event Ledger events using same pattern as useEventLedger (direct fetch to backend):
  - `FILE_OPENED` event after successful `open()` with all 3 currencies
  - `FILE_SAVED` event after successful `save()` with all 3 currencies
  - Event structure: `{ event_type, actor, timestamp, cost_tokens, cost_usd, cost_carbon, payload }`
  - Use `getUser()` from `browser/src/lib/auth.ts` for actor field
  - POST events to `/api/flow-events` endpoint (same as useEventLedger)

### File 2: MonacoApplet.tsx (minimal additions)
**Path:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\code-editor\MonacoApplet.tsx`

**Changes:**
1. Import `monacoVolumeAdapter` as `adapter`
2. Accept optional `volumePath` prop in `MonacoAppletProps`
3. On mount, if `volumePath` is provided:
   - Call `adapter.open(volumePath)`
   - Pass content to `setValue()` via ref interface
   - Handle errors gracefully (console.error, do not crash)
4. Expose `saveFile()` method via ref interface:
   - Calls `adapter.save(volumePath, getValue())`
   - Sets `isDirty` to false after successful save
   - Requires `volumePath` to be set (throw if missing)
5. Subscribe to `file:selected` bus event on mount:
   - Event payload: `{ path: string }` (volume path format)
   - On receipt: call `adapter.open(event.data.path)`, load content into editor
   - Update `volumePath` state to track current file
   - Handle errors gracefully

**Updated ref interface:**
```typescript
export interface MonacoAppletRef {
  getValue: () => string
  setValue: (content: string) => void
  saveFile: () => Promise<void>
  isDirty: boolean
}
```

### File 3: Tests
**Path:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\code-editor\__tests__\monacoVolumeAdapter.test.ts`

**Minimum 10 tests:**
1. `open()` fetches content from hivenode and returns it
2. `open()` throws on 404 (file not found)
3. `open()` throws on 400 (invalid path)
4. `open()` throws on 500 (server error)
5. `save()` writes content to hivenode with base64 encoding
6. `save()` throws on network error
7. `save()` sends POST to /storage/write with correct payload structure
8. FILE_OPENED event appears in Event Ledger after successful open
9. FILE_SAVED event appears in Event Ledger after successful save
10. Event Ledger events include all 3 currencies (CLOCK, COIN, CARBON)

**Additional tests (MonacoApplet integration):**
- `file:selected` bus event loads file into editor
- `saveFile()` ref method calls adapter.save() and resets isDirty
- MonacoApplet loads file on mount when volumePath prop is provided

Ensure existing MonacoApplet tests still pass (no regressions).

---

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All 10+ adapter tests pass
- [ ] MonacoApplet integration tests pass
- [ ] Existing MonacoApplet tests still pass (no regressions)
- [ ] Edge cases:
  - File not found (404)
  - Invalid volume path (400)
  - Server error (500)
  - Network timeout
  - Missing volumePath when calling saveFile()
  - Empty file content
  - Large file content (>1MB)

---

## Constraints
- No file over 500 lines (current MonacoApplet is 129 lines, adapter should be <200 lines)
- CSS: var(--sd-*) only (not applicable — no CSS changes)
- No stubs (every function fully implemented)
- No fs or path imports anywhere (grep check required)
- All file paths absolute in task docs

---

## Acceptance Criteria
- [ ] adapter.open("home://projects/myfile.ts") fetches content from hivenode and returns it
- [ ] adapter.save("home://projects/myfile.ts", content) writes content to hivenode as base64
- [ ] FILE_OPENED and FILE_SAVED events appear in Event Ledger with all 3 currencies
- [ ] file:selected bus event loads file into editor automatically
- [ ] saveFile() ref method resets isDirty to false after successful save
- [ ] No fs or path imports present anywhere (run: `grep -r "from 'fs'" "from 'path'" browser/src/primitives/code-editor/`)
- [ ] All tests pass (minimum 10 adapter tests + 3 integration tests)
- [ ] Existing MonacoApplet tests still pass (0 regressions)

---

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260324-TASK-MON-002-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.
