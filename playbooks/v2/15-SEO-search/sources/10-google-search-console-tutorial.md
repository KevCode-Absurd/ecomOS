# Google Search Console Tutorial (2026)

source_id: 1SFtoeiwB9Njoe-mUK0MHm-4b-f2l_nEC  |  folder: /15-SEO-search  |  cards: 19  |  words: 5668  |  type: transcript (YouTube tutorial video)

credibility: The presenter runs an SEO practice with paying clients (references "a client of mine took a hit from a Google algorithm update" and "the number I put in front of my clients every month"), and hosts or is affiliated with the "Surfer Academy" YouTube channel. The video is also a promotional vehicle for Surfer SEO's paid product ("Positive Surfer") and its sister social tool "Icon Square": almost every workflow that goes beyond native Google Search Console (GSC) ends with "and here's how Surfer does this for you automatically." Evidence offered is: 2 first-hand client/practitioner examples with real numbers (an algorithm-drop diagnosis, a blog post's query data), general practitioner experience narrating GSC's UI, and unverified claims about Google's roadmap and intentions. No formal studies or aggregated data are cited. Treat all Surfer-specific claims (thresholds, feature names, "AI magnets" terminology) as one vendor's product description, not GSC documentation.

date signals: Title says "(2026)". Presenter states Google shipped the generative AI performance report in June 2026 (beta). Platform properties (social accounts as GSC properties) were "announced by Google in July 2026" and rolling out gradually, none active yet in presenter's own accounts. An AI-Overviews opt-out toggle "started with UK site owners and is now rolling out globally." A client "took a hit from a Google algorithm update earlier this year" (i.e., earlier in 2026, undated). Presenter frames "the last 2 years" as when clicks-falling-despite-stable-rankings became common, implying a mid-2024-to-2026 trend tied to AI Overviews. Because GSC's UI and Google's AI features change quickly, every navigation path below is tagged `[verify UI]` and every claim about how Google actually behaves is tagged `[web check]`.

## 1. What this source is for

A scenario-driven walkthrough of Google Search Console for people who have GSC installed but have "only glanced at the clicks graph." It covers: setting up and verifying a property, reading overall organic performance and proving it to leadership, diagnosing why a specific page is not indexed, using GSC as a free rank tracker, finding the pages behind a traffic drop, retargeting a page to the keyword it actually earns clicks for, mining question queries for content ideas, pulling backlink and internal-link data for free, fixing video indexing, and reading Google's new generative AI (AI Overviews / AI mode) visibility report. It is not a UI tour and not a Surfer setup guide (the source itself flags both as skipped).

## 2. Principles

