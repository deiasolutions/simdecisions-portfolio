# SPEC-INJECT-01: Model-Specific Prompt Injection

**Priority:** P2
**Complexity:** Haiku
**Estimate:** 1 hour
**Dependencies:** None

---

## Problem

Claude Code exhibits behavior patterns that waste dispatch cycles:
- Premature action without confirmation (edits before "go")
- Wrong diagnostic paths / red herring chasing
- Fixing adjacent issues instead of the requested bug
- Scope creep into unrelated files

These are CC-specific behaviors. Other models (Gemini, OpenAI) may have different failure modes. We need model-specific prompt shims without changing core PROCESS-13.

## Solution

Add an injection loader to `dispatch.py` that prepends model-specific guardrails to the task content before `send_task()`. Same pattern as CLI adapters — shim per model, not core process change.

---

## Implementation

### 1. Create Injection Directory

```
.deia/config/injections/
├── base.md               # shared across all models
├── claude_code.md        # CC-specific guardrails
└── openai.md             # placeholder for future
```

### 2. Add Injection Loader to dispatch.py

Add this function after the imports, before `dispatch_bee()`:

```python
INJECTIONS_DIR = Path(".deia/config/injections")

def load_injection(model: str) -> str:
    """Load base + model-specific injection content.
    
    Returns concatenated markdown from base.md + model-specific file.
    Missing files return empty string (no injection, no error).
    """
    parts = []
    
    # Always load base if exists
    base_path = INJECTIONS_DIR / "base.md"
    if base_path.exists():
        parts.append(base_path.read_text(encoding="utf-8").strip())
    
    # Map model to injection file
    model_map = {
        "sonnet": "claude_code.md",
        "haiku": "claude_code.md",
        "opus": "claude_code.md",
        "gpt-4": "openai.md",
        "gpt-4o": "openai.md",
        "gemini": "gemini.md",
        "gemini-2.5-flash": "gemini.md",
    }
    
    injection_file = model_map.get(model.lower())
    if injection_file:
        path = INJECTIONS_DIR / injection_file
        if path.exists():
            parts.append(path.read_text(encoding="utf-8").strip())
    
    return "\n\n".join(parts)
```

### 3. Integrate in dispatch_bee()

In `dispatch_bee()`, after MCP telemetry injection (~line 592) and before `adapter.send_task()` (~line 626), add:

```python
# Model-specific prompt injection
injection = load_injection(model)
if injection:
    task_content = f"{injection}\n\n---\n\n{task_content}"
```

### 4. Create Injection Files

**`.deia/config/injections/base.md`**

```markdown
# HIVE DISPATCH PROTOCOL

You are a worker bee in the DEIA hive system. You have been dispatched to complete a specific task.

## ABSOLUTE RULES

- Complete ONLY the task in your task file
- Do NOT modify files outside your assigned scope
- All file paths must be absolute — never relative
- If blocked, emit a blocker report to your response file — do not hang waiting
- Report completion with files modified and tests run
```

**`.deia/config/injections/claude_code.md`**

```markdown
# CLAUDE CODE BEHAVIOR OVERRIDES

## STOP BEFORE ACTING

- Present your plan in numbered steps BEFORE any file edit
- Wait for explicit "go" — silence is not consent
- If unsure whether to proceed, ASK

## SCOPE LOCK

- Fix ONLY what was requested in the task file
- Do NOT fix adjacent test failures you notice
- Do NOT refactor nearby code "while you're in there"
- If you see something else broken, REPORT it in your response — do not fix it

## PATH DISCIPLINE

- All file paths must be absolute
- Never use relative paths
- Verify file exists before editing

## NO RABBIT HOLES

- State your top 2 hypotheses before investigating
- If first hypothesis fails, STOP and report before trying second
- Maximum 2 fix attempts before reporting blocker
- Do NOT chase red herrings

## TERMINOLOGY (NON-NEGOTIABLE)

- Terminal = INPUT ONLY (hive> prompt)
- Text-pane = OUTPUT display
- EGG = app unit with .set.md config
- Chrome = shell UI (menu, sidebar) — NEVER in ALWAYS_REGISTERED
- Set = collection of EGGs on the Stage
```

---

## Files to Modify

| File | Change |
|------|--------|
| `.deia/hive/scripts/dispatch/dispatch.py` | Add `load_injection()` function (~25 lines), add injection call in `dispatch_bee()` (~3 lines) |
| `.deia/config/injections/base.md` | Create new file |
| `.deia/config/injections/claude_code.md` | Create new file |

## Files to Read First

- `.deia/hive/scripts/dispatch/dispatch.py`

---

## Acceptance Criteria

- [ ] `load_injection("sonnet")` returns base.md + claude_code.md concatenated
- [ ] `load_injection("unknown-model")` returns base.md only (no error)
- [ ] `load_injection("sonnet")` with missing files returns empty string (no error)
- [ ] Dispatched bees receive the injection prepended to their task content
- [ ] Injection appears before the task file content, separated by `---`
- [ ] No changes to PROCESS-13, queue runner, or scheduler

## Tests

Add to existing dispatch tests:

```python
def test_load_injection_known_model():
    """Known model returns base + model-specific content."""
    result = load_injection("sonnet")
    assert "HIVE DISPATCH PROTOCOL" in result
    assert "CLAUDE CODE BEHAVIOR OVERRIDES" in result

def test_load_injection_unknown_model():
    """Unknown model returns base only."""
    result = load_injection("unknown-model-xyz")
    assert "HIVE DISPATCH PROTOCOL" in result
    assert "CLAUDE CODE" not in result

def test_load_injection_missing_files():
    """Missing injection files return empty string, no error."""
    # Temporarily rename injections dir
    # Assert empty string returned
    # Restore dir
```

---

## Rationale

This follows the same pattern as CLI adapters (`hivenode/adapters/cli/claude_cli_subprocess.py`) — model-specific behavior in a shim layer, not core process changes. The injection files are plain markdown, editable without code changes. Adding a new model's guardrails = add one .md file + one entry in `model_map`.

We do NOT change:
- PROCESS-13 gates
- Queue runner behavior  
- Scheduler logic
- Task file format
- Response file format

We DO add:
- Behavioral guardrails that address CC's specific failure modes
- Extensibility for other models' quirks (Gemini verbosity, OpenAI formatting, etc.)
