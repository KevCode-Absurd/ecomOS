# The Head of Growth at a $100M Company Explains AEO

source_id: 16UkZRLAK_Ho4_4Wepj0YlJWvw6UKe_Us  |  folder: /16-AEO-answer-and-generative-engines  |  cards: 10  |  words: 11,694  |  type: transcript (podcast interview, two speakers)
credibility: Ravish Agrawal, Head of Growth at Gamma (an AI presentation tool, prosumer/consumer SaaS, described in the intro as having reached 100 million users and 100 million in ARR profitably; "killing PowerPoint"). Interviewed on the "Distribution" podcast by an unnamed host. Evidence is entirely his own team's internal observations: Google Analytics referral patterns, a "how did you hear about us" (HDYHAU) survey, a manual spreadsheet tracking citations, and personal impressions from watching Gamma's own citations. No controlled experiments, no audited or third-party-verified numbers. He hedges constantly and explicitly: "I don't have a thesis," "I don't know," "it's a black box," "that's a theory," "I haven't seen a pattern." Treat every number and ranking here as one growth lead's heuristic account at one company, not a benchmark.
date signals: References "Fable 5" and "Opus 4.8" as current top-tier models, and a "GPT-5.5" free-tier rollout `[web check: do these model names/versions exist and when]`. References Google's "AI mode" as a recent, fast-moving development and a Google "search update" on "May 21st" with no year given `[web check: which Google update, what year]`. Describes MCP remote installation via OAuth as a recent change from a "3 months ago" zip-file/local-install flow `[web check: current MCP install UX]`. States the Reddit-ChatGPT data deal as current fact `[web check: is this deal still active]`. Every platform behavior claim (what gets indexed, cited, or favored) is a snapshot of one team's observation in a field the speaker himself says changes "every 3 months." Tag all platform-specific claims below as fast-decaying.

## 1. What this source is for

It gives an operator a working mental model for answer-engine optimization (AEO): execute it like SEO, but measure it like a paid social view-through channel because most AI-driven discovery is invisible to click-through analytics. It ranks which AI platforms matter for which buyer type (consumer/prosumer vs. enterprise), gives a detailed, if unproven, Reddit playbook, and raises two forward-looking bets: LLM "memory" as a new ranking factor, and marketing directly to autonomous agents. It is thin on hard "how" (no reproducible test design, no tool workflow beyond a spreadsheet) and thick on hypotheses the speaker labels as unproven.

## 2. Principles

### 2.1 Execute AEO like Google SEO, measure it like Facebook view-through
The channel behaves like Google (you do content and intent-matching work), but you must measure it like Facebook ads: mostly view-through and self-reported, not click-through. Reason given: Google Analytics can only see click-through traffic, and AI-assistant referrals to Gamma often never produce a click. Condition: applies whenever direct referrer traffic understates AI-driven discovery. [e07344cb96f8]

### 2.2 The discovery moment: click-through can rise then fall while true influence keeps growing
Gamma's growth lead first noticed ChatGPT-referred (click-through) traffic in Google Analytics rise, then decrease in the middle of "last year." During the rise, ChatGPT-referred traffic grew roughly 8x across all Gamma's channels, from a small base (source says less than 1% of total traffic at the time). This mismatch between falling click-through and rising real influence is why they built the HDYHAU survey. Example only, single company, single time period. [e07344cb96f8]

### 2.3 Bring AI options to the front of the "how did you hear about us" survey
Previously, AI assistant options were buried under "Other." Once Gamma moved AI options to be explicit, front-facing choices, self-reported responses naming AI assistants rose sharply, even as click-through referrals kept falling. Track both curves separately: they can move in opposite directions at once. [e07344cb96f8]

### 2.4 One AEO strategy does not fit all AI platforms
Reddit's influence, in the source's observation, is concentrated almost entirely in ChatGPT. The playbooks for ChatGPT, Claude, Perplexity, Gemini and Google AI Overviews are, in his words, "completely different," with roughly 30-40% overlap across all four (his own "heuristic observation," not a measurement) and about 60% platform-specific work. Google AI Overviews follow standard SEO rules ("good SEO is good AEO" for Google specifically); the other engines do not. [dec3540c6b72]

