# SPEC: Command-Palette Mobile Overlay

## Priority
P2

## Objective
Convert command-palette to fullscreen overlay on mobile instead of centered modal. Requires JSX changes + CSS.

## Context
The command-palette component (`browser/src/primitives/command-palette/CommandPalette.tsx`) is the command search UI. Desktop CSS is at `browser/src/primitives/command-palette/CommandPalette.css`. Desktop shows centered modal. On mobile, centered modals are awkward — convert to fullscreen overlay:
- Fullscreen on phones (<480px)
- Bottom sheet on tablets (768px)
- Animated slide-up
- Tap outside to close (optional on fullscreen)

Files to read first:
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/command-palette/CommandPalette.css`
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/command-palette/CommandPalette.tsx`

## Acceptance Criteria
- [ ] Add `@media (max-width: 768px)` breakpoint for tablet (bottom sheet)
- [ ] Add `@media (max-width: 480px)` breakpoint for phone (fullscreen)
- [ ] On phones: `.command-palette` fullscreen (width: 100vw, height: 100vh, border-radius: 0)
- [ ] On tablets: keep bottom sheet (width: 100vw, max-height: 80vh, border-radius top only)
- [ ] Animation: slide-up from bottom (already exists, verify)
- [ ] Increase `.command-palette-item` padding to min 48px touch target on mobile
- [ ] Add safe area handling: `padding-bottom: env(safe-area-inset-bottom)` on `.command-palette-list`
- [ ] JSX changes: detect screen size, apply mobile class
- [ ] Test on Chrome DevTools mobile emulator (375px, 768px viewports)

## Smoke Test
- [ ] Open command-palette on 375px viewport — fullscreen overlay
- [ ] Tap command item — easy to hit (48px min height)
- [ ] Type in search input — keyboard doesn't cover results
- [ ] Tap outside (if applicable) — palette closes
- [ ] Safe area respected on iPhone notch

## Model Assignment
sonnet

## Depends On
None (Phase 5, but requires JSX changes)

## Constraints
- Location: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/command-palette/CommandPalette.css`
- Location: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/command-palette/CommandPalette.tsx` (JSX changes for mobile class)
- Use ONLY `var(--sd-*)` CSS variables
- No hardcoded colors, no rgb(), no hex
- Max 100 lines of new CSS
- Max 50 lines of JSX changes
