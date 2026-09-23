# Landing Pages — draft playbook

**Status:** source-linked draft; not owner-approved or outcome-tested.

Read [the operating contract](../OPERATING_CONTRACT.md) before using a workflow.

## Inputs
- Product facts
- traffic source
- audience
- offer
- proof
- existing page
- constraints

## Measures
- Purchase conversion
- contribution per visitor
- message comprehension

## Foundation candidates
Inferred principle labels do not establish universal applicability. Retain source conditions; empty means no matched labelled principle, not absence of foundational knowledge.

- **Build a physical-product hero around outcome, mechanism, proof, and reassurance** (`12c3e5742646afd432cd5a5c`): A product hero should pair a clear customer outcome with an honest explanation of how the item delivers it, a direct purchase action, relevant proof, and friction reducers.
  Applies when: Designing the above-the-fold portion of a PDP or dedicated single-product campaign page for cold traffic.
  Condition: The source’s preference for stacking two forms of social proof reflects its agency experience, not a guaranteed lift.
  Condition: Do not imply endorsements, fabricate reviews, or present generic logos as evidence of product performance.

- **Traffic-Aware Above-the-Fold Layouts by Awareness Stage** (`0c22726bae24b46f8c967986`): Match the first screen to how aware the visitor is: educate for interruption traffic, lead with proof and a form for high-intent search.
  Applies when: When designing the top of a campaign landing page or PDP for a specific traffic source such as Meta, Google, or organic search.
  Condition: The source's own site is cited as the example of the search-traffic pattern; this is not an independent benchmark.
  Condition: Awareness assumptions should be validated against funnel data rather than assumed.

- **Match the Product-Page Hero to Traffic Awareness** (`af3eaeba1a44d8149e6d521d`): Lead with product selection for high-intent visitors, but lead with the problem, mechanism, and product relevance when campaign traffic is less aware.
  Applies when: Choosing the above-the-fold structure for a PDP, collection landing page, or advertorial-to-product journey based on acquisition source and shopper intent.
  Condition: Awareness is a planning heuristic, not a substitute for analytics. Validate with product-page engagement, add-to-cart rate, and purchase conversion by source.
  Condition: Education must not make unsupported scientific, health, or root-cause claims.

## Write a product landing page
Workflow ID: `landing-pages.write-page`

**Deliverable:** Complete section-by-section landing-page copy

### Proposed decision sequence
1. Match the page promise to traffic intent and supported customer need
2. Order benefits, mechanism, proof, offer and objections around purchase decisions
3. Write finished sections using approved facts and a consistent CTA

### Supporting knowledge candidates
These cards were ranked locally for this task. They are evidence to assess, not proof that every proposed step is supported. Full steps and conditions are retained below.

#### Voice of Customer Research Before Writing Any Copy
Card: `10b436ef5145c8ef197e19f2` · Source: The NEW Way Of Landing Pages in 2026.docx · Section: 0

Harvest exact customer language, pain points and objections from Reddit, sales calls and qualitative testing before drafting page copy.

Applies when: Starting a new landing page, PDP rewrite or advertorial and you need the raw material for headlines, pain sections and objection handling.

- Mine secondary sources: Reddit threads, YouTube comments, forums in your product category. Record recurring themes and the exact words customers use, not your industry's jargon.
- Interview internal stakeholders who talk to buyers — sales team, customer support, founders. Ask what objections come up most and what a typical sales conversation looks like.
- Run qualitative user testing with a tool like UserBrain: give real customers a set of tasks on your site and ask them to think aloud. A 30-minute recording per person surfaces confusion and the phrasing they use unprompted.
- Pull demographic and interest breakdowns from Google Analytics to segment who is actually arriving.
- Capture, per segment: pain points, dream outcomes/goals, needs and wants, demographics (age, gender, income, personality), and common objections.
- Sort the raw language into a research document, then map each phrase to the section it will feed — headline, pain point, proof or value prop. The copy should be assembled from this document, not invented.
- **Condition:** This is qualitative input; themes from forums may skew toward the most vocal users rather than the average buyer.
- **Condition:** Verify any third-party tool's current pricing and interface before committing.

#### Follow Jakob's Law: familiar layouts beat creative reinvention
Card: `a556c62817f0cb335d4f5222` · Source: I Studied 1000 Landing Pages, Here's What Works in 2025.docx · Section: 0

Users expect landing pages to look and function like other sites they use, so standard structures (one headline, close body copy, top social proof, CTA) convert better than clever deviation.

Applies when: Choosing a landing page layout, template or redesign direction, especially when balancing brand creativity against conversion goals.

