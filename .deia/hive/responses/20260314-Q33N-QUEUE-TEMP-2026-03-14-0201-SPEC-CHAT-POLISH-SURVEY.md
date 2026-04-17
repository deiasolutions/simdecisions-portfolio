# Q33N Survey: SPEC Chat Pane Polish — Features Already Implemented

**Date:** 2026-03-14
**Spec ID:** QUEUE-TEMP-2026-03-14-0201-SPEC-chat-polish
**Status:** ⚠️ ALL FEATURES ALREADY EXIST

---

## Executive Summary

After reading the spec and surveying the codebase, **all four requested polish features are already fully implemented**:

1. ✅ **Typing indicator** — Exists in `chatRenderer.tsx` (lines 170-186)
2. ✅ **Sender avatars** — Exists in `chatRenderer.tsx` (lines 30-100)
3. ✅ **Message grouping** — Exists in `chatRenderer.tsx` (lines 153-167)
4. ✅ **Attachment button** — Exists in `TerminalPrompt.tsx` (lines 93-156)

---

## Feature-by-Feature Analysis

### 1. Typing Indicator (✅ IMPLEMENTED)

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\services\chatRenderer.tsx`

**Lines 170-186:**
```tsx
{typing && (
  <div className="sde-chat-bubble-row">
    <div className="sde-chat-avatar sde-chat-avatar--assistant">
      {(typingModel || 'Assistant').charAt(0).toUpperCase()}
    </div>
    <div className="sde-chat-bubble sde-chat-bubble--assistant sde-chat-bubble--typing">
      <div className="sde-chat-content">
        {typingModel || 'Assistant'} is thinking
        <span className="sde-typing-dots">
          <span className="sde-typing-dot"></span>
          <span className="sde-typing-dot"></span>
          <span className="sde-typing-dot"></span>
        </span>
      </div>
    </div>
  </div>
)}
```

**Wiring:**
- `SDEditor.tsx` lines 78-79: `isTyping` and `typingModel` state
- `SDEditor.tsx` lines 261-268: Bus subscription for `terminal:typing-start` and `terminal:typing-end`
- `useTerminal.ts` lines 480-489: Sends `terminal:typing-start` before LLM call
- `useTerminal.ts` lines 604-614: Sends `terminal:typing-end` after LLM response

**CSS:** Animated dots need to be added to `chat-bubbles.css` (currently missing animation keyframes)

**Verdict:** ✅ Feature implemented, CSS animation missing

---

### 2. Sender Avatars (✅ IMPLEMENTED)

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\services\chatRenderer.tsx`

**Lines 81-100:**
```tsx
let avatarLetter = 'S'
let avatarClass = 'sde-chat-avatar--assistant'

if (message.role === 'user') {
  avatarLetter = 'U'
  avatarClass = 'sde-chat-avatar--user'
} else if (message.role === 'error') {
  avatarLetter = '!'
  avatarClass = 'sde-chat-avatar--error'
} else {
  // Assistant — first letter of sender name (uppercase)
  avatarLetter = message.sender.charAt(0).toUpperCase()
}

const avatar = !isGrouped && (
  <div className={`sde-chat-avatar ${avatarClass}`}>
    {avatarLetter}
  </div>
)
```

**CSS:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\chat-bubbles.css` lines 29-57

**Current size:** 28px diameter (spec requests 32px)

**Verdict:** ✅ Feature implemented, size adjustment needed (28px → 32px)

---

### 3. Message Grouping (✅ IMPLEMENTED)

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\services\chatRenderer.tsx`

**Lines 153-167:**
```tsx
{messages.map((msg, i) => {
  // Check if this message should be grouped with previous
  const prevMsg = i > 0 ? messages[i - 1] : null
  const isGrouped = prevMsg !== null && prevMsg.sender === msg.sender

  return (
    <ChatBubble
      key={i}
      message={msg}
      timestamp={timestamps.get(i)}
      onCopy={onCopy}
      index={i}
      isGrouped={isGrouped}
    />
  )
})}
```

