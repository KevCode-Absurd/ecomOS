# Claude Code Full Content Automation

source_id: 1Dc0poVswXSgqBVZqS9PWVsgiOhw4Ageo  |  folder: 15-SEO-search  |  cards: 14  |  words: 3,436  |  type: YouTube-style video transcript (informal talk, promotional/affiliate)

credibility: Unnamed presenter, spoken transcript with filler words ("uh," "um") and visual references that do not survive as text (charts, screen recordings of "hockey stick growth" are described but never quantified in words). The presenter promotes two named third-party tools, Arvo and a scheduling tool referred to inconsistently across the transcript as "Blotado," "Blowado," "Blowto," "Plotato," and "BLT" (almost certainly transcription variants of one product, likely "Blotato" `[web check: exact product name and current features]`). The presenter offers to send "the prompt" only if viewers "type prompt below" — a lead-generation tactic, and it means the source's own core artifact (the actual automation prompt) is not reproduced in this transcript. Evidence offered: "real results," client traffic growth, and AI-overview appearance, all described visually ("you can see they're getting a ton of AI overviews") with no numbers, no client names, and no before/after data stated in words. The presenter states personal daily use ("I use this every single day for multiple brands") as the only concrete credibility claim. Treat this whole source as one operator's opinion and workflow sketch, not a benchmarked method. `[web check: presenter identity, if attribution matters]`

date signals: No dates, version numbers, or prices are stated anywhere in this transcript (unlike other sources in this library that give exact tool prices). It references Claude Code as an installable coding agent run from a local code editor (Visual Studio Code), and Arvo and a scheduling tool as SaaS products with API integrations, plus "AI overviews" in Google search and citation in ChatGPT and Perplexity — this places it in the same AI-search/AEO era as the rest of folder 16, roughly 2025-2026. All tool UI, tool names, and API steps described below should be treated as likely stale within months. `[web check: current Claude Code, Arvo, and scheduling-tool interfaces and names]`

## 1. What this source is for

A high-level sketch of an end-to-end AI content pipeline: use Claude Code as an orchestration agent that (a) researches bottom-of-funnel keyword opportunities from competitor gaps, (b) sends approved blog concepts via API to a specialized SEO writing tool (Arvo) that handles on-page SEO and CMS publishing, and (c) repurposes the resulting blog RSS feed into scheduled social posts and auto-generated infographics via a second tool (the scheduling tool). It also covers monitoring brand visibility inside AI/LLM answers (AEO) with an "LLM brand monitor" feature. It is a workflow map and a sales pitch for two named tools, not a hands-on technical manual — most exact commands, prompts, and menu paths are not given.

## 2. Principles