### 2.5 Platform priority should flip by customer segment, not follow one universal ranking
For Gamma's prosumer/consumer base, over 90% of AEO-driven new user acquisition comes through ChatGPT, because ordinary consumers "just type on ChatGPT" and often don't know Claude exists. His prosumer ranking: 1) ChatGPT, 2) Google AI Overviews (because it carries a secondary SEO/distribution benefit), 3) Perplexity, 4) Claude (Claude, per the source, does not help acquire new customers; it helps retain/serve existing sophisticated users). For an enterprise-facing product he explicitly says he is guessing, and flips the order: 1) Claude (because he personally searches for tools inside Claude while working), 2) Copilot/Bing (Gamma sees meaningful referral traffic here, calling Copilot-linked companies "massive" with a "distribution advantage"), then ChatGPT, Google AI Overviews, and Perplexity roughly tied for last. [f467d7f0fff2]

### 2.6 Reddit works as a wedge via interoperability, not brand promotion
The Reddit tactic that works, per the source: post from an "open ecosystem" angle. Gamma is not a walled garden, so its team can say things like "I created a PowerPoint but actually made it in Gamma and exported it," inside a PowerPoint-focused subreddit, without directly promoting Gamma or bashing competitors ("how is gamma better than powerpoint" is explicitly the wrong move). The generalizable shape: if your tool imports from or exports to something people in a given community already use, you have a legitimate, non-promotional reason to be in that community. Example given for adaptation: a CRM company that can import from Salesforce has a legitimate reason to participate in a Salesforce subreddit. [9efc84d55e51]

### 2.7 Comments influence sentiment, not discovery direction
The source has not seen comments meaningfully change which posts get cited or how much a brand gets discovered via Reddit. His mental model: comments shape sentiment only. He does state, as an explicit theory (not a fact he can prove), that negative sentiment may get picked up and persist, citing a secondhand story about an unnamed "presumer" competitor that could not get a negative, since-indexed comment removed for "several months" despite trying "everything." Practical read: good sentiment is not required for citation, but bad sentiment should be avoided at all costs because it may stick. [9efc84d55e51]

### 2.8 Reddit citation slots are a zero-sum, competitive game
Only about 4-5 references typically appear in an LLM's answer from Reddit-sourced content, similar to ranking for a handful of top organic search results. You are always competing directly against category competitors for those slots. This is compared explicitly to SEO's "only top 3 results" dynamic, with backlinks as the SEO analogy (though the source has no equivalent mechanism identified for what makes an LLM pick one Reddit post over another from a similarly-positioned competitor). [1d269cb7fde5]

### 2.9 When you cannot win the broad query, niche the query down
You cannot win a broad AI query like "best CRM" against incumbents. Instead: "best CRM" -> "best CRM for SMB" -> "best CRM for fintech" -> "best CRM for health tech sales people." Enter at the narrow end where competition is low, build topical authority/relevance there, then make another attempt at the broader term later. Expect competitors to copy the same niching move once it works; the source's response to that is simply "keep moving" to the next under-served angle, calling that "what growth is." This applies both to general content and to Reddit posts specifically. [1d269cb7fde5]

### 2.10 Own website content is prioritized because it is fast and controllable
The source ranks Gamma's own website content as the second most influential surface for AEO overall (after Reddit, which only works for ChatGPT). Reason: it gets cited faster than third-party mentions, and the brand controls exactly how its own product and its competitors are described there. Third-party sites (other blogs, PR, reviews) form the third cluster, and the source says he "constantly switches" between calling second place vs. third place more important, so treat them as close and don't over-invest in only one. YouTube and then LinkedIn rank lower; LinkedIn citation behavior is called "thin" and unpredictable, with no clear pattern tying engagement (likes/comments) to citation. [2d4e6a109986]

