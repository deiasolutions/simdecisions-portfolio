# Terminal Primitive Test Suite

This directory contains comprehensive tests for the ShiftCenter terminal primitive, ported from the simdecisions-2 project.

## Test Files

### 1. terminalCommands.test.ts (16 tests)
Tests for core slash commands:
- `/clear` - Reset terminal and create new conversation
- `/help` - Show command list
- `/ledger` - Display session totals
- `/history` - List conversations with resume codes
- `/save` - Show current resume code
- `/resume <code>` - Resume conversation by code
- `/pane <nickname>` - Set pane nickname (pane mode only)
- Navigation command routing to terminalCommands.nav.ts

### 2. terminalCommands.telemetry.test.ts (8 tests)
Tests for `/telemetry` command:
- View current telemetry tier (0, 1, 2)
- Set telemetry tier
- Delete telemetry data
- Export telemetry (stub)
- Error handling for invalid tiers

### 3. TerminalOutput.test.tsx (10 tests)
Tests for TerminalOutput component:
- Renders banner entries
- Renders input entries with prompt
- Renders response entries with metrics
- Renders system messages
- Renders IR entries with action buttons
- Displays loading spinner
- Handles multiple entries
- Auto-scroll behavior
- Empty state handling

### 4. TerminalPrompt.test.tsx (8 tests)
Tests for TerminalPrompt component:
- Renders input field
- Displays current input value
- Handles typing via setInput
- Submits on Enter key
- Disables input when loading
- Prevents submission when loading
- Auto-focus on mount
- Renders prompt prefix

### 5. TerminalResponsePane.test.tsx (8 tests)
Tests for TerminalResponsePane component:
- Renders response content
- Handles null/empty responses
- Close button functionality
- Multiline response rendering
- Whitespace preservation
- Long content handling

### 6. TerminalStatusBar.test.tsx (8 tests)
Tests for TerminalStatusBar component:
- Renders all three currency totals (time, cost, carbon)
- Zero value handling
- Large time value formatting
- Currency formatting (2 decimal places)
- Carbon formatting (1 decimal place)
- Message count display
- Singular/plural message count

### 7. TerminalStatusBar.currencies.test.tsx (5 tests)
Tests for currency filtering logic:
- All currencies displayed by default
- Currency icons (time, money, carbon)
- Correct display order

### 8. TerminalApp.paneNav.test.tsx (7 tests)
Tests for pane navigation behavior:
- Navigation suppression in pane mode
- Normal navigation in standalone mode
- Pane nickname management via `/pane` command
- IR routing to designer pane
- Pane-only command restrictions
- Cross-pane state preservation

### 9. irRouting.test.ts (5 tests)
Tests for IR routing logic:
- Valid IR identification
- Invalid IR rejection
- Null/undefined handling
- Bus-based routing to designer pane
- Graceful handling when bus unavailable

### 10. useTerminal.test.ts (15 tests - existing)
Tests for useTerminal hook:
- Initialization with banner
- Message sending via terminal service
- Command handling
- Ledger accumulation
- LocalStorage persistence
- Conversation management
- Error handling
- Loading states

## Test Architecture

### Mocking Strategy
All tests use consistent mocking:
- `../../../services/terminal` - Mocked for API calls
- `../terminalCommands.nav` - Mocked for navigation commands
- `localStorage` - Cleared before each test

### Test Patterns
1. **Component Tests**: Use `@testing-library/react` for rendering and interaction
2. **Command Tests**: Direct function calls with mocked context
3. **Hook Tests**: Use `renderHook` from `@testing-library/react`

### Key Testing Principles
- No stub tests - all tests verify real behavior
- Proper mocking of external dependencies
- Consistent test structure across files
- Clear test descriptions
- Comprehensive coverage of edge cases

## Running Tests

Run all terminal primitive tests:
```bash
npm test -- src/primitives/terminal/__tests__/
```

Run specific test file:
```bash
npm test -- __tests__/terminalCommands.test.ts
```

Run with coverage:
```bash
npm test -- --coverage src/primitives/terminal/
```

## Total Coverage
- **Total Test Files**: 10
- **Total Tests**: 90+
- **Commands Tested**: All 13 slash commands
- **Components Tested**: All 5 terminal components
- **Utilities Tested**: IR routing, command dispatcher

## Migration Notes
All tests ported from `simdecisions-2` project with the following updates:
- Updated import paths for `browser/src/primitives/terminal/` structure
- Maintained vitest + @testing-library/react test framework
- Preserved all mocking strategies and test patterns
- Ensured compatibility with new terminal primitive architecture
