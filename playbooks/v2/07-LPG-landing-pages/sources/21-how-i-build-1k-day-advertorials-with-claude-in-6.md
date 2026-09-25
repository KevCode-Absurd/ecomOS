# How I build $1k/day advertorials with Claude in 6 minutes and 41 seconds

source_id: 1l1eqD5cFx1TTOg43agY-ipNJ-uKz_m9J  |  folder: /07-LPG-landing-pages  |  cards: 7  |  words: 4311  |  type: transcript (screen-recorded YouTube video, single presenter)
credibility: The presenter is not named in the transcript. He is a dropshipping coach. He says this method scaled "a completely new drop shipping store to its first 1K a day" and that he has helped "hundreds of people" reach "1K a day, 100K months, multi6 figures, and even seven figures". He teaches an ad style of "thousand to 3,000 word sales letters". Evidence is 1 live demo plus his own opinion from testing. He shows no conversion rates, no test results, no before and after numbers for any advertorial, and no data for the $1k/day store in the title. The demo uses made-up variables and a third-party product he does not sell.
date signals: He says he plans to upload "a ton of videos in 2026", so the recording is likely late 2025 or early 2026. He names Claude (no model version), a full-page capture extension, Amazon and PageFly. The docx was modified 21 Sep 2026. [web check: current Claude file upload limits and HTML output; current name and behavior of the capture extension; current PageFly custom HTML element]
scope note: The document header says Shopify store setup belongs to 05-SET and Facebook media buying and scaling belong to 10-MCR. Ad creative length and style (the input to the congruency rule) is also covered in the ad copy and deployment folders.
name note: Transcript spellings are phonetic. "avitorials / advtorials / adversals / advvertorial" mean advertorial. "quad / claw / Cloud" is Claude. "Clarifon / clion odx" is the Clarifon cat odor eliminator used as the demo product. "VSSLs" is VSLs. "Lammo" is Lambo (a joke). "Ghost full page" is most likely the GoFullPage Chrome extension [verify UI]. "Thomas W Brener" is the Facebook page name running ads for the brand "Smoothspine".

## 1. What this source is for

It helps an operator decide when an advertorial (a sales page styled as an editorial article) is worth building, which style and length to build, and how to draft one fast with Claude. The core ideas are: build only after the ad has proven its messaging, match the page's selling load to how much the ad already sells, and pick a style by product type. The fast part is a 3-input prompt: a PDF of a swiped advertorial, a PDF of an Amazon product page, and 4 proven ad variables, with output in HTML pasted into PageFly. It is strong on the congruency rule. It is thin on testing, measurement, compliance and editing.

## 2. Principles

1. **An advertorial adds a second selling force.** Picture the buyer journey as a line from first ad view to purchase. A basic product page (generic benefits, product photos, trust elements) still leaves "all of the selling" on the ad. An advertorial means the ad and the page both push the buyer along. It lets you "educate the customer, handle objections, and intensify their desire" in a "low stakes, low pressure environment". Condition: this is the presenter's model, not a measured result. Trust elements still matter so the buyer feels safe to pay. [110546fbea50]

2. **Most dropshippers under-invest in the page.** He says most spend "all their time optimizing creatives" and "spam testing" ads but "can never get to consistent profitability" because the page is ignored. The landing page is "one half of your audience's buying journey". Condition: his opinion, no data. [110546fbea50]

3. **Advertorials amplify winning messaging. They do not create it.** "Advertorials are not a magic bullet." He applies this to any landing page other than a product page: advertorial, listicle, long-form sales page. Build one only after ads have confirmed 4 variables: avatar, desire, angle and unique mechanism. Condition: he says "there is a caveat", "not always, but the overwhelming majority of the time" an advertorial launched before any ad test "is unlikely to convert". He does not say what the exception is. [0623f1ad4849] [needs brand data: which ads convert at break-even or better, and the avatar, desire, angle and mechanism in each]

4. **The proof bar is break-even on a product page.** Get ads "converting to a product page first", confirm the 4 variables, and build once the ad is "converting at least break even". His example: "even if you are at break even on an ad with a thousand bucks in spend", a congruent page "will have a much higher success rate". Condition: presenter heuristic. He does not define break-even (ROAS 1.0 on revenue or on contribution margin) and gives no success rate. [0623f1ad4849] [needs brand data: break-even ROAS from product cost, shipping, fees and margin]

