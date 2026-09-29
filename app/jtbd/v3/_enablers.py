# Writes app/jtbd/v3/enablers.json. Enablers are the engines behind tactical jobs.
# One enabler powers many jobs across screens. Kevin's note that seeded it is in "note".
import json, pathlib
E = []
def e(id, name, what, inputs, powers, screens, note=None):
    E.append(dict(id=id, name=name, what=what, inputs=inputs, powers=powers, screens=screens, note=note))

e("awareness-map", "Awareness heat map",
  "Tags every ad, post, email and page we run, and every competitor ad, by awareness level (unaware, problem aware, solution aware, product aware, most aware) and funnel stage. Weights by spend and shows where we are thin, per platform, next to competitors.",
  ["our ads with spend and results (Meta, Google, TikTok)", "competitor ads from the Ad Library by page id", "our emails and landing pages", "a written rubric with 5 examples per level"],
  ["share of spend by awareness level", "gap to competitors by level", "which level has the cheapest new customers", "what to make next and where to find inspiration for it", "Google search terms split top, middle and bottom of funnel"],
  ["09-creative", "11-paid-social", "12-google-ads", "03-competitors", "10-copy", "14-email-messaging", "16-organic-content"],
  "Levels of awareness across your brand and are you servicing it vs competitors")
e("creative-archive", "Past creative archive",
  "One place with every ad we have run: the media, the copy, spend, results, dates, audience and placement, sortable and searchable. Dynamic and mixed creatives flagged.",
  ["Meta and TikTok ad history with media", "Google asset reports", "naming conventions"],
  ["find past winners in seconds", "stop remaking ads that already failed", "raw material for tags, postmortems and variants"],
  ["09-creative", "11-paid-social", "25-experiments"],
  "Easy to use interface for past creatives")
e("creative-tags", "Creative decomposition tags",
  "Breaks each ad into parts: hook, angle, pain point, avatar, awareness level, format, length, first frame, proof type, offer, CTA, talent, setting. Same tags on our ads, competitor ads and the inspiration library, so they can be matched.",
  ["creative archive", "competitor ads", "inspiration library", "tag list with definitions and examples", "a person to check 20 tags a week"],
  ["what winning ads share", "tags that lose money", "match a winner to library ads with the same tags", "tag coverage gaps"],
  ["09-creative", "10-copy", "11-paid-social", "03-competitors"],
  "Based on creatives which have worked in the past, decomposed and mapped to the database of creatives. Create tags for each and match tags")
e("principle-matcher", "Why-it-worked matcher",
  "Takes a winning ad's tags and checks them against the idea bank, the knowledge cards and the inspiration library. States the principle it followed, with a test anyone can repeat, and flags claims it cannot verify.",
  ["creative tags", "idea bank (ideas/v1)", "knowledge cards (library-v3)", "results by ad"],
  ["a plain reason each winner won", "principles to reuse in new concepts", "principles that do not hold for this brand"],
  ["09-creative", "10-copy", "25-experiments"],
  "Understand what made that creative work. Compare that against databases")
e("variant-stack", "Variant builder",
  "From one winner, makes near variants (new hook, new first frame, new length) and far variants (new angle, new avatar, new format) that keep the principle. Labels each as near or far.",
  ["the winner and its tags", "the principle it followed", "brand brain voice and claims", "product photos"],
  ["a weekly batch of variants tied to a reason", "a split of near and far bets"],
  ["09-creative", "10-copy", "11-paid-social"],
  "Create variants some similar some different")
e("script-builder", "Script builder",
  "Writes ad scripts from a principle, an avatar and a pain point: hook options, body, proof, CTA, with shot notes. Produces variations of the script.",
  ["principle", "avatar and pain points from the brain", "claims allowed", "past winning scripts"],
  ["scripts for UGC, founder, AI video and static storyboards", "a script bank linked to results"],
  ["09-creative", "10-copy", "16-organic-content"],
  "Create into variants and new concepts mapped to the best practices that the winning ad followed scripts available too")
e("video-stack", "AI video stack",
  "Takes one script, makes 3 to 5 variations, cuts each to 15, 30 and 30 to 45 seconds, renders with a video tool, and lays out the grid so one cut per stack is picked to launch.",
  ["access to a video tool such as Higgsfield", "the script and its variations", "real product photos and clips", "brand kit"],
  ["more video tests per week at a lower cost per test", "which length wins for this brand"],
  ["09-creative", "11-paid-social"],
  None)
