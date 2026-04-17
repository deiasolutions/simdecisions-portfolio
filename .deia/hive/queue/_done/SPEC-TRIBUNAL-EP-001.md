# SPEC-TRIBUNAL-EP-001: Tribunal Episode Production Package — Baumol Cost Disease

## Priority
P2

## Depends On
None

## Model Assignment
opus

## Objective

Create the complete production episode package for The Tribunal engine. Episode topic: "The Workers AI Can't Replace Are Going Broke" — a multi-model debate on Baumol's cost disease accelerated by AI. The bee writes the episode configuration files; the Tribunal engine then runs the actual multi-model debate using Claude, GPT, and Gemini as live panelists.

## Files to Read First

- production/episodes/tribunal/001-who-should-hire-dave/topic.md
- production/episodes/tribunal/001-who-should-hire-dave/context.md
- production/episodes/tribunal/001-who-should-hire-dave/personas.md
- production/episodes/tribunal/001-who-should-hire-dave/production.log
- production/episodes/tribunal/001-who-should-hire-dave/README.md

## Background: How The Tribunal Engine Works

The Tribunal engine is a multi-model debate orchestrator. It does NOT use a single LLM to write all sides. Each panelist IS a different LLM (Claude, GPT, Gemini) speaking for itself. The engine:

1. Reads the episode package (topic.md, context.md, personas.md, format.yaml)
2. Runs the moderator intro
3. For each debate phase, calls each panelist model with its system prompt + all prior debate history as context
4. Each round's output becomes input for the next round — context accumulates
5. Renders all responses to TTS via Kokoro-82M
6. Produces transcript, wav files, and manifest

See `production/episodes/tribunal/001-who-should-hire-dave/production.log` for the exact call sequence from Episode 001.

## Episode Identity

- **Show:** The Tribunal
- **Episode:** 002
- **Title:** "The Workers AI Can't Replace Are Going Broke"
- **Moderator:** Fr4nk (host and provocateur, does not advocate)
- **Panelists:** Claude, GPT, Gemini — each assigned a debate position
- **Runtime target:** 25-35 minutes

## Debate Round Structure

This episode uses 4 debater rounds (not 3 like Episode 001). Each round depends on the previous — the engine feeds all prior output as context.

### Round 0 — Moderator Intro
- Fr4nk opens with the Baumol mechanism (Beethoven story), summarizes the MIT Iceberg and Anthropic data, and poses the core question: "The workers safest from displacement are the workers society can least afford to pay. Who pays for this?"
- No panelist input needed

### Round 1 — Opening Statements (3 parallel)
- Each panelist receives: topic brief + context.md + their position assignment
- Each delivers their opening position (~250-400 words each)
- All three run in parallel (no cross-dependencies within this round)

### Round 2 — Main Arguments (3 sequential, depends on Round 1)
- Each panelist receives: everything from Round 1 (all three opening statements) + their position brief
- This is the substantive round — deeper argumentation, direct engagement with what the others said in their openers
- Each responds to the specific claims made by the other panelists, not generic talking points
- (~400-600 words each)

### Round 3 — Q&A (moderator + 3 responses, depends on Round 2)
- Fr4nk generates one pointed follow-up question per panelist based on Rounds 1-2
- The question should probe the weakest point in each panelist's argument
- Each panelist receives: full debate history + their specific question
- (~200-300 words each)

### Round 4 — Closing Statements (3 sequential, depends on Round 3)
- Each panelist receives: complete debate history (all prior rounds including Q&A)
- Final argument — what they want the audience to remember
- (~200-300 words each)

### Round 5 — Moderator Summary
- Fr4nk summarizes the debate, applies Three Currencies scoring, delivers the closing audience question verbatim:
- "You are a 24-year-old with a graduate degree entering a knowledge-work occupation. AI theoretically covers 94% of your tasks. Your observed exposure is 33% and rising. No one has been fired yet — but no one is being hired. Which of these three speakers is fighting for you?"

## Debate Positions and Model Assignments

| Position | Assigned To | Role |
|---|---|---|
| A — The Inevitabilist | Claude | Baumol is a law, not a warning. Fiscal policy, not AI policy. |
| B — The Redistributionist | GPT | Tax AI productivity gains at point of capture. Sovereign dividend. |
| C — The Displaced Professional | Gemini | The real crisis is the grad-school-educated analyst who did everything right. |

### Position A — The Inevitabilist (Claude)

Arguments:
- Historical transitions always created more jobs than they destroyed
- Productivity gains generate surplus that can be redistributed
- Capping AI productivity to protect cost-disease sectors is a worse outcome
- Essential service cost inflation has always been managed — healthcare and education are expensive but extant

### Position B — The Redistributionist (GPT)

Arguments:
- The gap between AI winners and cost-disease workers is structurally self-reinforcing without intervention
- Precedent: severance taxes, sovereign wealth funds, land value tax
- The 47%-higher-earning exposed class is also the political donor class — voluntary redistribution will not happen
- Clock and Coin are being optimized; Carbon and social stability are not

### Position C �� The Displaced Professional (Gemini)

