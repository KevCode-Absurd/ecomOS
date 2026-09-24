# eCommerce Marketing Data 101: Derric Haynie's Crash Course on Understanding Data Analytics

source_id: 1AEHhyT5v0fb7Sfsh5VMDU5HAv9IXH9cD  |  folder: /06-MEA-measurement  |  cards: 23  |  words: 11,257  |  type: transcript (podcast interview, 1 guest, 1 unnamed host)

credibility: The guest is Derric Haynie (transcribed "Derek Haney"), who runs eCommerceTech.io, a directory of "260 plus tools that we've reviewed independently", aimed mainly at Shopify merchants. He says his team recommends tools to merchants "for free"; how the directory earns money is not stated `[web check: eCommerceTech.io business model, e.g. vendor or affiliate fees]`. His favourite clients are growth-stage brands doing $1M to $10M a year. He says he was once in-house at a beauty box subscription company. He also runs an "E-commerce Day" live event. Evidence: 1 personal test story (beauty box, about $1M a month), 1 second-hand agency anecdote (misspelled ads), 1 second-hand rule of thumb (3% / 3%, from "the guy from ProfitWell", name not given), and otherwise opinion. No data sets, no sample sizes, no formulas beyond 2 spoken arithmetic examples. He admits he does not make most of his own business decisions from data ("I'm doing it more based on feel and opinion").
date signals: ChatGPT is named and described as giving its product away for free to get millions of users (points to 2023). "EnquireLabs now called Fairing" (rename happened before this talk). "ChatGPT to Figma" for design mock-ups. AI predictions are framed as "the next 3 to 5 years" from the talk date. No ad platform versions, iOS changes or consent rules are named, so the measurement advice is conceptual and ages slowly; tool names and the AI forecasts age fast.

scope note: The ingestion header (at the top of the source file) is a folder brief, not the speaker's words. It lists "incrementality and holdouts" and "consent and tracking loss" as topics. The speaker never says "incrementality", "holdout", "consent", "iOS" or "tracking prevention". Those ideas appear only in cards [859e4f5b289d] [7f3bed7f5dd1] [c50f782181a7] [9c479169d7e9] [45d7e49e638b] as card-writer additions. This mini playbook marks them as such. The header also says to skip AI futurism, the 4-hour week, web3, the gig economy and personal anecdotes; they are summarised briefly in section 9 because 2 cards cover them.

## 1. What this source is for

A beginner's frame for store analytics. It helps an operator: decide when and how much to invest in analytics; sort data into quantitative vs qualitative and zero-party, first-party, (second-party) and third-party; handle the conflict between platform attribution and "how did you hear about us" answers; pick where to ask customers questions; stop HiPPO (Highest Paid Person's Opinion) decisions; choose 1 top metric (customers, revenue or profit) and know when to change focus; and tell compounding levers from one-off ones. It is thin on how: no attribution method, no test design, no statistics, no formulas for CAC, LTV or ROAS.

## 2. Principles

### 2.1 Why and when to invest in analytics

1. **If you can't measure it, you can't improve it.** Without a known cost of acquisition you cannot tell if a campaign raised or lowered it. Without channel-level revenue for email, you cannot tell if this send beat the last one. Condition: applies to any metric you want to move. The speaker notes "better or worse" can be ambiguous, which is why the top metric must be chosen first (2.4). [11a74e34ca53]
2. **Analytics must end in a decision.** Collecting, organizing and staring at charts does not help unless someone acts. Sometimes the decision is "keep doing the same thing". Reports made to pat yourself on the back are "mindless self-indulgence", not analytics. [11a74e34ca53]
3. **Focus analysis on the unknowns.** Aim reports at the critical questions and unknown variables, where you cannot yet say which lever to pull, not at metrics you already understand. [11a74e34ca53]
4. **Collect data before it is worth anything.** You cannot analyse history you never logged. Decide which data points might matter later and start keeping them now. Early data sets pay off when the business and budget are larger. Salon example: haircut style, visit every 2 months, always Saturday, even after-photos, in a CRM, could predict the business. Condition: the speaker says "data points that might be of interest", not log everything. [776e59649374] [11a74e34ca53]
5. **Cost of acquisition exists before paid ads.** "Sometimes people only calculate cost of acquisition after they start paid advertising. Why is that? We have cost of acquisition prior to that." The source gives no formula or list of cost lines to include `[needs brand data: all acquisition costs before paid ads, e.g. influencer, content, samples, discounts, and new-customer count]`. [776e59649374] [11a74e34ca53]
6. **Analytics value scales with business size.** Speaker's heuristic: a $1M business can make $5K, $10K or $15K decisions from good analytics; a $100M business can make $1M, $5M or $10M decisions. So spend on analytics should grow with the business. Count both tool cost and human time: the analyst who builds the report and the executive who reads it and decides. The report must be something the decision maker can digest. Condition: illustrative numbers, not a benchmark. [11a74e34ca53] [776e59649374]

