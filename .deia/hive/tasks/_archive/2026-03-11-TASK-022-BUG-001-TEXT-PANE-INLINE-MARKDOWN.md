# TASK-022: Fix BUG-001 — Text-Pane Inline Markdown Rendering

**Date:** 2026-03-11
**Priority:** P1
**Component:** text-pane (SDEditor)
**Assigned to:** BEE (any model)
**Your role:** BEE — Write code, run tests, report results.

---

## Problem Statement

The `renderMarkdown()` function in `SDEditor.tsx` does NOT render inline markdown formatting. It handles block-level structures (headings, lists, blockquotes, code blocks) but treats inline syntax like `**bold**`, `*italic*`, `` `code` ``, and `[link](url)` as literal text.

**Current behavior:**
User sees `**You:** hello` as raw text with asterisks.

**Expected behavior:**
- `**text**` renders as **bold**
- `*text*` renders as *italic*
- `` `code` `` renders with code background
- `[text](url)` renders as clickable link
- Mixed inline: `**You:** hello *world*` renders correctly
- Malformed markdown (unmatched `**`, etc.) renders as plain text without crashing

---

## Files to Modify

All paths are absolute:

1. **`C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\SDEditor.tsx`**
   Lines 43-134: `renderMarkdown()` function. Add inline formatting support.

2. **`C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\sd-editor.css`**
   CSS classes for rendered elements (`sde-md-*`). Add classes for bold/italic/code/link if needed.

3. **`C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\__tests__\SDEditor.test.tsx`**
   Add tests for inline markdown rendering.

---

## Constraints

1. **Do NOT replace `renderMarkdown()` with a third-party library.** It must remain a custom renderer.
2. **Fault tolerance:** Malformed markdown renders as plain text, never crashes.
3. **CSS:** `var(--sd-*)` variables only. No hex, no rgb(), no named colors.
4. **Line count:** The function is currently 90 lines. Keep it under 150 lines after changes. If needed, extract a helper function like `parseInlineFormatting(line: string): JSX.Element` to keep `renderMarkdown()` readable.
5. **Preserve existing block-level rendering:** Headings, lists, blockquotes, code block markers, empty lines must continue working as-is.

---

## Implementation Guidance

### Step 1: Create an Inline Parser Helper

Extract a new function above `renderMarkdown()`:

```typescript
/**
 * Parse inline markdown (bold, italic, code, links) into React elements
 * Malformed syntax renders as plain text
 */
function parseInlineMarkdown(text: string): (string | JSX.Element)[] {
  // Implementation:
  // 1. Scan text left-to-right
  // 2. Match patterns: **bold**, *italic*, `code`, [text](url)
  // 3. Return array of strings and JSX elements
  // 4. Handle nesting carefully (bold inside italic, etc.)
  // 5. Unmatched delimiters render as literal text
}
```

### Step 2: Update Block Renderers

In `renderMarkdown()`, replace all instances of `{text}` or `{line}` with `{parseInlineMarkdown(text)}` or `{parseInlineMarkdown(line)}`.

Example (heading renderer):

```typescript
// Before:
elements.push(
  <div key={i} className={`sde-md-heading sde-md-h${level}`}>
    {text}
  </div>
)

// After:
elements.push(
  <div key={i} className={`sde-md-heading sde-md-h${level}`}>
    {parseInlineMarkdown(text)}
  </div>
)
```

### Step 3: CSS Classes

Add to `sd-editor.css`:

```css
.sde-md-bold {
  font-weight: bold;
}

.sde-md-italic {
  font-style: italic;
}

.sde-md-code {
  background: var(--sd-code-background);
  color: var(--sd-code-foreground);
  padding: 0.1em 0.3em;
  border-radius: 3px;
  font-family: 'Courier New', monospace;
}

.sde-md-link {
  color: var(--sd-link-color);
  text-decoration: underline;
  cursor: pointer;
}
```

If these CSS variables don't exist, define them in the `:root` section of `sd-editor.css`.

### Step 4: Write Tests

Add to `SDEditor.test.tsx`:

```typescript
describe('SDEditor inline markdown rendering', () => {
  it('renders bold text', () => {
    const { container } = render(<SDEditor ... initialContent="**bold**" format="markdown" />)
    const bold = container.querySelector('.sde-md-bold')
    expect(bold).toBeInTheDocument()
    expect(bold?.textContent).toBe('bold')
  })

  it('renders italic text', () => { ... })
  it('renders inline code', () => { ... })
  it('renders links', () => { ... })
  it('renders mixed inline formatting', () => {
    // Test: "**You:** hello *world*"
    // Expect: bold "You:", plain "hello", italic "world"
  })
  it('handles malformed markdown without crashing', () => {
    // Test: "**unmatched", "**nested **bold**", etc.
  })
})
```

---

## Acceptance Criteria

Mark each as `[x]` when verified:

- [ ] `**bold**` renders bold
- [ ] `*italic*` renders italic
- [ ] `` `inline code` `` renders with code background
- [ ] `[text](url)` renders as clickable link
- [ ] Mixed inline: `**You:** hello *world*` renders correctly
- [ ] Malformed markdown (unmatched `**`, etc.) renders as plain text
- [ ] Tests cover all inline formatting cases
- [ ] All existing text-pane tests still pass (run `cd browser && npx vitest run`)
- [ ] Function `renderMarkdown()` stays under 150 lines

---

## Test Command

```bash
cd browser && npx vitest run src/primitives/text-pane/__tests__/SDEditor.test.tsx
```

---

## Reporting

When done, create:
**`C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260311-TASK-022-RESPONSE.md`**

Follow the 8-section format from `.deia/BOOT.md`:

1. Files Modified
2. What Was Done
3. Test Results
4. Build Verification
5. Acceptance Criteria
6. Clock / Cost / Carbon
7. Issues / Follow-ups
8. Commit (format: `[BEE-XXX] TASK-022: add inline markdown rendering to text-pane`)

---

## Context

- The text-pane receives content via `terminal:text-patch` bus messages with markdown like `**You:** hello` and `**claude-sonnet-4-5-20250929:** response`.
- Chat.egg.md uses a 3-pane layout: tree-browser sidebar, text-pane (center), terminal (right).
- The terminal routes user input and LLM responses to the text-pane via bus messages.
- This bug affects readability — users see raw asterisks instead of formatted text.

---

## Notes

- Do NOT modify the terminal component in this task. That's BUG-002.
- Do NOT change the bus message format. The sender already includes markdown; the text-pane just needs to render it.
- The `renderMarkdown()` function is already fault-tolerant for block-level errors (lines 123-130). Extend this pattern to inline parsing.
