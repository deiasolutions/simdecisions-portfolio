# TASK-081: Voice Output (TTS) Hook + Speaker Buttons

## Objective
Implement text-to-speech voice output for terminal responses using browser-native `speechSynthesis` API, with speaker buttons on each message and auto-read settings support.

## Context
The terminal displays AI responses in `TerminalOutput.tsx`. We need to add speaker buttons (🔊 icon) to each response entry that read the message aloud using `window.speechSynthesis`. Users should be able to toggle auto-read mode via settings.

### Web Speech Synthesis API Reference
```typescript
// Browser API (universally supported, no vendor prefix)
const synth = window.speechSynthesis;

// Create utterance
const utterance = new SpeechSynthesisUtterance(text);
utterance.lang = 'en-US';
utterance.rate = 1.0;
utterance.pitch = 1.0;
utterance.volume = 1.0;

// Events
utterance.onstart = () => {};
utterance.onend = () => {};
utterance.onerror = (event) => {};

// Speak
synth.speak(utterance);

// Control
synth.cancel(); // Stop all speech
synth.pause();
synth.resume();
synth.speaking; // Boolean
```

### Current Terminal Structure
- **TerminalOutput.tsx** (220 lines) — renders terminal entries (banner/input/response/system/ir)
- **useTerminal.ts** (717 lines) — state management, DO NOT modify for this task
- **terminal.css** — var(--sd-*) only, includes `.terminal-ir-btn` pattern for buttons

### Response Entry Structure (lines 96-123)
```tsx
case 'response':
  return (
    <div className="terminal-response">
      {entry.terminalMessage && (
        <div className="terminal-system">{entry.terminalMessage}</div>
      )}
      {showContent && (
        <ResponseContent content={entry.content} ... />
      )}
      {entry.metrics && (
        <div className="terminal-metrics">
          {formatChatMetrics(entry.metrics, entry.metricsOnly || false)}
        </div>
      )}
    </div>
  );
```

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\TerminalOutput.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\types.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\terminal.css`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\settings\settingsStore.ts`

## Deliverables

### 1. Speech Synthesis Hook
**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\useSpeechSynthesis.ts`

**Interface:**
```typescript
export interface UseSpeechSynthesisReturn {
  isSupported: boolean;
  isSpeaking: boolean;
  speak: (text: string) => void;
  stop: () => void;
  pause: () => void;
  resume: () => void;
}

export function useSpeechSynthesis(): UseSpeechSynthesisReturn;
```

**Requirements:**
- [ ] Check `window.speechSynthesis` availability on mount
- [ ] Return `isSupported: false` if API not available
- [ ] Track speaking state via `synth.speaking` (poll every 100ms when active)
- [ ] `speak(text)` creates `SpeechSynthesisUtterance` with:
  - `lang: 'en-US'`
  - `rate: 1.0`, `pitch: 1.0`, `volume: 1.0`
  - Fire `synth.speak(utterance)`
- [ ] `stop()` calls `synth.cancel()` to stop all speech
- [ ] `pause()` calls `synth.pause()`
- [ ] `resume()` calls `synth.resume()`
- [ ] Clean up on unmount (stop any ongoing speech)
- [ ] Handle edge case: if `synth.speaking` stuck (rare browser bug), auto-cancel after 30s

### 2. Speaker Button Component
**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\SpeakerButton.tsx`

**Interface:**
```typescript
interface SpeakerButtonProps {
  text: string;
  isSpeaking: boolean;
  onSpeak: () => void;
  onStop: () => void;
}

export function SpeakerButton({ text, isSpeaking, onSpeak, onStop }: SpeakerButtonProps): JSX.Element | null;
```

**Requirements:**
- [ ] Use `useSpeechSynthesis` hook
- [ ] Return `null` if `!isSupported` (graceful fallback)
- [ ] Render button with class `.terminal-speaker-btn` (see CSS below)
- [ ] Icon: `🔊` when not speaking, `⏸` when speaking
- [ ] Click behavior:
  - If not speaking: call `onSpeak()` → speaks the `text` prop
  - If speaking: call `onStop()` → stops speech
