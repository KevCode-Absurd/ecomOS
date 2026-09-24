# Claude Code + SEO Masterclass

source_id: 1hYzTBBPl1sw7QddzmWe8xZ-hHQzyTdEL  |  folder: 15-SEO-search  |  cards: 33  |  words: 13,299  |  type: video transcript (masterclass/course-style YouTube video)

credibility: A single, unnamed presenter teaching his own past playbook. He claims he "earned over half a million dollars on the previous company I sold," generating "50,000 clicks every single month or 1,500 clicks every single day," and says it took him "four to maybe six years to learn this kind of stuff." No company name, niche, dates or third-party verification are given anywhere in the transcript; these are self-reported, unverifiable numbers used to open the video. His worked examples are all built live around a fictional/demo "plumbing" business, not the company he claims made him the money. He runs a free "school" community (gated lead magnet: a Claude.md template file, prompts, and a humor-reference example) and sells a paid community/agency program covering (a) becoming an AI-automation freelancer and (b) automating up to 80% of a business's operations, with weekly group calls and a free 30-minute agency consult. The curation metadata attached to this source (not the presenter's own words) explicitly flags "promotional pitches for Pexels API setups, Namecheap domain purchases, and the creator's paid agency/community programs" as material to skip. Treat every number and claim as one practitioner's self-reported opinion and demo, not a study, case audit or client result.

date signals: Modified 2026-09-20. Tools named as current: "antigravity.google" (a free desktop coding workspace into which a "Claude Code" extension is installed), SEMrush Keyword Magic Tool and Keyword Strategy Builder, Pexels API, GitHub, Vercel (Next.js preset), Google Search Console, Google Analytics, Google My Business, Chrome DevTools Lighthouse, Upwork. The presenter calls Google My Business "the lowest-hanging fruit that anyone can do in 2026," dating the recording to 2026. AI coding tools, IDEs and their extension ecosystems change fast; every tool name and UI step below is tagged for that reason.

## 1. What this source is for