### 2.2 Types of data

7. **Quantitative tells what and how; qualitative tells why.** Example: you changed page copy and conversion rate rose (quantitative). Why that headline or image won (people related to it, or it raised fear) needs qualitative research. The speaker estimates 90% of analytics talk is about quantitative data, which "doesn't actually mean that it's more important". Qualitative data is messier and costs more (research partners, customer calls, panels such as "asking 50 people Coke or Pepsi"). Quantitative alone "leaves you with more questions". [e2f188649f8f] [5dffd6bf5d3c]
8. **Data tiers.** Zero-party = the customer told you (post-purchase survey, quiz, feedback form, long-form answer). First-party = you tracked what the customer did on your site (purchases, behaviour, heatmaps). Second-party = from a partner; the speaker is unsure and says most people skip it. Third-party = aggregated large sources (Facebook, Google, Experian) that collect data on households. A good data team holds zero, first and third-party data. Get data "as close to the customer's mouth as possible", but third-party has value too. [9c479169d7e9] [e11ec2148e14]
9. **Zero-party and first-party often conflict on source.** Analytics says the buyer came from a Google ad click. Asked after purchase, the buyer says "a friend told me", social media, or "I walked by your store". "It's on you, or a smart analytics person, to decide how to handle that conflict and attribute the source." Condition: the speaker gives no rule for which to trust. Cards [9c479169d7e9] [45d7e49e638b] [7f3bed7f5dd1] go further and say to favour self-report for strategic channel calls; that is card-writer advice, not the speaker's. [e11ec2148e14] [9c479169d7e9]
10. **Third-party data is for enrichment and triggers.** Example: a furniture seller with 10,000 customers wants to know what percentage are homeowners, and who just became one, then times messages around that. Other trigger ideas: hired or fired, upcoming birthday (birthday could also be zero-party if you ask). [e11ec2148e14]
11. **Data privacy is out of scope for the speaker.** He declines to go into it but says data "is being bought and sold over and over again" in back-office exchanges. Anecdote: a friend filled out a mortgage form and got 45 calls between 5 am and 10 am the next morning. `[web check: privacy and consent rules for buying or using third-party data in each selling country]`. [e11ec2148e14]

### 2.3 Qualitative collection

12. **Ask at every stage.** Before they have heard of you, after they have heard of you, before purchase (on-site), after purchase, and after churn. For physical products, set a timeline, for example no purchase 1 year after the last one, and talk to those people. [7e8ec204ea88]
13. **Founders talk to customers weekly.** "In the first 3 years of any business, if you're not talking to a customer at least once a week, what are you doing." He has heard of Fortune 500 CEOs doing it forever. Some of this can be handed to customer service or marketing when larger data sets are needed. [7e8ec204ea88]
14. **Listen most to the 3% most loyal and the 3% biggest haters.** Attributed to "the guy from ProfitWell" (name not recalled). The 94% in the middle matter less for this. Loyal tell you what you do well; haters tell you what not to do. Condition: heuristic, no evidence given. Cards add how to pick them (repeat buyers, high LTV; refunds, complaints, bad reviews) and to size groups so each has enough respondents; those are card-writer steps. `[needs brand data: customer list ranked by orders or LTV, and refund, complaint and review records]` `[web check: who at ProfitWell said this and in what form]`. [375f45ad5513] [338914784a95]
15. **Turn qualitative answers into copy.** Take long-form survey or quiz answers (what they liked, pain solved, benefits), build a word board, then change the headline or product description "ever so slightly" to match how people feel and why they buy. [e11ec2148e14] [e2f188649f8f]
16. **Quiz and survey data must reach the CRM.** Do not leave it in a standalone data silo. The quiz earns its keep when it also returns personalised product recommendations right away. [e11ec2148e14] [7e8ec204ea88]
17. **Qualitative tools need an analyst.** Heatmaps, journey maps and open answers need summarising and work; "I wouldn't say it's instantly plug and play." Not every comment should be acted on ("sometimes you want to listen to it and sometimes you don't"); the speaker does not say how to decide. [7e8ec204ea88] [5dffd6bf5d3c]

