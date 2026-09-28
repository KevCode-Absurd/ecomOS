# UI kit v2 (28 Sep 2026)

One premium look for an e-commerce operating system, in `app/web/ui-kit.css`, `ui-kit.js`, `charts.js` and `shell.js`. Two globals, no build step: `UI` and `Charts`. Every component returns a DOM element; screens compose them with `UI.mount(target, ...elements)`. Live demo of every component: `/web/kit.html` (`#/kit` in the shell). v1 names all still work. v2 adds the components the depth contract needs (`depth.md`). A screen that needs a new component adds it to `ui-kit.js` in its own commit and notes it here.

A screen page includes, in this order: `/web/ui-kit.css`, `/web/ui-kit.js`, `/web/charts.js`, then its own `screen.js`. Set `data-screen="<slug>"` on `<body>` when the page is not served from `/screens/<slug>/`.

## 1. Tokens

Colours are tokens on `:root`, redefined for dark mode under `prefers-color-scheme` and under `[data-theme="dark"]`. Screens never write a hex colour; they use the tokens.

| Group | Tokens | Light | Dark |
|---|---|---|---|
| Surfaces | `--ground`, `--surface`, `--sunken`, `--raised`, `--overlay` | cool near-white `#f3f5f8`, white cards | `#0b101a`, `#121827` |
| Ink | `--ink`, `--muted`, `--faint`, `--line`, `--line-strong` | navy ink `#0b1220` | `#e9edf5` |
| Accent | `--accent`, `--accent-strong`, `--accent-soft`, `--accent-line`, `--on-accent`, `--link` | cobalt `#1f4fe0` | `#7ea0ff` |
| Semantic | `--good`, `--warn`, `--bad`, `--info`, each with `-soft` | emerald, amber, crimson | brighter |
| Series | `--s1` to `--s6` and `--s1-soft` to `--s6-soft` | cobalt, teal, violet, amber, rose, slate | |
| Us and them | `--us`, `--them` | cobalt, slate | |
| Scales | `--cohort-lo/hi`, `--heat-lo/mid/hi` | white to cobalt | |
| Shape | `--r-lg` 16, `--r-md` 12, `--r-sm` 8, `--r-xs` 6; `--shadow`, `--shadow-lg` | | |
| Type | `--font` Inter with system fallback, `--mono` JetBrains Mono; `--fs-body` 14, `--fs-small` 12.5, `--fs-micro` 11.5 | | |

Type: one family. Headings 700 with tight tracking (h1 22, h2 16, h4 13.5). `h3` is the section kicker: 11px uppercase letter-spaced muted. Numbers are always `tabular-nums` (`.num`). Density: body 14/1.45, table cells 6 by 10 px, tiles 10 by 12 px, screen gap 18 px at desktop, 16 px gutter on a phone, max width 1240 px.

## 2. Components

### v2: the execution surface

| Component | Props | Notes |
|---|---|---|
| `UI.planBoard` | title, sub, orient (see orientation), actions (from `rank` or `master`), limit (10), screen, showScreen, onDecision, empty, tools, foot | Section 1 of every screen. Rank badge, title, owner chip, severity, why with numbers bolded, stake, rubric, "How it gets done" (expands the implementation block), Copy brief, decision row. Top 3 get the accent badge; critical gets the bad badge. |
| `UI.orientation` | items [{label, value, unit, delta, higher_is_better, tone, title}] | Small numbers beside a plan or a heading. Null renders "unavailable". Never the main content. |
| `UI.sectionHead` | title, sub, orient, tools | h2 with the window and rule line under it, orientation numbers and tool buttons to the right. |
| `UI.actionCard` | action, {expanded, compact, screen, showScreen, make {label, onClick}, extra, onDecision} | Title, severity, rubric, why, the implementation block (owner, steps with who, artefact with draft, win and stop rule, check date), stake, Copy brief, Make it, decision row. |
| `UI.implementation` | action | The block alone, for panels. |
| `UI.rubric`, `UI.rubricLegend` | {revenue, profit, reputation, satisfaction, ease, confidence, total} | Six boxes 0 to 5 and the total /100. n/a when a dimension has no input. |
| `UI.ownerChip`, `UI.ownerOf` | owner or action | "Agent does it", "Agent drafts, you approve", "A person does it". Owner comes from `action.owner`, else the capability's autonomy. |
| `UI.decisionRow` (extended) | capability (id or {id, autonomy}), autonomy, owner, labels, screen, stub, current, onSaved, compact, finding_id | Three buttons still log `agent`, `person`, `not_now` to `POST /api/decisions` (now with `finding_id`). The first button reads "Agent does it" or "Agent drafts, I approve" from the owner and is disabled when a person must do it. |
| `UI.coverageMatrix` | rows [{key, label, sub}], cols [{key, label}], cells {row: {col: {us, them, unit, n, share}}}, unit, single, max, gapRule, action {label, onClick(cell, row, col)}, onCell, totals, corner, title, tools, note | Us against them in every cell. Missing cell reads "not tried" and is a gap. Default gap rule: they run it and we do not (red), we lead (green), we are 1.5x ahead (amber, check waste). Gap cells show the action button. `single: true` makes a heatmap (one measure, colour by `max`). |
| `UI.verdictTable`, `UI.verdict` | table props plus verdict {key, kind(row), text(row), reason(row), at}, reason {key, label, text(row)}, actions {label or label(row), onClick(row), cls} or per-row `row.actions` | A table where every row has a verdict chip (scale, watch, cut, keep, fix, stop, wait, new, na), the reason in numbers, and an action button. Sorting keeps the chips. |
| `UI.tabs` | items [{key, label, n, panel (element or fn)}], current, onChange | Jobs inside a section. Returns an element with `.show(key)`. |
| `UI.pills` | items [{key, label, n}], current, multi, onChange | Filters. Selected pill is ink. |
| `UI.panel` | title, body, tools, onClose | Side drawer for one entity's detail and its actions. Escape or backdrop closes. Returns the backdrop with `.close()`. |
| `UI.field` | key, name, sub, text, tier, source, date, confidence, used_by, placeholder, multiline, onSave(text) => Promise<{flows_to}>, onSaved | An editable brain fact. Shows tier, source and date; Edit turns it into a textarea; "Save as approved" calls onSave, which writes an approved founder record. |
| `UI.dropZone` | accept, hint, onFiles(files), onUrl(url), urlPlaceholder | Drop, choose or paste a url. |
| `UI.timeline` | items [{when, who, title, text, tone}] | Decisions, changes, launches. |
| `UI.copyButton`, `UI.copy`, `UI.csv`, `UI.briefText` | | Copy to clipboard with "Copied"; CSV download of rows and columns; the plain-text brief of an action. |
| `UI.sevChip`, `UI.escapeHtml` | | Helpers. |

