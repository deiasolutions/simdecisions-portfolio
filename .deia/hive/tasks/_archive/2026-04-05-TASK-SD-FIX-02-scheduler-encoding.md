# TASK-SD-FIX-02: Fix Scheduler UTF-8 Encoding for _done/ Parsing

## Objective
Fix the scheduler daemon's file reading to use UTF-8 encoding with error replacement when parsing specs in `_done/` directory, preventing codec errors on files containing unicode characters (emoji, special chars).

## Context
The scheduler daemon logs warnings when parsing specs in `_done/` that contain unicode characters:

```
Failed to parse SPEC-CANVAS3-SVG-ICONS.md: 'charmap' codec can't decode byte 0x8f
Failed to parse SPEC-KB-001A-keyboard-primitive-core.md: 'charmap' codec can't decode byte 0x8f
```

This happens because the `load_velocity_from_done()` function (line 107-146) uses `spec_file.read_text()` without specifying encoding, causing it to use the system default encoding (often cp1252 on Windows) which fails on unicode characters from bee output (emoji, special chars, etc.).

**Current code (line 130):**
```python
content = spec_file.read_text()
```

**Fix needed:**
```python
content = spec_file.read_text(encoding='utf-8', errors='replace')
```

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\scheduler\scheduler_daemon.py`
  Line 130 contains the problematic `read_text()` call in `load_velocity_from_done()`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\scheduler\test_scheduler_daemon.py`
  Existing tests for scheduler daemon

## Deliverables
- [ ] Add `encoding='utf-8', errors='replace'` to `spec_file.read_text()` call in `load_velocity_from_done()` (line 130)
- [ ] Add new test: `test_velocity_from_unicode_spec_content()`
  - Test that specs with emoji/unicode characters are parsed without error
  - Test that velocity computation still works correctly
- [ ] Verify all existing scheduler tests still pass

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All existing scheduler tests pass
- [ ] New test passes
- [ ] Edge cases covered:
  - Spec with emoji in title (e.g., "✅ Complete")
  - Spec with unicode special characters (e.g., "→", "•", "…")
  - Spec with mixed ASCII and UTF-8 content
  - Telemetry parsing still works after encoding fix

## Constraints
- No file over 500 lines
- TDD: write failing test first, then fix implementation
- No stubs
- Do not modify any other part of the scheduler daemon
- The fix should be minimal (one-line change)

## Implementation Notes
The fix is straightforward:

**Before:**
```python
content = spec_file.read_text()
```

**After:**
```python
content = spec_file.read_text(encoding='utf-8', errors='replace')
```

The `errors='replace'` parameter ensures that any undecodable bytes are replaced with the Unicode replacement character (�) rather than raising an exception. This is safe for telemetry parsing since the regex patterns only look for ASCII numeric values.

## Test Implementation
Create a test that writes a spec with unicode content to `_done/`, then verifies `load_velocity_from_done()` doesn't crash:

```python
def test_velocity_from_unicode_spec_content(temp_dirs):
    """Specs with unicode content should be parsed without codec errors."""
    spec = temp_dirs["done_dir"] / "SPEC-TEST-UNICODE.md"
    spec.write_text("""# SPEC-TEST-UNICODE ✅

## Summary
Task completed → success! 🎉

## Telemetry
- Estimated: 2 hours
- Actual: 1.8 hours
""", encoding='utf-8')

    velocity = load_velocity_from_done(temp_dirs["done_dir"])

    # Should not crash, velocity should be computed correctly
    assert velocity == 1.8 / 2.0  # 0.9
```

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260405-TASK-SD-FIX-02-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Acceptance Criteria** — copy from task, mark [x] or [ ]
5. **Test Results** — test files run, pass/fail counts
6. **Build Verification** — test/build output summary
7. **Clock / Cost / Carbon** — platform-populated from build monitor telemetry (do not estimate manually)
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.