1. Use the Domain property type, not URL-prefix, when setting up GSC for a store. Condition: any new property, or migrating off a URL-prefix property that only covers one subdomain/protocol. Evidence: presenter's description of Domain covering every subdomain (shop., blog., checkout.), www/non-www, HTTP/HTTPS. Trade-off stated: Domain requires DNS verification, URL-prefix does not. [02f0df47b84c]
2. Raw click totals overstate what content "earned" because they blend branded and non-branded demand. Condition: any time clicks are used as a KPI or reported to leadership. Evidence: presenter's stated reasoning, not a measured split. [f754914adaba] [ab49d7297c19]
3. "Not indexed" does not mean "error." Condition: reading the Pages report under Indexing. Evidence: presenter lists deliberate ecommerce exclusions (ad landing pages, thank-you/confirmation pages, internal search results, filtered category pages, staging/test pages) and gives the litmus test: "do I want people to find this content on Google?" If no, exclusion is correct. [2d733fe615435]
4. Average position is an average across every impression, location, and device, so it is a trend line, not a pinpoint rank. Condition: any use of the position metric, whether page-level or query-level. [f754914adaba] [0363a4df755b]
5. Low-volume keywords bounce; small position swings on them are noise. Example given: a 2-position wobble on a keyword with roughly 40 impressions should not cause alarm. This is a single illustrative example, not a stated statistical threshold. [0363a4df755b]
6. Branded queries sit at position 1 nearly all the time and reveal almost nothing about competitive standing, but branded search volume itself is argued to be an increasingly important separate signal because buyers may discuss purchases with AI assistants first and then Google the brand name before buying. This "AI-era branded search matters more" claim is the presenter's interpretation, not a measured benchmark. [0363a4df755b] [dd8f0c00b989]
7. Google indexes a video only when the video is "the main event" of a dedicated page (a "watch page"), modeled on a YouTube-style layout: video front and center, above the fold. A page can still rank normally with an embedded video; what is lost is video results, thumbnails, and the video search tab. [5bde395c6a3b]
8. Structured, direct question-and-answer content is favored both by users (it converts passing mentions into content people can find) and, per the presenter, by AI Overviews ("AI magnets"). This pattern is asserted, not measured against a control. [ad660f81d67a] [178afbabc0bc]
9. Losing a click to an AI Overview does not necessarily mean losing the sale; the presenter frames this as still "winning attention." This is opinion, offered without supporting data. [cc309b3d5cf7] [178afbabc0bc]
10. GSC retains a maximum of 16 months of performance history. Condition: any trend analysis or property migration; export older data before it ages out. [02f0df47b84c] [f754914adaba] [0363a4df755b]

## 3. Procedures

### A. Set up and verify a Domain property `[verify UI]`
1. Open the property dropdown, click "add property."
2. Choose Domain (not URL prefix). Domain covers every subdomain, www/non-www, HTTP/HTTPS.
3. Type the domain, hit continue. Google returns a TXT record.
4. Copy the TXT record; sign into the domain registrar (GoDaddy, Namecheap, Cloudflare, etc.) or hand it to a webmaster, and paste it into DNS settings.
5. If verification fails immediately, click "verify later" and retry the next day, since DNS propagation can take time.
6. Once verified, let the dashboard populate, then connect the property to any reporting tools already in use. [02f0df47b84c]

### B. Read overall performance with compare mode `[verify UI]`
1. Go to Performance > Search results.
2. Set the date range (options run 24 hours to 16 months).
3. Toggle the 4 metrics: total clicks, total impressions, average CTR, average position.
4. Click Compare; set last 3 months vs previous period (use 6 months vs previous when investigating a specific drop).
5. Read the top chart for growth/decline, the Queries tab for what people type, the Pages tab for which URLs carry the traffic.
6. If clicks are up period-over-period, current activity is working; if down, proceed to the traffic-drop procedure (D). [f754914adaba]

### C. Isolate non-branded clicks with custom regex `[verify UI]`
1. In Performance, add a query filter.
2. Switch match type to Custom regex.
3. Choose "doesn't match."
4. Enter brand terms separated by the pipe symbol `|` (regex OR), e.g. `brandname|brand name|brandname com`.
5. Review the filtered query list to confirm no legitimate non-branded terms were accidentally excluded by an overly broad pattern.
6. Layer Compare mode on top: non-branded clicks, last 3 months vs previous period, to show earned-content growth or decline. [ab49d7297c19]

### D. Diagnose a single page's indexation status `[verify UI]`
1. Paste the page URL into the URL Inspection bar at the top.
2. Read the reported status: indexed, last crawl date, and what is blocking it if anything.
3. If "URL is not on Google," read the specific reason given underneath (do not guess).
4. If the reason is "Discovered - currently not indexed": Google knows the page exists but hasn't crawled it. Common on new sites. Add internal links from stronger pages to speed this up.
5. If the reason is "Crawled - currently not indexed": Google read the page and passed, usually a content-quality or thinness signal. Strengthen the page before requesting recrawl. Caveat: on newer/smaller sites this status can reflect the whole site's authority rather than the page; the fix may be patience and site-wide authority building, not repeated rewrites.
6. Once the underlying issue is fixed (or if there was never one), click "Request Indexing." This is quota-limited per day, not instantaneous, and not guaranteed, but faster than waiting for organic recrawl. [b90f727119e2]

