# TASK-022: Inline Markdown Rendering in Text-Pane

**Assigned to:** BEE-SONNET
**Priority:** P1
**Created:** 2026-03-11
**Dependencies:** None

---

## Objective

Fix BUG-001: SDEditor's `renderMarkdown()` function currently renders only block-level elements (headings, lists, paragraphs, etc.) but outputs raw text inside them. This means inline formatting like `**bold**`, `*italic*`, `` `code` ``, and `[link](url)` render with literal markup visible instead of as formatted elements.

Add inline markdown parsing and extract the renderer to a separate module to bring SDEditor.tsx back under the 500-line limit.

---

## Context

The text-pane primitive (SDEditor) receives AI responses via `terminal:text-patch` bus messages with `format: 'markdown'`. The current `renderMarkdown()` function (lines 43-134 in SDEditor.tsx) correctly identifies block elements but does not parse inline formatting within those blocks.

Example broken output:
```
**You:** Hello
**claude-sonnet-4-5:** Here is my answer
```

The `**` asterisks are visible. They should render as `<strong>You:</strong> Hello`.

---

## Requirements

### 1. Inline Formatting Support

Implement parsing for these inline elements:

- **Bold**: `**text**` or `__text__` → `<strong>text</strong>`
- **Italic**: `*text*` or `_text_` → `<em>text</em>`
- **Inline code**: `` `code` `` → `<code>code</code>`
- **Links**: `[text](url)` → `<a href="url">text</a>`

### 2. Rendering Behavior

- Inline elements must render **within** block-level elements
- Multiple inline formats can stack: `**bold *italic* bold**` should work
- Escaped characters `\*`, `\[`, `\` ` should render as literal characters
- Malformed inline syntax (e.g., unclosed `**bold`) should render as-is, no error quarantine

### 3. Module Extraction

SDEditor.tsx is currently **564 lines** (over the 500-line limit). Extract the markdown rendering logic to a new module:

**New file:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\services\markdownRenderer.tsx`

This module should export:
- `renderMarkdown(content: string): JSX.Element[]` — the current function, moved
- `parseInline(text: string): JSX.Element | JSX.Element[]` — new inline parser

SDEditor.tsx imports and uses `renderMarkdown()` from the new module. After extraction, SDEditor.tsx should be under 500 lines.

### 4. CSS Classes

Add CSS classes for inline elements in `sd-editor.css`:

- `.sde-md-bold` — bold text
- `.sde-md-italic` — italic text
- `.sde-md-code` — inline code
- `.sde-md-link` — links

All classes **must** use `var(--sd-*)` variables only. No hardcoded colors.

Example CSS:
```css
.sde-md-bold {
  font-weight: 600;
  color: var(--sd-text-primary);
}

.sde-md-italic {
  font-style: italic;
  color: var(--sd-text-primary);
}

.sde-md-code {
  font-family: var(--sd-font-mono);
  font-size: var(--sd-font-sm);
  background: var(--sd-surface-alt);
  color: var(--sd-purple);
  padding: 2px 4px;
  border-radius: 3px;
}

.sde-md-link {
  color: var(--sd-purple);
  text-decoration: underline;
  cursor: pointer;
}

.sde-md-link:hover {
  color: var(--sd-purple-bright);
}
```

---

## Files to Modify

| File | Action | Line Count Constraint |
|------|--------|----------------------|
| `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\services\markdownRenderer.tsx` | **CREATE** | Must be under 500 lines |
| `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\SDEditor.tsx` | **EDIT** | Must be under 500 lines after extraction |
| `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\sd-editor.css` | **EDIT** | Add inline element classes |
| `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\__tests__\SDEditor.test.tsx` | **EDIT** | Add inline rendering tests |

Optional (if separate test file needed):
| `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\services\__tests__\markdownRenderer.test.tsx` | **CREATE** | Tests for inline parser |

---

## Test Requirements (TDD — Write Tests First)

### Test Coverage

Add tests in `SDEditor.test.tsx` (or new `markdownRenderer.test.tsx`):

1. **Bold rendering**:
   - `**bold**` renders `<strong>`
   - `__bold__` renders `<strong>`
   - Nested: `**bold *italic* bold**`

2. **Italic rendering**:
   - `*italic*` renders `<em>`
   - `_italic_` renders `<em>`

3. **Inline code rendering**:
   - `` `code` `` renders `<code>`
   - Multiple: `` `foo` and `bar` ``

4. **Link rendering**:
   - `[text](url)` renders `<a href="url">`
   - Link with bold: `[**bold link**](url)`

5. **Mixed inline formats**:
   - `**You:** Hello` → `<strong>You:</strong> Hello`
   - `` `code` with **bold** and *italic* ``

6. **Edge cases**:
   - Unclosed `**bold` → renders as-is
   - Escaped `\*` → renders literal `*`
   - Empty link `[](url)` → renders as-is or empty link

7. **Block + inline integration**:
   - Heading with inline: `# **Bold Heading**`
   - List item with inline: `- **Item** with *italic*`
   - Paragraph with inline: `This is **bold** text`

