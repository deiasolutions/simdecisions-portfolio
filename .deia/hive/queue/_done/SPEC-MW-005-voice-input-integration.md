# SPEC: Voice-Input Command-Interpreter Integration

## Priority
P1

## Depends On
MW-004

## Objective
Build the glue layer between `useVoiceInput` hook and command-interpreter backend. This includes the API route, WebSocket streaming, and state synchronization for real-time voice command execution.

## Context
MW-004 enhanced the voice input hook. Now we need the backend integration:
- FastAPI route to receive voice transcripts and return parsed commands
- Optional WebSocket endpoint for streaming interim transcripts
- State sync: voice → parse → confirm/disambiguate → execute → result
- Error handling: network failures, parsing errors, command execution failures

Files to read first:
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/hooks/useVoiceInput.ts` — frontend hook
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/shell/command_interpreter.py` — backend parser

## Acceptance Criteria
- [ ] FastAPI route: `POST /api/voice/parse` that receives transcript and returns ParseResult
- [ ] Request schema: `{ "transcript": str, "confidence": float, "context": dict }`
- [ ] Response schema: `{ "command": str, "arguments": dict, "confidence": float, "mode": str, "ir": dict }`
- [ ] WebSocket endpoint: `WS /api/voice/stream` for streaming interim transcripts (optional)
- [ ] Integration: call command_interpreter.parse() on transcript
- [ ] Integration: call prism_emitter.emit() to generate PRISM-IR
- [ ] Integration: call confirmation_handler.resolve() if mode is confirm/disambiguate
- [ ] Error handling: invalid transcript → 400, parsing error → 422, execution error → 500
- [ ] Logging: log all voice commands with timestamp, confidence, execution result
- [ ] Unit tests: 8+ tests covering parse endpoint, error cases, WebSocket streaming
- [ ] Integration test: real HTTP request → parse → emit → response

## Smoke Test
- [ ] `curl -X POST /api/voice/parse -d '{"transcript":"open terminal","confidence":0.95}'` → returns valid ParseResult JSON
- [ ] `curl -X POST /api/voice/parse -d '{"transcript":"opn terminal","confidence":0.78}'` → returns mode="confirm"
- [ ] `curl -X POST /api/voice/parse -d '{"transcript":"","confidence":0}'` → returns 400 error
- [ ] WebSocket test: connect → send interim transcript → receive interim parse result
- [ ] Run `pytest hivenode/routes/tests/test_voice_routes.py` — all tests pass

## Model Assignment
sonnet

## Constraints
- Location: `hivenode/routes/voice_routes.py` (new file)
- Location: `hivenode/routes/tests/test_voice_routes.py` (new file)
- TDD: Write tests first
- Use existing FastAPI patterns from other routes
- Max 300 lines for voice_routes.py
- Max 150 lines for tests
- NO STUBS — full implementation of parse endpoint and WebSocket
- Must register route in main FastAPI app
- Use Pydantic schemas for request/response validation
