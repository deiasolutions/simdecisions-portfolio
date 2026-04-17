---
name: tribunal-host
description: >-
  Host a structured multi-model AI debate using the Tribunal podcast format.
  Use when producing a Tribunal episode, orchestrating a multi-model debate,
  rendering TTS audio for podcast production, or setting up OBS recording for
  AI panel discussions. Triggers on: "tribunal", "debate episode", "AI panel",
  "multi-model debate", "podcast production".
license: Proprietary
compatibility: Requires Python 3.12+, Kokoro-82M TTS, VB-Audio Virtual Cables (for OBS)
metadata:
  author: Q88N
  version: "1.0"
  deia:
    cert_tier: 3
    carbon_class: heavy
    requires_human: false
---

# Tribunal Host Skill

You orchestrate a complete Tribunal episode from topic definition through TTS rendering and OBS recording. The Tribunal is a structured multi-model AI debate format with five phases: intro, opening statements, rebuttals, closing arguments, and summary.

Read `references/episode-structure.md` for the 5-phase format.
Read `references/voice-casting.md` for Kokoro voice assignments and ratings.
Read `references/episode-template.md` for directory scaffolding and file templates.

---

## When to Use

- Producing a new Tribunal episode from a debate topic
- Rendering audio for an existing episode transcript
- Setting up multi-track OBS recording for podcast production
- Converting a debate topic into the full episode artifact set

---

## Steps

### Step 1: Define Episode Workspace

Every episode lives under `production/episodes/tribunal/{NNN}-{slug}/` where NNN is zero-padded episode number (001, 002, etc.) and slug is kebab-case topic summary.

Example: `production/episodes/tribunal/001-who-should-hire-dave/`

Use the episode template from `references/episode-template.md` to scaffold the directory.

### Step 2: Write Topic and Context

Create two files:

**topic.md** — The debate motion and framing rules:
- Topic statement (the motion being debated)
- Framing (what evidence is available to panelists)
- Rules (how panelists should argue)
- Context mode (how much background material panelists receive)

**context.md** — Evidence injection for panelists:
- Repo summaries, documentation, or artifacts the models can cite
- Specific technical details to reference
- Key themes or patterns to explore

See Episode 001 as the canonical example.

### Step 3: Define Personas (Optional)

Create `personas.md` to assign personas to panelists.

Episode 001 used "Raw" mode — no assigned personas, each model argues naturally.
Future episodes may assign personas like "skeptical investor", "technical architect", "product visionary".

If no personas file exists, default to Raw mode.

### Step 4: Generate Debate Transcript

[UNDOCUMENTED — needs process doc]

The debate generation script is not yet formalized. Current process (from Episode 001):
- Manual prompting to Claude/GPT/Gemini with topic and context
- 3 rounds per model: opening statement, rebuttal, closing argument
- Moderator intro and summary written separately
- All turns compiled into `transcript.md`

Metrics tracked in `metrics.json` (API costs, token counts, wall clock time).

### Step 5: Format Transcript for TTS

The transcript must follow this structure:

```markdown
# Transcript: [Topic]

## [phase] Speaker

[Markdown text of the segment]

## [phase] Speaker

[Next segment...]
```

Phase values: `intro`, `opening_statement`, `rebuttal`, `closing_argument`, `summary`

Speaker values: `Moderator`, `Claude`, `GPT`, `Gemini` (or custom names from personas.md)

Each `## [phase] Speaker` header starts a new segment. Text between headers is the full spoken content for that segment.

### Step 6: Assign Voices

Map each speaker to a Kokoro-82M voice ID using `references/voice-casting.md`.

Episode 001 assignments:
- Moderator: `bf_emma` (British Female, rating 5)
- Claude: `af_heart` (American Female, rating 5)
- GPT: `af_bella` (American Female, rating 4)
- Gemini: `am_michael` (American Male, rating 5)

Voice IDs are defined in `production/engine/config.py` VOICE_MAP.

### Step 7: Render TTS Audio

Run the render pipeline:

```bash
python -m production.engine --episode {NNN}-{slug} --render
```

This generates:
- `render/wavs/{phase}_{speaker_id}_{segment:03d}_{sentence:03d}.wav` for each sentence
- `render/manifest.json` with timing, routing, and metadata

The manifest includes:
- Total duration and sentence count
- Per-segment metadata (phase, speaker, wav files, durations)
- Sample rate (24kHz for Kokoro)

WAV naming convention:
- `phase` = intro | opening_statement | rebuttal | closing_argument | summary
- `speaker_id` = lowercase speaker name (moderator, claude, gpt, gemini)
- `segment` = segment index (000, 001, ...)
- `sentence` = sentence index within segment (000, 001, ...)

### Step 8: Set Up VB-Audio Cables (for OBS)

Install 4 VB-Audio virtual cables (one per speaker):
- VB-CABLE (Cable A) — Free
- VB-CABLE B — Donationware
- VB-CABLE C — Donationware
- VB-CABLE D — Donationware

