# BRIEFING: Sim EGG bus.on crash

**From:** Q33NR
**To:** Q33N
**Date:** 2026-03-24
**Priority:** P0
**Q88N has approved dispatch.**

---

## Bug

The Sim EGG crashes at runtime with: `bus.on is not a function`

The error occurs in something called "sim-pane". This is NOT a source-level `bus.on()` call — a prior bus API sweep found zero `bus.on()` violations in source. The issue is likely:
1. A component receiving the wrong object as `bus` (e.g., getting the shell context but accessing it wrong)
2. A dependency or adapter expecting EventEmitter-style API (`.on()`) instead of MessageBus API (`.subscribe()`)
3. Something in the sim adapter chain passing a non-bus object

## Your Job

1. Write a task file for a Sonnet bee to investigate and fix this
2. The bee should:
   - Find where the error originates (stack trace reproduction)
   - Identify what object is being called with `.on()` and why it's not a MessageBus
   - Fix the root cause
   - Write regression tests
   - Ensure sim.egg.md loads without crash
3. Dispatch the bee immediately (Q88N approved)

## Key Files

- `eggs/sim.egg.md` — the EGG definition
- `browser/src/apps/simAdapter.tsx` — maps AppRendererProps to FlowDesigner
- `browser/src/apps/sim/` — all sim components
- `browser/src/infrastructure/relay_bus/` — MessageBus implementation
- `browser/src/shell/` — Shell context that provides bus

## Constraints

- Model: Sonnet
- `--inject-boot`
- Fix the bug, write tests, write response file
