# SPEC-MW-057-textpane-nested-menubar: Remove nested menu bar from text-pane in workdesk

## Priority
P0

## Depends On
None

## Model Assignment
sonnet

## Objective

On the workdesk set, the Conversation pane (appType `text-pane`) renders its own internal File/Edit/View/Help menu bar INSIDE the pane, in addition to the shell-level menu bar above it. This creates a duplicate menu bar. The text-pane should not render its own menu bar when it is running inside a shell that already has a menu-bar chrome pane. Investigate the TextPaneAdapter and the underlying text-pane primitive to find where this internal menu bar is rendered, and suppress it. The text-pane config in workdesk.set.md has `"format": "markdown"`, `"readOnly": true`, `"renderMode": "chat"` — none of these should trigger an internal menu bar.

## Files to Read First

- browser/src/apps/textPaneAdapter.tsx
- browser/src/primitives/text-pane/SDEditor.tsx
- browser/sets/workdesk.set.md
- browser/src/shell/components/ShellNodeRenderer.tsx

## Acceptance Criteria

- [ ] The Conversation pane does NOT render its own internal File/Edit/View/Help menu bar
- [ ] The shell-level menu bar (MenuBarPrimitive) still renders correctly above
- [ ] The text-pane content area uses the full height of the pane without a duplicate menu bar consuming space
- [ ] Other sets that use text-pane are not broken by this change
- [ ] No TypeScript compilation errors (`npx tsc --noEmit` passes)

## Smoke Test

- [ ] Open `http://localhost:5173/?set=workdesk` — verify the Conversation pane has NO internal menu bar (only the shell menu bar above)

## Constraints

- No file over 500 lines
- No stubs — every function complete
- No git operations
- Use var(--sd-*) CSS variables only
- Prefer a config-based solution (e.g. a `hideMenuBar` config option) over removing the internal menu bar entirely, since other sets may want it
