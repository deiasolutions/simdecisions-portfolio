# SPEC-MW-056-terminal-visibility: Fix terminal not visibly rendering on workdesk desktop

## Priority
P0

## Depends On
None

## Model Assignment
sonnet

## Objective

On the workdesk set desktop view, the terminal pane (workdesk-engine, right side of the top split) appears as a dark empty space. The terminal is configured with `"displayMode": "minimal"` which hides the response pane (TerminalResponsePane), and `"inputSource": "bus"` which routes input through the bus. In minimal mode, the terminal only shows a thin input bar with no output — leaving a large dark rectangle.

The workdesk design intent is: conversation output on the left, command input on the right. The terminal should show its response pane so users can see command output. Fix the terminal config in workdesk.set.md:

1. Remove `"displayMode": "minimal"` (or set to `"full"`) so the terminal response pane is visible
2. Keep `"inputSource": "bus"` if bus-routed input is desired, OR remove it so the terminal has its own standard prompt
3. Remove `"hideStatusBar": true` — the terminal's own status bar is redundant with the bottom chrome status bar, but the terminal should at least show its response pane
4. Remove `"zone2Position": "hidden"` so zone 2 can render if needed

The terminal should be a usable, visible command terminal — not an invisible bus processor.

## Files to Read First

- browser/sets/workdesk.set.md
- browser/src/primitives/terminal/TerminalApp.tsx
- browser/src/apps/terminalAdapter.tsx

## Acceptance Criteria

- [ ] The terminal pane on workdesk desktop shows a visible prompt and response area
- [ ] Typing a command in the terminal shows output in the terminal response pane
- [ ] The terminal is not a dark empty rectangle
- [ ] The conversation pane (left) and terminal pane (right) are both visibly functional
- [ ] The workdesk.set.md config changes are minimal — only fix the terminal config, do not restructure the layout
- [ ] The set file remains valid JSON inside the layout code fence

## Smoke Test

- [ ] Open `http://localhost:5173/?set=workdesk` on desktop — verify terminal pane shows a prompt and is interactive
- [ ] Type a command in the terminal — verify output appears in the terminal pane

## Constraints

- Only modify browser/sets/workdesk.set.md terminal config
- No git operations
- Do not change the layout structure (split ratios, pane order)
- Do not modify any TypeScript/TSX files
- Keep `"promptPrefix": "hive>"` and `"brandName": "Workdesk"`
