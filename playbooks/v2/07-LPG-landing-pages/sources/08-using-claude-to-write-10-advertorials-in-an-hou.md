# Using Claude to Write 10 Advertorials in An Hour

source_id: 1H8NNKcFO3LlDfEdAoSrWdJCmBPTz-I-X  |  folder: /07-LPG-landing-pages  |  cards: 10  |  words: 8226  |  type: transcript (screen-recorded video walkthrough, single presenter)
credibility: Presenter is Stephan Georgi (transcribed "Stephan georgei"), a direct-response copywriter. He sells "Copy Pro", an annual mastermind (copy review, funnel strategy, team training, 2 in-person masterminds a year, private WhatsApp group), and pitches it at the end. He says he is an equity partner in a pet supplement company and uses its advertorial as the main swipe. Evidence is a live demo only: he runs the prompts on camera and reads the outputs. No conversion data, no test results, no client numbers. His quality claim ("better than what 99% of copywriters would write on their own") is his opinion and part of the sales pitch.
date signals: He says he is recording "on April 8th" and that "we've got that eclipse happening today". That matches the 8 April 2024 total solar eclipse, so the recording is likely April 2024. He uses "Claude 3" in the Claude web app, hits a message cap ("7 messages remaining", then "5 messages remaining"), and suggests Poe at "like $20 a month I think". Models, limits and prices are all stale. [web check: current Claude plans, message limits and model names; current Poe pricing]
scope note: The document header describes this as "a comprehensive masterclass" with "format selection matrices, narrative consistency rules, and conversion benchmarks". The transcript contains none of those. It is 1 prompt workflow demo. Paid acquisition and ad-to-page congruency belong to 06-MEA and 24-DEP; email flows to 14-EML.
name note: Transcript spellings are phonetic. "Claud / clad / claw / quad" is Claude. "aoral / avoral / ad tutorial / aatori / avator" all mean advertorial (and sometimes "avatar", from context). "Po" is Poe. "keto activate / ke activate" is the third-party demo product Keto Activate. "Wild Belly / W / wber" is the pet supplement brand whose advertorial is the first swipe (exact name unclear). "Dr kellyanne" is a doctor-fronted weight-loss advertorial found on weather.com. "dbh be / BHB" is beta-hydroxybutyrate.

## 1. What this source is for

It helps an operator produce a batch of advertorials (pre-sell articles labeled as sponsored content) for 1 product fast, using an AI chat model. The method has 3 parts: turn the destination sales page into a text PDF, run a fixed battery of extraction prompts to build a reusable "inputs" document, then write advertorials by modeling a proven advertorial swipe and pointing each draft at 1 avatar archetype. Variants come from swapping the avatar or the swipe. It is strong on the prompt sequence and on where the model invents facts. It is thin on why advertorials work, how to test them, and what results to expect.

## 2. Principles

1. **Use an advertorial when the destination page cannot pre-sell a cold reader.** The presenter says advertorials are "great for" short-form ecommerce pages and "great as an intermediary between an ad and a long form sales letter". His example: sending a supplement buyer list straight to a short keto product page "is not quite enough information to necessarily sell them, it probably wouldn't convert very well". Condition: his expectation, not a measured result. He gives no test comparing direct-to-page against advertorial-first. [b757b2f67584] [needs brand data: conversion rate of cold traffic sent direct to the PDP or landing page versus through a pre-sell page]

2. **Advertorials are sponsored articles and are labeled as ads.** He calls them "kind of like fake articles", saying "it says it's a sponsored article or a sponsored ad", and says they have "been used for like a century". He notes the label "advertisement" goes "right at the top". Condition: the label is part of the format in his examples; he does not discuss rules or disclosure law. [b757b2f67584] [cc252faac5f7] [web check: current FTC native advertising and endorsement guidance, and Meta and Google policies on advertorial landing pages]

