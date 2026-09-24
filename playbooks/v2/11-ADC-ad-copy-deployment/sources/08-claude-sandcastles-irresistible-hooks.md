# Claude + Sandcastles = Irresistible Hooks

source_id: 1hKKpfZZuK3540BaBFbZysYS3cQFdSpVU  |  folder: /11-ADC-ad-copy-deployment  |  cards: 10  |  words: 7190  |  type: transcript (YouTube screen-share walkthrough, single presenter)
credibility: Presenter runs the "Callaway Marketing" channel and calls the workflow "the hook machine by Callaway". He says he has made some of the most popular hook trainings online, studied "thousands" of top videos, and done "billions of views" with over 1 million followers. He is tied to Sandcastles, the paid tool the workflow requires: he says "what we charge credits for is the deep analysis", "we give it to you for free" and "I wrote the rules". So the source sells the tool it recommends. Evidence is 1 live demo run on 4 organic creator channels (40 videos, 17 winners), his own reactions to the output, and model-generated findings he did not check against any test. No paid-ad data, no conversion data, no controlled tests. Treat every rule as "Source 08 says".
date signals: A generated hook says "Single trigger hooks are dead in 2026", so the demo ran in 2026. Names Claude Desktop, Claude Cowork and Code ("you need to be on the desktop app in order to run co-work or code"), claude.com/download, the Sandcastles MCP with "I believe 24 different tools", a Sandcastles Pro tier, credits, and a setup page the transcript renders as "help.sandcastle.ai/MCP". Drive file modified 21 Sep 2026. All product names, tiers, credit prices and tool counts can change `[web check: Sandcastles current plans, credit price per video, MCP tool list and setup URL]`.
scope note: The source header places the Hook Machine workflow in 11-ADC. It routes advanced media buying campaign setup to 10-MCR and product pages to 07-LPG. It says to skip the billion-view intro, the "mustache chef" emoji request and "Wavy World" community plugs; those are left out below. The demo is about organic short-form creator videos (content marketing topics), not product ads. The ecommerce use is an inference the cards make, not something the presenter shows.

## 1. What this source is for

