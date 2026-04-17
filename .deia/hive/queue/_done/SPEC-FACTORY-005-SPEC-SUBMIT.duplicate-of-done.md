## Clean Retry

**Previous attempt failed with no output.**

This is a clean retry — start from scratch. Check logs if available to
understand why the previous attempt failed.

---

# SPEC-FACTORY-005: Spec Submission Form

**MODE: EXECUTE**

**Spec ID:** SPEC-FACTORY-005
**Created:** 2026-04-09
**Author:** Q88N
**Type:** PRIMITIVE
**Status:** READY
**Wave:** 2 (depends on FACTORY-006 for API)

---

## Priority
P0

## Depends On
- SPEC-FACTORY-006 (backend `/factory/spec-submit` endpoint)

## Model Assignment
sonnet

## Purpose

Create `spec-submit` primitive — a mobile-friendly form for creating and submitting specs to the factory queue. Accessible via FAB tap or `factory:open-spec-submit` bus event. Renders as slideover on mobile, modal on desktop.

**Deliverable:** New primitive (~350 lines total across files)

---

## Component Structure

```
browser/src/primitives/spec-submit/
├── SpecSubmitForm.tsx       (~250 lines)
├── specTemplates.ts         (~60 lines)
├── types.ts                 (~30 lines)
├── SpecSubmitForm.css       (~50 lines)
└── index.ts                 (~10 lines)
```

---

## Data Model

### Spec Submission

```typescript
interface SpecSubmission {
  title: string;                 // e.g., "Fix SSE reconnect bug"
  type: SpecType;                // bug, feature, refactor, research, test
  priority: 'P0' | 'P1' | 'P2';
  model: 'haiku' | 'sonnet' | 'opus';
  description: string;           // markdown body
  dependsOn: string[];           // array of spec/task IDs
  areaCode?: string;             // optional area tag
  wave?: string;                 // optional wave assignment
}

type SpecType = 'bug' | 'feature' | 'refactor' | 'research' | 'test';
```

### Templates

```typescript
interface SpecTemplate {
  id: SpecType;
  label: string;
  icon: string;
  defaultModel: 'haiku' | 'sonnet' | 'opus';
  defaultPriority: 'P0' | 'P1' | 'P2';
  descriptionPlaceholder: string;
  sections: string[];            // markdown sections to include
}
```

---

## UI Design

### Form Layout (Slideover)

```
┌─────────────────────────────────┐
│ New Spec                    [✕] │
├─────────────────────────────────┤
│                                 │
│ Type: [Bug ▼]                   │
│                                 │
│ Title:                          │
│ ┌─────────────────────────────┐ │
│ │ Fix SSE reconnect on mobile │ │
│ └─────────────────────────────┘ │
│                                 │
│ Priority: [P0] [P1] [P2]        │
│                                 │
│ Model: [Haiku] [Sonnet] [Opus]  │
│                                 │
│ Description:                    │
│ ┌─────────────────────────────┐ │
│ │ ## Problem                  │ │
│ │ SSE stream disconnects...   │ │
│ │                             │ │
│ │ ## Expected                 │ │
│ │ Auto-reconnect with backoff │ │
│ │                             │ │
│ └─────────────────────────────┘ │
│                                 │
│ Depends On: (optional)          │
│ ┌─────────────────────────────┐ │
│ │ TASK-125, SPEC-FACTORY-006  │ │
│ └─────────────────────────────┘ │
│                                 │
│ Area: [factory ▼]               │
│                                 │
├─────────────────────────────────┤
│ [Cancel]            [Submit →]  │
└─────────────────────────────────┘
```

### Type Selector

```
┌────────┬────────┬────────┬────────┬────────┐
│  🐛    │  ✨    │  🔧    │  🔬    │  🧪    │
│  Bug   │Feature │Refactor│Research│  Test  │
└────────┴────────┴────────┴────────┴────────┘
```

Selecting type:
- Pre-fills description with template sections
- Sets default model and priority
- Updates placeholder text

### Priority Toggle

```
┌────────┬────────┬────────┐
│   P0   │   P1   │   P2   │
│  red   │ yellow │  gray  │
└────────┴────────┴────────┘
```

### Model Toggle

```
┌────────┬────────┬────────┐
│ Haiku  │ Sonnet │  Opus  │
│ fast   │balance │ power  │
└────────┴────────┴────────┘
```

---

## Templates

### specTemplates.ts

