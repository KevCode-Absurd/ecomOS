# Claude Code Website Masterclass: How I Got 20% Conversions (10x The Average)

source_id: 138QqvbshfkmK9XIwu-Hm8f3uRYqy2tJ6  |  folder: /07-LPG-landing-pages  |  cards: 32  |  words: 15,255  |  type: transcript (YouTube screen-share masterclass)

credibility: The presenter is Jonno Catliff (his name is read out in the speed-to-lead demo call). He built a wedding DJ business, then added photo and video services, grew it to "seven figures" and sold it. He now runs an AI automation agency and sells a paid community; a free community holds his claude.md file, prompts.md file and the full demo project. His evidence: his own ad account ($171,000 spent on 1 of 3 campaigns), an SEO campaign with 1,500 clicks a day, his own analytics showing a 20% landing-page conversion rate, $1.2M made, and single-case before and after numbers. He cites 2 "found on Google" stats that he says he does not fully trust. No sample sizes or test durations are given. All results are lead-generation (form fills and calls) for a local service business, not ecommerce purchases.
date signals: File modified 21 Sep 2026. Names Claude Code as a plugin inside Google's Anti-Gravity desktop app, Claude routines, PostHog with its install wizard and MCP connection, Vercel with a Next.js preset, GitHub, Dribbble, Lighthouse in Chrome developer tools, Twilio, Calendly, Zapier, Make, n8n, Trustpilot, Google Lens, "This Person Does Not Exist". Note: the export header scopes this document to 06-MEA (measurement) and lists Vercel, GitHub, Anti-Gravity and environment-variable walkthroughs under "Skip". The document sits in 07-LPG, and this task asks for every build step, so those steps are included in section 3 and marked `[verify UI]`.

## 1. What this source is for

It helps an operator build a lead-generation landing page with an AI coding agent, load it with the page elements the presenter ranks as "S tier", scale it into many keyword-matched pages, make it fast and mobile-safe, and then measure it with a thank-you page, a PostHog split test, heatmaps and session recordings. It also covers speed-to-lead: calling a new lead within about 10 seconds. For ecommerce, the page rules (proof, offer, CTA, speed, mobile, message match) transfer; the form, phone and speed-to-lead parts apply mainly to high-ticket, quote-based or service offers. Several cards are "merchant adaptations" that translate the lead-gen rules to a store; they are marked as such below.

## 2. Principles