### E. Audit site-level not-indexed pages by reason `[verify UI]`
1. Open Indexing > Pages in the sidebar to see every not-indexed URL grouped by exclusion reason.
2. Apply the litmus test per group: "Do I want people to find this content on Google?" If yes, it should not sit under "excluded by noindex tag" or "blocked by robots.txt."
3. Confirm intentional exclusions: ad landing pages (protects ad tracking from organic contamination), thank-you/confirmation pages, internal search results, filtered category pages, staging/test pages.
4. Look specifically for accidental exclusions: staging pages that slipped through robots.txt before launch, or money pages accidentally noindexed.
5. Fix only the unintended exclusions; leave deliberate ones alone. [2d733fe615435]

### F. Track a page or keyword as a free rank tracker `[verify UI]`
1. In Performance, add a filter, choose Page, paste the exact URL.
2. Turn on average position; the chart becomes that page's ranking history (up to 16 months).
3. To track one keyword instead, filter by Query, switch to "Exact query," so one term = one line on the chart.
4. Add Compare mode: average position over last 3 months vs previous 3 months for a hard delta.
5. Prioritize tracking non-branded queries; branded terms sit at position 1 and show nothing about competitive movement. [0363a4df755b]

### G. Find the pages behind a traffic drop `[verify UI]`
1. Set the comparison window to cover the drop (example given: last 6 months vs previous period).
2. Sort the table by click difference, ascending, so the biggest losers float to the top.
3. Inspect what the losing pages have in common: same topic cluster, same page type, thin content, or pages cannibalizing each other.
4. If no pattern is obvious, consider that the SERP itself changed: users may now want more depth, a different format, or query intent may have shifted.
5. Fix the identified cause on the affected pages, prioritizing the largest click losses first. [c879262f60c4]

### H. Retarget a page using its own query data `[verify UI]`
1. Filter Performance by the page's URL; open the Queries tab.
2. Compare the page's intended target keyword against the actual click leaders in that tab.
3. Rewrite the title tag and H1 around the keyword with demonstrated click demand.
4. Read the pages currently ranking for that keyword to see what the page is missing: terms covered, headings, questions answered, depth.
5. After publishing changes, use URL Inspection to request a recrawl. [96052232339a]

### I. Mine question queries for FAQ and content ideas `[verify UI]`
1. In Performance, add a query filter, switch to Custom regex.
2. Match question words: who, what, when, where, why, how, can, does (adjust the pattern for other languages/phrasings; the source only lists English terms).
3. Review returned queries; for each, ask whether any existing page answers it directly.
4. Where no page answers it directly, the site is ranking on a passing mention only. Add an FAQ section to the relevant page, or write a dedicated page if the topic warrants it. [ad660f81d67a]

### J. Get backlink and internal-link data from GSC `[verify UI]`
1. Click Links in the sidebar.
2. Read most-linked pages, internal link counts, and referring sites, at no cost.
3. Click into any page to see the exact sites linking to it.
4. Identify high-authority pages (most internally and externally linked).
5. Point internal links from those authority pages at newer or strategic pages you want to rank (e.g. launch pages, priority categories). [00909ce99f85]

### K. Fix video indexing with dedicated watch pages `[verify UI]`
1. Open the Videos report under Indexing to see which indexed pages contain videos Google indexed, and the stated reason for ones it did not.
2. If the reason is "video isn't on a watch page," apply the rule: the video must be the main event of the page.
3. Move top-performing videos off mid-post embeds, sidebars, or small players onto a dedicated page modeled on a YouTube watch page (video front and center, above the fold).
4. Leave embeds that serve readers in place if a dedicated page is not warranted, but accept the page will rank normally without earning video results, thumbnails, or the video search tab. [5bde395c6a3b]

