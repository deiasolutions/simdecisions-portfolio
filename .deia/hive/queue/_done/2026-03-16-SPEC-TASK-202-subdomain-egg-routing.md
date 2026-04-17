# TASK-202: Add canvas.shiftcenter.com mapping and comprehensive EGG routing tests

## Objective
Add `canvas.shiftcenter.com` → `canvas` hostname mapping to `eggResolver.ts` and write 10+ tests to verify subdomain-based EGG routing, query param override, and fallback behavior.

## Context

**Current State:**
- File: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\eggs\eggResolver.ts`
- Hostname mappings exist at lines 87-100
- Query param support (`?egg=`) already implemented (line 119)
- Fallback to `'chat'` already implemented (line 100)
- Available EGG files: `chat`, `canvas`, `code`, `monitor`, `sim`, `apps`, `login`, etc.
- Missing EGG files: `pm.egg.md` (does not exist)

**What's Missing:**
- `canvas.shiftcenter.com` not in hostname map
- No test coverage for EGG resolver logic

**How it works:**
1. `resolveCurrentEgg()` checks `?egg=` URL param first (priority 1)
2. If no param, checks pathname (priority 2)
3. If no pathname, calls `resolveEggFromHostname()` (priority 3)
4. `resolveEggFromHostname()` uses hardcoded `hostnameMap` (lines 87-98) or routing config
5. Unknown hostnames fall back to `'chat'` (line 100)

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\eggs\eggResolver.ts` (file to modify)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\useEggInit.ts` (to understand how resolver is called)

## Deliverables
- [ ] Add `'canvas.shiftcenter.com': 'canvas'` to `hostnameMap` in `eggResolver.ts` (line ~92)
- [ ] Verify all other hostname mappings match spec:
  - `chat.efemera.live` → `chat` ✓ (already exists)
  - `code.shiftcenter.com` → `code` ✓ (already exists)
  - `pm.shiftcenter.com` → `pm` ✓ (already exists)
  - `dev.shiftcenter.com` → `chat` ✓ (already exists)
  - `localhost:5173` → `chat` ✓ (already exists)
  - `canvas.shiftcenter.com` → `canvas` ✗ (ADD THIS)
- [ ] Create test file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\eggs\__tests__\eggResolver.test.ts`
- [ ] Write 10+ test cases (see Test Requirements below)
- [ ] All tests pass
- [ ] No other changes to `eggResolver.ts` (query param and fallback logic already work)

## Test Requirements

**Test file:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\eggs\__tests__\eggResolver.test.ts`

Write tests FIRST (TDD). Minimum 10 test cases covering:

### Query Param Override (3 tests)
1. `?egg=canvas` param overrides hostname → returns `'canvas'`
2. `?egg=monitor` param overrides hostname → returns `'monitor'`
3. `?egg=sim` param overrides any hostname (e.g., `pm.shiftcenter.com?egg=sim`) → returns `'sim'`

### Hostname Mapping (6 tests)
4. `chat.efemera.live` hostname → returns `'chat'`
5. `code.shiftcenter.com` hostname → returns `'code'`
6. `canvas.shiftcenter.com` hostname → returns `'canvas'`
7. `pm.shiftcenter.com` hostname → returns `'pm'`
8. `dev.shiftcenter.com` hostname → returns `'chat'`
9. `localhost:5173` hostname → returns `'chat'`

### Fallback (1 test)
10. Unknown hostname (e.g., `unknown.example.com`) → returns `'chat'` (fallback)

### Pathname-based Routing (1 test)
11. Pathname `/canvas` (with any hostname) → returns `'canvas'`

### Edge Cases (optional, bonus)
- Empty hostname → returns `'chat'`
- Hostname with port (`localhost:3000`) → returns `'chat'`
- Mixed case query param (`?Egg=canvas`) → case sensitivity check

**Test setup:**
- Mock `window.location` to control hostname, pathname, search params
- Test both `resolveEggFromHostname()` and `resolveCurrentEgg()` functions
- Use `describe` blocks to organize test categories
- Use `beforeEach` to reset mocks between tests

**Example test structure:**
```typescript
import { describe, it, expect, beforeEach, vi } from 'vitest'
import { resolveEggFromHostname, resolveCurrentEgg } from '../eggResolver'

describe('eggResolver', () => {
  describe('resolveEggFromHostname', () => {
    it('returns "chat" for chat.efemera.live', () => {
      expect(resolveEggFromHostname('chat.efemera.live')).toBe('chat')
    })
    // ... more tests
  })

  describe('resolveCurrentEgg', () => {
    beforeEach(() => {
      delete (window as any).location
      // Mock window.location
    })

    it('returns EGG from ?egg= param when present', () => {
      // Mock window.location with ?egg=canvas
      // expect(resolveCurrentEgg()).toBe('canvas')
    })
    // ... more tests
  })
})
```

## Constraints
- No file over 500 lines (current file is 133 lines — plenty of room)
- No hardcoded colors (N/A — logic only, no UI)
- No stubs (all functions already implemented, just add one mapping line)
- TDD: tests first, then add the one-line mapping change
- Do NOT modify error handling in `useEggInit` (already exists)
- Do NOT modify query param logic (already works)
- Do NOT modify fallback logic (already works)

## Acceptance Criteria
- [ ] `canvas.shiftcenter.com` added to hostname map
- [ ] All existing mappings verified (no changes needed)
- [ ] Test file created with 10+ passing tests
- [ ] All tests pass: `cd browser && npx vitest run src/eggs/__tests__/eggResolver.test.ts`
- [ ] No regressions in existing shell/EGG loading

## Dependencies
- **Depends on:** None (code changes only)
- **Blocks:** None (DNS config in w3-02 is separate)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260316-TASK-202-RESPONSE.md`

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
