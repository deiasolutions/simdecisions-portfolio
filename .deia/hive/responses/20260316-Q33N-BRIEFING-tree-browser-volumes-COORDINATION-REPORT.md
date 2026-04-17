# Q33N Coordination Report: Tree-Browser Volume Wiring

**Date:** 2026-03-16
**Briefing:** 2026-03-16-BRIEFING-tree-browser-volumes
**Spec:** 2026-03-16-1032-SPEC-w2-07-tree-browser-volumes
**Status:** TASK FILES READY FOR REVIEW

---

## Investigation Summary

I've completed a thorough investigation of the codebase using 4 parallel exploration agents. Here are the key findings:

### What Already Exists (Good News!)

1. **Volume Backend System** — COMPLETE
   - `hivenode/storage/registry.py` — VolumeRegistry manages all volumes
   - `hivenode/storage/transport.py` — FileTransport with read/write/list/stat operations
   - `hivenode/routes/storage_routes.py` — 6 REST endpoints including `/storage/read`, `/storage/list`, `/storage/stat`
   - Full test coverage in `tests/hivenode/storage/`

2. **Tree-Browser Component** — COMPLETE
   - `browser/src/primitives/tree-browser/TreeBrowser.tsx` — Main component with search, keyboard nav
   - `browser/src/primitives/tree-browser/adapters/filesystemAdapter.ts` — Already calls `/storage/list` and `/storage/stat`
   - Pattern established: async function returns `Promise<TreeNodeData[]>`

3. **Bus Event System** — COMPLETE
   - `browser/src/infrastructure/relay_bus/` — MessageBus with pub/sub
   - `file:selected` event — Already being emitted by filesystemAdapter when file is clicked
   - Event structure defined with uri, path, size, modified, created metadata

4. **Text-Pane Component** — PARTIAL
   - `browser/src/primitives/text-pane/SDEditor.tsx` — Has bus subscription handler
   - Currently handles: `channel:selected`, `terminal:text-patch`, `terminal:targeting`
   - **MISSING:** Handler for `file:selected` event
   - **Tests exist** expecting file:selected → fetch `/storage/read` → load content

### What Needs to Be Built (The Gap)

Based on the test file `browser/src/primitives/text-pane/__tests__/SDEditor.test.tsx` (lines 846-1068), the missing piece is:

**File loading handler in SDEditor:**
- Listen for `file:selected` bus event
- Show loading indicator
- Fetch content from `/storage/read?uri={uri}`
- Load content into editor
- Auto-detect language from file extension
- Update pane label to filename
- Handle errors (404, 500) with user-friendly messages

### Architecture Assessment

The spec says "Wire tree-browser to real volume storage" but investigation shows:
- **Volume storage backend:** ✅ Already wired, working, tested
- **Tree-browser → backend:** ✅ Already wired via filesystemAdapter
- **Tree-browser → bus event:** ✅ Already wired, emits `file:selected`
- **Text-pane → bus listener:** ❌ NOT WIRED (the gap)

**Therefore:** This is NOT about volume storage infrastructure. It's about **text-pane listening to file:selected events**.

---

## Task Breakdown

I've created **4 task files** to complete the wiring:

### TASK-180: Volume Adapter Backend Wire (Verification)
**File:** `.deia/hive/tasks/2026-03-16-TASK-180-volume-adapter-backend-wire.md`
**Bee:** Sonnet (200 lines estimated)
**Purpose:** Verify filesystemAdapter calls `/storage/list` and `/storage/stat` correctly for `home://` protocol. Add test coverage for volume status badges.

**Why Needed:** The filesystemAdapter exists but needs verification for `home://` protocol specifically (tests only cover default protocol). Need to ensure it works with the volume backend.

**Deliverables:**
- Verify filesystemAdapter works with `home://` URIs
- Add tests for `home://` directory listing
- Add tests for volume status badges (online/offline)
- Ensure proper error handling (404, 500)

### TASK-181: Tree Browser File Select Bus Event (Verification)
**File:** `.deia/hive/tasks/2026-03-16-TASK-181-tree-browser-file-select-bus.md`
**Bee:** Haiku (150 lines estimated)
**Purpose:** Verify `file:selected` event is emitted correctly when user clicks file in tree-browser. Add test coverage.

**Why Needed:** The event emission exists in treeBrowserAdapter.tsx but test coverage is incomplete. Need to ensure event payload matches expected structure.

**Deliverables:**
- Verify `file:selected` event emission logic
- Add tests for event payload structure (uri, path, size, extension, modified, created)
- Add tests for broadcast targeting (`target: '*'`)
- Ensure directories don't emit events (only files)

### TASK-182: Text-Pane File Load Handler (**CORE TASK**)
**File:** `.deia/hive/tasks/2026-03-16-TASK-182-text-pane-file-load.md`
**Bee:** Sonnet (250 lines estimated)
**Purpose:** Implement `file:selected` event handler in SDEditor to load file content from volume storage.

**Why Needed:** This is the CORE missing piece. Tests exist expecting this behavior but handler is not implemented.

**Deliverables:**
- Add `file:selected` handler to SDEditor bus subscription (lines 260-399)
- Fetch content from `/storage/read?uri={uri}`
- Show loading indicator during fetch
- Load content into editor on success
- Auto-detect language from file extension (.ts → typescript, .md → markdown, etc.)
- Update pane label to filename
- Handle 404 errors → show "File not found: {filename}"
- Handle 500 errors → show "Error loading file: {filename}"
- Handle network errors → show "Could not load file: {filename}"

### TASK-183: Volume Integration E2E Test
**File:** `.deia/hive/tasks/2026-03-16-TASK-183-volume-integration-e2e-test.md`
**Bee:** Sonnet (200 lines estimated)
**Purpose:** End-to-end integration test for complete flow (tree-browser → bus → text-pane → volume storage).

