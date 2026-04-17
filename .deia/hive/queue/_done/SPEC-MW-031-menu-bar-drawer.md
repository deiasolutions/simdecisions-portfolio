# SPEC: Menu-Bar → Drawer (Mobile)

## Priority
P2

## Objective
Convert menu-bar to a slide-out drawer on mobile instead of horizontal menu bar. This is STRUCTURAL — requires JSX changes + CSS animation.

## Context
The menu-bar component (`browser/src/primitives/menu-bar/MenuBarPrimitive.tsx`) is the horizontal menu bar with File/Edit/View menus. Desktop CSS is at `browser/src/primitives/menu-bar/MenuBarPrimitive.css`. On mobile, horizontal menus are hard to use. Convert to slide-out drawer:
- Triggered by hamburger button in top-bar
- Slides in from left
- Full-height overlay
- Tap outside to close
- Animated open/close

Files to read first:
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/menu-bar/MenuBarPrimitive.css`
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/menu-bar/MenuBarPrimitive.tsx`
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/shell/components/MobileNav.tsx` (if exists — may have drawer pattern already)

## Acceptance Criteria
- [ ] Add `@media (max-width: 768px)` breakpoint for tablet/phone
- [ ] On mobile: hide horizontal `.menu-bar-primitive`, show drawer trigger button
- [ ] Add drawer container: `.menu-bar-drawer` (fixed position, left: -100%, slides to left: 0)
- [ ] Drawer animation: CSS transition `left 0.3s ease-out`
- [ ] Drawer overlay: `.menu-bar-drawer-overlay` (fixed, full-screen, rgba backdrop)
- [ ] Drawer content: `.menu-bar-drawer-content` (width 280px, max-width 80vw, background, shadow)
- [ ] JSX changes required: wrap menu-bar in drawer container, add open/close state
- [ ] Safe area handling: `padding-top: env(safe-area-inset-top)`, `padding-left: env(safe-area-inset-left)`
- [ ] Test on Chrome DevTools mobile emulator (375px viewport)

## Smoke Test
- [ ] Open app on 375px viewport — horizontal menu-bar hidden
- [ ] Tap hamburger button (in top-bar) — drawer slides in from left
- [ ] Tap menu item in drawer — action executes, drawer closes
- [ ] Tap overlay outside drawer — drawer closes
- [ ] Drawer respects safe area on iPhone notch

## Model Assignment
sonnet

## Depends On
None (Phase 5, but requires JSX changes)

## Constraints
- Location: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/menu-bar/MenuBarPrimitive.css`
- Location: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/menu-bar/MenuBarPrimitive.tsx` (JSX changes for drawer state)
- Use ONLY `var(--sd-*)` CSS variables
- No hardcoded colors, no rgb(), no hex
- Max 150 lines of new CSS
- Max 80 lines of JSX changes
