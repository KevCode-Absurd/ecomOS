# Brand brain: {brand name}

One file per brand. Every screen, agent and brief reads this file first and nothing else about the brand. It is written in plain words so the founder can read it, correct it and sign it.

Version: {date}. Owner: {founder name}. Home market: {country}. Industry: {category in the founder's words}.

## How this file works

Every line carries a source and a date in square brackets. The sources:

| Tag | Means | Filled by |
|---|---|---|
| I | intake form, written by the founder before the call | founder |
| F12 | founder interview, question 12 (see FOUNDER-INTERVIEW.md) | founder, on the call |
| S | the brand's own site | crawl |
| A | the brand's ads and competitor ads, Meta Ad Library by page id | crawl |
| D | connected accounts: store, ads, analytics, email, support | data pull, refreshed on a schedule |
| R | public sources: press, reviews, forums, job posts | research |
| ? | nobody knows yet | open question, owner and date in section 16 |

Rules.
- A founder line beats a site line. A site line beats a data guess. A public line never overrides the founder.
- Unknown stays "unknown". Never a guess in a fact's place.
- Numbers come from D when D has them. A founder number is a range and says so.
- Market-specific fields are split by country. A brand in one country has one column.
- When a line changes, the old line goes to the change log (section 17) with the reason.
- No jargon. If a term needs a definition, it does not belong here.

Which parts of the business read which sections:

| Work | Reads |
|---|---|
| research and product | 1, 2, 5, 9, 10, 15 |
| customers and avatars | 6, 7, 8, 12 |
| competitors | 2, 7, 10, 11 |
| offers and pricing | 4, 5, 11, 15 |
| creative and copy | 6, 7, 8, 9, 10 |
| paid and organic | 4, 6, 8, 12, 15 |
| email and retention | 5, 6, 11, 15 |
| operations and finance | 4, 5, 13, 14 |
| every proposal to the founder | 3, 13, 14, 16 |

## 1. Identity

- Brand name, site, year started: {} [I]
- Founder or founders, and who runs day to day: {} [I]
- Industry and category, in the founder's words: {} [I]
- What we sell in one sentence: {} [S, founder confirms]
- Business model: direct to consumer {share}, marketplaces {share}, wholesale or retail {share}, offline {share} [D for what is connected, F6 for the rest]
- Size band: orders per month {range}, revenue band {range}, team size {n} [D, I]
- Stage: {new, growing, steady, turning around} [F1, F2]

## 2. Markets

One column per country sold in. Home market first.

| Field | {Country A, home} | {Country B} | Source |
|---|---|---|---|
| Share of revenue, last 12 months | | | D |
| Currency, tax and duty rules | | | I, R |
| Marketplaces used | | | I |
| Delivery expectation, days | | | F R7, S |
| Cash on delivery share | | | D |
| Price difference from home | | | S, F R7 |
| Language of ads and site | | | S |
| Peaks and dead zones | | | F24 |
| Biggest customer difference | | | F R7 |

- Where to grow next, and why: {} [F8]
- Where we refuse to sell, and why: {} [F8]
- What stopped growth in the next market so far: {} [F8]
- What an outsider gets wrong about this category: {} [F9]
- The founder's rule of thumb a new hire always doubts: {} [F9]

## 3. Goal and limits

- The 12 month target, one number: {} [F1]
- The 12 month target, one thing that is not a number: {} [F1]
- Which of the two matters more: {} [F1]
- What breaks first if sales doubled next month: {} [F2]
- What must be in place before that growth is wanted: {} [F2]
- Off the table, even if it would sell: {list} [F3]
- The one fix for the next 30 days, in the founder's words: {} [F25]

Every proposal checks itself against this section before it reaches the founder.

## 4. Money

Top products, one row each:

| Product | Price | Landed cost per unit | Margin per unit | Best or worst margin | Source |
|---|---|---|---|---|---|
| {} | | | | | S for price, F4 for cost, computed |

- Lowest contribution per order the founder can live with: {} [F5]
- Most the founder would pay for a new customer: {} [F5]
- Is the floor different for a repeat order: {} [F5]
- What the founder looks at today to judge ads, if no floor exists: {} [F5]
- Revenue not in the connected accounts: {kind, share, where the records live} [F6]
- Does any of it appear inside store data as bulk or test orders: {} [F6]
- Real cost of a return: {shipping both ways, restock, write-off} [F7]
- Worst products and regions for returns: {} [F7]
- Share of returns that are the customer's expectation versus our fault: {} [F7]
- Cash cycle: supplier payment terms, marketplace and gateway payout days, the tight month: {} [F R1]
- From the data, last 90 days: average order value {}, repeat rate {}, return rate {}, ad spend {}, blended cost per order {} [D]

## 5. Products

| Product | Line | Price | Hero | Stock cover, days | Reorder lead time | Minimum order | Can it scale | Going away | Source |
|---|---|---|---|---|---|---|---|---|---|
| {} | | | | | | | | | S, D, F22 |

- Launches in the next 90 days: {} [F22]
- The product the founder would push hardest if stock were no issue: {} [F22]
- Uses the product was not designed for, and any surprising segment: {} [F R3]
- Sizes, materials, care and specs: as listed on the site, not repeated here [S]

## 6. Customers

The best customer, as a person the founder has talked to:
- Who they are: {} [F12]
- Why they buy: {} [F12]
- What they say when they reorder: {} [F12]
- What they read, watch or follow: {} [F12]

Avatars, up to 4, each backed by data and quotes:

| Avatar | Share of orders | What they buy first | Why they buy | Top doubt | Their words | Source |
|---|---|---|---|---|---|---|
| {} | | | | | | D, R, F12 |

- Why customers leave or do not reorder, in their words: {} [F14]
- Which of those reasons could be fixed in 30 days: {} [F14]
- Marketplace buyers: same avatar or a different one: {} [D, F R7]

## 7. Doubts and answers

The three doubts heard most on calls, WhatsApp, DMs and support, ranked by sales lost:

| Rank | Doubt, in the customer's words | What the founder says back | Does it work | Our proof | Where the answer lives today | Source |
|---|---|---|---|---|---|---|
| 1 | | | | | | F13, F16 |
| 2 | | | | | | F13 |
| 3 | | | | | | F13 |

- Doubts from reviews and public threads, added under the founder's three, never above them [R]
- Claims unhappy buyers throw back at us: {} [R]

## 8. Words

- What customers call the product: {} [F15]
- What customers call the problem: {} [F15]
- Our words customers never use: {} [F15]
- A word the founder is tired of: {} [F15]
- A word the founder is proud of: {} [F15]
- Lines buyers repeat that could open an ad, with source and date: {} [R]
- Tone in three words, from the site and the founder: {} [S, founder confirms]
- Banned words and phrases: {} [F17]
- Founder as the face of the brand: {yes, no, sometimes} and hours per week: {} [F R6]

## 9. Positioning and story

- What we want to be known for, one line: {} [F R8, founder signs]
- The moment a customer chooses us over the others: {} [F R8]
- Does that reason appear on the site or in the ads today: {} [S, A]
- The making of the product: choices that cost money and were kept, and why: {} [F18]
- Which of those choices a customer would pay more for if they knew: {} [F18]
- Origin story, as the founder tells it: {} [F18, R]
- Category frames buyers use, and whether our line matches them: {} [R, F9]
- The substitute: what people do when they buy neither us nor a competitor: {} [F R2]

## 10. Claims

Allowed, with proof:

| Claim | Proof | Where the evidence file is | Used today | Source |
|---|---|---|---|---|
| {} | | | | F16 |

- Site claims not yet backed by a proof file: {list} [S, waiting on F16]
- A proof the founder has and has never used: {} [F16]

Forbidden:

| Never say | Why | Who said so | Source |
|---|---|---|---|
| {} | legal, regulator, platform, cannot keep, shaky, off-brand | | F17 |

- Has a regulator, platform or lawyer ever pushed back on a claim: {} [F17]
- Customer photos, videos and quotes we may use, and where the permission is recorded: {} [F R5]

## 11. Competitors

The brands we actually lose sales to, 3 to 5:

| Brand | Why the customer picks them | Their price band | Their lead angle in ads | Their formats | What we refuse to copy | What we wish we had started earlier | Threat in 12 months | Source |
|---|---|---|---|---|---|---|---|---|
| {} | | | | | | | | F10, F11, A, S |

- The one that worries the founder most, and why: {} [F10]
- A move the founder is about to copy: {} [F11]
- Angles competitors run that we never run: {} [A]
- Names public threads recommend instead of us, and the doubt behind each: {} [R]

## 12. Offers and policies

- Live offers, prices, bundles, shipping threshold, returns policy: as on the site, not repeated here [S]
- Discount limits: deepest discount allowed {}, products never discounted {}, when discounts are allowed {} [F3, F5]
- Guarantees we make: {} [S, F16]
- Loyalty or subscription, if any: {} [S, D]
- Offers that worked and stopped: {} [F19]
- Offers that failed and must not return: {} [F20]

## 13. Channels and history

From the data, last 12 months:

| Channel | Share of revenue | Spend | Return on spend | Trend | Source |
|---|---|---|---|---|---|
| {} | | | | | D |

What worked and then stopped, or could not scale:

| What | When | Why it stopped | What it would take to bring back | Source |
|---|---|---|---|---|
| {} | | | | F19 |

What failed and must not be repeated:

| What | When | Idea or execution | The lesson | Source |
|---|---|---|---|---|
| {} | | | | F20 |

- Agencies, creators and affiliates paid, cost, use again or not: {} [F R4]
- Live ad angles, formats and hooks: from the Ad Library, not repeated here [A]

## 14. Data trust

- Accounts connected: {store, ads, analytics, email, support, marketplace} with last refresh date [I, D]
- Accounts not connected, and what we cannot see because of it: {} [I]
- Numbers the founder does not trust, and why: {tracking gap, attribution, bulk orders, test orders, offline, broken pixel} [F21]
- When each problem started: {} [F21]
- Revenue outside the connected accounts: see section 4 [F6]
- The rule: a screen that uses an untrusted number says so next to the number.

## 15. Team, approvals and calendar

Who does what:

| Area | Person or agency | Approves | Typical speed | Would hand to an agent | Source |
|---|---|---|---|---|---|
| creative | | | | | F23 |
| offers and pricing | | | | | F23 |
| ad spend | | | | | F23 |
| site and landing pages | | | | | F23 |
| email and messages | | | | | F23 |
| support | | | | | F23 |
| stock and supply | | | | | F23 |

Calendar, per market:

| Peak or dead zone | Market | Dates | Prep starts | Under-prepared last year | Source |
|---|---|---|---|---|---|
| {} | | | | | F24 |

- Launches and events in the next 90 days: {} [F22]

## 16. Open questions

| Question | Owner | Due | Asked on | Source |
|---|---|---|---|---|
| {every "I would have to check" from the call} | | | | F |
| {what the founder said we should have asked} | | | | F26 |

## 17. Change log

| Date | Section | Old line | New line | Why | Who |
|---|---|---|---|---|---|
| {date} | | | | | |

## 18. Decisions

| Date | Decision | Why | Who | Source |
|---|---|---|---|---|
| {date} | | | | |

## Sign-off

The founder reads sections 1 to 15 in one sitting, corrects anything wrong, and signs with a date. Nothing in this file is used by a screen or an agent before that signature. Re-sign after every interview and at least every 90 days.

Signed: {name}, {date}.
