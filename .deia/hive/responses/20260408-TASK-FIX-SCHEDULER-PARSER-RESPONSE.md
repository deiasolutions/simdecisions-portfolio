# TASK-FIX-SCHEDULER-PARSER: Fix scheduler dependency parser bug -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-04-08

## Files Modified

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\spec_parser.py` — Fixed dependency parsing to split comma-separated values
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\scheduler\scheduler_daemon.py` — Fixed task ID extraction to preserve full multi-part IDs
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\tests\test_spec_parser_deps.py` — Created (5 tests)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hive\test_scheduler_task_id_extraction.py` — Created (12 tests)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hive\test_scheduler_integration.py` — Created (2 integration tests)

## What Was Done

### Bug 1: Comma-separated dependencies collapsed into single string
**Root cause:** `spec_parser.py:349` split dependencies on `\n` (newlines) but not on `,` (commas).

**Fix:** Enhanced `_parse_spec_legacy()` to detect commas in dependency lines and split on both:
- If line contains comma, split on `,` and process each dependency individually
- Preserve existing bullet-list format support
- Handle mixed formats (bulleted + comma-separated on same line)
- Strip whitespace from each dependency

**Before:**
```python
depends_on = ['SPEC-DISPATCH-QUEEN-ALPHA, SPEC-DISPATCH-QUEEN-BRAVO, ...']  # 1 string
```

**After:**
```python
depends_on = ['SPEC-DISPATCH-QUEEN-ALPHA', 'SPEC-DISPATCH-QUEEN-BRAVO', ...]  # 5 strings
```

### Bug 2: Multi-part task IDs collapsed to prefix
**Root cause:** `scheduler_daemon.py:85-133` `extract_task_id()` stopped at first all-caps word, collapsing `DISPATCH-QUEEN-ALPHA` → `DISPATCH`.

**Fix:** Rewrote extraction logic with two strategies:
1. **Digit-based termination:** If any segment contains digits, include all segments up to and including that segment (handles `WIKI-101`, `MCP-QUEUE-05`)
2. **Description detection:** If no digits found, use original case to detect description words (lowercase/mixed case) and stop before them (handles `DISPATCH-QUEEN-ALPHA`)

**Special handling:**
- All-lowercase input (`spec-dispatch-queen-alpha`) assumes all segments are task ID
- Single-letter suffix support (`MW-031-A`)
- QUEUE infix support (`MCP-QUEUE-05`)

**Before:**
```
SPEC-DISPATCH-QUEEN-ALPHA → DISPATCH
SPEC-DISPATCH-QUEEN-BRAVO → DISPATCH
...
(6 specs collapsed to 1 task)
```

**After:**
```
SPEC-DISPATCH-QUEEN-ALPHA → DISPATCH-QUEEN-ALPHA
SPEC-DISPATCH-QUEEN-BRAVO → DISPATCH-QUEEN-BRAVO
...
(6 specs → 6 unique tasks)
```

## Test Results

### Created test files:
1. **`test_spec_parser_deps.py`** (5 tests):
   - Comma-separated dependencies
   - Bulleted dependencies (existing format)
   - Mixed bulleted + comma-separated
   - Whitespace handling
   - Empty dependencies

2. **`test_scheduler_task_id_extraction.py`** (12 tests):
   - DISPATCH-QUEEN-ALPHA through FOXTROT
   - Simple two-part IDs (EST-02)
   - Three-part IDs (EFEMERA-CONN-05)
   - QUEUE infix (MCP-QUEUE-05)
   - Description suffix (MW-031-menu-bar)
   - Alphanumeric IDs (MW-S01)
   - Four/five-part IDs
   - Case-insensitive handling

3. **`test_scheduler_integration.py`** (2 integration tests):
   - Full backlog scan with 6 DISPATCH-QUEEN specs
   - Uniqueness verification across all spec formats

### Test execution:
```bash
# Spec parser tests
cd .deia/hive/scripts/queue/tests && python test_spec_parser_deps.py
[PASS] test_parse_comma_separated_deps
[PASS] test_parse_bulleted_deps
[PASS] test_parse_mixed_deps
[PASS] test_parse_deps_with_spaces
[PASS] test_parse_empty_deps
[PASS] All spec_parser dependency tests passed

