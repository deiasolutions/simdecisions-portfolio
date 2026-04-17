# TASK-061: Update Subdomain-to-EGG Routing

## Objective

Update `eggResolver.ts` to add hostname → EGG mappings for production and dev subdomains. Add comprehensive test coverage for hostname resolution, query param override, and pathname fallback.

## Context

The EGG resolver currently uses a hardcoded fallback to `'chat'` when `routing.config.egg` is not loaded (line 85). We need to add explicit hostname mappings for:
- `chat.efemera.live` → `chat`
- `code.shiftcenter.com` → `code`
- `pm.shiftcenter.com` → `pm`
- `dev.shiftcenter.com` → `chat` (default)
- `localhost:5173` → `chat` (dev default)

The resolver already supports query param override (`?egg=name`) and pathname fallback (`/code` → `code`). We need to ensure hostname mappings work correctly and test all resolution paths.

Existing file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\eggs\eggResolver.ts` (118 lines)

Existing test file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\eggs\__tests__\eggResolver.test.ts` (17 lines, 1 test)

## Deliverables

- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\eggs\eggResolver.ts` — Add hostname mappings
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\eggs\__tests__\eggResolver.test.ts` — Add 7 new tests (8 total)

## Code Changes Required

### eggResolver.ts

Update `resolveEggFromHostname()` function (lines 80-92) to add hardcoded hostname mappings as a fallback when `routing.config.egg` is not loaded:

```typescript
export function resolveEggFromHostname(hostname: string): string {
  const routingData = configEggCache.get('routing.config')?.data

  if (!routingData) {
    console.warn('routing.config.egg not loaded — using hardcoded hostname mappings')

    // Hardcoded hostname → EGG mappings (fallback until routing.config.egg is loaded)
    const hostnameMap: Record<string, string> = {
      'chat.efemera.live': 'chat',
      'code.shiftcenter.com': 'code',
      'pm.shiftcenter.com': 'pm',
      'dev.shiftcenter.com': 'chat',
      'localhost:5173': 'chat',
      'localhost:3000': 'chat',
    }

    return hostnameMap[hostname] ?? 'chat'
  }

  const subdomains = (routingData.subdomains as Record<string, string>) || {}
  const fallback = (routingData.fallback as string) || 'chat'

  return subdomains[hostname] ?? fallback
}
```

**Key changes:**
- Add hardcoded `hostnameMap` when `routing.config.egg` is not loaded
- Include `localhost:5173` and `localhost:3000` for local dev
- Fallback to `'chat'` for any unrecognized hostname

No changes needed to `resolveCurrentEgg()` — it already calls `resolveEggFromHostname()` and supports query param override and pathname fallback.

### eggResolver.test.ts

Add 7 new tests to cover all resolution paths. Use **TDD**: write tests FIRST, then update `eggResolver.ts` to make them pass.

```typescript
/**
 * Tests for eggResolver.ts
 */

import { describe, it, expect, beforeEach } from 'vitest'
import { resolveEggFromHostname, resolveCurrentEgg } from '../eggResolver'

describe('eggResolver', () => {
  describe('resolveEggFromHostname()', () => {
    it('falls back to "chat" when routing not loaded', () => {
      const eggId = resolveEggFromHostname('example.com')
      expect(eggId).toBe('chat')
    })

    // NEW TESTS (TDD: write these first, then update eggResolver.ts)

    it('maps chat.efemera.live to chat', () => {
      const eggId = resolveEggFromHostname('chat.efemera.live')
      expect(eggId).toBe('chat')
    })

    it('maps code.shiftcenter.com to code', () => {
      const eggId = resolveEggFromHostname('code.shiftcenter.com')
      expect(eggId).toBe('code')
    })

    it('maps pm.shiftcenter.com to pm', () => {
      const eggId = resolveEggFromHostname('pm.shiftcenter.com')
      expect(eggId).toBe('pm')
    })

    it('maps dev.shiftcenter.com to chat', () => {
      const eggId = resolveEggFromHostname('dev.shiftcenter.com')
      expect(eggId).toBe('chat')
    })

    it('maps localhost:5173 to chat', () => {
      const eggId = resolveEggFromHostname('localhost:5173')
      expect(eggId).toBe('chat')
    })

    it('maps localhost:3000 to chat', () => {
      const eggId = resolveEggFromHostname('localhost:3000')
      expect(eggId).toBe('chat')
    })
  })

  describe('resolveCurrentEgg()', () => {
    beforeEach(() => {
      // Mock window.location for browser-based tests
      delete (window as any).location
      ;(window as any).location = {
        hostname: 'localhost:5173',
        pathname: '/',
        search: '',
      }
    })

    it('resolves from query param ?egg=code', () => {
      window.location.search = '?egg=code'
      const eggId = resolveCurrentEgg()
      expect(eggId).toBe('code')
    })
  })
})
```

**Test coverage:**
- 1 existing test (fallback for unknown hostname)
- 6 new hostname mapping tests
- 1 new query param override test
- Total: **8 tests**

## Test Requirements

- [ ] **TDD required:** Write all 7 new tests FIRST, verify they fail
- [ ] Update `eggResolver.ts` to make tests pass
- [ ] All 8 tests pass: `npm run test -- eggResolver.test.ts`
- [ ] No console warnings in test output (except the expected "routing.config.egg not loaded" warning)

## Constraints

- **No file over 500 lines** — `eggResolver.ts` is currently 118 lines, adding ~10 lines is safe
- **No breaking changes** — existing behavior must be preserved:
  - Query param override (`?egg=`) still takes priority (line 102-108)
  - Pathname fallback (`/code`) still works (line 110-114)
  - `routing.config.egg` still used if loaded (line 81-92)
- **Do NOT modify routing.config.egg** — that's out of scope for this task
- **Do NOT add new dependencies** — use existing vitest imports only

## Acceptance Criteria Verification

After implementation, verify:
- [ ] `resolveEggFromHostname('chat.efemera.live')` returns `'chat'`
- [ ] `resolveEggFromHostname('code.shiftcenter.com')` returns `'code'`
- [ ] `resolveEggFromHostname('pm.shiftcenter.com')` returns `'pm'`
- [ ] `resolveEggFromHostname('dev.shiftcenter.com')` returns `'chat'`
- [ ] `resolveEggFromHostname('localhost:5173')` returns `'chat'`
- [ ] `resolveEggFromHostname('localhost:3000')` returns `'chat'`
- [ ] `resolveEggFromHostname('unknown.com')` returns `'chat'` (fallback)
- [ ] Query param override still works: `?egg=pm` loads `pm` EGG (tested in test file)
- [ ] All 8 tests pass

## Response Requirements -- MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260313-TASK-061-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** -- task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** -- every file created/modified/deleted, full absolute paths
3. **What Was Done** -- bullet list of concrete changes (hostname mappings added, 7 tests added)
4. **Test Results** -- test output from `npm run test -- eggResolver.test.ts` (8 tests passed)
5. **Build Verification** -- `npm run build` succeeds (browser builds without errors)
6. **Acceptance Criteria** -- copy deliverables above, mark [x] or [ ]
7. **Clock / Cost / Carbon** -- all three, never omit any
8. **Issues / Follow-ups** -- note that routing.config.egg overrides these hardcoded mappings when loaded

DO NOT skip any section. A response without all 8 sections is incomplete.

## Model Assignment

sonnet