3. **Build the inputs once per product, then reuse them.** The extraction prompts are "prep work but you only have to do this one time for all the advertorials you want to write". Every output goes into 1 saved document so later runs skip re-analysis. Condition: same product and same sales page. If the page changes, re-run extraction. [0d2192d48fc9] [22ce9222dfea] [5149dfc9e812]

4. **Do not stop when the page is thin.** On a short ecommerce page the model will report that a section (credible proof, social proof, common solutions, real culprit, spokesperson, anchor price) is missing. He says "if it doesn't have it no big deal", keeps running every prompt, and lets the model fill gaps, which he then edits by hand. He adds that the process is "easier if it's a sales letter". Condition: gaps filled by the model are unverified (see principle 9). [22ce9222dfea] [0d2192d48fc9]

5. **Speak to 1 segment per advertorial, not to everyone.** His prompt says "if we try to speak to everyone we'll struggle", so he asks the model for avatar archetypes "based on the data you pulled". Each advertorial is written from and to 1 archetype. He adds known market facts as constraints: "let's assume this market skews female since the weight loss market typically does". Condition: the archetypes are model output for 1 product, not validated segments. [d02a32ae552f] [needs brand data: customer demographics and reasons for purchase from orders, surveys or reviews]

6. **Model a proven advertorial's structure, style and tone.** He attaches a real advertorial for an unrelated product and first asks the model only to "analyze the structure". He says he does this "to make sure it gets what the advertorial should look like" and "I've just found these prompts really help". Then he asks for a new advertorial that follows that page's structure, style and tone for his product. Condition: his own practice, no comparison against skipping the step. The swipe gives format and flow, not claims, names or facts. [e9318cd29eae] [8d0b230d2e81] [65a962dc4285]

7. **Pick a swipe whose credibility source you actually have.** The Dr Kellyann swipe is "all about a doctor", so he says he "might not use this for Keto Activate because it doesn't have a doctor". When he does use it, he tells the model to swap the doctor for "leading health and weight loss experts" or "brand credibility in general". [8d0b230d2e81] [c8062b86370a]

8. **Do not let the model shorten the copy.** His write prompt says "effective direct response is often on the longer side so I do not want you to try to condense copy here to try to conserve outputs", and asks the model to go "section by section" and ask him to "continue" when it runs out of space. Condition: long-form direct response for a pre-sell page; he does not test length. [e9318cd29eae] [65a962dc4285]

9. **Assume the model invents people, studies, prices and testimonials.** In the demo it invented "Dr Ryan Shelton" as the expert behind the article, produced "clinical studies" he says you must "go look up and make sure these are legit because Claude will hallucinate", wrote testimonials "I think it just made these ones up", and gave a price he could not confirm. He says "there's going to be hallucinations", more so on short pages. Fix: supply the true facts up front when it is your brand, or replace them with real ones before going live. [cc252faac5f7] [e9318cd29eae]

10. **Change 1 variable at a time to build the batch.** Variants come from a new avatar on the same swipe, or a new swipe (re-analyzed first) with a new avatar. He says this could give "10, 12, 15, 20 advertorials to test in a very short period of time". Condition: the card frames this as isolating format versus audience; the presenter does not discuss test design or reading results. [c8062b86370a] [d02a32ae552f]

11. **Add specificity by hand.** He says the AI output is about "99%" there and the missing part is "judgment, specificity, things of that nature". His example edits: change "this delicious drink mix" to "this delicious chocolate drink recipe", and "the morning chocolate drink". He praises sensory details the model wrote ("tasted like a rich creamy milkshake, not a diet supplement") because "flavor is really important when you're selling consumables that you're going to eat". [e9318cd29eae] [5149dfc9e812]

## 3. Procedures

### 3.1 Prepare the source PDF (once per product) [0d2192d48fc9]

