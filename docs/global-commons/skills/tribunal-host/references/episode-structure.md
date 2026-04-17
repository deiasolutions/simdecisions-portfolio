# Tribunal Episode Structure

The Tribunal format has 5 phases, executed in sequence. This structure is fixed across all episodes.

---

## Phase Breakdown

### Phase 0: Intro (Moderator Only)

**Speaker:** Moderator
**Typical duration:** 45-60 seconds
**Sentence count:** 9-12 sentences

The moderator:
1. Opens the show ("Welcome to The Tribunal...")
2. States the motion/topic being debated
3. Introduces the format (opening statements, rebuttals, closing arguments)
4. Frames the question (what dimensions are we exploring?)
5. Sets expectations ("The panelists will argue. You will decide.")
6. Hands off to panelists

No panelist participation. Pure setup.

---

### Phase 1: Opening Statements (3 Panelists)

**Speakers:** Claude, GPT, Gemini (or custom personas)
**Typical duration per panelist:** 90-130 seconds
**Sentence count per panelist:** 13-24 sentences

Each panelist delivers a complete argument answering the motion. No rebuttals yet — just their strongest case.

Episode 001 order:
1. Claude opens
2. GPT follows
3. Gemini closes

Order can vary by episode. First speaker sets the tone. Last speaker has the advantage of knowing what the others will argue (if generated sequentially).

---

### Phase 2: Rebuttals (3 Panelists)

**Speakers:** Claude, GPT, Gemini
**Typical duration per panelist:** 60-100 seconds
**Sentence count per panelist:** 8-17 sentences

Each panelist responds to one or more other panelists by name, challenging specific claims.

Rules (from topic.md):
- Must name a specific panelist and challenge a specific claim
- "I agree, but..." is not a rebuttal
- Reference evidence, not vibes

Rebuttals are shorter than opening statements — focused, surgical arguments.

---

### Phase 3: Closing Arguments (3 Panelists)

**Speakers:** Claude, GPT, Gemini
**Typical duration per panelist:** 90-110 seconds
**Sentence count per panelist:** 11-20 sentences

Each panelist:
1. Restates their core thesis
2. Acknowledges valid points from opponents (optional but effective)
3. Delivers final verdict on the motion
4. Leaves the audience with clarity

No new evidence. Synthesis and summation only.

---

### Phase 4: Summary (Moderator Only)

**Speaker:** Moderator
**Typical duration:** 80-100 seconds
**Sentence count:** 12-15 sentences

The moderator:
1. Recaps the debate ("Three perspectives, one candidate...")
2. Highlights points of agreement across panelists
3. Highlights points of divergence
4. Restates the question without answering it
5. Closes the show ("The evidence is clear. The context is yours to define.")

No verdict. No winner declared. The moderator synthesizes but does not judge.

---

## Typical Episode Metrics (Based on Episode 001)

| Metric | Value |
|--------|-------|
| Total segments | 11 (1 intro + 3 openings + 3 rebuttals + 3 closings + 1 summary) |
| Total sentences | 150-170 |
| Total duration | 16-20 minutes |
| Moderator share | ~15% of runtime (intro + summary) |
| Panelist share | ~85% of runtime (evenly split across 3) |

---

## Segment Indexing Convention

Segments are numbered sequentially in manifest.json:

| Index | Phase | Speaker |
|-------|-------|---------|
| 0 | intro | Moderator |
| 1 | opening_statement | Claude |
| 2 | opening_statement | GPT |
| 3 | opening_statement | Gemini |
| 4 | rebuttal | Claude |
| 5 | rebuttal | GPT |
| 6 | rebuttal | Gemini |
| 7 | closing_argument | Claude |
| 8 | closing_argument | GPT |
| 9 | closing_argument | Gemini |
| 10 | summary | Moderator |

This indexing is used for `--start-from N` resume functionality.

---

## Format Variations (Future Episodes)

The 5-phase structure is fixed, but these can vary:
- Number of panelists (could be 2, 4, or 5 instead of 3)
- Panelist names/personas (not always Claude/GPT/Gemini — could be personas like "Investor", "Architect", "User")
- Moderator voice
- Phase durations (shorter episodes = tighter time limits per phase)

Episode-level overrides go in `format.yaml`. If no overrides, inherit from `production/shows/tribunal/format.yaml`.
