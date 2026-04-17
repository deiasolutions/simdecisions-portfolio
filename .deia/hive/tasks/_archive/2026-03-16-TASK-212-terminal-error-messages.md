# TASK-212: Terminal Error Message Rendering (User-Friendly)

## Objective
Create a centralized error message classifier and renderer for the terminal, so users see helpful messages instead of stack traces.

## Context
Currently, errors in useTerminal.ts are caught and displayed as system messages, but the error messages are raw and technical. We need:
- Error classifier that detects error types (API unreachable, timeout, auth failure, rate limit, 500 error, network error)
- Human-readable message generator with actionable suggestions
- Consistent error styling in terminal output
- Link to settings when API key is missing or invalid

The terminal already has infrastructure for system messages. We need to enhance it with better error detection and formatting.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\useTerminal.ts` (lines 754-775 show current error handling)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\TerminalOutput.tsx` (line 131 shows system message rendering)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\types.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\terminal\providers\anthropic.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\terminal\providers\groq.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\terminal\providers\openai-compatible.ts`

## Deliverables
- [ ] Create `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\errorClassifier.ts`
  - Function `classifyError(error: Error | unknown): ErrorType`
  - Enum or union type for ErrorType: 'api_unreachable' | 'timeout' | 'auth_failure' | 'rate_limit' | 'server_error' | 'network_error' | 'unknown'
  - Detection logic based on error message, status code, error type
- [ ] Create `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\errorMessages.ts`
  - Function `getErrorMessage(errorType: ErrorType, error?: Error): { message: string, suggestion?: string }`
  - Messages:
    - api_unreachable: "Cannot reach server. Check your connection."
    - timeout: "Request timed out. Try again."
    - auth_failure: "Authentication failed. Check your API key in Settings."
    - rate_limit: "Rate limit exceeded. Wait a moment and try again."
    - server_error: "Something went wrong. Error logged."
    - network_error: "Network error. Check your connection."
    - unknown: "An error occurred. Try again or check the console."
  - Each message includes actionable suggestion
- [ ] Update `useTerminal.ts` catch blocks (lines 754-775, 411-415, 478-481, 553-556) to use error classifier
  - Replace raw error.message with classified message
  - Add suggestion text if available
  - For auth_failure, add link to settings (via onOpenSettings callback)
- [ ] Add error styling to `terminal.css`
  - `.terminal-error` class with var(--sd-red) color
  - `.terminal-error-suggestion` class with var(--sd-text-secondary) and var(--sd-orange) link
  - Warning variant: `.terminal-warning` with var(--sd-yellow)
- [ ] Update TerminalOutput.tsx system message rendering to support error level
  - Add optional `level: 'error' | 'warning' | 'info'` to TerminalEntry type (in types.ts)
  - Apply `.terminal-error` or `.terminal-warning` class based on level

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Edge cases:
  - Network timeout (fetch timeout) → classified as 'timeout'
  - 401 status code → classified as 'auth_failure'
  - 429 status code → classified as 'rate_limit'
  - 500 status code → classified as 'server_error'
  - Network offline / ERR_NETWORK → classified as 'network_error'
  - ECONNREFUSED → classified as 'api_unreachable'
  - Unknown error object → classified as 'unknown' with safe message
  - Error without message property → handled gracefully

## Test Files
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\__tests__\errorClassifier.test.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\__tests__\errorMessages.test.ts`

Expected test count: **8+ tests** (5+ classifier, 3+ message formatter)

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only (no hex, no rgb(), no named colors)
- No stubs
- Error messages must be user-friendly (no technical jargon or stack traces)
- Must preserve full error details in console for debugging (don't lose info)
- Must handle all error types from all LLM providers (Anthropic, Groq, OpenAI)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260316-TASK-212-RESPONSE.md`

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
