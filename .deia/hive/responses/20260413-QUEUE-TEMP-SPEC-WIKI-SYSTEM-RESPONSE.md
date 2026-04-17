# SPEC-WIKI-SYSTEM: FBB Wiki System Specification -- BLOCKED

**Status:** BLOCKED (dispatch protocol violation)
**Model:** Sonnet
**Date:** 2026-04-13
**Bot ID:** BEE-QUEUE-TEMP-SPEC-WIKI-SYSTEM

## Files Modified
None - task not started

## What Was Done
Analyzed task assignment and identified protocol violation

## Tests Run
None - blocked before implementation

## Deliverables
N/A - task blocked

## Blockers
**CRITICAL: Improper dispatch detected**

This spec was placed in `.deia/hive/tasks/` as `QUEUE-TEMP-SPEC-WIKI-SYSTEM.md`, triggering direct bee dispatch. However:

1. **This is a full spec, not a bee task**
   - 500+ lines covering architecture, schema, API, frontend, compilation services
   - Spans 5 implementation phases
   - Multiple acceptance criteria across different domains

2. **Chain of Command Violation**
   - Per HIVE.md: Q88N → Q88NR → Q33N → Bees
   - Q88NR should write briefing for Q33N
   - Q33N should break spec into discrete bee tasks
   - Bees execute specific, scoped tasks

3. **Worker Bee Role Constraint**
   - I'm b33 (worker bee): "You write code, run tests, report results"
   - I do NOT orchestrate or implement entire systems
   - I need a focused task like "Implement wiki_pages table" or "Build WikiEditor component"

## Recommendations

**Option 1: Return to Q33NR for proper dispatch**
1. Q33NR reads SPEC-WIKI-SYSTEM
2. Q33NR writes briefing for Q33N
3. Q33N creates task breakdown (e.g., TASK-WIKI-001 through TASK-WIKI-015)
4. Q33NR approves task files
5. Bees execute individual tasks

**Option 2: Emergency simplified scope (if urgent)**
If Q88N needs immediate progress on this spec:
1. Define Phase 1 only (schema + basic API)
2. Create single focused task: "Implement wiki_pages table and CRUD endpoints"
3. Dispatch that specific task to a bee
4. Subsequent phases dispatched separately

## Cost Summary
- Input tokens: ~15,000 (reading spec + context)
- Output tokens: ~1,000 (this response)
- Estimated cost: ~$0.15
- **No implementation cost incurred** - blocked before work started

## Next Steps Required
**Q88NR or Q88N must:**
1. Acknowledge this blocker
2. Choose Option 1 (proper dispatch) or Option 2 (emergency scope)
3. Either:
   - Route SPEC-WIKI-SYSTEM to Q33N for task breakdown, OR
   - Create a focused Phase 1 task file and dispatch to a bee

**I await instructions.**

---

## Context Notes

The spec itself is well-formed and comprehensive:
- Clear acceptance criteria
- Detailed technical design
- Migration path with phases
- API schemas defined
- Frontend component structure outlined

The issue is purely procedural: a spec entered the queue without Q33N task breakdown, resulting in improper bee dispatch.

## Spec Summary (for Q33N when properly dispatched)

If this goes to Q33N for breakdown, key task candidates:

**Database Layer:**
- TASK-WIKI-001: Create wiki_pages table + indexes
- TASK-WIKI-002: Create wiki_compilation_log table
- TASK-WIKI-003: Create wiki_raw_sources table

**Backend Services:**
- TASK-WIKI-004: Implement WikiRetrievalService
- TASK-WIKI-005: Implement ClinicalWikiCompiler
- TASK-WIKI-006: Implement FamilyWikiCompiler
- TASK-WIKI-007: Implement wiki CRUD API endpoints

**Frontend Components:**
- TASK-WIKI-008: Build WikiTree component
- TASK-WIKI-009: Build WikiEditor component
- TASK-WIKI-010: Build WikiExplorer layout
- TASK-WIKI-011: Implement wikilink parser/renderer

**Integration:**
- TASK-WIKI-012: Wire retrieval service to prompt assembly
- TASK-WIKI-013: Add post-chat compilation hook
- TASK-WIKI-014: Implement progression page auto-generation

**Testing:**
- TASK-WIKI-015: Write integration tests for wiki compilation
- TASK-WIKI-016: Write frontend tests for WikiExplorer

Estimated: 15-20 discrete bee tasks across 5 phases