1. Target bottom-of-funnel, high-search-intent keywords over broad top-of-funnel terms, because conversion potential is what should drive content investment, not raw traffic volume. Condition: applies when choosing which keyword/topic to write about first. Evidence: presenter's directional example only — "running shoes" (top of funnel, no brand/style/function decided, low buying intent) versus "running shoes for men over 50 with sore backs" (bottom of funnel, near-term buying decision). No data on relative conversion rates is given. [00ce29e0773866f28f31f36b]
2. Close the loop between content and money pages in both directions: every published article should link back to money/service pages, and money/service pages should link out to best-performing articles. Condition: applies to site architecture whenever bottom-of-funnel articles are published. Evidence: presenter's own described loop; no click-through or conversion data given. [d03002241ed37acc19c3616e]
3. Run the AI agent from a local, native environment (a code editor on your own computer) rather than through a plain web chat interface, so brand assets and generated output are saved on your machine and reusable across sessions instead of "going externally." Condition: applies to any AI-assisted content workflow meant to compound over time. Evidence: presenter's own stated preference; no comparison data against cloud-only workflows. [ab48255e465e611dd35682e9]
4. Build reusable "skills" once (a blog skill, a social skill) through a longer setup prompt, then trigger repeat work with short instructions that reference the stored skill. Condition: applies once you expect to repeat the same kind of content task weekly. Evidence: presenter's own described pattern; no data on time saved. [09eb0afacdd25708f535b0db]
5. Run competitive gap analysis before generating any titles, so title/keyword choices target either an unmet gap or something a competitor is already succeeding with (to duplicate). Condition: applies at the start of a content-planning cycle. Evidence: presenter's own workflow description; no scoring method or data source is given for what counts as a "gap." [39046caefd1f3c5e55a3cbf8]
6. Hand off approved title/keyword concepts to a specialized SEO-writing tool rather than having the general agent (Claude) write and then manually add SEO elements. Condition: applies once titles/keywords are approved and ready for drafting. Evidence: presenter states "Claude, sure, Claude could write really good articles, but then you're going to have to basically edit them and include all the back-end SEO" — this is the presenter's own comparison, not tested output from both paths. [095649605d128d8a11ca16ca]
7. Wire tools together with API keys so approved work flows without manual copy-paste: one integration lets the agent send generations to the SEO tool, a second lets the SEO tool push to the website/CMS. Condition: applies once you are ready to automate delivery, not just generation. Evidence: presenter's own setup description; exact menu steps are generic ("go into integrations... hit API") and not tool-specific. [f3eff0cd77a45f2de661600d]
8. Repurpose the blog's own RSS feed into social content instead of researching social topics separately, so social posts reuse the same bottom-of-funnel research and drive traffic back into the same loop (blog to money page to social to blog). Condition: applies once a blog is publishing on a regular cadence. Evidence: presenter's own described pipeline; no post-performance data given. [845f4874cb616d2d8e8a7e40]
9. Automate social scheduling by API, with defined time slots per channel, and let the agent place approved posts into the next open slot or a specified time. Condition: applies once social captions/images are already approved. Evidence: presenter's own daily personal use across "multiple brands"; no controlled test of posting cadence. [d7c89b8565dc156e9c94d98e]
10. Keep a human-approval gate between each automated stage (title list before generation, generated article before publish, social caption before scheduling) rather than running the whole pipeline hands-off, even though full automation is technically possible. Condition: the presenter's own personal default is to draft rather than auto-publish. Evidence: "I usually send it to my website as a draft and then I go in and just schedule and publish it. But you never really need to even go to Arvo." [6e4f81398cf7963239d1f89a]
11. Layer multiple specialized AI tools rather than relying on one general tool for everything: a general agent for orchestration and research, a specialized SEO writer for on-page structure and brand-aligned copy, and a scheduler for cross-channel distribution and image generation. Condition: presenter's own architectural opinion. Evidence: "when you piggyback AIS on top of one another with this workflow, this is what makes this really, really powerful" — an unverified claim about why results occur. [b422877d7c387c1427a3b1a1]
12. Structure articles for AI-overview and LLM pickup: clear H2/H3 hierarchy, focus keyword, meta description, image alt text, a call to action, internal and external links, and an embedded relevant video. Condition: applies when configuring the SEO-writing tool's formatting options. Evidence: presenter states these settings are "perfect for AI overviews" and should be left on — an assertion, not measured before/after data. [10f5ad7136799724d786ecab]
13. Monitor AI/LLM visibility (AEO) separately from traditional rank tracking, using long-tail keyword inputs into an "LLM brand monitor" feature to check visibility, sentiment, and cross-platform ranking across ChatGPT and Perplexity. Condition: applies to measuring whether content strategy is producing AI citations, not just search rankings. Evidence: presenter's own tool demo; no baseline/after numbers given in words. [b099c3b284763f67260dbec3]
14. Auto-generate on-brand infographics from the same content pipeline and schedule them alongside written social posts, using either your own uploaded brand images or the tool's generated visuals and templates. Condition: applies once visual social content is wanted without a dedicated designer. Evidence: presenter's own demo ("create a trail-marker infographic"); no engagement data. [03ac780b7ba97b7e24b8304e]

## 3. Procedures

