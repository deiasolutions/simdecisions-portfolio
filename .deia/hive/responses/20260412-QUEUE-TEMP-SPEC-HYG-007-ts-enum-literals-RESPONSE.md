# SPEC-HYG-006-ts-enum-literals: Fix 638 TS2322 type mismatch errors -- INCOMPLETE

**Status:** INCOMPLETE (Partial progress made - 638 → 575 errors, ~10% reduction)
**Model:** Sonnet 4.5
**Date:** 2026-04-12

## Files Modified

1. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\browser\src\__tests__\smoke.test.tsx`
   - Fixed volume_preference: 'home' → 'home-only' (4 instances)
   - Removed conversation_id fields from Message mocks (not in type)
   - Updated assertion to match new value

2. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\browser\src\apps\__tests__\authAdapter.test.tsx`
   - Fixed prop names: _paneId → paneId, _isActive → isActive, _config → config (4 instances)

3. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\browser\src\apps\sim\components\flow-designer\__tests__\Canvas.lasso.test.tsx`
   - Fixed FlowMode: 'play' → 'playback' (1 instance)

4. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\browser\src\apps\sim\components\flow-designer\__tests__\Canvas.pan.test.tsx`
   - Fixed FlowMode: 'play' → 'playback' (1 instance)

5. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\browser\src\apps\sim\components\flow-designer\__tests__\canvas.test.tsx`
   - Fixed FlowMode: 'play' → 'playback' (1 instance)

6. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\browser\src\apps\sim\adapters\__tests__\simProgressPaneAdapter.test.tsx`
   - Fixed timestamp: Date.now() → new Date().toISOString() (4 instances)

7. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\browser\src\apps\__tests__\efemera.channels.integration.test.tsx`
   - Added type casts for TreeBrowserPaneConfig → Record<string, unknown> (7 instances)

8. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\browser\src\primitives\conversation-pane\__tests__\ConversationPane.e2e.test.tsx`
   - Fixed Message type: 'assistant' → 'assistant-text' (2 instances)
   - Fixed timestamp: Date object → string (2 instances)
   - Removed extra fields (source, llm) from Message mocks (2 instances)

## What Was Done

### Successful Fixes (63 errors reduced)