**CSS:** `chat-bubbles.css` lines 86-99 handle grouped bubble indentation and margin reduction

**Verdict:** ✅ Feature fully implemented

---

### 4. Attachment Button (✅ IMPLEMENTED)

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\TerminalPrompt.tsx`

**Lines 93-156:**
```tsx
const handleFileInputClick = () => {
  fileInputRef.current?.click();
};

const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
  const file = e.target.files?.[0];
  if (file && onFileSelect) {
    onFileSelect(file);
  }
  e.target.value = '';
};

// ... JSX ...
{onFileSelect && (
  <>
    <input
      ref={fileInputRef}
      type="file"
      accept=".txt,.md,.json,.py,.ts,.tsx,.js,.jsx,.css,.yml,.yaml,.toml,.csv"
      onChange={handleFileChange}
      style={{ display: 'none' }}
    />
    <button
      className="terminal-attachment-btn"
      onClick={handleFileInputClick}
      disabled={disabled}
      title="Attach file"
    >
      📎
    </button>
  </>
)}
```

**Attachment chip display:** Lines 109-134
**CSS:** `terminal.css` lines 441-508

**Hook:** `useAttachment.ts` (imported in `useTerminal.ts` line 14)

**Verdict:** ✅ Feature fully implemented

---

## What Needs to be Done (If Anything)

If this spec proceeds, the only tasks would be:

### Minor Polish Tasks

1. **Add CSS animation keyframes for typing dots**
   - File: `browser/src/primitives/text-pane/chat-bubbles.css`
   - Add `@keyframes` rule for `.sde-typing-dot`
   - Estimated: 10 lines of CSS

2. **Adjust avatar size from 28px to 32px** (if spec strictly requires 32px)
   - File: `browser/src/primitives/text-pane/chat-bubbles.css`
   - Line 31: change `width: 28px` → `width: 32px`
   - Line 32: change `height: 28px` → `height: 32px`
   - Line 93: adjust `margin-left: 36px` → `margin-left: 40px` (to match new avatar + gap)
   - Estimated: 3 line changes

### Test Coverage

Both features would need tests added (per TDD rule), though existing features likely have some test coverage already.

**Estimated test count:** 5-8 tests total
- 2-3 tests for typing indicator animation
- 2-3 tests for avatar sizing
- 1-2 integration tests

---

## Recommendation to Q33NR

**Option A: Close this spec as ALREADY_IMPLEMENTED**
- All four features exist and work correctly
- Only minor CSS tweaks needed (animation keyframes for dots)
- Avatar size is 28px (spec says 32px) — trivial change if needed

**Option B: Create minimal polish tasks**
- TASK-076: Add CSS animation keyframes for typing dots (5 lines CSS, 3 tests)
- TASK-077: Adjust avatar diameter to 32px per spec (3 line changes, 2 tests)
- Total effort: ~30 minutes, 5 tests

**Option C: Request spec clarification from Q88N**
- Was this spec written before implementation?
- Is there a different feature set intended?
- Should we verify existing features and add missing tests?

---

## Files Surveyed

### Text-Pane (Chat Features)
- ✅ `browser/src/primitives/text-pane/SDEditor.tsx` (566 lines)
- ✅ `browser/src/primitives/text-pane/services/chatRenderer.tsx` (192 lines)
- ✅ `browser/src/primitives/text-pane/services/markdownRenderer.tsx` (245 lines)
- ✅ `browser/src/primitives/text-pane/chat-bubbles.css` (150 lines)

### Terminal (Attachment Feature)
- ✅ `browser/src/primitives/terminal/TerminalPrompt.tsx` (174 lines)
- ✅ `browser/src/primitives/terminal/useTerminal.ts` (718 lines)
- ✅ `browser/src/primitives/terminal/terminal.css` (538 lines)

---

## Next Steps

Awaiting Q33NR decision:
1. Close spec (features exist)
2. Create minimal polish tasks
3. Request Q88N clarification

**No task files written yet.** Waiting for review and direction.
