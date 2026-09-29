# Jobs to be done, per screen: the brief for the drafting agents

Date 29 Sep 2026. Owner Kevin. Nothing here is a feature. Do not design anything, do not build anything.

## The lens

An e-commerce business exists to make money: pay the team, last, serve more customers, enrich the owner. Everything else is second. A founder or agency owner hires a screen the way they would hire an expert: to get a job done that moves money, and to take the complexity off their desk.

So for each screen, answer: why would a business owner hire this expert? What are the jobs they expect done? The Meta ads expert is hired to put the right message in front of the right customer at the right time so the account returns the most gross profit per dollar spent. The page speed expert is hired so a shopper sees the product before they lose patience, which shows up as bounce rate, then conversion rate, then revenue.

Every job must be tied to a metric the owner can watch move: where they are now, what they will do, where the number should go. If the metric is not directly observable, name the closest proxy and say so.

## What to write

For each screen, a ranked list of its jobs to be done. Aim for 25. Fewer if the screen honestly has fewer; never pad. Rank 1 is the job the owner would fire the screen for not doing.

One record per job:

```json
{
  "rank": 1,
  "job": "Stop paying for clicks that never convert",
  "why": "One or two sentences. What the owner is trying to get done and what happens if it is not done. Plain words. Concrete.",
  "watch": {"metric": "cost per purchase, 7 day", "unit": "currency", "source": "Meta Ads Manager"},
  "drives": {"metric": "blended cost per new customer", "unit": "currency"},
  "business": "gross profit",
  "now_after": "Now: cost per purchase is 2.1x the floor on 40% of spend. After: paused or rebuilt ad sets bring the account under the floor within 14 days.",
  "score": {"money": 5, "satisfaction": 2, "speed": 4, "ease": 3},
  "who_today": "media buyer or agency"
}
```

Fields:
- `job`: one line, from the owner's mouth, starts with a verb. Not a feature name.
- `why`: 1 to 2 sentences. What breaks if this is not done.
- `watch`: the first metric that moves when the job is done. Must be observable in a connected store: Shopify or equivalent, GA4, Meta, Google Ads, Klaviyo, Gorgias, Search Console, marketplace seller tools, PageSpeed, or the brand brain. Say the window.
- `drives`: the metric one level up that `watch` moves.
- `business`: the top of the chain. One of: revenue, gross profit, contribution margin, cash, customer satisfaction, risk. Prefer gross profit when honest.
- `now_after`: one line. What the screen shows today, what it shows after the owner acts. Use a plausible example number so the reader sees it move. Mark it as an example if it is invented.
- `score`: 1 to 5 each. money = gross profit impact if done well. satisfaction = effect on the customer's experience or the founder's peace of mind. speed = how fast the watch metric moves after acting (5 = days, 1 = quarters). ease = how little effort or money it takes to act (5 = an afternoon, 1 = a quarter and a budget).
- `who_today`: who does this job today without the software: founder, agency, freelancer, in-house role, a tool, nobody.

Total score = 4 x money + 2 x satisfaction + 2 x speed + 2 x ease, maximum 50. Rank by total, then by your judgement. Do not rank by ease alone.

## Ground it

Read, in this order, and nothing else:
1. `app/screens/<slug>/CLAUDE.md` for the screen's purpose and its room pointers.
2. The room file it points to in `agents/rooms/*.rooms.json` (the questions and jobs the room spec already lists).
3. The matching idea bank file in `ideas/v1/` (titles, bottlenecks, signals, expected effects). Use it to check you have not missed a job that the field knows about. Do not copy idea titles as jobs.
4. `ideas/README.md` for the metric vocabulary.

You may do up to 3 web searches per screen when the repo sources do not settle a question, for example a benchmark or how a platform reports a metric. Prefer platform documentation.

For research-type screens (market research, competitors, customers), jobs still get metrics: category demand index from search trends, growth versus category growth, share of shelf, price index against the category, input cost index, review theme share. Include Kevin's asks for market research: is the category growing or shrinking, quarter by quarter; where are we growing slower than the market; input costs rising or falling; allied categories growing; emerging trends to catch early; the competitive forces (five forces) in plain words; where consumers are moving from and to.

## Writing rules

Short sentences. Simple words. Digits. No em dashes. No jargon; if a term needs a definition, say it another way. No feature language ("a dashboard that", "a module for"). The reader is a founder or agency owner.

## Output

Write `app/jtbd/<slug>.json`: `{"screen": "<slug>", "title": "<screen title>", "hired_for": "<one sentence: why an owner hires this screen>", "jobs": [ ... ]}`. Valid JSON. Nothing else on disk. Report back with the file paths and the count per screen.
