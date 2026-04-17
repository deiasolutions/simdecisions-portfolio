# TASK-007: EGG System Port — Parser, Inflater, Resolver, Types

## Objective

Port the EGG (Executable Graph Geometry) system from `simdecisions-2/src/eggs/` to `browser/src/eggs/`. The EGG system is the keystone — it parses `.egg.md` files into EggIR, inflates node types, resolves which EGG to load for a given hostname, and defines the canonical NODE_TYPES used by the shell reducer. Without it, no product launches.

## Dependencies

- **TASK-005 (Relay Bus)** must be complete. The inflater wires commands to the bus, and `configEggCache` + `permissionsResolver` are delivered by TASK-005.

## Source Files

Port from `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\`:

### Primary (newer generation — these are the canonical implementations):

| Source Path | Dest Path | Lines | What It Does |
|-------------|-----------|-------|-------------|
| `eggs/parseEggMd.ts` | `eggs/parseEggMd.ts` | 200 | Parses `.egg.md` frontmatter + fenced JSON blocks into `ParsedEgg` |
| `eggs/eggInflater.ts` | `eggs/eggInflater.ts` | 477 | Converts `ParsedEgg` → `EggIR`. Field translation, favicon resolution, permissions, mode engine wiring, command registry, away manager |
| `eggs/parseEggManifest.ts` | `eggs/parseEggManifest.ts` | 104 | Parses markdown app manifest table into `AppEntry[]`. COLOR_MAP uses `var(--sd-*)` |
| `eggs/fieldTranslator.ts` | `eggs/fieldTranslator.ts` | 73 | Recursive legacy field name translation in layout tree |
| `eggs/index.ts` | `eggs/index.ts` | 40 | EGG_REGISTRY barrel. Top-level await — needs refactoring |
| `eggs/useEggManifest.ts` | `eggs/useEggManifest.ts` | 72 | React hook: returns primary apps from active EGG |
| `services/shell/eggResolver.ts` | `eggs/eggResolver.ts` | 95 | Hostname → EGG ID mapping. URL param override (`?egg=`). Uses configEggCache for routing config |

### Secondary (older generation — port types only, not the full implementation):

| Source Path | Dest Path | Lines | What It Does |
|-------------|-----------|-------|-------------|
| `services/egg/eggConfig.ts` | `eggs/eggConfig.ts` | 194 | Older JSON EGG config types: `EggLayoutNode`, `EggLayout`, `EggPaneConfig`, `EggConfig`. Validation. Keep types + validation for backwards compat |
| `services/egg/defaultEggs.ts` | `eggs/defaultEggs.ts` | 108 | Fallback EGG configs. References `EggConfig` type |
| `services/egg/eggLoader.ts` | `eggs/eggLoader.ts` | 22 | Simple async loader — fetches + parses .egg.md |
| `services/egg/eggMarkdownParser.ts` | — | 117 | Older parser (predecessor of parseEggMd). DO NOT PORT — parseEggMd supersedes it |

### New file (not from old repo):

| Dest Path | What It Does |
|-----------|-------------|
| `eggs/types.ts` | Canonical NODE_TYPES enum + EGG type definitions. Source of truth for TASK-008 (shell reducer) |

## Port Rules

### 1. Create `types.ts` as Source of Truth

Extract node types from `eggInflater.ts` layout tree processing and define them canonically:

```typescript
// browser/src/eggs/types.ts

/** Canonical node types for the pane layout tree. */
export enum NodeType {
  SPLIT = 'split',
  PANE = 'pane',
  TAB_GROUP = 'tab-group',
  FLOAT = 'float',
  DOCK = 'dock',
}

/** Layout direction for split nodes. */
export enum SplitDirection {
  HORIZONTAL = 'horizontal',
  VERTICAL = 'vertical',
}

/** EGG layout tree node (recursive). */
export interface EggLayoutNode {
  type: NodeType;
  direction?: SplitDirection;
  ratio?: number;
  children?: EggLayoutNode[];
  appType?: string;
  paneId?: string;
  label?: string;
  config?: Record<string, unknown>;
}

