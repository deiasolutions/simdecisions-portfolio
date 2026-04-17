# Conversation Pane Output Components

This document describes the output surface components added to conversation-pane for MW-010.

## Components

### CodeBlock

Syntax-highlighted code block with copy functionality.

**Features:**
- Syntax highlighting using highlight.js (JavaScript, Python, TypeScript)
- Copy to clipboard button
- Language badge display
- Mobile-optimized with horizontal scroll
- Touch-friendly copy button (min-height 44px)

**Usage:**
```tsx
import { CodeBlock } from './primitives/conversation-pane'

<CodeBlock
  code="const x = 42;\nconsole.log(x);"
  language="javascript"
/>
```

**Props:**
- `code: string` — The code to display
- `language: string` — Programming language (javascript, python, typescript, etc.)
- `className?: string` — Optional CSS class

**CSS Variables:**
- `--sd-code-bg` — Background color
- `--sd-border` — Border color
- `--sd-text-primary` — Text color
- `--sd-syntax-*` — Syntax highlighting colors

---

### ImageOutput

Image component with inline rendering and lightbox for full-size view.

**Features:**
- Inline image display
- Lightbox opens on tap/click
- Loading placeholder with spinner
- Error state with fallback UI
- Mobile-optimized lightbox (fullscreen)
- Touch-friendly close button

**Usage:**
```tsx
import { ImageOutput } from './primitives/conversation-pane'

<ImageOutput
  src="https://example.com/image.png"
  alt="Description of image"
/>
```

**Props:**
- `src: string` — Image URL
- `alt?: string` — Alt text (default: empty string)
- `className?: string` — Optional CSS class

**Interactions:**
- Click/tap image → opens lightbox
- Click close button → closes lightbox
- Click backdrop → closes lightbox
- Click image in lightbox → no action (prevents accidental close)

---

### FileAttachment

File attachment display with download functionality.

**Features:**
- File icon based on type (PDF, image, code, document, archive)
- Filename display with truncation
- File size formatting (B, KB, MB)
- Download button
- Mobile-optimized layout
- Touch-friendly download button (min-height 44px)

**Usage:**
```tsx
import { FileAttachment } from './primitives/conversation-pane'

<FileAttachment
  filename="report.pdf"
  url="https://example.com/report.pdf"
  size={2097152}
  onDownload={(url, filename) => console.log('Downloading:', filename)}
/>
```

**Props:**
- `filename: string` — File name
- `url: string` — Download URL
- `size: number` — File size in bytes
- `onDownload?: (url: string, filename: string) => void` — Optional download callback
- `className?: string` — Optional CSS class

**File Types:**
- PDF files → 📄 icon
- Images → 🖼 icon
- Code files → ⌨ icon
- Documents → 📝 icon
- Archives → 📦 icon
- Generic → 📁 icon

---

### ActionButton

Action button for command results and user interactions.

**Features:**
- Multiple variants (default, primary, secondary, danger)
- Status indicators (success ✓, error ✕)
- Loading state with spinner
- Disabled state
- Optional icon support
- Mobile-optimized (min-height 44px)

**Usage:**
```tsx
import { ActionButton } from './primitives/conversation-pane'

// Primary action
<ActionButton
  label="Open file"
  onClick={() => console.log('Opening file')}
  variant="primary"
/>

// Success status
<ActionButton
  label="Command succeeded"
  onClick={() => console.log('View details')}
  status="success"
/>

// Error status
<ActionButton
  label="Command failed"
  onClick={() => console.log('Retry')}
  status="error"
/>

// Loading state
<ActionButton
  label="Processing"
  onClick={() => {}}
  loading
/>
```

**Props:**
- `label: string` — Button text
- `onClick: () => void` — Click handler
- `variant?: 'default' | 'primary' | 'secondary' | 'danger'` — Visual variant
- `status?: 'success' | 'error'` — Status indicator
- `icon?: string` — Optional icon (text/emoji)
- `disabled?: boolean` — Disabled state
- `loading?: boolean` — Loading state with spinner
- `ariaLabel?: string` — Custom aria-label (defaults to label)
- `className?: string` — Optional CSS class