### 2.11 Test additional surfaces (Medium, Quora, Substack) once Reddit and owned content are saturated
When Reddit is saturated, the source has observed continued AI-citation activity on Medium and Quora ("if you've exhausted Reddit, you should move to Quora"), and some activity on Substack, though Substack content is gated more often (many Substack writers are journalists who prefer paywalls), which the source believes reduces its citation pickup. Only add a surface if your target buyers actually use it or it already turns up when you sample real category questions on AI platforms; do not assume any platform is universally in or out. [b92cbebdb398]

### 2.12 Retrieval mode and memorization mode need different tactics
The source frames AI answers as coming from two different mechanisms: "retrieval" (the assistant does a live web search and cites fresh pages) and "memorization" (the assistant answers from what it learned in training, static until the next model retrain, and tied to his "citation half-life" idea, see 2.13). He cites an unnamed study claiming ChatGPT queries the live web for about 60% of queries and answers purely from its own trained knowledge for about 40%. His own attempt to sort Reddit vs. blogs into these buckets: he believes Reddit interventions mostly become training data (i.e., they shape what the model "knows," but a Reddit citation, if one appears, sends the click-through to Reddit, not to your site), while owned blogs and third-party PR are more likely to surface as live retrieval citations that route users into "our ecosystem." Card caveat, and the source's own inconsistency: elsewhere he explicitly says Reddit does get cited by ChatGPT, so "Reddit = training only" should be read as his working hypothesis, not a settled rule; source type (Reddit vs. blog) does not reliably predict which mode a model used. [c156aac34f0f]

### 2.13 Citation half-life: an unmeasured, theorized decay
The source believes AI citations decay over time (his own analogy: carbon dating's half-life) and that maintaining visibility requires an "always-on" content engine, not a one-time push. He explicitly states he has no formula for this: he does not know how long a citation lasts before it stops counting, and suspects the half-life differs by LLM. Gamma's only tracking method is a manual spreadsheet: log what got cited, from where, and watch for changes in "citation share" over time. He floats this as a product gap ("product idea for Profound" -- Profound being an AI-answer-tracking tool he references elsewhere) rather than something any tool currently measures for you. [b78f1ae27412] [2d4e6a109986]

### 2.14 Memory may compound first-mover advantage
Beyond training-time memorization, the source raises "memory" -- what a logged-in user's session or account has previously been shown -- as a separate, newer factor. His reasoning: tools like Profound run prompts logged out, but average consumers use ChatGPT/Claude/Google logged in, so what was referenced before may influence what gets referenced again for that user (drawing a parallel to Google personalizing rankings toward links you've already clicked). His example: when GPT-5.5 rolled out to free users, Gamma saw a jump in ChatGPT click-through traffic, concentrated in developing countries (where the free rollout reached furthest); his interpretation is that GPT-5.5 had a bigger "memory component" than earlier models, though he is explicit this is a hypothesis and the mechanism is "a black box." First-mover framing: moving early on AEO for a given query means you may get shown, then remembered, then shown again -- a compounding advantage if the theory holds. [c156aac34f0f]

## 3. Procedures

The source gives few clean numbered procedures; most are reconstructed from a loosely sequential narrative. Steps not explicitly stated as a sequence are marked "(reconstructed)."

