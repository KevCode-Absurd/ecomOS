# Jobs to be done, third list: tactical and executable

Date 29 Sep 2026. The first list (`BRIEF.md`) ranked jobs by money. The second (`BRIEF-v2.md`) wrote them from the owner's moment, per Competing Against Luck. This third list goes to the ground: what we actually do, what makes it possible, and what has to be in place first. Read `NOTES-KEVIN-29SEP.md` before anything else. It is the seed and the standard.

Nothing here is built or designed. We are writing the list.

## The shape: three levels

1. **Top jobs** per screen, 3 to 5. The owner's progress, taken from the second list (`app/jtbd/v2/<slug>.json`), in its "When ..., help me ..., so I ..." form. Example: "When the same buyers keep seeing our ads and new customers cost more each month, help me put more ads in front of people who do not know us yet, so I grow instead of rebuying old customers."
2. **Tactical jobs** under the top jobs, 20 per screen. A task a person or an agent can start this week. Verb first. Concrete nouns. Example: "Tag every live ad and every competitor ad by awareness level, and show spend share per level next to 3 rivals."
3. **Steps** inside each tactical job, 3 to 7. Each step is one action with a clear output. Example for the AI video job: write the script; write 3 variations of the hook and angle; cut each variation to 15, 30 and 30 to 45 seconds; render with the video tool; pick one cut per stack; launch as one test.

Each tactical job also names its **enablers** (the engine behind it, from `app/jtbd/v3/enablers.json`) and its **inputs** (what must be given before it can run). This is Kevin's point: the job is "publish more top of funnel ads"; what enables it is the awareness heat map; what the heat map needs is our ads with spend, competitor ads, and a rubric. One enabler powers many jobs.

## Enablers

Use the ids in `app/jtbd/v3/enablers.json` wherever one fits. If a job needs an engine that is not there, add it to your screen file under `new_enablers` with the same fields (id, name, what, inputs, powers, screens, note: null). Do not invent a new enabler when an existing one fits. Keep new ones to 3 per screen at most.

## Inputs and their status

Every input has a status, so we know what blocks the job:
- `connected`: comes from an account connected on onboarding day. The day one kit is: store platform (Shopify or similar) with orders, products and customers; Meta Ads (read only); Google Ads (read); GA4; Search Console; the helpdesk; the reviews app; the public Meta Ad Library by page id.
- `brain`: from a brand brain shelf (see `app/brain/BRAIN-CONTENTS.md`). Name the shelf.
- `founder`: only the founder can give it (see `app/brain/FOUNDER-INTERVIEW.md`).
- `have`: already in ecomOS today (idea bank `ideas/v1`, knowledge cards `data/library-v3`, the playbooks as reference).
- `setup`: we can install or connect it in under a day, free or cheap (Clarity, a post-purchase survey, TikTok Ads, Amazon Seller Central when they sell there, a Google Sheet).
- `buy`: a paid tool, service or person (a video tool such as Higgsfield, an SEO data source, creators, a translator).
- `enabler`: the output of an enabler that must be built first. Put the enabler id in `from`.

## Record shape

```json
{
  "id": "09-01",
  "top": "T1",
  "job": "Tag every live ad and every competitor ad by awareness level, and show spend share per level next to 3 rivals",
  "trigger": "once at onboarding, then every Monday after the ad pull",
  "enablers": ["awareness-map", "competitor-feed"],
  "inputs": [
    {"need": "last 90 days of our ads with media, copy, spend and purchases", "from": "Meta Ads", "status": "connected"},
    {"need": "3 to 5 competitor page ids", "from": "competitors shelf", "status": "brain"},
    {"need": "awareness rubric with 5 examples per level", "from": "awareness-map", "status": "enabler"}
  ],
  "steps": [
    "Pull our ads and 3 rivals' active ads",
    "Tag each ad with one awareness level and one funnel stage, using the rubric",
    "Spot check 20 tags by hand and fix the rubric where it is wrong",
    "Weight each level by spend and lay ours next to each rival's",
    "Write the 1 line gap: the level where we spend least and rivals spend most"
  ],
  "output": "a heat map: 5 awareness levels by 4 brands, share of spend in each cell, plus the gap line",
  "next": "feeds 09-02 (brief 4 top of funnel ads) and 11-05 (prospecting budget split)",
  "watch": {"metric": "share of spend on unaware and problem aware ads", "window": "28 day", "source": "Meta Ads"},
  "drives": "new customers per week, and cost per new customer",
  "business": "revenue",
  "score": {"money": 4, "satisfaction": 3, "speed": 3, "ease": 4},
  "ready": 4,
  "effort": "days"
}
```

