# 13-ORG-organic-and-content playbook

version: 2.0-draft  |  date: 24 Sep 2026  |  sources: 10  |  cards: 149  |  built from: sources/*.md

## 0. How to use this playbook

**Who runs it.** The organic content and social agent: the role that plans a brand's organic social calendar, writes hooks, scripts and captions, builds series, sets up comment-to-DM lead capture, reads monthly results and decides what to make next. A writer, editor or reviewer worker can run any checklist in section 5 alone. Paid amplification of organic winners hands off to 10-MCR-paid-social-creative and 24-DEP-ad-deployment. Email sequences after a lead is captured hand off to 14-EML-email-lifecycle. Landing pages and lead-magnet pages hand off to 07-LPG-landing-pages. Ad copy fields hand off to 11-ADC-ad-copy-deployment.

**Ecommerce first.** This playbook is for stores, not for personal brands, coaches or media accounts. Section 3.0 ranks the levers below by impact for a store; load it before the detail groups in section 3. Store-type conditions (hero SKU vs catalogue, low vs high AOV, subscription vs one-off, marketplace-heavy, luxury or considered purchase, mobile-first India vs US) decide which rules apply and in what order, and several rules in the sections below now carry a store-specific condition for this reason.

**Which sections to load for which task.**

| task | load |
|---|---|
| Set up or fix an account's positioning, pillars and topic | 3.1, 3.9, P1, P22, checklist 5.3 |
| Build the monthly calendar | 3.2, 3.7, P3, P4, checklist 5.3, section 6 |
| Write or review a hook | 3.3, P5, checklist 5.1, section 6 |
| Write or review a script or caption | 3.4, 3.5, P6, P7, checklist 5.2 |
| Use AI to draft, remix or review | 3.5, P7, checklist 5.7 |
| Find a story or angle for a product or founder | 3.6, P8, P9 |
| Design a series, challenge or format | 3.7, P10 |
| Decide posting cadence and batching | 3.2, P4, section 7 (C1, C3) |
| Set up comment-to-DM, lead magnets and CTA timing | 3.10, P12, P13, P14, checklist 5.8, section 7 (C4) |
| Repurpose a winner | 3.11, P17, section 7 (C10) |
| Tear down a top performer or build the swipe file | 3.12, P9, P2 |
| Read monthly performance | 3.13, P15, P16, checklist 5.4 |
| Decide how content makes money | 3.14, section 7 (C5) |
| Compliance and brand safety before publishing | 3.15, P21, checklist 5.5 |
| Any algorithm behaviour question | 3.8 (all marked as claims), section 11 |
| Any point where sources disagree | section 7 |
| What to hand back | section 9 |

**Fetch before acting.**

- From brand data: the brand record (voice rules, substantiated claims list, product facts, price ladder, target market and country, regulated-category flags), the founder's real history and stories, real customer stories with permission, current account setup per platform (account type, country, who posts), current follower counts and the last 30 to 90 days of post-level data (views, follower share of views, retention, shares, saves, comments, watch rate after 3 seconds), lead and sales data by post where it exists (discount codes, DM automation opens, clicks, purchases), team capacity (who can be on camera, editor hours, batch days), footage archive status. Full list in section 2 and section 10.
- From the data layer: the Meta Ads read tools (read only) if organic winners are being tested as paid ads; the gallery data in `data/meta-gallery/` for Gehna; the experiment or test log if one exists.
- From the web: current Instagram and TikTok account-type rules, current comment-to-DM automation policy and approved partner list, current platform treatment of outbound links, current disclosure rules for AI-generated voices or spokespeople, current names and prices of any tool a procedure names. List in section 10, cadence in section 11.

**ecomOS rules that override any source.** Several sources tell the reader to exaggerate a claim with ChatGPT, court controversy, stitch another creator's viral clip, quote a statistic they did not measure, or drop a formal register for an informal one. Those instructions are recorded in section 7 and section 12 as what the source said. They are not rules here. The rules below win every time:

1. No invented claims. A number, study, result or comparison goes into a hook, script or caption only when the brand record can back it. "This is a national ice bath crisis" (06) is out unless it is literally true. "Stories are 22x more memorable" (05) and "5% remembered facts, 63% remembered stories" (06) are unverified figures and never appear in client-facing copy.
2. No copying competitor or creator content. Frame swiping (06), format borrowing (10) and swipe files (01, 05) give structure, pacing and mood only. Never reuse their text, logos, products, faces or footage. A hook swap that stitches a third party's clip (04, 05) runs only with confirmed usage rights.
3. Claims match the brand record. Product facts, guarantees, materials, sourcing, before-to-after outcomes and founder history come from the brand record, not from the source's example or from an AI draft.
4. Reading level below tenth grade on every hook, script and caption. The sources are stricter (5th to 8th grade), and that stricter target is the default here.
5. Brand voice from the brand record wins over any source's tone advice. "Informal is not the opposite of professional" (01), "exaggerate on purpose" (06), "publish a polarising hot take" (10), "write from I, not you" (02) and "negative framing outperforms" (05) are options to test inside the brand's voice, never reasons to leave it.
6. Meta is read only. Nothing here publishes, pauses, boosts or changes budgets. The agent prepares calendars, scripts and DM-automation specs; a human publishes.
7. House writing rules: short sentences, simple words, digits, no em dashes, no inflated words, concrete before-to-after benefits. Do not mention GPT or .env on client pages.

**Source notes to keep in mind while reading.**

- 9 of the 10 mini playbooks are one creator, coach or agency selling a course, community, tool or mentorship inside the same talk (01: Maven course and copythat.com; 02: TypeShare and Ship 30 for 30; 03 and 10: the same "Cut 30" program; 04 and 05: the same Instagram coach, Brock Johnson, selling Insta Club; 07: an AI research tool and mentorship; 08: Wavy World and Sandcastles; 09: a ManyChat affiliate trial and a free course). Only 06 reads as an operator's talk with no product named on screen, and even 06 is self-reported. Section 12 rates each one.
- 2 pairs share a presenter, so "2 sources agree" can mean 1 person said it twice. 04 and 05 are the same coach (hook effort at 80%, the "drunk grandma" test, hook swaps). 03 and 10 are the same Cut 30 program (expert content, format ideas). When this playbook counts agreement, it says whether the sources are independent.
- Every number in every source is self-reported, a retold anecdote or a heuristic. No source shows a controlled test, a data export or third-party verification. No rule here is a promise.
- Card-writer ecommerce adaptations that the source never said are marked "(card adaptation)". Examples: 08's cards add pet-supply and camping-gear account examples and "route PDP traffic to email"; 10's cards add series commitment, content calendars and a legal screen for pop-culture hijacks; 04's cards map a fitness-equipment challenge onto product demos; 02's cards supply the "I tested this knife for a month" example; 05's mini playbook adds the rights check on borrowed clips; 06's mini playbook adds the defensibility review after exaggeration.
- Tags: `[verify UI]` for platform steps that change, `[needs brand data: what]` for anything that depends on the brand's own numbers, `[web check: what]` for anything to confirm live.

## 1. Scope and outcomes

**This folder covers.**

- Positioning an organic account: who it is for, what topic it owns, expert or student stance, brand account vs named human.
- Content pillars and the monthly operating plan: which pillars, how many posts, how long to hold a mix, when to review.
- Hook craft for short-form video and carousels: visual first, word count, reading level, hook types, curiosity gap, negative framing, first frame.
- Writing process: pre-writing decisions, copywork, draft, incubation, edit, read-aloud and readability passes.
- Writing with AI: what a human must originate, what AI may repeat or remix, voice as variables, the "I" vs "you" question.
- Formats, series and challenges; scalable production; sets, props, lighting; batching and cadence.
- Algorithm behaviour claims from the sources, all marked as claims, with what to verify.
- Platform choice and account setup: hero platform vs cross-posting, Creator vs Business account, country, satellite accounts.
- Comment-to-DM automation, lead magnets, CTA timing, comment and DM sales handling.
- Repurposing and asset life: reuse counts, cross-format and cross-account reuse, timely vs timeless.
- Teardown and swipe-file method.
- Measurement: macro reads over single-post verdicts, which metric per goal, business attribution checks.
- Monetisation logic: owned funnels vs sponsors, low-ticket vs high-ticket paths.
- Brand safety and compliance for organic content.

**This folder does not cover.** 02's own scope card routes paid media setup, sales-letter copy and email automation to 10-MCR, 07-LPG and 14-EML [88b7d114b8b5]. Paid social creative and testing (10-MCR), ad account setup, budgets and scaling (24-DEP), ad copy fields (11-ADC), landing pages and lead-magnet pages (07-LPG), email and SMS sequences after capture (14-EML), measurement infrastructure and attribution models (06-MEA), search engine optimisation (no source in this folder covers it; 01's concision advice does not override SEO needs), influencer and creator paid partnerships (10-MCR covers UGC briefs).

**Business measures this domain moves.** New accounts reached (non-follower share of views), retention and completion, shares, saves and comments by phase, follower growth as a funnel step, leads captured per post (DM automation opens, clicks, emails), sales tied to content (discount codes, DM purchase tracking, sales spikes against post dates), cost per lead where content is amplified, and the size of the reusable asset library (approved stories, hooks bank, series formats).

## 2. Inputs the agent needs

| input | from where | required or optional | why |
|---|---|---|---|
| Brand record: voice rules, tone limits, regulated-category flags | brand record | required | Voice wins over source tone advice (section 0). Regulated or luxury brands change which angles are allowed (C9). |
| Substantiated claims list and product facts | brand record | required | Every hook and script claim must match it (section 0, R163). |
| Founder history: years, failures, sourcing trips, reasons for starting | brand record or user | required for story pillars | Founder questions (P8), 30-minute carousel (P8), unmade data set (R60). |
| Real customer stories with permission | brand record or user | optional | Inspiring customer story pillar (06). Never invented. |
| Positioning statement or proof points (credentials, years, volumes, process) | brand record or user | required | Creator DNA statement (P1). Expert vs student stance (R4). |
| Target market and country | brand record | required | Account registration and posting country (R113). |
| Price ladder: which products are low ticket, which are considered | brand record | required for CTA and funnel design | Low-ticket in-app vs high-ticket to a call (R127). No source gives a cutoff. |
| Current account setup per platform: type, country, who has access, who posts | user | required | Creator vs Business account (R112), manual posting (R116). |
| Follower counts and 30 to 90 days of post-level data | data layer or user export | required for any performance read | Macro read (P15), follower share of views (R148), phase metrics (R146). |
| Retention curve, 3-second watch rate, shares, saves, comments, Story views per post | data layer | required for reads, optional for planning | Phase metrics (R146). `[verify UI: which fields the platform exposes]` |
| DM automation analytics: opens, clicks, purchases per keyword | DM tool export | required if automation is live | Follow-up retargeting (R124), lead per Reel (R151). |
| Sales by day, discount code redemptions, impressions by post | data layer | optional | Business attribution check (R150). Arithmetic in code. |
| Team capacity: on-camera people, editor hours, batch days available | user | required | Volume floor (R14), batching (R16), scalable formats (R85). |
| Footage archive status and location | user | optional | Creator bench and archive (R94). |
| Existing lead magnet or mid-funnel asset | brand record or 07-LPG | required before CTA layer | Lead magnet fit (R122), mid-funnel asset (R159). |
| Existing series, formats and their results | user or data layer | optional | Series pipeline (P10), repurposing (P17). |
| Competitor and category accounts (for structure only) | inspiration, web | optional | Competitive format research (P2). Signals, not proven winners. |
| Current platform rules: account types, DM automation policy, link handling, AI disclosure | web | required before setup or automation | Section 10 and 11. |
| Current tool names and prices (DM automation, readability checker, scheduler) | web | optional | `[web check]` before naming a tool to a client. |
| Experiment log | data layer | optional | Record scheduler tests, CTA timing tests, hook-type results (C3, C4, R142). |

## 3. Decision rules

Every rule states the rule, when it applies, the mini playbooks that support it (by number), any conflict (by section 7 code), and card ids. Where only 1 source supports a rule, the rule says so. Where 2 sources share a presenter (04 and 05; 03 and 10), the rule says so. Where sources disagree, the strictest condition is kept here and the disagreement is written out in section 7. Algorithm behaviour is grouped in 3.8 and every rule there is a claim, not a fact.

### 3.0 Ecommerce priority order

This block ranks the levers below by impact for a store. It is not source-backed as a ranking; it is built by ordering the rules in this playbook for store use. Load it first and branch by store type (hero SKU vs catalogue, low vs high AOV, subscription vs one-off, marketplace-heavy, luxury or considered purchase, mobile-first India vs US) before applying the detail sections.

1. Fix the funnel: every post maps to top, mid or bottom funnel and reuses across the PDP, email and DM (R10, R131, R134). A missing funnel tag is the most common way a store account gets views with no sales.
2. Set CTA and price-ladder routing before scaling reach: low-ticket in-app, high-ticket or considered purchase to a call, capacity confirmed first (R24, R127, R118, C4). Ranks above cadence for luxury or considered-purchase brands.
3. Get the hook and first frame right; it gates everything downstream (R25, R26, R29), so it outranks writing-process polish.
4. Move specs to the PDP, lead with story or demo (R65). For a wide catalogue, pick 1 hero SKU per post rather than a generic "our products" post. `[general practice]`
5. Set the floor and pillar mix by catalogue size and capacity: a hero-SKU brand sustains fewer, deeper pillars than a wide catalogue (R2, R3, R13, R14). The catalogue-size branch is `[general practice]`.
6. Pick the hero platform by where the store's actual customers are, checked with the sample in P22 step 2, not by presenter preference; a mobile-first India audience and a US audience can answer differently (R110, P22). `[general practice]` for the geography branch.
7. Build the comment-to-DM and lead-magnet layer once the account has traction, tied to a lead magnet the store can fulfil (R119, R121, R122, R24).
8. Run the compliance and claims check before publishing, especially for regulated or health-adjacent categories (R163, R167, P21).
9. Sell founder or sourcing story for considered or handmade products; use expert-breakdown or ratings pillars for commodity products (R4, R76, R156). `[general practice]` for the product-type branch.
10. Tie every month's read to sales, not views: spikes vs post dates, discount codes, week-on-week sales (R150, R95).
11. Repurpose winners into paid tests once they move sales; route catalogue-wide creative decisions to 24-DEP and 10-MCR (R132, R150).
12. Layer seasonal sales and launches on continuous lead-magnet content; timing matters more with real inventory and drop dates than for a media account (R130). `[general practice]` for the inventory-timing framing.

Load this block first; the groups below are the detail.

### 3.1 Positioning, topic and pillars

**R1. Write a positioning statement before planning any content.** Fill in: "I am [X]. I do [Y] for people who [Z]. Listen to me because [proof]." Each blank must be specific enough that a direct competitor could not paste in their own name and have it read true. Fill the proof slot with something a stranger can verify, and check it does not contradict the PDP: if the statement says "fastest" or "best," the product page must say the same thing. Use the statement to filter every hook, on-screen line and caption so the library reads as one voice. Condition: every account, before the first calendar; redo it when the account stalls. 01 adds the "personal monopoly" filter: own the topic the founder or brand is most specifically obsessed with, because nobody can compete there. 02 adds that association is built by writing about a narrow set of topics repeatedly, not by writing about everything. Sources: 07 (statement), 01, 02. `[needs brand data: the proof point]` Cards: [bab1ea1d6132] [4adfe40984ba] [712445a708f1].

**R2. One account covers one topic area for one customer avatar.** Derive ideas from that avatar's pain points, not from industry trends. A brand with unrelated categories runs separate content lines or separate accounts rather than one mixed feed. Condition: split into satellite accounts only after a format has proven on the main account (09); never launch several accounts at once. 04 agrees the niche must be fixed before growth, though it can stay loose during the first exploratory posts. Sources: 08, 09, 04. Conflict: C15 (satellite accounts vs one feed). Cards: [d84a8df8c294] [5bb14404abb5] [13325d6dff66]. (Card adaptation: 08's cards add pet-supply and camping-gear examples the presenter never gave.)

**R3. Pick 2 to 3 content pillars from the 4 expert-driven pillars.** The 4 are storytelling, ratings and rankings, breakdowns, and scenarios. Pick 2 minimum, 3 if ambitious. Storytelling is the hardest pillar with the lowest hit rate, so never run it alone. 10 (same program as 03) adds an angle menu that can sit inside any pillar: format shakeup, speed, viral vehicle, attention hijack, hot take, versus, embarrassed questions, lore and depth, tour guide, event reframe. Condition: any brand starting or restarting organic; hold the pillar mix for a full month (R13). Sources: 03, 10 (same presenter program). Cards: [db75d5f43244] [aa78ae3a6fe1] [ada6b00c3e15] [bde55a0463de] [7af226f4da5b] [d7e7a7512a23] [07ab40bc6089] [a38c90da39f7] [2cc9d0eca5c6] [6cb62b6f330a] [bcaf193b340c] [16be31adb83e].

**R4. Choose the expert or the student stance honestly.** Lead with credentials and "look the part" only when the title or credential is real. Otherwise document the research or journey openly as a student. Both build trust by different routes. 03 calls expert-led content "the cheat code right now" but bounds it to roughly 9 months from the talk (late 2025), so treat it as a window, not a law. Condition: every on-camera person and every "we tested" claim. Source: 03 only. `[needs brand data: which credentials are real]` Cards: [4b03755b2896] [db75d5f43244].

**R5. Design every post for a stranger who has never seen the PDP.** No inside jokes, no product nicknames, no assumed familiarity with SKUs, sizes or the catalogue, and no references to earlier videos. Lead with the clearest version of the idea, not the cleverest. The stated reason is the algorithm claim in R97 (a sample of non-followers sees the post first); the reason holds even if the mechanism is wrong, because most viewers of any post are new or infrequent. Condition: growth content; retention content for existing customers is a separate job. Sources: 04, 07, 08, 09 (4 independent presenters). Cards: [37ea3485764f] [e3a9ae26373a] [34a52f48158a] [e1440ddfb8b1].

**R6. Aim for on-target reach inside the avatar slice, not the broadest possible hit.** A 10 million view video that pulls in tech people, architects and home buyers at once gives the platform a noisy signal about who to show the next post to and does little for sales. 06 says the same from the sales side: 90 million views with no story is worth less than 10 million views with the reason behind the visual. 10's lore principle narrows the audience on purpose to convert a smaller group intensely. Condition: a business account; a pure media account may want broad reach. Sources: 08, 06, 10. Cards: [d6fdd4b41759] [d37ea33564f1] [6cb62b6f330a].

**R7. Layer the brand's point of view onto proven topics; never copy wholesale.** Research what already works (P2), then add the missing perspective, method, segment or caveat from the positioning statement. Blind copying gives random, non-repeatable results. The gap can be small; do not over-engineer it. Condition: every idea in the bank should carry both a proven topic and the brand's angle. ecomOS: structure only, never text, footage, product or faces (section 0, R164). Sources: 07, 06 (frame swipe), 10 (format borrowing). Cards: [1bdc7fef77c8] [646870522f21] [ada6b00c3e15].

**R8. Personality content lives on a named human's account; the brand account repeats agreed positions.** 02 says a branded page "always underperforms" a real person and that personal biography should not come from a faceless handle. 03 says decide who is front and centre (founder, employee or hired creator) and batch with that person. 06 warns the same founder's personal story repeated on the same page fatigues. Condition: brands with a willing founder or named employee; faceless brands run the carousel path (R90). Sources: 02, 03, 06. Conflict: C14 (founder story as an asset vs founder story as a scaling limit). Cards: [49c888bb326e] [2b0c662e2dd0] [f63181942aa7] [34c4c10786ba].

**R9. There is no boring category, only boring treatment.** Before concluding a category cannot work on social, run at least 3 of the 10 reframes in R3 and the single-element test in R26. Condition: any "our product is too dull" objection. Source: 10 only, stated as strong personal conviction. Cards: [6cb62b6f330a] [2e322467dede].

**R10. Map every piece to a funnel stage before it is made.** Top of funnel earns curiosity and trust, not a sale. Mid funnel nurtures (longer video, email, case study, lead magnet). Bottom of funnel makes the offer. Reuse each asset across the sales path: landing page, pre-purchase email, DM reply, post-purchase story. Pitching a hard sale on discovery is "asking someone to marry you on the first date" (09). Condition: every calendar entry carries a stage tag. Sources: 03, 09. Cards: [36e148349505] [92f5abb59008] [5f22157f3977].

**R11. Label every piece timely or timeless before publishing.** Timely content (a launch, a holiday, a trend) spikes for about 24 hours and cannot be reused; timeless content (a durable how-to, an origin story) pays slowly for years. A single date or "just launched" line turns a timeless piece timely, so strip it if you want reuse. Timely reactions must ship fast: 06 says react to category news within 3 days; 10 says pop-culture hijacks decay quickly; 06's own brand missed a mascot moment a competitor turned into 15 million views (example, not a promise). Condition: every calendar entry carries the label. Sources: 02, 06, 10. Cards: [3014faaee9da] [9143824217f6] [da9c7887e7c9] [d899a52a55f2].

**R12. Weigh short, medium and long-term value before spending time on a piece.** A 20-minute post that restates a known idea adds a little approved language. A 2-week essay that crystallises a new position can feed formats for years. Budget time to the value, not equally per piece. Condition: any piece that would take more than a normal batch slot. Source: 02 only. Cards: [1193451bea64].

### 3.2 Monthly operating plan, cadence and batching

**R13. Set the starting cadence by catalogue shape: a single hero SKU runs 2 pillars at the stated cadence; a wide catalogue needs a rotation so no SKU goes untouched for a month.** `[general practice]` for the catalogue-shape branch. The stated cadence for a new or restarted account is each chosen pillar twice a week, 4 to 6 posts a week, hold the exact mix for 1 full month. Daily posting is not required at this stage. After about 4 iterations per pillar, read which pillar, topic and format pulls. Repeat the monthly cycle for about 3 months; some accounts take 1 to 3 months to show traction. Condition: this is the minimum plan; higher-capacity teams raise the floor under R14. Source: 03 only for the numbers. Conflict: C1. Cards: [aa78ae3a6fe1].

**R14. Set an explicit volume floor the team can hit every week for a month, and do not judge content below the floor.** The sources give very different floors: 02's agency floor is 5 pieces a day; 04 says "the more you post, the more you grow" and ran 4 posts a day; 06 says once a day is a starting point, not a ceiling, and to post more only when the data says it works; 07 says under-posting is what holds back 95% of the people he coaches; 03 says 4 to 6 a week. Strictest condition kept: the floor must be sustainable for 4 weeks in a row, and it is raised only when the monthly read (P15) shows the content works. Condition: every brand. `[needs brand data: team capacity and audience fatigue signals such as unfollows per post]` Sources: 02, 03, 04, 06, 07. Conflict: C1. Cards: [7d684acdc24b] [c318b8e45196] [8292e101004a] [868f6861da16] [aa78ae3a6fe1].

**R15. Fix input before infrastructure.** More posting systems without a source of original ideas produce more generic content, faster. Solve "can we ship the volume" and "do we have anything original to say" as 2 separate problems, in that order of diagnosis but with the idea library never behind the posting machine. Condition: whenever volume rises. Source: 02 only. Cards: [ed26cf9e8b40] [4392aa839fe7].

**R16. Batch in separate research, scripting and filming sessions.** Script on a fixed day: 3 to 5 ideas per sitting, continue until 10 to 20 scripts exist (a few hours). Film all scripts back to back on a separate day. Person-led brands shoot roughly once every 2 weeks with hooks, prompts and scripts prepared in advance. Daily overthinking is the friction that stops consistent posting. Condition: any account above 3 posts a week. Sources: 07, 03. Cards: [868f6861da16] [f63181942aa7].

**R17. Commit before judging: 3 months minimum before changing the pillar mix, 12 months before declaring the channel dead.** 03 says 1 to 3 months to traction; 04's coaching window grew from 90 days to 120 days to 6 months to "at least a year"; 08 says 6 months on one hero platform plus email, and 30 to 50 consecutive videos on one topic before the algorithm has "learned" the audience (claim, R98). Strictest kept. Condition: consistent posting at the floor the whole time; a gap resets the clock. Sources: 03, 04, 08. Cards: [aa78ae3a6fe1] [13325d6dff66] [e46ef6c2491a] [d84a8df8c294].

**R18. Uploads are the KPI in the first phase.** Track the input the team controls (posts shipped against the floor), not the outcomes it does not (views, followers). Condition: months 1 to 3 or until the first macro read shows a pattern. Sources: 04, 02. Cards: [13325d6dff66] [7d684acdc24b].

**R19. Never compare the account's outcomes to established creators.** Use other accounts for format ideas and market gaps only. Comparing growth speed or follower counts creates a "why not me" stall before results can show. Condition: every review meeting. Source: 04 only. Cards: [38b7805726e7].

**R20. After the first month, add comment-question posts.** Take the common questions and objections under the best posts and make a new post that opens with the exact question and answers it. 10 adds: answer the questions people are embarrassed to ask. Condition: needs at least a month of comments. Sources: 03, 10 (same program). Cards: [aa78ae3a6fe1] [1212d5fe9ec6] [2cc9d0eca5c6].

**R21. Ignore micro tactics until the library and the floor exist.** Exact posting time, trending audio, TikTok text posts, reposting Reels to Stories, buying retweets, the "close friends" trick: 02 calls them irrelevant without a library, 03 calls them "easy dopamine" distractions, 06 dismisses them against story. Condition: always, until R14 and R60 are in place. Sources: 02, 03, 06. Cards: [3335c7ab8443] [26f23bfd7ece] [d37ea33564f1].

**R22. Keep a permanent idea bank of 10 to 20 one-line ideas drawn from research, not memory.** Each line names the proven topic and the brand's angle. Refill it before every batch day. Condition: always. Source: 07 only. Cards: [348619262de0] [1bdc7fef77c8].

**R23. Past underperformance does not doom the next post.** Under interest-based distribution each post is judged on its own, so one strong post can reset the account (09's "hook over history"). The mini playbook for 09 notes this overstates variance because account-level quality signals still exist. Condition: do not abandon an account because of history; do not expect a reset from a weak post. Source: 09 only, with its card's caveat. Cards: [ff7b85a40e7b].

**R24. Plan intake and fulfilment capacity before scaling reach.** A single post can bring more leads or orders than the team can serve; 07 closed a mentorship intake once for this reason. Condition: once a lead magnet or DM automation is live. Source: 07 only. Cards: [4a4a14bf5c74].

**R175. Rotate which SKU gets a post by catalogue size.** A catalogue of 50 or more items needs a rotation plan so no SKU goes untouched for a month; a single-hero-SKU brand instead deepens angles on the one product rather than rotating. Condition: any catalogue larger than a handful of SKUs; ties to the catalogue-shape branch in R13. `[general practice]` No library source; verify against brand data before use.

### 3.3 Hook craft

**R25. The hook is the gate. Put most of the planning effort into the first 3 seconds.** 04 and 05 (same presenter) say 80% of planning time and effort goes to the hook; 09's AI review asks whether the hook is clear and attention-grabbing in under 3 seconds; 04 names watch rate after 3 seconds as the foundational metric. Condition: every Reel, Short, TikTok and the first slide of every carousel. Sources: 04, 05 (1 presenter), 09. Cards: [c173b995a2f5] [8690e3531230] [8907bbacfafe] [3380206cba51].

**R26. Plan the visual hook before the words.** Viewers process the image faster than they read text, so a generic or unrelated first frame causes the swipe before the text hook is read. Visual levers: a prop, a human face with eyes to camera, dynamic movement, a sudden lighting change, subject-matched footage (a fitness creator exercising, not typing), an unusual vantage point (10's roofing tips filmed from a ladder), a split screen. Condition: every video; for a carousel, the first slide. Sources: 04, 05 (1 presenter), 10, 07 (first frame and lighting). Cards: [c173b995a2f5] [cee2da009c53] [2e322467dede] [26bf14383383].

**R27. Hook line of 5 to 8 words; up to about 12 at most.** 05's own review of 1,300 viral Reels found top performers averaged 7.7 words, rarely under 4, with diminishing returns from 13 words up. The sample has no disclosed selection method. Condition: on-screen text and the spoken first line; captions can run longer. Source: 05 only. Cards: [c98d12e4ca71].

**R28. Reading level: hook text at or below 5th grade; body copy 5th to 8th grade; never at or above 10th grade.** 05 scored its hook list at 5th grade with an undisclosed ChatGPT check; 01 targets 5th to 8th grade for consumer copy and accepts 4th; ecomOS caps everything below 10th grade. Strictest kept. Match the hook and caption reading grade to the PDP and checkout copy, so a viewer who clicks through meets the same voice and grade level. `[general practice]` Check with a readability tool (01 names the Hemingway app) `[verify UI]`. Condition: every hook, script and caption. Sources: 05, 01, ecomOS. Cards: [c98d12e4ca71] [a3cac5e01c5a] [d8fbcddae70a].

**R29. The "drunk grandma" test: a stranger with zero context and zero effort must get the hook and the frame instantly.** Cut insider terms, acronyms and unexplained jargon. 09's AI review asks the same question in different words: would the target market immediately understand what this is about. Condition: every hook. Sources: 04, 05 (1 presenter), 09. Cards: [9fce1289b063] [c98d12e4ca71] [8907bbacfafe].

**R30. Open a curiosity gap in the right width, then pay it off honestly.** Too small (the hook already gives the mechanism or ending) and there is no reason to watch; too wide ("this changed everything for me") and the viewer cannot tell the domain or stakes. Open the gap with the product's before-state; name the problem's stakes, withhold the specific result until the payoff. `[general practice]` 01's test: cover all but the first 2 sentences and ask whether an indifferent reader needs the next one; repeat to sentence 3 or 4, then let the piece breathe. 06 says open the loop in the first sentence and do not close it in the next one; hold it through the body and resolve it later. All 3 agree the payoff must be real: "it ain't bait if you deliver on the promise" (01); the dramatic thing must actually happen (04). Condition: curiosity, story and open-loop hooks; 05 says this type takes the most practice. Sources: 05, 01, 06, 04. Conflict: C6 (open loop vs clear benefit). Cards: [97e147c3e5a1] [26bc815a7b84] [0980397e62b4] [c1f05a1e6af3] [d686739bfd6c].

**R31. Test negative framing against positive framing; do not assume either.** 05's sample found hooks with threat words (don't, stop, avoid, never, cancel, stay away from) outperformed their positive counterparts on average, and 05 itself says to keep testing positive hooks against the account's baseline. Benefit-forward framing is standard for paid conversion copy (11-ADC), so this is an organic-hook finding, not a copy rule. Condition: only within the brand's voice; a warm or luxury voice may exclude threat words. Source: 05 only. Conflict: C12. Cards: [5897c79754a5].

**R32. Pick the hook type on purpose from the 15-type menu, and log it.** The types, each with 05's example: pattern interrupt ("Stop scrolling"); contrarian ("Post daily? Yes. Create daily? No."); curiosity gap ("This one thing changed everything about my Pokemon card collection, and after 4 years I finally finished"); outcome ("My client put on 12 pounds of muscle in 3 months"); direct address ("If you're a mom of 3 under 3, keep watching"); story ("I almost quit X last year"); hook swap (a borrowed viral clip with a match cut); authority or data-backed ("It took me 10 years to get 60,000 followers, then 1 month to get 60,000 more"); bold claim; relatable ("me when I spend 3 hours editing a Reel and it gets 7 likes"); POV ("POV: you just opened the box"); urgency or time-bound ("Before your head hits the pillow tonight"); list ("3 ways to fix your bench press"); comparison ("Me before walking 10K steps a day", split screen); identity ("Good snowboarders always do this"). For the outcome hook type, use a real before-and-after tied to the product, backed by a customer or test result from the brand record, never a generic "results" claim. `[general practice]` Do not default to a habitual type. Condition: every hook in the hooks bank carries a type tag. Source: 05 only. Cards: [11f62e1913d1] [1ab0e11dcafa] [97e147c3e5a1] [01267ffe7cb0] [e679699e4817] [d22074737dfa] [6fbe7c8824cd] [9dd434350255] [9b17f7a80dfc].

**R33. Prefer a conversational opener that still names a concrete payoff over a loud formula.** 07 says audiences discount "3 mistakes you're making" and "stop doing this" as recognised bait, and that "did you know if you add oats and chia seeds..." reads like a friend talking (1 example at 20,000 likes). 05 lists those same formulas as working types. Strictest condition kept: any formula hook must pass the read-aloud test ("would a friend say this") and still signal a specific payoff. Condition: every hook. Sources: 07 vs 05. Conflict: C6. Cards: [3a5f43d052ea] [9dd434350255] [11f62e1913d1].

**R34. A hook swap is not bait: the teased moment must happen on camera, the match cut must align, and rights must be confirmed.** Two routes: stitch a proven viral clip and transition into your own content, or stage your own real dramatic moment. The last frame of the borrowed clip and the first frame of your footage must match in motion or composition; if there is no genuine match point, do not force it. 05 says nothing about usage rights; 05's mini playbook adds the rights check and ecomOS requires it (R164). Condition: hook-swap hooks only. Sources: 04, 05 (1 presenter). Cards: [d686739bfd6c] [d22074737dfa].

**R35. No dead time in the first second.** Cut the "millennial pause", static setup shots, visual clutter and low contrast. Screenshot the video at about half a second: a stranger should be able to say what it is about from that frame. Condition: every video. Source: 05 only; 06 adds that retention is "a game of milliseconds". Cards: [cae016218009] [cee2da009c53] [c1f05a1e6af3].

**R36. Use specific, realistic numbers, not extreme ones, and only numbers the brand can back.** Outcome hooks with believable figures hold more viewers than unattainable ones. ecomOS: the number comes from the brand record or does not appear. Condition: outcome and data-backed hooks. Source: 05 only for the "realistic beats extreme" claim; ecomOS for the backing rule. Cards: [01267ffe7cb0].

**R37. Borrowed credibility needs a real, relevant citation.** "According to [named body]" lowers stranger scepticism only if it is true. 02 shows the same lever as a voice variable: adding 2 or 3 citation phrases (about 1% of a piece) fixed a client's "doesn't sound like me" complaint. Condition: authority hooks and any cited study; 05's own "stories are 22x more memorable" and 06's "5% vs 63%" Stanford study are uncited and never go into copy. Sources: 05, 02. Cards: [01267ffe7cb0] [612587c6befe].

**R38. Contrarian and bold-claim hooks only for positions the brand actually holds and will defend in the comments.** 05 and 10 both make this the condition; 10 adds that a hedged verdict "undermines credibility faster than a boring video". Condition: every contrarian, hot-take and versus hook; see R167 for the legal line. Sources: 05, 10, 06 (contrarian angle). Conflict: C7. Cards: [1ab0e11dcafa] [07ab40bc6089] [86b7c9130744].

**R39. Identity hooks describe behaviour, not judgment.** "Disciplined runners never do this" works through self-comparison; "lazy moms start their day like this" is a stereotyping risk 05 flags on its own example. Condition: identity and direct-address hooks. Source: 05 only. Cards: [e679699e4817].

**R40. A list hook must deliver the full promised count.** "3 ways" with only 2 delivered breaks the implicit promise and hurts retention. Condition: list hooks. Source: 05 only. Cards: [9dd434350255].

**R41. Do not rely on sound for the hook.** A large share of viewers watch on mute; a loud sound effect can also read as annoying. Text and visual carry the interrupt. Condition: every video. Source: 05 only. Cards: [11f62e1913d1].

**R42. Attention hijack: open with the scenario the audience already cares about, then deliver the expertise inside it.** "The hook isn't how to use bonus depreciation. The hook is G-Wagon, then bonus depreciation." Pop-culture and news variants (a lawyer opening with 3 seconds of rap lyrics, a barista making a drink "for" a celebrity) work because the audience already knows and likes the reference. Condition: ship fast (R11) and screen for real people, legal matters and implied endorsement (R168; card adaptation, the source did not say it). Source: 10 only. Cards: [d7e7a7512a23] [da9c7887e7c9].

**R43. Relatability comes from extreme specificity and shared context.** "Me when my Reel gets no views" is weak; "me when I spend 3 hours editing a Reel and it gets 7 likes" lands with fewer but more resonant viewers. 06's blanket ad worked because it assumed the viewer already owned a similar item; people repeat the story about the restaurant around the corner, not one far away. Condition: relatable, POV and scenario hooks. Sources: 04, 06. Cards: [9fce1289b063] [d899a52a55f2] [6fbe7c8824cd].

**R44. Exaggerated language is recorded as 06's advice and is not a rule here.** 06 says write plainly, then ask ChatGPT for an "extremely exaggerated" version and pick the strongest line anchored to a real event ("This is a national ice bath crisis"). ecomOS overrides: no invented claims (section 0). What survives: choose the most charged true wording ("we failed a lot, like a lot a lot" about a real test history), and let the brand voice decide the ceiling. Condition: never on health, safety, legal or comparative claims. Source: 06 only. Conflict: C7, C9. Cards: [d52d9eff6cd1].

### 3.4 Writing process and readability

**R45. Before writing a word, decide the reaction, the action and the one line the reader should remember.** Reaction is an emotion (awe, outrage, warmth, curiosity). Action is what they do (comment the keyword, save, share, buy). The one line replaces the outline; for a headline-plus-subheadline format the subheadline (about 180 characters) is the stable thesis. 06 pairs the same first step with an emotional-trigger map (curiosity, moral outrage, belonging, confusion, visual shock) and a delivery technique (novelty, relatability, visual shock, trend relevance, credibility, controversy). 01 frames all of this as persuasion at scale, not self-expression: the writing exists to move a reader to act. Condition: any script, caption, carousel or founder story. Sources: 01, 06. Cards: [5286ee7f0f32] [797d8a7279aa] [6f735c911cc5] [1629164d5fc0].

**R46.** Moved to Appendix A, section A.4: the 4-step writing process (copywork, dump draft, incubate, edit) as general writing craft, with no product or funnel tie; the how-to steps remain live in P6 steps 3 to 5.

**R47. Punch with the first sentence; move the thesis, promise or most provocative true statement to the top and cut the background.** 01's model opener: "I spent the last 30 days eating nothing but Soylent. Why would I do something so stupid? I'll explain." 04 says lead with the clearest version, not the cleverest. Condition: every opener; add context only after the reader is invested (about sentence 3 or 4). Sources: 01, 04. Cards: [26bc815a7b84] [37ea3485764f].

**R48. Readability edit pass: cut adverbs, jargon, thesaurus words and LinkedIn words ("utilize"); if you had to look a word up, it is the wrong word.** Target grade in R28. 01's evidence: Buffett's shareholder letters fell from 17 to 13 words per sentence and 10th to 4th grade over 1974 to 2013 while the subject got harder. Condition: every script and caption before publishing. Source: 01 only. Cards: [d8fbcddae70a] [a3cac5e01c5a].

**R49.** Moved to Appendix A, section A.4: say it out loud before writing, read aloud before publishing; general writing craft with no product or funnel tie; the how-to step remains live in P6 step 9.

**R50.** Moved to Appendix A, section A.4: vary sentence length for rhythm, comma to period; general writing craft with no product or funnel tie; the how-to step remains live in P6 step 6.

**R51. Write to one person.** Pick one real or composite customer and write only to them; it is a coincidence that others read it. 08's avatar rule is the account-level version of the same idea. Condition: any copy that starts to sound corporate. Sources: 01, 08. Cards: [9783e7f32959] [d84a8df8c294].

**R52. Run a redundancy pass: for every sentence ask "necessary, or already said?"** 04's bad example: "fit, lean, lose weight, healthy" is 4 ways to say 1 thing and makes viewers scroll. Condition: every script. Source: 04 only. Cards: [9fce1289b063] [37ea3485764f].

**R53.** Moved to Appendix A, section A.4: filter topics with a 60-second voice memo; general writing craft with no product or funnel tie; the how-to step remains live in P6 step 4 and P8 step 3.

**R54. Unlearn school writing.** No minimum word count, no fancy vocabulary, no formal outline; the one-line thesis (R45) replaces the outline. Condition: all consumer-facing internet copy; this does not override SEO depth needs, which no source here covers. Source: 01 only. Cards: [797d8a7279aa].

**R55. State the topic and the intended viewer plainly in speech and in the caption.** 08 claims the algorithm reads topic mainly from the auto-transcript and the caption (R98), so name the topic and audience in both. Where a comment keyword is used, put the keyword on screen and in the caption (07, 09). Condition: every video and caption. Sources: 08 (claim), 07, 09. Cards: [34a52f48158a] [d84a8df8c294] [302840d96c34] [00f161224b14].

### 3.5 Writing with AI and voice

**R56. AI repeats approved language; humans originate.** Human work: net-new thinking, the first articulation of an idea, taking a side on a category debate, specific founder or customer stories. AI work: remixing sentences already written, slicing long pieces into shorts, cross-format versions, 10 or more hook and caption variations of one human idea (09). 02 softens its own rule for non-writers: a brain dump into an LLM that drafts in the person's voice is "no different" from a human ghostwriter, so the operator decides which mode applies per piece. 06's use of ChatGPT to exaggerate falls under R44. Condition: every AI-assisted piece is tagged "remix" or "originated by [name]". Sources: 02, 09. Cards: [ad4c55b5d306] [4392aa839fe7] [8b3238183f67] [c5eaa02ce9d1].

**R57. Record the brand's side on debates that gate a purchase decision: material vs synthetic, price vs quality, in-house vs sourced, not abstract industry opinions.** AI writes generic copy because it does not know which side of a settled debate the brand holds ("buy heavy pans" vs "light pans done right"). Write the position, or mark it "deliberately neutral". Condition: before any AI draft; keep a running positions log in the brand record. Source: 02 only. `[needs brand data: the category's recurring debates and the brand's side]` Cards: [cbbb787360b8].

**R58. Prescriptive "you should" copy reads as commodity; first-person experience reads as personality; reader-benefit "you" is fine.** Rewrite prescriptive lines as a first-person product test: "I used this for 30 days before we shipped it," not a general category claim (card adaptation: the knife example is the card writer's). Route "I" content to a named person's account (R8). 02's mini playbook flags that benefit-focused "you" ("you'll get X") is standard converting copy and is not what 02 attacks. 05's story hooks open with "I"; 06's breakout video opened "My name is Davey, this is my story". Condition: prescriptive advice lines; leave benefit lines alone. Sources: 02, 05, 06. Conflict: C8. Cards: [2b0c662e2dd0] [e679699e4817] [da155e10b870].

**R59. Voice is a small bundle of variables: word choice (neutral, elevated or blunt), sentence length and structure, and stance (opinion-led or citation-led).** When a draft "doesn't sound like us", find the one variable that is off and make the smallest edit (02's case: 2 or 3 citation phrases, about 1% of the piece) instead of discarding the draft. Record the confirmed variables in the brand voice guide. ecomOS: the brand record's voice is the reference; the agent does not derive a new voice from a source's taste. Condition: every voice complaint on an AI or ghostwritten draft. Source: 02 only. Cards: [612587c6befe].

**R60. Build the "unmade data set": the founder's and team's unwritten stories, mistakes and positions, stored where AI and writers can read it.** The tool does not matter (a doc, a sheet, Obsidian); the structure does. Once a story has been told well once or twice, mark it approved and let AI redeploy it. Drop a specific story into the exact slot where the generic claim ("we care about quality") would go. At company scale this is the "company brain": 1 or 2 people whose only job is original long-form thinking that feeds every downstream format. ecomOS note: the general brand brain is not built yet; this rule defines what it should hold for this domain. Condition: before scaling volume (R15). Source: 02 only. `[needs brand data: founder stories, failures, sourcing history]` Cards: [33bc4c19a527] [0d61d18719cc] [bda11c7340cf] [320db8651bf5].

**R61. Use AI as a pre-publish reviewer with targeted questions, not open ones.** Paste the script, caption or transcript and ask: "Is my hook clear and attention-grabbing in under 3 seconds?", "Would my target market immediately understand what this is about and want to keep watching?", "Make this caption shorter and easier to read on a phone", "Where could I cut or speed up so viewers don't drop off?". 09 also asks for "10 hook ideas similar to the top performing videos in my niche"; under R164 those ideas are structural prompts, never lifted lines. Condition: every script before filming and every caption before posting. Source: 09 only. Cards: [8907bbacfafe] [1445bdd3ed8e].

**R62. Review every AI-remixed piece for facts and voice before it reaches a customer.** AI is repeating, not verifying. Claims are checked against the brand record (R163). Condition: always. Sources: 02, 09. Cards: [4392aa839fe7] [8907bbacfafe].

**R63. Publish to discover the voice; do not wait to find it.** "I don't like my voice" is usually a fear problem, not a voice problem; most feared commodity opinions ("the key to marketing is knowing your customer") are low risk to publish. Ship small pieces and compare variants. Condition: founder-led accounts stalled on "not ready". Source: 02 only. Cards: [8b3238183f67] [910b7d45cd6e].

**R64. Ask of every AI-drafted piece: did this add net-new thinking, or only rearrange what exists?** Track the answer so the library grows rather than cycles. Condition: monthly, alongside P15. Source: 02 only. Cards: [ad4c55b5d306] [1193451bea64].

### 3.6 Story and angle craft

**R65. Tell the sensory, embodied version, not the spec version.** Facts activate language processing; a story of someone kicking a ball fires the listener's motor cortex ("neural coupling"). 06 cites an unnamed Stanford study (5% recalled the fact version, 63% the story version) `[web check: locate the study before quoting it]`. 06's own case: 2 years stuck under about 200,000 with a 400,000-view ceiling, broken by opening with "My name is Davey, this is my story" and telling the story before the lesson. 05 repeats the "22x more memorable" figure without measuring it. Condition: product descriptions in video, carousel and caption; specs move to the body or the PDP. Sources: 06, 05, 01. Cards: [da155e10b870] [b79bd0ea1c02] [e679699e4817] [b5c0734ef3bc].

**R66. Mine stories with a fixed question set.** What does everyone think is true about the product but isn't? What is controversial or frustrating in the industry? What is the most inspiring customer story (film it on a phone)? What proves the product beats competitors, as a story not a thickness chart? What is the strangest or most visually shocking thing about it? What happened in the category's news in the last 3 days? 01 adds: high stakes can come from a low-stakes setting (an HOA dispute, a packaging argument) rendered with honest emotional weight, and a story driven by a real emotion (01's Hint Water founder story, dismissed by a Coca-Cola executive, later promoted by the brand itself) can earn distribution the brand did not pay for; the sales figures 01 attaches are unverified. Condition: whenever the idea bank runs low. Sources: 06, 01, 02. Cards: [9143824217f6] [9affec3cf159] [33bc4c19a527] [0dcc74caac04].

**R67. Every story names an intention and an obstacle, revealed fast.** Pause anywhere in the story and you should be able to say what the character wants and what is in the way. If not, the reader has lost the thread. Condition: founder stories, About content, customer stories, story-led carousels. Source: 01 only. Cards: [b5c0734ef3bc] [b372918f62e6].

**R68. Build the founder-history carousel in 30 minutes when a postable asset is needed today.** Write down the last 10 to 20 years of business life, 1 iconic event per year including failures, as a journey that reaches success; 1 photo per moment; a text overlay on each; assemble and post. 06 reports 45,000 likes on his own attempt and says the same story worked again on YouTube and Twitter (example, not a promise). Condition: needs the founder's real timeline `[needs brand data: founder timeline and failures]`. Source: 06 only. Cards: [2147e1a9ca59].

**R69. Frame swipe out-of-niche winners for structure only.** Take a teeth-whitening ad's pacing and camera angles and apply them to a clothing brand; never reuse the story, because a copied story serves an already saturated audience. Run the teardown grid (R140). 10's format shakeup is the same move with entertainment formats (a "Hot Ones" interview format turned into "Hot Law"). ecomOS: structure, pacing and mood only (section 0). Condition: needing a new format without a new idea. Sources: 06, 10. Cards: [646870522f21] [b7abaa44d689] [ada6b00c3e15].

**R70. Judge creative by what is remembered the next day, not raw views.** Scroll a batch, return tomorrow, note what you recall unprompted; story-led pieces survive, "brain rot does not make sales". Condition: choosing between 2 concepts; this sits alongside, not instead of, the metric read in 3.13. Source: 06 only. Conflict with KPI-first practice noted in section 7 (C19). Cards: [d37ea33564f1].

**R71. Run a contrarian angle to reach an audience nobody else is serving, within the limits of R38 and R167.** If the category sells ice baths on recovery, "ice baths are toxic if not cleaned" finds an underserved pocket; do not reject the new angle as "cringe". 10's hot-take rule and 05's contrarian hook are the same lever. Condition: saturated category messaging; the claim must be true and defensible. Sources: 06, 10, 05. Conflict: C7. Cards: [86b7c9130744] [07ab40bc6089] [1ab0e11dcafa].

**R72. Choose the story angle by proximity: where the audience already is in life, geography or habit.** Condition: choosing which customer scenario leads a post. Source: 06 only. Cards: [d899a52a55f2].

**R73. A versus format needs a real verdict.** "Product vs brand", "material A vs material B": state the comparison in the title, give a professional verdict with reasons, never a hedge. Condition: comparison content; named competitors trigger R167. Source: 10 only. Cards: [a38c90da39f7].

**R74. Answer the questions customers are embarrassed to ask, and the questions in the comments.** Condition: education pillar. Sources: 10, 03 (same program). Cards: [2cc9d0eca5c6] [1212d5fe9ec6].

**R75. Go obsessively deep to build a cult following in a narrow slice.** An army-surplus retailer posting about the exact German aircraft and the year Sweden changed its camo pattern (1962) became the reference point for enthusiasts. 01's version: monitor practitioner writing (a 10,000-word grocery-app UX teardown hit #15 on Hacker News) and use the "I know nothing about X, but I do know Y" outsider angle. Condition: categories with an enthusiast subculture; it narrows reach on purpose (R6). Sources: 10, 01. Cards: [6cb62b6f330a] [d6daae75f48f].

**R76. Sell access to the hidden world, not the product.** Reframe factory visits, sourcing trips and trade shows from "here is what we sell" to "we are tour guides to a world you have never seen", shot with travel-documentary energy. 09's coffee roaster swapped studio content for raw roasting, packing and staff banter and reach "expanded significantly" in a couple of weeks (no numbers). 03's student stance is the same move for a founder without credentials. Condition: businesses with an operation outsiders never see; luxury and regulated brands test raw content on a lower-stakes account first (09). Sources: 10, 09, 03. Cards: [bcaf193b340c] [ccecf6f16262] [4b03755b2896]. (Card adaptation: 10's card adds "keep a share of what-we-make content as one pillar".)

**R77. Reframe mundane industry events as the exciting thing insiders know they are.** "The Coachella of dermatologists." The analogy must survive scrutiny. Condition: trade shows, launches, audits, seasonal peaks. Source: 10 only. Cards: [16be31adb83e].

**R78. A first-person founder letter is a format to test on landing pages and in email, not a proven lift.** Open with a contrarian reframe of the category, not the product ("Email gets a bad rap, but it shouldn't. Email is a treasure."), then plain short sentences. 03's plain-text founder email (a sale, a release, an overlooked product's story, a milestone, an apology) goes into the welcome and post-first-purchase flows. Both route to 07-LPG and 14-EML for mechanics. Condition: must be genuinely attributable to the named person. Sources: 01, 03. Cards: [32e6539348a0] [8b7c348825ce].

**R79. Study comedians for timing, callbacks and crisis ownership.** In a mistake or crisis, name it directly and self-aware instead of denying or spinning. Condition: brand storytelling and any apology post; legal review still applies. Source: 01 only. Cards: [2a2b22a57381].

**R80. Give away the playbook.** Full breakdowns do not stop qualified buyers; most viewers will not execute, and buyers are buying proof of expertise. 02 agrees basic commodity advice is the most useful thing for beginners even if it is low leverage for the writer. Condition: breakdown pillar; keep the offer for after traction (R118). Sources: 03, 02. Cards: [db75d5f43244] [bdf52e0f0da8].

**R176. Turn verified reviews, ratings and customer photos into posts.** Pull a strong review line or a customer photo (with permission) and build a short post or carousel around it: the quote as the hook, the product in use as the visual. This folder only turns approved material into content; 07-LPG and 17-CXP collect the reviews and photos themselves. Condition: any store with a review or UGC pipeline. `[general practice]` No library source; verify against brand data before use.

### 3.7 Formats, series and production

**R81. New accounts split effort toward product demo and use-case Reels first; carousels carry spec comparisons and size or fit guides.** `[general practice]` About 80% of effort goes to Reels at this stage; hold Stories until there are followers. Reels reach non-followers most; Stories are seen almost only by followers, so early Story effort is wasted. Once followers exist, Stories become the home for clicks and CTAs. 03 says carousels can carry any pillar with no camera; 06's founder carousel drew 45,000 likes. Condition: the 80% split is a new-account rule; adjust after the first macro read. Source: 04 only for the split; 03 and 06 for carousels. Conflict: C13. Cards: [fa1ae83e8a27] [4c8610731e7c] [e96110e037ff] [2147e1a9ca59].

**R82. Turn a proven concept into a named, repeatable series instead of chasing a new idea each time.** 09's B2B case: 5 formats tested, 1 ("rapid-fire common mistake") doubled engagement, was branded and run twice a week, and within 2 months drove over half of inbound leads (example). 04 predicts series and challenges will dominate 2026 and says a recognisable format is faster to make and easier for viewers to identify. 06: once a format wins, stay with it for a long period. Condition: needs 1 winner first; do not brand a format before the macro read. Sources: 09, 04, 06, 10 (card adaptation for series commitment). Cards: [3df74f892c3f] [a0a28a40b29f] [34c4c10786ba] [ada6b00c3e15].

**R83. Package a series with a name, a distinct visual signature and a clear promise of what each episode gives.** Adapt length per platform (09's example: a 60-second version for TikTok, a 3-minute version for LinkedIn). Condition: every series in the pipeline. Source: 09 only. Cards: [3df74f892c3f].

**R84. A challenge must be a genuine stretch, safe, and yours first.** "A different salad every day" carries no weight; a runner doing a mile per follower does, but 04 says not to copy that extreme and rules out anything dangerous. Smaller real challenges work (speaking 60 seconds without filler words, day by day). For a product brand, make the repeatable demo the challenge: "day [N] of exercising in a new location with my invention" (card adaptation of a product-demo mapping). Community participation is a bonus, not the design goal. Condition: challenge series. Source: 04 only. Cards: [a0a28a40b29f].

**R85. Prefer formats a team can repeat many times in a day without the founder's body.** Cooking and travel fail ("you can't get 15 Reels in one day" if each needs a meal or a trip); podcast-style and street-interview formats pass. A single founder's personal story on the same page fatigues. Pilot a format for a week (impressions and sales) before building a team or archive around it. Condition: any brand planning to scale beyond the founder. Source: 06 only. Conflict: C14. Cards: [34c4c10786ba].

**R86. Compress the expected pace as a vehicle.** A 10-second apartment "speedrun", "30-second makeup", "1-minute recipes": the gap between expected and actual length is the hook. 10 frames this partly as an algorithm preference for fast content (claim, R106). Condition: content where the audience knows the normal pace. Source: 10 only. Cards: [bde55a0463de].

**R87. Invest the signature prop or set around the product itself (a wall of stock, a fitting room, a workbench) so the set doubles as merchandising,** rather than in monthly complex shoots. 10's toy store bought a hydraulic press ("thousands of dollars", not the largest) and became "one of the more interesting toy stores on the internet". 03: a consistent set (a wall of product for a fragrance founder, scrubs and a dentist's chair, an apron and kitchen) compounds credibility but cannot rescue weak content; a student visibly displays what they have tested so far. 10's related card: demonstrate what the product makes possible (a skill or outcome shown in an impressive way) rather than describing it; 10's example is a copywriting agency bringing romance novels to life in 15-second videos, which has no card of its own. Condition: one-off content asset; expect the payoff in notoriety more than any single post. Sources: 10, 03 (same program). Cards: [7af226f4da5b] [3f6eca540367] [e95cfa96efe9].

**R88. Commit to the bit: raise production stakes a little so the content does not look like everyone else's.** Filming outdoors (a park, a front yard) instead of a static indoor setup adds variability; street interviews work because outcomes are unknown. No dangerous stunts. Condition: talking-head formats that have gone flat. Source: 04 only. Cards: [4289340e4d3b].

**R89. "Raw" is not an excuse for bad lighting.** Turn off ambient light, set one key light (a large window or a cheap softbox), add practical background lights for depth; 1 to 2 hours to set up; a phone camera is enough. 09 says raw behind-the-scenes beats polished "gallery era" content; 04 says authentic means a short gap between idea and execution, not heavy editing. All 3 agree the first frame must look intentional. Condition: every filming setup; luxury or regulated brands check the brand record before going raw (C9). Sources: 07, 09, 04. Conflict: C18. Cards: [26bf14383383] [ccecf6f16262] [9fce1289b063].

**R90. If no one will go on camera, run the faceless carousel path and invest more in design and editing.** Visuals and craft must carry the credibility a person would. Condition: faceless brands. Source: 03 only. Cards: [e96110e037ff].

**R91. Run every Reel through SHARE before publishing.** Simple (drunk grandma), Hook (visually arresting), Authentic (short idea-to-execution, not over-edited), Relatable (specific, not vague), Entertaining (entertainment leads, education rides inside it). Condition: every short video; see C2 on entertainment vs education. Source: 04 only. Cards: [9fce1289b063].

**R92. Keep more than 1 format live once winners exist.** 09 says run several formats in rotation to spread risk and avoid fatigue; 06 says stay with a winning format for a long period rather than swapping weekly. Strictest merge: never swap a winner out weekly, and never let the account depend on 1 format. Condition: after the first winner. Sources: 09, 06. Conflict: C16. Cards: [3df74f892c3f] [34c4c10786ba].

**R93. Give the video an ending.** 06's teardown of a 10 million view clip flags a strong beginning and no ending as a missed chance to be remembered; the same grid shows a worked ending (product reveal, apology, bundled offer). Condition: any story-led video; speed formats (R86) are the exception. Source: 06 only. Cards: [b7abaa44d689].

**R94. Build a creator bench, a footage archive and incentive-paid editors before the founder becomes the bottleneck.** Hire for proven views, not corporate polish (06's customer-service employee with a 10,000-follower TikTok grew the brand account past 500,000). Get founder, staff and even family to upload every usable clip to one shared drive continuously. Give overseas editors the drive plus examples, let them experiment, pay a CPM base with bonuses for videos that go viral and convert. Condition: once the founder is the sole creator and output is capped; rates are not given. Source: 06 only. `[needs brand data: archive status, editor capacity]` Cards: [3b8dc00bf68a].

**R95. Diagnose a sales plateau as a founder-capacity ceiling before blaming the product.** Same output in a tougher market gives falling sales; check whether competitors entered, whether the founder still films everything at about once a day, then look at sales spikes against posts, weekly sales in a strong-content week, discount codes and impressions (R150). If the content works, post more than once a day; if not, stop assuming daily posting is the fix. Condition: flat or falling sales with a founder-led account. Source: 06 only. Cards: [8292e101004a].

**R96. Adapt length and cut per platform, keep the idea.** Condition: cross-posting a series. Source: 09 only (1 example, no stated reason). Cards: [3df74f892c3f].

**R177. Film the unboxing or packaging reveal as its own format.** Show the box, the unwrap and the first look at the product; packaging becomes part of the story, not just a detail inside a founder story. Condition: any physical product with a considered unboxing moment. `[general practice]` No library source; verify against brand data before use.

### 3.8 Algorithm behaviour claims (every rule here is a claim)

No source in this folder cites platform documentation. Every mechanism below is a presenter's explanation, stated as fact in the talk. The agent treats each as a hypothesis, records what it would look like in the brand's own data, and re-verifies on the cadence in section 11. `[web check: current Instagram and TikTok creator documentation on distribution]`

**Moved to Appendix A, section A.1: R97 to R109**, the algorithm behaviour claims (stranger-first sampling; topic learned from transcript and caption; broad-hit targeting noise; posting-volume claims; the scheduler-penalty claim; TikTok account-type and country claims; outbound-link throttling; DM-thread and comment signals; fast-content and exaggeration claims; the search-surfacing claim; top-content scoring claim; follower count as a funnel step). None of these rules is store-specific; they are kept as background hypotheses, not decisions. See Appendix A.1 for the full text and section 11 for the re-verify cadence.

### 3.9 Platforms, accounts and cross-posting

**R110. Pick 1 hero platform by where the store's actual buyers spend time; a mobile-first India audience and a US audience can answer differently.** `[general practice]` for the geography check. Cross-post only where it adds no work and never route an audience between social platforms. 08 says one platform plus email for 6 months; 03 says TikTok and Instagram as the base with cross-posts to LinkedIn, X, YouTube Shorts and Snapchat Spotlight because the same content performs on both base platforms. Strictest merge: the read (P15) is done on the hero platform; secondary platforms are manual cross-posts with zero expectation; no "watch my YouTube" call-outs. Condition: small teams starting from zero; 08 says an established multi-platform brand may not need the constraint. Sources: 08, 03. Conflict: C11. `[needs brand data: which platform holds the most customers]` Cards: [e46ef6c2491a] [03e0df5b81d9] [19bea8d6aaa6].

**R111. LinkedIn and X only if someone will show up to comment there; YouTube Shorts with zero business expectation.** 03: about 30,000 Shorts views "doesn't really do much"; a million "maybe does some stuff". Condition: cross-post destinations. Source: 03 only. Cards: [19bea8d6aaa6].

**R112. Default to a Creator account on TikTok and Instagram; use a TikTok Business account only when a TikTok Shop needs it, and keep a separate Creator account for posting.** Instagram Creator accounts can still run ads. Source: 03 only. `[verify UI]` Cards: [b22a54d48616].

**R113. Register and post the account from the target country.** Matters most outside the US, Canada and English-speaking Europe. If nobody is in-country, hire someone there to set up and post, with account access and a backup under the brand's control. Do not set up an account while travelling somewhere else. Source: 03 only. `[verify UI]` `[needs brand data: target country vs registration]` Cards: [b22a54d48616].

**R114. Spin a format into a satellite account only after it proves on the main account; keep the main account as the sandbox.** 09's hypothetical structure: main account for product stories, a tips account, a testimonials account, a founder account. A drop on a single-format satellite is easier to diagnose. No source gives a limit on how many. Source: 09 only. Conflict: C15. Cards: [5bb14404abb5].

**R115. "World build" instead of cross-promoting: keep visuals and story consistent across platforms so a second discovery feels aligned.** Source: 08 only. Cards: [03e0df5b81d9].

**R116. Post manually on each platform (2 to 3 minutes per platform, 12 to 15 minutes for 6 platforms) until the brand has tested a scheduler against manual posting on its own account.** 03's rule; 03's own cards downgrade it to a hypothesis. Condition: run the test in P11 before choosing. Source: 03 only. Conflict: C3. Cards: [7ff53d5768f7].

**R117. Once followers exist, use Stories as the secondary format and the home for CTAs.** Sources: 04, 08. Cards: [4c8610731e7c] [fa1ae83e8a27] [e46ef6c2491a].

**R178. Use shoppable posts and product tagging beyond TikTok Shop.** Tag products directly in Instagram and Facebook posts and Reels where the platform supports it, not only through a TikTok Shop tie-in (R112). `[verify UI: current shoppable tagging features per platform]` Condition: any platform that supports native product tags. Partial source: TikTok Shop only [b22a54d48616]; the wider claim is `[general practice]`. No further library source; verify against brand data before use.

### 3.10 CTA timing, comment-to-DM, lead magnets and the funnel

**R118. Set the CTA-free window and view threshold by price point: a low-AOV store can add a soft CTA sooner than a high-AOV or considered-purchase store.** `[general practice]` for the price-point branch. On a new account, the default is to run the first month with no CTA at all, then add soft CTAs once posts consistently reach the niche's view threshold. 03 says no "buy", "join my list" or "go to my page" until posts consistently hit about 5,000 views (about 2,000 in very narrow niches such as construction or SEO), and calls early CTAs "shooting yourself in the foot". 09 says every piece needs one clear next step. 04 sells low-ticket items in-app continuously. 07 attaches a lead magnet to 1 or 2 Reels a week. Strictest kept as the default for a new account; section 7 (C4) gives the path for brands that need leads sooner. Condition: new or restarted accounts. Sources: 03 vs 09, 04, 07. Conflict: C4. Cards: [bf0b2be7f3cf] [5f22157f3977] [3dd25615d38b] [302840d96c34].

**R119. Replace "link in bio" with a comment keyword that triggers a DM containing the link or asset.** "Link in bio" tells an engaged viewer to leave the post and walk a confusing path; a keyword keeps them on the post, raises comments, and lands a notification in their inbox. 4 sources name ManyChat; 04 calls it (per him) the only officially approved Instagram DM partner. Condition: any post with an offer, guide or link. `[verify UI: current comment-to-DM setup]` `[web check: current Meta messaging partner list and DM automation policy]` Sources: 04, 07, 09, 03. Cards: [79467cee9f17] [302840d96c34] [00f161224b14] [bf0b2be7f3cf].

**R120. One distinct, memorable keyword per campaign so engagement is attributable.** State it on screen and in the caption. Sources: 04, 07, 09. Cards: [79467cee9f17] [302840d96c34] [00f161224b14].

**R121. Attach a lead magnet to 1 or 2 Reels a week, not every post.** Source: 07 only. Cards: [302840d96c34].

**R122. The lead magnet must match a strong audience want, and a mid-funnel asset must exist before any hard offer.** 07 says a well-matched freebie keeps producing comments and leads for 6 to 8 months (his account). 09 says the mid-funnel asset can be simple (newsletter, webinar, free trial, waitlist) but must exist. 03's example: a luxury web-design report drew 5,000 to 6,000 signups, of which "only a fraction" were customers over a roughly 1-year cycle (example, not a promise). Condition: before P14. Sources: 07, 09, 03. `[needs brand data: which free resource fits the store's customer]` Cards: [302840d96c34] [5f22157f3977] [36e148349505].

**R123. Automate a thank-you DM on new follow with no pitch.** "Hey, thanks so much for the follow. I appreciate you." No offer, no code. At scale this creates a heavy inbox that may need batching (card caveat). Source: 04 only. `[verify UI]` Cards: [b539e41f421e].

**R124. Use DM automation analytics to follow up with people who opened or clicked but did not buy.** 04's example: 10 clicked, 3 bought, 7 identifiable to message ("the sale ends tomorrow night, any questions?"). His own account showed about 98% opens and 37% clicks (examples, not benchmarks). Condition: DM automation live; keep follow-ups inside platform messaging rules. Source: 04 only. Cards: [13e3b50fabea].

**R125. Connect the DM automation to email or CRM, and test the whole flow before the triggering post goes live.** A broken link during a spike wastes the spike. Source: 09 only. Cards: [00f161224b14].

**R126. Answer every comment and DM with a specific reply, fast; proactively DM anyone who looks like a lead with the answer plus a next step (a code, a size guide, a booking).** If the founder will not do it, a sales team does, but speed and personalisation stay. 08 adds: comment on others' posts in the niche on the hero platform. Condition: from the first engagement onward. Sources: 03, 08. Cards: [eaadc77a360f] [e46ef6c2491a].

**R127. Sell low-ticket products and free lead magnets inside the app; route high-ticket or considered purchases to a call or consultation.** No source gives a price cutoff. Condition: `[needs brand data: price ladder]`. Source: 04 only. Cards: [3dd25615d38b].

**R128. Most viewers do not buy from the post; route them to a landing page with a hard CTA (buy) or a soft CTA (lead magnet for an email).** Source: 03 only. Cards: [36e148349505].

**R129. The only outbound bridge is social to owned (email list or private community).** 08's islands rule; 07 and 08 both say email is the durable asset if the platform "burns down". Condition: all CTAs. Sources: 08, 07. Cards: [03e0df5b81d9] [4a4a14bf5c74].

**R130. Launch cadence: continuous free lead magnets, plus 1 or 2 launches a year, plus seasonal sales.** Source: 04 only. Cards: [3dd25615d38b].

**R131. Reuse every content asset along the sales path.** Landing page, pre-call or pre-purchase email, in-DM answer, post-purchase follow-up; for no-call ecommerce, email and SMS take the call steps (route to 14-EML). Source: 03 only. Cards: [92f5abb59008].

**R179. Turn stock status into content: restock alerts, low-stock or sold-out framing, and waitlist drops.** Post when a hero SKU is about to sell out or has just restocked; use a waitlist opener ahead of a drop. Condition: stores with real stock constraints or drop-based launches; pairs with the launch cadence in R130. `[general practice]` No library source; verify against brand data before use.

**R180. Offer a bundle or a higher-AOV alternative in CTA content, not only "buy" or a lead magnet.** For a returning or engaged viewer, the next step can be a bundle, an upgrade or a higher-tier product, not always the entry item. Condition: stores with more than 1 price point; route the bundle logic itself to 03-OFF. `[general practice]` No library source; verify against brand data before use.

### 3.11 Repurposing and asset life

**R132. Reuse a proven winner at least 4 times by changing the wrapper, not the story.** Change the hook, convert to an AI voiceover (disclosure check, R170), turn a video script into a text carousel, recheck impressions and sales after each version before making more. 05 shows "post everything 3 times; repost anything over 60 days old" in a caption montage with no explanation and no card, so it is thin. 03 says valuable content keeps earning for months (claim R106). Condition: the asset must have moved impressions and sales, not just views. Sources: 06, 05 (uncarded), 03. Cards: [4f527d2d3eb2] [26f23bfd7ece].

**R133. Reusing the same story across brand-controlled accounts is 06's advice, recorded with its risk.** 06: post variations to a main brand account and a separate fan or creator account, each slightly different, and stay with the format on both. 06's mini playbook flags that this sits against general platform guidance on duplicate content, which no source addresses. Condition: see C10 before doing it. Source: 06 only. Conflict: C10. Cards: [4f527d2d3eb2].

**R134. One deep piece feeds many formats.** A long-form essay or founder interview becomes shorts, carousels, PDP nuance, buying-guide copy, email and ad creative; 09 scales a winner across platforms with the length adapted. Condition: needs the remix machinery (R137). Sources: 02, 09. Cards: [bda11c7340cf] [3df74f892c3f] [c5eaa02ce9d1].

**R135. Once a story is told well, mark it approved and redeploy the exact line.** 02 reused one Quora opening line ("When I was 17...") hundreds of times over 5 to 10 years; 06 retold the same founder story on YouTube, Twitter and a carousel. Condition: personality content stays on the named person's account (R8). Sources: 02, 06. Cards: [33bc4c19a527] [49c888bb326e] [2147e1a9ca59].

**R136. Retire timely pieces after their window; never resurface a dated post.** Source: 02 only. Cards: [3014faaee9da].

**R137. Value a content asset by the brand's ability to distribute it; do not buy, license or commission a library without the machinery to mine it.** Write down the channels and workflow before spending. Source: 02 only. Cards: [4a3f81e0a69c] [7b9b8ce18fd2].

### 3.12 Teardown and swipe-file method

**R138. Keep categorised swipe files and capture the moment something lands.** 01: separate files for openers, closers, phrases, headlines, connecting words; sources from podcasters, YouTubers, competitor and non-competitor sites, comedians, engineering posts; pull 2 or 3 entries before writing and riff on structure. Split swipe files further by DTC competitor ads and non-competitor ads (banks, SaaS, media), so structure borrowed from a non-retail source never applies unchanged to a physical product's PDP. `[general practice]` 05: folders by the 15 hook types; record on-screen text, spoken words, audio and visual together, because the combination does the work. Condition: ongoing. Sources: 01, 05. Cards: [6ff9c1f9fc32] [9b17f7a80dfc].

**R139. Never paste swiped wording into customer-facing copy.** 01's mini playbook adds this as a legal and brand risk; ecomOS makes it a rule (section 0). Sources: 01 (mini playbook addition), ecomOS. Cards: [6ff9c1f9fc32].

**R140. Tear down a video with the grid: beginning, middle, end against location and visuals, cuts and pacing, audio and script trigger words, on-screen text, lighting, and the viewer's emotional state at each stage.** Add a free "other notes" column. 06's worked example (a teeth-whitening ad answering an influencer callout): beginning in a warehouse, normal pacing, "ripoff" and "disgusting", viewer curious and suspicious; middle switches to a GoPro POV, faster cuts, "fake", Temu and Shein references, viewer fearful of having bought a fake; end reveals the real product in darker purple, an apology, a bundled offer. 09's version: download and transcribe top performers and have AI check hook clarity, pacing and slow sections. 07's version: a spreadsheet of topic, exact hook line and recurring pattern per video. Condition: run it on competitors, out-of-niche winners, and the brand's own top and bottom performers. Sources: 06, 09, 07. Cards: [b7abaa44d689] [646870522f21] [1445bdd3ed8e] [348619262de0].

**R141. Do competitive format research by hand at least the first time.** Search the 3 broadest phrases a customer would type on Instagram, then TikTok and YouTube, note the adjacent phrases those surface, re-search them on Instagram, scroll past the first screen, log what gets unusual views. Manual work trains judgment before any tool. Source: 07 only (its AI tool is a plug). Cards: [348619262de0].

**R142. Track hook type against post performance over time.** 05's example uses an automated Notion agent (a sponsor plug) to pull the hook text and compare it with results; any spreadsheet works. Condition: every post logged with its hook type (R32). Source: 05 only. Cards: [9b17f7a80dfc].

**R143. Study flops as deliberately as winners.** 07 calls the flop list "the most valuable data"; 06 runs the grid on the brand's own weak ads; 09 keeps losers as data for the next round. Condition: every monthly read. Sources: 07, 06, 09. Cards: [6bff3121b5a8] [b7abaa44d689] [c5eaa02ce9d1].

### 3.13 Measurement

**R144. Judge formats over weeks, never by a single post.** 07: a flopped Reel is not a verdict; 03: at least 4 iterations per pillar; 02: do not judge the library by 1 post's attribution; 09: keep losers as data. Condition: every read. Sources: 07, 03, 02, 09. Cards: [6bff3121b5a8] [aa78ae3a6fe1] [bda11c7340cf] [c5eaa02ce9d1].

**R145. Build 3 separate top lists (most views, most followers gained, most comments or deep engagement) plus a flop list.** Expect the lists to differ; expand the formats that recur across the first 2 lists; write a do-not-do list from the flops. Source: 07 only. Cards: [6bff3121b5a8].

**R146. Read retention and the watch rate after 3 seconds per SKU featured, not just per post, so the read shows which products the content builds demand for.** `[general practice]` for reading by SKU. Then read shares in a growth phase and comments plus Story views in a selling phase. Label each period growth or selling and judge posts against the matching metric only. Confirm which fields the analytics surface exposes `[verify UI]`. Source: 04 only. Cards: [3380206cba51].

**R147. For test rounds, measure completion rate, saves, comments, replays, CTR and cost per lead, not raw views or follower count.** Publish variations in a short window, ideally at the same time, to limit time-of-day effects. Source: 09 only. Cards: [c5eaa02ce9d1] [3df74f892c3f].

**R148. If about 70% to 80% of a video's views come from followers and reach is flat, the content is stranger-blind.** Audit the last 5 to 10 posts against R5 and rewrite openers going forward. Source: 07 only. `[verify UI: where the follower vs non-follower split lives]` Cards: [e3a9ae26373a].

**R149. Audit the last 20 videos for topic and avatar consistency before touching content quality.** If all 20 point the same way and growth is still weak, the problem is script, editing or value, not targeting. Source: 08 only. Cards: [34a52f48158a].

**R150. Tie content to business results with simple checks, computed in code.** Sales spikes lined up with post dates, week-on-week sales in a week with several strong posts, impressions that week vs a normal week, month vs prior month, discount codes mentioned only in content, and the same organic post run as a paid ad for a cleaner read (route to 24-DEP; Meta is read only here). ecomOS: missing values show as unavailable, not zero; totals stay separate from breakdowns. Source: 06 only. `[needs brand data: sales by day, impressions by post, code redemptions]` Cards: [8292e101004a].

**R151. Count leads per Reel over time and which keywords produce leads that later convert, not reply volume.** Sources: 07, 09. Cards: [302840d96c34] [00f161224b14].

**R152. Run the next-day recall check alongside the numbers when choosing between concepts.** Source: 06 only. Cards: [d37ea33564f1].

**R153. After any unusually broad hit, check whether engagement stayed inside the avatar slice and whether the next 3 posts held.** Source: 08 only. `[needs brand data]` Cards: [d6fdd4b41759].

**R154. View thresholds decide CTA timing (R118), not "good" or "bad" engagement.** No source gives a good engagement rate, retention rate or share rate. Do not invent one; set the brand's baseline from its own first 3 months. Sources: 03, 04 (silence noted in its mini playbook). Cards: [bf0b2be7f3cf] [3380206cba51].

**R155. In the first phase, the KPI is uploads against the floor (R18).** Sources: 04, 02. Cards: [13325d6dff66] [7d684acdc24b].

### 3.14 Monetisation

**R156. Route attention to the product page and cart, not a vague "product layer": every high-performing post gets a matching PDP or collection link ready before it goes live.** Content is the attention engine; value is captured at the product layer, not the media layer. 08's stack: platform, media (creators), offering. His own early AdSense: about $52 after 12 months and hundreds of hours; occasional $500 to $1,000 brand deals (his case, not a benchmark). Direct attention to owned products, services or affiliate deals with uncapped upside. Condition: every brand account; a pure creator account may differ. Source: 08 only. Cards: [0e331c158903].

**R157. Build an owned list from organic reach; do not build the plan on sponsorships.** 07 stopped taking sponsors ("usually a pain") and attributes about $100,000 and $38,000 from 2 Reels to the email list and his mentorship, not to the Reels. 08 says brand deals sit at the layer with the least value. No source in this folder argues for sponsors; the conflict is with common creator practice. For an ecommerce brand the product is the offer, so sponsorships are a separate revenue decision, not the content model. Condition: any brand with something to sell. Sources: 07, 08. Conflict: C5. Cards: [4a4a14bf5c74] [302840d96c34] [0e331c158903].

**R158. Reach without a monetisation layer is a vanity metric; route spikes to the mid-funnel asset, not a hard pitch.** Source: 09 only. Cards: [5f22157f3977].

**R159.** Moved to Appendix A, section A.3: funding deep thinkers to build the original library as a media-strategy opinion, with no store analogue.

**R160.** Moved to Appendix A, section A.3: owned media as brand strategy, illustrated with a B2B podcast acquisition, with no store analogue.

**R161. Discount codes named only in content are the simplest attribution signal, not a discount strategy.** Source: 06 only. Cards: [8292e101004a].

**R162.** Moved to Appendix A, section A.3: a distinct methodology as a moat, illustrated with a SaaS's own product, with no store analogue.

**R181. Post a "time to reorder" reminder for consumable or replenishable products.** Time the post to the product's typical use-up window and route it to the repeat-purchase customer segment. Condition: consumable, wearable-out or subscription-adjacent products; ties to R157's owned-list point. `[general practice]` No library source; verify against brand data before use.

### 3.15 Brand safety, compliance and ecomOS overrides

**R163. No invented claims; every number, study, result and comparison matches the brand record.** Overrides 06's exaggeration (R44), 05's outcome numbers unless real (R36), 06's uncited Stanford figures and 05's 22x figure (R37), and any AI-suggested statistic (R62). Source: ecomOS; 05 and 02 support the citation condition. Cards: [01267ffe7cb0] [d52d9eff6cd1] [4392aa839fe7].

**R164. Competitor and creator content is a signal for structure, pacing and mood only.** No copying of text, logos, products, faces or footage; no stitched third-party clips without confirmed rights; swipe files are for structure. Source: ecomOS; 06 (structure not content), 07 (no blind copying), 01 (no verbatim swipes) support it. Cards: [646870522f21] [1bdc7fef77c8] [6ff9c1f9fc32] [d22074737dfa].

**R165. The brand record's voice wins over every source's tone advice.** Informality (01), exaggeration (06), hot takes (10), "I" copy (02), negative framing (05) and raw production (09) are options tested inside the voice, never reasons to leave it. Regulated categories (health, finance, legal) and luxury positioning may require a formal register (01's own caveat; 09's own caveat). Source: ecomOS; 01, 09 caveats. Conflict: C9. Cards: [4f3116aa30c6] [ccecf6f16262].

**R166. Reading level below tenth grade on everything; the sources' 5th to 8th grade is the default target (R28).** Source: ecomOS; 01, 05. Cards: [a3cac5e01c5a] [c98d12e4ca71].

**R167. Controversy is allowed only as a true, defensible position the brand holds, and never as an accusation against a named or identifiable competitor without legal review.** 06 builds a moral-outrage ad around counterfeits it calls "obviously illegal" and says to court some controversy and tolerate negative comments; 10 says publish polarising hot takes; 05 says defend the claim in the comments. None checks defamation, platform policy on comparative claims, or health and safety claim rules. Condition: every contrarian, versus, hot-take or counterfeit angle goes through P21. Sources: 06, 10, 05 (as advice), ecomOS (as limit). Conflict: C7. `[web check: platform policy on comparative and competitor claims]` Cards: [6f735c911cc5] [86b7c9130744] [07ab40bc6089] [1ab0e11dcafa].

**R168. Screen any content about real people, legal matters or live news for defamation and implied endorsement.** Card adaptation from 10; the source did not say it. Condition: attention hijacks and pop-culture posts. Cards: [da9c7887e7c9].

**R169. No dangerous stunts, for hooks or challenges.** 04 discourages them even while describing his own risky example. Source: 04 only. Cards: [a0a28a40b29f] [c173b995a2f5].

**R170. AI voices, AI spokespeople and synthetic footage need a disclosure check before publishing.** 06 describes an AI-voiced ad (5 million views, 360,000 likes) without discussing disclosure. Condition: any AI voiceover reuse (R132). Source: 06 (describes), ecomOS (requires). `[web check: current platform and regulatory disclosure rules for synthetic media]` Cards: [4f527d2d3eb2].

**R171. DM automation runs inside current Meta messaging policy with an approved partner; follow-ups respect messaging windows.** Sources: 04, 09 (name ManyChat as approved, per them). `[web check: partner list, policy, pricing]` Cards: [79467cee9f17] [00f161224b14].

**R172. Raw, behind-the-scenes or edgy content for a luxury or regulated brand is tested on a lower-stakes account or not at all.** Source: 09's own caveat; 01's caveat on informal register. Cards: [ccecf6f16262].

**R173. Hook swaps and borrowed footage: rights confirmed, source credited where required, and the teased event real (R34).** Sources: 04, 05 (event must happen), 05's mini playbook (rights), ecomOS. Cards: [d686739bfd6c] [d22074737dfa].

**R174. Keep brands apart and keep public web research separate from private business data.** Gehna, Peach Bucket and TrailFold stories, hooks and results never mix. Source: ecomOS.

**R182. Use shipping and returns policy clarity as pre-purchase trust content.** A short post or Story explaining free returns, delivery time or a guarantee can be the hook for a nervous first-time buyer. Condition: any store where checkout hesitation is a known drop-off point. `[general practice]` No library source; verify against brand data before use.

## 4. Procedures (implementation)

Each procedure: goal, preconditions, steps with settings, checks, rollback, tags. The mini playbooks that supply the steps are named in the heading. Where a source gave the concept but not the steps, the step says so.

### P1. Set the account foundations: positioning, avatar, pillars, stance (07, 08, 03, 01, 02)

Goal: an account that reads as one voice to a stranger and gives the platform a clean topic signal.
Preconditions: brand record loaded (voice, claims, proof points, regulated flags); founder or named person decided (R8); target country known.

1. Write the Creator DNA statement: "I am [X]. I do [Y] for people who [Z]. Listen because [proof]." Fill the proof slot from the brand record only. `[needs brand data: proof point]` [bab1ea1d6132]
2. Run the swap test: paste a direct competitor's name into the statement. If it still reads true, tighten the audience and proof slots until it does not. [bab1ea1d6132]
3. Write the single customer avatar and 10 of their pain points in their words (reviews, support tickets, comments). Ideas come from this list, not from industry trends. [d84a8df8c294]
4. Choose expert or student stance. Expert only if the credential is real; otherwise student. Record which. [4b03755b2896]
5. Choose 2 or 3 pillars from storytelling, ratings and rankings, breakdowns, scenarios. If storytelling is chosen, pair it with at least 1 other. For each pillar, pick the format: talking head, edited vlog, green screen, or carousel. [db75d5f43244] [aa78ae3a6fe1]
6. Record the brand's side on the category's recurring commodity debates (R57) in a positions log for writers and AI. [cbbb787360b8]
7. Record the timely vs timeless mix the brand wants (default: mostly timeless; timely only when the team can ship in under 3 days). [3014faaee9da] [9143824217f6]
8. Write the voice variables from the brand record: preferred word register (neutral, elevated, blunt), sentence rhythm, opinion-led or citation-led. [612587c6befe]

Checks: a stranger reading the statement can name who it is for and why to trust it; every pillar has a named person or a carousel path; no pillar depends on a claim the brand record cannot back.
Rollback: if the account stalls after 3 months at the floor, redo steps 1 to 3 before changing anything else (R149).

### P2. Competitive format research and the idea bank (07, 06, 09, 01)

Goal: 10 to 20 one-line ideas that each pair a proven topic with the brand's angle.
Preconditions: P1 done.

1. List the 3 broadest phrases a customer would type for the category (not brand names). `[needs brand data: phrases]` [348619262de0]
2. Search each on Instagram; scroll well past the first screen; note creators and posts with unusually high views for their size. `[verify UI]`
3. Repeat on TikTok and YouTube; note the adjacent phrases those platforms suggest; re-search those on Instagram.
4. Log per post in a sheet: topic, exact hook line, hook type (R32), format, length, on-screen text style, editing pace, and anything recurring. [348619262de0] [9b17f7a80dfc]
5. For 3 to 5 of the strongest posts, run the teardown grid (P9). [b7abaa44d689]
6. For each logged topic, write the gap: which perspective, method, segment or caveat is missing that the brand's DNA statement can supply. Do not invent a credential to fill it. [1bdc7fef77c8]
7. Add out-of-niche winners (a different category's format that could carry this brand's story) to the same log, marked "structure only". [646870522f21]
8. Write 10 to 20 one-line ideas: "[proven topic] + [brand angle] + [pillar] + [timely or timeless]". Keep the sheet as a permanent bank. [348619262de0]
9. Do this by hand the first time; a research tool may speed later rounds but does not replace the judgment. [348619262de0]

Checks: every idea traces to a logged post or a pain point; no idea is a copy of a logged post's content; ecomOS override: no competitor text, product or face goes into an idea.
Rollback: if the bank fills with lookalikes, redo step 6 with the positions log open.

### P3. Build the monthly calendar (03, 04, 07, 02, 09)

Goal: a 4-week calendar the team can ship at the floor, tagged so the monthly read is possible.
Preconditions: P1 and P2 done; team capacity known; lead magnet status known.

1. Set the floor. New account default: each pillar twice a week, 4 to 6 posts a week. Higher-capacity teams set a higher floor they can hold for 4 weeks (R14). `[needs brand data: capacity]` [aa78ae3a6fe1] [7d684acdc24b]
2. Fill the calendar from the idea bank. Each entry carries: pillar, format, hook type, funnel stage (top, mid, bottom), timely or timeless, series name if any, CTA (none in month 1 on a new account, R118), keyword if a lead magnet is attached.
3. New account format split: about 80% of effort on Reels or short video, the rest carousels and photos, no Story production until followers exist. [fa1ae83e8a27]
4. Reserve 1 or 2 slots a week for a comment-question post from month 2 onward. [aa78ae3a6fe1] [1212d5fe9ec6]
5. Reserve 1 or 2 slots a week for a lead-magnet post once the CTA layer is on (P14). [302840d96c34]
6. Reserve at most 1 or 2 timely slots a week and leave them empty until a real moment appears; if nothing appears, fill from the bank. [9143824217f6]
7. Label the month growth phase or selling phase so the read uses the right metric (R146). [3380206cba51]
8. Hold the exact mix for the full month. Do not change pillars mid-month on single-post results. [aa78ae3a6fe1] [6bff3121b5a8]

Checks: uploads per week equal the floor; every entry has all tags; no entry carries a claim outside the brand record; no more than 1 pillar is storytelling.
Rollback: if the team misses the floor 2 weeks running, lower the floor rather than skipping the read.

### P4. Batch day: script, then film (07, 03, 01)

Goal: 10 to 20 scripts written in one sitting and filmed in one separate session.
Preconditions: calendar (P3) and idea bank (P2).

1. Scripting day (fixed weekday). Take 3 to 5 ideas; for each, run P5 (hook) and P6 (script). Then take the next 3 to 5; continue until 10 to 20 are done (a few hours). [868f6861da16]
2. For each script, plan the visual hook, the first frame, the set or location, and any prop before the words are final. [c173b995a2f5] [cee2da009c53]
3. Prepare on-screen text lines and captions with the keyword where used. [302840d96c34]
4. Filming day (separate day). Set lighting per P20. Film all scripts back to back. Person-led brands film about once every 2 weeks. [868f6861da16] [f63181942aa7]
5. Upload all raw footage to the shared archive the same day (R94). [3b8dc00bf68a]
6. Edit: cut to the first frame where the hook starts; no dead time; captions on. [cae016218009]
7. Keep research, writing and filming strictly separate; do not research on filming day. [868f6861da16]

Checks: every filmed piece passes checklist 5.1 and 5.2; the batch covers the calendar's pillar mix.
Rollback: if a batch runs short, film comment-question posts from the last month's comments rather than skipping uploads.

### P5. Write a hook (05, 04, 01, 06, 07, 10)

Goal: a first 3 seconds a stranger stops for, with an honest payoff.
Preconditions: the idea, the pillar, the brand's positions and claims list.

1. Decide the visual event first: a prop, a face to camera, movement, a lighting change, subject-matched footage, an unusual vantage point, a split screen. Write it down before the words. [c173b995a2f5] [2e322467dede]
2. Pick the hook type from the 15-type menu on purpose; check the hooks bank for the last 5 types used and avoid the habitual one. [9b17f7a80dfc]
3. Draft the line in 5 to 8 words (up to about 12). Name the domain and the stakes; withhold the mechanism. [c98d12e4ca71] [97e147c3e5a1]
4. If the type is curiosity or story, run 01's cover test: cover all but the first 2 sentences; would an indifferent reader need the next one? Repeat to sentence 3 or 4. [26bc815a7b84]
5. If the type is open loop (06), write the unresolved question or claim as sentence 1, optionally stack a second loop, and mark where in the body it resolves. It must not resolve in sentence 2. [c1f05a1e6af3]
6. Write a negative-framed and a positive-framed version of the same line for the hooks bank; the calendar picks one and logs which. [5897c79754a5]
7. Read it aloud: does it sound like a friend or like an ad? Rewrite formula phrasing that a viewer would read as bait, without losing the concrete payoff. [3a5f43d052ea]
8. Run the drunk grandma test on the line and the frame together: zero context, zero effort, instant meaning. Cut jargon and acronyms. [c98d12e4ca71] [9fce1289b063]
9. Check the reading grade (at or below 5th for the hook). `[verify UI: readability tool]` [c98d12e4ca71]
10. Check the payoff: the teased event, count or result must actually appear in the piece, and any number or citation is in the brand record. [0980397e62b4] [d686739bfd6c] [01267ffe7cb0]
11. If contrarian, bold or versus: confirm the brand holds the view and will defend it; route to P21 if a competitor is named or implied. [1ab0e11dcafa] [07ab40bc6089]
12. If a hook swap: confirm the match-cut point exists and the rights are confirmed; if either fails, choose another type. [d22074737dfa]
13. Log the final hook in the hooks bank with type, framing (negative or positive), visual event, and post id once published. [9b17f7a80dfc]

Checks: checklist 5.1.
Rollback: if a hook fails the payoff check, change the type, not the promise.

### P6. Write a script or caption: the 4-step process plus the readability pass (01, 04, 09, 06)

Goal: a script or caption that a stranger understands, that reads at 5th to 8th grade, and that says one thing.
Preconditions: hook from P5; brand voice variables; positions log.

1. Before writing: name the reaction (emotion), the action (comment the keyword, save, share, buy), and the one line to remember. For a headline-plus-subheadline format, write the subheadline (about 180 characters) as the fixed thesis. [5286ee7f0f32] [797d8a7279aa]
2. If the piece is a story, name the intention and the obstacle and plan to reveal both early. [b372918f62e6]
3. Warm up: 10 to 15 minutes of copywork from a swipe-file piece in the target tone (skip for short captions). [c807997f7db2]
4. Dump draft: write fast and badly; show no one. For story topics, the voice-memo transcript (R53) can be the draft. [8c85d056f475] [16e4989b065a]
5. Incubate at least about 90 minutes away from the draft (longer is fine). [8c85d056f475]
6. Edit hard. In order: punch the first sentence and cut background (R47); redundancy pass (R52); cut adverbs, jargon and thesaurus words (R48); vary sentence length, comma to period (R50); write to one person (R51); state the topic and the audience plainly in the spoken script and the caption (R55). [26bc815a7b84] [9fce1289b063] [d8fbcddae70a] [056882fe4e22] [9783e7f32959] [34a52f48158a]
7. Where a line reads as generic category advice, replace it with a specific true story or position from the brand record (R58, R60); keep benefit "you" lines. [2b0c662e2dd0] [33bc4c19a527]
8. Give the piece an ending: a payoff, a reveal or the resolved loop (R93). [b7abaa44d689]
9. Read the whole thing aloud; if you would not say a sentence to a person, rewrite it. [4f3116aa30c6]
10. Run the readability check: 5th to 8th grade, never 10th or above. `[verify UI]` [a3cac5e01c5a]
11. Caption: the first line repeats or extends the hook; the keyword is stated if a lead magnet is attached; no outbound social link (R129). [302840d96c34] [03e0df5b81d9]
12. Optional AI review pass with 09's targeted questions (P7 step 6). [8907bbacfafe]
13. Label timely or timeless; strip dates from timeless pieces. [3014faaee9da]

Checks: checklist 5.2.
Rollback: if the one-line takeaway cannot be stated, the thinking is not done; go back to step 1 rather than editing the prose.

### P7. Write with AI: brief, remix, review, voice fix (02, 09, 06)

Goal: AI output that repeats the brand's approved language and never invents.
Preconditions: positions log, approved stories, voice variables, claims list.

1. Decide the mode per piece: "originated by [name]" (human writes the first version) or "remix" (AI recombines approved language). Net-new positions, first tellings of a story and customer stories are always human. [ad4c55b5d306] [4392aa839fe7]
2. Brief the model with: the positions log entries that apply, the approved stories to draw from, the voice variables, the claims list, the reading-grade target, the hook type, and the platform length. [cbbb787360b8] [612587c6befe]
3. For variation work, ask for 10 or more hooks, alternate openings, per-platform captions, and benefit-emphasis versions of one human idea. [c5eaa02ce9d1]
4. For 09's "hook ideas similar to top performers in my niche", use the output only as structure; rewrite any line that echoes a specific creator. [1445bdd3ed8e]
5. Do not ask for "extremely exaggerated" versions (06). Ask instead for "the most specific, most concrete true wording" of a real event. [d52d9eff6cd1]
6. Review pass: paste the script or caption and ask "Is the hook clear in under 3 seconds?", "Would the target market immediately understand what this is about?", "Make this shorter and easier to read on a phone", "Where could I cut so viewers don't drop off?". Apply the edits by hand. [8907bbacfafe]
7. Fact check every claim, number and product fact against the brand record; AI repeats, it does not verify. [4392aa839fe7]
8. If the draft "doesn't sound like us", find the single off variable (word register, sentence rhythm, opinion vs citation) and make the smallest edit; add the finding to the voice guide. [612587c6befe]
9. Tag the piece with its mode and note whether it added net-new thinking to the library (R64). [1193451bea64]

Checks: checklist 5.7.
Rollback: if a remix cannot be traced to approved language, treat it as an originated draft and send it to a human writer.

### P8. Mine and build a brand or founder story (06, 01, 02)

Goal: a bank of approved, true stories that replace generic claims.
Preconditions: the founder's real history and permission to use it; customer permissions.

1. Ask the founder question set (R66) in an interview or voice memos; record answers verbatim. `[needs brand data: founder history, failures, sourcing trips]` [9143824217f6]
2. Add the low-stakes moments (a shipping mishap, a packaging argument) rendered with honest weight. [9affec3cf159]
3. For each candidate, run the voice-memo test: would the founder tell a friend this unprompted? Drop the ones that fail. [16e4989b065a]
4. For each survivor, write the intention and the obstacle in 1 line each. [b372918f62e6]
5. Map the emotional trigger (curiosity, moral outrage, belonging, confusion, visual shock) and pair it with a delivery technique (novelty, relatability, visual shock, trend relevance, credibility, controversy). Controversy routes to P21. [6f735c911cc5]
6. Write each story once well (P6). Mark it approved. Store it in the unmade data set with labels (topic, emotion, formats used). [33bc4c19a527] [0d61d18719cc]
7. For a same-day asset: the 30-minute carousel. 10 to 20 years, 1 iconic event per year including failures, 1 photo per moment, a text overlay per photo, assemble, post. [2147e1a9ca59]
8. Decide the account for each story: personal biography on the named person's account, agreed positions on the brand account. [49c888bb326e]

Checks: every story is true and attributable; intention and obstacle are visible in the first 3 sentences; no competitor is accused.
Rollback: if the founder cannot supply stories, run the student stance (P1 step 4) and the tour-guide reframe (R76) instead.

### P9. Frame-swipe teardown grid (06, 09, 07)

Goal: a structural blueprint from a winning video, without its content.
Preconditions: a chosen video, out of niche where possible; the brand's own top and bottom performers for the internal version.

1. Watch once straight through. [646870522f21]
2. Build the grid: rows beginning, middle, end; columns location and visuals, cuts and pacing, audio and script trigger words, on-screen text and captions, lighting, viewer emotional state. Add "other notes to copy". [b7abaa44d689]
3. Watch again and fill every cell with the concrete choice at that stage. Track the viewer's emotion explicitly; misreading it is the common failure. [b7abaa44d689]
4. Optional: transcribe the video and ask AI where the hook lands, where pacing slows, and where a viewer would drop off. [1445bdd3ed8e]
5. Rebuild the structural choices with the brand's own product, story and script. Reuse none of the source's content. [646870522f21]
6. Check the rebuilt piece routes the borrowed attention into the brand's actual message (a tip, a demo, a story). [d22074737dfa]
7. Run the same grid on the brand's own top 3 and bottom 3 posts each month; write the flop patterns into the do-not-do list. [6bff3121b5a8]

Checks: no cell of the rebuild contains the source's words, footage or product; the ending row is filled (R93).
Rollback: if the structure only works with the source's content, it is a copy; drop it.

### P10. Design a series or challenge (09, 04, 06, 10)

Goal: a named, repeatable format the team can produce at volume.
Preconditions: at least 1 concept that beat the account's baseline on the macro read (P15); or, for a new account, a pilot slot.

1. Start with 1 core idea (a tip, an insight, a demo, a versus, a tour-guide episode). [3df74f892c3f]
2. Generate hook, length and angle variations (P7 step 3) and publish 3 to 5 of them in a short window. [c5eaa02ce9d1]
3. Measure on completion, saves, comments and replays, not views. [3df74f892c3f]
4. Refine the winner with small changes (shorter, stronger hook, tweaked CTA) and repost. [3df74f892c3f]
5. Scalability test: can a team make many episodes in a day without the founder's body? Cooking and travel fail; interview, street-interview, ratings and versus formats pass. If it fails, keep it as an occasional pillar, not the series. [34c4c10786ba]
6. Pilot for 1 week and check impressions and sales before committing team or archive resources. [34c4c10786ba]
7. Package: a name, a visual signature, a promise of what each episode gives, a fixed opening beat. [3df74f892c3f]
8. If it is a challenge: it must be a genuine stretch for the person, safe, and doable daily; for a product, make the repeatable demo the challenge ("day [N] of using the product in a new place"). Community participation is optional. [a0a28a40b29f]
9. Set the cadence (09's case ran twice a week) and add it to the calendar for at least 8 weeks. [3df74f892c3f]
10. Keep at least 1 other format live so the account never depends on 1 series (R92). [3df74f892c3f] [34c4c10786ba]

Checks: episodes 1 to 3 pass checklist 5.1 and 5.2; the series has a stage tag and a CTA plan; the name is in the calendar.
Rollback: if 4 episodes fall below the account baseline on the phase metric, pause the series and study it in P9 before killing it.

### P11. Publish manually and test a scheduler (03, 08)

Goal: consistent native posting, and a brand-specific answer on schedulers.
Preconditions: the account is registered and posted from the target country; account types set (R112, R113) `[verify UI]`.

1. Default: upload every post natively, by hand, on each platform. Budget 2 to 3 minutes per platform. [7ff53d5768f7]
2. Post to the hero platform first; cross-post to secondary platforms with zero expectation and no cross-platform call-outs. [19bea8d6aaa6] [03e0df5b81d9]
3. State the topic and the audience in the caption; put the keyword in the caption if a lead magnet is attached; no outbound social links. [34a52f48158a] [302840d96c34]
4. Scheduler test, once the account has 4 weeks of manual baseline: alternate weeks (manual, scheduled, manual, scheduled) with the same pillar mix; log non-follower reach, retention and shares per post. Compare in code. Record the result in the experiment log. [7ff53d5768f7]
5. Adopt whichever the brand's own data supports; 03's penalty claim stays a hypothesis until then.

Checks: every post went out at the floor; captions carry topic, audience and keyword.
Rollback: if the scheduled weeks show lower non-follower reach across 2 cycles, return to manual.

### P12. Set up comment-to-DM and the thank-you DM (04, 07, 09)

Goal: engagement on a post turns into a captured lead without sending the viewer to the bio.
Preconditions: a lead magnet that matches audience demand (R122) and a page or file to deliver (07-LPG); an email or CRM destination (14-EML); current policy checked.

1. Choose the DM automation tool. Sources name ManyChat and call it Meta-approved (per them). `[web check: current approved partner list, policy, pricing]` [79467cee9f17] [00f161224b14]
2. Pick 1 distinct keyword per campaign (for example GUIDE, SIZE, SEARCH). [79467cee9f17] [302840d96c34]
3. Build the flow: comment containing the keyword triggers a DM with the asset link; the DM asks for an email where the asset is gated; the email lands in the list or CRM. `[verify UI]` [00f161224b14]
4. Turn on the new-follow DM with a thank-you only, no offer. `[verify UI]` [b539e41f421e]
5. Test the whole flow end to end with 2 team accounts before any post goes live. [00f161224b14]
6. Put the keyword on screen and in the caption of the triggering post. [302840d96c34]
7. Attach the flow to 1 or 2 posts a week, not every post. [302840d96c34]
8. Set up the backend read: opens, clicks, emails captured, purchases per keyword. `[needs brand data]` [13e3b50fabea]
9. Build the follow-up for clicked-not-bought: a short, time-boxed personal message referencing the interest and any deadline, inside messaging rules. [13e3b50fabea]
10. Confirm intake capacity (who answers replies, who fulfils) before the first post. [4a4a14bf5c74]

Checks: checklist 5.8.
Rollback: turn the automation off and revert to a manual DM reply if the flow breaks or policy changes.

### P13. Run the comment and DM sales process (03, 04, 08)

Goal: every question becomes a reply, and every lead gets a next step.
Preconditions: someone owns the inbox daily.

1. Reply to every comment with a specific answer, not "thanks!". [eaadc77a360f]
2. Reply to every DM personally. [eaadc77a360f]
3. When a commenter asks a product question, DM them: answer, then offer the next step (a code, a size guide, a booking link). [eaadc77a360f]
4. Low-ticket: send the product link. High-ticket or considered: offer a call or consultation. `[needs brand data: price ladder]` [3dd25615d38b]
5. Comment on other accounts' posts in the niche on the hero platform. [e46ef6c2491a]
6. Log leads by post and by keyword. [302840d96c34]
7. Pull the comment questions into the idea bank for comment-question posts. [1212d5fe9ec6]

Checks: median reply time is measured `[needs brand data]`; no lead sits unanswered past the day.
Rollback: if volume exceeds capacity, hand the inbox to a sales team but keep the personal standard.

### P14. Add the CTA layer after traction (03, 07, 09, 04)

Goal: CTAs that arrive when the account can carry them.
Preconditions: month 1 done with no CTA on a new account (R118); a mid-funnel asset exists (R122).

1. Check the view threshold: posts consistently at about 5,000 views (about 2,000 in a very narrow niche). If not met, see C4 for the alternative path and record the choice. [bf0b2be7f3cf]
2. Introduce soft CTAs first: a lead magnet by keyword (P12) on 1 or 2 posts a week. [302840d96c34]
3. Route spikes to the mid-funnel asset, never to a hard pitch. [5f22157f3977]
4. Keep the pillar mix and the floor unchanged while adding the layer; do not cut content to sell. [bf0b2be7f3cf]
5. Once followers exist, move hard CTAs to Stories. [4c8610731e7c]
6. Add hard CTAs (buy) only on bottom-funnel posts and only for low-ticket products in-app. [3dd25615d38b]
7. Layer launches: 1 or 2 a year plus seasonal, on top of continuous lead magnets. [3dd25615d38b]

Checks: the ratio of CTA posts to non-CTA posts is logged; non-follower reach is watched for 4 weeks after the layer goes on.
Rollback: if non-follower reach falls for 4 weeks after CTAs start, drop back to keyword-only CTAs on 1 post a week and re-read.

### P15. Monthly performance read (07, 04, 03, 09, 06, 08)

Goal: patterns over weeks, not verdicts on posts.
Preconditions: 4 weeks at the floor; post-level export; phase label for the month.

1. Confirm uploads against the floor. If under, the read is about capacity, not content. [7d684acdc24b]
2. Baseline health: retention and watch rate after 3 seconds per post. [3380206cba51]
3. Phase metric: shares in a growth month; comments and Story views in a selling month. [3380206cba51]
4. Build the 3 top lists (views, followers gained, comments or deep engagement) and the flop list. [6bff3121b5a8]
5. Per pillar: after 4 iterations, which pillar, topic and format pulls. [aa78ae3a6fe1]
6. Stranger check: follower share of views per post; flag posts at 70% to 80% or more with flat reach. `[verify UI]` [e3a9ae26373a]
7. Topic check: last 20 videos consistent on topic and avatar? If yes and growth is weak, the fix is script, editing or value. [34a52f48158a]
8. Hook-type read: performance by hook type and by negative vs positive framing from the hooks bank. [9b17f7a80dfc] [5897c79754a5]
9. Lead read: leads per post and per keyword; DM opens, clicks, purchases; clicked-not-bought count. [302840d96c34] [13e3b50fabea]
10. Business read in code: sales spikes against post dates, week-on-week sales in strong weeks, code redemptions, impressions vs a normal week. Missing values show as unavailable. `[needs brand data]` [8292e101004a]
11. Broad-hit check: after any unusually broad post, did the next 3 posts hold? [d6fdd4b41759]
12. Next-day recall check on the month's top 10 by the team. [d37ea33564f1]
13. Write the do-not-do list from the flops and the "expand" list from the recurring winners; feed both into P3 for next month. [6bff3121b5a8]
14. Decide the next month's floor: raise only if the content works and capacity allows. [8292e101004a]

Checks: checklist 5.4.
Rollback: no strategy change on fewer than 4 iterations per pillar or fewer than 4 weeks.

### P16. Hook and variation test loop: S.G.T.M.S. (09, 05)

Goal: a fast read on which hook, cut or caption of one idea to scale.
Preconditions: 1 strong idea; the ability to publish several variations in a short window.

1. Start with 1 idea. [c5eaa02ce9d1]
2. Generate 10 or more variations: hooks (across types and framings), cuts, captions per platform, benefit emphasis, translations if relevant. [c5eaa02ce9d1]
3. Test: publish the chosen 3 to 5 within a short window, ideally the same time of day, on the hero platform or a satellite account. [c5eaa02ce9d1]
4. Measure: completion, saves, comments, replays, CTR and cost per lead where tracked; not raw views. [c5eaa02ce9d1] [3df74f892c3f]
5. Scale the winner across platforms and formats; log losers by hook type for the next round. [c5eaa02ce9d1] [9b17f7a80dfc]
6. No source gives a minimum sample for a confident read; treat 1 round as a signal and 3 rounds as a pattern (unsourced house default, see section 6).

Checks: variations differ in hook type or framing, not in 1 word; claims are identical across variations and match the brand record.
Rollback: a round with no clear winner is data; do not pick by taste.

### P17. Life-extend a winner (06, 02, 09)

Goal: 4 or more uses of one proven asset.
Preconditions: the asset moved impressions and sales, not only views.

1. Confirm the win on the business read (P15 step 10). [4f527d2d3eb2]
2. Version 2: new hook, same body. Version 3: text carousel from the script. Version 4: AI voiceover or new footage (disclosure check, R170). [4f527d2d3eb2]
3. Adapt length per platform (60 seconds vs 3 minutes as 09's example). [3df74f892c3f]
4. Space the versions across weeks; recheck impressions and sales after each before making the next. [4f527d2d3eb2]
5. Cross-account reuse only after the C10 decision is recorded for the brand. [4f527d2d3eb2]
6. Mark the underlying story approved in the library so the exact line can be redeployed later. [33bc4c19a527]
7. Retire any version that carried a date or trend reference once the window closes. [3014faaee9da]

Checks: each version differs in wrapper; the story and claims are unchanged.
Rollback: stop at the first version that fails to move the phase metric.

### P18. Train a new or refocused account on one topic (08, 04)

Goal: a clean topic signal over 30 to 50 videos.
Preconditions: P1 done.

1. One topic, one avatar, ideas from pain points. [d84a8df8c294]
2. Name the topic and audience in speech and caption on every post. [34a52f48158a]
3. Post 30 to 50 consecutive videos on that topic before judging whether the platform has found the audience (claim R98). [d84a8df8c294]
4. Avoid: mixing topics, content the avatar would not value, broad content that does not apply to the avatar. [d84a8df8c294]
5. During this run, track uploads as the KPI and set the 8% a month growth expectation from 04 as an expectation, not a target. [13325d6dff66]
6. At the end of the run, do the last-20-video audit (R149) and the follower-share check (R148).

Checks: no post in the run is off topic.
Rollback: a mixed month restarts the count.

### P19. Founder-capacity plateau: diagnose and build the bench (06)

Goal: remove the founder as the bottleneck without losing the voice.
Preconditions: flat or falling sales with a founder-led account.

1. Confirm the founder is the primary creator and output is capped (about once a day). [8292e101004a]
2. Check whether competitors entered the category since the plateau started. [8292e101004a]
3. Run the business read (P15 step 10) before changing anything. [8292e101004a]
4. Choose a scalable format (P10 step 5). [34c4c10786ba]
5. Hire for proven views: an influencer, videographer or social manager who has had a video perform; or promote the employee who already posts. [3b8dc00bf68a]
6. Start the shared footage archive: founder, staff and family upload every usable clip, continuously. [3b8dc00bf68a]
7. Recruit editors, give them the archive and examples, pay a CPM base plus a bonus for videos that go viral and convert; rates are not given. `[needs brand data: budget]` [3b8dc00bf68a]
8. If the content works, raise the floor above once a day; if not, fix the content before adding people. [8292e101004a]

Checks: the founder still supplies stories and positions (R56); the brand voice guide is in the editors' brief.
Rollback: if editor output drifts from the voice, tighten the brief with the voice variables before cutting the program.

### P20. Lighting and set (07, 03)

Goal: a first frame that looks intentional on a phone camera.
Preconditions: 1 to 2 hours, a window or a cheap softbox, a few lamps.

1. Turn off ambient room light. [26bf14383383]
2. One key light facing the subject: a large window or a cheap softbox. `[web check: current low-cost options]` [26bf14383383]
3. Practical background lights (lamps, small warm lights) for depth. [26bf14383383]
4. Choose a consistent set that fits the stance: a wall of product, a workshop, a kitchen; a student displays what they have tested; an expert dresses the part. [3f6eca540367]
5. Compare before and after on the same phone; the lit version must read as deliberate. [26bf14383383]
6. If filming outdoors for variability, keep the key light rule in mind (a shaded spot, face to the light). [4289340e4d3b]

Checks: the half-second screenshot test passes (R35).
Rollback: if the set distracts from the subject, simplify it; the set cannot rescue weak content.

### P21. Compliance and brand-safety check before publishing (all sources' risks; ecomOS overrides)

Goal: nothing goes out that invents a claim, copies a competitor, breaks the voice, defames anyone, or breaks platform policy.
Preconditions: brand record with claims list, voice rules, regulated flags.

1. Claims: every number, study, comparison, product fact and outcome is in the claims list. Uncited stats (22x, 5% vs 63%) are removed. [01267ffe7cb0]
2. Exaggeration: any charged line is literally true and matches a real event; "crisis", "scam", "toxic" and similar words pass only with evidence. [d52d9eff6cd1]
3. Copying: no competitor or creator text, footage, logo, product or face; borrowed clips have confirmed rights; frame swipes are structure only. [646870522f21] [d22074737dfa]
4. Competitors: no accusation (counterfeit, illegal, fake) against a named or identifiable competitor without legal review; versus content about named brands passes the same review. [6f735c911cc5] [a38c90da39f7]
5. Real people and news: no defamation, no implied endorsement, no use of a real person's likeness without permission. [da9c7887e7c9]
6. Voice: the piece sits inside the brand record's voice; informal, edgy, negative or exaggerated options are inside the allowed range or they are cut. [4f3116aa30c6]
7. Regulated or luxury: raw or provocative content is on a lower-stakes account or dropped; health, finance and legal claims meet the category's rules. [ccecf6f16262]
8. Safety: no dangerous stunt, no challenge that could harm. [a0a28a40b29f]
9. Synthetic media: AI voice or spokesperson disclosed per current rules. `[web check]` [4f527d2d3eb2]
10. Automation: comment-to-DM and follow-ups inside current Meta policy with an approved partner. `[web check]` [79467cee9f17]
11. Identity hooks: no judgmental labels. [e679699e4817]
12. Reading level below tenth grade; no em dashes; no inflated words.
13. Brand separation: no other brand's data, story or hook in the piece.

Checks: checklist 5.5.
Rollback: any failed item blocks publishing; fix or drop.

### P22. Choose the hero platform (08, 03)

Goal: 1 platform to judge the channel by for 6 months.
Preconditions: some customers or a proxy.

1. List the candidates: Facebook, YouTube, LinkedIn, TikTok, Instagram, X `[web check: current usage]`. [e46ef6c2491a]
2. Ask a small random sample of customers which platform they use most; if not possible, use where the team learns about the category as a proxy. `[needs brand data]` [e46ef6c2491a]
3. Pick the densest platform; add email as the only other channel. [e46ef6c2491a]
4. If the answer is a tie between TikTok and Instagram, run both as the base and cross-post between them (03), but read results on 1. [19bea8d6aaa6]
5. Commit for 6 months before adding a platform. [e46ef6c2491a]
6. On the hero platform: post video, reply to comments, comment on niche posts, and use the secondary format (Stories) once followers exist. [e46ef6c2491a]

Checks: the calendar names the hero platform; the read uses its data.
Rollback: switch platforms only after a 6-month read shows the customers are elsewhere.

## 5. Diagnostic checklists

Written so a worker can run each one alone. Columns: what to check | how | good | bad | fix | source.

### 5.1 Hook review

| what to check | how | good | bad | fix | source |
|---|---|---|---|---|---|
| Visual event exists | Watch the first 3 seconds with sound off | A prop, face, movement, lighting change or subject-matched shot reads clearly | Only text or speech carries the open | Rebuild the open around a visual event before rewriting words | 04, 05 [c173b995a2f5] [cee2da009c53] |
| Half-second frame | Screenshot at about 0.5 s | A stranger can say what the video is about | Ambiguous, generic (typing, desk) or unrelated frame | Reshoot or recut to a subject-matched, uncluttered, high-contrast frame | 05 [cee2da009c53] [cae016218009] |
| Dead time | Watch the first 1 s | Hook already active | Pause, setup shot, "millennial pause" | Trim to the first frame where the hook starts | 05 [cae016218009] |
| Word count | Count words in the on-screen or spoken line | 5 to 8; up to about 12 | 13 or more, or under 4 without a complete thought | Cut words; drop clauses | 05 [c98d12e4ca71] |
| Reading grade | Readability tool `[verify UI]` | At or below 5th grade | 6th or above | Replace multi-syllable and niche words | 05, 01 [c98d12e4ca71] [a3cac5e01c5a] |
| Drunk grandma | Read line and frame with zero context | Instant meaning, no decoding | Needs an acronym, insider term or a beat of thought | Simplify vocabulary; cut jargon | 04, 05 [9fce1289b063] |
| Hook type logged | Check the hooks bank entry | Type and framing recorded; not the same type as the last 3 posts | No type, or the habitual type again | Pick a different type from the 15 | 05 [9b17f7a80dfc] |
| Curiosity gap width | Ask: does it reveal the mechanism? does it name domain and stakes? | Domain and stakes named, mechanism withheld | Reveals everything, or reveals nothing identifiable | Add back domain and stakes, or remove the resolution | 05, 01 [97e147c3e5a1] [26bc815a7b84] |
| Open loop timing | Find where the loop resolves | Resolves after the body, not in sentence 2 | Closed in the next sentence | Move the answer later; educate in between | 06 [c1f05a1e6af3] |
| Payoff is real | Compare the promise to the body | The teased event, count or result appears | Bait: the promise is never delivered | Reshoot, reframe or soften the promise | 01, 04, 05 [0980397e62b4] [d686739bfd6c] [9dd434350255] |
| Formula vs friend | Read aloud | Sounds like a friend and still names a concrete payoff | "3 mistakes...", "stop doing this" with no specific payoff, or vague chat | Rewrite conversationally; keep the payoff | 07 [3a5f43d052ea] |
| Negative or positive framing | Check the bank | A framing was chosen on purpose and logged; both versions exist | Framing by habit; threat words outside the voice | Write the other version; choose inside the voice | 05, ecomOS [5897c79754a5] |
| Numbers and citations | Check the claims list | Every number and named source is in the brand record and realistic | Extreme, unbacked or uncited | Remove or replace with a backed number | 05, ecomOS [01267ffe7cb0] |
| Contrarian or bold claim | Ask the owner | The brand holds it and will defend it in comments | Made for reach only | Soften or use a different type | 05, 10 [1ab0e11dcafa] [07ab40bc6089] |
| Identity language | Read the label | Describes behaviour | Judgmental or stereotyping ("lazy moms") | Rewrite around behaviour | 05 [e679699e4817] |
| Hook swap match cut | Compare last borrowed frame and first own frame | Motion or composition continuous; rights confirmed | Jump cut, or no rights | Pick another clip or another type | 05, 04 [d22074737dfa] |
| Sound dependence | Watch on mute | The hook still works | Only a sound effect interrupts | Add text and a visual interrupt | 05 [11f62e1913d1] |
| Stranger context | Read assuming zero history with the brand | No inside reference | Product nickname, past post, inside joke | Rewrite the first line | 04, 07 [37ea3485764f] [e3a9ae26373a] |

### 5.2 Script and caption review

| what to check | how | good | bad | fix | source |
|---|---|---|---|---|---|
| Reaction, action, one line | Ask the writer for all 3 | Stated in 1 sentence each | Missing or several takeaways | Cut material that does not serve the one line | 01 [5286ee7f0f32] |
| Intention and obstacle (stories) | Pause at any point | Both can be named instantly | One is missing or arrives late | Foreground the missing piece; move it earlier | 01 [b372918f62e6] |
| First sentence | Read only sentence 1 | Thesis, promise or provocative true claim | Background, intro, context | Delete until the punch is first | 01, 04 [26bc815a7b84] [37ea3485764f] |
| Redundancy | Read each sentence asking "already said?" | No synonyms stacked | "fit, lean, lose weight, healthy" | Cut repeats | 04 [9fce1289b063] |
| Readability | Tool `[verify UI]` | 5th to 8th grade; never 10th or above | Above 8th; adverbs, jargon, thesaurus words | Run the readability pass | 01, ecomOS [d8fbcddae70a] |
| Read aloud | Say it to a person | Every sentence is speakable | Corporate or LinkedIn words ("utilize") | Rewrite in spoken form | 01 [4f3116aa30c6] |
| Rhythm | Scan sentence lengths | Mostly short, some medium, rare long | Uniform long sentences, commas everywhere | Comma to period; vary | 01 [056882fe4e22] |
| One person | Ask who it is written to | A named real or composite customer | "Everyone" | Rewrite to the avatar | 01, 08 [9783e7f32959] |
| Commodity lines | Look for "you should", "we care about quality" | Replaced with a specific true story or position; benefit "you" lines kept | Generic advice any competitor could post | Insert the approved story or position | 02 [2b0c662e2dd0] [33bc4c19a527] |
| Positions | Compare to the positions log | Takes the brand's side on any debate it touches | Silent default to category consensus | Add the position or mark neutral | 02 [cbbb787360b8] |
| Ending | Read the last 3 lines | A payoff, reveal or resolved loop | Stops after the middle | Add the ending row from the teardown grid | 06 [b7abaa44d689] |
| Topic and audience stated | Read the script and caption | Both name the topic and who it is for | Only implied | State them plainly | 08 [34a52f48158a] |
| Keyword | Check caption and on-screen text | Keyword present if a lead magnet is attached | Missing or 2 keywords | One keyword, stated in both | 04, 07 [79467cee9f17] |
| Outbound links | Scan caption | Only owned destinations, via keyword or bio | "Watch my YouTube", raw URL to another social | Remove | 08 [03e0df5b81d9] |
| Timely or timeless | Look for dates and "just launched" | Labelled; timeless pieces carry no date | Unlabelled; a date in a timeless piece | Label; strip the date | 02 [3014faaee9da] |
| SHARE | Run the 5 letters | Simple, hooked, authentic, specific, entertainment-led | Vague, over-edited, education-only | Apply the missing letter | 04 [9fce1289b063] |
| AI mode | Check the tag | "remix" or "originated by [name]" | Untagged AI draft | Tag; route net-new thinking to a human | 02 [ad4c55b5d306] |
| Claims | Compare to the claims list | All match | Any unbacked claim | Remove | ecomOS |
| Voice | Compare to the voice variables | Register, rhythm and stance match the brand record | One variable off | Smallest edit on that variable | 02, ecomOS [612587c6befe] |

### 5.3 Monthly calendar review

| what to check | how | good | bad | fix | source |
|---|---|---|---|---|---|
| Floor | Count planned posts per week | At or above the floor the team held last month | Below floor, or above what the team can hold for 4 weeks | Reset to a sustainable floor | 02, 03, 07 [7d684acdc24b] [aa78ae3a6fe1] |
| Pillar mix | Count posts per pillar | 2 to 3 pillars, each about twice a week; storytelling not alone | 1 pillar, or 4 or more, or storytelling only | Rebalance | 03 [aa78ae3a6fe1] |
| Format split (new account) | Count by format | About 80% short video, rest carousel and photo, no Stories | Story production before followers exist | Shift effort to Reels | 04 [fa1ae83e8a27] |
| Tags complete | Read each entry | Pillar, format, hook type, stage, timely or timeless, series, CTA, keyword | Any tag missing | Fill before the batch day | this playbook |
| CTA status | Count CTA posts | Month 1 new account: 0; after traction: keyword CTAs on 1 to 2 posts a week | Hard sells before threshold; CTA on every post | Follow P14 | 03, 07 [bf0b2be7f3cf] [302840d96c34] |
| Stage coverage | Count by stage | Mostly top of funnel, some mid, bottom only after traction | All bottom of funnel | Rebalance | 09 [5f22157f3977] |
| Timely slots | Count | 1 to 2 open slots a week, filled only for real moments | Half the month is reactions, or no capacity to react in 3 days | Cap timely slots | 02, 06 [3014faaee9da] [9143824217f6] |
| Series | Check named series | Each series has a name, signature, promise and 8-week run | One-off experiments only | Package a winner (P10) | 09 [3df74f892c3f] |
| Comment-question posts | Count from month 2 | 1 to 2 a week | None | Pull questions from comments | 03 [1212d5fe9ec6] |
| Topic discipline | Read all entries | One topic, one avatar | Mixed topics | Move off-topic ideas to a separate line or account | 08 [d84a8df8c294] |
| Stranger test | Read the hooks | No inside references | Inside jokes | Rewrite | 04, 07 [37ea3485764f] |
| Batch feasibility | Compare to the filming schedule | All entries can be filmed in the planned sessions | Needs daily filming | Move to batch or cut | 07, 03 [868f6861da16] |
| Claims | Scan for claims | All in the claims list | Any invented | Remove | ecomOS |
| Phase label | Check the header | Growth or selling stated | Missing | Add | 04 [3380206cba51] |
| Capacity for leads | Ask who answers | Inbox owner and fulfilment named | Nobody | Assign before lead-magnet posts | 07 [4a4a14bf5c74] |

### 5.4 Post-performance read (monthly)

| what to check | how | good | bad | fix | source |
|---|---|---|---|---|---|
| Uploads vs floor | Count | At floor | Under | Fix capacity before judging content | 02, 04 [7d684acdc24b] |
| Iterations per pillar | Count | 4 or more | Fewer | Do not judge that pillar yet | 03 [aa78ae3a6fe1] |
| Retention and 3-second watch rate | Export per post | Stable or rising month on month | Falling | Hook and first-frame review on the bottom posts | 04 [3380206cba51] |
| Phase metric | Shares (growth) or comments and Story views (selling) | Matches the month's label | Wrong metric reviewed | Realign | 04 [3380206cba51] |
| Three lists | Views, followers gained, comments | Recurring formats across lists 1 and 2 | Judgments post by post | Build the lists | 07 [6bff3121b5a8] |
| Flop list | Bottom 5 by phase metric | Named patterns in a do-not-do list | Skipped because it hurts | Write it | 07 [6bff3121b5a8] |
| Follower share of views | Per post `[verify UI]` | Below about 70% or reach rising | 70% to 80% or more with flat reach | Stranger rewrite of openers | 07 [e3a9ae26373a] |
| Last 20 topic audit | Scroll | Same topic and avatar | Scattered | Fix topic before quality | 08 [34a52f48158a] |
| Hook type and framing | Hooks bank vs results | A type or framing recurs among winners | No log | Log going forward | 05 [9b17f7a80dfc] |
| Leads per post and keyword | DM tool export | Rising; keywords that convert identified | Reply volume only | Track conversion by keyword | 07, 09 [302840d96c34] [00f161224b14] |
| Clicked not bought | DM tool export | A follow-up went out | None | Build the follow-up | 04 [13e3b50fabea] |
| Business tie | Sales by day vs post dates, codes, impressions, in code | Visible lift in strong weeks | No lift despite views | Run the winner as a paid ad for a cleaner read (24-DEP) | 06 [8292e101004a] |
| Broad hit aftermath | Next 3 posts after an outlier | Held | Dropped | Return to on-target content | 08 [d6fdd4b41759] |
| Next-day recall | Team test on the top 10 | Story pieces remembered | High views, nothing remembered | Add the story layer | 06 [d37ea33564f1] |
| CTA effect | Non-follower reach 4 weeks after CTAs started | Held | Fell | Drop to keyword-only on 1 post a week | 03 [bf0b2be7f3cf] |
| Series health | 4 latest episodes vs baseline | At or above | Below | Study in P9 before killing | 09 [3df74f892c3f] |
| Comparison discipline | Read the report | No "vs competitor X's followers" | Outcome comparisons | Redirect to format ideas | 04 [38b7805726e7] |
| Missing data | Check every metric | Unavailable shown as unavailable | Zeros for missing | Fix the export | ecomOS |

### 5.5 Compliance and brand-safety check

| what to check | how | good | bad | fix | source |
|---|---|---|---|---|---|
| Claims | Compare every number, study, result, product fact to the claims list | All backed | Any unbacked, or 22x or 5% vs 63% quoted | Remove | ecomOS, 05 [01267ffe7cb0] |
| Exaggeration | Read charged words | Literally true, tied to a real event | "Crisis", "scam", "toxic" without evidence | Rewrite to the true, specific line | 06, ecomOS [d52d9eff6cd1] |
| Copying | Compare to the source video and swipe file | Structure only; own words, footage, product, faces | Any lifted text, clip, logo or face | Remove | ecomOS, 06, 01 [646870522f21] [6ff9c1f9fc32] |
| Borrowed clip rights | Check the rights record | Confirmed in writing | Assumed | Do not publish | 05 (mini playbook), ecomOS [d22074737dfa] |
| Competitor accusations | Read for "fake", "counterfeit", "illegal", "ripoff" | No named or identifiable target, or legal review done | Accusation without review | Hold for legal | 06, ecomOS [6f735c911cc5] |
| Versus content | Check named brands | Verdict with reasons; no false comparative claim | Unbacked comparison | Rewrite or hold | 10 [a38c90da39f7] |
| Real people and news | Read for names and likenesses | Factual, no implied endorsement, permission where needed | Defamation or endorsement risk | Cut or hold | 10 (card adaptation) [da9c7887e7c9] |
| Voice | Compare to the brand record | Inside the allowed register | Informal, edgy or exaggerated beyond the record | Rewrite | ecomOS, 01 [4f3116aa30c6] |
| Regulated or luxury | Check the brand's flags | Raw or provocative content on a lower-stakes account or dropped; category rules met | On the main account | Move or drop | 09 [ccecf6f16262] |
| Safety | Read the stunt or challenge | Safe | Any harm risk | Drop | 04 [a0a28a40b29f] |
| Synthetic media | Check for AI voice, face or footage | Disclosed per current rules `[web check]` | Undisclosed | Add disclosure or drop | 06, ecomOS [4f527d2d3eb2] |
| DM automation | Check partner and flow | Approved partner, inside policy, follow-ups inside windows `[web check]` | Unknown tool or policy | Pause | 04, 09 [79467cee9f17] |
| Identity labels | Read | Behaviour-based | Judgmental | Rewrite | 05 [e679699e4817] |
| Reading level and house style | Tool and scan | Below tenth grade; no em dashes; no inflated words | Any breach | Edit | ecomOS |
| Brand separation | Check sources of stories and data | Only this brand's | Another brand's | Remove | ecomOS |
| Hot take ownership | Ask the owner | Held and defensible | Manufactured | Drop the hot take | 10, 05 [07ab40bc6089] |

### 5.6 Series pipeline review

| what to check | how | good | bad | fix | source |
|---|---|---|---|---|---|
| Origin | Check the macro read | Built on a winner across 4 or more iterations | Built on 1 viral post or a guess | Pilot first | 09, 07 [3df74f892c3f] [6bff3121b5a8] |
| Scalability | Ask "can a team make 10 in a day without the founder?" | Yes | Cooking, travel, founder-only | Keep as a pillar, not a series | 06 [34c4c10786ba] |
| Packaging | Check name, signature, promise | All 3 present | Missing | Package | 09 [3df74f892c3f] |
| Challenge stakes | Ask "would we do this anyway?" | A real stretch, safe | Low stakes or dangerous | Raise safely or change | 04 [a0a28a40b29f] |
| Pilot data | 1-week impressions and sales | Moved | Flat | Do not commit resources | 06 [34c4c10786ba] |
| Run length | Count weeks | 8 or more committed | Swapped weekly | Hold | 06 [34c4c10786ba] |
| Portfolio | Count live formats | 2 or more | 1 | Add a second | 09 [3df74f892c3f] |
| Cross-platform version | Check lengths | Adapted per platform | Same cut everywhere | Adapt | 09 [3df74f892c3f] |

### 5.7 AI draft review

| what to check | how | good | bad | fix | source |
|---|---|---|---|---|---|
| Mode | Tag | Remix of approved language, or originated by a human | AI originated a position or story | Route to a human | 02 [ad4c55b5d306] |
| Position | Compare to the positions log | The brand's side stated | Category consensus | Supply the position | 02 [cbbb787360b8] |
| Facts | Compare to the claims list | All match | Any invented | Remove | 02, 09, ecomOS [4392aa839fe7] |
| Voice variable | Read for register, rhythm, stance | Matches | One off | Smallest edit; note in the voice guide | 02 [612587c6befe] |
| Echoes | Compare hooks to the research log | No lifted creator lines | A recognisable line | Rewrite | 09, ecomOS [1445bdd3ed8e] |
| Net-new | Ask "did this add thinking?" | Logged either way | Untracked | Log | 02 [1193451bea64] |
| Review questions | Check the 4 targeted questions were asked | Asked and applied by hand | Open prompt only | Rerun | 09 [8907bbacfafe] |

### 5.8 DM funnel check

| what to check | how | good | bad | fix | source |
|---|---|---|---|---|---|
| Keyword | Read post and caption | 1 distinct keyword, on screen and in caption | Missing or generic | Fix | 04, 07 [79467cee9f17] |
| Flow tested | 2 test accounts | Link delivered; email captured; lands in list | Broken anywhere | Fix before posting | 09 [00f161224b14] |
| Lead magnet fit | Comments and leads over weeks | Sustained | Quick drop-off | Revisit the resource | 07 [302840d96c34] |
| Frequency | Count posts with the flow | 1 to 2 a week | Every post | Reduce | 07 [302840d96c34] |
| New-follow DM | Read it | Thank-you only | Pitch or code | Replace | 04 [b539e41f421e] |
| Follow-up | Check clicked-not-bought | A time-boxed message exists | None | Build | 04 [13e3b50fabea] |
| Policy | Partner and window check `[web check]` | Inside policy | Unknown | Pause | 04, 09 |
| Capacity | Ask who answers and fulfils | Named | Nobody | Assign | 07 [4a4a14bf5c74] |
| Price routing | Check the offer | Low ticket in-app; high ticket to a call | High ticket closed in DM | Insert the booking step | 04 [3dd25615d38b] |

## 6. Thresholds and benchmarks

One table for the folder. Confidence: how many independent presenters agree (04 and 05 count as 1; 03 and 10 count as 1), and the basis. Unsourced numbers are marked "unsourced house default".

| value | condition | source | confidence |
|---|---|---|---|
| 2 to 3 pillars; each twice a week; 4 to 6 posts a week; hold 1 month; about 4 iterations per pillar before judging | new or restarted account starting plan | 03 | 1 presenter, coaching heuristic |
| 5 pieces a day volume floor | 02's own agency bar for "a fair shot" | 02 | 1 presenter, own agency; not universal |
| 2.5 posts a day then 4 posts a day (20,000 then 60,000 followers in 6 months each) | 04's own account, confounded by collaborations | 04 | 1 presenter, single account example |
| Once a day is a floor not a ceiling; peers at 3, 10 or "hundreds" a day | only when the data says the content works | 06 | 1 presenter, opinion |
| 95% of coached people are held back by under-posting | general claim | 07 | 1 presenter, unverified |
| Twice a week for a proven series | 09's B2B case | 09 | 1 case example |
| 3 to 5 scripts per sitting; 10 to 20 per batch day; a few hours | batching | 07 | 1 presenter, workflow estimate |
| Shoot once every 2 weeks | person-led content | 03 | 1 presenter, "most companies" claim |
| 10 to 20 one-line ideas in the bank | before batching | 07 | 1 presenter |
| Commit 3 months before changing the mix; 12 months before judging the channel; 6 months on one hero platform; 30 to 50 same-topic videos | judging the channel | 03, 04, 08 | 3 presenters, different numbers; all heuristics |
| About 8% follower growth per month | small brand expectation, not a target | 04 | 1 presenter, heuristic |
| 80% of planning effort on the hook | every short video | 04, 05 | 1 presenter (same coach twice) |
| Hook under 3 seconds; watch rate after 3 seconds as the base metric | hook review, retention read | 09, 04 | 2 presenters |
| Hook line 5 to 8 words (top performers averaged 7.7); up to about 12; rarely under 4 | on-screen or spoken hook | 05 | 1 presenter, self-collected 1,300 Reels, no method |
| Hook at or below 5th grade; copy 5th to 8th grade (4th acceptable); everything below 10th | readability | 05, 01, ecomOS | 2 presenters plus house rule |
| Negative framing outperforms positive on average | hook copy; keep testing both | 05 | 1 presenter, self-collected sample |
| Cover test: first 2 sentences, then 3 to 4 before the piece breathes | opener review | 01 | 1 presenter, rule of thumb |
| 80% to 90% of readers only read the headline | why openers matter | 01 | 1 presenter, estimate, not measured |
| Subheadline about 180 characters as the thesis | headline plus subheadline formats `[verify UI]` | 01 | 1 presenter, platform-dependent |
| Copywork 10 to 15 minutes; incubation at least about 90 minutes (up to a week) | writing process | 01 | 1 presenter, own practice |
| USA Today about 4th grade; NYT about 7th grade; Buffett letters 17 to 13 words per sentence, 10th to 4th grade, 1974 to 2013 | reading level calibration `[web check]` | 01 | 1 presenter, retold |
| Voice is about 20% of a piece; a 1% edit (2 to 3 citation phrases) fixed a voice complaint | voice repair | 02 | 1 presenter, anecdote |
| Timely content spikes about 24 hours; react to category news within 3 days | timely planning | 02, 06 | 2 presenters |
| 2-week essay reused for about 10 years vs 20-minute post | time allocation | 02 | 1 presenter, own example |
| About 80% of early effort on Reels; Stories after followers | new account format split | 04 | 1 presenter |
| No CTA until posts consistently reach about 5,000 views (about 2,000 in narrow niches) | new account CTA timing | 03 | 1 presenter, no data; conflicts C4 |
| Lead magnet on 1 to 2 Reels a week; a well-matched one keeps producing leads 6 to 8 months | organic-to-email funnel | 07 | 1 presenter, own account |
| 98% DM open, 37% click; 10 clicked, 3 bought, 7 to follow up | 04's own campaigns; examples only | 04 | 1 presenter, own data, not a benchmark |
| 5,000 to 6,000 signups per luxury report; "only a fraction" customers over about 1 year | lead magnet example | 03 | 1 client example |
| 70% to 80% of views from followers with flat reach signals stranger-blind content | stranger audit `[verify UI]` | 07 | 1 presenter, client pattern |
| Audit the last 20 videos for topic consistency | topic discipline check | 08 | 1 presenter |
| 2 to 3 minutes per platform; 12 to 15 minutes for 6 platforms, manual | posting | 03 | 1 presenter, own workflow |
| Scheduler reduces reach | organic posting | 03 | 1 presenter, internal test, no method; test per brand (C3) |
| About 30,000 YouTube Shorts views does little; a million "maybe" | cross-post expectation | 03 | 1 presenter, opinion |
| Reuse a winner at least 4 times; "post everything 3 times, repost after 60 days" | asset life | 06; 05 (uncarded caption) | 1 presenter each; the 05 line is thin |
| 10 or more variations per idea; publish in one window | test loop | 09 | 1 presenter |
| 60 seconds TikTok vs 3 minutes LinkedIn | length adaptation | 09 | 1 example, no reason given |
| 5 formats tested, 1 winner doubled engagement, over half of inbound leads in 2 months | series case | 09 | 1 case example |
| Lighting setup 1 to 2 hours; phone camera enough | production | 07 | 1 presenter |
| Viral vehicle "thousands of dollars", one-off | prop investment | 10 | 1 presenter, no ROI |
| 5% recalled facts vs 63% recalled story ("a Stanford study") | story vs specs `[web check]` | 06 | 1 presenter, uncited; never in copy |
| Stories 22x more memorable than facts | story hooks | 05 | repeated stat, not measured; never in copy |
| 45,000 likes on a founder-history carousel; about $1 million from a $250,000 relatability ad; "over a million dollars" from a counterfeit-angle ad; 15 million views on a competitor's timely mascot post | examples only | 06 | 1 presenter, self-reported |
| 1,400 to 185,000 followers "in a few months"; about $100,000 and $38,000 from 2 Reels; $400 in a day from an 8-minute Reel | examples only | 07 | 1 presenter, self-reported |
| 10,000-follower employee grew the brand account past 500,000 | hiring example | 06 | 1 presenter |
| "10 times" or "1,500%" more followers than competitors | tour-guide case; the transcript contradicts itself | 10 | 1 presenter, unreliable figure |
| About $52 AdSense after 12 months; $500 to $1,000 brand deals | media-layer income example | 08 | 1 presenter, own case |
| 1 round of variations is a signal; 3 rounds is a pattern | test loop read | none | unsourced house default |
| Post-performance read at 4 weeks; no strategy change under 4 iterations per pillar | read cadence | 03, 07 for the principle; the 4-week cadence is a house choice | 2 presenters for the principle; cadence unsourced |
| Good retention, share rate, engagement rate or view-to-follow rate | any | none | no source gives one; set from the brand's first 3 months `[needs brand data]` |
| Low-ticket vs high-ticket price cutoff | in-app vs call | none | 04 gives no number `[needs brand data]` |
| Maximum posts a day before fatigue | cadence | none | no source gives one `[needs brand data: unfollows and follower share as cadence rises]` |

## 7. Where sources disagree

Each conflict: what each side says, when each is right, what the agent should do. Codes are referenced from section 3.

**C1. Post volume: more is better vs fatigue and a fixed weekly plan.**
- More is better: 04 ("the more you post, the more you grow"; interest-based distribution stops punishing volume; his own 2.5 to 4 posts a day), 02 (5 pieces a day floor before judging anything), 07 (under-posting holds back 95% of his clients), 06 (once a day is not a rule; post more when it works).
- Fixed and modest: 03 (2 to 3 pillars twice a week, 4 to 6 posts a week, daily not required, hold a month), 09 (a proven series twice a week), 08 (30 to 50 same-topic videos, consistency over volume). 04's own mini playbook notes he gives no upper bound or fatigue signal.
- When each is right: high volume suits accounts with batching, a creator bench and a deep idea bank (02's condition: input before infrastructure). The modest plan suits a founder-led brand with 1 shoot every 2 weeks. Neither side measured fatigue; 04's 3x result is 1 confounded account.
- Agent: start at 03's plan or the highest floor the team can hold for 4 weeks; raise the floor only after a monthly read shows the content works and unfollows and follower-share of views did not worsen. Record the cadence and the read in the experiment log. `[needs brand data: unfollows per post, follower share as cadence rises]`

**C2. Entertainment vs education.**
- Entertainment first: 04 (SHARE's E; an unofficial Meta contact said brands must make entertainment the primary driver), 10 (format shakeup, speed, viral vehicles, attention hijack).
- Education with a lens: 03 (expert-driven pillars: ratings, breakdowns, scenarios; "give away the playbook"), 10 (versus format and embarrassed questions are education with a verdict), 07 (a conversational tip, "add oats and chia seeds"), 02 (commodity advice is the most useful thing for beginners), 06 (education inside an open loop).
- When each is right: the sides mostly describe the same content: useful expertise delivered in an entertaining wrapper. 04's Meta claim is single-source and unofficial. Pure entertainment with no story or use "does not make sales" (06).
- Agent: every post carries a real, useful point (education) and an entertaining delivery (a format, a scenario, a story, speed, a prop). Reject posts that are only one. Log which pillar and which wrapper each post used so the monthly read can show the brand's own balance. `[web check: any public Meta statement on content type weighting]`

**C3. Scheduler vs no scheduler.**
- No scheduler: 03 (native and third-party schedulers hurt reach, from an internal test over "hundreds of videos" with no method shown; manual posting takes 12 to 15 minutes for 6 platforms).
- Scheduler: no source argues for it, but 03's own cards say to test manual vs scheduled on the brand's account, and 07 and 09's batching workflows assume posts can be queued. Common agency practice schedules.
- When each is right: unknown. The claim is unverified and platform behaviour changes.
- Agent: post manually by default for the first 4 weeks (cheap), then run the alternating-week test in P11 and adopt what the brand's own non-follower reach shows. Never claim a scheduler penalty to a client as fact.

**C4. CTA from day 1 vs after about 5,000 views.**
- Wait: 03 (zero CTAs, including "join my list", until posts consistently reach about 5,000 views, 2,000 in narrow niches; early CTAs are "shooting yourself in the foot").
- Always a next step: 09 (every piece needs one clear next step; reach without a monetisation layer is a vanity metric), 04 (sell low-ticket in-app continuously; comment keywords raise engagement), 07 (lead magnet on 1 to 2 Reels a week from the start of his system).
- When each is right: 03's rule protects a new account's growth signal, on his coaching experience only. 09 and 04 note the next step can be a keyword comment, which keeps the viewer on the post. A brand that needs leads this quarter cannot wait for a threshold it may never hit.
- Agent: new account: month 1 with no CTA (03). From month 2: keyword lead-magnet CTAs on 1 to 2 posts a week (07) even below the threshold, no hard sells, and watch non-follower reach for 4 weeks. Hard sells only after the threshold or in Stories once followers exist. Log the choice and the reach effect so the brand builds its own answer.

**C5. Sponsors vs none.**
- No sponsors: 07 (stopped taking them; "usually a pain"; sell your own offer via the email list), 08 (brand deals and AdSense are the layer with the least value; his first AdSense was about $52).
- Sponsors: no source in this folder argues for them; the conflict is with common creator practice and with a brand's own creator partners who may rely on deals.
- When each is right: 07 and 08 speak as creators with a product or mentorship to sell. An ecommerce brand is the product layer already, so its organic account has no sponsor question. A founder's personal account might.
- Agent: for the brand account, content routes to the brand's products and list; sponsorships are out of scope. For a founder's personal account, treat sponsorships as a separate revenue decision that must not dilute topic discipline (R2) or brand voice, and never as the content model.

**C6. Open-loop hooks vs clear-benefit hooks (and conversational vs formula).**
- Open loop and withhold: 06 (open a loop in sentence 1, never close it in sentence 2, resolve later), 05 (curiosity gap in the Goldilocks zone), 01 (cover test, thesis first but with a gap).
- Clear benefit fast: 07 (a conversational opener must still signal a concrete payoff; formula bait is discounted), 04 (lead with the clearest version, not the cleverest; "drunk grandma"), 09 (the hook must make the target market understand what this is about in under 3 seconds), and direct-response practice in 11-ADC.
- When each is right: for organic reach content, a gap that names the domain and the stakes keeps strangers watching. For bottom-funnel or product-aware posts, and for Stories to followers, the benefit stated plainly wins. Both sides agree on payoff honesty and on naming what the video is about.
- Agent: default to "name the domain and the stakes, withhold the mechanism" for top-of-funnel short video; state the benefit plainly for mid and bottom funnel and for Stories. Write both a formula and a conversational version into the hooks bank and let the monthly hook-type read decide for this brand. Never ship a gap with no payoff.

**C7. Courting controversy.**
- Court it: 06 (do not fear negative comments; manufacture some controversy; exaggerate language; a counterfeit moral-outrage ad made "over a million dollars"), 10 (polarising hot takes as a taste barometer; "everyone wants to be everyone's friend" is the failure mode), 05 (contrarian hooks fuel watch time).
- Limit it: 05 and 10 themselves (only claims the creator holds and will defend), 09 (raw or edgy content does not fit luxury or regulated brands), 01 (crisis response should own the mistake, not spin), common brand-safety practice, and ecomOS (no invented claims; brand voice wins).
- When each is right: a true, held, defensible opinion about the category can build a distinct voice. Accusations against named competitors, safety or health claims, and manufactured outrage carry legal and platform risk none of the sources assessed.
- Agent: allow contrarian and hot-take content only when the brand record supports the position and the owner will defend it in comments; route any competitor accusation, safety claim or health claim through P21 and legal review; never exaggerate beyond the literal truth; for luxury or regulated brands, keep hot takes to category opinions on a lower-stakes account or skip them.

**C8. "I" copy vs "you" copy.**
- "I": 02 (prescriptive "you should" reads as commodity and mildly patronising; first-person experience is personality content), 05 (story hooks open with "I"), 06 ("My name is Davey, this is my story").
- "You": 05 (direct-address hooks "if you're a mom of 3 under 3"; identity hooks), 10 (scenario hooks address the viewer), 04 (relatable "me when" and POV formats), and standard benefit copy ("you'll get X"), which 02's own mini playbook says 02 is not attacking.
- When each is right: "I" for stories, positions and personality content on a named person's account. "You" for direct address, benefits, scenarios and instructions on any account. Prescriptive "you should" lines are the only ones 02 targets.
- Agent: rewrite prescriptive "you should" lines as a specific first-person experience or a stated position; keep benefit "you", direct-address hooks and scenario framing; route first-person biography to the named person's account and agreed positions to the brand account; the brand record's voice decides the final balance.

**C9. Informal tone vs regulated or luxury voice.**
- Informal: 01 ("informal is not the opposite of professional"; write like you talk; 4th to 8th grade), 06 (exaggerated, charged language), 10 (hot takes), 09 (raw behind-the-scenes over polish), 07 (friend-like openers).
- Formal where required: 01's own caveat (regulated categories and luxury positioning may need a formal register), 09's own caveat (raw content can conflict with luxury or compliance; test on a lower-stakes account), ecomOS (brand voice from the brand record wins).
- When each is right: plain, spoken-register writing at a low reading grade suits almost every brand. Slang, exaggeration, edginess and raw production suit some brands and not luxury, health, finance or legal.
- Agent: keep the plain-language and reading-grade rules for every brand; take register, edge and production polish from the brand record; for Gehna (jewellery, considered purchase) default to plain but polished, and test raw or informal formats on a secondary account first if at all.

**C10. Reusing stories across accounts.**
- Reuse: 06 (post variations of one winner to the brand account and a separate fan or creator account, slightly different, stay with the format on both), 02 (reuse an approved line hundreds of times over years), 09 (satellite accounts per format).
- Caution: 06's mini playbook (general platform guidance discourages duplicate or near-duplicate content across accounts, unaddressed by 06), 08 (islands: each platform and account is its own audience; do not route between them), 02 (personality content belongs to a named human, not a brand handle).
- When each is right: reusing a story across formats and platforms is safe and compounds. Near-duplicate posts across several brand-controlled accounts on one platform is the risky case, and no source verified the platform's treatment.
- Agent: reuse freely across formats and platforms with adapted wrappers; across accounts on the same platform, only with a different wrapper, a different angle and a different named voice (founder account vs brand account), never as a near-duplicate; check current platform policy on duplicate content before a second brand-controlled account exists. `[web check: current platform rules on duplicate content across accounts]`

**C11. One hero platform vs cross-post everywhere.**
- One platform: 08 (one hero platform plus email for 6 months; islands not ecosystems; outbound links throttled; users resent being moved).
- Cross-post: 03 (TikTok and Instagram as the base, cross-post to LinkedIn, X, Shorts and Spotlight because it costs 2 to 3 minutes each), 06 (life-extend across accounts and platforms), 09 (scale the winner across platforms).
- When each is right: 08 aims at judgment and focus for a small team; 03 aims at cheap extra reach. They agree on never routing an audience from one social platform to another.
- Agent: judge the channel on 1 hero platform (P22); cross-post manually to secondary platforms with zero expectation and no cross-platform call-outs; all links go to owned destinations by keyword or bio.

**C12. Negative framing vs benefit-forward framing.**
- Negative: 05 (threat words outperform on average in his sample).
- Benefit-forward: 05 itself (keep testing positive hooks), 11-ADC direct-response practice, and brand voice records that exclude threat language.
- Agent: write both versions, choose inside the voice, log the framing, read results monthly; never merge into one universal rule.

**C13. Reels-first vs carousels.**
- Reels at about 80% of early effort: 04.
- Carousels can carry any pillar without a camera and can win (45,000 likes on a founder carousel): 03, 06.
- Agent: new video-capable accounts follow 04's split; faceless brands run carousels with higher design investment (R90); every account keeps some carousels for stories and breakdowns.

**C14. Founder story as the asset vs founder story as the scaling limit.**
- Asset: 02 (personality beats credibility; the unmade data set; a named human's account), 03 (founder front and centre), 01 (founder letter, intention and obstacle), 06 (the 30-minute founder carousel; "My name is Davey").
- Limit: 06 (a single founder's personal story on the same page fatigues; formats gated by the founder's body do not scale; build a bench).
- Agent: use the founder's approved stories as a library that feeds many formats and voices (R135), not as the only format; from month 3 pilot 1 team-repeatable format (R85) so volume does not depend on 1 person.

**C15. Satellite accounts vs one feed.**
- Split: 09 (satellite accounts per proven format), 08 (separate accounts for unrelated categories).
- One feed until proven: 09 itself (never launch several at once; prove on the main account), 08 (30 to 50 videos on one topic first).
- Agent: one account until a format proves across a monthly read; then a satellite only if the team can hold both floors; no limit is given, so start with at most 1 satellite.

**C16. Stay with a winning format vs rotate formats.**
- Stay: 06 (once a format wins, run it for a long period; do not swap weekly).
- Rotate: 09 (several formats in rotation to spread risk and avoid fatigue).
- Agent: run a winner for at least 8 weeks and keep at least 1 other format live; retire a winner only after the phase metric falls for 4 episodes.

**C17. Speed and short formats vs a full ending.**
- Short and fast: 10 (speedruns, 30-second makeup, 15-second skill demos), 05's caption montage ("I post 7 to 15 second Reels", attribution uncertain).
- A full arc: 06 (a strong beginning with no ending is a missed chance; add journey and length for memory).
- Agent: speed formats keep the compression as the point; story formats keep an ending. Tag the format so the read compares like with like.

**C18. Raw and authentic vs lit and intentional.**
- Raw: 09 (raw behind-the-scenes beat studio content for a coffee roaster), 04 (short idea-to-execution, no heavy editing).
- Lit: 07 (raw is not an excuse for bad lighting; a stranger swipes on a bad first frame), 03 (a consistent set compounds credibility).
- Agent: raw in subject, edit and pace; deliberate in lighting and first frame. These are not opposed.

**C19. Next-day recall vs measurable metrics.**
- Recall: 06 (would I remember this tomorrow; "brain rot does not make sales").
- Metrics: 04, 07, 09 (retention, shares, comments, completion, saves, CTR, cost per lead), ecomOS (arithmetic in code).
- Agent: metrics decide; the recall test is a tiebreaker between concepts and a check that a high-view post has a story layer.

**C20. Personality vs credibility.**
- Personality wins: 02 (less-credentialed creators with strong narrative out-reach Ray Dalio).
- Credibility matters: 03 (expert stance, "look the part"), 05 (borrowed credibility hooks), 07 (a verifiable proof slot), and ecommerce trust practice (reviews, guarantees).
- Agent: proof in the positioning and in every claim; personality in the stories and the delivery. For considered or regulated purchases, credibility leads.

**C21. Give away the playbook vs hold back for the offer.**
- Give it away: 03, 02.
- Hold back: no source; the tension is with 03's own CTA-timing rule, which delays the offer but not the content.
- Agent: give the full breakdown; delay the offer, not the value.

**C22. Timely reactions vs timeless library.**
- Timely: 06 (react within 3 days; a competitor's timely mascot post got 15 million views), 10 (attention hijacks).
- Timeless: 02 (timely content is worth almost nothing after 24 hours; the library compounds), 03 (content keeps earning for months).
- Agent: default to timeless; cap timely slots at 1 to 2 a week and use them only when the team can ship inside 3 days and the moment fits the brand's topic.

## 8. Common mistakes

Merged from all sources, deduplicated, with the fix.

1. Judging the channel after days or weeks, or comparing follower counts to established accounts. Fix: uploads as the KPI, 3-month mix hold, 12-month channel window, competitors for ideas only (R17, R18, R19). [13325d6dff66] [38b7805726e7]
2. Under-posting because every post must be perfect. Fix: a sustainable floor, batching, "publish to find the voice" (R14, R16, R63). [868f6861da16] [910b7d45cd6e]
3. Raising volume with no source of original ideas. Fix: the idea bank, the positions log and the unmade data set before the posting machine (R15, R22, R60). [ed26cf9e8b40]
4. Content built for people who already know the brand: inside jokes, product nicknames, references to past posts. Fix: stranger test on every opener; follower-share audit (R5, R148). [e3a9ae26373a] [37ea3485764f]
5. Mixing unrelated topics on one account, or launching several accounts at once. Fix: one topic, one avatar; satellites only after a format proves (R2, R114). [d84a8df8c294] [5bb14404abb5]
6. A generic positioning any competitor could paste their name into. Fix: the swap test on the DNA statement (R1). [bab1ea1d6132]
7. Treating a well-written text hook as enough when the first frame is generic (typing, a desk, a car). Fix: visual first, half-second screenshot, subject-matched footage (R26, R35). [cee2da009c53]
8. Dead time at the start: a hesitation, a setup shot, clutter, low contrast. Fix: cut to the hook (R35). [cae016218009]
9. Hooks with jargon, acronyms, 13 or more words, or a curiosity gap that is too wide or too narrow. Fix: 5 to 8 words, 5th grade, name domain and stakes, withhold mechanism (R27, R28, R30). [c98d12e4ca71] [97e147c3e5a1]
10. Bait: a teased moment, count or result that never arrives. Fix: payoff check before publishing (R30, R34, R40). [0980397e62b4] [d686739bfd6c]
11. Loud formula hooks a viewer reads as an ad. Fix: read aloud; conversational wording with a concrete payoff (R33). [3a5f43d052ea]
12. Closing an open loop in the very next sentence. Fix: resolve after the body (R30). [c1f05a1e6af3]
13. Extreme numbers, uncited statistics, invented studies. Fix: realistic numbers from the brand record only; no 22x, no 5% vs 63% (R36, R37, R163). [01267ffe7cb0]
14. Contrarian or hot-take claims the brand does not hold, or accusations against competitors. Fix: defensibility check and legal review (R38, R167). [1ab0e11dcafa] [07ab40bc6089]
15. Judgmental identity labels. Fix: describe behaviour (R39). [e679699e4817]
16. Relying on a sound effect as the hook. Fix: text and visual carry it (R41). [11f62e1913d1]
17. Leading with specs, features or a corporate claim instead of the story. Fix: story first, specs in the body; founder question set (R65, R66). [da155e10b870]
18. Burying the lead under background, or writing school-style long sentences with fancy words. Fix: punch first, readability pass, comma to period (R47, R48, R50). [26bc815a7b84] [d8fbcddae70a]
19. Drafting and editing in one sitting, or treating the first draft as final. Fix: dump draft, incubate, edit (R46). [8c85d056f475]
20. Stacking synonyms ("fit, lean, lose weight, healthy"). Fix: redundancy pass (R52). [9fce1289b063]
21. Writing about topics you would never mention to a friend. Fix: voice-memo test (R53). [16e4989b065a]
22. Letting AI originate positions or stories, or shipping an AI draft without a fact check. Fix: remix only from approved language; targeted review; claims check (R56, R61, R62). [ad4c55b5d306] [4392aa839fe7]
23. Discarding an AI or ghostwritten draft because one voice variable is off. Fix: find the variable, smallest edit (R59). [612587c6befe]
24. Posting personal biography from a faceless brand handle. Fix: personality on a named human's account (R8). [49c888bb326e]
25. A date or "just launched" line in a piece meant to compound. Fix: label timely or timeless, strip the date (R11). [3014faaee9da]
26. Missing a timely moment by being slow, or filling the calendar with reactions. Fix: 1 to 2 timely slots, 3-day ship rule (R11, C22). [d899a52a55f2] [9143824217f6]
27. Copying a competitor's content, story or clip instead of its structure. Fix: teardown grid, structure only, rights check (R69, R140, R164). [646870522f21]
28. Rejecting a new angle as "cringe" or a category as "boring". Fix: run the reframes before concluding (R9, R71). [86b7c9130744] [6cb62b6f330a]
29. A versus video with no verdict, or education that is "very straightforward and dull". Fix: a professional verdict; embarrassed questions; a wrapper (R73, R74, C2). [a38c90da39f7] [2cc9d0eca5c6]
30. Chasing raw view counts or broad virality that pulls unrelated audiences. Fix: on-target reach, next-day recall, broad-hit aftermath check (R6, R70, R153). [d6fdd4b41759] [d37ea33564f1]
31. One-off experiments never refined into a series. Fix: package winners as named series and run them 8 weeks (R82, R83). [3df74f892c3f]
32. A "challenge" you would do anyway, or a dangerous stunt. Fix: genuine stretch, safe (R84, R169). [a0a28a40b29f]
33. The lowest-effort setup that looks like everyone else's. Fix: commit to the bit, a signature prop or set, deliberate lighting (R87, R88, R89). [4289340e4d3b] [7af226f4da5b] [26bf14383383]
34. Confusing "raw" with bad lighting and clutter. Fix: 1 key light, practical background lights, a lit first frame (R89). [26bf14383383]
35. Building the machine around the founder's body or around cooking and travel formats. Fix: scalable formats, creator bench, footage archive (R85, R94). [34c4c10786ba] [3b8dc00bf68a]
36. Hiring a corporate social manager who has never had a video perform; waiting to start the archive until it is urgent. Fix: hire for proven views; upload continuously (R94). [3b8dc00bf68a]
37. Blaming the product for a plateau caused by founder capacity. Fix: P19. [8292e101004a]
38. Early Story production before followers exist; ignoring Stories once they do. Fix: R81, R117. [fa1ae83e8a27]
39. "Link in bio" as the CTA; pitching in the new-follow DM; no follow-up to clicked-not-bought; a broken flow during a spike. Fix: keyword DM, thank-you only, follow-up, end-to-end test (R119, R123, R124, R125). [79467cee9f17] [b539e41f421e] [13e3b50fabea] [00f161224b14]
40. CTAs and hard sells on a new account before any traction; or no next step at all after traction. Fix: C4 path (R118, R158). [bf0b2be7f3cf] [5f22157f3977]
41. Unanswered or generic replies to comments and DMs. Fix: personal, fast, proactive (R126). [eaadc77a360f]
42. Closing high-ticket sales in DMs. Fix: route to a call (R127). [3dd25615d38b]
43. Scaling reach with no intake or fulfilment capacity. Fix: R24. [4a4a14bf5c74]
44. Routing followers between social platforms; raw outbound URLs in posts. Fix: owned destinations only (R129). [03e0df5b81d9]
45. Being everywhere with no team; or expecting business value from YouTube Shorts views. Fix: hero platform, zero-expectation cross-posts (R110, R111). [e46ef6c2491a] [19bea8d6aaa6]
46. Running a TikTok Business account with no Shop; registering the account in the wrong country. Fix: R112, R113 `[verify UI]`. [b22a54d48616]
47. Chasing micro tactics (posting time, trending audio, close friends) before the library exists. Fix: R21. [3335c7ab8443] [26f23bfd7ece]
48. Judging a single flop as a verdict, or skipping the flop review because it hurts. Fix: 3 lists plus a flop list (R144, R145). [6bff3121b5a8]
49. Reviewing the wrong metric for the phase, or raw views instead of completion, saves, comments, CTR and cost per lead. Fix: R146, R147. [3380206cba51] [c5eaa02ce9d1]
50. Relying on ad revenue or brand deals as the income model. Fix: content routes to the owned offer and list (R156, R157). [0e331c158903] [4a4a14bf5c74]
51. Making a winner once and never reusing it, or reusing near-duplicates across brand accounts. Fix: 4 wrappers; C10 rule (R132, R133). [4f527d2d3eb2]
52. Buying or commissioning a content library with no machinery to distribute it. Fix: R137. [4a3f81e0a69c]
53. Pasting swiped lines into copy. Fix: structure only (R139). [6ff9c1f9fc32]
54. Exaggerating claims for reach. Fix: literal truth, brand voice (R44, R163). [d52d9eff6cd1]
55. Undisclosed AI voices or spokespeople. Fix: R170. [4f527d2d3eb2]
56. Zeros where data is missing; totals mixed with breakdowns; arithmetic done by hand. Fix: ecomOS metric rules (R150).

## 9. Deliverables

What the agent produces for each task in this domain, and the format. Every deliverable names its brand, its sources by rule number, and any `[needs brand data]` or `[web check]` still open.

### 9.1 Monthly calendar
Format: a table, 4 weeks, 1 row per post. Columns: date, platform (hero or cross-post), pillar, format (Reel, carousel, photo, Story), series name, SKU or collection featured, hook type, framing (negative or positive), funnel stage, timely or timeless, CTA (none, keyword, Story link, hard), keyword, who is on camera, filming batch date, status. Header: floor, phase label (growth or selling), pillars chosen, open timely slots, inbox owner. The SKU or collection column ties the calendar to the catalogue, not only to pillar and format. Built by P3, reviewed by checklist 5.3.

### 9.2 Hooks bank
Format: a table. Columns: hook line, word count, reading grade, hook type (1 of 15), framing, visual event, first-frame plan, domain and stakes named (yes or no), payoff location, claim check (brand record reference), rights check if borrowed, post id once published, phase metric result. Kept as a permanent file; the monthly read (P15 step 8) writes results back. Built by P5, reviewed by checklist 5.1.

### 9.3 Scripts
Format: per video. Header: reaction, action, one line to remember; intention and obstacle for stories; timely or timeless; AI mode tag; stage. Body: hook (visual event, on-screen text, spoken line), open loop or gap and where it resolves, body in short spoken sentences, ending, spoken topic and audience line, CTA line if any. Footer: reading grade, claims referenced, voice variables checked, compliance items (P21) ticked. Built by P6 and P7, reviewed by checklists 5.2, 5.5, 5.7.

### 9.4 Captions
Format: per post. First line extends the hook; topic and audience stated; keyword if a lead magnet is attached; no outbound social links; reading grade; timely or timeless; platform variants where length differs. Reviewed by checklist 5.2.

### 9.5 Repurposing plan
Format: per winning asset. Confirmation of the win (impressions and sales moved, from P15 step 10); 4 or more planned versions (new hook, carousel, voiceover or new footage, platform-length cuts) with dates spaced across weeks; account for each version and the C10 decision recorded; disclosure note for any synthetic voice; retirement date for any timely version; approved-story reference in the library. Built by P17.

### 9.6 Series pipeline
Format: a table of candidate and live series. Columns: origin (which macro read), core idea, scalability test result, pilot week result (impressions and sales), name, visual signature, promise, cadence, start date, committed run (8 weeks minimum), episodes shipped, phase metric vs baseline for the last 4 episodes, status (pilot, live, paused, retired), second live format named. Built by P10, reviewed by checklist 5.6.

### 9.7 Comment-to-DM funnel spec
Format: per campaign. Tool and its policy status `[web check]`, keyword, lead magnet and its destination page (07-LPG), email or CRM destination (14-EML), flow steps, test log (2 accounts, date), posts it is attached to (1 to 2 a week), new-follow DM text, follow-up message for clicked-not-bought, capacity owner, backend metrics to export. Built by P12, reviewed by checklist 5.8.

### 9.8 Monthly performance read
Format: a short report. Uploads vs floor; retention and 3-second watch rate trend; the phase metric; the 3 top lists and the flop list; pillar read after 4 iterations; follower share of views; last-20 topic audit; hook type and framing read; leads per post and keyword; the business tie computed in code with unavailable values shown as unavailable, including sales by SKU or collection, not only total sales; the do-not-do list; the expand list; the next month's floor and mix decision; any scheduler or CTA test result written to the experiment log. Built by P15, reviewed by checklist 5.4.

### 9.9 Account foundations document
Format: the Creator DNA statement, avatar and pain points, price ladder and catalogue shape, stance (expert or student), pillars and formats, positions log, voice variables, hero platform and cross-post list, account setup per platform (type, country, access), timely vs timeless policy, compliance flags. The price ladder and catalogue shape drive the ranking in section 3.0. Built by P1 and P22.

### 9.10 Story library entries
Format: per story. Title, the founder question it answers, intention, obstacle, emotional trigger and technique, the approved telling (text), formats it has been used in, accounts it may appear on, permission status, claims referenced. Built by P8.

### 9.11 Teardown grids
Format: the 3-by-6 grid (beginning, middle, end against location and visuals, pacing, audio and script trigger words, on-screen text, lighting, viewer emotion) plus "other notes", marked "structure only", with the rebuilt version's plan. Built by P9.

## 10. What needs live data or a web check

**Needs brand data**
- The proof point for the positioning statement (R1, P1).
- Which credentials are real, for the expert vs student stance (R4).
- The category's recurring commodity debates and the brand's side (R57, P1).
- Founder timeline, failures, sourcing history and formative stories (R60, R66, R68, P8).
- Real customer stories and permissions (R66, P8).
- Team capacity: on-camera people, editor hours, batch days; the sustainable floor (R14, P3).
- Audience fatigue signals as cadence rises: unfollows per post, follower share of views (R14, R100, C1).
- The 3 broadest customer search phrases (P2).
- Target country vs where the account and phone number are registered (R113).
- Which platform holds the most customers (R110, P22).
- Price ladder: low ticket vs considered (R127, P13).
- Which free resource fits the customer as a lead magnet (R122, P12).
- Post-level data: views, follower share, retention, 3-second watch rate, shares, saves, comments, Story views (R146, R148, P15).
- DM automation backend: opens, clicks, emails, purchases per keyword (R124, R151, P12).
- Sales by day, impressions by post, discount-code redemptions (R150, P15).
- Aftermath of any broad hit (R153).
- Footage archive status, editor budget (R94, P19).
- The brand's own baselines for retention, shares and engagement after 3 months (R154, section 6).
- Median reply time in comments and DMs (P13).
- Results of the scheduler test and the CTA-timing test, written to the experiment log (C3, C4).
- Which of the 10 reframes fits the brand's assets, supply-chain visibility and risk tolerance (R3, R76; from 10's mini playbook).
- How the store currently attributes content to sales, if at all (02's gap).

**Web check**
- Current Instagram and TikTok creator documentation on distribution: stranger-first sampling, topic learning from transcript and captions (R97, R98).
- Current account types and any stated difference between Creator and Business accounts on TikTok and Instagram (R102, R112).
- Current treatment of outbound links, link stickers and cross-platform routing per platform (R103).
- Whether an open DM thread or comment volume affects the next post's reach (R104).
- Whether Instagram content still surfaces in Google search (R106).
- Any public Meta statement on entertainment vs education weighting (R107, C2).
- Current Meta messaging partner list, DM automation policy, messaging windows, and ManyChat's status, features and pricing (R119, R171, P12).
- Current platform and regulatory disclosure rules for AI voices, AI spokespeople and synthetic footage (R170).
- Platform policy on comparative and competitor claims; legal exposure of implying a competitor sells counterfeits (R167).
- Platform rules on duplicate or near-duplicate content across accounts (C10).
- The Stanford study behind 06's 5% vs 63% recall claim (R65).
- Readability tool availability and grading (Hemingway or equivalent) (R28, R48).
- Current low-cost softbox options (P20).
- Current stitch or duet feature names and mechanics for hook swaps (R34).
- Instagram auto-translate and "suggested profile" features named by 05 (section 11).
- Whether the 6-platform list (Facebook, YouTube, LinkedIn, TikTok, Instagram, X) still matches usage (P22).
- Identity and current claims of the unnamed presenters in 07, 08 and 09; the host's "$30 million" claim about 02; whether Cut 30 (03, 10), Ship 30 for 30 (02), Wavy World and Sandcastles (08) still exist as described.
- The Micro One and Spirit Airlines data purchase and the OpenAI and TBPN acquisition cited by 02 (R137, R160).
- Recording dates of 01, 03, 04 and 05.

## 11. Freshness and stale-risk notes

| area | what can go stale | rules affected | re-verify |
|---|---|---|---|
| Algorithm behaviour claims | Every mechanism in 3.8 is a presenter's explanation; 07 says the rules "changed like crazy" in 12 months; 03 bounds the expert-content advantage to about 9 months from late 2025 | R5, R6, R14, R17, R23, R97 to R109, C1, C2, C3 | every quarter, and whenever a platform announces a distribution change; keep the brand's own follower-share and reach data as the real test |
| Platform features | Reels vs Stories reach, stitch and duet names, auto-translate, "suggested profile", Story link stickers, Creator vs Business account differences, TikTok Shop tie-in, Instagram in Google search, Snapchat Spotlight and YouTube Shorts value | R34, R81, R102, R103, R106, R111, R112, R117 | every quarter `[verify UI]` |
| DM automation and messaging policy | Approved partner list, comment-to-DM mechanics, new-follow DM trigger (04 says it arrived late 2025 or 2026), messaging windows, ManyChat pricing and trial terms (09's 30-day offer is an affiliate promotion) | R119 to R125, R171, P12 | before every new campaign and at least every quarter `[web check]` |
| AI tools | 09 names ChatGPT, Gemini, Grok and Claude; 02 names none; 05's Notion agent and 08's Sandcastles are sponsor or own-product plugs; model behaviour and pricing change; do not name GPT on client pages | R56, R61, P7 | every quarter; the workflow (repeat, remix, review) does not go stale, the tool names do |
| Automation and scheduling tools | 03's scheduler penalty is 1 internal test; native schedulers change | R101, R116, P11 | test per brand; recheck after any platform scheduler change |
| Synthetic media rules | Disclosure obligations for AI voices and spokespeople are moving | R170 | before any AI voiceover reuse `[web check]` |
| Readability tooling | Hemingway or equivalent grading | R28, R48 | yearly `[verify UI]` |
| Presenter products and claims | Cut 30, Ship 30 for 30, TypeShare, Insta Club, Wavy World, Sandcastles, copythat.com, the Maven course; case numbers were current at recording only | section 12 | before citing any to a client `[web check]` |
| Named examples | Viral examples (Wants and Needs, Citizen the Artist, Americana Pipe Dream, the Drumstick mascot post) age out and may be deleted | section 12 | do not cite to clients without checking they still exist |
| Cross-source numbers | 04's 8% a month, 03's 5,000-view threshold, 02's 5-a-day floor, 08's 30 to 50 videos and 6 months, 07's 70% to 80% follower share: all heuristics from 2025 to 2026 | section 6 | replace with the brand's own baselines after 3 months of data |
| Hook-length and reading-level findings | 05's 1,300-Reel sample is one creator's undated collection | R27, R28 | keep as a starting point; the hooks bank read replaces it |
| Expert-content window | 03 says expert-led content is "the cheat code right now" for about 9 months from the talk | R4 | re-read the brand's own pillar results each quarter |

**24 Sep 2026:** ecommerce specificity pass applied from ECOM_REVIEW.md; priority block added (3.0), 15 rules reworded, 8 levers added (R175 to R182), about 2,300 words moved to Appendix A.

## 12. Source index

Each mini playbook: number, title, type, credibility and bias, what it contributed most. Ratings: credibility 1 (opinion only) to 5 (measured, independent); bias 1 (no commercial interest) to 5 (selling the thing the advice justifies).

**Full source credibility write-ups (01 to 10) moved to Appendix A, section A.2.** Each entry there names the presenter, what they sell, the credibility and bias ratings on the scale above, and what each source contributed most. This is background about the presenters, not about stores.

**Independence note.** 10 files, 8 independent presenters: 04 and 05 are one coach; 03 and 10 are one program. No source is independent of a commercial interest except partly 06.

**Neighbour folders and what lives there.**
- 10-MCR-paid-social-creative: paid concepts, statics, video scripts for ads, UGC and founder ad briefs, creative testing. Organic winners go there to be run as paid tests (R150, 06's "run it as a Facebook ad").
- 24-DEP-ad-deployment: account structure, budgets, bidding, boosting. Meta is read only from this playbook.
- 11-ADC-ad-copy-deployment: primary text, headlines, descriptions; benefit-forward paid copy that C6 and C12 contrast with organic hooks.
- 07-LPG-landing-pages: lead-magnet pages, founder-letter pages (R78), hard and soft CTA destinations (R128).
- 14-EML-email-lifecycle: the email sequence after a DM capture (R125), plain-text founder emails (R78), welcome and post-purchase flows.
- 06-MEA-measurement: attribution and measurement infrastructure behind the business read (R150).
- 09-CRO-testing: test design and statistics; this folder's test loop (P16) has no sourced sample-size rule.
- 01-PRD-product-research and 03-OFF-offers: what the product is and what the offer is; this folder assumes both exist.
- 17-CXP-post-purchase: customer stories and reviews that feed the story library (R66).


## Appendix A. General background

Moved here by the ecommerce specificity pass (ECOM_REVIEW.md, applied 24 Sep 2026). This material is presenter opinion, unverified algorithm mechanism claims, source biographies and non-store examples. It is kept for reference and traceability, not for day-to-day decisions; the main sections above are.

### A.1 Algorithm behaviour claims (moved from section 3.8)

No source in this folder cites platform documentation. Every mechanism below is a presenter's explanation, stated as fact in the talk. The agent treats each as a hypothesis, records what it would look like in the brand's own data, and re-verifies on the cadence in section 11. `[web check: current Instagram and TikTok creator documentation on distribution]`

**R97. Claim: new posts are shown to a small sample of strangers first; their reaction, not follower count, decides further reach.** 04 ("TikTokification", interest-based distribution), 07 (Instagram tests Reels and carousels with non-followers), 08 ("media matching" replaced the social graph since 2020), 09 ("content graph", "small test audience" with no size given). 4 independent presenters say a version of it; none show data. What it implies if true: R5 (stranger-first design), R23 (each post judged alone), R14 (volume is not punished). What to check: share of views from non-followers per post `[verify UI]`. Cards: [c318b8e45196] [e3a9ae26373a] [34a52f48158a] [e1440ddfb8b1].

**R98. Claim: the platform reads a video's topic mainly from the auto-transcript and the caption, and needs about 30 to 50 consecutive same-topic videos to learn the avatar.** 08 only; the presenter says the number is his heuristic, not a platform figure. Implication: R55 (name topic and audience in speech and caption), R17 (commitment window). Cards: [34a52f48158a] [d84a8df8c294].

**R99. Claim: a broad hit that pulls in unrelated groups makes the platform's next-post targeting noisier and hurts monetisation.** 08 only, illustrated with a hypothetical, not a case. Implication: R6. What to check: performance of the 3 posts after any unusually broad hit `[needs brand data]`. Cards: [d6fdd4b41759].

**R100. Claim: under interest-based distribution, posting more does not punish the account; a weak post is simply shown less.** 04 only, backed by the presenter's own 2 half-years (2.5 posts a day gained 20,000 followers in 6 months with collaboration boosts; 4 posts a day gained 60,000 in the next 6 months without them). Single account, confounded, as the presenter admits. Implication: R14. What to check: unfollows and follower-share of views as cadence rises `[needs brand data]`. Conflict: C1. Cards: [c318b8e45196].

**R101. Claim: scheduling tools, native or third party, reduce organic reach.** 03 only, from an internal Cut 30 comparison across "hundreds of videos" with no method shown. 03's own cards say to test manual vs scheduled on the brand's account before adopting it. Implication: R116. Conflict: C3. Cards: [7ff53d5768f7].

**R102. Claim: TikTok Business accounts without a Shop are deprioritised; Creator accounts are the default; the account must be registered and posted from the target country.** 03 only. `[verify UI: current account types and any stated distribution difference]` `[needs brand data: where the account and phone number are registered]` Implication: R112, R113. Cards: [b22a54d48616].

**R103. Claim: outbound links and cross-platform routing are throttled, and users resent being moved between platforms.** 08 only. The only allowed bridge is social to owned (email, community). 03 conflicts by cross-posting everywhere and linking to lead magnets. Implication: R129, R110. `[web check: current treatment of link stickers and outbound URLs per platform]` Conflict: C11. Cards: [03e0df5b81d9].

**R104. Claim: an open DM thread makes the platform more likely to show the person your next post; comments are a rewarded engagement signal.** 04 (thank-you DM and comment-to-DM loop), 09 (comment spikes). `[web check: is any of this documented]` Implication: R119, R123. Cards: [b539e41f421e] [79467cee9f17] [00f161224b14].

**R105. Claim: the platform prefers fast content, and exaggerated language changes algorithmic pickup.** 10 (speed), 06 (exaggeration). Neither shows data; 06's exaggeration advice is overridden by R44. Cards: [bde55a0463de] [d52d9eff6cd1].

**R106. Claim: valuable short-form content keeps earning for months because Instagram content surfaces in Google search and seasonal topics re-spike.** 03 only, from his own channel. `[web check: current Instagram indexing in Google]` Implication: R132. Cards: [26f23bfd7ece].

**R107. Claim: Meta wants brands to lead with entertainment, not education.** 04 attributes this to a private, unofficial conversation with an unnamed Meta employee who asked him not to promote it. Not citable. Conflict: C2. `[web check: any public Meta statement]` Cards: [9fce1289b063].

**R108. Claim: platforms score new content against the patterns of top content in the category (visuals, transcript, captions, pacing).** 09 only, offered as a premise. Implication: R140 teardown research. Cards: [1445bdd3ed8e].

**R109. Follower count is a weaker but real funnel step.** Followers are slightly more likely to see the post, more likely to become superfans, and viewers rarely go straight from stranger to customer. Stories are where followers pay off (clicks and CTAs). 04 only; no conversion rates given. Cards: [4c8610731e7c].

### A.2 Source credibility write-ups (moved from section 12)

Each mini playbook: number, title, type, credibility and bias, what it contributed most. Ratings: credibility 1 (opinion only) to 5 (measured, independent); bias 1 (no commercial interest) to 5 (selling the thing the advice justifies).

**01. The 3-Step Writing Framework That Helped Us Build +$10M Newsletters.** Podcast transcript (My First Million), Sam Parr and Shaan Puri. Operators who built and sold The Hustle (about 2 million subscribers) and Milk Road; craft advice with borrowed frameworks (Ogilvy, Sorkin, Stephen King, Paul Graham). Credibility 3: real operating experience, no tests, every number a heuristic or a retold case (Hint Water, Buffett letters). Bias 3: promotes a $1,000 Maven course and copythat.com mid-episode; the title says 3 steps, the content teaches 4. Contributed most: the writing process (copywork, dump draft, incubate, edit), reading-grade targets, the cover test for openers, honest curiosity gaps, voice-memo topic filter, swipe files, intention and obstacle, sentence rhythm. Cards: 24.

**02. The Right Way To Write With AI.** Podcast interview transcript with Nicolas Cole. Ghostwriter for "north of 300" clients, co-founder of TypeShare and Ship 30 for 30; no ecommerce data, all anecdote. Credibility 3: a coherent framework from long practice, no measurement, an unverified "$30 million" host claim. Bias 4: the framework is the pitch for his SaaS and cohort; the "5 pieces a day" floor is his agency's number. Contributed most: AI repeats and humans originate, the positions log, "I" vs prescriptive "you", voice as variables, timely vs timeless, the unmade data set and company brain, value-by-horizon, infrastructure vs input. Cards: 24.

**03. How to start brand social media from scratch in 2026.** YouTube talk by a creative-strategy consultant running Cut 30 (2,000 graduates claimed). Credibility 2: self-reported pattern-matching across students, one internal scheduler test with no method, algorithm claims stated as certain, a paid Omnisend segment. Bias 4: sells the Cut 30 challenge; sponsor read inside. Contributed most: the 4 pillars and the 2-to-3-pillar, 4-to-6-posts, 1-month plan; the no-CTA-until-5,000-views rule; Creator vs Business accounts and country; manual posting; comment and DM sales process; the set as a credibility multiplier; batching every 2 weeks; plain-text founder email. Same program as 10. Cards: 16.

**04. Instagram Expert Explains How to Grow from Zero Followers in 2026.** YouTube interview with Brock Johnson, Instagram coach. Credibility 2: one account's confounded posting experiment, anecdotes about other creators, an unofficial Meta conversation, his own ManyChat figures. Bias 4: sells courses and coaching; the entertainment-over-education claim cannot be cited. Contributed most: the 1-year horizon and 8% expectation, 80% Reels, more posts more growth (claim), visual hook first, hook swaps vs clickbait, SHARE, stranger-first, metric by phase, comment-to-DM and the thank-you DM, follow-up from DM analytics, low-ticket in-app, series and challenges, commit to the bit. Same presenter as 05. Cards: 16.

**05. I Studied 1,300 Hooks, Here's What Actually Works.** Video transcript by the same coach as 04. Credibility 2: a self-collected sample of 1,300 "viral" Reels with no selection method, a ChatGPT reading-level check with no rubric, a repeated 22x stat; the findings are directional. Bias 4: sells Insta Club ($7 trial) and DM-gated guides; 3 unrelated sponsor reads; a Notion plug in the tracking step. Contributed most: 5 to 8 word hooks, 5th-grade hooks, negative framing on average, visual over text, the 15 hook types with examples, the Goldilocks curiosity gap, match-cut hook swaps, first-frame rules, hook swipe file and type tracking. Cards: 14.

**06. The Secret to Making Viral Content That Actually Sells.** Live talk transcript by "Davey", an ecommerce operator (a wearable-blanket brand and an oral-care brand; "7.5 billion impressions" claimed). Credibility 3: the only source speaking as a store operator with sales numbers, but all self-reported, an uncited Stanford study, mangled brand names in the captions. Bias 2: no product pitched on screen; still a self-promotional talk. Contributed most: story over specs, founder questions, the 30-minute carousel, frame swiping and the teardown grid, open loops, the founder-capacity plateau, scalable formats, creator bench and archive, 4-times reuse, next-day recall, contrarian angles, proximity. Also the source of the riskiest advice here: exaggeration, courting controversy, counterfeit accusations, undisclosed AI voices (all overridden). Cards: 16.

**07. the ONLY way to BEAT the Instagram algorithm in 2026.** Video transcript by an unnamed Instagram coach ("over 300 creators"). Credibility 2: client cases with no verification, algorithm claims from "the analytics right there". Bias 5: sells an AI research tool and a mentorship built on exactly this narrative; single-Reel revenue claims tied to that mentorship. Contributed most: the Creator DNA statement, manual competitive research and the idea bank, the gap on proven topics, lighting over camera, conversational hooks, batching in separate sessions, macro analytics (3 lists plus flops), the 70% to 80% follower-share signal, comment-triggered lead magnets 1 to 2 a week, owned list over sponsors, capacity before reach. Cards: 10.

**08. Social Media Isn't Hard. It's Misunderstood.** Video script by a creator with "1 million+ followers". Credibility 2: a consistent strategic argument with no platform documentation; numbers are metaphors ($52 AdSense, 35 mph vs 50 mph platforms). Bias 4: promotes Wavy World and Sandcastles inside the talk. Contributed most: media matching (claim), topic discipline and 30 to 50 videos (claim), on-target virality, one hero platform plus email for 6 months, islands not ecosystems and the outbound-link claim, world building, the media-layer monetisation trap. Card adaptations (pet supplies, camping gear, PDP-to-email) are the card writer's. Cards: 6.

**09. 5 Proven Social Media Marketing Strategies to Grow ANY Business.** Video transcript by an unnamed marketing YouTuber. Credibility 2: anonymised cases ("Bob and Bob 2", a coffee roaster, a B2B firm), "100x" and "9 cents per click" anecdotes, the content graph explained without a platform citation. Bias 5: a ManyChat affiliate trial and his own free course inside the video. Contributed most: the content-graph frame (claim), raw over gallery-era polish with the luxury and regulated caveat, the S.G.T.M.S. loop and 10-plus variations, AI as a targeted pre-publish reviewer, transcribing top performers, branded series with completion, saves and replays as metrics, satellite accounts after proof, the mid-funnel asset, end-to-end DM flow testing. Cards: 10.

**10. How to Make Viral Content for ANY Business.** Video transcript by the Cut 30 presenter (same program as 03). Credibility 2: a menu of reframes with named anecdotes and no numbers except one self-contradicting follower multiple; strong absolute language. Bias 4: sells Cut 30; a Dropbox sponsor read. Contributed most: "no boring business", format shakeup, speed as a vehicle, the viral vehicle prop, attention hijacking, pop-culture riding, hot takes, the versus format with a verdict, embarrassed questions, lore and depth, tour-guide positioning, event reframing, the single distinctive visual element. Card adaptations (series commitment, calendars, legal screening, keeping a "what we make" pillar) are the card writer's. Cards: 13.

### A.3 Owned-media and moat examples (moved from section 3.14)

**R159. Funding 1 or 2 deep thinkers to build the original library is, per 02, the best marketing spend a company with budget can make, but only with the remix and distribution machinery in place.** Source: 02 only, stated as opinion. Cards: [320db8651bf5] [bda11c7340cf].

**R160. Expect owned media to be part of brand strategy.** 02 cites OpenAI buying the podcast TBPN `[web check]`; the small-brand version is owning the category narrative through an original library rather than only ads. Source: 02 only. Cards: [264a1b8b2dd8].

**R162. A distinct methodology is a moat for a product as much as for a content program.** 02's own SaaS is sold on a method, not features; a self-interested example. Source: 02 only. Cards: [687b8507e264].

### A.4 Writing-process mechanics (moved from section 3.4)

**R46. Run the 4-step process: copywork, dump draft, incubate, edit.** Copywork: hand-copy (or type) a piece of admired writing in the tone you want, word for word, for 10 to 15 minutes. Draft: write fast and badly, show no one. Incubate: step away for at least about 90 minutes doing something passive (walk, shower, cook); longer gaps up to a day or a week are fine. Edit: come back and cut hard; quality is made here, so budget more time for editing than drafting. Condition: any piece that matters; short captions can skip copywork but not the edit. Source: 01 only. Cards: [c807997f7db2] [ea8652fd50e8] [8c85d056f475].

**R49. Say it out loud before you write it, and read it aloud before you publish it.** Ask the writer to explain the idea in plain speech; the spoken sentence often becomes the first line or all the copy needed. If it cannot be said plainly the thinking is not clear yet. 07 applies the same test to hooks ("does it sound like an ad or like a friend"). 09's AI review asks for captions "shorter and easier to read on a phone screen". Condition: every hook and script. Sources: 01, 07, 09. Cards: [4f3116aa30c6] [4f38d9d987ed] [3a5f43d052ea] [8907bbacfafe].

**R50. Vary sentence length for rhythm; default short.** "Any time you want to use a comma, use a period", then start the next sentence with "and" or "but" if needed. After a run of short sentences, add a medium one, then occasionally a long one. Use imagined reader lines ("you're asking yourself right now...") as pacing devices. Condition: any copy that reads flat on review. Source: 01 only. Cards: [056882fe4e22].

**R53. Filter topics with a 60-second voice memo.** Record yourself telling a friend about the topic. If it would not come up naturally in that conversation, drop it. If it passes, transcribe the memo and lightly edit it into the draft. Condition: choosing story angles, blog topics and campaign angles. Source: 01 only. Cards: [16e4989b065a].
