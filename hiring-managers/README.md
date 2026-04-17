# SimDecisions — For Hiring Managers

**Author:** Dave Eichler
**LinkedIn:** [linkedin.com/in/daaaave-atx](https://linkedin.com/in/daaaave-atx)
**Full Source:** Available on request

---

## Quick Hits

| JD Criterion | Evidence |
|--------------|----------|
| Multi-tier, 12-factor apps | 5-tier architecture, all 12 factors verified |
| Clean architectural separation | view / API / service / persistence / database |
| AI agent orchestration | Hive system: Human → Regent → Coordinator → Workers |
| Evaluating and correcting AI output | PROCESS-13 validation gates (paused for DDD testing) |
| CI/CD pipelines | Railway + Vercel auto-deploy from main |
| Strangler Fig / incremental delivery | 2003 Java/PHP → 2026 Python/TypeScript evolution |

---

## What This Platform Does

SimDecisions is an AI orchestration platform built on a simple premise:

**Simulate before you ship. Stop playing what-if with your customers.**

The platform coordinates multiple AI agents to execute complex tasks under governance, with full audit trails and cost tracking.

---

## Documents in This Directory

| Document | What It Covers |
|----------|----------------|
| [12-FACTOR-COMPLIANCE.md](12-FACTOR-COMPLIANCE.md) | Point-by-point verification against 12-factor principles |
| [HIVE-ORCHESTRATION.md](HIVE-ORCHESTRATION.md) | How AI agents coordinate under human oversight |
| [PROCESS-13-VALIDATION.md](PROCESS-13-VALIDATION.md) | Build integrity gates (currently paused for DDD testing) |
| [THREE-CURRENCIES.md](THREE-CURRENCIES.md) | Tracking time, cost, and carbon for every task |
| [DES-PHILOSOPHY.md](DES-PHILOSOPHY.md) | Why simulation matters before execution |
| [EVOLUTION-STORY.md](EVOLUTION-STORY.md) | 20-year journey from 2003 Java to 2026 AI platform |

---

## Live Systems

| System | Status | Evidence |
|--------|--------|----------|
| Hivenode API | Running | Railway deployment |
| Browser SPA | Running | Vercel deployment |
| Factory (scheduler/dispatcher/queue_runner/triage) | Running | Local nohup daemons via `_tools/restart-services.sh` |
| Three Currencies tracking | Active | Tokens in/out logged per task |
| PROCESS-13 validation | Paused | Testing DDD approach |

---

**Full source code available on request.**
