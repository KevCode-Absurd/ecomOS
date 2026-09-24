# Claude & Shopify Built $750k/m AI Powered Ecom Brand

source_id: 1Ig6z4IGo0uaqFz7wHZSEla-LB2LUOsUi  |  folder: /05-SET-store-setup  |  cards: 27  |  words: 15,021  |  type: single YouTube tutorial/course video, auto-transcribed, no timestamps or section headers

credibility: The presenter runs a paid agency/education program ("White Label E-Commerce") and sells or affiliate-markets nearly every tool used in the build: the "White Labeler AI Vault" of Claude prompt templates ("AI employees"), the "White Labeler" page-mirroring tool and Chrome extension, and (by referral link) Winning Hunter and Topview. He states "we've built thousands of websites for clients," which is his only claim to independent track record; every number in the video is self-reported and none is from a named, checkable client. The video's stated goal is to sell the White Label E-Commerce program (explicit pitch at the end: "swap out the logo and launch it as your own"). Read every revenue, traffic, and score figure as marketing for that program, not as audited data. `[web check: presenter identity, program name, and current pricing]`.

date signals: No year is spoken. Tools named place this in the 2025-2026 AI-tooling wave: Claude with custom MCP-style "connectors" (Settings > Connectors > Add custom connector), Claude Design (an image/board design tool inside Claude), ChatGPT, Nano Banana (stated to be "Gemini's platform"), Topview (an AI image/video generation tool with a "chat GBT 2.0" text-to-image model), Winning Hunter (an ad/store intelligence tool), and Shopify's Edit Code / Sections theme architecture. All of these are fast-moving consumer AI products; tool names, UI labels, and even continued existence should be re-checked before relying on this playbook. `[web check: current names, pricing and feature sets for Winning Hunter, Topview, White Labeler, Claude Design, Claude connectors]`. File modified 2026-09-19.

**Scope note:** this folder's own README (embedded in the source export) scopes 05-SET to store/domain setup, payments, tax, shipping, tracking, and legal pages, and explicitly routes branding, sourcing, product research and landing-page section strategy to other folders (04-BRD, 18-COG, 01-PRD, 07-LPG). This source is almost entirely about branding, product validation, sourcing, and page-building rather than Shopify store configuration — only a minority of its 27 cards are genuine Shopify click-path/store-setup content (see section 1). It contains **no** material on domain purchase, email setup, payment gateway configuration, tax settings, shipping profiles, tracking pixel install, or legal pages, despite living in this folder. Pass 2 should treat sections 3.1-3.4 and 3.7-3.8 below as this folder's real contribution and route the rest toward 04-BRD, 18-COG, 01-PRD and 07-LPG.

## 1. What this source is for

The genuinely store-setup part of this source is a mechanical click path for building a custom Shopify product page without Shopify's native page builder: paste externally generated HTML/Liquid into the theme's Edit Code interface as a new Section, build a matching product Template, assign a specific product to it, and set inventory so the product is actually buyable. It also gives a repeatable pattern for updating that code later and for verifying every setup step on the live, logged-out storefront before sending traffic. Everything else in the video (product validation, branding, sourcing, page-mirroring, copywriting) is upstream input that this source treats as already done by the time Shopify work starts.

## 2. Principles