1. Open the landing page or sales letter the advertorials will send traffic to. In the demo he Googled "keto activate" and used the first result, a third-party page.
2. Copy the body copy and paste into a Google Doc as plain text (Command+Shift+V on Mac). [verify UI]
3. Expand every FAQ accordion and copy them in. He calls them "valuable to have".
4. Copy several testimonials with names (he copied 3, including "Rene G" and "Kathleen S").
5. Title the doc (his: "Keto Activate Ecom landing page for Claude") and put the page URL at the top.
6. Download the doc as PDF (File, Download, PDF). [verify UI] The PDF has no images.

### 3.2 Extraction battery (once per product) [22ce9222dfea]

Run these in 1 chat with the PDF attached. Paste each answer into a separate "Claude outputs" doc (his: "Claude outputs advertorial Keto Activate"). He bolds the section labels for his own ease. He keeps a prompts doc with an example output for each prompt (from a vision supplement) and highlights in blue the parts to change per product. The exact prompt text was promised as a link and is not in the transcript; wording below is what he read aloud.

1. **Market, pain, promise.** "Attached you'll find a sales letter for a [keto product]. I want you to analyze it and then tell me: target market, problems/pain points of the market, primary promises made." His doc includes an example output.
2. **Proof.** "Great job. Now two more things: credible proof, social proof." Credible proof means universities or a person's reference. Social proof means "X amount of people". If none exists, move on.
3. **Common solutions.** "If you were going to make a list of common solutions along with reasons they are not effective, what would be on it and what would the reasons be? Please do it in the format of the example showed a moment ago." Format: traditional solution, why it is not working, real answer. Demo output: strict ketogenic diet, keto flu, exogenous ketone supplements, fasting, excessive exercise. He considered adding "what about weight loss as well".
4. **Real culprit.** Ask what the page names as the real culprit or mechanism. Demo: difficulty staying in ketosis, answered by BHB ketones "the same ketones your body actually makes".
5. **Product facts.** Ask for a description of the product without naming it, outcome and results, spokesperson, product name, how to consume, price, and any exclusive price. The transcript suggests he removed a "claims" item from this prompt (the line is garbled) and changed "sales letter" to "sales page" ("it really doesn't matter"). Demo: 1 scoop in your favorite beverage; no spokesperson; anchor price not mentioned.
6. **Testimonials.** Ask for them. He skipped this because step 5 already returned some.
7. **Ingredients.** Ask for the ingredient list in a clean format, with any studies. He deletes the repeated "no studies are shared" lines when pasting. Demo: exogenous ketones (proprietary blend), MCT oil, monk fruit.
8. **Avatar archetypes.** "Since the market is wide ranging for this product I need your help with something. We're going to be doing several advertorials for this product. I think if we try to speak to everyone we'll struggle, so it's probably best to pick a few different avatars who we can have the advertorial come from, archetypes as it were. Based on the data you pulled, what are some of the avatar archetypes we can have the advertorial come from that would speak to specific segments of the market?" Add known constraints (his: "also let's assume this market skews female since the weight loss market typically does"). Ask for more archetypes if you want more variants. [d02a32ae552f]

Time: he reached this point about 17 minutes into the video, including explanation.

### 3.3 Find and prepare a swipe [8d0b230d2e81]

1. Browse mainstream content sites and look in the sponsored content slots. He uses weather.com. Health offers often sit there. Spy tools (none named) and sites you already read also work.
2. Click through to see where each piece goes. Dr Kellyann went to a text advertorial that links to a video sales letter. Performance Golf went straight to a VSL. He says "a lot of people go to advertorials".
3. Save the link. Pick a swipe whose spokesperson type fits your brand.
4. Paste the swipe into a doc, replace the live link with a placeholder (his: "CTA link: click here to watch the video now"), and download as PDF.

### 3.4 Write advertorial 1 [e9318cd29eae] [65a962dc4285]