### 2.4 Decision making and metric choice

18. **Let data reveal its position; do not use it to back yours.** The HiPPO (CMO, CEO, director or VP of marketing) wants things their way from past experience or convenience, then shows graphs that support them and pushes the rest aside. The flip side is ignoring data that disagrees. Condition: speaker's opinion; he admits he is not fully data-driven himself. [129ad3db527d] [c50f782181a7]
19. **Test, do not swap on advice.** Speaker's observation: white-background product images are generally not the highest converting; lifestyle or action shots usually are. But the move is "go test it and let the data inform", not "change everything". Brand rules (everything must match; images copied from manufacturers) should not block a better customer experience; often you can raise conversion inside brand guidelines. `[web check: marketplace rules that require white-background main images, e.g. Amazon, Google Shopping]`. [129ad3db527d]
20. **Ask "can we do both?"** When a test result clashes with another goal (brand, retention, annual subscriptions), look for a way to get both, for example keep the long plan on page 2. [129ad3db527d]
21. **When there is no data, act on opinion but design the act to collect data.** Example: launching E-commerce Day with no idea if people would come; check what data exists first (can I get enough people, enough sponsors, profit and cost expectations), then use the first run's data to plan the next. [129ad3db527d]
22. **Optimise 1 of 3 top metrics at a time: number of customers, revenue, or profit.** You can sometimes move 2; almost never all 3. Customers max at a free price (and you go broke, unless you are ChatGPT with a big backer). Revenue sits in the middle with a reasonably priced product that makes money on each sale. Profit "typically is your highest priced product". The executive team must tell every department which one it is. Customer experience and value also matter, and feed profit through LTV and retention. [13ce65376d8f]
23. **Levers fight each other.** Raising conversion rate can lower LTV (lower-quality customers). Raising AOV can lower LTV "believe it or not". Raising referral coefficient may lower CAC and so raise profit. Decide which trade you accept. Condition: stated as possible, not measured. [13ce65376d8f] [06aa9f46abe7]
24. **Track what your winning metric breaks.** Leaving out metrics your decision affects is the third mistake. Example: an ad agency (transcript unclear, possibly "Optima") raised conversions by misspelling ads; it worked, but hurt brand affinity. A brand team could fairly say the gain was not worth it. No numbers given. [06aa9f46abe7]
25. **Match the top metric to stage and bankroll.** Early stage: customers (virality, referrals, breaking out from "nothing brand to something brand"); this is why early companies lose money, buying customers and hoping LTV pays later. Later: pivot to revenue, then profit. A stable business not chasing 5x or 10x growth may choose profit (lifestyle business choice is fine). Bigger bankroll means longer horizon (Apple "thinks in 10-year terms"); a small startup needs the next customer tomorrow but must not burn them with a poor product or experience. [0c302f4b2883] [13ce65376d8f]
26. **Keep the top metric fixed for about a year.** Big focus swings ("now loyalty, next month acquisition") are quarterly, bi-annual or annual initiatives, not weekly or monthly. Swapping monthly "causes turmoil". Small quick-win KPI pushes of a couple of weeks to a month are fine: review count, referral coefficient, loyalty points used, products per order, purchase frequency. [13ce65376d8f] [5869b757b0e7]
27. **Change focus at the top of the S curve.** When each extra dollar into your main lever returns less and less, move to the next lever. Speaker's order for a store: conversion rate optimisation first ("one of the highest levers", and it should improve customer experience too), then AOV (merchandising, cross-sell, upsell, co-marketing partners, affiliate offers on the post-purchase page), then LTV (selling to existing, past and churned customers), which "more closely aligns with profit maximising". No numeric threshold. [5869b757b0e7] [3a1918a526e2]
28. **Classify each lever: compounding, incremental or one-off.** Speaker names conversion rate and referral coefficient as compounding, and calls them the biggest levers for whichever top metric you chose. See section 4 for his arithmetic and section 9 for a caveat. [3a1918a526e2] [63817d833e21]
29. **Use comparative metrics, not 1-line graphs.** "Revenue went up month over month" strokes the ego but does not say why or which lever to pull. Compare revenue to AOV, revenue to profitability, revenue to new customers, revenue by channel. [3a1918a526e2] [5869b757b0e7]
30. **Predictive analytics replaces hand analysis.** Old way: organise data, choose metrics, a human explains the chart (opinions sneak in). Now: tools use past data and regression-style machine learning to predict, for example, "increase ad spend by 5% and new customers rise by X, revenue by Y, cost of acquisition stays about steady". Condition: the speaker names no tool and gives no accuracy figure. [0f952763382f]