```typescript
export const SPEC_TEMPLATES: Record<SpecType, SpecTemplate> = {
  bug: {
    id: 'bug',
    label: 'Bug Fix',
    icon: '🐛',
    defaultModel: 'sonnet',
    defaultPriority: 'P1',
    descriptionPlaceholder: 'Describe the bug and expected behavior...',
    sections: ['## Problem', '## Expected Behavior', '## Steps to Reproduce', '## Acceptance Criteria'],
  },
  feature: {
    id: 'feature',
    label: 'Feature',
    icon: '✨',
    defaultModel: 'sonnet',
    defaultPriority: 'P1',
    descriptionPlaceholder: 'Describe the feature and user value...',
    sections: ['## Purpose', '## User Story', '## Implementation', '## Acceptance Criteria'],
  },
  refactor: {
    id: 'refactor',
    label: 'Refactor',
    icon: '🔧',
    defaultModel: 'sonnet',
    defaultPriority: 'P2',
    descriptionPlaceholder: 'Describe what needs refactoring and why...',
    sections: ['## Current State', '## Target State', '## Approach', '## Constraints'],
  },
  research: {
    id: 'research',
    label: 'Research',
    icon: '🔬',
    defaultModel: 'sonnet',
    defaultPriority: 'P1',
    descriptionPlaceholder: 'Describe what needs to be researched...',
    sections: ['## Purpose', '## Questions', '## Survey Targets', '## Deliverable'],
  },
  test: {
    id: 'test',
    label: 'Test',
    icon: '🧪',
    defaultModel: 'haiku',
    defaultPriority: 'P2',
    descriptionPlaceholder: 'Describe what needs testing...',
    sections: ['## Scope', '## Test Cases', '## Acceptance Criteria'],
  },
};
```

---

## Generated Spec Format

On submit, generates markdown file:

```markdown
# SPEC-{TYPE}-{TIMESTAMP}: {Title}

**MODE: EXECUTE**

**Spec ID:** SPEC-{TYPE}-{TIMESTAMP}
**Created:** {date}
**Author:** Q88N
**Type:** {type}
**Status:** READY

---

## Priority
{P0|P1|P2}

## Depends On
{dependsOn or "None"}

## Model Assignment
{haiku|sonnet|opus}

## Purpose

{description}

---

## Acceptance Criteria

- [ ] (from description)

## Response File

`.deia/hive/responses/{date}-{SPEC-ID}-RESPONSE.md`

---

*{SPEC-ID} — Q88N — {date}*
```

---

## Bus Events

| Event | Direction | Payload |
|-------|-----------|---------|
| `factory:open-spec-submit` | IN | `{}` or `{ template?: SpecType }` |
| `factory:spec-submitted` | OUT | `{ specId, filename, path }` |
| `factory:spec-submit-error` | OUT | `{ error }` |

---

## API Integration

### POST /factory/spec-submit

Request:
```json
{
  "title": "Fix SSE reconnect on mobile",
  "type": "bug",
  "priority": "P1",
  "model": "sonnet",
  "description": "## Problem\n...",
  "dependsOn": ["TASK-125"],
  "areaCode": "factory"
}
```

Response:
```json
{
  "success": true,
  "specId": "SPEC-BUG-20260409-1234",
  "filename": "SPEC-BUG-20260409-1234.md",
  "path": ".deia/hive/queue/backlog/SPEC-BUG-20260409-1234.md"
}
```

---

## File Targets

| File | Action | Lines |
|------|--------|-------|
| `browser/src/primitives/spec-submit/SpecSubmitForm.tsx` | CREATE | ~250 |
| `browser/src/primitives/spec-submit/specTemplates.ts` | CREATE | ~60 |
| `browser/src/primitives/spec-submit/types.ts` | CREATE | ~30 |
| `browser/src/primitives/spec-submit/SpecSubmitForm.css` | CREATE | ~50 |
| `browser/src/primitives/spec-submit/index.ts` | CREATE | ~10 |
| `browser/src/apps/specSubmitAdapter.tsx` | CREATE | ~30 |
| `browser/src/apps/index.ts` | MODIFY | +3 |

---

## Reference Files

Read before implementation:
- `browser/src/primitives/settings-panel/` — slideover/modal pattern
- `browser/src/hooks/useSlideOver.ts` — if exists
- `hivenode/routes/build_monitor.py` — API pattern
- Existing form components in the codebase

---

## Acceptance Criteria

- [ ] Form renders as slideover on mobile, modal on desktop
- [ ] Type selector pre-fills template sections
- [ ] Priority and model toggles work
- [ ] Description supports markdown
- [ ] Depends On accepts comma-separated IDs
- [ ] Submit calls `/factory/spec-submit`
- [ ] Success shows toast and closes form
- [ ] Error shows toast with message
- [ ] Bus event `factory:spec-submitted` emitted on success
- [ ] Form accessible via FAB (`factory:open-spec-submit`)
- [ ] All CSS uses `var(--sd-*)` tokens

## Smoke Test

```bash
# Files exist
test -d browser/src/primitives/spec-submit && echo "Dir exists" || echo "MISSING"

# TypeScript compiles
cd browser && npx tsc --noEmit && echo "TS OK" || echo "TS ERRORS"

# Form submission (manual)
# Fill form, submit, verify file appears in queue/backlog/
```

## Constraints

- No file over 300 lines
- Mobile-first responsive design
- Touch-friendly inputs (min 44px targets)
- Keyboard accessible
- All CSS via `var(--sd-*)` tokens

## Response File

`.deia/hive/responses/20260409-FACTORY-005-RESPONSE.md`

---

*SPEC-FACTORY-005 — Q88N — 2026-04-09*

## Triage History
- 2026-04-12T18:52:40.076855Z — requeued (empty output)