Fields:
- `id`: screen number, dash, 2 digits. `top`: the top job id it serves.
- `job`: one sentence, verb first. Something a person could start this week. No feature names as the job; the feature goes in `enablers`.
- `trigger`: when it runs. Once, every Monday, before a launch, when a number moves.
- `enablers`: 1 to 3 ids.
- `inputs`: 2 to 6. Each with `need`, `from`, `status` from the list above.
- `steps`: 3 to 7. Each an action with a visible result. Include the human check where a model could be wrong.
- `output`: the thing you hold at the end. A list, a table, a brief, a launched test, a fixed page.
- `next`: which tactical job uses the output, by id, on this screen or another. One line. "none" if it ends here.
- `watch`: the first metric that moves, with window and source. `drives`: one level up. `business`: revenue, gross profit, contribution margin, cash, customer satisfaction or risk. Revenue and gross profit both count as the top.
- `score`: 1 to 5. money = revenue or gross profit impact. satisfaction = the customer's experience or the founder's peace of mind. speed = how fast the watch metric moves. ease = how little effort and money it takes.
- `ready`: 1 to 5. How much of the inputs exist on onboarding day. 5 = all `connected`, `brain`, `have`. 1 = needs something bought and an enabler built.
- `effort`: `hours`, `days` or `weeks` to the first output.

Total = 4 x money + 2 x satisfaction + 2 x speed + 2 x ease, maximum 50. A job with `ready` of 4 or 5 and effort of hours or days is a "start now" job. The build script computes both; do not write them.

Per screen, also write `top_jobs`: 3 to 5 records `{"id": "T1", "job": "When ..., help me ..., so I ...", "metric": "...", "from_v2": [rank numbers in the second list]}`. Every top job gets at least 3 tactical jobs.

## What to cover

- Kevin's notes first. Every note that belongs to your screen must show up as at least one tactical job, with its enabler. Say in your report which notes you covered.
- Then the ground-level work the second list implies for the screen: what the owner or the agency actually does on a Monday, before a launch, when a number jumps.
- Go deep, not wide. "Improve creative" is not a tactical job. "Cut last month's top 3 video ads to 15 seconds with a new first frame and launch them as one test" is.
- For research screens (market research, customers, competitors), include the ground work: pull the category's search demand quarter by quarter; compare our growth with the category's; check input costs; list allied categories; name the forces in plain words; track where buyers are moving.
- Show inputs honestly. If a job needs a paid tool or an enabler built, say so. That is how we find what to build first.

## Ground it

Read, in this order, and keep reading light:
1. `app/jtbd/NOTES-KEVIN-29SEP.md` and this brief.
2. `app/jtbd/v3/enablers.json`.
3. `app/jtbd/v2/<slug>.json` for the top jobs and the moments.
4. `app/screens/<slug>/CLAUDE.md` for what the screen covers.
5. Skim `app/brain/BRAIN-CONTENTS.md` for shelf names.
6. Grep `ideas/v1/` for tactics when you need depth. Do not read whole files.

No web searches. No paid calls.

## Writing rules

Short sentences. Plain words a founder uses. Digits. No em dashes. No jargon without a plain word next to it. Awareness levels are fine by name: unaware, problem aware, solution aware, product aware, most aware.

## Output

Write `app/jtbd/v3/<slug>.json`: `{"screen": "<slug>", "title": "<title from v2>", "top_jobs": [...], "jobs": [20 records], "new_enablers": [...]}`. Valid JSON. Nothing else on disk. Report the paths, the count per screen, the notes you covered, and any new enablers.
