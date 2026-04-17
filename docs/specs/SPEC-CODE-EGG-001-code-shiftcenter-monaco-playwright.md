# SPEC-CODE-EGG-001: code.shiftcenter.com — Monaco + Relay Bus + Playwright AI QA

**Date:** 2026-03-13
**Author:** Q88N (Dave) × Claude (Anthropic)
**Status:** SPEC — LOCKED
**Area:** EGG
**T-Shirt Size:** XL
**Depends On:** relay_bus (BUILT), code-editor applet (Monaco, SPECCED), prompt service (BUILT),
               log-viewer applet (SPECCED), terminal applet (BUILT), git-panel applet (SPECCED),
               SPEC-SIM-CHAT-001

---

## 1. Purpose

`code.shiftcenter.com` is the developer workspace EGG. It realizes the IDE-as-agent pattern:

- Monaco code editor emits `CODE_CHANGED` events on the relay_bus
- A subscribed agent bee evaluates, lints, tests, and generates
- Results route back to response panes in the same EGG
- Playwright integration generates and runs E2E tests with a visible headed browser
- The user watches code and live test output side by side

No competitor has a code editor wired to a governed agent loop with simulation-before-execution.
This is the developer version of the SimDecisions thesis: write code → simulate consequences
(lint, test, type-check) → decide → commit.

---

## 2. EGG Layout

Five-pane layout. The primary split is horizontal (code left, tools right). The right
column splits vertically into three zones.

```
┌─────────────────────┬──────────────────┐
│                     │  sim-chat / agent│
│   Monaco Editor     │  response pane   │
│   (code-editor)     ├──────────────────┤
│                     │  log-viewer      │
│                     │  (test output)   │
├─────────────────────┼──────────────────┤
│  file-explorer      │  terminal        │
│  (git panel)        │  (hive> prompt)  │
└─────────────────────┴──────────────────┘
```

```yaml
layout:
  type: split
  direction: horizontal
  children:
    - type: split
      direction: vertical
      ratio: 0.75
      children:
        - type: app
          appType: code-editor
          nodeId: monaco-main
          config:
            language: auto            # auto-detected from file extension
            theme: auto
            emitOnChange: true        # fires CODE_CHANGED on relay_bus
            emitDebounceMs: 800       # debounce — don't fire on every keystroke
            showMinimap: true
            wordWrap: off

        - type: app
          appType: file-explorer
          nodeId: file-tree
          config:
            rootPath: ./
            adapter: git
            showGitStatus: true

    - type: split
      direction: vertical
      ratio: 0.33
      children:
        - type: app
          appType: sim-chat
          nodeId: agent-response
          config:
            channelId: code-agent-chat
            nodeVerbosity: summary
            label: Agent

        - type: app
          appType: log-viewer
          nodeId: test-output
          config:
            source: relay_bus
            filter: "TEST_OUTPUT"
            colorCoded: true
            label: Test Output

        - type: app
          appType: terminal
          nodeId: dev-terminal
          config:
            welcomeBanner: "code.shiftcenter.com — hive>"
            zone2Dock: right
```

---

## 3. The CODE_CHANGED Feedback Loop

This is the core of the EGG. When the user edits code in Monaco:

```
User edits code in Monaco
    ↓ (800ms debounce)
CODE_CHANGED event → relay_bus
    {
      nodeId: "monaco-main",
      filePath: string,
      language: string,
      content: string,
      cursorLine: number,
      changeType: "edit" | "save" | "paste"
    }
    ↓
Agent BEE subscribes → evaluates
    ↓
BEE posts to sim-chat channel (code-agent-chat)
    - lint warnings/errors
    - type errors (if TypeScript)
    - suggested improvements
    - test suggestions
    ↓
User sees feedback inline without leaving the editor
```

The BEE is configured via the EGG's `agent` block. Default behavior:

```yaml
agent:
  model: auto
  onCodeChanged:
    - lint: true
    - typeCheck: true                 # if TypeScript
    - suggestTests: false             # opt-in — can be verbose
    - explainChanges: false           # opt-in — narrates what changed
  requireHumanOnApply: true           # BEE suggestions require approval to apply
  silenceThresholdMs: 2000            # wait 2s after last change before evaluating
```

The BEE never modifies the editor directly without user approval. It posts to sim-chat.
The user can type `apply` in the terminal to accept the last suggestion, or click the
inline diff accept button in Monaco (standard Monaco diff API).

---

## 4. Playwright AI QA Pane

The Playwright integration adds a fourth right-column pane (or floater) for visual browser
testing.

### 4.1 Architecture

```
User types in terminal: "test login flow"
    ↓
Terminal routes to agent BEE via prompt service
    ↓
BEE generates Playwright test script
    ↓
BEE posts script to sim-chat for review (REQUIRE_HUMAN)
    ↓
User approves
    ↓
Playwright runner executes in headed mode
    ↓
capture-source pane streams the browser window (screen capture via WebRTC)
    ↓
Test results stream to log-viewer (TEST_OUTPUT events on relay_bus)
    ↓
Pass/fail summary posted to sim-chat
```

