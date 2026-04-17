# SPEC-WIKI-ONET-READVIEW-001

**MODE: EXECUTE**

**Spec ID:** SPEC-WIKI-ONET-READVIEW-001
**Created:** 2026-04-09
**Author:** Q88N
**Type:** BUILD — wiki read interface over ONET/exposure/profile data
**Status:** READY
**Priority:** P2

---

## Purpose

Expose the ONET occupation data, AI exposure scores, and Four-Vector
operator profiles as a searchable read view in the SimDecisions wiki.
A user searches an occupation name or SOC code and sees its full
profile: skills, tasks, exposure scores, and Four-Vector breakdown.

No data entry. No duplication. Pure query interface over tables built
by SPEC-ONET-INGEST-001, SPEC-AI-EXPOSURE-SCORES-001, and
SPEC-OPERATOR-PROFILE-SEED-001.

---

## Depends On

- SPEC-ONET-INGEST-001
- SPEC-AI-EXPOSURE-SCORES-001
- SPEC-OPERATOR-PROFILE-SEED-001

## Model Assignment

sonnet

---

## Backend — New API Endpoints

Add to hivenode FastAPI. New file: `hivenode/routers/onet.py`.
Register router in `main.py` under prefix `/api/onet`.

### GET /api/onet/search

Query param: `q` (string, min 2 chars)

Searches `onet_occupations.title` using PostgreSQL `ILIKE '%q%'`.
Returns up to 20 matches.

Response shape:
```json
{
  "results": [
    {
      "soc_code": "15-1252.00",
      "title": "Software Developers",
      "job_zone": 4,
      "bright_outlook": true
    }
  ]
}
```

### GET /api/onet/occupation/{soc_code}

Returns full occupation profile for a single SOC code.

Response shape:
```json
{
  "soc_code": "15-1252.00",
  "title": "Software Developers",
  "description": "...",
  "job_zone": 4,
  "bright_outlook": true,
  "skills": [
    {
      "element_id": "2.A.1.b",
      "name": "Critical Thinking",
      "category": "Basic Skills",
      "importance": 4.5,
      "level": 5.2
    }
  ],
  "tasks": [
    {
      "task_id": 123,
      "description": "...",
      "category": "Core"
    }
  ],
  "wages": {
    "median_annual": 132270,
    "employment": 1847900,
    "year": 2025
  },
  "ai_exposure": {
    "theoretical_pct": 94.3,
    "observed_pct": 35.8,
    "source": "anthropic_2026_03",
    "captured_at": "2026-03-05"
  },
  "four_vector": {
    "sigma": 0.7821,
    "pi": 0.6340,
    "rho": 0.3120,
    "alpha": 0.9430
  }
}
```

Skills sorted by importance descending, max 20 returned.
Tasks sorted by category (Core first), max 10 returned.
If wages row absent, return null for wages object.
If exposure row absent, return null for ai_exposure object.
If profile row absent, return null for four_vector object.

---

## Frontend — OnetPane Component

New wiki pane component: `OnetPane.tsx`
Registered in the wiki pane registry as type `onet`.

### Layout

Two states: search and detail.

**Search state (default)**
- Text input: "Search occupations..."
- Results list below input, appears on keystroke (debounced 300ms)
- Each result shows title and SOC code
- Click a result → detail state

**Detail state**
- Back button → returns to search state
- Header: occupation title, SOC code, job zone badge, bright outlook badge
- Four sections, collapsible:

  1. **AI Exposure**
     Two horizontal bar charts side by side:
     - Theoretical coverage % (filled bar, color: amber)
     - Observed coverage % (filled bar, color: teal)
     Label beneath: source and date

  2. **Four-Vector Profile**
     Radar/spider chart with four axes: σ π ρ α
     Each axis labeled with full name below the chart
     (Skill Depth, Process Orientation, Relational Load, AI Exposure)

  3. **Top Skills**
     Table: skill name, category, importance (0–5), level (0–7)
     Sorted by importance. Max 20 rows. No pagination needed.

  4. **Tasks**
     List: Core tasks first, then Supplemental
     Max 10 items. Each item is one line of text.

- Wages strip at bottom of detail:
  Median annual wage (formatted as $XXX,XXX) | Employment: X,XXX,XXX | Year: XXXX

### Styling

Glass-first. Consistent with existing wiki pane aesthetic.
Use existing CSS variables — no new color definitions.
Bar charts and radar chart: inline SVG, no charting library dependency.

---

## Acceptance Criteria

**Backend**
- [ ] GET /api/onet/search returns results for "software", "nurse", "accountant"
- [ ] GET /api/onet/occupation/15-1252.00 returns full profile
- [ ] Null objects returned gracefully where data absent — no 500 errors
- [ ] Both endpoints respond in < 200ms on Railway

**Frontend**
- [ ] Search input returns results within 300ms of keystroke
- [ ] Detail view renders all four sections for any occupation
- [ ] Null data sections render gracefully (collapsed or labeled "Not available")
- [ ] Back button returns to search state with previous query intact
- [ ] Renders correctly at 1280px and 1920px viewport widths

## Smoke Test

```bash
# Backend
curl "http://127.0.0.1:8420/api/onet/search?q=software" | jq '.results | length'
# Expected: > 0

curl "http://127.0.0.1:8420/api/onet/occupation/15-1252.00" | jq '.four_vector'
# Expected: object with sigma, pi, rho, alpha values

curl "http://127.0.0.1:8420/api/onet/occupation/15-1252.00" | jq '.ai_exposure'
# Expected: object with theoretical_pct and observed_pct

# Frontend: manual — load wiki, open OnetPane, search "financial analyst",
# click first result, verify all four sections render
```

## Constraints

- Read-only — no writes from either endpoint
- No new charting library — SVG only
- OnetPane is self-contained — no shared state with other panes
- Backend file max 150 lines
- Frontend component max 300 lines

## Response File

`.deia/hive/responses/20260414-WIKI-ONET-READVIEW-RESPONSE.md`

---

*SPEC-WIKI-ONET-READVIEW-001 — Q88N — 2026-04-09*
