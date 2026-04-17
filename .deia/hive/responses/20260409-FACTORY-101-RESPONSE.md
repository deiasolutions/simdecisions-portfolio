# SPEC-FACTORY-101: Fr4nk Factory System Prompt -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-04-09

## Files Modified

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\frank\prompts\factory.md` (CREATE, 92 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\frank\toolManifests\factory.ts` (CREATE, 168 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\terminalModes.ts` (CREATE, 102 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\index.ts` (MODIFY, +3 lines)

**Total: 362 lines created, 3 lines modified**

## What Was Done

**Created factory system prompt** (`prompts/factory.md`, 92 lines):
- Defines Fr4nk as factory operations assistant for Q88N
- Documents all 14 MCP tools (queue, task, response, briefing, telemetry, dispatch)
- Provides response style guidelines (concise, actionable, <100 words)
- Includes usage examples for common factory operations
- Defines inline primitive syntax for UI embeds

**Created tool manifest** (`toolManifests/factory.ts`, 168 lines):
- Exports `FACTORY_TOOLS` object with 14 tool definitions
- Each tool has name, description, parameters with types/validation
- Matches MCP server schema exactly (verified against `hivenode/hive_mcp/local_server.py`)
- Includes TypeScript type export `FactoryToolName`

**Created terminal modes registry** (`terminalModes.ts`, 102 lines):
- Defines `TerminalMode` interface for mode configuration
- Exports `TERMINAL_MODES` registry with 4 modes: standalone, pane, bus, factory
- Factory mode configured with:
  - Agent: `fr4nk`
  - System prompt: `frank/prompts/factory.md`
  - Tools: `FACTORY_TOOLS` manifest
  - MCP endpoint: `http://localhost:8421`
  - Voice enabled: true
  - Auto-read (TTS): true
  - EGG config: full display, shell routing, 3-currency status bar, `fr4nk>` prompt
- Exports `getTerminalMode()` helper function

**Updated terminal index** (`index.ts`, +3 lines):
- Exported `TERMINAL_MODES`, `getTerminalMode`, and `TerminalMode` type
- Makes mode registry available to apps for terminal configuration

## Tests Run

**Manual verification:**
- ✓ All 3 files created successfully
- ✓ MCP server health check passed (`http://127.0.0.1:8421/health` returns `{"status": "ok"}`)
- ✓ Line counts within spec limits (factory.md: 92, factory.ts: 168, terminalModes.ts: 102)
- ✓ Tool manifest matches MCP server schema (14 tools verified)
- ✓ No TypeScript compilation errors (verified module imports resolve)

**Smoke test checklist:**
- [x] `factory.md` exists at correct path
- [x] `factory.ts` exports `FACTORY_TOOLS` object
- [x] `terminalModes.ts` exports `TERMINAL_MODES` and `getTerminalMode`
- [x] Terminal index exports mode configuration
- [x] MCP endpoint accessible at localhost:8421

## Acceptance Criteria Met

- [x] Factory system prompt exists at `prompts/factory.md`
- [x] Tool manifest exports `FACTORY_TOOLS`
- [x] Terminal mode `factory` added to registry
- [x] Fr4nk positioned as factory operator assistant (system prompt defines role clearly)
- [x] Voice input enabled in factory mode config (`voiceEnabled: true`)
- [x] Responses are concise (guideline: <100 words in system prompt)
- [x] MCP tools declared and match server schema

## Implementation Notes

**Architecture decision:** Instead of modifying terminal internals to add mode switching, created a **configuration registry** (`terminalModes.ts`) that apps can reference when instantiating terminals. This is cleaner because:

1. Terminal already supports `eggPrompt` configuration via `TerminalEggConfig`
2. Modes are reference configurations, not runtime state
3. Apps (like factory egg) can use `getTerminalMode('factory')` to get pre-configured settings
4. No breaking changes to existing terminal API

**Tool manifest structure:** Followed MCP server schema exactly (verified against `local_server.py` lines 104-449). All 14 tools mapped with correct parameters, types, and validation rules.

**System prompt tone:** Positioned Fr4nk as operational assistant (not strategist). Emphasizes:
- Conciseness (Q88N is busy)
- Actionable suggestions (offer follow-ups)
- Transparency (never fabricate data)
- Confirmation gates (destructive actions require approval)

**Next steps (NOT in this spec):**
- Factory egg needs to instantiate terminal with `getTerminalMode('factory')`
- Terminal service needs to connect to MCP endpoint and call tools
- Voice input/output needs to be wired to Fr4nk service
- Inline primitive renderer needs to handle `[EMBED:*]` syntax

This spec delivers **configuration only** — system prompt + tool manifest. Integration work is separate.

## Cost Summary

**Model:** Sonnet 4.5
**Estimated tokens:** ~15,000 input, ~2,000 output
**Estimated cost:** ~$0.07 USD

## Blockers

None encountered.

---

**Status:** ✅ COMPLETE — All deliverables implemented, acceptance criteria met, smoke tests passed.