e("segment-map", "Best segment map",
  "Shows which age, gender, placement and region buy at the lowest cost per new customer, per creative and per tag. Tells the writer who the ad is for.",
  ["Meta and TikTok breakdowns by age, gender, placement, region", "purchases and value"],
  ["tailor copy and creative to the best segment", "spot placements that burn money", "spot segments no ad speaks to"],
  ["09-creative", "10-copy", "11-paid-social", "02-customers-avatars"],
  "Copy and creative will be tailored to the best performing segment of the population (age/gender/placement)")
e("format-translator", "Format translator",
  "Takes a principle that worked in one format and rewrites it for others: static, carousel, UGC video, founder video, native article, email, landing page block.",
  ["principle and winning ad", "format specs per platform"],
  ["more formats from one proven idea", "native and advertorial ads for top of funnel"],
  ["09-creative", "10-copy", "16-organic-content"],
  "Recommends different formats following the same principles")
e("competitor-feed", "Competitor feed",
  "Pulls competitor ads (Ad Library by page id) and organic posts on a schedule, records how long each ad has run, and tags them. Long-running ads are treated as signals, never as proven winners.",
  ["list of competitors with page ids and handles", "Ad Library access", "organic post pulls"],
  ["what rivals push and at which awareness level", "new launches and offers the day they appear", "principles to test in our own words"],
  ["03-competitors", "09-creative", "16-organic-content", "04-offers-pricing"],
  "Feed in competition. Look through their organic content + ads library and get ideas from there. Convert those ideas into base principles")
e("swipe-file", "Swipe file with notes",
  "A saved library of ads and posts anyone on the team can clip, with a short note on why it was saved and which tag or gap it fills.",
  ["competitor feed", "manual saves", "creative tags"],
  ["inspiration filtered by awareness level, format or angle", "notes that turn into briefs"],
  ["09-creative", "16-organic-content", "03-competitors"],
  "AdLibNote. Muse for content on meta")
e("creative-postmortem", "Creative postmortem",
  "For each ad that lost money: spend, reach, who saw it (age, gender, placement), where people dropped (thumb stop, hold, click, page, cart), and the likely cause. Ends with a fix and a relaunch plan, or a kill note.",
  ["creative archive", "segment map", "landing page data", "tags"],
  ["fix and relaunch instead of starting from zero", "a record of what fails for this brand"],
  ["09-creative", "11-paid-social", "25-experiments"],
  "Postmortem of bad creatives with really good context on spend and demographic data and how you can improve and relaunch")
e("creator-roster", "Creator and partnership roster",
  "A list of creators and partners with fit, rates, rights, content delivered and the results of partnership ads run through their handles.",
  ["creator outreach list", "rights and usage terms", "partnership ad results from Meta"],
  ["which creators sell", "whitelisting and partnership ads", "renewals and cuts"],
  ["09-creative", "11-paid-social", "16-organic-content", "27-wild-bets-pr"],
  "Influencer marketing and partnership ads")
e("copy-decomposer", "Copy decomposition by avatar and pain",
  "Splits every ad and page into avatar, pain point, promise, proof and CTA, and counts spend and results for each avatar and pain pair.",
  ["ad copy and results", "avatar list and pain points from the brain", "landing page text"],
  ["which avatar and pain pairs sell", "pairs we never speak to", "copy briefs per pair"],
  ["10-copy", "02-customers-avatars", "09-creative"],
  "Ad copy decomposition based on avatar and pain point")
e("signal-bridge", "Cross-channel signal bridge",
  "Moves proven words and angles between channels: Google search terms, Amazon reviews and questions, site search and tickets into Meta hooks, and Meta winners into Google ads, SEO and pages.",
  ["Google search terms", "Search Console queries", "Amazon reviews and Q&A", "site search", "Meta winning copy"],
  ["hooks in the customer's own words", "new keyword and article ideas from ad winners"],
  ["10-copy", "11-paid-social", "12-google-ads", "17-seo", "20-marketplaces"],
  "Funnel Google insights/amazon reviews/search data into meta ads and vice versa")
e("review-miner", "Review miner",
  "Reads our reviews and competitors' reviews (site, Amazon, marketplaces), groups what people love, hate and wish for, and counts each theme.",
  ["our reviews", "competitor reviews on Amazon and their sites", "return reasons"],
  ["claims and objections to use in ads and pages", "product fixes", "where rivals fail and we can win"],
  ["02-customers-avatars", "03-competitors", "10-copy", "15-customers-cx", "01-market-research"],
  "Competitor review mining - get insights on what doesn't work or what's working and incorporate it into your marketing")
