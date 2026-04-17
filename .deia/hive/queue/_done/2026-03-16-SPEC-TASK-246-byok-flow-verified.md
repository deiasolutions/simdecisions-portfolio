# TASK-246: BYOK Flow Verified — Paste API Key, Chat Works (W5 — 5.8)

## Objective
Verify the BYOK (Bring Your Own Key) flow works: user pastes their Anthropic/OpenAI API key in settings, and the chat terminal immediately starts working with their key.

## Context
Wave 5 Ship. BYOK is the first-run experience — the moment a new user goes from "signed up" to "using the product." It must be frictionless. Paste key → chat works. No config files, no environment variables, no restart.

## Source Spec
`docs/specs/WAVE-5-SHIP.md` — Task 5.8

## Files to Read First
- `browser/src/shell/components/SettingsModal.tsx` — Settings UI (if exists)
- `browser/src/services/` — Service layer for API key storage
- `hivenode/routes/` — Backend routes that use LLM providers
- `eggs/chat.egg.md` — Chat EGG references llmProvider config

## Deliverables
- [ ] Trace the BYOK flow and document:
  1. User opens settings (or is prompted on first use)
  2. User selects provider (Anthropic, OpenAI, Groq)
  3. User pastes API key
  4. Key is stored in localStorage (`sd_user_settings`)
  5. Terminal sends messages using the stored key
  6. Chat responses appear in text-pane
- [ ] Verify each step works
- [ ] If settings UI doesn't exist, create a minimal one:
  - Modal with provider dropdown + API key input + Save button
  - Opens from menu bar Help → Settings (or gear icon)
- [ ] Fix any broken steps
- [ ] Add test: BYOK key stored, terminal uses it for requests
- [ ] Run: `cd browser && npx vitest run`

## Priority
P1

## Model
haiku
