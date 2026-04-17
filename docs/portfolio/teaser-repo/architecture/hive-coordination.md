# DEIA Hive: Constitutional AI Governance

**System:** Multi-agent development orchestration
**Roles:** 4 (Q88N, Q33NR, Q33N, BEE)
**Governance:** Constitutional (10 hard rules)
**Evidence:** 1,358 specs completed, 98.7% autonomous completion
**Date:** April 2026

---

## Chain of Command

```
Q88N (Dave, human sovereign)
  ↓ sets direction
Q33NR (Queen Regent — live session with Dave)
  ↓ writes briefing, dispatches Q33N
Q33N (Queen — headless coordinator)
  ↓ writes task files, dispatches bees after Q33NR approval
BEEs (workers — headless)
  ↓ write code, run tests, write response files
Results flow UP: BEE → Q33N → Q33NR → Q88N
```

**No shortcuts. No skipping levels.**

- Q33NR never talks to bees directly
- Bees never talk to Q88N directly
- Q33N never talks to Q88N directly

---

## Role Definitions

### Q88N: Human Sovereign

**Who:** Dave (human developer)
**Job:** Sets direction, approves specs, makes final decisions
**Does NOT:** Write code (unless necessary for unblocking)
**Authority:** All decisions flow through Q88N. No agent can override.

**Typical workflow:**

1. Q88N identifies work (bug report, feature request, refactor need)
2. Q88N tells Q33NR: "We need X"
3. Q33NR writes briefing, dispatches Q33N
4. Q88N reviews results from Q33NR
5. Q88N approves/rejects/requests changes

---

### Q33NR: Queen Regent

**Who:** Claude Opus/Sonnet in live session with Q88N
**Job:** Regent role — manages Q33N, reviews work, reports to Q88N
**Does NOT:** Write code, write task files, dispatch bees directly

**Workflow:**

**Step 1: Receive direction from Q88N**

Q88N: "We need Export/Import buttons in the canvas toolbar"

**Step 2: Write briefing for Q33N**

File: `.deia/hive/coordination/2026-04-16-BRIEFING-export-import-buttons.md`

Contents:

```markdown
# Briefing: Export/Import Buttons for Canvas Toolbar

**To:** Q33N
**From:** Q33NR
**Date:** 2026-04-16
**Model:** sonnet

## Objective
Add Export and Import buttons to the canvas toolbar, next to zoom controls.

## Context
Currently the toolbar has zoom controls but no way to export/import scenarios.
Users have requested this feature for saving/loading work.

## Relevant Files
- browser/src/components/toolbar/Toolbar.tsx (existing toolbar)
- browser/src/stores/uiStore.ts (UI state management)
- browser/src/components/dialogs/ (dialog components)

## Constraints
- No hardcoded colors (use var(--sd-*))
- No file over 500 lines
- TDD required
- Must use Lucide icons (Download, Upload)

## Success Criteria
- Export button appears in toolbar
- Import button appears in toolbar
- Clicking Export opens export dialog
- Clicking Import opens import dialog
- All tests pass
```

**Step 3: Dispatch Q33N**

```bash
python .deia/hive/scripts/dispatch/dispatch.py \
  .deia/hive/coordination/2026-04-16-BRIEFING-export-import-buttons.md \
  --model sonnet \
  --role queen \
  --inject-boot
```

**Step 4: Wait for Q33N to return task files**

Q33N reads briefing, reads codebase, writes task files to `.deia/hive/tasks/`, returns summary.

**Step 5: Review Q33N's task files**

Check every task file for:

- Missing deliverables
- Stubs or vague acceptance criteria
- Hardcoded colors
- Files that would exceed 500 lines
- Missing test requirements
- Imprecise file paths

**If corrections needed:** Tell Q33N what to fix, Q33N fixes and returns.

**Step 6: Approve dispatch**

Q33NR: "Approved. Dispatch bees."

Q33N dispatches bees (one per task file).

**Step 7: Receive results from Q33N**

When bees complete, Q33N reads response files, writes completion report, reports to Q33NR.

Q33NR reviews:

- Did all bees complete?
- Do test counts match requirements?
- Any response files missing sections?
- Any stubs shipped?
- Any regressions?

**If issues:** Tell Q33N to dispatch fix tasks.

**Step 8: Report to Q88N**

Q33NR: "Export/Import buttons complete. 8 tests added, all passing. Files modified: ExportButton.tsx, ImportButton.tsx, Toolbar.tsx."

Q88N reviews and approves.

**Step 9: Archive**

