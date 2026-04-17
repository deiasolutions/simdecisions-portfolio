# TASK-IRD-02: IR Density — Batch Scoring + Gate 0 Integration -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-04-06

## Files Modified

- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/_tools/ir_density.py` — added batch_score_directory(), gate_check_file(), format_table(), format_json(), format_csv(), cmd_batch(), cmd_gate_check()
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/scripts/queue/gate0.py` — added check_ir_density() as 6th validation step
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/_tools/tests/test_ir_density.py` — added 14 new tests for batch, gate-check, and Gate 0 integration

## What Was Done

### Batch Scoring (ir_density.py)
- `batch_score_directory(directory, mode)` — scans directory for SPEC-*.md, TASK-*.md, IMPL-*.md (or *.prism.md in prism mode), scores all matching files
- Handles encoding errors gracefully (UTF-8 with latin-1 fallback)
- Returns list of dicts with filename, filepath, and all scoring metrics
- Three output formats:
  - `format_table()` — ASCII table with visual bar chart (# chars instead of Unicode for Windows compatibility)
  - `format_json()` — JSON array for machine consumption
  - `format_csv()` — CSV with all fields

### Gate Check (ir_density.py)
- `gate_check_file(file_path, min_density, min_ird)` — returns dict with passed (bool), score (float), threshold, message
- Exit code 0 = pass, 1 = fail (for CI/dispatch integration)
- Configurable thresholds via CLI flags: --min-density (spec mode), --min-ird (prism mode)
- Handles missing files gracefully
- Auto-detects mode (spec vs prism)

### Gate 0 Integration (gate0.py)
- `check_ir_density(spec, min_density, warn_density, min_ird, warn_ird)` — 6th validation check
- **Spec mode thresholds:**
  - Block if density < 0.2 (default min_density)
  - Warn if density < 0.4 (default warn_density)
  - Pass if density >= 0.4
- **PRISM mode thresholds:**
  - Block if IRD < 5/kt (default min_ird)
  - Warn if IRD < 10/kt (default warn_ird)
  - Pass if IRD >= 10/kt
- Thresholds configurable via function params
- Graceful fallback if ir_density module unavailable (returns warning, not failure)
- All warnings use ASCII text (no Unicode emoji) for Windows compatibility

### Tests Added (14 new tests)
- `test_batch_scores_multiple_files` — batch scores 3 files (SPEC, SPEC, TASK)
- `test_batch_scores_prism_files` — batch scores PRISM files with mode="prism"
- `test_batch_empty_directory` — handles empty directory gracefully
- `test_batch_mixed_files` — skips non-matching files
- `test_gate_check_pass_spec` — gate check passes for high density spec
- `test_gate_check_fail_spec` — gate check fails for low density spec
- `test_gate_check_pass_prism` — gate check passes for high IRD prism file
- `test_gate_check_configurable_thresholds` — thresholds are configurable
- `test_gate_check_file_not_found` — handles missing file gracefully
- `test_format_table_spec_mode` — table output for spec mode
- `test_format_table_prism_mode` — table output for prism mode
- `test_format_json_output` — JSON output format
- `test_format_csv_output` — CSV output format
- `test_check_ir_density_pass_spec` — Gate 0 check passes for high density spec
- `test_check_ir_density_warn_low` — Gate 0 check warns (but passes) for low density spec

### Unicode/Windows Compatibility Fixes
- Replaced block character `█` with `#` in table output (Windows console compatibility)
- Replaced warning emoji `⚠️` with `WARNING:` text (Windows console compatibility)
- Added explicit UTF-8 encoding to all test file writes
- Added UTF-8 with latin-1 fallback in batch_score_directory()

## Test Results

**All tests pass: 41 passed, 1 skipped**

```
python -m pytest _tools/tests/test_ir_density.py -v
======================== 41 passed, 1 skipped in 0.27s ========================
```

### Smoke Tests (from spec)

✅ **Batch scoring:**
```bash
python _tools/ir_density.py batch .deia/hive/queue/backlog/
# Output: ASCII table with 3 specs scored (average: 0.447)
```

✅ **Batch JSON output:**
```bash
python _tools/ir_density.py batch .deia/hive/queue/backlog/ --format json
# Output: Valid JSON array with all scoring metrics
```

