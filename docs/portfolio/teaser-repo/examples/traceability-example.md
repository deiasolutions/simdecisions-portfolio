# Traceability System Example

**System:** REQ → SPEC → TASK → CODE → TEST lineage tracking
**Purpose:** Portfolio demonstration of traceability DAG

---

## ID Format

| Level | Prefix | Example | Description |
|-------|--------|---------|-------------|
| L0 | `REQ-{CAT}-{NNN}` | `REQ-UI-001` | Requirements from ASSIGNMENT |
| L1 | `SPEC-{NNN}` | `SPEC-001` | Specification items |
| L2 | `TASK-{NNN}` | `TASK-001` | Implementation tasks |
| L3 | `CODE-{NNN}` | `CODE-001` | Code artifacts (files/functions) |
| L4 | `TEST-{NNN}` | `TEST-001` | Test cases |

**Categories for Requirements:**

- `UI` - User interface
- `BE` - Backend/API
- `DB` - Database
- `SEC` - Security
- `PERF` - Performance
- `TEST` - Testing
- `DOC` - Documentation

---

## Example: Export Button Feature

### Requirement (L0)

```markdown
## REQ-UI-001: Export Button

**Category:** UI
**Type:** user_story
**Mandatory:** true

**Description:** User can click Export button in canvas toolbar to export current scenario.

**Acceptance Criteria:**
- Export button appears in toolbar next to zoom controls
- Clicking button opens export dialog
- Icon uses Lucide Download icon
- Button disabled when no scenario loaded
```

### Specification (L1)

```markdown
## SPEC-001: Export Button Component

**Implements:** REQ-UI-001
**Category:** UI

The Export button appears in the canvas toolbar next to the zoom controls.
Clicking the button opens the export dialog. The button uses the Lucide
Download icon and is disabled when no scenario is loaded.

### Acceptance Criteria
- Button visible in toolbar
- Clicking button opens export dialog
- Icon uses Lucide Download icon
- Button disabled when no scenario loaded
```

### Task (L2)

```markdown
## TASK-001: Build Export Button Component

**Implements:** SPEC-001
**Satisfies:** REQ-UI-001
**Assignee:** Haiku
**Complexity:** Simple

Create a new ExportButton.tsx component that renders in the toolbar.

### Files to Create
- browser/src/components/buttons/ExportButton.tsx
- browser/src/components/buttons/ExportButton.test.tsx

### Dependencies
- None (standalone component)

### Acceptance Criteria
- [x] ExportButton.tsx created
- [x] ExportButton.test.tsx created
- [x] Toolbar.tsx modified to include button
- [x] Tests written first (TDD)
- [x] All tests pass
```

### Code (L3)

```typescript
// Implements: TASK-001 | Satisfies: REQ-UI-001
// File: browser/src/components/buttons/ExportButton.tsx
// Code ID: CODE-001

import { Download } from 'lucide-react';
import { useUIStore } from '../../stores/uiStore';

export function ExportButton() {
  const { openExportDialog, scenarioLoaded } = useUIStore();

  return (
    <button
      onClick={openExportDialog}
      disabled={!scenarioLoaded}
      className="toolbar-button"
      title="Export Scenario"
      style={{
        color: 'var(--sd-text-primary)',
        backgroundColor: 'var(--sd-bg-secondary)',
      }}
    >
      <Download size={20} />
    </button>
  );
}
```

### Tests (L4)