5. **Less selling in the ad means more selling on the page, and the reverse.** He calls this "a simple paradigm that is not always true but the overwhelming majority of the time is true". Before writing, "consider the mindset of someone who has just consumed the ad they'll be coming from". A clickbait image that "sells the click" needs a long advertorial with a long lead. A long ad (story, sales letter, long UGC, VSL) needs a shorter advertorial that shows the product early. He calls ignoring this "probably the biggest mistake". [ffdf5c3a30ff] [e74fd721f7f7]

6. **Pick the style by product type.** Improvement product (a better version of something known, like bed sheets with a silver lining or an antibacterial fabric): personal stories of people who "tried a bunch of failed solutions like the other products in the category" and then solved the problem. Innovation or gadget (something the market "has not seen before" or never "considered as a solution"): a "breaking news" or "big revelation" frame, such as "revolutionary device", that gets "straight into the selling" faster. Condition: "I find", from his own work, no numbers. "One advertorial style does not work for others." [e74fd721f7f7]

7. **Swipe a page that already converts, and look outside your niche too.** Same-niche swipes give "confidence going into an advertorial test" that the page works "for a similar product". Out-of-niche swipes can give an edge because "people in one niche are just copying each other", so you can "introduce the market to different types of avatars they've never seen before". Condition: same niche is a confidence boost, not a must. His demo prompt used an advertorial "from another brand in a different niche". [64349a706993]

8. **Keep proven ad messaging fixed when the AI rewrites.** Give Claude the 4 variables and tell it they "must remain consistent because they are proven winning messaging from our ads". The swipe supplies structure. The variables supply the message. [6ec3aac63864]

9. **AI output is a draft skeleton.** He says the result gives "90% of the page built" and, a sentence later, "80% of the skeleton done". Expected edits: headline, lead, mechanism explanation, and real images. Condition: he did not edit or review the demo output on camera. [6ec3aac63864] [2424ba647b51]

## 3. Procedures

### 3.1 Decide the advertorial type and length (before any prompt) [e74fd721f7f7] [ffdf5c3a30ff] [0623f1ad4849]

1. Classify the product: improvement (better version of a known product) or innovation (new, or never considered as a solution to the problem).
2. Pull the ads that will send traffic to the page. Judge how much selling each one does:
   - Low selling: a clickbait image with little or no body copy, built for cheap clicks.
   - High selling: long-form personal stories, 1,000 to 3,000 word sales letters, 1 to 2 minute AI UGC videos, 4 to 5 minute VSLs, or any ad with a full problem, agitate, solution run.
3. Set the lead length:
   - Low-selling ad: long lead. Remind the reader of the problem, agitate the pain, intensify desire, then introduce the product. In his example, the reader scrolls about 50 to 60% of the page before learning a product is being sold.
   - High-selling ad: short lead. Show the product in the top image and in the first few lines. "You don't need an advertorial that's 3,000 words long."
