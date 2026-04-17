# TASK-225: InMemoryPipelineStore Implementation

**Priority:** P1
**Model Assignment:** haiku
**Parent Spec:** SPEC-PIPELINE-001 (Unified Build Pipeline)
**Dependencies:** TASK-222 (COMPLETE — PipelineStore ABC + FilesystemPipelineStore)

---

## Objective

Implement an in-memory version of the `PipelineStore` ABC to enable DES (Discrete Event Simulation) mode for the build pipeline. This store uses Python dicts and lists instead of filesystem operations.

---

## Context

Part of SPEC-PIPELINE-001 Wave 2 (W2-B). The build pipeline needs two runtimes:
1. **Production mode:** FilesystemPipelineStore (COMPLETE in TASK-222)
2. **DES simulation mode:** InMemoryPipelineStore (THIS TASK)

The DES engine will use the in-memory store to simulate queue operations without touching the filesystem. This enables capacity planning, bottleneck analysis, and performance predictions.

The in-memory store must pass the same test suite structure as the filesystem store, proving both implementations satisfy the `PipelineStore` protocol.

---

## Files to Read First

Before writing code, read these files to understand the interface and reference implementation:

1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\pipeline_store.py` — The `PipelineStore` ABC and `SpecFile` dataclass
2. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\filesystem_store.py` — Reference implementation (use as pattern)
3. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\tests\test_pipeline_store.py` — Existing filesystem tests (mirror these)
4. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\specs\SPEC-PIPELINE-001-UNIFIED-BUILD-PIPELINE.md` — Section 6.3 (InMemoryPipelineStore design)

---

## Deliverables

### 1. Implementation File

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\inmemory_store.py`

**Requirements:**
- Class `InMemoryPipelineStore(PipelineStore)` implementing all abstract methods
- No filesystem operations — pure in-memory using dicts and lists
- Stages stored as dict of lists: `{"hold": [], "queue": [], "active": [], "done": [], "failed": [], "needs_review": [], "dead": []}`
- Events stored as append-only list: `self.events = []`
- Spec content stored and modifiable (append_section works)
- All abstract methods fully implemented:
  - `list_specs(stage: str) -> list[SpecFile]`
  - `move_spec(spec_id, from_stage, to_stage, metadata=None)`
  - `append_section(spec_id, stage, section_name, content)`
  - `get_done_ids() -> set[str]`
  - `deps_satisfied(spec: SpecFile) -> bool`
  - `emit_event(event: dict)`
  - `get_orphans() -> list[SpecFile]`

**Implementation Pattern (from SPEC-PIPELINE-001 Section 6.3):**

```python
class InMemoryPipelineStore(PipelineStore):
    """DES runtime. Dicts are the state machine."""

    def __init__(self):
        self.stages = {
            "hold": [], "queue": [], "active": [], "done": [],
            "failed": [], "needs_review": [], "dead": [],
        }
        self.events = []  # append-only list

    def move_spec(self, spec_id, from_stage, to_stage, metadata=None):
        spec = self._pop_spec(spec_id, from_stage)
        if metadata:
            spec.content += f"\n## {metadata['section']}\n{metadata['content']}\n"
        self.stages[to_stage].append(spec)
        self.events.append({
            "event_type": "spec_transition",
            "spec_id": spec_id,
            "from": from_stage,
            "to": to_stage,
        })
```

**Key Differences from FilesystemPipelineStore:**
- No pathlib, no file I/O
- `SpecFile` objects stored directly in lists
- Modifying spec content = modifying the `SpecFile.content` string in-place
- Events append to `self.events` list instead of writing to DB

### 2. Test File

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\tests\test_inmemory_store.py`

**Requirements:**
- **TDD: Write tests FIRST, then implementation**
- **Mirror the structure of filesystem store tests** from `test_pipeline_store.py`
- Test all PipelineStore methods work correctly with in-memory state
- Test event recording (events append to list)
- Test spec content modification (append_section)
- **Minimum 10 tests**

**Test Coverage (mirror filesystem tests):**
1. `test_inmemory_store_initialization` — verify stages dict and events list created
2. `test_list_specs_empty_queue` — returns empty list for empty stage
3. `test_list_specs_returns_specs_in_queue` — returns specs from stage
4. `test_move_spec_between_stages` — spec moves from one stage list to another
5. `test_get_done_ids_empty` — returns empty set when done stage is empty
6. `test_get_done_ids_returns_spec_ids` — returns set of IDs from done stage
7. `test_deps_satisfied_no_dependencies` — returns True when spec has no deps
8. `test_deps_satisfied_all_deps_in_done` — returns True when all deps satisfied
9. `test_deps_satisfied_missing_dependency` — returns False when dep missing
10. `test_get_orphans_empty` — returns empty list when active is empty
11. `test_get_orphans_returns_active_specs` — returns specs in active stage
12. `test_append_section` — section added to spec content
13. `test_move_spec_with_metadata` — metadata appended during move
14. `test_emit_event` — event appended to events list