### A. Set up the local environment for Claude Code
1. Download Visual Studio Code (stated as free) so Claude Code runs natively on your own computer instead of through the web chat, keeping assets local rather than external. `[verify UI]`
2. In the editor, go to the apps/extensions area and search for "Claude." Click it. `[verify UI]`
3. Open the resulting window (the source notes it "looks the same as it would look on your computer on a website" but assets now save locally). Close the initial popup window if one appears. `[verify UI]`
4. At the top of the screen, use File > Open Folder. First create a dedicated folder on your desktop (worked example names given by the presenter: "clawed AI workflow" or "clawed SEO" — read as "Claude AI workflow" / "Claude SEO," transcription artifacts of "Claude"). Open that folder. `[verify UI]`
5. This creates a working folder of assets on your computer that the agent continues to update, pull from, and save into — store brand photos and other brand assets here so Claude can reference them when building content.
Gap: the source does not give the exact current menu labels, so treat every click path above as approximate and confirm against the live interface before following it. `[verify UI]`

### B. Build the automation using a setup prompt (prompt text itself not given)
1. The source states there is a prompt that you copy and paste into Claude to build out "skills" (a blog skill, a social media skill) that can be referenced later with short instructions (e.g., "plan my week's worth of content for blogs"). **The prompt's exact text is not included in this transcript** — the presenter only says "type prompt below" to receive it separately. Do not invent this prompt; treat it as a gap. `[needs brand data: the actual setup prompt, if it exists in the linked lead magnet]`
2. Before running the prompt, edit it to include your own business information — the source states this is the first thing the prompt asks for. `[needs brand data: business information — name, offerings, positioning, target customer]`
3. Claude will ask clarifying questions and request approval as it builds each skill; answer and approve to shape what the skill does.

### C. Research and title generation (inside the Claude Code workflow)
1. Have the agent analyze your local competition, per the built-in step in the prompt.
2. From that analysis, extract two outputs: gaps in the market (unaddressed opportunities) and things competitors are already doing well (candidates to duplicate). `[needs brand data: list of actual competitors / local market]`
3. Generate blog titles, each paired with one primary keyword, mapped to those gaps/opportunities, biased toward bottom-of-funnel, high-intent topics (see Principle 1).
4. Review and approve the list of title-plus-keyword concepts before anything is sent onward for generation (approval gate — see Principle 10).

