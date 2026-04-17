# SPEC-DIALECT-PREFERENCE-001: User Vocabulary & Shell Dialect Preference System

**Status:** Draft
**Priority:** P2
**Source:** `platform/simdecisions-2/src/data/dialectPacks.ts`, `platform/simdecisions-2/src/services/frank/dialectLoader.ts`
**Backlog:** BL-TBD
**Origin:** Q88N directive, 2026-03-19. Platform repo already contains partial implementation.

---

## Problem

ShiftCenter is a governed application runtime used by people with different professional backgrounds (developers, project managers, engineers, operations staff) and different computing preferences (Unix, DOS/PowerShell, GUI-first). The current interface uses a single fixed vocabulary and a single terminal dialect. Users cannot:

1. Choose terminology that matches their professional domain
2. Use their preferred command-line conventions (DOS `dir` vs Unix `ls`)
3. Customize the voice/tone of interface elements

The platform repo has partial implementations of all three layers, but none are ported to shiftcenter or wired to user preferences.

---

## What Exists in Platform (Port Candidates)

### Layer 1: Vocabulary Theme Packs (IMPLEMENTED in platform)

**File:** `platform/simdecisions-2/src/data/dialectPacks.ts` (109 lines)

Three theme packs mapping 20 canonical terms to domain-specific labels:

| Canonical | Developer (default) | PMP | Engineer |
|-----------|-------------------|-----|----------|
| `task` | Task | Work Package | Process Step |
| `decision` | Decision | Decision Gate | Branch Point |
| `checkpoint` | Checkpoint | Milestone | Quality Gate |
| `queue` | Queue | Resource Pool | Buffer |
| `delay` | Delay | Lag | Wait State |
| `parallel_split` | Fork | Concurrent Tasks | Parallel Processing |
| `parallel_join` | Join | Synchronization | Convergence |
| `human` | Human | Resource (Human) | Operator |
| `llm` | LLM | Resource (AI) | AI Agent |
| `design` | Design | Planning | Design |
| `experiment` | Experiment | What-If Analysis | Simulation |
| `run` | Run | Execute | Production |

Resolution cascade: `resolveTerm(packId, canonical)` → active pack → Developer → canonical key.

### Layer 2: Dialect Loader (IMPLEMENTED in platform)

**File:** `platform/simdecisions-2/src/services/frank/dialectLoader.ts` (71 lines)

Composable system prompt assembly. Core dialects (Patois + Envelope) always loaded. Context-dependent dialects (IR-Generation, Simulation, Co-Author) added per session. `composeSystemPrompt()` concatenates with `---` separators.

### Layer 3: Shell Dialect / Terminal Personality (DESIGNED, not implemented)

**Source:** `platform/.deia/hive/coordination/ADR-FRANK-001-EGG-EXTENSION-ARCHITECTURE.md`