- Apply Jakob's Law: because users spend most of their time on other sites, they expect your page to follow familiar patterns — deviating from standard structure forces them to relearn navigation and hurts conversion.
- Adopt the source's baseline structure: one clear headline, body text in close proximity to the headline, social proof near the top, CTA button directly underneath, FUD reducers beneath the CTA, and an image or video.
- Avoid the minimalist trap of headline-only pages with no body text and no CTA — minimalism that removes clarity removes action.
- Avoid multi-headline hero sections, oversized social proof that overpowers the headline, and body copy that sits far from the headline.
- Before shipping a novel layout, ask whether the creativity comes at the cost of clarity; if yes, revert to a standard pattern.
- When the layout is unconventional, run an A/B test against a familiar-layout control rather than assuming the creative version wins.
- **Condition:** Jakob's Law is a UX heuristic, not a conversion guarantee; some strong brands convert well with differentiated design.
- **Condition:** This contradicts advice to stand out visually — the source frames it as a trade-off favoring clarity over creativity when conversions are the goal.

#### Write PDP Headlines for Scanners
Card: `2877b10aa93fd325b229d989` · Source: The Only Landing Page Guide You'll Ever Need.docx · Section: 2

Assume many shoppers scan headings rather than read every paragraph, so every heading should communicate a standalone product benefit or decision aid.

Applies when: Writing product-page headings, campaign-page section titles, bundle descriptions, comparison blocks, and testimonial summaries.

- Audit every heading without its body copy. A shopper should still understand the key benefit, use case, or proof point from the heading alone.
- Replace generic labels with benefit-led statements. Instead of “Ingredients,” state the relevant shopper implication, then provide the ingredient details beneath it; instead of “Reviews,” summarize the genuine theme of the proof.
- Use a clear hierarchy: the hero claim first, then the most important decision information, followed by supporting details. Use type size, weight, and color contrast to distinguish headings from body copy.
- Keep body copy available for substantiation and product specifics, but do not force shoppers to read it to understand why a section matters.
- Apply the same scanning discipline to review cards: a short, accurate summary heading can surface the relevant usage outcome, while the full verified review remains available below.
- **Condition:** The source cites a general rule of thumb that people read only a small portion of page content; treat it as a rationale for clear information design, not a precise measurement of your traffic.
- **Condition:** Do not edit testimonial headings in a way that changes what the reviewer actually said.

### Retrieval and applicability
Search: `product landing page headline proof objection copy`
Related domains: avatars, ad-copy-deployment, offers, testing
Mixed-folder candidate IDs: 010fe64918f47b6230e2899e, e1abe7ca30f5e8577e6ad432, 1c351701fc029c4cb73bae3a

- Does this advice fit the product lifecycle, market, audience and requested deliverable?
- Does it require proof, access, budget or assets the brand does not have?
- Does it change a fixed price, offer, policy or other explicit constraint?
- Are platform details or numerical claims current and substantiated?

### Output checks
- Deliver the specified artifact, not general advice about creating it.
- Use supplied brand facts; label hypotheses and missing inputs separately.
- Preserve relevant source conditions; do not copy another business’s proof or results.
- Include an owner, measurement and decision rule when proposing a test.
- Check the output against the requested constraints and owner feedback.

Stop after the requested artifact passes factual and brief checks; allow at most two revision passes, then report the unresolved issue.

## Create a landing-page hero brief
Workflow ID: `landing-pages.hero-section`

**Deliverable:** Hero copy and layout brief

### Proposed decision sequence
1. Choose the single promise that matches visitor awareness
2. Combine clear product identification, relevant proof and CTA
3. Specify mobile hierarchy and visual requirements without fabricated proof

### Supporting knowledge candidates
These cards were ranked locally for this task. They are evidence to assess, not proof that every proposed step is supported. Full steps and conditions are retained below.

#### Hero Headline Formula: End Result + Time Period + Emotional Payoff
Card: `59be84f0758c5860c10e1ca6` · Source: The NEW Way Of Landing Pages in 2026.docx · Section: 0

Write the above-the-fold headline with three components and never lead with who you are or what you do.

Applies when: Writing or rewriting the hero section of a landing page, PDP above-the-fold block or paid-traffic advertorial.

- Build the headline from three parts: the end result the customer wants (e.g. 3x your revenue, lose weight, calm your horse), a time period (24 hours, 2 weeks, 12 weeks), and the emotional payoff (how they feel once they have it).
- Reorder the three parts to whatever reads naturally; the source's sequence is not fixed.
- Do not open with who you are or what your company does — the source calls this a massive waste of space. The headline only has to answer 'what's in it for me?'
- Worked ecommerce example from the source: 'Calm your horse… enjoy safer, happier rides… in just 2 weeks' — end result, emotional payoff, time period for a horse-supplement brand.
- Write the sub-headline as pain point first (if applicable), then the solution, then list the unique components from your offer decomposition that deliver the headline result.
- Above the fold also needs at least two forms of relevant social proof (reviews, stats, press), FUD-reducing copy near the CTA, and one image or video that reinforces the core value prop — not a decorative shot.
- **Condition:** The formulas are the source's proprietary framework; they have not been validated by independent testing in the material.
- **Condition:** A time-period claim must be defensible for your product and category — do not insert a number you cannot substantiate.