### Existing Tests

All existing SDEditor tests must continue to pass:
- Banner/input/response rendering
- Bus message handling
- Co-Author mode
- Word count
- Markdown/raw mode toggle

---

## Implementation Notes

### Inline Parser Algorithm

1. Walk the text string character by character
2. Detect inline marker start (`**`, `*`, `` ` ``, `[`)
3. Find matching end marker
4. If valid, create JSX element with CSS class
5. Recursively parse content inside (for nested formats)
6. Return array of JSX elements and text nodes

Example structure:
```typescript
function parseInline(text: string): (JSX.Element | string)[] {
  const elements: (JSX.Element | string)[] = [];
  let i = 0;

  while (i < text.length) {
    // Detect **bold**
    if (text[i] === '*' && text[i+1] === '*') {
      const end = text.indexOf('**', i + 2);
      if (end !== -1) {
        const content = text.slice(i + 2, end);
        elements.push(<strong className="sde-md-bold" key={i}>{parseInline(content)}</strong>);
        i = end + 2;
        continue;
      }
    }

    // Similar for *italic*, `code`, [link](url)
    // ...

    // Plain text
    elements.push(text[i]);
    i++;
  }

  return elements;
}
```

### Integration with Block Renderer

Modify each block element to pass its text content through `parseInline()`:

**Before:**
```typescript
elements.push(
  <div key={i} className="sde-md-paragraph">
    {line}
  </div>
)
```

**After:**
```typescript
elements.push(
  <div key={i} className="sde-md-paragraph">
    {parseInline(line)}
  </div>
)
```

Apply this to: paragraphs, headings, list items, blockquotes.

**Exception:** Code block markers (` ```json `) should NOT parse inline formatting — render raw text.

---

## Constraints (Hard Rules)

1. **CSS variables only**: No `#hex`, no `rgb()`, no named colors. All colors via `var(--sd-*)`.
2. **File size limit**: No file over 500 lines. After extraction, SDEditor.tsx must be under 500 lines.
3. **TDD**: Write tests first, then implementation.
4. **No stubs**: Every function fully implemented. No `// TODO`, no placeholder returns.
5. **No third-party libraries**: Extend the existing hand-rolled markdown renderer. Do not install or import external markdown libraries.

---

## Verification Checklist

After implementation, verify:

- [ ] All inline formats render correctly (bold, italic, code, links)
- [ ] Nested inline formats work (e.g., `**bold *italic* bold**`)
- [ ] Block elements correctly contain inline elements
- [ ] SDEditor.tsx is under 500 lines
- [ ] markdownRenderer.tsx is under 500 lines
- [ ] All new CSS classes use `var(--sd-*)` only
- [ ] All existing SDEditor tests pass
- [ ] New inline rendering tests pass (at least 10 new test cases)
- [ ] No console errors or warnings in test output

---

## Definition of Done

1. `markdownRenderer.tsx` module created and exported
2. SDEditor.tsx imports and uses the extracted module
3. SDEditor.tsx is under 500 lines
4. Inline markdown rendering works for bold, italic, code, links
5. All new CSS classes use CSS variables only
6. All tests pass (existing + new)
7. No stubs, no TODOs, no placeholder code
8. Feature tested manually in Chat EGG — `**You:** Hello` renders with bold `You:`

---

## Q&A

**Q: Should we use a regex-based parser or character-by-character?**
A: Either is acceptable. Regex is faster but harder to debug. Character-by-character is easier to test and extend. Choose based on complexity comfort.

**Q: What if the inline parser gets recursive (nested formats)?**
A: Yes, support recursion for nested formats. Example: `**bold *italic* bold**` should work. Depth limit of 5 is acceptable to prevent stack overflow.

**Q: Should links open in a new tab?**
A: Yes, add `target="_blank" rel="noopener noreferrer"` to `<a>` elements.

**Q: What about edge cases like `**bold *italic**` (mismatched nesting)?**
A: Graceful degradation: render what's valid, leave the rest as-is. No error quarantine needed for inline syntax.

---

**END OF TASK-022 SPEC**
