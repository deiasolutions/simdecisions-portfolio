# CHROME-E4: On-Close and On-Return Prompts

## Objective
Implement on-close prompt (save / don't save / cancel) when dirty flags are true. Implement on-return recovery prompt (restore / discard) when temp files exist from a previous session.

## Build Type
**New build** — No close prompt or recovery prompt exists. ClosePromptDialog.tsx and RecoveryPromptDialog.tsx are new components.

## Problem Analysis
If either dirty flag (layout or content) is true when the user closes the tab, a prompt appears: "You have unsaved changes. Save as a new version?" with Save / Don't Save / Cancel. On return, if temp files exist for the same EGG, a recovery prompt: "You have unsaved changes from [date]. Restore?" with Restore / Discard. If the user ignores recovery, temp files remain until 7-day TTL expires.

## Files to Read First
- browser/src/shell/components/Shell.tsx
- browser/src/shell/autosave.ts
- docs/specs/ADR-SC-CHROME-001-v3.md

## Files to Modify
- browser/src/shell/components/ClosePromptDialog.tsx — NEW component
- browser/src/shell/components/RecoveryPromptDialog.tsx — NEW component
- browser/src/shell/components/Shell.tsx — wire prompts to lifecycle
- browser/src/shell/components/__tests__/ClosePromptDialog.test.tsx — NEW tests
- browser/src/shell/components/__tests__/RecoveryPromptDialog.test.tsx — NEW tests

## Deliverables
- [ ] ClosePromptDialog: Save / Don't Save / Cancel
- [ ] Save → writes derived EGG, clears temp files
- [ ] Don't Save → temp files remain with 7-day TTL
- [ ] Cancel → stay in app
- [ ] No prompt if neither dirty flag is true
- [ ] RecoveryPromptDialog: Restore / Discard
- [ ] Restore → load temp layout and content, set dirty flags true
- [ ] Discard → delete temp files, load canonical/user EGG
- [ ] beforeunload fires native dialog as backup

## Acceptance Criteria
- [ ] Close with dirty state shows prompt
- [ ] Close with clean state closes silently
- [ ] Save clears temp files and dirty flags
- [ ] Recovery prompt shown when temp files exist on load
- [ ] Restore loads temp state correctly
- [ ] Discard removes temp files

## Test Requirements
- [ ] Tests written FIRST (TDD) — before implementation
- [ ] Test file: browser/src/shell/components/__tests__/ClosePromptDialog.test.tsx
- [ ] Test: renders when dirty flag true
- [ ] Test: does not render when both flags false
- [ ] Test: Save button triggers save and close
- [ ] Test: Cancel button keeps app open
- [ ] Test file: browser/src/shell/components/__tests__/RecoveryPromptDialog.test.tsx
- [ ] Test: renders when temp files exist
- [ ] Test: Restore loads temp state
- [ ] Test: Discard deletes temp files
- [ ] All tests pass
- [ ] Minimum 7 tests

## Smoke Test
- [ ] cd browser && npx vitest run src/shell/components/__tests__/ClosePromptDialog — tests pass
- [ ] cd browser && npx vitest run src/shell/components/__tests__/RecoveryPromptDialog — tests pass

## Constraints
- No file over 500 lines
- No stubs
- CSS: var(--sd-*) only
- Portal target for dialogs: .hhp-root

## Depends On
- SPEC-CHROME-E3 (autosave provides temp files)
- SPEC-CHROME-E2 (save-as-derived for Save button)
- SPEC-CHROME-A6 (dirty flags)

## Model Assignment
haiku

## Priority
P2