---

## CSS Variables

All components use CSS variables exclusively (no hardcoded colors). Required variables:

```css
:root {
  /* Surface colors */
  --sd-surface: #ffffff;
  --sd-surface-hover: #f5f5f5;
  --sd-surface-active: #ebebeb;
  --sd-code-bg: #f8f8f8;

  /* Border and text */
  --sd-border: #e0e0e0;
  --sd-text-primary: #1a1a1a;
  --sd-text-secondary: #666666;
  --sd-text-muted: #999999;
  --sd-text-on-primary: #ffffff;

  /* Primary colors */
  --sd-primary: #0066cc;
  --sd-primary-hover: #0052a3;
  --sd-primary-active: #003d7a;

  /* Status colors */
  --sd-error: #d32f2f;
  --sd-error-bg: #ffebee;
  --sd-success: #2e7d32;
  --sd-success-bg: #e8f5e9;

  /* Overlay */
  --sd-overlay-bg: rgba(0, 0, 0, 0.5);
  --sd-shadow: rgba(0, 0, 0, 0.2);

  /* Fonts */
  --sd-font-sans: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  --sd-font-mono: 'Consolas', 'Monaco', 'Courier New', monospace;
  --sd-font-xs: 12px;
  --sd-font-sm: 14px;
  --sd-font-md: 16px;
  --sd-font-lg: 18px;
  --sd-font-xl: 24px;

  /* Syntax highlighting */
  --sd-syntax-keyword: #d73a49;
  --sd-syntax-string: #032f62;
  --sd-syntax-number: #005cc5;
  --sd-syntax-comment: #6a737d;
  --sd-syntax-function: #6f42c1;
  --sd-syntax-variable: #e36209;
}
```

---

## Tests

All components have comprehensive unit tests:

- **CodeBlock.test.tsx** — 15+ tests covering rendering, copy functionality, syntax highlighting
- **ImageOutput.test.tsx** — 12+ tests covering rendering, lightbox, loading/error states
- **FileAttachment.test.tsx** — 12+ tests covering rendering, file types, download functionality
- **ActionButton.test.tsx** — 15+ tests covering variants, states, click handling

**Run tests:**
```bash
npm test CodeBlock.test.tsx
npm test ImageOutput.test.tsx
npm test FileAttachment.test.tsx
npm test ActionButton.test.tsx
```

**Integration test:**
```bash
npm test OutputComponents.integration.test.tsx
```

---

## Mobile Optimization

All components are mobile-optimized:

- Touch-friendly button sizes (min-height 44px on mobile)
- Responsive layouts
- Horizontal scroll for code blocks
- Fullscreen lightbox on mobile
- Filename truncation with ellipsis
- Adequate padding for touch targets

---

## Accessibility

All components follow accessibility best practices:

- Proper ARIA labels on interactive elements
- Keyboard navigation support
- Role attributes (e.g., dialog for lightbox)
- Disabled and loading states announced
- Alt text support for images

---

## File Structure

```
conversation-pane/
├── CodeBlock.tsx              # Code block component
├── CodeBlock.css              # Code block styles
├── CodeBlock.test.tsx         # Code block tests
├── ImageOutput.tsx            # Image component
├── ImageOutput.css            # Image styles
├── ImageOutput.test.tsx       # Image tests
├── FileAttachment.tsx         # File attachment component
├── FileAttachment.css         # File attachment styles
├── FileAttachment.test.tsx    # File attachment tests
├── ActionButton.tsx           # Action button component
├── ActionButton.css           # Action button styles
├── ActionButton.test.tsx      # Action button tests
├── OutputComponents.integration.test.tsx  # Integration tests
└── OUTPUT-COMPONENTS.md       # This file
```

---

## Dependencies

- `highlight.js` — Syntax highlighting (already installed)
- `react` — React 18.3+
- No additional dependencies required

---

## Notes

- CodeBlock uses highlight.js (already configured in ConversationPane.tsx)
- All components use CSS modules pattern
- No hardcoded colors — CSS variables only
- All files under 250 lines (constraint met)
- TDD approach: tests written before implementation
- No stubs — full implementation of all features