✅ **Gate check (pass):**
```bash
python _tools/ir_density.py gate-check .deia/hive/queue/backlog/SPEC-MW-V04-verify-conversation-pane.md --min-density 0.4
# Output: Density: 0.460 (threshold: 0.400) - PASS
# Exit code: 0
```

✅ **Gate check (fail):**
```bash
python _tools/ir_density.py gate-check .deia/hive/queue/backlog/SPEC-MW-V04-verify-conversation-pane.md --min-density 0.9
# Output: Density: 0.460 (threshold: 0.900) - FAIL
# Exit code: 1
```

✅ **Gate 0 integration:**
```python
from gate0 import validate_spec
from spec_parser import parse_spec

spec = parse_spec(Path('.deia/hive/queue/backlog/SPEC-MW-V04-verify-conversation-pane.md'))
result = validate_spec(spec, Path('.'))

# Output: Passed: True, 6 checks (including ir_density: 0.460)
```

## Acceptance Criteria — ALL MET ✓

- [x] `batch <dir>` scores all SPEC-*.md and TASK-*.md files, outputs table
- [x] `batch --format json` outputs JSON array
- [x] `batch --format csv` outputs CSV
- [x] `gate-check <file> --min-density 0.4` returns exit code 0 (pass) or 1 (fail)
- [x] `gate-check <file> --min-ird 10` works for prism mode
- [x] Gate 0 calls density check as 6th validation step
- [x] Warn if density < 0.4 (spec) or IRD < 10 (prism)
- [x] Block if density < 0.2 (spec) or IRD < 5 (prism)
- [x] Thresholds configurable via flags (--min-density, --min-ird)
- [x] Batch handles empty directories gracefully
- [x] Batch handles mixed file types (skips non-matching files)
- [x] 8+ tests covering batch, gate-check, Gate 0 hook (14 tests added)
- [x] All tests pass: `python -m pytest _tools/tests/test_ir_density.py -v`

## Design Decisions

1. **Windows console compatibility:** Used `#` instead of `█` for progress bars, `WARNING:` instead of `⚠️` emoji. Windows console (cp1252 encoding) doesn't support Unicode block drawing characters reliably.

2. **Graceful fallbacks:** If ir_density module unavailable in Gate 0 context, return warning instead of failure. Allows Gate 0 to work even if _tools/ is not in path.

3. **Thresholds are soft defaults:** Initial thresholds (0.2 block, 0.4 warn) are estimates. Configurable via function params and CLI flags. Will be tuned after 30+ specs scored (Phase 3 calibration).

4. **UTF-8 with latin-1 fallback:** batch_score_directory() tries UTF-8 first, falls back to latin-1 if decode fails. Handles specs with special characters gracefully.

5. **Clarity component keeps baseline high:** A spec with all 7 sections present gets 0.30 * 1.0 = 0.3 from clarity alone. This means Gate 0 only blocks truly broken specs (< 0.2 composite). This is by design — we want Gate 0 to catch incoherent specs, not micromanage density.

## Next Steps (from plan)

**Phase 0 COMPLETE** — IRD-01 and IRD-02 done.

**Deferred to Phase 1 (after MW build):**
- IRD-04: IMPL doc density gate (requires doc-driven dev process first)

**Deferred to Phase 3 (after 30+ tasks with actuals):**
- IRD-03: Calibration ledger integration (requires EST-02 + build history)
- Threshold tuning based on correlation analysis

## Notes

- Gate 0 now has 6 checks: priority_present, acceptance_criteria_present, file_paths_exist, deliverables_coherence, scope_sanity, **ir_density**
- All existing specs in `.deia/hive/queue/backlog/` pass Gate 0 (3 scored, average density: 0.447)
- Batch scorer auto-detects mode (spec vs prism) from file content
- CSV output includes all fields from score result (variable columns depending on mode)
- JSON output is valid JSON array, parseable by `jq` and other tools

## Deliverables Summary

| Deliverable | Status | Lines | Tests |
|-------------|--------|-------|-------|
| batch_score_directory() | ✓ | 32 | 4 |
| gate_check_file() | ✓ | 58 | 5 |
| format_table() | ✓ | 67 | 2 |
| format_json() | ✓ | 7 | 1 |
| format_csv() | ✓ | 19 | 1 |
| check_ir_density() (gate0.py) | ✓ | 95 | 2 |
| cmd_batch() | ✓ | 14 | — |
| cmd_gate_check() | ✓ | 11 | — |

**Total:** 303 lines added, 14 tests added, all tests pass.
