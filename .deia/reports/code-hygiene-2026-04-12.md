# Code Hygiene Audit � 2026-04-12

**Repository:** simdecisions (post-flatten)
**Scope:** hivenode/, simdecisions/, _tools/, hodeia_auth/, browser/src/
**Tools:** vulture, ruff, mypy, knip, tsc

## 1. Dead Code (vulture)

**Total findings:** 93

- Test fixtures (false positives): 57
- Exception handlers (false positives): 21
- Unused imports: 15
- Unused variables (real): 0

### Real Dead Code (Top 10)

- `_tools\des_investigation_sims.py:370` � unused import 'DriftDetector' (90% confidence)
- `hivenode\entities\vectors_core.py:16` � unused import 'pg_insert' (90% confidence)
- `hivenode\hive_mcp\local_server.py:25` � unused import 'AnyUrl' (90% confidence)
- `hivenode\hive_mcp\local_server.py:28` � unused import 'Starlette' (90% confidence)
- `hivenode\hive_mcp\local_server.py:29` � unused import 'Mount' (90% confidence)
- `hivenode\hive_mcp\tests\test_state.py:7` � unused import 'mock_open' (90% confidence)
- `hivenode\inventory\store.py:9` � unused import 'literal_column' (90% confidence)
- `hivenode\llm\des_adapter.py:10` � unused import 'LLMAdapter' (90% confidence)
- `hivenode\queue_watcher.py:18` � unused import 'FileCreatedEvent' (90% confidence)
- `hivenode\queue_watcher.py:18` � unused import 'FileMovedEvent' (90% confidence)

## 2. Lint Violations (ruff)

**Total violations:** 446

### By Category

- **F401** (unused-import): 313
- **F541** (f-string-missing-placeholders): 46
- **F841** (unused-variable): 36
- **E402** (module-import-not-at-top): 16
- **F821** (undefined-name): 10
- **E401** (multiple-imports-on-one-line): 9
- **E741** (ambiguous-variable-name): 5
- **F811** (redefined-while-unused): 3
- **E722** (bare-except): 3
- **E711** (none-comparison): 2

## 3. Type Issues (mypy)

**Total errors:** 481

- Missing library stubs: 28
- Implicit Optional (PEP 484): 39
- Type mismatches: 106
- Other: 308

### Critical Errors (sample)

