# SPEC-FACTORY-110: Inventory System Research

**MODE: EXECUTE**

**Spec ID:** SPEC-FACTORY-110
**Created:** 2026-04-09
**Author:** Q88N
**Type:** RESEARCH
**Status:** READY
**Blocks:** SPEC-FACTORY-111 (build spec)

---

## Priority
P1

## Depends On
None

## Model Assignment
sonnet

## Purpose

Survey the existing `inventory.py` system to understand its current state, capabilities, and integration points. This research informs SPEC-FACTORY-111 which will resurrect and integrate it with the factory mobile app.

**Deliverable:** Research report answering all questions below, written to `.deia/hive/responses/20260409-FACTORY-110-RESPONSE.md`

---

## Survey Targets

Find and read these files (report if not found):

- `inventory.py` — wherever it lives (search repo)
- Any `inventory*.py` variants
- Any `backlog*.py` or `bugs*.py` related files
- Database schema related to inventory/backlog
- Any CLI or API that interacts with inventory
- Any specs or docs mentioning inventory system

Report exact file paths, line counts, and key functions/classes.

---

## Questions

### Section 1: Current State

**Q1.1** Where does `inventory.py` live? What's its current state — working, broken, partial?

**Q1.2** What data does it store? (backlog items, bugs, features, specs, tasks?) What fields per item?

**Q1.3** Where is the data persisted? (JSON file, SQLite, PostgreSQL, markdown files?)

**Q1.4** Is there a CLI interface? What commands exist?

**Q1.5** Is there an API? What endpoints?

---

### Section 2: Data Model

**Q2.1** What is the schema for an inventory item? List all fields.

**Q2.2** Are there different item types (bug, feature, spec, task)? How are they distinguished?

**Q2.3** What statuses can an item have? (backlog, active, blocked, done, archived?)

**Q2.4** Is there priority/ordering? How is it represented?

**Q2.5** Are there dependencies between items? How represented?

---

### Section 3: Integration Points

**Q3.1** Does inventory integrate with the queue system? How?

**Q3.2** Does inventory integrate with the scheduler? How?

**Q3.3** Does inventory feed into spec generation or task creation?

**Q3.4** Is there any UI for inventory currently?

**Q3.5** Does inventory emit to Event Ledger?

---

### Section 4: Gaps & Recommendations

**Q4.1** What's broken or missing that needs fixing?

**Q4.2** What would be needed to expose inventory via `/factory/inventory` API?

**Q4.3** What would be needed to add an inventory tab to the factory mobile app?

**Q4.4** Should inventory items become first-class queue items, or stay separate?

**Q4.5** Recommended approach for FACTORY-111 build spec?

---

## Acceptance Criteria

- [ ] All survey target files located and read (or reported as not found)
- [ ] All 17 questions answered with file+line citations
- [ ] Schema documented if found
- [ ] Integration points mapped
- [ ] Clear recommendation for FACTORY-111 scope
- [ ] Response written to `.deia/hive/responses/20260409-FACTORY-110-RESPONSE.md`

## Smoke Test

```bash
test -f .deia/hive/responses/20260409-FACTORY-110-RESPONSE.md && echo "Response exists" || echo "MISSING"
grep -c "^##" .deia/hive/responses/20260409-FACTORY-110-RESPONSE.md
# Should show at least 5 sections
```

## Constraints

- RESEARCH ONLY — do not modify any code
- Answer from actual file reads, not memory
- If file not found, state "FILE NOT FOUND" and search alternatives
- Provide enough detail for FACTORY-111 to be written without further research

## Response File

`.deia/hive/responses/20260409-FACTORY-110-RESPONSE.md`

---

*SPEC-FACTORY-110 — Q88N — 2026-04-09*