```typescript
// Verifies: REQ-UI-001
// File: browser/src/components/buttons/ExportButton.test.tsx
// Test IDs: TEST-001, TEST-002, TEST-003, TEST-004

import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { ExportButton } from './ExportButton';

describe('ExportButton', () => {
  // TEST-001: Verifies REQ-UI-001 (button renders)
  it('renders export button in toolbar', () => {
    render(<ExportButton />);
    expect(screen.getByTitle('Export Scenario')).toBeInTheDocument();
  });

  // TEST-002: Verifies REQ-UI-001 (click behavior)
  it('opens export dialog on click', () => {
    const mockOpen = vi.fn();
    vi.mock('../../stores/uiStore', () => ({
      useUIStore: () => ({ openExportDialog: mockOpen, scenarioLoaded: true }),
    }));

    render(<ExportButton />);
    fireEvent.click(screen.getByTitle('Export Scenario'));
    expect(mockOpen).toHaveBeenCalledTimes(1);
  });

  // TEST-003: Verifies REQ-UI-001 (disabled state)
  it('is disabled when no scenario loaded', () => {
    vi.mock('../../stores/uiStore', () => ({
      useUIStore: () => ({ openExportDialog: vi.fn(), scenarioLoaded: false }),
    }));

    render(<ExportButton />);
    expect(screen.getByTitle('Export Scenario')).toBeDisabled();
  });

  // TEST-004: Verifies REQ-UI-001 (icon presence)
  it('uses Lucide Download icon', () => {
    render(<ExportButton />);
    const button = screen.getByTitle('Export Scenario');
    expect(button.querySelector('svg')).toBeInTheDocument();
  });
});
```

---

## Traceability Graph (DAG)

```
REQ-UI-001 (User clicks Export)
    ↓ implements
SPEC-001 (Export Button Component)
    ↓ breaks_into
TASK-001 (Build ExportButton.tsx)
    ↓ produces
CODE-001 (ExportButton.tsx)
    ↓ tested_by
TEST-001 (Export button renders)
TEST-002 (Opens export dialog on click)
TEST-003 (Disabled when no scenario)
TEST-004 (Uses Lucide Download icon)
```

---

## Graph Schema

```typescript
interface TraceabilityGraph {
  nodes: TraceNode[];
  edges: TraceEdge[];
}

interface TraceNode {
  id: string;                    // REQ-UI-001, SPEC-001, etc.
  type: 'requirement' | 'spec' | 'task' | 'code' | 'test';
  data: {
    text?: string;               // Human-readable description
    file?: string;               // Source file path
    line?: number;               // Line number in file
    category?: string;           // UI, Backend, Security, etc.
    mandatory?: boolean;         // Is this required?
    embedding?: number[];        // Voyage embedding (1024 dimensions)
  };
}

interface TraceEdge {
  source: string;                // Parent node ID
  target: string;                // Child node ID
  type: 'implements' | 'breaks_into' | 'produces' | 'tested_by';
}
```

---

## Graph Queries (Examples)

```python
# Find all code implementing UI requirements
ui_code = graph.query(
    start_type='requirement',
    category='UI',
    end_type='code'
)
# Returns: [CODE-001, CODE-002, ...]

# Find orphaned requirements (no downstream implementation)
orphans = graph.find_nodes(
    type='requirement',
    has_outgoing_edges=False
)
# Returns: [REQ-UI-003, REQ-BE-005, ...]

# Get full lineage for a requirement
lineage = graph.get_descendants('REQ-UI-001')
# Returns: [SPEC-001, TASK-001, CODE-001, TEST-001, TEST-002, TEST-003, TEST-004]

# Find all tests verifying a specific requirement
tests = graph.query(
    start_node='REQ-UI-001',
    end_type='test'
)
# Returns: [TEST-001, TEST-002, TEST-003, TEST-004]
```

---

## Benefits

1. **Impact Analysis:** "If I change REQ-UI-001, what code/tests are affected?"
2. **Coverage Verification:** "Does every requirement have at least one test?"
3. **Orphan Detection:** "Are there requirements with no implementation?"
4. **Traceability Audits:** "For compliance, show me the full lineage from requirement to shipped code."
5. **Debugging:** "Which requirement caused this test to fail?"

---

## Enforcement

- **Task templates** mandate traceability comments
- **Code review** (Q33N) checks for missing IDs
- **Validation gates** verify every SPEC/TASK has a REQ- reference
- **Test suites** must include `// Verifies: REQ-XX-NNN` comments

---

**END OF TRACEABILITY EXAMPLE**

Full traceability graph implementation available in private repo on request.
