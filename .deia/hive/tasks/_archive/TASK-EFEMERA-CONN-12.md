# TASK-EFEMERA-CONN-12: Port Command System

**Priority:** P2
**Depends on:** CONN-11
**Blocks:** None
**Model:** Haiku
**Role:** Bee

## Objective

Port the slash command system from platform to hivenode. Messages starting with `/` are intercepted and routed to command handlers instead of being saved as regular messages.

## Read First

- `.deia/BOOT.md` — hard rules
- Platform source:
  - `C:\Users\davee\OneDrive\Documents\GitHub\platform\platform\efemera\src\efemera\commands\router.py` (39 lines)
  - `C:\Users\davee\OneDrive\Documents\GitHub\platform\platform\efemera\src\efemera\commands\parser.py` (57 lines)
  - `C:\Users\davee\OneDrive\Documents\GitHub\platform\platform\efemera\src\efemera\commands\status_commands.py` (207 lines)
- `hivenode/efemera/routes.py` — message creation endpoint (intercept point)
- `.deia/hive/responses/20260328-EFEMERA-ASSESSMENT.md` — section 1.7

## Files to Create

### 1. `hivenode/efemera/commands/__init__.py`

Empty init.

### 2. `hivenode/efemera/commands/parser.py` (~57 lines)

Port from platform. Parses `/command arg1 --flag value` syntax.

```python
from dataclasses import dataclass, field
from typing import List, Dict, Optional

@dataclass
class ParsedCommand:
    name: str
    args: List[str] = field(default_factory=list)
    flags: Dict[str, str] = field(default_factory=dict)
    raw: str = ""

def parse_command(text: str) -> Optional[ParsedCommand]:
    """Parse a slash command from message text. Returns None if not a command."""
    text = text.strip()
    if not text.startswith("/"):
        return None

    parts = text[1:].split()
    if not parts:
        return None

    name = parts[0].lower()
    args = []
    flags = {}

    i = 1
    while i < len(parts):
        if parts[i].startswith("--"):
            flag_name = parts[i][2:]
            if i + 1 < len(parts) and not parts[i + 1].startswith("--"):
                flags[flag_name] = parts[i + 1]
                i += 2
            else:
                flags[flag_name] = "true"
                i += 1
        else:
            args.append(parts[i])
            i += 1

    return ParsedCommand(name=name, args=args, flags=flags, raw=text)
```

### 3. `hivenode/efemera/commands/router.py` (~40 lines)

Port from platform. Registry pattern for command handlers.

```python
from typing import Callable, Dict, Optional
from hivenode.efemera.commands.parser import ParsedCommand

CommandHandler = Callable[[ParsedCommand, dict], dict]  # (command, context) -> response

_registry: Dict[str, CommandHandler] = {}

def register_command(name: str, handler: CommandHandler) -> None:
    _registry[name.lower()] = handler

def route_command(command: ParsedCommand, context: dict) -> Optional[dict]:
    handler = _registry.get(command.name)
    if not handler:
        return {"error": f"Unknown command: /{command.name}", "available": list(_registry.keys())}
    return handler(command, context)

def get_registered_commands() -> list:
    return sorted(_registry.keys())
```

### 4. `hivenode/efemera/commands/status_commands.py` (~150 lines)

Port from platform's `status_commands.py`. Adapt to our store and hivenode APIs.

```python
from hivenode.efemera.commands.router import register_command
from hivenode.efemera.commands.parser import ParsedCommand

def cmd_status(command: ParsedCommand, context: dict) -> dict:
    """/status — Show system status."""
    store = context.get("store")
    channels = store.list_channels() if store else []
    return {
        "content": f"**Status:** Online\n**Channels:** {len(channels)}",
        "author_name": "System",
        "author_type": "system",
        "message_type": "system",
    }

def cmd_help(command: ParsedCommand, context: dict) -> dict:
    """/help — List available commands."""
    from hivenode.efemera.commands.router import get_registered_commands
    cmds = get_registered_commands()
    lines = [f"- `/{c}`" for c in cmds]
    return {
        "content": f"**Available commands:**\n" + "\n".join(lines),
        "author_name": "System",
        "author_type": "system",
        "message_type": "system",
    }

def cmd_members(command: ParsedCommand, context: dict) -> dict:
    """/members — List members of current channel."""
    store = context.get("store")
    channel_id = context.get("channel_id")
    if not channel_id or not store:
        return {"content": "No channel selected.", "author_name": "System"}
    members = store.list_members(channel_id)
    lines = [f"- {m['username']} ({m['role']}) — {m.get('status', 'unknown')}" for m in members]
    return {
        "content": f"**Members ({len(members)}):**\n" + "\n".join(lines),
        "author_name": "System",
        "author_type": "system",
    }

# Register all commands
def register_all():
    register_command("status", cmd_status)
    register_command("help", cmd_help)
    register_command("members", cmd_members)
```

### Integration with Message Creation

**Update `routes.py` `create_message` endpoint:**

```python
from hivenode.efemera.commands.parser import parse_command
from hivenode.efemera.commands.router import route_command

@router.post("/channels/{channel_id}/messages", status_code=201)
async def create_message(channel_id: str, req: CreateMessageRequest):
    store = _get_store()

    # Check for slash command
    command = parse_command(req.content)
    if command:
        context = {"store": store, "channel_id": channel_id, "user_id": req.author_id}
        result = route_command(command, context)
        if result:
            # Save command response as a system message
            return store.create_message(
                channel_id=channel_id,
                author_id="system",
                author_name=result.get("author_name", "System"),
                content=result.get("content", ""),
                author_type=result.get("author_type", "system"),
                message_type=result.get("message_type", "system"),
            )

    # Normal message flow (moderation + save)
    ...
```

**Register commands on startup:** Call `register_all()` in the store init or route setup.

## Tests to Create

### `tests/hivenode/test_efemera_commands.py`
- parse_command: `/status` → name="status", no args
- parse_command: `/search hello world` → name="search", args=["hello", "world"]
- parse_command: `/log --days 7` → name="log", flags={"days": "7"}
- parse_command: regular text returns None
- parse_command: empty `/` returns None
- route_command: registered command returns handler result
- route_command: unknown command returns error with available list
- cmd_status: returns channel count
- cmd_help: returns list of registered commands
- cmd_members: returns member list for channel
- Integration: `/status` message creates system response, not regular message

## Constraints

- Port from platform code — adapt to SQLite store
- Commands are synchronous (no async handlers needed)
- Command responses are saved as system messages in the channel
- If commands module is not importable, messages pass through normally
- No file exceeds 500 lines
- TDD: write tests first