Q33NR tells Q33N to archive completed tasks.

---

### Q33N: Queen Coordinator

**Who:** Claude Sonnet in headless mode (no live session)
**Job:** Coordinator — writes task files, dispatches bees, reviews responses
**Does NOT:** Write code (unless Q88N explicitly approves for specific task), talk to Q88N directly

**Workflow:**

**Step 1: Read briefing from Q33NR**

Briefing injected into task prompt by dispatch.py.

**Step 2: Read codebase**

Read files listed in briefing. Understand existing structure.

**Step 3: Write task files**

One file per bee-sized unit of work.

File: `.deia/hive/tasks/2026-04-16-TASK-001-export-button.md`

Contents:

```markdown
# TASK-001: Build Export Button Component

## Objective
Create ExportButton.tsx component that renders in canvas toolbar.

## Context
Toolbar exists at browser/src/components/toolbar/Toolbar.tsx.
Export dialog exists at browser/src/components/dialogs/ExportDialog.tsx.
Need to add button that opens this dialog.

## Files to Read First
- browser/src/components/toolbar/Toolbar.tsx
- browser/src/stores/uiStore.ts
- browser/src/components/dialogs/ExportDialog.tsx

## Deliverables
- [ ] browser/src/components/buttons/ExportButton.tsx (new file)
- [ ] browser/src/components/buttons/ExportButton.test.tsx (new file)
- [ ] Modify Toolbar.tsx to include ExportButton

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Edge cases: button disabled when no scenario loaded

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only (no hardcoded colors)
- No stubs
- Use Lucide Download icon

## Response Requirements
Write response file: `.deia/hive/responses/20260416-TASK-001-RESPONSE.md`
MUST contain these 8 sections:
1. Header (task ID, status, model, date)
2. Files Modified
3. What Was Done
4. Test Results
5. Build Verification
6. Acceptance Criteria
7. Clock / Cost / Carbon
8. Issues / Follow-ups
```

**Step 4: Return to Q33NR for review**

Q33N writes summary:

```
Task files written:
- TASK-001: Export Button Component (Haiku, 2 files, 4 tests)
- TASK-002: Import Button Component (Haiku, 2 files, 4 tests)

Ready for dispatch approval.
```

**Step 5: If Q33NR requests corrections**

Q33NR: "TASK-001 is missing edge case: what if export fails?"

Q33N adds to TASK-001:

```markdown
## Test Requirements
- [ ] Edge cases: button disabled when no scenario loaded
- [ ] Edge case: export fails, show error toast
```

Returns to Q33NR.

**Step 6: Q33NR approves. Dispatch bees.**

```bash
python .deia/hive/scripts/dispatch/dispatch.py \
  .deia/hive/tasks/2026-04-16-TASK-001-export-button.md \
  --model haiku \
  --role bee \
  --inject-boot
```

**Step 7: When bees complete**

Read response files:

`.deia/hive/responses/20260416-TASK-001-RESPONSE.md`:

```markdown
# TASK-001: Build Export Button Component -- COMPLETE

**Status:** COMPLETE
**Model:** Haiku
**Date:** 2026-04-16

## Files Modified
- browser/src/components/buttons/ExportButton.tsx (created, 42 LOC)
- browser/src/components/buttons/ExportButton.test.tsx (created, 68 LOC)
- browser/src/components/toolbar/Toolbar.tsx (modified, +3 LOC)

## What Was Done
- Created ExportButton component with Lucide Download icon
- Added tests for rendering, click behavior, disabled state, error toast
- Integrated into Toolbar

## Test Results
- 4 tests run
- 4 tests pass
- 0 failures

## Build Verification
All tests pass. Build succeeds.

## Acceptance Criteria
- [x] ExportButton.tsx created
- [x] ExportButton.test.tsx created
- [x] Toolbar.tsx modified
- [x] Tests written first (TDD)
- [x] All tests pass
- [x] Edge case: button disabled when no scenario
- [x] Edge case: export fails, show error toast

## Clock / Cost / Carbon
- **Clock:** 87s
- **Cost:** $0.0043
- **Carbon:** ~0.4g CO2

## Issues / Follow-ups
None. All requirements met.
```

Q33N checks:

- ✅ All 8 sections present
- ✅ Tests pass
- ✅ No stubs
- ✅ No regressions

Q33N writes completion report:

```
All tasks complete.
- TASK-001: COMPLETE (4 tests, $0.0043)
- TASK-002: COMPLETE (4 tests, $0.0045)
Total: 8 tests, $0.0088, 174s
```

**Step 8: Archive**