## 3. Procedures

The source gives few step-by-step procedures. These are the sequences it states or clearly implies. Steps added only by cards are marked "card".

### 3.1 Decide how much to invest in analytics
1. List the data you keep now and the questions you may want answered later. [776e59649374]
2. Start logging missing data points now, even without a use yet. [776e59649374]
3. Compute cost of acquisition now, even before paid ads `[needs brand data: acquisition costs and new customers by month]`. [776e59649374]
4. Size analytics spend (tools plus analyst and decision-maker time) to the size of decisions it can inform (section 4). [11a74e34ca53]
5. Name an owner who turns data into a short, decision-ready report. [11a74e34ca53] [776e59649374]
6. Point each report at an open question and end it with a decision. [11a74e34ca53]

### 3.2 Handle platform vs self-reported attribution
1. Run a 1-question post-purchase survey ("where did you hear about us?" / "where did you buy this?"), e.g. with Fairing `[verify UI]`. The speaker says this is typically for larger businesses fine-tuning their attribution model. [7e8ec204ea88] [45d7e49e638b]
2. Compare survey answers with what analytics credits for the same buyers. [e11ec2148e14]
3. Where they conflict, decide a rule for how to attribute the source, and record it. The speaker gives no rule. [e11ec2148e14]
4. Card only: compute the gap per channel for the same window; treat the platform number as directional; do not cut an over-claiming channel on platform data alone until incrementality is tested; keep budget on channels customers name that platforms cannot see (word of mouth, podcasts, offline). [7f3bed7f5dd1]
5. Card only: incrementality test: define channel and outcome (sales, new customers, contribution margin); hold out a random segment or geography; measure the difference over "a sufficient window"; compare lift to platform-claimed conversions; scale only where lift pays. No volume, window or threshold is given. [859e4f5b289d]

### 3.3 Run a voice-of-customer program
1. Map stages: before awareness, after awareness, on-site prospect, after purchase, after churn (e.g. no purchase in 1 year). [7e8ec204ea88]
2. On-site: add an open question, "What is this page missing?" (Hotjar-style poll) `[verify UI]`. Expect answers like "I couldn't find the price", "I couldn't find it in my color", "I don't know if this will work for me", "I still don't understand what you do" (message clarity). [7e8ec204ea88]
3. Post-purchase: 1-question source survey (3.2). [7e8ec204ea88]
4. Quiz: use a quiz tool that sends answers to the CRM or email platform and gives personalised product recommendations on the spot (Octane AI, Typeform named) `[verify UI]`. [7e8ec204ea88] [e11ec2148e14]
5. Founder calls at least 1 customer a week (first 3 years). [7e8ec204ea88]
6. Prioritise the top 3% most loyal and 3% biggest haters for deep listening. [375f45ad5513] [338914784a95]
7. Build a word board from long-form answers; adjust headline and product description to match. [e11ec2148e14]
8. Pair each quantitative drop with a recording, heatmap or verbatim before proposing a fix; repeat after the change (card steps). [5dffd6bf5d3c]

### 3.4 Get a test past a HiPPO
1. State the hypothesis and the metric that will judge it, separately (card). [c50f782181a7]
2. Run the test instead of arguing opinions. [129ad3db527d]
3. If a stakeholder objects (brand, retention, "we must sell the annual"), ask "why", "how can we do both", "can we try it", and put a value on the missed opportunity. [129ad3db527d]
4. Card only: ask what data would falsify the belief; run strong-conviction, thin-evidence changes on a limited segment first. [c50f782181a7]