e("question-matrix", "Question coverage matrix",
  "Lists every question customers ask (tickets, chat, Amazon Q&A, reviews, search) and marks where it is answered: product page, FAQ, ad, email, help centre. Blank cells are the work.",
  ["tickets and chat logs", "Amazon questions", "site search terms", "page and FAQ text"],
  ["fewer tickets", "higher conversion from answered objections", "article and FAQ briefs"],
  ["15-customers-cx", "07-landing-pages-cro", "17-seo", "18-answer-engines", "20-marketplaces"],
  "Coverage matrix from customer tickets amazon")
e("ticket-clock", "Ticket clock",
  "Tracks first reply time, time to resolution, follow-ups owed and reopen rate per ticket, with the order value at stake.",
  ["helpdesk (Gorgias, Zendesk, Freshdesk or email)", "order data"],
  ["no customer left waiting", "which issues cost the most", "staffing needs"],
  ["15-customers-cx", "23-team-ops"],
  "Follow up and time to resolution of tickets")
e("vip-list", "VIP list",
  "Ranks customers by value and recency, picks the top slice, and runs quiet perks: a personal letter, early access, a private offer. Tracks who got what and what they did next.",
  ["orders and customer records", "margin by order", "a letter template and budget"],
  ["repeat rate of top customers", "referrals", "early reads on new products"],
  ["15-customers-cx", "14-email-messaging", "02-customers-avatars"],
  "Sending personal letters to high value clients /vip clients giving them special access be secretive about it")
e("behaviour-map", "Page behaviour map",
  "Joins scroll depth, heatmaps and recordings (Clarity or similar) with GA4 funnels per page and device, and names where shoppers stop.",
  ["Clarity or Hotjar", "GA4", "page list with traffic sources"],
  ["the one block to fix on each money page", "CRO test ideas with evidence"],
  ["07-landing-pages-cro", "08-site-speed"],
  "Scroll depth and clarity/GA insights to drive CRO changes")
e("congruence-check", "Ad to page congruence check",
  "For each ad with spend, compares the ad's promise, offer, visual and awareness level with the page it lands on and scores the match. Flags ads whose page breaks the promise.",
  ["ads with URLs and results", "landing page text and screenshots", "creative tags"],
  ["fix the page for the best ads first", "new pages for winning angles", "fewer bounces from paid traffic"],
  ["07-landing-pages-cro", "11-paid-social", "12-google-ads", "09-creative"],
  "Ad changes linked to landing pages. Congruence of ad + LP. Ad to landing page congruence of best ads to promote best practices")
e("app-audit", "App and code audit",
  "Lists every installed app and script, whether it is still used, what it costs a month, and how much it slows pages. Ties the slowdown to lost revenue.",
  ["store admin app list and billing", "theme code", "page speed tests", "conversion by load time"],
  ["apps to remove", "monthly savings", "revenue lost to slow pages"],
  ["08-site-speed", "06-store-health", "21-finance-cash"],
  "Old app code deleted are you using these tie to revenue lost")
e("theme-twin", "Theme twin test",
  "Duplicates the live theme, makes the speed or flow change on the copy, tests both (speed and a checkout walk-through), and merges only when the copy wins.",
  ["theme access", "speed test tool", "checkout test script"],
  ["safe speed fixes", "no broken checkout on a Friday"],
  ["08-site-speed", "06-store-health", "07-landing-pages-cro"],
  "Duplicate and test speed on both. Test flow and then merge")
e("win-loss-ledger", "Win and loss ledger",
  "Every test gets a result. A win is promoted to the standard (T0) that all new work starts from. A loss writes a fail note with why. Sets the date to recheck each rule.",
  ["experiment list", "results", "a recheck rule per standard"],
  ["what works for this brand, with proof", "no repeated failed tests", "standards that expire when they stop working"],
  ["25-experiments", "09-creative", "07-landing-pages-cro", "14-email-messaging"],
  "Win promotes to T0 loss writes a fail when to check what all things work and what doesn't")
e("search-feed", "Search and answer engine feed",
  "Pulls Search Console, SEO tool data and answer engine checks (what ChatGPT, Gemini and Perplexity say about us and the category).",
  ["Search Console", "an SEO data source such as OpenSEO", "a list of buyer questions to ask assistants"],
  ["queries rising and falling", "pages losing clicks", "where assistants mention rivals and not us"],
  ["17-seo", "18-answer-engines", "01-market-research"],
  "Openseo geo GSC mcp")
