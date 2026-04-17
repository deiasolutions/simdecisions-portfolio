# SPEC: Fix useEffect Dependency Instability in useEfemeraConnector

## Priority
P0

## Objective
Fix the useEffect dependency array in useEfemeraConnector.ts that causes re-initialization on every state change, and memoize the config fallback in AppFrame.tsx to prevent new object references on every render.

## Context
Firefox reports "slowing down your browser" on efemera.live. Root cause: the main useEffect in useEfemeraConnector.ts has `config` and `handleMessageSend` in its dependency array. `handleMessageSend` changes whenever `activeChannelId` changes (it's in the useCallback deps), causing the entire init effect to re-run — tearing down WS, reloading channels, re-subscribing bus events, and restarting presence. Additionally, AppFrame.tsx passes `config={node.appConfig || {}}` which creates a new `{}` on every render if appConfig is falsy.

## Files to Read First
- C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\efemera-connector\useEfemeraConnector.ts
- C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\AppFrame.tsx

## Acceptance Criteria
- [ ] Remove `handleMessageSend` and `config` from the useEffect dependency array
- [ ] Use a ref for handleMessageSend instead (useRef + useEffect to keep it current), so the bus subscription always calls the latest version without re-running the init effect
- [ ] Use a ref for config values needed inside the effect (pollingIntervalMs, presenceAutoIdleMs) so the effect doesn't depend on the config object
- [ ] In AppFrame.tsx, memoize the config fallback: `const stableConfig = useMemo(() => node.appConfig || {}, [node.appConfig])` and pass that instead of inline `node.appConfig || {}`
- [ ] The useEffect dependency array should only contain truly stable references: `[bus, paneId]`
- [ ] Tests written FIRST (TDD)
- [ ] All existing tests still pass: `cd browser && npx vitest run src/primitives/efemera-connector`
- [ ] Add test: verify useEffect does not re-run when activeChannelId changes
- [ ] Add test: verify AppFrame passes referentially stable config across re-renders

## Smoke Test
cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser && npx vitest run src/primitives/efemera-connector

## Model Assignment
sonnet

## Depends On
(none)

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs
- TDD — tests first
- Do NOT change any public API or component signatures
- Do NOT remove functionality — only stabilize the re-render behavior
- Write response to: .deia/hive/responses/20260401-SPEC-PERF-01-RESPONSE.md