### 4.2 EGG Config Addition for Playwright

```yaml
playwright:
  enabled: true
  browserVisible: true              # headed mode — user sees the browser
  captureSource: playwright-browser # nodeId of capture-source pane showing browser
  testOutputChannel: TEST_OUTPUT    # relay_bus channel for streaming results
  requireHumanOnRun: true           # generated scripts require approval before run
  screenshotOnFailure: true
  baseUrl: "{{env.DEV_BASE_URL}}"
```

### 4.3 Playwright Pane Addition to Layout

When `playwright.enabled: true`, a fifth pane appears (floater by default):

```yaml
- type: app
  appType: capture-source
  nodeId: playwright-browser
  config:
    source: playwright-window       # captures the Playwright headed browser window
    displayMode: stream             # renders the live browser stream
    label: Browser
  pin: float
  initialSize: { width: 640, height: 480 }
  initialPosition: { x: 100, y: 80 }
```

The user watches the Playwright browser execute the test script in real time.

### 4.4 Terminal Commands

```
hive> test login flow
hive> test [describe what to test in natural language]
hive> run tests
hive> run last test
hive> show test history
hive> generate tests for [component name]
hive> playwright record                  # starts Playwright record mode
```

`playwright record` starts Playwright's codegen mode — the user interacts with the browser
manually, Playwright records the actions as a test script, the BEE then cleans up and
proposes the script for approval.

---

## 5. relay_bus Events

### Emitted by Monaco (code-editor applet)

| Event | Payload | When |
|-------|---------|------|
| `CODE_CHANGED` | `{ nodeId, filePath, language, content, cursorLine, changeType }` | On edit (debounced) |
| `CODE_SAVED` | `{ nodeId, filePath }` | On explicit save (Cmd+S) |
| `CODE_FILE_OPENED` | `{ nodeId, filePath, language }` | File opened in editor |
| `CODE_SELECTION_CHANGED` | `{ nodeId, selectedText, startLine, endLine }` | Selection changes |

### Emitted by Playwright runner

| Event | Payload | When |
|-------|---------|------|
| `TEST_STARTED` | `{ testId, scriptPreview }` | Test run begins |
| `TEST_OUTPUT` | `{ testId, line, level, timestamp }` | Streaming output line |
| `TEST_SCREENSHOT` | `{ testId, imageData, step }` | Screenshot captured |
| `TEST_PASSED` | `{ testId, durationMs }` | Test passed |
| `TEST_FAILED` | `{ testId, error, screenshotPath }` | Test failed |

### Consumed by code EGG

| Event | Source | Effect |
|-------|--------|--------|
| `PROMPT_TO_PANE` | terminal / BEE response | Routes agent response to sim-chat pane |
| `CODE_SUGGESTION` | BEE | Proposed edit — shown as diff in Monaco |
| `TEST_OUTPUT` | Playwright | Streamed to log-viewer |

---

## 6. Git Panel Integration

The file-explorer pane in the lower-left uses the `git` adapter and shows:

- Modified files (git status)
- Branch name in pane header
- One-click diff (opens diff-viewer in Monaco)
- Commit from terminal: `hive> commit "message"`
- PR creation: `hive> open pr`

The git adapter is already specced in the SDK. No new work here — just EGG config wiring.

---

## 7. The IDE-as-Agent Thesis

Standard IDEs have extensions. Those extensions are isolated. They don't share a bus. They
don't log to an event ledger. They don't know about each other. They can't be governed.

code.shiftcenter.com is different:

- Every code change is a bus event — observable, loggable, governable
- The agent that evaluates your code is a BEE — its reasoning is in sim-chat, not a black
  box tooltip
- Test generation is IR-authored — the same process that governs meetings governs QA
- The Playwright browser is just another capture-source pane — same primitive as the
  meeting room's screen share
- CLOCK/COIN/CARBON on every agent evaluation — you know what your dev workflow costs

This is the dev domain (`dev.simdecisions.com`) thesis in an EGG.

---

## 8. Open Items — PARTIALLY RESOLVED

| # | Question | Decision (Q88N, 2026-03-13) |
|---|----------|-----------------------------|
| 1 | Should Playwright runner be a GC infrastructure service (reusable by any EGG) or code-EGG-specific? | **GC infrastructure service.** Other EGGs will want test running too (build queue already uses it). Not code-specific. |
| 2 | `emitOnChange: true` with 800ms debounce — right cadence? | Still open — no decision recorded. |
| 3 | `playwright record` mode — hivenode capability requirement? | Still open — no decision recorded. |
| 4 | Multi-file projects: full project context or just changed file? | Still open — no decision recorded. |

---

*Signed,*
**Q88N (Dave) × Claude (Anthropic)**
SPEC-CODE-EGG-001 — LOCKED 2026-03-13
License: CC BY 4.0 | Copyright: © 2026 DEIA Solutions
