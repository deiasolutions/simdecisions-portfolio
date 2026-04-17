# SPEC: User-Facing Error Handling

## Priority
P1

## Objective
Users see helpful error messages, not stack traces or blank screens. Every failure state has a UI.

## Context
Files to read first:
- `browser/src/shell/components/PaneContent.tsx`
- `browser/src/shell/components/AppletShell.tsx`
- `browser/src/primitives/terminal/`

## Acceptance Criteria
- [ ] Applet load failure: pane shows "Failed to load [applet name]. Try refreshing." with retry button
- [ ] API unreachable: terminal shows "Cannot reach server. Check your connection." (not a stack trace)
- [ ] LLM error (bad API key, rate limit, model down): terminal shows human-readable message with suggestion ("Check your API key in Settings")
- [ ] 500 error from hivenode: user sees "Something went wrong. Error logged." (not the raw JSON error)
- [ ] Network timeout: terminal shows "Request timed out. Try again."
- [ ] React error boundary wraps every pane -- one crashing pane doesn't take down the whole app
- [ ] All error messages use var(--sd-*) colors (red accent for errors, yellow for warnings)
- [ ] 5+ tests

## Smoke Test
- [ ] Remove API key -> send message -> terminal shows "No API key configured" with link to settings
- [ ] Kill hivenode -> send message -> terminal shows connection error, not crash

## Model Assignment
haiku