#### Above-the-fold hero formula for landing pages
Card: `f4cbc2b893ed2250e6331bc1` · Source: I Studied 1000 Landing Pages, Here's What Works in 2025.docx · Section: 0

A six-element hero section (benefit headline, USP sub-headline, two social proofs, CTA, risk reducers, complementary image) that captures the majority of visitors who never scroll.

Applies when: Building or redesigning the topmost section of a product, offer or lead-capture landing page for paid traffic.

- Treat the above-the-fold area (visible without scrolling) as the make-or-break section: the source states a large share of users never scroll past it, so put 80–90% of early effort here.
- Write one benefit-driven headline that answers 'why should I care?' and ties to the customer's dream outcome. Avoid stating who you are, what you do, jargon or vague phrasing.
- Add a sub-headline that carries your USP — who you are and why you differ from competitors.
- Include at least two forms of social proof above the fold (reviews, testimonials, featured-in) to build credibility and give a reason to scroll.
- Place a clear, action-oriented CTA button that stands out visually.
- Directly beneath the CTA, place FUD reducers (free trial, money-back guarantee, easy returns, warranty) to defuse online-purchase anxiety.
- Add one image or video that complements the messaging and subtly communicates the offer.
- Run A/B tests on the headline and on the FUD block separately — the source reports these two elements alone produced large lifts for agency clients, but treat those figures as case examples, not guaranteed results.
- **Condition:** Conversion lifts cited (e.g., 80% from headline alone, 40–60% from FUD testing) are the source's agency case-study examples, not universal benchmarks.
- **Condition:** Apply to landing pages for a specific offer; top-of-funnel ad scaling belongs elsewhere.

#### Test the above-the-fold section first — it is the highest-leverage area
Card: `cb7820a5960b6a281e8be4fa` · Source: Alex Hormozi's Advice on Landing Pages.docx · Section: 0

The top of the page is the only section 100% of visitors see and roughly 60% never scroll past it, so headline and hero image tests generate the largest gains.

Applies when: Choosing which page element to test next on a landing page, PDP, or homepage when you can only run one experiment.

- Treat the above-the-fold area (headline and the image below it) as the default testing target, especially in early optimization stages. The source advises spending the vast majority of early effort there.
- Test the headline first, then the hero image underneath it. The source's agency says nearly all of the biggest conversion jumps come from these two elements, with headline tests producing lifts in the 60–80% range and above-the-fold tests reported as high as 130% across both B2B and ecommerce clients.
- Justify prioritization with two facts the source cites: 100% of visitors see the above-the-fold area, and statistically about 60% never scroll past it, so changes below the fold are only ever seen by a minority.
- Keep one change per test so you can attribute the lift to the headline or the image rather than a combined redesign.
- Once the above-the-fold is strong, move budget and test slots to lower sections such as trust elements or product-detail modules.
- **Condition:** The 60% no-scroll figure and the percentage lifts are source-reported approximations and case examples, not universal benchmarks.
- **Condition:** Some product categories need scroll depth for considered purchases; test whether adding above-the-fold information changes scroll behavior.

### Retrieval and applicability
Search: `hero headline product page above fold clarity`
Related domains: avatars, ad-copy-deployment, offers, testing
Mixed-folder candidate IDs: f792955c5fb659be723119f0, 1cd22fa872f7e953a41c9c91, 7d460350a38096003d9e2fa5

- Does this advice fit the product lifecycle, market, audience and requested deliverable?
- Does it require proof, access, budget or assets the brand does not have?
- Does it change a fixed price, offer, policy or other explicit constraint?
- Are platform details or numerical claims current and substantiated?

### Output checks
- Deliver the specified artifact, not general advice about creating it.
- Use supplied brand facts; label hypotheses and missing inputs separately.
- Preserve relevant source conditions; do not copy another business’s proof or results.
- Include an owner, measurement and decision rule when proposing a test.
- Check the output against the requested constraints and owner feedback.

Stop after the requested artifact passes factual and brief checks; allow at most two revision passes, then report the unresolved issue.

## Choose an appropriate landing-page format
Workflow ID: `landing-pages.select-page-format`

**Deliverable:** Page-format decision and wireframe outline

### Proposed decision sequence
1. Assess how much explanation the product and audience need
2. Compare direct PDP, guide and advertorial approaches
3. Define a test preserving offer and attribution consistency

### Supporting knowledge candidates
These cards were ranked locally for this task. They are evidence to assess, not proof that every proposed step is supported. Full steps and conditions are retained below.