1. **A custom Liquid section, not the default theme, is how you get a bespoke product page in Shopify.** Condition: Shopify's built-in page builder cannot produce the layout you want (e.g. a branded PDP with a guarantee block, founder note, and comparison table in your own visual style). The source's basis: the presenter states plainly that "building pages on Shopify has been very difficult, they don't have a page builder... that is really really good," so the entire build routes custom HTML/Liquid through Edit Code instead. [cb2126cc048b] [8818e8f9c5b2]
2. **A custom page only renders where you explicitly assign it.** Condition: any product-specific template work. A custom section and a custom template do nothing until you (a) build the template, (b) select the custom section inside it, and (c) assign a specific product to that template. Leaving a product on the default template means none of the custom layout appears for it. [3d2c297be211] [54bad54781d1]
3. **Never launch a product without confirming it is actually purchasable end to end.** Condition: any new product, drop-shipped or private-label, before traffic is sent. Setting inventory to a non-zero number and hitting Save is not sufficient proof; the source's rule is to open the live page in a fresh/incognito session, add to cart, and reach checkout. [9ffaac57744e] [d7c81282140d] [220bda0dd2e7] [e5db2ba0cf5e]
4. **Verify every mechanical setup step on the live, logged-out storefront, not in the admin preview.** Condition: after any theme code change, product change, or template assignment. The theme editor's preview can show unsaved or cached states; the source's practice is to hard-refresh the actual public URL. [220bda0dd2e7] [e5db2ba0cf5e]
5. **Inventory in Shopify is just a number, not proof of real stock.** Condition: drop-shipping, or any model where Shopify inventory is decoupled from a real warehouse. Source opinion: setting a large available-inventory figure (the source used 10,000 as an example) stops the storefront from showing "sold out," but you must separately confirm your fulfillment app or supplier actually holds that stock. [d7c81282140d] [9b0648a9c684]
6. **A branded PDP but an unbranded shipped product is a mismatch the source explicitly warns against.** Condition: drop-shipping before you can afford private-label packaging. If you cannot yet afford branded packaging ($500-$1,000 stock, per the source's example), keep the branding on the website/brand pages, not on product photos that promise a branded item the customer will not receive. [d175a55e4165]
7. **Reusing one section-based PDP structure across many SKUs trades some uniqueness for speed.** Condition: multi-SKU stores or a white-label relaunch of the same structure under a different brand. Build the first PDP as modular sections (guarantee, how-it-works, comparison, founder, testimonials, FAQ) once, then swap logo/copy/imagery per brand or product rather than rebuilding from scratch. Source opinion: this can make a store "feel generic" if copy and imagery are not genuinely differentiated. [309fee9d852d]
8. **AI-generated page code can ship broken interactive elements that look fine until clicked.** Condition: any page/section built by an AI page-generation tool before QA. The source found an accordion that visually rendered but did not open on click, because it was built as placeholder code. This is caught only by actually clicking every interactive element on the live page. [a8e85e602df8] [e5db2ba0cf5e]

## 3. Procedures

### 3.1 Inject a custom Liquid section into a Shopify theme (core click path) `[verify UI]`
Source basis: [cb2126cc048b] [8818e8f9c5b2] [c7884fec6d58]
1. In Shopify admin, go to **Online Store**, then **Themes**.
2. Duplicate the current (live) theme and work on the unpublished copy, so you can roll back. Open its actions menu and choose **Edit Code**.
3. In the left file tree, open the **Sections** folder.
4. Click **Add a new section**. Name the file with a clear convention ending in `.liquid` — the source's own convention is `[brand-prefix]_[product]_gg.liquid` (their prefix "WLE" = White Label E-commerce, "gg" = the product nickname "Grow Getter"), e.g. `wle_hair_nectar_gg.liquid`. Typing `.liquid` is what makes Shopify recognize and icon the file correctly.
5. Paste your prepared HTML/Liquid code (generated externally, see section 3.5-3.6) into the new file and **Save**. The file is now stored permanently in the theme and can be deleted later if needed.
6. The section now appears in the theme customizer's **Add Section** picker for placement on any template.
7. To revise the section later: reopen Edit Code, open the same file, paste the new code over the old code (do not create a second file — that causes duplicates), Save, then hard-refresh the live page to confirm the change actually rendered (theme-editor preview can show stale state). [a8e85e602df8]

### 3.2 Build a custom product template and assign a product to it `[verify UI]`
Source basis: [3d2c297be211] [54bad54781d1] [c7884fec6d58] [9b0648a9c684]
1. Create the product first: **Products > Add product**, upload the images the custom section should display, and set the price.
2. Go to **Online Store > Customize Theme** to enter the theme editor.
3. In the template selector, **create a new template** for this product rather than editing the default product template (the source names it after the product, e.g. `hair_nectar_gg`).
4. Hide or remove the default sections you do not want so only the custom layout shows. (Hiding is not deletion — you can restore default sections later.)
5. Click **Add Section**, scroll to find your custom Liquid file (it will appear by the filename you gave it), and add it to the template.
6. **In the section's settings, explicitly select the product** so the section's product object populates images, price and variants automatically. The source calls this step "the biggest thing" to do — a section with no product selected renders empty or broken.
7. Reorder, show, or hide individual blocks inside the section to match your preferred merchandising order.
8. Preview the template with that product assigned; confirm images, price and section content all render, on desktop and mobile.
9. Note: bundles (buy-one-get-one, multi-unit) and subscription options are configured separately in the product/app area, not inside the page section. [9b0648a9c684] [c7884fec6d58]

### 3.3 Make a new product actually buyable before sending traffic
Source basis: [9ffaac57744e] [d7c81282140d] [9b0648a9c684]
1. Go to **Products**, open the product you just added.
2. Set the price. In the source's worked example, the price was set to the supplier's recommended single-unit price of **$21.50** — taken from the supplier, not invented.
3. Set the product to **Active** so it is published to the storefront.
4. Set **Available inventory** for the variant to a non-zero number (the source's example used **10,000** units — an illustration, not a recommended stock level; set your own number to match your real replenishment or supplier stock).
5. Save.
6. If drop-shipping, separately confirm with your fulfillment app/supplier that they actually hold that stock — the Shopify number does not create real inventory.
7. Open the live storefront product page in a fresh/incognito session and confirm the add-to-cart button is enabled, not "Sold out."
8. Add to cart and reach the start of checkout to prove the product is genuinely purchasable end to end.

### 3.4 Verify every store-setup step on the live storefront (pre-launch QA pass) `[verify UI]`
Source basis: [220bda0dd2e7] [e5db2ba0cf5e]
1. After each setup task (theme code, product, payment, shipping, tax — though this source only demonstrates the theme/product side), define the specific observable behaviour that proves it worked (product adds to cart, new section shows, order completes).
2. Open the live storefront in a private/incognito window (removes Shopify admin toolbars and cached admin state).
3. Walk the page top to bottom; confirm every section renders (hero, ingredients/mechanism, testimonial grid, FAQ accordion, guarantee, founder note, footer).
4. Click every interactive element — every accordion, tab, and slider — not just look at them. The source's own build had an accordion that visually rendered but did not open, because AI-generated placeholder code was never wired to a click handler.
5. Check image sizing (oversized images broke the source's own layout on first pass — see section 8) and confirm every link/menu item points to a real destination.
6. Confirm the product is purchasable: price shows, no "sold out" state, variants selectable, add-to-cart works.
7. Record the item as verified only once live behaviour matches; do not trust the theme-editor preview.
8. This is a desktop-focused source; do a separate mobile pass, which the source does not demonstrate. `[needs brand data: mobile QA coverage]`

### 3.5 Fixing a broken AI-generated interactive block
Source basis: [a8e85e602df8]
1. Keep the external page-design tool open alongside Shopify so you can edit one section rather than rebuild the whole page.
2. Identify the misbehaving block (source example: an accordion whose plus button did not open the panel).
3. In the page tool, select that block and request a rebuild with the exact behaviour spelled out. The source's literal instruction, quoted from the transcript: *"This is an accordion section. If someone clicks the plus button, it should open the accordion."*
4. Hit rebuild/regenerate on that section only.
5. Re-publish/download the regenerated code from the external tool.
6. Back in Shopify Edit Code, open the **existing** section file (do not create a second file) and paste the new code over the old code. Save.
7. Refresh the live site to confirm the fix. Edit any remaining text/description inside the block as needed.

### 3.6 Upstream pipeline this source uses before touching Shopify (context for 3.1-3.5; substance belongs to other folders)
This is the presenter's full workflow, given here because the source presents it as one continuous build. Only step 6 onward is genuinely store-setup.
1. **Product validation** (-> 01-PRD): screenshot a competitor's page with a "White Labeler Chrome" extension full-page capture, feed it to an AI prompt template ("white labeler product validator") connected to a paid research tool ("Winning Hunter") via Claude's Settings > Connectors > Add custom connector, and get a 0-10 score plus a "go / go with conditions / no-go" verdict. [42a898b74a67] [7ff9026e43a5]
2. **Branding** (-> 04-BRD): run a second AI prompt template ("white labeler branding design specialist v3") in Claude, answer positioning questions (the source names a "dinner party test," a "3-second feeling," and a "naming the territory/instinct" question), generate and critique candidate names, check domain availability (suffix fallbacks used: `.co`, a "shop" prefix, or a "co" suffix if the `.com` is taken), then generate a brand board and lock a logo. [10d18b2b9c4a] [d3082ef30971] [26655e13ae5d]
3. **Product mockup and packaging** (-> 04-BRD / 18-COG): feed a competitor photo, logo, brand board, and a written brand-reference guide into a third AI prompt template ("white labeler product mockup generator"); generate the base product image (source used a 3:4 ratio, 2K, "medium" setting, 2 generations), then lifestyle and clean pack-shot images, then a packaging brief for front/back panel art to send to a supplier. [c962036d33a6] [6fd1b113469847] [3dca4354b6dc]
4. **Sourcing** (-> 18-COG): run a fourth AI prompt template ("white labeler AI supplier scout v2") to produce a sourcing report (dropship vs. private-label vs. local supplier options, price, ETA, trust signals). Source's own sequencing recommendation: start dropshipping, move to a faster-delivery dropship supplier (named: **ZenDrop** or **Spocket**) once orders come in, then move to private-label once volume justifies it. AliExpress and local US suppliers are named as dropship fallbacks. [d175a55e4165]
5. **Page building** (-> 07-LPG / this source's own scope-note says 07-LPG owns section strategy): use a page-mirroring tool ("White Labeler," a different product from the Chrome extension) to crawl and clone a competitor's full page structure, re-theme it to your brand palette, run a "page score" audit, generate the missing sections it recommends, rewrite copy with an AI copywriting tab (paste in raw supplier specs, ingredients, and genuine review language — more input, better output, but always edit), then export/download the HTML. [c386abd9ce99] [40f69bed15d7] [005f75877ee9] [3db5a6811648]
6. **Shopify implementation** (this source's real scope): take the exported HTML/code from step 5 and follow procedures 3.1-3.4 above to get it live.

### 3.7 Publish a fully designed PDP into Shopify as a reusable section (end-to-end)
Source basis: [c7884fec6d58]
1. In Shopify admin: **Online Store > Edit Code**, create a new section file with a clear naming convention (source: `WLE` + brand + product + `.liquid`).
2. Paste the generated page code into that file and save.
3. Create the product in **Products**, upload images, set the selling price (source used the supplier's recommended $21.50), and set available inventory to a non-zero number (source used 10,000) so the product does not show "sold out."
4. Under the theme's product templates, create a new template for this product and hide the default sections.
5. **Add Section**, select the custom section — the whole designed page loads into the template.
6. In the section settings, explicitly select the product; this populates images, price and variants automatically. The source repeats that this is "the biggest thing" to remember.
7. Reorder, show, or hide individual blocks to match your preferred merchandising.
8. `[verify UI]` — confirm current Shopify admin labels, since theme editor menus and layout change over time.

### 3.8 Confirm purchase options and inventory before launch traffic
Source basis: [9b0648a9c684]
1. Set the selling price from your cost structure and a real reference point (the source used the supplier's recommended price rather than inventing one).
2. Decide the purchase structure explicitly: add buy-one-get-one or multi-unit bundles only if you want them; the source's reference competitor (Rosemary/Hair Syrup) only ran one-time purchase and subscribe-and-save, so the source built no extra bundle logic to match.
3. Confirm inventory quantity is non-zero, otherwise the theme shows "sold out" and blocks purchase.
4. Verify the custom section displays the correct product by checking the section settings.
5. Re-check the live page in an incognito window (no admin branding) before spending on traffic.

## 4. Rules, thresholds and numbers

| Rule / figure | Number | Condition | Source's basis | Card id |
|---|---|---|---|---|
| Example inventory level to avoid "sold out" | 10,000 units | Illustration only, not a stock recommendation | Presenter's own build | [9ffaac57744e] [d7c81282140d] |
| Selling price used | $21.50 | Set from supplier's recommended single-unit price | Presenter's own build | [c7884fec6d58] [9b0648a9c684] |
| Logo generation aspect ratio | 1:1 (square) | Generating logo concepts in an image tool | Presenter's own workflow | [d3082ef30971] |
| Product mockup image spec | 3:4 ratio, 2K resolution, "medium" setting, 2 generations | Base product photo generation | Presenter's own workflow | [c962036d33a6] |
| Product validation score example | 7.95 / 10, verdict "go with conditions" | One product, one research tool's scoring model | Winning Hunter + web research, presenter's build | [42a898b74a67] |
| Demand sub-score example | 9 / 10 | Same validation run | Same tool | [42a898b74a67] |
| Meta/Facebook ad-fit sub-score example | 7.5 | Same validation run | Same tool | [42a898b74a67] |
| Data completeness without the paid research tool | "roughly 55%" of the data set (source's own wording, garbled: also states combining tools gives "over 50% more data") | Using the validator prompt without a Winning Hunter account | Presenter's own estimate, self-reported and internally inconsistent — `[web check]` if reusing this claim | [42a898b74a67] |
| Mirrored page score before upgrade | 55 / 100 | One page, one scoring model, "trained on thousands of pages" per the tool | White Labeler tool, presenter's opinion | [40f69bed15d7] [005f75877ee9] |
| Mirrored page score after adding guarantee, how-it-works, us-vs-them, founder sections | 92 / 100 | Same page, same tool, single before/after example | White Labeler tool, presenter's opinion | [005f75877ee9] |
| Bootstrap capital for first branded inventory | $500-$1,000 | Threshold the source uses for "can you afford private label yet" | Presenter's own example figure | [d175a55e4165] |
| Reference brand's claimed monthly revenue | "$390,000 to $790,000" (title rounds to "$750k/m") | Self-reported by a third-party research tool the presenter uses to select which brand to study/clone | Winning Hunter estimate, **unverified, third-party, not the presenter's own numbers** | (not a store-setup card; context only) |
| Reference brand's claimed daily site traffic | 80,000-100,000 visitors/day | Same context | Same tool, unverified | (context only) |
| Guarantee example used in copy | "90-day promise… or we refund every cent" | Copy example for the risk-reversal section | Presenter's own generated copy for this build | [9229d200e653] [3db5a6811648] |

## 5. Diagnostics and checks

| What to check | How | Good | Bad | Fix |
|---|---|---|---|---|
| Is the product buyable? | Open live PDP in incognito, add to cart, reach checkout | Add-to-cart enabled, checkout reachable | "Sold out" shown, or add-to-cart does nothing | Check inventory is non-zero and tracking settings match intended state [9ffaac57744e] |
| Did a Liquid code edit actually publish? | Hard-refresh the live URL (not the theme-editor preview) | New code/section visible on the public page | Old version still shows | Re-open Edit Code, confirm you saved the correct file, refresh again [a8e85e602df8] |
| Does the custom section show the right product? | Open the section settings inside the template editor | Product explicitly selected; images/price populate | Section empty or shows wrong/no data | Explicitly select the product in the section's settings [9b0648a9c684] [c7884fec6d58] |
| Are interactive elements (accordions, tabs) functional? | Click every one on the live, logged-out page | Opens/closes/responds as expected | Renders visually but does nothing on click | Request an explicit rebuild describing the exact click behaviour, then paste the regenerated code into the same file [a8e85e602df8] |
| Is a product still assigned to the default template? | Check product's template setting in admin | Product assigned to your custom template | Product still on default template | Reassign; a product left on default never shows the custom layout [3d2c297be211] |
| Are images sized correctly? | View the live page for layout breaks | Layout compact and correct | Broken/oversized layout (the source's own first pass) | Re-upload at normal size instead of the originally generated large size [3dca4354b6dc] |
| Is the page ready to send traffic to? | Full incognito walkthrough top to bottom | Every section renders, all links work, purchasable | Missing sections, dead links, broken elements | Run the section-by-section checklist in procedure 3.4 before spending on ads [e5db2ba0cf5e] |

## 6. Tools, settings and named features

- **Claude** — the general-purpose AI assistant used to run every "AI employee" prompt template in this build (product validator, branding specialist, product mockup generator, brand mockup studio, supplier scout, copywriter). Connected to third-party research tools via **Settings > Connectors > Add custom connector**. `[verify UI]` — connector setup UI in Claude changes.
- **White Labeler AI Vault** — the presenter's own paid collection of Claude prompt templates ("AI employees"). Not independently available; a product this source is selling. `[web check]`
- **White Labeler (page tool)** — a separate paid product from the presenter that mirrors a live competitor page structure, lets you re-theme it to a logo/palette, scores the page against the tool's model, generates missing sections, offers an AI copywriting tab, and exports downloadable HTML/Shopify-ready code. Has "three plans" per the source, pricing not given. `[web check: current plans/pricing]`
- **White Labeler Chrome extension** — a browser extension for full-page screenshot capture of a competitor's storefront, used as input to the validator and branding prompts.
- **Image Eye** — a Chrome extension that lists every image on a page and lets you download them individually, used to gather lifestyle-image inspiration. `[web check]`
- **Winning Hunter** — a paid ad-and-store intelligence tool (active-ad counts, ad-library data, store-level revenue/trust signals) that the product-validator prompt queries via a Claude connector. Requires "a basic account." `[web check]`
- **Claude Design** — described as an in-Claude design tool used to lock a brand board and logo into pixel-accurate, print-ready files (as opposed to approximate generative output). Presenter's opinion: good for precision, "too technical and not visual enough" for exploring brand-board concepts. `[web check]`
- **ChatGPT** and **Nano Banana** (described as "Gemini's platform") — alternative text-to-image tools the presenter compared for brand-board generation; picked Topview's output over these on visual taste, not a measured test.
- **Topview** — the AI image/video generation tool ultimately used for brand boards, logo concepts, product mockups, and lifestyle imagery, organized into "boards." A "chat GBT 2.0" model option is used for text-to-image inside it. `[web check: current model names/pricing]`
- **Shopify** — the storefront platform. Features used: **Online Store > Themes** (duplicate before editing), **Edit Code** (theme code editor), **Sections** folder (`.liquid` files), theme customizer's **Add Section** picker, **Customize Theme** template creation and assignment, **Products > Add product / Edit product** (images, price, available inventory, Active status). `[verify UI]` — admin labels and menu positions change.
- **ZenDrop** and **Spocket** — named as faster/domestic dropship fulfillment options to move to once initial orders validate demand. `[web check]`
- **AliExpress** — named as a default dropship sourcing fallback if branded inventory is not yet affordable.

## 7. Examples and case results

All examples below are from one single build (a hair-oil brand the presenter calls "Hair Nectar," modeled on a brand he calls "Hair Syrup" / "Rosemary" in the transcript). Treat every number as an unverified, self-reported illustration from one presenter's own promotional video, not a benchmark.

- Reference brand's estimated revenue: "$390,000 to $790,000 per month" (title rounds this to "$750k/m"); estimated site traffic "80,000 to 100,000 people... every single day." Both figures are attributed to the research tool's estimate of a third-party brand, not verified by the presenter or by any independent source. This is the entire premise of the video's title and should be treated as marketing framing, not a proven case result.
- Product validation run scored 7.95/10, "go with conditions," with sub-scores: demand 9/10, meta ad fit 7.5, plus qualitative flags for ad momentum, winner concentration, store-level trust signals (Trustpilot), and a "brand-driven, crowded" competitive moat. [42a898b74a67]
- Brand naming: first AI-generated name round ("Slurp"-style names) was rejected by the presenter as disconnected from the customer; after feedback asking for names containing "hair," the tool returned options including Main Course, Mainline, Hair Drip, Main Squeeze, Hair Nectar (chosen), Hair Sauce, Hair Snack, Thirsty Hair, Locks and Honey, Goldie Locks. [10d18b2b9c4a]
- Logo: 4 concepts generated at 1:1, presenter picked concept #2, then generated logo variants from it. [d3082ef30971]
- Product mockup: 2 image generations at 3:4/2K/medium; presenter picked the "see-through" variant style over a more literal one. [c962036d33a6]
- Page mirroring and scoring: the cloned/rethemed page scored 55/100; after generating the tool's four recommended missing sections (risk-reversal/guarantee, how-it-works, us-vs-them, founder/brand credibility), it rescored at 92/100. Single page, single tool run. [005f75877ee9] [40f69bed15d7]
- Guarantee copy generated for the page: "90-day promise: grow it back in 90 days or we refund every cent." [9229d200e653]
- Broader industry anecdote (not this brand): the presenter cites Grazia/Graza olive oil's squeeze-bottle packaging as the inspiration for the hair-oil brand's own bottle shape, and states Graza did "about $100,000 in their first week of launch" — a third-party, unverified anecdote used only to justify a packaging choice. `[web check]`

## 8. Mistakes the source warns about

1. **Oversized images broke page layout.** The presenter uploaded very large image files and the page "looked broken"; fixed by re-uploading at normal size. [3dca4354b6dc]
2. **Placeholder-generated interactive elements can look done but not work.** An AI-built accordion rendered visually but its plus button did not open the panel, because the underlying code was placeholder. Caught only by clicking it on the live page. [a8e85e602df8] [e5db2ba0cf5e]
3. **Editing the wrong file, or creating a duplicate section file, breaks the layout.** When updating a section's code, paste over the existing file — creating a second file for the same content risks duplicates. [a8e85e602df8]
4. **Leaving a product on the default template silently drops the custom design.** Custom sections and templates apply only to products explicitly assigned to them. [3d2c297be211] [54bad54781d1]
5. **A branded PDP shown alongside an unbranded shipped (dropship) product creates a visible mismatch with the customer's real experience.** The source explicitly warns against this and recommends keeping branding on the website rather than fake product photography until real branded stock exists. [d175a55e4165]
6. **Large inventory numbers on a dropship SKU do not guarantee real fulfillment.** Shopify's inventory count is just a number; verify the supplier/app actually holds stock. [d7c81282140d] [9b0648a9c684]
7. **Not saving/exporting work in the external page tool before exiting loses it.** The source explicitly warns to always download the HTML before exiting the page-mirroring tool, so work can be re-uploaded and resumed. [c386abd9ce99]
8. **Publishing generated PDP claims without checking them against your real product or ad-compliance rules.** The source's own copy example includes specific outcome claims ("thicker and fuller hair in 90 days," "cured my scalp pain") pulled from generated copy and testimonial-style language; it warns not to publish generated health/efficacy/timeframe claims without verifying they match your actual product and comply with advertising rules. [3db5a6811648]

## 9. Caveats, conflicts and what is missing

- **This source is promotional content for the presenter's own paid tools and program.** Every AI prompt template, the page-mirroring tool, and (via affiliate link) the research and image-generation tools are products the presenter sells or is paid to promote. Scores, verdicts, and "before/after" page results all come from the presenter's own tools, evaluated by the presenter, on the presenter's own demo build. There is no independent audit anywhere in the source. Treat all quantitative claims (revenue, traffic, scores) as illustrations of how the tools are marketed to work, not as proof they work at those levels for a reader's own brand.
- **The headline revenue claim is unverified and third-party.** "$390,000-$790,000/month" (rounded to "$750k/m" in the title) is the research tool's estimate of a different, named brand's revenue — not the presenter's own numbers, and not independently confirmed anywhere in the transcript. `[web check]` if this brand or figure needs citing elsewhere.
- **Folder-scope mismatch.** As noted at the top of this file, the vast majority of this source's content (branding, product validation, sourcing, page-section strategy, copywriting) is out of this folder's stated scope per its own README, and belongs in 04-BRD, 18-COG, 01-PRD, and 07-LPG respectively. Only the Shopify Edit Code / Sections / Templates / inventory click paths (sections 3.1-3.4, 3.7-3.8 above) are genuinely store-setup material.
- **No coverage at all of core store-setup tasks this folder is supposed to own**: domain purchase/DNS, business email setup, payment gateway configuration, tax settings, shipping profiles/rates, tracking pixel installation (Meta/GA), or legal pages (returns, privacy, terms). `[needs brand data: these settings for any real store built from this playbook]`. A separate source is needed to cover those.
- **No settings, screenshots, or exact menu labels are given for the theme customizer beyond high-level names** ("Add Section," "Customize Theme," "Edit Code"), and the presenter himself repeatedly says to verify the current UI since Shopify's admin changes. Every Shopify click-path step above is tagged `[verify UI]` for this reason.
- **Bundles and subscriptions are explicitly out of scope for this build**, since the presenter's reference brand only used one-time purchase and subscribe-and-save; no bundle-app configuration steps are given. [9b0648a9c684]
- **No mobile QA step is shown.** The entire demo appears to be desktop-only; the source itself never demonstrates a mobile check, even though it recommends verifying "on desktop and mobile" in the abstract. [cb2126cc048b] [e5db2ba0cf5e]
- **The data-completeness figures for the validator tool are internally inconsistent** ("roughly 55%... you get like over 50% more data... the winning hunter 45%") — the transcript itself is garbled here; do not treat the exact percentages as reliable. [42a898b74a67]
- **No conflict with other sources is evident** because this source does not overlap with typical store-setup guidance (payments, tax, shipping) at all; it only conflicts internally with this folder's own scope note, as covered above.

## 10. Card index

1. [cb2126cc048b] Inject custom Liquid sections into a Shopify theme via Edit Code
2. [3d2c297be211] Assign a product to a custom page template
3. [9ffaac57744e] Make a product buyable with inventory set before launch
4. [220bda0dd2e7] Verify each store-setup step on the live storefront
5. [8818e8f9c5b2] Inject custom Liquid sections into a Shopify theme
6. [54bad54781d1] Assign a custom page template to a specific product
7. [d7c81282140d] Make a product actually buyable before launch
8. [42a898b74a67] Reverse-engineer a validated product via a challenger angle
9. [7ff9026e43a5] Capture competitor pages and ads as structured research inputs
10. [10d18b2b9c4a] Build the brand kit before the store: intake, positioning and naming
11. [d3082ef30971] Generate a brand board, then lock it for production consistency
12. [26655e13ae5d] Write a brand reference guide for every downstream asset creator
13. [c962036d33a6] Draft the product mockup before contacting any supplier
14. [6fd1b1134698] Create on-brand lifestyle imagery from competitor inspiration
15. [d175a55e4165] Sequence sourcing modes: dropship, then faster fulfillment, then private label
16. [c386abd9ce99] Mirror a proven competitor page into your brand as a starting structure
17. [40f69bed15d7] Score and upgrade a mirrored page section-by-section
18. [005f75877ee9] Score a Product Page Against a High-Converting Template and Fill the Gaps
19. [9229d200e653] The Four Objection-Covering Sections Every PDP Should Consider
20. [3db5a6811648] Feed the Copywriter Raw Product Data for Better PDP Copy
21. [c7884fec6d58] Publish a Custom PDP into Shopify as a Reusable Section
22. [a8e85e602df8] Update a Live Shopify Section Without Rebuilding the Page
23. [3dca4354b6dc] Generate On-Brand Product and Lifestyle Images with AI Assistants
24. [309fee9d852d] Product Page Template Standardisation as an Output, Not the Goal
25. [160e445095ae] Use a Competitor PDP as the Reference Target for a New Build
26. [9b0648a9c684] Configure Purchase Options and Inventory So the Page Can Actually Sell
27. [e5db2ba0cf5e] Inspect the Guest-View Page Before Launching Traffic
