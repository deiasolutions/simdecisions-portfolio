---
id: WIKI-102
priority: P1
model: sonnet
role: bee
depends_on:
  - WIKI-101
---
# SPEC-WIKI-102: Wikilink Parser and Frontmatter Extractor

## Priority
P1

## Model Assignment
sonnet

## Depends On
- WIKI-101

## Intent
Build wikilink parser and frontmatter parser as pure functions. These functions extract structured data from markdown content. No database writes, no API routes — just parsing logic with comprehensive tests.

## Files to Read First
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/queue/_stage/SPEC-WIKI-V1.md` — lines 173-241 for page schema examples
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/queue/_stage/SPEC-WIKI-SYSTEM.md` — lines 263-385 for frontmatter examples

## Acceptance Criteria
- [ ] File created: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/wiki/parser.py`
- [ ] `parse_wikilinks(content: str) -> List[str]` function:
  - Extracts all `[[link]]` patterns
  - Handles `[[link|display text]]` format (returns 'link', ignores display text)
  - Returns deduplicated list
  - Works with nested brackets, unicode, spaces
- [ ] `parse_frontmatter(content: str) -> Tuple[dict, str]` function:
  - Extracts YAML frontmatter between `---` delimiters
  - Returns (frontmatter_dict, content_without_frontmatter)
  - Returns ({}, original_content) if no frontmatter
  - Handles YAML lists, nested dicts, strings, numbers
- [ ] At least 8 tests for wikilink parsing:
  - Basic `[[link]]`
  - With display text `[[link|text]]`
  - Multiple links in one document
  - Links with spaces and special chars
  - No links (empty result)
  - Nested brackets edge case
  - Unicode links
  - Deduplication
- [ ] At least 6 tests for frontmatter parsing:
  - Valid YAML frontmatter
  - No frontmatter
  - Empty frontmatter
  - Frontmatter with lists
  - Frontmatter with nested objects
  - Malformed YAML (should not crash)
- [ ] No file over 500 lines

## Constraints
- You are in EXECUTE mode. Write all code and tests. Do NOT enter plan mode. Do NOT ask for approval. Just build it.
- Use regex for wikilink parsing: `/\[\[([^\]|]+)(?:\|[^\]]+)?\]\]/g`
- Use PyYAML for frontmatter parsing
- Pure functions — no side effects, no database access
- TDD: tests first
- No stubs
- No git operations

## Smoke Test
```bash
cd hivenode && python -m pytest wiki/tests/test_parser.py -v
```

Expected: All 14+ tests pass.