### L. Read Discover and Google News reports `[verify UI]`
1. Open the Discover report. There are no queries (Discover is interest-based push, not search), so you get pages and impressions only.
2. Open the Google News report, which works the same way.
3. If content skews timely, visual, or list-driven, treat Discover/News as a channel that can outdraw classic search and is visible only in these reports.
4. Use page-level performance to decide which content formats to repeat. [b978f1f1601a]

### M. Diagnose falling clicks with stable rankings `[verify UI]`
1. Compare CTR against position for the affected pages over time.
2. If a page holds its position (example: position 3) but CTR has shrunk for months, 2 explanations are offered: (a) title/meta description have gone stale while competitors' improved — an easy snippet rewrite; or (b) something now sits above the result answering the query before a scroll, most likely an AI Overview.
3. Open the generative AI performance report and check the specific losing pages: heavy AI impressions on those pages indicate content is being read inside Google's AI answer instead of driving a site click.
4. If it's a snippet problem, rewrite title/meta description. If it's an AI-answer problem, treat that content as an "AI magnet" and produce more structured, direct answers on adjacent buyer topics. [cc309b3d5cf7]

### N. Read the generative AI performance report `[verify UI]` `[web check: has this report added click/position data since its June 2026 beta]`
1. Open the generative AI performance report (beta as of the source date); confirm it has rolled out to the property.
2. Read impressions: how many times a link to the site appeared inside an AI feature, broken down by page, country, device. No click or position data at time of recording; presenter states Google says these are "coming later" — unverified.
3. Sort by impressions, study top pages to see what the AI already surfaces from the site.
4. Apply the same structure/directness pattern to other buyer topics.
5. Before using Google's AI-Overviews opt-out toggle (rolling out from UK outward), use this report to see exactly how much AI visibility would be given up, page by page. Presenter does not recommend opting out. [178afbabc0bc]

### O. Build a content plan from exported query data
1. In Performance, export all queries to a spreadsheet (interface allows up to 1,000 rows).
2. Provide the list to an AI assistant (e.g. Claude or ChatGPT — named generically by the presenter) together with the site's sitemap.xml.
3. Ask the assistant to identify gaps: queries the site already surfaces for that no page properly covers.
4. Turn each gap into an FAQ section on an existing page or a new page, depending on topic weight.
5. Validate the AI's suggested gaps for real demand and difficulty before committing production time (source's own caveat). [d2808d386582]

### P. Add social accounts as Search Console properties `[verify UI]` `[web check: platform properties general availability]`
1. Add Instagram, TikTok, X, or YouTube accounts as their own GSC properties via the "platform properties" feature (rolling out gradually; presenter had access to none at recording time).
2. Once available, view which search terms lead people to posts and how those posts perform in Google Search and Discover, even for accounts with no attached website.
3. Pair with a social analytics tool to see performance outside Google search/discover. [e1582b8051f0]

## 4. Rules, thresholds and numbers