### 3.5 Set and change the top metric
1. Executive team picks 1: customers, revenue or profit, based on stage and bankroll. [13ce65376d8f] [0c302f4b2883]
2. Map each department's sub-metrics (conversion rate, AOV, referral coefficient, retention) to it (card wording). [13ce65376d8f]
3. List the secondary metrics each tactic may hurt (LTV, customer quality, brand, customer experience) before scaling a winner. [06aa9f46abe7]
4. Keep the top metric about 1 year. Review big focus shifts quarterly at most. [13ce65376d8f] [5869b757b0e7]
5. Track return per dollar on the current main lever with comparative charts. When it flattens (top of S curve), move to the next lever. [5869b757b0e7]
6. Allow short quick-win KPI pushes without changing the top metric. [5869b757b0e7]

## 4. Rules, thresholds and numbers

| rule | number or threshold | condition | source's basis | card id |
|---|---|---|---|---|
| Analytics decision size by revenue | $1M business: $5K to $15K decisions. $100M business: $1M to $10M decisions | Illustrative. Derived ratio: 0.5% to 1.5% of revenue at $1M; 1% to 10% at $100M (ratios are arithmetic on his numbers, he did not state them) | Opinion | [11a74e34ca53] |
| Preferred client size | $1M to $10M a year revenue, past product-market fit, adding staff | Speaker's favourite tooling clients, not an analytics-readiness rule | Own business | [0c302f4b2883] |
| Share of analytics talk that is quantitative | about 90% | "Let's just say", a guess | Opinion | [e2f188649f8f] |
| Customer conversations | At least 1 a week | First 3 years of a business; founders | Opinion; Fortune 500 CEO hearsay | [7e8ec204ea88] |
| Churn interview trigger | No purchase 1 year after last | Physical products; "you might set a timeline" | Example | [7e8ec204ea88] |
| Qualitative focus | Top 3% loyal + bottom 3% haters; 94% middle lower priority | Heuristic | Second-hand, ProfitWell | [375f45ad5513] [338914784a95] |
| Top metrics | Optimise 1 of 3 (customers, revenue, profit); sometimes 2; almost never 3 | Company level | Opinion | [13ce65376d8f] |
| Top-metric lifespan | About 1 year ("relatively annually fixed") | Company level | Opinion | [13ce65376d8f] |
| Big focus shifts | Quarterly, bi-annual or annual | Department level | Opinion | [5869b757b0e7] |
| Quick-win KPI pushes | A couple of weeks to a month | Reviews, referral coefficient, loyalty points used, products purchased, purchase frequency | Opinion | [5869b757b0e7] |
| Conversion rate "compounding" | Next month revenue = this month revenue x (1 + relative CVR lift). $10,000 x 1.01 = $10,100 | Same traffic, 1% relative lift. Speaker first said $11,000 then corrected to $10,100. $11,000 would be a 10% relative lift (e.g. CVR 10% to 11%, +1 point) | Spoken arithmetic | [3a1918a526e2] |
| Referral "compounding" | Next month customers = base customers x (1 + referral coefficient). 100 x 1.05 = 105; 100 x 1.10 = 110 | Same input; referral coefficient 5% to 10% | Spoken arithmetic | [3a1918a526e2] |
| Profit-mode trade | Revenue $1M to $900K, keep an extra $100K | Stable business happy with its market; cut opex, headcount, or ad spend to cheaper customers | Example | [0c302f4b2883] |
| Beauty box homepage test | About $1M a month more revenue | 4 plan lengths (monthly, 3, 6, 12 months) on homepage replaced by 1 buy-now box; plans moved to page 2. Vetoed by execs | Speaker's own test; one company | [129ad3db527d] |
| Predictive example | +5% ad spend predicts change in ROAS, new customers and revenue; CAC "largely steady" | Tool output example, no tool named | Illustration | [0f952763382f] |
| AI landing-page loop | 18 variants | Prediction, not result | Opinion | [0f952763382f] |
| AI customer service error rate | "1 in a thousand cases would have a problem" | Speaker's guess; escalate when needed | Opinion | [0f952763382f] |
| Tool directory | 260+ tools reviewed | eCommerceTech.io, at time of talk | Own business | [28a475f2a0fd] |