- [ ] Title attribute: "Read aloud" or "Stop reading"
- [ ] Apply `.terminal-speaker-btn--active` class when `isSpeaking` is true

### 3. CSS Styles
**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\terminal.css`

**Add these styles (var(--sd-*) only):**
```css
/* Speaker button for TTS */
.terminal-speaker-btn {
  background: transparent;
  border: none;
  color: var(--sd-text-muted);
  cursor: pointer;
  font-size: 16px;
  padding: 2px 6px;
  transition: color 0.15s ease, transform 0.15s ease;
  display: inline-flex;
  align-items: center;
  vertical-align: middle;
  margin-left: 8px;
}

.terminal-speaker-btn:hover {
  color: var(--sd-text-primary);
  transform: scale(1.1);
}

.terminal-speaker-btn--active {
  color: var(--sd-purple);
  animation: speaker-pulse 1s ease-in-out infinite;
}

@keyframes speaker-pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.6; }
}
```

### 4. Integration into TerminalOutput
**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\TerminalOutput.tsx`

**Changes:**

**A. Add TTS state to TerminalOutput component:**
```typescript
interface TerminalOutputProps {
  entries: TerminalEntry[];
  loading: boolean;
  onOpenInDesigner: (ir: any) => void;
  onCopy: (text: string) => void;
  onDownload: (ir: any) => void;
  autoReadEnabled?: boolean; // NEW: from settings
}

export function TerminalOutput({ entries, loading, onOpenInDesigner, onCopy, onDownload, autoReadEnabled = false }: TerminalOutputProps) {
  const { isSupported, isSpeaking, speak, stop } = useSpeechSynthesis();
  const [speakingEntryIndex, setSpeakingEntryIndex] = useState<number | null>(null);

  // Auto-read latest response if autoReadEnabled
  useEffect(() => {
    if (!autoReadEnabled || !isSupported) return;

    const lastEntry = entries[entries.length - 1];
    if (lastEntry?.type === 'response' && lastEntry.content) {
      speak(lastEntry.content);
      setSpeakingEntryIndex(entries.length - 1);
    }
  }, [entries.length, autoReadEnabled, isSupported]);

  // Update speakingEntryIndex when speech stops
  useEffect(() => {
    if (!isSpeaking) {
      setSpeakingEntryIndex(null);
    }
  }, [isSpeaking]);

  // ... rest of component
}
```

**B. Add SpeakerButton to response entries (in TerminalLine component):**
```tsx
case 'response':
  const showContent = !('metricsOnly' in entry && entry.metricsOnly);
  const entryIndex = /* pass from TerminalOutput map */;
  const isThisEntrySpeaking = speakingEntryIndex === entryIndex && isSpeaking;

  return (
    <div className="terminal-response">
      {entry.terminalMessage && (
        <div className="terminal-system">
          {entry.terminalMessage}
          <SpeakerButton
            text={entry.terminalMessage}
            isSpeaking={isThisEntrySpeaking}
            onSpeak={() => { speak(entry.terminalMessage!); setSpeakingEntryIndex(entryIndex); }}
            onStop={stop}
          />
        </div>
      )}
      {showContent && (
        <>
          <ResponseContent content={entry.content} ... />
          <SpeakerButton
            text={entry.content}
            isSpeaking={isThisEntrySpeaking}
            onSpeak={() => { speak(entry.content); setSpeakingEntryIndex(entryIndex); }}
            onStop={stop}
          />
        </>
      )}
      {entry.metrics && (
        <div className="terminal-metrics">
          {formatChatMetrics(entry.metrics, entry.metricsOnly || false)}
        </div>
      )}
    </div>
  );
```

**C. Pass entryIndex from map:**
```tsx
{entries.map((entry, idx) => {
  if ('hidden' in entry && entry.hidden) return null;
  return (
    <TerminalLine
      key={idx}
      entry={entry}
      entryIndex={idx}  // NEW
      speakingEntryIndex={speakingEntryIndex}  // NEW
      isSpeaking={isSpeaking}  // NEW
      onSpeak={(text) => { speak(text); setSpeakingEntryIndex(idx); }}  // NEW
      onStop={stop}  // NEW
      onOpenInDesigner={onOpenInDesigner}
      onCopy={onCopy}
      onDownload={onDownload}
    />
  );
})}
```

