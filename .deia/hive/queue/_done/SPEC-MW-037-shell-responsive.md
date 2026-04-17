# SPEC: Shell.tsx Responsive Wiring for Mobile

## Priority
P2

## Objective
Wire Shell.tsx for responsive layout behavior across desktop, tablet, and mobile viewports. Implements CSS media query breakpoints, conditionally renders components (menu-bar vs drawer, sidebar vs bottom-nav), and manages state for mobile-specific UI elements (FAB, mobile-nav, drawer).

## Context
The Shell component is the root layout frame for the ShiftCenter UI. It currently supports desktop layouts with sidebar + menu-bar. This spec adds responsive breakpoints to swap layouts on mobile: menu-bar becomes a drawer, sidebar becomes MobileNav, and the QuickActionsFAB appears for primary actions.

Files to read first:
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/shell/components/Shell.tsx` — shell component (already integrated MobileNav + FAB)
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/shell/components/MenuBar.tsx` — desktop menu bar
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/shell/components/MobileNav.tsx` — mobile navigation component
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/quick-actions-fab/QuickActionsFAB.tsx` — floating action button
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/scheduler/scheduler_mobile_workdesk.py:153` — task context in scheduler

## Dependencies
- MW-V05 (mobile-nav must be verified)
- MW-033 (command-palette mobile overlay must exist)

## Acceptance Criteria
- [ ] CSS media query breakpoints in `browser/src/shell/components/shell.css`:
  - Desktop: `>= 1024px` (menu-bar visible, MobileNav hidden, FAB hidden)
  - Tablet: `768px - 1023px` (menu-bar → drawer, FAB visible, MobileNav partial)
  - Mobile: `< 768px` (drawer only, FAB visible, MobileNav full-screen)
- [ ] Shell state: `isMobileViewport: boolean`, updated via `useMediaQuery()` hook
- [ ] Conditional rendering:
  - `{!isMobileViewport && <MenuBar />}` for desktop
  - `{isMobileViewport && <DrawerMenu isOpen={drawerOpen} onClose={...} />}` for mobile
  - `{isMobileViewport && <QuickActionsFAB />}` for mobile
  - `{isMobileViewport && <MobileNav />}` for mobile
- [ ] Drawer state: `drawerOpen: boolean`, toggled by hamburger icon (top-left) or swipe-from-edge gesture
- [ ] Layout swap: desktop uses flexbox sidebar, mobile uses fixed-position drawer + full-width content
- [ ] Status bar: always visible, position changes (bottom on mobile, integrated on desktop)
- [ ] Hide workspace bar on mobile viewports (< 768px)
- [ ] All CSS transitions smooth (300ms ease-in-out for drawer slide, FAB fade)
- [ ] 8+ integration tests (React Testing Library): render at each breakpoint, drawer toggle, FAB visibility

## Smoke Test
- [ ] Load Shell at 1920x1080 → MenuBar visible, FAB hidden, MobileNav hidden
- [ ] Resize to 375x667 → MenuBar hidden, FAB visible, MobileNav visible, drawer closed
- [ ] Click hamburger icon → drawer slides in from left
- [ ] 8+ tests pass covering all breakpoints and state transitions

## Model Assignment
sonnet

## Constraints
- Location: modify `browser/src/shell/components/Shell.tsx` (existing file)
- Location: modify `browser/src/shell/components/shell.css` (existing file)
- Location: create `browser/src/shell/hooks/useMediaQuery.ts` (new file, if not exists)
- CSS: only use CSS variables (no hardcoded colors)
- Max 100 lines added to Shell.tsx
- Max 80 lines for useMediaQuery hook
- Max 150 lines for tests
- TDD: tests first, then implementation
- No external responsive libraries (pure CSS + React hooks)