4. Set the frame: improvement product uses a failed-solutions personal story. Innovation uses breaking news or revelation.
5. From the winning ad, write down the avatar, desire, problem, angle and unique mechanism. [needs brand data: the winning ad's copy and results]

### 3.2 Extract the 4 variables from a winning ad [0623f1ad4849]

1. Take an ad that has converted at break-even or better (his example: about $1,000 spend at break-even).
2. Avatar: who the ad speaks to. Example (Smoothspine ad): retired senior men with sciatica who "can't move around anymore".
3. Problem and desire: stated plainly in the ad. Example: sciatica.
4. Unique mechanism: the named product mechanism and how it works. Example: a "spinal decompression home device" that takes pressure off the sciatic nerve "by gently stretching the spine and forcing the fluid in your bulging discs back into place", explained by a physical therapist in the ad copy.
5. Angle: he says the Smoothspine ad is missing an angle, and he does not show how to name one. The source is thin here.
6. Check for longevity: the example ad was 1 day old, but "they had other variations that have been on for months". He uses long-running variants as a sign the messaging works. [web check: Meta Ad Library run dates for any competitor ad used as a reference]

### 3.3 Find a swipe [64349a706993]

1. Open an affiliate page that aggregates many advertorials across niches. He calls these one of his "favorite places to swipe" because of the quantity and range. He does not name one.
2. Pick an advertorial that matches your product type (improvement or innovation) and, ideally, your niche.
3. Also scan other niches for structures or avatar treatments your niche has not used.
4. Note its section order so you can check the AI's output against it. The demo swipe's structure, as Claude read it: urgency banner, curiosity headline, author intro, problem, agitation, product reveal, mechanism, quality, social proof, price justification.

### 3.4 Draft the advertorial in Claude (his demo run: 6 minutes 41 seconds) [6ec3aac63864]

1. Open the swipe advertorial. Capture the full page with a full-page screen capture extension ("Ghost full page", likely GoFullPage) and download it as a PDF. [verify UI]
2. Go to Amazon. Find your exact product or "a very similar product". Expand all highlights and feature sections. Capture the full page and download it as a PDF. [verify UI] (He uses this so Claude "can actually understand my product".)
3. Open Claude. Attach both PDFs. [verify UI: file upload limits]
4. Write the 4 variables: avatar, problem, desire, unique mechanism. Use confirmed ones from your ads. He made them up for the demo and says "don't do what I'm doing here". Demo values: avatar "senior women in their 60s who don't yet realize how cat pee odor exposes them to ammonia which can harm their health"; problem "cat pee smell"; desire "freedom from fear pain"; mechanism pasted from the Amazon listing ("UVC molecular neutralization", as Claude later restated it).
5. Send the instruction. His prompt, lightly cleaned from the transcript:
   > "I sell the [product]. I'm attaching a PDF of the Amazon sales page so you can understand the product. I'm also attaching an advertorial from another brand in a different niche. My goal in this session is to create the same advertorial that I'm giving you an example of, but for my product. I'm also giving you 4 key variables that must remain consistent because they are proven winning messaging from our ads: the avatar, the desire, the problem we solve and the unique mechanism. Keep these elements consistent and create the advertorial in HTML that's exactly like the one I am giving you but for my product."
6. Read Claude's plan before the output. In the demo it first restated the swipe's section list and the 4 variables it would keep. Check that both are right.
7. Wait for the HTML. In the demo it did not finish inside 5 minutes. He needed an extra 1 minute 40 seconds, and says Claude seemed to stall ("I think claw just broke").
8. Edit: headline, lead, mechanism explanation, and replace placeholder images with real images. See section 5 for the checks he skips.

### 3.5 Deploy on Shopify with PageFly [2424ba647b51]

1. In PageFly, create a blank page. [verify UI]
2. Add a custom HTML section or element. [verify UI]
3. Paste the full HTML from Claude.
4. Hide the theme header and footer so the page reads as an article, not a store page. [verify UI]
5. Use the page builder's page list to track all advertorial pages.
6. He says "I'm sure there's a way to do it for free natively with Shopify" but prefers a page builder for header and footer control and page tracking. He does not show the native route. [verify UI: Shopify custom liquid or page template that hides header and footer]

## 4. Rules, thresholds and numbers

| Rule | Number or threshold | Condition | Source's basis | Card |
|---|---|---|---|---|
| Build advertorial only after ad proof | Ad converting at least break-even to a product page | "Overwhelming majority of the time"; exception not described | Presenter experience | [0623f1ad4849] |
| Example proof level | Break-even on about $1,000 ad spend | Example, not a minimum | Presenter example | [0623f1ad4849] |
| Variables to confirm first | 4: avatar, desire, angle, unique mechanism | His prompt swaps angle for problem | Presenter framework | [0623f1ad4849] [6ec3aac63864] |
| Low-selling ad needs long lead | Product appears after about 50 to 60% of scroll | Clickbait image with no body copy | 1 observed page | [ffdf5c3a30ff] |
| High-selling ad needs short page | Product in top image and first few lines | Ad is long story, sales letter or VSL | 1 observed page | [ffdf5c3a30ff] |
| High-selling ad lengths | 1,000 to 3,000 word ads; 1 to 2 min AI UGC; 4 to 5 min VSL | Then no 3,000 word advertorial needed | Presenter opinion | [ffdf5c3a30ff] |
| Improvement product style | Failed-solutions personal story | Better version of a known product | "I find" | [e74fd721f7f7] |
| Innovation product style | Breaking news or revelation, faster to the product | New product or new solution type | "I find" | [e74fd721f7f7] |
| Claude draft time | Claimed under 5 min; actual 6 min 41 s | 1 demo, includes PDF capture | Stopwatch on camera | [6ec3aac63864] |
| Draft completeness | "90% of the page" and "80% of the skeleton" | His estimate, not checked | Opinion | [6ec3aac63864] |
| Same-niche swipe | Nice to have | Out-of-niche can give an edge | Opinion | [64349a706993] |

## 5. Diagnostics and checks

| Check | How | Good | Bad | Next step |
|---|---|---|---|---|
| Is the messaging proven? | Look up the feeding ad's results on a product page | At or above break-even with meaningful spend (his example: about $1,000) | No ad test yet, or below break-even | Keep testing ads; do not build the advertorial yet [needs brand data: ad results and break-even ROAS] |
| Does page length fit the ad? | Rate the ad: clickbait image vs long story or VSL | Low-selling ad paired with long lead; high-selling ad paired with early product reveal | Long VSL traffic sent to a 3,000 word page, or clickbait traffic sent to a product page | Rewrite the lead length (section 3.1) |
| Does the style fit the product? | Improvement or innovation? | Improvement uses failed-solutions story; innovation uses revelation | Swipe copied from the other product type | Pick a new swipe |
| Did the variables survive? | Compare the draft to your avatar, desire, problem and mechanism | Same avatar, same mechanism wording, same desire | Claude drifted to the swipe's avatar or mechanism | Re-prompt with the variables |
| Did the structure survive? | Compare section order to the swipe | Same sections in the same order | Sections dropped | Ask Claude to add the missing section |
| Invented proof (do-not-copy) | Read every testimonial, review count, author name, expert, study, stat and price | All real and on file | Names, quotes, doctors, "physical therapist" claims or numbers not on file | Replace with real proof or cut. Not covered by the source. [needs brand data: real reviews, real expert, real prices] |
| Claims borrowed from Amazon | Compare product claims to your own product's specs | Every claim true for your product | Claims taken from "a very similar product" | Cut or verify [needs brand data: product specs and test results] |
| Health and fear claims (do-not-copy) | Scan for disease, pain, harm or cure claims | None unless proven and allowed | "Ammonia can harm their health", "forcing fluid back into bulging discs" | Remove or substantiate [web check: Meta health claim policy and local ad law] |
| Disclosure | Is the page labeled as advertising? | Clear label | Page presented as real news with no label | Add a label. Source is silent. [web check: FTC native advertising guidance, Meta landing page policy] |
| Deployment | Open the published page | Header and footer hidden, HTML renders, images load | Theme header shows, broken layout | Fix in PageFly [verify UI]. Mobile check not covered by the source. |

## 6. Tools, settings and named features

- **Claude** (chat app): takes 2 PDF uploads plus a prompt, returns an advertorial in HTML. No model version named. [verify UI] [6ec3aac63864]
- **"Ghost full page"** (likely GoFullPage browser extension): captures a whole scrolling page and downloads it as a PDF. [verify UI] [6ec3aac63864]
- **Amazon product page**: product information source. Expand "all the highlights and the features" before capture. [6ec3aac63864]
- **Affiliate advertorial hub pages**: swipe library, not named. [64349a706993]
- **PageFly** (Shopify page builder): blank page, custom HTML section, hide header and footer, page list for tracking. [verify UI] [2424ba647b51]
- **Shopify native route**: mentioned as likely possible, not shown. [verify UI] [2424ba647b51]

## 7. Examples and case results

All examples. None comes with conversion numbers.

- **Smoothspine ad** (page "Thomas W Brener"): used to show 3 of the 4 variables in 1 ad. Avatar: retired senior men with sciatica. Problem: sciatica. Mechanism: physical-therapist-explained spinal decompression home device. Angle: missing. The ad had run about 1 day; other variants had run for months. Do-not-copy: the ad fronts a personal name page and a "physical therapist" and makes a medical mechanism claim. The source does not say whether the person or therapist is real. Use for structure only. [0623f1ad4849]
- **Long-form story ad (about 1,000 words, problem-agitate-solution)** paired with an advertorial that shows the product in the top image and in the first few lines. [ffdf5c3a30ff]
- **Clickbait image ad (no copy after the first line)** paired with an advertorial where the product appears after about 50 to 60% of the scroll. [ffdf5c3a30ff]
- **Improvement example**: bed sheets with a silver lining or antibacterial fabric. Style: personal story of failed alternatives. [e74fd721f7f7]
- **Innovation example**: a page using "revolutionary device" and getting to the product quickly. [e74fd721f7f7]
- **Clarifon demo**: third-party cat odor device. Made-up variables. Out-of-niche swipe. Claude mirrored the swipe structure and he calls the result "a pretty crazy recreation", "pretty much on the money". Time: 6 min 41 s. He shows no edits and no results. [6ec3aac63864]
- **Title claim**: "$1k/day" refers to a store he scaled with AI advertorials. No page, spend, conversion rate or time frame is shown for that store. Treat as a claim, not a result.

## 8. Mistakes the source warns about

1. **Building the advertorial first.** Launching an advertorial before testing any ads, before the messaging is proven. "Unlikely to convert." [0623f1ad4849]
2. **Building the wrong advertorial for the product and awareness level.** Using an improvement-product style for an innovation, or the reverse. [e74fd721f7f7]
3. **Ignoring ad-to-advertorial congruency.** Copying "whatever page they find" without checking how much selling the ad already did, "then they wonder why it doesn't work". He calls this "probably the biggest mistake". [ffdf5c3a30ff]
4. **Sending low-selling ad traffic to a product page.** "I can't send this traffic to a product page because I haven't sold them" on anything. [ffdf5c3a30ff]
5. **Relying only on the ad.** Endless creative testing while the page is a basic product page. [110546fbea50]
6. **Making up the 4 variables.** He does it in the demo and says not to. [6ec3aac63864]
7. **Shipping raw AI output.** Tweak the headline, lead and mechanism, and add real images. [6ec3aac63864] [2424ba647b51]

## 9. Caveats, conflicts and what is missing

- **Disguise vs disclosure.** He says an advertorial is "disguised as an editorial. It's not meant to look like an actual sales letter." He never mentions an "advertisement" or "sponsored" label. Source 08 in this folder shows the label at the top of its advertorials. Common practice and ad platform rules expect native ads to be identifiable as ads. Treat the disguise as the article format only, and label the page. [110546fbea50] [web check: FTC native advertising guidance; Meta and Google landing page policies]
- **"Exactly like" the swipe vs ecomOS rules.** His prompt asks for an advertorial "exactly like the one I am giving you but for my product". ecomOS rules allow competitor pages as signals for layout and structure only, never their text, faces, names or products. Rephrase the ask as "follow the section order and pacing, write all copy fresh from our variables and facts".
- **Invented proof risk (do-not-copy).** The swipe had an author intro and social proof. Asking Claude to mirror it for a new product will produce an author, testimonials and possibly a price justification with no real source. He does not check any of this. Every name, quote, review count, expert and number must be real and on file. [needs brand data: reviews, founder or expert, price history]
- **Amazon listing of "a very similar product".** Using another seller's listing as product input can carry over claims that are not true for your product. Use your own specs where you have them. [needs brand data: product specs]
- **Health and fear claims (do-not-copy).** The demo avatar says ammonia from cat urine "can harm their health", and the Smoothspine example claims fluid is forced "back into bulging discs". Neither is supported in the source. [web check: claim substantiation and Meta health policy before any similar claim]
- **Variables are inconsistent.** The rule says avatar, desire, angle, mechanism. The Smoothspine walk-through lists "avatar, problem, desire, angle and unique mechanism". The prompt drops angle and uses problem. Treat the working set as 5: avatar, problem, desire, angle, mechanism. He never shows how to find or phrase an angle.
- **Break-even is undefined.** No ROAS number, no margin basis, no minimum sample beyond the $1,000 example. [needs brand data: break-even ROAS]
- **"Not always true."** Both the build-after-proof rule and the selling-pressure rule are hedged as true "the overwhelming majority of the time". He does not describe the exceptions.
- **Completeness numbers conflict.** "90% of the page" and "80% of the skeleton" in the same breath. Neither was measured.
- **No testing or measurement.** Nothing on how to A/B test the advertorial against the product page, which metrics to read (click-through to product page, conversion rate, AOV), how long to run, or when to kill it. [needs brand data: page-level conversion and click-through]
- **No mobile, speed or image guidance.** Nothing on how the HTML renders on phones, page speed, or where images come from. ecomOS rule: use the real product photo where accuracy matters.
- **Amazon may not carry the product.** Not addressed. For a brand with its own catalog (for example Gehna), the brand's own product page and specs are the better input.
- **Fit with other sources.** The long lead for cold, low-selling traffic agrees with general direct-response practice. The rule that long ads need short pages is his own framing; check it against the other advertorial sources in this folder during Pass 2.

## 10. Card index

- [110546fbea50] Advertorials Split Selling Pressure With the Ad
- [0623f1ad4849] Validate Four Ad-Level Variables Before Building the Advertorial
- [e74fd721f7f7] Choose Advertorial Style by Product Type: Improvement vs Innovation
- [ffdf5c3a30ff] Match Advertorial Length to How Much Selling the Ad Already Did
- [64349a706993] Swipe Proven Advertorial Structures From Affiliate Hubs
- [6ec3aac63864] Claude Advertorial Workflow: PDFs In, HTML Out
- [2424ba647b51] Deploy Advertorial HTML on Shopify via PageFly Custom HTML Block
