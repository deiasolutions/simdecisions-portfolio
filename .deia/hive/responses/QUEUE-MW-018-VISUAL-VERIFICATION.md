# Visual Verification Guide: Queue Task Card Display

## Component: QueueTaskCard (MW-018)

### Quick Verification Steps

1. **Start hivenode** (if not running):
   ```bash
   cd hivenode
   python -m hivenode.main
   ```

2. **Start browser dev server**:
   ```bash
   cd browser
   npm run dev
   ```

3. **Navigate to queue pane** (via mobile workdesk or build monitor EGG)

### Expected Visual Elements

#### Status Indicators
- **Active (Running)**: Blue spinning gear icon ⚙
- **Complete**: Green checkmark ✓
- **Failed**: Red X ✗
- **Queued**: Yellow clock ⏱

#### Metadata Row
Format: `model · bee_id · $cost · tokens · duration`
Example: `sonnet · BEE-001 · $0.042 · 5.2K · 2h 30m`

#### Progress Bar (Active Tasks Only)
- **Determinate** (task running >5min): Shows percentage (0-95%)
- **Indeterminate** (task <5min): Animated sliding bar
- **Hidden** (completed tasks): No progress bar shown

#### Card Layout
- **Mobile (<768px)**: Card with 12px padding, stacked metadata
- **Desktop (≥768px)**: Card with 8px padding, inline metadata

#### Expand/Collapse
- **Collapsed**: Shows summary with expand arrow ▶
- **Expanded**: Shows logs with collapse arrow ▼
  - Log entries with timestamps
  - Error messages for failed tasks (red background)
  - "No logs available" if messages array is empty

### Color Verification
All colors use CSS variables (Rule 3):
- Active: `var(--sd-blue)`
- Complete: `var(--sd-green)`
- Failed: `var(--sd-red)`
- Queued: `var(--sd-yellow)`
- Text: `var(--sd-text-primary)`, `var(--sd-text-muted)`
- Background: `var(--sd-bg)`, `var(--sd-bg-secondary)`, `var(--sd-bg-hover)`

### Responsive Behavior
1. **Open browser DevTools** (F12)
2. **Toggle device toolbar** (Ctrl+Shift+M)
3. **Switch between mobile (375px) and desktop (1200px)**
4. **Verify**:
   - Mobile: Card layout with stacked elements
   - Desktop: Optimized card with inline metadata
   - Resize triggers layout update immediately

### Accessibility Verification
1. **Keyboard navigation**:
   - Press Tab → card should receive focus (blue outline)
   - Press Enter/Space → card should expand
   - Press Enter/Space again → card should collapse

2. **Screen reader** (optional):
   - Status icons have aria-label ("Active", "Complete", "Failed")
   - Cards have aria-expanded attribute (true/false)
   - Progress bars have role="progressbar" with aria-valuenow

### Data Sources
Tasks are fetched from `/build/status` endpoint (hivenode):
- Active tasks: `status = "running" | "dispatched"`
- Completed tasks: `status = "complete"`
- Failed tasks: `status = "failed" | "timeout"`

### Known Limitations
- Progress percentage is heuristic-based (assumes 15min typical task)
- Queued specs still use old modal pattern (not QueueTaskCard)
- Desktop layout is optimized cards (not literal HTML table)
