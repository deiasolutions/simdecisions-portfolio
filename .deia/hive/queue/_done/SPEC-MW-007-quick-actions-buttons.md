# SPEC: Quick-Actions Mic + Keyboard Buttons

## Priority
P1

## Depends On
MW-006

## Objective
Build the action buttons for the QuickActions FAB: microphone button (voice input) and keyboard button (text input). Integrate with voice-input hook and command-interpreter.

## Context
MW-006 built the FAB shell. Now we add the actual action buttons:
- **Mic button**: Triggers voice input, shows listening state, handles errors
- **Keyboard button**: Opens text input modal for typed commands
- Both integrate with command-interpreter for execution

Files to read first:
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/quick-actions/QuickActions.tsx` — FAB component from MW-006
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/hooks/useVoiceInput.ts` — voice input hook

## Acceptance Criteria
- [ ] `MicButton.tsx` component that uses `useVoiceInput()` hook
- [ ] Mic button shows 3 states: idle (mic icon), listening (pulsing animation), error (error icon)
- [ ] Click mic → start voice input → show listening state → on final transcript → execute command
- [ ] Error handling: mic permission denied → show error message, fallback to keyboard input
- [ ] `KeyboardButton.tsx` component that opens text input modal
- [ ] Text input modal: single-line input, submit on Enter, cancel on Escape
- [ ] Text input integrates with command-interpreter for parsing and execution
- [ ] Both buttons show loading state while command executes
- [ ] Accessibility: keyboard shortcuts (Ctrl+K for keyboard, Ctrl+M for mic)
- [ ] Component tests: 12+ tests covering both buttons, all states, error cases
- [ ] Integration test: click mic → mock transcript → verify command execution

## Smoke Test
- [ ] Click mic button → mic permission requested, listening state shown
- [ ] Speak (mocked) "open terminal" → command executes, FAB closes
- [ ] Click mic button when mic denied → shows error, offers keyboard fallback
- [ ] Click keyboard button → text input modal opens
- [ ] Type "open terminal" + Enter → command executes, modal closes
- [ ] Run `npm test MicButton.test.tsx KeyboardButton.test.tsx` — all tests pass

## Model Assignment
sonnet

## Constraints
- Location: `browser/src/primitives/quick-actions/MicButton.tsx` (new file)
- Location: `browser/src/primitives/quick-actions/KeyboardButton.tsx` (new file)
- Location: `browser/src/primitives/quick-actions/TextInputModal.tsx` (new file)
- Location: `browser/src/primitives/quick-actions/MicButton.test.tsx` (new file)
- Location: `browser/src/primitives/quick-actions/KeyboardButton.test.tsx` (new file)
- TDD: Write tests first
- CSS variables only
- Max 250 lines per component
- Max 150 lines per test file
- NO STUBS — full implementation of voice and keyboard flows
- Use existing modal patterns for TextInputModal
