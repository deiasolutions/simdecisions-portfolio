# SPEC-EFEMERA-CONN-12: Port Command System

> **Project:** Efemera Connector (12 specs submitted as batch, 2026-03-28)
> Dependencies between specs ensure correct execution order.
> Design doc: `.deia/hive/responses/20260328-EFEMERA-CONNECTOR-DESIGN.md`

## Priority
P2

## Depends On
- SPEC-EFEMERA-CONN-11-moderation-pipeline (commands intercept BEFORE moderation in create_message)

## Model Assignment
haiku

## Objective

Port the slash command system from platform to hivenode. Messages starting with `/` are intercepted and routed to command handlers instead of being saved as regular messages. Commands intercept BEFORE moderation — if the user types `/status`, it never hits the moderation scanner.

## Read First

- `.deia/BOOT.md` — hard rules
- Platform source:
  - `C:\Users\davee\OneDrive\Documents\GitHub\platform\platform\efemera\src\efemera\commands\router.py` (39 lines)
  - `C:\Users\davee\OneDrive\Documents\GitHub\platform\platform\efemera\src\efemera\commands\parser.py` (57 lines)
  - `C:\Users\davee\OneDrive\Documents\GitHub\platform\platform\efemera\src\efemera\commands\status_commands.py` (207 lines)
- `hivenode/efemera/routes.py` — message creation endpoint (intercept point, after CONN-11 moderation)
- `.deia/hive/responses/20260328-EFEMERA-ASSESSMENT.md` — section 1.7

## Files to Create

### 1. `hivenode/efemera/commands/__init__.py`
Empty init.

### 2. `hivenode/efemera/commands/parser.py` (~57 lines)
Port from platform. Parses `/command arg1 --flag value` syntax.

```python
@dataclass
class ParsedCommand:
    name: str
    args: List[str] = field(default_factory=list)
    flags: Dict[str, str] = field(default_factory=dict)
    raw: str = ""

def parse_command(text: str) -> Optional[ParsedCommand]:
    """Parse a slash command from message text. Returns None if not a command."""
```

### 3. `hivenode/efemera/commands/router.py` (~40 lines)
Registry pattern for command handlers.

```python
CommandHandler = Callable[[ParsedCommand, dict], dict]
_registry: Dict[str, CommandHandler] = {}

def register_command(name: str, handler: CommandHandler) -> None
def route_command(command: ParsedCommand, context: dict) -> Optional[dict]
def get_registered_commands() -> list
```

### 4. `hivenode/efemera/commands/status_commands.py` (~150 lines)
Port from platform. Adapt to our store.

```python
def cmd_status(command, context) -> dict:  # /status
def cmd_help(command, context) -> dict:    # /help
def cmd_members(command, context) -> dict: # /members

def register_all():
    register_command("status", cmd_status)
    register_command("help", cmd_help)
    register_command("members", cmd_members)
```

### Integration with create_message

Add command intercept BEFORE the moderation pipeline (CONN-11) in `routes.py`:
```python
# Check for slash command FIRST
command = parse_command(req.content)
if command:
    context = {"store": store, "channel_id": channel_id, "user_id": req.author_id}
    result = route_command(command, context)
    if result:
        return store.create_message(
            channel_id=channel_id, author_id="system",
            author_name=result.get("author_name", "System"),
            content=result.get("content", ""),
            author_type="system", message_type="system",
        )

# THEN run moderation pipeline (from CONN-11)
scan = run_pipeline(req.content)
...
```

## Acceptance Criteria
- [ ] parse_command: `/status` -> name="status", no args
- [ ] parse_command: `/search hello world` -> name="search", args=["hello", "world"]
- [ ] parse_command: `/log --days 7` -> name="log", flags={"days": "7"}
- [ ] parse_command: regular text returns None
- [ ] parse_command: empty `/` returns None
- [ ] route_command: registered command returns handler result
- [ ] route_command: unknown command returns error with available list
- [ ] cmd_status: returns channel count
- [ ] cmd_help: returns list of registered commands
- [ ] cmd_members: returns member list for channel
- [ ] Integration: `/status` message creates system response, not regular message
- [ ] Integration: commands intercept BEFORE moderation pipeline
- [ ] All tests pass

## Smoke Test
- [ ] `cd hivenode && python -m pytest tests/hivenode/test_efemera_commands.py -v` — all pass
- [ ] `cd hivenode && python -m pytest tests/ -v` — no regressions

## Constraints
- Port from platform code — adapt to SQLite store
- Commands are synchronous (no async handlers needed)
- Command responses are saved as system messages in the channel
- If commands module is not importable, messages pass through normally
- No file exceeds 500 lines
- TDD: write tests first

## Response File
20260328-EFEMERA-CONN-12-RESPONSE.md