| Rule | Number / threshold | Condition | Source's basis | Card id |
|---|---|---|---|---|
| GSC history retention | 16 months max | Any trend or migration | Presenter's stated platform limit `[web check]` | 02f0df47b84c |
| Performance date range | 24 hours to 16 months selectable | Performance > Search results `[verify UI]` | Presenter's UI description | f754914adaba |
| Query export cap | 1,000 rows | Exporting Performance queries | Presenter's stated UI limit `[web check]` | d2808d386582 |
| Regex OR operator | Pipe symbol `\|` | Custom regex filters (brand exclusion, question-word matching) | Presenter's regex usage | ab49d7297c19, ad660f81d67a |
| Low-volume noise example | ~40 impressions, 2-position wobble = noise, not signal | Single-keyword rank tracking | One illustrative example, not a formula | 0363a4df755b |
| Content-refresh candidate band (3rd-party tool heuristic) | Positions 6-8 | Tool-based rank monitoring (Surfer, per presenter) | Vendor feature description, not native GSC | 7a8b4ae0cd5c |
| Ranking-drop alert window (3rd-party tool heuristic) | 7-day stretch | Tool-based rank monitoring | Vendor feature description | 7a8b4ae0cd5c |
| Comparison window, general reporting | Last 3 months vs previous period | Monthly/quarterly organic reporting | Presenter's recommended default | f754914adaba, ab49d7297c19 |
| Comparison window, traffic-drop investigation | Last 6 months vs previous period | Diagnosing an algorithm-hit or unclear drop | Presenter's client example | c879262f60c4 |
| Worked example: keyword retargeting clicks | "is beeswax good for your skin" = 3 clicks vs "benefits of beeswax for skin" = 19 clicks, both over 3 months | Single blog post, single client, single time window | One case example, not a benchmark | 96052232339a |
| Request Indexing quota | Daily quota exists; exact number not stated | Requesting recrawl via URL Inspection | Presenter mentions the quota without a figure `[web check]` | b90f727119e2 |
| Generative AI report launch | Shipped beta, June 2026 | Reading AI visibility | Presenter's stated timeline `[web check]` | 178afbabc0bc |
| Platform properties announcement | Announced July 2026, gradual rollout | Adding social accounts as properties | Presenter's stated timeline `[web check]` | e1582b8051f0 |
| AI Overviews opt-out toggle rollout | Started with UK site owners, expanding globally | Deciding whether to exclude content from AI features | Presenter's stated rollout status `[web check]` | 178afbabc0bc |

## 5. Diagnostics and checks

| What to check | How | Good | Bad / next step |
|---|---|---|---|
| Is overall organic traffic growing? | Performance > Search results, Compare last 3 months vs previous `[verify UI]` | Clicks up period-over-period | Clicks down: proceed to click-difference sort (traffic-drop check below) [f754914adaba] |
| Is a specific page actually not indexed, and why? | URL Inspection bar with the exact page URL `[verify UI]` | "URL is on Google" | "Discovered - currently not indexed" -> add internal links, wait; "Crawled - currently not indexed" -> strengthen content, or if new/small site, build overall site authority and be patient [b90f727119e2] |
| Are site-wide exclusions intentional? | Indexing > Pages, grouped by reason `[verify UI]` | Excluded pages are ad landing pages, thank-you pages, internal search, filtered categories, staging | Money pages or category pages appear under noindex/robots.txt unintentionally -> fix the tag/rule [2d733fe615435] |
| Which pages caused a traffic drop? | Sort comparison table by click difference, ascending (6mo vs previous) `[verify UI]` | Losses cluster in one identifiable group (topic, page type, thin content, cannibalization) | No shared pattern -> consider SERP/intent shift, hand off to content-gap analysis [c879262f60c4] |
| Is a page's keyword targeting correct? | Filter Performance by page URL, open Queries tab `[verify UI]` | Title/H1 keyword matches the query producing the most clicks | Click leader query differs from targeted keyword -> retarget title/H1 to the click leader [96052232339a] |
| Are there unanswered questions the site already surfaces for? | Query filter, Custom regex matching question words `[verify UI]` | Every returned question has a page that answers it directly | Question has no direct-answer page -> add FAQ section or new page [ad660f81d67a] |
| Which pages hold the most link authority? | Links report in sidebar `[verify UI]` | High-authority pages identified and already linking to priority pages | High-authority pages are NOT linking to newer/strategic pages -> add internal links from them [00909ce99f85] |
| Why isn't a video showing in video results? | Videos report under Indexing `[verify UI]` | Video's page is a dedicated watch page, video is indexed | Reason given is "video isn't on a watch page" -> move video to a dedicated, above-the-fold page [5bde395c6a3b] |
| Why are clicks falling while rank holds steady? | Compare CTR vs position over time on affected pages `[verify UI]` | CTR stable relative to position | CTR shrinking at stable position -> check title/meta staleness vs competitors, then check generative AI report for heavy AI impressions on those pages [cc309b3d5cf7] |
| Is content being consumed inside AI answers instead of driving clicks? | Generative AI performance report, sorted by impressions, cross-checked against pages losing clicks `[verify UI]` `[web check]` | Low AI impression overlap with clicks-lost pages | Heavy AI impression overlap -> treat as AI magnet, replicate structure on adjacent topics; consider whether losing the click still wins the sale [178afbabc0bc] |