1. **The only goal of a website is to make money.** It does that by generating leads (this source) or selling products (a Shopify store). A low-converting page is a bottleneck that wastes all acquisition spend. Source says: if your page converts at 10x a competitor's on the same Google Ads campaign, the competitor pays 10x as much per customer. [cb722cd52538]
2. **Design is a binary trust check, not the main lever.** Source says "beautiful websites make you zero dollars". A visitor decides in about 50 milliseconds whether the page looks trustworthy enough to keep reading or looks like a scam. Good design does raise conversion, but it is not the primary metric; "a lot of ugly websites make a ton of money". His 20% page was not especially beautiful. Clear the trust bar with a reference design, then spend time elsewhere. The 50 ms figure is his statement, not a cited study. [8d4d6395709d]
3. **Less copy is more, except for SEO pages.** Visitors read about 10% of the text: headline, subheadline, second subheadline, 3 bullet points, maybe one more line. If everything is visible, the visitor picks which 10% they read; you want to pick it. For pages that must rank, the source targets 1,500+ words and hides the extra text in accordions or dropdowns so it is on the page but only seen on click. Heuristic, not a tested number. [de1cd5d08ee6]
4. **Sell benefits; features are how buyers rationalise.** People buy emotionally and rationalise logically. Benefits are: saving time, earning money, pain aversion, peace of mind or comfort, status, freedom. Nobody pays $500,000 for a Ferrari for the leather seats; they buy status and justify it with the build. Builders love their tech stack; buyers do not care. "Outcomes never change. Business tools always rotate." Example: "the top 1% of DJs out of 5,000" is a peace-of-mind benefit, not a staffing stat. [9b3e679ad878] [de1cd5d08ee6] [cb722cd52538]
5. **Ad pages have one job: kill the navbar and the footer.** Applies to pages for Google Ads, Facebook ads "or anything that's just really not SEO". Every click to an about page or terms page (unless legally required) lowers the chance the visitor converts. If you pay $10 for a lead, you do not want to pay $10 for them to read your about page. Only 2 actions count: call or fill the form. Does not apply to SEO or exploration pages (card caveat). Merchant adaptation: on a store campaign page, keep delivery, returns, support and required policy access; test navigation removal on campaign traffic only and do not remove normal store navigation by default. [cb722cd52538] [511b0c6e9e86]
6. **The form (and phone number) must be on the page.** Source calls this mandatory. Do not make visitors hunt for a contact page; bounce rate rises when they cannot find what they want. [cb722cd52538] [383e8651cc0e]
7. **Two devices, two CTA rules.** Desktop: sprinkle CTAs down the whole page so a visitor who has "read enough" can act at that moment; each CTA jumps to the form. Mobile: his page has only one CTA, pinned to the bottom of the screen, visible while scrolling, and it jumps straight to the form. No CTA density number is given. [622577c84cdc]
8. **Page elements are added over time.** Source says you will not get most of them done in 2 hours; they are added incrementally as the business gets testimonials, reviews and case studies. The page is "a living project". [4435f3fae23c] [45546f922308]
9. **The founder video is "the biggest non-negotiable".** Sell yourself, not the service. People do not want to buy from a faceless brand; they want to see, like and trust the person. A bad video hurts conversion. [cbc6126cdb67] [b32f8041f945]
10. **Video testimonials are non-negotiable; written testimonials are not trusted.** Source says most people no longer trust written testimonials: they may be written with AI in seconds, and faces can come from "This Person Does Not Exist" or stock photos (a reverse search with Google Lens shows the same stock face on thousands of sites). Presence alone adds peace of mind, even if few visitors press play. Self-shot phone clips often do better than studio clips because they do not look staged. Written testimonials still beat nothing, and read as legit when paired with video. He calls this his "personal bias". [4435f3fae23c] [05575fd44bd3]
11. **The best indicator of future performance is past performance, and the best indicator of past performance is social proof.** His finished page has little text and is "mostly social proof". [4bc5cc0e725e] [4435f3fae23c]
12. **Portfolio is close to binary for visual services.** For a wedding photographer, visitors will not inquire without a portfolio they like. Not required for every business. Merchant adaptation: show real examples of the relevant product variant (furniture, decor, custom products) with scale, materials and variations clear, placed near the purchase decision and matched to the ad promise. [e90da6b10562]
13. **Case studies: specific beats vague.** Add them in B2B; not necessarily needed in B2C. Give before and after numbers and a time period. Merchant adaptation: use a real customer or product test with a measured before-and-after where the category supports it, state the period, conditions and limits, and never reuse agency revenue results as product proof. [e03cd7999ee5]
14. **FAQ is an objection-handling block.** Not "BS" text added because you do not know what to put, unless it is SEO filler. Ask what stops a visitor: price, business model, something ambiguous. Harvest objections on sales calls by asking "was anything ambiguous?"; they will tell you. Add answers so the next 10,000 visitors can get past it. No lift number given. [3f57d3484974]
15. **Phone callers are in "get it done" mode.** They are not in research or planning mode; they want an answer now. So calls may convert higher than forms. The presenter says this is his own reasoning and he is "not 100% sure"; he shows a Google-found stat he does not trust. [383e8651cc0e]
16. **Borrowed authority and external proof raise trust with modest effort.** Logos of real past clients, external review badges (outside your control, so more credible), and trust stats. He rates these as "lesser points" than video, testimonials and offer. [4bc5cc0e725e]
17. **Offer design: a "golden formula" when the outcome is concrete.** "We will [verb] your [metric] by [number] in [time frame] or [risk reversal]." Works best when you sell something hyper concrete (leads, sales). He does not know how to apply it to landscaping and says it "doesn't always work". Otherwise, name the few things the buyer really wants and promise those. Rotate and test promises. Merchant adaptation: name the product, benefit, contents and price; use a quantified or time-bound benefit only when product evidence supports it; state the real guarantee and returns terms; do not invent guaranteed outcomes. [2602a57feb17] [9b3e679ad878]
18. **Message match across the whole journey (the "zipper").** Build one page per city x service. A searcher for "tree trimming in Toronto" skips results about tree removal or "trees in Toronto". The search result, the page headline, the follow-up text and the sales call must all use the same keyword. "They're not looking for a proxy." Source calls this "fundamentally game-changing" for him. [ca6dfd85e131]
19. **More pages means more shots.** One page is one basketball shot; 500 pages are 500 shots. Covers both SEO and ads ("you want to create ads for everything"). But ramp SEO pages slowly: do not create 1,000 or 2,000 pages in a day or Google "will penalize you". No safe rate is given. [ca6dfd85e131]
20. **Mobile first.** Source says about 64% of visitors are on mobile, 3% tablet, 33% desktop. A page broken on mobile misses 64% of your shots; he calls ignoring this "a rookie mistake". His figures, not universal. [38729fdb61c9] `[needs brand data: own device split from analytics]`
21. **Page speed is a conversion problem, not a technical nicety.** Cited study (unnamed): 1-second load converts at 3.05% on average; 2 seconds cuts that by half; 3 seconds cuts it by roughly another third to half; 4 seconds halves it again, leaving about 20% of what a fast page would get. He wants 1 second and says "definitely not longer than 4 seconds". Main culprits: images, videos and large graphics. [4d6326770c4b] [fdc8482e2d86] `[web check: the original load-time study behind 3.05%]`
22. **Nobody can hand you a 20% page; only data can.** "You can implement everything we just talked about and still not crack a 5% conversion rate." No roadmap exists. The 20% page came from testing "40, 50, 60 landing pages". Data "doesn't lie"; it says when a page is bad or great. [e4ed90b85412] [2f79f41a6063]
23. **Split tests beat session recordings as evidence.** Source finds A/B tests "way more interesting" because enough runs give a statistically significant winner. Recordings are for spotting anomalies: things people consistently get wrong. [d77e97941d57] [075c7f2d2c43]
24. **You are too close to your own page.** After 10 hours of building, a page feels intuitive to you but can be "a maze" to a first-time visitor. Heatmaps show the outsider's view. [d77e97941d57]
25. **A good landing page is a multi-year asset.** His winners converted for 5, 6 or 7 years; a found winner can "run for the next 10 years". It is an upfront investment "that pays you dividends". His experience, not a measured lifespan. [45546f922308]
26. **Speed to lead: call within the same minute.** Leads want an answer in 1 minute, not 5 days. Source says "the data is pretty conclusive": calling in the same minute can yield 4x the sales, with no extra marketing spend or work. Calling 30 minutes later hits voicemail and leads to about 10 more calls that also hit voicemail. No source for the 4x is named. [383e8651cc0e] `[web check: speed-to-lead study behind the 4x claim]`

