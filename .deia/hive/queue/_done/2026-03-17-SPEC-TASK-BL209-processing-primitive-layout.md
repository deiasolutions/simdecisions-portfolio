# BL-209: Processing primitive - file browser + processing window + code editor layout

## Objective
Create the Processing primitive EGG layout: a three-pane layout with file browser (left), processing/p5 canvas (center), and code editor (right).

## Context
Processing (p5.js creative coding) needs its own EGG layout. Left pane: tree-browser for sketch files. Center: canvas/p5 rendering window. Right: code editor for sketch source. Similar to the turtle-draw concept but for Processing/p5.js sketches.

## Files to Read First
- `eggs/turtle-draw.egg.md` (similar concept)
- `eggs/code.egg.md` (code editor reference)
- `browser/src/primitives/canvas/`
- `browser/src/primitives/tree-browser/`
- `browser/src/shell/eggToShell.ts`

## Deliverables
- [ ] Create or update processing EGG config (eggs/processing.egg.md)
- [ ] Three-pane layout: tree-browser | canvas | code-editor
- [ ] Correct pane ratios and app type assignments
- [ ] Tests for EGG parsing and layout structure

## Acceptance Criteria
- [ ] ?egg=processing loads three-pane layout
- [ ] Left pane shows file browser
- [ ] Center pane shows canvas/rendering area
- [ ] Right pane shows code editor
- [ ] Tests pass

## Smoke Test
- [ ] `cd browser && npx vitest run --reporter=verbose src/shell/__tests__/eggToShell.test.ts`
- [ ] `cd browser && npx vitest run`

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs

## Model Assignment
haiku

## Priority
P0
