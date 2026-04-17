# TASK-010: SDEditor — Text Pane Primitive (P-01)

## Objective

Port SDEditor (text/markdown editor with Co-Author AI rewriting) from `simdecisions-2/src/components/SDEditor/` to `browser/src/primitives/text-pane/`. This is primitive P-01 — the foundational text editing surface. Also port the textPane services (`textOps`, `unifiedDiff`, `languagePack`) which SDEditor depends on. Co-Author rewrites route through the bus to the LLM router instead of importing providers directly.

## Dependencies

- **TASK-005 (Relay Bus)** — SDEditor subscribes to bus events (`frank:text-patch`, targeting). Co-Author sends prompts via bus message to LLM router.
- **Independent of TASK-008/009** — SDEditor is a leaf component. It does not depend on the shell reducer or shell renderer.

## Source Files

Port from `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\`:

### SDEditor Components

| Source Path | Dest Path | Lines | What It Does |
|-------------|-----------|-------|-------------|
| `components/SDEditor/SDEditor.tsx` | `primitives/text-pane/SDEditor.tsx` | 576 | Full text editor: rendered/raw toggle, markdown renderer, Co-Author mode, bus subscription, undo/redo, keyboard shortcuts |
| `components/SDEditor/CoAuthorOverlay.tsx` | `primitives/text-pane/CoAuthorOverlay.tsx` | 81 | Inline diff display for AI rewrites: original vs rewrite, Tab=accept, Esc=reject |
| `components/SDEditor/sd-editor.css` | `primitives/text-pane/sd-editor.css` | 325 | All `var(--sd-*)` custom properties. Covers root, header, toolbar, textarea, rendered markdown, co-author overlay |

### textPane Services (dependencies)

| Source Path | Dest Path | Lines | What It Does |
|-------------|-----------|-------|-------------|
| `services/textPane/textOps.ts` | `primitives/text-pane/services/textOps.ts` | 204 | Text operations: `applyTextOps()` for insert, delete, replace, format operations |
| `services/textPane/unifiedDiff.ts` | `primitives/text-pane/services/unifiedDiff.ts` | 268 | Unified diff parsing and application: `applyUnifiedDiff()`, `parseUnifiedDiff()` |
| `services/textPane/languagePack.ts` | `primitives/text-pane/services/languagePack.ts` | 21 | Language pack registry for syntax highlighting/rendering |

### Existing Tests (port these)

| Source Path | Dest Path | Lines |
|-------------|-----------|-------|
| `services/textPane/__tests__/textOps.test.ts` | `primitives/text-pane/__tests__/textOps.test.ts` | 144 |
| `services/textPane/__tests__/unifiedDiff.test.ts` | `primitives/text-pane/__tests__/unifiedDiff.test.ts` | 295 |
| `components/SDEditor/__tests__/SDEditor.test.tsx` | `primitives/text-pane/__tests__/SDEditor.test.tsx` | 511 |
| `components/SDEditor/__tests__/CoAuthor.test.tsx` | `primitives/text-pane/__tests__/CoAuthorOverlay.test.tsx` | 252 |

## Port Rules

### 1. Route Co-Author Through Bus → LLM Router

The old SDEditor imports LLM providers directly:
```typescript
// OLD — don't do this
import { AnthropicProvider } from '../services/llm/AnthropicProvider';
import { GroqProvider } from '../services/llm/GroqProvider';
```

Replace with bus-based routing:
```typescript
// NEW — route through bus
import { useBus } from '../infrastructure/relay_bus';  // or correct TASK-005 path

// In Co-Author handler:
const handleCoAuthorRewrite = async (selectedText: string, instruction: string) => {
  setCoAuthorLoading(true);
  try {
    const response = await bus.request('llm:rewrite', {
      prompt: instruction,
      text: selectedText,
      system: 'You are a writing assistant. Rewrite the provided text according to the instruction.',
    });
    setCoAuthorRewrite(response.text);
  } catch (err) {
    console.error('Co-Author rewrite failed:', err);
    setCoAuthorRewrite(null);
  } finally {
    setCoAuthorLoading(false);
  }
};
```

The bus `llm:rewrite` message type will be handled by whatever LLM integration layer connects the browser bus to the backend LLM router. For now, the SDEditor just sends the message — if nobody handles it, Co-Author gracefully fails.

### 2. Abstract Shell Hook Dependencies

SDEditor imports shell-specific hooks:
```typescript
// OLD
import { usePaneContext } from '../shell/PaneContext';
import { useApplet } from '../shell/AppletShell';
```

These don't exist yet (TASK-008/009). Create minimal interface types:

```typescript
// browser/src/primitives/text-pane/types.ts

