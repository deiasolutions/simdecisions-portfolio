# SPEC: Chart Primitive (P-14) — Recharts

## Priority
P0

## Backlog
BL-TBD

## Objective
Build the chart pane primitive using Recharts (MIT licensed, built on D3, React-native components). Renders line, bar, area, scatter, pie, radar, gauge, and treemap charts. Subscribes to relay bus events for live dashboard updates. Registers as appType "chart" in the app registry.

## Context
The chart primitive is used by 20 of our planned products — the #2 unbuilt primitive. Recharts is built on D3, React-native (components not imperative), responsive, animated, and already in the dependency tree.

Files to read first:
- `browser/src/apps/index.ts` — app registry
- `browser/src/apps/canvasAdapter.tsx` — adapter pattern to follow
- `browser/src/infrastructure/relay_bus/` — bus API
- `browser/package.json` — verify recharts is available, install if not

## Dependencies to Install
```bash
cd browser
npm install recharts  # if not already present
```

## File Structure
```
browser/src/primitives/chart/
├── ChartApp.tsx             # Main chart component with type switching
├── chart.css                # var(--sd-*) theme colors for Recharts
├── chartTypes.ts            # TypeScript types for chart config
├── resolveThemeColors.ts    # CSS variable → hex resolver for SVG rendering
├── charts/
│   ├── LineChartView.tsx     # Line + Area chart renderer
│   ├── BarChartView.tsx      # Bar chart renderer (vertical + horizontal)
│   ├── ScatterChartView.tsx  # Scatter plot renderer
│   ├── PieChartView.tsx      # Pie + Donut chart renderer
│   ├── RadarChartView.tsx    # Radar/spider chart renderer
│   ├── GaugeView.tsx         # Single-value gauge (custom, built from Recharts PieChart)
│   └── TreemapView.tsx       # Treemap renderer
├── busSubscriber.ts         # Bus event subscription + time-window buffer
└── __tests__/
    ├── ChartApp.test.tsx
    ├── LineChartView.test.tsx
    ├── BarChartView.test.tsx
    ├── PieChartView.test.tsx
    ├── GaugeView.test.tsx
    ├── busSubscriber.test.ts
    └── chartAdapter.test.ts

browser/src/apps/
├── chartAdapter.ts          # App registry adapter (follows existing adapter pattern)
```

## CSS Variable Resolution for SVG

**Critical implementation detail.** Recharts renders to SVG. SVG `fill` and `stroke` attributes do NOT resolve CSS variables natively. The bee MUST resolve CSS variables to computed hex values at render time:

```typescript
// resolveThemeColors.ts
export const resolveVar = (varName: string): string =>
  getComputedStyle(document.documentElement).getPropertyValue(varName).trim();
```

Call once on mount and on theme change. Pass resolved hex strings to Recharts component props. Store resolved colors in component state or a memo. Re-resolve on theme change events.

## Acceptance Criteria

### Chart Type Rendering
- [ ] **Line chart**: single or multi-series, dots optional, area fill optional, curved or linear interpolation
- [ ] **Bar chart**: vertical or horizontal, stacked or grouped, single or multi-series
- [ ] **Area chart**: same as line but with fill under the curve
- [ ] **Scatter plot**: X/Y data points, optional size dimension (bubble chart), optional color dimension
- [ ] **Pie chart**: standard pie or donut (innerRadius config), labels inside or outside
- [ ] **Radar chart**: multi-axis spider/radar, filled or outline
- [ ] **Gauge**: single-value semicircle gauge with min/max/current, color zones (thresholds via var(--sd-*))
- [ ] **Treemap**: hierarchical rectangles, sized by value, colored by category
- [ ] Chart type switchable at runtime via config or bus message

### Data Format
- [ ] Accepts data as JSON array:
  ```json
  [
    { "name": "Jan", "revenue": 4000, "cost": 2400 },
    { "name": "Feb", "revenue": 3000, "cost": 1398 },
    { "name": "Mar", "revenue": 2000, "cost": 9800 }
  ]
  ```
- [ ] Auto-detects axes from data keys (first string key = X axis category, numeric keys = Y axis series)
- [ ] Manual axis config available in EGG:
  ```yaml
  config:
    chartType: line
    xAxis: name
    series:
      - dataKey: revenue
        color: var(--sd-accent)
        label: Revenue
      - dataKey: cost
        color: var(--sd-warning)
        label: Cost
  ```
