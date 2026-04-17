# BUG-031: Code explorer files return error on click -- COMPLETE (Additional Fixes)

**Status:** COMPLETE
**Model:** Sonnet 4.5
**Date:** 2026-03-17
**Note:** This is supplementary work to BUG-031-RESPONSE.md (Haiku). Both fixes are compatible.

## Files Modified

### My Changes (Sonnet):
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\filesystemAdapter.ts` — Added extension extraction for file nodes (lines 100-105)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\__tests__\fileExplorerIntegration.test.tsx` — Fixed MessageBus constructor calls to pass mockDispatch function parameter (5 tests)

### Previous Changes (Haiku):
- `treeBrowserAdapter.tsx` — Added `name` field and protocol-prefixed URI to `file:selected` event
- `treeBrowserAdapter.fileSelected.test.tsx` — 4 new tests for file:selected event data
- `SDEditor.fileLoading.test.tsx` — 4 new tests for file loading via bus event

## What I Did

While investigating BUG-031, I discovered two additional issues:

### Issue 1: Missing Extension Field
The filesystemAdapter was not extracting and storing the file extension in node.meta, causing test assertions to fail. I added logic to extract extensions from filenames:

```typescript
// Extract extension from filename
const lastDot = name.lastIndexOf('.');
if (lastDot > 0) {
  node.meta!.extension = name.slice(lastDot + 1); // e.g., "md" from "README.md"
}
```

### Issue 2: MessageBus Constructor Test Setup
The integration tests were calling `new MessageBus()` without required parameters, causing `this._dispatch is not a function` errors. Fixed by passing a mock dispatch function:

```typescript
const mockDispatch = vi.fn()
const bus = new MessageBus(mockDispatch)
```

## Test Results

**All tests passing:**
- ✅ 5 tests in `fileExplorerIntegration.test.tsx` (my fixes)
- ✅ 4 tests in `treeBrowserAdapter.fileSelected.test.tsx` (Haiku's work)
- ✅ 4 tests in `SDEditor.fileLoading.test.tsx` (Haiku's work)
- **Total: 13 tests passing**

## Combined Solution

The complete fix for BUG-031 now includes:
1. **Protocol prefix in URI** (Haiku) — `home://README.md` instead of `README.md`
2. **Name field in event** (Haiku) — `name: node.label` for display purposes
3. **Extension field in metadata** (Me) — `extension: "md"` extracted from filename
4. **Proper test infrastructure** (Me) — MessageBus constructed correctly in tests

## Architecture Verified

The file selection flow is now complete and tested:
1. User clicks file in Code explorer
2. TreeBrowserAdapter emits `file:selected` with uri, path, name, size, extension
3. SDEditor receives event, shows loading state using name field
4. SDEditor fetches content via `/storage/read?uri=${encodedUri}`
5. Backend returns file content or 404/400 error
6. SDEditor displays content or error message

## Smoke Test

```bash
cd browser && npx vitest run src/apps/__tests__/fileExplorerIntegration.test.tsx src/apps/__tests__/treeBrowserAdapter.fileSelected.test.tsx src/primitives/text-pane/__tests__/SDEditor.fileLoading.test.tsx
```

**Result:** ✅ All 13 tests passed

## Impact

**Compatibility:** Fully backward compatible with Haiku's changes
**Performance:** No impact
**Security:** No impact
**Breaking changes:** None
