# TASK-BUG030B: Fix chatHistoryAdapter tests to match API contract

## Objective
Fix the chatHistoryAdapter.test.ts tests so they pass. The adapter implementation is correct, but the test expectations don't match the actual API behavior.

## Context

**Previous bee work:** BUG-030 added AUTO_EXPAND_ADAPTERS fix (correct) but wrote tests with wrong expectations.

**Current state:** 30 failed tests in chatHistoryAdapter.test.ts, 163 passing across tree-browser.

**Root cause:** Test mock expectations use hardcoded values that don't match the real API:
- Tests expect `conversationId: 'conv-1'` but API generates dynamic IDs like `'conv-1773866695314-3hhi8o'`
- Tests expect `volume: 'cloud://'` but API defaults to `'home://'`
- Tests expect `volumePreference: 'cloud-only'` but API defaults to `'both'`
- Tests expect badge `'🟢'` but API returns `'🔴'` (offline status when mocked)

**What's correct:**
- chatHistoryAdapter.ts implementation (no changes needed)
- AUTO_EXPAND_ADAPTERS in treeBrowserAdapter.tsx (already fixed)

**What needs fixing:**
- Test mock expectations in chatHistoryAdapter.test.ts

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\__tests__\chatHistoryAdapter.test.ts` — failing tests
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\chatHistoryAdapter.ts` — adapter (reference only, don't modify)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\terminal\chatApi.ts` — API contract (generateId(), defaults)

## Deliverables

- [ ] Fix test mock data to use dynamic conversationId pattern matching (not hardcoded 'conv-1')
- [ ] Fix test expectations for volume (use 'home://' default, not 'cloud://')
- [ ] Fix test expectations for volume_preference (use 'both' default, not 'cloud-only')
- [ ] Fix badge test expectations (use 'offline' → '🔴' for mocked volumeStatus)
- [ ] All chatHistoryAdapter.test.ts tests pass
- [ ] No changes to chatHistoryAdapter.ts source code
- [ ] No regressions in other tree-browser tests

## Test Requirements

- [ ] Run: `cd browser && npx vitest run --reporter=verbose src/primitives/tree-browser/adapters/__tests__/chatHistoryAdapter.test.ts`
- [ ] All 9 tests must pass
- [ ] Run full suite: `cd browser && npx vitest run src/primitives/tree-browser/`
- [ ] No regressions (should be 163+ passing)

## Specific Test Fixes Needed

### 1. Dynamic conversationId matching
Instead of:
```typescript
expect(conv.meta.conversationId).toBe('conv-1')
```
Use:
```typescript
expect(conv.meta.conversationId).toMatch(/^conv-\d+-[a-z0-9]{6}$/)
```

### 2. Volume defaults
Change mock data from:
```typescript
volume: 'cloud://',
volume_preference: 'cloud-only',
```
To:
```typescript
volume: 'home://',
volume_preference: 'both',
```

### 3. Badge expectations
Mock volumeStatus to return 'offline' (default for mocked state), then expect:
```typescript
expect(conv.badge!.text).toContain('🔴') // offline, not 🟢
```

OR mock volumeStatus to explicitly return 'online':
```typescript
vi.mocked(volumeStatus.getVolumeStatus).mockResolvedValue('online')
```

## Constraints
- No file over 500 lines (current file is 275 lines, under limit)
- No stubs
- **Do NOT modify chatHistoryAdapter.ts source code** — it's correct
- **Do NOT modify treeBrowserAdapter.tsx** — AUTO_EXPAND fix is already in place
- Only fix the test file

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260318-TASK-BUG030B-RESPONSE.md`

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

## Acceptance Criteria (from spec)

- [ ] Chat tree-browser shows conversation entries when they exist
- [ ] Date headers group conversations correctly
- [ ] Empty state shows placeholder text
- [ ] Tests pass
- [ ] No regressions in tree-browser tests

## Model Assignment
**sonnet** — Test fixing requires understanding API contracts and mock expectations.

## Priority
**P0** — Blocking queue progress.
