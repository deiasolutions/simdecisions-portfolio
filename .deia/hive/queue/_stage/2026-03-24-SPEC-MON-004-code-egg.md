# SPEC-MON-004: code.shiftcenter.com EGG Assembly

## Priority
P1

## Depends On
SPEC-MON-001-monaco-applet-component
SPEC-MON-002-monaco-volume-adapter
SPEC-MON-003-monaco-relay-bus

## Objective
Create code.egg.md — the Monaco-powered code editor product for code.shiftcenter.com. The previous code EGG has been renamed to code-2026-03-24.egg.md as a reference template. This task creates a new code.egg.md from scratch using the code-editor appType built by MON-001/002/003. Two layout modes: code-default (sidebar + editor + Fr@nk terminal) and code-zen (editor only, all chrome hidden). Both share nodeId "code-editor" so document content survives mode swaps. Use code-2026-03-24.egg.md as a layout reference for the sidebar/terminal structure but replace the editor pane appType "text" with "code-editor".

## Files to Read First
- C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\code-2026-03-24.egg.md
- C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\eggs\eggResolver.ts
- C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\efemera.egg.md

## Scope

1. **Create new code.egg.md** — use code-2026-03-24.egg.md as layout template. Replace appType "text" with "code-editor" for the editor pane. Update config to use Monaco-specific settings (language, theme, minimap, fontSize, wordWrap, lineNumbers). All panes chrome: false. Standard menubar with displayName "Code", File/Edit/View/Help, username on right.

2. **Verify subdomain** — confirm "code" subdomain exists in eggResolver.ts hardcoded fallback table. If missing, add it following the efemera pattern.

3. **Verify EGG inflation** — code.egg.md inflates without errors through the EGG loader.

4. **Commands block** — register format-document, save-file, and zen-toggle commands.

5. **Zen mode** — code-zen mode hides chrome, shows editor only.

## Deliverables
1. C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\code.egg.md (new file)
2. C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\eggs\eggResolver.ts (subdomain if missing)
3. C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\eggs\__tests__\codeEgg.test.ts

## Acceptance Criteria
- [ ] code.egg.md exists as a new file (not overwriting code-2026-03-24.egg.md)
- [ ] code.egg.md inflates without errors (EGG loader parses cleanly)
- [ ] code-editor pane uses appType "code-editor" (not "text")
- [ ] code-default layout renders sidebar + editor + terminal
- [ ] code-zen mode renders editor only with chrome hidden
- [ ] Switching between modes preserves editor content (shared nodeId)
- [ ] Ctrl+S triggers code.save command (registered in Command Registry)
- [ ] code subdomain routes correctly in EGG router
- [ ] All panes have chrome: false
- [ ] MenuBar shows "Code" as app name with File/Edit/View/Help and username
- [ ] All tests pass (minimum 5 tests)
- [ ] npx vite build passes

## Response File
20260324-TASK-MON-004-RESPONSE.md