- `_tools\cross_reference.py:3` � error: Item "TextIO" of "TextIO | Any" has no attribute "reconfigure"  [union-attr]
- `_tools\add_game_states.py:36` � error: Unsupported operand types for + ("None" and "int")  [operator]
- `_tools\add_game_states.py:36` � error: Unsupported operand types for < ("int" and "None")  [operator]
- `_tools\add_game_states.py:37` � error: Unsupported operand types for + ("None" and "int")  [operator]
- `_tools\add_game_states.py:37` � error: Unsupported operand types for < ("int" and "None")  [operator]
- `hivenode\wiki\parser.py:9` � error: Library stubs not installed for "yaml"  [import-untyped]
- `hivenode\storage\adapters\base.py:76` � error: Function "builtins.any" is not valid as a type  [valid-type]
- `hivenode\shell\allowlist.py:35` � error: Incompatible default for argument "allowlist" (default has type "None", argument has type "li
- `hivenode\shell\allowlist.py:36` � error: Incompatible default for argument "denylist" (default has type "None", argument has type "lis
- `hivenode\scheduler\model_capabilities.py:12` � error: Library stubs not installed for "yaml"  [import-untyped]

## 4. TypeScript Errors (tsc)

**Total errors:** 1887

### Top Error Codes

- **TS2322**: 638
- **TS2304**: 344
- **TS2339**: 273
- **TS2345**: 108
- **TS2741**: 82
- **TS2353**: 70
- **TS2739**: 48
- **TS2683**: 48
- **TS2591**: 32
- **TS2740**: 29

## 5. Unused Dependencies & Stranded Files (knip)

**Total issues analyzed:** 250 files

### Unused Dependencies
- **@types/p5** — devDependency in package.json, never imported

### Stranded Files (55 total)
Files that exist but are never imported or referenced:
- `test-build-monitor-page.mjs` — legacy test file
- `test-runner.mjs` — legacy test file
- `vitest.config.ts.timestamp-*.mjs` — Vite build artifact
- `scripts/copy-eggs.cjs` — legacy script (eggs renamed to sets)
- `public/sw.js` — service worker, likely obsolete
- `src/auth/login.ts` — unused auth module
- `src/apps/factoryAdapter.tsx` — adapter not loaded
- `src/apps/responseBrowserAdapter.tsx` — adapter not loaded
- `src/hooks/useVoiceInput.smoke.tsx` — smoke test, not imported
- `src/lib/eventLedger.ts` — ledger integration, unused

### Unused Exports (126 total)
- Empty exports in `src/primitives/auth/authStore.ts`
- Empty exports in `src/primitives/settings/settingsStore.ts`
- Multiple empty exports in `src/primitives/tree-browser/index.ts`

**Note:** Many "unused exports" are public API surface for external consumers — requires manual triage.

---

## Summary

- **Dead Code:** 15 findings (after filtering false positives)
- **Lint Violations:** 446 (ruff)
- **Type Errors (Python):** 481 (mypy)
- **Type Errors (TypeScript):** 1887 (tsc)
- **Unused Dependencies:** See knip report

### Recommendations

1. **Unused imports (F401):** Clean up 313 unused imports from ruff report — prioritize high-density files like `inventory_db.py` (49 imports)
2. **TypeScript errors:** 1887 errors — primarily test type issues (TS2304: `global`, `__dirname`) and type mismatches (TS2322: string literals vs union types)
3. **Missing type stubs:** Install `types-PyYAML`, `types-requests` for better Python type checking
4. **Implicit Optional:** Fix 39 PEP 484 violations in function signatures (use `Optional[T]` explicitly)
5. **Dead code:** Review 15 unused imports flagged by vulture — low priority (mostly test fixtures)
6. **Stranded files:** Remove 55 unreferenced files — includes legacy test files, obsolete adapters, and Vite build artifacts

---

## Appendix A: Unused Imports by File (Top 15)

**_tools/inventory_db.py** (49 unused imports)
  - Line 17: `hivenode.inventory.store.reset_engine` imported but unused
  - Line 18: `hivenode.inventory.store.db_add_feature` imported but unused
  - Line 18: `hivenode.inventory.store.db_update_feature` imported but unused
  - ... and 46 more

**simdecisions/phase_ir/validation.py** (9 unused imports)
  - Line 14: `typing.Any` imported but unused
  - Line 14: `typing.Optional` imported but unused
  - Line 17: `.node_types.validate_node` imported but unused
  - ... and 6 more

**hivenode/hive_mcp/local_server.py** (7 unused imports)
  - Line 16: `sys` imported but unused
  - Line 25: `pydantic.AnyUrl` imported but unused
  - Line 28: `starlette.applications.Starlette` imported but unused
  - ... and 4 more

**_tools/des_investigation_sims.py** (6 unused imports)
  - Line 11: `simdecisions.phase_ir.primitives.Variable` imported but unused
  - Line 11: `simdecisions.phase_ir.primitives.Distribution` imported but unused
  - Line 16: `simdecisions.des.checkpoints.CheckpointManager` imported but unused
  - ... and 3 more

**hivenode/inventory/store.py** (6 unused imports)
  - Line 7: `typing.Optional` imported but unused
  - Line 11: `sqlalchemy.insert` imported but unused
  - Line 11: `sqlalchemy.update` imported but unused
  - ... and 3 more

**hodeia_auth/services/reset_token.py** (5 unused imports)
  - Line 5: `typing.Optional` imported but unused
  - Line 6: `sqlalchemy.select` imported but unused
  - Line 7: `sqlalchemy.orm.Session` imported but unused
  - ... and 2 more

**simdecisions/des/tests/test_token_attrs.py** (5 unused imports)
  - Line 9: `pytest` imported but unused
  - Line 11: `simdecisions.des.core.EngineState` imported but unused
  - Line 11: `simdecisions.des.core.SimConfig` imported but unused
  - ... and 2 more

**hivenode/entities/archetype_routes.py** (4 unused imports)
  - Line 10: `typing.Optional` imported but unused
  - Line 18: `hivenode.entities.archetypes.ArchetypeResponse` imported but unused
  - Line 24: `hivenode.entities.archetypes.deserialize_embedding` imported but unused
  - ... and 1 more

**hivenode/relay/store.py** (4 unused imports)
  - Line 18: `sqlalchemy.insert` imported but unused
  - Line 18: `sqlalchemy.update` imported but unused
  - Line 18: `sqlalchemy.delete` imported but unused
  - ... and 1 more

**_tools/build_index.py** (3 unused imports)
  - Line 19: `pathlib.Path` imported but unused
  - Line 20: `typing.Set` imported but unused
  - Line 21: `warnings` imported but unused

---

## Appendix B: TypeScript Error Patterns

### TS2322 (Type mismatch) — 638 errors
**Pattern:** String literal vs union type mismatch
```
src/__tests__/smoke.test.tsx(46,7): Type '"home"' is not assignable to type '"both" | "home-only" | "cloud-only" | undefined'
```
**Root cause:** Enum string values changed, tests use old literals

**Pattern:** Missing props in test mocks
```
src/apps/__tests__/authAdapter.test.tsx(73,25): Type '{ _paneId: string; _isActive: boolean; _config: {}; }' is not assignable to type 'IntrinsicAttributes & AppRendererProps'
```
**Root cause:** Test mocks use old prop names (`_paneId` → `paneId`)

### TS2304 (Cannot find name) — 344 errors
**Pattern:** Missing Node.js global types
```
src/__tests__/smoke.test.tsx(22,1): Cannot find name 'global'
src/__tests__/buildMonitorLoad.integration.test.tsx(31,31): Cannot find name '__dirname'
```
**Root cause:** Missing `@types/node` in tsconfig `types` array

### TS2339 (Property does not exist) — 273 errors
**Pattern:** Deprecated or renamed properties
```
src/__tests__/smoke.test.tsx(51,11): Object literal may only specify known properties, and 'conversation_id' does not exist in type 'Message'
```
**Root cause:** Schema evolution (snake_case → camelCase)

