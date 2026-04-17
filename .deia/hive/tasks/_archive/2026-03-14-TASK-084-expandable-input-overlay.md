# TASK-084: Expandable Input Overlay

## Objective
Implement expand-up overlay behavior for terminal input when text exceeds 3 lines, allowing the input area to overlay the neighboring pane above it.

## Context
The terminal prompt currently grows inline via auto-resize logic in `TerminalPrompt.tsx` (lines 52-63). When in a bottom pane of a vertical split, we want the input area to expand upward and overlay the pane above it when typing long messages.

This requires:
- CSS positioning changes to make `.terminal-prompt-area` overlay-capable
- State tracking for expand/collapse behavior
- Config flag in `TerminalEggConfig` to enable this mode
- Smooth CSS transitions

The feature is controlled by `expandMode: 'expand-up'` in the terminal EGG config. Default is `'fixed'` (current behavior).

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\TerminalPrompt.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\TerminalApp.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\terminal.css`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\types.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\SplitContainer.tsx`

## Deliverables

### 1. Type Updates
- [ ] Add `expandMode?: 'expand-up' | 'fixed'` to `TerminalEggConfig` in `types.ts` (default: 'fixed')

### 2. TerminalApp.tsx Changes
- [ ] Read `expandMode` from `eggConfig` (default 'fixed')
- [ ] Pass `expandMode` prop to `TerminalPrompt`
- [ ] Add state for tracking expanded/collapsed: `const [inputExpanded, setInputExpanded] = useState(false)`
- [ ] Pass `inputExpanded` and `setInputExpanded` to `TerminalPrompt`
- [ ] Add `data-input-expanded` attribute to `.terminal-prompt-area` div for CSS targeting
- [ ] Reset `setInputExpanded(false)` when `terminal.handleSubmit` completes

### 3. TerminalPrompt.tsx Changes
- [ ] Accept new props: `expandMode`, `inputExpanded`, `setInputExpanded`
- [ ] Track line count in `autoResize()`: count `\n` chars + 1
- [ ] Set `setInputExpanded(true)` when line count > 3 AND `expandMode === 'expand-up'`
- [ ] Set `setInputExpanded(false)` when line count <= 3
- [ ] Ensure expand state resets on submit (parent already handles this via `terminal.handleSubmit`)

### 4. CSS Changes in terminal.css
- [ ] Add `.terminal-prompt-area[data-input-expanded="true"]` styles:
  - `position: absolute`
  - `bottom: 0`
  - `left: 0`
  - `right: 0`
  - `z-index: 100`
  - `max-height: 50vh`
  - `overflow-y: auto`
  - `box-shadow: 0 -4px 12px var(--sd-shadow-lg)`
- [ ] Add transition: `transition: max-height 0.15s ease, box-shadow 0.15s ease`
- [ ] Ensure `.terminal-prompt-area` default remains `position: relative` (or static)

### 5. Edge Cases
- [ ] Works in both seamless and non-seamless splits
- [ ] Does NOT modify split container resize logic
- [ ] Only the prompt area expands, not the entire terminal pane
- [ ] Expansion limited to 50vh (50% of viewport height, NOT split container height)
- [ ] Smooth collapse when text is deleted back under 3 lines
- [ ] Expand state resets on Enter/submit

## Test Requirements

### Unit Tests (6+ tests)
File: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\__tests__\TerminalPrompt.expand.test.tsx`

Test scenarios:
- [ ] Default behavior: `expandMode='fixed'` does NOT expand regardless of line count
- [ ] Expand-up mode: input expands when text exceeds 3 lines
- [ ] Expand-up mode: input collapses when text goes back under 3 lines
- [ ] Expand state resets on submit (via onSubmit callback)
- [ ] CSS classes applied correctly: `data-input-expanded` attribute matches state
- [ ] Max height constraint enforced via CSS

### Integration Test
File: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\__tests__\TerminalApp.expand.test.tsx`

Test scenario:
- [ ] TerminalApp with `eggConfig.expandMode='expand-up'` passes correct props to TerminalPrompt
- [ ] Submit handler resets expand state

All tests MUST:
- Be written FIRST (TDD)
- Use vitest framework
- Mock user typing via `fireEvent.change`
- Assert on `data-input-expanded` attribute or expanded state

## Constraints
- **No file over 500 lines.** Check before committing.
- **CSS: var(--sd-*) only.** No hex, no rgb(), no named colors except in transitions/shadows where unavoidable.
- **No stubs.** Every function fully implemented.
- **Do NOT modify SplitContainer.tsx.** This is a CSS overlay, not a split resize.
- **Do NOT modify shell reducer or split resize logic.**
- **Expansion is visual overlay only** — the split pane sizes do NOT change.

## Acceptance Criteria (from spec)
- [ ] Terminal input expands upward when text exceeds 3 lines
- [ ] Expansion overlays the neighboring pane (position: absolute, z-index above sibling)
- [ ] Maximum expansion: 50% of viewport height (50vh)
- [ ] Input collapses back to normal height on submit (Enter or send button)
- [ ] Smooth CSS transition on expand/collapse (150ms ease)
- [ ] Works in both seamless and non-seamless splits
- [ ] Config flag: `expandMode: 'expand-up' | 'fixed'` (default 'fixed')
- [ ] 6+ tests
- [ ] CSS: var(--sd-*) only

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260314-TASK-084-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.