## 6. Tools, settings and named features

- Google Search Console sections named: Overview, Insights (plain-English summary), URL Inspection bar, Performance (Search results, Discover, Google News, generative AI report), Indexing (Pages, Video, Sitemaps, a removal tool), Experience (Core Web Vitals, HTTPS), Shopping/Enhancements (for ecommerce product markup rich-result eligibility), Security & Manual Actions, Links, Settings (user access, crawl reports). `[verify UI]`
- Compare mode: period-over-period overlay on any Performance chart. `[verify UI]`
- Custom regex query filter: "matches" / "doesn't match" operators, pipe `|` for OR. `[verify UI]`
- Request Indexing: manual recrawl request from URL Inspection, daily-quota limited. `[verify UI]`
- Platform properties: adding social accounts (Instagram, TikTok, X, YouTube) as GSC properties. New, gradual rollout as of the source date. `[verify UI]` `[web check]`
- Generative AI performance report: beta AI Overviews/AI mode impressions report, by page/country/device. `[verify UI]` `[web check]`
- AI Overviews opt-out toggle: pulls content out of AI Overviews/AI mode without affecting normal rankings. `[verify UI]` `[web check]`
- Third-party (not GSC, vendor-specific, mentioned throughout as the presenter's own product): Surfer / "Positive Surfer" — content editor (keyword gap scoring against competitors), content audit (auto ranking monitoring, refresh flags), recommendations tab (topic clustering, opportunity scoring by search volume/difficulty/competitor coverage), internal linking tool, AI tracker (cross-model brand/citation tracking). Icon Square — sister tool for social analytics. These are vendor features layered on top of GSC data, not native GSC capability. `[verify UI]`

## 7. Examples and case results

- Client hit by a Google algorithm update earlier in 2026: presenter used a 6-months-vs-previous comparison, sorted by click difference ascending, to find the exact pages that lost the most traffic, then looked for shared traits (topic cluster, page type, thin content, cannibalization). No recovery outcome or numbers given; this is a diagnostic method example only. [c879262f60c4]
- Beeswax-for-skin blog post (a previous client's page): targeted keyword "is beeswax good for your skin" produced about 3 clicks in 3 months; the actual click leader, "benefits of beeswax for skin," produced 19 clicks in the same window. Used as the basis for retargeting the title/H1. Single case, not a benchmark. [96052232339a]

## 8. Mistakes the source warns about

- Reporting raw clicks as proof of content/SEO performance without stripping out branded search. [f754914adaba] [ab49d7297c19]
- Assuming every "not indexed" URL is a problem to fix, instead of checking whether the exclusion was intentional (ad pages, thank-you pages, staging, filtered categories). [2d733fe615435]
- Repeatedly rewriting a page stuck at "crawled - currently not indexed" on a new/small site when the real blocker is site-wide authority, not that specific page. [b90f727119e2]
- Reacting to small position swings on low-volume keywords as if they were meaningful signal. [0363a4df755b]
- Treating branded keyword position (usually 1) as a sign of ranking strength. [0363a4df755b]
- Leaving important videos embedded mid-post, in a sidebar, or sized small, then expecting video search results, thumbnails, or a video-tab placement. [5bde395c6a3b]
- Assuming a click drop means a ranking drop, when CTR-vs-position analysis and the generative AI report may show the real cause is an AI Overview or a stale snippet. [cc309b3d5cf7]
- Opting out of AI Overviews without first checking the generative AI report to see how much visibility would be lost, page by page (the presenter does not recommend opting out at all). [178afbabc0bc]
- Trusting AI-bot server-log hits as evidence of AI recommendation; a crawl is not a citation, a citation means the model used the page. [05e68a491915]

## 9. Caveats, conflicts and what is missing

- Strong vendor bias: nearly every workflow beyond native GSC funnels into a Surfer (Positive Surfer) product feature (content editor, content audit, recommendations tab, internal linking tool, AI tracker) or its sister tool Icon Square. Numbers presented as "the" refresh band (positions 6-8) or "the" drop-alert window (7 days) are that vendor's tool heuristics, not documented Google Search Console behavior or an industry-wide standard. Treat these as one tool's configuration, to be verified in whichever tool is actually used. [7a8b4ae0cd5c]
- The generative AI performance report is explicitly beta at time of recording: impressions only, no click or position data, and Google's promise of adding those later is relayed by the presenter, not confirmed independently. `[web check: current state of GSC's generative AI performance report]` [178afbabc0bc]
- Platform properties (social accounts as GSC properties) had not reached the presenter's own accounts at recording time; rollout status is unverified beyond "gradual." `[web check: platform properties availability]` [e1582b8051f0]
- The AI Overviews opt-out toggle's rollout ("UK first, expanding globally") is stated but not verified as complete; check current availability before advising a client to use it. `[web check]` [178afbabc0bc]
- No exact Request Indexing daily quota number is given, only that one exists. `[web check: current GSC Request Indexing quota]` [b90f727119e2]
- The source explicitly skips: general GSC dashboard-navigation tours and Surfer's own signup/configuration walkthroughs (per the routing header, not part of this transcript).
- No conflict found with common ecommerce SEO advice; the source's ecommerce-specific guidance (noindex ad landing pages and thank-you pages to protect ad tracking, use Domain property to cover checkout/shop subdomains) matches standard practice rather than contradicting it.
- The source gives no numeric backlink-count or domain-authority-equivalent benchmarks; the Links report guidance is qualitative ("identify high-authority pages") with no threshold for what counts as high authority. This is a stated gap, not an omission by this playbook.
- AEO/AI-visibility content here overlaps with the 16-AEO-answer-and-generative-engines folder; this source covers only the GSC-native angle (generative AI performance report) plus a pointer to a cross-model brand tracker as a named category, without naming or evaluating specific cross-model tools beyond Surfer's own "AI tracker."

## 10. Card index

- 02f0df47b84c — Set Up a Domain Property in Google Search Console
- f754914adaba — Read Overall Search Performance With Compare Mode
- ab49d7297c19 — Isolate Non-Branded Clicks With Custom Regex
- b90f727119e2 — Diagnose Indexation Status With URL Inspection
- 2d733fe61543 — Audit Site-Level Not-Indexed Pages by Reason
- 0363a4df755b — Track a Specific Page or Keyword Without a Paid Rank Tracker
- c879262f60c4 — Find the Pages Behind a Traffic Drop
- 96052232339a — Re-Target a Page Using Its Own Query Data
- ad660f81d67a — Mine Question Queries for FAQ and Content Ideas
- 00909ce99f85 — Get Backlink and Internal Link Data Free From Search Console
- 5bde395c6a3b — Fix Video Indexing by Building Dedicated Watch Pages
- b978f1f1601a — Use the Discover and Google News Reports for Non-Query Traffic
- cc309b3d5cf7 — Diagnose Falling Clicks With Stable Rankings
- 178afbabc0bc — Read the Generative AI Performance Report for AEO Benchmarks
- d2808d386582 — Build a Content Plan From Exported Query Data
- 7a8b4ae0cd5c — Track Rankings Automatically and Flag Refresh Candidates
- dd8f0c00b989 — Split Branded From Non-Branded in Ongoing Reporting
- e1582b8051f0 — Add Social Accounts as Search Console Properties
- 05e68a491915 — Map AI Visibility Beyond Google With a Brand Tracker