RAG EGGs as loadable personality modes. A "strict unix mode" or "DOS mode" would be an EGG loaded onto Fr@nk's terminal that:
- Translates command names (`dir` ↔ `ls`, `type` ↔ `cat`, `cls` ↔ `clear`)
- Adjusts path separators in display (`\` vs `/`)
- Adapts output formatting (PowerShell table style vs Unix columnar)
- Customizes prompt appearance (`C:\>` vs `$`)

### Layer 4: Primitive Role Architecture (DESIGNED in platform)

**Source:** `platform/.deia/hive/coordination/2026-03-04-Q33N-PRIMITIVE-DIALECT-ARCHITECTURE.md`

19 canonical primitives sit below all vocabulary layers. Training data normalizes to primitives regardless of user's chosen vocabulary. CSS analogy: primitive = `var(--sd-role)`, dialect = theme resolving it.

| Primitive | Hive Dialect | Corporate | Internal |
|-----------|-------------|-----------|----------|
| `coordinator` | Queen | Manager | Q33N |
| `strategic_coordinator` | Hivemaster | Director | Q33NR |
| `llm_worker` | Bee | AI Agent | b33 |
| `mechanical_worker` | Drone | Worker | b33 (no LLM) |
| `human_agent` | Human | Human | Human |

---

## Deliverables (When Scheduled)

### Phase 1: Port Vocabulary Theme System
- [ ] Port `dialectPacks.ts` to `browser/src/data/dialectPacks.ts`
- [ ] Add `vocabularyTheme` preference to settings store (`sd_user_settings` in localStorage)
- [ ] Wire `resolveTerm()` into UI components that display canonical terms (canvas node labels, properties panel, tree-browser)
- [ ] Settings UI: theme selector dropdown (Developer / PMP / Engineer)
- [ ] Tests: theme resolution, fallback cascade, settings persistence

### Phase 2: Port Dialect Loader
- [ ] Port `dialectLoader.ts` to `browser/src/services/frank/dialectLoader.ts`
- [ ] Port prompt files: `patois.md`, `envelope.md`, `ir-generation.md`, `simulation.md`
- [ ] Wire `composeSystemPrompt()` into terminal/chat LLM request pipeline
- [ ] Tests: prompt composition, dialect activation/deactivation

### Phase 3: Shell Dialect EGGs
- [ ] Define EGG schema for terminal personality overlays
- [ ] Create `unix.egg.md` — default, no translation needed
- [ ] Create `dos.egg.md` — DOS/PowerShell command translation layer
- [ ] Implement command translation map (bidirectional: display ↔ execution)
- [ ] Add `shellDialect` preference to settings store
- [ ] Tests: command translation accuracy, path separator handling, prompt display

### Phase 4: Training Normalization
- [ ] Event Ledger stores both `theme_label` and `canonical` for every term
- [ ] Training corpus export normalizes to primitives
- [ ] Dialect switching triggers re-render, not data migration

---

## Architecture Principles

1. **Primitives are canonical.** Vocabulary packs are presentation. Data layer never stores theme-specific terms.
2. **Sparse override.** Theme packs only define terms that differ from Developer (standard). Missing terms cascade to standard → canonical key.
3. **Composition over hardcoding.** Terminal personalities are loadable EGGs, not if-else branches.
4. **Lossless round-trip.** Domain dialect compilers (BPMN, SBML, Terraform) preserve original + IR + metadata in PIE packages.
5. **User preference is sticky.** Stored in `sd_user_settings`, survives page reload, syncs via hivenode when online.

---

## Constraints

- CSS: `var(--sd-*)` only. No hardcoded colors.
- No file over 500 lines. Modularize at 500.
- TDD. Tests first.
- No stubs. Every function complete.
- Port, not rewrite. Same logic, same interfaces, TypeScript conversion only.

---

## Dependencies

- Settings store (`browser/src/stores/settingsStore.ts` or equivalent in shiftcenter)
- Fr@nk service (if ported) or terminal primitive
- EGG loader (for Phase 3 shell dialect EGGs)
- Event Ledger (for Phase 4 training normalization)

---

## Platform Source Files Reference

| File | Lines | What |
|------|-------|------|
| `simdecisions-2/src/data/dialectPacks.ts` | 109 | Theme packs + resolveTerm() |
| `simdecisions-2/src/services/frank/dialectLoader.ts` | 71 | Prompt composition |
| `simdecisions-2/src/services/frank/prompts/patois.md` | ~200 | Identity protocol |
| `simdecisions-2/src/services/frank/prompts/envelope.md` | ~100 | Response format |
| `.deia/hive/coordination/2026-03-04-Q33N-VOCABULARY-THEMES.md` | — | Theme architecture briefing |
| `.deia/hive/coordination/2026-03-04-Q33N-IMPLEMENT-VOCABULARY-THEMES.md` | — | 5-phase implementation plan |
| `.deia/hive/coordination/2026-03-08-FRANK-INPUT-MODES-v2.md` | — | Terminal input modes spec |
| `.deia/hive/coordination/ADR-FRANK-001-EGG-EXTENSION-ARCHITECTURE.md` | — | RAG EGG personality system |
| `.deia/hive/coordination/2026-03-04-Q33N-PRIMITIVE-DIALECT-ARCHITECTURE.md` | — | Primitive role architecture |
| `canonical/docs/adr-013-domain-dialect-compilers.egg.md` | — | Domain dialect compiler plugins |
