# TASK-029: Browser Terminal Shell Parsing

**Assigned to:** BEE-SONNET
**Model:** Sonnet
**Date:** 2026-03-12
**Spec:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\specs\SPEC-HIVENODE-E2E-001.md` (Section 4)
**Parent:** SPEC-HIVENODE-E2E-001 Wave 2

---

## Objective

Add smart input parsing to the browser terminal so it can detect shell commands vs natural language, route shell commands to the hivenode `/shell/exec` endpoint, and support mode switching (`/mode shell`, `/mode chat`, `/mode hybrid`).

NO LLM needed for parsing. All detection is rule-based.

---

## Smart Parsing Rules (Section 4.1)

Parse user input in this order:

1. **Starts with `!`** → force shell. Strip `!`, parse as shell command, send IR to `/shell/exec`.
2. **Starts with `/`** → slash command (already implemented in `terminalCommands.ts`).
3. **Starts with `//`** → IPC (existing behavior).
4. **Starts with `>`** → command palette mode.
5. **First token matches known shell command** → shell. Parse as IR, send to `/shell/exec`.
6. **Natural language** → route to LLM (existing behavior).
7. **Ambiguous** → route to LLM (default safe path).

---

## Known Shell Command Detection (Section 4.2)

Static set of command names. If first token (lowercased) is in this set → shell command:

```typescript
const SHELL_COMMANDS = new Set([
  // Unix
  'ls', 'cd', 'pwd', 'mkdir', 'rmdir', 'cp', 'mv', 'rm', 'cat',
  'grep', 'find', 'chmod', 'chown', 'touch', 'head', 'tail', 'wc',
  'sort', 'uniq', 'tar', 'curl', 'wget',
  // DOS
  'dir', 'copy', 'move', 'del', 'ren', 'type', 'findstr', 'cls',
  // Cross-platform tools
  'git', 'npm', 'npx', 'node', 'python', 'pip', 'pytest', 'docker',
  'ssh', 'scp',
]);
```

---

## Mode Override (Section 4.3)

Three modes, controlled by `/mode` command:

| Command | Effect |
|---------|--------|
| `/mode shell` | Everything treated as shell. `!` prefix added automatically. No LLM calls. |
| `/mode chat` | Everything treated as natural language. Shell commands sent to LLM. |
| `/mode hybrid` | Default. Smart parsing decides. |

Mode persists for the session. Resets on page reload or EGG switch.

When in shell mode, the prompt shows visual indicator (e.g., `!` prefix or shell badge).

---

## Shell Command Execution Flow

1. Parse input → detect shell command
2. Split into command + args (first token = command, rest = args)
3. POST to hivenode `/shell/exec` with:
   ```json
   {
     "command": "mkdir",
     "args": ["foo/bar"],
     "working_dir": "home://",
     "os_hint": "auto"
   }
   ```
4. Display result in terminal (stdout/stderr/exit_code)
5. If denied, show denial reason

---

## Efemera Shell Toggle (Section 4.5)

In Efemera (headless chat EGG), shell is hidden by default. EGG config controls:

```yaml
terminal:
  allow_shell: false    # Efemera default
```

When disabled:
- `!` prefix is ignored (treated as natural language)
- `/mode shell` command is not available
- Shell command detection is skipped

Read EGG config from current EGG metadata. Default to `allow_shell: true` if not specified.

---

## Files to Read First

**Browser terminal files:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\useTerminal.ts` (main input handler — `handleSubmit` function)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\TerminalPrompt.tsx` (input component)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\terminal\terminalCommands.ts` (existing slash commands)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\terminal\terminalService.ts` (sendMessage flow)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\terminal\index.ts` (exports)

**EGG config format:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\efemera.egg.md` (check for `terminal.allow_shell` setting)
- Any other EGG files to understand config format

---

## Architecture — New Files to Write

### 1. `browser/src/services/terminal/shellCommands.ts`

```typescript
export const SHELL_COMMANDS = new Set([
  // Unix
  'ls', 'cd', 'pwd', 'mkdir', 'rmdir', 'cp', 'mv', 'rm', 'cat',
  'grep', 'find', 'chmod', 'chown', 'touch', 'head', 'tail', 'wc',
  'sort', 'uniq', 'tar', 'curl', 'wget',
  // DOS
  'dir', 'copy', 'move', 'del', 'ren', 'type', 'findstr', 'cls',
  // Cross-platform tools
  'git', 'npm', 'npx', 'node', 'python', 'pip', 'pytest', 'docker',
  'ssh', 'scp',
]);

export function isShellCommand(token: string): boolean {
  return SHELL_COMMANDS.has(token.toLowerCase());
}
```

### 2. `browser/src/services/terminal/shellParser.ts`

```typescript
export type ParsedInputType = 'shell' | 'slash' | 'ipc' | 'palette' | 'chat';

export interface ParsedInput {
  type: ParsedInputType;
  command?: string;
  args?: string[];
  rawInput: string;
}

export function parseInput(input: string, mode: 'shell' | 'chat' | 'hybrid', allowShell: boolean): ParsedInput {
  // Implement the 7 parsing rules from Section 4.1
  // Return { type, command?, args?, rawInput }
}
```

**Logic:**
- If `!allowShell`, skip shell detection entirely (return `chat` for everything except slash/ipc/palette)
- If `mode === 'shell'`, prefix `!` automatically (treat everything as shell)
- If `mode === 'chat'`, skip shell detection (everything → `chat`)
- If `mode === 'hybrid'`, apply the 7 rules