---

## Test Requirements

- [ ] **TDD:** Tests written FIRST (before implementation)
- [ ] All tests pass (`pytest test_inmemory_store.py -v`)
- [ ] Minimum 10 tests (14 listed above is ideal)
- [ ] Tests mirror filesystem store test structure
- [ ] Edge cases covered:
  - Empty stages (no specs)
  - Missing specs (spec_id not found)
  - Dependency checking with partial matches
  - Event emission
  - Content modification

---

## Constraints

- **No file over 500 lines** (this task will be ~100 lines implementation + ~150 lines tests)
- **No stubs** — every method fully implemented
- **No filesystem operations** — pure in-memory (dicts, lists, strings only)
- **Model:** haiku (fast, low-cost for straightforward implementation)
- **TDD:** Tests first, then implementation

---

## Acceptance Criteria

- [ ] `InMemoryPipelineStore` class exists and inherits from `PipelineStore`
- [ ] All abstract methods implemented (no `NotImplementedError`)
- [ ] Stages stored as dict of lists (7 stages: hold, queue, active, done, failed, needs_review, dead)
- [ ] Events stored as append-only list (`self.events = []`)
- [ ] Spec content stored and modifiable (append_section works)
- [ ] Tests mirror filesystem store tests (≥10 tests)
- [ ] All tests pass (`pytest test_inmemory_store.py -v`)
- [ ] No filesystem operations in implementation
- [ ] File under 500 lines (should be ~100 lines)

---

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260317-TASK-225-RESPONSE.md`

The response MUST contain these 8 sections:

### 1. Header
```markdown
# TASK-225: InMemoryPipelineStore Implementation -- COMPLETE

**Status:** COMPLETE | FAILED (reason)
**Model:** haiku
**Date:** 2026-03-17
```

### 2. Files Modified
List every file created/modified/deleted with full absolute paths:
```markdown
## Files Modified
- C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\inmemory_store.py (CREATED, 95 lines)
- C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\tests\test_inmemory_store.py (CREATED, 165 lines)
```

### 3. What Was Done
Bullet list of concrete changes, not intent:
```markdown
## What Was Done
- Created `InMemoryPipelineStore` class implementing `PipelineStore` ABC
- Implemented 7 abstract methods using dict of lists for stages
- Implemented event recording to append-only list
- Implemented spec content modification via string concatenation
- Created 14 tests mirroring filesystem store test structure
- All tests pass
```

### 4. Test Results
```markdown
## Test Results
- Test file: `test_inmemory_store.py`
- Tests run: 14
- Tests passed: 14
- Tests failed: 0
```

### 5. Build Verification
```markdown
## Build Verification
- Tests pass: YES
- pytest output summary: `14 passed in 0.12s`
- No build required (pure Python module)
```

### 6. Acceptance Criteria
Copy from task, mark [x] or [ ]:
```markdown
## Acceptance Criteria
- [x] `InMemoryPipelineStore` class exists and inherits from `PipelineStore`
- [x] All abstract methods implemented (no `NotImplementedError`)
- [x] Stages stored as dict of lists (7 stages)
- [x] Events stored as append-only list
- [x] Spec content stored and modifiable
- [x] Tests mirror filesystem store tests (≥10 tests)
- [x] All tests pass
- [x] No filesystem operations in implementation
- [x] File under 500 lines
```

### 7. Clock / Cost / Carbon
```markdown
## Clock / Cost / Carbon
- **Clock:** 8 minutes (5 min tests, 3 min implementation)
- **Cost:** $0.02 (Haiku, ~12K tokens in + 3K tokens out)
- **Carbon:** ~0.002 kg CO2e
```

### 8. Issues / Follow-ups
```markdown
## Issues / Follow-ups
- None — implementation complete and tested
- Ready for Wave 3 (W3-A: PHASE-IR flow encoding)
```

DO NOT skip any section. All 8 sections are mandatory.

---

## Test Command

From repository root:
```bash
cd .deia/hive/scripts/queue
python -m pytest tests/test_inmemory_store.py -v
```

---

**END OF TASK FILE**
