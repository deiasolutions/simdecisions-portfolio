# SPEC: BL-003 Expandable Input Overlay

## Priority
P2

## Objective
Terminal input area expands upward over the neighboring pane when the user is typing a long message, then collapses back when submitted.

## Context
When the terminal is in the bottom portion of a vertical split, the input field should be able to expand upward to give more typing space. This is controlled by `expandMode: expand-up` in the terminal config.

Files to read first:
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\TerminalInput.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\useTerminal.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\SplitContainer.tsx`

## Acceptance Criteria
- [ ] Terminal input expands upward when text exceeds 3 lines
- [ ] Expansion overlays the neighboring pane (position: absolute, z-index above sibling)
- [ ] Maximum expansion: 50% of the split container height
- [ ] Input collapses back to normal height on submit (Enter or send button)
- [ ] Smooth CSS transition on expand/collapse (150ms ease)
- [ ] Works in both seamless and non-seamless splits
- [ ] Config flag: `expandMode: 'expand-up' | 'fixed'` (default 'fixed')
- [ ] 6+ tests
- [ ] CSS: var(--sd-*) only

## Model Assignment
haiku

## Constraints
- Expansion is visual overlay only — does NOT resize the actual split
- Do NOT modify split container resize logic
- Only the terminal input expands, not the entire terminal pane
