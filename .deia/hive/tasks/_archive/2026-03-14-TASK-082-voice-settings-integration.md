# TASK-082: Voice Settings Integration

## Objective
Add voice-related settings to the settings store and settings UI: enable/disable voice input, auto-read responses toggle.

## Context
The settings system uses `settingsStore.ts` for localStorage persistence and a settings UI component for user controls. We need to add two new settings for voice features:

1. **voice_enabled** — master toggle for voice features (default: true if API available, false otherwise)
2. **voice_auto_read** — auto-read AI responses aloud (default: false)

These settings will be consumed by TASK-080 (voice input button visibility) and TASK-081 (auto-read behavior).

### Current Settings Structure
The settingsStore uses a simple key-value pattern:
```typescript
interface UserSettings {
  apiKeys: Record<string, string>;
  defaultProvider: string;
  defaultModel: string;
  updatedAt: string;
}
```

Settings are stored in localStorage under key `sd_user_settings`.

### Current Settings UI
Settings UI is component-based:
- **SettingsModal.tsx** or similar component (location TBD via code search)
- Toggle switches for boolean settings
- Styled with var(--sd-*) CSS variables

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\settings\settingsStore.ts`
- Search for settings UI component: `Glob: browser/src/primitives/settings/*.tsx`
- Search for settings modal: `Grep: "SettingsModal|Settings.*Modal" --type ts`

## Deliverables

### 1. Update Settings Store Types
**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\settings\types.ts`

**Changes:**
```typescript
export interface UserSettings {
  apiKeys: Record<string, string>;
  defaultProvider: string;
  defaultModel: string;
  voice_enabled?: boolean;      // NEW
  voice_auto_read?: boolean;    // NEW
  updatedAt: string;
}
```

### 2. Update Settings Store Defaults
**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\settings\settingsStore.ts`

**Changes:**

**A. Update DEFAULT_SETTINGS:**
```typescript
const DEFAULT_SETTINGS: UserSettings = {
  apiKeys: {},
  defaultProvider: 'anthropic',
  defaultModel: 'claude-sonnet-4-5-20250929',
  voice_enabled: typeof window !== 'undefined' && !!(window.SpeechRecognition || (window as any).webkitSpeechRecognition),
  voice_auto_read: false,
  updatedAt: new Date().toISOString(),
};
```

**B. Add voice settings getters/setters:**
```typescript
/**
 * Get voice enabled setting.
 * Returns true if voice features should be available.
 */
export function getVoiceEnabled(): boolean {
  const settings = loadSettings();
  // Default to true if API available and setting not explicitly disabled
  if (settings.voice_enabled === undefined) {
    return typeof window !== 'undefined' && !!(window.SpeechRecognition || (window as any).webkitSpeechRecognition);
  }
  return settings.voice_enabled;
}

/**
 * Set voice enabled setting.
 */
export function setVoiceEnabled(enabled: boolean): void {
  const settings = loadSettings();
  settings.voice_enabled = enabled;
  saveSettings(settings);
}

/**
 * Get voice auto-read setting.
 * Returns true if AI responses should be read aloud automatically.
 */
export function getVoiceAutoRead(): boolean {
  const settings = loadSettings();
  return settings.voice_auto_read ?? false;
}

/**
 * Set voice auto-read setting.
 */
export function setVoiceAutoRead(enabled: boolean): void {
  const settings = loadSettings();
  settings.voice_auto_read = enabled;
  saveSettings(settings);
}
```

### 3. Find and Update Settings UI Component
**Discovery Step:**
- [ ] Use `Glob: browser/src/primitives/settings/*.tsx` to find settings UI
- [ ] Use `Grep: "SettingsModal|Settings.*Component" --type tsx` to find modal/panel
- [ ] If settings UI doesn't exist yet, create minimal component (see fallback below)

**Integration into existing Settings UI:**

**Add voice settings section:**
```tsx
{/* Voice Settings Section */}
<div className="settings-section">
  <h3 className="settings-section-title">Voice</h3>

  <div className="settings-row">
    <label className="settings-label">
      <input
        type="checkbox"
        checked={voiceEnabled}
        onChange={(e) => {
          setVoiceEnabled(e.target.checked);
          saveSettings({ ...settings, voice_enabled: e.target.checked });
        }}
        className="settings-checkbox"
      />
      <span>Enable voice input (microphone button)</span>
    </label>
    <p className="settings-help-text">
      Use browser speech recognition for voice input in terminal.
    </p>
  </div>

  <div className="settings-row">
    <label className="settings-label">
      <input
        type="checkbox"
        checked={voiceAutoRead}
        onChange={(e) => {
          setVoiceAutoRead(e.target.checked);
          saveSettings({ ...settings, voice_auto_read: e.target.checked });
        }}
        className="settings-checkbox"
      />
      <span>Auto-read AI responses</span>
    </label>
    <p className="settings-help-text">
      Automatically read AI responses aloud using text-to-speech.
    </p>
  </div>
</div>
```

**If settings UI doesn't exist, create minimal component:**

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\settings\SettingsPanel.tsx`