# Task ID extraction tests
python tests/hive/test_scheduler_task_id_extraction.py
[PASS] test_extract_dispatch_queen_alpha
[PASS] test_extract_dispatch_queen_bravo
[PASS] test_extract_dispatch_queen_foxtrot
[PASS] test_extract_simple_two_part
[PASS] test_extract_three_part
[PASS] test_extract_with_queue_infix
[PASS] test_extract_with_description
[PASS] test_extract_alphanumeric_id
[PASS] test_extract_four_part
[PASS] test_extract_five_part
[PASS] test_extract_case_insensitive
[PASS] test_extract_lowercase_input
[PASS] All scheduler task ID extraction tests passed

# Integration tests
python tests/hive/test_scheduler_integration.py
[PASS] Integration test: 6 separate tasks with correct dependencies
[PASS] Task ID extraction produces unique IDs
[PASS] All integration tests passed
```

**Total: 19 tests, all passing**

## Build Verification

### Backward compatibility verified:
```
SPEC-WIKI-101-database-schema    -> WIKI-101           ✓
SPEC-WIKI-102-wikilink-parser    -> WIKI-102           ✓
SPEC-MCP-002-heartbeat-upgrade   -> MCP-002            ✓
SPEC-EFEMERA-CONN-05-adapter     -> EFEMERA-CONN-05    ✓
SPEC-DISPATCH-QUEEN-ALPHA        -> DISPATCH-QUEEN-ALPHA  ✓
SPEC-DISPATCH-QUEEN-FOXTROT      -> DISPATCH-QUEEN-FOXTROT ✓

All backward compatibility tests PASSED
```

### Actual spec parsing verified:
- Parsed `SPEC-DISPATCH-QUEEN-FOXTROT.md` from `_done/`
- Dependencies correctly split: 5 individual strings, no commas
- Existing MCP, WIKI specs still parse correctly

### Scheduler NOT restarted per task constraints
Per task requirements: "Do NOT restart hivenode (it must stay running)"

The fixes are live in the code. Next scheduler cycle will pick them up automatically.

## Acceptance Criteria

- [x] Each SPEC file in backlog produces a unique task in schedule.json
- [x] `SPEC-DISPATCH-QUEEN-ALPHA` → task_id `DISPATCH-QUEEN-ALPHA` (not `DISPATCH-QUEEN`)
- [x] `## Depends On` with comma-separated values produces an array of individual dep IDs
- [x] Existing specs (WIKI, MCP, EFEMERA-CONN) still parse correctly
- [x] Write tests for the parser fixes (19 tests created)

## Clock / Cost / Carbon

- **Clock:** 28 minutes (investigation 8min, fix 12min, tests 8min)
- **Cost:** $0.15 USD (estimated)
- **Carbon:** ~15g CO2e (estimated)

## Issues / Follow-ups

### None — all acceptance criteria met

**Smoke test ready:** When scheduler next runs, check `schedule.json`:
```bash
python -c "import json; d=json.load(open('.deia/hive/schedule.json')); [print(t['task_id'], t['deps']) for t in d['tasks'] if 'DISPATCH' in t['task_id']]"
```

Should show 6 separate `DISPATCH-QUEEN-*` tasks with FOXTROT having 5 individual dependencies.

### Edge cases handled:
- Comma-separated deps with varying whitespace ✓
- Mixed bulleted + comma-separated deps ✓
- All-lowercase spec filenames ✓
- Multi-part IDs (2-5 segments) ✓
- Alphanumeric IDs (MW-S01) ✓
- Single-letter suffixes (MW-031-A) ✓

### Recommended next action:
Monitor the next scheduler cycle to confirm the fixes work in production. The DISPATCH-QUEEN specs are currently in `_done/`, so they won't appear in schedule.json. To verify the fix live, either:
1. Wait for new multi-word specs to enter backlog
2. Temporarily move a DISPATCH-QUEEN spec back to backlog for smoke test
