# SPEC: Progress-Pane Polish

## Priority
P2

## Objective
Create or polish the progress-pane CSS for mobile-friendly progress indicators (loading, build status, async operations).

## Context
The progress-pane is a utility primitive for showing async operation progress (spinners, progress bars, status messages). If it doesn't exist yet, create a minimal version. If it exists, add mobile CSS. Mobile requires:
- Touch-optimized spacing
- Responsive layout for narrow screens
- Safe area handling
- Clear visual feedback

Files to read first:
- Search for existing progress-pane files: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/**/progress*.tsx`
- Search for existing progress CSS: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/**/progress*.css`
- If none found, create new files

## Acceptance Criteria
- [ ] If progress-pane doesn't exist: create `progress-pane.css` with basic styles (spinner, progress bar, message container)
- [ ] If it exists: add mobile CSS optimizations
- [ ] Add `@media (max-width: 768px)` breakpoint for tablet
- [ ] Add `@media (max-width: 480px)` breakpoint for phone
- [ ] Reduce padding on mobile for `.progress-container`
- [ ] Responsive font sizes for progress messages
- [ ] Safe area handling if needed (bottom padding)
- [ ] Test on Chrome DevTools mobile emulator (375px, 768px viewports)

## Smoke Test
- [ ] Open progress-pane on 375px viewport — spinner/progress bar visible and centered
- [ ] Progress message readable on mobile
- [ ] Layout doesn't break on narrow screens

## Model Assignment
sonnet

## Depends On
None (Phase 5 CSS-only)

## Constraints
- Location: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/progress-pane/progress-pane.css` (create if needed)
- CSS only — no JSX if file doesn't exist, just CSS styles
- Use ONLY `var(--sd-*)` CSS variables
- No hardcoded colors, no rgb(), no hex
- Max 100 lines total (including base styles if creating new file)