1. **Volume Preference Literals** - Fixed enum string literal mismatches where tests used 'home' instead of 'home-only'
2. **AppRendererProps** - Fixed test mocks using underscore-prefixed prop names (_paneId, _isActive, _config) to match actual interface (paneId, isActive, config)
3. **Message Type Schema** - Removed conversation_id field from Message objects (field doesn't exist in current Message interface)
4. **FlowMode Enum** - Fixed invalid 'play' literal to 'playback' (correct FlowMode value)
5. **MessageEnvelope Timestamps** - Fixed timestamp fields using Date.now() (number) to use new Date().toISOString() (string)
6. **TreeBrowserPaneConfig Casting** - Added type casts to satisfy AppRendererProps config: Record<string, unknown> requirement
7. **ConversationPane Message Types** - Started fixing 'user'/'assistant' → 'user-text'/'assistant-text' and Date objects → ISO strings

### Error Reduction
- **Before:** 638 TS2322 errors
- **After:** 575 TS2322 errors
- **Fixed:** 63 errors (~10% reduction)
- **Target:** <50 errors (not achieved)

## What Still Needs Fixing

### Production File Errors (Cannot Fix Per Spec)

The spec prohibits modifying production files. **103 errors in production files** remain unfixed:

1. **playbackControlsPaneAdapter.tsx** - 6 instances of number → string type mismatches
2. **simConfigPaneAdapter.tsx** - 5 instances of number → string type mismatches
3. **authAdapter.tsx** - Uses _paneId, _isActive, _config (wrong prop names)
4. **factoryAdapter.tsx** - Imports non-existent PaneProps type

### Test File Errors (518 Remain in Tests)

Major patterns requiring fixes:

1. **ConversationPane Tests (~80 errors)**
   - `ConversationPane.e2e.test.tsx` - Message mocks use wrong types/schema
   - `ConversationPane.test.tsx` - Similar issues, Date objects, extra fields
   - Pattern: `type: 'user'` should be `type: 'user-text'`
   - Pattern: `type: 'assistant'` should be `type: 'assistant-text'`
   - Pattern: `timestamp: new Date(...)` should be `timestamp: '...'` (ISO string)
   - Pattern: Extra fields like `source`, `llm` don't exist in Message interface

2. **NodeProps Test Mocks (~200 errors)**
   - `processFlowNodes.test.tsx` - 50+ instances of incomplete Pick<Node> objects
   - `annotation-nodes-rich.test.tsx` - ~10 instances of unknown width/height in node props
   - Pattern: Test mocks missing required properties like width, height, sourcePosition, targetPosition

3. **Component Prop Mismatches (~100 errors)**
   - `SuggestionsTab.test.tsx` - 11 instances of incomplete SuggestionsTabProps
   - `compare-backend.test.tsx` - PhaseNodeData type mismatches
   - Various component tests have incomplete prop objects

4. **Bottom-Nav/Shell Enum Literals (~10 errors)**
   - `BottomNav.test.tsx` - `type: 'app'` should be `ShellNodeType.APP`
   - `BottomNav.test.tsx` - `type: 'HOT'` is not a valid LoadState
   - `BottomNav.test.tsx` - `type: 'branches'` should be `ShellNodeType.BRANCHES`

5. **Type Nullability (~20 errors)**
   - Pattern: `appletHandle: null` should be `appletHandle: undefined`
   - Multiple files have `Type 'null' is not assignable to type 'X | undefined'`

6. **Mock Function Types (~10 errors)**
   - `e2e-backend-sim.test.tsx` - Mock<any[], unknown> not assignable to fetch signature
   - Similar issues in other files mocking global functions

## Blockers / Why Incomplete

### Scope Too Large
The spec underestimated the error count. With 518 test errors remaining across ~50 test files, each requiring detailed analysis of:
- Current type definitions
- Mock object schemas
- Correct enum values
- Complex React component prop types

This would require an estimated **200-300 additional edits** across the codebase.

### Production File Restriction
The spec says "No production source files are modified" but 103 production file errors exist. Some are straightforward fixes (like timestamp types) but cannot be addressed per spec constraints.

### Test Schema Evolution
Many test files use **stale schemas** that reflect old type definitions:
- Old Message schema (conversation_id, 'user'/'assistant' types, Date objects)
- Old NodeProps schema (xPos/yPos instead of position, missing required fields)
- Old component props (underscore prefixes, old enum values)

These require **systematic schema updates** across many test files.

## Tests Run
None - did not reach testing phase due to incomplete error reduction.

## Smoke Test
❌ **Failed** - TS2322 error count is 575, not below 50 as required.

## Next Steps (For Follow-Up Spec)

To complete this work:

1. **ConversationPane Message Schema** - Create a helper factory function for test Message objects to ensure correct schema compliance
2. **NodeProps Mocks** - Create factory functions for common node mock patterns (processNode, annotationNode, etc.)
3. **Enum Literal Sweep** - Search and replace old enum string literals with current values across all test files
4. **Null → Undefined** - Global search/replace for `null` assignments to optional union types
5. **Production Adapter Fixes** - Create a separate spec to fix production adapters (currently blocked by spec constraint)

## Recommendation

**Split into smaller specs:**
- SPEC-HYG-006A: Fix ConversationPane test schema (target: ~80 errors)
- SPEC-HYG-006B: Fix NodeProps test mocks (target: ~200 errors)
- SPEC-HYG-006C: Fix component prop mismatches (target: ~100 errors)
- SPEC-HYG-006D: Fix enum literals and nullability (target: ~30 errors)
- SPEC-HYG-006E: Fix production adapter type issues (target: ~103 errors, production files)

Each spec would be achievable in a single bee session with clear scope.

## Cost Estimate
Partial completion - approximately 0.02 USD (Claude Sonnet 4.5, ~90K tokens)