### 3. `browser/src/services/terminal/shellExecutor.ts`

```typescript
export interface ShellResult {
  status: 'success' | 'error' | 'denied';
  exit_code?: number;
  stdout?: string;
  stderr?: string;
  error?: string;
  os_used?: string;
  command_executed?: string;
  duration_ms?: number;
}

export async function executeShellCommand(
  command: string,
  args: string[],
  nodeUrl: string,
  workingDir: string = 'home://'
): Promise<ShellResult> {
  // POST to nodeUrl/shell/exec with { command, args, working_dir, os_hint: 'auto' }
  // Return formatted result
  // Handle network errors, 403 (denied), 500 (execution error)
}
```

---

## Architecture — Files to Modify

### 4. `browser/src/primitives/terminal/useTerminal.ts`

**Changes:**
- Import `parseInput` from `shellParser.ts`
- Import `executeShellCommand` from `shellExecutor.ts`
- Add state: `const [mode, setMode] = useState<'shell' | 'chat' | 'hybrid'>('hybrid')`
- Read `allowShell` from current EGG config (if EGG metadata available)
- In `handleSubmit`:
  - Call `parseInput(input, mode, allowShell)`
  - If type === 'shell': call `executeShellCommand()`, display result
  - If type === 'slash': existing behavior
  - If type === 'ipc': existing behavior
  - If type === 'palette': existing behavior
  - If type === 'chat': existing LLM flow

### 5. `browser/src/services/terminal/terminalCommands.ts`

**Add `/mode` command:**

```typescript
{
  command: '/mode',
  description: 'Set terminal mode: shell, chat, or hybrid',
  execute: (args, context) => {
    const validModes = ['shell', 'chat', 'hybrid'];
    const newMode = args[0]?.toLowerCase();
    if (!validModes.includes(newMode)) {
      return `Invalid mode. Use: /mode shell | /mode chat | /mode hybrid`;
    }
    context.setMode(newMode);
    return `Terminal mode set to: ${newMode}`;
  }
}
```

Pass `setMode` callback from `useTerminal.ts` to command context.

### 6. `browser/src/services/terminal/index.ts`

**Add exports:**

```typescript
export { parseInput } from './shellParser';
export { executeShellCommand } from './shellExecutor';
export { SHELL_COMMANDS, isShellCommand } from './shellCommands';
```

---

## Test Requirements (~18 tests)

Write tests in:
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\terminal\__tests__\shellParser.test.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\terminal\__tests__\shellExecutor.test.ts`

### shellParser.test.ts (~12 tests)

1. Parse `!mkdir foo` → type: 'shell', command: 'mkdir', args: ['foo']
2. Parse `/help` → type: 'slash'
3. Parse `//pane-1` → type: 'ipc'
4. Parse `>search` → type: 'palette'
5. Parse `ls -la` → type: 'shell' (known command)
6. Parse `git status` → type: 'shell' (known command)
7. Parse `how do I deploy?` → type: 'chat' (natural language)
8. Test mode='shell': `mkdir foo` → automatically treated as shell
9. Test mode='chat': `ls` → treated as chat (not shell)
10. Test mode='hybrid': `ls` → treated as shell
11. Test allowShell=false: `!ls` → type: 'chat' (shell disabled)
12. Test allowShell=false: mode cannot be set to 'shell'

### shellExecutor.test.ts (~6 tests)

1. Mock `/shell/exec` success response → returns { status: 'success', exit_code: 0, stdout: '...' }
2. Mock `/shell/exec` error response (exit_code != 0) → returns { status: 'error', stderr: '...' }
3. Mock 403 response → returns { status: 'denied', error: '...' }
4. Mock network error → returns { status: 'error', error: 'Network unreachable' }
5. Test command + args correctly serialized in request
6. Test working_dir parameter passed correctly

Use vitest. Run with: `npx vitest run browser/src/services/terminal/__tests__/`

---

## Constraints

- No file over 500 lines.
- TDD — write tests first, then implementation.
- No stubs. Every function fully implemented.
- Browser tests use vitest.
- No CSS changes needed (all terminal rendering already exists).
- If visual indicator for shell mode is added (e.g., `!` prefix in prompt), use `var(--sd-*)` CSS variables only.

---

## Definition of Done

- [x] `shellCommands.ts` written (SHELL_COMMANDS set + isShellCommand function)
- [x] `shellParser.ts` written (parseInput function with 7 parsing rules)
- [x] `shellExecutor.ts` written (executeShellCommand function calling `/shell/exec`)
- [x] `useTerminal.ts` modified (integrate parseInput + executeShellCommand in handleSubmit)
- [x] `terminalCommands.ts` modified (add `/mode` command)
- [x] `index.ts` modified (export new modules)
- [x] 18 tests written and passing (`npx vitest run browser/src/services/terminal/__tests__/`)
- [x] EGG config `terminal.allow_shell` wired (shell disabled when false)
- [x] Mode switching works (session-persistent, resets on reload)
- [x] Shell command execution flow end-to-end (send to `/shell/exec`, display result)

---

## Response File

Write your response to:
`C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260312-TASK-029-RESPONSE.md`

Use the standard 8-section format from BOOT.md Rule 10.

---

**End of TASK-029.**
