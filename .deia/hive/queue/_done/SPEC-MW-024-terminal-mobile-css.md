# SPEC: Terminal Mobile CSS + Pills

## Priority
P2

## Objective
Add mobile CSS to terminal primitive and implement command suggestion pills for touch-optimized command input.

## Context
The terminal component (`browser/src/primitives/terminal/TerminalApp.tsx`) is the PowerShell-style LLM interface. Desktop CSS is at `browser/src/primitives/terminal/terminal.css`. This task is SPECIAL — not just CSS, but also adds pill UI for command suggestions (MW-024 includes pill JSX + CSS). Mobile requires:
- Reduced padding, smaller fonts
- Touch-optimized buttons (48px minimum)
- Command suggestion pills (tap to insert command)
- Safe area handling for notched devices
- Hide status bar metrics on narrow screens

Files to read first:
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/terminal/terminal.css`
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/terminal/TerminalApp.tsx`
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/terminal/TerminalPrompt.tsx`

## Acceptance Criteria
- [ ] Add `@media (max-width: 768px)` breakpoint for tablet
- [ ] Add `@media (max-width: 480px)` breakpoint for phone
- [ ] Reduce `.terminal-output` padding from 16px 24px to 12px 16px on mobile
- [ ] Reduce font size from 14px to 13px on mobile
- [ ] Hide `.terminal-status-metrics` on mobile (<768px)
- [ ] Increase touch targets: `.terminal-status-btn`, `.terminal-voice-btn`, `.terminal-attachment-btn` min 48px on mobile
- [ ] Add command suggestion pills: `.terminal-suggestions` container below prompt
- [ ] Pill styles: `.terminal-pill` (inline-block, padding 8px 12px, border-radius 16px, touch-optimized)
- [ ] Pill tap behavior: insert command into prompt (JSX change required)
- [ ] Use `padding-bottom: env(safe-area-inset-bottom)` on `.terminal-prompt-area`
- [ ] Test on Chrome DevTools mobile emulator (375px, 768px viewports)

## Smoke Test
- [ ] Open terminal on 375px viewport — content readable, buttons tappable
- [ ] Tap voice button — 48px target, easy to hit
- [ ] See command suggestion pills below prompt
- [ ] Tap a pill — command inserted into prompt
- [ ] Scroll to bottom — safe area padding visible on iPhone notch

## Model Assignment
sonnet

## Depends On
None (Phase 5 CSS-only, but includes JSX for pills)

## Constraints
- Location: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/terminal/terminal.css`
- Location: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/terminal/TerminalPrompt.tsx` (add pills JSX)
- Use ONLY `var(--sd-*)` CSS variables
- No hardcoded colors, no rgb(), no hex
- Max 150 lines of new CSS
- Max 50 lines of JSX changes for pills