Formulas the source does not give: CAC, LTV, ROAS, contribution margin, referral coefficient definition, conversion rate definition. Pass 2 must take these from other 06-MEA or 20-FIN sources.

## 5. Diagnostics and checks

| check | how | good | bad | next |
|---|---|---|---|---|
| Do reports change decisions? | For the last few reports, name the decision each led to | Each ends in a decision, even "keep going" | Reports read and filed; used to celebrate | Rewrite reports around 1 open question and 1 decision [11a74e34ca53] |
| Is CAC known before paid ads? | Look for a monthly cost-of-acquisition number that predates paid ads | Exists and is tracked | Only computed since ads started | Compute it `[needs brand data: acquisition costs, new customers]` [776e59649374] |
| Can email be judged send by send? | Check that revenue is tracked per email channel and per send | Per-send revenue exists | No channel revenue | Add tracking [11a74e34ca53] |
| Are charts comparative? | Scan dashboard for single-line metric graphs | Revenue shown against AOV, profit, new customers, channel | "Revenue up MoM" alone | Add comparison series [3a1918a526e2] |
| Do platform and survey sources agree? | Survey answers vs analytics-credited source for the same buyers | Gaps are known and a written rule decides attribution | Nobody has compared; or 1 source trusted by default | Write the rule; card adds incrementality test [e11ec2148e14] [7f3bed7f5dd1] |
| Is zero-party data in the CRM? | Check quiz and survey fields in CRM/ESP | Fields flow in and drive segments and recs | Answers live only in the quiz app | Connect or change tool [e11ec2148e14] |
| Founder customer contact | Count customer calls per week | 1 or more (first 3 years) | None | Book calls [7e8ec204ea88] |
| HiPPO test | For a recent decision: was data used to reveal or to defend? Were contrary charts shown? | Test run; contrary data shown | Graphs picked to fit; tests refused | Run the test; "can we do both" [129ad3db527d] |
| Top metric clarity | Ask each department which of customers, revenue, profit the company optimises | Same answer everywhere | Different answers, or changed in the last month | Exec team sets 1 for about a year [13ce65376d8f] |
| Side effects of a winner | Before scaling, list LTV, customer quality, brand, CX effects | Listed and judged | Only the target metric checked | Check before scale [06aa9f46abe7] |
| S-curve position | Return per extra dollar on the main lever over time `[needs brand data: spend and result by lever over time]` | Still rising | Each dollar returns less | Move to next lever (AOV, then LTV) [5869b757b0e7] |

## 6. Tools, settings and named features

| tool | use in source | notes |
|---|---|---|
| Hotjar | On-site open poll "What is this page missing?" for prospects; heatmaps, click maps, on-site journey mapping (speaker classes heatmaps as first-party) | `[verify UI]` [7e8ec204ea88] [5dffd6bf5d3c] |
| Fairing (formerly EnquireLabs) | 1-question post-purchase survey, "where did you hear about us / buy this", for attribution | `[verify UI]` `[web check: current features and price]` [7e8ec204ea88] [45d7e49e638b] |
| Octane AI | "One of the leading" ecommerce quiz tools; push answers to CRM, give personalised recs | `[verify UI]` [7e8ec204ea88] |
| Typeform | Alternative for quizzes and surveys | `[verify UI]` [7e8ec204ea88] |
| Experian | Example of third-party data (household-level) | `[web check: availability outside the US]` [e11ec2148e14] |
| Facebook, Google | Named as third-party aggregate sources; Google Ads as the platform that may claim a sale the customer credits to a friend | [e11ec2148e14] |
| CRM / email service provider | Destination for zero-party data; avoid data silos. Data lakes and warehouses mentioned but not explained | [e11ec2148e14] |
| Predictive analytics, "big ERPs" | Regression-style predictions of spend outcomes; no product named | [0f952763382f] |
| ChatGPT, OpenAI | Rewriting landing pages; "ChatGPT to Figma" design mock-ups | Prediction context [0f952763382f] [ae8e451f0caa] |
| eCommerceTech.io | Speaker's directory, 260+ independently reviewed tools, mainly Shopify | Speaker's own business; `[web check: current listings]` [28a475f2a0fd] |
| Shopify, Oberlo, Amazon | Named as having "democratised" ecommerce | Context only |