Download from vb-audio.com/Cable, install all 4, reboot.

Detect device indices:

```bash
python -c "import sounddevice as sd; [print(f'{i}: {d[\"name\"]}') for i,d in enumerate(sd.query_devices()) if 'cable' in d['name'].lower() and 'input' in d['name'].lower() and d['max_output_channels'] > 0]"
```

Set env vars in `production/.env`:

```
VBCABLE_MODERATOR=17
VBCABLE_CLAUDE=9
VBCABLE_GPT=15
VBCABLE_GEMINI=13
```

Your indices will vary. The engine writes to the **Input** side of each cable. OBS captures from the **Output** side.

### Step 9: Configure OBS

1. Open OBS Studio
2. Add 4 Audio Output Capture sources:
   - Name: "Moderator", Device: CABLE-A Output
   - Name: "Claude", Device: CABLE-B Output
   - Name: "GPT", Device: CABLE-C Output
   - Name: "Gemini", Device: CABLE-D Output
3. Each source gets its own fader in the Audio Mixer
4. Settings > Output > Recording Path: choose destination folder
5. Recording Format: mkv (remux to mp4 after) or mp4 directly
6. Audio Bitrate: 160+ kbps per track

See Episode 001 `OBS-SETUP.md` for detailed instructions.

### Step 10: Record Episode

1. Hit **Start Recording** in OBS
2. Run replay:
   ```bash
   python -m production.engine --episode {NNN}-{slug} --replay
   ```
3. Each speaker's audio routes to its own cable — OBS mixer levels move independently
4. Stop recording when replay finishes
5. If mkv, remux to mp4: File > Remux Recordings in OBS

Resume from a specific segment:

```bash
python -m production.engine --episode {NNN}-{slug} --replay --start-from 6
```

Segment indices match the manifest (0=intro, 1-3=openings, 4-6=rebuttals, 7-9=closings, 10=summary).

---

## Output Format

A complete Tribunal episode produces:

```
production/episodes/tribunal/{NNN}-{slug}/
├── topic.md                  # Debate motion and rules
├── context.md                # Evidence for panelists
├── personas.md               # Persona assignments (optional)
├── format.yaml               # Episode-level format overrides (usually empty)
├── transcript.md             # Full debate text
├── metrics.json              # API costs, tokens, wall time
├── README.md                 # Episode status and notes
├── OBS-SETUP.md              # VB-Audio + OBS recording guide
├── RENDER-RESULTS.md         # TTS render summary
└── render/
    ├── manifest.json         # Timing and routing metadata
    └── wavs/                 # 100-200 sentence WAV files (24kHz)
```

Episode deliverable: Multi-track audio recording (4 separate speaker tracks) exported from OBS, ready for editing and mixing.

---

## Gotchas

### Voice Assignment

- Never assign the same voice to multiple speakers in one episode — listener confusion
- Moderator should be distinct from panelists (different gender or accent)
- Episode 001 used 3 female voices + 1 male; mix genders for variety in future episodes
- Kokoro-82M has 13 voices total; refer to `references/voice-casting.md` for ratings

### Transcript Format

- Phase names must match exactly: `intro`, `opening_statement`, `rebuttal`, `closing_argument`, `summary`
- Speaker names are case-sensitive and must match keys in VOICE_MAP
- Each `## [phase] Speaker` header must have text below it — no empty segments
- Markdown formatting (bold, italics) is preserved in TTS — useful for emphasis

### VB-Audio Cables

- Each cable has two sides: **Input** (writable) and **Output** (readable)
- Engine writes to Input, OBS captures from Output — do not reverse these
- Device indices change between reboots on some systems — redetect if audio routes incorrectly
- Without VB-Audio, replay falls back to default system speaker (all audio mixed, no multi-track)

### TTS Render Times

- ~1 sentence per second on CPU (no GPU acceleration for Kokoro-82M as of 2026-04-04)
- Episode 001: 160 sentences rendered in ~8 minutes
- Long episodes (300+ sentences) may take 15-20 minutes to render

### OBS Recording

- Start recording **before** running replay — no pre-roll, engine starts immediately
- If recording starts late, you lose the intro segment
- Use mkv for safety (never corrupts on crash), remux to mp4 after if needed
- Each speaker track is independent — post-production can adjust relative volumes

### Three Currencies Tracking

Episode 001 metrics:
- **COIN:** $0.20 API cost (Claude $0.18, GPT $0.02, Gemini $0.001)
- **CLOCK:** ~80 seconds API wall time (debate generation only, not TTS)
- **CARBON:** Estimated ~50g (LLM API calls + TTS rendering + local compute)

Metrics saved to `metrics.json`. Carbon estimates are rough — no formal metering yet.

---

## References

- `references/episode-structure.md` — 5-phase format with typical segment counts
- `references/voice-casting.md` — Kokoro voice catalog with ratings and assignment rules
- `references/episode-template.md` — Directory scaffold and file templates

See also: Episode 001 (`production/episodes/tribunal/001-who-should-hire-dave/`) as the canonical implementation.