### D. Configure and connect the SEO-writing tool (Arvo, per this source)
1. In the SEO tool, open its knowledge base setting and include your website so generated articles align with your brand and offerings. `[needs brand data: live website URL/content] [verify UI]`
2. In formatting/structure settings, enable structure, calls to action, and any "AI overview"-oriented options, and leave them on. `[verify UI]`
3. In internal linking settings, include your sitemap so generated articles automatically link to your other pages and your money pages. `[needs brand data: sitemap, list of money/service pages] [verify UI]`
4. Confirm external linking is set to point to trusted outside sources (the tool does this automatically per the source).
5. For images: upload your own images/brand assets, or let the tool generate them. `[needs brand data: product/brand photography if using real images]`
6. For video: supply your own YouTube video, or let the tool find a relevant one automatically.
7. In the SEO tool's integrations area, create an API integration to get an API key. `[verify UI]`
8. Give that API key to Claude Code so it can send generated blog opportunities to the SEO tool via API.
9. Create a second integration in the SEO tool linking to your website/CMS, so the SEO tool can push finished articles directly to the site. `[needs brand data: CMS/website connection details] [verify UI]`
10. Decide, per your own risk tolerance, whether generated articles land on your site as **drafts** (source author's own default — "I usually send it to my website as a draft and then I go in and just schedule and publish it") or publish automatically.

### E. Generate and review blog content
1. Once titles/keywords are approved, the agent sends them via API to the SEO tool, which generates full articles using the knowledge-base/formatting/linking configuration from procedure D.
2. Worked examples the presenter showed inside the SEO tool's editor: an article on lawn service, one on brakes, and one on "high protein diet for women over 40." Each showed, inside the editor: H2/H3 headings, a focus keyword field, a meta description field, image alt text, internal links (to the site's own pages), external links (to trusted sources), and an embedded relevant YouTube video.
3. Review the draft (do not assume it is ready to publish untouched — see Principle 10 and section 8).
4. Send to your site as a draft, then manually schedule and publish (source author's stated habit), or let the integration auto-publish if you have accepted that risk.

### F. Repurpose blog content into social media (the "bonus" workflow)
1. Curate the blog's RSS feed as the input for social content generation — this reuses the same bottom-of-funnel keyword research already done for the blog.
2. Have the agent create a dedicated social media skill (see procedure B) so caption/title generation stays consistent in format across channels (worked platforms named: Facebook, Instagram).
3. Review and approve generated captions/titles before anything is sent to the scheduling tool (approval gate).
4. Point social posts back to the blog articles and money pages to keep the loop going.

### G. Connect and configure the scheduling tool (referred to as Blotado/Blowado/Blotato — name unclear in transcript)
1. In the scheduling tool, get your API key and give it to the AI agent. `[verify UI] [web check: exact tool name and current API/setup flow]`
2. Decide which time slots you want to post in and which channels use which slots. Worked example given verbally: slots around "a 10, a three, a five" (read as roughly 10am, 3pm, 5pm) — exact meaning not fully clear in the transcript; treat as illustrative, not a rule. `[needs brand data: actual posting cadence/audience timing]`
3. Optionally restrict to one time slot per day per channel to avoid over-posting (source's own suggestion, not tied to data).
4. Once social content is approved, instruct the agent to place each post into the next available slot, or a specific time you name.
5. Confirm posts appear correctly on the scheduling tool's own calendar without manual entry — presenter demonstrates checking the calendar to confirm auto-scheduling worked.
6. For images: upload your own brand images, or let the agent/tool generate them. If it fits your brand, have Claude Code send an image prompt to the scheduling tool to create images or video. Worked example prompt given: "create a trail-marker infographic," referencing a template inside the scheduling tool's own template library. `[needs brand data: which infographic templates match your brand]`
7. The scheduling tool then both creates the asset and schedules it to post.

### H. Monitor AI/LLM visibility (AEO)
1. In the LLM brand monitor feature (Arvo, per this source), enter long-tail keyword searches relevant to your brand. `[needs brand data: which long-tail terms to monitor]`
2. Review reported visibility (whether/how you appear), sentiment (how you are described), and cross-platform ranking across LLM surfaces such as ChatGPT and Perplexity.
3. Use this as an ongoing measurement layer paired with the content workflow above, not a one-time check. `[web check: current LLM brand-monitoring feature set — this category of tool changes fast]`

## 4. Rules, thresholds and numbers

| Rule / setting | Number or threshold | Condition | Source's basis | Card id |
|---|---|---|---|---|
| Keyword targeting priority | Bottom-of-funnel over top-of-funnel (no numeric split given) | Choosing which topics to write first | Presenter's directional opinion, no data | 00ce29e0773866f28f31f36b |
| Social posting cadence | Example slots roughly "10, 3, 5" (times of day); optionally as low as 1 slot/day/channel | Setting up the scheduler | Presenter's own habit, not tested | d7c89b8565dc156e9c94d98e |
| Publish path | Draft-to-CMS then manual schedule (presenter's own default) vs. full auto-publish (technically possible, riskier) | Deciding how hands-off to go | Presenter's stated personal preference | 6e4f81398cf7963239d1f89a |
| Traffic/growth claims | "Zero traffic to an explosion in traffic," "hockey stick growth" | Presented as case evidence for 2+ unnamed companies | Visual chart shown on screen, no numbers stated in words — cannot be verified from this transcript | b422877d7c387c1427a3b1a1 |
| Worked example topics | Lawn service; brakes; "high protein diet for women over 40" | Demonstrating the SEO tool's output format | Presenter's live demo inside the tool | 095649605d128d8a11ca16ca |
| Cost claim | "Very very inexpensive" (no figure given) | Describing the scheduling tool | Presenter's opinion, no price stated | b422877d7c387c1427a3b1a1 |

Note: this source gives almost no hard numbers (no prices, no percentages, no traffic figures, no time-savings figures) despite making strong outcome claims. That gap is itself worth flagging when using this source to justify spend or timelines.

## 5. Diagnostics and checks

| What to check | How | Good | Bad | Next step |
|---|---|---|---|---|
| Is the content actually targeting bottom-of-funnel intent? | Read the generated title/keyword list before approving | Titles solve a specific, near-purchase problem (e.g., a named audience + named pain point) | Titles are broad/generic (e.g., a bare product category) | Reject and regenerate with a narrower angle; do not send broad titles to the SEO tool |
| Is the SEO tool's output actually SEO-complete? | Open the generated article in the tool's own editor | H2/H3 present, focus keyword set, meta description filled, image alt text present, internal + external links present | Any of these fields empty or generic | Do not publish; fix in the tool's config (knowledge base, formatting settings) before regenerating |
| Is the article aligned to brand voice/facts? | Human review of the draft before it leaves draft status | Matches known brand facts, offers, tone | Contains claims about the business that are not true, or a tone mismatch | Hold at draft; do not auto-publish (this is exactly the case the source's own draft-first habit exists for) |
| Is AI/LLM visibility actually improving? | Run the LLM brand monitor periodically with the same long-tail terms | Visibility, sentiment, and ranking trend up over successive checks | No movement, or negative sentiment appears | Revisit content targeting and structure (Principle 12); do not assume one check is enough — AI answers change often |
| Are social posts landing in the calendar as intended? | Check the scheduling tool's calendar after approval | Posts appear in the chosen slots without manual entry | Posts missing, duplicated, or in wrong slots | Re-check API connection and time-slot configuration before scaling volume |

## 6. Tools, settings and named features

- **Claude Code**: the general AI agent used for orchestration — research, competitive gap analysis, title/keyword generation, and triggering the other two tools via API. Run from a local code editor, not the web chat. `[verify UI]`
- **Visual Studio Code**: free code editor used to host Claude Code natively on the user's own computer so assets save locally. `[verify UI]`
- **Arvo**: named specialized SEO content-generation tool. Named features used: knowledge base (fed with your website), formatting/structure options (H2/H3, focus keyword, meta description, alt text, CTA), internal linking (via sitemap), external linking (to trusted sources), image handling (own or generated), YouTube embedding (own or auto-found), an "integrations" area for API key creation, and a separate **LLM brand monitor** feature (long-tail keyword input, visibility/sentiment/ranking output across ChatGPT and Perplexity). `[web check: current Arvo feature set and pricing]`
- **Scheduling tool** (name unclear in transcript — variants "Blotado," "Blowado," "Blowto," "Plotato," "BLT," likely "Blotato"): used for cross-channel social scheduling by API, time-slot configuration, calendar view, and template-based image/infographic/video generation. `[web check: confirm exact product name and current feature set]`
- **RSS feed**: used as the mechanical link between the blog (Arvo/CMS output) and the social-content generation step.
- **CMS/website integration**: a second API connection (separate from the Arvo API key) so generated articles can push to the live site, either as drafts or published directly.

## 7. Examples and case results

- Example (illustrative, not a controlled test): two unnamed companies shown on screen with "hockey stick growth" after adopting this strategy and tool stack; no traffic numbers, dates, or verification given in the transcript. Treat as anecdote.
- Example: AI-overview/citation appearance for unnamed clients, attributed by the presenter to "matching search intent better" — again shown visually, no numbers stated.
- Worked example topic 1: an article on lawn service, shown inside the SEO tool's editor to illustrate on-page SEO fields.
- Worked example topic 2: an article on brakes, same purpose.
- Worked example topic 3: "high protein diet for women over 40," walked through in the most detail — shown with H2/H3 structure, focus keyword, meta description, image with alt text, internal links, external links to trusted sources, and an embedded relevant YouTube video.
- Worked example: a "trail marker infographic" generated and scheduled via the scheduling tool's template library, as a demonstration of the visual-content step.
- Worked example: a content calendar screenshot showing posts already scheduled across time slots without manual entry, offered as proof the automation ran unattended.
- Presenter's personal-use claim: "I use this every single day for multiple brands" — a claim of habitual use, not a measured outcome.

## 8. Mistakes the source warns about

- Running Claude only from the web chat rather than a local, native setup — the source frames this as losing local asset storage and reuse ("we don't want to run Claude from Claude... you're not going externally and having your stuff external").
- Skipping the human-approval gates and going fully hands-off end to end — the source's own author does not do this; the author's real habit is: approve titles, draft (don't auto-publish) articles, approve social captions before scheduling. Fully automated publishing is described as possible but is not the author's own practice.
- Relying on Claude alone to both write and hand-do the "back-end SEO" (headings, meta description, alt text, internal/external links) — the source frames this as unnecessary manual rework once a dedicated SEO tool is wired in.
- Note: beyond these, the source gives few explicit "don't do X" warnings; most cautions above are inferred from what the presenter actually does (drafts, approvals) versus what is only described as technically possible (full auto-publish).

## 9. Caveats, conflicts and what is missing

- The core artifact the whole workflow depends on — the actual setup prompt fed into Claude Code — is not given in this transcript. The presenter states it is available only by request ("type prompt below"). Any reconstruction of that prompt would be invented and is out of scope for this playbook.
- The scheduling tool's name is inconsistent across the transcript (five different renderings). This mini playbook treats them as one product but this is an inference, not a stated fact. `[web check: exact product name]`
- No numeric results are stated anywhere in the transcript: no traffic percentages, no dollar figures, no time-to-result, no cost of either paid tool beyond "very very inexpensive" for the scheduler. Growth claims are illustrated with on-screen charts that do not transcribe into verifiable numbers.
- The presenter has a clear commercial interest in both named tools (affiliate-style links "below" the video for both Arvo and the scheduling tool), which is a source of bias this playbook cannot independently verify or discount.
- This source does not address ecomOS's own writing-quality bar. Everything generated by Arvo in this workflow (blog copy) and by the scheduling tool (social captions) would need a separate quality gate before use on a client-facing page or post: short sentences, simple words, digits for numbers, no em dashes, no inflated words, below tenth-grade reading level, concrete before-to-after benefits, and no invented claims. The source's own "AI-overview-friendly" formatting settings (Principle 12) optimize for machine extraction, not for this reading-level bar, and the two are not guaranteed to agree — this gap should be closed with a review/rewrite step inserted between "SEO tool generates draft" and "publish," on top of the source's own draft-first habit.
- The source does not say how the "gap analysis" step actually identifies gaps (no methodology, no keyword-volume/difficulty data source named) — treat Principle 5/Procedure C as a qualitative starting point only, and validate any resulting keyword with an actual keyword-research tool before committing content budget to it.
- No conflict with other ecomOS sources was found in this transcript's substance (bottom-of-funnel targeting and internal-linking loops are standard SEO practice); the conflict risk is entirely about unverified tool claims and the missing prompt, not about a competing SEO doctrine.

## 10. Card index

- 00ce29e0773866f28f31f36b — Bottom-of-Funnel Keyword Targeting for Content ROI
- d03002241ed37acc19c3616e — Internal Linking Loop Between Articles and Money Pages
- ab48255e465e611dd35682e9 — Set Up a Local Project Folder for AI Content Workflows
- 09eb0afacdd25708f535b0db — Build Reusable Skills to Standardize Content Planning
- 39046caefd1f3c5e55a3cbf8 — Automate Competitive Gap Analysis for Keyword Opportunities
- 095649605d128d8a11ca16ca — Use a Dedicated SEO Writer Tool for On-Page Optimization
- f3eff0cd77a45f2de661600d — Connect Content Tools via API for a Hands-Off Pipeline
- 845f4874cb616d2d8e8a7e40 — Repurpose SEO Blog Content into Social Posts via RSS
- d7c89b8565dc156e9c94d98e — Integrate a Social Scheduling Tool for Automated Publishing
- b099c3b284763f67260dbec3 — Monitor AI Search Visibility with an LLM Brand Monitor
- 10f5ad7136799724d786ecab — Choose Category Content Structure for AI Overviews
- 03ac780b7ba97b7e24b8304e — Auto-Generate Branded Infographics for Content
- 6e4f81398cf7963239d1f89a — Keep Human Approval Gates in Automated Content Pipelines
- b422877d7c387c1427a3b1a1 — Layer Multiple AI Tools Rather Than Relying on One