### v1, restyled, same props

| Component | Props | Notes |
|---|---|---|
| `UI.tile` | name, plain, value, unit, window, freshness, delta, higher_is_better, unavailable_reason, fix, tone | Orientation only from round 1. Add class `sm` for a smaller tile. |
| `UI.insight` | sentence, rule, severity (critical, high, medium, low, info), capability, autonomy, evidence, stub, screen | Renders the decision row when capability is set. |
| `UI.table` | columns [{key, label, unit, align, format}], rows, sort, maxRows, empty, onRow | Tabular numbers, sticky header, sortable, null shows "unavailable". `.update(rows)`. Add class `dense` on the table for tighter rows. |
| `UI.filmstrip`, `UI.founderNote`, `UI.emptyState`, `UI.sampleBadge` | unchanged | |

Helpers unchanged: `UI.el`, `UI.mount`, `UI.api`, `UI.screen`, `UI.loadBrand`, `UI.theme`, `UI.fmt.*`.

## 3. Charts

All charts are plain SVG from arrays, theme-aware, `null` means unavailable (hatched bar, broken line, blank cell). Every chart takes `title` and `note`; the note is the caveat and is not optional on a screen.

| Chart | Props | Right when |
|---|---|---|
| `Charts.bar` | labels, series, benchmark, benchmark_label, unit, stacked, values, shade [i0, i1] | One measure over categories or time, with the benchmark drawn. `shade` marks the selected window. |
| `Charts.line`, `Charts.step` | labels, series, benchmark, unit, values, shade | Trend with a benchmark. |
| `Charts.funnel` | stages [{label, value, rate, benchmark}], breakAt | Stage drop with the break marked. |
| `Charts.cohort` | rows [{label, values}], columns, unit | Behaviour of a group since a start. |
| `Charts.positioningMap` | x {label, lo, hi, min, max, unit}, y {...}, points [{label, x, y, us, size, gap, note}], quadrants [tl, tr, bl, br], midX, midY, usLabel, themLabel | Where we sit against competitors or where avatars sit against what we serve. Empty quadrants named; `gap: true` draws a dashed marker. Axes come from the brain. |
| `Charts.trendStrip` | rows [{label, sub, values, unit, higher_is_better, band [lo, hi], delta_label}] | Many metrics in little space, orientation only. |
| `Charts.waterfall` | steps [{label, value, kind: total, up, down, sub, sub (small label)}], unit | A total decomposed into steps: revenue bridge, margin stack, budget moves. |

Chart CSS classes: `.shade`, `.bench`, `.hatch`, `.pmap`, `.wf`, `.trend`. Series colours are `--s1` to `--s6` in order; us is `--us`, them is `--them`.

## 4. Layout classes

`.screen`, `.screen-head`, `.section` with an `h3` kicker, `.sec-head`, `.grid` (`tiles`, `two`, `three`, `side`), `.card` (`flat`, `sunken`, `tight`), `.row` (`between`, `end`), `.stack`, `.divider`, `.btn` (`primary`, `soft`, `quiet`, `danger`, `sm`, `xs`, `pill`, `sel`), `.chip` (`good`, `warn`, `bad`, `accent`, `ink`, `mono`, `dot`, `owner agent|draft|person`), `.verdict`, `.pills`, `.tabs`, `.plan`, `.action`, `.matrix`, `.field`, `.drop`, `.timeline`, `.scale-legend`, `.kicker`, `.muted`, `.faint`, `.small`, `.micro`, `.num`, `.na`, `.mono`. Print styles hide buttons and keep cards whole.

## 5. Rules for screens

- Section order from `depth.md` section 2: head, plan, what is wrong, actions, implementation, desk, audit, notes.
- No hex colours, no inline font sizes, no new fonts. Tokens and classes only.
- Every number through `UI.fmt`. Every chart with a note. Every action with a decision row.
- Phone width first: everything wraps at 360 px with a 16 px gutter and no horizontal page scroll (matrices and tables scroll inside their wrapper).
- The shell nav shows "To approve N" from the master list; a screen never duplicates the shell.
