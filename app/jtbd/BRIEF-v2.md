# Jobs to be done, second list: the brief for the drafting agents

Date 29 Sep 2026. This is an alternate list to `BRIEF.md`, written the way Competing Against Luck defines a job. Read `BOOK-NOTES.md` first and follow it. Nothing here is a feature. Do not design or build anything.

## The lens

A founder or agency owner hires a screen the way they hire an expert or an agency: to make progress in a moment of struggle, and to take the complexity off their desk. A job is the progress they want in a particular circumstance. It has a functional side, an emotional side and a social side. It is written in verbs and nouns, never adjectives. The things they could hire instead come from different categories: an agency, a freelancer, a spreadsheet, a weekly call, their gut, or doing nothing. If only a screen like ours could do it, it is a feature, not a job; cut it.

Every job must name what the owner hires today, what has to be fired, the anxiety that stops them switching, and the metric that shows the progress. Revenue and gross profit both count as the top of the metric chain.

## What to write

For each screen, 35 ranked jobs. Aim for exactly 35. If you honestly run out, stop, but do not pad with adjectives or with features dressed as jobs. Rank 1 is the job the owner would fire the screen for not doing.

One record per job:

```json
{
  "rank": 1,
  "job": "When ad spend is up and revenue is flat on a Monday, tell me by noon whether to cut or hold, and which ad sets, so I do not burn the week's budget",
  "circumstance": "Monday morning, weekly numbers in, spend up 20 percent, revenue flat, a media buyer waiting for a decision",
  "progress": {
    "functional": "know which ad sets are losing money and by how much",
    "emotional": "stop dreading the Monday numbers; feel in control of the budget",
    "social": "give the buyer a clear call and look decisive to a partner or client"
  },
  "hire_today": "an agency's Monday call, or a spreadsheet of last week's ROAS, or gut feel",
  "fire": "the Monday call and the spreadsheet; the habit of waiting a week to see",
  "forces": {
    "push": "money is leaving every day the decision waits",
    "pull": "a ranked list of losers with dollars at stake and one button each",
    "habit": "the agency has always made this call",
    "anxiety": "what if I cut an ad set that was about to turn; what if the numbers are wrong"
  },
  "little_hire": "every Monday, and any day spend jumps",
  "watch": {"metric": "cost per purchase against the floor, by ad set, 7 day", "unit": "currency", "source": "Meta Ads Manager"},
  "drives": {"metric": "blended cost per new customer, 28 day", "unit": "currency"},
  "business": "gross profit",
  "now_after": "Example. Now: 40 percent of spend sits in ad sets above the floor. After: under 10 percent within 14 days, with the cut and hold decisions logged.",
  "score": {"money": 5, "struggle": 5, "satisfaction": 4, "speed": 5, "ease": 4},
  "not_for": "a store spending under a few hundred a month, where a weekly look is enough"
}
```

Fields:
- `job`: one sentence from the owner's mouth. Starts with "When" and the circumstance, then "help me" or "tell me" or "make", then the progress, then "so I" and the outcome. Verbs and nouns. No feature names.
- `circumstance`: one line. When, where, what just happened, who is waiting, what pressure.
- `progress`: the three dimensions. Each one line. If a dimension is honestly absent, write "none".
- `hire_today`: what the owner hires now for this job without our software. Name the category: agency, freelancer, in-house role, tool, spreadsheet, gut, a friend, nothing. "Nothing" means nonconsumption, and it matters: say why they do nothing.
- `fire`: what must be fired for the screen to be hired. Something always has to be fired.
- `forces`: push, pull, habit, anxiety. One phrase each. The anxiety is the one the screen must remove before the owner trusts it.
- `little_hire`: the recurring moment they would come back for. Daily, weekly, before a launch, when a number jumps.
- `watch`: the first metric that shows the progress, the way the owner would check it. Must be observable in a connected store or the brand brain. Say the window.
- `drives`: the metric one level up. `business`: revenue, gross profit, contribution margin, cash, customer satisfaction or risk.
- `now_after`: one line with an example number, marked as an example.
- `score`: 1 to 5 each. money = gross profit impact. struggle = how badly they want it solved today, with evidence: workarounds, nonconsumption, hours lost, sleepless nights (5 = they have built a workaround or lie awake; 1 = mild). satisfaction = effect on the customer's experience or the founder's peace of mind. speed = how fast the watch metric moves after acting. ease = how little effort or money it takes to act.
- `not_for`: who should not hire this job from the screen, in one line. A job hired for the wrong reason gets fired.

Total = 3 x money + 3 x struggle + 2 x satisfaction + 1 x speed + 1 x ease, maximum 50. Rank by total, then judgement. A job where `hire_today` is "nothing" and the struggle is real ranks above a job with the same total.

Per screen, also write:
- `purpose`: the purpose-brand line. "When [circumstance], open [screen] to [progress]." One sentence.
- `fires`: what the owner fires when they hire this screen well. One line. The agency's report, the weekly call, the spreadsheet, the gut feel, the not looking.
- `not_for`: who should not hire this screen at all. One line.

## Ground it

Read, in this order, and nothing else:
1. `app/jtbd/BOOK-NOTES.md`.
2. `app/screens/<slug>/CLAUDE.md`.
3. The room file it points to in `agents/rooms/*.rooms.json`.
4. `app/jtbd/<slug>.json`, the first list. Use it as raw material for what the screen covers. Do not copy its jobs. Rewrite each one from inside a moment, drop the ones that are features, and find the ones the first list missed: negative jobs (things the owner does not want to do), nonconsumption (things nobody does today), workarounds, unusual uses.
5. The matching idea bank file in `ideas/v1/` and `ideas/README.md` for the metric vocabulary.

No web searches needed. Depth over breadth.

For research-type screens (market research, competitors, customers), still include: is the category growing or shrinking, quarter by quarter; where we grow slower than the market; input costs rising or falling; allied categories growing; emerging trends to catch early; the competitive forces in plain words; where consumers are moving from and to. Each as a job with a moment and a metric.

## Writing rules

Short sentences. Plain words. Digits. No em dashes. No jargon. No adjectives as jobs. The reader is a founder or agency owner who would recognise the moment.

## Output

Write `app/jtbd/v2/<slug>.json`: `{"screen": "<slug>", "title": "<screen title>", "purpose": "...", "fires": "...", "not_for": "...", "jobs": [ ... ]}`. Valid JSON. Nothing else on disk. Report the file paths and the count per screen, and name any job from the first list you cut as a feature and why.