- [ ] Gauge data format: `{ "value": 73, "min": 0, "max": 100, "label": "CPU Usage", "unit": "%" }`
- [ ] Treemap data format (nested objects, Recharts Treemap accepts this natively):
  ```json
  [
    { "name": "Engineering", "value": 50, "children": [
      { "name": "Frontend", "value": 30 },
      { "name": "Backend", "value": 20 }
    ]},
    { "name": "Design", "value": 20 }
  ]
  ```

### Responsive + Animated
- [ ] Chart fills available pane space (ResponsiveContainer from Recharts)
- [ ] Resizes when pane resizes — no overflow, no clipping
- [ ] Entry animation on first render (Recharts default animations)
- [ ] Smooth transitions when data updates (Recharts handles this)

### Interactive Features
- [ ] Tooltip on hover: shows data point values
- [ ] Legend: shows series names with color indicators, clickable to toggle series visibility
- [ ] Click on data point: publish `chart:point-clicked { seriesKey, dataIndex, value }` to bus
- [ ] Zoom: optional X-axis brush/zoom control (Recharts Brush component) when config.zoomable: true

### Bus Integration — Live Data (DEFERRED — depends on ADR-RTD-001 implementation)

**RTD = Real-Time Display Value.** Every headless or visible service publishes named metrics to the platform bus. Format: `{service_id, metric_key, value, unit, currency?, timestamp}`. Emitted on state change, not on a timer. Defined in ADR-RTD-001 (2026-03-18). Not yet built in code.

Build the bus subscriber infrastructure now — the subscribe config, time window, and ring buffer — but wire it to regular bus events. When RTD lands, the subscription code works unchanged. For smoke testing, use build monitor heartbeat events as the test producer.

- [ ] **Bus subscription**: config `subscribe` array of metric_key patterns
  ```yaml
  config:
    chartType: line
    subscribe:
      - metric_key: "RTD:cost_coin"
        seriesLabel: "Cost (USD)"
      - metric_key: "RTD:elapsed"
        seriesLabel: "Time (ms)"
    timeWindow: 300  # seconds — rolling window, oldest data drops off
  ```
- [ ] Each matching bus event appended as a new data point with timestamp as X axis
- [ ] Rolling time window: when `timeWindow` is set, data older than N seconds drops off the left edge
- [ ] Buffer: accumulate up to 1000 data points per series, then start dropping oldest (ring buffer)
- [ ] No polling — bus subscription only. Events arrive via relay_bus, chart reacts.

### Bus Integration — Commands
- [ ] Listen for `chart:load-data { data, config? }` — replaces current data entirely
- [ ] Listen for `chart:append-data { data }` — adds new data points to existing series
- [ ] Listen for `chart:set-type { chartType }` — switches chart type (re-renders same data in new format)
- [ ] Listen for `chart:clear` — empties the chart
- [ ] Publish `chart:point-clicked { seriesKey, dataIndex, value }` on click

### Recharts Theme Override
- [ ] ALL Recharts colors use var(--sd-*) CSS variables, resolved via `resolveThemeColors.ts` to hex values for SVG rendering
- [ ] Default series color palette (6 colors, with modulo cycling for 7+ series):
  ```css
  :root {
    --sd-chart-series-1: var(--sd-accent);
    --sd-chart-series-2: var(--sd-warning);
    --sd-chart-series-3: var(--sd-success);
    --sd-chart-series-4: var(--sd-error);
    --sd-chart-series-5: var(--sd-info);
    --sd-chart-series-6: var(--sd-text-secondary);
  }
  ```
- [ ] 7+ series: cycle back to series-1 with 20% opacity shift. Series 7 = series-1 at 80% opacity, series 8 = series-2 at 80%, etc. Simple modulo with opacity step-down.
- [ ] Grid lines: var(--sd-border)
- [ ] Axis labels: var(--sd-text-secondary)
- [ ] Tooltip background: var(--sd-surface-secondary)
- [ ] Tooltip text: var(--sd-text-primary)
- [ ] Tooltip border: var(--sd-border)
- [ ] Legend text: var(--sd-text-secondary)
- [ ] No hardcoded hex, rgb, or named colors anywhere