/** Pane context provided by the shell. */
export interface PaneContext {
  nodeId: string;
  paneId: string;
  isFocused: boolean;
  label?: string;
}

/** Applet interface for undo/redo and state management. */
export interface AppletHandle {
  undoLedger: {
    push(state: unknown): void;
    undo(): unknown | null;
    redo(): unknown | null;
    canUndo: boolean;
    canRedo: boolean;
  };
  setTitle(title: string): void;
  getState(): Record<string, unknown>;
  setState(state: Record<string, unknown>): void;
}
```

SDEditor accepts these as props instead of calling hooks:
```typescript
interface SDEditorProps {
  paneContext: PaneContext;
  applet?: AppletHandle;
  initialContent?: string;
  readOnly?: boolean;
  onContentChange?: (content: string) => void;
}
```

When the shell renders SDEditor (TASK-009), it passes the context from hooks. For standalone/test use, SDEditor works without shell context.

### 3. Fix Hardcoded Color in CSS

`sd-editor.css` has one hardcoded color:
```css
/* OLD */
box-shadow: 0 2px 8px rgba(0,0,0,0.3);
```

Replace with:
```css
/* NEW */
box-shadow: 0 2px 8px var(--sd-shadow-medium, rgba(0,0,0,0.3));
```

Use fallback value so it works even if the custom property isn't defined yet.

### 4. Port textOps and unifiedDiff Exactly

These are pure utility modules with no external dependencies. Port them exactly — they're well-tested (144 + 295 lines of tests).

### 5. Port languagePack as Skeleton

`languagePack.ts` is 21 lines — a registry pattern. Port exactly. Future tasks add actual language packs.

### 6. Preserve Class Prefix

All CSS classes use the `sde-` prefix. Keep this convention.

### 7. Markdown Rendering

SDEditor has a "rendered" mode that displays markdown as HTML. The old implementation uses a custom `renderMarkdown()` function. Port the rendering logic, but use a lightweight approach:
- If a markdown library is already in `browser/package.json`, use it
- If not, implement a basic markdown-to-HTML renderer (headers, bold, italic, code blocks, links, lists) — enough for the editor preview
- Do NOT add a heavy dependency like `marked` or `remark` unless it's already present

### 8. calculateMetrics

SDEditor imports `calculateMetrics` for word/char counts. Port as a local utility in `primitives/text-pane/services/metrics.ts`:

```typescript
export function calculateMetrics(text: string): {
  characters: number;
  words: number;
  lines: number;
  paragraphs: number;
} {
  return {
    characters: text.length,
    words: text.trim() ? text.trim().split(/\s+/).length : 0,
    lines: text.split('\n').length,
    paragraphs: text.split(/\n\s*\n/).filter(p => p.trim()).length,
  };
}
```

## File Structure

```
browser/src/primitives/text-pane/
├── index.ts                  -- Public exports
├── types.ts                  -- PaneContext, AppletHandle, SDEditorProps interfaces
├── SDEditor.tsx              -- Main editor component
├── CoAuthorOverlay.tsx        -- AI rewrite diff overlay
├── sd-editor.css             -- Styles (all var(--sd-*))
└── services/
    ├── textOps.ts            -- Text operations
    ├── unifiedDiff.ts        -- Unified diff parsing/application
    ├── languagePack.ts       -- Language pack registry
    └── metrics.ts            -- Word/char/line counts
