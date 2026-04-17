# SimDecisions Brand Constants
# manim-animation skill v1.0
# Always define these at the top of every scene file — never hardcode hex inline.

---

## Color Palette

```python
# Core
SD_DARK    = "#0D0F14"   # background — use for self.camera.background_color
SD_SURFACE = "#161B22"   # card / panel fill
SD_WHITE   = "#E8EAF0"   # primary text
SD_MUTED   = "#6B7280"   # secondary text, dividers, subtle elements

# Accent
SD_BLUE    = "#4A9EFF"   # primary accent — nodes, arrows, highlights
SD_GREEN   = "#3DDC84"   # success, chosen branch, positive outcome
SD_AMBER   = "#FFB347"   # warning, alternative branch, caution
SD_RED     = "#FF6B6B"   # failure, rejected branch, error state

# Currency
SD_CARBON  = "#8B5CF6"   # CARBON currency (purple)
SD_COIN    = "#F59E0B"   # COIN currency (gold) — use SD_AMBER if unavailable
SD_CLOCK   = "#60A5FA"   # CLOCK currency (light blue) — use SD_BLUE if close enough
```

---

## Usage Rules

1. Always define all constants at the top of the file, before imports.
2. Never use hex values inline in scene code — always reference the constant.
3. `SD_DARK` is always the background. Set it in `construct()`:
   ```python
   self.camera.background_color = SD_DARK
   ```
4. Text on dark backgrounds: use `SD_WHITE` for primary, `SD_MUTED` for secondary.
5. Nodes and shapes: stroke `SD_BLUE`, fill `SD_SURFACE` with opacity 0.8-0.9.
6. The chosen/winning path gets `SD_GREEN`. The rejected/losing path gets dimmed opacity.
7. CARBON animations use `SD_CARBON`. COIN uses `SD_COIN`. CLOCK uses `SD_CLOCK`.

---

## Three Currencies Visual Convention

When animating CLOCK / COIN / CARBON comparisons:

```python
# Currency labels
clock_label  = Text("CLOCK",  font_size=20, color=SD_CLOCK)
coin_label   = Text("COIN",   font_size=20, color=SD_COIN)
carbon_label = Text("CARBON", font_size=20, color=SD_CARBON)
```

Always show all three together. Never show fewer than three.
Order is always: CLOCK / COIN / CARBON (left to right, or top to bottom).

---

## Typography

ManimCE uses system fonts. Default `Text()` renders in the system sans-serif.
Do not specify custom fonts — they may not be available on all render hosts.

Font size conventions:
- Title / headline: 48-56pt
- Section label: 32-40pt  
- Node label: 20-28pt
- Caption / annotation: 16-20pt
- Fine print: 14pt minimum — below this is unreadable in video
