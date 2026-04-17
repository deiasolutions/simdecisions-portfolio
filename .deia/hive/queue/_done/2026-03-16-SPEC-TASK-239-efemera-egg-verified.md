# TASK-239: efemera.egg.md Verified (W4 — 4.11)

## Objective
Verify the Efemera EGG renders correctly with Efemera branding: channels sidebar, messages pane, compose terminal, members list.

## Context
Wave 4 Product Polish. Efemera is the team chat product — a full EGG configuration. Backend (store, routes) and frontend (adapters, relay poller) are already implemented.

## Source Spec
`docs/specs/WAVE-4-PRODUCT-POLISH.md` — Task 4.11

## Files to Read First
- `eggs/efemera.egg.md` — Efemera EGG layout (209 lines)
- `hivenode/efemera/store.py` — Backend store (channels, messages, members, presence)
- `hivenode/efemera/routes.py` — 8 API endpoints
- `browser/src/primitives/tree-browser/adapters/channelsAdapter.ts` — Channels tree
- `browser/src/primitives/tree-browser/adapters/membersAdapter.ts` — Members tree

## Deliverables
- [ ] Load `?egg=efemera` in browser and verify:
  - Left sidebar (18%): channels tree-browser with channelsAdapter
  - Center top (70%): messages text-pane with chat bubble rendering
  - Center bottom (30%): compose terminal with `routeTarget: "relay"`
  - Right sidebar (15%): members tree-browser with presence indicators
- [ ] Verify channel selection loads messages in text-pane via bus events
- [ ] Verify compose terminal sends messages via relay poller
- [ ] Verify presence indicators show online/away/offline status
- [ ] Fix any layout, data loading, or bus event issues
- [ ] Run: `cd browser && npx vitest run`

## Priority
P1

## Model
haiku