## 3. Procedures

### 3.1 Set up the build environment `[verify UI]`
1. Download Anti-Gravity, a free Google desktop "coding workspace". No coding skill needed, per the source.
2. In the left sidebar, open the plugin section, search "Claude Code", install it. Claude Code needs a paid Claude plan. Free alternative: the agent builder inside Anti-Gravity, which comes with some free credits.
3. Create a project folder (his: a master Claude Code folder, then a subfolder "CRO-brief"). Open it in Anti-Gravity.
4. Add a `claude.md` file to the folder. His version comes from his free community. It tells Claude how to behave, "like training a new employee". The source does not show the file's contents.
5. Optional: `git clone` his full demo project from the community link instead of building from scratch.

### 3.2 Build the first page from a reference design
1. Open the Claude panel and prompt: "Can you please build me a one-page website for my landscaping business? I want to upload an image of an example design and I want you to replicate it for me."
2. Find a reference design on dribbble.com (free, human-made designs). Search the niche, e.g. "landscaping website", and pick one you like.
3. Screenshot or save the image; upload it with the "+" button, "Upload from computer". Send.
4. Open the localhost link Claude returns. If none appears, ask: "Can you give me the link so that I can view the site?"
5. Purpose: clear the trust bar quickly. Do not spend most of your time here. [8d4d6395709d]

### 3.3 Add the conversion elements in one prompt
1. Paste the element prompt from his `prompts.md` file (contents not shown in the transcript; the source is thin here).
2. His "after" page contains: clickable phone number; trust stats; external review badges (demo: Trustpilot with 67 reviews); founder video; client logos; CTAs throughout; shorter copy with lists; video testimonials; written testimonials; before-and-after; FAQ (Q&A); form on the page. Missing in his demo: portfolio.
3. Check the page against the tier list in 4.2. Adjust layout and structure to taste.
4. Only show assets you really have: a Trustpilot badge needs a real Trustpilot account with reviews. [4bc5cc0e725e] `[needs brand data: real reviews, logos, stats, testimonials, founder footage]`

### 3.4 Record the founder video
1. Keep it to 45 seconds. His own ran longer; he says that was too long because people get bored and tune out.
2. Suggested flow (not a fixed script): quick intro, some social proof, results, 3 reasons to choose you, a call to action, optional risk reversal (e.g. money back in the first week if they do not like the service).
3. Sell yourself, not the service list.
4. Expect many takes: "it might take you 50 times". Take a full day if needed.
5. For a professional background without an office, he rented a WeWork co-working space on a Saturday.
6. Card additions not in the transcript: place it below the headline and above the form, use a still thumbnail, no autoplay with sound, keep the file small to protect load time, add a text summary, A/B test with and without. Treat as card-author advice. [cbc6126cdb67] [b32f8041f945]

### 3.5 Collect video testimonials
1. Ask real clients to film a genuine 30-second testimonial on their phone. No studio.
2. Aim for a set; he used 9.
3. Expect that many visitors will not watch; presence still helps.
4. If you cannot get video, use written testimonials; pair them with external review sources.
5. Expect it to feel awkward to ask ("will make your skin crawl"). He says do it anyway. [4435f3fae23c] [05575fd44bd3]

### 3.6 Build the FAQ from sales calls
1. List what could stop a visitor: price, business model, unclear process, anything ambiguous.
2. On every sales call, ask "Is there anything you felt ambiguous about?"
3. Write answers that remove those objections. Update the FAQ as new objections repeat.
4. Keep the FAQ collapsed (card advice, consistent with principle 3). [3f57d3484974] `[needs brand data: objections from sales calls, support tickets or reviews]`

### 3.7 Add click-to-call and call tracking
1. Add a tappable call link, not just a printed number, so a mobile visitor is calling within seconds.
2. For attribution, buy a separate phone number per page and track which number rang.
3. Use a VoIP number, bought from Twilio or, more commonly, through your CRM (Twilio sits behind most CRMs). It works from computer, phone or web app, and separates work calls from personal calls.
4. Route: landing page, then VoIP, then your phone. [383e8651cc0e]

### 3.8 Multiply pages with a skill (the "zipper") `[verify UI]`
1. Keep one homepage as the root. Branch landing pages off it.
2. List both sides of the zipper: cities or regions (Toronto, Vancouver, Montreal, Calgary; or Manhattan, the Bronx within New York) and services (tree trimming, landscaping, snow removal).
3. Rewrite the headline to the exact keyword. His on-the-fly edit: "Tree trimming services made easy in Toronto".
4. Prompt Claude to turn the page into a skill called `/landing-page-generator`. A Claude Code skill is an on-demand workflow.
5. Run it in a new tab with inputs: service, city and traffic source. Demo: "New York, landscaping, Google Ads".
6. Match the follow-up: text "I saw you're looking for a tree trimming quote in Toronto", and open the call the same way.
7. Ramp SEO page volume slowly; do not publish 1,000 pages in a day. The skill can run daily "or whatever cadence". [ca6dfd85e131] `[web check: current Google policy on scaled or programmatic pages]`

