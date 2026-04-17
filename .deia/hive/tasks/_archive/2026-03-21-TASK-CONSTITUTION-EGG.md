# TASK-CONSTITUTION-EGG: Governance Home for hodeia.org

**Priority:** P2
**Dispatched by:** Q88N
**Date:** 2026-03-21
**Model:** Haiku (straightforward layout + adapter)
**Depends on:** None

---

## Objective

Create `eggs/constitution.egg.md` — the constitutional/foundation home served at **hodeia.org**. This surfaces DEIA governance documents: ethics.yml, carbon.yml, grace.yml, the #NOKINGS manifesto, and the constitutional framework.

## Context

hodeia.org is the governance face of Hodeia. "No platform lock-in. User sovereignty over data and compute." This is where the principles live — publicly readable, version-controlled, immutable in spirit.

Currently mapped to `'chat'` as a placeholder. Needs its own EGG with a doc-browsing layout.

## Deliverables

### 1. EGG file: `eggs/constitution.egg.md`
- schema_version: 3
- id: `constitution`
- Layout: horizontal split
  - Left (20%): tree-browser with `governance-docs` adapter
  - Right (80%): text-pane in `doc` renderMode

### 2. Governance docs adapter: `browser/src/primitives/tree-browser/adapters/governanceDocsAdapter.ts`
- Fetches governance doc list from a known set:
  - `.deia/config/ethics.yml`
  - `.deia/config/carbon.yml`
  - `.deia/config/grace.yml`
  - `docs/DEIA-ELEVATOR-PITCH-60s.md` (if exists)
- Returns tree items with name, path, icon
- On select: sends `doc:selected` bus event with file path
- Text-pane subscribes to `doc:selected`, fetches and renders the document

### 3. Routing update
- `eggResolver.ts`: change `hodeia.org` and `www.hodeia.org` from `'chat'` to `'constitution'`

### 4. Tests
- EGG parse test: `browser/src/eggs/__tests__/constitutionEgg.test.ts`
- Adapter test: `browser/src/primitives/tree-browser/adapters/__tests__/governanceDocsAdapter.test.ts`

## Constraints

- CSS: `var(--sd-*)` only.
- Files: 500 lines max.
- No stubs.
- TDD.

---

*hodeia gara*
