# SPEC: Diff-Viewer Swipe Actions

## Priority
P2

## Depends On
MW-021

## Objective
Add swipe actions for diff-viewer lines and hunks: swipe-left to stage (approve), swipe-right to unstage (reject), and optional comment action for code review workflow.

## Context
Diff-viewer should support mobile code review gestures:
- Swipe line left (>50% width) → stage line (approve change)
- Swipe line right (>50% width) → unstage line (reject change)
- Optional: long-press line → comment action (code review)
- Visual feedback: line follows finger during swipe (translate transform)
- Action icons: checkmark (stage), X (unstage), comment bubble (comment)
- State persisted in localStorage: staged/unstaged lines per file

Files to read first:
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/diff-viewer/DiffViewer.tsx` — viewer from MW-020/021
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/hooks/useSwipeNotification.ts` — swipe gesture pattern from MW-015
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/hooks/useSwipeBack.ts` — swipe gesture pattern from MW-012
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/infrastructure/relay_bus.ts` — bus events

## Acceptance Criteria
- [ ] `useSwipeDiffLine` hook for swipe gestures (based on useSwipeNotification pattern)
- [ ] Swipe left (>50% width) → stage line (checkmark icon appears, line marked as staged)
- [ ] Swipe right (>50% width) → unstage line (X icon appears, line marked as unstaged)
- [ ] Visual feedback: line follows finger during swipe (translate transform)
- [ ] Swipe cancel: if distance < 50% → snap back to original position
- [ ] Action icons: checkmark (✓) for stage, X (✗) for unstage, rendered during swipe
- [ ] Staged state persisted in localStorage: `sd:diff_viewer_staged` (JSON map of file:line)
- [ ] Optional: long-press line (500ms) → comment action (show comment input)
- [ ] Haptic feedback: if Navigator.vibrate available → vibrate(50) on swipe complete
- [ ] All CSS variables only (no hardcoded colors)
- [ ] 10+ unit tests (swipe, stage, unstage, persistence) + 2 E2E tests
- [ ] Accessible: keyboard shortcuts (Ctrl+S = stage line, Ctrl+U = unstage line)

## Smoke Test
- [ ] Swipe diff line left (>50%) → line staged, checkmark icon appears
- [ ] Swipe diff line right (>50%) → line unstaged, X icon appears
- [ ] Swipe 30% left, release → snap back (no stage)
- [ ] Reload page → staged lines remain staged (persistence works)
- [ ] Keyboard: Ctrl+S on focused line → line staged
- [ ] On device with haptics: swipe complete → vibration

## Model Assignment
sonnet

## Constraints
- Location: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/diff-viewer/DiffViewer.tsx` (modify)
- Location: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/hooks/useSwipeDiffLine.ts` (new file)
- Location: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/hooks/__tests__/useSwipeDiffLine.test.ts`
- TDD: tests first
- Max 150 lines for hook
- Max 100 lines of changes to DiffViewer.tsx
- Max 150 lines for tests
- localStorage key: `sd:diff_viewer_staged`
- Action icons: CSS-only (Unicode ✓ and ✗, not SVG)
- Use CSS transforms for 60fps animation (not position/margin)
