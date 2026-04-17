# SPEC-FACTORY-103: Voice Command Integration

**MODE: EXECUTE**

**Spec ID:** SPEC-FACTORY-103
**Created:** 2026-04-09
**Author:** Q88N
**Type:** FEATURE
**Status:** READY
**Phase:** P1

---

## Priority
P1

## Depends On
- SPEC-FACTORY-101 (Fr4nk factory context)

## Reference
- `browser/src/hooks/useVoiceInput.ts` — existing voice hook

## Model Assignment
haiku

## Purpose

Wire up voice commands for factory operations via existing `useVoiceInput` hook. Hold-to-talk on mobile, push-to-talk on desktop. Fr4nk receives transcription and responds with TTS.

**Deliverable:** Voice integration for factory mode (~80 lines)

---

## Current State

Per telemetry survey:
- `browser/src/hooks/useVoiceInput.ts` exists
- Terminal already has voice infrastructure
- Web Speech API for recognition
- TTS via Kokoro-82M or browser SpeechSynthesis

Need:
- Wire voice to factory terminal mode
- Add voice button to factory mobile UI
- Ensure Fr4nk responses are TTS-friendly

---

## Implementation

### 1. Add Voice Button to Factory EGG

In `factory.set.md`, add voice FAB:

```yaml
voiceButton:
  enabled: true
  position: bottom-left
  mode: hold-to-talk  # mobile default
  desktopMode: push-to-talk
  action:
    type: bus
    event: factory:voice-start
```

### 2. Voice Button Component

If not already abstracted, create minimal voice button:

```tsx
// browser/src/components/VoiceButton.tsx

import { useVoiceInput } from '../hooks/useVoiceInput';
import { Mic, MicOff } from 'lucide-react';

interface VoiceButtonProps {
  onTranscript: (text: string) => void;
  mode?: 'hold' | 'toggle';
}

export function VoiceButton({ onTranscript, mode = 'hold' }: VoiceButtonProps) {
  const { isListening, startListening, stopListening, transcript } = useVoiceInput();
  
  useEffect(() => {
    if (transcript && !isListening) {
      onTranscript(transcript);
    }
  }, [transcript, isListening]);
  
  const handleInteraction = mode === 'hold' 
    ? {
        onTouchStart: startListening,
        onTouchEnd: stopListening,
        onMouseDown: startListening,
        onMouseUp: stopListening,
      }
    : {
        onClick: () => isListening ? stopListening() : startListening(),
      };
  
  return (
    <button 
      className={`hhp-voice-btn ${isListening ? 'listening' : ''}`}
      {...handleInteraction}
      aria-label={isListening ? 'Listening...' : 'Hold to speak'}
    >
      {isListening ? <Mic className="animate-pulse" /> : <MicOff />}
    </button>
  );
}
```

### 3. Wire to Factory Terminal

In factory terminal mode, connect voice to Fr4nk:

```typescript
// In factory terminal or chat component

const handleVoiceTranscript = async (text: string) => {
  // Send to Fr4nk as if typed
  await sendMessage(text);
  
  // Fr4nk response will be TTS'd via autoRead flag in terminal mode
};

// Subscribe to voice events from EGG
useEffect(() => {
  const unsub = messageBus.subscribe('factory:voice-start', () => {
    voiceInputRef.current?.startListening();
  });
  return unsub;
}, []);
```

### 4. TTS Response

Factory terminal mode has `autoRead: true` in terminalModes.ts (from FACTORY-101). Ensure responses are spoken:

```typescript
// In terminal or Fr4nk response handler

const handleFrankResponse = (response: string) => {
  // Display in terminal
  appendOutput(response);
  
  // TTS if autoRead enabled
  if (terminalMode.autoRead && 'speechSynthesis' in window) {
    const utterance = new SpeechSynthesisUtterance(response);
    utterance.rate = 1.1;  // Slightly faster
    utterance.pitch = 1.0;
    speechSynthesis.speak(utterance);
  }
};
```

### 5. Voice-Optimized Responses

Update Fr4nk factory prompt to include voice guidance:

```markdown
## Voice Responses

When responding to voice input (indicated by [VOICE] prefix):
- Keep responses under 30 words
- No markdown formatting
- No lists or bullet points
- Conversational, speakable sentences
- Offer one follow-up action

Example voice response:
"Factory has 3 tasks queued and 1 blocked. The blocked one needs your approval for a deploy. Want me to show it?"
```

---

## File Targets

| File | Action | Lines |
|------|--------|-------|
| `browser/src/components/VoiceButton.tsx` | CREATE or MODIFY | ~50 |
| `eggs/factory.set.md` | MODIFY | +10 |
| `browser/src/primitives/terminal/TerminalPane.tsx` | MODIFY | +20 |
| `browser/src/services/frank/prompts/factory.md` | MODIFY | +15 |

---

## Reference Files

Read before implementation:
- `browser/src/hooks/useVoiceInput.ts` — existing voice hook
- `browser/src/primitives/terminal/` — terminal implementation
- `browser/src/services/frank/` — Fr4nk service

---

## Acceptance Criteria

- [ ] Voice button visible in factory mobile UI
- [ ] Hold-to-talk captures speech
- [ ] Transcription sent to Fr4nk
- [ ] Fr4nk response spoken via TTS
- [ ] Voice responses are concise and speakable
- [ ] Works on iOS Safari, Android Chrome
- [ ] Desktop has keyboard shortcut (Space to talk)

## Smoke Test

```bash
# Manual test on mobile:
# 1. Open factory EGG on phone
# 2. Hold voice button
# 3. Say "status"
# 4. Release button
# 5. Verify Fr4nk responds with spoken summary

# Desktop test:
# 1. Open factory in browser
# 2. Press and hold Space
# 3. Say "what's blocking"
# 4. Release Space
# 5. Verify response
```

## Constraints

- Use existing `useVoiceInput` hook
- Browser Web Speech API only (no external services)
- TTS via browser SpeechSynthesis (Kokoro optional upgrade)
- Voice button must not block FAB (spec submit)

## Response File

`.deia/hive/responses/20260409-FACTORY-103-RESPONSE.md`

---

*SPEC-FACTORY-103 — Q88N — 2026-04-09*