```

```
browser/src/primitives/text-pane/__tests__/
├── SDEditor.test.tsx
├── CoAuthorOverlay.test.tsx
├── textOps.test.ts
├── unifiedDiff.test.ts
├── metrics.test.ts
└── types.test.ts
```

## Test Requirements

### Port Existing Tests

Port these test files, fixing imports:
- `SDEditor.test.tsx` (511 lines) — Mock shell hooks with prop-based interface instead
- `CoAuthor.test.tsx` (252 lines) → `CoAuthorOverlay.test.tsx` — Mock bus for LLM requests
- `textOps.test.ts` (144 lines) — Pure function tests, minimal changes
- `unifiedDiff.test.ts` (295 lines) — Pure function tests, minimal changes

### New Tests

#### metrics.test.ts
- [ ] Empty string returns zero for all metrics
- [ ] Single word: characters, words=1, lines=1, paragraphs=1
- [ ] Multi-word single line
- [ ] Multi-line text
- [ ] Multi-paragraph text (separated by blank lines)
- [ ] Whitespace-only text

#### types.test.ts
- [ ] PaneContext has required fields
- [ ] AppletHandle undoLedger interface
- [ ] SDEditorProps with optional fields

#### CoAuthorOverlay.test.tsx (new tests beyond ported)
- [ ] Shows loading state
- [ ] Tab key accepts rewrite
- [ ] Esc key rejects rewrite
- [ ] Diff display: removed lines styled
- [ ] Diff display: added lines styled

**Minimum: 55+ tests (ported + new).**

## Source Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\SDEditor\SDEditor.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\SDEditor\CoAuthorOverlay.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\SDEditor\sd-editor.css`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\services\textPane\textOps.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\services\textPane\unifiedDiff.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\services\textPane\languagePack.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\services\textPane\__tests__\textOps.test.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\services\textPane\__tests__\unifiedDiff.test.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\SDEditor\__tests__\SDEditor.test.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\SDEditor\__tests__\CoAuthor.test.tsx`

Also check TASK-005 output for:
- `RelayBus` import path and `bus.request()` or `bus.emit()` API
- Any existing bus message type definitions

## What NOT to Build

- No shell reducer integration (TASK-008)
- No shell renderer / AppletShell (TASK-009)
- No actual LLM provider implementations (backend handles that via LLM router)
- No frank service integration (replaced by bus messages)
- No useSettings hook (use props or local defaults)
- No pane chrome / tab bar (TASK-009)
- No drag-drop (TASK-008)
- No heavy markdown library — keep it lightweight

## Constraints

- TypeScript strict mode
- React 18+
- Vite
- All files under 500 lines (SDEditor.tsx was 576 — with shell deps abstracted to props, should be under 500)
- No stubs — every function fully implemented
- All CSS uses `var(--sd-*)` — no hex, no rgb, no named colors (fix the one rgba box-shadow)
- Class prefix: `sde-`
- Test with vitest + @testing-library/react
- SDEditor must work standalone (without shell context) for testing and future embedding

## Deliverables

### Source Files
- [ ] `browser/src/primitives/text-pane/index.ts`
- [ ] `browser/src/primitives/text-pane/types.ts`
- [ ] `browser/src/primitives/text-pane/SDEditor.tsx`
- [ ] `browser/src/primitives/text-pane/CoAuthorOverlay.tsx`
- [ ] `browser/src/primitives/text-pane/sd-editor.css`
- [ ] `browser/src/primitives/text-pane/services/textOps.ts`
- [ ] `browser/src/primitives/text-pane/services/unifiedDiff.ts`
- [ ] `browser/src/primitives/text-pane/services/languagePack.ts`
- [ ] `browser/src/primitives/text-pane/services/metrics.ts`

### Test Files
- [ ] `browser/src/primitives/text-pane/__tests__/SDEditor.test.tsx`
- [ ] `browser/src/primitives/text-pane/__tests__/CoAuthorOverlay.test.tsx`
- [ ] `browser/src/primitives/text-pane/__tests__/textOps.test.ts`
- [ ] `browser/src/primitives/text-pane/__tests__/unifiedDiff.test.ts`
- [ ] `browser/src/primitives/text-pane/__tests__/metrics.test.ts`
- [ ] `browser/src/primitives/text-pane/__tests__/types.test.ts`

**15 deliverables total (9 source + 6 test).**

## Response Requirements -- MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/YYYYMMDD-TASK-010-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** -- task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** -- every file created/modified/deleted, full paths
3. **What Was Done** -- bullet list of concrete changes
4. **Test Results** -- test files run, pass/fail counts
5. **Build Verification** -- vitest output summary
6. **Acceptance Criteria** -- copy deliverables above, mark [x] or [ ]
7. **Clock / Cost / Carbon** -- all three, never omit any
8. **Issues / Follow-ups** -- edge cases, dependencies, recommended next tasks

DO NOT skip any section. A response without all 8 sections is incomplete.
