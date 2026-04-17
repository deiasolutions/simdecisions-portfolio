# TASK-MON-003: Monaco Relay Bus Integration

**Status:** QUEUED
**Wave:** Wave B (parallel with MON-002)
**Assigned To:** BEE-001
**Date:** 2026-03-24
**Depends On:** TASK-MON-001 (component must exist)
**Blocks:** TASK-MON-004

---

## Context

TASK-MON-001 exposed `getValue()` via ref. This task wires Monaco into the relay bus
per SPEC-MONACO-BUS-001 — emitting `CODE_CHANGED` events on content change and accepting
inbound code payloads from other panes.

This is the integration that makes Monaco a first-class ShiftCenter citizen: other panes
(the ai assistant, the log-viewer, a terminal) can push code into the editor and receive
code output from it via the bus. No pane talks directly to another pane's component.

Reference: SPEC-MONACO-BUS-001 (relay bus feedback loop), SPEC-PANE-MESSAGING-001 (envelope/links/bus).

---

## Scope

Build `browser/src/primitives/code-editor/monacoRelayBus.ts` and wire into `MonacoApplet`.

### What to build

1. **monacoRelayBus.ts** — Bus wiring module
   ```ts
   interface MonacoRelayBus {
     init(editorRef: MonacoEditorRef, nodeId: string, bus: RelayBus): void
     dispose(): void
   }
   ```

   **Outbound — `CODE_CHANGED` event:**
   - Debounced 300ms (do not emit on every keystroke)
   - Payload: `{ type: "CODE_CHANGED", nodeId, language, content, cursor_line, cursor_col }`
   - Only emit when content actually changes (compare hash, not reference)
   - Emit to relay_bus topic: `code-editor:${nodeId}`

   **Inbound — accept code payloads:**
   - Subscribe to `code:set` bus events targeting this nodeId
   - Payload: `{ type: "code:set", target: nodeId, content, language? }`
   - On receipt: call `setValue(content)`, optionally switch language
   - Do NOT emit a `CODE_CHANGED` event in response (would create a loop)

   **Inbound — `code:save` command:**
   - Subscribe to `code:save` bus events targeting this nodeId
   - On receipt: call `saveFile()` (delegates to Volume adapter)

2. **Wire into MonacoApplet.tsx** (minimal)
   - On mount: `monacoRelayBus.init(editorRef, nodeId, bus)`
   - On unmount: `monacoRelayBus.dispose()`

3. **Event Ledger emissions**
   ```ts
   // On CODE_CHANGED (debounced, not every keystroke)
   { type: "CODE_CHANGED", nodeId, language, line_count: n,
     clock: elapsed, coin: cost, carbon: co2e }
   ```

4. **RTD publication**
   - Publish RTD on every `CODE_CHANGED`: `{ metric_key: "code:line_count", value: n, unit: "lines" }`
   - Publish RTD on language switch: `{ metric_key: "code:language", value: language }`

---

## File Locations

```
browser/src/primitives/code-editor/
  monacoRelayBus.ts         ← new file (this task)
  MonacoApplet.tsx          ← minimal additions (init/dispose calls)
  __tests__/
    monacoRelayBus.test.ts  ← vitest tests (TDD — write first)
```

---

## Constraints

- No file over 500 lines
- Mock the bus in tests — do NOT use real WebSocket or HTTP
- Debounce must be tested (fast-type scenario: only 1 event emitted)
- Loop guard must be tested (`code:set` does not re-emit `CODE_CHANGED`)
- TDD: write tests before implementation
- Do NOT change MonacoApplet.tsx beyond the minimal additions listed above

---

## Acceptance Criteria

- [ ] `CODE_CHANGED` emitted after 300ms debounce on content change
- [ ] `CODE_CHANGED` NOT emitted when content is set programmatically via `code:set`
- [ ] `code:set` payload loads content into editor
- [ ] `code:save` triggers volume save (delegates correctly)
- [ ] RTD published on `CODE_CHANGED` with `code:line_count`
- [ ] `CODE_CHANGED` appears in Event Ledger with all 3 currencies
- [ ] All tests pass (minimum 10 tests)
- [ ] Existing MON-001 tests still pass (no regressions)

---

## Response Requirements -- MANDATORY

Write response file: `.deia/hive/responses/20260324-TASK-MON-003-RESPONSE.md`

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
features_delivered: [monaco-relay-bus, code-changed-event, rtd-publication]
features_modified: [code-editor-component]
features_broken: []
test_summary: "X/Y passing"
area_code: SHELL
```