### 3.9 Mobile check `[verify UI]`
1. In Chrome: three dots, More tools, Developer tools.
2. Click the device toolbar icon to enter responsive mode.
3. Switch between iPhone, tablet and desktop presets.
4. Set "Responsive" and drag the handle slowly to see every width.
5. If a width looks broken, have the agent fix it. Card additions: confirm the pinned mobile CTA stays visible and works, the form is usable one-handed, nothing overflows. [38729fdb61c9] [622577c84cdc]

### 3.10 Speed fix loop with Lighthouse `[verify UI]`
1. Chrome: three dots, More tools, Developer tools, then the ">>" arrows, then Lighthouse.
2. Run a report. It scores 4 areas: performance, SEO, accessibility, best practices.
3. Open all performance diagnostics. Items he shows: minify JavaScript, reduce unused JavaScript, render-blocking requests, improve image delivery, network dependency tree, LCP request discovery, legacy JavaScript, use efficient cache lifetimes.
4. Select and copy the whole report. Paste into Claude with: "Here's the Lighthouse report. Can you optimize for page load speed? And can you also optimize for desktop, tablet and mobile devices?"
5. Re-run Lighthouse. His demo went from 90 to 95.
6. If not 100, paste the new report: "We're at 95%, get this to 100%." Repeat until you reach your target. [4d6326770c4b]
7. Card additions not in the transcript: compress and size images, defer non-critical scripts, remove unused tags and fonts, test on throttled mobile. [fdc8482e2d86]

### 3.11 Install PostHog `[verify UI]`
1. Go to posthog.com, "Get started", sign up with email, pass security checks.
2. Create an organisation. In onboarding he picked "understanding behavior".
3. Copy the install command PostHog shows.
4. Open the terminal in Anti-Gravity (not the Claude chat) and paste it; press Enter. This starts the PostHog wizard. Press Enter again.
5. Confirm and authorise the account in the browser (he used an incognito tab because he was signed in elsewhere).
6. Wait about 8 minutes. Connect the MCP when offered. If stuck, ask Claude Code to walk you through it.

### 3.12 Add the thank-you page and tracking (his "prompt number 5")
1. Prompt Claude to (a) add a thank-you page the form redirects to, (b) optionally embed a calendar booking widget (e.g. Calendly) so leads can book a sales call at once, (c) add PostHog tracking to the homepage and all pages, (d) add heatmaps.
2. Two ways to count a conversion: track the form-submit event (more complex; Claude can do it) or track arrival on the thank-you page (easier). He uses the thank-you page.
3. Conversion rate = form fills / page visitors. Example: 10 fills / 100 visitors = 10%.
4. Merchant adaptation: for quiz or email signup, fire a named completion event only after a successful submit, or use a confirmation page; deduplicate reloads; validate with test submissions. Track purchases separately via order confirmation and a stable order id. Purchase conversion = purchasing sessions / eligible sessions. Compare revenue and contribution margin per visitor by channel and variant. [a835b362c4f5] [8dcda9c4f61d] [2296ba94b6ea] [9ffcba120b24]

### 3.13 Create the split test in PostHog `[verify UI]`
1. Click "+", search "Experiments", create a new experiment. Name it.
2. Optional: write a hypothesis, e.g. "page A will do better".
3. Split traffic evenly: 50/50 for 2 pages. You can add more variants and split evenly (his concept example: 3 pages at 33% each).
4. Add a primary metric: "single use" funnel, name optional, event "quote submitted".
5. If "quote submitted" is missing: (a) submit the form once yourself so the event exists; (b) add an authorised URL: "+", Settings, Web analytics, add authorised URL.
6. Authorised URL rules: root domain only; remove any subpage path and the trailing "/"; "http" without "s" is normal on localhost; check the port (3000 by default; 3001, 3002, 3003 are possible).
7. Restart the experiment setup if needed, re-add the metric, create, "Save as draft".
8. Copy the code snippets PostHog gives for control and test. Which page is "control" is arbitrary; he used the homepage as control and "version 2" as test.
9. Prompt Claude: "I need to add tracking to pages in PostHog. Control is the home page, test is page 2", then paste each snippet under its label.
10. Click "Launch".
11. Test routing in an incognito window. PostHog sets a cookie, so a normal browser keeps showing the same variant. Close and reopen incognito to see both.
12. Submit the form in each variant to check the conversion registers.
13. Refresh results manually: data can take about 30 minutes to update.
14. When a loser is clear, rotate it out, make the winner the new control, add new challengers. Repeat. [a835b362c4f5] [2f79f41a6063] [4239f2807a97]

### 3.14 Watch sessions
1. PostHog records sessions by default once installed. Open the Activity tab to view each visit.
2. Note any action you do not want (repeated misclicks, dead ends, form confusion), change the page, then check it stops happening. [d77e97941d57] [075c7f2d2c43]

### 3.15 Speed-to-lead automation
1. Prompt Claude: when the form is submitted, send first name, last name, email and phone to a webhook URL.
2. In the automation behind the webhook: create a CRM contact, assign it to a rep, trigger an automated call.
3. The call rings the rep first: "you have a new lead, press any key to connect". Pressing a key dials the lead. His demo connected in about 10 seconds.
4. Alternatives: send a text or Telegram message to yourself and call by hand at once. Tools named: Zapier, Make, n8n, Claude routines, or direct to the CRM. "The outcome doesn't change": call immediately.
5. Test with dummy data before going live. [383e8651cc0e]

