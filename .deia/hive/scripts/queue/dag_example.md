# DAG Support Examples

FACTORY-007: DAG support for shared module references.

## Overview

PRISM-IR v1.1 adds support for DAG (Directed Acyclic Graph) structure through SHARED_REF nodes. This allows multiple specs to reference the same shared module without duplicating work.

## Node Types

### ORIGINAL
Standard node with its own content, acceptance criteria, and lifecycle.

### SHARED_REF
Reference to an ORIGINAL node. Used when multiple nodes depend on the same module.
- `target_id`: points to the ORIGINAL node
- Does not have its own content or acceptance_criteria (inherits from target)
- Phase mirrors target's phase
- When target is BUILT, all SHARED_REFs are automatically BUILT

## Usage

### Creating a SHARED_REF spec

```markdown
---
id: REF-FILE-SAVE-001
priority: P1
model: sonnet
node_type: SHARED_REF
target_id: SHARED-FILE-SAVE
depends_on: []
---
# SPEC-REF-FILE-SAVE-001: Reference to Shared File Save Module

## Intent
This spec references the shared file save module that is built separately.

## Acceptance Criteria
- [ ] Inherits from SHARED-FILE-SAVE target

## Constraints
- Manual annotation only for now
```

### Creating an ORIGINAL shared module

```markdown
---
id: SHARED-FILE-SAVE
priority: P1
model: sonnet
node_type: ORIGINAL
depends_on: []
content_type: python_file
---
# SPEC-SHARED-FILE-SAVE: Shared File Save Module

## Intent
Implement file save logic used by multiple applications.

## Acceptance Criteria
- [ ] Syntax valid
- [ ] All imports resolve
- [ ] Tests pass
- [ ] Handles common file formats (txt, json, csv)

## Constraints
- Must be reusable across Word, Excel, PowerPoint
```

## Example: Office Suite with Shared Modules

```
OFFICE-SUITE (root)
│
├── WORD
│   ├── EDITOR
│   └── REF-FILE-SAVE → SHARED-FILE-SAVE
│
├── EXCEL
│   ├── GRID
│   └── REF-FILE-SAVE → SHARED-FILE-SAVE
│
├── POWERPOINT
│   ├── SLIDES
│   └── REF-FILE-SAVE → SHARED-FILE-SAVE
│
└── SHARED-FILE-SAVE (ORIGINAL)
    └── (built once, referenced by all three apps)
```

## API Usage

### Find dangling references

```python
from spec_parser import parse_spec, find_dangling_refs

# Parse all specs in queue
specs = [parse_spec(spec_path) for spec_path in queue_dir.glob("SPEC-*.md")]

# Find SHARED_REF nodes with invalid target_id
dangling = find_dangling_refs(specs)
if dangling:
    print(f"Warning: {len(dangling)} dangling references found")
    for spec in dangling:
        print(f"  {spec.id} → {spec.target_id} (not found)")
```

### Resolve SHARED_REF phases in manifest

```python
from spec_parser import resolve_shared_refs

# Load manifest
with open("manifest.json") as f:
    manifest = json.load(f)

# Resolve SHARED_REF nodes to inherit phase from targets
manifest = resolve_shared_refs(manifest)

# Now all SHARED_REF nodes have correct phase from their targets
```

### Traverse DAG with cycle detection

```python
from dag_traversal import traverse_dag_specs

specs_by_id = {spec.id: spec for spec in specs}
visited = set()

# Traverse from a starting spec
reachable = traverse_dag_specs("WORD", specs_by_id, visited)
print(f"WORD depends on: {reachable}")

# SHARED-FILE-SAVE appears only once even if referenced multiple times
```

### Check for circular dependencies

```python
from dag_traversal import check_circular_dependencies

cycles = check_circular_dependencies(specs)
if cycles:
    print("Circular dependencies detected:")
    for spec_id, dep_id in cycles:
        print(f"  {spec_id} → {dep_id} (cycle)")
```

### Topological sort

```python
from dag_traversal import topological_sort_specs

# Get specs in dependency order (build order)
sorted_ids = topological_sort_specs(specs)
print("Build order:", sorted_ids)

# Specs with no dependencies come first
# Dependencies are built before dependents
```

## Constraints

1. **Manual annotation only** — Automated similarity detection is out of scope for FACTORY-007
2. **SHARED_REF specs are lightweight** — Just frontmatter + short description
3. **DAG traversal must use visited set** — Prevents infinite loops on cycles
4. **No file over 500 lines** — Per Hard Rule 4

## Integration Points

### Scheduler
- Uses `traverse_dag_specs()` to compute transitive dependencies
- Uses `check_circular_dependencies()` to validate specs before dispatch
- Uses `topological_sort_specs()` to determine build order

### Executor
- Uses `resolve_shared_refs()` on manifest before dispatch
- SHARED_REF nodes inherit phase from target automatically
- When target is BUILT, all referencing SHARED_REFs become BUILT

### Queue Runner
- Calls `find_dangling_refs()` on backlog scan
- Warns if SHARED_REF nodes have invalid target_id
- Prevents dispatch of dangling refs (blocks until fixed)

## Future Enhancements (Out of Scope)

- Automated similarity detection to suggest shared module extraction
- Version tracking for shared modules (dependents re-evaluated on update)
- Lazy loading of shared modules (build only when first referenced)
- Shared module caching across specs
