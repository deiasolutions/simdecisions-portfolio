# SPEC-FACTORY-104: Diff Viewer Slideover

**MODE: EXECUTE**

**Spec ID:** SPEC-FACTORY-104
**Created:** 2026-04-09
**Author:** Q88N
**Type:** FEATURE
**Status:** READY
**Phase:** P1

---

## Priority
P1

## Depends On
- SPEC-FACTORY-004 (approval-cards)

## Reference
- `browser/src/primitives/diff-viewer/DiffViewer.tsx` — existing diff-viewer primitive

## Model Assignment
haiku

## Purpose

When reviewing an approval card that has an associated diff, allow tapping [View Diff] to open the diff-viewer in a slideover. This provides full context for REQUIRE_HUMAN gate decisions without leaving the approval flow.

**Deliverable:** Diff viewer integration (~60 lines)

---

## Current State

Per telemetry survey:
- `browser/src/primitives/diff-viewer/DiffViewer.tsx` (744 lines, complete)
- Supports swipe approve/reject
- Already works as standalone component
- Approval cards have optional `diff` field

Need:
- Slideover wrapper for diff-viewer
- Wire [View Diff] button in approval cards
- Pass diff content to viewer

---

## User Flow

```
1. View approval card for DEPLOY action
2. Card shows "47 files changed, +1,200 -340"
3. Tap [View Diff]
4. Slideover opens from right
5. Full diff-viewer renders with:
   - File tree on left (collapsible on mobile)
   - Diff content on right
   - Swipe or button to approve/reject
6. Approving in diff-viewer closes slideover
7. Card removed from approval stack
```

---

## Implementation

### 1. Create Slideover Wrapper

```tsx
// browser/src/components/DiffSlideover.tsx

import { DiffViewer } from '../primitives/diff-viewer/DiffViewer';
import { X } from 'lucide-react';

interface DiffSlideoverProps {
  isOpen: boolean;
  onClose: () => void;
  diff: string;
  gateId: string;
  onApprove: (gateId: string) => void;
  onReject: (gateId: string) => void;
}

export function DiffSlideover({ 
  isOpen, 
  onClose, 
  diff, 
  gateId,
  onApprove,
  onReject 
}: DiffSlideoverProps) {
  if (!isOpen) return null;
  
  const handleApprove = () => {
    onApprove(gateId);
    onClose();
  };
  
  const handleReject = () => {
    onReject(gateId);
    onClose();
  };
  
  return (
    <div className="hhp-slideover-overlay" onClick={onClose}>
      <div 
        className="hhp-slideover hhp-slideover-right"
        onClick={(e) => e.stopPropagation()}
      >
        <header className="hhp-slideover-header">
          <h2>Review Changes</h2>
          <button onClick={onClose} aria-label="Close">
            <X size={20} />
          </button>
        </header>
        
        <div className="hhp-slideover-content">
          <DiffViewer 
            diff={diff}
            onApprove={handleApprove}
            onReject={handleReject}
            showActions={true}
          />
        </div>
      </div>
    </div>
  );
}
```

### 2. Wire to Approval Cards

In `ApprovalCard.tsx`:

```tsx
const [showDiff, setShowDiff] = useState(false);

// In render
{approval.diff && (
  <button 
    className="hhp-btn hhp-btn-secondary"
    onClick={() => setShowDiff(true)}
  >
    View Diff
  </button>
)}

<DiffSlideover
  isOpen={showDiff}
  onClose={() => setShowDiff(false)}
  diff={approval.diff}
  gateId={approval.id}
  onApprove={handleApprove}
  onReject={handleReject}
/>
```

### 3. CSS for Slideover

```css
/* browser/src/components/DiffSlideover.css */

.hhp-slideover-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: var(--sd-z-modal);
}

.hhp-slideover {
  position: fixed;
  top: 0;
  bottom: 0;
  width: 90vw;
  max-width: 800px;
  background: var(--sd-bg-primary);
  display: flex;
  flex-direction: column;
  animation: slideIn 0.2s ease-out;
}

.hhp-slideover-right {
  right: 0;
}

@keyframes slideIn {
  from { transform: translateX(100%); }
  to { transform: translateX(0); }
}

.hhp-slideover-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--sd-space-3);
  border-bottom: 1px solid var(--sd-border);
}

.hhp-slideover-content {
  flex: 1;
  overflow: auto;
}

/* Mobile: full width */
@media (max-width: 768px) {
  .hhp-slideover {
    width: 100vw;
    max-width: none;
  }
}
```

---

## File Targets

| File | Action | Lines |
|------|--------|-------|
| `browser/src/components/DiffSlideover.tsx` | CREATE | ~50 |
| `browser/src/components/DiffSlideover.css` | CREATE | ~40 |
| `browser/src/primitives/approval-cards/ApprovalCard.tsx` | MODIFY | +15 |

---

## Reference Files

Read before implementation:
- `browser/src/primitives/diff-viewer/DiffViewer.tsx`
- `browser/src/primitives/approval-cards/ApprovalCard.tsx`
- Existing slideover/modal patterns in codebase

---

## Acceptance Criteria

- [ ] [View Diff] button appears when approval has diff
- [ ] Clicking opens slideover from right
- [ ] Diff-viewer renders in slideover
- [ ] Approve in diff-viewer resolves gate and closes
- [ ] Reject in diff-viewer resolves gate and closes
- [ ] Tapping overlay closes slideover
- [ ] Full width on mobile
- [ ] Keyboard escape closes slideover

## Smoke Test

```bash
# Files exist
test -f browser/src/components/DiffSlideover.tsx && echo "Exists" || echo "MISSING"

# Manual test:
# 1. Create mock approval with diff field
# 2. Tap [View Diff]
# 3. Verify slideover opens with diff content
# 4. Swipe approve in diff-viewer
# 5. Verify slideover closes and approval removed
```

## Constraints

- Reuse existing diff-viewer component
- Slideover pattern reusable for other contexts
- All CSS via `var(--sd-*)` tokens
- Accessible (focus trap, escape key)

## Response File

`.deia/hive/responses/20260409-FACTORY-104-RESPONSE.md`

---

*SPEC-FACTORY-104 — Q88N — 2026-04-09*