A start-to-finish demo of using an AI coding agent (Claude Code, run inside Google's Antigravity desktop app) plus SEMrush to build, write, optimize and deploy a lead-generation website for a local service business, then package the whole process into a reusable "skill." It covers keyword research, site scaffolding, blog and service-page generation, brand-voice injection, on-page and technical SEO remediation, deployment, and post-launch indexing/tracking. It is built entirely on a services/local-business example (plumbing); it does not natively address ecommerce catalog structure, PDPs or checkout, and the cards attached to this source mark every ecommerce application as a suggested translation, not a demonstrated one.

## 2. Principles

1. **Not every keyword is equal; filter before writing.** A blog post or landing page built on the wrong keyword fails regardless of how well it is written or built. Condition: applies at the start of any content or landing-page plan. Evidence: presenter's framing and years of stated experience, no external data. [f4d899912dce] [e3f640eda70f]
2. **Match search intent to page type.** Informational-intent keywords (e.g. "how much does a plumber cost") get blog posts; transactional/money keywords (e.g. "plumbing Toronto") get service or landing pages; keywords whose top results are other businesses, directories or unrelated brands get skipped entirely. Condition: judge intent from what Google currently shows for the term, not from the words alone. Evidence: presenter's live walkthrough of a SERP. Generic principle; source's own worked examples are services, not ecommerce; the source's own suggested ecommerce mapping (buy-intent → category/product pages, research-intent → blog/guides linking into them) is not demonstrated. [4cf93efa0b3e]
3. **AI cannot supply keyword data on its own.** Asking a model directly for keywords (the source's own bad example: "Give me 20 keywords for plumbing") returns a guess with no difficulty or volume attached. Condition: always source keyword difficulty/volume from a dedicated keyword tool first, then hand the shortlist to the coding agent. Evidence: presenter's direct claim, untested against a specific model. [e3f640eda70f]
4. **Static rendering is framed as a hard requirement for crawlability.** The presenter states plainly that with client-side rendering "it doesn't even give you the site back... you can't really rank on Google whatsoever," and instructs the Claude.md file to force static site generation (SSG) by default. Evidence: presenter's own analogy (ordering pizza already made vs. cooked to order vs. made from scratch), no citation. **This is contradicted** by this library's own added caveat on the crawling card: "Static generation is not a Google indexing requirement... Google can execute JavaScript." Treat the presenter's version as overstated; see section 9. [b5a63fb310d9] [df678a62]
5. **A design reference stops AI output from reading as generic.** Without an attached visual reference, the source says Claude Code output "comes out as AI slop." Condition: always attach a screenshot before the first build prompt. Evidence: presenter's stated experience, no measurement. Generic to any AI site-build task. [b5a63fb310d9]
6. **Generic AI writing kills read-through; inject real voice, humor and stats before publishing.** The source reads its own first-draft blog opening ("In today's fast-paced world...") and calls it "crap" that nobody will read. Condition: applies to any AI-drafted page meant to hold a visitor's attention. Evidence: presenter's own before/after comparison, subjective. [24994938e6b4]
7. **Reverse-engineer the current top three results before drafting.** Have the agent check the live SERP, average the top 3 non-forum results' length, heading count and subtopics, and use that average as the target spec. Condition: pre-step before every new page. Evidence: presenter's method, framed explicitly as a heuristic ("SEO is a black box... mimicry... is a heuristic, not a guaranteed ranking mechanism"). [5e49646f576c]
8. **Keyword clusters let one page rank for many queries.** One root keyword plus a tight cluster of variants, with the root placed in the first 100 words. Evidence: presenter's own explanation and example (root "how to unclog a drain" plus 6 variants). [ef4ca0c529fd]
9. **Content pages and money pages play different roles and should feed each other.** Blog posts build topical authority; service/landing pages capture buy-intent traffic and convert; interlink blog → money pages so authority flows toward conversion. Evidence: presenter's stated model, explicitly given as opinion ("in my opinion"), not measured. [b818a1cea77a]
10. **Zip services and locations into landing pages, but do not overbuild.** List services on one axis, locations/municipalities on the other, and build one page per combination for the resulting "service + city" money keywords; deliberately cap the count because near-duplicate pages can be a negative signal. Evidence: presenter's own judgment; he gives no objective cap ("no objective metric where it's like 52.7 is the cap... probably wouldn't even have like multiple hundreds"). [ecfb3aa47dee]
11. **A/B test landing pages, then standardize the winner everywhere.** Presenter ran 5-10 paid landing-page variants via Google Ads and found a version converting at 20% (1 in 5 visitors to paying customer); he then reused that structure across every service page. Evidence: single, undated case result with no stated traffic volume, duration or significance test. [79879edd876d]
12. **SEO is a black box; content quality is the practical lever.** Over 200 rumored ranking signals exist and nobody outside Google knows the weighting; the presenter's operating simplification is "Google wants ad money, ad money needs attention, attention needs content people actually want to read," so content quality/engagement (dwell time, bounce rate, scroll depth, CTR) is the tiebreaker. Evidence: presenter's own reduction of an admittedly opaque system, stated as such. [054b0e78e62b]
13. **AI-search visibility is asserted to follow from ordinary search visibility.** The presenter's claim: ChatGPT, Perplexity and Claude all "search for the answer... on a search engine like Google" first, so ranking well for SEO should carry over to AI answers, and he treats "AI SEO" as a label rather than a separate playbook. Evidence: presenter's own reasoning, offered explicitly as "my honest thoughts," no measurement, and retrieval behavior across AI answer engines changes often. [b21ef0f9381d] [web check: whether current AI-answer engines (ChatGPT, Perplexity, Google AI Overviews, Claude) still source primarily from live web search rather than licensed/first-party data, since this changes]
14. **Off-page SEO is treated as optional and risky, by this presenter's own choice.** He states he does not do off-page SEO now, has "seen so many people have their businesses devastated by it," and prefers reinvesting effort in content and technical work. Evidence: personal, undated anecdotal experience ("used to work really well... 2018, 2019, 2020"), explicitly presented as his opinion, not a rule. [0878cf8caa37] [2d1aea0b1ec7]
15. **Programmatic/bulk publishing risks a Google penalty; ramp it.** A sudden flood of new pages is described as "an easy way to get banned," so pages should be released on an increasing cadence rather than all at once. Evidence: presenter's own caution, not cited to any Google policy statement. [e400cd54ed6c]

## 3. Procedures

**A. Scaffold the site**
1. Install the coding workspace: go to antigravity.google, download the free desktop app, open the Extensions tab, search "Claude code," install it. [verify UI: install flow, pricing, and whether "Antigravity" and its Claude Code extension still exist under these names] [b5a63fb310d9]
2. Create one empty project folder on your computer (source's example name: "SEO brief").
3. Add a single `Claude.md` file at the folder root. Source's own description: "In this file... think about an analogy of you hiring an employee. You need to train them on what they need to do, how to behave, all the standard operating procedures." The presenter's own template is gated behind his free community link; its exact contents are not given in this source, so its rules cannot be reproduced here. [web check: Claude.md is a real, load-bearing convention for the Claude Code CLI — verify current file name/behavior] [needs brand data: your own house-style / SOP rules to put in this file, since the source's copy is not reproducible]
4. Open Claude inside the workspace and send the build prompt, quoted verbatim from the source: **"Can you please build out a beautiful website for me with the following pages: a homepage, a index page for my blog posts, an index page for my service posts, and that's it. I'm going to attach a screenshot down below of the design I'm looking for. Please clone or copy that exact design when building out the website page."**
5. Before sending, get a design reference: go to Dribbble, search a relevant term (source's example: "plumbing website"), open the first result, screenshot the landing page, and attach it via the chat's upload/plus button. [verify UI: Dribbble search/UX] [needs brand data: your brand's actual visual identity/design system — the source substitutes a stranger's Dribbble shot]
6. Open the local preview link (localhost) the agent returns and check the build.
7. Confirm the build is static site generation (SSG), not server-side rendering (SSR) or pure client-side rendering. The source's own Claude.md sets SSG "by default" as "a requirement." [b5a63fb310d9] — but see principle 4 above on how strongly the source overstates this requirement.

**B. Find and filter keywords**
1. Do not ask the coding agent for keywords directly; use a standalone keyword tool. Source: SEMrush, "SEO" then "Keyword Magic Tool." [verify UI: SEMrush interface/pricing; source says "you can get started on a free trial" and states he has used it "for probably 4, 5 years"]
2. Enter a root keyword (source's example: "plumber"). The tool returns keyword variations containing that root.
3. Filter to keyword difficulty of 30 or below (source's example of an easy win: difficulty 2/10).
4. Filter to monthly search volume of at least 100.
5. Manually sweep the remaining list and discard: other businesses' names, industry mascots/branded terms, and job-seeker queries (source's own rejected examples: "Hydrojet Plumbing," "Plumb Bob," "Zeke the Plumber").
6. Use the tool's "Questions" tab for long-tail "how much does X cost"-style queries; select ones with buyer intent (source keeps "how much does a plumber cost," discards "how long does it take to become a plumber" as competitor/job-seeker intent).
7. Add adjacent, higher-funnel topics for the same eventual buyer (source's examples: "best water softener 2026," "tankless first tank water heater," "signs you need a new water heater").
8. Optionally pull competitor keywords: enter a competitor's domain in SEMrush and harvest their ranking terms.
9. Add selected keywords to a named list inside the tool (source: "plumbing keywords"), then export as CSV once you have "a couple hundred to a couple thousand" entries.
10. Drag the exported CSV into the coding workspace and rename it (source renames it "keywords"). [e3f640eda70f]

**C. Generate a first blog post with images and a keyword cluster**
1. Get a free image API key: go to Pexels, create an account, request an API key under a project name, copy the key into a `.env` file in the project as `VARIABLE_NAME=key`. The source explicitly warns: ".env folder is just where you store your password, secret keys, anything you wouldn't want anyone else to see" — do not expose this key in any client-facing code or commit. [verify UI: Pexels API signup flow] [needs brand data: consider whether stock photos (Pexels) are acceptable for your brand, or whether real product/location photos are required — see conflict noted in section 9]
2. Send the build prompt, quoted verbatim: **"Can you please create a blog post for me about plumber for low water pressure? That's the keyword that I want you to use, and I also want you to create a keyword cluster. That keyword cluster can either be from common keywords in the keywords.csv file or you can just make it up. Please add in images from Pexels, and my API key is in the .env file attached."**
3. Review the result. The source's own honest assessment of this first pass: "this is crap... nobody's going to sit through this guide." Do not stop here. [ef4ca0c529fd]

**D. Inject brand voice, humor and stats before anything ships**
1. Gather source material: call/video transcripts, emails, LinkedIn or other social posts you've written, or passages from other writers whose tone you like.
2. Create separate reference files inside the project for voice, humor, opinions, and stories/stats. Prompt pattern used in the source (paraphrased, not a single verbatim line): ask the agent to create and then update these files from the pasted reference material.
3. Include concrete, real numbers and anecdotes the model can reuse (source's prompts to itself: "how many drains have you unclogged, how long you've been in business... stories, if there's any anecdotes from... past jobs"). [needs brand data: your own real numbers, tenure, and anecdotes — required for this step to work at all]
4. If you have no reference material, borrow and adapt a tone reference. The source's own example, lifted from an unnamed rap lyric and adapted: "I've got 99 problems, I feel bad for you, son. I've got 99 problems, but humor ain't one." Prompt: "Please add this as a humor reference."
5. The resulting humor-rule text the agent produced and the source shows verbatim: **"Plumbing is boring, your job is to make it more fun. Blog. Every blog post should be funny, this isn't optional."** and the opening rule: **"if the first 50 words don't land at least one dad joke... or a self-aware wink or a parenthetical side, rewrite them. We are not a brochure, we are a guy at the pub who has had one beer and is now explaining how the toilet works."** This specific comedic voice is the presenter's own choice, not a universal rule — substitute a tone that fits your brand. [24994938e6b4]
6. Re-run any later optimization pass with an explicit instruction to preserve this voice (see step F).

**E. Reverse-engineer the top-ranking pages before rewriting**
1. Identify the top 3 non-forum results (source excludes Reddit) for the target keyword.
2. Have the agent analyze all three for average word count, average H2 count, image count and subtopics covered.
3. The source states it has a saved prompt for this step ("I have prompts and we can literally just copy this in") but the transcript does not quote the prompt's exact text — only its intended effect: rewrite using the brand's voice/humor/opinion/stats/stories, first check Google for the primary keyword's top results, then steal the winning format, length and topics. **The exact prompt wording is not recoverable from this source; do not invent it.**
4. Compare before/after: source's before example ("In today's fast-paced world, maintaining a functional household...") vs. after ("Your toilet has been hissing for longer than most celebrity marriages..."). [5e49646f576c]

**F. Build a service/landing page**
1. In SEMrush's Keyword Magic Tool, sort the root keyword by cost-per-click (CPC) to surface money keywords (advertisers paying for a term is treated as evidence of commercial value). Source's caveat: a displayed CPC of ~$700 in his own demo is "bad data... overexaggerated"; he states typical CPC usually runs "between 3 and $20."
2. Identify the "service + city" or "city + service" pattern directly in the CPC-sorted list (examples: "Plumber West Chase," "Arnold, MD," "Baldwin Park, CA").
3. Save these to a separate keyword list (source: "service pages"), export as CSV, and drag it into the workspace (source renames it "service keywords").
4. Send the build prompt, quoted verbatim: **"I want to build out a page with the primary keyword from this. This is a landing page specifically for city and service. The landing page should look pretty much the same as the homepage."**
5. Reuse your best-converting layout as the template for every service page (see principle 11); the source deliberately makes the service page look like the homepage.
6. Cap the number of these pages. The source gives no formula, only judgment: avoid thousands, probably avoid "multiple hundreds." [ecfb3aa47dee]

**G. Apply the on-page SEO checklist**
1. The source describes maintaining an "80+ signal" on-page checklist as a standalone document/prompt it pastes in whole; the exact checklist content is provided in the video description, not the transcript, so **only the following verified sub-items are recoverable from this source**: primary keyword in the first 100 words; 4-8 questions per post; exactly one H1 (multiple H2/H3 allowed); 2-3 external links; 3-5 internal links to your own related pages; a meta title and meta description (invisible on-page; check via DevTools → Elements → head/meta tags, or search the OG tags).
2. Send the checklist prompt, quoted verbatim: **"Can you please upload the blog posts or update the blog post with the on page SEO checklist item from this. We also need to add all the following items but still maintain the voice and style of the blog post."**
3. Verify by spot-checking the rendered page (not just trusting the agent's summary): confirm the external/internal link counts, check the primary keyword appears early, and inspect the meta title/description in DevTools.
4. Run this same checklist on every page — blog posts and service pages alike. [aeeccc51cf9d]

**H. Run the Lighthouse remediation loop**
1. Open Chrome DevTools (three-dot menu → More tools → Developer tools), find the Lighthouse panel (behind a double-arrow icon if hidden), and run an audit ("analyze page load").
2. Read all four scores. Source's own first-run numbers: **SEO 92, best practices 100, accessibility 96, performance 53**.
3. Expand every failing audit tab, including SEO failures, so the full detail is visible.
4. Copy the entire report and send it with this verbatim prompt: **"here's my lighthouse report. Can you please optimize it so that I have a 100% score across all areas performance, accessibility, best practices, SEO. Can you also generate the robot.txt file and the sitemap.xml file?"**
5. Re-run Lighthouse. Source's own second-run numbers: **100, 100, 100, and 96** (performance did not reach 100 on this run either).
6. If any score still falls short, paste the new report back in and repeat until resolved. [67c0def66dd3]
7. Inspect the generated `sitemap.xml` (confirm every page you want indexed is listed) and `robots.txt` (confirm it allows crawling except admin/dashboard/login paths, or any other paths you don't want indexed — for ecommerce, the cards suggest excluding internal search, filtered/faceted URLs, and account/cart paths, though the source itself never discusses ecommerce URL structures). [dc2f8bf6bb36]

**I. Package the workflow into a reusable "skill"**
1. Complete at least one blog post manually end-to-end first, per the workflow above, before automating.
2. Send the skill-creation prompt, quoted verbatim: **"Can you please create a skill for me called blog. Where we automatically generate blog posts with all of the details that we just covered in this conversation. We need to grab a keyword from keywords.csv. Then we need to create a keyword cluster. We need to publish that blog post and pull in pictures from Pexel. We need to also add in our writing style, voice, tone, humor. We need to then optimize it for on-page SEO. And for the technical SEO, we need to make sure that we use the same standard template every single time. We've already optimized the technical SEO. I want you to reuse the same page structure for every future blog post."**
3. Start a fresh chat session for the skill to take effect (source's own note).
4. Trigger the skill by typing its name (source: typing "blog" and sending it).
5. Optionally schedule it (source mentions running it automatically at 9:00 a.m., skipping already-used keywords), but verify current scheduling capability in your coding tool. [verify UI: skills and scheduled/automated runs are a fast-moving feature area]
6. Build a second, parallel skill for service/landing pages using the same pattern.
7. Spot-check outputs manually; the source itself hit an error on one scheduled run and had to resend. [cd866609b795] [7ad5eaa168b2]

**J. Deploy**
1. Create a new GitHub repository (source recommends private) and copy its setup code.
2. In the coding tool, send: **"Please upload my whole project here."**
3. Create a free Vercel account, connect/integrate GitHub, add a new project, import the repo.
4. **Set the application preset to Next.js** — the source states this is required for the deploy to work.
5. Click deploy; source states it goes live in about 60 seconds.
6. Optionally add a custom domain via Vercel's own domain purchase, or buy cheaply elsewhere (source names Namecheap — flagged by the source's own curation metadata as a promotional mention) and import it. [894f3a3ed6026]

**K. Post-launch checklist, in the source's stated order**
1. Claim a free Google My Business listing (source calls this "the lowest-hanging fruit... in 2026").
2. Set up Google Search Console: copy the live Vercel URL, add it as a URL-prefix property, choose HTML-tag verification, copy the tag, and send: **"Please add this meta tag to the website for the Google Search Console verification, and then deploy this live to GitHub and then to Vercel."** Then verify in Search Console (source warns a typo in the tag breaks verification).
3. In Search Console's sitemap section, enter `sitemap.xml` and submit it.
4. To speed up indexing of a specific new page, paste its URL into the Search Console search bar and click "Request indexing." Source: this can get a page indexed in about a day versus the weeks or months it would otherwise take, but is capped at roughly 10 requests per day.
5. Set up Google Analytics to track visitor behavior.
6. Test landing pages (source ran this via paid Google Ads traffic, 5-10 variants) to find the highest-converting version, then standardize it across all pages.
7. Throughout all of this, keep publishing volume moderate (see section D of principles / the cadence table below). [45d4cfbd90fd] [4f3b94c692d3] [427d9666c474] [4b0b2abd2630]

**L. Off-page/backlink tactics (source frames as theoretical; he does not practice this himself)**
1. Broken-backlink swap: run a site audit (source names SEMrush) on a relevant competitor or industry hub (source's example: Homestars.com), find their backlinks returning 404s, confirm you have an equivalent page, and reach out offering your page as the replacement link. Source warns this is slow and often gets no response. [03b3bc6a6a34]
2. Guest posting: search Google for `[your niche] write for us`, using quotation marks for exact match (source: "You want to have the quotations here to get the exact match" — exact query syntax not spelled out beyond this). Review sites soliciting guest posts, write for them, and get a backlink back to your site. [ee0764e85157]
3. "Hero journalism": watch for journalists publicly requesting expert answers to a question in your niche; answer with genuine expertise; if used, you get a backlink. [0d17f081b5be]
4. Paid quality backlinks: pay a reputable domain (source names Forbes/TechCrunch as possibly pay-to-play, and states he "could be wrong" about this) roughly $10-$1,000 for a post or an included link. Any paid placement must carry `rel="sponsored"` or `rel="nofollow"` — this qualifier is the card's own added compliance note, not stated by the presenter. [ed80a4bbd5e3]
5. Vet any backlink vendor by asking for a specific past client site plus the campaign's start/end dates, then check that site's traffic trend over the window. Source's own anecdote: a "top 1%" Upwork backlinker's example site showed a declining traffic line over the campaign period. [2d1aea0b1ec7]
6. Avoid "$5 for 100 backlinks" offers — these are typically PBNs (private blog networks / link farms) that Google detects, which can get a site blacklisted or permanently damaged. [0878cf8caa37]

## 4. Rules, thresholds and numbers

| Rule | Number / threshold | Condition | Source's basis | Card id |
|---|---|---|---|---|
| Keyword difficulty filter | ≤ 30 (example of an easy win: 2/10) | Filtering a root keyword's variations before committing content budget | Presenter's stated heuristic, "happened multiple times" for him | e3f640eda70f |
| Keyword volume filter | ≥ 100 searches/month | Same | Presenter's heuristic | e3f640eda70f |
| Keyword list size to aim for | A few hundred to a couple thousand keywords | Before exporting to the coding agent | Presenter's heuristic | e3f640eda70f |
| Keyword-cluster placement | Primary keyword in first 100 words | Every blog post, category or landing page | Presenter's convention | ef4ca0c529fd |
| Reverse-engineering sample | Top 3 non-forum (excl. Reddit) results, averaged | Pre-draft step for any new page | Presenter's method | 5e49646f576c |
| Humor-rule trigger | If the first 50 words don't land a joke/aside, rewrite | The presenter's own brand-voice rule, quoted above | Presenter's own stated rule, explicitly his opinion | 24994938e6b4 |
| On-page: external links | 2-3 per page | Every blog post/service page | Presenter's checklist item | aeeccc51cf9d |
| On-page: internal links | 3-5 per page | Same | Presenter's checklist item | aeeccc51cf9d |
| On-page: questions per post | 4-8 | Same | Presenter's checklist item | aeeccc51cf9d |
| On-page: headings | Exactly 1 H1; multiple H2/H3 allowed | Same | Presenter's checklist item | aeeccc51cf9d |
| On-page checklist size | "80+ signals" total (only the above are individually itemized in this source) | Same | Presenter's own compiled list, not published by Google | aeeccc51cf9d |
| Lighthouse target | 100/100 on SEO, accessibility, best practices, performance | Every page, pre- and post-launch | Presenter's own standard, not a Google-published requirement | 67c0def66dd3 |
| Lighthouse run 1 (example) | SEO 92, best practices 100, accessibility 96, performance 53 | Presenter's demo page, first run | Presenter's own demo result, not a benchmark | 67c0def66dd3 |
| Lighthouse run 2 (example) | 100, 100, 100, 96 | Same page, after Claude Code fixes | Presenter's own demo result | 67c0def66dd3 |
| Typical CPC for money keywords | ~$3-$20 (his own demo's $700 figure called "bad data") | Sorting Keyword Magic Tool by CPC to find service+city keywords | Presenter's observation | ecfb3aa47dee |
| Service-page count cap | No fixed number; presenter's own judgment is to avoid thousands and "probably wouldn't even have like multiple hundreds" | Service/location landing pages | Presenter's opinion, explicitly not an "objective metric" | ecfb3aa47dee |
| Landing-page conversion example | 20% (1 in 5 visitors → paying customer) | One winning variant out of 5-10 tested via paid Google Ads traffic | Single, undated case result, no sample size or duration given | 79879edd876d |
| Publishing ramp (example) | Day 1: 1 post, day 2: 1, day 3: 2, day 5: 3, day 8: 4 (roughly doubling) | Rolling out new programmatic/blog pages | Presenter's own illustrative, untested schedule | e400cd54ed6c |
| Publishing ceiling warning | Do not publish "a thousand blog posts a day" | Same | Presenter's caution, no Google citation | e400cd54ed6c |
| Indexing request cap | ~10 requests/day via Search Console "Request indexing" | Speeding up indexing of a specific new page | Presenter's stated rough limit; verify current Google quota | 427d9666c474 |
| Indexing speed via request | ~1 day, vs. weeks/months normally | Same | Presenter's claim | 427d9666c474 |
| Ranking signal count | "Over 200 rumored ranking signals" | General framing for why content quality is the practical lever | Presenter's stated figure, sourced to none | 054b0e78e62b |
| Off-page paid backlink cost | Roughly $10-$1,000 | Paying a reputable domain for a link/post | Presenter's estimate, hedged as possibly wrong | ed80a4bbd5e3 |
| Scam backlink red flag | "$5 for 100 backlinks" offers | Vetting off-page vendors | Presenter's warning | 0878cf8caa37 |
| Unsourced SERP CTR figures (not in any card; from raw transcript only) | ~40% of clicks to position 1, ~20% to position 2, "dramatically" less after | Framing why ranking position matters | Presenter's claim with no citation; not attached to a card | n/a — [web check: current organic CTR-by-position data, which also shifts with AI Overviews eating top-of-page clicks] |
| Presenter's own past results (context only, not a rule) | "$500,000," "50,000 clicks/month," "1,500 clicks/day," "4-6 years to learn" | Framing device for the whole video | Self-reported, unverified, no company named | f4d899912dce |

## 5. Diagnostics and checks

- **Static vs. rendered check.** Confirm the build outputs static HTML (SSG) rather than waiting on client-side JS. Good: content is present without waiting for JS execution. Bad: blank/incomplete initial HTML. Fix, per the source: instruct the Claude.md file to require SSG. Broader fix, per this library's own added guidance (not the presenter's): also check rendered HTML via Google's URL Inspection tool, since Google does execute JavaScript — SSG is a safety margin, not a strict requirement. [df678a62] [verify UI: URL Inspection tool location/behavior in current Search Console]
- **Lighthouse 4-score check.** Run DevTools → Lighthouse → analyze page load. Good: 100/100/100/100 (or as close as achievable — the source's own best run left performance at 96). Bad: any score meaningfully below 100, especially performance in the 50s (source's own starting point: 53). Fix: copy the full expanded report (including SEO tab) and hand it to the coding agent with the explicit instruction to hit 100% across all four areas plus generate robots.txt/sitemap.xml; repeat until resolved. [67c0def66dd3]
- **On-page checklist spot-check.** After running the checklist prompt, manually verify (don't trust the agent's summary): 2-3 external links present, 3-5 internal links pointing to your own related pages, exactly one H1, primary keyword within the first 100 words, and a populated meta title/description (check via DevTools Elements tab or an OG-tag search). Good: all present and voice/humor intact. Bad: checklist applied but tone reverted to generic/dry text — source explicitly warns this "fine balance" often breaks. [aeeccc51cf9d]
- **Sitemap completeness check.** Open the generated `sitemap.xml` and step through it page by page to confirm every page you want indexed is actually listed. Bad: pages missing from the sitemap cannot be found by Google regardless of content quality. Fix: regenerate the sitemap whenever new pages ship. [dc2f8bf6bb36]
- **Keyword relevance sweep.** After a keyword-tool export, manually scan for other businesses' brand names, mascots and job-seeker queries before saving to the campaign list. Good: every kept keyword represents a realistic prospective customer's search. Bad: kept a competitor's business name or an industry mascot term (source's own caught examples: "Hydrojet Plumbing," "Zeke the Plumber"). [4cf93efa0b3e]
- **Backlink vendor vetting check.** Before engaging any paid backlink provider, ask for one specific past client site and the campaign's start/end dates, then check that site's traffic trend across the window. Good: traffic held or grew. Bad: traffic declined over the campaign period (source's own example of a claimed "top 1%" vendor). Fix: do not engage; treat as a red flag regardless of the vendor's claimed reputation. [2d1aea0b1ec7]

## 6. Tools, settings and named features

- **Antigravity (antigravity.google)** — free desktop coding workspace; the source installs a "Claude Code" extension inside it via its Extensions tab. [verify UI: product name, install flow, extension availability all subject to change]
- **Claude Code** — the AI coding agent doing all build/write/fix/deploy work in this source; run as an extension inside Antigravity per this source (not necessarily how it runs elsewhere). [verify UI]
- **Claude.md** — a root-level markdown file used as a standing instruction/SOP file for the coding agent (design references, formatting rules, the SSG requirement). The presenter's own copy is gated behind his free community and not reproduced in this transcript. [needs brand data: your own SOP content for this file] [web check: current file-name convention for Claude Code project instructions]
- **Dribbble** — free design-inspiration site used to source a screenshot reference before the first build prompt. [verify UI]
- **SEMrush** — keyword research and competitive tool. Named sub-features used: Keyword Magic Tool (root-keyword expansion, difficulty/volume filters, Questions tab, CPC sort), Keyword Strategy Builder (saved keyword lists, CSV export), Site Audit (competitor backlink/broken-link discovery for off-page work). Presenter states years of personal use; a free trial is mentioned. [verify UI: current SEMrush pricing/interface] [not flagged in this source as sponsored, but is the sole named paid SEO tool throughout]
- **Pexels + Pexels API** — free stock image source and API used to auto-populate blog images; requires an API key stored in `.env`. Flagged by this source's own curation metadata as a promotional mention to otherwise skip. [verify UI: Pexels API signup]
- **Chrome DevTools / Lighthouse** — built-in browser auditing tool for SEO/accessibility/best-practices/performance scoring, used in the remediation loop. [verify UI: panel location described as "three dots → more tools → developer tools → Lighthouse," may move]
- **GitHub** — code hosting; source recommends a private repo for the project. [verify UI]
- **Vercel** — free hosting/deployment; requires the Next.js application preset to be selected for this workflow to work, per the source. Custom domains purchasable through Vercel or imported (source names Namecheap — flagged as a promotional mention). [verify UI]
- **Google Search Console** — property verification (URL-prefix + HTML meta-tag method), sitemap submission, and per-URL "Request indexing." [verify UI]
- **Google Analytics** — visitor behavior tracking, set up after Search Console per the source's checklist. [verify UI]
- **Google My Business** — free local business listing, called out as the easiest win for local/service businesses specifically. [verify UI]
- **Google Ads** — used in the source only to run paid traffic tests across 5-10 landing-page variants to find a conversion winner; not part of the core AI-SEO build, and outside this ecomOS repo's Meta-only ad scope. [verify UI]
- **Upwork.com** — mentioned only as where the presenter sourced (and then distrusted) a backlink vendor; not recommended as a tool to use, presented as a cautionary example. [verify UI]
- **"Skill" (Claude Code feature)** — a saved, reusable, named workflow (source names its blog skill "blog") that on invocation performs the entire keyword→cluster→draft→images→voice→on-page→technical pipeline using a fixed template. Source claims it can optionally run on a schedule. [verify UI: skills syntax and scheduling are a fast-moving feature area]

## 7. Examples and case results

- Presenter's framing claim (undemonstrated, no company named): "$500,000... 50,000 clicks every single month or 1,500 clicks every single day," attributed to a company he says he sold, condensed from "four to maybe six years" of learning. [f4d899912dce]
- Keyword filtering example: root "plumber" → filtered from "a million keywords" down to roughly 6,000 after applying intent, then down further with manual review; kept examples "plumbing installation," "plumber fix shower," "plumber plumbing drain washing machine"; rejected examples "Hydrojet Plumbing," "Plumb Bob," "Zeke the Plumber." [4cf93efa0b3e] [e3f640eda70f]
- Blog draft before/after: before — "In today's fast-paced world, maintaining a functional household is more important than ever..."; after — "Your toilet has been hissing for longer than most celebrity marriages. It's 11:00 p.m., you're Googling 'running toilet' instead of sleeping..." Presented as the source's own illustrative comparison, not a measured engagement result. [24994938e6b4]
- Keyword cluster example: root "how to unclog a drain," cluster includes "unclog kitchen sink," "unclog bathroom sink," "drain won't drain," "slow drain sink," "home remedy clogged drain," "what dissolves hair in drain." [ef4ca0c529fd]
- Service+location zipper example: services (emergency plumber, drain cleaning, hot water repair, leak detector) × cities (Vancouver, Toronto, Montreal, Edmonton). [ecfb3aa47dee]
- Landing-page conversion case: 5-10 Google Ads-tested variants, best performer reached a 20% (1-in-5) visitor-to-customer conversion rate; reused as the standard template. No sample size, duration or significance testing stated. [79879edd876d]
- Lighthouse before/after (same page): before 92/100/96/53 (SEO/best practices/accessibility/performance); after 100/100/100/96. [67c0def66dd3]
- Off-page vendor case: a claimed "top 1%" Upwork backlinker's own shown example site had a declining traffic line between the campaign's start and end dates. [2d1aea0b1ec7]

## 8. Mistakes the source warns about

- Asking the AI model to invent keywords instead of pulling difficulty/volume from a dedicated tool first. [e3f640eda70f]
- Building on client-side-rendered or slow-to-render architectures that crawlers can't index in time (source overstates the severity of this — see section 9). [b5a63fb310d9] [df678a62]
- Skipping a design reference image, which the source says produces generic "AI slop" output. [b5a63fb310d9]
- Publishing the raw, unvoiced first AI draft (source's own example opener: "In today's fast-paced world..."). [24994938e6b4]
- Running the on-page SEO checklist pass without an explicit instruction to preserve voice/humor, which reverts copy to "dry, boring" text. [aeeccc51cf9d]
- Keeping keywords that are actually competitor business names, industry mascots or job-seeker queries. [4cf93efa0b3e]
- Building "thousands" or even "multiple hundreds" of near-duplicate service pages, which the source treats as a potential negative ranking signal. [ecfb3aa47dee]
- Bulk-publishing a large batch of new pages at once instead of ramping the cadence — called "an easy way to get banned on Google." [e400cd54ed6c]
- Trusting cheap "$5 for 100 backlinks" offers, typically PBNs that Google detects and that can get a site permanently damaged or blacklisted. [0878cf8caa37]
- Hiring a backlink vendor without checking a concrete before/after traffic example first. [2d1aea0b1ec7]
- Skipping the Next.js preset step in Vercel, which the source says the deploy requires. [894f3a3ed6026]
- A typo in the Google Search Console verification meta tag, which breaks verification. [4f3b94c692d3]
- Trying to force a hero-journalism, guest-post or paid-placement backlink onto a page that doesn't genuinely cover the same material. [03b3bc6a6a34] [ee0764e85157]

## 9. Caveats, conflicts and what is missing

- **Direct conflict on static rendering.** The source states as fact that non-SSG sites "can't really rank on Google whatsoever." This library's own added caveat on the related crawling card directly contradicts that: "Static generation is not a Google indexing requirement... Google can execute JavaScript. Rendering support differs across crawlers; assess the actual store and target engine." Follow the corrected version — SSG is good practice for speed and reliability, not an absolute gate — and verify with Google's own URL Inspection tool rather than the source's stronger claim. [b5a63fb310d9] vs. [df678a62]
- **Tension with this repo's own product-accuracy rule.** ecomOS's house rules state that where accuracy matters, use the real product photo rather than a generated or stock substitute. This source defaults to free Pexels stock images for every blog post, which is workable for a local-service blog but should not be extended to ecommerce PDPs or category pages where the actual product must be shown accurately. This is not addressed by the source at all — it never discusses ecommerce product imagery. [needs brand data: real product photography, if this workflow is adapted to PDP or category content]
- **Almost entirely a services-business demo, not ecommerce.** Every worked example (blog posts, service+city landing pages, the humor voice, the CPC keyword sourcing) is built around a plumbing company. Every "for ecommerce" application in the attached cards is the card-writer's own translation and is explicitly marked as not demonstrated by the source. Treat the specific numbers (difficulty ≤30, volume ≥100, 2-3/3-5 link counts, 20% conversion example) as this presenter's heuristics for a local-service niche, not validated ecommerce benchmarks.
- **Two prompts are described but not quoted verbatim in the transcript.** The "reverse-engineer the top 3 results" rewrite prompt and the full "80+ signal" on-page checklist prompt are both said to exist and be pasted in, but their exact text is only in the video's description/community materials, not in this source. Do not reconstruct or invent this text; the procedure steps above state only what the source actually describes about their effect.
- **The Claude.md template itself is not reproducible from this source.** It is gated behind the presenter's free community; only its stated purpose (SOP, design references, SSG requirement) is known.
- **AI-SEO equivalence claim is asserted, not measured.** The presenter explicitly frames his "AI SEO is essentially the same as SEO" position as "my honest thoughts," with no data, and this is an area (how ChatGPT/Perplexity/Google AI Overviews/Claude actually source and cite) that changes quickly. [b21ef0f9381d] [web check: current AI-answer sourcing behavior before treating this as settled]
- **Off-page section is explicitly theoretical.** The presenter states he does not practice off-page SEO himself and is not an expert in it; his four "legit" tactics (broken-link swap, guest posting, hero journalism, paid placement) are offered "to be as comprehensive as possible," not as tested advice. [0878cf8caa37] [03b3bc6a6a34] [ee0764e85157] [0d17f081b5be] [ed80a4bbd5e3]
- **Every specific number is a single, undated, self-reported case, not a benchmark:** the $500k/50k-clicks framing, the 20% landing-page conversion rate, the Lighthouse before/after scores, the publishing-ramp schedule, and the ~10-requests/day indexing cap should all be treated as one presenter's examples, per the writing rule that a case result is an example, never a promise.
- **No engagement with ecommerce-specific technical SEO topics** (faceted navigation, canonical tags for variant URLs, out-of-stock handling, structured data/schema for products, pagination) — this source does not mention any of them. A folder-level (pass 2) merge should pull that from other, more ecommerce-native sources in this folder, not from this one.
- **Promotional material excluded per this source's own curation notes**: Pexels API setup, Namecheap domain purchases, and the presenter's own paid agency/community programs are flagged in the source's header metadata as pitches to skip; they are referenced above only where load-bearing to the technical steps (e.g., the Pexels API key is required for the image-generation prompt to work).

## 10. Card index

- 4cf93efa0b3efe218ae7e66e — Match search intent before writing anything
- e3f640eda70f616c8fce24ec — Filter keywords by difficulty and volume
- a8ed94c10b20e242f2bf9d4e — Build adjacent top-of-funnel topics to capture future buyers
- ef4ca0c529fd50b67ff78a7a — Build keyword clusters so one page ranks for many queries
- 5e49646f576c58e11fb56c8a — Reverse-engineer the top-ranking pages into a template
- 24994938e6b4add526299c1e — Train the AI on your voice, stories and stats before drafting
- b5a63fb310d920e5063b3dae — Batch a site build: pages, design reference and SOP file
- df678a626742279fa1b1ca43 — Check initial and rendered HTML on ecommerce money pages
- 67c0def66dd3c3bcbc2f8cdb — Run a Lighthouse audit and hand the report to the agent to fix
- dc2f8bf6bb362efd104e58e3 — Generate sitemap and robots.txt so pages can be discovered
- aeeccc51cf9d99081c380cd9 — Apply an on-page checklist without destroying the content's voice
- b818a1cea77a5032014286c8 — Separate content pages from money pages and let them feed each other
- ecfb3aa47deebc500cb8c106 — Zip services and locations into landing pages — without overbuilding
- 79879edd876dfca3379e7dd6 — Reuse your best-converting landing page across all money pages
- cd866609b795ed455014a951 — Package the whole workflow as a reusable skill
- 021e76f554cbd31a53cfc2fd — Stage ecommerce content releases around review capacity
- 0878cf8caa375f35d14d0a1a — Treat off-page SEO as optional and risky
- b21ef0f9381d653286d535b7 — Rank for search to rank in AI answers
- 054b0e78e62b4edf02efda18 — Optimize for content quality as the leading ranking lever
- f4d899912dce4e0421294f5f — Compress the whole SEO workflow into four buckets
- e400cd54ed6cd7c741474add — Stage programmatic page publishing to avoid indexing penalties
- 2d1aea0b1ec767f8a885fc48 — Why off-page link building is risky and often backfires
- 03b3bc6a6a34ab90bacbe933 — Broken backlink swapping as a legitimate link tactic
- ee0764e85157a82b88d0e0d7 — Guest posting for backlinks via 'write for us' searches
- 0d17f081b5be70b222d21708 — Hero journalism (journalist query response) for expert backlinks
- ed80a4bbd5e3ba79971b1ae1 — Paid quality backlinks from reputable domains
- 894f3a3ed6026ea40e130ff0 — Deploy a Next.js site free with GitHub and Vercel
- 4f3b94c692d30913c4fe6108 — Set up Google Search Console, verify ownership via HTML tag, and submit your sitemap
- 427d9666c4747692a9c5a4ff — Request indexing of a new page in about a day
- 4b0b2abd263042d0a00817ec — Claim a free Google My Business listing as the lowest-hanging local win
- 45d4cfbd90fd640a47edd0b9 — Post-launch SEO checklist order for a new store site
- 0800ac45ed9350449346cbb1 — Test landing pages to find the winning conversion formula, then roll it out
- 7ad5eaa168b21f83356c1f9a — Reuse a publishing skill across page types (blog and service pages)