/** Parsed EGG frontmatter + code blocks. */
export interface ParsedEgg {
  egg: string;
  version: string;
  schema_version: number;
  displayName: string;
  description?: string;
  product?: string;
  favicon?: string;
  layout: EggLayoutNode;
  modes?: Record<string, unknown>;
  ui?: Record<string, unknown>;
  tabs?: Record<string, unknown>;
  commands?: Record<string, unknown>;
  prompt?: Record<string, unknown>;
  settings?: Record<string, unknown>;
  away?: Record<string, unknown>;
  startup?: Record<string, unknown>;
  permissions?: Record<string, unknown>;
}

/** Inflated EGG ready for shell consumption. */
export interface EggIR {
  id: string;
  displayName: string;
  description: string;
  version: string;
  schemaVersion: number;
  favicon: string;
  layout: EggLayoutNode;
  modes: Record<string, unknown>;
  ui: Record<string, unknown>;
  tabs: Record<string, unknown>;
  commands: Record<string, unknown>;
  settings: Record<string, unknown>;
  permissions: Record<string, unknown>;
}

/** App entry from the EGG manifest. */
export interface AppEntry {
  name: string;
  appType: string;
  description: string;
  color: string;
  category: 'primary' | 'governance';
}

/** EGG registry keyed by EGG ID. */
export type EggRegistry = Record<string, EggIR>;

/** EGG ID type for type safety. */
export type EggId = string;
```

TASK-008 (shell reducer) will `import { NodeType, SplitDirection, EggLayoutNode } from '../eggs/types'`.

### 2. Separate Core Inflation from Side-Effect Wiring

The old `eggInflater.ts` (477 lines) mixes pure data transformation with side-effect wiring (mode engine, command registry, away manager). Split into:

**Pure inflation** (in `eggInflater.ts`):
- `inflateEgg(parsed: ParsedEgg): EggIR` — pure data transformation
- Field translation (schema < 3)
- Favicon URL resolution
- Layout tree validation
- Startup config extraction

**Side-effect wiring** (in `eggWiring.ts` — new file):
- `wireEgg(egg: EggIR, bus: RelayBus): void` — wires commands, modes, away
- Command registry wiring (emits to bus)
- Mode engine initialization
- Away manager loading
- Permissions registry building

This separation enables:
- Testing inflation without mocking the bus
- Shell reducer can consume EggIR without triggering side effects
- Bus-dependent wiring can be deferred until bus is ready

### 3. Refactor Top-Level Await in `index.ts`

The old `index.ts` uses top-level await with `fetch()`:
```typescript
// OLD — don't do this
const codeDefaultParsed = parseEggMd(codeDefaultRaw);
const codeDefault = await inflateEgg(codeDefaultParsed);
export const EGG_REGISTRY = { 'code-default': codeDefault };
```

Refactor to lazy initialization:
```typescript
// NEW — lazy registry
import { parseEggMd } from './parseEggMd';
import { inflateEgg } from './eggInflater';

// Raw EGG markdown imports (Vite ?raw)
import codeDefaultRaw from '../../eggs/code-default.egg.md?raw';
// ... other EGGs

let _registry: EggRegistry | null = null;

export async function getEggRegistry(): Promise<EggRegistry> {
  if (_registry) return _registry;
  _registry = {};
  // Inflate all built-in EGGs
  const entries = [
    ['code-default', codeDefaultRaw],
    // ... other entries
  ] as const;
  for (const [id, raw] of entries) {
    const parsed = parseEggMd(raw);
    _registry[id] = inflateEgg(parsed);
  }
  return _registry;
}
```

Note: The actual .egg.md files in `eggs/` will be added in a later task when products are defined. For now, `getEggRegistry()` returns an empty registry and the import lines for .egg.md files should be commented out or conditionally imported.

### 4. eggResolver Uses configEggCache from TASK-005

`eggResolver.ts` calls `configEggCache.get('routing')` to load routing config. This import should reference:
```typescript
import { configEggCache } from '../infrastructure/relay_bus/configEggCache';
// (or wherever TASK-005 places it — check TASK-005 output)
```

If `configEggCache` isn't available yet at the exact expected path, create a placeholder import and add a `// TODO: verify path after TASK-005 delivery` comment.

### 5. useEggManifest Hook