### 3.1 Detect and start measuring an emerging AEO signal (reconstructed from Gamma's own story)
1. Watch Google Analytics referral sources for AI assistant traffic (ChatGPT, etc.), even if the raw numbers are tiny (Gamma's was under 1% of total traffic when they first noticed it). [e07344cb96f8]
2. Watch for a divergence: click-through referral traffic can rise then plateau or fall while the underlying channel is still growing. Do not conclude the channel is dying from click-through alone. [e07344cb96f8]
3. Add or upgrade a "how did you hear about us" survey at signup/checkout. Put AI assistant names as explicit, visible options rather than leaving them folded into "Other." `[verify UI]` [e07344cb96f8]
4. Track click-through referrals and self-reported AI mentions as two separate curves, not one blended number. [e07344cb96f8]
5. Once a pattern shows up (source's trigger: "common knowledge was LLMs pick up from Reddit"), begin deliberate content work on the channels believed to feed that LLM. [e07344cb96f8]

### 3.2 Decide where to invest AEO effort by platform and segment (reconstructed)
1. Identify your buyer segment: prosumer/consumer vs. enterprise. The source's rankings invert between the two (see 2.5). `[needs brand data: which segment(s) the brand actually serves]` [f467d7f0fff2]
2. Sample real buyer questions on the relevant AI platforms; record which platform, and note the model, date, mode (search vs. AI mode) if possible `[web check: current UI for checking this]`. [dec3540c6b72]
3. Do not assume Reddit help transfers across engines: it is, in the source's observation, isolated to ChatGPT. Build separate plans for Claude, Perplexity, Gemini and Google AI Overviews. [dec3540c6b72]
4. For Google AI Overviews specifically, apply standard SEO practice; the source says the two are the same game there. [dec3540c6b72]
5. For Claude specifically, prioritize building an MCP server and listing it in Claude's ecosystem over trying to win citations directly (see 3.4). [dec3540c6b72]

### 3.3 Run the Reddit playbook (source's stated approach, reconstructed into steps)
1. Choose subreddits from two angles: (a) an ICP angle -- where does your buyer persona (e.g., a sales leader, marketing leader, founder) already go for content (example given: r/SaaS); (b) a problem-universe angle -- where is the underlying problem or category discussed (example given: r/PowerPoint, r/Canva for a presentation tool). [b78f1ae27412]
2. At Gamma's current scale, they skip subreddits with only thousands to tens of thousands of members; the source says this threshold is a function of scale, and that a startup or smaller company should treat small subreddits as "fair game." `[needs brand data: current subreddit member counts relevant to the brand's category]` [b78f1ae27412]
3. If starting from zero, prioritize participation in other people's subreddits first (faster payoff); treat building your own subreddit as the longer-term investment, since content from your own newer subreddit gets picked up later than content elsewhere. [b78f1ae27412]
4. When posting in someone else's subreddit, lead with an "open ecosystem" value angle (2.6): show your tool's interoperability with what that community already uses, rather than direct self-promotion or direct "we're better than X" claims. [9efc84d55e51]
5. If doing competitor comparisons, choose deliberately which competitors to name; naming a competitor can, in the source's view, also help that competitor's own AEO, so weigh who you bring into the frame. [9efc84d55e51] [1d269cb7fde5]
6. If a broad query/topic is saturated by competitors, niche the angle down (2.9) rather than competing head-on. [1d269cb7fde5]
7. Do not rely on comments to move citation outcomes; use them only as a sentiment signal, and monitor for negative sentiment that could get indexed and stick. [9efc84d55e51]
8. Log every citation you find (query, platform, date, source URL/post) in a tracking spreadsheet; revisit periodically to see if citation share is declining (their proxy for "half-life"). [b78f1ae27412] [2d4e6a109986]
9. Treat the whole effort as an always-on engine: there is no "finished" state, per the source. [b78f1ae27412] [1d269cb7fde5]

### 3.4 Build the Claude / MCP play (reconstructed)
1. Build an MCP (Model Context Protocol) server for your product and list it so it can be discovered inside Claude's ecosystem. `[verify UI]` [dec3540c6b72]
2. Expect an approval step from Anthropic before it goes live; the source calls this play inherently "slow." `[verify UI]` [dec3540c6b72]
3. Installation friction has reportedly dropped: the source says that roughly 3 months before this interview, users needed to download a zip file and install locally; at interview time, remote installation via an OAuth link ("like connecting Facebook... with any... third party website") was already possible. `[web check: current MCP install flow]` [dec3540c6b72]
4. Do not expect Claude to surface your MCP to users on its own. The source is explicit: Claude will not proactively recommend your MCP just because it exists on your site; you still have to do the work of telling your own users "we have an MCP, connect it." [dec3540c6b72]
5. Expect this play to matter more for engagement/retention of existing users than for net-new acquisition (Gamma's own MCP connector drove usage from people already working inside Claude, e.g., someone drafting content in Claude who then triggers a Gamma deck creation) -- not primarily a top-of-funnel acquisition channel today. [dec3540c6b72] [f467d7f0fff2]

### 3.5 Produce AEO-designated content with the 80/20 crawler/human split
1. Explicitly label a content initiative as "AEO-first" before producing it, separate from content made primarily for humans to click on. [4959f5bec48f]
2. Choose titles, headings, and structure based on the actual prompts and phrases people type into AI assistants, rather than clickbait headlines meant to earn human clicks. `[needs brand data: real buyer prompt phrasing, from support tickets, search queries, or sampled AI conversations]` [4959f5bec48f]
3. Still make the page fully useful and accurate if a human lands on it; it should never read as obviously broken or nonsensical to a person. [4959f5bec48f]
4. Decide the content's depth and angle deliberately: go beyond a bare product description (source's example: don't just say "this is a glass of water") into a comparative or reasoned angle (why this product is meaningfully better than an alternative, e.g., 5 concrete benefits) rather than short, keyword-stuffed, repetitive copy. [4959f5bec48f]
5. Recheck citation results after publishing; treat any gains as experimental, not settled. [4959f5bec48f]

## 4. Rules, thresholds and numbers

| rule | number or threshold | condition | source's basis | card id |
|---|---|---|---|---|
| ChatGPT-referred traffic growth (Gamma, one period) | ~8x growth across all channels | during the rise phase, before click-through later fell | one company's GA data, single time window; example not a promise | e07344cb96f8 |
| Starting size of that signal | under ~1% of total traffic | when first noticed | same | e07344cb96f8 |
| Cross-engine overlap in AEO playbooks | ~30-40% overlap, ~60% platform-specific | across ChatGPT, Claude, Perplexity, Gemini, Google AI Overviews | source's "heuristic observation" | dec3540c6b72 |
| Claude citation volume vs. ChatGPT | Claude cites roughly 5x less than ChatGPT | general comparison | source cites unnamed "studies... out there," not verified here | dec3540c6b72 |
| Gamma AEO-driven acquisition via ChatGPT | "north of 90%" | of Gamma's AEO-attributed new users | source's estimate | f467d7f0fff2 |
| Reddit-to-ChatGPT citation lag | ~30-45 days | new Reddit content, ChatGPT citation | source's observation, "in one case," not an SLA | b78f1ae27412 |
| Reddit-to-Perplexity citation lag | as fast as "the next day" | for a specific, exact-phrase query | source's observation | b78f1ae27412 |
| Reddit-to-Google-AI-Overviews lag | same-day pickup observed once | one niche query, told by the podcast host, not the guest | anecdote from the interview, not Gamma data | b78f1ae27412 |
| Reddit citation slots per query | roughly 4-5 references | typical LLM answer pulling from Reddit | source's estimate | 1d269cb7fde5 |
| Negative Reddit comment persistence (secondhand case) | "several months," could not be removed | an unnamed presumer competitor | secondhand story, unverified | 9efc84d55e51 |
| Retrieval vs. memorization split (ChatGPT) | ~60% live web queries, ~40% from trained knowledge | general, not ecommerce-specific | a study the source cites but does not name; not verified here | c156aac34f0f |
| Calendly revenue anecdote | "I think they went to like $300 million in revenue" | tied to its viral "Powered by Calendly" branding | source's own uncertain recollection ("I think") | none (discussed in text only, not carried into a card) |
| MCP install-flow change | zip file + local install -> remote OAuth install | "3 months" before the interview vs. at interview time | source's own timeline | dec3540c6b72 |

## 5. Diagnostics and checks

| check | how | good | bad | next step | card |
|---|---|---|---|---|---|
| Is AEO actually happening but invisible? | Compare GA click-through referral trend against self-reported HDYHAU AI mentions | Self-reported AI mentions rising even if click-through is flat or falling | Both flat, no self-reported signal at all | Add/upgrade the HDYHAU survey; surface AI options explicitly, don't wait for click-through to prove it | e07344cb96f8 |
| Is your Reddit effort wasted on the wrong engine? | Sample the same buyer question across ChatGPT, Claude, Perplexity, Gemini, Google AI Overviews and note which cites Reddit content | Reddit content shows up mainly in ChatGPT answers | Reddit content absent from ChatGPT too, or only showing on other engines | Redirect Reddit effort to ChatGPT-relevant queries; use other tactics for other engines | dec3540c6b72 |
| Is a competitor's content winning your niche query? | Search the exact narrow phrase you're targeting (e.g., "best CRM for fintech") on the target AI platform | Your content or comparison appears | A competitor consistently appears instead | Niche down further, or pick a less-contested comparison angle | 1d269cb7fde5 |
| Is a Reddit thread carrying negative sentiment? | Periodically re-read your own top cited/likely-to-be-cited threads | Neutral-to-positive tone, or no strong sentiment | A visible negative comment with traction | Address early; source warns it can persist for months once indexed | 9efc84d55e51 |
| Are you losing citation share over time (possible half-life decay)? | Manually log each citation (query, platform, date, URL) in a spreadsheet; re-check the same queries periodically | Citation share holds or grows | Citation share drops on previously-cited queries | Refresh or republish that content; treat as an ongoing task, not one-time | b78f1ae27412, 2d4e6a109986 |
| Is content actually agent/crawler-oriented, or just relabeled marketing copy? | Check whether headings/structure use real buyer prompt phrasing vs. clickbait | Structure matches how people phrase questions to AI assistants | Still built around a human clickbait headline | Rewrite headings and structure around actual query phrasing; keep it human-readable too | 4959f5bec48f |
| Is your MCP actually getting used? | Track connector installs/usage inside Claude, separate from web traffic | Rising usage among users already in the Claude ecosystem | No usage despite MCP existing | Remember Claude will not push it for you; you must tell your own users to connect it | dec3540c6b72 |

## 6. Tools, settings and named features

| tool or feature | use in the source | tag |
|---|---|---|
| Google Analytics | Used to first notice, then to track, click-through AI referral traffic; source notes it cannot see non-click AI discovery | `[verify UI]` |
| "How did you hear about us" (HDYHAU) survey | Self-reported attribution at signup/checkout; moving AI options to the front increased responses | `[verify UI]` |
| Reddit (own subreddit + other subreddits) | Primary AEO surface for ChatGPT; mixed approach of own-community and other-community posting | `[web check: current Reddit-ChatGPT data relationship]` |
| MCP (Model Context Protocol) server | The recommended way to be discoverable/integrated inside Claude, described as increasingly like an app-store listing | `[web check: current MCP submission/approval process]` |
| Claude / OAuth remote install | Newer, lower-friction way to connect an MCP vs. older zip-file local install | `[web check: current install flow]` |
| YouTube | Secondary AEO surface; transcripts get picked up; no clear view-count-to-citation correlation observed | `[web check]` |
| LinkedIn (posts and articles) | Secondary AEO surface; described as thin and unpredictable at time of interview | `[web check]` |
| Medium, Quora | Additional surfaces to test once Reddit is saturated; both described as currently indexed | `[web check]` |
| Substack | Indexed but often gated by journalist-authors, which the source believes reduces citation pickup | `[web check]` |
| Discord | Not indexed at time of interview per the source; predicted to lag behind Instagram | `[web check]` |
| Instagram | Predicted (speculative) to get indexed before Discord, within "6 to 12 months" of the interview | `[web check]` |
| X / Twitter | Source has never observed X content being indexed by LLMs, despite X ranking in Google search/news; flagged by the source himself as worth re-checking | `[web check]` |
| Profound | Named third-party AI-answer/citation tracking tool; source notes it runs prompts logged out, unlike typical logged-in users, and jokes it could add a "citation half-life" feature | `[web check: current Profound feature set]` |
| "Powered by Gamma" / "Made with Gamma" watermark | PLG/virality mechanic, compared to "Powered by Calendly" | none |

## 7. Examples and case results

All are the presenter's own anecdotes or secondhand stories from the interview, not independently verified results.
- Gamma: ChatGPT-referred (click-through) traffic rose, then fell mid-"last year"; during the rise, ChatGPT-referred traffic across all channels grew roughly 8x from under 1% of total traffic. [e07344cb96f8]
- Gamma's own subreddit gets cited for specific how-to questions, e.g., "how to export a presentation from Gamma." [9efc84d55e51]
- A citation observed from both an 18K-view and a 400K-view YouTube video, with no clear pattern by view count. [2d4e6a109986]
- An unnamed "presumer" competitor got a negative Reddit comment indexed and could not get it removed "for several months" despite trying everything. [9efc84d55e51]
- Multiple companies impersonating Gamma with copycat landing pages and near-identical branding; these fakes rarely rank organically but do appear via paid ads, causing user confusion. [9efc84d55e51] (mentioned in text; not the card's main focus)
- Gamma's MCP connector: someone drafting with Claude triggers creation of a Gamma presentation directly inside that workflow. [dec3540c6b72]
- GPT-5.5's rollout to free users (reaching developing countries furthest) coincided with a jump in ChatGPT click-through traffic to Gamma; attributed by the source to a stronger "memory component," an unverified hypothesis. [c156aac34f0f]
- Calendly's "Powered by Calendly" branding is cited (uncertainly, "I think") as driving it to roughly $300M in revenue, as a PLG/virality comparison; Gamma runs the same mechanic via "Made with Gamma." (Discussed in text; not tied to a specific card.)
- Gamma's 4,000-drone stunt over San Francisco, explained only as a culture/creativity choice ("let ideas breathe"), with no measured result given. (Discussed in text; explicitly flagged by the source header itself as skippable banter, not carried into a card.)

## 8. Mistakes the source warns about

1. Judging an AEO/AI-discovery channel only by Google Analytics click-through referrals; most AI-driven discovery is invisible to it. [e07344cb96f8]
2. Burying AI-assistant options under "Other" in attribution surveys instead of surfacing them explicitly. [e07344cb96f8]
3. Applying one AEO playbook across all AI platforms instead of building separate plans per engine. [dec3540c6b72]
4. Assuming Reddit gains transfer to Claude, Perplexity, Gemini, or Google AI Overviews the way they do for ChatGPT. [dec3540c6b72]
5. Promoting your brand directly on Reddit ("X is great," "X beats Y") instead of leading with an open-ecosystem/interoperability angle. [9efc84d55e51]
6. Assuming comments will move your citation ranking; they mainly shape sentiment. [9efc84d55e51]
7. Letting a negative, indexed Reddit comment sit unaddressed; the source's secondhand case suggests it can persist for months. [9efc84d55e51]
8. Assuming AI-written content is automatically "spam"; the source argues today's models can write deep, well-researched content, and calls this a wrong assumption twice over (once on AI authorship, once on thinness). [4959f5bec48f]
9. Writing thin, keyword-stuffed content instead of going deep on comparative or meaningful angles. [4959f5bec48f]
10. Trying to win a broad, contested query outright instead of niching down first. [1d269cb7fde5]
11. Assuming a small subreddit will move the needle at large-company scale (source's own caveat: this may not apply to smaller subreddits or niche topics, or to startups). [9efc84d55e51]
12. Treating an MCP server as self-marketing; Claude will not proactively surface it, you must still drive your own users to connect it. [dec3540c6b72]
13. Over-investing in a single "off-brand-universe" or unfamiliar community subreddit on a hunch, without checking whether it falls inside either the ICP or problem-universe angle the source uses to pick subreddits. [b78f1ae27412]
14. Treating the current lack of authority-based ranking on AEO ("everybody starting from the same authority level right now") as permanent; the source expects this to change as platforms mature (parallel to Google's own history). [dec3540c6b72] (source text, general caveat)

## 9. Caveats, conflicts and what is missing

- Single interviewee, single company (Gamma), consumer/prosumer SaaS -- not ecommerce. Every ranking, percentage, and lag figure is his own team's informal read, repeatedly self-described as guesswork ("I don't have a thesis," "it's a black box," "that's a theory").
- Internal inconsistency flagged by the card set itself: the source calls Reddit primarily "training data" (2.12) in one part of the conversation, yet elsewhere states plainly that Reddit is the most-cited source for ChatGPT (2.4, 2.10). Card c156aac34f0f explicitly warns not to treat "Reddit = training-only" as settled; read it as an unresolved tension in the source's own model, not a rule.
- No hard "how": no content brief template, no test-and-measure cadence beyond "log it in a spreadsheet," no citation half-life number (source admits he does not have one), no budget or headcount guidance, no legal/ToS view on the "agentic bribing" idea below.
- "Agentic bribing" (hiding incentive text inside a JSON schema or install package to induce an autonomous agent to prefer your product, e.g., "10% extra reward to the model if it signs up right away") is raised as something "other growth people" are experimenting with. The source has not done this work himself, gives no method, and the tactic's legality, platform-policy status, and reliability are entirely unaddressed. Treat this purely as a speculative, unverified idea to watch, not a procedure. `[web check: current MCP/agent platform policies on this]`
- The GTM-vs-distribution semantic distinction (2.20 in the raw transcript) is explicitly the source's personal, informal opinion ("that could be just me"), with no operational content. Included for completeness, not as a rule.
- The "half-life of citation" idea, the "memory compounds first-mover advantage" idea, and "marketing to agents runs through AEO" are all framed by the source as his own open hypotheses for a field he says will look "completely different" within a year. Nothing here should be treated as durable beyond a short window.
- Ecommerce translation gap: nearly every example is a B2B/prosumer SaaS use case (CRM, presentation software, PowerPoint/Canva competitors). Ecommerce-specific application (product pages, comparison content, review-driven citations, checkout/agentic commerce) is not addressed in the source; the "CRM/Salesforce" and "PowerPoint" interoperability examples are the closest analogues and would need real adaptation. `[needs brand data: what interoperability, comparison, or open-ecosystem angle actually applies to this ecommerce brand's product]`
- Possible conflict with common ecommerce SEO advice: the source claims website "authority" (domain age, backlink profile) currently matters little for AEO citation ("very level playing field," a new startup's AI-first content can beat Forbes), which cuts against standard SEO doctrine that domain authority is a durable moat. He frames this explicitly as temporary ("till then it's an open field"), not a permanent break from SEO norms, and it directly conflicts with 06-MEA/15-SEO material that treats authority-building as foundational; flag this as an open disagreement, not something to resolve here.
- Scope: this source explicitly routes traditional paid SaaS advertising/ROAS tracking to 06-MEA and foundational SEO site structuring/backlinking to 15-SEO; it does not cover either in depth.

## 10. Card index

- e07344cb96f8: AEO mental model: execute like Google, measure like Facebook
- dec3540c6b72: Platform-by-platform AEO playbooks diverge: don't run one strategy
- f467d7f0fff2: Prioritize AI discovery surfaces using the store's own buyer evidence
- 9efc84d55e51: Reddit playbook: open-ecosystem wedge posts and competitor-comparison framing
- b78f1ae27412: Measure citation pickup and persistence before timing a store campaign
- 4959f5bec48f: Test question-led product content while preserving shopper usefulness
- 1d269cb7fde5: Compete in AI citation by niching down the prompt, then expanding
- 2d4e6a109986: AEO channel priority and citation-lifetime tracking
- b92cbebdb398: Test additional publishing surfaces against observed category citations
- c156aac34f0f: Understand retrieval vs memorization to choose content tactics
