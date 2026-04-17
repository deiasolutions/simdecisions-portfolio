# TASK-BL-956-A: EGG Registry Population

## Objective
Import all 20 EGG files from `eggs/` directory and inflate them into the EGG registry, replacing the current empty TODO implementation in `getEggRegistry()`.

## Context

**Current state:** `getEggRegistry()` in `browser/src/eggs/index.ts` returns an empty registry with TODO comments.

**What needs to happen:**
1. Import all 20 `*.egg.md` files using Vite's `?raw` import syntax
2. Parse each using `parseEggMd()`
3. Inflate each using `inflateEgg()`
4. Build registry map `{ [eggId]: EggIR }`
5. Remove all TODO comments

**Available EGG files (20 total):**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\playground.egg.md`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\monitor.egg.md`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\kanban.egg.md`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\ship-feed.egg.md`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\apps.egg.md`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\login.egg.md`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\processing.egg.md`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\sim.egg.md`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\constitution.egg.md`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\build-monitor.egg.md`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\code-2026-03-24.egg.md`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\turtle-draw.egg.md`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\home.egg.md`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\chat.egg.md`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\primitives.egg.md`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\canvas.egg.md`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\hodeia.egg.md`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\code.egg.md`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\efemera.egg.md`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\canvas2.egg.md`

**Example pattern (from existing codebase):**
```typescript
import codeRaw from '../../eggs/code.egg.md?raw'
import chatRaw from '../../eggs/chat.egg.md?raw'
// ... import all 20

export function getEggRegistry(): EggRegistry {
  if (_registry) return _registry

  _registry = {}

  // Parse and inflate synchronously
  const entries = [
    ['code', codeRaw],
    ['chat', chatRaw],
    // ... all 20 entries
  ] as const

  for (const [id, raw] of entries) {
    const parsed = parseEggMd(raw)
    _registry[id] = await inflateEgg(parsed) // Wait, inflateEgg is async!
  }

  return _registry
}
```

**IMPORTANT:** `inflateEgg()` is async, but `getEggRegistry()` is currently sync. You must either:
- Make `getEggRegistry()` async and update all callers, OR
- Keep the sync version and use `getEggRegistryAsync()` for initialization, OR
- Make inflation synchronous by removing the async from `inflateEgg()` (check if it's truly async or just has async signature)

After reviewing `inflateEgg()` code, it only calls `await loadConfigEgg()` which returns `null` (placeholder). The function doesn't actually need to be async yet. You can call `inflateEgg()` without await for now, or refactor it to be sync.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\eggs\index.ts` (current implementation)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\eggs\parseEggMd.ts` (parser)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\eggs\eggInflater.ts` (inflater)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\eggs\types.ts` (types)

## Deliverables
- [ ] Import all 20 EGG files using `?raw` syntax
- [ ] Build entries array with `[eggId, rawContent]` tuples
- [ ] Parse each EGG with `parseEggMd()`
- [ ] Inflate each EGG with `inflateEgg()` (handle async/sync correctly)
- [ ] Populate `_registry` map
- [ ] Remove all TODO comments from `getEggRegistry()`
- [ ] Keep `getEggRegistryAsync()` for future use
- [ ] Verify all 20 EGGs load without errors

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Edge cases:
  1. Registry returns all 20 EGGs
  2. Registry caches after first call (returns same object)
  3. Each EGG has correct `egg` ID matching its key
  4. Each EGG has valid `displayName` and `description`
  5. `clearEggRegistry()` resets cache correctly
  6. Invalid EGG throws parse error (test with malformed YAML)
  7. Missing layout block throws error
  8. `getEggRegistryAsync()` returns same registry as sync version
  9. Registry contains EGGs with different layout types (split, pane, tab-group)

**Minimum 9 tests required.**

## Constraints
- No file over 500 lines (current file is 119 lines, imports will add ~40 lines)
- CSS: var(--sd-*) only (N/A for this task)
- No stubs — every EGG must be fully parsed and inflated
- No hardcoded colors (N/A)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260325-TASK-BL-956-A-RESPONSE.md`

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