### 3.16 Deploy live: GitHub then Vercel `[verify UI]`
1. Why: a localhost:3000 site runs only on your computer; nobody else can visit, and PostHog heatmaps do not work on localhost.
2. Create a free GitHub account. Repositories, New. Set it to private (his advice). Create.
3. Copy the setup command GitHub shows. Paste to Claude: "Can you please upload the entire project to GitHub for me?"
4. Create a free Vercel account. New project. Connect GitHub. Import the repository.
5. Set the application preset to Next.js.
6. Add the environment variable that reconnects PostHog. Open your local env file (his: ".env.local" or similar): text before "=" goes in Key, text after "=" goes in Value. Needed because `.gitignore` keeps secret keys out of GitHub. Never commit keys.
7. Deploy (he says about 60 seconds; elsewhere "about 10 seconds" for the build). Open the live link.
8. Optional: buy a domain in Vercel or import one from a provider such as GoDaddy. [7091bbdbaa48]

### 3.17 Heatmaps on the live site `[verify UI]`
1. PostHog: Settings, Web analytics, add the deployed Vercel URL as an authorised URL. Save.
2. Open Heatmaps, create new, enter the URL, pick "screenshot" (or "iframe"). He used screenshot.
3. Review where people click and what they do. Use it to find friction you could not see as the builder. [d77e97941d57]

## 4. Rules, thresholds and numbers

### 4.1 Table

| rule | number or threshold | condition | source's basis | card id |
|---|---|---|---|---|
| Presenter's landing-page conversion | 20% | lead form fills, local services, Google Ads plus SEO | own analytics; example, not a target | [cb722cd52538] [e4ed90b85412] |
| "Average worldwide" conversion | 2% to 4% | his claim; 20% puts him in "top 1%" | no source named | [cb722cd52538] |
| Lead-to-customer close rate | 6% to 8%; Google Ads and SEO at the high end (8%) | form fill to paying customer, his business | own data | [383e8651cc0e] |
| First impression time | about 50 ms | trust or back out | stated, not cited | [8d4d6395709d] |
| Share of copy read | about 10% | headline, 2 subheads, 3 bullets, 1 more line | his heuristic | [de1cd5d08ee6] |
| SEO page length | 1,500+ words | only pages meant to rank; hide in accordions | his heuristic | [de1cd5d08ee6] |
| Founder video length | 45 seconds max | his own ran over; says that was too long | opinion | [cbc6126cdb67] |
| Founder video lift | 10% to 15% conversion; he calls it "33% more leads" | one page, one case | own result; see arithmetic note in 9 | [cbc6126cdb67] |
| Founder video takes | up to 50 | normal to need many | opinion | [cbc6126cdb67] |
| Video testimonial length | 30 seconds, phone-shot | real clients | opinion | [4435f3fae23c] |
| Video testimonial count | 9 | his photo/video business | own case | [4435f3fae23c] |
| Video testimonial result | cost per conversion $200 to $30 ("7x decline") | separate Google Ads account | own case; example | [4435f3fae23c] |
| Reviews stat he distrusts | "270% more likely" with 5+ reviews | found on Google; he calls it "kind of BS" | none | (transcript only) |
| Star rating that looks real | 4.7 to 4.9 beats 5.0 | 5.0 reads as no reviews or hidden ones | opinion | [4bc5cc0e725e] |
| Device split | 64% mobile, 3% tablet, 33% desktop | his figures | cited on screen, unnamed | [38729fdb61c9] |
| Load time: 1 s | 3.05% average conversion | cited study | unnamed study | [4d6326770c4b] |
| Load time: 2 s | conversion halves | cited study | unnamed study | [4d6326770c4b] [fdc8482e2d86] |
| Load time: 4 s | about 20% of the 1 s result | cited study | unnamed study | [4d6326770c4b] |
| Load target | 1 s ideal; never over 4 s. Card sets "under 2 s" | all pages | source plus card interpretation | [fdc8482e2d86] |
| Lighthouse demo | 90 to 95; iterate toward 100 | performance score | own demo | [4d6326770c4b] |
| Speed to lead | same minute = up to 4x sales | leads who inquire | "the data", unnamed | [383e8651cc0e] |
| Auto-call connect time | about 10 seconds | webhook, CRM, auto-dial | own demo | [383e8651cc0e] |
| Pages tested to find winner | 40 to 60 | over years | own experience | [e4ed90b85412] |
| Winner lifespan | 5 to 7 years ("next 10 years") | with ongoing iteration | own experience | [45546f922308] |
| Split | 50/50 for 2 pages; 33/33/33 for 3 | even random split | method | [2f79f41a6063] |
| Example variant rates | 7.1%, 11.4%, 19.6% | illustration of a 3-way test | illustrative | [2f79f41a6063] |
| PostHog data lag | about 30 minutes | refresh manually | own experience | [2f79f41a6063] |
| PostHog setup time | about 8 minutes | install wizard | own demo | (transcript only) |
| Vercel deploy time | about 60 seconds | after import | own demo | [7091bbdbaa48] |
| Local port | 3000 default; 3001 to 3003 possible | authorised URL must match | method | [a835b362c4f5] |
| SEO page ramp | not 1,000 to 2,000 in a day | programmatic SEO pages | Google penalty risk, no rate given | [ca6dfd85e131] |
| Ad spend context | $171,000 on 1 of 3 campaigns; 1,500 SEO clicks a day; $1.2M made | his previous business | own account | [cb722cd52538] |