When Q33NR approves, Q33N:

- Moves task files to `.deia/hive/tasks/_archive/`
- Runs: `python _tools/inventory.py add --id FE-100 --title 'Export/Import Buttons' --task TASK-001,TASK-002 --layer frontend --tests 8`
- Runs: `python _tools/inventory.py export-md`

---

### BEE: Worker

**Who:** Claude Haiku/Sonnet/Gemini Flash in headless mode
**Job:** Write code, run tests, write response file
**Does NOT:** Orchestrate, dispatch other bees, modify files outside task scope

**Workflow:**

**Step 1: Read task file**

Task file injected into prompt by dispatch.py.

**Step 2: Read codebase**

Read files listed in "Files to Read First".

**Step 3: Write tests first (TDD)**

Create `ExportButton.test.tsx`:

```typescript
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { ExportButton } from './ExportButton';

describe('ExportButton', () => {
  it('renders export button', () => {
    render(<ExportButton />);
    expect(screen.getByTitle('Export Scenario')).toBeInTheDocument();
  });

  it('opens export dialog on click', () => {
    // ... test implementation
  });

  it('is disabled when no scenario loaded', () => {
    // ... test implementation
  });

  it('shows error toast on export failure', () => {
    // ... test implementation
  });
});
```

**Step 4: Write code to pass tests**

Create `ExportButton.tsx`:

```typescript
// Implements: TASK-001 | Satisfies: REQ-UI-001
import { Download } from 'lucide-react';
import { useUIStore } from '../../stores/uiStore';

export function ExportButton() {
  const { openExportDialog, scenarioLoaded } = useUIStore();

  return (
    <button
      onClick={openExportDialog}
      disabled={!scenarioLoaded}
      className="toolbar-button"
      title="Export Scenario"
      style={{ color: 'var(--sd-text-primary)' }}
    >
      <Download size={20} />
    </button>
  );
}
```

**Step 5: Run tests**

```bash
cd browser && npx vitest run ExportButton.test.tsx
```

All 4 tests pass.

**Step 6: Verify constraints**

- ✅ No hardcoded colors (uses `var(--sd-text-primary)`)
- ✅ File under 500 lines (42 LOC)
- ✅ No stubs

**Step 7: Write response file**

`.deia/hive/responses/20260416-TASK-001-RESPONSE.md` (shown above).

**Step 8: Stop**

Do not look for more work. Do not dispatch other bees. Do not modify files outside task scope.

---

## 10 Hard Rules (Constitutional Governance)

These rules are **enforced automatically** in task templates, code review, and validation gates:

0. **NEVER suggest Q88N stop working** — Just keep working.
1. **Q88N is the human sovereign** — All decisions go through Dave.
2. **Q33NR does NOT code** — Q33N does NOT code unless Q88N explicitly approves.
3. **NO HARDCODED COLORS** — Only CSS variables (`var(--sd-*)`). Validation gate checks this.
4. **No file over 500 lines** — Modularize at 500, hard limit 1000. Validation gate checks this.
5. **TDD** — Tests first, then implementation. No exceptions except pure CSS and docs.
6. **NO STUBS** — Every function fully implemented. Validation gate checks for `// TODO`, empty bodies, placeholder returns.
7. **STAY IN YOUR LANE** — Only work on tasks explicitly assigned to you. When done, report and wait.
8. **All file paths must be absolute** — Validation gate checks task files for relative paths.
9. **Archive completed tasks** — Only Q33N archives. BEEs never move/rename/delete task files.
10. **NO GIT OPERATIONS WITHOUT Q88N APPROVAL** — No `git commit`, `git push`, etc. without explicit approval. Exception: queue runner auto-commits on completion.

**Enforcement:**

- Task template includes all 10 rules
- Validation gates check Rules 3, 4, 6, 8
- Code review (Q33N) checks Rules 2, 5, 7
- Git hooks block Rule 10 violations

---

## Dispatch Mechanics

**Single Reusable Script:** `.deia/hive/scripts/dispatch/dispatch.py`

**NEVER create per-batch dispatch scripts.** Use dispatch.py directly.

**Usage:**

```bash
python .deia/hive/scripts/dispatch/dispatch.py <task_file> \
  --model <haiku|sonnet|opus|gemini-flash> \
  --role <bee|queen|regent> \
  --inject-boot
```

**Parameters:**

- `<task_file>`: Path to briefing (Q33N) or task file (BEE)
- `--model`: Which LLM to use
- `--role`: Which role prompt to inject (bee/queen/regent)
- `--inject-boot`: Inject `.deia/BOOT.md` rules

