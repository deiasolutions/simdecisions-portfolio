# TASK-080: Voice Input (STT) Hook + Component + Integration

## Objective
Implement speech-to-text voice input for terminal using browser-native Web Speech API, with visual feedback and graceful fallbacks.

## Context
The terminal currently uses `TerminalPrompt.tsx` for text input with file attachments. We need to add a microphone button next to the attachment button that activates browser-native speech recognition and transcribes speech to the input field.

### Web Speech API Reference
```typescript
// Browser API (vendor-prefixed)
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const recognition = new SpeechRecognition();
recognition.continuous = false;
recognition.interimResults = true;
recognition.lang = 'en-US';

// Events
recognition.onstart = () => {};
recognition.onresult = (event) => {
  const transcript = event.results[0][0].transcript;
};
recognition.onerror = (event) => {};
recognition.onend = () => {};

// Methods
recognition.start();
recognition.stop();
```

### Current Terminal Structure
- **TerminalPrompt.tsx** (173 lines) — handles textarea input, file attachments (📎 button)
- **useTerminal.ts** (717 lines) — state management, command handling, LLM interaction
- **terminal.css** — var(--sd-*) only, includes `.terminal-attachment-btn` pattern

### File Attachment Button Pattern (to mirror)
```tsx
<button
  className="terminal-attachment-btn"
  onClick={handleFileInputClick}
  disabled={disabled}
  title="Attach file"
>
  📎
</button>
```

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\TerminalPrompt.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\useTerminal.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\terminal.css`

## Deliverables

### 1. Voice Recognition Hook
**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\useVoiceRecognition.ts`

**Interface:**
```typescript
export interface UseVoiceRecognitionReturn {
  isSupported: boolean;
  isListening: boolean;
  transcript: string;
  startListening: () => void;
  stopListening: () => void;
  error: string | null;
}

export function useVoiceRecognition(options?: {
  onTranscript?: (text: string) => void;
  onError?: (error: string) => void;
  silenceTimeout?: number; // ms, default 3000
}): UseVoiceRecognitionReturn;
```

**Requirements:**
- [ ] Check `window.SpeechRecognition || window.webkitSpeechRecognition` on mount
- [ ] Return `isSupported: false` if API not available
- [ ] Set `continuous: false`, `interimResults: true`, `lang: 'en-US'`
- [ ] Track listening state (`isListening`)
- [ ] Track interim transcript (updates as user speaks)
- [ ] Fire `onTranscript` callback with final transcript when recognition ends
- [ ] Fire `onError` callback on recognition errors
- [ ] Auto-stop after silence timeout (default 3s, measured from last interim result)
- [ ] Clean up recognition instance on unmount
- [ ] Handle vendor prefixes (`webkitSpeechRecognition` for Safari/Chrome)

### 2. Voice Input Button Component
**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\VoiceInputButton.tsx`

**Interface:**
```typescript
interface VoiceInputButtonProps {
  onTranscript: (text: string) => void;
  disabled: boolean;
}

export function VoiceInputButton({ onTranscript, disabled }: VoiceInputButtonProps): JSX.Element | null;
```

**Requirements:**
- [ ] Use `useVoiceRecognition` hook
- [ ] Return `null` if `!isSupported` (graceful fallback)
- [ ] Render microphone button: `🎤` unicode icon
- [ ] Apply `.terminal-voice-btn` CSS class (to be added)
- [ ] Toggle listening on click: if listening, stop; if not, start
- [ ] Show pulsing indicator dot when `isListening` (see CSS below)
- [ ] Disable button when `disabled` prop is true
- [ ] Call `onTranscript(text)` when final transcript received
- [ ] Show error state if recognition fails (brief visual feedback, no modal)
- [ ] Title attribute: "Voice input (click to start/stop)"

### 3. CSS Styles
**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\terminal.css`

**Add these styles (var(--sd-*) only):**
```css
/* Voice input button */
.terminal-voice-btn {
  background: transparent;
  border: none;
  color: var(--sd-text-secondary);
  cursor: pointer;
  font-size: 18px;
  padding: 0 8px;
  transition: color 0.15s ease, transform 0.15s ease;
  display: flex;
  align-items: center;
  position: relative;
}

.terminal-voice-btn:hover:not(:disabled) {
  color: var(--sd-text-primary);
  transform: scale(1.1);
}

.terminal-voice-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Listening state */
.terminal-voice-btn[data-listening="true"] {
  color: var(--sd-red);
}

/* Pulsing indicator dot */
.terminal-voice-indicator {
  position: absolute;
  top: 0;
  right: 4px;
  width: 6px;
  height: 6px;
  background: var(--sd-red);
  border-radius: 50%;
  animation: voice-pulse 1.5s ease-in-out infinite;
}

@keyframes voice-pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.4; transform: scale(1.3); }
}

/* Error state */
.terminal-voice-btn[data-error="true"] {
  color: var(--sd-red);
}
```