### 4.2 His conversion tier checklist
- **S tier (non-negotiable):** video testimonials; form on the landing page; video of yourself talking (founder video); speed to lead; offer plus risk reversal.
- **Tiers A, B and C:** shown on screen only ("pause the video to read more"). The transcript does not list them. Do not assign tiers the source did not state.

## 5. Diagnostics and checks

| check | how | good | bad | next step | card |
|---|---|---|---|---|---|
| Trust at first glance | Look at the page cold for a few seconds, or ask someone new | Looks like a real, current business | Looks dated, broken or like a scam | Rebuild from a Dribbble reference; then move on | [8d4d6395709d] |
| What gets read | Read only headline, 2 subheads, 3 bullets | Those lines alone carry outcome, proof and next step | Key point is buried in body text | Cut text; move key claim up; hide SEO text in accordions | [de1cd5d08ee6] |
| Benefit vs feature | Mark each line as benefit or feature | Benefits lead (time, money, pain, peace of mind, status, freedom) | Tech stack or method leads | Rewrite lead lines as outcomes; move features lower | [9b3e679ad878] |
| Exit links on ad pages | Count links that are not form, call or required policy | 0 (lead page) or only policy, delivery, returns, support (store) | Navbar, footer, about, blog links | Remove on ad pages; test on campaign traffic | [cb722cd52538] [511b0c6e9e86] |
| Form reachable | Scroll the page | Form on the page; every CTA jumps to it | Separate contact page | Put form on page | [622577c84cdc] |
| Mobile CTA | Device mode, scroll top to bottom | One pinned CTA always visible, goes to form | CTA scrolls away or opens a section | Pin one bottom CTA | [622577c84cdc] [38729fdb61c9] |
| Layout at all widths | Responsive mode, drag width | No breaks at any width | Overflow, broken sections | Prompt agent to fix | [38729fdb61c9] |
| Speed | Lighthouse performance | Near 100; load near 1 s | Heavy images or video; over 4 s | Copy report to agent; repeat | [4d6326770c4b] |
| Proof mix | List proof on page | Video testimonials, founder video, real logos and stats, external badges | Only written reviews; stock faces; 5.0 with few reviews | Collect phone testimonials; add external badge | [4435f3fae23c] [4bc5cc0e725e] |
| Offer | Read the offer block | Concrete promise plus risk reversal | Vague "quality service" | Apply the formula or name the 1 to 2 real wants | [2602a57feb17] |
| FAQ | Compare FAQ to sales-call objections | Each answer kills a real objection | Filler questions | Rewrite from call notes | [3f57d3484974] |
| Keyword match | Compare search term, ad, headline, follow-up | Same term everywhere | Generic catch-all page | Generate a page per city x service | [ca6dfd85e131] |
| Tracking works | Submit test form in each variant, check PostHog | "quote submitted" registers in both | Event missing | Submit once; fix authorised URL and port | [a835b362c4f5] |
| Variant routing | Incognito, reopen several times | Both variants appear | Always the same page | Cookie pins you; use incognito | [2f79f41a6063] |
| Session anomalies | Activity tab recordings | No repeated misclicks or dead ends | Same mistake repeats | Document, change, re-check | [d77e97941d57] |
| Speed to lead | Submit dummy lead | Phone rings in about 10 s | Lead waits minutes or days | Webhook to CRM auto-call or instant alert | [383e8651cc0e] |

Merchant checks from adaptation cards: purchase conversion is measured on purchasing sessions, not form fills; quiz and signup events are deduplicated and kept apart from orders; sample size and stopping rules are set before a test; results are judged on revenue per visitor. [9ffcba120b24] [2296ba94b6ea] [e4ed90b85412]

## 6. Tools, settings and named features

| tool | use in source | notes |
|---|---|---|
| Anti-Gravity (Google) | Free desktop coding workspace hosting Claude Code | Plugin sidebar; built-in agent builder with free credits `[verify UI]` `[web check: Anti-Gravity availability and plugin support]` |
| Claude Code | Builds pages, applies prompts, fixes speed, installs tracking, creates skills | Needs paid Claude plan; `claude.md` sets behaviour; skill `/landing-page-generator` `[verify UI]` |
| claude.md, prompts.md | His behaviour file and element prompts | In his free community; contents not in transcript |
| Dribbble (dribbble.com) | Free human-made design references | Screenshot and upload to replicate |
| Chrome developer tools | Device toolbar and responsive mode; Lighthouse | Path: three dots, More tools, Developer tools `[verify UI]` |
| Lighthouse | Performance, SEO, accessibility, best-practices scores | Paste report into agent |
| PostHog | Experiments (A/B), primary metric, sessions (Activity), heatmaps, authorised URLs, MCP | Free tier; "Settings > Web analytics" for authorised URLs; screenshot or iframe heatmaps `[verify UI]` |
| Hotjar, Microsoft Clarity | Named as alternatives for recordings and heatmaps | He is "ambivalent" about the tool |
| GitHub | Private repo for the code | Copy setup command to Claude |
| Vercel | Hosting from GitHub; Next.js preset; env variables; domains | `[verify UI]` |
| GoDaddy | Example external domain provider | Import into Vercel |
| Calendly | Optional calendar embed on thank-you page | For instant booking |
| Twilio / CRM VoIP | Per-page tracking numbers; call routing | Twilio is behind most CRM calling |
| Zapier, Make, n8n, Claude routines | Webhook automation for speed to lead | Any tool works |
| Trustpilot | External review badge | Needs a real profile |
| Google Lens, This Person Does Not Exist | His examples of how fake testimonial faces are spotted or made | Reason he distrusts written testimonials |
| WeWork | Rented background for founder video | Saturday rental |