**Example (Q33NR → Q33N):**

```bash
python .deia/hive/scripts/dispatch/dispatch.py \
  .deia/hive/coordination/2026-04-16-BRIEFING-export-import-buttons.md \
  --model sonnet \
  --role queen \
  --inject-boot
```

**Example (Q33N → BEE):**

```bash
python .deia/hive/scripts/dispatch/dispatch.py \
  .deia/hive/tasks/2026-04-16-TASK-001-export-button.md \
  --model haiku \
  --role bee \
  --inject-boot
```

**Parallel Dispatch:**

When tasks are independent (different directories), dispatch in parallel:

```bash
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/TASK-001.md --model haiku --role bee --inject-boot &
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/TASK-002.md --model haiku --role bee --inject-boot &
wait
```

**Sequential Dispatch:**

When tasks depend on each other, dispatch sequentially:

```bash
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/TASK-001.md --model haiku --role bee --inject-boot
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/TASK-002.md --model haiku --role bee --inject-boot
```

**Cost Control:** Never more than 5 bees in parallel.

---

## File System Layout

| Artifact | Who creates it | Where it goes |
|----------|---------------|---------------|
| Briefing | Q33NR | `.deia/hive/coordination/` |
| Task file | Q33N | `.deia/hive/tasks/` |
| Response file | BEE | `.deia/hive/responses/` |
| Completion report | Q33N | `.deia/hive/responses/` |
| Archived task | Q33N (moves it) | `.deia/hive/tasks/_archive/` |

---

## Model Selection Strategy

| Task Type | Model | Why |
|-----------|-------|-----|
| **Coordination** | Sonnet | Complex reasoning, multi-file context |
| **Simple builds** | Haiku | Fast, cheap, good for isolated components |
| **Complex builds** | Sonnet | Deep codebase understanding needed |
| **Research** | Haiku | Fast file reads, pattern matching |
| **Spec writing** | Sonnet | Nuanced requirement interpretation |
| **Test writing** | Haiku | Straightforward from acceptance criteria |

**Cost Comparison (per 1M tokens):**

- Haiku: $1.00 input, $5.00 output
- Sonnet: $3.00 input, $15.00 output
- Opus: $15.00 input, $75.00 output

**Typical build (10 requirements, 5 tasks):**

- Q33N (Sonnet): ~20k tokens → $0.01
- 5 BEEs (Haiku): ~60k tokens → $0.07
- **Total:** ~$0.08 per build

---

## Success Metrics

**From 1,358 Completed Specs:**

- **Autonomous completion:** 98.7%
- **Human escalation:** 1.3% (17 specs)
- **Average cost per spec:** $0.08
- **Average time per spec:** ~143 seconds (2.4 minutes)
- **Regressions:** 0 (all tests pass after completion)

**Escalation Triggers (1.3% of specs):**

- PROCESS-13 validation failures after 3 retries (Gate 0, Phase 0/1/2)
- Circular dependencies discovered during task breakdown
- External API changes requiring human decision
- Ambiguous requirements that LLM cannot disambiguate after 3 healing attempts

**Resolution:** Human intervention (Q88N) approves override, manually edits SPEC/TASKS, or aborts task.

---

## Comparison to Other Frameworks

| Framework | Orchestration | Correction | Governance | Traceability |
|-----------|--------------|-----------|-----------|--------------|
| **LangGraph** | ✅ (graph-based) | ⚠️ (manual retry logic) | ❌ (no built-in rules) | ❌ (no DAG) |
| **CrewAI** | ✅ (role-based) | ⚠️ (basic validation) | ❌ (no hard rules) | ❌ (no IDs) |
| **AutoGen** | ✅ (multi-agent) | ⚠️ (conversation-based) | ❌ (no constitution) | ❌ (no DAG) |
| **DEIA Hive** | ✅ (4-tier hierarchy) | ✅ (Gate 0 + 3 phases) | ✅ (10 hard rules) | ✅ (REQ→CODE DAG) |

**DEIA Hive differentiator:** Constitutional governance + systematic validation with healing loops.

---

## Future Enhancements

1. **Auto-scaling:** Dynamically adjust bee count based on queue depth
2. **Model routing:** Automatically select model tier based on task complexity
3. **Cross-repo coordination:** Q33N coordinates bees across multiple repos
4. **Budget enforcement:** Hard stop when session cost hits threshold
5. **A/B testing:** Dispatch same task to multiple models, compare outputs

---

**END OF HIVE COORDINATION DOCUMENTATION**