## 7. Examples and case results

All are examples, not promises.

- **Beauty box homepage (speaker's own, in-house).** 1 product (a box of 5 random products) sold monthly, every 3 months, every 6 months or yearly, with discounts for longer plans, shown as a big 4-option box on the homepage. Hypothesis: 1 box with 1 buy-now button on the homepage (plans moved to page 2) cuts choice paralysis. Result as told: conversion rose enough for "about a million dollars a month in revenue". Executives rejected it because they needed annual subscriptions and retention metrics. The speaker thought both could be had. Note: he first says "I wasn't given permission to run this test", then says he ran it; see section 9. No traffic, time frame or significance given. [129ad3db527d]
- **Misspelled ads (second-hand).** An agency lifted ad clicks and conversions by misspelling ads; brand affinity suffered. No numbers. [06aa9f46abe7]
- **Google ad vs friend.** Analytics credits a Google ad click; buyer says a friend told them. Illustrates attribution conflict. [e11ec2148e14]
- **Furniture and homeowners.** 10,000 customers; use third-party data to find homeowners and new homeowners to time messages. [e11ec2148e14]
- **Salon CRM.** Style, every 2 months, Saturdays, photos; shows value of early data. [776e59649374]
- **Profit mode.** $1M to $900K revenue, keep $100K more by cutting opex, headcount or ad spend. [0c302f4b2883]
- **E-commerce Day event.** First run launched on opinion; data from it drove next year's decisions. [129ad3db527d]
- **Mortgage form.** 45 calls from 5 am to 10 am after a form fill, showing data resale. [e11ec2148e14]

## 8. Mistakes the source warns about

1. HiPPO decisions: using data to back an opinion, showing only supporting graphs, or ignoring data that disagrees. [129ad3db527d] [c50f782181a7]
2. Not knowing which metric you optimise. [13ce65376d8f]
3. Leaving out metrics your decision affects (LTV, customer quality, brand, customer experience). [06aa9f46abe7]
4. Staring at charts and not acting; self-congratulating reports. [11a74e34ca53]
5. Computing cost of acquisition only after paid ads start. [776e59649374]
6. Not keeping data early, so later questions cannot be answered. [776e59649374]
7. Relying on quantitative data alone and never talking to customers. [e2f188649f8f] [7e8ec204ea88]
8. Leaving quiz and survey data in a standalone silo. [e11ec2148e14]
9. Swapping everything on advice (e.g. all lifestyle images) instead of testing. [129ad3db527d]
10. Letting brand guidelines, or manufacturer images copied as-is, block a better customer experience. [129ad3db527d]
11. Changing the core KPI focus weekly or monthly. [13ce65376d8f] [5869b757b0e7]
12. Single-metric graphs with no comparison. [3a1918a526e2]
13. Early-stage: winning the next sale by burning the customer with a poor product or experience. [0c302f4b2883]
14. Raising conversion rate in ways that lower customer experience. [5869b757b0e7] [06aa9f46abe7]
15. Host's point: marketers get lost in numbers and forget the people, offer and message behind them. (Not carded.)
16. Resisting AI on HiPPO grounds (e.g. "AI in customer service will hurt our brand"); speaker predicts those brands lose on cost. Opinion. [0f952763382f]

## 9. Caveats, conflicts and what is missing

- **Incrementality is not in the text.** The folder brief and cards [859e4f5b289d] [c50f782181a7] [7f3bed7f5dd1] present holdouts and incrementality as this source's corrective. The speaker never mentions them. Treat those card steps as card-writer additions with no volume, window or threshold.
- **Which attribution to trust is left open.** The speaker says the analyst must decide. Cards [45d7e49e638b] [7f3bed7f5dd1] say to favour self-report for strategic calls, and [9c479169d7e9] says first-party is "unreliable for attribution"; those are card stances. Cards also mention consent loss and tracking prevention; the speaker does not.
- **"Compounding" arithmetic is a 1-time step, not compounding.** $10,000 to $10,100 from a 1% relative CVR lift is a lasting multiplier on all traffic, not a gain that grows on itself month after month. The referral example is 1 generation only (100 to 105 or 110); true compounding would need referred customers to refer again. The speaker also mixes "1 percent" with a $1,000 then $100 result, so relative vs percentage-point lift is unclear. Card [63817d833e21]'s claim that linear metrics should be judged "purely on marginal cost" is card wording.
- **Beauty box story conflicts with itself.** "I wasn't given permission to run this test" then "I was able to create and run a test". Card [129ad3db527d] calls the $1M a month "projected"; the transcript says the test "increased" revenue. No traffic, duration or significance.
- **AOV can lower LTV** is stated without mechanism or data. [13ce65376d8f]
- **White vs lifestyle images** is the speaker's general observation, no data. Some marketplaces require white main images `[web check: current marketplace image rules]`.
- **1 of 3 metrics** is a simplification; card [13ce65376d8f] notes revenue and profit can move together. The speaker says "profit typically is your highest priced product", which is a claim about pricing, not a measured rule.
- **3% / 3%** is second-hand; ProfitWell source unnamed; no method to pick the groups.
- **Second-party data** definition is uncertain ("I always get this one wrong").
- **Missing:** formulas for CAC, LTV, ROAS, AOV, contribution margin; attribution windows; UTM rules; event deduplication; match quality; consent; restatement; test sample sizes or significance; how to decide which qualitative feedback to act on; which cost lines go into pre-ads CAC; an S-curve threshold.
- **AI section is prediction.** Next 3 to 5 years: AI executes tests (landing pages, creative), humans only set guardrails ("no misspelled words, no cussing") and adding humans "slows the process"; media agencies, creative and writing teams shrink to 1 editor then none; customer service near fully automated; merchandising by AI including false-door demand tests before a 10,000-unit purchase order; "$1M in a bank account and 25 conditions" to run a business; 15 to 20 years to full democratisation. The "humans slow the loop" view conflicts with this repo's rules (brand voice, no invented claims, owner review). Career advice: move toward strategy, running AI tools and understanding the tech; learn business fundamentals and bankroll management; no-code and low-code make tech startups easier. [0f952763382f] [ae8e451f0caa]
- **Commercial interest:** the speaker runs a tool directory, so "add tools as you grow" advice suits his business `[web check: eCommerceTech.io revenue model]`. [28a475f2a0fd]
- Card [3a1918a526e2] has a typo ("comp1ounding"); content unaffected.

## 10. Card index

- [9c479169d7e9] Zero-party vs first-party vs third-party data
- [45d7e49e638b] Use post-purchase surveys as another attribution signal
- [375f45ad5513] Prioritize the 3% most loyal and 3% most dissatisfied customers
- [c50f782181a7] Avoid HiPPO decision-making
- [63817d833e21] Distinguish compounding metrics from linear metrics
- [7f3bed7f5dd1] Reconcile platform attribution with self-reported attribution
- [859e4f5b289d] Test incrementality instead of trusting attribution
- [5dffd6bf5d3c] Capture the 'why' behind quantitative results with qualitative tools
- [11a74e34ca53] Two Ground Rules Before Investing in Ecommerce Analytics
- [e2f188649f8f] Qualitative vs Quantitative Ecommerce Data: What and Why
- [e11ec2148e14] Zero, First and Third-Party Data for Ecommerce Attribution
- [7e8ec204ea88] Collect Customer Feedback at Every Lifecycle Stage
- [338914784a95] The 3% Rule for Qualitative Feedback
- [129ad3db527d] Don't Let the HiPPO Pick Your Ecommerce Metrics
- [13ce65376d8f] Pick One Primary Metric: Customers, Revenue or Profit
- [0c302f4b2883] Match KPI Focus to Your Company Stage
- [3a1918a526e2] Compounders vs Linear Metrics in Ecommerce
- [06aa9f46abe7] Watch What Your Winning Metric Breaks
- [5869b757b0e7] When to Change KPIs: The Top-of-S-Curve Test
- [0f952763382f] Predictive Analytics and AI Execution in Ecommerce
- [776e59649374] Start Collecting Store Data Before It's Worth Anything
- [ae8e451f0caa] Plan ecommerce roles around AI-resistant work
- [28a475f2a0fd] Use an independent tool directory before buying ecommerce software