1. In the same chat, attach the swipe PDF: "Here is an advertorial for an unrelated product. Analyze the structure."
2. Send the write prompt, changing the bracketed parts: "Now you're going to write a new advertorial for [product]. Follow the structure of the [swipe name] advertorial page and also the style and tone, but this will be for the [product] that you reviewed the sales page for. For the spokesperson of the advertorial, for now let's create one that matches the demographic and psychographic experience [avatar archetype]. Before going live we'll update the advertorial copy for your customer."
3. Add the 2 notes: (a) "As you begin writing, match the sound and tone of the example advertorial that you analyzed, but write for this new product and brand. Just like the example advertorial, find a good blend of storytelling and sounding like a news article report." (b) "When you write please take your time, go section by section, and just ask me to continue whenever you run out of space. We can do so over multiple outputs from you. Please keep in mind that effective direct response is often on the longer side, so I do not want you to try to condense copy here to try to conserve outputs. Take as long as you need to really capture the style and strength of that same advertorial page but for [product] in this market. Go ahead and start now, and ask me to continue whenever you're ready."
4. Read each section as it arrives. Correct mid-stream: when the model named a doctor not tied to the brand he sent "Great job so far, but instead of using Dr Ryan Shelton let's just say the article came from a world-renowned expert in holistic medicine and weight loss... with that note in mind please continue."
5. Type "continue" until the CTA section is done.
6. Paste the draft into a new doc labeled by number and avatar (his: "Keto Activate new advertorial number 1"). Clean stray heading markers.
7. Ask: "Great job. One thing, I'd love to see some alternative headline options. Can you please provide some now?" Save them under the draft. [5149dfc9e812]

His timing: writing started about 26 minutes in; 3 advertorials were done at about 47 minutes, including talk. The third came out "in one take" without "continue".

### 3.5 More variants [c8062b86370a]

- **Same swipe, new avatar:** "Great job with this. Now let's write another advertorial for [product] using the same [swipe] advertorial example as a template to model off of, but this time let's make the avatar archetype we are speaking to, and that the advertorial is coming from, the following: [archetype]."
- **New swipe, new avatar:** attach the new swipe PDF, then: "Great job. Now we're going to write another advertorial for [product]. This time we're going to model off a different advertorial example which I have attached. For this next advertorial let's focus on this avatar: [archetype]. One important note: since this is for [product] we don't have a doctor spokesperson, so instead of talking about [doctor], who is not associated with [product], we would want to talk about maybe leading health and weight loss experts or leverage brand credibility in general. Go ahead and start now." He forgot to attach the file the first time; check the attachment is there before sending.
- **Blind product:** if you do not want the product named early, edit by hand or tell the model not to mention the product name until the last section.

### 3.6 Later runs, new chat ("version 2") [5149dfc9e812] [e9318cd29eae]

1. Open a new chat (or another tool; he suggests Poe with Claude 3 when message limits run out).
2. Upload a swipe and ask the model to analyze the structure.
3. Paste in the saved inputs from 3.2 ("take the information you pulled previously") plus the archetype you want, then use the write prompt from 3.4.

### 3.7 Pre-publish edit [cc252faac5f7]

1. Replace or remove any named expert, doctor or spokesperson the brand does not have.
2. Look up every study cited. Keep only real ones; remove the rest.
3. Replace model-written testimonials with real ones from the site.
4. Correct price, offer, bundle size and shipping claims against the real offer page. [needs brand data: current price, offer, bundle sizes, shipping times]
5. Add specificity (flavor, format, ritual) where headlines are generic.
6. Set the CTA link and keep the "advertisement" label at the top.

## 4. Rules, thresholds and numbers