```tsx
import { useState, useEffect } from 'react';
import { loadSettings, saveSettings, getVoiceEnabled, setVoiceEnabled, getVoiceAutoRead, setVoiceAutoRead } from './settingsStore';
import './settings.css';

export function SettingsPanel() {
  const [voiceEnabled, setVoiceEnabledState] = useState(getVoiceEnabled());
  const [voiceAutoRead, setVoiceAutoReadState] = useState(getVoiceAutoRead());

  const handleVoiceEnabledChange = (enabled: boolean) => {
    setVoiceEnabledState(enabled);
    setVoiceEnabled(enabled);
  };

  const handleVoiceAutoReadChange = (enabled: boolean) => {
    setVoiceAutoReadState(enabled);
    setVoiceAutoRead(enabled);
  };

  return (
    <div className="settings-panel">
      <div className="settings-section">
        <h3 className="settings-section-title">Voice</h3>

        <div className="settings-row">
          <label className="settings-label">
            <input
              type="checkbox"
              checked={voiceEnabled}
              onChange={(e) => handleVoiceEnabledChange(e.target.checked)}
              className="settings-checkbox"
            />
            <span>Enable voice input</span>
          </label>
          <p className="settings-help-text">
            Use browser speech recognition for voice input in terminal.
          </p>
        </div>

        <div className="settings-row">
          <label className="settings-label">
            <input
              type="checkbox"
              checked={voiceAutoRead}
              onChange={(e) => handleVoiceAutoReadChange(e.target.checked)}
              className="settings-checkbox"
            />
            <span>Auto-read AI responses</span>
          </label>
          <p className="settings-help-text">
            Automatically read AI responses aloud using text-to-speech.
          </p>
        </div>
      </div>
    </div>
  );
}
```

### 4. CSS for Settings (if creating new component)
**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\settings\settings.css`

**Add these styles (var(--sd-*) only):**
```css
.settings-panel {
  padding: 24px;
  background: var(--sd-bg);
  color: var(--sd-text-primary);
  max-width: 600px;
}

.settings-section {
  margin-bottom: 32px;
}

.settings-section-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--sd-text-primary);
  margin-bottom: 16px;
  border-bottom: 1px solid var(--sd-border);
  padding-bottom: 8px;
}

.settings-row {
  margin-bottom: 20px;
}

.settings-label {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  font-size: 14px;
  color: var(--sd-text-primary);
}

.settings-checkbox {
  width: 18px;
  height: 18px;
  cursor: pointer;
  accent-color: var(--sd-purple);
}

.settings-help-text {
  font-size: 12px;
  color: var(--sd-text-muted);
  margin: 4px 0 0 26px;
  line-height: 1.5;
}
```

### 5. Wire Settings to Voice Components

**TASK-080 (VoiceInputButton) should read:**
```typescript
import { getVoiceEnabled } from '../settings/settingsStore';

// In component:
const voiceEnabled = getVoiceEnabled();
if (!isSupported || !voiceEnabled) {
  return null;
}
```

**TASK-081 (TerminalOutput) should read:**
```typescript
import { getVoiceAutoRead } from '../settings/settingsStore';

// In component:
const autoReadEnabled = getVoiceAutoRead();
```

**Note:** This wiring is informational for context. Actual implementation will be done by TASK-080 and TASK-081 bees when they integrate with settings.

## Test Requirements

### File: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\settings\__tests__\settingsStore.voice.test.ts`

**Test Scenarios (6 tests):**
- [ ] **Test 1:** `getVoiceEnabled()` returns `false` when SpeechRecognition not supported
- [ ] **Test 2:** `getVoiceEnabled()` returns `true` when SpeechRecognition supported and not disabled
- [ ] **Test 3:** `setVoiceEnabled(false)` persists to localStorage
- [ ] **Test 4:** `setVoiceEnabled(true)` persists to localStorage
- [ ] **Test 5:** `getVoiceAutoRead()` returns `false` by default
- [ ] **Test 6:** `setVoiceAutoRead(true)` persists to localStorage

### File: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\settings\__tests__\SettingsPanel.voice.test.tsx`

**Test Scenarios (4 tests):**
- [ ] **Test 1:** Voice enabled checkbox renders with correct initial state
- [ ] **Test 2:** Toggling voice enabled checkbox updates setting
- [ ] **Test 3:** Voice auto-read checkbox renders with correct initial state
- [ ] **Test 4:** Toggling voice auto-read checkbox updates setting

**Total tests:** 10+

## Constraints
- **No file over 500 lines.** Current file: settingsStore.ts (210 lines)
- **CSS: var(--sd-*) only.** No hex, rgb(), or named colors.
- **No stubs.** Full implementation only.
- **TDD.** Write tests first, then implementation.
- **Graceful fallback.** If SpeechRecognition not available, default `voice_enabled` to false.
- **Settings persistence.** All changes must persist to localStorage immediately.

## Acceptance Criteria
- [ ] `voice_enabled` setting added to UserSettings type
- [ ] `voice_auto_read` setting added to UserSettings type
- [ ] `voice_enabled` defaults to true if SpeechRecognition API available, false otherwise
- [ ] `voice_auto_read` defaults to false
- [ ] `getVoiceEnabled()` and `setVoiceEnabled()` functions exported from settingsStore
- [ ] `getVoiceAutoRead()` and `setVoiceAutoRead()` functions exported from settingsStore
- [ ] Settings UI includes voice settings section with two checkboxes
- [ ] Checkbox changes persist to localStorage immediately
- [ ] Help text explains what each setting does
- [ ] 10+ tests pass
- [ ] CSS uses var(--sd-*) only
- [ ] No file over 500 lines

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260314-TASK-082-RESPONSE.md`

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
