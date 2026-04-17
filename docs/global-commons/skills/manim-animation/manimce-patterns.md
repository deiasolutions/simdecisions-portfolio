# ManimCE Patterns Reference
# manim-animation skill v1.0
# Target: ManimCE v0.18+

---

## Imports

```python
from manim import *
```

This imports everything. Do not import selectively — Manim's namespace is
designed for wildcard import.

---

## Scene Skeleton

```python
"""
[Module docstring — see SKILL.md for required fields]
"""

# Brand constants — always first
SD_DARK    = "#0D0F14"
SD_SURFACE = "#161B22"
SD_BLUE    = "#4A9EFF"
SD_GREEN   = "#3DDC84"
SD_AMBER   = "#FFB347"
SD_WHITE   = "#E8EAF0"
SD_MUTED   = "#6B7280"
SD_CARBON  = "#8B5CF6"
SD_RED     = "#FF6B6B"

from manim import *

class MyScene(Scene):
    def construct(self):
        self.camera.background_color = SD_DARK
        # scene content here
```

---

## Text Objects

```python
# Plain text
label = Text("Hello", font_size=36, color=SD_WHITE)

# Multiline
label = Text("Line one\nLine two", font_size=28, color=SD_MUTED)

# Math (only when task requires it)
eq = MathTex(r"\sum_{n=1}^\infty \frac{1}{n^2}", color=SD_BLUE)
```

Text does not wrap automatically. Use `\n` for line breaks.

---

## Shapes

```python
# Rectangle
box = Rectangle(width=3, height=1.5, color=SD_BLUE)
box.set_fill(SD_SURFACE, opacity=0.8)

# Rounded rectangle
box = RoundedRectangle(corner_radius=0.2, width=3, height=1.5, color=SD_BLUE)
box.set_fill(SD_SURFACE, opacity=0.8)

# Circle
dot = Circle(radius=0.3, color=SD_GREEN)
dot.set_fill(SD_GREEN, opacity=1.0)

# Arrow
arrow = Arrow(start=LEFT * 2, end=RIGHT * 2, color=SD_BLUE)

# Line
line = Line(start=UP, end=DOWN, color=SD_MUTED)
```

---

## Positioning

```python
# Absolute positions
obj.move_to(ORIGIN)           # center
obj.move_to(LEFT * 3)         # 3 units left
obj.move_to(UP * 2 + RIGHT)   # compound

# Edge positioning
obj.to_edge(UP)               # top edge with default buffer
obj.to_edge(DOWN, buff=0.5)   # bottom edge, custom buffer
obj.to_corner(UL)             # upper left corner

# Relative positioning
obj.next_to(other, DOWN)              # below other
obj.next_to(other, RIGHT, buff=0.3)   # right of other, custom gap
obj.align_to(other, LEFT)            # align left edges
```

Direction constants: `UP`, `DOWN`, `LEFT`, `RIGHT`, `UL`, `UR`, `DL`, `DR`, `ORIGIN`

Frame bounds (default Scene): approximately ±7 wide, ±4 tall. Keep objects
within ±6 wide, ±3.5 tall to avoid clipping.

---

## Grouping

```python
# VGroup — vertical group, positions relative to each other
group = VGroup(label, box, arrow)
group.arrange(DOWN, buff=0.3)     # stack vertically
group.arrange(RIGHT, buff=0.5)    # stack horizontally
group.move_to(ORIGIN)             # position the group

# Adding objects together
combined = VGroup(obj1, obj2)
```

Call `.arrange()` before adding to scene or playing animations.

---

## Animations

```python
# Appear animations
self.play(FadeIn(obj))
self.play(FadeIn(obj, shift=UP))       # fade in from below
self.play(Write(text_obj))             # draw text stroke by stroke
self.play(Create(shape))               # draw shape outline
self.play(GrowArrow(arrow))            # grow arrow from tail

# Disappear animations
self.play(FadeOut(obj))
self.play(FadeOut(obj, shift=DOWN))

# Transform
self.play(Transform(obj_a, obj_b))     # morphs a into b; a is consumed
self.play(ReplacementTransform(a, b))  # a replaced by b; cleaner

# Move
self.play(obj.animate.move_to(RIGHT * 3))
self.play(obj.animate.scale(1.5))
self.play(obj.animate.set_color(SD_GREEN))

# Multiple simultaneous
self.play(FadeIn(obj1), FadeIn(obj2))

# Staggered
self.play(LaggedStart(
    FadeIn(obj1),
    FadeIn(obj2),
    FadeIn(obj3),
    lag_ratio=0.3
))

# Timed
self.play(FadeIn(obj), run_time=2.0)   # slow fade
```

---

## Timing

```python
self.wait(1)       # 1 second pause
self.wait(2.5)     # fractional seconds OK
self.wait(0)       # zero wait — valid, useful for sync
```

Narration pace: ~2.5 words per second at normal speed.
A 10-word narration line needs at least `self.wait(4)` after it.

---

## Camera

Default Scene has a fixed camera. Do not use MovingCameraScene or
ThreeDScene unless explicitly required by the task file.

```python
# Zoom (MovingCameraScene only — avoid unless required)
self.play(self.camera.frame.animate.scale(0.5))
```

---

## Common Patterns

### Node with label

```python
def make_node(label_text, color=SD_BLUE):
    box = RoundedRectangle(corner_radius=0.15, width=2.5, height=0.8)
    box.set_stroke(color, width=2)
    box.set_fill(SD_SURFACE, opacity=0.9)
    label = Text(label_text, font_size=22, color=SD_WHITE)
    label.move_to(box.get_center())
    return VGroup(box, label)
```

### Flow with arrows

```python
node_a = make_node("DEF")
node_b = make_node("SIM")
node_a.move_to(LEFT * 3)
node_b.move_to(ORIGIN)
arrow = Arrow(node_a.get_right(), node_b.get_left(), color=SD_MUTED)

self.play(FadeIn(node_a))
self.play(GrowArrow(arrow))
self.play(FadeIn(node_b))
```

### Side-by-side comparison

```python
left_group.move_to(LEFT * 3.5)
right_group.move_to(RIGHT * 3.5)
divider = Line(UP * 3, DOWN * 3, color=SD_MUTED, stroke_width=1)
divider.move_to(ORIGIN)

self.play(
    FadeIn(left_group),
    FadeIn(divider),
    FadeIn(right_group)
)
```

### Highlight winner

```python
# Dim loser, brighten winner
self.play(
    left_group.animate.set_opacity(0.3),
    right_group.animate.set_color(SD_GREEN)
)
```

---

## Debugging Tips

- Run with `-ql` first — much faster than `-qh`
- Add `-p` to auto-open the video after render
- Manim errors point to the exact line — read them carefully
- If objects disappear unexpectedly, check for accidental `FadeOut` or `Transform` consuming them
- If text is clipped, reduce font size or use `\n` to break lines
- Use `self.add(obj)` to add without animation (useful for static backgrounds)
