# SPEC-LEDGER-01: Event Emission Foundation

## Priority
P1

## Model Assignment
sonnet

## Depends On
None

## Intent
Implement the core event emission infrastructure: event schemas, hash chaining, emission API, and storage. This is phase 1 of the Event Ledger system - establish append-only storage and basic emission before adding consumers.

## Files to Read First
.deia/BOOT.md
hivenode/main.py
hivenode/routes/__init__.py

## Acceptance Criteria
- [ ] Event base schema implemented with actor, target, context, currencies, prev_hash, event_hash fields
- [ ] Hash chaining function implemented using SHA-256 over canonical JSON
- [ ] Event storage table created (PostgreSQL compatible, SQLite fallback)
- [ ] Python emission API `emit_event()` available for backend code
- [ ] TypeScript emission API `emitEvent()` available for frontend code
- [ ] Events stored with all required fields including timestamps in ISO 8601 UTC
- [ ] Genesis event (first event with prev_hash = null) automatically created on first emission
- [ ] Hash chain integrity verifiable via sequential hash validation
- [ ] At least 3 unit tests for hash chain integrity
- [ ] At least 2 integration tests for event emission and retrieval
- [ ] No file over 500 lines
- [ ] All colors use CSS variables (if any UI components)

## Constraints
- This spec implements ONLY event emission and storage
- Event consumers (gamification, ML) are NOT in scope for this spec
- Event kinds enumeration is minimal - just SYSTEM_STARTED, TEST_EVENT, and placeholders for future kinds
- Use SQLAlchemy Core pattern (not ORM) per existing hivenode patterns
- Database must support both PostgreSQL (production) and SQLite (local dev)
- All file paths absolute in implementation
- No stubs - complete implementation of all functions
- No git operations

## Smoke Test
After completion:
1. Start hivenode backend
2. Call `emit_event(kind="TEST_EVENT", actor_id="test", target_id="test", context={})` from Python
3. Query events table - should show 2 events: SYSTEM_STARTED (genesis) and TEST_EVENT
4. Verify prev_hash of TEST_EVENT matches event_hash of SYSTEM_STARTED
5. Run integrity validation - should pass for all stored events