It gives an operator a data-grounded way to write and grade short-form video hooks with an LLM. Instead of asking a cold chat for hooks, you pull real top videos (yours and close competitors'), split winners from losers by a view break point, have the model extract psychology, framing, grammar and non-obvious patterns, turn them into a scoring rubric, then generate, grade and rewrite hooks for a new topic. For an ecommerce team the transferable parts are: ground hook generation in your own winning creative, compare winners against losers, screen formats for fit before generating, and grade drafts against a written rubric. The source is strong on the shape of the loop and weak on the rubric content: the 8 universal principles and most of the 11 custom principles are never stated, and the prompt and skill file are linked but not in the text.

## 2. Principles

### 2.1 Cold AI hook prompts produce generic hooks
LLMs "just aren't optimized for short form social data". Unless trained extensively, they do not know how to write persuasively for social media. Dumping a topic into a cold chat and asking "write me hooks" ends up "horrible", "super generic and never compelling". Condition: applies when the model has no grounding data. The fix is grounding, not giving up on AI. Evidence: presenter's opinion, no test shown. [a80ff986fd63]

### 2.2 Copy-pasting a viral hook from another niche usually fails
Taking a viral hook from a creator in a distant niche and applying it to yours "usually" does not work: the psychology does not translate, the format crossover does not fit, and "even the grammar usually isn't working". He blames "fake gurus" for promoting straight hook clones. Condition: strongest when niches are far apart ("all the way in this niche ... all the way over to the other"). The card notes this is a practitioner claim; cross-niche copying sometimes works. [a80ff986fd63]

### 2.3 Combine data with storytelling principles
The Hook Machine is a "four-step process that combines data with storytelling principles to give you the best chance at writing an original hook". The data side is transcripts, metrics and visual analysis of winning videos. The storytelling side is the presenter's 8 universal hook principles. Neither alone is the method. [728fcae3dec6] [e9f81c60dc73]

### 2.4 Hook analysis needs deep data, not captions and view counts
Lightweight scrapers (he names Apify) pull metrics and captions. That is "very surface level": good for ranking which videos did best, not for finding why. Deep analysis processes the transcript, idea, topic, hook format, storytelling format, visual layout and all metrics. Only that layer found non-obvious patterns such as audio-clip openers underperforming by about 60% for 1 creator. Condition: he sells the deep layer, so weigh the claim. [cfa4e7c04581] [38a495e39205]

### 2.5 Screen out paid or boosted videos before analysis
A high-view video with engagement below about 2% "has paid spend behind it" and would "artificially inflate the video and give you a false sense of what will work". Screen these out by default. In the demo, a Peter Visuals post (a Gamma brand post) showed 0% engagement and was removed as clearly paid. Condition: this is his rule of thumb for organic creator channels. Engagement norms vary by platform and account size (card caveat). The source does not define how engagement rate is calculated. [03d175f0d156]

### 2.6 Content is 80/20, so study only the breakout videos
"Content is just like anything else. It's 80/20": a few big videos drive most growth. Rank a channel's top 10 by views, find the natural drop-off (the break point), and call videos above it winners and the rest losers. Extract principles from winners; use losers as contrast. [ad297d96546e]

### 2.7 Keep each creator's analysis separate
Do not mash all videos into 1 pool. Sort and analyze each channel on its own, because hook styles differ by person (a tight speaker versus a "yapper" who uses more words per sentence). Only after per-channel analysis look for shared patterns. [ad297d96546e] [fdd73f8bda1d]

### 2.8 More competitors in 1 analysis makes the result "muddier"
"The more competitors you add in one analysis, the muddier it gets." He suggests running the flow 4 times with 1 competitor each, giving a "Brier hook writer", a "bonus footage hook writer", a "Callaway hook writer", and using them separately. Condition: his words are "I have a feeling that when you combine all the insights, it does dilute to the average". This is a hypothesis, not a tested result. Cross-channel synthesis is still useful for patterns that truly repeat. [fdd73f8bda1d] [14df3bb700a0]

### 2.9 Your own backlog is the best data
"You may want to run this flow just on you alone because that's really the way to get the best data." The "real way" is to make about 100 of your own videos, analyze all 100, let it run the top 20, and expect a break point around 10, 12 or 15. The generator's "originals" are built only from the presenter's storytelling principles and your account, not from competitors. [14df3bb700a0]

### 2.10 Check that a format fits the topic before using it
A winning format only helps if it matches the kind of topic. The generator picks only winning formats that fit; a stat or case-study format does not fit a theoretical psychology concept. Forcing a mismatched template is the cross-pollination failure from 2.2. Rejection is correct behaviour. If too few formats fit, analyze more videos rather than force-fit. [721989c4c0ef] [fdd73f8bda1d]

### 2.11 Reskin formats, do not clone them
The generator takes a winning format and "reskin[s] it using our principles to write it close but not exactly". This is the middle path between cold prompting (2.1) and copy-paste (2.2). [721989c4c0ef]

### 2.12 The AI produces candidates; a human picks and edits
In the demo the presenter liked only a few of the generated hooks, rejected several, wrote his own derivative draft, then had it graded and rewritten. His favourite came from a rewrite. The loop ends with human judgement, not with the model's grade. [a80ff986fd63] [e9f81c60dc73]

### 2.13 The rubric is not one-and-done
The rubric changes with more videos per channel, different channels, or only your own channel. "You can run this a bunch of times to get different variations of your hook rubric." Re-run with fresh or larger data. [14df3bb700a0] [e9f81c60dc73]

### 2.14 Hook patterns the demo extracted (examples of output, not proven laws)
These are model findings from 1 run on 4 organic creator channels. They are the source's only concrete hook rules. [38a495e39205]

Presenter's own channel (4 winners, 6 losers):
- Psychology: winners attach a concrete outcome to a constrained input ("30 days of content in 30 minutes"). Losers lean on series or episode branding with no standalone value promise in the first sentence.
- Trigger words and framing: winners use words like "actually", "everyday", "crushing", "right now", "easiest". Losers use vague superlatives.
- Grammar: winners are declarative and front-load the payoff ("Here's how to do X and Y"). Losers delay the takeaway and have "no identity".
- Pattern: when he names a specific outcome the video wins; when he leans on episode branding alone it "sinks 50%".

Peter Visuals (5 winners, faceless case-study channel):
- Psychology: the hook is the stat, but winners pair the stat with a second-sentence amplifier (a comparison or contrarian reframe). Losers state the stat and stop.
- Framing: magnitude language, with like counts as extra proof. Exact numbers matter: "90 to 120 million outperforms 19 to 40". Bigger evidence wins.
- Anti-pattern: audio-clip openers (opening on a reference video's clip instead of his own framing) underperform by about 60%.

Cross-channel synthesis (patterns in 2 or more channels):
- Specificity beats abstraction (all 4 channels).
- 2-sentence amplifier: state something, then amplify in sentence 2 (Peter Visuals and the presenter, "somewhat" Brier).
- Avoid throat-clearing openers that delay the value (Brier, bonus footage, presenter).
- Confident declaratives beat hedged questions: "Winners say things, losers ask questions" (Brier, presenter, Peter Visuals).
- The model also listed "divergences" where channels differ. Their content is not given.

## 3. Procedures

### 3.1 One-time setup
1. Get a Sandcastles account, at least the Pro tier. Without the MCP you cannot pipe social data in, cannot deep-analyze videos, and cannot run the data loop. `[verify UI]` `[web check: Sandcastles tiers and price]` [728fcae3dec6]
2. Install the Claude Desktop app (claude.com/download). The desktop app is required to run Cowork or Code. `[verify UI]` [728fcae3dec6]
3. Set up the Sandcastles MCP to connect Sandcastles to Claude. The presenter links a setup video and a help page (transcribed as help.sandcastle.ai/MCP) and says it takes about 2 minutes. You do this once. The setup steps themselves are not in the source. `[verify UI]` `[web check: current MCP setup page]` [728fcae3dec6]
4. Get the Hook Machine prompt and the Claude skill file from the video description. They are free but not included in this source text. `[web check: prompt and skill file from the video description]` [728fcae3dec6]

### 3.2 Build the rubric and generator (the Hook Machine run)
1. Open Claude Desktop, use Cowork, paste the Hook Machine prompt and run it. Claude builds a project plan in the progress tab (upper right). `[verify UI]` [728fcae3dec6]
2. The prompt announces 3 outputs: (a) a hook format library listing top hooks with a "Mad Lib" template (a bonus you can export), (b) a personalized grading rubric, (c) a hook generation engine that writes hooks for any topic. [728fcae3dec6]
3. Give the channels. Demo input: your own channel plus 3 competitors, with the instruction "grab the top 10 videos from these channels" and "ignore any videos about personal life that are not related to the topic". The off-topic filter saves credits and keeps vlog hooks out. [728fcae3dec6]
4. Read the cost preview. Demo: 10 videos x 4 channels = 40 videos, about 40 credits, about 10 minutes. Videos already analyzed in Sandcastles are not charged again, and the tool says so at the next step. [728fcae3dec6] [14df3bb700a0]
5. Answer the brand-deal question. The tool asks whether to include all videos or screen out brand deals (below about 2% engagement). Say yes, screen them out. Then confirm the topic filter. [03d175f0d156]
6. The tool checks your Sandcastles watch list. Channels not on it are found in the Sandcastles database and added. Channels not in the database are live-added: it scrapes their backlog and imports it first, and tells you if it has to. `[verify UI]` [728fcae3dec6]
7. It pulls the top 10 videos per channel, screens out off-topic and paid videos, and keeps a separate list of 10 per person. [ad297d96546e]
8. It runs deep analysis with the MCP's analyze tool. Unanalyzed videos take about 1 to 2 minutes each and run concurrently. Demo: 34 of 40 were already done; the 6 remaining ran at once in about 1 more minute. [cfa4e7c04581]
   - Time-saving alternative: when many videos are unanalyzed, bulk-analyze them in the Sandcastles web app (faster than going back and forth through the MCP), export a CSV, and drop the CSV into the Claude chat. `[verify UI]` [cfa4e7c04581]
9. It sorts winners and losers per channel by the natural break point in views, then asks whether to adjust the line. Keep it or move it. Demo: kept all lines, though the presenter noted bonus footage was borderline (4 or 5). [ad297d96546e]
10. It analyzes winners per channel in 4 buckets: psychology takeaways, trigger words and framing, grammatical takeaways, non-obvious takeaways. It already has transcripts and hooks, so this is a meta-analysis on stored data. [38a495e39205]
11. It runs a cross-channel synthesis: patterns that appear in 2 or more channels, plus divergences. It assumes the channels are close competitors, so shared attributes are a good sign. [fdd73f8bda1d]
12. It builds the rubric: the presenter's 8 universal hook principles plus custom principles from the data, each tagged to its source video or channel. Demo: 8 universal plus 11 custom. Review it. If anything looks off, say so; otherwise say "continue". [e9f81c60dc73]
13. It outputs the bonus hook library: per video, the original hook and its format. Copy it, save it as a skill, or export it elsewhere. [14df3bb700a0]

### 3.3 Generate hooks for a new topic
1. Enter the topic in a couple of sentences. Demo: "dopamine ladders", the 6 levels of dopamine released while watching a video, "how you make people addicted to content". You can add more research; he kept it short for the demo. [721989c4c0ef]
2. The generator screens winning formats for fit with the topic. Demo: 4 of Peter Visuals' 5 formats failed (case-study stat library versus a conceptual topic with no external stat); 2 of the presenter's 4 fit. [721989c4c0ef]
3. It writes up to 5 hooks per channel from compatible winning formats only, fewer if fewer formats won or fit. Then it writes its own list of 5 "originals". [721989c4c0ef]
4. Each hook is graded against the rubric. The presenter coded it to hide anything at C or below ("if it's a C or below, don't even give it to me"), so shown hooks were mostly A grades. [e9f81c60dc73]
5. Read and pick. Expect own-channel formats and originals to be strongest, and competitor formats to be "hit or miss" depending on style fit. [fdd73f8bda1d]

### 3.4 Grade and rewrite your own draft hook
1. Write your own draft, for example a derivative of a generated hook you half liked. [e9f81c60dc73]
2. Paste it and ask Claude to grade it against the rubric and rewrite it. [e9f81c60dc73]
3. Read the line-by-line breakdown and the "why not higher" section, not only the letter grade. [e9f81c60dc73]
4. Review the rewrites (demo gave 3) and pick one that fits your voice. [e9f81c60dc73]

### 3.5 Reuse without rerunning
1. Once the rubric exists, drop new topics into the same thread, or set up a Cowork project with the rubric and hit it repeatedly. `[verify UI]` [728fcae3dec6] [e9f81c60dc73]
2. Do not rerun the full flow for each topic: it burns tokens and credits. [728fcae3dec6]
3. Re-run the full flow when you want a new rubric variant (more videos, different channels, own channel only). Re-apply the brand-deal filter each time the channel list changes (card addition). [14df3bb700a0] [03d175f0d156]

### 3.6 Low-credit variant
Keep using the MCP, but drop in transcripts of your own videos yourself to avoid per-video analysis credits. The presenter says this "could also kind of work" but you lose the visual processing, "so you kind of want the sandcastles analysis". [14df3bb700a0] [cfa4e7c04581]

## 4. Rules, thresholds and numbers

| rule | number or threshold | condition | source's basis | card id |
|---|---|---|---|---|
| Screen out likely paid or brand-deal videos | engagement below about 2% | high-view videos on organic creator channels | presenter's default rule; demo removed a 0% engagement post | [03d175f0d156] |
| Videos pulled per channel | top 10 | demo setting; more is better | demo | [728fcae3dec6] |
| Channels in demo run | 4 (own plus 3 competitors) | fewer competitors per run is cleaner | demo | [728fcae3dec6] |
| Cost of demo run | 40 videos, about 40 credits, about 10 minutes | first-time analysis; already-analyzed videos not charged again | tool preview in demo | [728fcae3dec6] [14df3bb700a0] |
| Deep analysis price | about 1 credit per video | scraping, metrics and captions are free and unlimited per the presenter | presenter, who sells the tool | [cfa4e7c04581] |
| Time per unanalyzed video | about 1 to 2 minutes, run concurrently | through the MCP; web app bulk analysis is faster | demo | [cfa4e7c04581] |
| MCP setup time | about 2 minutes, once | per presenter | presenter | [728fcae3dec6] |
| MCP tools | about 24 ("I believe") | named: channel recap, analyze, credit, hooks, format | presenter | [cfa4e7c04581] |
| Winner break point, own channel | between video 4 and 5 (4 winners, 6 losers) | top 10 by views | demo output | [ad297d96546e] |
| Winner break point, other channels | Peter Visuals 5, bonus footage 4 (borderline 4 or 5), Brier 4 | top 10 by views; smaller channels may break differently | demo output | [ad297d96546e] |
| Content distribution | 80/20 | a few breakouts drive most growth | presenter opinion | [ad297d96546e] |
| Episode branding without an outcome | sinks about 50% | presenter's own channel only, 10 videos | model finding in demo | [38a495e39205] |
| Audio-clip openers | underperform by about 60% | Peter Visuals only | model finding in demo | [cfa4e7c04581] |
| Bigger evidence numbers win | "90 to 120 million outperforms 19 to 40" | Peter Visuals case-study hooks | model finding in demo | [38a495e39205] |
| Cross-channel pattern bar | appears in 2 or more channels | synthesis step | demo prompt behaviour | [fdd73f8bda1d] |
| Rubric size | 8 universal plus 11 custom | demo run; custom count changes with data | demo | [e9f81c60dc73] |
| Hooks per channel | up to 5 | capped by winning formats that fit the topic | prompt design | [721989c4c0ef] |
| Original hooks | 5 | built from presenter principles plus your account only | prompt design | [721989c4c0ef] [14df3bb700a0] |
| Hide weak hooks | grade C or below not shown | presenter's coded setting | prompt design | [e9f81c60dc73] |
| Usable hooks from demo | about 7 to 9 across all channels | small analyzed set, conceptual topic | demo | [721989c4c0ef] |
| Ideal own-channel run | about 100 own videos analyzed, top 20 run, expect break point near 10, 12 or 15 | long-term setup | presenter's suggestion, not done in demo | [14df3bb700a0] |
| Competitors per analysis | 1 per run preferred | to avoid dilution | presenter's hunch | [fdd73f8bda1d] |

## 5. Diagnostics and checks

- Generic hooks from AI. Check: was the model given any real winning transcripts and metrics? Bad: a cold "write me hooks" prompt. Next: ground it in your own winners first (3.2). [a80ff986fd63]
- Suspect winners in the analysis set. Check: engagement rate on high-view videos. Bad: below about 2%, or near 0% as in the demo's Gamma post. Next: exclude it. If a known organic winner falls under the line, override and keep it (card caveat). [03d175f0d156]
- Winner line placement. Check: is there a clear drop-off in views in the top 10? Good: a visible gap (demo: after video 4). Bad: a smooth slope or a borderline case (demo: bonus footage, 4 or 5). Next: move the line when prompted, or add more videos. [ad297d96546e]
- Thin rubric. Check: how many winners fed each channel's analysis? Bad: 4 or 5 winners, as in the demo; the presenter says "imagine if you ... ripped 50 videos". Next: analyze the whole backlog. [ad297d96546e] [14df3bb700a0]
- Muddy or averaged principles. Check: are channels with very different styles (tight versus long-winded) in 1 run? Next: split into 1 competitor per run. [fdd73f8bda1d]
- Few hooks generated. Check: how many formats passed the topic-fit screen? Bad: most rejected (demo: 4 of 5 for Peter Visuals). Next: analyze more videos with formats that fit this kind of topic; do not force-fit. [721989c4c0ef]
- Draft hook grade. Check the line-by-line critique. The demo draft got a B with these faults: weak distillation, "this is how you" is soft, no specificity, no credibility anchor, second line "good but vague" and missing a concrete asset. Next: add a specific number, a concrete asset or a comparison (see rewrites in section 7). [e9f81c60dc73]
- Voice fit. Check: does a high-graded hook match your voice and length? The presenter rejected A-graded hooks that were too long or "rambly" for his style. Next: reject off-voice hooks regardless of grade. [fdd73f8bda1d]
- Hook opener self-check against the demo's shared patterns: specific or abstract? Payoff in the first sentence or delayed? Declarative or hedged question? Throat-clearing opener? Stat alone or stat plus a second-sentence amplifier? [38a495e39205]

## 6. Tools, settings and named features

- Sandcastles: social video analysis tool. Watch list of channels; database of channels with backlog scraping; live-add for missing channels; web app with manual and bulk analysis; CSV export; credits for deep analysis (about 1 per video); Pro tier named as the minimum. Presenter says scraping, metrics and captions are free and unlimited. `[verify UI]` `[web check: plans, credit price, free scraping claim]` [728fcae3dec6] [cfa4e7c04581]
- Sandcastles MCP: connects Sandcastles to Claude so Claude can tell Sandcastles what to do. About 24 tools; named ones: channel recap, analyze, credit, hooks, format. `[verify UI]` [cfa4e7c04581]
- Claude Desktop app: required to run Cowork or Code. Shows a progress tab in the upper right with the project plan. `[verify UI]` [728fcae3dec6]
- Claude Cowork project: holds the rubric so you can reuse it without rerunning the full flow. `[verify UI]` [728fcae3dec6]
- Hook Machine prompt and Claude skill file: free, linked in the video description, not in this source. [728fcae3dec6]
- Apify: named as the lightweight alternative that scrapes metrics and captions only; the presenter says it gives surface-level results. [cfa4e7c04581]

## 7. Examples and case results

All are from 1 demo run. They are examples, not promises.

Demo run: own channel plus Peter Visuals (faceless, case-study format), bonus footage (newer, "growing fast", long-winded), Brier (long-winded). 40 videos, 34 already analyzed, 6 analyzed live. Winners: 4, 5, 4, 4. [728fcae3dec6] [ad297d96546e]

Topic "dopamine ladders", generated hooks and the presenter's reaction: [721989c4c0ef]
- Own-format: "Here's how to release six levels of dopamine in 60 seconds of video." He did not love it.
- Own-format: "Dopamine driven content is outperforming everything else. So here's the easiest framework for triggering six layers of it." He "kind of" liked it.
- Peter Visuals format (the 1 that fit): "One level of dopamine is bad for attention. Three levels is good, and six levels is what makes people addicted." "That might actually work."
- Bonus footage format: "I studied 200 of the most addicting videos on the internet, but a comment said, 'You're overthinking it.' And the truth is, they all hit the same six dopamine triggers I now use in every script." Something there, but long-winded.
- Bonus footage format: "If you force me to make your next video addictive in six steps, [this] is exactly what I would do." Decent.
- Bonus footage format: "How to turn any boring topic into an addictive video because dopamine driven hooks are on fire right now." He would skip it.
- Brier format: "If you held a gun to my head and said you had to make a video addictive in the next 24 hours, I'd basically give you my six level dopamine ladder." Could work for a "yapper", too long for him.
- "For dopamine hooks, single trigger is D-tier. Nobody actually stays for one trigger anymore." He did not love it.
- "I have bad news for all of you who copy hook templates. Single trigger hooks are dead in 2026 because dopamine has gone multi-layered." He did not love it.
- Originals he rated "pretty good": "There are six levels of dopamine your brain hits while watching a video, and most creators only trigger one of them." and "Most creators trigger one type of dopamine in a video. The viral ones trigger six."
- Original with "something good": "Some videos release six types of dopamine in under a minute. That's why they feel impossible to stop watching."
- Originals he disliked: "Addictive videos don't have one good hook. They have a dopamine ladder and there are exactly six rungs." (did not love "exactly six rungs") and "Six levels of dopamine separate the videos people watch from the videos people can't stop watching." ("like a good tweet", not a hook).

Draft grading example: [e9f81c60dc73]
- Draft: "This is how you get people actually addicted to your content. It's called dopamine ladders. And once you learn it, you'll never look at content the same way again." He expected B- or C+. Grade: B.
- Critique: line 1 weak distillation, "this is how you" soft, no specificity, credibility anchor none; line 2 good but vague, missing a concrete asset.
- Rewrite 1: "This is how you get people actually addicted to your content. It's called dopamine ladders, and there are exactly six rungs." Stronger because specific.
- Rewrite 2: "Most creators trigger one type of dopamine in their videos. The addictive ones use a six-level ladder." His favourite; "I would use that one in my video."
- Rewrite 3: "I studied 200 of the most addictive videos online, and they all do the same thing: climb six rungs of a dopamine ladder." "Something interesting there."
- Note: the favourite hook uses a contrast between most and the best, plus a specific number, matching the specificity and 2-sentence amplifier patterns in 2.14. Note also that "200 videos studied" is a claim the model wrote; do not use invented proof in real copy.

## 8. Mistakes the source warns about

1. Asking a cold AI chat to "write me hooks". Output is generic. [a80ff986fd63]
2. Copy-pasting a viral hook from a distant niche. Psychology, format and grammar do not transfer. [a80ff986fd63]
3. Studying boosted or brand-deal videos as organic winners. Paid spend inflates views. [03d175f0d156]
4. Mashing all channels into 1 pool. Each creator's winner and loser signal gets lost. [ad297d96546e]
5. Adding many competitors to 1 analysis. Insights dilute to the average. [fdd73f8bda1d]
6. Forcing a format onto a topic it does not fit (for example a case-study stat hook onto a concept with no stat). [721989c4c0ef]
7. Relying on caption and view scraping for hook principles. It ranks videos but cannot explain them. [cfa4e7c04581]
8. Analyzing too few videos. Fewer winners means fewer usable formats and a thinner rubric. [14df3bb700a0]
9. Rerunning the whole flow for every new topic. Burns tokens; reuse the rubric in a thread or Cowork project. [728fcae3dec6]
10. Wasting credits on off-topic videos such as personal vlogs. Tell the tool to ignore them. [728fcae3dec6]
11. Trusting a high grade over your own ear. Several A-graded hooks were rejected for length or voice. [fdd73f8bda1d]

## 9. Caveats, conflicts and what is missing

- Conflict of interest: the presenter sells Sandcastles credits. Claims that deep analysis is required, that Apify is surface level, and that scraping is free and unlimited are product positioning. [cfa4e7c04581]
- Missing: the 8 universal hook principles are named but never listed. Only a few of the 11 custom principles are stated. The Hook Machine prompt, the skill file, the grading scale definitions and the MCP setup steps are not in the text. An operator cannot rebuild the rubric from this source alone. `[web check: prompt and skill file from the video description]`
- Missing: how "engagement rate" is calculated for the 2% rule, and how the break point is computed (the model "noted a natural break point"; no formula). [03d175f0d156] [ad297d96546e]
- Organic versus paid: the whole demo is organic creator content ranked by views. For paid ecommerce ads, views mostly follow spend, so a view break point would rank budget, not hooks, and the 2% brand-deal screen has no meaning when every ad is paid. The cards propose running this on your own ad creative, but the source never shows that. A paid-ad version would need spend-normalized ranking (for example hook rate, CTR, cost per purchase, ROAS) instead of raw views. This substitution is not from the source. `[needs brand data: ad-level transcripts plus spend, hook rate, CTR and purchase metrics per ad]` [a80ff986fd63] [ad297d96546e]
- Common ecommerce advice conflict 1: many ad-copy guides recommend question hooks and call-out questions. This source's model finding is "confident declaratives beat hedged questions" across 3 creator channels. That is 1 run on content-marketing creators, not product ads. Test before adopting for a brand. `[needs brand data: question versus declarative hook results in own ads]` [38a495e39205]
- Common ecommerce advice conflict 2: swipe files of other brands' winning hooks are standard practice. This source says cross-niche copying usually fails and within-niche copying should be reskinned, not cloned. The two agree once the swipe file is limited to close competitors and used for format, not wording. [a80ff986fd63] [721989c4c0ef]
- Evidence is thin: 4 or 5 winners per channel, 1 topic, 1 draft graded, reactions from the presenter only, no performance test of any generated hook. The "sinks 50%" and "about 60%" figures are model outputs on 10 videos per channel, not measured lifts. Treat them as hypotheses. [38a495e39205]
- The dilution warning (2.8) is explicitly a hunch ("I have a feeling"). [fdd73f8bda1d]
- Letter grades are the presenter's coded criteria, not an external standard. A B from this rubric says nothing about ad performance until tied to results. [e9f81c60dc73]
- Model-written hooks can include invented proof (for example "I studied 200 of the most addicting videos"). For brand copy, strip or verify any claim, number or credential the model adds.
- Tool details (Pro tier, credit per video, 24 tools, 2-minute setup, Cowork, progress tab) are dated to 2026 and can change. `[verify UI]` `[web check: Sandcastles and Claude Desktop current features]`
- Cost: 100 own videos at about 1 credit each is real spend; the source gives no money price per credit. `[web check: credit price]` [14df3bb700a0]

## 10. Card index

- a80ff986fd63  Why Cold AI Hooks Fail (and the Copy-Paste Fallback Also Fails)
- 728fcae3dec6  The Four-Step Hook Machine Workflow
- 03d175f0d156  Filter Brand Deals Out of Hook Analysis With a 2% Engagement Floor
- ad297d96546e  Find the View Drop-Off Break Point to Separate Winners From Losers
- 38a495e39205  Extract Hook Principles in Four Buckets (Psychology, Framing, Grammar, Non-Obvious)
- fdd73f8bda1d  Don't Cross-Pollinate Creator Styles in One Analysis
- e9f81c60dc73  Build a Custom Hook Rubric From Data, Then Grade and Rewrite Draft Hooks
- 14df3bb700a0  Analyze Your Own Backlog First, Competitors Second
- 721989c4c0ef  Use Topic-Format Compatibility Screening Before Generating Hooks
- cfa4e7c04581  Prefer Transcript-Based Analysis Over Lightweight Caption Scraping