## 7. Examples and case results

All are the presenter's own single cases or illustrations. Not promises.
- **DJ business turnaround:** started with $10,000, spent down to about $2,000 and was "2 weeks away from being completely broke", then closed 10 deals and made the first $10,000 from Google Ads. Later grew to seven figures and sold. Example of persistence, not a method.
- **20% conversion page:** a wedding DJ lead page; "10 times higher" than his quoted 2% to 4% average. Not a store benchmark. [cb722cd52538] [e4ed90b85412]
- **Founder video:** page conversion 10% to 15% right after adding it. He frames it as "$10,000 a month becomes $13,333". [cbc6126cdb67]
- **9 video testimonials:** Google Ads cost per conversion $200 to $30 on a separate photo/video account. [4435f3fae23c]
- **DJ offer without the formula:** "We'll take care of everything. We have the top 1% of DJs out of 5,000. We remove the stress of planning so you can focus on having fun." Wants: no screw-ups (peace of mind), affordable. [9b3e679ad878]
- **Formula examples:** "We'll generate you 20 leads per month or your money back." "We'll increase your sales by 20% in 90 days or you don't pay a dime." [2602a57feb17]
- **Agency offer he is split-testing:** "In a free 30-minute call, we'll show you how to make your business up to 4 times more profitable with AI." Risk reversal variant: "We'll pay you $200 just for showing up." Result not given.
- **Case study specificity:** "before it was 3.1, we got it to 19.4, then increased revenue by X over a time period", plus a "3 more case studies" link. He had one specific and one vague case study on his own site and was fixing the vague one. [e03cd7999ee5]
- **Logos:** TD, Microsoft, McLaren, Samsung (his real clients). [4bc5cc0e725e]
- **Trust stats on his page:** events done, five-star rated, events per year. [4bc5cc0e725e]
- **Keyword page:** "Tree trimming services made easy in Toronto". [ca6dfd85e131]
- **Speed:** Lighthouse performance 90 to 95 after one paste-and-fix loop. [4d6326770c4b]
- **Speed-to-lead demo:** dummy form fill, rep's phone rang in about 10 seconds, key press connected rep to lead. [383e8651cc0e]

## 8. Mistakes the source warns about

1. Spending most of your time on beautiful design. [8d4d6395709d]
2. Over-explaining: walls of text let visitors pick the wrong 10%. [de1cd5d08ee6]
3. Selling the tech stack or features instead of outcomes. [9b3e679ad878]
4. Navbar and footer on ad pages; paying for clicks that go to the about page. [cb722cd52538]
5. Hiding the form on a contact page. [cb722cd52538]
6. Only one CTA at the end on desktop; no pinned CTA on mobile. [622577c84cdc]
7. A bad or long founder video; it lowers conversion. Going over 45 seconds. [cbc6126cdb67]
8. Studio-polished testimonials that look staged; relying on written testimonials alone; stock or generated faces. [4435f3fae23c]
9. Vague case studies. [e03cd7999ee5]
10. FAQ as filler text. [3f57d3484974]
11. Printed phone number with no tap-to-call. [383e8651cc0e]
12. A perfect 5.0 rating that looks filtered (opinion). [4bc5cc0e725e]
13. A generic catch-all page for a specific search. [ca6dfd85e131]
14. Publishing 1,000+ SEO pages at once. [ca6dfd85e131]
15. Ignoring mobile ("rookie mistake"). [38729fdb61c9]
16. Slow pages; images and videos are the usual cause. [4d6326770c4b]
17. Believing any checklist guarantees results; not testing. [e4ed90b85412]
18. Checking variants in a normal browser (cookie shows the same one). [2f79f41a6063]
19. Reading PostHog results without refreshing (about 30 min lag). [2f79f41a6063]
20. Whitelisting a subpage, trailing slash or wrong port. [a835b362c4f5]
21. Trying heatmaps on localhost. [d77e97941d57]
22. Committing secrets to GitHub; forgetting to add the env variable in Vercel so tracking breaks live. [7091bbdbaa48]
23. Calling leads 30 minutes later and chasing voicemail. [383e8651cc0e]
24. Trusting your own sense that the page is intuitive. [d77e97941d57]

## 9. Caveats, conflicts and what is missing