Arguments:
- Entry-level hiring in exposed occupations down 14% for workers aged 22-25 (Anthropic, March 2026)
- The Iceberg Index shows 4/5ths of the problem is invisible to policymakers
- The workers being harmed are the political base of neither party
- "No unemployment increase yet" is what economists said about manufacturing in 2005

## Source Material for Context Document

The context.md file must contain the data that all panelists draw from:

**MIT / Oak Ridge — Project Iceberg (October 2025)**
arXiv:2510.25137 | iceberg.mit.edu/report.pdf
- 151 million workers modeled across 923 occupations and 3,000 counties
- Visible exposure: 2.2% of US wage value ($211B)
- Hidden exposure: 11.7% ($1.2T) — five times larger
- Tennessee, North Carolina, Utah show higher exposure than California

**Anthropic — Labor Market Impacts of AI (March 5, 2026)**
anthropic.com/research/labor-market-impacts | Massenkoff & McCrory
- "Observed exposure" vs theoretical capability
- Most exposed workers earn 47% more, 16pp more likely female, ~4x more likely graduate degree
- Computer/math: 94% theoretical, 33% observed — gap closing
- 14% drop in job-entry rates for ages 22-25 in high-exposure occupations

**Baumol's Cost Disease (Baumol & Bowen, 1966)**
- Beethoven string quartet: same 4 musicians, same 25 minutes, 1865 to today
- 50-year record: productive sectors got cheaper, essential human services got relentlessly expensive
- AI compresses a decade of productivity gains into years — Baumol accelerates

**Brynjolfsson et al. 2025** — entry-level employment decline data, Stanford Digital Economy Lab

## Fr4nk Voice Profile

Authoritative, dry, slightly amused. Tempo is measured — Fr4nk does not rush. Fr4nk names the tension without resolving it. Fr4nk does not take sides — any output where Fr4nk advocates a position is rejected.

## Deliverables

All files written to `production/episodes/tribunal/002-workers-ai-cant-replace/`:

| File | Purpose |
|---|---|
| topic.md | Debate question, framing, rules (follow ep 001 structure) |
| context.md | Source material data for all panelists to draw from |
| personas.md | Position-to-model mapping and persona instructions |
| format.yaml | Phase definitions overriding show defaults for 4-round structure |
| moderator-prompts.md | System prompt + per-phase turn prompts for Fr4nk |
| panelist-prompts.md | System prompt per position (A/B/C) with argument seeds and citations |
| scoring-rubric.md | Three Currencies (Clock/Coin/Carbon) scoring criteria per segment |

## Production Notes

- TTS: Kokoro-82M local (NVIDIA GPU)
- Each panelist gets a distinct voice (see ep 001 README for voice lineup reference)
- OBS compositing: three-panel debate layout, score ticker
- The engine handles all multi-model API calls — the bee does NOT call GPT/Gemini APIs
- The bee writes the episode package; Q88N runs `python -m production.engine --episode 002-workers-ai-cant-replace`

## Source Citations

1. Chopra, A. et al. "The Iceberg Index." arXiv:2510.25137, October 2025.
2. Massenkoff, M. & McCrory, P. "Labor Market Impacts of AI." Anthropic, March 2026.
3. Baumol, W.J. & Bowen, W.G. "Performing Arts: The Economic Dilemma." 1966.
4. Brynjolfsson, E. et al. "Canaries in the Coal Mine?" Stanford DEL, August 2025.

## Acceptance Criteria

- [ ] All 7 deliverable files exist in production/episodes/tribunal/002-workers-ai-cant-replace/
- [ ] topic.md follows the structure of production/episodes/tribunal/001-who-should-hire-dave/topic.md
- [ ] context.md contains all source material data with proper citations
- [ ] personas.md maps Position A to Claude, Position B to GPT, Position C to Gemini
- [ ] format.yaml defines 6 phases: intro, opening_statement, main_argument, qa, closing_statement, summary
- [ ] format.yaml specifies that main_argument depends on opening_statement, qa depends on main_argument, closing_statement depends on qa
- [ ] moderator-prompts.md includes the Beethoven/Baumol story for intro and the verbatim closing question for summary
- [ ] panelist-prompts.md contains one system prompt per position seeded with that position's argument points and source citations
- [ ] scoring-rubric.md applies Three Currencies (Clock, Coin, Carbon) at least once per debater phase
- [ ] No panelist system prompt advocates for a position other than its assigned one
- [ ] Fr4nk prompts are neutral — no advocacy for any position

## Smoke Test

- [ ] Directory production/episodes/tribunal/002-workers-ai-cant-replace/ exists with 7 files
- [ ] format.yaml is valid YAML with a phases key containing 6 entries
- [ ] context.md mentions all four source citations
- [ ] personas.md contains the strings "Claude", "GPT", and "Gemini"
- [ ] moderator-prompts.md contains the verbatim closing audience question

## Constraints

- The bee writes the episode package only — it does NOT generate the debate transcript
- The actual debate is run by the Tribunal engine calling each model's API live
- No file over 500 lines
- No stubs — every deliverable complete
- No git operations
- No code changes to any platform source
- Script bee reads all source citations before writing — no argument invented from training data
- Debater arguments stay within bounds defined in this spec
- Three Currencies applied consistently — never fewer than all three
