# SPEC: Terminal Pill UI Component

## Priority
P2

## Objective
Build a React component that renders TF-IDF suggestions as horizontally scrollable pill buttons. Pills are tappable on mobile and clickable on desktop, inserting the suggested command into the terminal input when selected.

## Context
The terminal suggestion system (MW-034) provides ranked command suggestions based on TF-IDF scoring. This spec creates the UI layer that displays those suggestions as interactive pills. The design is mobile-first with horizontal scroll, similar to browser tab bars or filter chips.

Files to read first:
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/terminal/TerminalApp.tsx` — terminal component structure
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/terminal/TerminalPrompt.tsx` — terminal input component
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/queue/backlog/SPEC-MW-034-tfidf-index.md` — backend index spec
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/scheduler/scheduler_mobile_workdesk.py:147` — task context in scheduler

## Dependencies
- MW-034 (TF-IDF index must exist to provide suggestions)

## Acceptance Criteria
- [ ] `SuggestionPills` component in `browser/src/primitives/terminal/SuggestionPills.tsx`
- [ ] Props: `suggestions: Array<{command: string, score: number}>`, `onSelect: (command: string) => void`
- [ ] Horizontal scrollable container (CSS: `overflow-x: auto`, `display: flex`, `gap: 8px`)
- [ ] Each pill is a button with command text and optional score badge (hidden by default, shown on hover/long-press)
- [ ] Tap/click pill → calls `onSelect(command)` → parent inserts command into terminal input
- [ ] Mobile: smooth scroll physics, no scrollbar visible (CSS: `::-webkit-scrollbar { display: none }`)
- [ ] Desktop: hover states, scrollbar auto-hide
- [ ] Pill style: rounded corners (12px), padding (8px 16px), CSS variables for colors (`var(--sd-pill-bg)`, etc.)
- [ ] Integration with `TerminalApp.tsx`: fetch suggestions on input change (debounced 300ms)
- [ ] Integration with `TerminalPrompt.tsx`: insert selected command at cursor position
- [ ] Empty state: hide pills container when no suggestions
- [ ] Accessibility: pills are focusable, keyboard navigation (arrow keys to cycle), Enter to select
- [ ] 8+ unit tests (React Testing Library): render, select, keyboard nav, empty state

## Smoke Test
- [ ] Render `<SuggestionPills suggestions={[{command: "ls", score: 0.9}, {command: "cd", score: 0.8}]} />`
- [ ] Pills render horizontally, scrollable
- [ ] Click "ls" pill → `onSelect("ls")` called
- [ ] Keyboard: Tab to pills, ArrowRight → focus next pill, Enter → select
- [ ] 8+ tests pass with 100% coverage of component logic

## Model Assignment
sonnet

## Constraints
- Location: `browser/src/primitives/terminal/SuggestionPills.tsx` (new file)
- Location: `browser/src/primitives/terminal/SuggestionPills.css` (new file)
- Integration: modify `TerminalApp.tsx` to fetch suggestions and pass to `<SuggestionPills />`
- CSS: only use CSS variables (no hardcoded colors)
- Max 250 lines for component
- Max 150 lines for tests
- TDD: tests first, then implementation
- No external UI libraries (pure React + CSS)