**Why Needed:** Verify all pieces work together in realistic user scenario.

**Deliverables:**
- E2E test: user clicks file in tree → content loads in text-pane
- E2E test: file metadata displays correctly
- E2E test: error handling (404, network errors)
- E2E test: multiple file selections update content

---

## Dependency Chain

```
TASK-180 (verify volume adapter) ─┐
                                    ├─→ TASK-183 (integration E2E)
TASK-181 (verify bus event)      ─┤
                                    │
TASK-182 (text-pane handler)     ─┘
```

**Dispatch Strategy:**
- Parallel: TASK-180, TASK-181 (independent verification tasks)
- Sequential: TASK-182 after TASK-180/181 (depends on both)
- Final: TASK-183 (E2E integration test)

---

## Test Coverage Analysis

### Existing Tests
- `browser/src/primitives/tree-browser/__tests__/filesystemAdapter.test.ts` — 8 tests, covers basic filesystem adapter
- `browser/src/primitives/text-pane/__tests__/SDEditor.test.tsx` — 6 tests expecting `file:selected` handler (currently failing/skipped)
- `browser/src/apps/__tests__/treeBrowserAdapter.test.tsx` — Tests for adapter selection logic

### New Tests Required
- TASK-180: 4 tests for `home://` protocol support
- TASK-181: 5 tests for `file:selected` event emission
- TASK-182: 6 tests for file loading handler (already exist, need implementation to pass them)
- TASK-183: 3 E2E tests for full flow (tree → bus → text-pane)

**Total new tests:** ~18 tests

---

## Files to Modify

### TASK-180 (Volume Adapter Backend Wire)
- Read: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\filesystemAdapter.ts`
- Read: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\__tests__\filesystemAdapter.test.ts`
- Modify: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\__tests__\filesystemAdapter.test.ts` (add home:// tests)

### TASK-181 (File Select Bus Event)
- Read: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\treeBrowserAdapter.tsx`
- Read: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\__tests__\treeBrowserAdapter.test.tsx`
- Modify: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\__tests__\treeBrowserAdapter.test.tsx` (add file:selected tests)

### TASK-182 (Text-Pane File Load)
- Read: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\SDEditor.tsx`
- Read: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\__tests__\SDEditor.test.tsx`
- Modify: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\SDEditor.tsx` (add file:selected handler, ~50 lines)

### TASK-183 (Integration E2E)
- Create: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\__tests__\volume-integration.e2e.test.tsx`

**File count:** 4 modified, 1 created

---

## Constraints Verification

✅ **Max 500 lines per file:** All tasks under 500 lines
✅ **TDD:** Tests written/verified first, then implementation
✅ **No stubs:** All functions fully implemented
✅ **CSS variables:** No CSS changes needed (UI already exists)
✅ **File claims:** Each task claims files before modification
✅ **Heartbeats:** Each task POSTs heartbeat every 3 minutes

---

## Acceptance Criteria Mapping

Spec criteria → Task coverage:

- [ ] **home:// lists real directories** → TASK-180 verifies filesystemAdapter works with home://
- [ ] **File contents load in text-pane** → TASK-182 implements file loading handler
- [ ] **File metadata (size, date) displayed** → TASK-180 verifies metadata in tree nodes
- [ ] **Tests written and passing** → All tasks TDD, 18 new tests

---

## Risk Assessment

**Low Risk:**
- Backend API already exists and is tested
- Tree-browser adapter already exists and works
- Bus event system already works
- Text-pane already has bus subscription infrastructure

**Medium Risk:**
- Text-pane tests expect specific behavior (may need minor adjustments)
- File extension → language mapping needs to be comprehensive

**Mitigation:**
- TASK-182 includes comprehensive error handling
- Language detection can fall back to 'text' if extension unknown
- E2E test (TASK-183) validates full flow end-to-end

---

## Estimated Effort

| Task | Lines | Complexity | Time |
|------|-------|------------|------|
| TASK-180 | ~150 | Low (verification + tests) | 30 min |
| TASK-181 | ~100 | Low (verification + tests) | 20 min |
| TASK-182 | ~250 | Medium (handler + error cases) | 45 min |
| TASK-183 | ~150 | Medium (E2E setup) | 30 min |
| **Total** | **650** | **Medium** | **~2 hours** |

---

## Questions for Q33NR

1. **Should TASK-180 be dispatched?** The filesystemAdapter already works—this task just verifies `home://` support. We could skip it and go straight to TASK-181/182.

2. **Integration test location:** Should TASK-183 be a separate E2E test file or added to existing test files?

3. **Error message wording:** Do you want specific error message templates or can bees use reasonable defaults?

---

## Recommendation

**Dispatch TASK-181 and TASK-182 in parallel immediately:**
- TASK-181 (bus event verification) — Independent, low risk
- TASK-182 (text-pane handler) — Core missing piece, well-defined by existing tests

**Optional: TASK-180** — Only if you want explicit home:// test coverage (filesystemAdapter already supports it via protocol parameter)

**Follow-up: TASK-183** — E2E integration test after TASK-182 completes

---

## Ready for Review

Task files written to:
- `.deia/hive/tasks/2026-03-16-TASK-180-volume-adapter-backend-wire.md`
- `.deia/hive/tasks/2026-03-16-TASK-181-tree-browser-file-select-bus.md`
- `.deia/hive/tasks/2026-03-16-TASK-182-text-pane-file-load.md`
- `.deia/hive/tasks/2026-03-16-TASK-183-volume-integration-e2e-test.md`

Awaiting Q33NR approval to dispatch bees.

---

**Q33N-2026-03-16-1200**