e("article-brief", "Article brief builder",
  "Builds SEO article briefs from Search Console gaps, ad winners, search terms, reviews and tickets, with the question, the angle, the proof and the product link.",
  ["search feed", "signal bridge", "review miner", "question matrix"],
  ["articles that answer real questions and sell", "content for answer engines"],
  ["17-seo", "18-answer-engines", "16-organic-content"],
  "Also SEO focused articles can be built from Google insights, meta ads data and search data/reviews")
e("marketplace-plan", "Marketplace plan",
  "A per-channel plan for Amazon, TikTok Shop and quick commerce: listings, pricing floor, ads, reviews, stock and fees, with margin per unit after fees.",
  ["Seller Central and TikTok Shop data", "fees", "unit costs", "stock"],
  ["which SKUs to list where", "margin per channel", "listing fixes"],
  ["20-marketplaces", "13-affiliate-marketplace-ads", "19-supply-inventory"],
  "Amazon seller and tiktok shop strategy")
e("brain-graph", "Brain intake and split",
  "Takes everything we ingest (site, ads, reviews, tickets, documents, interviews) and files it onto the brain's shelves, linked like a graph: product to claim to proof to avatar to ad.",
  ["connected sources", "founder interview", "the 22 shelves in BRAIN-CONTENTS.md"],
  ["every agent starts from the same facts", "find the proof for any claim in one step"],
  ["05-brand-brain", "02-customers-avatars", "09-creative"],
  "Main ingestion and split - splits into categories accordingly think like a graph. Choose a brand first build brand brain then select appropriate creatives landing pages etc")
e("customer-jobs", "Customer jobs map",
  "Finds why customers hire the product: the moment, the progress wanted, what they used before, what nearly stopped them. From reviews, tickets, post-purchase surveys and a few interviews.",
  ["post-purchase survey", "reviews", "tickets", "5 to 10 customer calls"],
  ["angles and hooks from real moments", "new audiences in other moments", "product and bundle ideas"],
  ["02-customers-avatars", "10-copy", "09-creative", "01-market-research"],
  "Jobs to be done why are they hiring")
e("work-board", "Work board",
  "A kanban board of every task from every screen: to do, doing, waiting on approval, live, measured. Each card links to the job, owner, due date and the metric it should move.",
  ["tasks from each screen", "team list", "approval rules from the brain"],
  ["nothing lost between screens and people", "who is overloaded", "what shipped and what it did"],
  ["23-team-ops", "00-today", "26-reports"],
  "Kanban board")
e("access-vault", "Security folder",
  "A register of every account, who has access, 2-step status, and the recovery path, plus a folder for policies and incident notes. Holds no passwords itself.",
  ["account list", "team list", "admin checks per platform"],
  ["no lost access when someone leaves", "fast recovery after a takeover"],
  ["24-security", "23-team-ops"],
  "Security folder")
e("funnel-mix", "Funnel stage mix",
  "Splits spend and results by funnel stage on every channel: prospecting vs retargeting on Meta, generic vs brand search on Google, new vs returning buyers.",
  ["Meta campaigns and audiences", "Google campaigns and search terms", "new vs returning from orders"],
  ["are we buying new customers or rebuying old ones", "brand search inflation", "where to add top of funnel spend"],
  ["11-paid-social", "12-google-ads", "22-measurement", "00-today"],
  "Levels of awareness across your brand ... top of funnel, middle of funnel, bottom of funnel")
e("margin-view", "Margin view",
  "Gross profit per order, per product and per channel after product cost, shipping, fees, discounts and returns.",
  ["orders", "product costs", "shipping and fees", "returns"],
  ["which ads and offers make money, not just revenue", "floors for cost per purchase"],
  ["21-finance-cash", "04-offers-pricing", "11-paid-social", "00-today"],
  None)
e("market-pulse", "Market pulse",
  "Quarter by quarter view of the category: search demand, marketplace sales rank, competitor launches, input costs and allied categories, next to our own growth.",
  ["Google Trends and search volumes", "marketplace best seller data", "input cost indices", "our sales by quarter"],
  ["is the category growing and are we keeping pace", "costs about to rise", "trends to catch early"],
  ["01-market-research", "03-competitors", "19-supply-inventory"],
  None)
json.dump(E, open(pathlib.Path(__file__).with_name("enablers.json"), "w"), indent=1, ensure_ascii=False)
print(len(E), "enablers")