Port as-is. It depends on `resolveCurrentEgg()` from `eggResolver.ts` and the `EGG_REGISTRY`. Update to use `getEggRegistry()` async pattern.

### 6. fieldTranslator — Port Exactly

`fieldTranslator.ts` is 73 lines, pure function, no dependencies. Port exactly as-is.

### 7. parseEggManifest — Port Exactly

`parseEggManifest.ts` is 104 lines. Verify `COLOR_MAP` uses only `var(--sd-*)` properties (it already does). Port exactly.

### 8. eggConfig + defaultEggs — Port Types

These are the older JSON-format EGG types. Port:
- All type definitions (`EggLayoutNode`, `EggLayout`, `EggPaneConfig`, `EggAppletProtocol`, `EggConfig`)
- `validateEggConfig()` function
- `defaultEggs.ts` fallback configs

These provide backwards compatibility for any code still using the JSON config format.

### 9. eggMarkdownParser — DO NOT PORT

This is the predecessor of `parseEggMd.ts`. It has a simpler `EggIR` interface and less robust parsing. `parseEggMd.ts` supersedes it completely. Skip.

## File Structure

```
browser/src/eggs/
├── index.ts              -- getEggRegistry(), re-exports
├── types.ts              -- NODE_TYPES, ParsedEgg, EggIR, AppEntry, EggRegistry (SOURCE OF TRUTH)
├── parseEggMd.ts         -- .egg.md parser
├── eggInflater.ts        -- Pure inflation: ParsedEgg → EggIR
├── eggWiring.ts          -- Side-effect wiring: commands, modes, away → bus (NEW)
├── parseEggManifest.ts   -- App manifest table parser
├── fieldTranslator.ts    -- Legacy field name translation
├── eggResolver.ts        -- Hostname → EGG ID resolution
├── eggConfig.ts          -- Older JSON config types + validation
├── defaultEggs.ts        -- Fallback EGG configs
├── eggLoader.ts          -- Simple async .egg.md loader
└── useEggManifest.ts     -- React hook for EGG manifests
```

```
browser/src/eggs/__tests__/
├── types.test.ts
├── parseEggMd.test.ts
├── eggInflater.test.ts
├── eggWiring.test.ts
├── parseEggManifest.test.ts
├── fieldTranslator.test.ts
├── eggResolver.test.ts
├── eggConfig.test.ts
├── defaultEggs.test.ts
├── eggLoader.test.ts
└── useEggManifest.test.ts
```

## Test Requirements

### Port Existing Tests

Port tests from old repo:
- `simdecisions-2/src/eggs/__tests__/parseEggMd.test.ts` (167 lines)
- `simdecisions-2/src/eggs/__tests__/eggInflater.test.ts` (213 lines)
- `simdecisions-2/src/eggs/__tests__/parseEggManifest.test.ts` (203 lines)
- `simdecisions-2/src/eggs/__tests__/fieldTranslator.test.ts` (84 lines)
- `simdecisions-2/src/eggs/__tests__/index.test.ts` (87 lines)
- `simdecisions-2/src/eggs/__tests__/useEggManifest.test.ts` (107 lines)
- `simdecisions-2/src/services/egg/__tests__/eggConfig.test.ts` (166 lines)
- `simdecisions-2/src/services/egg/__tests__/defaultEggs.test.ts` (92 lines)
- `simdecisions-2/src/services/egg/__tests__/eggLoader.test.ts` (68 lines)

Fix imports from `src/eggs/...` to relative imports. Fix any references to old `eggMarkdownParser`.

### New Tests

#### types.test.ts
- [ ] NodeType enum has all 5 values
- [ ] SplitDirection enum has 2 values
- [ ] EggLayoutNode supports recursive children
- [ ] ParsedEgg has all required fields
- [ ] EggIR has all required fields
- [ ] AppEntry has category field

#### eggWiring.test.ts
- [ ] wireEgg registers commands on bus
- [ ] wireEgg initializes mode engine
- [ ] wireEgg loads away manager
- [ ] wireEgg with empty commands/modes is no-op
- [ ] wireEgg with no bus throws

**Minimum: 60+ tests (ported + new).**

## Source Files to Read First