- **Arithmetic error on the founder video.** 10% to 15% is a 50% relative lift ((15 - 10) / 10). The source calls it 33% and "$3,333 on $10,000". 33% is the gain measured against the new rate (5 / 15). Whichever he meant, it is one case. Card [cbc6126cdb67] repeats "33%". Do arithmetic in code before quoting it.
- **"7x decline" is about 6.7x.** $200 / $30 = 6.67; the cost fell about 85%.
- **Speed numbers are loose.** The study is unnamed. At 3 seconds he says "almost halving or going down by a third again". The card sets "under 2 seconds" [fdc8482e2d86]; the source itself says "you want it to be 1 second" and "not longer than 4". The Topic header says "50% for every additional second", which the source only states for 1 to 2 and 3 to 4 seconds. `[web check: load-time conversion study]`
- **Card additions beyond the transcript.** Steps in [fdc8482e2d86] (compress images, defer scripts, throttled mobile), [cbc6126cdb67] (placement, thumbnail, no autoplay, text summary), [05575fd44bd3] (placement near CTA, specific claims), [f31e01f03e62] (scroll depth, rage taps), [4239f2807a97] (pre-set sample size) and [cb722cd52538] (split-test the stripped page) are sensible but come from the card writer, not the presenter.
- **Merchant adaptation cards.** [511b0c6e9e86] [b32f8041f945] [e90da6b10562] [e03cd7999ee5] [2602a57feb17] [e4ed90b85412] [8dcda9c4f61d] [9ffcba120b24] [2296ba94b6ea] translate lead-gen advice to stores. The source gives no ecommerce data.
- **No statistics method.** He says a split test "if you do it enough times is statistically significant". No sample size, duration or significance threshold. `[needs brand data: traffic and conversion volume per variant]` Low-traffic stores may not reach significance.
- **Lead conversion is not purchase conversion.** The 20% and the 2% to 4% "average" are form fills. Do not compare to store purchase rates. [9ffcba120b24]
- **Tiers A to C are not in the transcript.** Only the S tier is spoken.
- **prompts.md and claude.md contents are not given.** The build procedure cannot be fully reproduced from this source alone.
- **Two stats he distrusts himself:** the phone-versus-form comparison and "270% more likely with 5+ reviews". Treat as unverified.
- **Speed-to-lead 4x has no named source.** `[web check]`
- **Privacy and consent** for session recordings and call recording are not covered. `[web check: consent rules for session recording in target markets]`
- **Google penalty for mass pages** is asserted without a policy reference or safe rate. `[web check]`
- **Conflicts with common ecommerce advice:**
  - Removing nav and footer: common DTC practice keeps store navigation and footer policies on PDPs. The source limits this to ad pages; the adaptation card keeps delivery, returns and policy access. Test, do not default.
  - "Less copy": many DTC operators run long-form advertorials and sales pages for cold traffic. This source's short-page rule comes from local-service lead pages with high intent (search traffic). Match copy length to traffic temperature and test. `[needs brand data: scroll depth and engagement]`
  - Written reviews: ecommerce practice leans on review volume and star ratings; this source discounts written reviews in favour of video. His view is a stated personal bias.
  - Case studies "not needed in B2C" versus common ecommerce use of before-and-after and UGC results.
  - Click-to-call and speed-to-lead fit high-ticket or quote-based products; for most low-ticket DTC they are not relevant.

## 10. Card index

- cb722cd52538 Landing page composition for conversion
- fdc8482e2d86 Page load speed threshold: target under 2 seconds
- cbc6126cdb67 45-second founder video on the landing page
- 05575fd44bd3 Video testimonials as landing page proof
- 2296ba94b6ea Track product-quiz or signup completion separately from purchases
- 4239f2807a97 A/B test landing page variants with PostHog traffic splitting
- f31e01f03e62 Use heatmaps and session recordings to find friction
- 9ffcba120b24 Measure purchases separately from landing-page signups
- 8d4d6395709d Judge design as binary trust, not beauty
- de1cd5d08ee6 Write less: control the 10% visitors actually read
- 9b3e679ad878 Sell outcomes, let buyers rationalize with features
- 511b0c6e9e86 Reduce distractions on dedicated product campaign pages
- 622577c84cdc Place CTAs throughout the page and pin one on mobile
- b32f8041f945 Use a short founder video to explain product credibility
- e90da6b10562 Show examples of visually differentiated products
- 3f57d3484974 Turn FAQ into an objection-handling block
- 383e8651cc0e Make the phone number a click-to-call on mobile
- 4435f3fae23c Video testimonials: 30-second self-shot clips as primary proof
- e03cd7999ee5 Present documented product-use outcomes
- 4bc5cc0e725e Borrow authority with brand logos, review badges and trust stats
- 2602a57feb17 Make the product offer concrete and supportable
- 38729fdb61c9 Mobile-first audit with browser device mode
- 4d6326770c4b Fix page load speed with Lighthouse, not guesswork
- ca6dfd85e131 Build a reusable landing page skill to multiply pages
- e4ed90b85412 Improve product landing pages through measured iteration
- 8dcda9c4f61d Verify successful form events without treating them as orders
- 075c7f2d2c43 Use heatmaps and session recordings to find friction
- a835b362c4f5 Set Up Conversion Tracking Before Running Any Test
- 2f79f41a6063 Run a 50/50 Split Test and Iterate Losers Out
- d77e97941d57 Use Session Recordings and Heat Maps to Find Friction
- 7091bbdbaa48 Deploy From Localhost to a Live URL via GitHub and Vercel
- 45546f922308 Treat Landing Pages as Multi-Year Assets, Not One-Off Builds