### App Registry
- [ ] Register `appType: "chart"` in `browser/src/apps/index.ts`
- [ ] Adapter at `browser/src/apps/chartAdapter.ts` — follows same pattern as other adapters
- [ ] Accepts config from EGG:
  ```yaml
  - type: app
    appType: chart
    nodeId: cost-chart
    config:
      chartType: line
      title: "Cost Over Time"
      xAxis: timestamp
      series:
        - dataKey: coin
          label: "USD"
          color: var(--sd-accent)
      subscribe:
        - metric_key: "RTD:cost_coin"
      timeWindow: 600
      zoomable: true
  ```

### Empty + Loading + Error States
- [ ] Empty state: centered text "No data" with subtle chart icon, uses var(--sd-text-secondary)
- [ ] Loading state: spinner while data loads
- [ ] Error state: "Failed to render chart" with error details if data format is wrong

### Gauge Details (Custom Component)
- [ ] Built as custom component using Recharts PieChart with startAngle/endAngle
- [ ] Semicircle layout: 180 to 0 arc
- [ ] Default style: `gaugeStyle: "fill"` (alternative: `"needle"`)
- [ ] Color zones configurable:
  ```yaml
  config:
    chartType: gauge
    zones:
      - min: 0
        max: 50
        color: var(--sd-success)
      - min: 50
        max: 80
        color: var(--sd-warning)
      - min: 80
        max: 100
        color: var(--sd-error)
  ```
- [ ] Large center number showing current value
- [ ] Label and unit below the number

## EGG Examples

### Live Cost Dashboard
```yaml
egg: cost-dashboard
layout:
  type: split
  direction: vertical
  ratio: [60, 40]
  children:
    - type: app
      appType: chart
      config:
        chartType: line
        title: "Token Cost Over Time"
        subscribe:
          - metric_key: "RTD:cost_coin"
            seriesLabel: "USD"
        timeWindow: 3600
    - type: split
      direction: horizontal
      ratio: [33, 33, 34]
      children:
        - type: app
          appType: chart
          config:
            chartType: gauge
            title: "Budget Used"
            subscribe:
              - metric_key: "RTD:budget_pct"
            zones:
              - { min: 0, max: 60, color: "var(--sd-success)" }
              - { min: 60, max: 80, color: "var(--sd-warning)" }
              - { min: 80, max: 100, color: "var(--sd-error)" }
        - type: app
          appType: chart
          config:
            chartType: pie
            title: "Cost by Model"
        - type: app
          appType: chart
          config:
            chartType: bar
            title: "Tasks by Status"
```

### Simulation Results
```yaml
# After sim run, terminal sends chart:load-data with results
- type: app
  appType: chart
  nodeId: sim-results
  config:
    chartType: bar
    title: "Resource Utilization"
    xAxis: resource_name
    series:
      - dataKey: utilization
        label: "Utilization %"
      - dataKey: wait_time
        label: "Avg Wait (min)"
```

## Smoke Test
- [ ] Load an EGG with appType: chart — renders empty state
- [ ] Send `chart:load-data` with 10 data points — line chart renders
- [ ] Switch type via `chart:set-type { chartType: "bar" }` — same data renders as bar chart
- [ ] Subscribe to bus events with metric_key — data points appear (use build monitor heartbeats as test producer)
- [ ] Hover data point — tooltip shows
- [ ] Click legend item — series toggles visibility
- [ ] Resize pane — chart resizes responsively
- [ ] Gauge renders with color zones and center value

## Model Assignment
sonnet

## Constraints
- Recharts only — do not import D3 directly, Chart.js, or Plotly. Recharts is the standard for this project.
- Each chart type is a separate sub-component file under charts/. ChartApp.tsx switches between them. No file over 500 lines.
- The gauge is a custom component because Recharts doesn't have one built-in. Build it from Recharts PieChart with angle constraints. Do NOT import a separate gauge library.
- All colors via var(--sd-*), resolved to hex via resolveThemeColors.ts for SVG. Zero hardcoded colors. The series color palette MUST use CSS variables so it adapts to theme changes.
- Dynamic import for chart sub-components: `React.lazy(() => import('./charts/LineChartView'))` — don't load all chart types if only one is used.

## Test Requirements
- 3+ tests for ChartApp (render, type switching, empty state)
- 2+ tests for LineChartView (render with data, responsive resize)
- 2+ tests for BarChartView (vertical, horizontal)
- 2+ tests for PieChartView (standard, donut)
- 2+ tests for GaugeView (render, color zones)
- 3+ tests for busSubscriber (subscribe, time window, ring buffer, append)
- 2+ tests for chartAdapter (registration, config parsing)
- Total: 16+ tests minimum
