# SPEC-FACTORY-003: Response Browser Primitive

**MODE: EXECUTE**

**Spec ID:** SPEC-FACTORY-003
**Created:** 2026-04-09
**Author:** Q88N
**Type:** PRIMITIVE
**Status:** READY
**Wave:** 2 (depends on FACTORY-006 for API)

---

## Priority
P0

## Depends On
- SPEC-FACTORY-006 (backend `/factory/responses` endpoint)

## Model Assignment
sonnet

## Purpose

Create `response-browser` primitive — a mobile-first interface for browsing, reading, and archiving bee response files. Users swipe through responses, tap to read full markdown, swipe to archive.

**Deliverable:** New primitive (~400 lines total across files)

---

## Component Structure

```
browser/src/primitives/response-browser/
├── ResponseBrowser.tsx      (~250 lines)
├── ResponseCard.tsx         (~80 lines)
├── responseStore.ts         (~80 lines)
├── types.ts                 (~30 lines)
├── ResponseBrowser.css      (~60 lines)
└── index.ts                 (~10 lines)
```

---

## Data Model

### Response Item (from API)

```typescript
interface ResponseItem {
  id: string;                    // filename without extension
  filename: string;              // full filename
  path: string;                  // relative path
  taskId: string;                // extracted from filename
  beeId: string;                 // BEE-XXX
  model: string;                 // sonnet, haiku, opus
  timestamp: string;             // ISO datetime
  status: 'pending' | 'reviewed' | 'archived';
  success: boolean;              // from response header
  duration: number;              // seconds
  cost: number;                  // USD
  turns: number;                 // conversation turns
  excerpt: string;               // first 200 chars of content
  sections: number;              // count of ## headers
}
```

### Store State

```typescript
interface ResponseBrowserState {
  responses: ResponseItem[];
  loading: boolean;
  error: string | null;
  filter: 'all' | 'pending' | 'reviewed' | 'archived';
  selectedId: string | null;
  selectedContent: string | null;  // full markdown when viewing
}
```

---

## UI Components

### ResponseBrowser.tsx (Main Container)

```
┌─────────────────────────────────┐
│ [Filter: All ▼] [↻ Refresh]     │
├─────────────────────────────────┤
│ ┌─────────────────────────────┐ │
│ │ TASK-127 · BEE-003 · sonnet │ │
│ │ 2m ago · $0.42 · 12 turns   │ │
│ │ "Survey complete. Found..." │ │
│ │              [✓] [📄] [🗑️]  │ │
│ └─────────────────────────────┘ │
│ ┌─────────────────────────────┐ │
│ │ TASK-126 · BEE-001 · haiku  │ │
│ │ 15m ago · $0.08 · 4 turns   │ │
│ │ "Implementation complete.." │ │
│ │              [✓] [📄] [🗑️]  │ │
│ └─────────────────────────────┘ │
│         (pull to refresh)       │
└─────────────────────────────────┘
```

Features:
- Pull-to-refresh (reuse pattern from queue-pane)
- Filter dropdown: All, Pending, Reviewed, Archived
- Tap card → expand to full markdown view
- Swipe left → archive (emit `factory:archive-response`)
- Swipe right → mark reviewed
- Auto-refresh every 30s

### ResponseCard.tsx (Individual Card)

```
┌─────────────────────────────────┐
│ TASK-127                    ✓/✗ │  ← success indicator
│ BEE-003 · sonnet · 2m ago       │
├─────────────────────────────────┤
│ $0.42 · 38 turns · 282s         │  ← cost, turns, duration
├─────────────────────────────────┤
│ "Survey complete. Found 17      │  ← excerpt
│ endpoints, 3 SSE streams..."    │
├─────────────────────────────────┤
│ [Mark Reviewed] [View] [Archive]│  ← actions (or swipe)
└─────────────────────────────────┘
```

### Full View (Modal/Slideover)

When tapping a card:
- Slideover from right (mobile) or modal (desktop)
- Renders full markdown with `markdownRenderer.tsx`
- Header: filename, metadata
- Footer: [Archive] [Create Follow-up] [Close]

---

## Store Implementation

### responseStore.ts (Zustand)

