# PRISM-IR: Primitive Invocation Schema for Mobile IR

**Version:** 1.0
**Schema:** `mobile/v1`
**Last Updated:** 2026-04-06

## Overview

PRISM-IR (Primitive Invocation Schema for Mobile IR) is the intermediate representation that bridges natural language commands to executable actions in the Mobile Workdesk. It provides a formal, validated structure for command interpretation and routing.

## Architecture

```
User Input (voice/text)
        ↓
Command Interpreter (parser + fuzzy matching)
        ↓
PRISM-IR (structured JSON)
        ↓
Validation (schema check)
        ↓
Execution Layer (primitive invocation)
```

## Schema

### Required Fields

- **`command`** (string): The action verb to execute
  - Examples: `"open"`, `"close"`, `"navigate"`, `"search"`, `"toggle"`
  - Min length: 1, Max length: 50

- **`confidence`** (number): Confidence score from the interpreter
  - Range: `0.0` (no confidence) to `1.0` (certain)
  - Used to trigger confirmation prompts for low-confidence commands

### Optional Fields

- **`target`** (string): The object or primitive the command operates on
  - Examples: `"terminal"`, `"file"`, `"pane"`, `"notification"`
  - Max length: 100

- **`arguments`** (object): Key-value parameters for command execution
  - Example: `{ "filename": "test.py", "mode": "readonly" }`

- **`alternatives`** (array): Alternative interpretations for ambiguous input
  - Each alternative has: `command`, `confidence`, optional `target`/`arguments`/`reason`
  - Used when confidence is below threshold (typically < 0.75)

- **`raw_input`** (string): Original user input that generated this IR
  - Useful for debugging and telemetry

- **`timestamp`** (string): ISO 8601 timestamp when command was parsed
  - Example: `"2026-04-06T12:00:00Z"`

- **`metadata`** (object): Additional metadata for debugging/telemetry
  - `parser_version`: Version of the command interpreter
  - `input_method`: How the command was entered (`"voice"`, `"text"`, `"gesture"`, `"shortcut"`)
  - `session_id`: Session identifier for tracking

## Command Dictionary

### Categories

1. **Navigation**: `open`, `close`, `navigate`, `back`, `home`, `switch`
2. **Execution**: `execute`, `run`, `cancel`, `retry`, `pause`, `resume`
3. **Search**: `search`, `find`, `filter`, `grep`
4. **State**: `toggle`, `enable`, `disable`, `show`, `hide`
5. **Data**: `save`, `load`, `export`, `import`, `copy`, `paste`
6. **Voice**: `listen`, `stop-listening`
7. **Help**: `help`, `info`

See `hivenode/prism/mobile_commands.yml` for the complete command dictionary with 37 commands.

## Examples

### Minimal Valid IR

```json
{
  "command": "open",
  "confidence": 0.95
}
```

### Full IR with All Fields

```json
{
  "command": "open",
  "target": "terminal",
  "arguments": {
    "filename": "test.py"
  },
  "confidence": 0.95,
  "alternatives": [
    {
      "command": "navigate",
      "target": "terminal",
      "confidence": 0.85,
      "reason": "Similar phonetics between 'open' and 'navigate'"
    }
  ],
  "raw_input": "open terminal",
  "timestamp": "2026-04-06T12:00:00Z",
  "metadata": {
    "parser_version": "1.0",
    "input_method": "voice",
    "session_id": "abc-123"
  }
}
```

### Low-Confidence IR with Alternatives

```json
{
  "command": "search",
  "target": "file",
  "confidence": 0.65,
  "alternatives": [
    {
      "command": "find",
      "target": "file",
      "confidence": 0.55
    },
    {
      "command": "grep",
      "target": "logs",
      "confidence": 0.45
    }
  ],
  "raw_input": "ferch my file"
}
```

## Validation

### Python Validator

```python
from hivenode.prism.ir_validator import validate_ir

ir = {"command": "open", "target": "terminal", "confidence": 0.95}
result = validate_ir(ir)

if result.valid:
    print("Valid IR")
else:
    print("Errors:", result.errors)
```

### TypeScript Validator

```typescript
import { validateIR } from '@/services/prism/irValidator';

const ir = { command: 'open', target: 'terminal', confidence: 0.95 };

if (validateIR(ir)) {
  console.log('Valid IR');
} else {
  console.log('Invalid IR');
}
```

### React Hook

```typescript
import { useIRValidator } from '@/services/prism/useIRValidator';

function MyComponent() {
  const { validate, validateWithErrors, lastResult } = useIRValidator();

  const handleCommand = (ir: unknown) => {
    const result = validateWithErrors(ir);
    if (!result.valid) {
      console.error('Validation errors:', result.errors);
      return;
    }
    // Execute command
  };
}
```

### Backend API

```bash
# Validate IR via REST API
curl -X POST http://localhost:8420/api/prism/validate \
  -H "Content-Type: application/json" \
  -d '{
    "ir": {
      "command": "open",
      "target": "terminal",
      "confidence": 0.95
    }
  }'

# Response
{
  "valid": true,
  "errors": [],
  "warnings": []
}
```

## Confidence Thresholds

| Range | Action |
|-------|--------|
| 0.85 - 1.0 | Execute immediately |
| 0.70 - 0.84 | Execute with confirmation |
| 0.50 - 0.69 | Show alternatives, ask user to choose |
| 0.0 - 0.49 | Show "command not understood" error |

## Error Handling

### Common Validation Errors

- **Missing required field**: `"Missing required field 'command'"`
- **Wrong type**: `"Field 'command' must be a string"`
- **Out of range**: `"Field 'confidence' must be between 0.0 and 1.0"`
- **Extra properties**: `"Additional property 'unknown_field' not allowed"`

### Semantic Warnings

- **Low confidence**: `"Confidence below 0.5 may indicate ambiguous input"`
- **Unusual alternatives**: `"High confidence with alternatives present is unusual"`

## Files

- **Schema**: `hivenode/prism/mobile_ir_schema.json`
- **Command Dictionary**: `hivenode/prism/mobile_commands.yml`
- **Python Validator**: `hivenode/prism/ir_validator.py`
- **TypeScript Validator**: `browser/src/services/prism/irValidator.ts`
- **React Hook**: `browser/src/services/prism/useIRValidator.ts`
- **Backend Routes**: `hivenode/routes/prism_routes.py`
- **Tests**:
  - `tests/hivenode/prism/test_ir_validator.py` (17 tests)
  - `browser/src/services/prism/irValidator.test.ts` (17 tests)

## Integration

### Command Interpreter Flow

1. **Parse**: Natural language → PRISM-IR
2. **Validate**: Check against schema
3. **Confidence Check**: Determine if confirmation needed
4. **Route**: Send to appropriate primitive
5. **Execute**: Invoke primitive action

### Bus Events

PRISM-IR commands are routed via the RTD bus:

```typescript
bus.send({
  type: 'command:execute',
  target: '*',
  data: {
    ir: prismIR,
    timestamp: new Date().toISOString()
  }
});
```

## Version History

- **v1.0 (2026-04-06)**: Initial release
  - 37 commands across 7 categories
  - Python and TypeScript validators
  - Backend REST API
  - React hook for frontend
  - Full test coverage (34 tests total)