#### Pick the Awareness Stage, Then Choose the Headline Type
Card: `d235019925fc049ac7c56338` · Source: Psychological Tricks I Used To Sell $1 Billion in Products Online - Craig Clemens.docx · Section: 2

Match your headline to what the reader already knows: symptom-first for unaware buyers, contrarian category-claim for aware buyers.

Applies when: You're choosing between a problem-led and a contrarian headline on a PDP, advertorial or landing page.

- For unaware audiences: use a symptom or consequence headline that presumes nothing about your category, then teach. Clemens used 'digestive health' framing in early probiotic ads.
- For aware audiences: use a pattern-interrupt that contradicts a belief they already hold — 'throw your probiotics in the trash' — and deliver the counter-explanation on the page (not enough strains, prebiotics matter, etc.).
- The contrarian headline only converts if the reader has a prior belief to disrupt; on a clueless audience it reads as nonsense.
- Keep the proof and dream elements of the seven hijacks after the headline: the page still needs demonstration, believable proof and a vivid outcome.
- **Condition:** Clemens' examples are his own campaigns; timing and performance aren't transferable as benchmarks.
- **Condition:** Contrarian claims may be scrutinised by ad platforms and regulators — keep them defensible.

#### Six Advertorial Formats and the Obstacle Each Solves
Card: `68ab05281912cda9fb4a6c19` · Source: $100 Million Advertorial Formula.docx · Section: 0

Map each of the source's six advertorial formats to the specific buyer obstacle it is designed to overcome.

Applies when: Selecting which advertorial angle to write when cold-traffic conversion is blocked by a known objection.

- Storytelling: emotional, identity-driven narrative (e.g. a 72-year-old grandmother's foot-pain fix) that introduces a unique mechanism — use for cold, unaware traffic with emotional problems and identity framing.
- Authority Expert: a real or perceived expert (dermatologist, veterinarian, doctor) gives the reader 'permission' to buy — strong in health, beauty, pain relief and pet niches.
- Buyer's Guide / comparison: a 'Top 5' style listicle that names and discredits real competitors before crowning the featured product.
- Beauty Review / Scandal-Whistleblower: positions a small lab against a corrupt industry (the example cites a $511B beauty industry) to tap distrust of big corporations.
- Case Study: documents a problem, the failure of standard solutions one by one (e.g. discrediting each prescription then surgery), and the product's eventual success.
- Listicles / 'reasons why': a numbered list of reasons to choose the product, handling objections such as time cost alongside comparisons.
- Match the format to the obstacle: low trust → story plus early proof; need for permission → expert; too many options → comparison; skepticism/'seen it all' → buyer's guide; 'will this work for me?' → case study or targeted objection handling.
- **Condition:** The presenter admits some examples use AI-generated or possibly non-existent 'doctors'; he says he does not recommend fake doctors.
- **Condition:** Format effectiveness varies by niche and awareness level — treat the mapping as a starting hypothesis to test.

#### Test multiple advertorial variants instead of trusting one draft
Card: `1bc5a164d45765175642fd25` · Source: The Most Valuable 60 Minutes on Advertorials You'll Ever Watch.docx · Section: 2

Treat the advertorial as a hypothesis: write variations and expect only some to win, guided by the awareness portfolio.

Applies when: Moving from a single advertorial draft to a testing plan for a new product launch.

- Generate several advertorials spanning archetypes (warning, breaking news, origin) and awareness levels.
- Distribute them per your awareness portfolio (e.g., 30% unaware, 30% problem-aware, rest solution/product/most-aware).
- Run them and let data decide which angle wins, not internal preference.
- Iterate the winning angle by tightening headline, subheads and CTA placement.
- **Condition:** The presenter explicitly says he doesn't know for certain any angle will work — treat all as hypotheses.
- **Condition:** Don't change too many variables between variants if you want to learn which element drove performance.

### Retrieval and applicability
Search: `advertorial buyer guide awareness demonstration proof`
Related domains: avatars, ad-copy-deployment, offers, testing
Mixed-folder candidate IDs: 8004c3204936fdf92a1fc4e1, cb1e0f63e55e5b76dea610b0, 390171c535c9ceaa4a976d88

- Does this advice fit the product lifecycle, market, audience and requested deliverable?
- Does it require proof, access, budget or assets the brand does not have?
- Does it change a fixed price, offer, policy or other explicit constraint?
- Are platform details or numerical claims current and substantiated?

### Output checks
- Deliver the specified artifact, not general advice about creating it.
- Use supplied brand facts; label hypotheses and missing inputs separately.
- Preserve relevant source conditions; do not copy another business’s proof or results.
- Include an owner, measurement and decision rule when proposing a test.
- Check the output against the requested constraints and owner feedback.

Stop after the requested artifact passes factual and brief checks; allow at most two revision passes, then report the unresolved issue.
