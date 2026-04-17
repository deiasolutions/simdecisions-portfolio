# TASK-206: Event Ledger Auto-Attach for CLI Dispatches

## Objective
Auto-attach cost metadata (CLOCK, COIN, CARBON) to Event Ledger for every CLI dispatch completion, replicating the pattern used in `emit_llm_event()`.

## Context
**Current state:**
- `hivenode/llm/cost.py:emit_llm_event()` writes Event Ledger entries for terminal chat LLM calls
- Event Ledger schema (lines 40-45 in ledger/schema.py) has cost columns: cost_tokens, cost_tokens_up, cost_tokens_down, cost_usd, cost_carbon
- CLI adapter completes dispatches and returns ProcessResult with usage dict containing tokens, cost_usd, carbon_kg
- BUT: CLI dispatches do NOT write to Event Ledger

**Fix required:**
1. After CLI dispatch completes, extract usage data from ProcessResult
2. Write Event Ledger entry with event_type="CLI_DISPATCH"
3. Include cost_tokens_up (input_tokens), cost_tokens_down (output_tokens), cost_usd, cost_carbon
4. Replicate emit_llm_event() pattern

**Where to implement:**
- Option A: In dispatch.py after `result = process.send_task(...)`
- Option B: Inside ClaudeCodeProcess.send_task() after ProcessResult is created
- **Recommended:** Option B (inside send_task) because it's closer to the source and guarantees every dispatch is logged

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\llm\cost.py` (lines 60-116, emit_llm_event pattern)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\ledger\writer.py` (lines 25-96, write_event interface)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\adapters\cli\claude_cli_subprocess.py` (lines 458+, ProcessResult creation)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\dispatch\dispatch.py` (dispatcher that calls send_task)

## Deliverables

### 1. Add Ledger Writer to ClaudeCodeProcess
**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\adapters\cli\claude_cli_subprocess.py`

**Changes:**
1. Import ledger writer:
   ```python
   from hivenode.ledger.writer import LedgerWriter
   ```

2. Add ledger_writer parameter to `__init__()`:
   ```python
   def __init__(
       self,
       work_dir: Path,
       ...
       heartbeat_callback: Optional[Any] = None,
       ledger_writer: Optional[LedgerWriter] = None,  # NEW
   ):
       ...
       self.ledger_writer = ledger_writer
   ```

3. After ProcessResult is created (line ~458), if ledger_writer exists and usage is not None, write event:
   ```python
   # Auto-attach cost to Event Ledger
   if self.ledger_writer and usage:
       try:
           self.ledger_writer.write_event(
               event_type="CLI_DISPATCH",
               actor="system:hivenode",
               target=None,
               domain="cli",
               signal_type="internal",
               payload_json={
                   "model": usage.get("model", ""),
                   "duration_ms": usage.get("duration_ms", 0),
                   "num_turns": usage.get("num_turns", 0),
                   "session_id": usage.get("session_id", ""),
               },
               cost_tokens=usage.get("input_tokens", 0) + usage.get("output_tokens", 0),
               cost_tokens_up=usage.get("input_tokens", 0),
               cost_tokens_down=usage.get("output_tokens", 0),
               cost_usd=usage.get("cost_usd", 0.0),
               cost_carbon=usage.get("carbon_kg", 0.0),
           )
       except Exception as e:
           logger.warning(f"Failed to write CLI_DISPATCH event to ledger: {e}")
   ```

### 2. Update Dispatch Script to Pass Ledger Writer
**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\dispatch\dispatch.py`

**Changes:**
1. Import ledger writer:
   ```python
   from hivenode.ledger.writer import LedgerWriter
   ```

2. Create ledger writer instance (before creating ClaudeCodeProcess):
   ```python
   ledger_db_path = Path.home() / ".deia" / "ledger.db"
   ledger_writer = LedgerWriter(str(ledger_db_path))
   ```

3. Pass to ClaudeCodeProcess constructor:
   ```python
   process = ClaudeCodeProcess(
       work_dir=repo_root,
       ...
       ledger_writer=ledger_writer,  # NEW
   )
   ```

4. Close ledger writer after dispatch completes:
   ```python
   try:
       result = process.send_task(...)
   finally:
       ledger_writer.close()
   ```

### 3. Verify Ledger Entry After Dispatch
**Manual verification step:**
1. Run a test dispatch
2. Query Event Ledger: `SELECT * FROM events WHERE event_type='CLI_DISPATCH' ORDER BY id DESC LIMIT 1`
3. Verify columns populated: cost_tokens_up, cost_tokens_down, cost_usd, cost_carbon

## Test Requirements

**Test file:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\adapters\cli\test_ledger_auto_attach.py`

Minimum 4 tests (TDD — write tests first):

1. `test_cli_dispatch_writes_ledger_entry()` — Mock dispatch with usage data, verify Event Ledger contains CLI_DISPATCH entry
2. `test_ledger_entry_cost_fields()` — Verify Event Ledger entry has cost_tokens_up, cost_tokens_down, cost_usd, cost_carbon matching usage dict
3. `test_ledger_entry_payload_json()` — Verify payload_json contains model, duration_ms, num_turns, session_id
4. `test_no_ledger_writer_no_crash()` — If ledger_writer=None, dispatch completes without error (no Event Ledger write)

**Integration test:**
5. `test_e2e_dispatch_ledger_auto_attach()` — Run real dispatch (simple task), verify Event Ledger contains entry with non-zero cost_usd

## Constraints
- No file over 500 lines
- No stubs — all functions fully implemented
- Event Ledger write must be try/except wrapped (don't crash dispatch on ledger failure)
- Ledger writer must be closed in finally block
- If usage is None or empty, skip ledger write (don't write 0-cost entries)

## Acceptance Criteria
- [ ] ClaudeCodeProcess.__init__() accepts ledger_writer parameter
- [ ] ProcessResult creation auto-writes Event Ledger entry if ledger_writer exists and usage is not None
- [ ] Dispatch script creates LedgerWriter and passes to ClaudeCodeProcess
- [ ] Dispatch script closes ledger_writer in finally block
- [ ] 4+ tests pass
- [ ] Event Ledger query shows CLI_DISPATCH entry with cost_usd, cost_carbon, cost_tokens_up, cost_tokens_down

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260316-TASK-206-RESPONSE.md`

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