### 4. Integration into TerminalPrompt
**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\TerminalPrompt.tsx`

**Changes:**
- [ ] Import `VoiceInputButton` component
- [ ] Add voice button next to file attachment button (before prompt label)
- [ ] Wire `onTranscript` callback to append transcript to textarea value
- [ ] On transcript received: `onChange(value + ' ' + transcript)` (append with space)
- [ ] Stop listening when Enter key pressed (tie into existing `onSubmit` logic)
- [ ] Ensure button disabled state matches textarea disabled state

**Integration point (line 136-157, after file button):**
```tsx
{/* File attachment button */}
{onFileSelect && (
  <>
    <input ref={fileInputRef} type="file" ... />
    <button className="terminal-attachment-btn" ...>📎</button>
  </>
)}

{/* Voice input button */}
<VoiceInputButton
  onTranscript={(text) => onChange(value + (value ? ' ' : '') + text)}
  disabled={disabled}
/>

<span className={promptLabel.cssClass || 'terminal-prompt'}>{promptLabel.text}</span>
```

## Test Requirements

### File: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\__tests__\useVoiceRecognition.test.ts`

**Mock Setup:**
```typescript
const mockRecognition = {
  start: vi.fn(),
  stop: vi.fn(),
  addEventListener: vi.fn(),
  removeEventListener: vi.fn(),
  onstart: null,
  onend: null,
  onresult: null,
  onerror: null,
  continuous: false,
  interimResults: false,
  lang: 'en-US',
};

// Mock window.webkitSpeechRecognition
(globalThis as any).webkitSpeechRecognition = vi.fn(() => mockRecognition);
```

**Test Scenarios (6 tests):**
- [ ] **Test 1:** Returns `isSupported: false` when SpeechRecognition API not available
- [ ] **Test 2:** Returns `isSupported: true` when API available, sets recognition config
- [ ] **Test 3:** `startListening()` sets `isListening: true` and calls `recognition.start()`
- [ ] **Test 4:** `stopListening()` sets `isListening: false` and calls `recognition.stop()`
- [ ] **Test 5:** Fires `onTranscript` callback with final result when recognition ends
- [ ] **Test 6:** Fires `onError` callback when recognition error occurs

### File: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\__tests__\VoiceInputButton.test.tsx`

**Test Scenarios (5 tests):**
- [ ] **Test 1:** Renders `null` when `isSupported: false` (graceful fallback)
- [ ] **Test 2:** Renders microphone button when `isSupported: true`
- [ ] **Test 3:** Toggles listening state on click (starts/stops recognition)
- [ ] **Test 4:** Shows pulsing indicator when `isListening: true`
- [ ] **Test 5:** Calls `onTranscript` callback with recognized text
- [ ] **Test 6:** Disables button when `disabled` prop is true
- [ ] **Test 7:** Shows error state when recognition fails

### File: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\__tests__\TerminalPrompt.voice.test.tsx`

**Test Scenarios (2 tests):**
- [ ] **Test 1:** Voice input appends transcript to existing value with space separator
- [ ] **Test 2:** Voice input works when value is empty (no leading space)

**Total tests:** 13+

## Constraints
- **No file over 500 lines.** Current files: TerminalPrompt (173), useTerminal (717 — do NOT modify)
- **CSS: var(--sd-*) only.** No hex, rgb(), or named colors.
- **No stubs.** Full implementation only.
- **TDD.** Write tests first, then implementation.
- **Browser-native API only.** No external speech services or npm packages.
- **Graceful fallback.** Hide mic button if API not supported.
- **No hardcoded timeouts in components.** Use hook options.

## Acceptance Criteria
- [ ] Microphone button appears next to file attachment button (📎🎤)
- [ ] Button hidden if browser doesn't support SpeechRecognition
- [ ] Click mic → starts listening → shows pulsing red dot indicator
- [ ] Speech transcribed to textarea in real-time (interim results visible)
- [ ] Final transcript appends to input value when recognition ends
- [ ] Click mic again → stops listening
- [ ] Stop listening on Enter key submit
- [ ] Auto-stop after 3s of silence
- [ ] Error handling with visual feedback (no modals)
- [ ] 13+ tests pass (mock SpeechRecognition API)
- [ ] CSS uses var(--sd-*) only
- [ ] No file over 500 lines

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260314-TASK-080-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.

## Model Assignment
sonnet