```typescript
import { create } from 'zustand';
import type { ResponseItem, ResponseBrowserState } from './types';

export const useResponseStore = create<ResponseBrowserState>((set, get) => ({
  responses: [],
  loading: false,
  error: null,
  filter: 'all',
  selectedId: null,
  selectedContent: null,

  fetchResponses: async () => {
    set({ loading: true, error: null });
    try {
      const res = await fetch('/factory/responses');
      const data = await res.json();
      set({ responses: data.responses, loading: false });
    } catch (err) {
      set({ error: err.message, loading: false });
    }
  },

  archiveResponse: async (id: string) => {
    await fetch('/factory/archive', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ responseId: id }),
    });
    // Optimistic update
    set((state) => ({
      responses: state.responses.map((r) =>
        r.id === id ? { ...r, status: 'archived' } : r
      ),
    }));
    // Emit bus event
    window.messageBus?.publish('factory:response-archived', { id });
  },

  selectResponse: async (id: string) => {
    set({ selectedId: id, selectedContent: null });
    const res = await fetch(`/factory/responses/${id}/content`);
    const data = await res.json();
    set({ selectedContent: data.content });
  },

  clearSelection: () => set({ selectedId: null, selectedContent: null }),

  setFilter: (filter) => set({ filter }),
}));
```

---

## Bus Events

| Event | Direction | Payload |
|-------|-----------|---------|
| `factory:response-archived` | OUT | `{ id: string }` |
| `factory:response-reviewed` | OUT | `{ id: string }` |
| `factory:create-followup` | OUT | `{ responseId: string, taskId: string }` |
| `factory:responses-refresh` | IN | `{}` — triggers refetch |

---

## File Targets

| File | Action | Lines |
|------|--------|-------|
| `browser/src/primitives/response-browser/ResponseBrowser.tsx` | CREATE | ~250 |
| `browser/src/primitives/response-browser/ResponseCard.tsx` | CREATE | ~80 |
| `browser/src/primitives/response-browser/responseStore.ts` | CREATE | ~80 |
| `browser/src/primitives/response-browser/types.ts` | CREATE | ~30 |
| `browser/src/primitives/response-browser/ResponseBrowser.css` | CREATE | ~60 |
| `browser/src/primitives/response-browser/index.ts` | CREATE | ~10 |
| `browser/src/apps/responseBrowserAdapter.tsx` | CREATE | ~30 |
| `browser/src/apps/index.ts` | MODIFY | +3 |

---

## Reference Files

Read before implementation:
- `browser/src/primitives/queue-pane/QueuePane.tsx` — pattern for list + pull-to-refresh
- `browser/src/primitives/queue-pane/queueStore.ts` — Zustand store pattern
- `browser/src/primitives/text-pane/markdownRenderer.tsx` — markdown rendering
- `browser/src/hooks/useSwipeNotification.ts` — swipe gesture pattern
- `browser/src/apps/progressAdapter.tsx` — adapter pattern

---

## Acceptance Criteria

- [ ] `ResponseBrowser.tsx` renders list of response cards
- [ ] Pull-to-refresh fetches from `/factory/responses`
- [ ] Filter dropdown filters by status
- [ ] Tap card opens full markdown view
- [ ] Swipe left archives response
- [ ] Swipe right marks reviewed
- [ ] Bus events emitted on actions
- [ ] Auto-refresh every 30s
- [ ] Registered in app registry as `response-browser`
- [ ] Mobile responsive (cards stack, touch-friendly)
- [ ] All CSS uses `var(--sd-*)` tokens

## Smoke Test

```bash
# Files exist
test -d browser/src/primitives/response-browser && echo "Dir exists" || echo "MISSING"

# TypeScript compiles
cd browser && npx tsc --noEmit && echo "TS OK" || echo "TS ERRORS"

# Component renders (manual)
# Add to test EGG: nodeType: response-browser
# Verify list renders with mock data
```

## Constraints

- No file over 300 lines
- Reuse existing hooks and patterns
- All CSS via `var(--sd-*)` tokens
- Mobile-first design
- No external dependencies beyond what's already installed

## Response File

`.deia/hive/responses/20260409-FACTORY-003-RESPONSE.md`

---

*SPEC-FACTORY-003 — Q88N — 2026-04-09*
