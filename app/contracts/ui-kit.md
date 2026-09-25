# UI kit

Built once in round 0 in `app/web/ui-kit.js`, `ui-kit.css`, `charts.js`. Screens compose these and add new ones in their own commit, noted here.

| Component | Props | Notes |
|---|---|---|
| `tile` | name, plain, value, unit, window, freshness, unavailable_reason | shows "unavailable" plus the connector that fixes it |
| `insight` | sentence, rule, severity, capability, autonomy | renders the decision row underneath |
| `decisionRow` | capability, autonomy, labels | 3 buttons; writes to `decisions` with screen, capability, choice, reason, time |
| `table` | columns, rows, sort | tabular numbers, sticky header |
| `chart.bar`, `chart.line`, `chart.step`, `chart.funnel`, `chart.cohort` | series, labels, benchmark line | drawn to scale, theme-aware |
| `filmstrip` | before frames, after frames, load markers | ported from `speed_lab/build_founder_page.py` |
| `founderNote` | text | the plain-English paragraph at the top of a screen |
| `emptyState` | screen, missing connectors, first action | what a screen shows before data lands |
| `sampleBadge` | brand | "Tallgrass Goods is a fictional brand with generated data" on every page |
