# UI kit

Built in Phase A session 1 in `app/web/ui-kit.js`, `ui-kit.css`, `charts.js`. Two globals, no build step: `UI` and `Charts`. Every component returns a DOM element; screens compose them with `UI.mount(target, ...elements)`. Live demo of every component: `/web/kit.html` (also `#/kit` in the shell). Screens add new components in their own commit, noted here.

A screen page includes, in this order: `/web/ui-kit.css`, `/web/ui-kit.js`, `/web/charts.js`, then its own `screen.js`. Set `data-screen="<slug>"` on `<body>` when the page is not served from `/screens/<slug>/`.

| Component | Props | Notes |
|---|---|---|
| `UI.tile` | name, plain, value, unit, window, freshness, delta, higher_is_better, unavailable_reason, fix, tone | value null or non-numeric renders "unavailable" plus the reason and "Connect: <fix>". unit: `$`, `%` (ratio 0 to 1), `x`, `ms`, `n`, or a plain suffix. delta is a ratio vs prior. tone: `good`, `bad`. |
| `UI.insight` | sentence, rule, severity (high, medium, low, info), capability, autonomy, evidence, stub, screen | renders `decisionRow` underneath when capability is set |
| `UI.decisionRow` | capability, autonomy (agent, founder_gate, human_assist), labels {agent, person, not_now}, stub, screen, current, onSaved | 3 buttons. Each opens the stub (what would happen, reason box), then `POST /api/decisions` with screen, capability, choice (agent, person, not_now), reason, autonomy. human_assist disables the agent button. |
| `UI.table` | columns [{key, label, unit, align, format}], rows, sort {key, dir} or false, maxRows, empty, onRow | tabular numbers, sticky header, click to sort, null cells show "unavailable". Returns an element with `.update(rows)`. |
| `Charts.bar` | labels, series [{name, values, color}], benchmark, benchmark_label, unit, title, note, stacked, values | null values draw a hatched stub |
| `Charts.line`, `Charts.step` | labels, series, benchmark, benchmark_label, unit, title, note, values | the line breaks at null |
| `Charts.funnel` | stages [{label, value, rate, benchmark}], breakAt, unit, title, note | widths to scale of the first stage; the break is the worst stage against its benchmark (or lowest rate) unless breakAt is given |
| `Charts.cohort` | rows [{label, values}], columns, unit, title, note | colour by value across the grid; null is a blank cell |
| `UI.filmstrip` | before {frames [{t, src}], loaded_at}, after {...}, seconds, markers [{t, label}], caption, before_label, after_label | ported from `speed_lab/build_founder_page.py`: one clock, play, restart, scrub |
| `UI.founderNote` | text (string or list of paragraphs) | the plain-English paragraph at the top of a screen |
| `UI.emptyState` | screen, title, text, missing (connector names), action {label, href or onClick} | what a screen shows before data lands |
| `UI.sampleBadge` | brand (optional, fetched from `/api/brand` if missing) | "Tallgrass Goods is a fictional brand with generated data" on every page |

Helpers: `UI.el(tag, attrs, ...children)`, `UI.mount(target, ...children)`, `UI.api(path, {method, body})` (throws on non-2xx), `UI.screen()` (slug from the URL), `UI.loadBrand()`, `UI.theme.get/set` (auto, light, dark, shared through localStorage), `UI.fmt.money/pct/ratio/int/num/compact/ms/date/ago/unit` (all return "unavailable" for a non-number).

Layout classes in `ui-kit.css`: `.screen` (page wrapper, 16px gutter on a phone), `.screen-head`, `.section` with an `h3` label, `.grid`, `.grid.tiles`, `.grid.two`, `.card`, `.row`, `.btn` (`primary`, `quiet`, `sm`), `.chip` (`good`, `warn`, `bad`, `accent`, `mono`). Colours are tokens on `:root` and switch for dark mode; charts use `--s1` to `--s6`.
