# Unregistered Routes Analysis

**Date:** 2026-04-08

## Summary

This analysis identifies route modules that exist in the codebase but may not be properly registered in `hivenode/routes/__init__.py:create_router()`.

## Route Module Files Found

Total route files discovered: 38

### Registered in create_router() ✓

Based on imports in `hivenode/routes/__init__.py`:

1. ✓ health.router
2. ✓ auth.router
3. ✓ ledger_routes.router
4. ✓ storage_routes.router
5. ✓ node.router
6. ✓ llm_routes.router
7. ✓ shell.router
8. ✓ sync_routes.router
9. ✓ kanban_routes.router
10. ✓ progress_routes.router
11. ✓ build_monitor.router
12. ✓ sim.router
13. ✓ inventory_routes.router
14. ✓ des_routes.router
15. ✓ phase_nl_routes.router
16. ✓ pipeline_sim.router
17. ✓ optimize_routes.router
18. ✓ tabletop_routes.router
19. ✓ preferences.router
20. ✓ early_access.router
21. ✓ queue_events.router
22. ✓ prism_routes.router
23. ✓ voice_routes.router
24. ✓ notifications.router
25. ✓ repo.routes (from hivenode.repo)
26. ✓ rag_routes.router
27. ✓ indexer_routes.router (mounted separately in main.py)
28. ✓ bok_routes.router (mounted separately in main.py)
29. ✓ relay_routes.router
30. ✓ relay_message_routes.router
31. ✓ relay_moderation_routes.router
32. ✓ entity_routes.router (mounted separately in main.py)
33. ✓ playback_routes.router
34. ✓ compare_router (mounted separately in main.py)
35. ✓ phase_schema_routes.router (from engine.phase_ir)
36. ✓ phase_trace_routes.router (from engine.phase_ir)
37. ✓ phase_validation_routes.router (from engine.phase_ir)

### Potentially Unregistered ⚠️

Route modules that exist but NOT found in create_router():

1. ⚠️ **hivenode/routes/build_monitor_claims.py** - Build monitor claims management
2. ⚠️ **hivenode/routes/build_monitor_liveness.py** - Liveness tracking
3. ⚠️ **hivenode/routes/build_monitor_slots.py** - Slot management
4. ⚠️ **hivenode/routes/build_slots.py** - Build slots
5. ⚠️ **hivenode/routes/canvas_chat.py** - Canvas chat routes
6. ⚠️ **hivenode/routes/llm_chat_routes.py** - Additional LLM chat routes
7. ⚠️ **hivenode/terminal/routes.py** - Terminal routes
8. ⚠️ **hivenode/entities/archetype_routes.py** - Archetype routes (main.py mounts entities but not archetype separately)

## Analysis Notes

### canvas_chat.py Investigation

Found route: `@router.post("/api/canvas/chat")`

This route exists but the router is not imported in `__init__.py`. This appears to be a standalone Canvas integration route.

**Status:** UNREGISTERED

### llm_chat_routes.py Investigation

This file has routes but is NOT imported in `__init__.py`. Only `llm_routes.py` is imported.

**Status:** UNREGISTERED

### build_monitor_* modules Investigation

Multiple build monitor sub-modules exist:
- build_monitor.py (✓ registered)
- build_monitor_claims.py (⚠️ not registered)
- build_monitor_liveness.py (⚠️ not registered)
- build_monitor_slots.py (⚠️ not registered)
- build_slots.py (⚠️ not registered)

These may be sub-routers included in build_monitor.py itself, not directly in create_router().

**Status:** NEEDS VERIFICATION

### terminal/routes.py Investigation

A terminal module exists with routes but is not imported anywhere in routes/__init__.py.

**Status:** UNREGISTERED

### archetype_routes.py Investigation

Found in `hivenode/entities/archetype_routes.py`. Main.py includes `archetype_router` import and mounting:

```python
from hivenode.entities.archetype_routes import router as archetype_router
app.include_router(archetype_router)
```

**Status:** REGISTERED (but in main.py, not create_router())

## Recommendations

1. **Verify build_monitor sub-modules** - Check if build_monitor.py includes sub-routers
2. **Register canvas_chat routes** - Add to create_router() if needed
3. **Consolidate LLM routes** - Merge llm_chat_routes.py into llm_routes.py or register separately
4. **Register terminal routes** - Add terminal.router to create_router()
5. **Document main.py registrations** - Routes mounted directly in main.py should be listed in a comment

## 404 vs Unregistered Correlation

Many 404s in smoke test may be due to:

1. **Wrong path assumptions** - Test script guessed paths that don't match actual routes
2. **Missing auth** - Some routes may exist but reject unauthenticated requests as 404
3. **Method mismatches** - Routes exist but use different HTTP methods
4. **Actual missing routes** - Auth routes, many ledger routes, storage info, etc.

To resolve 404s:
- Read actual route files to find correct paths and methods
- Check if routes use auth dependencies (may return 404 instead of 401)
- Verify route prefix in create_router() matches route decorator paths
