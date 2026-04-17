# Hive Orchestration — AI Agent Coordination

The Hive is a hierarchical system for coordinating AI agents under human oversight.

---

## The Hierarchy (Plain English)

| Role | Who/What | Responsibility |
|------|----------|----------------|
| **Human** | Dave (the developer) | Sets direction, approves specs, makes final decisions |
| **Regent** | Claude (planning session) | Breaks down objectives into specs, reviews results, reports to human |
| **Coordinator** | Claude (headless) | Manages task queue, dispatches work to bees, reviews responses |
| **Worker Bees** | Claude/GPT/Gemini (headless) | Execute tasks, write code, run tests, produce deliverables |

---

## How It Works

1. **Human** creates an objective or approves a spec
2. **Regent** decomposes the objective into task files, writes briefings
3. **Coordinator** reads briefings, dispatches tasks to the queue
4. **Worker Bees** pick up tasks, execute, write response files
5. **Coordinator** reviews responses, routes failures for retry
6. **Regent** compiles results, reports to human

---

## The Factory (Daemons)

Six daemons run continuously to process the queue:

| Daemon | Purpose |
|--------|---------|
| `scheduler` | Monitors backlog, evaluates dependencies, queues ready tasks |
| `dispatcher` | Assigns tasks to available workers |
| `queue_runner` | Executes tasks, captures output |
| `triage_daemon` | Validates responses, routes failures |
| `vite` | Frontend dev server |
| `hivenode` | API server |

All managed by `_tools/restart-services.sh` (nohup with smart restart).

---

## Why This Matters

- **Audit trail:** Every task has a spec file and response file
- **Reproducibility:** Tasks can be re-run with same inputs
- **Multi-vendor:** Works with Claude, GPT-4, Gemini — no lock-in
- **Human oversight:** Nothing ships without human approval

---

## File Locations

| Artifact | Path |
|----------|------|
| Task queue | `.deia/hive/queue/` |
| Response files | `.deia/hive/responses/` |
| Process specs | `.deia/processes/` |
| Hive config | `.deia/HIVE.md` |