| rule | number or threshold | condition | source's basis | card id |
|---|---|---|---|---|
| Throughput claim | 5 to 10 advertorials per hour | once the process and inputs doc exist | presenter's estimate; title says 10 | [c8062b86370a] |
| Demo throughput | 3 advertorials in about 47 minutes | includes explaining on camera; 2 of 5 planned were skipped | demo | [c8062b86370a] |
| Prep time | about 17 minutes | 1 product, short page, with talk | demo | [22ce9222dfea] |
| Extraction prompts | 8 steps (market/pain/promise, proof, common solutions, culprit, product facts, testimonials, ingredients, archetypes) | once per product | his process doc | [22ce9222dfea] |
| Archetypes returned | 6 for 1 keto product | model output, female skew assumed | demo | [d02a32ae552f] |
| Batch size to test | "10, 12, 15, 20" advertorials | same product, avatar x swipe | his statement, not a benchmark | [c8062b86370a] |
| Testimonials copied into the PDF | 3 in the demo | short page | demo | [0d2192d48fc9] |
| Swipes used | 2 (pet supplement, doctor-fronted weight loss) | 1 product | demo | [8d0b230d2e81] |
| AI draft quality | "99%" there; "better than what 99% of copywriters would write" | his opinion, part of a sales pitch | none | [e9318cd29eae] |
| Tool cost at recording | about $20 a month (Poe or Claude paid plan, "I think") | April 2024 | his recollection | [5149dfc9e812] [web check: current pricing] |
| Advertorial history | "used for like a century" | general claim | none given | [b757b2f67584] |

## 5. Diagnostics and checks

| check | how | good | bad | next |
|---|---|---|---|---|
| Does cold traffic need a pre-sell? | Look at how much the destination page explains to a stranger | Long sales letter or rich PDP that answers pain, mechanism, proof | Short ecommerce page with a few lines, FAQs and 3 testimonials | Put an advertorial in front, or send the advertorial to a VSL or long letter. [b757b2f67584] [needs brand data: direct vs pre-sell conversion] |
| Input completeness | Read the inputs doc against the 8 extraction steps | Each section filled from the page | "Not in the copy" for proof, solutions, culprit, spokesperson, price | Fill true facts from brand records; otherwise accept and flag the gaps for editing. [22ce9222dfea] |
| Swipe fit | Compare the swipe's credibility source to what the brand has | Same type (customer story, founder, experts) | Doctor-fronted swipe for a brand with no doctor | Pick another swipe, or instruct the model to swap in brand credibility. [8d0b230d2e81] |
| Named people | Search each name against the brand | Real, associated with the brand, permission on file | Name not tied to the brand (e.g. "Dr Ryan Shelton") | Tell the model to say "a world-renowned expert" or remove. [cc252faac5f7] |
| Studies | Look up each citation | Real study that supports the stated claim | Cannot find it, or it says something else | Remove it. [cc252faac5f7] [web check: each cited study] |
| Testimonials and price | Compare to the live site | Match | Model-written quotes, unconfirmed price | Replace with real ones. [cc252faac5f7] |
| Structure match | Map draft sections to the swipe sections | Headline, personal-problem subhead, story, failed solutions, discovery, mechanism, product and taste, proof, risk-free CTA | Missing a section or product dumped in early | Ask the model to rewrite that section. [65a962dc4285] |
| Headline specificity | Read headlines for concrete details | Names flavor, format or ritual ("morning chocolate drink") | Generic ("this delicious drink mix") | Ask for 10 more headlines, add specifics by hand. [e9318cd29eae] |
| CTA fit | Check the CTA verb against the next page | "Click here to try [product] risk-free" for a product page | "Watch the video" when there is no video | Fix the CTA. The model got this right on draft 3. [65a962dc4285] |

## 6. Tools, settings and named features

- **Claude web app (Claude 3 at recording).** Used for every prompt. Attach PDFs in chat. Message caps appeared mid-demo. [verify UI] [web check: current model names and limits]
- **Poe.** Suggested as a way to keep using Claude 3 when the Claude app message cap is reached; "you can pick different models". About $20 a month "I think". [verify UI] [web check: Poe pricing and model list]
- **Google Docs.** Paste as plain text (Command+Shift+V), then download as PDF, to build the image-free source file. Also used for the prompts doc, the outputs doc and each finished draft. [verify UI]
- **weather.com sponsored content slots.** Where he finds live advertorial swipes, especially health offers. [web check: what currently runs there]
- **Spy tools.** Mentioned, none named.
- **Loom.** Only used to record the video.

