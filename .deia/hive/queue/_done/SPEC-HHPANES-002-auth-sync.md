# SPEC-HHPANES-002: Panes to hodeia.auth Sync

## Priority
P0

## Depends On
HHPANES-001

## Model Assignment
sonnet

## Objective

Ensure HiveHostPanes stay in sync with hodeia.auth state. When auth state changes (login, logout, token refresh, session expiry), all mounted panes must reflect the new state correctly within 100ms.

## Files to Read First

- browser/src/primitives/auth/authStore.ts
- browser/src/apps/authAdapter.tsx
- browser/src/apps/sim/lib/auth.ts
- browser/src/infrastructure/relay_bus/__tests__/messageBus.test.ts

## Acceptance Criteria

- [ ] Auth context available to all panes via React context or bus subscription
- [ ] Login event propagates to all mounted panes within 100ms
- [ ] Logout event propagates to all mounted panes within 100ms
- [ ] Token refresh is transparent (no pane re-render unless permissions change)
- [ ] Session expiry triggers graceful degradation (auth-blocked state, not crash)
- [ ] hodeia.auth is single source of truth — panes never cache stale auth state locally
- [ ] All existing auth tests still pass
- [ ] New tests cover login/logout propagation

## Smoke Test

- [ ] Load composite with 3+ panes — all reflect logged-in user
- [ ] Logout via hodeia.auth — all panes transition to logged-out state without manual refresh
- [ ] Login again — all panes restore logged-in state

## Constraints

- No file over 500 lines
- No stubs — every function complete
- No git operations
- Use var(--sd-*) CSS variables only