### 5. Wire to Terminal Pane (consumer)
**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\TerminalPane.tsx`

**Read settings and pass to TerminalOutput:**
```tsx
import { loadSettings } from '../settings/settingsStore';

// In component:
const settings = loadSettings();
const autoReadEnabled = settings.voice_auto_read ?? false;

<TerminalOutput
  entries={entries}
  loading={loading}
  onOpenInDesigner={openInDesigner}
  onCopy={copyToClipboard}
  onDownload={downloadIR}
  autoReadEnabled={autoReadEnabled}  // NEW
/>
```

## Test Requirements

### File: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\__tests__\useSpeechSynthesis.test.ts`

**Mock Setup:**
```typescript
const mockSynth = {
  speak: vi.fn(),
  cancel: vi.fn(),
  pause: vi.fn(),
  resume: vi.fn(),
  speaking: false,
  pending: false,
  paused: false,
};

Object.defineProperty(globalThis, 'speechSynthesis', {
  value: mockSynth,
  writable: true,
});

global.SpeechSynthesisUtterance = vi.fn().mockImplementation((text) => ({
  text,
  lang: 'en-US',
  rate: 1.0,
  pitch: 1.0,
  volume: 1.0,
  onstart: null,
  onend: null,
  onerror: null,
}));
```

**Test Scenarios (5 tests):**
- [ ] **Test 1:** Returns `isSupported: false` when `speechSynthesis` not available
- [ ] **Test 2:** Returns `isSupported: true` when API available
- [ ] **Test 3:** `speak(text)` creates utterance and calls `synth.speak()`
- [ ] **Test 4:** `stop()` calls `synth.cancel()`
- [ ] **Test 5:** `isSpeaking` reflects `synth.speaking` state

### File: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\__tests__\SpeakerButton.test.tsx`

**Test Scenarios (5 tests):**
- [ ] **Test 1:** Renders `null` when `isSupported: false`
- [ ] **Test 2:** Renders 🔊 icon when not speaking
- [ ] **Test 3:** Renders ⏸ icon when speaking
- [ ] **Test 4:** Calls `onSpeak` when clicked (not speaking)
- [ ] **Test 5:** Calls `onStop` when clicked (speaking)

### File: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\__tests__\TerminalOutput.tts.test.tsx`

**Test Scenarios (3 tests):**
- [ ] **Test 1:** Auto-read fires `speak()` for latest response when `autoReadEnabled: true`
- [ ] **Test 2:** Auto-read does NOT fire when `autoReadEnabled: false`
- [ ] **Test 3:** Speaker button on response entry calls `speak()` with entry content

**Total tests:** 13+

## Constraints
- **No file over 500 lines.** Current files: TerminalOutput (220), TerminalPane (~200)
- **CSS: var(--sd-*) only.** No hex, rgb(), or named colors.
- **No stubs.** Full implementation only.
- **TDD.** Write tests first, then implementation.
- **Browser-native API only.** No external TTS services.
- **Graceful fallback.** Hide speaker buttons if API not supported.
- **DO NOT modify useTerminal.ts** (717 lines, out of scope).

## Acceptance Criteria
- [ ] Speaker button (🔊) appears on each terminal response entry
- [ ] Button hidden if browser doesn't support `speechSynthesis`
- [ ] Click speaker → reads message aloud
- [ ] Icon changes to ⏸ while speaking, pulsing animation
- [ ] Click again → stops speaking
- [ ] Auto-read mode: latest response spoken automatically when setting enabled
- [ ] Auto-read respects `voice_auto_read` setting from settingsStore
- [ ] Only one message speaks at a time (stop previous when starting new)
- [ ] 13+ tests pass (mock speechSynthesis API)
- [ ] CSS uses var(--sd-*) only
- [ ] No file over 500 lines

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260314-TASK-081-RESPONSE.md`

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