## 7. Examples and case results

All are demo outputs, not results. None were run as ads.

- **Swipe 1, pet supplement advertorial (brand the presenter is an equity partner in).** Headline "A scoop a day keeps the vet away: how I keep my senior dog at heart..."; subhead "Low energy, limping and whimpering, I felt helpless until I gave my dog this bacon-flavored treat" (transcribed "baking flavor", likely bacon); personal-problem line "My dog Daisy was slowing down, I was scared of losing her"; then "Daisy is my whole world", "Discovery that changed everything", "Restoring your dog's energy and health", "Trying [product] was easy, I went to the company's website", "Thousands of owners are sharing similar stories", "An affordable, no-risk solution", "Act now, supplies won't last", CTA. [65a962dc4285]
- **Swipe 2, Dr Kellyann advertorial.** Headline "This one morning habit could change everything", labeled advertisement, heavy on credibility proof, links to a video sales letter. [8d0b230d2e81]
- **Archetypes returned for Keto Activate:** busy working mom (20s to 40s), post-pregnancy weight struggler (new mom, 20s to late 30s), perimenopausal woman (40s to 50s, fat gain, lower energy), yo-yo dieter, keto-conscious health enthusiast, post-retirement weight gainer. [d02a32ae552f]
- **Advertorial 1, busy working mom, swipe 1.** Headlines: "From Exhausted Mom to Keto Queen: How I Lost 30 Pounds and Reclaimed My Energy"; "Juggling work and family left me overweight and drained until I discovered this delicious secret weapon"; "I thought I'd never lose the baby weight but this tasty drink made keto easy". Subhead "I was drowning in mom guilt and stubborn baby weight". Sections include "Keto diet sounded promising but impossible for busy mom", "A discovery that changed everything", "Science-backed shortcut to keto success", "Trying Keto Activate was a game changer" (ordered a 3-month supply, arrived 2 days later, dark chocolate powder in coffee). Problems: invented doctor, invented studies, invented testimonials, unconfirmed price. The "30 pounds" figure is model-written. [e9318cd29eae] [cc252faac5f7]
- **Advertorial 2, perimenopausal woman, swipe 1.** Headlines: "Menopause wrecked my life until I found this delicious drink mix"; "Struggling with menopause belly, hot flashes and fatigue? Read this now"; "How I'm thriving through menopause and staying slim eating my favorite foods". Narrator "Lisa Thompson", "gained 20 pounds" (model-written), tried calorie counting, intense workouts and hormone replacement therapy. Section "The menopause metabolism shift that changed everything" explains why keto is harder in menopause; he liked this. Subheads are in all caps. [65a962dc4285]
- **Advertorial 3, post-retirement weight gainer, swipe 2.** Headlines: "Discover the morning ritual that's helping retirees shed pounds and reclaim their vitality"; "Expert reveals the surprising drink that's transforming lives in the golden years". Body includes "takes just 30 seconds a day", "developed by renowned nutritionists" and "metabolic miracle" (all model-written claims), a studies section, testimonials, and CTA "click here to try Keto Activate risk-free". Alternative headlines: "The 30-second morning mix melting post-retirement pounds"; "Retirees are raving about this fat-burning drink mix"; "Keto drink is transforming lives after 60". [c8062b86370a]

## 8. Mistakes the source warns about

- Sending cold readers straight to a short ecommerce page. "It probably wouldn't convert very well." [b757b2f67584]
- Trying to speak to everyone in 1 advertorial. [d02a32ae552f]
- Modeling a doctor-fronted swipe when the brand has no doctor. [8d0b230d2e81]
- Publishing model-named experts, studies, testimonials or prices without checking. [cc252faac5f7]
- Letting the model condense copy to save outputs. [e9318cd29eae]
- Throwing away the inputs, which forces a full re-run next time. [5149dfc9e812]
- Forgetting to attach the new swipe before sending the prompt (he did this on camera). [c8062b86370a]
- Leaving headlines generic; add specific details such as flavor. [e9318cd29eae]