Primary generation (read these first):
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\eggs\parseEggMd.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\eggs\eggInflater.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\eggs\parseEggManifest.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\eggs\fieldTranslator.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\eggs\index.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\eggs\useEggManifest.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\services\shell\eggResolver.ts`

Older generation (types + validation only):
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\services\egg\eggConfig.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\services\egg\defaultEggs.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\services\egg\eggLoader.ts`

Tests (port all):
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\eggs\__tests__\parseEggMd.test.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\eggs\__tests__\eggInflater.test.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\eggs\__tests__\parseEggManifest.test.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\eggs\__tests__\fieldTranslator.test.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\eggs\__tests__\index.test.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\eggs\__tests__\useEggManifest.test.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\services\egg\__tests__\eggConfig.test.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\services\egg\__tests__\defaultEggs.test.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\services\egg\__tests__\eggLoader.test.ts`

Also check TASK-005 output for:
- `configEggCache` location and export path
- `permissionsResolver` location and export path
- `RelayBus` import path

## What NOT to Build

- No shell reducer (TASK-008)
- No shell renderer components (TASK-009)
- No actual .egg.md product files (separate task — just define the registry interface)
- No mode engine implementation (just the wiring call — mode engine is a future task)
- No away manager implementation (just the wiring call)
- No command registry implementation (just emit to bus)
- No eggMarkdownParser.ts (superseded by parseEggMd.ts)
- No backend Python code (EGG system is browser-only)

## Constraints

- TypeScript strict mode
- React 18+ (for useEggManifest hook)
- Vite (for `?raw` imports of .egg.md files)
- All files under 500 lines (eggInflater.ts was 477 — after splitting out wiring, both files should be well under)
- No stubs — every function fully implemented
- All `var(--sd-*)` custom properties in COLOR_MAP — no hex, no rgb
- Test with vitest
- Import `configEggCache` and `permissionsResolver` from TASK-005 delivery location

## Deliverables

### Source Files
- [ ] `browser/src/eggs/types.ts`
- [ ] `browser/src/eggs/parseEggMd.ts`
- [ ] `browser/src/eggs/eggInflater.ts`
- [ ] `browser/src/eggs/eggWiring.ts`
- [ ] `browser/src/eggs/parseEggManifest.ts`
- [ ] `browser/src/eggs/fieldTranslator.ts`
- [ ] `browser/src/eggs/eggResolver.ts`
- [ ] `browser/src/eggs/eggConfig.ts`
- [ ] `browser/src/eggs/defaultEggs.ts`
- [ ] `browser/src/eggs/eggLoader.ts`
- [ ] `browser/src/eggs/useEggManifest.ts`
- [ ] `browser/src/eggs/index.ts`

### Test Files
- [ ] `browser/src/eggs/__tests__/types.test.ts`
- [ ] `browser/src/eggs/__tests__/parseEggMd.test.ts`
- [ ] `browser/src/eggs/__tests__/eggInflater.test.ts`
- [ ] `browser/src/eggs/__tests__/eggWiring.test.ts`
- [ ] `browser/src/eggs/__tests__/parseEggManifest.test.ts`
- [ ] `browser/src/eggs/__tests__/fieldTranslator.test.ts`
- [ ] `browser/src/eggs/__tests__/eggResolver.test.ts`
- [ ] `browser/src/eggs/__tests__/eggConfig.test.ts`
- [ ] `browser/src/eggs/__tests__/defaultEggs.test.ts`
- [ ] `browser/src/eggs/__tests__/eggLoader.test.ts`
- [ ] `browser/src/eggs/__tests__/useEggManifest.test.ts`

**23 deliverables total (12 source + 11 test).**

## Response Requirements -- MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/YYYYMMDD-TASK-007-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** -- task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** -- every file created/modified/deleted, full paths
3. **What Was Done** -- bullet list of concrete changes
4. **Test Results** -- test files run, pass/fail counts
5. **Build Verification** -- vitest output summary
6. **Acceptance Criteria** -- copy deliverables above, mark [x] or [ ]
7. **Clock / Cost / Carbon** -- all three, never omit any
8. **Issues / Follow-ups** -- edge cases, dependencies, recommended next tasks

DO NOT skip any section. A response without all 8 sections is incomplete.
