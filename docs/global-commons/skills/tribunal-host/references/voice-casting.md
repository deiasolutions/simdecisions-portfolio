# Tribunal Voice Casting Guide

Kokoro-82M provides 13 voices. Episode 001 auditioned all 13 and rated them for Tribunal use.

---

## Voice Ratings (5=best, 1=worst)

Ratings are subjective, based on clarity, naturalness, and suitability for podcast debate.

### Female Voices — Leads

| Name | ID | Accent | Rating | Grade | Notes |
|------|----|--------|--------|-------|-------|
| Heart | `af_heart` | American | 5 | A | Clear, warm, natural. Best female voice. |
| Emma | `bf_emma` | British | 5 | B- | Crisp, authoritative. Great for moderator. |
| Bella | `af_bella` | American | 4 | A- | Smooth, professional. Slight robotic edge. |

### Male Voices — Leads

| Name | ID | Accent | Rating | Grade | Notes |
|------|----|--------|--------|-------|-------|
| Michael | `am_michael` | American | 5 | C+ | Best male voice. Deep, clear, confident. |
| Puck | `am_puck` | American | 4 | C+ | Lighter than Michael, still solid. |
| Fenrir | `am_fenrir` | American | 4 | C+ | Similar to Puck, slightly more gravitas. |
| Fable | `bm_fable` | British | 4 | C | British accent, dignified. |

### Female Voices — Backups

| Name | ID | Accent | Rating | Grade | Notes |
|------|----|--------|--------|-------|-------|
| Aoede | `af_aoede` | American | 3 | C+ | Serviceable, but less natural than leads. |
| Nicole | `af_nicole` | American | 2 | B- | Flat affect, useful for certain personas. |
| Isabella | `bf_isabella` | British | 2 | C | British, but muddy articulation. |
| Sarah | `af_sarah` | American | 2 | C+ | Robotic, avoid for leads. |

### Male Voices — Backups

| Name | ID | Accent | Rating | Grade | Notes |
|------|----|--------|--------|-------|-------|
| Adam | `am_adam` | American | 3 | — | Usable, but Michael is better. |
| George | `bm_george` | British | 3 | C | British, lacks warmth. |

---

## Episode 001 Assignments

| Speaker | Voice | ID | Accent | Gender | Why This Choice |
|---------|-------|----|--------|--------|----------------|
| Moderator | Emma | `bf_emma` | British | Female | Authority, distinctiveness from panelists |
| Claude | Heart | `af_heart` | American | Female | Top-rated female voice, warmth |
| GPT | Bella | `af_bella` | American | Female | Professional, smooth |
| Gemini | Michael | `am_michael` | American | Male | Only male panelist, provides contrast |

Episode 001 used 3 female + 1 male for variety. Future episodes should mix genders differently.

---

## Assignment Rules

### Rule 1: Never Duplicate Voices

Each speaker gets a unique voice. Listener confusion is fatal in audio-only debate.

### Rule 2: Moderator Must Be Distinct

Moderator should contrast with panelists in accent, gender, or both. Episode 001 used British accent (Emma) vs. 3 American panelists.

### Rule 3: Gender Balance

Avoid all-male or all-female panelists if possible. 2:1 or 3:1 split is ideal. Episode 001 was 3F:1M (panelists) + 1F (moderator).

### Rule 4: Prioritize Ratings 4-5

Use rating 3 voices only when you need more than 4 speakers total. Rating 2 voices are emergency backups — avoid in polished episodes.

### Rule 5: Accent Variety (Optional)

British accent (Emma, Fable, Isabella, George) provides contrast. Episode 001 used 1 British (moderator) + 4 American (panelists + extras).

---

## Recommended Lineups

### 3-Panelist Debate (Standard)

**Option A (3F + 1M):**
- Moderator: Emma (bf_emma) — British Female
- Panelist 1: Heart (af_heart) — American Female
- Panelist 2: Bella (af_bella) — American Female
- Panelist 3: Michael (am_michael) — American Male

**Option B (2F + 2M):**
- Moderator: Emma (bf_emma) — British Female
- Panelist 1: Heart (af_heart) — American Female
- Panelist 2: Michael (am_michael) — American Male
- Panelist 3: Puck (am_puck) — American Male

**Option C (1F + 3M):**
- Moderator: Emma (bf_emma) — British Female
- Panelist 1: Michael (am_michael) — American Male
- Panelist 2: Puck (am_puck) — American Male
- Panelist 3: Fenrir (am_fenrir) — American Male

### 4-Panelist Debate (Extended)

- Moderator: Emma (bf_emma)
- Panelist 1: Heart (af_heart)
- Panelist 2: Bella (af_bella)
- Panelist 3: Michael (am_michael)
- Panelist 4: Puck (am_puck)

### 2-Panelist Debate (Focused)

- Moderator: Emma (bf_emma)
- Panelist 1: Heart (af_heart)
- Panelist 2: Michael (am_michael)

---

## Voice ID Reference

Kokoro-82M voice IDs are defined in `production/engine/config.py` VOICE_MAP.

Format: `{accent_code}{gender_code}_{name}`

Where:
- `a` = American, `b` = British
- `f` = Female, `m` = Male
- `name` = voice name (lowercase)

Examples:
- `af_heart` = American Female Heart
- `bf_emma` = British Female Emma
- `am_michael` = American Male Michael

---

## TTS Engine Notes

- Kokoro-82M is CPU-only as of 2026-04-04 (no GPU acceleration in production)
- Sample rate: 24kHz
- Output format: float32 WAV
- Sentence-level rendering (~1 sentence/second on CPU)
- No real-time streaming — offline batch render only

---

## Future Voices

If Kokoro releases new voices or if DEIA integrates a different TTS engine:
1. Audition all voices on the same test script
2. Rate on 1-5 scale for clarity, naturalness, suitability
3. Update this reference with new entries
4. Update VOICE_MAP in `production/engine/config.py`
5. Regenerate affected episodes if voices change