## 9. Caveats, conflicts and what is missing

- **No performance evidence.** The only numbers are production speed. Nothing shows these advertorials convert, or convert better than direct-to-page. Treat every structural rule as the presenter's practice. [b757b2f67584] [c8062b86370a]
- **Invented spokespeople and first-person stories.** He says using "a fake spokesperson" is "actually not uncommon" because the page is labeled an ad, and his write prompt asks the model to create a spokesperson matching the avatar. The drafts are first-person results stories ("I lost 30 pounds", "gained 20 pounds") from people who do not exist. This conflicts with common advice and with endorsement rules that testimonials reflect real customers' honest experience and typical results. It also conflicts with the ecomOS rule "no invented claims". An agent should use real customer stories with permission, or write in a clearly editorial third-person voice without fake results. [e9318cd29eae] [web check: FTC Endorsement Guides and native advertising guidance; Meta and Google policies on weight-loss and health claims and on misleading landing pages]
- **Health and weight-loss claims.** Model output included "metabolic miracle", "developed by renowned nutritionists", weight-loss figures and menopause and post-pregnancy targeting. The presenter only flags doctor names and studies; he does not raise compliance. The cards add a compliance caveat. [cc252faac5f7] [d02a32ae552f] [web check: platform policy on personal-attribute and health targeting language]
- **Third-party product in the demo.** He wrote advertorials for a brand he does not own from its public page, so product facts were guesses. For real use, run it on your own brand with true facts supplied up front. [0d2192d48fc9]
- **Swipes are for structure only.** Cards say not to copy claims, names or brand facts from swipes. This matches the ecomOS rule that competitor ads are signals for layout and mood only. [8d0b230d2e81]
- **Exact prompts missing.** He promised links to the prompt doc and outputs; they are not in the source. Prompt wording in section 3 is transcribed from what he read aloud and may differ slightly.
- **Card overreach to note.** Card [b757b2f67584] says to keep advertorial labels and claims consistent with the destination page; the transcript does not state this. Card [d02a32ae552f] says he asked for "roughly 10" archetypes; he only said he could ask for 10 more versions. Card [0d2192d48fc9] says formatted paste "breaks" the attachment; he gives no reason beyond cleaner text. Card [c8062b86370a] frames variants as isolated tests; he does not discuss test design, traffic, metrics or winners.
- **Missing how:** how to pick which archetype to write first, how to measure an advertorial (CTR to offer, conversion, cost per purchase), how long an advertorial should be, how to design the page (images, layout, mobile), and how to route traffic from ads. [needs brand data: ad-to-advertorial CTR, advertorial-to-offer click rate, purchase conversion by archetype]
- **Stale tooling.** Claude 3, message caps and Poe pricing date to April 2024. [web check: current tools]

## 10. Card index

- [0d2192d48fc9] Advertorial input-prep: strip the sales page into a clean text PDF once
- [22ce9222dfea] Extract the sales-page input set before writing any advertorial
- [d02a32ae552f] Split one broad product into avatar archetypes for advertorial variants
- [8d0b230d2e81] Find live advertorial swipe structures to model
- [65a962dc4285] Advertorial architecture: the repeating section skeleton
- [e9318cd29eae] Prompt pattern: model a new advertorial on a swipe plus your input doc
- [cc252faac5f7] Scrub hallucinated spokespeople, studies and prices from AI drafts
- [c8062b86370a] Vary the swipe template as well as the avatar
- [b757b2f67584] Advertorial as pre-sell between ad and offer
- [5149dfc9e812] Keep a running outputs doc so later advertorial runs skip re-analysis
