## Inject custom Liquid sections into a Shopify theme via Edit Code
Use when: You need a custom PDP, landing page, or storefront section (founder block, ingredient panel, size chart) that Shopify's default page builder sections cannot produce, and want it reusable across templates.
- Keep the current theme available for rollback and preview the complete purchase journey before publishing any edited theme.
- From the Shopify admin go to Online Store, then open the Themes page.
- Duplicate the current theme and work on the unpublished copy; click its actions menu, and choose Edit Code to open the code editor.
- In the left file tree, open the Sections folder.
- Use Add a new section, give the file a descriptive name that ends in .liquid (for example wle_hair_nectar_gg.liquid), and create it.
- Paste your prepared HTML/Liquid code into the new file and Save.
- The section now appears in the theme customizer's Add Section picker, where you can place it and edit its schema settings.
- To update the section later, reopen Edit Code, paste the new code over the old, Save, and preview the draft page on desktop and mobile to confirm the change rendered.
Caveat: Sections live inside the theme, so changes are lost or overwritten if the theme is replaced or updated without carrying the file forward — keep a copy of the Liquid code outside Shopify.
Caveat: Shopify's Edit Code interface labels and menu positions change; verify the current click path in your admin before following these steps literally.
Caveat: Verify the section has valid theme-compatible schema and any preset needed for the Add Section picker; pasted HTML alone does not guarantee a configurable section.

Tags: store-setup, shopify, liquid, theme-editing, product-page, landing-page, merchandising
Source: Claude & Shopify Built $750k_m Ai Powered Ecom Brand.docx

---

## Assign a product to a custom page template
Use when: Merchandising a hero or specialty product on a bespoke PDP layout, or building a landing page where you want your custom section to render that product's data.
- Create the product first: Products, Add product, upload the images you want the custom section to display, and set the price.
- Open Online Store, then Customize Theme to enter the theme editor.
- In the template selector at the top, create a new template for the product (for example name it hair_nectar_gg) rather than editing the default product template.
- Hide or remove the default sections so only your intended layout shows.
- Use Add Section and select the custom Liquid file you created (for example wle_hair_nectar_gg) to place it on the template.
- Assign the specific product to the template so the custom section's product object references it and populates correctly.
- Preview the template with that product assigned to confirm images, price and section content all render.
Caveat: A custom product template only applies to products you assign to it; leaving a product on the default template means the custom layout will not appear.
Caveat: If the custom section references product objects, it will render empty or broken on products that have no such data assigned.

Tags: store-setup, shopify, liquid, product-page, merchandising, templates, theme-editing
Source: Claude & Shopify Built $750k_m Ai Powered Ecom Brand.docx

---

## Make a product buyable with inventory set before launch
Use when: After adding a product through Products, Add product, before driving any traffic — you need to confirm the product is not showing as sold out or unavailable at checkout.
- Go to Products in the Shopify admin and open the product you just added.
- Set the price and make sure the product is set to Active so it is published to the storefront.
- Set available inventory for the variant (the source example uses 10,000 units) and Save.
- Open the live storefront product page in a fresh session and confirm the add-to-cart button is enabled rather than showing Sold out.
- Add the product to cart and reach the checkout start to verify it is genuinely purchasable end to end.
Caveat: The 10,000 figure is just an example from the source, not a recommended stock level — set inventory to match your real replenishment plan.
Caveat: Inventory can be tracked or untracked per variant; a product with inventory tracking on and zero available will display as sold out even if the page looks correct.

Tags: store-setup, shopify, inventory, product-page, checkout, pre-launch, verification
Source: Claude & Shopify Built $750k_m Ai Powered Ecom Brand.docx

---

## Verify each store-setup step on the live storefront
Use when: Any time you complete a store setup task — theme code, product, payment, shipping profile or tax — before moving to the next setup item.
- After each setup task, define the observable behaviour that proves it worked (product adds to cart, page shows the new section, order can complete).
- Open the live storefront in a private/incognito window or offline-test mode so admin-session caching does not mask problems.
- Exercise the exact customer action tied to that task — add to cart, reach checkout, submit a test order where your payment settings allow it.
- If you edited Liquid, hard-refresh the live page rather than trusting the theme editor preview, which can show unsaved or cached states.
- Record the setup item as verified only after the live behaviour matches, then move on.
Caveat: Preferences and interfaces vary; the specific test steps depend on your payment, shipping and tax configuration, so adapt the verification to each item.
Caveat: Test orders and payment gateways may need test mode or refunding, which is outside the scope of the pure click path.

Tags: store-setup, shopify, verification, pre-launch, checkout, theme-editing, launch-qa
Source: Claude & Shopify Built $750k_m Ai Powered Ecom Brand.docx

---

## Inject custom Liquid sections into a Shopify theme
Use when: You need to build a custom PDP section or page by hand in Shopify (no page builder), e.g. a branded product template for a new SKU.
- In Shopify admin go to Online Store, then Edit Code to open the theme code editor.
- Open the Sections folder and choose Add a new section; name the file with a clear convention (in the source example: a product-specific name like [brand]_[product]_gg.liquid).
- Paste your HTML/Liquid code into the new section file and Save.
- To revise later, return to Edit Code, paste the new code over the old code, Save, then refresh the live page to confirm the change rendered.
- Verify the current Shopify admin labels and menus yourself — theme editor layout changes over time.
Caveat: Section code lives in the theme; theme updates or switching themes can drop or conflict with custom files.
Caveat: Only edit code in a duplicated/published-safe theme if you cannot afford downtime.

Tags: store-setup, shopify, liquid, theme-editing, product-page, custom-sections
Source: Claude & Shopify Built $750k_m Ai Powered Ecom Brand.docx

---

## Assign a custom page template to a specific product
Use when: You want one hero/paid-traffic product to have a unique PDP layout while all other products keep the default template.
- Create the product first: Products, Add product, upload images, set price, and Save.
- Go to Online Store, then Customize Theme and create a new template for the product (name it per product, e.g. hair_nectar_gg).
- Inside that template, hide the default sections you do not want, then Add Section and select the custom Liquid file you created earlier.
- Assign the specific product to the template so it populates the section.
- Confirm the product page renders the custom layout and that the default template is untouched for other products.
- Verify current Shopify template-assignment UI before relying on this path.
Caveat: Template names are arbitrary but must match what you assign in the product; mismatches silently fall back to the default template.
Caveat: Hiding default sections is not deletion — you can restore them if the layout breaks.

Tags: store-setup, shopify, product-page, theme-editing, templates, product-template
Source: Claude & Shopify Built $750k_m Ai Powered Ecom Brand.docx

---

## Make a product actually buyable before launch
Use when: Immediately before driving paid traffic or launch content to a new product, to avoid wasting spend on an unbuyable PDP.
- Go to Products, Edit product on the SKU you are launching.
- Set Available inventory (the source example used a large number like 10,000 for a launch SKU) and Save.
- If drop shipping, confirm the fulfillment app or supplier actually holds that stock — Shopify inventory is only a number and does not create real stock.
- After saving, add the product to cart yourself on the live store to confirm it is purchasable and the variant/price is correct.
Caveat: Setting a large inventory number on a drop-ship SKU does not guarantee fulfillment; keep it aligned with real supplier stock.
Caveat: If you later toggle inventory tracking, re-check the PDP still allows purchase.

Tags: store-setup, shopify, inventory, product-launch, checkout, fulfillment
Source: Claude & Shopify Built $750k_m Ai Powered Ecom Brand.docx

---

## Reverse-engineer a validated product via a challenger angle
Use when: Product selection: deciding whether to base a new store on a proven seller you found in ad libraries.
- Pick a product from a brand already scaling with active ads; treat sustained active-ad counts as the strongest ad-momentum indicator (source treats growing active ads as the key signal).
- Score the opportunity across demand, ad momentum, store-level revenue/trust signals (e.g. Trustpilot), competition/concentration of top-spending ads, and Facebook/Meta ad-fit.
- Check for a moat: if the winning tier is crowded and the moat is brand- and content-driven, a clone will lose — you must bring a sharp angle.
- Check policies and ad-language compliance before committing, since category language can gate scaling.
- If the score is high but the moat is brand-driven, plan for serious content and influencer support, not just a better product.
- Treat the source's 7.95/10 'go with conditions' verdict as a heuristic example, not a benchmark threshold.
Caveat: Scores combine one tool's ad-library data plus web research; without ad-library access expect materially less data (source cites roughly 55% of its data set).
Caveat: Source opinion: a product can be validated yet still fail if you clone the incumbent instead of out-branding it.

Tags: store-setup, product-selection, product-validation, research, ad-library, competitor-research, positioning
Source: Claude & Shopify Built $750k_m Ai Powered Ecom Brand.docx

---

## Capture competitor pages and ads as structured research inputs
Use when: Starting any reverse-engineering workflow (validation, branding, product mockup, page clone) and needing a clean source image of the target brand page.
- Open the competitor's store page in the browser.
- Use a full-page capture browser extension to screenshot the entire page, then download it.
- Feed the screenshot into the research/branding tool as the reference brand you are modeling.
- Note what is copied versus elevated: the source explicitly says it models what works but intends to improve pages, branding and voice rather than clone.
- If visual references are needed, a page-image extraction extension lists every image on the page and lets you download them individually for use as inspiration inputs.
Caveat: Downloading a competitor's imagery is for research/inspiration; do not ship their copyrighted assets as your own.
Caveat: Screenshots are reference inputs, not validated product data — pair with ad-library and store-level signals.

Tags: store-setup, research, competitor-research, screenshots, brand-research, creative-strategy
Source: Claude & Shopify Built $750k_m Ai Powered Ecom Brand.docx

---

## Build the brand kit before the store: intake, positioning and naming
Use when: Building a new store's brand from scratch when you already have a validated product and a competitor to model.
- Run a branding intake with: specific product, business name, target market, price position, competitors, existing assets, and launch channel (the source used a US target market and a Shopify store).
- Set brand-voice sliders (playful vs. serious, bold vs. soft), then answer the positioning prompts — source cites the 'dinner party test', '3-second feeling', and naming the territory/instinct questions.
- Generate a brand strategy snapshot: colors, motif, product names.
- Generate candidate names, then critique them against the actual customer; the source rejected names that felt disconnected and asked for names with 'hair' in them, which produced usable options.
- Check domain availability and pick alternates (.co, .shop prefix, 'co' suffix) if the .com is taken.
- Lock the name before generating assets so everything downstream stays consistent.
Caveat: First-round AI names can miss the customer; plan to give corrective feedback rather than accepting the first list.
Caveat: The source's chosen name and domain alternatives are examples, not recommendations for your category.

Tags: store-setup, branding, positioning, naming, color-palette, logo, brand-strategy
Source: Claude & Shopify Built $750k_m Ai Powered Ecom Brand.docx

---

## Generate a brand board, then lock it for production consistency
Use when: Preparing brand assets before sending a logo or packaging to a supplier or designer, or building landing-page visuals on-brand.
- Prompt a text-to-image tool to generate a brand board: logo, signature palette, pattern, headline treatment, element style and social vibe (the source used a poster-style brand board and preferred the most visual output over the most technical one).
- Feed your accepted brand board back so the brand strategy can be finalized.
- Generate logo concepts at a square (1:1) aspect ratio and pick one; the source generated four options and chose manually.
- Move the chosen logo and palette into a precision design tool to recreate them exactly — generative tools approximate logos, which is unsafe for supplier files.
- Export pixel-accurate PNGs of the logo in its variants and the exact color palette, so the mark never drifts across assets.
Caveat: Generative image outputs are approximations — never send a generated logo to a supplier without recreating it precisely.
Caveat: The source preferred one specific visual style/tool, which is a taste preference, not a universal rule.

Tags: store-setup, branding, logo, color-palette, creative-strategy, design-tools, print-files
Source: Claude & Shopify Built $750k_m Ai Powered Ecom Brand.docx

---

## Write a brand reference guide for every downstream asset creator
Use when: Briefing product mockup generation, a photographer/videographer, or a designer and needing one consistent description of what the brand stands for.
- From your branding exercise, request a written description covering: what the brand is, what it stands for, its personality, and its unique identity.
- Format it as a reference usable by a photographer, videographer or any asset creator.
- Reuse the same guide as an input to product mockup and image generation so visuals stay consistent with the positioning.
- Update the guide if the brand positioning shifts, so old asset prompts do not pull in stale mood.
Caveat: The guide is only useful if it is actually pasted into every asset workflow; a file nobody opens changes nothing.
Caveat: Keep it descriptive and specific — generic adjectives produce generic imagery.

Tags: store-setup, branding, content-brief, creative-strategy, product-photography, brand-guide
Source: Claude & Shopify Built $750k_m Ai Powered Ecom Brand.docx

---

## Draft the product mockup before contacting any supplier
Use when: Product sourcing and packaging prep: you need a visual target to send a supplier and to populate PDP imagery.
- Start with a competitor product photo so the tool understands the physical product you are making.
- Add your logo, brand board, and written brand guide as inputs, then confirm the generated brand snapshot.
- Name the first product with a consumer-friendly name (the source used a fun name instead of an ingredient name) and approve a bottle concept, e.g. a 'nectar window' label style.
- Generate the base product image in the image tool at a print-friendly ratio (source used 3:4, 2K, medium) and generate multiple variations to choose from.
- For image two, use your approved mockup plus your logo to generate lifestyle/setting shots; for image three, generate a clean pack shot.
- Feed the approved images into a packaging brief to produce front/hero and back-panel packaging art, then send the product image and packaging spec together to the supplier.
Caveat: Suppliers can improve on your spec — treat it as a direction, not a final print file.
Caveat: Generated mockups are concepts; verify dimensions and label legal/ingredient copy before production.

Tags: store-setup, product-mockup, packaging, supplier-management, product-page, creative-strategy, image-generation
Source: Claude & Shopify Built $750k_m Ai Powered Ecom Brand.docx

---

## Create on-brand lifestyle imagery from competitor inspiration
Use when: Building PDP, landing-page and ad creative imagery that looks on-brand without a photoshoot.
- Collect inspiration images from the competitor page (a page-image downloader extension speeds this up).
- Pair each inspiration image (composition/lighting reference) with an image of your own product (identity reference).
- Rewrite the scene for your formulation: the source swapped competitor props (e.g. white ice, oranges, lavender) for props matching its own ingredients (rosemary, cucumber, honey, avocado).
- Generate at a usable resolution and iterate by swapping only the inspiration image while keeping the brand reference constant.
- Use these images for the store, supplier presentations, influencer briefs and investor/pitch visuals.
Caveat: Output quality tracks prompt quality — the source states images are only as good as the prompts.
Caveat: Reusing a competitor's exact composition may risk looking derivative; change props, setting and brand cues.

Tags: store-setup, creative-strategy, product-photography, image-generation, product-page, ad-creative, landing-page
Source: Claude & Shopify Built $750k_m Ai Powered Ecom Brand.docx

---

## Sequence sourcing modes: dropship, then faster fulfillment, then private label
Use when: Choosing fulfillment/sourcing model for a new store built around a validated product, especially when launch capital is limited.
- Build the sourcing report for the product: supplier options by model, unit costs and margins, ETA and trust signals for each.
- Launch on dropshipping first to take orders without inventory risk, using supplier product images for your store's product visuals.
- Once orders are coming, move to a faster/domestic delivery option (source names ZenDrop/Spocket) to cut delivery time.
- Once sales justify it, move into private labeling: order inventory, send your branding, have labels printed and the product prepared by the supplier.
- If branded packaging is not yet affordable ($500–$1,000 stock example in the source), keep dropshipping and apply branding on the website and brand pages rather than the product — avoid showing branded product photos that mismatch the unbranded item the customer receives.
- Do branding first anyway, as a target vision, even while shipping unbranded stock.
Caveat: The source's model sequence (dropship → ZenDrop/Spocket → private label) is a recommendation, not a proven mandatory path.
Caveat: A branded PDP with an unbranded shipped product creates a visible mismatch — the source explicitly warns against this; reconcile imagery with what actually ships.

Tags: store-setup, supplier-management, fulfillment, dropshipping, private-label, inventory, product-page
Source: Claude & Shopify Built $750k_m Ai Powered Ecom Brand.docx

---

## Mirror a proven competitor page into your brand as a starting structure
Use when: Building a homepage, collection page or PDP for a new brand when you have a proven competitor page to model and no page-builder available.
- Open the proven competitor page and run the mirror tool to crawl and capture the page's full section structure.
- Name the mirrored product/page and declare whether the page is transactional (customers buy on it) — checkout needs differ for buy-on-page vs. browse-only pages.
- Watch the section-by-section build to confirm the tool captured the right structure; compare against the original section by section (hero media, description, video grid, reviews, FAQs, testimonials, footer).
- Upload your logo and color palette and generate theme variants, then pick one that matches your brand.
- Export/save your work (download the HTML) and re-upload to resume later — the source warns to always save before exiting.
Caveat: Tool names, plans and buttons in the source are vendor-specific and may change — verify the current interface.
Caveat: Mirroring produces a neutral structural template; you still need to rebrand copy and imagery or the result reads as a clone.

Tags: store-setup, landing-page, product-page, page-builder, shopify, branding, competitor-research
Source: Claude & Shopify Built $750k_m Ai Powered Ecom Brand.docx

---

## Score and upgrade a mirrored page section-by-section
Use when: Pre-launch page review: improving a PDP or homepage before spending on acquisition.
- Run the page score calculation so the tool evaluates existing sections and outputs a score plus specific missing-section recommendations.
- Treat the score as a comparative heuristic, not an absolute benchmark: the source's mirrored page scored 55/100 and it added every recommended section.
- Add recommended sections (the source suggested adding all of them), then manually reorder, hide, or add sections as needed for your offer.
- Rewrite copy with AI as a separate pass rather than accepting mirrored copy.
- Re-score after edits and compare before/after so the upgrade is measurable within the tool's model.
Caveat: The 55/100 figure and 'add all sections' advice are the source's tool and opinion, not a published standard — judge whether each section fits your offer.
Caveat: Adding sections can lengthen the page; do not add a block that has no real content behind it.

Tags: store-setup, conversion-optimization, product-page, landing-page, page-audit, copywriting, measurement
Source: Claude & Shopify Built $750k_m Ai Powered Ecom Brand.docx

---

## Score a Product Page Against a High-Converting Template and Fill the Gaps
Use when: Auditing an existing product page or deciding which sections a new PDP needs before launch.
- Enter the product page into a scoring tool that compares it to a modeled library of high-performing pages and returns a 0-100 score with a list of missing sections.
- Treat the score as a directional checklist, not a guaranteed conversion forecast: the source's model was trained on 'thousands of pages,' so the bands are a heuristic for layout completeness, not a formula.
- Review the flagged gaps and prioritise the ones tied to buyer objections: risk reversal (guarantee), how it works, us-versus-them comparison, and founder/brand credibility.
- Add or generate each missing block, keeping the tool's suggested ordering as a starting point since it places sections based on where high-performing pages typically put them.
- Re-score after adding the sections to confirm the page is structurally complete before moving on to copy and imagery.
- In the source example, a page moved from 55 to 92 after adding guarantee, how-it-works, us-versus-them, and founder-credibility sections — treat that jump as an illustration of the method, not a benchmark you should expect.
Caveat: A high structural score does not guarantee sales; copy, offer, traffic and price still drive results.
Caveat: Do not chase a perfect score at the expense of clarity or brand fit.

Tags: store-setup, conversion-optimization, product-page, landing-page, page-audit, risk-reversal, social-proof
Source: Claude & Shopify Built $750k_m Ai Powered Ecom Brand.docx

---

## The Four Objection-Covering Sections Every PDP Should Consider
Use when: Deciding what content blocks to add to a product page that feels thin or isn't converting.
- Add a risk-reversal / guarantee block near the top or after the price: state the guarantee and the exact number of days (e.g. '90-day promise'), because 'nobody knows if it's 100% risk-free' and that uncertainty stops purchases.
- Add a how-it-works block as 3 numbered steps showing the mechanism by which the product achieves the customer's goal, so the buyer understands the path from use to result.
- Add an 'us versus them' comparison that states why the buyer should choose this product over alternatives, so differentiation is explicit rather than assumed.
- Add a founder / brand credibility block that answers 'who is this coming from and why should I trust you', which is especially valuable for newer or unbranded stores.
- Keep the wording tied to the actual product claim; in the source example the founder note and guarantee coexist with testimonials and an FAQ section.
Caveat: The exact mix should match the product's price point and buyer skepticism; not every section is mandatory for every SKU.
Caveat: A guarantee must reflect a policy you will actually honour at scale.

Tags: store-setup, product-page, conversion-optimization, risk-reversal, trust-building, offer-design
Source: Claude & Shopify Built $750k_m Ai Powered Ecom Brand.docx

---

## Feed the Copywriter Raw Product Data for Better PDP Copy
Use when: Generating product descriptions, benefit copy, FAQ text, or section headings for a new or refreshed product page.
- Open your supplier page or spec sheet in a separate tab and collect ingredients, materials, mechanism details, sizing, and genuine customer review language.
- Paste that raw material into the copy tool along with the product name and brand name so the model has concrete nouns and claims to work from.
- Generate the copy and treat it as a first draft: the source calls it 'a really good standard to start with' rather than a finished asset.
- Edit aggressively for accuracy and voice — in the source build the operator manually corrected text colours and wording after generation.
- Keep review quotes intact where they read like real customer language, since testimonial phrasing (e.g. shedding, scalp comfort, hair looking younger) carries credibility that invented copy lacks.
- After copy is in place, replace placeholder or oversized images so layout and load stay clean.
Caveat: Do not publish generated claims (health, efficacy, or timeframe) without verifying they match your product and comply with advertising rules.
Caveat: More input improves output but never removes the need for human editing.

Tags: store-setup, product-page, copywriting, ai-tools, product-research, landing-page
Source: Claude & Shopify Built $750k_m Ai Powered Ecom Brand.docx

---

## Publish a Custom PDP into Shopify as a Reusable Section
Use when: Moving a page built in an external page designer into a live Shopify store.
- In Shopify admin go to Online Store, then edit the theme code, and create a new section file with a clear naming convention (source used a WLE/brand/product prefix plus the .liquid extension).
- Paste the generated page code into that section file and save; the file is then stored permanently in the store and can be deleted later if needed.
- Create the product in Products, upload images, set the selling price (source used the supplier's recommended price of 21.50), and confirm inventory is not zero — the source set available units to 10,000 so the page would not show 'sold out'.
- Under the theme's product templates, create a new template for this product and hide the default theme sections you do not want.
- Add a section and select your custom section from the list; the whole page loads in.
- In the section settings, explicitly select the product — the source says this is 'the biggest thing' to do — which then populates images and price automatically.
- Reorder, show or hide individual blocks within the section to match your preferred merchandising.
- Verify the current Shopify theme editor steps in your admin, as menus and labels change.
Caveat: Custom Liquid sections need maintenance when the theme updates.
Caveat: Bundles and subscription options are configured separately in the product area, not inside the page section.

Tags: store-setup, shopify, product-page, liquid, theme-editing, product-template
Source: Claude & Shopify Built $750k_m Ai Powered Ecom Brand.docx

---

## Update a Live Shopify Section Without Rebuilding the Page
Use when: Fixing or improving one block (e.g. a broken accordion) on an already-published PDP.
- Keep the page designer open alongside Shopify so you can edit a single section rather than the whole page.
- Select the block you want to change; in the source tool you can click a section to change layout, design, or rebuild it directly.
- When a block misbehaves because it was generated as placeholder code (source example: an accordion that did not open), request a rebuild specifying the behaviour — e.g. 'clicking the plus button should open the accordion'.
- Re-publish to Shopify and download or copy the regenerated code.
- Return to the theme code editor, open the existing section file, paste the new code over it, and save — do not create a second section file, or you will end up with duplicates.
- Refresh the live site to confirm the change appears, then edit the text/descriptions inside the block as needed.
- Verify current publish/export labels in the page tool, since these interfaces change.
Caveat: Placeholder-generated interactive elements (accordions, sliders) often need an explicit rebuild instruction to function.
Caveat: Overwriting the wrong file or creating duplicates can break the page layout.

Tags: store-setup, shopify, liquid, product-page, theme-editing, troubleshooting, conversion-optimization
Source: Claude & Shopify Built $750k_m Ai Powered Ecom Brand.docx

---

## Generate On-Brand Product and Lifestyle Images with AI Assistants
Use when: Producing hero images, ingredient/lifestyle shots, and customer-use imagery for a product page or ad creative.
- Use a branding/design assistant to develop image prompts that stay inside your brand's visual system before generating anything.
- Use an image-mirroring workflow that takes a competitor's visual and recreates it in your own brand style — useful for referencing a proven composition without copying assets.
- Use a customer-experience workflow to generate images of people using your product, filling the testimonial and lifestyle blocks on the PDP.
- Match asset dimensions to the section before upload: the source build looked broken because images were uploaded at very large sizes, which was fixed by using normally sized images.
- Sort product-page images and choose the hero/first image deliberately, since it sets expectations and drives click-through from collection pages.
- For video, use equivalent AI workflows to produce testimonial and product-use clips if video blocks are on the page.
Caveat: Generated images must be checked for accuracy against the real product — never show a product or result the customer won't receive.
Caveat: Oversized uploads hurt layout and load time regardless of generator quality.

Tags: store-setup, creative-strategy, ai-tools, product-page, imagery, ad-creative
Source: Claude & Shopify Built $750k_m Ai Powered Ecom Brand.docx

---

## Product Page Template Standardisation as an Output, Not the Goal
Use when: Deciding whether to build each PDP from scratch or reuse a section library for a multi-SKU store or a white-label brand launch.
- Build the first PDP as modular sections (guarantee, how-it-works, comparison, founder, testimonials, FAQ) so subsequent products can reuse the same structure.
- Store the page as a section file so it can be added to any product template in the store.
- Swap the logo, copy, imagery and product selection to relabel the same structure for a different brand or product — the source describes this as the white-label launch path from zero to live quickly.
- Customise per product only where the buyer's objections differ; keep the objection-covering blocks consistent.
- Compare against a chosen reference brand's page to sanity-check that your page covers everything theirs does and, per the source's intent, adds sections theirs is missing.
Caveat: Reusing one structure across many products can make a store feel generic if copy and imagery aren't genuinely differentiated.
Caveat: The source's claim that the rebuilt page often looks better than the original is the presenter's opinion from a single build, not a measured result.

Tags: store-setup, product-page, templating, shopify, white-label, merchandising
Source: Claude & Shopify Built $750k_m Ai Powered Ecom Brand.docx

---

## Use a Competitor PDP as the Reference Target for a New Build
Use when: Planning a PDP for a new product where you lack your own conversion data.
- Pick a competitor or reference brand that is already selling a comparable product at volume and open its PDP for study.
- Inventory every block on their page: hero, ingredients, how-it-works, testimonials with specifics, comparison, FAQ, guarantee, founder note.
- Map your design so that everything they have is covered as a baseline.
- Then add the sections the source's audit flags as commonly missing — risk reversal, mechanism explanation, us-versus-them, founder credibility — so you exceed the reference rather than match it.
- Adapt their subscription/purchase structure decisions: the source's reference brand only offered one-time purchase and subscribe-and-save, so no extra bundle logic was built; replicate only what fits your economics.
- Record their pricing and selling units, and set your own price against your costs rather than copying theirs.
Caveat: Studying structure is not the same as copying copy or assets — produce your own.
Caveat: A competitor's page may be optimised for a different traffic source and buyer awareness level.

Tags: store-setup, product-page, competitive-research, conversion-optimization, landing-page, positioning
Source: Claude & Shopify Built $750k_m Ai Powered Ecom Brand.docx

---

## Configure Purchase Options and Inventory So the Page Can Actually Sell
Use when: Finalising a new product listing before launching traffic to the PDP.
- Set the selling price from your cost structure and a reference point; the source used the supplier's recommended single-unit price rather than inventing one.
- Decide the purchase structure explicitly: if you want buy-one-get-one or multi-unit bundles, add them as bundle options on the product; if you are matching a reference brand that only runs one-time and subscribe-and-save, you may not need bundle logic at all.
- Check inventory quantity is non-zero, otherwise the theme shows 'sold out' and blocks purchase — the source set a high available count to guarantee purchasability.
- Verify that the custom section displays the right product by selecting it in the section settings, which pulls images, price and variants automatically.
- Re-check the live page in an incognito window with no admin branding so you see exactly what a shopper sees before spending on traffic.
Caveat: Inventory counts, currency and variant setup can override what the section displays; test an actual add-to-cart.
Caveat: Bundles and subscriptions need separate app or platform configuration beyond the page section.

Tags: store-setup, pricing, bundles, subscriptions, shopify, inventory, product-page
Source: Claude & Shopify Built $750k_m Ai Powered Ecom Brand.docx

---

## Inspect the Guest-View Page Before Launching Traffic
Use when: Final QA pass on a PDP, landing page or store before running ads or sending traffic.
- Open the product URL in a private/incognito browser window so Shopify or admin toolbars don't appear.
- Walk the page top to bottom and confirm every section renders: hero, ingredients, mechanism, testimonial grid, FAQ accordion, guarantee, founder note, footer.
- Confirm interactive elements actually work — click every accordion, tab and slider; the source found accordions that did not open because the code was a placeholder.
- Check images are correctly sized and not oversized, and that all links and menus connect to a real destination.
- Confirm the product is purchasable: price shows, no 'sold out' state, variants selectable.
- Compare against the reference competitor page one final time and fix anything missing before launch.
Caveat: Incognito hides logged-in state and admin tools but won't simulate every device or slow connection.
Caveat: Do a separate mobile check — the source demo was desktop-focused.

Tags: store-setup, quality-assurance, product-page, conversion-optimization, shopify, launch-readiness
Source: Claude & Shopify Built $750k_m Ai Powered Ecom Brand.docx

---

## Set Up a Local AI Coding Environment for Shopify Theme Edits
Use when: You want to make custom theme or product-page edits (new blocks, modified cart, custom templates) without hiring a developer or adding apps.
- Verify current Claude Code access, authentication and billing options before buying a plan. The tutorial used a paid Claude plan; its plan-access claim is point-in-time.
- Download and install Visual Studio Code (free).
- In VS Code, use File > Open Folder to create and open an empty directory named something like 'Shopify editor'; this folder becomes the environment where theme files and connections live.
- Open the Extensions panel, search 'Claude', and install the extension published by Anthropic (ignore other similarly named extensions).
- Click the Claude button in the top-right to open the Claude chat panel inside VS Code; the left sidebar shows your files, the chat panel is the main work area.
- Verify the current Claude/VS Code extension interface and menu locations at install time, since extension UI and plan names change.
Caveat: Install only the Anthropic-published extension among the many search results.
Caveat: This sets up the tooling; it does not guarantee conversion improvements on its own.
Caveat: Use an unpublished theme copy and preview changes before making them live.

Tags: store-setup, claude-code, shopify, theme-editing, ai-coding, developer-environment, visual-studio-code
Source: Claude Just Changed Shopify Forever.docx

---

## Connect Shopify CLI and Authenticate Your Store
Use when: Your local Claude/VS Code environment is set up but not yet connected to your Shopify store, so you need it to see and pull themes.
- Prompt Claude to install the Shopify CLI (command line interface) — this is the tool that lets Claude talk to your store.
- When asked how to install, choose the NPM version. The presenter reports the Homebrew version failed for them; treat this as a situational preference, not a universal rule.
- Approve the installation prompts as they appear, checking each one before allowing.
- Prompt Claude to 'connect to my Shopify store and give me a list of the themes' — this triggers authentication.
- Provide the store URL when asked, then copy the authentication command Claude gives you (e.g. 'shopify auth login') into a new VS Code terminal and run it.
- Choose the correct account in the terminal prompt; a browser authentication screen may appear on some setups.
- Once authenticated, confirm Claude can list your themes (the presenter's store showed 13).
- Verify current CLI install options and login command in the Shopify CLI docs, since these change.
Caveat: Claude cannot authenticate on your behalf for security reasons; you complete login manually in the terminal.
Caveat: Ask for the theme list first to confirm the connection before editing anything.

Tags: store-setup, shopify-cli, claude-code, authentication, theme-management, terminal
Source: Claude Just Changed Shopify Forever.docx

---

## Duplicate the Live Theme Before Any AI Editing
Use when: You are about to make any AI-driven theme change and need a safe staging environment.
- After connecting, prompt Claude to 'duplicate the live theme' — the presenter's result was called 'copy of horizon'.
- Immediately instruct Claude to 'continue to work just on that theme' so every subsequent edit targets the copy.
- Confirm the duplicated theme appears under Online Store > Themes in Shopify (the copy is created on the store as well as pulled locally).
- Verify all theme files are now pulled into your local folder so edits happen against the copy's code.
- Treat the live theme as untouchable until the edited copy is validated and published.
Caveat: Editing a live theme risks breaking the entire storefront if something goes wrong.
Caveat: Do not skip the 'work only on that theme' instruction — otherwise Claude may target the wrong theme.

Tags: store-setup, theme-management, staging, claude-code, risk-control, shopify
Source: Claude Just Changed Shopify Forever.docx

---

## Inject an Editable Objection-Busting Trust Block Under Add to Cart
Use when: Your product page lacks shipping, guarantee and returns reassurance near the add-to-cart button and you want it editable without an app.
- Identify the template to edit (e.g. the default product template) in the theme editor.
- Prompt Claude with specifics, e.g.: 'In the product page default template, underneath the add-to-cart button, add three icons and text I can edit in the theme editor — one for shipping, one for guarantees, one for returns.'
- Optionally approve all edits for the session to avoid confirming each change individually.
- Wait for Claude to report what it built (the example produced delivery truck, shield and refresh-arrow icons).
- In the theme editor, refresh the template and confirm a new block (named something like 'Product Trust Buttons') appears, is movable/reorderable, and its icons and text are editable.
- Replicate the pattern for other repeated reassurance needs (payment icons, sizing notes).
Caveat: This is more capable than Shopify's Sidekick, which the presenter says can essentially only generate sections — Claude Code can add editable blocks and templates.
Caveat: Build time in the example was roughly one to two minutes; longer prompts or many instructions can fail (see the one-change-at-a-time caveat).

Tags: product-page, store-setup, trust-signals, claude-code, conversion-optimization, theme-editing, pdp
Source: Claude Just Changed Shopify Forever.docx

---

## Generate a Full High-Converting Product Template from a Framework Document
Use when: You want a structured, reusable PDP template beyond what your default theme ships with, and you already have a page anatomy/framework to follow.
- Have your product-page framework document ready (the presenter uses a 'Perfect Product Page' framework covering hero, trust badges, benefits grid, outcome, image+text, feature highlight and social proof).
- Prompt Claude: 'Create a brand new product template in this theme using the attached framework,' and upload the document.
- Let Claude analyze the framework and generate the template; the example took a couple of minutes.
- In Shopify, refresh and confirm a new template (labeled e.g. 'PPP') exists on the duplicate theme.
- Treat the generated template as a baseline outline to refine: toggle sections on/off, resize icons, remove duplicated elements (the presenter hid a redundant benefits grid).
- Use the theme editor's section settings (badge position, swatch style, etc.) to configure the template per product.
- Assign the template to products where it fits, or duplicate it for testing.
Caveat: The generated layout is a starting outline, not a finished page — expect to edit and remove redundant sections.
Caveat: Don't assume the framework itself will translate into conversion gains without testing.

Tags: product-page, landing-page, claude-code, template-design, conversion-optimization, pdp, merchandising
Source: Claude Just Changed Shopify Forever.docx

---

## Clone a Competitor Design Element via Screenshot
Use when: You spot a specific high-performing UI element (e.g. a 'Top Seller' badge on a swatch) on a competitor's store and want an equivalent on your PDP.
- Find the element on the competitor's site (the example is True Classic's 'Top Seller' heart badge on a variant swatch).
- Screenshot or copy that section.
- Attach the image to Claude with a prompt like: 'Using the attached reference image, add a similar badge... to my swatches on my product page. I need to add an icon, change the text and color, but the styling must look exactly the same as the reference image.'
- Let Claude build the component; it will return setup instructions (the example added a 'Swatch label' block with an emoji/icon and color options).
- Apply it in the theme editor: click Add block > Swatch label, and set the option/option value to match the variant name exactly.
- Customize the icon, text and color to fit your brand.
Caveat: Match the swatch label to the exact option value, or the badge won't bind to the variant.
Caveat: Copy the styling pattern, not the competitor's trademark or content — avoid using their brand assets.
Caveat: This copies a design element, not proven conversion results; test it on your own store.

Tags: product-page, creative-strategy, claude-code, competitor-research, pdp, merchandising, trust-signals
Source: Claude Just Changed Shopify Forever.docx

---

## Make Global Theme Edits (Cart Icon and Notification Bubble)
Use when: You want storewide cosmetic/UX changes (cart icon, cart count color, add-to-cart feedback) that aren't exposed as template-level settings.
- Prompt with a clear scope, e.g.: 'Change the shopping cart icon and let me pick from pre-selected icons like cart, bag, trolley. Add a small animation when something is added to cart, and let me change the color of the number notification on the cart.'
- Wait for Claude to report where the new controls live (the example placed them under Header > Utilities).
- In the theme editor, go to the reported location and select the new icon style and set the cart count background and number colors.
- Test add-to-cart feedback on the storefront.
Caveat: The presenter's bundle of instructions produced the icons and colors but failed to implement the requested add-to-cart animation — too many instructions at once is the suggested cause.
Caveat: If a requested feature doesn't appear, break it into a single focused follow-up prompt rather than assuming it worked.

Tags: store-setup, theme-editing, claude-code, cart, ux-optimization, shopify
Source: Claude Just Changed Shopify Forever.docx

---

## Give Claude One Change at a Time, Not a Bundle
Use when: You are planning a series of theme or PDP edits and deciding how to sequence prompts.
- Decide the single change you want (e.g. change the cart icon only).
- Write a prompt scoped to that one change.
- Verify the result in the theme editor before moving on.
- If a bundled prompt (like the cart icon + animation + count color request) partially fails, re-run the missing piece as its own prompt.
- Track which changes succeeded so you can re-issue the failed ones.
Caveat: This is the presenter's observed lesson from a request that partially failed, not a hard rule — a clearly related bundle can still work but is riskier.

Tags: claude-code, experiment-design, theme-editing, prompting, workflow
Source: Claude Just Changed Shopify Forever.docx

---

## Manage Claude Usage Limits During Heavy Theme Coding
Use when: You are doing multi-hour AI theme work and want to avoid running out mid-task.
- Watch for the usage-limit warning (the example reported '90% of your limit used').
- When you hit the limit, pause theme coding — the source states it resets in about an hour.
- Use the cooldown to plan the next changes or review already-generated output.
- Batch your most important edits earlier in a session before the limit approaches.
Caveat: The reset window (about an hour) and limit percentage are the source's observation and may change with Claude's plans — verify current limits.

Tags: claude-code, usage-limits, workflow, store-setup, ai-coding
Source: Claude Just Changed Shopify Forever.docx

---

## Publish a Claude-Edited Theme and Maintain an Up-to-Date Working Copy
Use when: Your AI-edited theme or template is validated and you are ready to push it live.
- In Shopify, confirm the duplicate theme looks correct before publishing.
- Click Publish on the edited theme; the previously live theme moves to unpublished.
- Treat theme file edits as saved automatically in the theme files — only in-editor content/setting changes need saving.
- For the next round of work, duplicate the now-live theme so your working copy is the most current, then edit and republish that.
Caveat: Publishing is the riskiest step — the source calls it the scariest part of the process.
Caveat: Skipping the re-duplicate step means you could edit a stale copy and overwrite newer live changes.

Tags: store-setup, theme-management, publishing, risk-control, shopify, workflow
Source: Claude Just Changed Shopify Forever.docx

---

## Clean a Fresh WordPress/WooCommerce Install
Use when: Setting up a brand-new WooCommerce store on Hostinger and needing a clean baseline before adding products, pages or shipping rules.
- Review the bundled plugins individually and remove only confirmed unused demo or promotional plugins. Keep WooCommerce and required payment, security, backup and hosting integrations; test the storefront after changes.
- Go to Pages and move every Hello-World style placeholder page to Trash (select all, Bulk Actions > Move to Trash). Empty the trash so dead pages don't get indexed later.
- Go to Settings > General and change the Site Title from 'My WordPress Website' to a phrase matching your search intent and market. The source's example is 'Prima Sofas for USA and Canada' rather than a generic default - this title appears in browser tabs and search results.
- Set the Timezone in Settings > General to your operating region so order timestamps and scheduled tasks align with your customers and bookkeeping.
- Verify the WordPress address and site URL still point to the domain you configured during the Hostinger onboarding, then load the storefront once to confirm it renders.
Caveat: Menu labels and plugin bundles vary by host and WordPress version - verify the current admin interface before following click paths.
Caveat: The 'Prima Sofas' title is an illustrative naming pattern, not a keyword recommendation for your niche.
Caveat: This cleanup is for a fresh installation. On an existing store, use a backup and staging site and preserve cart, checkout, account, product and order data.

Tags: store-setup, woocommerce, wordpress, hostinger, site-configuration
Source: How To Start an Online Store That Runs on Autopilot (WooCommerce Tutorial).docx

---

## Pick the Right WooCommerce Product Type for Each Item
Use when: Adding products to a new WooCommerce store and choosing which product type template fits each item.
- For an item with one option that ships physically (one SKU, one price), use the Simple product type and set price, stock and shipping weight.
- For an item sold in multiple options (size, color, material), use the Variable product type. Install a variation swatches plugin so buyers can pick attributes visually, then generate variations and assign each one its own price and inventory count.
- For a booking, repair, installation or consulting offer with no physical shipment, create a Simple product and mark it Virtual so no shipping is charged.
- For digital goods (ebooks, templates, files), create a Simple product, mark it Virtual and Downloadable, then attach the file URL so buyers receive the download after purchase.
- For products you promote but fulfil elsewhere, use the External/Affiliate product type and supply the destination link and button text.
- Audit the catalog afterward: a wrongly typed product (e.g. physical item marked downloadable) breaks shipping and tax calculations.
Caveat: Variable products require attributes and generated variations; if you never generate variations the product shows no selectable options.
Caveat: External/affiliate products leave your checkout entirely, so your payment, tax and shipping rules do not apply to them.

Tags: store-setup, woocommerce, product-types, catalog, variations, digital-products
Source: How To Start an Online Store That Runs on Autopilot (WooCommerce Tutorial).docx

---

## Connect Stripe and PayPal with Test Mode First
Use when: Enabling payment collection on a new WooCommerce store and deciding where Apple Pay / Google Pay buttons show.
- Install the official WooCommerce Stripe and PayPal plugins from the plugin directory so payments sync cleanly with WooCommerce orders.
- In each plugin's settings, connect your account through the API keys (or the plugin's connect flow for Stripe). Keep Test Mode / sandbox enabled for your first transactions.
- Place a live test order using the provider's test card while in sandbox mode, then confirm the order appears in WooCommerce with the correct status and the payment records correctly on the provider dashboard.
- Decide express checkout placement: enable Apple Pay / Google Pay buttons either on product pages (faster impulse purchase) or restrict them to the checkout page (less premature checkout, cleaner product page). The plugin toggles control this.
- Once sandbox orders succeed, switch to live mode, re-enter live API credentials and place a small real order to verify.
Caveat: API key locations and toggle names change across plugin versions and provider dashboards - verify the current interface.
Caveat: Express buttons appearing on product pages can create a separate checkout path that bypasses some cart logic; test both placements before committing.

Tags: store-setup, payments, woocommerce, stripe, paypal, checkout, express-checkout
Source: How To Start an Online Store That Runs on Autopilot (WooCommerce Tutorial).docx

---

## Set Up Flexible Table-Rate Shipping by Order Value
Use when: Configuring shipping charges and free-shipping thresholds in a new WooCommerce store, especially when rate should depend on order value rather than just weight.
- Install the 'Table Rate Flexible Shipping' plugin (or an equivalent table-rate plugin) and add a shipping zone covering the regions you sell to.
- Create a flat-rate method inside the zone and add conditional rules. The source's example: charge a flat $4.99 when the cart total is below $200, and set free shipping above $200.
- Use bracket-based conditions for finer tiers. The source's example brackets: $0-$90 costs $6.99; $20-$49 costs $8.99 - demonstrating that the plugin charges shipping based on cart price brackets.
- Stack conditions with care: if brackets overlap or leave gaps, some carts will have no available method and checkout will fail. Order your rules so each cart falls into exactly one bracket.
- Add weight-based conditions where physical shipping cost is driven by mass, and test multiple example carts near each bracket boundary to confirm the correct rate appears.
- Publish the free-shipping threshold on the site (announcement bar or cart) so customers know how much more to spend to earn free shipping.
Caveat: The dollar figures here are the source's examples, not benchmarks - set brackets from your own margin and carrier costs.
Caveat: Rule priority and overlap behaviour is plugin-specific; verify how your installed version resolves conflicting conditions.

Tags: store-setup, shipping, woocommerce, table-rates, free-shipping, cart-value
Source: How To Start an Online Store That Runs on Autopilot (WooCommerce Tutorial).docx

---

## Configure Standard, Reduced and Zero Tax Rates
Use when: Setting up tax classes and price display in WooCommerce, particularly when you sell a mix of physical goods, reduced-rate items and digital products.
- Decide the tax class for each product: Standard for most physical goods, Reduced for items taxed at a lower statutory rate (the source's example is books), and Zero for digital products where no tax applies.
- Assign the correct tax class on each product or variation rather than relying on a blanket default, since digital goods and books often differ from the rest of the catalog.
- Turn on tax calculations in WooCommerce settings so prices and cart totals reflect the class and rate applied.
- Consider the B2B/B2C hybrid display option: the source describes displaying prices exclusive of tax in the shop but inclusive of tax at checkout, which lets buyers see net prices while still showing the final gross amount before paying.
- After configuring classes and display, place test orders for one product of each class and confirm the tax shown matches expectations.
Caveat: Tax law and rates vary by jurisdiction and change over time - confirm rates with a current authority or calculation service; this source only shows the mechanism, not current rates.
Caveat: The exclusive-in-shop / inclusive-at-checkout display is a specific setting choice, not a universal best practice; it can confuse some consumer audiences.

Tags: store-setup, taxes, woocommerce, tax-classes, pricing-display
Source: How To Start an Online Store That Runs on Autopilot (WooCommerce Tutorial).docx

---

## Manually Configure US State Tax Rates in WooCommerce
Use when: Setting up tax collection in WooCommerce for US states where you need state-specific rates without an automated tax service.
- Determine the exact combined percentage you should charge for the target state using a tax calculation service (the source uses TaxJar).
- In WooCommerce, go to Tax > Standard Rates.
- Click Insert Row to add a rate. Set the Country Code to US, then the State Code (e.g. CA for California or NV for Nevada).
- Enter the exact percentage using four decimals (the source's example is 7.2500) rather than rounding, so the amount matches the service's figure.
- Repeat the insert for each state you are required to collect in. Add a row per state rather than trying to approximate with a single rate.
- Place a test order to a destination in each configured state and verify the tax line matches the rate you entered.
Caveat: Rates change; a manually entered rate will silently become wrong - schedule a periodic review or move to an automated service.
Caveat: Nexus rules determine which states you should collect in, and this source does not cover nexus analysis - get tax advice for your specific obligations.

Tags: store-setup, taxes, woocommerce, us-states, taxjar, compliance
Source: How To Start an Online Store That Runs on Autopilot (WooCommerce Tutorial).docx

---

## Create Legal Pages and Place Them in a Footer Menu
Use when: Publishing a new ecommerce store and needing Privacy Policy and Terms & Conditions pages linked from every page for trust and compliance.
- Draft the Privacy Policy and Terms & Conditions content (the source suggests generating a first draft with ChatGPT). Use it as a starting point to speed up the first version rather than as final legal advice.
- Create two WordPress pages and paste the respective content into each, with clear titles such as 'Privacy Policy' and 'Terms & Conditions'.
- Go to Appearance > Menus and create a dedicated menu - the source names it 'Legal' - containing only those legal page links, separate from your primary navigation.
- Open the WordPress customizer and assign the Legal menu to the footer menu location so it is reachable from every page without cluttering the main header navigation.
- Load the storefront and confirm the footer links resolve to the correct pages on both desktop and mobile widths.
Caveat: AI-generated legal text is a draft; review it against the regulations that apply to your business and jurisdiction before publishing - this source only describes the mechanics.
Caveat: Customizer menu locations differ by theme (the source uses Blocksy), so verify where footer menus are assigned in your theme.

Tags: store-setup, legal-pages, wordpress, woocommerce, footer-menu, trust
Source: How To Start an Online Store That Runs on Autopilot (WooCommerce Tutorial).docx

---

## Set Up Free Hosting, Domain and WordPress for a WooCommerce Store
Use when: Launching a brand-new store from scratch and you need hosting, a domain and WordPress installed before any product work can start.
- Buy a hosting plan that includes a free domain for the first year and free domain privacy; the source's example tier allowed roughly 50 sites on NVMe storage with daily backups at a promotional rate when paid for a long term (the presenter notes longer terms lower the monthly price, and later upgrades are always possible).
- Register with an email and password, complete billing, and pay with whatever local method is offered; corporate/company billing fields may remove VAT charges depending on your country.
- In the hosting onboarding choose: website for yourself or your business → create a new website → WordPress → set your admin email and password → create a blank website (skip AI/theme preview).
- Claim the free domain at the checkout step (choose .com or a local extension), complete registrant details, and confirm via the verification email.
- When asked for the target audience location, choose the server region closest to your focused buyers; the source still notes CDN keeps load times fast globally.
- Expect the real domain to activate in ~10 minutes (rarely up to 24 hours); meanwhile the site loads on a temporary domain. Once active, log into the WordPress dashboard (backend) and view the front end.
Caveat: Exact plan names, prices, promo codes and storage figures change; verify the current hosting interface before buying.
Caveat: Domain privacy and free-domain-for-a-year offers are provider-specific, not universal.

Tags: store-setup, hosting, woocommerce, wordpress, domain, infrastructure
Source: How To Start an Online Store That Runs on Autopilot (WooCommerce Tutorial).docx

---

## Clean a Fresh WordPress Install Before Building the Store
Use when: Right after a fresh WordPress install, before installing WooCommerce, themes or page builders.
- Dismiss the dashboard welcome notice and open Screen Options to switch off the widget panels you don't use, so the dashboard is scannable.
- Go to Plugins, select all, Bulk Actions → Deactivate, apply, then select all again → Delete, apply; this removes preinstalled tools such as caching plugins you may not need.
- Go to Pages, select all, Move to Trash, then empty the trash; do the same for the default post under Posts.
- Go to Appearance → Themes, open Theme Details on every inactive theme and Delete it, leaving exactly one theme.
- Edit your profile: set first name, last name and nickname, choose the display name shown publicly on posts, pick an admin color scheme, and set the admin color scheme/display name — this is what shows as 'Howdy [name]' and authors blog posts.
- Optionally register the profile email at Gravatar (free) so an avatar appears next to your author name site-wide.
- Under Settings → General set site language, time zone, date format, time format and first day of week, then save.
Caveat: Deleting default plugins can remove a built-in caching layer; add a caching plugin later if you need one.
Caveat: Profile display name becomes public author byline — choose it deliberately.

Tags: store-setup, wordpress, housekeeping, configuration
Source: How To Start an Online Store That Runs on Autopilot (WooCommerce Tutorial).docx

---

## Write a Site Title That Matches What Buyers Search
Use when: Setting the WordPress site title and tagline for a new store, or rewriting them when organic/paid traffic lands on generic pages.
- Never use a generic site title like 'my website' or a welcome phrase; customers search for the thing they want to buy, not for your store's existence.
- Check what competitors in your niche put in their titles and descriptions (e.g. searching 'buy PS5 online' surfaces titles like 'PlayStation 5, PS5, buy online'), then describe your store the same concrete way.
- Optionally prompt an AI assistant with a plain description ('my website is about selling furniture, mostly sofas, in the USA and Canada — write me a great site title') and adapt the output.
- Order the words so the searchable product/category terms come first and your brand name last.
- Use the tagline to state a concrete service promise (the source's example: 'we deliver in the USA and Canada'), keeping it consistent with the title.
Caveat: The source treats title wording as a discoverability aid, not a ranking guarantee; rankings depend on far more than the title.

Tags: store-setup, seo, positioning, wordpress, naming
Source: How To Start an Online Store That Runs on Autopilot (WooCommerce Tutorial).docx

---

## Install a Free Store Theme and Import a Starter Site
Use when: Choosing the visual foundation of a new WooCommerce store when you want a working layout fast instead of designing pages from scratch.
- Install a free theme from Appearance → Themes → Add New by name (the source uses Blocksy), then activate it and install its companion plugin when prompted.
- Delete the previously active default theme afterwards to keep the theme list to one.
- Open the theme's starter-sites screen, filter to Free plans, then filter category to e-commerce.
- Preview each candidate template (open several, review them, then close the ones you reject) and pick one whose product presentation you actually like.
- Import it: choose the editor variant offered (the source supports Gutenberg and Elementor but notes some front-end effects such as hover zoom are missing in the Elementor variant) and select Gutenberg if you want the full set.
- If WooCommerce is not yet installed it will be installed by the import; otherwise it is greyed out. Finish the import and view the site.
- Inspect a demo product page: breadcrumb, title, price, short description, add-to-cart, additional information tab, and related products should already be in place.
Caveat: Imported demo content includes placeholder products, images and copy — you must replace all of it before launch.
Caveat: Elementor vs Gutenberg variants differ in available features; decide before importing.

Tags: store-setup, theme, woocommerce, starter-site, themes
Source: How To Start an Online Store That Runs on Autopilot (WooCommerce Tutorial).docx

---

## Install WooCommerce Manually and Complete the Setup Wizard
Use when: Building the store without importing a starter site, or when you need to re-run the WooCommerce setup wizard after import.
- Go to Plugins → Add New, search WooCommerce, install and activate; the source notes it has millions of active installs, recent updates and is maintained by the WordPress makers.
- Check the 'set up my store' box after activation to enter the onboarding wizard.
- Choose 'I'm just starting my business' (or the appropriate alternative) and continue.
- Select your industry and the store's physical location; the country selection sets the store currency (choosing United States gives dollars).
- Enter your email address, continue, and skip steps you can configure later.
- Afterwards, verify the front end now shows Cart, Checkout, My Account and Shop pages — note WooCommerce places the store in 'coming soon' mode by default.
- Clean the dashboard of the leftover WooCommerce setup panel via Screen Options once done.
Caveat: Changing store country later affects currency, tax and shipping defaults; set it correctly up front.
Caveat: The wizard wording and steps change between WooCommerce versions — verify the current wizard.

Tags: store-setup, woocommerce, plugin, configuration
Source: How To Start an Online Store That Runs on Autopilot (WooCommerce Tutorial).docx

---

## Apply Global Brand Colors and a Logo Through the Customizer
Use when: Rebranding an imported store template, adjusting colors for a client, or setting a logo/favicon before content launch.
- Open Appearance → Customize and locate the theme's global color settings; the source's theme exposes six palette slots used consistently across the site.
- Set slot 1 (the primary/accent color used in buttons and highlights) to your brand color and watch every instance update live — this replaces manual per-element edits.
- Fill the remaining slots with derived tints/shades of the same family (paste a color, drag the slider for a lighter or darker tint) so hover states and backgrounds stay coherent.
- For the logo: upload an SVG where possible for sharpness and small file size (the source's example logo was about 4 KB), then set logo height (around 35 px in the example) and add the alt text and description.
- Set the site icon (favicon) under Site Identity: a square image with transparent background, uploaded and cropped as needed — this shows in browser tabs and helps visitors recognise the site.
- Publish and check the front end; if a section background looks off (e.g. mismatched grey vs the new accent), open the page in the block editor, select the block, and set the background to the global color or to a custom color.
Caveat: Global palette slots and their names are theme-specific; a different theme may not expose the same six colors.
Caveat: The source recommends SVG logos but some themes/headers may not accept SVG — test before committing.

Tags: store-setup, branding, theme-customizer, colors, logo
Source: How To Start an Online Store That Runs on Autopilot (WooCommerce Tutorial).docx

---

## Shape the Header and Main Menu for Store Navigation
Use when: Configuring site navigation right after importing a theme, especially before adding many product categories.
- Open Appearance → Customize → Menus → Main Menu and delete entries that don't belong, e.g. a 'Home' item, because the logo already links home (this mirrors how large retailer sites behave).
- Drag items to reorder; drag an item slightly to the right to nest it as a sub-item under its parent (so hovering 'Products' reveals children).
- Choose the menu style variant that fits (the source preferred a simple hover colour-change style over more elaborate animated styles).
- Reduce excessive spacing between menu items, roughly 30 px in the source's example, to keep the header compact.
- Set the menu link font colour to a darker palette slot and the hover colour to your accent slot; do the same for the header search icon and other header icons.
- In header settings, choose the icon set, optionally give the header a background colour, reduce header height, and enable 'sticky' if you want the header to remain visible while scrolling (transparency is also available).
- Set the header defined as the global header so the same header appears on every page; publish and verify.
Caveat: Sticky headers consume vertical space on mobile; test on a phone before keeping it.
Caveat: Menu style names (Type 1–4) are theme-specific.

Tags: store-setup, navigation, theme-customizer, merchandising, ux
Source: How To Start an Online Store That Runs on Autopilot (WooCommerce Tutorial).docx

---

## Standardise Layout Widths for Store and Product Pages
Use when: Imported template pages feel too wide or cramped and you want a consistent grid across shop, category and product pages.
- In the customizer, open the global Layout section and set the site container width to about 1120 px — the source calls this a reliable default for most sites.
- Then open the WooCommerce → Single Product section in the customizer and switch the single product layout to the narrower width.
- Close the customizer and inspect a live product page: images, add-to-cart and description should no longer stretch edge to edge.
- Re-check the shop archive and category pages to confirm the grid still looks balanced at the new container width.
Caveat: 1120 px is a source-specific heuristic, not a benchmark; very image-heavy or editorial stores may need a wider container.
Caveat: Option names vary by theme.

Tags: store-setup, layout, product-page, theme-customizer
Source: How To Start an Online Store That Runs on Autopilot (WooCommerce Tutorial).docx

---

## Create a Simple Product with Price, Sale Price, Stock and Categories
Use when: Adding a physical product that has no size/colour variants — e.g. a couch, glasses, a cap — and you need the PDP to be complete before launch.
- Create the product with just a name and publish to see the bare PDP, then go back and fill it in progressively.
- Add a long description (appears below the fold) and a short description (appears next to the price) — they serve different positions on the product page.
- Under Product data keep type 'Simple'; leave Virtual and Downloadable unchecked for physical goods.
- Set the regular price and, if running a promotion, a sale price; enter sale dates so the regular price returns automatically after the end date (the source sets a sale ending the last day of the month).
- Under Inventory set a SKU (useful to search stock across variants), enable stock management, enter quantity, and choose the back-order policy: disallow (safest), allow but notify customers when restocked, or allow silently — the source warns silent back-orders only work if you can restock fast.
- Set a low-stock threshold (e.g. notify at two remaining) and optionally enable 'sold individually' to cap one unit per order.
- Under Advanced set a purchase note shown after purchase (e.g. instructions or a scheduling link for services).
- Upload a featured product image (this is the thumbnail on archives) and additional gallery images; copy the title into alt text and description for each.
- Assign a category (parent or sub-category, e.g. Furniture → Sofas) and tags (material, colour, style) so the breadcrumb and related filters work.
Caveat: Sale prices without an end date stay discounted until you remove them — set an end date if the promotion is time-limited.
Caveat: Allowing back-orders without reliable restocking creates unhappy customers.

Tags: store-setup, product-page, woocommerce, inventory, pricing, categorization
Source: How To Start an Online Store That Runs on Autopilot (WooCommerce Tutorial).docx

---

## Build Variable Products with Attributes, Swatches and Generated Variations
Use when: Listing apparel or any product with multiple sizes/colours and you want customers to select options visually on the product page.
- Install a variation-swatches plugin (the source uses the one from Brainstorm Force) from Plugins → Add New and activate it.
- Create global attributes under WooCommerce → Attributes: define one attribute per option type (e.g. Size with type 'Label', Color with type 'Color'), each with a shape (e.g. circle) and size (e.g. 36 px).
- Populate each attribute's terms: for Size add XS, S, M, L, XL, 2XL, 3XL and reorder them because new terms may be added in reverse; for Color add each colour name and pick its swatch colour (you can paste an exact hex).
- Create a new product, set Product data type to 'Variable', and under Attributes add each global attribute and tick only the values this product actually has (e.g. XS, M, L, XL and black, white, navy — not all terms).
- Save attributes, then click 'Generate variations': the number of variations equals the product of the selected values (4 sizes × 3 colours = 12).
- Use bulk actions on the variations list to toggle manage stock across all, then set a base regular price (e.g. 19.99) and adjust outliers individually (e.g. XL at 24.99) — the PDP then shows a price range.
- Override stock per variation where demand differs (XS black at 3 units, L black at 10).
- Assign a featured image and gallery, then open each variation and assign its own image so switching colour changes the displayed photo; the source notes this is done once and then runs automatically.
- Optionally set default form values (e.g. large + navy) and, via the swatches plugin's global styling, thicken swatch borders and centre-align swatches.
Caveat: With many attribute combinations the variation list becomes long and manual per-variation images are time-consuming — budget for it.
Caveat: The default-selected variation should be one you actually stock and want to feature.
Caveat: Swatch styling options and centring may require extra CSS depending on theme; the source uses additional CSS for centring.

Tags: store-setup, product-page, woocommerce, variants, attributes, merchandising
Source: How To Start an Online Store That Runs on Autopilot (WooCommerce Tutorial).docx

---

## Create a Downloadable Digital Product with Unlimited Delivery
Use when: Listing any non-physical deliverable where the same file serves every customer.
- Create a product, set type Simple, and tick both Virtual and Downloadable.
- Set a regular price (the source uses 14.99 for an ebook) — for a fixed-price digital item a sale price isn't required.
- In the Downloadable files section add the file: either upload it via the media library and copy the file URL into the Downloadable files field, or select an existing media item.
- Set the download expiry — leave blank/never-expiring in the source's example, or set a day limit such as 365 days if you want to limit access.
- Add a short description and long description, assign a category (e.g. eBooks), and publish.
- Optionally enable 'Sold individually' under Inventory so one buyer cannot purchase the same download twice in one order.
- Test the purchase flow end to end to confirm the delivery link works after payment.
Caveat: Uploaded media URLs are guessable if unprotected — consider a download-protection setup if the file is valuable.
Caveat: The source presents unlimited downloads as a benefit, but some sellers prefer expiry windows for licensing reasons.

Tags: store-setup, digital-products, woocommerce, delivery, product-page
Source: How To Start an Online Store That Runs on Autopilot (WooCommerce Tutorial).docx

---

## List an Affiliate/External Product Without Shipping or Inventory
Use when: Monetising storefront traffic with tools, themes or services you resell via an affiliate programme.
- Copy your affiliate link for the partner product.
- Create a new product, give it the partner's product name, and upload a product image (the source recommends fixing odd aspect ratios, e.g. resizing to a square canvas, before uploading).
- Change Product data type to 'External/Affiliate' — this removes inventory and shipping fields.
- Paste the affiliate link into the product URL field and set the button text (e.g. 'Buy now', 'More information', 'See plans') to match the destination's call to action.
- Enter the price context (the source shows a 'from $5 per month' style price) so shoppers know the commitment before clicking.
- Write a short and long description covering what the tool does and why you recommend it, assign a category (e.g. Tools), and publish.
- Open the live product page and click the button to confirm the affiliate link and tracking parameters survive the round trip.
Caveat: Revenue depends on the partner's commission terms and cookie window, which the store owner does not control.
Caveat: The source recommends checking the image dimensions first because external products are often displayed cropped.

Tags: store-setup, woocommerce, affiliate, product-page, monetization, external-product
Source: How To Start an Online Store That Runs on Autopilot (WooCommerce Tutorial).docx

---

## Configure Currency and Store Locale in WooCommerce
Use when: Right after setting the store's country, or when the store sells to a different market than its setup country.
- Go to WooCommerce → Settings → General.
- Set the store's country selection first, because it determines the default currency (choosing United States sets dollars).
- Choose the currency symbol, then the currency position (before or after the amount).
- Set the thousand separator and decimal separator per your market's convention so large prices read naturally (e.g. a $1,999 couch should not appear as 1.999).
- Set the number of decimal places — the source uses two.
- Save and inspect a product page and a cart page to confirm prices render across the PDP, cart, checkout and any price ranges on variable products.
Caveat: Changing the currency after publishing products does not convert existing prices; you must update each price manually.
Caveat: Separator and decimal settings are market conventions, not universal — match your buyer's locale.

Tags: store-setup, woocommerce, pricing, localization, configuration
Source: How To Start an Online Store That Runs on Autopilot (WooCommerce Tutorial).docx

---

## Use the Contrast Trick to Fix Mismatched Block Backgrounds
Use when: After importing a template, a section on the homepage or landing page has a slightly-off background that breaks visual consistency.
- Install/use a browser colour-picker extension (the source uses a Chrome colour picker) to sample the exact colour of the surrounding area you want to match.
- Copy the hex value.
- Open the page you want to change via Edit Page (the source uses the Gutenberg block editor).
- Select the section/block, open the Styles panel on the right, and choose Background.
- Either pick one of the theme's global colour variations or choose Custom colour and paste the sampled hex.
- Consider leaving the section transparent instead of filling it, which the source found looked better in their example.
- Save and compare the rendered page against the adjacent sections.
Caveat: Only applies to editors that expose a styles/background panel (e.g. Gutenberg); block or theme differences may move the option.
Caveat: Sampling the wrong region compounds the mismatch — sample from the area you want to match, not from the broken section.

Tags: store-setup, page-building, gutenberg, design, theme-customizer
Source: How To Start an Online Store That Runs on Autopilot (WooCommerce Tutorial).docx

---

## Set Up Manual US State Tax Rates with Inclusive/Exclusive Display
Use when: Selling to US customers where you must charge state-level sales tax, especially in a B2B/B2C hybrid store.
- Research the correct state and local rate for each destination you charge (the source derives exact rates, e.g. 7.2500, from TaxJar).
- In WooCommerce, go to Tax → Standard Rates and insert a new row per jurisdiction.
- Set the country code (e.g. US) and the state code (e.g. CA, NV) for each row, then enter the rate to four decimal places (e.g. 7.2500).
- Repeat for each state you ship to, rather than applying one blanket rate.
- Decide whether standard, reduced and zero rates are needed — reduced for categories like books, zero for digital products.
- For hybrid B2B/B2C stores, configure prices to display excluding tax in the shop/catalogue but inclusive at checkout so B2B buyers can see the net figure while consumers see the final amount they pay.
- Test the cart and checkout with an address in each configured state to confirm the rate applies and the display mode behaves as intended.
Caveat: The source notes exact US state rates should come from a tax service rather than being guessed — many states have local district taxes on top of the state rate.
Caveat: Displaying net prices in the shop while charging gross at checkout can surprise consumers; check this matches your market's legal expectations.
Caveat: Tax rules and WooCommerce tax screens have changed across versions — verify the current settings UI.

Tags: store-setup, woocommerce, taxes, pricing, compliance, checkout
Source: How To Start an Online Store That Runs on Autopilot (WooCommerce Tutorial).docx

---

## Set Shipping Cost Brackets and a Free-Shipping Threshold in WooCommerce
Use when: Configuring shipping zones and rates for a physical-goods store where you want shipping cost to scale with order value.
- Install a WooCommerce shipping plugin that supports conditions based on cart totals or price brackets.
- Define brackets mapping cart value to cost — the source's examples include $0–$90 costing $6.99 and a $20–$49 bracket costing $8.99.
- Add a free-shipping condition for carts above your chosen threshold (the source uses $200).
- Review the brackets for gaps or overlaps before saving; a customer's cart value must land in exactly one bracket.
- Test the cart at several price points — just under and just over the free-shipping threshold, and inside each bracket — to confirm the correct rate appears.
- Check that variable and sale-priced products still produce the same bracket logic at checkout.
Caveat: Bracket values and the free-shipping threshold are source-specific examples, not recommended numbers — set them from your own margin analysis.
Caveat: Plugin conditions vary: some evaluate cart subtotal before tax/discounts, others after, which changes which bracket applies.

Tags: store-setup, shipping, woocommerce, pricing, cart, fulfillment
Source: How To Start an Online Store That Runs on Autopilot (WooCommerce Tutorial).docx

---

## Create WooCommerce affiliate products with external/affiliate product type
Use when: Merchandising: you want to add a partner tool, brand or recommended gear to your catalog and earn affiliate commission on click-through rather than selling stocked goods.
- Create a new product and switch the product type dropdown to 'External/Affiliate product' in the linked product data area.
- Paste your affiliate link into the product URL field and set the button text (e.g. 'More information' or 'See plans') in the button text field.
- Enter the starting price (e.g. '$5 per month') and add a short description of the partner product.
- Assign a relevant category (e.g. 'tools').
- Fix cropped product images: open the image in an editor, expand the canvas to a square (e.g. 1000x1000 px) and re-upload so the tile displays correctly on the shop archive.
- Publish and view the product; confirm the button links out through your affiliate URL.
Caveat: Affiliate products do not use your checkout or inventory — the transaction happens on the partner site, so you cannot offer your own coupons or control the post-purchase experience.
Caveat: If no related-product block appears, that is expected until you add upsells/cross-sells manually.

Tags: store-setup, merchandising, affiliate, product-catalog, woocommerce
Source: How To Start an Online Store That Runs on Autopilot (WooCommerce Tutorial).docx

---

## Add WooCommerce upsells (product page) vs cross-sells (cart)
Use when: Merchandising / AOV: you want to lift average order value by recommending complementary products at the product page or in the cart.
- Open the product, go to the 'Linked products' section in product data.
- Add one or more products to the 'Upsells' field — these display on the product page (theme-dependent, often as 'You may also like').
- Add one or more products to the 'Cross-sells' field — these display in the cart below the cart line items.
- Update the product and verify by viewing the product page (upsells) and adding the product to the cart (cross-sells).
- Test remove: if you empty the triggering product from the cart, the cross-sells disappear because they are tied to that specific product.
Caveat: Cross-sells only show when a matching product is in the cart, so they will not surface for unrelated carts.
Caveat: Upsell placement and label text depend on the active theme.

Tags: store-setup, merchandising, bundles, average-order-value, woocommerce, cross-sell
Source: How To Start an Online Store That Runs on Autopilot (WooCommerce Tutorial).docx

---

## Customize shop look with fonts, spacing and archive layout
Use when: PDP/landing page and storefront design: your product archive looks cluttered or off-brand and you want to tighten the top area and standardize typography before running traffic.
- Pick fonts on fonts.google.com (filter by category, e.g. sans-serif). Use one font for headings and another for body text for contrast.
- In the customizer's typography settings, set the base font (e.g. Open Sans) and set the heading/title font (e.g. Nunito Sans).
- Under the appearance menu, set the menu font to the heading font; adjust capitalisation, letter spacing (e.g. 0.05) and size.
- On the product archive, reduce or remove the big page title area so products appear higher; toggle the display type to control whether pricing shows.
- Turn on 'add to cart and price' cart options if you want those on the archive, or use a variation layout (e.g. variation type 1) with image, title, price ordering.
- Drag archive element order (image, title, price, rating, taxonomies) to rearrange; set image border radius (1em ≈ 16px) and confirm a hover zoom if desired.
- Match colors (price, taxonomies, buttons) to your brand palette; add custom CSS (e.g. rounded buttons) under Additional CSS and publish.
Caveat: Exact settings, labels and preview behavior depend on the active theme (shown here with a free theme).
Caveat: If you want a test order flow, remember to disable 'coming soon' maintenance mode first.

Tags: store-setup, product-page, landing-page, merchandising, woocommerce
Source: How To Start an Online Store That Runs on Autopilot (WooCommerce Tutorial).docx

---

## Sell to specific countries and set flexible table-rate shipping by price tiers
Use when: Fulfillment / pricing: you ship to a limited set of countries and want shipping cost that scales with order value instead of a flat rate.
- Go to WooCommerce → Settings → General, set Selling locations to 'Sell to specific countries' (or all except some) and list the target countries.
- Remove the default free-shipping method in WooCommerce → Settings → Shipping → Shipping zones.
- Install and activate a table-rate plugin (e.g. 'Flexible Shipping' from Octolize) from the plugin repository; keep it updated.
- Add a shipping method to each zone, name the carrier (e.g. UPS), and set a free-shipping minimum order value (e.g. $200).
- Build price-based rules, e.g. $0–$99.99 = $6.99, $20–$49.99 = $8.99 (adjust band edges to be non-overlapping), $50–$99.99 = $12.99, $100–$199.99 = $14.99.
- If your band edges overlap, items get placed in the widest matching region — review band boundaries carefully.
- Alternatively switch the rule basis to weight; set product weights/dimensions and adjust weight/length units in WooCommerce → Settings → Products.
- Repeat the whole method for each additional country zone (e.g. Canada with FedEx and a different free-shipping threshold).
Caveat: The example price tiers and free-shipping thresholds are the presenter's own setup, not universal rules — set your own based on margins.
Caveat: Table-rate plugins and their settings screens change over time; verify the current interface.

Tags: store-setup, fulfillment, shipping, pricing, woocommerce
Source: How To Start an Online Store That Runs on Autopilot (WooCommerce Tutorial).docx

---

## Configure tax rates by country, state and product class
Use when: Pricing/checkout: you sell physical, book/reduced and digital products across multiple countries and need tax to calculate correctly and display consistently.
- Ensure the store address is filled in, then enable taxes in WooCommerce → Settings → General; the Tax tab appears.
- Understand the three classes: standard (normal physical products), reduced (e.g. books), zero (e.g. digital in the US). Add custom classes if needed.
- In Standard rates, add per-region rows: e.g. US 20%, Canada 30% (fill in real rates for your business).
- In Reduced/Zero rates, set the appropriate percentages per country.
- To decide whether tax is added on shipping, turn it on if you sell to companies.
- Assign a product's Tax class (standard/reduced/zero) on the product's General tab — this changes the tax applied at cart/checkout.
- Choose how prices display: enter prices inclusive or exclusive of tax, and set whether prices in shop / cart / checkout display including tax. Aim for a consistent number across product page → cart → checkout.
- To calculate taxes per US state, look up state rates (e.g. California 7.25%, Nevada 6.85%) and add each state row, checking the correct state code.
- Alternatively use WooCommerce automated taxes (paid add-on) via the plugin search to avoid manual state-by-state entry.
Caveat: The example percentages used in the tutorial are illustrative, not real tax advice — apply your own jurisdiction's rules.
Caveat: Display price inclusive vs exclusive changes the cart line maths; mixing shop-inclusive with checkout-exclusive causes confusing prices.
Caveat: Automated tax is a paid tool; whether it is worth it depends on your volume.

Tags: store-setup, pricing, checkout, taxes, woocommerce, measurement
Source: How To Start an Online Store That Runs on Autopilot (WooCommerce Tutorial).docx

---

## Generate legal pages content and add them to the footer menu
Use when: Store setup: you are preparing to launch and need compliant legal pages without paying for legal drafting, and want them discoverable sitewide.
- Ask an AI assistant: 'I sell [category] in [countries]. Which legal pages do I need? Create the content, and tell me what info you need from my company.'
- Provide your legal company name, business address and product category so the drafts are specific.
- In the customizer's menus, create a new menu (e.g. 'Legal') and add pages: Privacy Policy, Terms and Conditions, and any additional required policies.
- Paste the generated content into each page and publish.
- Edit the footer, remove any placeholder info, and add the Legal menu so it appears sitewide.
- Save and preview each legal page from the live site to confirm content and links render.
Caveat: AI-drafted legal text is a starting point, not legal advice — have it reviewed for your jurisdiction and business model.
Caveat: Requirements differ by country and product type (e.g. subscription, digital, furniture), so verify what applies to you.

Tags: store-setup, landing-page, compliance, woocommerce
Source: How To Start an Online Store That Runs on Autopilot (WooCommerce Tutorial).docx

---

## Enable card, PayPal and wallet payments (Stripe + PayPal) and test the flow
Use when: Checkout: you are launching a store and need working card, PayPal and wallet payment methods before sending real traffic.
- Install 'WooCommerce Stripe Payment Gateway' from the plugin directory and click activate.
- Connect your Stripe account via the on-screen flow (returning redirects to WooCommerce).
- In Stripe settings, enable test mode first; create/connect a test account to generate the webhook so payouts and webhook status show enabled.
- Optionally turn on Apple Pay / Google Pay in the payment settings and hide them on product pages if you don't want express buttons there.
- Install 'WooCommerce PayPal Payments' and connect your business PayPal account; enable it and set your preferred payment method order (drag card above PayPal, or vice versa).
- Place a test order to confirm the buyer confirmation email and the seller new-order email both fire.
- When ready, uncheck test mode on Stripe so live payments are enabled, then place a live test order.
- In the customizer's WooCommerce → Checkout page settings, hide unnecessary fields (company name, second address line) and make phone optional if you don't need it, then link the Privacy Policy and Terms pages so buyers must agree before ordering.
Caveat: Live mode uses real cards and real charges — verify amounts before finalising.
Caveat: Plugin settings, webhook naming and account-connection steps change over time; confirm the current interface before following screenshots.

Tags: store-setup, checkout, conversion-optimization, woocommerce, payment-gateways
Source: How To Start an Online Store That Runs on Autopilot (WooCommerce Tutorial).docx

---

## Handle incoming orders and manage WooCommerce order statuses
Use when: Fulfillment: you have live orders and need a repeatable process for processing, shipping, completing or refunding them.
- Go to WooCommerce → Orders and open an order.
- For paid physical orders the status starts as Processing (the buyer receives 'we received your order and it's now being processed').
- After shipping, change the status to Completed and update — the buyer then receives the completed-order email (e.g. 'good things are heading your way').
- Use Cancelled or Refunded statuses when the order doesn't proceed.
- Because products, shipping, taxes and payments are already configured, the only manual step for physical goods is dispatching the shipment — digital products and services need no manual shipping step.
Caveat: Status-to-email mapping depends on your WooCommerce email settings; verify which emails are sent to customer vs admin.
Caveat: Automated flows cover the order lifecycle but physical fulfilment still requires you (or your 3PL) to ship.

Tags: store-setup, fulfillment, retention, woocommerce, order-management
Source: How To Start an Online Store That Runs on Autopilot (WooCommerce Tutorial).docx

---

## Brand transactional order emails (colors, logo, copy)
Use when: Retention / post-purchase: your order confirmation emails look generic and you want them consistent with your brand and better worded.
- Go to WooCommerce → Settings → Emails to see the list of customer and admin emails; each shows a preview of the email it corresponds to.
- Copy the site's primary color from the customizer's colors section and paste it into the email style color field so the buttons/accents match.
- Upload your logo, set the logo size (e.g. 120) and alignment, and confirm site title / store address text lower in the email.
- Edit the processing email's heading (e.g. 'your order at [store].com has been received') and additional content (e.g. a help/contact line).
- To change hard-coded template strings, copy the WooCommerce email template file to the theme (Appearance → Theme File Editor → WooCommerce → emails) and edit the PHP text, or copy the template into your child theme first.
- Set the From name (e.g. 'Ferdy from SofaSupa') and From address so replies route correctly, then send a test email or place a test order.
Caveat: Editing theme PHP directly means theme updates can overwrite your changes — the tutorial explicitly notes making a copy; use a child theme in practice.
Caveat: Changing wording in the settings only covers the fields exposed there; deeper copy lives in template files.

Tags: store-setup, retention, email-marketing, woocommerce, branding
Source: How To Start an Online Store That Runs on Autopilot (WooCommerce Tutorial).docx

---

## Connect OmniSend to WooCommerce and brand the account
Use when: Retention/acquisition: you want an email list and marketing automation tied to your store, plus revenue attribution from email.
- Sign up at OmniSend via email (business email), verify via the link sent to that inbox.
- Enter store details (name, URL), platform (WooCommerce) and current provider (or 'none'), business address and time zone.
- Install the OmniSend plugin from the plugin uploader (download the connect plugin, then upload → install → activate).
- Click 'connect your store' and approve the required permissions; OmniSend will attempt to grab your branding colors automatically.
- Set brand assets: accent/dark/light colors from the customizer, upload a logo PNG, choose heading fonts, add social links if wanted, then save brand assets.
- Note whether you migrated from another provider — OmniSend offers a migration service via a form (claimed completion within five business days).
- Track email-attributed revenue in the OmniSend dashboard once sending begins.
Caveat: The free tier has a monthly sending cap (500 emails/month shown) and displays OmniSend branding; paid tiers remove branding and raise limits.
Caveat: Automated migration timing is the vendor's claim, not a guarantee.

Tags: retention, email-marketing, acquisition, woocommerce, omn isend, measurement
Source: How To Start an Online Store That Runs on Autopilot (WooCommerce Tutorial).docx

---

## Build a discount opt-in pop-up to grow the email list
Use when: Acquisition/retention: you want to capture emails on-site by offering a discount pop-up instead of relying only on paid traffic.
- In OmniSend, go to Forms and pick a template (e.g. a simple pop-up offering 'get 10% off your first order').
- Edit the heading and copy, then add a first-name field and remove its label so it reads 'enter your first name'.
- Match the store style: set button corner radius, field radius, fonts and colors to the site's existing look, and make the success message in capital letters/style consistent.
- Set display rules: trigger after a time on site (e.g. 3–10 seconds), after scrolling a percentage (e.g. 30%) or on exit intent; set the frequency so it reappears e.g. once per day after being dismissed.
- Choose display type (pop-up, flyout, landing page or embed) and device targeting.
- Enable the form so it goes live on the store — the connected store means enabling it triggers the pop-up on-site.
- Optionally include a phone field only if you plan to send SMS, otherwise remove it to reduce friction.
Caveat: In the free tier the form shows OmniSend branding/badge; remove it only by upgrading.
Caveat: Trigger and frequency settings are the tutorial's preferences — test them against your own traffic.

Tags: acquisition, retention, email-marketing, opt-in, conversion-optimization, woocommerce
Source: How To Start an Online Store That Runs on Autopilot (WooCommerce Tutorial).docx

---

## Set up a welcome automation with a unique per-person discount code
Use when: Retention: after a visitor subscribes, you want an automated welcome sequence that delivers a personal discount and nudges a first purchase.
- On the form, copy its name so you can match the form to the workflow.
- In OmniSend Automation, choose a welcome workflow template (e.g. three-email version).
- Set the trigger to 'subscribed via a signup form' and add a filter so only subscribers from this specific form (e.g. the 10% discount pop-up) enter — prevents cross-contamination between forms.
- Adjust the wait nodes: remove or shorten the default wait if you want the first email to send immediately.
- In the email, add a 'unique discount code' element; choose percent (e.g. 10%) or fixed amount, set the expiry (e.g. 7 days), and check 'reuse the unique discount code in this workflow' so the same code appears in later emails.
- Personalise the subject line and body with a first-name variable, and note the discount expiry is calculated once and reused automatically — do not re-set it per email.
- Style the email (rounded buttons, colors) to match the site, then finish editing and start the workflow to make it live.
- Edit the follow-up emails (e.g. day 1 and day 4) to include the reused unique discount element and the same button.
Caveat: The 10% discount, 7-day expiry and 1-day/4-day sends are the presenter's example values — pick numbers that protect your margin.
Caveat: Workflows made with email-dependent code generation require the connected store; verify the discount element works before launching widely.

Tags: retention, email-marketing, automation, discounts, acquisition, woocommerce
Source: How To Start an Online Store That Runs on Autopilot (WooCommerce Tutorial).docx

---

## Welcome Email Series with Unique Per-Subscriber Coupon Codes
Use when: You are setting up the opt-in to first-purchase email flow and want a personal, trackable discount instead of one shared public code.
- Create the opt-in form on the site (name + email) and connect it to an email platform automation workflow.
- In the workflow builder, add an email step and insert the 'unique discount code' element so the platform generates a one-code-per-contact coupon, not a static code.
- Set the coupon expiry once in the workflow settings; it is calculated automatically per recipient, so you should NOT adjust the expiry date per individual email.
- Personalize the copy with the subscriber's first name, and include a redeemable copy button plus a link that applies the code at cart/checkout.
- Add a second email with a different angle or urgency, then a third, so the sequence continues beyond the first message (e.g., day 1, then day 4).
- Remove any leftover block or element not needed in the follow-up emails before publishing.
- Publish and finish the workflow, then test the full path: sign up with a real or test email, receive the code, add a product, apply the coupon at cart, and check out.
- Verify in the store's coupon list that a unique coupon was created and is restricted to a single use for that contact.
Caveat: The unique discount code feature is platform-specific; verify the current element name and location in your email tool's interface.
Caveat: Confirm that coupon usage limits and expiry are actually enforced by your store coupon settings after the code is generated.

Tags: store-setup, email-marketing, automation, retention, discounting, customer-research
Source: How To Start an Online Store That Runs on Autopilot (WooCommerce Tutorial).docx

---

## Split Testing Email Subject Lines and Content to Lift Revenue
Use when: You have an established email flow or campaign and want to improve open rates or revenue per send.
- In your email platform's workflow or campaign builder, locate the split/A-B testing element and drag it into the flow.
- Duplicate the email into two branches and change one variable at a time, e.g., change only the subject line to 'last chance' vs. the original.
- Assign a portion of the list to each variant so results are comparable rather than sending different messages sequentially.
- Publish and let the test run long enough to collect meaningful data before declaring a winner (two-day tests are too short for strong conclusions).
- Compare open rate first, then clicks and sales, and keep the winning version as the standard for that send.
- Repeat tests on other emails in the sequence so improvements accumulate across the whole flow.
Caveat: The presenter claims A/B testing can 'increase revenue big time' — treat that as a general argument for testing, not a guaranteed result.
Caveat: Short tests (e.g., a day) give unreliable winners; avoid acting on tiny sample sizes.

Tags: store-setup, email-marketing, experiment-design, conversion-optimization, retention
Source: How To Start an Online Store That Runs on Autopilot (WooCommerce Tutorial).docx

---

## Abandoned Cart Email Triggered by Cart Inactivity
Use when: You want to recover checkout/cart abandonment without manual outreach.
- Create a new workflow in your email platform and select the abandoned cart trigger.
- Set the trigger to fire on cart inactivity after a realistic window (the tutorial uses one hour in production; one minute was used only for demo purposes).
- Build the email with a subject line that creates urgency (e.g., 'items in your cart are selling out fast').
- Dynamically insert the actual cart contents so the recipient sees the specific product(s) and a link back to buy.
- Activate the workflow so it runs automatically as soon as shoppers opt in and leave items in the cart.
- Test end-to-end: add a product, stop activity, confirm the email arrives and the product link resolves correctly.
Caveat: The one-minute delay was only for demonstration — production delays should reflect real shopping behavior, typically at least one hour.
Caveat: This flow depends on the visitor being identifiable (e.g., opted in or logged in) for the email address to be captured.

Tags: store-setup, retention, email-marketing, automation, cart, checkout
Source: How To Start an Online Store That Runs on Autopilot (WooCommerce Tutorial).docx

---

## Behavioral and Value-Based Subscriber Segments Feeding Targeted Automations
Use when: You want to send different offers to different customer groups automatically rather than one list-wide campaign.
- Go to the audience segments area and use AI creation or the pre-built segment templates to define groups.
- Build segments such as: active email subscribers, birthdays, inactive subscribers (no opens or purchases across recent weeks/months or last ~20 emails), geographically grouped (e.g., Europe), recent buyers, and high-value subscribers (active openers who purchase).
- Create a new workflow from scratch and select 'entered a segment' as the trigger, then choose the specific segment.
- Add an appropriate delay (e.g., 10 days for a high-value segment) before sending.
- Send a segment-specific message, e.g., a 15% extra discount for three days to customers who spent over $1,000, or a 'we miss you' offer (e.g., 50% off for two days) to inactive subscribers.
- Activate each workflow so offers fire automatically as contacts qualify for or move between segments.
- Review segment membership periodically to ensure the criteria still match your intent.
Caveat: The 'bought more than $1,000' and discount levels (15%, 50%) are illustrative examples from the tutorial, not recommended thresholds.
Caveat: Confirm the actual segment criteria options in your email platform's interface before building, as names and logic may change.

Tags: store-setup, retention, email-marketing, automation, segmentation, customer-research, discounting
Source: How To Start an Online Store That Runs on Autopilot (WooCommerce Tutorial).docx

---

## Custom Branded Order Confirmation Email Replacing the Default
Use when: Your default WooCommerce order confirmation looks generic and you want a branded post-purchase touchpoint.
- In your email platform, create a new workflow and select the order confirmation trigger (search 'confirmation' if needed).
- Edit the email content and maintain consistent styling, including button settings (e.g., primary button color/style) to match your brand.
- Finish editing and start the workflow.
- Test by placing a real or test order through checkout, and confirm that the customer receives the branded email (you as the shop owner will still see the WooCommerce order notification).
- Decide whether to use the platform's version instead of the default store confirmation going forward.
Caveat: The default WooCommerce confirmation still fires by default; manage messaging to avoid customers receiving confusing duplicates if both are active.
Caveat: Verify current trigger names and settings in the email platform, as interfaces change.

Tags: store-setup, email-marketing, automation, retention, fulfillment, checkout
Source: How To Start an Online Store That Runs on Autopilot (WooCommerce Tutorial).docx

---

## Revenue Attribution: Separating Platform-Driven Sales from Total Store Revenue
Use when: You want to judge whether your email automations and opt-in offers are actually driving revenue before investing further.
- Connect your email platform to your store so it can track sales originating from its automations (the tutorial shows the platform distinguishing WooCommerce-driven vs. platform-driven sales).
- In the platform dashboard, compare total store revenue against the revenue attributed to automations.
- Use campaign-level reporting to see how many sales came from a specific broadcast to the whole list.
- Use this split to decide where to invest: more automation, better flows, or list-building campaigns.
- Re-measure after each significant change to see whether attributed revenue moves.
Caveat: Attribution logic is platform-dependent and can overlap; treat platform-attributed revenue as directional, not exact.
Caveat: The tutorial's figures ($1,991 total, $900 from automations) are one example, not a benchmark.

Tags: store-setup, measurement, email-marketing, automation, analytics
Source: How To Start an Online Store That Runs on Autopilot (WooCommerce Tutorial).docx

---

## Swap Shared Discount Codes for Unique, Single-Use, Time-Limited Codes
Use when: You are designing an opt-in incentive and want protection against code sharing and clearer attribution.
- Use an automation element that generates a unique coupon code per subscriber rather than publishing one universal discount code.
- Set an expiry window (the tutorial used seven days) so urgency is created and liability is limited.
- Enforce single use so the code cannot be redeemed again once used.
- Confirm in your store's coupon list that the code appears, is limited to one use, and carries the intended expiry date.
- Deliver the code so the shopper can copy it and apply it at cart.
- Test applying the code yourself, then verify that it is marked used and cannot be reused.
Caveat: Confirm your store's coupon settings actually enforce single-use and expiry after the platform generates the code.
Caveat: Manage the operational burden of many coupon records as your list grows.

Tags: store-setup, discounting, email-marketing, automation, measurement
Source: How To Start an Online Store That Runs on Autopilot (WooCommerce Tutorial).docx

---

## Editing Homepage Content, Product Blocks and Prices in the Site Editor
Use when: You need to update your store homepage hero, featured product blocks, or promotional text without a developer.
- Open the page for editing and triple-click (or click into) a text block to change copy directly.
- For a button: open the style tab to set hover behavior (e.g., darken or scale) and the borders/shadows settings to adjust border radius; in the details panel, set the link and type the target product/page name so the editor auto-suggests matching products, pages and posts.
- For a featured product image: select the image block, choose select image, and replace it with the product photo.
- Update the price text manually to the new value (e.g., $90.99); if the text is too large, adjust size under typography.
- Repeat for a second featured product block the same way.
- For icons, click the icon block and search for a replacement icon.
- Dynamic sections like 'Arrivals' are auto-fetched from the store, so verify they reflect the intended products rather than editing them by hand.
- For background images: open style > background and choose a new image; for text color, open style > typography and set the color (e.g., white) per text block.
- To add new page areas, click and add a block (or type '/' to pick a block type).
Caveat: Manually edited prices can drift out of sync with actual product prices — update both when you change pricing.
Caveat: Exact block names and panels vary by theme/editor version; verify against your current WordPress editor.

Tags: store-setup, product-page, merchandising, landing-page, wordpress, content
Source: How To Start an Online Store That Runs on Autopilot (WooCommerce Tutorial).docx

---

## Making the Header, Menu and Off-Canvas Mobile View Responsive
Use when: Your site looks broken on tablet or mobile and you need to correct layout and styling for smaller screens.
- Open the header/footer builder and switch to the tablet/mobile view.
- Check how elements render on the smaller breakpoint and identify what looks wrong or misaligned.
- In the design settings, set the background (e.g., light), swap the logo for the appropriate version, and confirm it updates.
- Select the main menu, go to design, set text color (e.g., dark) and the hover color (e.g., orange); adjust fonts as needed.
- Add or adjust the location/HTML block with matching dark-text and orange-hover styling.
- Switch to mobile view, open the off-canvas menu area, and under design set the icon color (e.g., dark) so the X/close control is visible.
- Publish and re-check both tablet and mobile to confirm the header, menu and off-canvas behavior are correct.
Caveat: The specific settings paths depend on your builder/theme; verify the current options in your editor.
Caveat: Always preview on desktop, tablet and mobile after changes before publishing.

Tags: store-setup, landing-page, conversion-optimization, wordpress, mobile
Source: How To Start an Online Store That Runs on Autopilot (WooCommerce Tutorial).docx

---

## Optional Channels: Texts and Push Notifications Alongside Email
Use when: Your list includes phone numbers or app/device access and you want to reach people beyond the inbox.
- If you collect phone numbers, add an SMS step in the workflow (additional to the email steps).
- If push notifications are available, add a push step so subscribers see the message on their device.
- Use timing/delay controls so channels do not fire simultaneously and overwhelm the contact.
- Use tags for context so a step only sends when a contact has a specific tag (e.g., only send this offer to a particular group).
- Test each channel separately to confirm delivery before activating.
Caveat: SMS requires collecting phone numbers and appropriate consent; only send where you have permission.
Caveat: Channel availability depends on your platform and integrations — verify current support.

Tags: store-setup, retention, email-marketing, automation, sms
Source: How To Start an Online Store That Runs on Autopilot (WooCommerce Tutorial).docx

---

## Using Tags to Conditionally Gate Automation Emails
Use when: You want certain workflow emails to fire only for a subsection of subscribers (e.g., a specific offer or cohort).
- Assign meaningful tags to contacts based on behavior or source (e.g., a tag identifying a specific interest or purchase context).
- In the workflow, add a condition/tag step that checks whether the contact has the required tag.
- Place the conditional email after the tag check so only tagged contacts proceed.
- Use delays before or after the tag condition to control timing.
- Test with a tagged and an untagged contact to confirm the email only reaches the intended group.
Caveat: Tag hygiene matters — a bloated or inconsistent tag scheme causes misfires.
Caveat: Conditional logic naming and placement differ by platform; verify the current interface.

Tags: store-setup, email-marketing, automation, segmentation, retention
Source: How To Start an Online Store That Runs on Autopilot (WooCommerce Tutorial).docx

---

## Prioritizing Your Next Store Improvements: SEO and Email First
Use when: You have a functioning store and are deciding which growth skill or project to invest in next.
- If your store lacks organic discovery, prioritize learning search optimization and using a rank-tracking plugin to be found in search results.
- If you already have traffic but weak repeat revenue, prioritize deepening your email list and automation setup.
- Treat affiliate marketing as an optional, separate monetization path (promoting other people's products) rather than a core store requirement.
- Pick one priority at a time and implement it fully before moving on.
Caveat: This is the presenter's stated opinion on prioritization, not a proven universal rule; your store's bottleneck should drive the choice.
Caveat: The presenter's affiliate earnings figure is a personal example, not a promise of results.

Tags: store-setup, retention, acquisition, seo, email-marketing
Source: How To Start an Online Store That Runs on Autopilot (WooCommerce Tutorial).docx

---

## Install Node, Git and Shopify CLI before AI-assisted theme work
Use when: You are preparing a machine to build or modify a Shopify theme with an AI coding agent rather than in the theme editor.
- Install Node.js from nodejs.org using the pre-built installer for your OS; accept defaults. On the 'Tools for native modules' screen leave the box unchecked — the presenter says it is not needed for this setup.
- Install Git from git-scm.com (needed as a helper for the Shopify CLI).
- Open PowerShell (Windows) or Terminal (Mac) and run npm install -g @shopify/cli@latest on a single line.
- Verify with shopify version. A version number means it installed; lines of install output are normal, not errors.
- Install Claude Code separately: on Windows run irm https://claude.ai/install.ps1 | iex, then restart the terminal and type claude to authenticate.
- Log in with the Claude account that has the Pro subscription, since Pro is what includes Claude Code.
- Verify current install URLs and commands in the official docs before running them — these interfaces change.
Caveat: The presenter's exact install commands and pricing are point-in-time and should be re-verified.
Caveat: Native modules were left unchecked specifically for this workflow; other Node projects may need them.

Tags: store-setup, shopify, claude-code, developer-environment, nodejs, shopify-cli, theme-development
Source: How to Build a Full Shopify Store using AI (Claude Code).docx

---

## Pull the live theme locally so the AI can edit real code
Use when: You are about to have an AI agent customise a Shopify theme and need the live theme files on your machine first.
- Exit any running Claude Code session with /exit to return to a plain terminal.
- Create and enter a fresh project folder: mkdir my-store-build then cd my-store-build.
- Copy your store domain from Shopify admin > Settings (top of the page).
- Run shopify theme pull --store [your-store-domain] --live.
- Complete the browser login prompt; the code shown in the terminal confirms you are logging into the correct device.
- Wait for the 'pulled successfully' message, which means the theme is now local and editable by the agent.
Caveat: Pulling --live copies the live theme; changes are made locally first and are not live until you push and publish.
Caveat: The store password and account password are different things — see the preview card.

Tags: store-setup, shopify, shopify-cli, theme-development, claude-code
Source: How to Build a Full Shopify Store using AI (Claude Code).docx

---

## Add products and collections before generating the store
Use when: You are starting an AI-assisted store build and need something for the design to be built around.
- In Shopify admin go to Products > Add product.
- Draft the title and description yourself or ask a chat AI for a short, clean title and description, dragging the product image into the prompt for context; iterate with feedback if the first version misses.
- Upload product photos in the Media section — own photos, AI-generated, or stock (the presenter used Pexels stock).
- Set price, inventory quantity and shipping per product; enable variants (e.g. Size: S/M/L/XL) and set per-variant price, inventory and variant-specific images where relevant.
- Create a manual collection (e.g. 'T-Shirts') for each product type and assign the product, optionally with a collection image, then save.
- Repeat for every product; collections make the catalog easier to organise as it grows.
Caveat: Category metafields and SEO fields were left at defaults in the walkthrough — not required for a first build.
Caveat: Shipping is configured later at the store level, not fully per product.

Tags: store-setup, shopify, product-management, collections, variants, merchandising
Source: How to Build a Full Shopify Store using AI (Claude Code).docx

---

## Organise a local asset folder as the AI's design brief
Use when: You are briefing an AI agent to build a homepage or theme and need it to match a specific look instead of guessing.
- Browse the Shopify theme store demo pages and screenshot the specific sections you like — hero, product display, collection page, product page, reviews, story — mixing and matching across themes.
- Create folders for product photos, store inspiration screenshots, logo (including transparent dark and light versions), and homepage lifestyle images.
- Generate a logo if needed (the presenter used Canva) and source lifestyle images from stock sites, AI generation or your own photography.
- Inside your project folder run mkdir inspiration, then 'explorer .' (Windows) to open the folder and paste all assets in.
- Start the agent with the project open so it can see the inspiration directory before it writes any code.
Caveat: Folder structure does not have to match the presenter's exactly; the point is that every reference asset is reachable in one place.
Caveat: Screenshots of third-party themes are references, not licensed assets to copy wholesale.

Tags: store-setup, creative-strategy, inspiration-research, shopify, asset-management, claude-code
Source: How to Build a Full Shopify Store using AI (Claude Code).docx

---

## Prompt the AI to interview you before it builds
Use when: You are starting a store build or major redesign and want controlled, reviewable output rather than a single giant generation.
- Write an initial prompt that gives the agent a few instructions and guidelines, and swap in your real brand name (the guide's version uses a placeholder).
- Let it first read the theme and the inspiration folder to understand the starting point.
- Answer its questions: choose the visual direction (e.g. loud/blue-yellow inspiration vs clean and neutral matching your logo and photography), select homepage sections, and pick fonts.
- Expect a plan confirmation request including your Shopify URL; approve building only the first section.
- Approve command-permission prompts as they appear (choose 'yes, and don't ask again' for repeat permissions) and use plain English to correct anything that diverges.
Caveat: The presenter frames this as working like a real designer — the interview step is what stops mismatched output, so do not skip to 'build the whole store'.
Caveat: Approving commands blindly is risky; read what the agent is about to run.

Tags: store-setup, claude-code, prompt-architecture, brand-positioning, shopify
Source: How to Build a Full Shopify Store using AI (Claude Code).docx

---

## Build the homepage section by section in plain English
Use when: You are generating or redesigning a homepage and want to catch layout and content problems before they compound.
- Order sections deliberately, e.g. Hero, Shop by Category, Featured Products, Customer Reviews, Our Story.
- After each section, refresh the local preview, judge it, and describe changes conversationally ('the icons don't match the category — quality check this section').
- When the Featured Products section comes up, explicitly instruct the agent to use the real products already in the store: 'my store already has three products — use the real products.'
- Approve the section verbally ('looks great') and then explicitly tell it to build the next section in the same style.
- Once every section exists, run a final quality pass prompt asking it to catch anything missed and improve polish.
- Optionally batch small remaining fixes (product pages, header with logo, footer with policy links, rest of the store) into one prompt.
Caveat: Placeholder review names, text and images will need real replacement later.
Caveat: Section prompts assume the store already has products — add them first or the featured section has nothing to reference.

Tags: store-setup, landing-page, prompt-architecture, shopify, claude-code, merchandising
Source: How to Build a Full Shopify Store using AI (Claude Code).docx

---

## Preview changes privately on a local dev server
Use when: You are iterating on theme code and need to see changes live without exposing them to customers.
- Pick 'local dev server' when the agent asks how to preview sections — it is a private live preview running on your machine that updates as the agent writes.
- Open a second terminal, cd into the project folder, and paste the preview command the agent prints.
- When asked for a store password, use the Shopify admin Online Store password (Online Store > Edit password), not your account password.
- Open the resulting link in a browser and refresh after each change to see updates.
- Request adjustments in plain English — e.g. ask for easing animations on load and fade-in on scroll, then refine speed and stagger timing.
Caveat: This is the presenter's recommended preview mode; unpublished preview theme and static mockups were the other options offered.
Caveat: After the initial easing request the presenter found the result improved but noted timing may need further refinement.

Tags: store-setup, shopify, claude-code, theme-development, conversion-optimization
Source: How to Build a Full Shopify Store using AI (Claude Code).docx

---

## Use easing and scroll animations to soften load friction
Use when: A page feels harsh or unpolished because everything renders instantly on load.
- Review the first load: if all text and images appear at once, request a clean easing animation for elements as they appear.
- Also request that subsequent sections fade in as the visitor scrolls.
- Phrase it in plain English to the coding agent, describing the desired feel rather than the implementation.
- After the change, refresh the preview and judge it; if needed, ask to tune the animation speed and stagger timing.
- Confirm the effect on both desktop and mobile before moving on.
Caveat: This is the presenter's taste judgement, not a measured conversion claim.
Caveat: Animation is a polish step, not a substitute for content or offer quality.

Tags: store-setup, conversion-optimization, landing-page, claude-code
Source: How to Build a Full Shopify Store using AI (Claude Code).docx

---

## Push the AI-built theme, then keep editing it in Shopify
Use when: Your AI-assisted theme build is done and you need to review, adjust and prepare it for publishing.
- Tell the agent you are ready to publish to the live theme; it will return a command for your preview terminal.
- In the preview terminal press Ctrl+C, paste the upload command and run it — the theme uploads to Shopify without being published.
- In Shopify admin go to Online Store and click Edit theme on the uploaded theme.
- Manually edit text and images by clicking sections, reorder sections by dragging them in the left panel, add sections with the plus button, and undo from the top right.
- Use the mobile-phone icon in the editor to check every page and section on mobile as well as desktop, then save.
- Only after manual review, publish.
Caveat: Anything you change in the visual editor works the same as any other Shopify theme — building with AI does not lock you into code-only edits.
Caveat: Reordering sections changes the homepage format; review after each move.

Tags: store-setup, shopify, theme-development, conversion-optimization, merchandising
Source: How to Build a Full Shopify Store using AI (Claude Code).docx

---

## Configure shipping zones, free-shipping thresholds and taxes
Use when: You are finishing back-office configuration before taking orders.
- In Settings > Payments, complete Shopify Payments setup so you can be paid.
- In Settings > Shipping and delivery, open your shipping profile; the presenter recommends simply offering free shipping for most stores.
- Delete the express option if unused, then edit the standard rate: rename to 'Free Shipping', turn on the offer-free-shipping toggle, and set the minimum order amount (e.g. $10).
- Set the transit time you will actually honour (the example used 5–8 business days) and save.
- For international zones, configure them deliberately or delete the zone entirely if you do not ship internationally (the example kept only US free shipping).
- In Settings > Taxes and duties, confirm the Shopify tax service and the regions where you collect tax — in the example, only the US.
Caveat: The $10 free-shipping minimum and 5–8 day transit are the presenter's examples, not benchmarks; choose based on your margins and carrier reality.
Caveat: The presenter advises consulting a tax professional if unsure.

Tags: store-setup, shipping, tax, shopify, fulfillment, checkout
Source: How to Build a Full Shopify Store using AI (Claude Code).docx

---

## Generate policy pages from templates and AI, then publish
Use when: You need the legal pages that checkout and the theme footer link to before you remove the store password.
- In Settings > Policies, open each policy and use the Insert template option where offered.
- Scan the template for placeholders — e.g. delete 'insert return address' and enter your real return address — before publishing.
- Publish each policy after reviewing it.
- Write your own shipping policy if no template exists, using an AI with your exact shipping rules and regions, then paste and publish.
- Skip the legal notice only if it genuinely does not apply; the presenter says to consult a professional if unsure.
- Recheck the store footer afterwards: the presenter's build only showed policy links once policies existed in admin.
Caveat: Templates are a starting point, not legal advice.
Caveat: AI-written policies should be reviewed for accuracy against your actual operations.

Tags: store-setup, shopify, legal-pages, retention, customer-trust
Source: How to Build a Full Shopify Store using AI (Claude Code).docx

---

## Connect a custom domain and go live
Use when: You are finalising the store for public launch.
- In Settings > Domains, choose Connect existing domain or Buy new domain (the example priced a .com at about $16/year).
- The presenter recommends a .com for a professional store rather than staying on the Shopify subdomain long term.
- Once products, theme, shipping, taxes and policies are done, go to Online Store, open the theme, click Publish and confirm.
- Click Remove password to open the store to everyone.
- Use View store to confirm the published theme transferred correctly.
Caveat: Domain pricing is point-in-time and varies by registrar/TLD.
Caveat: The presenter treats the default Shopify domain as a long-term liability for professionalism, but it works for testing.

Tags: store-setup, shopify, domains, conversion-optimization, brand-positioning
Source: How to Build a Full Shopify Store using AI (Claude Code).docx

---

## WordPress + WooCommerce baseline stack with Astra and Elementor
Use when: Standing up a brand-new store from scratch and choosing your theme and page builder before building any pages or products.
- Install WordPress on your chosen host first, then install WooCommerce to create the store foundation.
- Install the Astra theme via Appearance > Themes > Add Theme, then activate it.
- Install and activate the Astra Starter Templates plugin to get prebuilt site designs.
- When prompted to choose a page builder during Starter Template import, explicitly select Elementor rather than the WordPress block editor — this decision locks in which editor you will use for later page edits.
- Because WordPress, Elementor and Astra interfaces change frequently, verify current menu names and click paths against live documentation before following any step-by-step tutorial, and avoid tutorials older than roughly 18 months.
Caveat: The source is a walkthrough for a specific version of the tools; menu locations may have moved.
Caveat: Hosting affiliate pitches and domain/server definitions in the source are not part of the setup procedure and can be skipped.

Tags: store-setup, wordpress, woocommerce, elementor, astra, theme-setup, page-builder
Source: How to Create an Ecommerce Website with WordPress 2026 (step by step).docx

---

## Creating mobile-specific layouts with Elementor responsive toggles
Use when: Merchandising a homepage or landing page where the desktop layout (e.g. wide hero with side-by-side blocks) would break or read poorly on phones.
- Build the primary section or container for desktop first, e.g. a wide hero with two columns.
- Duplicate the entire container so you have an identical copy to modify.
- On the duplicate, restyle it for mobile — stack elements, enlarge tap targets, simplify content.
- Open the duplicate's Advanced > Responsive settings.
- Use the 'Hide on tablet' and 'Hide on desktop' toggles on the mobile version, and the 'Hide on mobile' toggle on the original desktop version, so only one version renders per device.
- Preview each breakpoint in Elementor to confirm the correct variant appears and no duplicate content shows.
- Because the Elementor interface changes, verify the current location of the Responsive toggles in your installed version.
Caveat: Duplicating full sections doubles maintenance: a content change must be made in both the desktop and mobile copies.
Caveat: Device-specific hiding is a layout tool, not a substitute for genuinely responsive design — overuse creates divergent content across devices.

Tags: store-setup, elementor, responsive-design, mobile, landing-page, merchandising
Source: How to Create an Ecommerce Website with WordPress 2026 (step by step).docx

---

## Building WooCommerce variable products with color/size variations
Use when: Listing a product that comes in multiple colors, sizes or options where each variant needs separate inventory and pricing.
- Create or edit the product, then change Product type to 'Variable product'.
- Go to the Attributes tab, add an attribute such as Color, and enter its values separated by the | symbol (for example Red | Blue | Green).
- Check 'Use for variations' for that attribute so WooCommerce treats it as a variation axis, then save the attribute.
- Open the Variations tab and click 'Generate variations' to build a row for every combination of attribute values.
- Edit each generated variation individually to set its SKU, stock quantity and price.
- Save the product and preview it on the front end to confirm the variation dropdown shows all options and updates price/availability correctly.
- Verify current menu labels in your WooCommerce version, as admin screens shift between releases.
Caveat: Every variation generated must be manually configured — generated rows start blank, so unedited variations can ship with missing prices or SKUs.
Caveat: Attribute values typed with the | separator must match exactly across the attribute definition and variation rows.

Tags: store-setup, woocommerce, variable-products, product-catalog, inventory, attributes
Source: How to Create an Ecommerce Website with WordPress 2026 (step by step).docx

---

## Connecting Stripe and PayPal payments in WooCommerce
Use when: Enabling card and PayPal checkout on a new store before going live.
- Install the WooCommerce Stripe payment gateway plugin and the WooCommerce PayPal payment gateway plugin (the source names 'Payment Plugins for Stripe WooCommerce' and 'Payment Plugins for PayPal WooCommerce').
- Open each plugin's settings and connect it to your Stripe and PayPal merchant accounts.
- Run the built-in connection test each plugin provides to confirm the handshake works.
- Place a test order using each gateway while still in Test mode to verify the full checkout and confirmation flow.
- Explicitly switch each gateway's mode setting from 'Test' to 'Live' — orders will not actually charge cards while Test mode is active.
- Re-verify in the live dashboard that the mode indicator reads Live after switching.
- Plugin names and settings screens change; confirm the current plugin and mode toggle before relying on these steps.
Caveat: Forgetting to flip from Test to Live mode is a common silent failure — checkout appears to work but no money is collected.
Caveat: The specific plugin vendors named may be replaced or renamed; verify you are installing the current, maintained integration.

Tags: store-setup, payments, stripe, paypal, woocommerce, checkout, go-live
Source: How to Create an Ecommerce Website with WordPress 2026 (step by step).docx

---

## Configuring shipping zones with flat rate vs free-shipping thresholds
Use when: Deciding how to charge for shipping and whether to offer a free-shipping threshold to lift average order value.
- Create Shipping Zones in WooCommerce for the regions you actually ship to (e.g. domestic, specific countries).
- Within each zone, add the shipping method you want to offer.
- Choose between a flat rate — a fixed charge per order regardless of basket size — and a free-shipping method conditioned on a minimum spend.
- If using free shipping, set a threshold amount (the source uses $100 as an example) above which shipping becomes free.
- Verify the threshold math in cart: confirm orders below the minimum are charged and orders at/above it show free shipping.
- Consider whether the threshold is set below, at, or above your typical basket size — a threshold just above average order value is what encourages an add-on. The $100 figure is the source's example, not a universal benchmark.
Caveat: A free-shipping threshold below typical basket size gives away margin without changing behavior.
Caveat: Flat rate and free-shipping-threshold models are situational alternatives, not a single correct answer.

Tags: store-setup, shipping, woocommerce, aov, pricing, fulfillment
Source: How to Create an Ecommerce Website with WordPress 2026 (step by step).docx

---

## Setting up a first-purchase welcome coupon with usage controls
Use when: Launching a store or running an acquisition push where you want a first-purchase incentive without unlimited reuse.
- Create a new coupon in WooCommerce and give it a recognizable code.
- Set the discount type to 'Percentage discount' with the rate you intend.
- Set 'Usage limit per user' to 1 so each customer can redeem it only once.
- Optionally set an overall usage limit and an expiry date to bound total liability.
- Test the coupon at checkout: confirm it applies, respects the one-per-user rule, and produces the expected order total.
- Confirm the discount is factored into your effective margin before promoting it widely.
Caveat: A percentage discount applied without a usage limit per user can be stacked repeatedly by the same buyer.
Caveat: Coupon abuse controls depend on customer account or email matching — guests may still work around limits.

Tags: store-setup, coupons, promotions, woocommerce, acquisition, discounting
Source: How to Create an Ecommerce Website with WordPress 2026 (step by step).docx

---

## Set up WooCommerce variable products with generated variations
Use when: Adding a product that comes in multiple colors, sizes or other options on a WooCommerce store.
- Create the product and change Product type to 'Variable product' before saving.
- In the Attributes tab add an attribute (e.g. Color), enter values separated by the pipe | symbol (white|blue|pink), tick 'Use for variations', and save attributes.
- Open the Variations tab and click 'Generate variations' to auto-create one row per combination instead of adding them manually.
- Edit each variation individually to set its own SKU (e.g. kova-echo-white), regular price, sale price, thumbnail and, if you manage stock per variation, stock quantity and low stock threshold.
- Set the main Product image (the image shown before a shopper picks a variation) and add extra gallery images for the default color.
- Publish, then preview the storefront and click through each option to confirm the image and price swap correctly per variation.
Caveat: The specific button labels live in the WooCommerce product editor and can move between versions; verify the current interface.
Caveat: Separate variations add admin overhead — don't generate variations for attributes that are purely descriptive.

Tags: store-setup, woocommerce, product-setup, variants, product-page, catalog-management
Source: How to Create an Ecommerce Website with WordPress 2026 (step by step).docx

---

## Product data fields that drive PDP content: SKU, stock, weight
Use when: Creating or auditing a physical product listing on WooCommerce before it goes live.
- Set the SKU (your own stock-keeping code) and, if you have a real barcode, a UPC/GTIN. Skip barcodes for placeholder or made-up products.
- Tick 'Track stock quantity' and enter the units on hand; set backorders to 'Do not allow' if you don't want to sell what you can't ship.
- Set a low stock threshold (e.g. 10) so the product page can show 'low stock, order soon' messaging.
- In the Shipping tab enter the weight and dimensions of the entire package — this is what shipping rates and label calculations use.
- Write two descriptions: the long product description (the full sales story) and the short description (the summary that appears near the price/button).
- Use the product image as the default PDP visual, a gallery for supporting shots, and category/tags so the item surfaces in on-site search and category browsing.
- For downloadable or service products select Virtual/Downloadable instead of shipping fields.
Caveat: Weight/dimensions are per package, not per item, when items ship together.
Caveat: Low-stock and stock-count messages only show if you actually track inventory.

Tags: store-setup, woocommerce, product-setup, inventory, product-page, shipping
Source: How to Create an Ecommerce Website with WordPress 2026 (step by step).docx

---

## Configure Stripe and PayPal for WooCommerce and switch to live
Use when: Enabling credit card and PayPal checkout on a WooCommerce store.
- Install and activate the Stripe and PayPal WooCommerce payment plugins from Plugins > Add New (search by name).
- Open WooCommerce settings for Stripe, connect your Stripe account (business details, bank account, statement descriptor) and agree/submit.
- With the account connected, change mode from Test to Live, run the connection test, and save.
- Repeat the connection flow for PayPal, then go to WooCommerce > Settings > Payments and enable the PayPal gateway (it may be inactive by default).
- Verify by adding a product to the cart, proceeding to checkout, and confirming both the card fields and the PayPal option appear.
Caveat: Plugin names and settings screens change; verify current onboarding flow.
Caveat: Do a live-mode test transaction before launch — the connection test confirms the link, not that checkout charges correctly.
Caveat: The presenter is compensated via a hosting affiliate link; treat host recommendations as opinion.

Tags: store-setup, payments, woocommerce, stripe, paypal, checkout
Source: How to Create an Ecommerce Website with WordPress 2026 (step by step).docx

---

## Shipping zones, flat rate and free-shipping thresholds
Use when: Setting up shipping charges and a free-shipping minimum for an online store.
- In WooCommerce > Settings > Shipping create a zone per region (e.g. United States) and assign zone regions.
- Add a Flat rate method: give it a name like 'Standard rate', set taxable status as appropriate, and enter a cost (example used: $10).
- Add a Free shipping method and set its requirement to Minimum order amount (example threshold: $100). The operator can use any threshold; it must be chosen so shipping cost is covered.
- Leave 'Apply minimum order rule before coupon' unchecked if the free-shipping threshold should be judged after coupons reduce the total.
- Drag Free shipping above the flat rate inside the zone so qualifying carts get it automatically.
- Save changes and test with a cart just above and just below the threshold.
Caveat: The $100 threshold and $10 rate are the tutorial's examples, not benchmarks — margin and average order value should set your own numbers.
Caveat: Local pickup is listed as rarely used; judge by whether customers can collect.

Tags: store-setup, shipping, woocommerce, free-shipping, pricing, conversion-optimization
Source: How to Create an Ecommerce Website with WordPress 2026 (step by step).docx

---

## Welcome coupon setup: percentage, usage limits, exclusions
Use when: Launching a store or promo and you need a discount code that can't be abused.
- Go to WooCommerce > Marketing > Coupons and create a coupon with a simple code (e.g. welcome10).
- Set discount type to Percentage and enter the value (example: 10).
- Optionally tick 'free shipping' to bundle shipping into the coupon; skip it for the welcome case in the tutorial.
- Set an expiration date, then under Usage restriction set minimum/maximum spend, prevent coupon stacking, exclude sale items, and scope to products/categories/brands if needed.
- Under Usage limits set the per-user limit (example: 1) so each shopper can use it once, and optionally a total usage cap.
- Publish, then test on the storefront by adding a product, applying the code in the cart, and confirming the discount amount.
Caveat: Discount depth is a margin decision — the 10% example is illustrative, not a recommended rate.
Caveat: Limits only work as configured; verify the per-user rule actually blocks a second redemption.

Tags: store-setup, coupons, promotions, woocommerce, pricing, retention
Source: How to Create an Ecommerce Website with WordPress 2026 (step by step).docx

---

## Use a starter template, then customize instead of building from scratch
Use when: Building a new WordPress/WooCommerce storefront and you want a working layout fast.
- Install and activate a lightweight theme (Astra is used in the tutorial), then launch its starter-templates plugin.
- When choosing templates, click back before proceeding and explicitly select Elementor as the page builder — the tutorial warns against the block editor for this workflow.
- Filter templates by Ecommerce, pick a free one (premium tags are paid), and let the importer install the pages, Elementor and WooCommerce.
- Logo, font and color choices at import are placeholders — the presenter says they get replaced later, so don't over-invest there.
- After import, use 'Edit with Elementor' on the homepage and replace text, images and backgrounds section by section rather than rebuilding.
Caveat: Imported templates include demo products and categories (e.g. 'Indoor plants') that must be deleted.
Caveat: Template import writes many pages/settings; check for leftover demo content before launch.

Tags: store-setup, wordpress, elementor, themes, site-build, merchandising
Source: How to Create an Ecommerce Website with WordPress 2026 (step by step).docx

---

## Elementor structure: sections, containers and widgets
Use when: Editing the homepage or a landing page in Elementor and you need to control layout and positioning.
- Treat the page as sections (full-width background bands, shown by the pink outline), containers inside them (gray dashed boxes), and widgets/elements inside containers.
- Add a section with the plus button, pick Flexbox, and choose a column/container arrangement; templates or AI-generated layouts are alternative starting points.
- To make a section fill the screen, select the container's six-dot handle, change minimum height units to VH and drag the slider to 100.
- Drag widgets in from the element panel (Heading, Text Editor, Divider, Button, Image, Icon Box) and edit text either in the sidebar field or directly on canvas.
- Center content vertically with the container's Justify Content setting.
- Reorder by dragging sections on canvas or by dragging entries in the structure/layers panel.
- Preview without editing outlines using the preview arrow, then publish to save.
Caveat: Newer Elementor versions default to containers rather than the older section/column model; verify the current editor.
Caveat: Two-height, viewport-sized sections can behave differently on mobile until you set responsive padding.

Tags: store-setup, elementor, landing-page, site-build, merchandising, wordpress
Source: How to Create an Ecommerce Website with WordPress 2026 (step by step).docx

---

## Style buttons for visibility: normal vs hover states, padding, radius
Use when: Designing add-to-cart or buy-now buttons on a homepage, landing page or product page.
- Select the button widget and open Style; note there are separate Normal and Hover tabs — set both.
- Set text color and background (classic solid color or gradient) for Normal; set a clearly different text and background for Hover so the change is obvious to shoppers.
- Optionally apply a hover animation such as 'Grow' to draw attention to the CTA.
- Control shape with Border Radius: 0 gives a square button, higher values approach a circle; the tutorial lands mid-range (~15).
- Control size with Padding; unlink the four values when you want wide but not tall buttons (example: 32 left/right, 15 top/bottom).
- Keep button padding and label short enough that the button doesn't read as a large box on mobile.
Caveat: These are styling levers, not proven conversion lifts — validate any change against your own analytics.
Caveat: Hover states don't exist on touch devices, so don't rely on hover alone to signal interactivity.

Tags: elementor, conversion-optimization, landing-page, product-page, design, cta
Source: How to Create an Ecommerce Website with WordPress 2026 (step by step).docx

---

## Video and image hero sections on the homepage
Use when: Building or replacing the homepage hero that showcases a top product.
- Select the hero section's six-dot handle, open Style > Background, and choose Classic (solid), Gradient, or the Video tab.
- For video, host it (the tutorial uses an unlisted YouTube video) and paste the link into the video URL field.
- Add a subtle gradient overlay or choose text colors that contrast with the moving background.
- After adding the video, change text to white (or a contrasting color) in Style > Text Color for each heading and paragraph, since overlaying copy on video can obscure it.
- Swap individual elements freely: duplicate a heading to create a subheading, adjust typography weight and size, and add a Divider at reduced width to separate content.
- Use an Image widget for product visuals where video is not appropriate.
Caveat: Background video typically will not autoplay on mobile and can look broken — plan a mobile-specific alternative (see responsive card).
Caveat: Only use media you have the rights to host.

Tags: elementor, landing-page, merchandising, design, homepage, creative-strategy
Source: How to Create an Ecommerce Website with WordPress 2026 (step by step).docx

---

## Header and footer are theme settings, not Elementor
Use when: Changing the store logo, navigation menu or header background color.
- Open Customize from the admin bar — this controls the theme header and footer, which Elementor does not manage.
- Replace the logo: untoggle the separate transparent logo option so one logo is used sitewide, then upload a transparent PNG and set the logo width (skip cropping so the image isn't cut).
- Set the site title, which is what appears in the browser tab.
- Enable a transparent header on the complete website, and uncheck it for WooCommerce product pages if you want the same header on PDPs.
- Adjust header background under Design > Primary Header: choose a color (e.g. black) and reduce the slider to about half opacity for a translucent header.
- Edit the navigation menu via the pencil icon > Configure Menu > Primary Menu: add Pages, Custom Links, Posts, Products or product categories, and drag items sideways under another item to create dropdown sub-items.
- Set menu text/link color and hover color under Transparent Header > Design to match the site's palette.
- Publish.
Caveat: Theme options and labels shift between Astra versions; verify the current Customizer panels.
Caveat: Changing header colors may require updating body-section text colors for contrast.

Tags: store-setup, wordpress, navigation, themes, design, site-build
Source: How to Create an Ecommerce Website with WordPress 2026 (step by step).docx

---

## Organize the catalog with product categories and parent/child structure
Use when: Organizing a WooCommerce product catalog into navigable categories and subcategories before building collection menus and homepage sections.
- Go to Products > Categories and delete demo categories that shipped with the template (e.g. 'Indoor plants').
- Add a new category with a clear name, a simple lowercase slug for the URL, and optionally a parent category.
- Use parent categories to group variants, e.g. put 'Wireless headphones' and 'Earbuds' under a parent 'Headphones'.
- Skip thumbnail/description for now if they aren't ready — they can be added later.
- Assign each product to the right category in the product editor (and uncheck Uncategorized) so it appears in that category's listings and the homepage sections that pull from it.
- Add tags to products to help on-site search, using your own brand or product name as tags.
Caveat: Categories are what on-site browsing and menu dropdowns rely on; tags help search but shouldn't replace categories.
Caveat: A flat, one-level category set is fine for small catalogs — the tutorial starts that way.

Tags: store-setup, catalog-management, woocommerce, merchandising, navigation, product-page
Source: How to Create an Ecommerce Website with WordPress 2026 (step by step).docx

---

## Upsells and cross-sells in WooCommerce linked products
Use when: Setting product recommendations on a PDP and in the cart to raise average order value.
- In the product editor's Linked Products tab, add Upsells — these show on the product page as an upgraded or higher-priced alternative to the item being viewed.
- Add Cross-sells — these appear in the cart when the shopper is close to checking out.
- Search for the products by name in each field; the targets must already exist as products in the store.
- Keep the relationship relevant (related product, not a random item) so the recommendation makes sense.
- Review on the storefront: open a PDP to see upsells and add an item to cart to see cross-sells render.
Caveat: Recommending unrelated items can distract from checkout; the tutorial's example pairs a cheaper headphone with a nicer one, not an arbitrary product.
Caveat: Cross-sells add cart steps — measure whether they help or hurt checkout completion.

Tags: woocommerce, merchandising, product-page, upsell, cross-sell, cart
Source: How to Create an Ecommerce Website with WordPress 2026 (step by step).docx

---

## Clean up demo products before adding your own catalog
Use when: Starting a store from an imported template and needing to replace placeholder products.
- Go to Products > All Products, select all demo products, apply the 'Move to trash' bulk action, then empty the trash.
- With an empty catalog, the 'Add product' flow prompts for product type: Physical (shipped), Variable (has variations like color/size), Grouped (a bundle sold as one).
- Reuse the structure: duplicate an existing configured product and edit it for the next item rather than repeating every field from scratch.
- Confirm new items appear in the homepage product sections that reference the catalog, and assign each to its category and price.
- If product thumbnails look grainy in grids, change the product image size in Customizer to e.g. 900x600 and republish.
Caveat: Duplicating carries over old images, descriptions and variations — scrub those before publishing.
Caveat: Image-size values are examples from the tutorial, not measured optimal sizes.

Tags: store-setup, woocommerce, catalog-management, product-setup, merchandising, product-page
Source: How to Create an Ecommerce Website with WordPress 2026 (step by step).docx

---

## Responsive design: serve different sections per device in Elementor
Use when: Fixing the homepage on mobile/tablet, e.g. a background video that doesn't play on phones.
- Switch to the phone/tablet icon in Elementor's responsive preview and inspect the section — video backgrounds often render as a gray gap on mobile.
- Duplicate the desktop hero section so you have two copies.
- On the duplicate meant for mobile, open Advanced > Responsive and hide it on tablet and desktop, leaving mobile enabled.
- On the original desktop section, hide it on mobile and leave tablet/desktop enabled, so each device sees one clean version.
- In the mobile section, remove the video link (or leave it blank), set the background to a gradient, and add a product Image widget instead.
- Use Advanced > Padding with the mobile-only indicator to space the section and keep content clear of the header; adjust per-element mobile settings like button position.
- Preview each device view before publishing.
Caveat: Duplicated sections multiply maintenance — update both when content changes.
Caveat: Pixel values shown are illustrative; check across real devices.

Tags: elementor, responsive-design, landing-page, mobile, design, conversion-optimization
Source: How to Create an Ecommerce Website with WordPress 2026 (step by step).docx

---

## Single product page spacing and button styling via Customize
Use when: Adjusting layout and colors on the WooCommerce product page so content clears the header and CTAs match the brand.
- Open the single product page and click Customize to reach the WooCommerce Single Product settings (these are theme options, not Elementor).
- Under Single Product > Design, unlink the padding values and set top padding (example: 120px) so the content clears the sticky header.
- Change the sticky add-to-cart button colors (background and hover) under the same Design panel; a page refresh may be needed for updates to show.
- Change global button background/hover under Global > Buttons, then publish and refresh to confirm.
- Edit the shipping-note text on the PDP (e.g. 'free shipping') under General > Single Product if your shipping terms differ.
- Add a purchase note under the product's Advanced tab for a custom post-purchase message, and keep menu order at 0 unless you need manual sorting.
Caveat: Setting padding without checking the responsive views can push content off small screens.
Caveat: Customizer labels vary by theme version.

Tags: woocommerce, product-page, design, conversion-optimization, elementor, checkout
Source: How to Create an Ecommerce Website with WordPress 2026 (step by step).docx

---

## Edit Elementor sections with device-specific padding
Use when: Tuning store homepage, PDP or landing-page section spacing in Elementor so content isn't cut off or crammed on mobile while staying correct on desktop.
- Select the section by clicking its six-dot handle, then open the Advanced tab to reach padding controls.
- Watch for the small device icon next to a control: if the icon is present the change applies only to that device; if it is absent the change is global across all breakpoints.
- Add padding around the section, unlink the values, and push extra padding to the top to move content down away from the header.
- Switch the editor viewport (desktop / tablet / mobile) and repeat the adjustment for each device that needs different spacing.
- Also edit individual widgets per device — buttons, headings and image widgets each have their own responsive controls.
- Click Publish to save, then use the preview (eyeball) icon to check the live rendering before moving on.
Caveat: Remember the device icon rule: a global edit will overwrite the value on every breakpoint, so make global changes first and device-specific ones after.
Caveat: If a section is disabled for desktop it won't render there at all — verify the correct breakpoint before assuming a layout is broken.

Tags: store-setup, elementor, wordpress, responsive-design, landing-page, page-builder, merchandising
Source: How to Create an Ecommerce Website with WordPress 2026 (step by step).docx

---

## Center misaligned Elementor widgets per breakpoint
Use when: Correcting a call-to-action button, heading or image on a store landing page that looks left-aligned or off-center on phones after template import.
- Switch the Elementor viewport to the device you want to fix (start with mobile).
- Click the widget (for example the button) and open the Style tab, then find the Position setting.
- Confirm the mobile device icon is showing next to the control before changing it, so the edit is scoped to that breakpoint only.
- Set the position to center.
- Switch back to desktop view — the widget automatically returns to its original alignment (for example left) because the change was mobile-scoped.
- Repeat the same operation in tablet view, then Publish and preview.
Caveat: If the device icon is not present, the alignment change will apply to all breakpoints — check before saving.
Caveat: Responsive overrides only behave as expected if the original desktop layout was left intact.

Tags: store-setup, elementor, responsive-design, landing-page, conversion-optimization, page-builder, mobile-commerce
Source: How to Create an Ecommerce Website with WordPress 2026 (step by step).docx

---

## Launch a WooCommerce store by switching from coming-soon to live
Use when: Final go-live step after building and previewing a WooCommerce store, when checkout and product pages need to be publicly reachable.
- Finish all page building, responsive edits and content replacement, and Publish your work in the builder.
- Preview the site with the eyeball icon to confirm layout, images, copy and store pages look correct on desktop and mobile.
- Locate the store's coming-soon indicator/notice and click it to open the setting.
- Change the status from Coming Soon to Live.
- Save changes.
- Verify on a logged-out browser or incognito window that product pages and checkout are reachable to the public.
Caveat: Don't switch to Live before testing checkout, payments and shipping settings — going live exposes the store immediately.
Caveat: Preview inside the editor is not the same as a public visit; confirm from an incognito session.

Tags: store-setup, woocommerce, wordpress, launch, checkout, pre-launch, go-live
Source: How to Create an Ecommerce Website with WordPress 2026 (step by step).docx

---

## Customise an imported template by replacing images, colours and text
Use when: Building a store homepage, category page or landing page quickly when a template already provides the section structure.
- Add or open the desired section and drop in an Image widget via the Add Element panel.
- Replace the placeholder image by selecting the image control and choosing the desired file from the media library.
- Overwrite placeholder copy with your own product, category or brand text.
- Change the template's accent colours in Style settings so the page matches your brand palette.
- Adjust spacing and alignment per device (see responsive padding/position cards) after swapping content, because template spacing rarely fits your assets.
- Publish and preview to confirm the swapped assets render correctly.
Caveat: Template images and copy may carry licensing/branding constraints — replace them before going live.
Caveat: Swapping content often breaks the original spacing, so always re-check padding and alignment afterwards.

Tags: store-setup, elementor, wordpress, templates, landing-page, merchandising, brand-consistency
Source: How to Create an Ecommerce Website with WordPress 2026 (step by step).docx

---

## Claim the $1/month trial link before the 3-day window closes
Use when: Opening a new Shopify account for a store build and choosing which plan to start on.
- Start at Shopify's official site, enter email, click start free trial, create a password and complete signup. Shopify then redirects to a promotional offer (source describes 3 months at $1/month, roughly 96% off).
- Activate the discounted plan immediately, or complete the short business setup questions first — the source says they take about 20 seconds and you still land on the dashboard afterward.
- If you skipped the offer in the signup flow, the source says it can still be claimed from the lower-left corner of the dashboard, but only before the initial 3-day free trial expires.
- Pick the Basic plan for a first store: it covers launching, accepting payments and running a functional store, and you can upgrade later.
- Verify the current plan names, trial length and offer terms in your own admin before assuming the promotional pricing still exists.
Caveat: Plan names, trial lengths and promotional pricing change; the source's figures are as-described at recording time.
Caveat: The source explicitly skips promotional pitches — treat the offer as a billing detail, not the point of the build.

Tags: store-setup, shopify, billing, plan-selection, account-creation
Source: Shopify Store Setup Full Tutorial 2026_ Step by Step.docx

---

## Know which three Shopify admin areas actually run the store
Use when: Orienting yourself in a new Shopify admin before adding products, designing the storefront or configuring checkout.
- Treat the admin as the store's control center: Orders, Products, Customers, Marketing, Discounts, Content, Markets, Analytics all live in one menu.
- Prioritize Products — this is where you add and manage the items you sell, including titles, descriptions, images, pricing, inventory and variants.
- Then Online Store — where you select and edit themes, build pages and manage navigation and the visual front end.
- Then Settings — where payments, shipping, taxes and store-wide configuration live.
- The source claims these three areas cover almost everything that matters; use them as the map, not as a reason to ignore Orders, discounts or analytics once you are live.
- Also note the source's framing: your store is technically already live at signup but password-protected, so you are optimizing an existing shell rather than starting from zero.
Caveat: Admin layout and menu labels change between Shopify releases; verify the current interface rather than hunting for exact labels.

Tags: store-setup, shopify, admin-navigation, store-configuration
Source: Shopify Store Setup Full Tutorial 2026_ Step by Step.docx

---

## Choose a clean, brandable domain instead of an over-thought one
Use when: Selecting the store domain before running ads, email or packaging that will display the URL.
- Run a quick ideation pass with a text AI — e.g. "generate 20 brandable domain names for a fitness apparel store" — to produce short variations instead of starting from nothing.
- Apply the source's filter: one or two words at most; no hyphens or numbers (buyers mis-type them and forget whether numbers are spelled out); no unusual spellings that force double-checking; brandable rather than generic. The source contrasts generic descriptors unfavorably with names like Gymshark, Allbirds or Glossier.
- Remember the impression cost: a myshopify.com URL or a long messy address appearing in an ad, email or packaging can create hesitation before a visitor reads a single product description.
- The source frames the goal as clarity, not perfection — easy to spell and easy to pronounce if heard once.
- Confirm availability and purchase inside Shopify where possible, so DNS connects automatically.
Caveat: Brand examples are the source's illustrations, not verified performance data.
Caveat: Perfectionism is explicitly called out as the failure mode; do not stall the build searching for an unused, flawless name.

Tags: store-setup, shopify, domain, branding, trust
Source: Shopify Store Setup Full Tutorial 2026_ Step by Step.docx

---

## Buy the domain inside Shopify vs. connecting an existing third-party domain
Use when: Setting up or migrating the store's domain before launch and before printing or advertising the URL.
- Fast path (buy new): go to Settings > Domains, click buy new domain, search the name, purchase if available. The source says it connects automatically with no manual DNS configuration.
- Migration path (existing domain, e.g. from GoDaddy): go to Settings > Domains > connect existing domain. Copy the DNS records Shopify provides, paste them into the registrar's DNS settings, save.
- Expect propagation to take a few hours; status may read as pending during that window. Do not treat pending as failure.
- The source flags a trade-off on third-party registrars: lower first-year pricing but often higher renewals. Buying through Shopify is described as the smoother route for beginners.
- Confirm the domain shows as connected before publishing, since launching on a broken domain creates immediate trust problems.
Caveat: DNS record names and screens differ by registrar and Shopify release; verify against the current Shopify domain instructions.
Caveat: The source's preference for buying through Shopify is a simplicity recommendation, not a cost guarantee.

Tags: store-setup, shopify, domain, dns, launch-checklist
Source: Shopify Store Setup Full Tutorial 2026_ Step by Step.docx

---

## Pick and publish a lightweight free Shopify theme before customizing
Use when: Choosing the storefront theme (fashion, beauty, large-catalog or general store) before any design work.
- Go to Online Store > Themes and scroll to explore free themes. The source names Dawn (minimal, versatile — suits fashion, beauty and general stores), Horizon (modern, bold — for stronger visual impact) and Trade (built for larger catalogs with many products).
- Always click the theme and choose view demo before installing. Preview first rather than installing blind.
- If it matches your brand direction, click add to theme library, then publish; the storefront updates within seconds.
- Weigh paid themes carefully: the source cites $200–$400 with extra built-in features, and argues most beginners do not need them because free themes now offer clean layouts, strong mobile optimization and fast loading. Speed matters because visitors abandon slow pages, especially on mobile.
- Do not over-analyze: the source says you can switch themes later, so pick one matching your niche and catalog size and move on.
Caveat: Theme names, features and paid pricing change; verify in the current theme store.
Caveat: Theme choice is not a permanent decision — treat it as reversible.

Tags: store-setup, shopify, theme-selection, mobile-optimization, storefront
Source: Shopify Store Setup Full Tutorial 2026_ Step by Step.docx

---

## Turn a default theme into a brand with global settings and a transparent logo
Use when: Customizing a freshly published theme so it stops looking generic and starts reading as a real brand.
- Open Edit theme. The left panel lists sections; the right panel is a live preview you refresh as you change things.
- Start with the header structure and alignment even if your logo is not ready yet.
- Go to Theme settings > Colors: set the primary brand color and keep the background white. The source argues white backgrounds generally convert better because products stand out on them.
- Go to typography settings and choose simple, readable fonts (the source names Montserrat and Source Sans Pro). Decorative fonts are explicitly called a clarity risk — if customers struggle to read, they leave.
- Generate a minimal logo with an AI image tool or free logo tools; text-based logos work well. Then use a background remover such as remove.bg to export a transparent PNG — the source calls messy logo backgrounds a common beginner mistake that instantly lowers perceived quality.
- Upload via the header/theme settings and adjust size so it looks balanced, not oversized or tiny.
- Optionally build a cohesive palette by asking an AI for a primary, secondary and accent hex set, then paste the primary hex into the color field and keep contrast high so text stays legible.
- Optionally use the theme editor's AI section recommendations: describe your brand in a few sentences and it generates layout suggestions for your niche.
Caveat: AI-generated palettes and sections are starting points; you still apply and review them inside the theme editor.
Caveat: White background and font choices are the source's conversion-oriented opinions, not tested rules for every brand.

Tags: store-setup, storefront, shopify, branding, theme-customization, typography, logo
Source: Shopify Store Setup Full Tutorial 2026_ Step by Step.docx

---

## Structure header, menu style and announcement bar for product count
Use when: Configuring the storefront header, menus and announcement bar before driving traffic to the store.
- In the theme editor, click header and review layout options — logo left or centered, depending on the aesthetic you want.
- Choose the menu style by catalog size: a drawer menu for stores with heavy mobile traffic, a dropdown menu for smaller catalogs, a mega menu for large stores with many categories.
- Keep the menu short. The source's reasoning: too many items create confusion and confused buyers rarely complete purchases.
- Enable the announcement bar and write a benefit-led prompt, e.g. free shipping on orders over $50 or a limited-time launch sale. The source frames these as small urgency cues that guide action.
- Refresh the preview and check the header/announcement combination doesn't crowd the top of the page, then re-check in mobile view.
Caveat: Menu-style suitability is the source's rule of thumb; test what fits your own traffic mix.
Caveat: Urgency prompts should reflect real terms — do not advertise a threshold or sale you will not honor.

Tags: store-setup, storefront, navigation, merchandising, announcement-bar, mobile-optimization
Source: Shopify Store Setup Full Tutorial 2026_ Step by Step.docx

---

## Build a hero banner that communicates one clear benefit
Use when: Designing or refining the homepage hero section — the first thing visitors see from ads or social traffic.
- Source the image direction first: prompt an AI with something like "produce a hero banner image that matches this brand" to get a concept aligned to your niche and positioning.
- Then use Shopify's built-in image library: click the hero section, select image, explore free images, and search niche keywords (fitness, skincare, jewelry). Choose high-resolution files only — a blurry banner immediately hurts credibility.
- Set a headline that communicates a benefit or outcome rather than a product name; the source's example is "confidence starts with skin."
- Add one short subtext sentence supporting the message, then a clear CTA button such as Shop now or Explore collection. The source says never leave a banner without a button because buttons drive the next click.
- Set the main homepage hero heading to an H1 tag so search engines can read the page structure.
- Preview on mobile: confirm the headline is readable and does not blend into the image. If contrast is weak, add a subtle overlay behind the text.
Caveat: Free stock imagery can look generic; the source treats image direction and resolution as the quality levers, not the source.
Caveat: H1 placement is a structural SEO practice the source asserts, not a ranking guarantee.

Tags: store-setup, storefront, landing-page, hero-section, seo, mobile-optimization
Source: Shopify Store Setup Full Tutorial 2026_ Step by Step.docx

---

## Generate policies from Shopify templates and customize every detail
Use when: Setting up privacy, terms, shipping and refund policies before the store accepts public orders.
- Go to Settings > Policies. Shopify provides templates for Privacy Policy, Terms of Service, Shipping Policy and Refund Policy; click create from template for each.
- Read through each generated policy and confirm it matches your actual business rather than publishing the default text unchanged.
- Draft shipping terms you will actually honor: delivery windows, handling time and conditions. The source notes that ignoring shipping details is a common beginner mistake that leads to disputes and unnecessary refunds.
- For the refund policy, decide the return window in days and who pays return shipping. The source ties clarity here directly to fewer chargebacks.
- If drafting is slow, prompt an AI (e.g. "write a simple shipping policy for this brand") for a starting draft, then replace every placeholder with your real terms — the source warns never to copy blindly.
- Save and confirm Shopify places the policies in the footer automatically.
Caveat: Templates are a starting point, not legal advice; the source repeatedly instructs reviewing and customizing them.
Caveat: Policy content must reflect what you actually do, or the mismatch creates the disputes it was meant to prevent.

Tags: store-setup, shopify, store-policies, refunds, shipping, legal-pages
Source: Shopify Store Setup Full Tutorial 2026_ Step by Step.docx

---

## Write a product page by describing the product, then generating and rewriting the copy
Use when: Adding a product to the catalog and building the PDP copy that will carry conversion.
- Go to Products > Add product. Write a simple, specific title so customers immediately know what the item is without guessing.
- Avoid copying supplier descriptions — the source says generic supplier text lowers trust because it reads overused.
- Write to benefits, not just features: explain how the product helps, improves or solves a problem, in short paragraphs that scan easily.
- To move faster, click the sparkle icon in the description box, briefly describe the product and let Shopify generate a draft — then edit it to match your brand voice.
- Keep formatting clean; better readability supports conversion.
- Also enable Track quantity and enter your available stock so you cannot oversell. The source notes dropshippers may disable tracking, but says tracking helps prevent order issues.
- Set the search engine listing preview: include your main keyword in the page title and write a concise meta description explaining what the product is.
Caveat: AI drafts are editing starting points, not finished copy.
Caveat: The track-quantity advice is framed with a legitimate dropshipping exception, so it is a situational default.

Tags: store-setup, product-page, shopify, copywriting, ai-assistant, seo, inventory
Source: Shopify Store Setup Full Tutorial 2026_ Step by Step.docx

---

## Use compare-at pricing, variants and 1000px+ images on the product page
Use when: Completing the pricing, options and imagery fields for each new product listing.
- Fill in both price and compare at price. The source's example: if the product sells for $49, set compare-at to $79 and Shopify displays the higher price struck through, creating perceived value. Keep the discount realistic — the source says overstated discounts reduce credibility.
- If the product has options like size or color, click add options and create variants (for example small, medium, large). Clear options smooth the buying process.
- Configure physical package dimensions in the product details so shipping calculations have accurate inputs.
- Upload bright, clear photos at least 1000x1000 pixels. Zoom in and check for blur; replace anything low quality. Sharper images build confidence and the source links this to fewer refund requests.
- Add product tags so the item can be grouped and found by your collections and internal search.
- Order the images so the first shot reads as the clearest representation of the product.
Caveat: Compare-at pricing only reads as credible when the original price is genuine; the source warns that exaggerated discounts backfire.
Caveat: The 1000x1000 pixel figure is the source's minimum guidance, not a platform requirement.

Tags: store-setup, product-page, pricing, product-images, variants, shopify, inventory
Source: Shopify Store Setup Full Tutorial 2026_ Step by Step.docx

---

## Choose manual vs. automatic collections and surface them on the homepage
Use when: Organizing the catalog into browsable categories and featuring them on the homepage.
- Go to Products > Collections > Create collection and name it clearly so customers know exactly what is inside.
- Choose manual collections to hand-pick individual products; choose automatic (smart) collections to group products by rules. The source's reasoning: automatic collections save time as the store grows.
- Add a collection image and a short description explaining what the category includes — this is what makes the browse step feel intentional rather than random.
- Return to the homepage in the theme editor, add a section that features your collection and select the correct category from the section settings.
- Preview the page and confirm products are now visible in the storefront rather than hidden in the backend.
- Use product tags consistently at the product level if you rely on smart collections, since rule-based grouping depends on those fields.
Caveat: Smart collection behavior depends on the rules and tags you configure; a mistagged product silently lands in the wrong collection.
Caveat: Collection image and description quality is what the source credits for perceived structure, not the collection type itself.

Tags: store-setup, shopify, collections, merchandising, product-page, navigation
Source: Shopify Store Setup Full Tutorial 2026_ Step by Step.docx

---

## Prune and rebuild the main menu around collections, then test it on mobile
Use when: Cleaning up store navigation before launch so customers can actually find products.
- Go to Online Store > Navigation and open your main menu. Remove default links such as home, catalog and contact that add no shopping path. The source's claim: cleaner menus convert better because they reduce decision fatigue.
- Click add menu item, name it clearly, click link, choose collections, select the matching collection and save. Repeat for your main categories.
- Limit the number of links — the source argues more options make customers hesitate.
- Open the theme preview and switch to the mobile view. Review spacing, test dropdown behavior and check the menu does not feel crowded; most buyers shop on their phone, so the layout must be thumb-friendly.
- Click every link, submenu and collection to confirm there are no broken paths or dead ends.
- Confirm your policies and support pages are reachable from the footer.
Caveat: Menu naming and link-picking flows change between Shopify versions; verify the current admin.
Caveat: The 'fewer menu items convert better' position is the source's stated rationale, not a measured benchmark.

Tags: store-setup, shopify, navigation, mobile-optimization, merchandising, launch-checklist
Source: Shopify Store Setup Full Tutorial 2026_ Step by Step.docx

---

## Order the homepage: hero, collections, featured products, then trust blocks
Use when: Arranging or auditing homepage sections after products and collections exist.
- Open the homepage in the theme editor and use Add section.
- Add a testimonials section. Even a few short quotes raise credibility; the source says pre-launch feedback from friends or early testers is acceptable when you have no buyers yet.
- Add an FAQ section covering the questions customers actually ask — shipping times, return policy, sizing. The source ties FAQs to reduced hesitation and fewer support emails.
- Review the whole page top to bottom and check the order: hero, then collections, then featured products, then trust elements like testimonials and FAQs. When it flows in that order the homepage feels guided rather than random.
- Look for anything that feels cluttered; the source compares the homepage to a storefront window where a random layout sends visitors away quickly.
- Re-check the same sequence in mobile view.
Caveat: Testimonials must be genuine; the source allows early tester feedback but misrepresenting reviews undermines the trust the section exists to build.
Caveat: Section names and availability vary by theme.

Tags: store-setup, storefront, homepage, social-proof, faq, merchandising
Source: Shopify Store Setup Full Tutorial 2026_ Step by Step.docx

---

## Activate Shopify Payments plus at least one alternative gateway
Use when: Enabling payment methods before taking the store off password protection.
- In admin, find Shopify Payments, click choose a provider, select it and complete setup — this connects payouts directly to your bank account and enables major card brands without separate integrations.
- Add at least one alternative method. The source calls activating only one method a common beginner mistake because it limits flexibility and can reduce trust.
- Enable PayPal: it is often already linked to your account email; otherwise click activate PayPal, log in and grant permissions — the source estimates about a minute.
- Consider that PayPal is familiar to international customers and may increase their comfort at checkout.
- Check what gateways are actually available in your region; the source notes some countries require specific providers.
- Reason from the source's principle: the smoother the checkout path, the less friction stands between a ready buyer and a completed order.
Caveat: Gateway availability and setup flows vary by country and change over time — verify what your region supports.
Caveat: Identity or document verification may be required and can delay payouts.

Tags: store-setup, shopify, payments, checkout, conversion-optimization
Source: Shopify Store Setup Full Tutorial 2026_ Step by Step.docx

---

## Define shipping zones, rates and a free-shipping threshold
Use when: Configuring shipping and delivery settings before launch, including whether to ship internationally.
- Go to Settings > Shipping and delivery, open your primary zone and define the countries you actually ship to. Decide deliberately between domestic-only and worldwide — the source notes global shipping adds complexity and starting simple is usually better.
- Pick a pricing model. Flat rate means a single fixed charge customers understand; dynamic rates calculate in real time by weight and carrier. The source says flat rate is often easier for beginners to manage and avoids confusion.
- Consider a free shipping threshold — the source's example is free over $75 — because customers respond strongly to free shipping and will add items to qualify, which lifts average order value.
- If you ship internationally, create separate zones and set higher flat rates or calculated rates for them.
- Add a handling buffer where it applies; the source describes adding around $5 to cover handling.
- State delivery times clearly everywhere shipping is mentioned. The source links long shipping without clear expectations to complaints.
Caveat: The $75 threshold and $5 handling buffer are the source's illustrative examples, not benchmarks for your margins — model them against your own cost structure.
Caveat: Carrier-calculated rates depend on accurate product weights and package dimensions.

Tags: store-setup, shopify, shipping, pricing, average-order-value, fulfillment
Source: Shopify Store Setup Full Tutorial 2026_ Step by Step.docx

---

## Configure taxes by verifying your own obligations first
Use when: Setting up tax collection for a store selling domestically or across borders.
- Go to Settings > Taxes and duties. The source's starting point: requirements depend entirely on your location, so verify your obligations under local law rather than guessing.
- Enable automatic tax collection, which calculates based on the customer's location, and review the rates configured for your region to confirm they align.
- If registered in the United States, review your state nexus rules to determine whether you must collect sales tax.
- If operating in the European Union, check VAT requirements and registration thresholds.
- Consult a tax professional if obligations are unclear — the source says mistakes here become expensive quickly.
- Once configured correctly, Shopify handles the calculations in the background.
Caveat: The source explicitly defers to local law and professionals; do not treat Shopify's defaults as compliance.
Caveat: Nexus and VAT rules change; re-verify as you add markets.

Tags: store-setup, shopify, taxes, compliance, international-selling
Source: Shopify Store Setup Full Tutorial 2026_ Step by Step.docx

---

## Install three apps, not ten — reviews, email, tracking
Use when: Adding apps to a new store without degrading page speed before launch.
- Go to Apps, open the Shopify app store and search only for essential tools. The source says most new stores need three things: a review app, an email app and a tracking/analytics app.
- Prioritize the review app because the source says reviews increase conversions almost immediately. Two named options are Judge.me and Loox: Judge.me is described as stronger on its free plan, Loox as focused on photo-based reviews.
- Enable automatic review requests so customers receive follow-up emails after purchase.
- Install a tracking/analytics app so you can see traffic sources, best-performing products and where people drop off. The source's framing: guessing is not a strategy.
- Resist installing many apps at once — the source says every added app adds weight and site speed affects conversion. Start lean and expand only when the business needs more.
- Review pricing and features before installing each app, especially as a store scales past the free tier.
Caveat: App features and free-tier limits change; the source's app comparisons reflect its recording time.
Caveat: Review apps may require configuration to avoid sending requests that look spammy or mistimed.

Tags: store-setup, shopify, apps, reviews, analytics, site-speed, retention
Source: Shopify Store Setup Full Tutorial 2026_ Step by Step.docx

---

## Run the pre-launch checklist: store details, domain, test order, mobile, policies, links
Use when: The last step before removing password protection and making the store publicly accessible.
- Verify store details: Settings > Store details — business name correct, email accurate, and store currency matching your target market. The source warns the wrong currency can confuse buyers and cause checkout abandonment.
- Check the domain: Settings > Domains should show Connected. If it still shows pending, allow a few hours for DNS propagation rather than launching on a broken domain.
- Test payments: enable test mode in payment settings, place a test order yourself, walk through the full checkout and confirm the order confirmation email actually arrives. Then disable test mode before launch.
- Review the store on your phone: scroll slowly, tap every button, add a product to the cart and complete checkout. Most customers shop on mobile, so the experience must feel smooth.
- Open every policy page from the footer and read the first paragraph — confirm your business name appears correctly and no placeholder or incomplete text remains.
- Click every menu item, submenu and collection to confirm no link leads to an empty or broken page.
Caveat: The source frames these as low-effort checks that prevent large post-launch problems; skipping the payment test is called out as risky because failed payments damage trust quickly.
Caveat: Test mode must be turned back off — launching with it active blocks real orders.

Tags: store-setup, shopify, launch-checklist, checkout, payments, mobile-optimization, store-policies
Source: Shopify Store Setup Full Tutorial 2026_ Step by Step.docx

---

## Remove password protection and verify the live store as a customer
Use when: Taking the store public for the first time, immediately before sharing the link on social or with testers.
- Go to Online Store and click remove password. The source describes this as the single step that makes the store publicly accessible — no preview mode, no restriction.
- Confirm the correct theme is live: go to Online Store > Themes and check your current theme shows as live. If it does not, click publish and confirm.
- Open a new browser tab, manually type your domain, and browse as a first-time visitor would: homepage, open a product, add it to cart, walk through checkout.
- Then start distributing the link — social bios, messages, a friend — and collect feedback rather than continuing to polish.
- The source's closing framing: the goal is progress, not perfection; keep improving and testing after launch.
- Also enable the email and SMS marketing opt-in checkboxes at the checkout/sign-in step so buyer consent is captured directly.
Caveat: Launching before collecting feedback is preferable to endless pre-launch tweaking, per the source; but re-run the checklist if any admin changes were made after the test order.
Caveat: Marketing opt-ins must match the consent rules in your jurisdiction.

Tags: store-setup, shopify, launch, retention, email-marketing, checkout
Source: Shopify Store Setup Full Tutorial 2026_ Step by Step.docx

---

## Shopify backend launch order
Use when: Preparing a newly built Shopify store to go live (final backend pass before publishing).
- In Settings > General, confirm store name, billing address, currency and default units. Getting these wrong affects order records later.
- Settings > Payments: activate Shopify Payments and connect the bank account. Have an ID document (driver's licence or passport) ready — identity verification is part of activation. Optionally add extra methods (e.g. crypto) via Add payment method; availability varies by region.
- Settings > Shipping and delivery: define zones and rates (details in the shipping card).
- Settings > Policies: generate refund, privacy, terms and contact templates; write a custom shipping policy (no template).
- Settings > Domains: connect an existing domain or buy one (the tutorial quotes roughly $16/year; verify current pricing).
- Online store: click Remove password — the store is inaccessible to customers until this is done.
Caveat: The presenter skips Shopify's onboarding questionnaire, noting it does not change what you get in the backend; skipping is fine but you must supply business details from your own records.
Caveat: Domain pricing and payment-method availability change over time — verify the current Shopify interface.
Caveat: Tax setup is jurisdiction-specific; consult a tax professional.

Tags: store-setup, shopify, checkout, operations, launch
Source: Shopify Tutorial for Beginners 2026 - Full Store Setup Guide.docx

---

## Adding product variants for size and colour
Use when: Product setup for an apparel store where one listing must cover multiple sizes or colours.
- Open the variant section while editing a product and add options such as size and colour.
- Add each option value so Shopify creates the variant grid.
- Set a distinct price per variant where justified (e.g. larger sizes or premium colours). In the tutorial's example the base product is $49 and variants are left at the default, but Shopify supports different prices per variant.
- Check inventory per variant after saving so each size/colour tracks separately.
- Save and confirm the variants appear on the product page and are selectable.
Caveat: Variant-level pricing is supported but the tutorial does not test it here; verify on your own listing.
Caveat: Skipping variants entirely means one price and one stock count for the whole product.

Tags: store-setup, shopify, product-page, merchandising, variants
Source: Shopify Tutorial for Beginners 2026 - Full Store Setup Guide.docx

---

## Compare-at price strike-through
Use when: Pricing a product on its Shopify product page when you want visible discount framing.
- While editing a product, set the Price field to the actual selling price (e.g. $49 in the tutorial).
- Fill the Compare at price field with the higher reference price. Shopify renders it as a strikethrough next to the live price.
- Save and preview the product page to check the discount reads clearly and the reference price is credible.
Caveat: The source presents this purely as a visual discount effect; it does not validate the fairness or legality of the reference price.
Caveat: Displaying a permanently raised compare-at price undermines trust if customers see the 'discount' never ends.

Tags: store-setup, shopify, pricing, product-page, merchandising
Source: Shopify Tutorial for Beginners 2026 - Full Store Setup Guide.docx

---

## Inventory tracking and out-of-stock behaviour
Use when: Backend inventory setup for a store deciding how to handle a product running out.
- Under Inventory, enter the current stock count; Shopify decrements it automatically on each sale.
- Leave 'continue selling when out of stock' off if you want the storefront to show a sold-out state when the count reaches zero.
- Turn it on if the product can be sourced after the sale (e.g. dropshipping) so checkout is not blocked.
- When new stock arrives, manually update the count.
- If you enable continued selling, watch that you can genuinely fulfil those orders or your refund/dispute rate will suffer.
Caveat: The source frames this as 'up to you' with no single rule; it notes manually adjusting the number when restocking.

Tags: store-setup, shopify, inventory, fulfillment, operations
Source: Shopify Tutorial for Beginners 2026 - Full Store Setup Guide.docx

---

## Manual collections: build category pages from a product list
Use when: Organising products into shoppable categories for navigation and the home page.
- Go to Products > Collections and add a collection.
- Give it a clear category title and upload a collection image — the image appears in collection lists and grids.
- Keep the collection type as Manual so you control membership.
- Under Products, click Browse, select the products for this collection and add them, then Save.
- Repeat for each category and for any curated set (the tutorial also builds a 'New arrivals' collection for home-page featuring).
- If Shopify pre-creates collections you do not want (e.g. a default Home page collection), delete it to keep the list clean.
Caveat: Manual collections do not auto-update as new products are added — you maintain them by hand, so revisit them when you add products.
Caveat: Collection images interact with the storefront layout (grids and lists) so choose crops that read at thumbnail size.

Tags: store-setup, shopify, merchandising, collections, navigation
Source: Shopify Tutorial for Beginners 2026 - Full Store Setup Guide.docx

---

## Delete default shipping zones before adding your own
Use when: Shipping configuration on a new store where default rates do not match your shipping plan.
- Settings > Shipping and delivery shows a profile for all products (one profile is fine for a simple store).
- Inspect the default zone: domestic shipping with weight-based rates and a free-shipping threshold ($50 and up in the tutorial).
- Delete the default zone via the three-dot menu > Delete — the source stresses this as a necessary step before adding your own.
- Click Add shipping zone, type the region (e.g. US), select it and Click done.
- Click Add rate, choose Flat rate (or dynamic rates by weight/volume/carrier), pick the shipping type (Standard, Express, Economy) and set the price — the tutorial uses Standard $6 and Express $15.
- Save and confirm the buyer-facing options at checkout.
Caveat: The transcript's 'Add rate' menu offers flat, dynamic and carrier-based rates; use flat only if you are not metering weight or volume.
Caveat: The $6/$15 figures are the source's example prices, not a benchmark — set rates to match your real costs.

Tags: store-setup, shopify, shipping, fulfillment, checkout
Source: Shopify Tutorial for Beginners 2026 - Full Store Setup Guide.docx

---

## Product shipping weight and box volume
Use when: Product setup where you are deciding whether to populate shipping dimensions.
- Under the product's Shipping section, enter the weight of the product and the volume of the box you ship it in.
- Use these fields only if your shipping rates are calculated by weight or volume.
- If you charge a flat rate, leave them blank — the tutorial deliberately skips them because it uses flat rates.
Caveat: Weight/volume only affects pricing if the matching rate type is active in shipping settings; filling fields without a dynamic rate does nothing.
Caveat: Accurate numbers matter later if you switch to dynamic rates; loose estimates produce wrong charges.

Tags: store-setup, shopify, shipping, fulfillment, product-data
Source: Shopify Tutorial for Beginners 2026 - Full Store Setup Guide.docx

---

## Product description and imagery for the PDP
Use when: Adding or improving a product listing on a Shopify store.
- Enter the product title, then the description; if stuck, use Shopify's built-in AI description helper (source offers this without judging quality).
- Drag several high-quality product images in, showing the product in its best light.
- Rearrange the image order because the first image is the one customers see on product and collection pages.
- Optionally complete the search-engine listing section of the product to control how the item appears in search results (the source leaves it default here).
- Save and preview on desktop and mobile.
Caveat: The source notes you should use high-quality images but offers no pixel or count guidance; decide based on your product.
Caveat: AI-written descriptions are offered as a convenience, not vetted for accuracy or brand voice.

Tags: store-setup, shopify, product-page, merchandising, product-data
Source: Shopify Tutorial for Beginners 2026 - Full Store Setup Guide.docx

---

## Pre-launch asset preparation checklist
Use when: You are about to build or rebuild a Shopify storefront and need to decide what to gather before starting theme customization.
- Prepare a logo as a transparent-background PNG (remove background with Canva, CapCut, or an AI background remover if you only have a colored-background version).
- Prepare a square favicon - the small icon shown in the browser tab; a single brand letter is enough, keep it simple.
- Lock a palette of four or five hex colors containing both dark and light values so you have contrast flexibility later in design; choose colors that make sense for the niche (blues for water-related products, greens for nature-related ones).
- Choose one or two fonts supported by the selected theme, and check matching fonts are available for other brand assets. Custom fonts may require theme configuration or code; verify the chosen theme rather than assuming a hired developer is mandatory.
- Prepare product list, collection list, product photos, lifestyle photos, and the About Us copy before building, since having them ready makes store work substantially easier.
Caveat: The source presents the four-to-five-color rule as a working habit, not an enforced standard.

Tags: store-setup, brand-assets, theme-customization, product-page, design
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Choosing a Shopify plan by card rate and staff seats
Use when: You are deciding which Shopify plan to subscribe to, or whether upgrading will pay for itself at your current sales volume.
- Compare the card rates the source cites: Basic 1.5%, Grow 1.3%, Advanced 1.1% on store payments - the main difference between tiers in this account.
- Estimate your monthly processed sales and check whether the rate saving on the higher tier exceeds the price difference before upgrading purely for rates.
- Check staff seats: Basic allows roughly one to two users, Grow up to five, Advanced up to 15; if multiple people must manage orders or the storefront, factor that in.
- Check whether you sell into multiple markets or need global settings; the source says market/global features differ by tier, so international sellers may need Grow or Advanced.
- Treat Shopify Plus separately: it is the only plan that allows customizing the Shopify checkout page, and the source cites roughly $2,000-$2,300/month - relevant only at an advanced stage.
- If your store is old, open Settings and audit which features you actually have: the source reports legacy accounts were migrated with varying entitlements, so an old Grow account may or may not include global settings.
- Verify plan pricing, card rates and seat limits in the current Shopify admin before committing, since these change.
Caveat: The 1.5/1.3/1.1% card rates are the source's figures at recording time; verify current rates.
Caveat: Plan names, seat counts and Plus pricing are the source's account and may have since changed.

Tags: store-setup, shopify-plans, pricing, unit-economics, payments
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Store details, currency, and order numbering configuration
Use when: You are in Shopify Settings > General during initial store setup and need to configure identity, currency and order numbering.
- Under General > Store details, set the store name exactly as you want customers to see it - it appears on order confirmation emails - and use a frequently-checked email for the store email address, ideally a branded one (e.g. hello@yourstore.com).
- Set the billing/legal business address to the region where the business is registered; the source says this drives which payment and shipping options, plus market behavior, Shopify offers you.
- Under Store defaults, set the store currency to your business region (e.g. EUR for a France-registered business) and change currency formatting there; per-market display currencies are managed under Markets and depend on payment gateway availability.
- Set the backup region, which is where customers outside your defined markets land by default.
- Choose the unit system you personally understand (e.g. kilograms).
- If you do not want customers inferring your order volume from order numbers (relevant during large launches), add a prefix or extra digits in the order ID settings so numbers are longer and harder to guess.
Caveat: Multi-currency display for foreign customers requires a suitable payment gateway such as Shopify Payments; availability depends on the country where the business is registered (the source notes limitations in some Middle East markets).

Tags: store-setup, settings, payments, localization, order-management
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Registering Shopify with your own owner email
Use when: You are creating a new Shopify account, possibly with help from an agency or freelancer.
- Sign up using your own email, not a contractor's or agency's address; the source stresses that only the store owner can change currencies, delete the store and similar critical actions.
- You can start on a personal Gmail, but plan to create a branded email later and use it for customer-facing communication to look more professional.
- Complete the payment method step (credit card or PayPal) to start the trial; the source describes Shopify commonly offering something like a short free trial then a heavily discounted first three months.
- Fill in business information properly at signup even though it can be edited later - under General settings this drives payment, shipping and market options.
- Set your store name when prompted; it can be changed afterward but appears in customer notifications, so choose deliberately.
Caveat: Trial length and introductory pricing vary; the source describes seeing seven-day and 14-day trials and roughly three months at $1 in different periods - confirm the current offer.
Caveat: Business-location restrictions mean some payment features (e.g. Shopify Payments) may not be available in your country.

Tags: store-setup, account-setup, shopify-payments, compliance
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Using role-based staff permissions instead of blanket access
Use when: You need to give an employee, contractor or agency access to your Shopify admin without exposing sales figures or settings.
- Upgrade to a plan with enough staff seats (the source moved to Grow to add users beyond the Basic limit).
- In Settings > Users, add the person's email; they receive a staff invitation to accept.
- Instead of a default role, create a custom role: name it, describe it, then tick exact permissions per admin area (home, products, orders, markets, etc.).
- Be deliberate about orders access - the source warns that order permissions let the person see your sales numbers, so grant it only where operationally necessary.
- If you cannot add a user on your plan, use collaborator access instead: share your myshopify.com domain and collaboration code so the developer or app requests access, then approve them as a collaborator.
- Remove access at any time as the store owner.
Caveat: Collaborator access is a workaround for the user-seat limit, not a full substitute - the source says at some point most stores genuinely need a paid staff seat, e.g. an order manager.
Caveat: Admin navigation and permission labels may change; verify in the current Shopify interface.

Tags: store-setup, security, team-permissions, settings
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Connecting a custom domain and handling DNS records
Use when: You are moving from the default myshopify.com URL to a branded customer-facing domain, or an app asks you to edit DNS records.
- Check domain availability when you first choose your brand name - the source warns that later, taken or premium names can be expensive or unavailable.
- Prefer the .com for customer familiarity and cross-market recognition; consider also buying other extensions (.co, .au, .de) defensively so nobody else registers your brand name.
- Buy either directly through Shopify (simplest, auto-linked to the store) or through a registrar like GoDaddy and use Settings > Domains > Connect existing to link it.
- Note that your myshopify.com domain remains important internally - apps and support may ask for it - even though customers should never see it.
- If automatic linking is unavailable, log into your registrar, open the domain's Manage DNS section, and add the records the requesting tool specifies: it usually provides type, name and value; the source says most tools require about three records.
- Save the records and allow propagation time before testing.
- Apply the same DNS-record workflow later for sender emails (Klaviyo, Omnisend) and review apps.
Caveat: The source notes it is not certain every registrar behaves identically to GoDaddy; consult the specific provider's DNS interface.
Caveat: Each DNS tool supplies its own record set - do not copy records between tools.

Tags: store-setup, domains, dns, deliverability, brand
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Setting up store policies and return rules
Use when: You are preparing to launch or run ads and need legally presentable store policies plus a workable returns process.
- In Settings > Policies, use Shopify's insert-template option for each policy (privacy, terms of service, shipping, contact information, terms of sale, legal notice) and then edit the template to match your actual business rather than publishing it untouched.
- Configure return rules so customers can initiate returns from their customer account; set the return window and shipping rates in the manage settings.
- Keep the shipping policy distinct from actual checkout shipping rates - the source notes rates are configured elsewhere, while the policy communicates how you manage shipping generally.
- Link shipping and return/refund policies in the product page where relevant, and all policies in the footer at minimum; the source treats this as required for running ads and for legal coverage.
- For contact information, review the auto-filled template - it pulls from your general business details - and edit anything you do not want published (e.g. a personal address).
Caveat: The source recommends double-checking policies with a lawyer or legal advisor, especially for the EU and UAE; it flags the UK privacy policy as having different rules.
Caveat: Shopify's default templates are described as generally good but needing tweaking.

Tags: store-setup, legal, returns, policies, conversion-optimization
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Choosing customer support tooling by catalog complexity
Use when: You are deciding how customers will ask pre-purchase questions and how you will answer them at launch versus at scale.
- For a new or simple store, install Shopify Inbox: the source describes it as free, with a phone app and a view of each customer's order history so you can reply with context rather than cold.
- For large catalogs or education-heavy niches (cosmetics, skincare, electronics) where customers ask many product questions, plan to move to a tool with AI reply features; the source names Gorgias and Tidio as examples.
- Use the customer's order and browsing history visible in the inbox to tailor the answer - the source explicitly contrasts context-based replies with random ones.
- Before launch, check that contact information is complete in your policies so the support channel is discoverable.
Caveat: The source describes the AI option as what you may need later, not a launch requirement; a simple business can run on Shopify Inbox.
Caveat: Tool names and feature sets change - verify current capabilities and pricing in each tool.

Tags: store-setup, customer-support, retention, chat, shopify-apps
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Adding a product: title, description and image ratios
Use when: You are creating a product record in Shopify before or alongside PDP design.
- Enter the product title. Decide per brand whether to use a clear SEO-friendly name or a branded product name - the source presents both as valid choices.
- Save, then check the auto-generated URL at the bottom of the editor; if you later rename the product, return and update the URL handle.
- Write a short, simple inline description. Treat it as the text appearing beside the product photos rather than as the whole sales argument - the source says complicated, education-heavy products should get their additional information in a properly structured product page below the fold instead.
- Upload all product images in one batch, and keep every image in the same dimensions and ratio across the catalog. The source prefers square because squares cannot mismatch, preventing weird cropping and misalignment.
- Keep final image sourcing consistent with the variants you will create (e.g. one set per color).
Caveat: Shopify's built-in AI description generator exists in the editor, but the source prefers writing descriptions with ChatGPT; use whichever produces on-brand copy.
Caveat: The source's short-inline-description guidance is a recommendation, not a hard rule - what determines length is product complexity.

Tags: product-page, product-setup, merchandising, seo, creative-strategy
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Configuring product type, vendor, tags and category
Use when: You are adding products and want collections, filters and product attributes to work without rework.
- Set the product Type to the closest descriptive term (e.g. legging, bra, jumpsuit, accessory) - the source notes type feeds collection filters, so specificity now saves cleanup later.
- Set the Vendor to the brand name of the item; use the actual third-party brand if you resell other labels.
- Use tags as product properties for collection rules, not as social-media-style hashtags. The source's method: decide which collections you intend to build (e.g. 'leggings', 'black leggings') and add tags matching them, because tag-based collection rules are hard to get wrong.
- Choose the most precise Shopify product Category via the suggested category. The source shows that a specific category (legging) unlocks an extra attribute section - colors, activewear/clothing features - whereas an uncategorized product shows nothing extra.
- Review the auto-detected attribute values (e.g. colors) Shopify pre-fills, then decide which to accept; the source accepted all and noted accuracy was close but not perfect.
- Optionally add the product to a collection manually; Shopify places new products in the homepage collection by default and the source considers keeping that acceptable.
Caveat: Metafields unlocked by category are not mandatory to fill.
Caveat: The source describes the category feature as relatively new at recording time; the available attributes per category may have expanded.

Tags: product-setup, merchandising, collections, metafields, taxonomy
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Pricing fields: compare-at and cost of goods
Use when: You are setting product pricing or running a sale and want correct strikethrough display and usable cost data.
- In the Pricing section, enter the Price as the amount the customer actually pays today.
- To show a sale, enter the original higher amount in Compare at price and the current amount in Price; the source describes the customer seeing the compare-at figure struck through next to the current price.
- Enter the per-unit Cost of goods - what you pay for the item itself, not all other expenses. The source cites the example of a €60 selling price with a €20 cost, and stresses that recording cost makes later margin, audit and profitability calculations easier.
- Use the 'sell by unit' option only where it applies to your product (the source does not use it for apparel).
Caveat: Cost of goods in the source's example excludes other business costs; do not treat it as full landed cost unless you include those.

Tags: pricing, product-setup, unit-economics, merchandising
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Independent inventory, SKUs and warehouse coordination
Use when: You are setting stock levels and identifiers on a product, or preparing to hand fulfillment to a warehouse.
- Turn on inventory tracking rather than managing stock only outside Shopify; the source questions the value of switching it off.
- Enter the on-hand quantity. Here 'available' is what you can sell; when an order comes in, 'committed' rises and available drops (100 in stock, first order shows committed 1 and available 99).
- Use the 'unavailable' quantity field for stock you hold back - damaged items or inventory you do not want publicly sellable - so it is not lost from your records.
- Enter at least one of SKU or barcode; the source says most warehouses work adequately with either, and suggests you can even use the same value in both fields. This is how the warehouse identifies what the customer bought and keeps order processing accurate.
- If you operate multiple warehouses/locations, each location shows its own quantity field so you can allocate stock per location.
- Decide deliberately whether to continue selling when out of stock, based on how quickly you can restock.
Caveat: The source describes SKU/barcode importance mainly in the context of third-party warehouse fulfillment.
Caveat: Inventory location behavior assumes locations are configured; the source covers that setup separately.

Tags: inventory, fulfillment, product-setup, operations, sku
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Product weight, shipping profile and variants
Use when: You are completing the shipping section of a product and setting up size/color options for apparel or similar catalog.
- In the Shipping section, switch weight on and enter the product weight (the source uses 0.25 in a chosen unit). The source states that leaving weight off makes Shopify treat the item as a digital product, so physical goods need it.
- Record weight even if you do not bill shipping by weight: the source notes some warehouses need product weight regardless of your shipping rate method.
- Use the customs/duties fields if you ship internationally.
- To create variants, click Add options and define the axes; the source's activewear example uses Size (small, medium, large shown, with more needed) and Colour (navy and red).
- Expect variants to drive separate media associations and per-variant inventory/pricing where relevant.
Caveat: The source's size list in the example is deliberately incomplete for a legging range - build the full size run your catalog needs.
Caveat: Weight units and the physical/digital determination should be verified in the current Shopify product editor.

Tags: product-setup, shipping, variants, fulfillment, apparel
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Defining brand assets in Shopify settings
Use when: You are in Settings > General > Store assets and want theme customization to pull consistent branding without manual re-entry.
- Upload the rectangular brand logo, then upload a square logo - the source reuses the favicon here because a favicon is square.
- Add brand colors by clicking plus and pasting each hex code; define a primary color, a contrasting color chosen to be light against the dark primary for contrast, and secondary colors. The source says brands typically use four to five colors.
- Optionally upload a cover image and add a slogan and short business description.
- Add social links - at minimum Instagram, TikTok and Facebook. The source observes that people landing on a new brand often check its Instagram next, so missing links cost credibility.
- Save. The source emphasizes that defining assets here makes later theme customization easier because the theme draws on these values.
Caveat: Cover image, slogan and description are optional in the source's walkthrough.
Caveat: This step only pays off if your theme is configured to use the store's brand assets; verify in your theme.

Tags: store-setup, brand-assets, theme-customization, social-proof, design
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Orienting yourself in the Shopify admin navigation
Use when: You are new to Shopify admin or onboarding a staff member and need to know where each store operation lives.
- Home: Shopify communications and later a sales summary.
- Orders: incoming orders and their management.
- Products: the product list, plus sub-items for Collections, Inventory, Purchase orders, Transfers and Gift cards.
- Customers and Segments: everyone who bought or merely signed up, with segmentation available.
- Marketing: campaigns and automations; Discounts sits alongside it.
- Content: uploaded files, Menus, Blog posts and Metaobjects (the source flags metaobjects as relevant when creating colour swatches).
- Markets: selling internationally to different countries or regions.
- Finance and Analytics: analytics becomes important once you have data; the source defers deep coverage to the end of the course.
- Sales channels: where you sell; Online Store by default, plus Facebook, Instagram, TikTok and Shop once connected.
- Apps: third-party apps; and Settings in the corner for all business configuration.
Caveat: Admin labels and grouping can change between Shopify releases; verify current navigation.

Tags: store-setup, shopify-admin, navigation, operations
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Create Physical Products with Weight to Enable Shipping
Use when: Adding a new physical product in Shopify admin and configuring shipping eligibility.
- When creating the product, enable the weight field; otherwise Shopify treats the product as digital and will not present shipping options.
- Enter the product weight (e.g. 0.25) and change the unit as needed to match your warehouse and carrier conventions.
- Optional: add customs/duties-related information for cross-border shipping from the same area.
- Save, then verify the weight by checking the product in the Shipping settings or by previewing checkout rates for a destination.
Caveat: Applies to physical goods; digital products intentionally skip weight.
Caveat: Weight units affect calculated carrier rates — keep them consistent across the catalog.

Tags: store-setup, product-setup, shipping, fulfillment, inventory
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Set Up Product Variants for Size and Color
Use when: Listing apparel or any product that comes in multiple sizes, colors, or materials.
- In the product editor, scroll to Variants and click Add options; add the first option such as Size and list values (Small, Medium, Large), then Done.
- Add a second option such as Color; Shopify links variant colors to the product's category meta fields automatically.
- Assign an image to each variant so shoppers see the right photo when they select a combination.
- Edit price and quantity per variant (e.g. 100 units each) if they differ; confirm quantities are accurate before saving.
- Click Save; if you use exotic colors or patterns, plan to set up color swatches later rather than relying on default names.
Caveat: Variant options are limited by Shopify's maximum option/combination constraints — verify current limit in the admin.
Caveat: Multiple images per single variant requires specific (often paid) themes.

Tags: store-setup, product-setup, variants, inventory, merchandising
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Build Manual vs Smart Collections
Use when: Organizing a catalog into collections that stay current as products are added.
- Go to Products > Collections and click Add collection.
- Name the collection and optionally add a description and image.
- Choose Manual (hand-pick products) or Smart (rule-based); once saved the type cannot be switched, so decide with future catalog growth in mind.
- For Smart collections, set a condition such as product tag equals 'leggings' so any tagged product joins automatically.
- Alternative rules include product type, category, vendor (e.g. Adidas), weight, or inventory stock (e.g. only items with 10 units left).
- Save and confirm the collection's condition displays correctly in the collections list.
Caveat: You cannot convert manual to smart or vice versa after creation — plan ahead for large catalogs.
Caveat: Tag-based collections require consistent tag spelling across products or items will not appear.

Tags: store-setup, collections, merchandising, taxonomy, catalog-management
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Tag Products Consistently for Smart Collections
Use when: Assigning tags to products so collections, filters, and navigation stay organized.
- Decide on a small, consistent tag vocabulary (e.g. leggings, bras, accessories, overalls) before tagging.
- In each product, add the exact tag text — copy and paste to avoid typos like 'bras' vs 'bra'.
- Build smart collections with conditions matching those tags (tag equals leggings, tag equals accessories).
- After saving, refresh the collections view; updates can take a few seconds to propagate.
- If a product is missing, verify its tag spelling and re-save.
- Only tag products with the category they are sold under to keep collections clean.
Caveat: Smart collections depend on exact tag matching; small typos break the rule silently.
Caveat: Tags can be edited later, but bulk changes may need third-party apps when Shopify's bulk editor is limited.

Tags: store-setup, collections, product-setup, merchandising, catalog-management
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Use Bulk Edit for Prices, Quantities, and Tags
Use when: Cleaning up prices, stock levels, or tags across a large product catalog.
- Go to Products, select products, and click Bulk edit to open the spreadsheet-style view.
- Use Columns to choose which fields are visible (e.g. price, inventory, tags).
- Fill in missing prices or quantities; drag values down across rows like a spreadsheet.
- For inventory, confirm 'track quantity' status per product and set quantities (e.g. 100) where missing.
- For tags, add consistent values such as 'accessories' or 'leggings' so future smart collections catch them.
- Save and re-verify in the products list and collections.
Caveat: Bulk edit has limitations; complex changes may require a dedicated bulk-editing third-party app.
Caveat: Tag changes propagate to smart collections only after a short delay or refresh.

Tags: store-setup, catalog-management, inventory, product-setup, bulk-edit
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Edit Product Images In-Shopify: Crop, Resize, Remove Background
Use when: Fixing inconsistent product photos or making PDP images match your visual standards without external tools.
- Open a product, click an image, and use the built-in tools.
- Crop to a fixed ratio (e.g. square) when images are inconsistent.
- Rotate, flip, or resize to a specific pixel size.
- Use background removal to strip the background and apply a solid color like white for consistent PDP backgrounds.
- Optionally use the AI background generator with a text prompt (e.g. 'outdoor garden') to place the product in a scene, but expect occasional failures.
- Choose Save in place or Save as new; saving as new keeps the original and adds the edited image to the product.
Caveat: The built-in AI background generator can fail or produce mediocre results; dedicated tools like Canva may be stronger for complex edits.
Caveat: AI-generated backgrounds may not match brand aesthetics — review before saving to the live PDP.

Tags: store-setup, product-setup, product-images, creative-strategy, product-page
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Generate Product Images with Sidekick AI
Use when: Creating lifestyle or contextual imagery for product pages or ads when you lack photoshoots.
- From the Shopify dashboard, click the Sidekick icon to open the AI assistant.
- Upload or paste your product image into the Sidekick conversation.
- Write a simple prompt describing the scene you want (e.g. 'show someone drinking this coffee in an office').
- If the first result is illogical, refine the prompt (e.g. 'show someone holding the coffee in their hands') and regenerate.
- Save the resulting image file from the Sidekick chat and upload it to the product or page.
- Verify the current interface, as Sidekick's capabilities and access change with Shopify releases.
Caveat: Access to Sidekick and its image generation may vary by store and Shopify plan; the interface has changed in recent editions.
Caveat: AI images can look unrealistic for some niches — review against brand standards before publishing.

Tags: store-setup, product-images, ai-tools, sidekick, creative-strategy
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Configure Variant Color Swatches with Hex or Pattern Images
Use when: Setting up color swatches for a product where default swatch colors are inaccurate or you sell patterns/textures.
- In the product editor, look under the linked category meta field for colors.
- Replace default color names by editing entries; add new entries like 'dark blue' or 'dark green' via Add new entry.
- Provide an exact hex code (search Google for the color hex if needed) so the swatch matches the real product color.
- For patterns, textures, or uncertain colors (e.g. lip butter texture), upload a label image instead of a hex code.
- Save and assign variant images for each color.
- Note: showing only selected-variant images on the PDP requires theme support — often paid themes, not free ones.
Caveat: Default Shopify color extraction is not accurate — always verify or override.
Caveat: Some themes (usually paid) support variant-specific image display; free themes often do not, and setup differs per theme.

Tags: store-setup, variants, product-page, merchandising, color-swatches
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Set Up Storefront Filters with the Search and Discovery App
Use when: Adding filterable navigation to a collection page so shoppers can narrow a large catalog by attributes.
- Install the free Shopify Search and Discovery app.
- Open Filters; Shopify starts with availability and price — remove those that don't fit your catalog.
- Click Add filter and pick a source: category meta fields, standard fields like vendor/brand, or your own product meta fields.
- Save and verify on the storefront that the right filter values exist for products in the collection.
- To check which categories a meta field applies to, go to Settings > Custom data > Products > Assigned to categories.
- Filter options to consider: brand, color, size, availability, sport type, waist style, length — driven by what shoppers actually search for.
Caveat: Filters only appear if the underlying meta field values are populated on products.
Caveat: The app's UI and available sources change with Shopify updates — verify the current interface.

Tags: store-setup, filters, collections, navigation, merchandising
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Create Custom Product Filters When Category Meta Fields Fall Short
Use when: Adding a filter attribute your niche needs that isn't in the default category meta fields.
- Go to Settings > Custom data (meta fields and meta objects) > Products, then Add definition.
- Name it (e.g. 'trial filter') and choose a type; 'list of values' lets one product appear under multiple values (e.g. gold and white gold).
- Set the input type (e.g. single line text) and assign it to categories or leave it open for all products.
- Save, then fill the meta field per product (or bulk edit across products).
- Return to the Search and Discovery app, Add filter, and choose the new product meta field as the source.
- Verify on the collection page after saving.
Caveat: If left unassigned to categories, the field appears on all products — which may add confusion for categories where it doesn't apply.
Caveat: Values must be populated per product or the filter shows empty.

Tags: store-setup, filters, meta-fields, navigation, merchandising
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Choose Filters from Customer Search Language
Use when: Deciding which filters to expose on category pages for a new or existing store.
- Review your product categories in Shopify to see default meta fields Shopify pre-assigns (e.g. yoga mats get color, material).
- Study competitors and large stores in your niche to see which filters they surface.
- List questions customers commonly ask and the ways they describe products (e.g. 'cotton leggings', 'ankle length', 'black leggings').
- Select only filters that map to real search intent — don't include every available attribute.
- For stores with large catalogs, plan filters early so the catalog stays organized as it grows.
Caveat: This is the presenter's recommended approach, not a universal rule; small catalogs may need fewer filters.
Caveat: Over-filtering with rarely used attributes clutters collection pages and can hurt navigation.

Tags: store-setup, filters, customer-research, merchandising, collections
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Filter Shopify Themes by Industry, Catalog Size, and Required Features
Use when: Shortlisting candidate Shopify themes before committing to a design foundation.
- In the theme store, filter by Industry to see demo themes closest to your niche (e.g. Beauty).
- Filter by Catalog size: modest catalogs (roughly 11–100 products) differ from large (500+) stores, which need heavier search and navigation.
- Filter by Features: e.g. before/after slider for cosmetics, color swatches, combined listing, age verifier for regulated goods.
- Prioritize paid themes ($100–$400 one-time) when the source's experience suggests free themes often lack features and polish; the source's opinion, not a universal rule.
- Open the demo store, check the PDP layout and section list, and read the reviews.
- Inspect the developer: click through to their profile, check how many themes they publish, and search the company on Google to gauge legitimacy.
Caveat: Filters may over-narrow results (e.g. only 20 themes for combined listing) — relax filters if the shortlist is too small.
Caveat: The source's preference for paid themes is a personal opinion; free themes can work for simple stores.

Tags: store-setup, themes, merchandising, product-page, store-design
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Preview Mobile and Desktop Before Buying a Theme
Use when: Evaluating theme candidates before purchase or trial installation.
- On the theme's page, click View demo to open the full desktop storefront.
- Scroll through home and PDP sections to evaluate layout, social proof placement (UGC video, before/after), and section variety.
- Check the mobile preview or open the demo URL on a phone; mobile is where most shoppers land.
- Note which sections exist in any demo preset of the same theme — features seen in one preset apply across the theme.
- Keep only themes whose mobile layout meets your standard; discard the rest.
Caveat: Demo stores may use different presets; confirm the feature you want actually exists in the theme settings.
Caveat: This is preparatory research, not a substitute for testing the theme with your own catalog.

Tags: store-setup, themes, mobile, product-page, store-design
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Trial a Theme Before Buying to Preserve Work
Use when: Deciding between finalist themes before committing to a purchase.
- Confirm you are signed into the correct Shopify store.
- Click Try theme on the theme's store page; Shopify adds a full trial version you can edit but not publish.
- Open the theme editor and build out key sections (home, PDP, coming soon page) to test fit.
- If satisfied, click Buy; all your changes are preserved and the theme becomes publishable.
- Optional: before upgrading, duplicate the theme via the three-dot menu to back it up (or use a backup app).
Caveat: Some features — e.g. editing theme code or using product page templates — may require purchase first; verify current limitations.
Caveat: Trial versions cannot be published to customers.

Tags: store-setup, themes, store-design, experiment-design, product-page
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Duplicate Your Theme as a Backup Before Big Changes
Use when: Before large theme edits, version pushes, or any risky change to a live storefront.
- Go to Online Store > Themes.
- Click the three dots next to the theme and choose Duplicate.
- Rename the duplicate clearly (e.g. 'backup pre-update').
- Use third-party theme backup apps if you need scheduled or versioned backups that Shopify's built-in duplication doesn't cover.
- Verify the duplicate appears in the theme list before proceeding with the risky change.
Caveat: Built-in duplication gives a snapshot, not automated version history; apps provide more robust backups.
Caveat: Duplicating is not a substitute for testing changes in a trial or unpublished theme first.

Tags: store-setup, themes, risk-management, store-design
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Set Up a Password-Protected Coming Soon Page
Use when: Preparing to launch a store or keep a site private while building it.
- By default the store is protected; visitors see the coming soon (password) page instead of the storefront.
- Go to Online Store > Themes > Password theme and start customizing — it works like any other theme page.
- To preview what customers see, open your store's domain in an incognito window (avoid the logged-in admin view).
- The password required to unlock the store is set under Settings > Preferences (or the account's password page settings) — share it only with intended viewers.
- Remove the lock when the store is ready to launch.
Caveat: Forgetting the store password or leaving the lock on post-launch blocks all customer traffic.
Caveat: The exact settings path may shift with Shopify releases — verify in your admin.

Tags: store-setup, coming-soon, themes, store-design, launch
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Reject One-Click AI Whole-Store Theming; Design for Conversion
Use when: Deciding whether to launch with an auto-generated theme or to design the storefront deliberately.
- Optional test: run Shopify's AI theme generator (e.g. with a prompt like 'active wear brand') to see the generated layout.
- Treat the output as a starting idea, not a final storefront — the source is not a fan of the feature and prefers building step-by-step.
- Design for conversion, not only aesthetics: make information legible, products easy to explore, and social proof visible.
- Aim to convert visitors into first-time buyers and repeat customers, not just to look polished.
- If the theme lacks needed sections, consider a paid theme or theme AI editor tools rather than forcing the auto-generated layout.
Caveat: Availability of the AI theme generator varies by store and Shopify plan.
Caveat: This is the presenter's opinion; some merchants may find the generated themes a useful starting point.

Tags: store-setup, themes, conversion-optimization, store-design, ai-tools
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Plan Theme Around Site Structure and Future Catalog
Use when: Committing to a theme for a store you plan to grow over years.
- Before browsing themes, list the features/sections you want (visual effects, product recommendations, comparison tables, ingredient panels, UGC, before/after sliders).
- Do competitor research and note the sections and layouts you want to emulate.
- Accept that the theme is a one-time, multi-year choice — changing later means redoing setup and settings across the store.
- Prefer themes from proven developers when planning to stay on the theme for years, since they maintain updates.
- Use the theme store's filters and the demo browser to shortlist and compare candidate themes.
- Keep in mind that the Shopify editor's logic applies across themes even if exact settings differ — you are learning the process, not one theme's menu.
Caveat: Theme migration later is possible but time-consuming; the presenter treats this as a major commitment.
Caveat: The theme's AI section-building tools are described as glitchy and inconsistent — don't rely on them as the primary customization method.

Tags: store-setup, themes, store-design, merchandising, product-page
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Lock the store with password during setup and use it for early access
Use when: Launching or pre-launching your store, or running an early-access drop for waitlist subscribers.
- Understand the default: every new Shopify store is locked with a password set by Shopify automatically, found under Preferences in the Shopify admin.
- Verify the lock by copying your store's domain and loading it in an incognito/private browser window (so you're not signed in); you should see only a 'coming soon' page with a password field.
- Before you go live, return to Preferences and turn the password protection off, or customers will keep seeing the coming soon page instead of your store.
- For a launch tactic: give your waitlist email subscribers the password a few hours before the public launch so they get first access to the products. This mirrors an approach the presenter used with a client's early-access launch, not a guaranteed outcome.
- Consider how long you leave the store locked; the longer it stays locked, the longer you delay any organic discovery or ads traffic actually seeing products.
- Confirm the current location of the password setting in your admin, as Shopify's interface changes over time.
Caveat: The default password and location of the Preferences setting may differ by Shopify plan and admin version; verify in your own store.
Caveat: Keeping the store locked means ad or SEO traffic cannot see products until you unlock it.

Tags: store-setup, launch, early-access, password-protection, retention, acquisition
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Edit products, collections and pages inside the theme editor
Use when: Eyeballing a section and wanting to tweak the linked product, collection title/description or page content while you stay in visual edit mode.
- Open the theme editor and click the section whose underlying data you want to change (for example a Featured Collection section pointing at your active wear collection).
- Click the edit pencil/button on the setting; the collection editor popup appears directly in front of you, so you can change the collection's rules, title or description without leaving the editor.
- Apply the same logic to products and pages: click the setting that references the product or page and edit it in the popup.
- Use this when merchandising sections quickly, e.g. swapping which collection a homepage section shows or fixing a collection title you noticed looks wrong in the preview.
- Still go back to the Shopify backend for things the editor doesn't handle: adding richer product information, creating menus, and other admin-level tasks.
- Confirm these inline edit affordances exist in your current theme and Shopify version before relying on them.
Caveat: This inline editing capability is tied to recent Shopify updates and may not cover every field or every theme setting.

Tags: store-setup, theme-editor, merchandising, product-page, product-data
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Navigate the theme editor: locations, pages, inspector and view modes
Use when: Setting up your store theme and figuring out where to make changes and which page or market you're editing.
- Check the location selector: at the start you must be editing Store Default; later you can customize per-market or per-country (for example a French banner for France, a German flag banner for Germany).
- Know the plan limitation: per-market customization is not available on the basic Shopify plan; if you plan to sell worldwide with per-market changes, you need to upgrade. Verify current plan features.
- Check the page selector: the editor always opens on the Homepage, but you can switch to Products (default product template), collections, pages, etc.
- Use the Sidekick button (Shopify's AI) for quick data questions—e.g. asking how many units of a specific product have sold instead of digging through analytics reports.
- Toggle the Inspector: hovering over store elements turns them blue so you can click them to open and add sections; turn it off to navigate from the sidebar instead.
- Switch between desktop, mobile and full-screen views; treat mobile view as accurate but not 100% accurate—always preview the real link on a phone before finishing.
- Use the three dots menu for preview, theme documentation and keyboard shortcuts; undo, redo and save control your edits in the sidebar.
Caveat: Mobile in-editor preview is not exactly the live mobile rendering.
Caveat: Per-market customization is plan-gated; check your Shopify plan before planning localized banners.

Tags: store-setup, theme-editor, mobile-preview, localization, markets, sidekick
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Get a shareable preview link for draft and published themes
Use when: Testing your store on a real phone, or sending a work-in-progress theme to a client or teammate for review.
- For a non-published (draft) theme: click the three dots, click Preview, then use the bar that appears and click Copy preview link—share that URL freely.
- For the published theme: the preview doesn't behave the same way. Click the three dots, click Preview, then right-click and choose Copy link address to obtain the shareable preview URL.
- Open the copied link in an incognito/private window or on a phone to check real mobile rendering, since the in-editor mobile view isn't exact.
- Use this before finalizing merchandising changes on mobile-first shoppers, especially for product card layout and menu behavior.
- Re-verify the three-dot menu options and preview bar behavior in your Shopify version, as the UI changes.
Caveat: The published-theme copy method depends on browser right-click behavior and may shift with theme/Shopify updates.

Tags: store-setup, theme-editor, mobile-preview, qa, workflow
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Set brand colors once and connect theme colors to them via dynamic sources
Use when: Setting up theme colors before launch, or rebranding, so a palette swap doesn't require hunting through every color field.
- Go to Shopify general settings and define your brand colors first (primary, accent, contrasting/secondary, light page, etc.).
- In the theme editor's Colors settings, click the dynamic-source icon on a color field (the icon that connects to a metafield) and pick from your saved brand colors instead of typing hex codes each time.
- Map the palette purposefully: text and headings to the primary brand color, links to an accent/contrasting color, product card sale badge to the accent color so it stands out.
- Set product card states: 'sale', 'sold out' and 'pre-order' badge colors should be chosen deliberately—if you don't need a given state (e.g. low inventory), skip changing it to save time.
- When you later change a brand color once at the brand-assets level, every theme field linked to it updates automatically—no field-by-field editing.
- Decide colors iteratively: it's hard to judge colors before seeing them on real content, so return to Colors settings after uploading images and sections; stay within your brand palette.
Caveat: The number and naming of color options varies by theme; more professional themes typically expose more options, some themes push choices down to section level instead.
Caveat: Dynamic source linking requires brand colors to be defined first.

Tags: store-setup, branding, colors, theme-editor, dynamic-sources, palette
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Configure buttons, background, header and section color schemes
Use when: Merchandising your storefront design, and planning how homepage sections will visually alternate (light/dark backgrounds) across the store.
- Define the primary button: choose background, hover background and text colors. This button appears across the store (e.g. Add to cart, checkout). Then define the secondary button (often white background with a border).
- Set the background: choose the full-store background color; keep it white for the shopper's ease of reading. Using an image as background is not recommended (you'd control repeat/tile options).
- Set header colors: background, text, main menu link color, hover color and the featured link color; you can also add a menu background color.
- Use image overlays (a transparent black layer over hero images) at adjustable opacity to make overlaid text pop; tune this after you upload real images rather than during initial setup.
- Build section color schemes: a scheme is a predefined combination of your brand colors (background, heading, text, links, plus primary/secondary button variations) so you can alternate between sections without re-picking colors.
- Create at least two schemes (e.g. white background with primary text; a bold/beige background with dark-blue text) and apply them to alternating sections so the design doesn't feel monotonous.
- Pick colors you can live with, then adjust after previewing; if you don't use a feature (e.g. low-inventory label), don't spend time styling it.
Caveat: Color schemes are theme-dependent; some themes don't offer them and only expose colors at the section or theme-settings level.
Caveat: Overlay opacity and scheme choices should be judged against actual imagery, not the placeholder content.

Tags: store-setup, theme-editor, colors, buttons, layout, merchandising
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Set typography, sizes and button shapes from theme settings
Use when: Setting up theme typography and button styling before launch, or tuning readability after seeing the store on desktop and mobile.
- Choose fonts from Shopify's font library so your font is guaranteed available without custom coding; this is the recommended approach over uploading custom fonts.
- Set the heading font (with options like all-caps and heading letter spacing), then text/button text, navigation text and store-name text separately.
- After selecting a font, check the style dropdown for available weights/styles and pick the one you want.
- Use the Sizes settings to adjust heading size, base size, navigation size and store-name size to get a readable hierarchy.
- Choose button text case (normal or all caps) and corner rounding (slightly rounded to fully rounded) if the theme exposes it—nicer than custom CSS to achieve rounded buttons.
- Verify typography and button choices on mobile preview and a real phone, since sizes read differently at small widths.
- Expect these settings to differ per theme but follow the same logic; search for the relevant setting if it isn't where expected.
Caveat: Available typography and button-shape options vary by theme; some require custom CSS.
Caveat: Custom-code solutions carry more risk than the built-in settings.

Tags: store-setup, typography, theme-editor, branding, buttons
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Customize product cards: image shape, cropping, alignment and mobile per-row count
Use when: Setting up how products appear on homepage and collection listings; fixing a listing where mixed square/portrait product images look inconsistent.
- Decide image shape (portrait, square, landscape). If you upload images pre-sized to the shape you want, the card looks clean; if you mix square and portrait/landscape images, most themes will crop to fill the required shape, which can cut products awkwardly.
- If the theme offers a 'don't crop' option, you can avoid cropping, but it's usually not practical because card sizes become mismatched; the better fix is uploading correctly sized images from the start.
- When cropping, set the image alignment (top/middle/bottom) to control which part of the image is retained—useful when a crop cuts off the product.
- Set image alignment (for example top) and text alignment (left/center/right) for the card text; center is a common choice.
- Keep mobile products per row at two for a more user-friendly browse experience; one per row is an option but less efficient.
- Enable additional images on hover where the theme supports it—a nice way to show a second shot without clicking.
- Choose quick-buy behavior: as a button or 'whole product' (clicking the card opens the product so customers can buy there); optionally allow app blocks (e.g. review ratings) and subscription options inside quick buy.
- Set overlay label position (top-right/left recommended) and show the sale reduction by percent or value; these options vary by theme.
Caveat: Cropping behavior and the availability of a 'no crop' option vary by theme; many themes crop automatically without offering a choice.
Caveat: Some card features (subtitles, swatches, app blocks in quick buy) depend on theme and installed apps.

Tags: store-setup, product-card, merchandising, product-page, mobile, theme-editor
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Set up header: announcement bar, sticky header and menus
Use when: Building the site-wide header that shoppers see on every page, including promo messaging and navigation.
- Announcement bar: add up to about three announcements (typically the theme limit). Type plain messages like free shipping, optionally link them (e.g. to your shipping policy) and add a countdown timer with an end date for promos.
- Use section-level vs block-level settings correctly: clicking the section changes section settings; clicking a block changes that block's settings. Style individual messages or let them inherit the section style.
- Add a country/region selector if you sell in multiple markets so shoppers can switch location and see products/pricing/shipping for their region; add a language selector if you offer multiple languages.
- Header: set logo width and mobile logo dimensions, and enable a sticky header so navigation follows as shoppers scroll (recommended).
- Optionally enable a transparent header (useful over a hero image) with a separate logo for the transparent state, but decide based on whether your first image suits it.
- Create the menu in the Shopify backend under Content > Menus, then link it in the header's Navigation setting; understand that a '#' prefix makes an item non-clickable, while linking to Products makes it link to all products.
- Keep the header simple: adding sections in the header group makes them appear on every page, which clutters navigation. Use Section settings to fine-tune.
Caveat: Announcement count is theme-limited (commonly three).
Caveat: Country/language selector usefulness depends on markets/languages actually configured.
Caveat: Sticky and transparent header options vary by theme.

Tags: store-setup, header, navigation, menus, announcement-bar, localization
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Build multi-level and mega menus that mirror how shoppers think
Use when: Designing site navigation and collection hierarchy to help different shopper intents find products quickly.
- Decide your top-level split by mental model. For activewear, a layered structure could be Shop > Clothes (with leggings, bras, jumpsuits) and Shop > Accessories (with bottle, mat), plus a second angle like Shop by Activity (yoga, pilates).
- Deliberately allow the same products to appear in multiple collections, because different shoppers search differently: some look for 'yoga leggings' specifically; others just want general activewear. Give each intent a path.
- Draw structure from a reference site's navigation (the presenter cites Lululemon): sports-based browsing, plus Men/Women browsing, so shoppers can enter from whichever angle fits them.
- Make second- and third-level items non-clickable if you don't yet have a collection for them, or make them clickable by creating a collection that includes all relevant products (e.g. a 'clothes' collection containing all clothes sub-collections).
- Feature a specific link (e.g. Leggings, or a sale/outlet collection) with a distinct featured color to highlight it—useful for promotions.
- Optionally use a different, simpler menu for mobile, and add theme-specific menu promotions (wide or small) with images and a call to action; helpful for luxury niches. Avoid adding header sections beyond navigation and maybe a slim store-message bar.
- When done, link the new menu in the theme editor Navigation setting; the header updates.
Caveat: Menu promotion blocks and featured-link coloring are theme-dependent (Symmetry-specific in the example).
Caveat: Deep multi-level menus can complicate mobile navigation; consider a simplified mobile menu.

Tags: store-setup, navigation, menus, merchandising, collection-structure, mega-menu
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Configure cart behavior: drawer vs page and free shipping bar
Use when: Setting up cart experience before launch, and optimizing how customers proceed from product to checkout.
- In theme settings' Cart options, choose between 'drawer' and 'page'. Drawer opens a popup overlay; page sends the shopper to the cart page.
- Prefer the drawer: the presenter argues page cart forces shoppers to click back to keep browsing, making it worse for browsing flow. Confirm this against your own store's data rather than treating it as universal.
- Optionally add a free shipping bar in the cart drawer and customize its colors, so shoppers see progress toward free shipping.
- Test the actual add-to-cart flow via quick buy and normal product page to confirm the drawer/page setting applies consistently in your theme.
- Review cart-related theme settings for anything else (e.g. cart notes, upsell blocks) that the theme exposes, and skip settings you won't use.
Caveat: Drawer vs page preference is a stated opinion; some stores/traffic convert better on the cart page. Test rather than assume.
Caveat: Available cart settings vary by theme.

Tags: store-setup, cart, checkout, conversion-optimization, merchandising
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Use currency formats, advanced settings and custom CSS carefully
Use when: Tweaking minor store display details (price formatting, filter and link behavior) or applying small display overrides without editing theme code.
- Currency formats: adjust how prices appear on the store if needed; keep defaults if you're happy with standard formatting.
- Advanced settings: review options related to filters and links; defaults are generally fine and many themes won't expose these settings.
- Custom CSS at the theme level: use it to change the display of the store globally (font styles, sizes, etc.) rather than editing theme base files—this is lighter-weight than editing theme files and lower risk because the editor CSS overrides theme code.
- Note there is also custom CSS at the section level for per-section overrides; choose the right scope for your change.
- If you're not familiar with CSS, skip this section—it's optional and everything works without it.
Caveat: Custom CSS is for those comfortable with it; misuse can produce broken displays.
Caveat: Pricing changes and formatting can have tax/legal implications depending on your markets—confirm before pushing live.

Tags: store-setup, pricing, custom-css, theme-editor, localization
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Use theme style presets as a starting point
Use when: Starting a new theme setup when you want a faster starting point and are willing to replace most section content anyway.
- In the theme editor, open the Theme style settings, which lets you switch between different pre-built demo styles.
- Review the demos and pick the one whose layout most resembles what you want your store to look like.
- Use it as a starting point, then customize sections and content as usual.
- Note that if you plan to replace most sections and content anyway, switching styles may not save much—many users keep the style they started with.
- After applying, review your color schemes and typography settings since presets can set defaults there.
Caveat: Switching styles affects many theme settings; verify your brand colors and typography survive the switch.

Tags: store-setup, theme-editor, theme-style, templates
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Build the footer with link lists, blocks and policies
Use when: Building site-wide secondary navigation and policy links at launch, and deciding whether to include a newsletter signup in the footer.
- Set footer background and text/heading colors in the theme settings' Colors section first; footer colors are global.
- In the Footer group, click the footer section to see its settings, then add blocks: Text (with logo), Link list and Newsletter.
- For each link list, create the menu in the Shopify backend under Content > Menus (e.g. Quick Links, Customer Support) and link it here; you can have multiple footer menus for different purposes.
- Generate your store policies in Settings > Policies (e.g. Terms of Service, Shipping Policy) using the provided templates, then link to those pages from a footer link list; read over any generated template before publishing.
- Consider hiding the footer newsletter block if you already capture emails via popups, or keep it if you want the footer as an additional capture point.
- Avoid adding unnecessary sections (like a scrolling banner) inside the footer group, since anything in header/footer/overlay groups appears on every page—keep the footer focused on links and policies.
Caveat: Footer blocks available vary by theme.
Caveat: Newsletter in footer may be redundant if you use popups—decide based on your email capture strategy.

Tags: store-setup, footer, navigation, menus, policies, retention, email-capture
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Build footer policy and support menus before linking them in the theme
Use when: Setting up the store footer so policy, contact and support pages are reachable from every page of the storefront.
- Generate every required policy in the Shopify admin under Settings > Policies (terms of service, refund, privacy, shipping). Insert the template for each, review and edit the text so it matches your store, then click Publish — unpublished policies have no URL to link to.
- Create the pages you want to link: go to Online Store > Pages and add at least an About Us page (and a contact/support page if the theme's default contact page isn't enough). Save without styling; edit the copy later.
- Go to Online Store > Navigation > Menus and create separate menus rather than one long list: for example 'Helpful Links' containing all policies, and 'Quick Links' containing About Us, Contact and support pages. This mirrors how larger retailers split footer navigation into services / help / about columns.
- Return to the theme editor, open the footer section, and point each Links block at one of the menus you created. Use the plus between footer blocks to add additional link-list blocks, then rename each block heading (e.g. 'Support') so customers can scan them.
- Optionally hide the newsletter block in the footer since popups already capture signups; keep it if the footer is your only email capture point.
Caveat: Menu contents are shared across all pages, so any change to a footer menu updates sitewide — double-check links after editing.
Caveat: The available footer blocks and their naming differ by theme; check the block types your theme actually exposes.

Tags: store-setup, navigation, footer, policies, theme-editor, customer-support
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Choose theme sections by first checking the available section library
Use when: Selecting or trialling a Shopify theme, or planning which homepage/PDP/collection sections your store will need.
- In the theme editor, hover between two existing sections, click the plus icon and browse the complete list of available sections, grouped by type (banners, collections, forms, info, product lists, etc.).
- Note that the default homepage sections a theme ships with are only a subset — you can remove them and add any other available section to any page.
- Map your niche requirements against that list before buying the theme. Example: a cosmetics brand needing a before/after gallery must verify the theme offers such a section, since it can't be added later if it doesn't exist.
- Confirm which section types are universal vs theme-specific: banners, collection list and featured collection are near-universal, while logo list, multicolumn, testimonials and subcollection blocks vary by theme.
- If the exact section is missing, look for generic substitutes — a multicolumn or column block that supports an image, text and link can stand in for a logo list.
Caveat: Reconciling this check against the theme store preview is faster than rebuilding later; section availability is a hard constraint, not a styling preference.

Tags: store-setup, theme-editor, sections, product-page, collection-page, homepage
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Assemble the homepage in a deliberate section order
Use when: Designing or rebuilding the store homepage structure after the header and footer are set.
- Start with a slideshow or background video as the first banner. Use it to state what you sell, announce a new collection or drop, and link the image or button directly to that collection — this is the source's recommended way to open a homepage.
- Keep the hero simple: one image or video, or at most two to three slides. Use a landscape image for desktop, and upload a separate mobile image if the theme allows it rather than accepting a bad crop.
- Follow the hero with a USP or logo-list section: each logo block carries one unique selling proposition (image, title, link). The same section type can show certifications or press logos.
- Add a featured-collection section for your bestsellers. The source's stated position is that bestsellers are bestsellers for a reason, so showing them on the homepage is always recommended.
- Continue with collection list, image-with-text linking to the About page, and a testimonial section populated with the strongest real reviews and optional customer photos.
- Add remaining sections only as needed (blog, rich text) and delete the theme's default filler — a shorter, intentional homepage is preferred over keeping everything the theme shipped.
Caveat: The recommended section sequence is the presenter's design opinion, not a tested universal rule; adapt to your catalogue and traffic source.
Caveat: Testimonial sections can also come from an app via app blocks; the theme's built-in section just avoids the dependency.

Tags: store-setup, homepage, theme-editor, merchandising, sections, social-proof, conversion-optimization
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Set hero slideshow height and focal point to prevent bad crops
Use when: Configuring a homepage hero slideshow or banner section where images crop awkwardly across devices.
- Click the slideshow section (not the individual slide) to reach its general settings, then choose a height mode: full screen, adapt to first image, or fixed height.
- Prefer 'adapt to first image' if you uploaded images at the correct dimensions — this shows the full image without cropping.
- If you need a consistent band instead, use fixed height. The source's working example used around 600px on both desktop and mobile; treat that number as a starting point, not a benchmark, and check both viewports.
- For images that still crop badly, open the image in the editor and set the focal point on the part that must survive cropping (e.g. a model's face). The theme then crops around that point.
- Set a separate mobile image where the theme supports it, and give each slide a full-slide link as an alternative to a button if you don't want a visible CTA.
- Check the mobile preview after each change; text-below-image on mobile is discouraged when a dedicated mobile image is available.
Caveat: Fixed-height values and the availability of mobile-specific images, focal points and text-below settings vary by theme; verify in your theme's editor.

Tags: store-setup, homepage, hero, theme-editor, mobile-optimization, creative-strategy
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Use duplicate and copy-paste to build section sets quickly and consistently
Use when: Building repetitive section structures such as logo lists, USP rows or cross-page content bands in the theme editor.
- Set the first block up completely — including image width — then use Duplicate to create siblings. Duplicated blocks inherit the same dimensions, so you only swap the image/text instead of resizing each one; the source explicitly regrets resizing every logo individually.
- Reorder blocks or sections by hovering and dragging them to the new position, including dragging a section to a different point in the page.
- To move a section to another page, select it and use Copy, then navigate to the target page and use Paste (or Paste after) — copied sections can be pasted on any Shopify page.
- Blocks can only be pasted into a section type that supports that block type, so keep whole reusable layouts at section level.
- Edit block text either through the settings panel or by turning on direct editing and double-clicking the text on the canvas.
Caveat: Section copy/paste between pages is a newer Shopify editor capability; interface details may change, so verify it exists in your editor version.

Tags: store-setup, theme-editor, sections, workflow, homepage
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Create a bestsellers collection with tags and feature it
Use when: Adding a bestsellers or curated homepage product row when the store has no existing bestsellers collection.
- Decide which products to feature, then tag them (e.g. tag equal to 'bestsellers') using Select all > Bulk edit > add tag in the products list.
- Go to Products > Collections and create a collection named 'bestsellers' with an automated condition of tag equals bestsellers, then save.
- In the theme editor, add a Featured Collection section and select the bestsellers collection. Some themes let you select individual products instead of a collection; this workflow assumes collection-only selection.
- Where the theme supports it, change the section's colour scheme to differentiate the band from adjacent sections and check badge styling in each scheme.
- Later, maintain the tag as your real bestsellers change — the section updates automatically because the collection is condition-based.
Caveat: The source recommends showing bestsellers on the homepage; if you have little or no sales data, define 'bestseller' by your own judgement or omit the label rather than implying sales volume you don't have.

Tags: store-setup, collections, merchandising, homepage, theme-editor, tagging
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Build automated collections with AND-style tag conditions
Use when: Building a parent category (e.g. all activewear) that should gather several product types tagged separately.
- In Products > Collections, create a new collection and choose automated conditions rather than manual selection.
- Decide whether products must match ALL conditions or ANY condition. To pool leggings, bras and overalls into one activewear collection, set 'any condition' with separate rules: tag equals leggings, tag equals bra, tag equals overall.
- Save and verify the product count matches expectations; the collection updates automatically as tags change.
- Keep tag values consistent in the product data or products will silently fall out of the collection.
Caveat: Using 'any condition' is the opposite of what you'd want for narrowing rules; mixing ALL and ANY logic carelessly produces either over-broad or empty collections.

Tags: store-setup, collections, tagging, catalog-management
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Configure collection filters using Shopify Search & Discovery
Use when: Setting up collection page filtering so shoppers can narrow a large catalogue by type, size, colour or price.
- In Shopify admin, open the Search & Discovery app > Filters and add the filters you want (standard fields such as product type and size, plus custom ones like fabric or colour).
- Fill in the underlying product data for filters to return results. A filter with only one value in the admin usually means you haven't entered product type (or the relevant field) on the other products — bulk-edit products to populate it.
- Write values consistently: 'legging' and 'leggings' create two separate filter options, so standardise the wording across products.
- Order filters in the app (e.g. product type before fabric, size where it fits logically) and save; order is controlled from the app, not the theme.
- In the theme editor's collection template, review theme-level filter settings — some themes render certain filters as buttons (e.g. sizes) and may support colour swatches natively.
Caveat: Filter display options vary by theme; the app determines which filters exist and their order, the theme determines how they render.
Caveat: Price is available as a filter but the source's example set also leaned on product data quality, which is the usual failure point.

Tags: store-setup, collection-page, filters, search-and-discovery, catalog-management, conversion-optimization
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Turn on colour swatches with defined colours or variant images
Use when: Collection-page merchandising when products come in multiple colours but the cards show no colour indication.
- In the theme editor, open the product card/swatch settings inside the collection template (or theme settings > swatches) and enable swatches.
- For hex-based swatches: select the colour-list option, then define each variant colour name and its hex code (look the code up by searching e.g. 'red hex'). The swatch appears once the name matches the variant value.
- For image swatches: select the variant-image option so the theme pulls the actual variant image, which the source preferred for its store.
- For custom swatch graphics (e.g. patterns rather than flat colours), upload an image named exactly after the variant value with the correct extension (e.g. red.png) and the theme will use it in place of the colour.
- Save and open the live/collection preview to confirm swatches appear under the product cards.
Caveat: Swatch configuration differs across themes, though all common themes support swatches; if they don't show, a setting is usually unset rather than unsupported.
Caveat: Variant naming must match swatch names exactly for the association to work.

Tags: store-setup, collection-page, colour-swatches, variants, theme-editor, merchandising
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Work on the default collection template first, then branch to custom templates
Use when: Deciding between editing the shared default collection layout and creating per-collection layouts.
- Open the theme editor's Collections section; the Default collection template applies to every collection assigned to it (the source observed six collections sharing one template).
- Configure the shared settings there: show/hide collection title and image, heading image height, overlay style, show/hide description, products per page, products per row, and whether to show vendor and product count.
- Add the description and collection image if you care about SEO, since these feed the collection page content.
- Set the default sort (bestselling, alphabetical, price low to high) in the collection section settings.
- Where a collection needs different content or extra sections, click Create template in the Collections area, name it after the collection (e.g. 'activewear'), and build its sections.
- Assign the template per collection in the admin; if the theme isn't published yet, template assignment may not be visible, so plan to assign after publishing.
Caveat: Changes to the default template affect every collection assigned to it — a common source of unintended sitewide edits.
Caveat: Template assignment options depend on whether the theme is published.

Tags: store-setup, collection-page, theme-editor, templates, merchandising
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Add a visual subcollection row with a multicolumn section
Use when: Large catalogues where a parent collection needs to route shoppers into leggings/bras/overalls-style subsections.
- Create a dedicated collection template for the parent collection and preview that collection against it.
- Add a multicolumn section above the product grid, delete all but one block, then fully configure the first: image, title (e.g. Leggings) and a link to that subcollection.
- Set the media width to a consistent, small size on the first block, then Duplicate it for each remaining subcollection and swap the image, title and link — duplicating preserves the dimensions.
- Hide the parent collection's own title and product count in the template settings so the subcollection row reads as the page's primary navigation.
- Optionally add a rich-text section above the row with an instruction such as 'select by product type' and its own heading removed, to avoid repeating the collection title.
- Use product images with transparent backgrounds where possible for a cleaner subcollection row, as seen on reference stores using the same theme.
Caveat: Native subcollection blocks exist in some themes but not all; the multicolumn approach is the portable fallback.
Caveat: This template must then be assigned to the specific collection in the admin once the theme is published.

Tags: store-setup, collection-page, navigation, templates, merchandising, theme-editor
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Use collection metafields to vary content inside a shared collection template
Use when: Running one collection layout with a promotion or lookbook band whose content must differ per collection.
- Decide which section elements need to vary (image, heading, body text, button link). Anything left static will show the same on every collection using that template.
- In Settings > Metafields and metaobjects > Collections, add definitions: an image-type field (e.g. 'promotion section image'), a single-line text field for the heading, a rich-text field for the body, and a URL-type field for the button link.
- In the theme editor, click the section element and use 'connect dynamic source' to bind it to the metafield — the section field only accepts metafield types it supports (an image field won't accept a text metafield, and a link field may require the URL type).
- Fill the metafields per collection in the admin (individually or via bulk edit with the metafield columns exposed), then save.
- Preview two different collections sharing the template to confirm the layout is identical but the content changes; empty metafields render as nothing.
Caveat: If a metafield doesn't appear as a selectable dynamic source, the defined type is wrong for that field — redefine it as URL vs link, single-line vs rich text, etc.
Caveat: Use templates, not metafields, when the whole layout must differ; metafields are for dynamic content within a shared layout.
Caveat: Metafield linking is easier once the theme is published and the collection admin fields are visible.

Tags: store-setup, collection-page, metafields, templates, theme-editor, merchandising
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Research competitor PDPs and reviews before designing your product page
Use when: Planning a product page layout or rewriting PDP content, especially before building a new template.
- List the sections and information blocks you plan to include before touching the theme editor.
- Audit competitor stores in your niche — prioritise large brands, on the reasoning that they have tested their PDP structures extensively and their choices indicate what customers care about.
- Read reviews on competitor sites and on Amazon to extract the specific questions, hesitations and objections customers raise before buying.
- Translate each objection into a PDP element. The source's example: a client selling a premium pasta knew taste was the core objection, so the page needed reviews and people visibly tasting and endorsing the product.
- Handle the price objection the same way: the pasta was roughly three times the price of supermarket pasta, so the page had to prove health and quality benefits to justify it.
Caveat: Competitor structure is a research input, not a template to copy wholesale; and the pasta example is an illustration of the method, not a measured result.

Tags: product-page, customer-research, positioning, reviews, conversion-optimization, product-selection
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Use Sidekick to make editor changes — with eyes open about scope
Use when: Making quick visual tweaks to a homepage or PDP section when you're not yet comfortable with theme settings.
- Open the theme editor, select the section you want to change, and use the 'ask for changes' option to describe the change (e.g. make the button text red and 25% larger, or restyle a grid as vintage).
- Review the result on the canvas; if you don't like it, keep asking for further adjustments or use the full chat to see and redo prior changes.
- After any Sidekick change, check other sections of the store that share the same setting — for example, a heading colour change may propagate to headings everywhere depending on how the theme defines them.
- For anything structural or precise, edit the theme settings yourself; the source's view is that manual theme control is still preferable, with Sidekick as a beginner aid.
Caveat: Sidekick updates theme settings, not code, so its reach is limited by how the theme shares settings across sections.
Caveat: This feature evolves quickly — verify its current behaviour and options in your editor.

Tags: store-setup, theme-editor, sidekick, ai-tools, workflow
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Mine competitor PDPs and reviews for objections
Use when: Before writing or redesigning any product page, to decide what proof and information to include.
- Open 3–5 competitor product pages in your niche; established brands have tested their layout, so treat their structure as evidence of what buyers care about.
- Note which modules they prioritize above the fold: benefits, size guides, comparison tables, reviews, ingredient lists.
- Read reviews and Q&A on competitor sites and on Amazon for the same or substitute products; log the questions, hesitations and objections buyers actually voice.
- Convert each objection into a PDP requirement: the pasta example — taste was the #1 worry, so the page needed reviews plus people visibly eating and endorsing the pasta.
- For a premium-priced claim (the pasta was 3x store price), add numerical and scientific facts that substantiate the 'healthier/better' claim directly on the page, so the answer is present before the customer asks.
- Tune the depth to your niche: low-objection products (e.g. active wear) need size charts, fabric and durability detail; high-solution products need taste/health/claims proof.
Caveat: Competitor pages show what works for them, not guaranteed results for you; validate with your own reviews and customer messages.
Caveat: Review-mining is qualitative input, not a benchmark.

Tags: store-setup, product-page, customer-research, conversion-optimization, positioning, competitive-research
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Answer objections in proportion to price and complexity
Use when: Deciding how much content a specific product page needs during PDP build-out.
- List every objection a buyer could raise: taste, sizing, durability, ethics claims, comfort, shipping, returns.
- Match each objection to a proof format — reviews and user videos for subjective claims (taste, comfort), spec sheets and certifications for technical claims, comparison tables for price objections.
- Back abstract claims with evidence: if you say a fabric stretches better, cite the certification; if you say the legging prevents camel toe, show women saying so or photos demonstrating it.
- If positioning the brand as a new invention or as sustainable, explain why the claim is true and how the product differs, rather than just stating it.
- Publish a detailed size chart for any apparel product — sizing is the biggest hesitation point in that niche.
- Add fabric and care information (material benefits, washing instructions, support level for bras and leggings) so buyers don't fear the item degrading.
- Rule of thumb from the source: the more complicated and the more expensive the product, the more detailed the product page should be.
Caveat: Content depth is a source heuristic, not a tested threshold; a cheap, familiar product does not need a dense page.

Tags: store-setup, product-page, conversion-optimization, positioning, objection-handling
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Repeat key information in multiple formats on the PDP
Use when: Designing PDP layout and section order after deciding what information to include.
- Pick the content customers most need to believe (ingredients, benefits, claims) and place it in at least two different formats.
- Example: a lip balm PDP can have an ingredients tab plus a separate section showing the product with each ingredient and its benefit mapped out.
- Use the range of formats — charts, infographics, images, comparison tables — to make a long page more digestible.
- Check how established supplement brands do this: benefit images sit inside the gallery while benefit sections repeat further down the page, so the message is caught whether the visitor scrolls or not.
- Treat the PDP as iteratively improvable: plan to revisit and update product pages over time to keep lifting store conversion rate, rather than building once.
Caveat: Repetition is about reinforcing the same claims, not padding with unrelated filler.
Caveat: Conversion-rate improvement over time is the source's expectation, not a guaranteed outcome.

Tags: store-setup, product-page, conversion-optimization, merchandising, content-design
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Decide product page templates by category vs. meta fields for per-product content
Use when: Setting up a Shopify product page structure across a catalog with multiple product types.
- Build the default product template first and put everything common to all products there (e.g. the benefit blocks moved above buy buttons, dividers, description placement).
- Create additional templates only where layout genuinely differs by category — e.g. one for bras and leggings, one for accessories — since templates copy from the default so you only adjust the differences.
- Use meta fields when the same block must hold different content per product: the 'USP/benefits' rich-text meta field, connected as a dynamic source in the theme editor, shows each product's own benefits and stays empty for products where it wasn't filled.
- Use a page-type meta field for the size chart when charts differ per product but you want to reuse a layout across categories; a single linked page works when every product shares the same chart.
- Assign templates from the product's admin settings under Template once the theme is published.
- Stay disciplined: keep templates for product categories and meta fields for per-product variation, rather than multiplying templates unnecessarily.
Caveat: Templates can only be created/assigned on a published theme or a version of the same theme.
Caveat: Theme editor labels and options change between themes — verify in your current theme.
Caveat: Meta field types must match the block type used in the theme (rich text vs. page).

Tags: store-setup, product-page, metafields, shopify-theme, merchandising
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Configure Shopify product page section settings
Use when: Initial setup of the product page in the theme editor on Shopify.
- Decide on 'first available variant selected' — the source usually keeps it on, but turns it off when worried customers will add to cart without consciously picking size/color and then request changes.
- Hide the vendor block unless you stock multiple brands, in which case showing the brand helps buyers.
- Keep the sticky add-to-cart, especially on mobile — it is user-friendly and eases navigation; you can choose position (center/left/right) and button style.
- Breadcrumbs are generally recommended and can be kept for SEO.
- Keep image zoom on if you have good photos, since detail viewing helps buyers.
- In media settings choose image size and layout: enlarged images suit jewelry/luxury; smaller or collage layouts suit stores that want more images visible, and left-side thumbnails can be awkward if the media isn't scrollable in that theme.
- Enable 'show all text over image' to display each image's alt text, which you can enter per image in the product admin.
Caveat: Available settings differ by theme — check your theme's options.
Caveat: Test layouts on mobile; the source found some thumbnail arrangements looked broken.
Caveat: Alt-text overlays are cosmetic here, not a substitute for real alt-text SEO.

Tags: store-setup, product-page, shopify-theme, conversion-optimization, mobile
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Group variant images by color using theme logic
Use when: Setting up product media for a product sold in multiple colors.
- Check whether your theme supports variant media grouping before buying it; most professional themes do, and some third-party Shopify apps can add it if not.
- If the theme offers an enable option (as in the Symmetry-style editor), switch it on so selecting red shows only red images and selecting blue shows only blue.
- Alternative theme logic: name each image's alt text with the variant name (e.g. 'red'), and the theme groups images by that tag.
- In either case order the images correctly in the admin — all first-color images, then all second-color images — or grouping will misbehave.
- If the demo store shows grouping but you can't find the setting, check the theme's help center article.
Caveat: These are the two logics the source observed; your theme may differ.
Caveat: Grouping behavior must be verified in the theme editor after saving.

Tags: store-setup, product-page, shopify-theme, merchandising, media
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Place short benefit bullets and description above the buy button
Use when: Structuring the above-the-fold content of a product page.
- Move the short description to sit above the buy buttons rather than below the media, and remove the default below-media description placement.
- If the product has clear benefits or is a solution product, add 3–4 benefit bullets near the buy button so the value is visible before scrolling.
- For per-product benefits, create a rich-text meta field (e.g. 'USP/benefits'), fill it on each product, then in the theme editor connect that block to the meta field as a dynamic source.
- Format meta field content consistently (the source used heading-5 for benefit lines) so it renders cleanly.
- Delete blocks you don't want (e.g. vendor) and use dividers to separate groups.
Caveat: The source prefers a small description here; don't duplicate the full long description above the fold.
Caveat: Meta field blocks render empty on products where the field wasn't filled — fill it for every product using that template.

Tags: store-setup, product-page, conversion-optimization, metafields, copywriting
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Deliver sizing confidence with a size chart page or meta field
Use when: Setting up apparel or any product where buyers hesitate about which size to pick.
- In the theme editor, enable the size guide option and select a page that contains the chart.
- Build the chart in Online Store > Pages, make the page visible, save, then refresh the theme editor before it can be selected.
- Build the table inside the page editor; optionally copy the HTML via 'show HTML code' and have a tool rewrite it for a nicer table, then paste it back.
- If charts differ per product (e.g. leggings vs. bras), create a page-type meta field ('size chart page'), fill it per product, and link the size guide to that meta field instead of a single page.
- Remember to publish the page — an unpublished chart page won't appear.
- In the source's active wear niche, a detailed size chart is the single most important PDP element because sizing is the biggest hesitation.
Caveat: Theme handling of size charts varies: some offer a built-in option, others need a popup or collapsible tab.
Caveat: Products where the meta field is empty will show no size guide.

Tags: store-setup, product-page, size-guide, metafields, apparel, conversion-optimization
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Use collapsible tabs for FAQ-type PDP content
Use when: Adding fitting, care, shipping and returns information to a product page.
- Add a collapsible-tab block for each recurring question area: description, fit, shipping and returns, care guide.
- For the description tab, link the content to the product description rather than retyping it.
- For shipping, write a short summary in the tab (e.g. free shipping over $100, 30-day money-back guarantee) and hyperlink to the full shipping/returns page — a summary plus link is more practical than pasting the whole policy.
- Publish any linked policy page first, otherwise the link won't resolve.
- If the content is identical across all products (e.g. a universal care guide), type it directly; if it varies per product, use a meta field to make the tab dynamic.
- Add small icons per tab (delivery, awards, care) where the theme supports them, and reorder tabs as needed.
Caveat: The source's summary-plus-link shipping approach is a preference, not a rule.
Caveat: Icon options and tab behavior depend on the theme.

Tags: store-setup, product-page, shipping, returns, conversion-optimization, merchandising
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Show fit/true-to-size rating when the theme supports it
Use when: Apparel PDPs where buyers are unsure whether to size up or down.
- Check if your theme offers a fit rating block (the source cites Symmetry's fit feature, similar to what Adidas uses).
- Display how true-to-size the item runs so buyers can choose confidently.
- Make the rating dynamic per product using meta fields so each product carries its own value rather than one global setting.
- Use the block for other product-specific ratings if useful, but the fit use case is the standard one.
Caveat: Not available in every theme; intended as a fashion/apparel feature.

Tags: store-setup, product-page, size-guide, apparel, metafields
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Choose between Add to cart and Buy it now
Use when: Configuring the buy buttons on a Shopify product page.
- Note that Buy it now is a Shopify dynamic button that only appears when Shopify Payments is activated.
- Keep it when customers are likely to buy a single product; hide it when customers typically add multiple products to the cart and should go through the cart instead.
- Understand the dynamic behavior: with the button kept and Shopify Payments on, it displays the wallet the customer uses most (Apple Pay, Google Pay, PayPal) rather than literally 'buy it now'.
- Hide the quantity selector if you believe no customer will buy two units at once — it saves space.
Caveat: Buy it now requires Shopify Payments; behavior depends on the shopper's saved wallets.
Caveat: These are the source's situational preferences, not universal rules.

Tags: store-setup, product-page, checkout, shopify-payments, cart
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Set complimentary products to lift average order value
Use when: Configuring the complimentary products section on a product page to raise AOV.
- Use the analogy of buying an iPad and being shown the case and screen protector: recommend items the buyer needs for the purchase they're already making, so they feel grateful rather than sold to.
- For a legging, set the matching bra or hoodie as the complimentary product — purchases that naturally pair with the original.
- In the Search & Discovery app, open the product recommendation section and manually choose the complimentary product(s) for that specific product, then save.
- By default Shopify populates 'related products' automatically; the complimentary slot stays empty unless you select products yourself.
- Keep it tight: recommend only the one or two products that make the most sense rather than overwhelming the buyer with ten options.
Caveat: Related products are auto-generated and editable; complimentary products require manual selection per product.
Caveat: This is an AOV tactic based on the source's reasoning, not a measured result.

Tags: store-setup, product-page, average-order-value, product-recommendations, merchandising
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Add brand-trust and feature sections below the buy area
Use when: Building the lower half of a product page after the core buy section is finished.
- Copy an existing brand/USP section from the homepage into the product page to build trust quickly — sections can be copied between pages in seconds.
- Adjust the color scheme so the pasted section contrasts appropriately with the product page.
- Add a feature-highlight section such as a hotspot block: choose an image (e.g. a woman training), then place hotspots that name and describe individual product features.
- Make section content dynamic per product using meta fields — the image, the content and even individual hotspot text can all pull from meta fields.
- Continue adding sections (video, text, etc.) with the same method used on the homepage until the page covers everything you decided in the information phase.
Caveat: Some sections (e.g. hotspot/highlight) don't exist in every theme.
Caveat: Copied sections may need their settings rebuilt per page.

Tags: store-setup, product-page, brand-positioning, metafields, merchandising
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Generate missing PDP sections with Shopify's AI section tool
Use when: When your theme library is missing a section you need on a product page (comparison table, custom layout).
- Buying a theme unlocks Shopify's AI section generation; open the theme editor, click Add section and choose Generate.
- Describe the section you want (e.g. 'create a comparison table') — the tool builds it with editable options you can then modify.
- If the first result isn't right, keep refining in the same session: ask for more customizability, color changes, icons, and so on; you can iterate until you save.
- Write detailed prompts; results correlate strongly with prompt quality, and an unreliable result usually means the request wasn't translated clearly.
- A practical tactic from the source: ask a general AI assistant to write the prompt for you, then paste it in.
- Once created, the section is reusable anywhere via Add section > AI generated sections.
Caveat: The source calls the tool unpredictable — sometimes perfect on the first try, sometimes slow to tweak.
Caveat: Generated sections can have bugs on some devices, and the source does not recommend it for total beginners.
Caveat: Safer to pick a theme that already includes most sections you need.

Tags: store-setup, product-page, shopify-theme, ai-tools, comparison-table
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Design the collections list ('all collections') page
Use when: Setting up navigation for a store with many collections or categories.
- By default the theme lists all collections; you can hide that and design the page yourself.
- Add collection-list sections and group collections by family — e.g. one section for active wear (bras, leggings, overall) and a separate section for accessories.
- Set the number of collections per row (e.g. three) to control density.
- For large catalogs, model the pattern from stores that group sub-collections into themed blocks (dog apparel, dog accessories, everyday essentials, health and care).
- Link to this page from the menu or homepage so shoppers can browse the full collection structure.
Caveat: Layout options depend on the theme's collection-list section.

Tags: store-setup, collections, navigation, merchandising, catalog-organization
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Keep the cart page and cart drawer simple
Use when: Reviewing the cart page or cart drawer in theme settings.
- Decide whether your theme uses a cart drawer or a cart page — customers land there after adding an item or when clicking the cart icon.
- Optionally edit the default cart copy and adjust settings by clicking the cart section in the theme editor.
- You can add product recommendations or app blocks here, but the source recommends keeping the cart simple.
- Expect theme-dependent options; the logic is broadly consistent across themes.
Caveat: The source's 'keep it simple' stance is a preference, not a tested rule.

Tags: store-setup, cart, conversion-optimization, shopify-theme
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Build richer static pages with templates instead of plain text
Use when: Creating or upgrading About Us, story or other static content pages.
- A page with only text pasted into the admin renders as a plain static page.
- To design it, create a template for that page and build it with sections like any other page on the store: image-with-text-overlay for a brand image, rich text for the story, image-with-text blocks, scrolling panels, video-with-text.
- Fill content directly in the template sections; because static pages don't vary per product, meta fields are unnecessary here.
- Remove sections you don't need and flip image/text orientation for variety.
- Save the template, then go back to the page in the admin and assign the template from the template selector.
- Apply the same template logic to any other page you want to look designed rather than static.
Caveat: Templates must be assigned to the page after creation or the design won't appear.

Tags: store-setup, pages, shopify-theme, content-design, brand-story
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Organize content into multiple blog families
Use when: Setting up a store blog with more than one content theme (e.g. recipes vs. health facts for a grocery store).
- In Content > Blog posts, create a post, add content and an image, make it visible and save.
- In Manage blogs, rename or add blogs: the store has a default 'News' blog and you can add a second (e.g. 'Workout') so content families stay separate.
- Assign each post to the correct blog so you can link to one family in one menu spot and the other elsewhere.
- Configure the blog listing page separately from the post template: the blog page settings control whether posts show as a list or grid, image ratio, and whether author/date are hidden.
- Modify individual post layout by editing the post template in the theme, and link to a blog from Content > Menus (e.g. add Workout to the main menu).
Caveat: A blog or post that isn't published won't appear after linking.
Caveat: You may need to refresh the theme preview to see menu changes.

Tags: store-setup, blog, content-marketing, navigation, shopify-theme
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Customize search, password and error pages
Use when: Finishing theme setup after homepage, product, collection, cart and static pages.
- Search page: adjust settings and optionally add sections such as product recommendations to help shoppers who search within the store.
- Password protection page (coming-soon page): treat it as a normal page — it includes a submit form and password login; add sections and set a background image, then check text contrast against the new background.
- Error (404) page: the source advises not touching it.
- Work through each page systematically in the theme editor, using the same section-based building approach as other pages.
Caveat: The source explicitly recommends leaving the error page alone.
Caveat: Adding a background image can break text legibility if contrast isn't checked.

Tags: store-setup, shopify-theme, search, pre-launch, content-design
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Expect limited checkout customization outside Shopify Plus
Use when: Planning checkout or account-page changes on a standard Shopify plan.
- Recognize that Shopify locks the checkout page unless you are on Shopify Plus, so most layout and content changes are not possible on standard plans.
- What you can do on standard plans is limited: add apps to hide or show elements in checkout, such as payment gateways.
- Shopify has been expanding checkout flexibility over time (the source references blocks and flexible payments after recent upgrades), so verify the current options in your admin rather than relying on older limitations.
- Approach the checkout and customer account pages as configuration only, and invest layout effort on product, collection and landing pages instead.
Caveat: Checkout capabilities change frequently — always verify against Shopify's current documentation and your plan.
Caveat: The source notes these restrictions are improving, so the limitation described may already be partly outdated.

Tags: store-setup, checkout, shopify-plus, customer-accounts, platform-limits
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Locked Shopify Checkout: What You Can Adjust Without Plus
Use when: Deciding how much checkout customization to attempt on a standard (non-Plus) Shopify store before spending time or budget on it.
- Confirm your plan tier first: the source states that on any normal Shopify plan (anything except Shopify Plus) checkout customization is very limited.
- Work within the non-Plus options: add a checkout logo, logo size and alignment, background colors/images, accent colors for buttons and error messages, and pick one-page vs multi-step checkout (source recommends keeping one-page).
- Use payment-flexibility apps to show or hide a payment method by country or audience — e.g. make cash on delivery visible only in France while the rest of the world does not see it.
- Accept that adding checkout blocks, notes, upsells and cross-sells, or forcing dropdown city fields for cleaner shipping addresses, generally requires Shopify Plus or specific warehouse setups.
- Before promising a client or stakeholder a customized checkout flow, verify current plan entitlements — Shopify has expanded checkout abilities over time and continues to roll out changes.
- If your checkout requirements exceed non-Plus limits, evaluate whether a third-party app, an upgraded plan, or a redesigned pre-checkout page (cart or upsell page) is the better path.
- Treat the locked checkout as partly a security and familiarity feature: the source argues limited customization is what has kept the Shopify checkout trusted and instantly recognizable to buyers.
Caveat: Plan entitlements change frequently with Shopify releases (the source references Winter Edition promises of more checkout blocks) — always verify current capabilities in your admin.

Tags: store-setup, checkout, shopify, conversion-optimization, apps, payment-methods
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Configure Contact Method and Required Fields at Checkout
Use when: Setting up the checkout form fields in Shopify checkout settings for a new store or auditing an existing one for data capture.
- In checkout settings, set the customer contact method to email only rather than offering email-or-phone at the top of the form — the source prefers this so every buyer supplies an email.
- Collect the phone number later, in the shipping address section, and make it required there. This is especially important if you offer cash on delivery, because you need a reachable number.
- Keep last name as the only required name field; customers typically fill in first name anyway. Do not require company name unless the store is B2B.
- Leave address fields at Shopify's default settings unless your warehouse logistics require something different.
- Do not force account creation before checkout — the source states many customers dislike creating accounts and recommends keeping it open.
- If you use Shop Pay, decide whether to show the order-tracking link in the checkout; the source notes this option exists in the same settings area.
- Verify the current layout of these settings in your Shopify admin, since checkout settings screens change with platform updates.
Caveat: Requiring the phone number adds one more mandatory field — the source weighs this against the value of reaching COD customers and accepts the trade-off.

Tags: store-setup, checkout, customer-research, email-capture, payment-methods, shopify
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Separate Transactional Consent From Marketing Consent at Checkout
Use when: Deciding how to present email/SMS marketing opt-in at checkout, and which regions should have it pre-selected.
- Understand the distinction: order notifications are permitted for anyone who bought, but marketing emails require explicit (or, where legal) pre-selected consent. The source notes legal requirements, especially in Europe and the UK.
- Turn on the checkout subscribe checkbox that appears next to the email or phone field, and configure it separately for email and SMS.
- Decide pre-selected vs opt-in based on business maturity: the source recommends pre-selecting for new businesses (more subscribers, lower engagement) and leaving it unchecked for established stores with lots of traffic (fewer but more engaged subscribers).
- Use Shopify's per-country pre-selection setting: pre-select for the United States and other permitted regions, and leave it unchecked where pre-selection is not legal, such as parts of Europe and the UK.
- Assess the checkbox's visibility — the source notes it is small and easy to miss on the checkout page, which is why some merchants pre-select it.
- Only send marketing to people who consented; the source ties this to both legal compliance and better email performance (interested subscribers open more).
Caveat: Pre-selected consent rules vary by country and were described as changing — verify current legal requirements for your customer locations before enabling pre-selection.

Tags: store-setup, checkout, email-capture, retention, compliance, shopify
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Turn On Abandoned Checkout Recovery Emails
Use when: Setting up post-checkout-abandon recovery for a new store or deciding whether Shopify or an external ESP should own the flow.
- In checkout settings, turn on the abandoned checkout email; the source describes it as very important and a source of many recovered sales.
- Know what it does: once a shopper has entered their email in checkout, Shopify sends them a reminder that they left an item behind, based on your settings.
- If you already run an email marketing platform (the source names Omnisend and Klaviyo), you can leave Shopify's version off and build the abandoned checkout flow there instead — the source does this on its own store.
- If you start out without an ESP, simply enable Shopify's built-in version; in Shopify's marketing automations area, activate the 'recover abandoned checkout' automation.
- Do not confuse this with transactional notifications: order confirmation, order shipped and similar emails are pre-made Shopify templates controlled by Shopify, while launches, win-back and abandoned cart campaigns belong to your marketing/email system.
- After enabling, test the flow by abandoning a checkout with a real email and confirming the email arrives.
Caveat: Turning on both Shopify's abandoned checkout email and an ESP's abandoned cart flow risks duplicate messages — pick one owner.

Tags: store-setup, checkout, retention, email-marketing, automation, shopify
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Limit Quantity Per Order to Protect Inventory
Use when: Protecting limited inventory from single large orders, or keeping stock counts less obvious during a limited release.
- Go to checkout advanced preferences in Shopify and find the option to limit the number of items a customer can add to cart or order at once.
- Set a cap that matches your stock reality — the source's example caps purchases at 10 units of a product per purchase.
- Use it as a light stock-concealment tactic: the source notes that capping quantities prevents customers from inferring exactly how much stock you hold.
- Use it to spread limited inventory across more buyers when you deliberately do not want one person buying out your stock.
- Leave address-collection settings at Shopify's recommended defaults unless warehouse requirements demand otherwise.
- Verify the option exists and its exact wording in your current admin, since this was described as a newer feature.
Caveat: The source presents this as a newer Shopify feature — confirm availability on your plan and admin version before relying on it.

Tags: store-setup, checkout, inventory, shopify, merchandising
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Configure the Customer Account Page and Its Domain
Use when: Setting up or upgrading the customer account experience — login method, order history, returns and branding — for a Shopify store.
- In checkout and customer account settings, choose the newer customer accounts option rather than legacy: customers log in via a passcode sent by Shopify instead of creating a password.
- Consider legacy only for specific cases like marketplace stores where merchants need to sign up with email and password; the source does not recommend it otherwise.
- Apply a branded customer account domain so login and order status pages use your store's domain instead of shopify.com — expect to adjust DNS records, the same process covered for adding domains.
- Optionally enable social sign-in (Shop, Google, Facebook) under manage sign-in methods and account access.
- Optionally enable self-returns by first configuring return rules in your store policies, then activating self-return in customer account settings.
- Optionally enable store credits so refunded customers can spend credit in the store instead of taking a cash refund.
- Review customer account page customization in the theme editor and note that addable blocks are largely limited to blocks from installed apps.
Caveat: The source labels social sign-in, self-returns and store credits as new features worth testing for fit rather than assuming they suit every business.

Tags: store-setup, customer-accounts, retention, shopify, returns, domain
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Choose Discount Code vs Automatic Discount
Use when: Creating a Shopify discount for a promotion, influencer campaign, welcome flow or sitewide sale.
- Default toward automatic discounts when the goal is simply that customers get the deal — the source calls them more practical because they apply without any action.
- Choose a typed discount code when you need attribution or distribution: influencer/affiliate coupons so sales can be tied to that person, or codes embedded in a welcome email.
- Name codes deliberately — a code like BLACKFRIDAY30 is what customers will type at checkout, so keep it legible.
- Decide between the four Shopify discount types: amount off products (specific products/collections), buy X get Y (BOGO), amount off order, and free shipping.
- Decide eligibility: all customers, a customer segment (e.g. a VIP segment), or specific customers.
- Set usage limits per customer to prevent repeat abuse of the same code, and decide whether the code can combine with other discounts such as free shipping plus 30% off.
- Set a start and end date for time-limited offers like Black Friday.
- When publishing, decide whether to expose the discount to other channels: including it lets Facebook and Instagram shoppers see it, excluding it hides it from those channels.
Caveat: Decide channel exposure carefully — the source warns that including a discount exposes it on Facebook/Instagram, so exclude it when you do not want those sales discounted.

Tags: store-setup, discounts, promotions, shopify, acquisition, attribution
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Share a Pre-Applied Discount Link Instead of a Code
Use when: Sending promotions by email, SMS or ads where you want the discount applied without the customer typing anything.
- Create the discount as usual in Shopify discounts, complete its summary review, and save it.
- Use the shareable link option rather than copying the raw code text.
- Paste that link as the destination for email or SMS buttons so anyone who arrives from that link gets the discount pre-applied at checkout.
- Keep the raw code handy only for cases requiring manual entry, such as a code printed on packaging or spoken by an influencer.
- Verify the link still applies the intended discount after editing the discount's rules.
Caveat: A shareable link hides the discount mechanics from the customer, which can weaken the perceived value of 'using a code' — the source presents both delivery methods as options, not one universal rule.

Tags: store-setup, discounts, promotions, email-marketing, shopify
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Know Shopify's Gap Limit and When to Add a Discount App
Use when: Designing percentage-off promotions for a store with a high average order value, where uncapped savings would be too costly.
- Set up a discount normally: choose code or automatic, set percentage or fixed amount, select eligible products/collections, set customer eligibility, minimum purchase requirement, per-customer usage limits, combinability, and active dates.
- Recognize the limitation: the source states you cannot natively define a maximum saving cap, such as 30% off but no more than $100 saved.
- Assess whether the gap matters to your economics: the source flags it as critical when average order value is high — e.g. at a $1,000 AOV, an uncapped 30% is a large concession.
- When the cap matters, search the Shopify app store for a discount app that supports maximum savings, since the source says many exist and no single app covers everything.
- Follow the same setup approach for BOGO offers (buy X get Y): define minimum quantity or minimum purchase amount, pick the product customers receive, choose free or discounted value for it, and set a maximum number per order.
- Review the discount summary before saving to confirm every rule matches intent.
Caveat: The source says Shopify's native discount features may be sufficient to start and that app needs depend on each business's specific offer structure.

Tags: store-setup, discounts, pricing, promotions, apps, shopify
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Set Up a Gift Card Product for Last-Minute Buyers
Use when: Adding gift cards as a product, especially ahead of holidays or any period when delivery timelines will miss the occasion.
- In Shopify products, find the gift cards option and create a gift card product, taking one of the two available routes (create a gift card or add a gift card product).
- Set it up like any product: name it, write a description, upload an image/design, and use the default gift card template.
- Define the purchasable denominations — the source's example offers $10, $25, $50 and $100 choices on the product page.
- Confirm the buyer can choose whether to send the gift card to their own email or the recipient's email, and can enter recipient details, a message, and a send date so Shopify delivers it on the chosen day.
- Consider offering a physical card option manually alongside the digital one; the source notes clients did this and that it makes the gift feel more special but reintroduces delivery time constraints.
- Run promotions for gift cards right before holidays when shoppers realize they have missed delivery windows.
Caveat: Shopify gift cards are digital by default; a physical option has to be offered and fulfilled manually and therefore cannot solve a last-minute delivery problem.

Tags: store-setup, gift-cards, merchandising, seasonal, shopify
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Choosing and Vetting Shopify Apps Before Committing
Use when: Selecting any Shopify app — reviews, bundles, subscriptions, upsells, loyalty — for a store you operate or manage.
- Spend time on the app listing before installing: read the feature description and look at the screenshots to see what the app actually does.
- Scroll down and read merchant reviews — the source notes many apps are not as good as they claim, so this step can save you from a bad install.
- If the app offers a demo store, open it and walk the storefront: check where review widgets appear, whether the design looks professional or spammy, and what options exist.
- Don't automatically reject an app with few reviews if it does something niche — a low review count may reflect a specialized use case, but still try it before committing.
- Install the app, then verify the support team actually responds before you depend on it.
- Remember that installation alone is not enough: you must enable the app embed in the theme editor and save, otherwise the app (e.g. its review blocks) will not appear on the storefront.
Caveat: This is a vetting process, not a specific app recommendation — usefulness and budget requirements vary by store.

Tags: store-setup, apps, shopify, theme-editor, research
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Install a Review App and Collect Reviews by Email
Use when: Adding social proof to product pages on a new or growing Shopify store and deciding which review app to use.
- Install a review app that supports automated review-request emails sent some days after purchase; the source describes this as a common feature that lowers friction and increases review volume.
- Set the request delay based on how long customers need to experience the product — the source's example is roughly 5–6 days after delivery, adjusted to niche.
- Let customers submit the review directly from the email to reduce the steps required.
- Judge Me is the source's current recommendation: the presenter notes it is one of the most-reviewed apps, cheap (around $15/month), practical, with good support, and says an earlier negative impression was reversed after revisiting it recently.
- Consider alternatives when you need more than reviews — for example, the source mentions Stamped.io (spelled Stamp.io in the transcript) when you also want loyalty-type functionality.
- Import existing reviews if you are migrating from another platform or from marketplace listings such as Amazon — the source notes Judge Me supports importing reviews during setup.
- Verify current pricing, plans and interface in the app's listing, since pricing and features change.
Caveat: App recommendations are the presenter's opinion and pricing is described at time of recording — verify current plans. The source notes the free plan is limited and the paid tier unlocks more features.

Tags: store-setup, apps, reviews, social-proof, product-page, email-marketing
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Add Bundling and Subscription Apps Only Where the Niche Supports Them
Use when: Deciding whether to add bundle listings or subscription options to a Shopify store's catalog.
- For bundles: use Shopify's free bundling app to combine products from your catalog, which also manages inventory across bundled products — when a bundle sells, each component's inventory decreases together.
- Recognize the free bundling app's limits: the source says it handles variant display and inventory logic but may not cover more sophisticated bundling needs, so a paid third-party app may be required later.
- Pair bundles with a small discount — the source notes people like bundles and that they help raise average order value.
- For subscriptions: judge fit by product type. The source lists supplements, food, coffee and makeup as plausible subscription categories, and questions fit for electronic devices.
- If subscriptions fit, install Shopify's free subscription app to start, and move to a paid app only when you need more advanced behavior.
- Frame subscriptions as a retention tool: the source describes them as helping customers come back again and again.
- Verify current app capabilities before committing, since both native apps have described limitations.
Caveat: The free native apps are described as sufficient for beginners but limited — do not assume they cover advanced bundling or subscription logic.

Tags: store-setup, apps, bundles, subscriptions, retention, average-order-value
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Use Shopify Search & Discovery for Filters and Recommendations
Use when: Setting up or cleaning up collection filters, upsell recommendations and on-site search results on a Shopify store.
- Install the free Search & Discovery app from Shopify — the source calls it a must-have.
- Use it to manage your collection filters, product recommendations and search results in one place.
- If you are still paying for older filtering or product-recommendation apps, the source recommends uninstalling them and consolidating on this free app.
- Configure recommendations with the store's real cross-sell logic in mind — this is the mechanism that surfaces related products on product pages and in search.
- Verify the current app interface in your admin, since it is actively developed by Shopify.
Caveat: The source presents this as strong enough to replace several older paid apps but frames it as the presenter's opinion rather than a benchmark.

Tags: store-setup, apps, merchandising, product-page, search, shopify
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Reduce Apps and Image Weight to Protect Store Speed
Use when: Diagnosing or preventing slow page loads after installing apps, changing themes, or uploading heavy product photography.
- Track the speed metrics Shopify exposes in your online store dashboard once you have traffic — the source names LCP and layout shift among the metrics to follow.
- Remove apps you no longer use: the source explains apps inject code into your theme and can slow it, so keep only apps you actually need.
- After any change — adding an app, updating the theme — revisit the speed metrics and compare, so you can attribute a regression to the change you just made.
- Keep product images at a reasonable resolution rather than maximum size; the source notes many good Shopify themes already shrink images for you.
- If image weight is still an issue, use a Shopify app that compresses store images in bulk.
- Aim for acceptable/moderate speed rather than chasing perfection — the source advises not over-stressing about speed.
- Re-check metric names and locations in your current admin, as reporting surfaces change.
Caveat: The source treats speed as important for user experience but explicitly says not to obsess over it and defers detailed optimization to a separate resource.

Tags: store-setup, performance, apps, images, measurement, shopify
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Cover the Evergreen SEO Basics on Products, Collections and Store Settings
Use when: Completing baseline SEO for product pages, collection pages and the store homepage before or after launch.
- On every product and collection, fill in the SEO fields in the editor: the page title, the meta description, and the URL handle.
- In online store preferences, complete the social sharing image and SEO section: upload an image, set the homepage title, and write a meta description covering what the store sells and what the brand is about.
- Publish articles on the store — the source argues that even though AI answers reduce click-through traffic, articles still signal trustworthiness and help AI platforms decide whether to recommend you.
- Adapt to changed search behavior: the source says customers increasingly ask AI assistants for recommendations, and Shopify has been rolling out the ability to list products in ChatGPT, initially in the USA.
- Check whether your store has access to AI listing features yet — the source notes it was still rolling out and not available to everyone at recording time.
- Treat long-form SEO wins (backlinks, blog depth) as a long game rather than a launch checklist item.
Caveat: AI-era product listing and recommendation behavior is evolving and platform-dependent — the source explicitly says rollout status varies by region and time.

Tags: store-setup, seo, product-page, content, acquisition, shopify
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Match Checkout Branding to Your Store's Design System
Use when: Styling the checkout page in the theme editor to keep the buying experience visually continuous with the storefront.
- In the theme editor, go to checkout and customer account settings to reach the checkout customization area.
- Optionally add a logo to the checkout header and set its size (the source's example sizes it to 170) and alignment (center or right).
- Decide whether to add a background image to the header or top area — the source tries it only to illustrate the contrast problem and ends up keeping it simple.
- Set the background colors for the checkout areas and, when adding an image, check that text remains readable against it.
- Set the accent color used for buttons and error messages to the same color as your storefront's accent — if your contrasting color is orange, keep the checkout button orange.
- Choose the single-page checkout rather than multi-step; the source recommends keeping one-page.
- Note that review, thank you, order status, orders and profile pages have very limited block options, restricted largely to blocks from apps you have installed.
Caveat: Checkout visual customization is limited on non-Plus plans, so treat this as the full extent of styling rather than a starting point for a fully bespoke checkout.

Tags: store-setup, checkout, branding, theme-editor, conversion-optimization, shopify
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Decide on Tipping, B2B Fields and Address Defaults at Checkout
Use when: Working through the full set of Shopify checkout settings on a new store setup or a settings audit.
- Tipping: decide whether to allow customers to tip at checkout — the source usually leaves it off.
- Company name: exclude the field unless the business is B2B, since it adds friction for consumer buyers.
- Address fields: keep Shopify's default address requirements unless warehouse or logistics operations need something more specific.
- Contact method: choose email as the single contact option where you want email capture; see the separate card for the phone-number trade-off.
- Where a warehouse asks for cleaner shipping data (e.g. dropdown city selection instead of free text), recognize this generally requires Shopify Plus or specific warehouse setups.
- Work through the remaining settings one by one, since the source notes Shopify's defaults are reasonable unless you have specific logistics requirements.
- Verify each setting's current location in the admin before changing it.
Caveat: Defaults are usually acceptable — the source advises deviating only for concrete business reasons rather than for customization's sake.

Tags: store-setup, checkout, fulfillment, b2b, shopify, settings
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Install and Configure the Judge.me Review Widget on Product Pages
Use when: Setting up social-proof tooling on your Shopify store's product pages (PDP) before or after launch.
- Open the Judge.me app setup and click 'install review widget'. This takes you into the theme editor at the product page level.
- Confirm the 'leave a review' section block is present on the product template and keep it.
- Add the star ratings block: go to the product information section, click add block, choose apps, select star ratings, then drag it to sit directly under the product price. Save the theme.
- If your store already has customers and you are installing the app now, consider holding back the star/widget display until you have collected real reviews — the presenter suggests waiting rather than showing empty widgets.
- You can retroactively email past customers (e.g. last 6–12 months) to request reviews; schedule this only AFTER the request email is branded and set up.
- After installing, mark the setup step complete in the app's checklist and continue to widget customization in app settings.
Caveat: Judge.me is presented as having a forever-free plan and a paid 'Awesome' plan (~$15/month, with a trial); the source recommends the paid tier for full features, but this is a preference, not a requirement.
Caveat: The app UI and block names may change — verify against the current app and theme editor interface.

Tags: store-setup, product-page, shopify-apps, social-proof, reviews, conversion-optimization
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Set Up Automated Review Request Emails (Delays, Templates, Branding)
Use when: Building a post-purchase review collection flow to generate PDP social proof on a Shopify store.
- In Judge.me settings, set up the review request emails BEFORE scheduling any bulk requests to past customers.
- Configure delays under 'manage email review request': the default is 14 days for domestic orders and 5 for others. Adjust based on your niche — if products take time to try, increase the delay; if instant-use, lower it. You can set different delays for international and point-of-sale orders.
- Use 'schedule requests for previous Shopify orders' to bulk-request reviews from existing customers; use 'send manual request' for one-offs.
- Edit the review request and reminder templates: change the trigger (button vs. stars), language, subject line, and email title.
- Apply template styling globally (store logo, fonts, brand colors, alignment) via edit template styling — these apply to all emails.
- If you want customers to review without leaving the email, create a custom template from scratch, drag in the 'classic form' block, add the product image and product title (via email variables), and toggle the custom template on / default off.
- Set review publishing/moderation rules so you can approve reviews before they go live if you want full control.
Caveat: Free plan may limit features; the presenter recommends the paid plan but acknowledges the free option exists.
Caveat: Third-party review app UI and defaults change over time — verify current settings.

Tags: store-setup, shopify-apps, reviews, retention, email-marketing, social-proof
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Enable Judge.me Features: Import Reviews, Product Groups, Widget Branding
Use when: Consolidating existing reviews, de-duplicating proof across product variants, and branding review widgets.
- Import existing reviews from Amazon or a spreadsheet via the app's import option so you start with social proof rather than an empty PDP.
- Use product groups to link reviews between related products — e.g. a bundle (product A + B) and the standalone product A — so a review on one shows on both pages. Create multiple groups matching your catalog structure.
- Customize each widget you actually use: click customize, edit title, colors, and review sections to match brand colors/fonts; use the preview to check appearance.
- Brand all notification emails and templates, not just the review request — go through each notification and modify as needed.
- The presenter highlights Judge.me's support as its standout feature; contact support for help rather than working around issues.
Caveat: Only customize widgets you actually use — the app offers more than many stores need.
Caveat: Grouping reviews across products changes what shoppers see on each PDP; apply it deliberately.

Tags: store-setup, shopify-apps, reviews, product-page, merchandising, social-proof, retention
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Create Shopify Markets for Multi-Country Selling
Use when: Expanding a Shopify store to sell internationally (e.g. a France-based store selling to Germany, Italy, the US).
- Find Markets in your Shopify left sidebar; if absent (rare, if the update hasn't rolled out), find it under Settings.
- Create a market, name it (e.g. 'Europe'), and add countries via 'add condition'. Group countries that share tax rules — e.g. Italy + Germany fit together under EU rules, while Switzerland (non-EU) should be separate.
- Your business-location country becomes the default/first market automatically.
- For currency display per market you need Shopify Payments (and a registered business to activate it); it is the presenter's preferred gateway for this.
- Choose currency per market and set rounding (e.g. round to nearest 0.95) so prices don't look like raw conversions — the presenter recommends rounding for a natural look.
- Create catalogs per market to control which products are sold where — exclude specific products (e.g. gift cards) or limit to a subset for stock/legal reasons.
- Use the graph view to see market hierarchy and add a country as a submarket of an existing market (e.g. France inside Europe).
Caveat: Currency-per-market display requires a payment gateway that supports exchange (Shopify Payments is cited as the best option) and a registered business.
Caveat: Submarket/grouping decisions affect tax treatment — the presenter separates non-EU countries like Switzerland.

Tags: store-setup, shopify-markets, international, currency, catalog-management, shopify-payments
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Adjust Prices and Catalog per Market
Use when: Setting country-specific pricing or excluding products for a specific Shopify market.
- Under the market's catalog section, create a catalog (e.g. 'Europe'). By default all products are included; creating a catalog lets you limit or modify what's available.
- Apply a general price adjustment to raise or lower ALL product prices by a percentage in that market if you want uniform uplift.
- Alternatively, edit prices product-by-product and set a compare-at price so customers see before/after pricing.
- Use this especially when a country adds duties: the presenter says they include additional duties within product prices by changing prices between markets rather than surprising customers at checkout.
- Exclude specific items (e.g. gift cards) from a market catalog where they don't apply.
- Save the catalog, then verify the per-market product list and prices.
Caveat: Price changes per market require a gateway supporting currency exchange to render currency correctly.
Caveat: Compare-at pricing must be genuine to avoid misleading displays.

Tags: store-setup, pricing, shopify-markets, catalog-management, international, duties
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Apply Market-Specific Theme Customizations
Use when: Running an international store and showing country-specific banners, shipping messages, or holidays.
- In a market, click plus and add theme customization — this opens the Shopify theme editor scoped to that market.
- Choose whether to edit the whole market (e.g. Europe) or a specific submarket (e.g. France only).
- Make the change (e.g. swap the hero image for a holiday banner with the country flag). A small diamond marker next to an image indicates it's a market-level change, not the default store.
- Verify: the default store still shows the original, the specific market shows the new content, and other markets do not.
- Use this to display different shipping conditions or market-specific messages only to the relevant audience.
- Check the graph view — Shopify logs that a market's homepage was changed, useful for tracking edits over time.
Caveat: The presenter believes this feature may require the second Shopify plan or higher, not the first plan.
Caveat: Extensive per-market customizations multiply maintenance; track changes via the graph view.

Tags: store-setup, shopify-markets, merchandising, international, theme-customization, shipping
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Configure Taxes and Duties per Market
Use when: Selling cross-border and deciding whether/how Shopify collects taxes by country.
- Go to Settings → Taxes and duties.
- Set business information per region: for the EU, enter business location (e.g. France) and tax details; add the US and other countries if you want Shopify to collect taxes there.
- The presenter's strong recommendation: do NOT bill B2C customers taxes at checkout — include taxes within product prices and pay them yourself, to avoid surprise charges that annoy buyers.
- If you must collect taxes (e.g. European sellers), define the different tax rules per market here since rates differ by country.
- Cross-check all tax setup with a legal advisor — the presenter explicitly warns taxes are tricky and differ by country.
- If you don't collect taxes, confirm your product-page settings don't charge taxes, and if you do collect, state it clearly on the product page.
Caveat: The presenter's 'never bill B2C taxes' is personal preference and may conflict with legal obligations in some regions (e.g. EU).
Caveat: Tax law varies by country and changes — always verify with a professional.

Tags: store-setup, taxes, shopify-markets, international, duties, compliance
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Add and Manage Warehouse Locations
Use when: Running multiple warehouses (e.g. one per region) and needing orders routed and inventory tracked correctly.
- Go to Settings → Locations and click add location, naming each (e.g. 'Paris warehouse', 'USA warehouse') and entering its address.
- Assign the relevant locations to your products: open a product, go to inventory, click edit location, and enter available quantities per warehouse.
- Manage quantities across locations via Products → Inventory, switching between warehouses to see stock per location.
- Assign each location to the countries it serves (e.g. Paris warehouse to Europe, USA warehouse to US) so orders route to the right warehouse.
- Plan to connect each warehouse to its shipping/delivery rates in Settings → Shipping and delivery so orders are processed from the correct origin.
Caveat: Accurate per-location inventory is a prerequisite for correct routing; unassigned locations break fulfillment logic.
Caveat: Multi-warehouse setups add operational complexity — the presenter stresses getting this right during setup.

Tags: store-setup, fulfillment, inventory, shipping, locations, multi-warehouse
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Set Up Shipping Zones and Flat Rates per Country
Use when: Setting up shipping and delivery for each country where your Shopify store sells.
- Go to Settings → Shipping and delivery. If a country has no shipping rate, Shopify marks the product as not shippable there — so every country you sell to needs a rate.
- For each shipping zone, set the fulfillment location (which warehouse handles it) and add rates.
- Use the 'use flat rate' option: the presenter strongly recommends flat rates because they're easiest for customers to understand and estimate, which reduces checkout drop-off.
- Always offer free shipping above a threshold: e.g. €10 shipping for Germany on orders 0–100, free shipping over €100; or free shipping over €50 with €8.80 below (as shown by default).
- Add custom-rate text so customers see an estimated delivery time, easing the checkout decision.
- Wire different warehouses to different countries: e.g. set USA rates at $20 flat from the USA warehouse, separate from the Paris warehouse rates for France/Germany.
- Use the on-screen preview to see exactly what customers will see at checkout.
- Also configure pickup/in-store and local delivery options if relevant to your business type.
Caveat: Missing shipping rates for a country makes products unavailable there entirely — double-check every target country.
Caveat: Local delivery and pickup suitability depend on business type (e.g. groceries); the presenter notes variance.

Tags: store-setup, shipping, checkout, international, fulfillment, conversion-optimization, flat-rate
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Add a Second Store Language with Translate & Adapt
Use when: Adding a second language (e.g. Arabic for KSA customers) to a Shopify store.
- Install the free Shopify 'Translate & Adapt' app.
- Go to Settings → Languages, click add language, select the language, and assign a subdomain/domain for it if desired.
- Run auto-translate in the app — it translates the whole store automatically; the results are described as very good but meant as a baseline.
- Review and edit translations: the app shows original text next to translated text for each section (products, pages, product templates). Use 'auto translate' to fill any fields that were missed.
- Adjust not just text but images too — if images contain text, you can set a different image per language.
- Assign the new language to the relevant market (e.g. Arabic → KSA market).
- Shopify detects customer browser language and loads the store in the matching available language by default, with header/footer switches for manual change.
Caveat: The app gives two free languages; going beyond two requires a paid plan.
Caveat: Auto-translations need human review — the presenter treats them as a starting point, not a final result.
Caveat: Auto-translation extends to product info, pages, templates, and images.

Tags: store-setup, international, languages, shopify-apps, localization, shopify-markets
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Handle Currency Display When Shopify Payments Isn't Available
Use when: Selling internationally from a country where Shopify Payments isn't offered and needing multi-currency display.
- If Shopify Payments is available, use it: Shopify detects customer location and shows the store in the preferred language AND local currency automatically.
- If Shopify Payments is NOT available in your country, use a third-party app to display prices in the visitor's local currency on the homepage, product pages, collection pages, and cart.
- Accept the key limitation: no app can change prices at checkout, so customers will see and pay in your store's base currency at checkout even if they browsed in their local currency.
- Given that limitation, set your base currency to a widely understood one (the presenter recommends USD or EUR rather than a niche local currency such as AED), so the checkout price is easy for international customers to interpret.
Caveat: Third-party currency apps only affect pre-checkout display; checkout always uses store currency.
Caveat: The presenter confirms Shopify Payments is the only gateway they know of that supports per-market currency.

Tags: store-setup, currency, international, shopify-payments, checkout, payment-gateways
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Choose and Set Up Payment Gateways by Market
Use when: Setting up checkout payment options, especially for international or multi-market stores.
- Go to Settings → Payments and click add payment method.
- If Shopify Payments is available in your country, use it as your primary gateway — the presenter calls it the cheapest option with the most features (cards via Stripe, Apple Pay, etc.). Activation requires a registered business and business registration documents.
- Add PayPal as a widely-used, universally recognized option alongside it.
- If Shopify Payments isn't available, use Stripe as the next-best (card payments + Apple Pay).
- Search payment providers to see what's available in your registered country; options vary (e.g. Klarna for the UK, Tabby for UAE/KSA).
- Ensure your main markets all have the most common gateways — and add regional must-haves, e.g. Cash on Delivery in Lebanon.
Caveat: Shopify Payments requires a registered business and may require verification; if deactivated after setup, checkout can break.
Caveat: Available gateways differ by country and change over time — verify the current provider list.

Tags: store-setup, payment-gateways, checkout, international, shopify-payments, stripe, paypal
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Manage Orders and Fulfillment Notifications
Use when: Setting up fulfillment after launch, whether with a warehouse integration or manual shipping.
- With a warehouse integration (via the warehouse's Shopify app or manual integration with permissions granted), orders route to the correct warehouse based on location/country.
- Shopify automatically sends the customer an order-confirmation email; order/shipping notifications are managed by Shopify, not the warehouse.
- The warehouse processes the order, adds the tracking number, and pushes it back to Shopify via the integration; Shopify then sends the customer the 'out for fulfillment' email with the tracking number.
- If fulfilling manually, print the shipping label, prepare and ship the order, then add the tracking number to the Shopify order so customers can track it.
- Warehouses without an app install an integration manually — you give them store permissions and they handle routing.
Caveat: Common failure points: orders not pushed to the warehouse, or a warehouse integration not fully transmitting order data (especially with many SKUs or bundles).
Caveat: The presenter notes that a tracking number added by the warehouse is what triggers Shopify's shipping notification.

Tags: store-setup, fulfillment, orders, shipping, warehouse, notifications
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Run Real Test Orders Across All Locations Before Launch
Use when: Pre-launch checklist for a Shopify store, especially multi-warehouse or high-SKU stores.
- Don't rely only on Shopify's non-real test order — place REAL orders so the actual payment gateway and fulfillment are exercised.
- Test in every location/market: e.g. if selling in five countries, place orders so each warehouse fulfills one. This surfaces issues with bundles/multi-SKU orders where warehouses may get confused or integrations misfire.
- Double-check the warehouse integration — the presenter calls this the most important thing to verify.
- Verify the payment gateway is active: gateways can get deactivated after setup due to missing business info or pending Stripe/Shopify Payments verification, which blocks all checkouts.
- Confirm shipping rates exist in every country you sell to.
- Confirm tax settings — if you don't intend to charge taxes, verify checkout isn't charging them; if you do, ensure it's stated on the product page.
- For shipments to the US/Canada, add a clear note that customers may pay additional duties/taxes (these aren't predictable from Shopify), separate from Europe where in-region buyers typically aren't charged extra.
Caveat: The presenter recommends many real test orders especially if you have pre-launch demand (email list) and expect immediate sales at launch.
Caveat: Duties/taxes to the US and Canada are not predictable via Shopify — they must be communicated as a customer-side possibility.

Tags: store-setup, launch, testing, fulfillment, payment-gateways, taxes, shipping
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Set Order ID Format and Order Processing Preferences
Use when: Finalizing checkout/order settings before launch on a Shopify store.
- Go to Settings → General → Orders.
- Under order ID, add a prefix/suffix extension to the order number — the presenter notes this hides the true count of orders you've received from customers.
- Under order processing, keep the confirmation step REQUIRED so customers see a summary of their order before checking out (the presenter recommends keeping this on).
- Do NOT change the 'automatically fulfill orders' setting — the presenter does not recommend enabling auto-fulfillment.
- After finalizing settings, remove password protection from the store (in preferences) to make it live.
Caveat: These are the presenter's stated preferences — verify against your specific fulfillment workflow.
Caveat: Auto-fulfillment can conflict with multi-warehouse or manual fulfillment setups.

Tags: store-setup, orders, checkout, launch, shopify-settings
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Order ID and order-processing settings to configure at launch
Use when: Initial store setup or a settings audit for cart/checkout and fulfillment workflow before launch.
- Go to Settings > General > Orders in Shopify (verify current menu path in your admin, as Shopify's interface changes).
- Use the order ID prefix/suffix field to add characters before or after order numbers — the source's purpose for this is to obscure how many orders you have actually received from customers who see the order number.
- Keep 'require confirmation step' enabled. The source strongly recommends this: customers see an order summary before completing checkout, which reduces errors and unwanted orders.
- Leave automatic fulfillment OFF for physical products, since most products have real fulfillment time; the source notes gift cards are the exception because Shopify emails them instantly and they need no fulfillment.
- Auto-archive fulfilled orders is optional and depends on your workflow — the source says this is genuinely up to you, so decide based on whether you regularly revisit fulfilled orders for support or reporting.
- Do not over-engineer this section; the source explicitly says order flow is 'not that big a thing' and you will find your own routine.
Caveat: Settings labels and locations change between Shopify versions — confirm in your own admin.
Caveat: Auto-fulfillment for non-gift-card products would mark orders shipped before they are, damaging delivery expectations.

Tags: store-setup, checkout, fulfillment, shopify-admin, order-management
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Configure Shopify customer notifications without breaking checkout emails
Use when: Notification and post-purchase communication setup for order confirmations, shipping updates and draft orders.
- Go to Settings > Notifications. The customer notifications are the most important group; the source prioritizes order confirmation and shipping confirmation above all others.
- Order confirmation sends immediately when a customer orders and carries all order details. Keep customer email required at checkout — the source 'highly highly recommends' this, because if a customer only gave a phone number they may not receive the email confirmation and you would need SMS enabled instead.
- Draft order invoice fires when you create orders manually in Shopify (draft orders).
- Shipping confirmation fires automatically the moment a tracking number is added to an order — e.g. when a warehouse integration feeds tracking back into Shopify, Shopify emails the customer the tracking link with no action from you.
- Other notifications exist (local pickup, local delivery, gift card, store credit); review them if relevant to your model but the source treats the first two as the priority.
- If you edit an email, use the preview and send-a-test features. The source barely touches order confirmation — occasional small text or color changes only — because it must arrive with correct information. Deeper edits mean working in HTML code.
Caveat: Timing and sending method are controlled by Shopify and cannot be changed — the source sees this as a benefit because it lowers error risk.
Caveat: The source warns you can break these emails if you edit them without being sure what you are doing.

Tags: store-setup, retention, post-purchase, notifications, shopify-admin, checkout
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Set up customer support before launch, not after
Use when: Preparing customer support capacity and response workflow ahead of a launch or high-volume sales period.
- Put a contact email or contact form on your contact page before launching — the source states you will receive customer emails as soon as the store goes live.
- Answer each email quickly and effectively. The source warns that slow or poor replies turn customers and potential customers into angry people who dislike your brand.
- At brand launch, keep support in-house — yourself, a family member or an employee — rather than outsourcing to a third-party support company. The source's stated reason is wanting full control early on.
- Expect tickets about delivery, shipping and order status rather than product questions; if product pages are thorough, product questions should be rare. A detailed shipping policy reduces ticket volume but will not eliminate it.
- Handle order changes in Shopify directly: you can open an order and edit fields such as the customer email, and fix addresses or change orders.
- Use live chat for real-time contact — the source mentions a free Shopify chat app that works on mobile so you can reply from your phone. For large SKU catalogs needing tier-one help, consider an AI chat tool that answers first and escalates to a human; the source names Gorgias/Juie-style AI chat as an example. Verify current app names and pricing before committing.
- Treat satisfaction as the mechanism for repeat purchase and brand durability, not as a nice-to-have.
Caveat: The outsourced-support tradeoff is the source's opinion for early-stage brands only; larger operations may reasonably choose otherwise.
Caveat: App names and free tiers change — verify before installing.

Tags: store-setup, retention, customer-support, live-chat, post-purchase, order-management
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Read conversion-rate funnel breakdowns to find where buyers drop
Use when: Diagnosing a weak conversion rate or deciding whether the problem sits in merchandising, PDP, cart or checkout.
- Open Analytics > Reports and locate the conversion-rate breakdown report, which shows the funnel stages: sessions, add-to-cart rate, reached-checkout rate and completed checkout (conversion rate).
- Use the window and comparison settings deliberately — a single day's number is not your average conversion rate; pick a longer window (the source uses last 12 months and year-over-year comparisons) so the average is meaningful.
- Locate the largest drop-off between adjacent stages rather than staring at the final number.
- If the big gap is between add-to-cart and completed checkout, the source's example diagnosis is a shipping-rate problem pushing people away at checkout — investigate shipping cost presentation before rewriting product copy.
- If add-to-cart itself is low, the issue is upstream: traffic quality or product page persuasion, not checkout.
- Compare against your own historical baseline and niche, not a universal benchmark — the source calls 10% add-to-cart 'very good' and 2.63% completed conversion 'acceptable for our niche' as its own example, not a target.
- When you know which stage leaks, at least one specific fix (shipping thresholds, PDP clarity, offer) can be tested instead of guessing.
Caveat: The stated rates are the source's example store, not benchmarks to hit.
Caveat: Shopify reports these metrics using its own definitions of gross vs net sales and session counting; check Shopify's documentation for current calculation methods.

Tags: store-setup, measurement, conversion-optimization, checkout, product-page, analytics
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Choose the analytics time window and comparison before drawing conclusions
Use when: Any recurring analytics review, launch post-mortem or monthly performance meeting.
- In Analytics, set the time window first. Available options include today, yesterday, last 30 minutes, last 7 days, last 12 months, last week, year, weekday, month-to-date, quarter-to-date, year-to-date, plus a dedicated Black Friday/Cyber Monday section.
- Use a long window for judgement calls: the source cautions that seeing 6% conversion today does not mean your average is 6%; you need 3, 6 or 12 months to see how the store actually performs and how it changed.
- Optionally set a comparison window (e.g. previous year) when you want to see whether a strategy or change moved the business; the source sometimes turns comparison off because it can be confusing.
- Set the display currency — useful if you sell in a currency other than your own and want to read your numbers in terms you understand.
- Use live view for real-time behaviour during launches rather than for judging performance.
- Expect the customer cohort/retention report and other data to be meaningless early — the source says you need roughly a year of customers, ads and sales before behaviour patterns are readable.
Caveat: Short windows are for operational monitoring only, not for evaluating strategy.
Caveat: Skip comparison when it makes the dashboard harder to read for your team.

Tags: store-setup, measurement, analytics, reporting, experiment-design
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Customize the Shopify analytics dashboard around your own metrics
Use when: Setting up recurring reporting for a store you operate or manage, especially when the default dashboard hides the metrics you act on.
- From Analytics use the customize/edit control to drag and drop metric cards into the layout you want; the source describes this as easy drag-and-drop and recommends aligning it with your workflow and business.
- Keep a default baseline view first so you understand Shopify's standard metric set before rearranging.
- Go to Reports for topic-specific reporting: reports are grouped by category such as acquisition (sessions over time, visitors over time, sessions by social referrer), behaviour, customers, sales and finance.
- Create your own reports and save them into the reports library — the source's example is a report comparing this year's sales to the previous year, saved for repeat access.
- Filter reports by creator so you can find reports you or teammates built.
- Use the sales reports' table/chart controls to change breakdowns when a chart alone is not answering the question.
- Over time, let the dashboard evolve: the source frames the default setup as a starting point, not the destination.
Caveat: Report names and category groupings are Interface-dependent — confirm available reports in your own admin.
Caveat: Do not rearrange before you understand each metric's definition; the source stresses the difference between gross sales, discounts and net sales and points to Shopify's own documentation for how each is calculated.

Tags: store-setup, measurement, analytics, reporting, shopify-admin
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Use the customer cohort/retention report to time win-back emails
Use when: Planning retention and email reactivation timing for a store with at least several months of order history.
- Open the customer cohort analytics report from the analytics dashboard; it opens as a full report showing retention rate month after month over the selected window (the source looks at last 12 months).
- Read two things: when returning customers come back, and what share of a cohort comes back in each period (e.g. of 100 customers acquired today, how many buy again in month 1, 2, 3, 6...).
- Use that timing to schedule win-back emails: the source's example is that if customers typically return after four months, then customers who have not returned by four months should receive an email asking why, inviting them back and offering an incentive.
- Use the pattern to estimate long-term customer value — how much revenue the same customer generates across a year or two — which informs how much you can spend to acquire them.
- Expect the report to be uninformative before you have real data: the source says it only makes sense once you have roughly a year of ads, sales and collected customers behind you.
- Treat this as the input for a retention calendar rather than a one-off read.
Caveat: The four-month example is illustrative of the method, not a universal return cycle for your niche.
Caveat: Small cohorts produce noisy retention percentages; wait for volume before acting aggressively.

Tags: store-setup, retention, customer-research, measurement, email-marketing, analytics
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Ask Shopify's AI agent for custom analytics reports
Use when: Producing a quick custom report (e.g. multi-year conversion trend) without manually constructing charts in the reports library.
- Access the AI report tool from Shopify analytics via the new exploration option; the source also references Sidekick, Shopify's AI agent, for analytics, reports and other store help.
- State the report you want in plain language — the source's example prompt is a report showing conversion-rate improvement over the last two years.
- Review the query the tool writes and the resulting report; the source notes the tool composed the query itself in its simple example.
- Use it for analysis and report generation, not as a replacement for understanding metric definitions — the source still directs you to Shopify's documentation for how gross vs net sales and similar figures are calculated.
- Keep any report you will reuse (save it into the reports library) so you are not re-prompting each period.
Caveat: The source calls its demo prompt a very basic example; complex questions may need refinement.
Caveat: AI features and their availability change quickly — verify the current entry point and capabilities in your Shopify admin.

Tags: store-setup, measurement, analytics, reporting, ai-tools, shopify-admin
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Read the sales breakdown and by-channel metrics correctly
Use when: Monthly performance review, channel-mix decisions or pricing/discount evaluation.
- Start with the dashboard summary cards: gross sales, returning customer rate, orders fulfilled and total orders — the source treats returning customer rate as a headline health metric alongside revenue.
- Open the total sales breakdown and learn the difference between gross sales and net sales, and how discounts sit between them. The source stresses this explicitly and points to Shopify's own resources for the exact calculation of each figure.
- Check total sales by sales channel to see where revenue actually originates, and use acquisition reports such as sessions by social referrer to see where visits come from — revenue channel and traffic channel are separate questions.
- Track average order value over time as its own trend line; the source calls AOV a very important metric.
- Check total sales per product to identify best sellers and confirm whether your catalog bets are paying off.
- Read total sales over time month to month to spot improvement or decline in context of the window and comparison you set.
Caveat: Metric definitions are Shopify's, not universal — always confirm the calculation before comparing to external benchmarks.
Caveat: Channel attribution in Shopify reflects Shopify's own channel labelling; a channel with high sessions may contribute little revenue.

Tags: store-setup, measurement, analytics, pricing, merchandising, reporting
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Don't rely on default Shopify emails to fix weak product pages
Use when: Deciding whether to expand shipping policies, FAQ content or PDP copy after launch based on incoming support tickets.
- Use the source's stated expectation as a diagnostic: if product pages are thorough, customers should mostly not be asking product questions; most tickets will be about delivery, shipping or order status.
- Classify incoming tickets into product questions versus logistics questions for the first weeks after launch.
- A high volume of product questions indicates weak PDP content or missing sizing/spec/usage information — fix the page rather than answering the same question repeatedly.
- A high volume of shipping/delivery questions indicates weak shipping-policy detail — the source states a very detailed shipping policy reduces ticket volume, though it will not eliminate it entirely.
- Resist changing order-confirmation and shipping-confirmation emails (which are order-status communications) as a substitute for fixing pre-purchase clarity; the source keeps those emails essentially untouched.
- Handle genuine per-order requests (email change, address fix, order modification) individually in Shopify instead of treating them as content problems.
Caveat: Even a strong PDP will not stop all contacts; the source accepts individual order-change requests as normal.
Caveat: This is the source's stated expectation based on its experience, not a measured benchmark.

Tags: store-setup, product-page, customer-support, post-purchase, conversion-optimization
Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx

---

## Initializing a Shopify account and choosing a store name
Use when: You are starting a brand-new store from scratch and need to create the Shopify account and store identity.
- Register with a business email address you control long-term, not a personal address you may lose access to; this becomes the account owner login and the destination for Shopify's billing and verification notices.
- Choose the store name carefully: the myshopify.com subdomain handle is generated from it and the source notes it is effectively permanent, while the customer-facing store name can be changed later in Settings.
- Before committing, set the store's country/region and currency correctly in the initial onboarding questions, since these influence default tax, payment and pricing behavior.
- Verify the current wording of the Shopify signup onboarding in the admin, because the source warns that click paths change; treat any tutorial path as a guide and confirm each screen live.
Caveat: Shopify onboarding screens change frequently; verify the current flow rather than following a stale path literally.
Caveat: The myshopify.com handle is treated as permanent per the source, so decide it before launch rather than after.

Tags: store-setup, shopify, domain-and-email, store-configuration, verification
Source: The OFFICIAL Shopify 2026 Tutorial.docx

---

## Setting up Shopify Payments with exact legal identity match
Use when: You are enabling payment capture for the first time and need payouts to clear without verification holds.
- Open Settings then Payments and activate Shopify Payments, then fill the business and personal details fields.
- Enter the account holder's legal first and last name exactly as printed on their government ID: the source's example is that 'Robert' must not be shortened to 'Rob' or the account can be flagged for verification.
- Match the address and business registration details to official documents, including any registered business name, tax ID and entity type fields.
- Expect that a mismatch triggers a verification hold that pauses payouts, so correct any discrepancy immediately rather than waiting for a failed payout.
- Review the payout bank account details for the correct currency and account type before saving; changing bank details later re-triggers verification.
Caveat: Name, address and ID mismatch is a documented cause of payout verification holds per the source, not a guarantee of one.
Caveat: Requirements for which documents are needed vary by country and entity type; check the current Shopify Payments requirements page for your region.

Tags: store-setup, shopify, payments-and-tax, payments, verification, fulfillment
Source: The OFFICIAL Shopify 2026 Tutorial.docx

---

## Defining physical presence for tax collection
Use when: You are configuring tax regions and need Shopify to calculate the correct rate at checkout.
- Go to Settings then Taxes and duties and add the locations where you have a physical presence: warehouse, office, home address used for operations, or any other location that creates a tax obligation.
- Add each region where you have nexus; Shopify collects tax based on the locations you register here, so an unlisted state or country can result in no tax being charged.
- Decide whether to register for tax in additional jurisdictions beyond your physical presence and add them individually if so.
- Where the source distinguishes them, use tax-included pricing settings only for regions where displayed prices must include tax, such as certain VAT countries.
- Review the tax settings after adding new shipping destinations, since a region where you now sell may need tax registration before you collect there.
Caveat: This card covers Shopify's configuration mechanics only; consult a tax professional about where you actually owe tax, because the source does not establish a universal nexus rule.
Caveat: Overriding tax rates manually can create compliance risk if your registered obligations change.

Tags: store-setup, shopify, payments-and-tax, tax, checkout, store-configuration
Source: The OFFICIAL Shopify 2026 Tutorial.docx

---

## Building shipping zones for domestic and international delivery
Use when: You are about to sell to customers outside your home country and need shipping rates that do not undercharge or block checkout.
- Open Settings then Shipping and delivery and create a domestic zone containing the home country with the rates you want to offer, using either flat rates, price-based rates or carrier-calculated rates.
- Create a second zone for international destinations and decide which countries to include; the source treats domestic and international as needing separate configuration rather than one global zone.
- Set at least one fallback rate in every zone, because a destination with no rate can block or confuse checkout.
- Check the list of countries you will ship to against the zones you built, adding individual countries or regions as needed.
- Re-test a sample address in each zone after editing, since changing zone membership silently changes which rate a customer sees.
Caveat: Carrier-calculated rates require an appropriate carrier account or Shopify plan feature; verify current requirements in the admin.
Caveat: International rules and duties are outside this source's scope; use Shopify's own current documentation for customs configuration.

Tags: store-setup, shopify, shipping-profiles, checkout, fulfillment, international
Source: The OFFICIAL Shopify 2026 Tutorial.docx

---

## Setting default package weights so calculated rates do not undercharge
Use when: You use carrier-calculated or weight-based shipping rates and are worried about undercharging on multi-item orders.
- In Settings then Shipping and delivery, find the packaged weight section for the shipping profile and set a default package empty weight for your standard box or mailer.
- Configure the units consistently in the store settings, since a mismatch between product and package weight units produces wrong quotes.
- Consider that each product's weight plus the default package weight determines the rate quote; a missing package weight makes every calculated rate too low as orders grow.
- Create additional shipping profiles for products that ship in different packaging, if a single default weight would misrepresent them.
- After changing package weights, quote a test order with several items and compare it against the same order before the change to confirm rates moved in the expected direction.
Caveat: This is a source-stated configuration risk, not a benchmark; the correct default weight depends on your actual packaging and carrier.
Caveat: Calculated rates also depend on carrier account settings outside Shopify; verify in the carrier's own tools if quotes look wrong.

Tags: store-setup, shopify, shipping-profiles, fulfillment, measurement, store-configuration
Source: The OFFICIAL Shopify 2026 Tutorial.docx

---

## Connecting a custom domain and a business email address
Use when: You have bought a domain and need it pointed at the store and a matching email set up before launch.
- Purchase the domain from a registrar (Shopify sells one, or use an external registrar), then open Settings then Domains in the admin.
- Add the existing domain rather than buying a new one if you already own it, then follow the DNS instructions: either point A and CNAME records to Shopify values or change nameservers to Shopify's, depending on the method chosen.
- Wait for the domain to show as connected before removing any store password, because a custom domain that has not propagated makes the store unreachable at that address.
- Set the primary domain to the custom one so Shopify uses it in links and emails rather than the myshopify.com URL.
- Set up a branded email address through a mail provider and forward or alias it appropriately, then test sending and receiving before you list it anywhere customer-visible.
Caveat: DNS changes can take time to propagate; the Shopify admin shows the connection status but the timing depends on the registrar.
Caveat: Exact button labels in the Domains section change over time, so verify the current interface.

Tags: store-setup, shopify, domain-and-email, store-configuration, verification, brand
Source: The OFFICIAL Shopify 2026 Tutorial.docx

---

## Testing checkout, tax and policy links with test mode transactions
Use when: You are one step from launching and need evidence that payments, tax and legal links function end to end.
- Enable test mode on Shopify Payments (or use Shopify's bogus gateway) and place test orders that exercise the full checkout, including card-like test details.
- Verify tax is calculated as expected for each tax region you configured by comparing the test order totals against the rates you set.
- Click every policy and legal page linked in the footer and checkout during the test order, confirming each opens the intended content rather than a placeholder.
- Test a shipping destination in each shipping zone to confirm the correct rate appears and there is always a fallback rate available.
- Only after checkout, tax, shipping and policy links pass, remove the store password to make the store publicly accessible; the source presents the test order as the verification gate before un-gating.
Caveat: Test mode is for verification, not proof of a live payment; make a real transaction separately if the source process requires it before launch.
Caveat: Never leave the store in test mode or the password gate on after launch, since either blocks real customers.

Tags: store-setup, shopify, verification, checkout, payments-and-tax, measurement
Source: The OFFICIAL Shopify 2026 Tutorial.docx

---

## Installing tracking and verifying it fires before launch
Use when: You are installing analytics or ad pixels and need to confirm data will be captured once the store is live.
- Install the tracking scripts or app for analytics and advertising platforms through the Shopify admin or the platform's own app.
- Use a test session with an analytics debug tool to confirm page views and, where configured, add-to-cart and checkout events register rather than assuming the script loaded.
- Check that tracking code is present on the checkout step as well as the storefront, since the source separates PDP and checkout concerns and a script that only covers the storefront misses purchases.
- Verify the data appears in the analytics platform's real-time view during the test session as the end-to-end proof the install worked.
- Re-verify after changing themes or installing new apps, because theme changes can drop tracking snippets.
Caveat: Checkout tracking behavior depends on the Shopify plan, checkout extensibility and the platform's integration; verify current support before relying on it.
Caveat: The exact debug workflow differs per analytics tool; this is a verification habit, not a specific tool instruction.

Tags: store-setup, shopify, tracking-install, measurement, verification, conversion-optimization
Source: The OFFICIAL Shopify 2026 Tutorial.docx

---

## Publishing required legal and policy pages before removing the password
Use when: You are preparing for launch and need the legal, policy and contact pages in place and linked.
- Create the standard policy set: refund and returns, privacy, terms of service, shipping and delivery, and a contact page, using Shopify's generated policy templates where available.
- Edit each generated policy to reflect your actual practices, since templates contain placeholder language that may not match how you operate.
- Confirm the policy pages are linked in the footer and wherever the checkout references them, checking the links during a test order rather than only on a normal page view.
- Where your market requires it, include the legal business identity and contact route on the relevant pages.
- Re-check the pages after publishing, because the source treats verification that each setup step actually worked as part of the setup process rather than optional.
Caveat: This is configuration and completeness guidance, not legal advice; jurisdiction-specific obligations require a qualified source.
Caveat: Generated policy templates must be adapted; leaving placeholders on a live store misrepresents your practices.

Tags: store-setup, shopify, legal-pages, verification, store-configuration, checkout
Source: The OFFICIAL Shopify 2026 Tutorial.docx

---

## Doing store setup in the right order to avoid launch breakage
Use when: You are planning the launch sequence and want to avoid discovering broken checkout or tax settings after customers arrive.
- Configure account identity and store settings first, since country, currency and store name affect the defaults of downstream tax and payment screens.
- Set up payments with exact legal identity next, then taxes and physical presence, then shipping zones and package weights, because shipping rates depend on weight data and tax regions depend on where you have presence.
- Connect the custom domain and business email after the store operational settings, so the store is reachable at the final address when you begin testing.
- Install tracking and create the legal pages, then run test-mode orders as the gate that verifies checkout, taxes, shipping rates and policy links together.
- Remove the store password only after the test order passes; the source treats un-gating as the last step, not an early one.
Caveat: This is the source's emphasis on order of operations, not a claim that any other sequence is impossible; it identifies what tends to break if steps are out of order.
Caveat: The source warns that interfaces change, so the exact screens for each step should be confirmed in the current Shopify admin.

Tags: store-setup, shopify, store-configuration, verification, payments-and-tax, shipping-profiles
Source: The OFFICIAL Shopify 2026 Tutorial.docx

---

## Verifying each setup step actually worked
Use when: You have configured a store section such as payments, shipping or domains and want to confirm it works before relying on it.
- After saving a setting, perform the action a customer would: place a test order for payments and checkout, quote a multi-item order for shipping rates, and open each footer link for legal pages.
- Check the domain resolves at the custom address rather than only the myshopify.com URL before considering the domain connected.
- Confirm the analytics platform receives data during a test session rather than only checking that a script tag exists in the theme.
- Check tax and shipping appear correctly in the test order total instead of only checking that the settings saved.
- Log any step that cannot be verified and resolve it before removing the store password; treat the test order as the aggregated proof of the whole setup.
Caveat: Some checks, such as DNS propagation, are outside your control and only show status rather than instant confirmation.
Caveat: Test mode verifies logic but does not prove a live payment settles; complete any live transaction test the current Shopify process requires.

Tags: store-setup, shopify, verification, measurement, checkout, store-configuration
Source: The OFFICIAL Shopify 2026 Tutorial.docx

---

## Configure Shopify Legal Business Name and Address Before Anything Else
Use when: Right after creating a new Shopify store and before setting up payments, shipping or taxes.
- On the Shopify home dashboard, open the Settings icon at the bottom of the left navigation.
- Select General, click the pencil icon, and enter your legal business name and full business address.
- Use the exact legal name your business is registered under; this feeds into payment verification and tax configuration later.
- If you cannot locate a setting mentioned in a tutorial, open Sidekick (top-right icon) and ask it where the setting lives rather than hunting through menus.
- Treat this as step one: skipping it means re-entering the same data across payments, taxes and shipping, and risk of mismatch when verifying Shopify Payments.
Caveat: The demo store is an example matcha business, so its settings will not match a different product category — adapt rather than copy.
Caveat: Admin interfaces change; verify current click paths in your own admin before following along.

Tags: store-setup, shopify, store-configuration, sidekick, payments, tax
Source: The OFFICIAL Shopify 2026 Tutorial.docx

---

## Add First Products with Descriptive Titles, Weight and Dimensions
Use when: Adding the first products to a new store before building collections or shipping rates.
- From the dashboard click 'Add your first product'; a small number of solid products is preferable to hundreds at launch.
- Write a descriptive title (e.g. a specific product type plus key attribute) rather than a generic name.
- If the description box is blank, ask Sidekick to draft a professional description, then edit it to reflect the actual product and value proposition.
- Upload product media via the upload button; images and videos can be refined inside the admin by asking Sidekick to create variations in natural lighting or lifestyle settings (up to five images per conversation — start a new conversation for more).
- Enter price, inventory stock, product weight and location — weight is needed for shipping calculations in the next setup stage.
- Review the search engine listing block (clickable title, URL, meta description); it auto-populates from the description but can be edited or generated by Sidekick.
- Save, then repeat for each product.
Caveat: AI-generated images are fine for banners and graphics, but the source advises mixing in authentic product shots because buyers want to see the product used by real people.
Caveat: Descriptions generated by AI should be checked against what the product actually is.

Tags: store-setup, shopify, product-page, product-data, seo, sidekick, media
Source: The OFFICIAL Shopify 2026 Tutorial.docx

---

## Organize Products into Manual or Smart Collections for Findability
Use when: Merchandising a product catalog so shoppers can navigate to relevant groups from the homepage and navigation.
- In the left sidebar under Products, click Collections, then Add collection.
- Choose the collection type: manual (you add products yourself) or smart (Shopify adds products based on rules you set).
- Add the title and description, then fill the search engine listing fields so the collection page can rank in Google or Bing.
- For manual collections add products directly; for smart collections define the rules that determine membership.
- Optionally have Sidekick create the collection (e.g. a three-product flavor collection featured on the homepage), then click Preview to check the result.
- Add a collection photo — upload your own or generate one in the admin (e.g. a single image showing all three flavors together) so the collection has a visual identity.
Caveat: Collection structure should map to how customers think, not to internal product taxonomy.
Caveat: The source's 'faster to find = more likely to purchase' claim is a merchandising principle, not a measured benchmark.

Tags: store-setup, shopify, merchandising, collections, navigation, seo
Source: The OFFICIAL Shopify 2026 Tutorial.docx

---

## Choose and Customize a Shopify Theme, Then Restyle It
Use when: Designing the visual layer of a new store before launch, after products and collections exist.
- From the admin click Online store, then Themes.
- Either type a store description into the theme generation box (e.g. 'health-inspired eco-chic matcha energy drink') and click Generate theme, or browse the theme store filtering by free themes and click Try theme.
- Open Edit theme to reach the theme editor; sections expose toggle buttons, sliders, color boxes and dropdowns, and most changes preview in real time.
- For brand direction, ask Sidekick for a professional, clean, organized design with color palettes including hex codes, font recommendations and layout tips.
- Apply colors under theme settings > Colors — Sidekick can push the palette into the editor, and you can review before publishing or adjust individual values.
- Set typography for headings, body text, subheadings and accents to match the recommended pairing.
- Upload the logo (and an inverse version for dark backgrounds) and a favicon under the logo and favicon settings.
- Edit page content sections directly in the preview (click a section such as the hero banner to replace its image; add sections via the plus icon), then save.
Caveat: Use a high-quality PNG with a transparent background for the favicon, kept to roughly 200–300 pixels wide for desktop.
Caveat: Two-thirds of online retail orders come through mobile per the source, so check every customization in the editor's phone preview, not just desktop.
Caveat: Verify the current theme-generation and Sidekick controls in your own admin.

Tags: store-setup, shopify, theme, branding, sidekick, visual-design, mobile
Source: The OFFICIAL Shopify 2026 Tutorial.docx

---

## Set Up Navigation Menus with Nested Submenus
Use when: Configuring store navigation after products, collections and pages exist, so menu links point to real destinations.
- From the admin click Content in the left sidebar, then Menus.
- Open a preset menu (main menu, catalog, contact) to edit its name and the link attached to it.
- Click Add menu item and choose the destination: a collection, product, page or external URL.
- Drag items using the vertical dots handle to reorder them; drag one slightly right under another to create a nested dropdown submenu.
- Add a new menu (e.g. link the flavor collection created earlier and nest it under the main menu) to keep the top level clean.
- Organize by customer-facing logic — category (men's, women's, accessories) or product type (shirts, pants, shoes) — not by internal naming.
- Save, then preview the storefront using the eye icon on the Online store row and test every menu path, including on a phone.
Caveat: Deep nesting works against the stated goal of a few clicks; use submenus to reduce clutter, not to bury items.
Caveat: Always click through the live preview — menu items can point to empty or wrong destinations.

Tags: store-setup, shopify, navigation, merchandising, mobile, store-preview
Source: The OFFICIAL Shopify 2026 Tutorial.docx

---

## Connect or Buy a Domain and Set It as Primary
Use when: Giving the store a real URL before launch so customers, email and search treat it as the canonical address.
- Go to Settings, then Domains.
- Click Connect existing and enter your domain, or Buy new domain and search your store name to see availability and suggestions.
- Purchase the domain and enter payment information; Shopify then connects a newly bought domain to the store automatically with no manual DNS configuration.
- Test the domain by visiting it in a browser to confirm it loads your store correctly.
- In domain settings, update the store's primary domain so customers see the custom domain rather than the myshopify.com address.
- Pair the domain with a business email rather than a personal address — the setup scope pairs domain and email as one foundation item.
Caveat: Connecting an existing domain from an external registrar may involve verification steps not covered here; check the current Shopify domain flow.
Caveat: The source notes automatic connection for domains bought via Shopify; externally purchased domains can behave differently.

Tags: store-setup, shopify, domain, launch, email, store-configuration
Source: The OFFICIAL Shopify 2026 Tutorial.docx

---

## Enable Two-Step Authentication Before Activating Shopify Payments
Use when: Preparing to activate payments on a new store — this is a gating requirement, not an optional security nicety.
- Go to your profile, then Security inside the Shopify admin.
- Click Turn on two-step and enter your password.
- Choose an authentication method: an authenticator app (e.g. Google Authenticator or Duo), SMS text message, a security key, or Shopify's built-in mobile prompts.
- Follow the on-screen steps to complete enrollment.
- Save the recovery codes somewhere secure — the source explicitly warns that a notes app does not count.
- Only then proceed to Settings > Payments to begin Shopify Payments setup.
Caveat: Without two-step authentication, Shopify Payments cannot be activated.
Caveat: Losing recovery codes and the second factor simultaneously can lock you out; treat codes as a business-critical credential.

Tags: store-setup, shopify, payments, security, account-access
Source: The OFFICIAL Shopify 2026 Tutorial.docx

---

## Activate Shopify Payments with Exact Legal Names to Avoid Verification Holds
Use when: Setting up Shopify Payments so the store can actually accept money, especially for solo founders or registered companies.
- Check that two-step authentication is enabled first, then go to Settings > Payments and click the prompt to finish setting up your account.
- Choose your business type. If you are starting out with no business number — including technically being a sole proprietor — select Individual; there is no separate sole proprietor option.
- For an individual, enter personal information: legal name exactly as it appears on your ID, date of birth, SSN/ITIN/TIN, email, phone number and home address.
- Upload a verification document such as a passport or driver's license.
- If you run a registered business (LLC, corporation, partnership) that has a business registration number, select Business and enter registered business name, business number/EIN/VAT number, business phone and address.
- Add an account representative (usually the owner or someone with signing authority) with their legal name, date of birth, ITIN/SSN/TIN and residential address.
- Use the exact government spelling everywhere — e.g. 'Robert' rather than the nickname 'Rob' if that is what the license says.
- Confirm your bank account can receive deposits in your region (A transfer in the US, EFT in Canada, SWIFT in Europe/Asia/Africa, BECS in Australia), then save and wait for review.
Caveat: Verification typically takes a few hours but can take a few days in some cases; continue building the store while waiting rather than blocking on it.
Caveat: If you are unsure whether a registered-but-not-incorporated entity counts as a business, ask Sidekick — if you have a business registration number, register as a business.
Caveat: Shopify Payments availability varies by country; if it is unavailable, supported gateways differ by region.

Tags: store-setup, shopify, payments, verification, compliance, payouts, sidekick
Source: The OFFICIAL Shopify 2026 Tutorial.docx

---

## Set Payment Capture, Wallets and Customer Contact Defaults
Use when: Finalizing checkout behavior on a new store after Shopify Payments is activated.
- In Settings > Payments, scroll to the payment capture method and select Automatically at checkout so funds are captured the moment an order is placed; manual capture can be switched on later if you want to review orders before charging.
- Confirm Shop Pay, Apple Pay and Google Pay appear at checkout — faster checkout is described as a conversion win; add or remove wallets under Manage next to Shopify Payments, then Manage payment methods.
- In Settings > Checkout, find the customer contact method setting to control whether order information is sent by email or SMS.
- Enable the checkbox that shows customers a link to track their order with Shop.
- Ensure the marketing consent box is enabled so the store builds an email list from day one.
- Optionally add additional payment methods such as PayPal or third-party card processors from the Additional payment methods section — multiple methods can run alongside Shopify Payments.
Caveat: Automatic capture is presented as the easiest starting default, not a universal rule; merchants who want to review orders before charging should use manual capture.
Caveat: Available wallets and alternative payment methods vary by country and account.

Tags: store-setup, shopify, checkout, payments, email-list, conversion-optimization
Source: The OFFICIAL Shopify 2026 Tutorial.docx

---

## Build Shipping Zones and Rates Without Undercharging
Use when: Setting up shipping so orders go out and shipping charges cover real carrier costs.
- Go to Settings > Shipping and delivery; Shopify pre-creates general shipping rates with domestic and international zones.
- Under the domestic zone, inspect the weight-based rates already filled in and click Add rate to add your own, deciding what to charge (e.g. a flat amount or free shipping).
- Alternatively let Shopify calculate shipping automatically based on origin, destination, and package weight and size.
- When unsure, describe your actual weights to Sidekick (e.g. a single unit at half a pound, a three-pack at 3 pounds, an eight-pack at 7 pounds) and ask it to walk you through updating domestic rates; it can provide reference prices based on typical carrier costs.
- Decide explicitly between charging a flat rate, passing through actual shipping cost, or baking shipping into the product price — the source describes the third as common among successful stores (e.g. $35 with free shipping rather than $30 plus $5).
- Click Done, then Save, and verify the rates appear correctly.
Caveat: Free shipping with the cost absorbed into product price is presented as a strategy tip the source says increases conversions, not a measured benchmark.
Caveat: If using dropshipping or print-on-demand, confirm supplier shipping costs to each region before setting rates, especially internationally.

Tags: store-setup, shopify, shipping, pricing, free-shipping, sidekick
Source: The OFFICIAL Shopify 2026 Tutorial.docx

---

## Add a New Shipping Zone to a Specific Country
Use when: Expanding shipping to a specific country or region with rates distinct from the default international zone.
- Go to Shipping and delivery and scroll to the International section.
- Click the three dots next to it, then Edit zone, and uncheck the country or countries you want to move out of the international zone.
- Click Done, then Save; the country is now unassigned and ready for its own zone.
- Back in Shipping and delivery, click Shipping, then 'start shipping to more places' / Go to markets, then Create market.
- Name the market, add a condition, check the box for the target country, then click Done and Save.
- Click Add rate to set what shipping to that country costs: flat rate, calculated rate using a carrier, or free shipping.
- Set the price and any conditions, then Done and Save, and repeat for each additional country or region.
Caveat: International shipping costs add up, so the source advises being intentional about rates rather than defaulting to free.
Caveat: Verify the current Market creation flow, which is an area Shopify has changed over time.

Tags: store-setup, shopify, shipping, international, markets, rates
Source: The OFFICIAL Shopify 2026 Tutorial.docx

---

## Set Default Package Weights and Dimensions to Prevent Shipping Undercharges
Use when: Any store using calculated shipping, before launch, to stop quietly losing money on every order.
- Go to Settings > Shipping and delivery and scroll to the Packages section.
- Click Add package and choose the package type.
- Enter the outside dimensions of the box and the weight of the empty packaging — the product weight alone is insufficient because boxes, packing materials and bubble wrap add weight.
- Give the package a memorable name such as 'small box' or 'standard mailer'.
- If all products ship in the same packaging, check 'set as default'.
- If different products use different packaging, assign packages at product level: open the product under Products, go to the shipping section and choose the matching package, then save.
- While in the product, double-check the product weight as well.
- Confirm zones, rates and packages are all saved before moving on to test orders.
Caveat: Inaccurate weights cause undercharging on calculated rates — the source frames this as a direct margin leak.
Caveat: Default package applies store-wide; mixed packaging requires per-product assignment.

Tags: store-setup, shopify, shipping, packaging, margin, calculated-rates
Source: The OFFICIAL Shopify 2026 Tutorial.docx

---

## Configure Local Delivery, Store Pickup and Shipping Labels with Billing Thresholds
Use when: Serving local customers or handling fulfillment in-house, and reconciling where shipping label charges appear financially.
- For local delivery: click Setup under the local delivery section, choose the delivery location, define a radius (e.g. 100 miles/kilometres) or specific postcodes, optionally set a minimum order amount and a delivery fee, then save.
- For store pickup: click Setup, select the pickup location, set pickup times, add special instructions, then save.
- For labels: buy shipping labels directly in the admin where available, which uses Shopify's pre-negotiated carrier discounts; if unavailable in your region, install a label app such as one of the shipping label apps from the app store.
- Understand the billing mechanism: label cost is not deducted from the customer's payment but added to your Shopify account balance, invoiced immediately when your billing threshold is reached, or bundled into your monthly subscription bill if the threshold is never hit.
- Check current threshold and accumulating charges under Settings > Billing, under Bills.
Caveat: The billing threshold is determined by account activity and store history, so it differs per merchant.
Caveat: Label apps and carrier availability vary by country; verify current options before committing to a workflow.

Tags: store-setup, shopify, fulfillment, shipping-labels, local-delivery, billing, operations
Source: The OFFICIAL Shopify 2026 Tutorial.docx

---

## Review Shipping Insurance Coverage Before High-Value Shipments
Use when: Deciding how to handle lost or damaged shipments of fragile or high-value products.
- If using Shopify Payments on the Grow, Advanced or Plus plan, note that up to $200 of insurance is included at no extra cost on each eligible label.
- Read the fine print to confirm the insurance covers what you are actually shipping — the source flags typical exclusions for fragile items and higher-value products.
- If on the Basic plan, shipping insurance is not automatically included when buying labels through Shopify, but insurance can be purchased for orders up to $5,000.
- If shipping from Canada or Europe, evaluate the alternatives: carrier insurance directly, a third-party insurance app, or self-insuring (absorbing losses yourself).
- Ask Sidekick for guidance on the best option for your country and product profile if the choice is unclear.
Caveat: Coverage limits and exclusions are plan- and product-dependent; the source states these figures for its own time of recording, so confirm current terms.
Caveat: Self-insuring is a deliberate risk-acceptance decision, not a free alternative.

Tags: store-setup, shopify, shipping, insurance, risk-management, fulfillment
Source: The OFFICIAL Shopify 2026 Tutorial.docx

---

## Set Up a Repeatable Fulfillment Workflow with Bulk Processing
Use when: Preparing fulfillment operations before orders arrive so the process is repeatable rather than improvised.
- Open the Orders tab; with no orders yet, establish the sequence in advance.
- For each approved order: review customer details, pull items from inventory, prepare packaging.
- Click Print packing slip (this goes inside the box), then print the shipping label.
- Ship by dropping off or scheduling a pickup depending on the option selected; the customer automatically receives the shipped email with tracking and Shopify normally marks the order fulfilled.
- For partial fulfillment: if an order contains multiple items and one is on back order, ship the available items now and fulfill the remainder once restocked.
- For volume: pack in small batches (e.g. two orders at a time, marked in progress), then return to Orders, select the checkbox at the top, bulk print packing slips and create shipping labels, and mark everything fulfilled in one action.
- Customize the customer notification: ask Sidekick where to edit customer email templates, then add your logo, set the accent color and preview before saving.
Caveat: Fulfilling the wrong item or partially fulfilling without confirming inventory can trigger support issues; verify stock before marking shipped.
Caveat: Verify current bulk action labels and locations in the admin, which change over time.

Tags: store-setup, shopify, fulfillment, operations, notifications, bulk-actions
Source: The OFFICIAL Shopify 2026 Tutorial.docx

---

## Publish Return and Refund Policies and Enable Self-Serve Returns
Use when: Launching a store that needs clear returns terms visible at checkout and a low-friction returns process.
- Go to Settings > Policies and click return and refund policy; if none exists, Shopify provides a template to edit.
- Customize the template to match your actual practices and click publish to make it live.
- Go to Settings > Customer accounts and toggle on self-serve returns.
- Return to Policies and open the return and refund policy; insert the template, customize, and publish if not already done.
- In the return rules area, set the return window in days, whether return shipping is charged, any restocking fee, and which items are final sale.
- Save the settings, then confirm the policy links are reachable from the storefront and visible at checkout.
- The source frames clear, simple policies as reducing disputes — the clearer the policy, the fewer arguments.
Caveat: Policy content must reflect real business practices; a published policy that contradicts what you actually do creates worse disputes than no policy.
Caveat: Return windows and restocking fees are business decisions, not benchmarks.

Tags: store-setup, shopify, returns, policy, customer-service, checkout
Source: The OFFICIAL Shopify 2026 Tutorial.docx

---

## Configure Sales Tax Based on Physical Presence and Set Duties for International Markets
Use when: Making the store legally collect tax at checkout before launch, including for international customers.
- Go to Settings > Taxes and duties and select the country where your store is based.
- Under sales tax, click Collect in a new region and select the appropriate location, such as a state or province.
- Enter your sales tax ID number if you have one, then click Collect sales tax to finalize.
- Scroll to Duties and import taxes, click Set up, select all markets that apply, and save — Shopify then calculates taxes and duties at checkout so customers do not pay them on delivery.
- Update your shipping policy to state explicitly that duties and taxes are handled at checkout, which the source flags as necessary collateral to that setting.
- Double-check shipping taxability: in Taxes and duties, open the country or state and find the shipping tax options; for US states, use advanced options to choose whether shipping is taxable, since this varies by jurisdiction.
- Decide on tax-inclusive pricing only where required or expected: enable 'include sales tax in product price and shipping rate' under global settings for markets like Japan, where it is required, and the EU, where it is common.
- For international selling, use dynamic tax-inclusive pricing under Markets with a selected market and adjusted pricing settings — e.g. a $100 product shows as $100 tax-included in the UK but $90.91 plus tax at checkout in the US.
Caveat: The source's basic rule is that tax settings should reflect where the business has physical presence (location, inventory, employees), but tax rules vary by jurisdiction and change frequently.
Caveat: The source explicitly advises keeping records of tax registrations and consulting a local tax professional rather than relying on the platform defaults alone.

Tags: store-setup, shopify, tax, duties, international, compliance, pricing
Source: The OFFICIAL Shopify 2026 Tutorial.docx

---

## Run Test Orders in Shopify Payments Test Mode Before Launch
Use when: Final pre-launch verification after payments, shipping, tax and fulfillment are all configured.
- In the Shopify Payments section of Settings > Payments, click Manage and toggle on test mode (or check 'use test mode').
- Go back to the admin and click the eye icon next to Online store to view the store as a customer.
- Add a product to the cart and attempt a purchase using an official Shopify test credit card number — ask Sidekick for the current test card numbers — so no real card is charged.
- Verify the full checkout flow: tax calculations, shipping rates presented correctly, and payment options working.
- Confirm that links to policy pages, such as the return policy, are visible at checkout.
- Test the downstream workflow by processing the test order through receiving and fulfillment to expose anything that sticks.
- Repeat the entire walkthrough on a phone; the source reiterates that most shoppers are on mobile.
- Ask Sidekick for a checklist of everything to review while test mode is active, then turn test mode off in Shopify Payments when satisfied.
Caveat: Test with multiple different addresses to catch rate and tax issues — a single address test may miss problems.
Caveat: Never use a real credit card during testing; use Shopify's test card numbers, which change and should be confirmed with Sidekick or current documentation.

Tags: store-setup, shopify, checkout, test-orders, payments, quality-assurance, mobile
Source: The OFFICIAL Shopify 2026 Tutorial.docx

---

## Run a Pre-Launch Audit of Products, Policies and Navigation
Use when: Final quality pass before removing password protection, when the builder has been staring at the store too long to spot obvious errors.
- Ask Sidekick to scan the product list for missing descriptions or prices; Sidekick is described as effective at catching missing product images, pricing gaps and half-finished details.
- Ask Sidekick to verify all contact, shipping and return policies are set up correctly.
- Ensure the essential pages exist before launch: contact page, shipping policy, return policy, privacy policy and terms of service — these affect both customer trust and how Google evaluates the site.
- Generate first drafts of policies by asking Sidekick (e.g. a shipping policy, or a return policy for a clothing business with a 30-day window), then customize to match actual practices.
- Do a final walkthrough as a first-time visitor: click through navigation, add an item to the cart, and complete checkout in test mode.
- Confirm shipping rates look right and all payment options work with test card numbers rather than a real card.
- Repeat the walkthrough on a phone before launch.
Caveat: AI-generated policies are starting points to customize, not legal documents to publish unedited.
Caveat: The source frames missing policy pages as a red flag for both shoppers and search engines; it does not promise a ranking outcome.

Tags: store-setup, shopify, pre-launch, quality-assurance, policy, legal-pages, sidekick
Source: The OFFICIAL Shopify 2026 Tutorial.docx

---

## Remove Password Protection to Go Live and Announce Launch
Use when: The day the store has passed verification and is ready to receive real customers.
- From the admin go to Sales channels > Online store > Preferences and deselect password protection; the store becomes publicly visible immediately.
- Draft a short personal launch email to friends, family and contacts featuring your best product or collection with a clear shop-now button (ask Sidekick to draft it, then add your own touch).
- Send via Apps > Messaging > Create campaign, choose an email template, paste the copy, add images, and send a test email before sending for real.
- Plan a three-post social sequence: a teaser to build curiosity, a behind-the-scenes post telling your story, and a clear launch announcement with the store link.
- Consider a small paid boost on the launch post (the source cites a $20–$50 range as extending reach beyond existing followers, particularly on Instagram or Facebook).
- Set SEO groundwork at launch rather than retrofitting later: ask Sidekick to audit the store for SEO issues, improve meta descriptions, and optimize homepage, about page and product listings.
- Write descriptive alt text for product images instead of generic file names (e.g. describing the product and pack size), and connect Google Analytics and Google Search Console on launch day to track traffic sources and detect indexing problems.
Caveat: Boost budgets and expected reach are source suggestions, not guarantees of results.
Caveat: Keep alt text natural for accessibility rather than keyword-stuffing.
Caveat: The source notes a beautiful store with zero visitors is just an expensive hobby — going live is not the same as getting traffic.

Tags: store-setup, shopify, launch, email, social-media, seo, analytics
Source: The OFFICIAL Shopify 2026 Tutorial.docx

---

## Use Campaigns and UTM Automatch Rules to Attribute Marketing in Shopify
Use when: Measuring which channels and campaigns actually drive sessions and orders, so budget and creative decisions are based on data rather than guesswork.
- Open the Marketing tab in the admin; the four sections that matter at the start are Overview, Campaigns, Attribution and Automations.
- Check Overview for key metrics over time and which marketing channels are actually bringing people in.
- Create a campaign with a specific, goal- or timeframe-based name (e.g. 'Black Friday' or 'Launch week'); Shopify assigns it a unique ID used for tracking.
- Add tracking by one of three methods: shareable links (custom URLs and QR codes for influencers, emails or in-person events), automatch rules, or campaign activities.
- For automatch rules, use UTM parameters consistently — e.g. apply utm_campaign=Black Friday to every promotional link and set utm_source to Instagram, Facebook, TikTok or email per platform; rules matching those parameters group the traffic into one campaign while still showing which platform drove it.
- Note that additional parameters like utm_content and utm_term are not used for matching but are still tracked, so they can differentiate creative variants.
- Add existing traffic sources such as a newsletter or a social ad as campaign activities to track them; removing an activity later removes its traffic from the report.
- Interpret results with the relevant attribution model: last non-direct click (default, excludes direct visits), last click, first click, any click (all interactions credited), or linear (credit split equally).
Caveat: Attribution models answer different questions — first click suits interest generation, last click suits final conversion, linear suits supporting touchpoints; no single model is universally correct.
Caveat: Automatch rules depend on consistent UTM naming discipline; inconsistent campaign or source values fragment the data.

Tags: store-setup, shopify, measurement, attribution, utm, campaigns, analytics
Source: The OFFICIAL Shopify 2026 Tutorial.docx

---

## Choose a Shopify attribution model by marketing goal
Use when: Deciding how to judge which traffic source or campaign is driving purchases before reallocating ad budget or cutting a channel.
- Open Shopify analytics reports and locate the attribution section; it reports sessions, sales, orders, return on ad spend (ROAS) and customer acquisition cost per marketing effort.
- Pick the model that matches your question: last non-direct click (default) credits the last marketing channel before purchase excluding direct visits — good for final-conversion questions.
- Last click credits the last touchpoint even if direct; first click credits the channel that started the journey (useful for awareness testing); any click gives credit to all interactions; linear splits credit equally across all touchpoints (useful for full-journey support).
- Compare the same campaigns across two models — if a channel wins on first click but loses on last click, it is generating interest rather than closing sales; treat that as a role, not a failure.
- If the models are unclear, ask Sidekick which attribution model suits your store and have it explain what each model measures best before acting on the numbers.
Caveat: Model choice changes which channel looks best, so don't judge a channel by one model alone.
Caveat: Direct visits are excluded from the default last non-direct click model, which can make brand searches look under-attributed.

Tags: store-setup, measurement, attribution, acquisition, analytics, marketing-dashboard
Source: The OFFICIAL Shopify 2026 Tutorial.docx

---

## Set up campaign tracking activities and a morning marketing report
Use when: You are running multiple channels and need a repeatable way to see which source is driving sessions and sales each day.
- In the marketing section, add campaign activities and filter by channel or UTM parameter; searching by traffic source lets you add only the activities you want tracked.
- Understand that adding a campaign activity pulls all its associated traffic into the campaign report, and removing it removes that traffic from the report — so the report only reflects what you have added.
- Set a daily habit: ask Sidekick for a marketing section report at the top of your day so you focus on the channels that matter before making changes.
- Use the report to compare channels on sessions and sales, then make one adjustment at a time rather than changing everything at once.
- Keep UTM tagging consistent on ads, emails and social links so the campaign report groups traffic correctly.
Caveat: Reports only show traffic from activities you have added, so missing an activity makes a channel look weaker than it is.
Caveat: Sidekick and dashboard wording change between Shopify releases; verify the current interface before following exact menu paths.

Tags: store-setup, measurement, utm-tracking, marketing-dashboard, acquisition, analytics
Source: The OFFICIAL Shopify 2026 Tutorial.docx

---

## Set up marketing automations for welcome, cart recovery and lifecycle messages
Use when: You want welcome discounts, abandoned cart recovery, post-purchase upsells, win-back or thank-you messages running without sending each one by hand.
- Go to the automation section of the marketing hub and browse pre-built templates from Shopify Messaging or third-party apps; some templates require an external app such as Shopify Flow, which is shown before you can select it.
- Choose the automation type that matches your goal: welcome discount for new subscribers, abandoned cart recovery, post-purchase upsell, win-back for lapsed customers, birthday message, or thank-you email after purchase.
- For each automation, configure settings such as wait times between the customer action and the send, and when emails go out.
- Note that most automations only send to customers subscribed to marketing, so list growth is a prerequisite for these to work.
- For custom logic, build in Shopify Flow using triggers, conditions and actions; ask Sidekick to either create the automation or walk you through the setup if you get stuck.
Caveat: Automations depend on opt-in subscriptions; non-subscribed buyers won't receive marketing automations.
Caveat: Templates and app requirements change; confirm the current setup in your admin.

Tags: store-setup, retention, automation, email-marketing, abandoned-cart, shopify-flow
Source: The OFFICIAL Shopify 2026 Tutorial.docx

---

## Use Shopify Messaging campaigns within the free email allowance
Use when: Sending announcements, newsletters, product highlights or promotions to your contact list and deciding whether you need a paid email platform.
- Open Apps, select Messaging, and click Create campaign; choose a goal-based template (announcement, newsletter, product highlights, promotion) or Code your own.
- Edit sections by dragging and dropping content blocks and clicking individual text, buttons or images to adjust them; the email automatically applies your store colors, fonts and logo and saves changes as you work.
- For product blocks, choose static (everyone sees the same products — good for launches and seasonal drops) or dynamic (products change per customer behavior and purchase history — the source suggests dynamic tends to suit upsells and repeat customers).
- Select the audience at the top via Select segment (all subscribers, purchased at least once, email subscribers) or create a new segment.
- Set a catchy subject line plus preview text; ask Sidekick for subject/preview options by specifying the email type, audience and offer.
- Verify the sender email: quick verification via a link sent to the address is fastest to start; full domain authentication with DNS records is better for long-term deliverability but can take up to 48 hours.
- Before sending, use Review to flag misses, check typos, featured products and that every button links correctly, then send now or schedule.
Caveat: Shopify plans include up to 10,000 free emails per month for campaigns and automations, except abandoned checkout emails which are always free; SMS is priced separately per message.
Caveat: SMS availability varies by market — check with Sidekick before planning SMS.
Caveat: A quick-verified sender address delivers worse long term than authenticated domain sending.

Tags: store-setup, email-marketing, retention, automation, segmentation, shopify-messaging
Source: The OFFICIAL Shopify 2026 Tutorial.docx

---

## Build targeted customer segments for email and offers
Use when: Sending a campaign, scheduling a promotion, or restricting a discount code to specific buyers such as repeat customers or high spenders.
- Go to Customers, then Segments in the Shopify admin.
- Build segments on behavior, for example customers with two or more orders, or customers with total spend over a threshold such as $200 — these represent loyal repeat buyers.
- Use the segment when sending a campaign by clicking Select segment at the top of the email builder.
- When creating a discount code, set eligibility to specific customer segments and choose the segment you built.
- Set usage limits (total uses or one use per customer) and active start/end dates so the offer doesn't leak beyond the intended audience and window.
- Use Segments beyond VIP work: lapsed customers for win-back, new subscribers for welcome series, first-time buyers for follow-up offers.
Caveat: Segment rules should match a clear business decision — defining VIPs as 'spent over $200' is a choice, not a validated benchmark.
Caveat: Discounts only to likely-full-price buyers protect margin, but the source's claim that blanket discounts waste margin on loyal buyers is its own reasoning.

Tags: store-setup, segmentation, retention, email-marketing, pricing, customer-research
Source: The OFFICIAL Shopify 2026 Tutorial.docx

---

## Connect Meta (Facebook/Instagram) and TikTok to Shopify before running ads
Use when: Launching your first paid social ads to drive immediate traffic to a new store.
- In Shopify settings, go to sales channels and search for the official Facebook and Instagram or TikTok app; install it.
- Before connecting Meta, ensure: an established Facebook account (not brand new, so Meta doesn't flag it as fraudulent), owner/admin permission on the business manager, Facebook page and Instagram account, and an Instagram professional account.
- Log in to Facebook first, then click Facebook and Instagram in admin and Get started to connect the account.
- Add business assets (the business page and Instagram account you'll sell from), then add data sharing from a pixel connected to your ad account if one exists.
- Add business details including the customer contact email and your return window, then agree to the seller agreement and grant the business portfolio access to the catalog.
- Submit for review; once approved you get Meta Ads Manager access for feed, stories and reels placements. Choose an objective matching your goal (traffic vs sales), set a daily budget, let Meta's AI help find the audience, and upload scroll-stopping image or video creative.
- Expect traffic on the site within 24–48 hours, then return to the Shopify marketing dashboard and pull Facebook ad attribution data; if traffic is missing, ask Sidekick for targeting or ad-copy suggestions.
Caveat: Both a platform business/ad account and Shopify-side app setup are required; set up the ad account first or the connection fails.
Caveat: Return window and contact email are shown to customers — get these policies right before submitting.
Caveat: The source defers detailed ad optimization to a separate tutorial, so treat this as connection setup only.

Tags: store-setup, acquisition, paid-social, meta-ads, tiktok, sales-channels
Source: The OFFICIAL Shopify 2026 Tutorial.docx

---

## Run an organic social content mix with clear paths to purchase
Use when: Building sustainable traffic and community on Instagram, Facebook or TikTok without relying only on paid ads.
- Plan posting frequency at 3–4 times per week (not daily) to stay consistent without burnout.
- Vary content types: aesthetic product shots with benefit-focused captions and a product link, behind-the-scenes sourcing or packing, customer testimonials (with permission), educational posts, motivational pieces and user-generated content reposted with permission.
- Define a few content pillars so messaging stays consistent (for a matcha brand the source suggests health, fitness, sustainability); turn pillars into recurring formats like lifestyle shots, ingredient carousels, or short explainer videos.
- Give every post three elements: a link back to the store (tagged product, bio link, or story link sticker), a clear call to action ('grab yours before we sell out', 'buy now'), and 5–10 targeted hashtags rather than 30 random ones.
- Use Stories for real-time packaging, shipping, product demos, quick FAQ answers and founder-to-camera clips; keep them quick and casual.
- Use Reels to reach new audiences with product demos, before/afters, transformations, customer reactions, or trending audio paired with product.
- Ensure every story and reel points somewhere — link sticker, tagged product, or bio link.
Caveat: Posting cadence of 3–4 times per week is the source's recommendation, not a validated performance benchmark.
Caveat: Get permission before reposting customer testimonials or user-generated content.
Caveat: Organic content builds long-term demand; for immediate new-store traffic the source points to paid ads.

Tags: store-setup, acquisition, organic-social, creative-strategy, content-marketing, ugc
Source: The OFFICIAL Shopify 2026 Tutorial.docx

---

## Vet Shopify apps before installing
Use when: Adding any app — email/SMS, reviews, pop-ups, referrals — to your store and deciding which one to trust.
- Check the app rating and review count: look for 4+ stars, ideally 4.5 or higher, and at least 100+ reviews as a reliability sign.
- Read recent reviews, not just the top ones, and look for patterns in complaints.
- Verify the developer by clicking the developer name to see their other apps; established developers usually have multiple apps or a strong track record.
- Look for the Built for Shopify badge — these apps meet Shopify's highest quality standards.
- In the beginning install one app at a time as an actual need arises, not a full stack upfront.
- Browse by category via Settings, Apps, Shopify App Store, filtering by rating, free-to-paid and category; or ask Sidekick for recommendations.
Caveat: Rating and review thresholds are the source's heuristics, not guaranteed quality measures.
Caveat: App features, free tiers and pricing change; recheck before committing.
Caveat: Every app adds code that loads, so app count directly affects speed.

Tags: store-setup, app-selection, speed, shopify-app-store, software-evaluation
Source: The OFFICIAL Shopify 2026 Tutorial.docx

---

## Match app choices to the marketing job you need done
Use when: You have outgrown built-in Shopify messaging or need SMS, review collection, pop-up capture or a referral program.
- Email beyond basics: if sending more than 10,000 emails a month, paid platforms become more competitive; the source names Klaviyo for advanced automations across email, SMS, WhatsApp and push, AI tools and support, noting a steeper learning curve.
- SMS: apps such as Postscript and Attentive send opted-in promotional texts; the source cites texts as strong for time-sensitive offers, flash sales, abandoned cart recovery and urgent updates, and quotes a 98% open rate with reads typically within minutes.
- Reviews/social proof: Judge.me and Loox automatically gather ratings with photos and videos, provide customizable widgets, sync to Google Shopping and the Shop app, offer discount incentives and allow importing reviews; the source calls Judge.me a good starting point and Loox a fit for consistent volume with more AI features.
- Pop-ups: Privy is positioned as an all-in-one with pop-ups plus email and SMS; Justuno focuses purely on advanced pop-up conversion, which the source suggests if you already use a platform like Klaviyo and don't want duplicate email tools.
- Referrals: Referral Candy runs referral and affiliate programs and integrates with themes and other apps.
- Check whether a listed SMS feature is available in your market before choosing an SMS app, since Shopify's own SMS support is limited to select markets.
Caveat: App names, pricing and features change; verify current capabilities and costs.
Caveat: The cited 98% SMS open rate is the presenter's figure, not a store-specific result.
Caveat: Avoid stacking overlapping tools (e.g. two email platforms) because of cost and complexity.

Tags: store-setup, app-selection, email-marketing, sms-marketing, social-proof, retention
Source: The OFFICIAL Shopify 2026 Tutorial.docx

---

## Find your largest funnel drop-off with the conversion rate breakdown report
Use when: Traffic is steady but purchases are low and you need to know which funnel stage to fix first.
- Go to Analytics, select Reports, open the category filter and choose Behavior.
- Open the conversion rate breakdown report.
- Read the chart on the right: sessions, sessions with cart additions, sessions that reached checkout, sessions that completed checkout.
- Identify the largest proportional drop. Example from the source: out of 100 sessions, 5 added to cart while 95 left without adding — the drop is before cart, so the leak is on product pages and merchandising, not checkout.
- Fix the stage with the biggest drop first; different stages call for different work (product page visuals/copy vs checkout friction).
- Ask Sidekick targeted questions such as 'Why is my product page conversion rate low?' — it surfaces common causes and suggested fixes you can act on.
- Optimization is continuous: recheck the funnel after changes because what works now can change in months.
Caveat: Stage comparisons are your own data, not industry benchmarks; read proportions within your funnel rather than comparing to another store's numbers.
Caveat: Sidekick insight cards and report locations shift between Shopify releases — verify the current interface.

Tags: store-setup, conversion-optimization, measurement, analytics, funnel, product-page
Source: The OFFICIAL Shopify 2026 Tutorial.docx

---

## Fix product pages: visuals, descriptions, trust signals and CTA
Use when: Your biggest funnel drop is before add-to-cart, or product pages get traffic but don't convert.
- Visuals: add at least 3–5 real images showing multiple angles with working zoom so buyers can see texture and stitching. Consider a product video or 3D model, which Shopify supports free alongside photos. Example from the source: footwear brand Vessi uses four images per product covering all angles, one lifestyle shot in a puddle, plus a 360-degree video. For anything where size or fit matters, include a scale-reference photo.
- Descriptions: lead with benefits and support with features ('so soft you'll forget you're wearing it' over 'made with organic cotton'), include sizing and fit information where relevant, and avoid generic copy with no story.
- Trust: install a review app (the source names Judge.me, Loox and Yotpo) and push for user-generated photos; a murky return policy removes trust — make it clear.
- Price vs perceived value: if the drop sits here, either strengthen value presentation or reconsider the price, since misalignment is one of the three named conversion killers.
- CTA: make Add to cart impossible to miss with high contrast and clear text, and test a sticky add-to-cart button that stays visible as mobile shoppers scroll through description and reviews.
- Consider showing inventory levels when stock is low — 'only three left' creates genuine urgency that can prompt buying now rather than bookmarking.
- Ask Sidekick: 'Analyze my top product page and suggest improvements' to get recommendations based on your actual content.
Caveat: The claim that product pages cause 60–70% of conversion killers is the presenter's framing, not a measured benchmark.
Caveat: Low-stock urgency only works if stock levels are genuine.
Caveat: Review and UGC use requires customer permission where applicable.

Tags: store-setup, product-page, conversion-optimization, social-proof, copywriting, mobile
Source: The OFFICIAL Shopify 2026 Tutorial.docx

---

## Reduce navigation friction with click depth, clear categories and mega menus
Use when: Shoppers can't find products, bounce out of category pages, or you're structuring a menu for a growing catalog.
- Count clicks from the homepage to products; the source's rule is any product should be reachable in two to three clicks maximum. Ask Sidekick to 'show my current navigation menu structure and identify how many clicks it takes to reach products' to get a click-depth analysis and feedback.
- Replace vague category names like 'products', 'shop', or 'items' with plain, descriptive names — 'Women's apparel' tells shoppers what's inside; 'The collection' doesn't. Ask Sidekick to review category names and suggest clearer alternatives for your store's theme.
- For large catalogs, use a mega menu — a large hover drop-down showing multiple categories and featured products at once. Ask Sidekick whether your theme supports mega menus and how to set one up, then preview via the eye icon next to Online Store.
- Add breadcrumb navigation on product and category pages so shoppers see where they are (Home > Women's > Dresses > Summer) and can move back up without the back button; many modern themes include them — check with Sidekick or use a free app such as Breadcrumbs Uncomplicated.
- On mobile, make the search bar prominent by switching the theme editor to mobile view and moving search placement to the top of the header if it isn't already, then save.
Caveat: The two-to-three-click rule is the source's heuristic, not a universal law.
Caveat: Theme capabilities for mega menus and breadcrumbs vary; confirm support before promising the feature.

Tags: store-setup, navigation, conversion-optimization, mobile, ux, merchandising
Source: The OFFICIAL Shopify 2026 Tutorial.docx

---

## Improve site search with predictive text and synonyms
Use when: Shoppers search and get no results, or you sell products with regional/alternative names (e.g. sneakers vs trainers).
- Check whether predictive text is already active by going to your live store view and typing in the search bar — predictive text shows related products as the customer types (typing 'cocoa' surfaces coconut matcha).
- Some themes include it automatically (the source names Horizon); if not, install the free Shopify-made Search and Discovery app and enable custom search suggestions and predictive search.
- Add search synonyms for common misspellings and alternative terms: if you sell sneakers, shoppers searching 'trainers' or 'tennis shoes' should still find the products.
- On mobile, keep the search icon visible in the header — phone shoppers prefer to search rather than browse nested menus.
- Ask Sidekick how to improve navigation on mobile if you're not sure where shoppers are getting lost.
Caveat: Search and Discovery app features and availability vary; confirm in the current app store listing.
Caveat: Synonym lists need maintenance as your catalog and customer vocabulary change.

Tags: store-setup, site-search, navigation, conversion-optimization, mobile, ux
Source: The OFFICIAL Shopify 2026 Tutorial.docx

---

## Diagnose and reduce site speed problems
Use when: Your bounce rate looks high, mobile pages load slowly, or conversions feel capped despite traffic.
- Check the signal first: under Analytics and Reports, open Bounce rate over time; the source treats above 60% as a likely speed problem.
- Test specific pages with Google's free PageSpeed Insights tool to get detailed performance metrics.
- Cut apps: in Apps, Installed apps, audit what is actively used and uninstall disabled or dormant apps (that popup app you tried months ago, the never-activated currency converter). If unsure, ask Sidekick to 'audit my installed apps and identify which ones are slowing down my store' and which to remove or replace.
- Optimize images before uploading: compress with free tools like TinyPNG or Squoosh, keep each image under 200 KB, use JPEG for product photos and PNG for graphics with transparency like logos.
- Handle video carefully: avoid autoplay on the homepage, especially on mobile; make video click-to-play.
- Check your theme: older themes can be replaced with ones built on Shopify's modern theme architecture (the source names the Horizon theme foundation), which use Shopify's CDN to serve images from servers near customers. Check load speed under Online Store, Themes, where Shopify reports milliseconds and a green/yellow/red rating.
- Optimize every element not rated green.
Caveat: The 'every 1 second delay costs around 7% in conversions' figure is cited by the source from studies — treat it as an illustrative estimate, not a guarantee. The source's own $10,000/month example is arithmetic on that assumption.
Caveat: The 60% bounce rate threshold is a heuristic for flagging a possible speed issue, not proof of one.
Caveat: PageSpeed tool output changes over time; interpret scores in context of your own pages.

Tags: store-setup, speed, conversion-optimization, app-selection, images, measurement
Source: The OFFICIAL Shopify 2026 Tutorial.docx

---

## Cut checkout friction: payment options, forms and cost transparency
Use when: The largest funnel drop is between cart/checkout and completed purchase, or abandoned cart rates look high.
- Enable accelerated checkout options — Shop Pay, Apple Pay, Google Pay — in payment settings via Manage payment methods (these auto-fill customer info so buyers check out in seconds). The source calls Shop Pay a standout because returning customers can check out in one click.
- Keep guest checkout on — forcing account creation before purchase kills conversions; the source suggests asking for an account after the purchase instead. Guest checkout is enabled by default in Shopify.
- Minimize form fields: go to Settings, Checkout and ask for only one of email or phone rather than both, and make company name, address line 2, and shipping phone optional. Every extra field is another chance for the buyer to leave.
- Show shipping costs early — surprise costs at the last step kill checkouts. If possible show estimated shipping on product pages or at least in the cart.
- Use the announcement bar to communicate thresholds upfront; in the theme editor, hover the announcement bar, click 'ask for changes' and enter something like 'Add free shipping over $75 to this announcement bar' (a Sidekick-assisted edit).
- If unsure where to focus, ask Sidekick to analyze checkout abandonment and suggest improvements, then review checkout abandonment analytics for specific problems.
Caveat: The ~70% average cart abandonment rate the source cites is an industry-wide figure; much abandonment is normal comparison shopping, not fixable friction.
Caveat: Accelerated payment availability depends on plan, region and buyer device.
Caveat: Free-shipping thresholds are a merchandising choice; the $75 example is illustrative.

Tags: store-setup, checkout, conversion-optimization, payments, cart-abandonment, mobile
Source: The OFFICIAL Shopify 2026 Tutorial.docx

---

## Build checkout trust with badges and concrete delivery dates
Use when: Checkout is where buyers hesitate, or you want clearer expectations to reduce 'where is my order' friction and abandonment.
- Payment logos and SSL padlock appear automatically in the checkout footer once payment methods are enabled, so enabling methods is the first trust step.
- Consider trust-badge apps from the Shopify app store (the source names Essential Trust Badges and Icons, Conversion Bear Trust Badges, Super Trust Badges and Icons) and pick the one that fits your look.
- Add estimated delivery dates: 'Arrives by Thursday' is more compelling than 'standard shipping 5–7 business days' because it is concrete and confident.
- On a professional plan, turn on automated delivery dates via Settings, Shipping and Delivery, Estimated Delivery Dates, selecting Automated, and setting your fulfillment time — Shopify then estimates delivery from carrier transit times.
- For more control, set manual delivery dates by adjusting processing times, transit times on flat-rate shipping, or by using carrier-calculated rates.
- The goal is removing uncertainty so checkout feels easy, clear and trustworthy.
Caveat: Automated delivery dates require specific plans/features; check your plan before promising the feature.
Caveat: Delivery estimates depend on accurate fulfillment and transit settings — wrong estimates create worse post-purchase problems.

Tags: store-setup, checkout, trust-signals, conversion-optimization, shipping, retention
Source: The OFFICIAL Shopify 2026 Tutorial.docx

---

## Set up abandoned cart and abandonment recovery flows
Use when: Customers add to cart or reach checkout then leave without buying, and you want automated recovery without manual outreach.
- Go to Marketing, Automations and confirm 'Recover abandoned checkout' is enabled — Shopify creates the email automatically. Review the design, messaging and recipient list.
- That email typically sends a few hours after abandonment and links directly back to the cart so the buyer can finish in one click; customize content and timing to match your brand.
- Also use the cart-abandonment automation, which fires when a customer adds at least one item and leaves without continuing to checkout. It automatically excludes anyone who received an abandoned checkout or product browse email in the last 14 days, preventing over-emailing the same person.
- Preview each template, edit the messaging and design to match your brand, then turn on the automation.
- For higher-value carts, layer WhatsApp recovery via Shopify Flow: install Flow if needed, browse templates, search for sending a WhatsApp message to recover abandoned checkout, install and turn on the workflow.
- If unsure where to focus, ask Sidekick to analyze checkout abandonment and suggest improvements, then use the abandonment analytics it points to.
Caveat: Automation emails generally go only to customers subscribed to marketing.
Caveat: The 14-day exclusion window is Shopify's default behavior, not a universal rule; review whether it fits your send cadence.
Caveat: Abandoned checkout emails are free under Shopify Messaging even though other campaigns count toward the monthly allowance.
Caveat: WhatsApp recovery involves external apps and regional availability.

Tags: store-setup, abandoned-cart, retention, automation, email-marketing, shopify-flow
Source: The OFFICIAL Shopify 2026 Tutorial.docx

---

## Run a VIP campaign using top products, a segment and an exclusive code
Use when: You want to reward repeat buyers and protect margin instead of sending a blanket discount to everyone.
- Identify bestselling products via Analytics, Reports, Sales by product, or ask Sidekick to 'show me my top five bestselling products'.
- Create a collection for the campaign — ask Sidekick to create an automated collection called Best Sellers VIP with those top products, review the collection details form, adjust title, description or products, preview, then save.
- Define VIPs in Customers, Segments using behavior such as two or more orders or total spend over a threshold like $200.
- Create a discount for the segment — for example ask Sidekick to create a 10% code called VIP10 for orders over $50; under eligibility choose the specific VIP segment; set usage limits (total or one per customer) and the active start and end dates; save.
- Draft the campaign email asking Sidekick to write a subject line and body promoting the VIP collection with the code; review and refine with follow-up prompts like 'make it shorter' or 'add more urgency'.
- Create the email campaign, choose a template, paste the copy, select the VIP segment from step three, review, then send or schedule.
Caveat: The source's reasoning is that blanket discounts give money to buyers who would have paid full price — that's a margin argument, not a measured result.
Caveat: VIP thresholds like two orders or $200 spend are examples; set the ones that match your order economics.
Caveat: Segments, discounts and campaigns depend on having enough identified repeat customers.

Tags: store-setup, retention, segmentation, pricing, email-marketing, personalization
Source: The OFFICIAL Shopify 2026 Tutorial.docx

---

## Test one variable at a time and watch real behavior with heat maps
Use when: You want to improve conversion scientifically rather than guessing, and need to prioritize which element to change first.
- Show half your visitors version A and half version B, then compare performance.
- Test only one element at a time — changing headline, images and button color together means you won't know which change made the difference.
- Worth-testing candidates named by the source: product page layouts, headline copy, add-to-cart button text (e.g. 'Add to cart' vs 'Buy now' vs 'Get yours'), and homepage hero images.
- Run tests for at least two weeks before drawing conclusions, so you have enough data to be confident the result isn't random variation.
- Consider a heat map app such as Lucky Orange or Hotjar to see where visitors click, how far they scroll and what they ignore — this reveals behavior you wouldn't guess and helps prioritize what to optimize next.
- Treat optimization as continuous: what works now can change in a few months, so re-test after meaningful changes.
Caveat: The two-week minimum is a rule of thumb; low-traffic stores need longer to reach confidence.
Caveat: Heat map tools add scripts that can affect speed — weigh the insight against load cost.

Tags: store-setup, experiment-design, conversion-optimization, measurement, analytics, heat-maps
Source: The OFFICIAL Shopify 2026 Tutorial.docx

---

## Keep a weekly marketing routine of one email, your post goal, one data-driven change
Use when: You're managing marketing alongside everything else and need a sustainable weekly cadence rather than launching five strategies at once.
- Send one email per week — an offer, update or story.
- Meet your social media post goal (one to two, or three to four posts, depending on the cadence you set).
- Check the marketing dashboard inside Shopify admin and review: which channel drove the most sessions, which brought sales, and what your conversion rate is.
- Adjust one thing based on that data rather than changing everything.
- Use Sidekick for ideas, summaries, suggestions and pulling reports so the routine isn't entirely manual.
- If you're tempted to start multiple new strategies, start with one, build the habit, then layer in more as you learn what works.
Caveat: This is the presenter's recommended cadence, not a proven universal optimum.
Caveat: Consistency and small tweaks are the stated goal; intensity is explicitly discouraged because of burnout risk.

Tags: store-setup, retention, measurement, email-marketing, organic-social, workflow
Source: The OFFICIAL Shopify 2026 Tutorial.docx

---

## Use Sidekick across setup, analysis and creative tasks
Use when: You need a quick answer or action in Shopify admin without knowing where to click, or you want to move faster on setup, optimization and content.
- Ask plain questions like 'Which attribution should I use for my store?' — the source says Sidekick suggests a model and explains what each measures (awareness, full journey, last touch).
- Delegate analysis: request a marketing section report at the top of the day, ask why product page conversion is low, or ask it to analyze top product pages and suggest improvements.
- Delegate build tasks: creating automated collections, discount codes for segments, subject lines and preview text, or a full VIP campaign email draft.
- Use it for store structure questions: menu structure and click-depth analysis, category naming suggestions, whether your theme supports mega menus or breadcrumbs, and how to improve mobile navigation.
- Use it for app and speed work: audit installed apps and identify which to remove or replace to improve speed and conversions.
- Use it as a setup guide for new features — it will either do the task or walk you through the steps in real time.
- Review anything Sidekick drafts or changes before sending or saving.
Caveat: Sidekick's capabilities, prompts and interface change across Shopify releases; verify the current behavior.
Caveat: AI-generated copy, collections and discounts still need human review for brand voice, accuracy and pricing logic.

Tags: store-setup, sidekick, workflow, conversion-optimization, measurement, automation
Source: The OFFICIAL Shopify 2026 Tutorial.docx

---

## Optimize WordPress permalinks and strip default plugins after install
Use when: You've just installed WordPress and WooCommerce on your host and need to lock down URL structure and plugin bloat before adding products.
- Go to Settings > Permalinks and select 'Post name' so product and page URLs read as /product-name/ rather than /?p=123. This matters for SEO and for customers sharing product links.
- Go to the Plugins screen and use bulk actions to deactivate and delete default plugins that ship with the host's WordPress install and aren't needed (e.g., sample/hello-world plugins, bundled marketing or AI plugins you won't use).
- After permalink changes, verify a product page and a category page load correctly, because some hosts need a .htaccess or server rewrite refresh.
- Confirm your SSL is active before launching checkout, since permalink and rewrites interact with HTTPS redirects on most hosts.
Caveat: The exact plugin names bundled by a host vary; verify which plugins are truly safe to delete before bulk-deleting.
Caveat: Some managed hosts force a permalink structure or manage rewrites themselves.

Tags: store-setup, wordpress, woocommerce, permalinks, plugins, hosting
Source: WooCommerce Tutorial 2026_ Complete MasterClass for Beginners.docx

---

## Set origin-based vs destination-based tax correctly per state
Use when: You're configuring WooCommerce tax rates and need to decide which address WooCommerce should use as the tax basis for each state you sell into.
- Use TaxJar (or a similar reference) to look up each state's tax rule and confirm whether the state is origin-based or destination-based.
- In WooCommerce, go to WooCommerce > Settings > Tax and choose the 'Calculate tax based on' option. For origin-based states, select 'Shop base address' so tax is computed from where your business is. For destination-based states, select 'Customer shipping address' so tax follows the buyer's location.
- Add tax rates with four decimal places (e.g., 7.2500), matching how WooCommerce expects rate entry.
- Test a cart with a shipping address in each type of state to confirm the tax line matches your expectation.
- For multi-state selling, use tax tables/rates per state rather than a single blanket rate.
Caveat: WooCommerce's setting is global; if you ship to both origin- and destination-based states, you need per-state rate tables plus rules, not just one setting.
Caveat: TaxJar data and state rules change; re-verify rates periodically or use an automated tax service for accuracy.

Tags: store-setup, tax, woocommerce, compliance, pricing, checkout
Source: WooCommerce Tutorial 2026_ Complete MasterClass for Beginners.docx

---

## Charge flat-rate shipping per item instead of per order
Use when: You want shipping priced per unit (e.g., heavy or bulky goods) rather than a flat charge for the whole order.
- In WooCommerce, go to Settings > Shipping, create or edit a shipping zone, and add a Flat Rate method.
- In the Flat Rate cost field, enter a formula such as [qty] * 10 where 10 is your per-item dollar amount, so each item adds $10 to shipping.
- Save and test with a two-item and three-item cart to confirm the shipping line scales as expected.
- Combine with shipping classes if different product types need different per-item amounts.
Caveat: [qty] counts total cart quantity; if you need per-weight or per-dimension pricing, use weight/dimension-based rules instead.
Caveat: Free-shipping thresholds or coupons can interact with flat-rate formulas; test combinations.

Tags: store-setup, shipping, woocommerce, flat-rate, cart, fulfillment
Source: WooCommerce Tutorial 2026_ Complete MasterClass for Beginners.docx

---

## Install Stripe and PayPal via dedicated third-party plugins, not defaults
Use when: You're connecting card and PayPal payments and deciding which gateway plugin to install and how to enter API credentials.
- In WordPress, go to Plugins > Add New and search for 'Payment Plugins for Stripe WooCommerce'; install and activate it. Repeat for 'Payment Plugins for PayPal WooCommerce'.
- For Stripe: obtain your Publishable Key and Secret Key from your Stripe dashboard, then in the plugin go to Stripe API Settings, paste the Publishable Key, paste the Secret Key, and run the provided Connection Test.
- Confirm the connection test passes before going live; a failed test usually means a wrong key or a test/live key mismatch.
- Repeat the analogous API-key flow in the PayPal plugin, using your PayPal app credentials.
- Place a live test transaction (small amount) and refund it to confirm the full capture and refund path works before launch.
Caveat: This is the presenter's recommendation; default WooCommerce gateway plugins also exist and may suit simpler setups.
Caveat: Plugin interfaces and menu names change — verify the current settings paths in your installed version.
Caveat: Never paste live secret keys into a shared or test environment you don't control.

Tags: store-setup, payments, stripe, paypal, woocommerce, plugins, checkout
Source: WooCommerce Tutorial 2026_ Complete MasterClass for Beginners.docx

---

## Create global product attributes before building variable products
Use when: You're creating a variable product (e.g., apparel with sizes and colors) and need a repeatable, correctly ordered workflow.
- Go to Products > Attributes and create global attributes (e.g., Weight, Toy Option, Size, Color) with their terms. Do this globally rather than only at the product level so attributes can be reused across the catalog.
- Open the product and set Product data to 'Variable product'.
- Add the existing global attributes on the Attributes tab and check 'Used for variations' for each one you want to generate combinations from.
- Click 'Generate variations' to create the full combination set, then assign each variation its own SKU, image, price and stock.
- Ensure every variation has a price, because a variation with no price is not purchasable.
- Save and check the product page to confirm all desired variations appear and are selectable.
Caveat: Generating all combinations can create many variations for multi-attribute products; prune unused combinations.
Caveat: Global attributes are the recommended pattern, but product-level (custom) attributes still exist and may be fine for one-off products.

Tags: store-setup, products, woocommerce, variable-products, attributes, catalog
Source: WooCommerce Tutorial 2026_ Complete MasterClass for Beginners.docx

---

## Build a Variable Product with Global Attributes
Use when: Adding a product to the catalog that comes in multiple sizes, weights, colors or option types and must be purchasable per variation.
- Create attributes globally first: go to Products > Attributes (not the product-level custom attribute field) and define each attribute such as Weight or Toy Option. Global attributes are reusable across the whole catalog and keep naming consistent, which matters once you have dozens of products.
- Create the product and set its type to Variable product.
- In the Attributes tab, add the existing global attributes, then tick 'Used for variations' on each one. An attribute not marked for variations cannot be used to generate variants.
- Click 'Generate variations' to create the child rows, then assign each variation its own SKU, image and price.
- Verify every variation you want sold has a price; a variation without a price is not purchasable, so it will silently fail at add-to-cart.
- Set stock, weight and dimensions per variation if they differ, then save and test add-to-cart for at least two variations on the front end.
Caveat: Building attributes at product level instead of globally forces you to re-enter them for every new product and causes inconsistent filter/attribute listings later.
Caveat: The product type must be set to Variable before the Attributes tab offers the variation options.

Tags: store-setup, woocommerce, product-catalog, variable-products, attributes, product-page
Source: WooCommerce Tutorial 2026_ Complete MasterClass for Beginners.docx

---

## Install Payment Gateways for Stripe and PayPal
Use when: Preparing a store checkout to accept card and PayPal payments directly on your own domain instead of sending buyers off-site.
- Decide the principle first: the goal is payment processed inside your store. The source recommends not relying on the default WooCommerce payment options and instead installing dedicated gateway plugins — specifically 'Payment Plugins for Stripe WooCommerce' and 'Payment Plugins for PayPal WooCommerce'.
- Install and activate both plugins from Plugins > Add New, searching the exact plugin names.
- Open the Stripe settings and enter credentials in this order: Stripe API Settings, paste the Publishable Key, paste the Secret Key, then run the Connection Test.
- Only move on to checkout testing after the connection test passes; a failed test means keys were mistyped or copied from the wrong Stripe mode (test vs live).
- Repeat for PayPal with its own credentials, then place a real low-value test order to confirm the charge goes through and the order status updates.
- Keep an offline method (e.g. cash on delivery) enabled if you serve local buyers, and enable local/regional gateways per the store's market.
Caveat: Plugin names, settings paths and key labels change between versions — verify the current plugin interface before following a click path.
Caveat: Never publish or share secret keys; rotate them if they are exposed.

Tags: store-setup, woocommerce, payments, checkout, stripe, paypal, ssl
Source: WooCommerce Tutorial 2026_ Complete MasterClass for Beginners.docx

---

## Set Store Address, Selling and Shipping Locations
Use when: Setting up or restricting which countries and regions your store sells and ships to before launching products.
- Go to WooCommerce > Settings > General and set the store address (use your business base if you have no physical store), city, state and postcode. This address feeds tax and shipping logic.
- Under Selling location, choose one of three modes: sell to all countries; sell to specific countries (a whitelist — select each country you serve); or sell to all countries except (a blacklist).
- Pick the shipping location mode. If you sell physical goods, keep 'ship to all countries you sell to' so shipping mirrors your selling whitelist. If the store sells only virtual goods (gift cards, ebooks, digital downloads), choose 'disable shipping and shipping calculations' instead.
- Enable taxes if you will calculate tax rates, and enable coupons if you plan to run discount codes; both add settings tabs you will need afterwards.
- Set the store currency (e.g. USD) — this is the currency all product prices are entered in.
- Save changes, then re-open the settings to confirm the new Taxes/Coupons tabs appeared as expected.
Caveat: Mismatched selling and shipping rules cause checkout errors for valid customers, so review both before launch.
Caveat: The disable-shipping option only makes sense when nothing physical is shipped.

Tags: store-setup, woocommerce, shipping, tax, currency, checkout
Source: WooCommerce Tutorial 2026_ Complete MasterClass for Beginners.docx

---

## Set a Catalog Placeholder Image
Use when: Launching a shop catalog where image uploads may fail or products may lack images, and you do not want empty grey boxes in the grid.
- Upload your desired placeholder graphic to WordPress Media Library (a simple branded tile works).
- Click the image and copy its File URL — this is what WooCommerce needs, an attachment ID or URL.
- Go to WooCommerce > Settings > Products and paste the URL into the Placeholder image field, replacing the default numeric value.
- Save changes, then view the shop page and confirm the placeholder renders wherever a product image fails to load.
Caveat: The placeholder is global: it appears for any product whose image is missing or fails to load, so it should look neutral rather than product-specific.
Caveat: This does not fix the underlying missing image — flag products lacking real imagery separately.

Tags: store-setup, woocommerce, product-catalog, merchandising, media, product-page
Source: WooCommerce Tutorial 2026_ Complete MasterClass for Beginners.docx

---

## Choose Tax-Inclusive or Tax-Exclusive Product Pricing
Use when: Configuring store tax settings before entering product prices, especially for multi-state or multi-country tax rules.
- Open WooCommerce > Settings > Taxes and pick between 'Yes, I will enter prices inclusive of tax' and 'No, I will enter prices exclusive of tax'.
- Understand the consequence with an example: if the intended all-in price is $100 and tax is 5%, inclusive mode means you type 105 as the product price; exclusive mode means you type 100 and the 5% is added at checkout.
- Consider what the shop page shows: inclusive mode displays the tax-included number to shoppers; exclusive mode displays the base price and adds tax later based on the buyer's location.
- Note that the customer's final total is effectively the same either way; only the display and the number you type differ.
- The source prefers exclusive pricing so the store page shows the base price and tax appears at checkout — but this is a presentation choice, so match it to your market convention.
- Set 'calculate tax based on customer shipping address' (the default) if tax should follow where the order ships, then save.
Caveat: Once you have entered many products, switching modes means re-checking every price.
Caveat: Tax display conventions differ by country; what looks correct in one market can look misleading in another.

Tags: store-setup, woocommerce, tax, pricing, checkout, product-page
Source: WooCommerce Tutorial 2026_ Complete MasterClass for Beginners.docx

---

## Build Location-Based Tax Rates with State Rows
Use when: Selling into the US (or any region with sub-region tax rates) and needing checkout to apply the right percentage automatically.
- Look up accurate current rates from a sales-tax reference (the source uses TaxJar's sales tax by state page) rather than guessing — for example California 7.25%, New York 4%, Washington 6.5%.
- In WooCommerce > Settings > Taxes, either use the standard rate table or create a new tax class by typing a name into the additional tax classes field and saving; the new tab appears for editing.
- In the rate table, insert rows: enter the country code (US), then the state code (CA, NY), leave postcode and city blank for a whole-state rule, and enter the rate with four decimal places — write 7.25 as 7.2500 and 4 as 4.0000.
- Give each row a tax name (e.g. Tax) and keep priority at 1 unless you need to stack rules.
- Toggle the shipping option per row: enable it if that state taxes shipping, disable it if not — this varies by state, so decide per rule.
- Add a country-level fallback row with country code US and state code left empty (e.g. 5.0000) so customers in states you have not listed still get taxed; save and test checkout with California and a non-listed state address.
Caveat: Rules can overlap — a California customer matches both the CA row and any US-wide row, so understand priority rather than assuming one silently wins.
Caveat: Rates change; verify against a current source before relying on any number.
Caveat: This covers tax configuration only, not full compliance obligations.

Tags: store-setup, woocommerce, tax, pricing, checkout, measurement
Source: WooCommerce Tutorial 2026_ Complete MasterClass for Beginners.docx

---

## Set Weight and Dimension Units Before Adding Products
Use when: Configuring a store that ships physical goods and will rely on weight/dimension data for shipping rates.
- Go to WooCommerce > Settings > Products > Measurements.
- Pick a weight unit (kilogram, gram, lbs, oz) — the source chose gram — and a dimension unit (meter, centimeter, millimeter, inches), choosing inches in the example.
- Save changes before creating products; units are store-wide, so changing later means re-entering or converting every product's numeric data.
- When creating products, enter weight and dimensions in these units only, and be consistent across the catalog so shipping rules compute correctly.
Caveat: Mixed units across products silently produce wrong shipping calculations.
Caveat: Product-level weight/dimensions won't matter until you configure shipping methods that use them.

Tags: store-setup, woocommerce, measurements, shipping, product-catalog
Source: WooCommerce Tutorial 2026_ Complete MasterClass for Beginners.docx

---

## Enable Customer Registration with Subscriber Role
Use when: Setting up account-based features such as order history, saved addresses, wishlists and logged-in checkout.
- In WordPress Settings > General, tick 'Anyone can register' so shoppers can create accounts.
- Set 'New user default role' to Subscriber, not Administrator, Editor, Author or Contributor. You remain the Administrator; everyone who self-registers gets only subscriber capabilities.
- Save changes, then test by registering a new account and confirming it lands as a subscriber.
- Expect WooCommerce to supply the customer-facing pages — My Account, Cart, Checkout, Shop, Wishlist — after activation; you will customise them rather than build from scratch.
Caveat: Leaving the default role above subscriber is a real security risk — self-registered users could edit or publish content.
Caveat: Some stores deliberately allow guest checkout instead of forcing accounts; this setting enables registration but does not obligate it.

Tags: store-setup, wordpress, woocommerce, user-roles, retention, checkout
Source: WooCommerce Tutorial 2026_ Complete MasterClass for Beginners.docx

---

## Set Post Name Permalinks for Clean Product and Page URLs
Use when: Immediately after installing WordPress and before creating shop, product or blog pages that should rank and be shareable.
- Go to Settings > Permalinks and review the default structures (plain, day and name, month and name, numeric, or post name).
- Understand the difference: plain produces URLs with random numbers and characters; day-and-name embeds the publish date; post name produces short readable slugs such as domain.com/shop.
- Select 'Post name' and save changes.
- Do this early — the source's recommendation is strong on post name because readable URLs look better to shoppers and support search ranking, but changing structure later can break existing links, so pair it with redirects if you switch after launch.
Caveat: Post name is a general good practice rather than a guaranteed ranking factor; content and site structure still drive SEO.
Caveat: Changing permalink structure on a live store requires maintaining redirects so old indexed URLs don't 404.

Tags: store-setup, wordpress, seo, urls, product-page, content
Source: WooCommerce Tutorial 2026_ Complete MasterClass for Beginners.docx

---

## Configure Site Title and Tagline as Positioning Statements
Use when: Setting up a new store and choosing the wording that appears in the browser tab, search results and site header.
- Go to Settings > General and set the Site Title to your store or brand name — it updates the header instantly.
- Write a tagline that is specific and market-facing rather than generic. The source's example: 'best pet food online store in California' — naming the category and the geography.
- Rationale: a specific phrase matches how a shopper might actually search, so the store has a chance of appearing for that kind of query.
- Keep the tagline meaningful and descriptive; avoid filler that says nothing about what you sell or who you serve.
- Save and check the front end to confirm the title and tagline read correctly in the header and title bar.
Caveat: The tagline is a positioning aid, not a guaranteed ranking mechanism — the source frames it as increasing the chance of appearing, not securing a position.
Caveat: Keep it short enough to display cleanly in headers and search snippets.

Tags: store-setup, wordpress, positioning, seo, copywriting, landing-page
Source: WooCommerce Tutorial 2026_ Complete MasterClass for Beginners.docx

---

## Choose a Lightweight Ecommerce Theme and Build with a Page Builder
Use when: Deciding the design stack for a new storefront before you build the homepage, shop and product pages.
- Recognise the trade-off: themes change the whole look-and-feel with one activation but constrain design, while a page builder gives control over every element — the source chose the builder route and built from scratch rather than using a template.
- Install a lightweight theme that still brings ecommerce structure. The source used the free Wooify theme, which provides an ecommerce-friendly sidebar for shop widgets and store customisation options.
- Install the page builder (Elementor) plus supporting add-on plugins for extra widgets and forms (the source added Elements Kit and MetForm), a wishlist plugin (MC Wish List / MoreConvert), a variation swatches plugin, and Classic Widgets for widget areas.
- Activate plugins in the correct order: WooCommerce first, then the variation swatches plugin that depends on it. WooCommerce being inactive blocks dependent plugins from activating.
- Expect WooCommerce to auto-create Cart, Checkout, My Account, Shop and Wishlist pages on activation — these are the pages you will design and configure, not replace.
Caveat: A page builder adds weight and its own update surface; the free version omits the theme builder, popups and form widgets that the pro tiers include.
Caveat: Plugin slugs and names shift between releases — confirm you are installing the current, actively maintained plugin.
Caveat: Build on staging or take a backup before swapping themes on a live store.

Tags: store-setup, wordpress, woocommerce, elementor, themes, product-page, plugins
Source: WooCommerce Tutorial 2026_ Complete MasterClass for Beginners.docx

---

## Back Up and Clean a Fresh WordPress Install
Use when: Right after installing WordPress and before installing store plugins, to start from a clean, secure base.
- Close the welcome popup and either dismiss dashboard widgets individually or use Screen Options to deselect every panel you do not need.
- Go to Plugins, select all default plugins, choose Deactivate from Bulk actions and apply, then select all again and choose Delete — the source deletes the stock plugins as a matter of course.
- Note it is safer to take a backup before bulk deletions; on the recommended hosting plan daily backups are included, so confirm backups are running before you delete.
- Deactivate before deleting — deleting active plugins directly can leave orphaned settings or errors.
- Verify that HTTPS is enforced (Force HTTPS enabled in the hosting panel) so the store serves the secure padlock buyers and search engines expect.
- After installing your store plugin set, reactivate in dependency order, starting with WooCommerce.
Caveat: Some default plugins may be required by the host or by a specific theme; check before deleting.
Caveat: Do not delete plugins you have not identified — the source's approach is bulk deletion of known stock plugins, not indiscriminate removal.

Tags: store-setup, wordpress, plugins, security, backups, ssl
Source: WooCommerce Tutorial 2026_ Complete MasterClass for Beginners.docx

---

## Verify Hosting, Domain and SSL Before Building
Use when: Commissioning hosting and the domain for a new store, prior to installing WordPress and WooCommerce.
- Purchase hosting and claim the included free first-year domain. Choose a term based on budget: the source notes longer terms give bigger discounts and recommends the 48-month lock-in if affordable, but 12 months is fine to start small.
- Register the hosting account with an email you check regularly, because verification codes and domain notices go there.
- Verify the email address for the hosting account and again for the domain registration — the source stresses verification is required to complete domain registration.
- Choose the .com extension for professionalism, checking availability before committing.
- Select the data centre region nearest your target audience when prompted (e.g. a US region for US customers) since this affects site speed for those shoppers.
- Enable Force HTTPS in the hosting panel after WordPress is installed, then log into WordPress admin via the hosting dashboard or by appending /wp-admin to your domain.
Caveat: Term lengths, plan prices and onboarding flows vary and change frequently — treat specific prices or plan names as examples, and verify current terms.
Caveat: Rather than relying on an onboarding wizard's layout, the source goes through the host admin panel so the steps remain findable even when onboarding changes.

Tags: store-setup, hosting, domain, ssl, wordpress, speed
Source: WooCommerce Tutorial 2026_ Complete MasterClass for Beginners.docx

---

## Build Store Front-End Structure That Mirrors Top Ecommerce Sites
Use when: Planning homepage and shop-page sections for a new store, so shoppers can search, browse and buy without friction.
- Header: logo left, navigation menu centre, and search, account and cart buttons right. Make the cart a mini-cart drawer that opens from the side and links to the full cart page.
- My Account should let customers manage orders, delivery addresses and account details so they self-serve instead of contacting you.
- Homepage order used in the build: banner, call-to-action, best-selling products with add-to-cart, a category section, latest products with a countdown offer, testimonials for trust, blog posts, and a footer.
- Shop page: product grid with add-to-cart and wishlist heart buttons, plus sidebar widgets — product search, price filter, recently viewed products, and category/tag filters.
- Product page: name, description, images, variations, a stock progress bar showing remaining stock, quantity selector, add-to-cart, full description, additional information, reviews and related products.
- Cart and checkout: allow removing items and editing quantities in the cart, then checkout with contact details, billing address, payment method choice, a coupon field that discounts automatically, an order summary showing tax, discount, subtotal and total, and a thank-you page after the order is placed.
Caveat: This is a conventional structure the source copied from large marketplaces, not a validated conversion benchmark — treat each section as a hypothesis to test for your catalog.
Caveat: A stock progress bar can create urgency or backfire by discouraging purchase when stock looks low; test it.

Tags: store-setup, merchandising, storefront, product-page, checkout, conversion-optimization, landing-page
Source: WooCommerce Tutorial 2026_ Complete MasterClass for Beginners.docx

---

## Set State and Country Tax Rates with Priority Rules
Use when: Configuring tax tables for a store that ships to multiple US states or countries and you need correct rates at checkout.
- Open WooCommerce > Settings > Tax (verify current label) and create rate rows. Enter a two-letter country code and, for state-level rules, the two-letter state code; leave state empty for a country-wide fallback rule.
- Enter rates in four-decimal format, e.g. California 7.2500 or a source-quoted New York 4.0000, so rounding behaves predictably.
- Build a hierarchy: state-specific rows for states with known rates, plus one country-wide row (e.g. US at 5.0000) as a catch-all.
- Resolve overlap with priority: when a California customer matches both a California row and the US row, the lower priority number wins. The source set California to priority 1 and the country fallback to priority 2, so California paid 7.25%.
- Turn off the shipping-tax flag on rows where you do not want tax charged on shipping cost, then save changes.
- Verify at checkout with a test address in each state before launch, and keep the rate table updated as jurisdictions change.
Caveat: Source caution: lower number = higher priority; getting this backwards silently charges the wrong rate.
Caveat: Use your jurisdiction's official rates; the quoted 7.25% California, 4% New York and 5% placeholder are examples, not current guidance.

Tags: store-setup, tax, checkout, woocommerce, compliance, settings
Source: WooCommerce Tutorial 2026_ Complete MasterClass for Beginners.docx

---

## Use Shipping Zones to Localize Fulfillment Offers
Use when: Deciding what shipping to offer for a whole country versus a specific state or region, and wanting region-specific perks.
- Go to WooCommerce > Settings > Shipping and click Add Zone (verify current interface).
- Name the zone (e.g. 'Whole USA') and search the region list for the country; for a state-level zone search and select the state entry, e.g. California, United States.
- Add a shipping method to the zone and click Continue; repeat per method.
- For a national zone, add a flat rate covering all states. For a narrower zone like California, add a different method such as free shipping with a requirement.
- Attach requirements to free shipping: a valid free-shipping coupon or a minimum order amount. The source example granted California free shipping only above a $400 order.
- Stack zones deliberately: general rules in the country zone, localized perks in the state zone, so a customer sees both applicable options at checkout.
Caveat: The $400 free-shipping threshold is the presenter's example setup, not a recommended benchmark.
Caveat: Zone and method names may differ in your WooCommerce version; confirm labels in the current UI.

Tags: store-setup, shipping, fulfillment, woocommerce, settings, offer-design
Source: WooCommerce Tutorial 2026_ Complete MasterClass for Beginners.docx

---

## Choose Per-Order or Per-Item Flat Rate Shipping
Use when: Setting the delivery cost for a physical product line where shipping multiple units would otherwise be unprofitable.
- In the zone's flat-rate method settings, enter the base cost as a number with two decimals, e.g. 10.00. By default this charges $10 per order regardless of quantity.
- Test the math: with per-order pricing, 10 units still cost $10 total.
- To charge per unit, write the cost as a formula using the quantity placeholder: a bracket-wrapped QTY token, a space, an asterisk, then the unit price. The source used [qty] * 10, so 1 unit = $10, 3 units = $30, 10 units = $100.
- Decide by product economics: bulky or high-cube goods like furniture should use per-item pricing because one bed pack cannot cost the same to ship as three; low-cost repeat-purchase goods like pet food packets can use per-order pricing to make bulk buys attractive.
- Set taxable/none on shipping to match your tax decisions, then save.
Caveat: The formula syntax and placeholder tokens can vary by shipping method and version; verify in your settings before relying on it.
Caveat: Mixing per-order simplicity with heavy goods can erode margin on large orders.

Tags: store-setup, shipping, pricing, woocommerce, fulfillment, margin
Source: WooCommerce Tutorial 2026_ Complete MasterClass for Beginners.docx

---

## Create Shipping Classes for Heavy or Premium Packaging
Use when: Storing products whose packaging weight or cost differs materially from the standard packaging, e.g. premium or heavy packs.
- In WooCommerce > Settings > Shipping > Classes, click Add Shipping Class (verify current labels).
- Name it for the customer-facing consequence (e.g. Premium Shipping), give it a unique slug, and describe what it covers, such as heavy packages.
- Return to the zone and edit the flat-rate method; a shipping-class cost field appears alongside a no-shipping-class cost.
- Enter the premium class price (source example: $20) and the default no-class price (source example: $10), so products without a class fall back to $10.
- Assign the class per product later on the product's Shipping tab, or assign it to a whole variable product so all variations inherit it.
- Review margins: raising a class rate is the lever for heavy packaging; keeping a low default keeps light goods competitive.
Caveat: The $10/$20 figures are the presenter's illustrative numbers; price from your own carrier rates.
Caveat: Only one class applies per product, so plan classes around your main cost drivers.

Tags: store-setup, shipping, fulfillment, woocommerce, pricing, margin
Source: WooCommerce Tutorial 2026_ Complete MasterClass for Beginners.docx

---

## Enable Cod and Verify Stripe and PayPal Setup
Use when: Turning on payment methods in a new store and connecting gateway accounts safely.
- In WooCommerce > Settings > Payments, enable offline methods such as direct bank transfer, check payments and cash on delivery; the source treated COD as a popular, easy win.
- Install and activate a Stripe plugin and a PayPal plugin from the plugin repository (the source chose the 'payment plugins' vendor versions; verify current vendor and compatibility).
- For Stripe: log into the Stripe dashboard, open Developers > API keys, copy the publishable key and secret key, paste them into the plugin's API settings, then run the connection test.
- While testing, stay in test mode and confirm a successful connection message before touching live keys.
- For go-live, switch the Stripe account to live mode, complete identity/bank verification, select live mode in the plugin too, and replace keys with live ones.
- For PayPal: use API settings with production (not sandbox) environment and paste production client ID and secret, or use Connect to PayPal and log in to link automatically; confirm the status reads connected.
Caveat: Plugin menu names and OAuth flows change; verify the current steps in the plugin UI. Never paste live keys while the plugin is still in test mode, and vice versa.

Tags: store-setup, payments, checkout, stripe, paypal, woocommerce
Source: WooCommerce Tutorial 2026_ Complete MasterClass for Beginners.docx

---

## Configure Accounts and Checkout Login Options
Use when: Setting account and checkout behaviour for a new store to balance frictionless purchase against account-based retention.
- Open WooCommerce > Settings > Accounts and Privacy (verify label).
- Enable guest checkout so buyers can complete an order without registering; the source calls this recommended.
- Enable login during checkout so returning customers can sign in from the cart/checkout flow.
- Allow account creation during checkout and on the My Account page so new buyers can register in one step rather than after the fact.
- Leave remaining defaults unless you have a specific need; the source kept them as-is.
- Save changes and test the whole path: add to cart as a guest, checkout, then confirm the account was created so order history, downloads and addresses are available.
Caveat: Guest checkout trades some account data capture for higher completion; if subscriptions or repeat purchases dominate, weigh whether requiring an account is worth the friction.

Tags: store-setup, checkout, account-creation, retention, woocommerce, settings
Source: WooCommerce Tutorial 2026_ Complete MasterClass for Beginners.docx

---

## Turn On Transactional Email Notifications Per Event
Use when: After orders start flowing, when customers report missing confirmations or you want branded status emails.
- Open WooCommerce > Settings > Emails and review each event: new order, cancelled, failed, on hold, processing, completed, refunded, and customer-facing copies.
- Identify the recipient for each: admin events go to your store email address, customer events go to the buyer.
- Enable each notification you want by opening Manage and using its enable toggle, then save; the source noted disabled notifications simply never send.
- Edit the recipient address, subject line, heading, and additional content to match your brand tone; the source edited a cancellation email's heading and closing line.
- Adjust the email colour palette so the template matches your store branding.
- Confirm both sides of a two-step flow, e.g. an order cancellation first notifies the admin and then, once confirmed, notifies the customer.
Caveat: Email delivery depends on your host or SMTP provider; if mail lands in spam, fix sending infrastructure rather than the templates.

Tags: store-setup, emails, retention, customer-experience, woocommerce, settings
Source: WooCommerce Tutorial 2026_ Complete MasterClass for Beginners.docx

---

## Keep the Store in Coming Soon Until Catalogs and Pages Are Ready
Use when: Building a store before launch and deciding when customers should be able to reach it.
- Find the visibility setting (the source used WooCommerce > Settings > Site Visibility; verify current location) and confirm it currently reads Coming Soon.
- While in Coming Soon, build the tax, shipping, payment, product and design work with real settings and products.
- Before switching to Live, complete a full purchase test: add to cart, checkout with each payment method, apply a coupon, confirm emails and download links arrive.
- Set a static homepage and confirm navigation, cart, checkout and My Account pages all resolve.
- Switch visibility to Live and save; the dashboard status should change to show the store is live.
- Treat launch as the last step, not a first one: the source deliberately published products, tested purchase flow, then went live.
Caveat: Coming Soon blocks search-engine and customer access, so switch it off only when products, pages and payments are verified.

Tags: store-setup, launch, settings, woocommerce, checkout, customer-experience
Source: WooCommerce Tutorial 2026_ Complete MasterClass for Beginners.docx

---

## Fill Store Details and Page Assignments in Settings
Use when: Finalizing store identity and confirming the cart, checkout, account and policy pages WooCommerce uses.
- In the point-of-sale/store settings area, replace the default store name with your brand name.
- Add the physical store address, phone number and email if you operate a physical location; these feed documents and contact details.
- Paste your refund and return policy text in the provided field so it can surface where policies are referenced.
- Under Advanced > Page Setup, verify the Cart, Checkout and My Account pages are assigned; the source kept WooCommerce defaults because they worked and looked fine.
- Assign a Terms and Conditions page; until you write one, the source temporarily selected the privacy policy page and planned to swap it once the real page existed.
- Save and click through each assigned page on the front end to confirm it loads and behaves.
Caveat: Do not leave a borrowed policy page as your terms permanently; replace it with accurate terms before launch.
Caveat: Interface labels for store details and page setup can move between versions.

Tags: store-setup, settings, legal-pages, woocommerce, customer-experience, checkout
Source: WooCommerce Tutorial 2026_ Complete MasterClass for Beginners.docx

---

## Create a Simple Physical Product With Pricing, SKU and Stock
Use when: Adding standard physical products to the catalog at initial setup.
- Go to Products > Add New, enter the product name and edit the auto-generated permalink slug only if needed.
- Write the rich-text description (headings, bold, lists) that appears in the product's main description area.
- In Product Data choose Simple. Set regular price and sale price with two decimals; the sale price displays as the active price with the original struck through.
- Set tax status to taxable and pick the tax class you built earlier so the product inherits your state/country rate logic.
- Add a unique SKU: the source built it from the title, lowercased, spaces replaced with hyphens, plus a sequence number (e.g. canine-crunch-01) so later variants become 02, 03.
- Enable stock management and enter quantity so the product page shows e.g. 10 in stock.
- On the Shipping tab enter weight in grams and length/width/height of the full package, not the bare product, then attach a shipping class or leave none for the default rate.
- Assign categories and tags for on-site search, set the thumbnail and gallery images, add a short description, and publish; then view /shop to confirm it appears.
Caveat: Measure the shipped package, not the item, or carrier rates will be wrong.
Caveat: SKU conventions are the presenter's suggestion; any unique, consistent scheme works.

Tags: store-setup, product-page, catalog, shipping, woocommerce, merchandising
Source: WooCommerce Tutorial 2026_ Complete MasterClass for Beginners.docx

---

## Build Variable Products from Global Attributes
Use when: Selling a product in multiple sizes, weights or bundle options where price and stock differ per option.
- Create attributes globally under Products > Attributes so they are reusable across products; the source created a Weight attribute with button type and terms 200g, 400g, 600g, and a Toy attribute with radio type and terms with-toy/without-toy.
- On the product, choose Variable, then use Add Existing to attach attributes and select their values, saving attributes each time.
- Click Generate Variations to auto-create every combination (two attributes with 3 and 2 values produced 6 variations).
- Open each variation and set its thumbnail, unique SKU, price, weight, shipping class and tax class; class and tax class set at the top level apply to all variations unless you override.
- Price by value logic: the source charged less for without-toy and more for larger weights, illustrating that option differences should be reflected in price.
- Set the parent product's short description, thumbnail, gallery, categories and tags, publish, then check the product page shows Select Options, the price range (e.g. $37–$68) and that switching options updates price.
Caveat: The source's per-variation pricing accidentally inverted the with-toy/without-toy logic, showing that option-price mapping must be reviewed.
Caveat: Many attributes multiply variation count quickly; too many combinations make maintenance heavy.

Tags: store-setup, product-page, variants, merchandising, pricing, woocommerce
Source: WooCommerce Tutorial 2026_ Complete MasterClass for Beginners.docx

---

## Create Virtual Downloadable Products for Digital Goods
Use when: Selling ebooks, guides, templates or other digital files in the store.
- Add a new product and keep it Simple, then tick Virtual: the shipping fields disappear because nothing ships.
- Tick Downloadable and add files either by pasting a URL or choosing a file from the media library; the source inserted a PDF and attached its file URL.
- Set regular and sale price as for a physical product, and assign the appropriate tax class.
- Decide download limits and expiry: the source left downloads unlimited and expiry at never; if you want controlled access, set a limit or day count.
- Skip stock management because digital goods do not deplete; give the product a SKU such as ebook-01.
- Link the digital product to other products as upsells/cross-sells, add a short description, thumbnail, tags and publish.
- After a test purchase, verify the order confirmation page exposes the download button and the file opens.
Caveat: Unlimited downloads and no expiry make sharing easy; if piracy matters, set limits and expiry or use protected delivery.
Caveat: File hosting and link stability affect delivery; host files somewhere durable.

Tags: store-setup, digital-products, fulfillment, product-page, woocommerce, retention
Source: WooCommerce Tutorial 2026_ Complete MasterClass for Beginners.docx

---

## List Affiliate Products as External Products
Use when: Monetizing affiliate programs by merchandising partner goods without fulfillment responsibility.
- Add a new product and choose External/Affiliate in Product Data.
- Paste your affiliate product URL in the product URL field; this is where the purchase button sends visitors.
- Set the button text to set expectations, e.g. 'Buy from Amazon'; the source used exactly that phrasing.
- Enter the partner's displayed price so listings look comparable, and skip tax status/class because the transaction occurs off-site.
- Add a description, short description, a product image you are allowed to use, and categories/tags, then publish.
- On the front end, confirm the button reads as intended and opens the partner page in the expected way.
Caveat: Commission is earned only when the tracked link converts; the source frames this as an example, not a guaranteed revenue channel.
Caveat: Check partner program terms for image and price display rules.

Tags: store-setup, affiliate, monetization, merchandising, woocommerce, product-page
Source: WooCommerce Tutorial 2026_ Complete MasterClass for Beginners.docx

---

## Use Upsells and Cross-Sells to Raise Cart Value
Use when: Configuring related-product recommendations on product pages and in the cart.
- On the product's Linked Products tab, add products to Upsells; the source says these surface in the cart as 'you may be interested in' suggestions tied to the viewed product.
- Add products to Cross-Sells; these render as 'you may also like' style recommendations connected to the cart contents.
- Build the catalog first: the source could not demonstrate upsells/cross-sells on the first product because no other products existed yet.
- Add complementary logic, not duplicates: pair the ebook guide with food, or an accessory with the main item, so the suggestion is relevant.
- After publishing, buy-through once to confirm both recommendation blocks appear in the cart and product page.
Caveat: Recommendations only work once there are other published products to select.
Caveat: The source notes upsell/cross-sell placements are tied to how WooCommerce renders them, which theme customization can change.

Tags: store-setup, merchandising, cart, upsell, woocommerce, conversion-optimization
Source: WooCommerce Tutorial 2026_ Complete MasterClass for Beginners.docx

---

## Configure Coupon Type, Restrictions and Usage Limits
Use when: Running a promotional discount and controlling who can use it, on what, and how often.
- Go to Marketing > Coupons > Add New and set the customer-facing code (e.g. JFD20) plus an internal description.
- Pick a discount type: Percentage Discount applies a percent of order or product value (20% of $100 = $20), while Fixed Cart/Fixed Product Discount subtract a flat amount regardless of price.
- Optionally set an expiry date so the promotion ends automatically.
- Use usage restrictions to steer behaviour: minimum spend (e.g. $200) makes the coupon unusable below the threshold; maximum spend (e.g. $500) switches it off above a ceiling because a large percentage becomes expensive; the source left both off.
- Include specific products/categories to target the offer, or exclude products/categories to protect low-margin lines.
- Set usage limit per coupon (total redemptions, source example 10) and usage limit per user (source example 10 per customer), then publish.
- Verify in checkout by applying the code and confirming the discount line and new total update.
Caveat: High percentages plus no maximum spend can gut margin on large carts; maximum-spend ceilings exist for that reason.
Caveat: Limits and thresholds shown are the presenter's examples, not recommended defaults.

Tags: store-setup, pricing, promotions, checkout, woocommerce, offer-design
Source: WooCommerce Tutorial 2026_ Complete MasterClass for Beginners.docx

---

## Run an End-to-End Purchase and Order Management Test
Use when: Before going live, and whenever payments, tax, shipping or emails change.
- As a shopper, add several product types: a simple product, a downloadable product and a variable product with a chosen option; manage quantities from the mini-cart and full cart.
- Open the cart page and read the totals breakdown: subtotal, shipping (flat rate), tax and estimated total, confirming each reflects your settings.
- Proceed to checkout, enter contact and shipping details, choose the shipping method, select a payment method (cash on delivery, Stripe card or PayPal), and optionally add an order note.
- Apply the coupon in the order summary and confirm the discount and new total, e.g. a 20% code reducing the total.
- Place the order and inspect the thank-you page for order details and, for digital products, the download button.
- As admin, go to WooCommerce > Orders, open the order, review items and prices, then set status (pending, on hold, completed, cancelled, refunded, failed) and update; shipping happens before marking completed, and the customer is notified.
- Check the My Account area for order history, downloads, addresses and payment methods as the customer sees it.
Caveat: Test mode payments do not move real money; repeat key checks with live credentials before relying on the flow.
Caveat: Order status wording and available statuses may vary with installed extensions.

Tags: store-setup, checkout, orders, testing, woocommerce, fulfillment
Source: WooCommerce Tutorial 2026_ Complete MasterClass for Beginners.docx

---

## Set a Static Homepage Before Building the Storefront
Use when: After creating the homepage page and before designing it in a page builder.
- Go to Pages > Add New, title it Home and publish; it can be empty at first.
- Open Settings > Reading and under homepage display change from latest posts to a static page, then select the new Home page as the homepage.
- Save changes and visit the bare domain to confirm the Home page loads instead of a blog roll.
- Then open the page with the Elementor editor (or your page builder) to design it.
- Note that default WooCommerce pages such as cart, checkout and my account already exist; leave them assigned and do not overwrite them with the homepage.
Caveat: Changing homepage display later requires re-selecting the page; if the root looks empty, check this setting first.
Caveat: Page-builder menu names and locations shift across versions.

Tags: store-setup, homepage, landing-page, wordpress, pages, launch
Source: WooCommerce Tutorial 2026_ Complete MasterClass for Beginners.docx

---

## Know Free Page Builder Versus Pro Widget Boundaries
Use when: Planning how to build product and homepage sections without buying pro, and deciding whether add-on widget plugins are needed.
- In the editor sidebar, inventory the free widgets: containers, grid, heading, image, text editor, video, button and similar basics.
- Scroll to the pro group to see advanced widgets like search, posts, portfolio, gallery, loop and carousel; these will not be available on the free tier.
- Plan sections using free equivalents: build image grids and headings manually rather than expecting a loop or portfolio widget.
- Consider add-on widget plugins such as the source's Elementskit to expand available widgets if the free set is insufficient.
- Check compatibility and performance before stacking multiple widget plugins, since each adds weight and update risk.
Caveat: Feature tiers and widget lists change; verify what your installed version includes.
Caveat: The source mentions a paid template marketplace; evaluate whether templates or building from scratch fits your time budget.

Tags: store-setup, page-builder, elementor, homepage, landing-page, tooling
Source: WooCommerce Tutorial 2026_ Complete MasterClass for Beginners.docx

---

## Build a WooCommerce Homepage Banner in Elementor with Containers
Use when: Building or rebuilding the hero/banner section of a WooCommerce storefront homepage in Elementor, or deciding how to structure the top-of-page offer area.
- Start from an empty Elementor canvas: add a container, rename it 'banner section' (renaming is organisational only, it has no functional effect but keeps structure navigable).
- Set the banner container to content width 'boxed' at 1240px, gaps 0, background color classic (e.g. a beige #FFF8F0), and padding of 20px left/right and ~132px bottom to create breathing room.
- Nest a 'top area' container inside it, set direction row, width 100%, padding-top ~34px, padding-bottom ~104px.
- Split the top area into three inner containers: left (~32.6% width, holds product imagery), middle (~31.5% width, holds headline copy and button), right (~31.2% width, justify-content end, holds visual accents).
- For the headline use a Heading widget with a heavy weight (source used 96px size, 800 weight, tight line-height ~108px and negative letter spacing for a compact editorial look) so the store's value proposition reads as the dominant page element.
- Add a CTA Button widget linking to the shop page (type 'shop' in the link field and select the suggested page). Add an SVG icon via Upload SVG with ~12px icon spacing, 50px border radius for a pill shape, and brand background colour.
- Add a social-proof cluster: image + Counter widget (source showed '40k+' regular customers). Use number suffix for 'k+' and style the label separately. This is a trust element placed inside the hero, not a separate section.
- If the section doesn't span the viewport, fix it with Page Settings > Page Layout > Elementor Full Width, and set a global page background colour under Page Settings > Style so individual sections don't each need their own fill.
- Use position:absolute on decorative images (Advanced tab > Position) with horizontal/vertical offsets — e.g. right/-15, top/-15 — so they overlay without consuming layout space.
- Set the outer bottom area container to direction row, justify-content space-between, align-items center for a balanced footer strip within the banner.
Caveat: The specific pixel values (1240px, 96px type, 132px padding) are the presenter's chosen design values for one project, not performance-proven numbers — adjust to your brand and test on real devices.
Caveat: The source used Elementor v3.33.6 for stability; the newest version at time of recording (4.0.1) was considered unstable, so pin to a known stable version during build.

Tags: store-setup, elementor, homepage, landing-page, container-layout, cta, social-proof, woocommerce, responsive-design
Source: WooCommerce Tutorial 2026_ Complete MasterClass for Beginners.docx

---

## Roll Back Elementor to a Stable Version Before Building
Use when: Before starting or resuming a storefront build when a page builder has just released a major version and layouts, widgets, or third-party add-ons may break.
- Confirm your builder version: open the editor, click the Elementor logo and read the version indicator in the panel.
- Exit to the WordPress dashboard via the logo menu, and hover over Elementor > Tools (this is where version control lives in the interface at time of recording — verify the current location as Elementor's menu can change).
- Open Version Control, choose 'Rollback Version', select the specific version you want (source used 3.33.6), and click Reinstall, then Continue.
- Close and reopen the editor tab, refresh, and confirm the older version is active before you build anything.
- Complete the whole build on the stable version; you can update to the newest release afterward once it settles.
- Publish frequently during the build so a refresh, browser crash, or closed tab doesn't cost you design work.
Caveat: Version numbers cited (3.33.6 stable, 4.0.1 unstable) are from the recording date; check the current release status yourself before pinning.
Caveat: The exact menu path (Elementor > Tools > Version Control) is UI-dependent and should be verified in your current installation.

Tags: store-setup, elementor, wordpress, version-control, build-reliability
Source: WooCommerce Tutorial 2026_ Complete MasterClass for Beginners.docx

---

## Speed Up Store Builds with Elementor Global Colors and Global Fonts
Use when: When first configuring a WooCommerce theme/page builder so that every subsequent product section, category block, or landing page is faster to build and visually consistent.
- Open the editor's site settings (Elementor > Site Settings > Global Colors) and reassign the defaults: put your most-used brand colour into Primary, your accent/CTA colour into Secondary, paragraph colour into Text, and the accent colour you reuse most into Accent.
- Under Global Fonts, set all four typography slots (Primary, Secondary, Text, Accent) to your brand typeface so new headings and paragraphs pick it up automatically instead of you re-selecting fonts each time.
- Under Site Settings > Layout, set Content Width to your design width (source used 1240px from a 1140px default), set default container padding to 0 and default gaps to 0 so each new container starts clean.
- Save changes, close the panel, then Publish and refresh the page — global settings don't apply to the already-loaded editor until you reload.
- After reload, add a new container and confirm the width and zero-gap defaults are inherited; this is the fastest ongoing check.
- Create reusable global colours inside the individual typography/colour pickers (the plus icon) for any brand tone you use repeatedly, e.g. a named 'black' text colour and 'orange' CTA colour.
Caveat: Global settings only take effect after a page refresh; forgetting to publish first risks losing unsaved work.
Caveat: Some widget typography fields (e.g. the countdown widget in the source) don't inherit the global font family by default and require selecting a custom/global font manually.

Tags: store-setup, elementor, design-system, global-settings, workflow, branding
Source: WooCommerce Tutorial 2026_ Complete MasterClass for Beginners.docx

---

## Use Position Absolute + Offsets to Place Decorative Store Images Precisely
Use when: Layering product photos, badges, paw prints, or accent graphics over a hero, category block, or promo box where images must overlap copy or each other at exact coordinates.
- Add the image widget where it belongs in the structure, then open Advanced > Positioning and set Position to Absolute.
- Set Horizontal Orientation (left/right/center) plus an offset in px, and Vertical Orientation (top/bottom/center) plus an offset. Example from source: right/-15 horizontally and top/-15 vertically to overlap a corner.
- Instead of offsets, you can also drag the image by hand once it is absolute — useful for eyeballing decorative placements, but switch to numeric offsets for values you want to reuse across breakpoints.
- For images that sit over a solid or branded section, use Style > CSS Filters to recolour them without a new asset: setting Contrast to 0 makes the image grey, and lowering Opacity (source used 0.7) softens it against the background.
- Give absolutely-positioned decorative images explicit Custom width/height in px (e.g. 96px, 49px, 52px) so they scale predictably.
- To stack avatars/thumbnails in a row, apply a negative margin (source used -35px) to pull the overlapping image over its neighbour.
- Set a text caption or label over an image by making the Heading widget absolute as well (source used right offset 28, top offset 56) rather than adding a background layer.
Caveat: Absolute positioning removes the element from layout flow, so sibling containers won't reserve space for it — verify each breakpoint separately or decoratives will overlap badly on mobile.
Caveat: Drag-and-drop positioning is not remembered per breakpoint; only numeric offsets are reliable across desktop/tablet/mobile.

Tags: store-setup, elementor, positioning, merchandising, product-page, visual-design
Source: WooCommerce Tutorial 2026_ Complete MasterClass for Beginners.docx

---

## Embed Best-Selling and Latest WooCommerce Products via Shortcode
Use when: Adding a best-sellers or new-arrivals rail to a homepage, landing page, or category page without hand-picking products that go stale.
- Add a Shortcode widget inside a container on your page.
- Get the shortcode code from the WooCommerce documentation (source showed 'product shortcode for best selling product' and 'for latest product' as distinct copy-paste lines — verify the current shortcode names and arguments in WooCommerce docs, as they can change).
- Paste the full shortcode line into the widget's shortcode field and the products load automatically from your catalogue.
- If product images render doubled/tall in the editor, ignore it — the source notes this is an editor display glitch that resolves on the published front end.
- Leave default shortcode styling for now; the raw output looks unfinished and is meant to be styled via WooCommerce/theme customization once you move to dashboard styling.
- For a 'latest products' rail, use the latest-products shortcode; for best sellers, use the best-selling one — don't manually reorder products to fake 'latest' since a real shortcode keeps the rail current as new items publish.
Caveat: Shortcode names, parameters, and styling behaviour are WooCommerce/plugin dependent and can change between versions — confirm in current docs.
Caveat: Default shortcode output is unstyled and will look broken until product title, price, and card layout are customized.

Tags: store-setup, woocommerce, shortcodes, merchandising, homepage, product-listing
Source: WooCommerce Tutorial 2026_ Complete MasterClass for Beginners.docx

---

## Import a Prebuilt Elementor Template (e.g. Reviews Section) Instead of Building From Scratch
Use when: Adding a common but tedious store section such as testimonials/reviews, contact, or FAQ where you already have a saved design file.
- Click the folder/Add Template icon in the Elementor panel, then use the Upload Template option and drag in your saved template JSON files.
- If a template fails to appear after a batch upload, re-upload the missing one individually (source had to re-upload the review section).
- Click Insert to drop the template in as a new section.
- Expect it to look messy in the editor — the source says evaluate it on the front end, where the layout resolves correctly.
- Customize editorial copy by selecting the text elements directly, and customize the testimonial widget via its Style tab (column gap, background colour, active background colour) and Content tab (description text, typography, text colour).
- Treat the imported template as fully yours — every element remains editable, so adapt spacing and colours to your globals rather than leaving template defaults.
Caveat: Templates carry their own typography and colour values, so you will need to re-map them to your global colours/fonts for brand consistency.
Caveat: The upload interface and icon location are Elementor-version dependent — verify in your version.

Tags: store-setup, elementor, templates, testimonials, retention, workflow
Source: WooCommerce Tutorial 2026_ Complete MasterClass for Beginners.docx

---

## Build a Countdown-Timer Promo Box for Offers and Drops
Use when: Running a time-limited promotion, flash sale, or product drop on a homepage or campaign landing page where urgency is part of the offer.
- Create a box container with a brand background colour (source used #F0D8B2) and a border radius (16px) so it reads as a distinct promo unit; give it balanced padding (source used 55/36/55/36).
- Add a Heading (offer title), a subheading (terms/description), the Countdown widget, and a Button inside the box.
- In the Countdown timer settings, set the exact expiration date and time. The widget counts down from now until that moment; on expiry the Expire Action shows a custom title and message you write.
- Customize the unit labels (days/hours/minutes/seconds) if your audience needs different wording, though the defaults are usually clear.
- For a flat look, remove the widget's background by setting the background type to classic and the colour to fully transparent (source did this so the timer matched the promo box).
- Style the digit and label separately: source set digits ~36px/700 weight/48px line height, labels ~20px/500 weight/30px line height, and saved these as typography presets so each of the four units could be restyled in one click.
- Set a top margin (~40px) to separate the timer from copy, and add a CTA button (source reused the hero button via copy/paste then centred it).
Caveat: The countdown widget in the source came from a third-party plugin (Elements Kit), not Elementor core — availability and settings depend on which add-on you install.
Caveat: Saved typography presets are what make the four-unit styling fast; without them, each unit must be styled manually.
Caveat: Urgency timers should only flag genuine deadlines; resetting a timer arbitrarily undermines the trust the offer depends on.

Tags: store-setup, elementor, countdown, promotion, landing-page, offer-design, conversion-optimization
Source: WooCommerce Tutorial 2026_ Complete MasterClass for Beginners.docx

---

## Build a Category Showcase Section with Floating Badges
Use when: Building a homepage or landing page category block that routes shoppers into top-level product categories (e.g. dog food, cat food).
- Create a section container with generous padding (source used 132/20/68/20) and add floating decorative images using absolute positioning (e.g. left -41/top 90; left 40/top 70; right -140/bottom 40) — they can sit outside the visible flow and settle into place once content is added.
- Inside, make a row container with justify-content center to hold the category tiles.
- For each tile: add a category image, then a Heading widget for the category name. Use a BR tag in the heading text to force a deliberate line break rather than letting it wrap arbitrarily.
- Style the heading with centre alignment and a bold weight (source used 36px/700, tight line-height 45px, negative letter spacing -2.52px) then make it absolute with right/bottom offsets so it sits on the image as a badge.
- Give the badge a coloured, rounded background: background type classic with your secondary/brand colour, then a border radius of 50% for a pill/circle shape. Give it padding (source used 41px top/bottom) and a set pixel width (~172px).
- Duplicate the whole group to create additional tiles, then just swap the image and the heading text and change the badge colour — this is the fastest way to keep badge sizing consistent across categories.
Caveat: Badges depend on precise absolute offsets; changing tile image aspect ratios later will require re-tuning those offsets.
Caveat: Keeping the badge text short matters — long category names will overflow the fixed-width pill.

Tags: store-setup, elementor, merchandising, category-page, navigation, homepage, visual-design
Source: WooCommerce Tutorial 2026_ Complete MasterClass for Beginners.docx

---

## Make Elementor Store Sections Responsive Without Breaking Desktop
Use when: After building a desktop store homepage/section, when it breaks on tablet or mobile and you need to correct it without regressing the desktop layout.
- Switch the editor to Tablet or Mobile mode at the bottom of the panel — edits you make in a breakpoint apply only to that breakpoint and below.
- Adjust outer section padding per breakpoint: source changed the banner's bottom padding from 104px to 90px on tablet, then set all-round padding to roughly 20/70/20 on mobile.
- Reduce hero typography on smaller screens: the source dropped the main heading from 96px to 72px (line-height 86px) on tablet, then to 64px (line-height 72px) on mobile.
- Fix multi-column rankings by changing each container's width per breakpoint (source: three hero columns 30%/32%/24% on tablet, then 48%+48% on mobile so two items share a row).
- When a block needs to move position on mobile only, DO NOT drag it — dragging changes the desktop order too. Instead, open Advanced > Order and set it to 'end' (or a number) so it reorders only for that breakpoint.
- Add breakpoint-specific spacing with margin (source added 30px bottom margin on mobile to push the second hero block down).
- Use per-breakpoint image controls (width slider) to reposition decorative images like paw graphics so they land sensibly at mobile widths.
Caveat: Edits made while in a smaller breakpoint cascade downward, so always check mobile after changing tablet.
Caveat: Drag-and-drop reordering inside a breakpoint is a common mistake the source warns against — use the Order property instead.

Tags: store-setup, elementor, responsive-design, mobile, breakpoints, homepage, workflow
Source: WooCommerce Tutorial 2026_ Complete MasterClass for Beginners.docx

---

## Set a Global Page Background and Full-Width Layout Once Per Page
Use when: When a store homepage or landing page needs a consistent background and its sections must span the full browser width.
- Open Page Settings (the gear/editor settings) and go to the Layout section.
- Under Page Layout, change from 'Default' to 'Elementor Full Width' so sections stretch edge-to-edge; the source used this to remove leftover side gutters.
- Go to the Style tab of Page Settings and set a global page background colour (the source used a soft cream) so you don't have to add a background to every section.
- Because the global page background gives the base colour, sections then only need their own distinct background where the design calls for a different tone (e.g. a pink promo band or beige hero).
- Apply these page-level settings once per page and build sections on top; this keeps the page background consistent even as you add, delete, and duplicate sections.
Caveat: Full-width layout changes how the 1240px content-width containers render, so verify hero spacing after switching.
Caveat: A global page background overrides the visual expectation of an empty section — sections intended to look 'plain' will now be cream, not white.

Tags: store-setup, elementor, page-settings, layout, homepage, design-system
Source: WooCommerce Tutorial 2026_ Complete MasterClass for Beginners.docx

---

## Use Negatives Margins and Order to Control Store Section Spacing
Use when: Tightening or separating elements within a product hero, promo box, or footer strip where default gaps look wrong.
- Use the Advanced > Margin control (unlink it) for element-level spacing: the source added 100px top / 50px bottom margin to a button to pull it away from surrounding content.
- Use padding on the parent container to create interior breathing room around a group, and keep child margins for finer control within the group.
- Use negative margins to overlap elements deliberately, e.g. -35px to pull one avatar/thumbnail onto the previous one for a stacked look.
- To reorder items on one breakpoint only, use Advanced > Order; to reorder across all breakpoints, physically drag the widget in the Structure tree.
- Check the Structure panel to confirm nesting is correct before styling — many spacing problems are caused by a widget being nested one level too deep (the source repeatedly moved widgets out of the wrong parent container).
- Name containers ('banner section', 'top area', 'title', 'count') so you can find and adjust the right one quickly during spacing passes.
Caveat: Negative margins can cause overlap on breakpoints the designer didn't check; verify on mobile and tablet.
Caveat: The editor's drag-and-drop can place a new container inside an existing one by accident — drag outside first, then position, or use 'Add to Container' to place it as a sibling.

Tags: store-setup, elementor, spacing, layout, structure-panel, workflow
Source: WooCommerce Tutorial 2026_ Complete MasterClass for Beginners.docx

---

## Create Global Font and Colour Shortcuts Inside Widget Settings
Use when: When building a store page and you find yourself re-applying the same font family, size/weight combination, or brand colour on every heading and button.
- In any typography panel, click the plus icon next to the font family field to create a global font (source created one named after the brand font, e.g. 'Nito').
- A small globe/earth icon then appears wherever typography is set — click it to select the saved global font rather than browsing the font list again.
- Likewise, in any colour picker click the plus to create a named global colour (source created 'black' for the primary text tone and an 'orange' for the CTA colour).
- For fonts used at different sizes across many widgets (the source found this necessary in the countdown widget), save typography presets for each role, e.g. a 'digit' preset for countdown numbers and a 'label' preset for their captions.
- When you duplicate a widget (e.g. for the four countdown units or duplicated category tiles), apply the saved presets so every instance stays consistent and future brand changes propagate.
- Use these presets alongside the Site Settings global colours/fonts to keep section-level styling fast without re-inventing the palette on each section.
Caveat: Saved typography presets are widget/site specific — verify they appear in the typography popup as expected, since some widgets (like countdown) don't inherit site-wide fonts and need a custom selection.
Caveat: Naming presets by role ('digit', 'label', 'black', 'orange') rather than by value keeps them maintainable when the brand palette changes.

Tags: store-setup, elementor, design-system, typography, workflow, branding
Source: WooCommerce Tutorial 2026_ Complete MasterClass for Beginners.docx

---

## Plan for a Blog Section by Deferring Styling Until Posts Exist
Use when: Building a store homepage in a builder where a blog/news section is planned but no real posts have been published yet.
- Add a container for the blog section (source used 132/20/132/20 padding) and a centred section heading (source used 72px/600 weight, 80px line height, in the brand colour).
- Add the Blog Posts / Posts widget; it will pull from your site's existing posts.
- If only the default 'Hello World' post exists, the widget will show a single item — the source deliberately leaves it unstyled at this stage.
- Proceed to build the rest of the homepage, then return to style this block once you've created and published real posts from the dashboard and can judge the layout with representative content.
- When you come back, style the post archive on the front end with the same typography and spacing conventions as the rest of the page.
Caveat: Styling an archive section with only placeholder content often leads to incorrect decisions — the source explicitly recommends deferring this work.
Caveat: Blog Posts widget availability and options depend on Elementor Pro or a third-party add-on; verify which widget you actually have.

Tags: store-setup, elementor, homepage, content-marketing, workflow, retention
Source: WooCommerce Tutorial 2026_ Complete MasterClass for Beginners.docx

---

## Fix the SVG Icon Upload 'Only One Image Shows' Bug
Use when: When uploading a batch of SVG icons (for store badges, payment icons, CTA arrows) and only one appears in the media library.
- Batch-select all your SVG files and drag them into the media library upload area as normal.
- If only one (or a few) show up after upload, don't re-upload repeatedly first — publish the page so you don't lose design work.
- Refresh the editor page.
- Select the widget using the SVG (e.g. the button), open Upload SVG again, and all uploaded icons should now be visible and selectable.
- For SVG icons to appear at all, the site must have SVG uploads enabled — the source enabled this ('click Enable') when first attempting an SVG upload.
- After inserting an icon, control its relationship to the text with the Icon Spacing control (source used 12px) and style the button icon separately from the label if needed.
Caveat: The source mentions the button icon can look small relative to the text and planned to fix that with custom CSS later.
Caveat: SVG upload is a security-sensitive capability on some hosts; enabling it is a site configuration decision, not just a UI toggle.

Tags: store-setup, elementor, svg-icons, media-library, cta, troubleshooting
Source: WooCommerce Tutorial 2026_ Complete MasterClass for Beginners.docx

---

## Renaming and the Structure Panel Keep Complex Store Builds Sane
Use when: Managing a multi-section store homepage where containers are nested several levels deep and selecting the right one in the canvas is slow or error-prone.
- Double-click a container's label to rename it with a functional name (e.g. 'banner section', 'top area', 'title', 'product section', 'testimonials section'); renaming has no functional effect but makes the build navigable.
- Use the Structure panel (the tree icon) to see the exact nesting: open a container there and you'll see its children listed, which is how the source diagnosed misplaced widgets.
- Reorder or move a widget by dragging it within the Structure tree, or use right-click > Add to Container to insert a new container as a sibling (source used this to add a container 'beside' rather than 'inside' the selected one).
- Delete example/placeholder content by right-clicking the container in Structure and choosing Delete, which removes the container and everything inside it cleanly.
- Rename sections as you go (source renamed a generic 'product section' to 'product section two' and a section to 'testimonials section') so later customisation passes and handoff are unambiguous.
Caveat: Renaming is organisation only — it does not affect rendering, so don't expect it to change spacing or layout.
Caveat: The exact Structure panel location and right-click options are version dependent; verify in your Elementor version.

Tags: store-setup, elementor, structure-panel, workflow, organization, debugging
Source: WooCommerce Tutorial 2026_ Complete MasterClass for Beginners.docx

---

## Choose the Right Text Widget for Store Copy
Use when: Deciding how to add hero headlines, product descriptions, or mixed-format body copy to a store page in a visual builder.
- For large display text (hero headlines, section titles, price callouts) use the Heading widget, which is designed for a single line of prominent text and gives clean control over alignment, typography, size, weight, line height, letter spacing, and text colour.
- For paragraphs and body copy use the Text Editor widget, which provides a rich inline editor (like a word processor) so you can style individual words within one block — e.g. colour just the words 'premium shop' in a different tone while the rest of the sentence stays black.
- Use inline styling sparingly and deliberately: it is powerful for emphasising a phrase inside a paragraph, but it creates inconsistency if overused.
- Apply global styling (alignment, font family, size, weight, colour) at the widget level using the Style tab so the whole block stays coherent, layering inline styles only on top.
- Remember both widgets respect your saved global fonts and colours, so the fastest path is to set the font role globally first and then only adjust size, weight, line height, and letter spacing per instance.
Caveat: Inline rich-text styling lives inside the widget content, not the global style, so it will not update automatically if you change brand colours later.
Caveat: Mixing many one-off inline colours across a page is hard to maintain; keep the palette to your global colours where possible.

Tags: store-setup, elementor, typography, copywriting, product-page, content
Source: WooCommerce Tutorial 2026_ Complete MasterClass for Beginners.docx

---

## Building a responsive homepage in Elementor (tablet/mobile pass)
Use when: You are laying out a WooCommerce store homepage in Elementor and it looks broken on tablet or mobile breakpoints.
- Work section by section: select the section, open Advanced, and reduce padding (e.g. top 90, sides 20, bottom 60–90) so content isn't cramped on narrow screens.
- When a banner's big heading is too large, select the text directly and lower font size (e.g. 60–64 on tablet, 36 on mobile) and line height (72 tablet, 48 mobile) separately.
- For two side-by-side items that should stack, set each container width to 100% and change the parent's layout direction to column.
- Add vertical breathing room with margin (e.g. margin-bottom 30 on tablet, 20 on mobile) rather than reordering widgets.
- For image/illustration widgets, set a custom width (e.g. 115px, 120px, 150px) and use offset values (horizontal/vertical) instead of drag to place decorations precisely.
- Adjust column gaps on the container's layout tab (e.g. gaps column 40 on tablet, gaps row 30 on mobile) to space repeated items.
Caveat: Exact pixel values in the source are one designer's choices, not universal; match them to your own type scale and grid.
Caveat: Gap settings sometimes don't fix a leftover gap — style the widget's margin instead (e.g. margin-right 20).
Caveat: Elementor's exact panel names change between versions; verify the current interface.

Tags: store-setup, page-builder, elementor, responsive-design, homepage
Source: WooCommerce Tutorial 2026_ Complete MasterClass for Beginners.docx

---

## Adding more pages before theme customization
Use when: You have published a store homepage and now need additional pages such as contact and blog before doing global theme setup.
- From the WordPress dashboard go to Pages → Add New, title the page (e.g. 'Contact'), and publish.
- Open the page with the page builder (Elementor) to design it.
- Keep a separate 'Blogs' page as an empty placeholder: publish it, then set it under Settings → Reading as the Posts page so the theme auto-populates it with all blog posts.
- Return to the homepage afterward to wire widgets (like a blog post widget) that depend on posts existing.
- Expect the product grid, header and footer to remain incomplete until theme customization; treat those as the last pass.
Caveat: An empty Blogs page shows content only after real posts exist.
Caveat: Theme and builder menus labels may shift with updates — verify current paths.

Tags: store-setup, wordpress, pages, blog, theme-setup
Source: WooCommerce Tutorial 2026_ Complete MasterClass for Beginners.docx

---

## Designing a contact page banner and contact-detail cards
Use when: You are building or polishing the contact page of a WooCommerce store and want it visually consistent with the brand.
- Add a container, rename it 'page banner', give it a background color, and set padding (e.g. 122 top/bottom, 0 sides).
- Add a heading ('Contact Us'), center it, specify a large size (e.g. 72), weight 800, line height 82 and slight negative letter spacing; add a secondary intro heading below it.
- If you constrain the intro text with a custom width, set align-self to center so it stays centered.
- Add decorative images as absolutely positioned widgets with offset values (e.g. left 72, bottom 0) and control stacking with width and transform flip if needed.
- Build contact detail 'cards' as containers: background color, border radius 12, padding 40/30. Duplicate the card three times for phone, email and shop address.
- Inside each card add an icon widget (upload SVG, set view to stacked and shape to circle), then a label heading and the actual value. Reuse cards by copy/paste and only swap the icon and text.
Caveat: Absolute-positioned decorative images need manual offset tweaks per breakpoint or they overlap text on mobile.
Caveat: SVG upload support depends on your WordPress/plugin configuration.

Tags: store-setup, contact-page, elementor, page-design, containers
Source: WooCommerce Tutorial 2026_ Complete MasterClass for Beginners.docx

---

## Building a contact form with MetForm in Elementor
Use when: Your store contact page needs a functional form that emails submissions to you.
- Add the MetForm widget to the page, click Edit Form, create a new form and name it.
- Inside the form builder add a container, then rows: make each row direction 'row' for side-by-side fields and adjust the column gap (e.g. 10–20px).
- Add an MF Text widget for first name; turn off 'Show Label' and set the placeholder. Style padding (e.g. 17/16/17/20), text color, white background, 1px solid border, border radius ~100 for a pill shape, and set placeholder typography.
- Duplicate the field for last name. Use 'Paste Style' to copy styling onto new inputs instead of restyling each.
- Add an MF Email field with 'Required' enabled so the form cannot submit without it; set its width to 100%. Add an MF Text Area for message and paste the style, but reduce border radius (~20) because the large radius looks wrong on a tall box.
- Add the submit widget, relabel it (e.g. 'Send Message'), align left, style padding, uppercase, accent background, radius 50%, and set box-shadow color transparent to remove default shadow.
- In Form Settings → Notifications, enable admin notification, set subject, and add one or more recipient addresses separated by comma-space; save the form then update the page.
Caveat: MetForm's interface differs by version; verify current label names.
Caveat: Requiring email improves data quality but adds friction — consider which fields truly need to be mandatory.
Caveat: Deliverability of form email depends on your host/SMTP setup.

Tags: store-setup, contact-page, forms, metform, lead-capture
Source: WooCommerce Tutorial 2026_ Complete MasterClass for Beginners.docx

---

## Embedding a store location map widget
Use when: Your store's contact page or footer should show where customers can find you physically.
- Add a Google Maps widget into a container on the contact page.
- Search your shop address in Google Maps on a separate tab and copy the exact place title shown.
- In the widget's location field, paste that exact title followed by a comma and your store name so the pin resolves to the right place.
- Set the zoom (e.g. 13–15) so the surrounding area is visible, and set the map height (e.g. 500) to match your layout.
- Add a 1px solid border with a partially transparent color and a border radius (e.g. 12) to match other cards.
- On tablet/mobile, reduce the map height so it doesn't dominate the viewport.
Caveat: The map only resolves correctly if the place title text matches Google's data.
Caveat: A live embedded map may require an API key on some setups; confirm your configuration.

Tags: store-setup, contact-page, maps, local-commerce, widgets
Source: WooCommerce Tutorial 2026_ Complete MasterClass for Beginners.docx

---

## Writing and publishing store blog posts
Use when: You want content marketing or SEO articles attached to your store and discoverable by visitors.
- From the dashboard go to Posts; trash the default 'Hello World' post and click Add Post.
- Write the body in the rich text editor; use the plus icon to insert headings, lists, images, galleries, video and prebuilt patterns.
- Set a Featured Image in the right-side panel — it becomes the post thumbnail wherever the post is listed.
- Set the author, assign or create a Category, and add Tags.
- Publish, then verify with 'View Post'.
- Ensure a Blogs page exists and is assigned under Settings → Reading as the Posts page so visitors can browse all posts.
Caveat: Without the Posts-page setting, visitors cannot find posts through navigation.
Caveat: Comment functionality is on by default; decide whether to keep it for your store.

Tags: store-setup, blog, content-marketing, wordpress, seo
Source: WooCommerce Tutorial 2026_ Complete MasterClass for Beginners.docx

---

## Configuring the blog post widget on the homepage
Use when: You want to surface recent articles on the homepage and control exactly what each card shows.
- Select the blog posts widget, set the layout style to 'Grid with Thumb' and set the featured image size to full so images show at full resolution.
- Turn off 'Show Content' and 'Read More' if you only want image + title cards; open Query and set number of posts shown (e.g. 3) and order by (category or recent).
- Enable meta data, set position to 'Before Title', then add the meta items you want (date, author) and delete the unwanted icons.
- In Style: set background type classic, make card backgrounds transparent, set box-shadow color fully transparent, and zero out radius/widths.
- Style the featured image: border radius ~12, margin-bottom ~15, padding 0, and set the image to cover so corners round correctly.
- Style meta typography (e.g. 14/500, line height 20) and set item margin (e.g. 10 right/bottom) with zero item padding and icon spacing; style the title (e.g. 24/600, line height 32) in your primary color.
Caveat: The source notes some card layouts still need custom CSS to look right — expect to revisit.
Caveat: Number of posts shown is a design choice, not a performance rule.

Tags: store-setup, homepage, blog, elementor, merchandising
Source: WooCommerce Tutorial 2026_ Complete MasterClass for Beginners.docx

---

## Setting site identity: logo, title, tagline and favicon
Use when: You are doing the global brand pass on a new store and the header still shows a default site title instead of a logo.
- Go to Appearance → Customize → Site Identity and select your logo; choose 'Skip Cropping' to keep the full image.
- Use the logo size slider (e.g. 185px) to fit the header; optionally set a retina logo for high-density screens and a separate smaller mobile logo.
- Edit the site title so it describes the store (it appears in the browser tab and search results).
- Write a tagline that reinforces what the store sells.
- Set the site icon (favicon) and publish.
- Verify the header updates immediately with the logo.
Caveat: Logo dimensions vary by theme; adjust the slider until the header looks balanced rather than using a fixed number.
Caveat: Retina and mobile logos are optional but help sharpness and layout on small screens.

Tags: store-setup, branding, site-identity, wordpress, favicon
Source: WooCommerce Tutorial 2026_ Complete MasterClass for Beginners.docx

---

## Setting global theme layout, colors and scroll-to-top
Use when: You want store-wide consistency instead of fixing colors and spacing page by page.
- In Customize → Layout → Site Container, set the main background color every page inherits (e.g. a beige FFF0E0-type tone) and set the content width (e.g. 1240px).
- Set the header background color to your accent color in the header design panel.
- For blog settings, choose the blog list structure and limit how many posts load per page (source kept 20; adjust to taste).
- For blog single, reorder or hide elements (title, featured image, meta) in the order you want readers to see them.
- Choose where sidebars appear: e.g. sidebar on blog single and shop archive (left), but none on the blog list if you prefer a cleaner archive.
- In Footer settings, set the number of widget columns (e.g. 4) and edit the copyright text; the theme supports dynamic tags like current year and site title, so remove any parts (e.g. theme author) you don't want.
- Configure the scroll-to-top button: which devices show it, position (left/right), background color, icon size and border radius.
- In Colors, verify theme/text/accent/link-hover colors — these propagate to buttons and many components.
Caveat: Changing global theme colors affects many elements at once; preview before publishing.
Caveat: Theme customizer option names vary between themes — verify in your current theme.

Tags: store-setup, theme-customization, colors, footer, wordpress
Source: WooCommerce Tutorial 2026_ Complete MasterClass for Beginners.docx

---

## Configuring WooCommerce catalog and product display settings
Use when: You are finishing the shop archive and need catalog, image and product-card behavior set up correctly.
- In Customize → WooCommerce → Site Notice, replace the default demo-store notice text or clear it once the store is live.
- Under Product Catalog, set products per page (e.g. 12) — pagination appears after that count.
- Under Product Images, keep the thumbnail width and cropping/aspect ratio and, most importantly, upload product images at the same width and height so cards align.
- In Shop Archive → Product Content, choose what the card shows (title, rating, price) and alignment (e.g. center).
- Set the product image hover effect — the source switched from gallery-image swap to zoom because the swap 'looked bad'.
- For the sale tag, choose whether to show a percentage or custom text and set its background color to match your palette.
- For the add-to-cart button, choose the style; the source preferred the hidden variant that appears on hover.
- On Product Single, set content background, gallery layout option, and reorder description/reviews sections.
Caveat: Same-size product images is a presentation rule, not a hard WooCommerce requirement, but misaligned cards hurt trust.
Caveat: Hover effects and card options differ by theme/plugin version.

Tags: store-setup, woocommerce, catalog, product-images, shop-page
Source: WooCommerce Tutorial 2026_ Complete MasterClass for Beginners.docx

---

## Creating header and footer nav menus in WordPress
Use when: Your store pages are published but there is no working navigation in the header or footer.
- In Appearance → Menus, create a new menu (e.g. 'Main Menu') and assign it to the primary/header location.
- Use 'Add Items' to pull in published pages (home, shop, blog, contact); reorder them logically (e.g. shop right after home).
- For the footer, create additional menus (e.g. 'Footer Menu 1' for quick links like blog/contact/shop/account) and assign them to footer locations.
- Create a legal/utility footer menu (e.g. 'Footer Menu 2') with custom links for privacy policy, terms and disclaimer; use '#' as a placeholder URL until those pages exist.
- Ensure each menu is assigned to a theme location, then save.
- Verify navigation works from the live site, not only the dashboard.
Caveat: Custom links with '#' placeholders go nowhere until you create the target pages — don't forget to fill them in.
Caveat: Menu locations available depend on the active theme.

Tags: store-setup, navigation, menus, footer, wordpress
Source: WooCommerce Tutorial 2026_ Complete MasterClass for Beginners.docx

---

## Building footer widget columns with logo, menus and contact info
Use when: The footer area is empty and you want quick links, brand identity and contact details there.
- Go to Appearance → Widgets and add a Columns block (one column) into the footer widget area.
- Add an Image block for the store logo; in the block's settings set a width (e.g. 200px) so it isn't oversized.
- Add a Paragraph block after the image with a short brand description.
- In the next footer column add a Navigation Menu block, give it a title (e.g. 'Quick Links') and select the corresponding footer menu.
- Repeat for additional footer menus (e.g. a 'Website' column for legal links).
- Add a Heading block ('Contact Us') plus contact detail blocks in a final column.
- Because the footer column count is set in the theme customizer (e.g. 4 columns), match the number of widget columns you populate.
Caveat: Footer widget areas must be registered by your theme; missing areas mean you must use a footer builder instead.
Caveat: Block editor vs widget editor differences will shift some labels — verify in your WordPress version.

Tags: store-setup, footer, widgets, navigation, wordpress
Source: WooCommerce Tutorial 2026_ Complete MasterClass for Beginners.docx

---

## Catching left-over homepage sections and finishing the pass
Use when: You are finishing a store homepage and some sections look broken or empty.
- Identify sections that depend on content not yet created — a blog section is empty until posts exist and a posts page is set.
- Identify sections that depend on global customization — product grids and button styles may be fixed via theme-level CSS or customizer settings rather than per-widget tweaks.
- After creating the missing content, refresh the page and re-select the widget to surface its settings.
- Log the remaining fixes (header setup, footer setup, product settings) and address them in the customization phase rather than forcing them early.
- Publish and re-check the homepage end to end.
Caveat: The source explicitly defers some visual fixes to custom CSS in the customization phase; don't assume every issue is a widget setting.

Tags: store-setup, homepage, workflow, troubleshooting, elementor
Source: WooCommerce Tutorial 2026_ Complete MasterClass for Beginners.docx

---

## Build a multi-column footer with navigation menus and contact details
Use when: Setting up or fixing a store footer in a block-based theme (e.g., WooCommerce block theme) so navigation, contact details and copyright display correctly.
- Add blocks sequentially in a footer column using the block inserter. For the first column, add an image (logo/site icon), then a paragraph block after it for a short store description.
- For the second column, add a Navigation Menu block, set its title (e.g. 'Quick Links') and select the footer menu assigned to it. You can rename the menu title (e.g. change to 'Shop') without changing the underlying menu.
- Repeat the Navigation Menu block in the third column, rename the title (e.g. 'Website') and select a second footer menu.
- For the contact column, add a Heading block ('Contact Us'), then add paragraph blocks after it for email, phone and address, adding each with the 'add after' option.
- If content spreads across the whole footer instead of staying in one column, insert a Columns block with a single column and drag each block into it one by one until all footer content sits in a single vertical column.
- Publish, then check the footer preview. If extra menus appear that you don't want, return to Appearance > Menus, open the relevant footer menu, deselect its footer menu location, save, and reload.
- Verify the current block inserter and menu-location interface in your WordPress/WooCommerce version, as labels may change.
Caveat: Menu location assignment must match the Navigation Menu block's selected menu, or the wrong links appear in the footer.
Caveat: Deselecting a menu's footer location removes it from the footer entirely, including any copyright or other links built into that menu.

Tags: store-setup, woocommerce, footer, site-navigation, block-theme, store-design
Source: WooCommerce Tutorial 2026_ Complete MasterClass for Beginners.docx

---

## Apply a curated custom-CSS set to polish theme design elements
Use when: When default theme styling makes product grids, buttons, counters, blog images or cart/checkout pages look unpolished and you want consistent store-wide design quickly.
- Go to Appearance > Customize > Additional CSS (or the theme's Additional CSS panel) and paste each snippet in order after the previous one, leaving spacing between blocks.
- Start with the site default style snippet to establish baseline typography and element styling.
- Add the homepage button style snippet — verify buttons and their icons become larger and more consistent.
- Add the product heading snippet for homepage section headings.
- Add the counter style snippet to fix counter/countdown widgets that break at tablet and smaller widths. After pasting, add the documented class name to the countdown widget's Advanced > Additional CSS Class field, publish, and resize the browser to confirm it holds at all widths.
- Add the blog post image snippet, then add the documented class name to the blog post widget's Advanced > Additional CSS Class field and refresh to confirm images are no longer distorted.
- Add the page header, product card, blog post and cart/checkout snippets. The product card snippet is the one that restyles product archives/shop grids; the cart/checkout snippet only takes effect once the WooCommerce shortcodes are placed on those pages.
- Publish/update and refresh the relevant pages after each batch to confirm the change applied.
Caveat: CSS snippets are theme/plugin-specific — they assume the same starter theme, widgets and class names. Adapt before assuming they transfer.
Caveat: Class names referenced by the CSS must be added to the specific widget's Advanced > CSS Classes field, or the styling silently does nothing.
Caveat: Layering many snippets makes future theme updates or redesigns harder to unpick; keep snippets commented.

Tags: store-setup, css, store-design, woocommerce, product-card, cart, checkout, theme-customization
Source: WooCommerce Tutorial 2026_ Complete MasterClass for Beginners.docx

---

## Replace default cart and checkout widgets with WooCommerce shortcodes
Use when: When cart or checkout pages use default template/widget layouts that look inconsistent with the rest of the store, and you want a simpler page structure.
- Look up the current WooCommerce shortcodes list in the official WooCommerce documentation (verify the exact shortcode names for your version rather than relying on copied text).
- Open Pages > Cart, edit it, select the existing cart container/blocks, delete them, and paste the cart shortcode. Save.
- Open Pages > Checkout, delete the default checkout widgets/blocks and paste the checkout shortcode. Save.
- Refresh both pages to confirm the shortcode-rendered layout appears and matches the theme.
- If the shortcode layout looks worse than the default, revert: open the page, remove the shortcode, insert the default Cart block/widget (search 'cart' in the block inserter) and re-add default structure.
- Optionally apply custom CSS after placing shortcodes, since cart/checkout styling snippets only affect shortcode-rendered pages.
Caveat: Deleting the default cart/checkout blocks removes the layout you may want to fall back to — note or screenshot before deleting.
Caveat: Shortcode output and available attributes change between WooCommerce versions; always check current documentation.
Caveat: The source presenter preferred the default widget layout for checkout with their theme but chose to showcase shortcode layout for cart — treat as a style preference, not a fixed rule.

Tags: store-setup, woocommerce, cart, checkout, shortcodes, store-design
Source: WooCommerce Tutorial 2026_ Complete MasterClass for Beginners.docx

---

## Enable and style a page header banner with breadcrumbs
Use when: When non-homepage store pages (shop, blog, cart, contact) start abruptly with no header context and you want a consistent branded banner with breadcrumbs.
- Go to Appearance > Customize > Layout > Page Header (naming varies by theme) and turn on 'Page Header Display'.
- Enable display of the page title and the breadcrumb trail so each page shows its name and navigation path.
- In the Page Header design settings, set the background color to a brand or theme color consistent with the site palette.
- Set padding-top and padding-bottom to roughly 112px each to give the banner breathing room (source used 112 top and 112 bottom), and keep margin-bottom around 68px to space content below.
- Publish and visit representative pages (shop, blog, cart, contact) to confirm the banner and breadcrumbs render consistently.
- Note the blog/page header CSS snippet works together with this setting — the banner may need the CSS present and the correct page settings enabled.
Caveat: Page Header is a template part; enabling it affects all pages that use the header, so verify it doesn't clash with pages that already have a custom hero.
Caveat: The exact menu path and setting labels differ across themes; locate the equivalent setting in your theme's customizer or site editor.

Tags: store-setup, page-header, breadcrumbs, store-design, woocommerce, site-navigation
Source: WooCommerce Tutorial 2026_ Complete MasterClass for Beginners.docx

---

## Change the blog author display name store-wide
Use when: When blog posts on the store's content section show a generic or blank author name and you want a personal or brand author name to appear.
- Go to Dashboard > Users and open the relevant user profile.
- Enter First Name and Last Name. WordPress will generate display-name variants from these fields.
- Choose the preferred Display Name from the dropdown (e.g., full name or first+last).
- Click Update Profile.
- Visit a published blog post to confirm the author name now reflects the chosen display name across all posts.
- If the theme hides author names, check the single-post template settings for an author/byline toggle.
Caveat: For guest authorship or a brand author, a role and capability review is often needed — simply changing display name keeps the account's publishing permissions.
Caveat: Changing the display name updates the byline everywhere that user is the author; verify it doesn't break any author archive links you rely on.

Tags: store-setup, blog, author-profile, users, content, wordpress
Source: WooCommerce Tutorial 2026_ Complete MasterClass for Beginners.docx

---

## Verify storefront pages end-to-end after setup
Use when: After completing theme setup, CSS, footer and shortcode work, before handing off or launching an ecommerce store.
- Check top navigation: confirm Home, Shop, Blog, Contact and other key links route to the right pages.
- Visit Shop: confirm product grid, sidebar search, price filter, category and attribute filters all render and return results.
- Open a product: verify gallery images, variation selector (sizes/options), description, related products and add-to-cart all work.
- Open the Blog listing and a single post: confirm title, featured image and related posts display, and that blog image/title CSS applied.
- Open the Contact page: confirm store details, the working contact form and the embedded map point to the real business location.
- Test search: find a product by keyword. Test the user account dashboard: wishlist (even empty), orders with details and mini-cart behavior.
- Close the loop by fixing anything visually broken (CSS class missing, wrong block in a column) and re-verify.
Caveat: The source walkthrough is a visual/functional sweep, not a payment or fulfillment test — actually place a test order separately.
Caveat: Wishlist and account features depend on installed plugins; confirm those are active before testing.

Tags: store-setup, qa-testing, storefront, shop-page, product-page, user-account, pre-launch
Source: WooCommerce Tutorial 2026_ Complete MasterClass for Beginners.docx

---

## WooCommerce Setup Order: From Blank to Sellable Store
Use when: You are launching a new WooCommerce store from nothing and need the correct build order so later steps (payments, shipping, taxes) have products and addresses to bind to.
- Start with domain and hosting, then install WordPress — this is the foundation everything else attaches to.
- Install the Blocksy theme (Appearance > Themes > Add Theme), then activate the Blocksy Companion plugin.
- Import a Starter Site template (Starter Sites > filter builder = Elementor > import, e.g. the 'Garter Robe' template) to get a working page structure fast.
- In Elementor settings, disable the Atomic Editor while you are learning — the source recommends this for beginners to avoid an extra editing paradigm.
- Configure store address and currency (this address drives tax origin rules, so do it before taxes).
- Create at least one Simple Product so you have something to test checkout with.
- Connect payments last-but-one: install Stripe and PayPal plugins, link accounts via API, run the connection test, and leave them in Test mode.
- Set up Shipping Zones and Tax, then run a full test order (test card, test address) before switching payments to Live.
Caveat: Tool menus and plugin names change between versions — verify the current click paths in your own WordPress admin.
Caveat: Starter Site templates bring demo content and styling you will need to strip out.
Caveat: Do not go Live on payments until a test order completes end-to-end.

Tags: store-setup, woocommerce, wordpress, theme-setup, launch-checklist, payments
Source: WooCommerce Tutorial for Beginners 2026.docx

---

## Installing and Importing a Blocksy + Elementor Starter Site
Use when: You are on a fresh WordPress install and want a styled, editable storefront skeleton without designing every page from scratch.
- Install the Blocksy theme via Appearance > Themes > Add Theme, then activate it.
- Install and activate the Blocksy Companion plugin — it unlocks the Starter Sites importer and Blocksy's extra options.
- Open Starter Sites, filter by builder = Elementor so the imported pages are editable in Elementor rather than another builder.
- Import a template that matches your niche (the source uses 'Garter Robe' as the worked example).
- Go into Elementor settings and turn off the Atomic Editor if you are a beginner — the source says it is recommended for beginners to reduce confusion.
- After import, replace demo copy, imagery and links with your own before going live.
Caveat: Imported templates ship with placeholder products and imagery that must be replaced.
Caveat: The Atomic Editor recommendation is the source's opinion aimed at beginners, not a universal rule.
Caveat: Verify current plugin and menu names — WordPress admin labels change between versions.

Tags: store-setup, blocksy, elementor, theme-setup, wordpress
Source: WooCommerce Tutorial for Beginners 2026.docx

---

## Creating a Simple Product in WooCommerce
Use when: You are listing a product with no size/color variants and need it purchasable, stocked correctly, and shipping-ready.
- Go to Products > Add New.
- Enter a clear product title and write the description (and short description for listing/above-the-fold placement).
- Set Product Type = Simple Product.
- Enter regular price and, if discounting, the sale price — WooCommerce applies the sale price automatically during the sale window.
- Manage inventory: enable stock management and set the stock quantity and low-stock threshold so you get warned before you sell out.
- Enter shipping weight and dimensions — these feed weight-based and class-based shipping rates, so missing them can break calculated shipping.
- Assign product categories and upload the featured image before publishing.
Caveat: Without weight/dimensions filled in, weight-based shipping rules will not calculate correctly.
Caveat: Skipping the low-stock threshold means you only find out you are out of stock from customers.

Tags: store-setup, woocommerce, product-setup, inventory, shipping, product-page
Source: WooCommerce Tutorial for Beginners 2026.docx

---

## Creating a Variable Product with Attributes and Generated Variations
Use when: You sell a product in multiple sizes, colors or materials and need each combination to have its own SKU, stock and price.
- Create the product (Products > Add New) and change Product Type to Variable product.
- Open the Attributes tab. Create or select an attribute (e.g. Size, Color) and enter its values separated by the pipe symbol, e.g. 8 | 9 | 10 | 11.
- Tick 'Use for variations' — without this tick the values will not become selectable buying options.
- Save the attributes.
- Open the Variations tab and click 'Generate variations' (or 'Generate all variations') — WooCommerce creates one row per combination, e.g. Size 10 / Red.
- For each variation, set an SKU, its own price, and its own stock level. A variation with no price set is not purchasable.
- Add variation images if buyers need to see each colorway, then publish and test every combination in the shop.
Caveat: A variation with no price will not be buyable — check every generated combination, not just the first.
Caveat: Generated variations can leave orphan rows when you later remove an attribute value; prune them.
Caveat: Verify current tab names in your WooCommerce version.

Tags: store-setup, woocommerce, product-setup, variants, inventory, product-page
Source: WooCommerce Tutorial for Beginners 2026.docx

---

## Connecting Stripe and PayPal via Payment Plugins
Use when: You are turning on card and wallet payments for a WooCommerce store and want to confirm the connection before taking real money.
- Install 'Payment Plugins for Stripe WooCommerce' and 'Payment Plugins for PayPal WooCommerce' (or your chosen WooCommerce payment extensions).
- Open the plugin settings and connect each account by entering the API keys/credentials from your Stripe and PayPal dashboards.
- Run the plugin's built-in connection test to confirm the credentials work.
- Set both plugins to Test mode first, then place a real test order using test card numbers.
- Confirm the order status changes correctly, the customer receives the confirmation email, and a refund path exists in the dashboard.
- Only switch to Live mode after the test order completes cleanly.
Caveat: API key fields and test-mode toggles differ between plugin versions — verify against the current plugin docs.
Caveat: Test-mode and live-mode credentials are different keys; swapping them is a common launch error.
Caveat: Payment plugin availability and interface may change over time.

Tags: store-setup, payments, stripe, paypal, checkout, launch-checklist
Source: WooCommerce Tutorial for Beginners 2026.docx

---

## Shipping Zones, Flat Rate vs Free-Over-Threshold, and Shipping Classes
Use when: You are setting shipping charges for a WooCommerce store and need to handle multi-region rates plus oversized/heavy products without losing margin.
- Create Shipping Zones for each region you sell into (e.g. United States, EU).
- Inside each zone, add Shipping Methods — a flat rate for standard orders and/or a free shipping method.
- Configure free shipping with a minimum-order threshold (the source uses $100 as an example) so free shipping rewards larger baskets instead of eroding every order's margin.
- Create Shipping Classes (e.g. 'Heavy') for oversized or weighty products.
- Assign the Heavy class to the relevant products, then add a Shipping Class cost to the zone's flat-rate method so those items carry a higher per-item charge.
- Place test orders with light-only, heavy-only, and mixed carts to confirm the rates combine the way you intend.
Caveat: The $100 free-shipping figure is the source's illustrative example, not a recommended benchmark — set yours from your own margins and AOV.
Caveat: Shipping Class costs are typically applied per item, so a cart of multiple heavy items can stack charges unexpectedly.
Caveat: Verify current WooCommerce shipping UI labels in your version.

Tags: store-setup, woocommerce, shipping, pricing, margin, cart
Source: WooCommerce Tutorial for Beginners 2026.docx

---

## Automated Sales Tax with WooCommerce Tax
Use when: You need correct sales tax across US states or other jurisdictions without hand-maintaining every rate table, or you sell goods with special tax treatment.
- Install and connect the 'WooCommerce Tax' plugin (by WooCommerce/Automattic, powered by TaxJar).
- Set your store address accurately — it determines whether origin-based or destination-based tax rules apply.
- Choose the calculation method that matches how your jurisdiction's law works (origin-based vs destination-based) rather than guessing.
- Enable automated calculation so rates update when jurisdictions change.
- For special categories — e.g. digital goods, or goods that are tax-exempt locally — configure reduced or zero tax rates tied to those product categories instead of a blanket rate.
- Run a test order to a few different addresses to confirm the tax lines look right before launch.
Caveat: Tax law varies by state and jurisdiction; automated tools assist but do not replace confirming your obligations with a tax professional.
Caveat: Correct store address is a prerequisite — a wrong address produces wrong tax.
Caveat: Plugin name, pricing and connection flow may change; verify the current interface.

Tags: store-setup, taxes, woocommerce, compliance, product-categories
Source: WooCommerce Tutorial for Beginners 2026.docx

---

## Elementor Responsive Controls for Product and Landing Pages
Use when: Your store pages look fine on desktop but cramped, overlapped or unreadable on mobile/tablet, and you need a mobile merchandising fix inside the builder.
- Open the section/container in Elementor and switch to Mobile or Tablet preview using the responsive device icons at the bottom of the panel.
- Use the device-specific toggle next to any setting (the little screen icon) so a change applies only to that viewport — this is how you adjust alignment, spacing and sizing per device.
- Use Advanced > Responsive to hide elements that do not belong on a given device (decorative graphics, wide comparison tables, dense desktop nav).
- Replace or reposition background images per device so hero imagery stays legible on narrow screens rather than cropping awkwardly.
- Preview on the actual device or a narrow browser window, not just the builder's preview, before publishing.
Caveat: Hiding content on mobile means that content is gone for mobile buyers — do not hide something they need to make a purchase decision.
Caveat: Per-device overrides multiply settings; document what you changed so later edits do not silently revert.
Caveat: Elementor's panel layout and icon placement change between versions — verify in your current build.

Tags: store-setup, elementor, mobile, responsive-design, product-page, landing-page
Source: WooCommerce Tutorial for Beginners 2026.docx

---

## Pre-Launch Store Configuration Checklist (Topic Map)
Use when: You are auditing a WooCommerce store before going live and want to confirm each configuration area is actually done rather than assumed.
- Domain and email: confirm the store's domain resolves and transactional email (order confirmations, password resets) actually sends and lands in inboxes — not just spam.
- Store configuration: WordPress installed, theme (e.g. Blocksy) active, page builder (e.g. Elementor) working, store address and currency set correctly.
- Products: at least one Simple Product and one Variable Product published, with prices, stock thresholds, weights/dimensions, and categories assigned.
- Payments and tax: Stripe and PayPal connected and connection-tested, tax plugin configured against the correct store address and calculation basis, test order completed.
- Shipping profiles: zones created for each region, flat vs free-shipping thresholds set deliberately, Shipping Classes assigned to heavy/oversized items and costed.
- Mobile: check key pages on a phone viewport and fix with Elementor responsive toggles.
- Finish with a full test purchase in Test mode before flipping payments to Live.
Caveat: This is a coverage map for baseline configuration — page copy, analytic accuracy, and ongoing speed work belong to separate disciplines and are not covered here.
Caveat: Do not treat 'plugin installed' as 'plugin configured'; the test order is the real verification.

Tags: store-setup, launch-checklist, woocommerce, payments, shipping, taxes, mobile
Source: WooCommerce Tutorial for Beginners 2026.docx

---

## WooCommerce baseline store configuration order
Use when: Launching a new WooCommerce store or deciding what to configure first before adding real products and taking live payments.
- Deactivate and delete the plugins pre-installed by the host (keeping only the caching plugin, e.g. LiteSpeed Cache) — the source notes leftover plugins can conflict with demo/starter-site imports; they can be reinstalled later.
- Set store-owner basics in Users > Profile (color scheme, contact email, password) and disable comments in Settings > Discussion by unchecking comment options and the 'email me whenever' boxes to block spam on a store that does not use blogging.
- Install an ecommerce theme (the tutorial uses Bloxy) plus its companion plugin, then import a free starter site using the Elementor builder with a selected set of pages and plugins: theme options, widgets, content, standard plugins and WooCommerce.
- Create products: at minimum learn the simple product (single price, no options) and the variable product (size/color combinations) — the source calls these the two most common types.
- Connect payments with the Stripe and PayPal WooCommerce plugins, add API credentials, run the connection test, and leave gateways in Test mode until verification succeeds.
- Configure shipping as zones (e.g. United States) with flat-rate vs free-shipping minimum thresholds (example: $100) and Shipping Classes such as 'Heavy' to charge per-item rates for oversized products.
- Configure tax with the WooCommerce Tax plugin (automatic calculation), the store address, and the origin- vs destination-based method required by the relevant state law; set reduced or zero rates for categories like digital goods.
Caveat: Host onboarding screens change frequently; treat the host's exact click path and plan names as of the recording date and verify the current interface.
Caveat: Free-shipping thresholds and tax methods depend on your jurisdiction and margins — the $100 and US example are illustrations, not benchmarks.
Caveat: Payment plugins and tax plugins are third-party; confirm current setup steps in their own docs.

Tags: store-setup, woocommerce, plugins, payments, shipping, tax, checkout
Source: WooCommerce Tutorial for Beginners 2026.docx

---

## Simple product configuration in WooCommerce
Use when: Adding a single-SKU product to a WooCommerce catalog, or auditing an existing product page for missing inventory, shipping or cross-sell data.
- Name the product and fill the long description with spec-style content (origin, technicals) that appears below the product; reserve selling copy for the short description, which is the text shoppers see first.
- Under Product data choose Simple product; optionally mark Virtual or Downloadable and add files for digital goods.
- Set Regular price and Sale price, and use Sale schedule to bound a promotion by date (example in the source: a $100 shirt on sale for $50 from the 6th to the 31st).
- Enter the SKU, enable stock management if you want quantities shown on the storefront, set the quantity (example: 10), decide on backorders (example: allow but notify the customer) and set a low-stock threshold (example: 3) so you are alerted before running out.
- Add weight and dimensions so shipping rates by weight or size calculate correctly.
- Attach an Upsell (shown on this product page, e.g. a matching cap) and a Cross-sell (offered further down the funnel at cart/checkout) — the source distinguishes the two by placement.
- Set the main product image and gallery images, assign a product category (creating a new one if needed, e.g. 'Daryl shirts') and add tags or brands.
- Publish and view the product page to confirm the price, sale badge, stock count, images, description, additional information and the 'You may also like' upsell block all render.
Caveat: Backorder choice is a policy decision: allowing backorders but promising notification means you must fulfil the notification.
Caveat: The source flags the short description as the most important text because it is what the customer reads first — do not bury key selling points in the long description.

Tags: store-setup, woocommerce, product-page, inventory, pricing, upsell, merchandising
Source: WooCommerce Tutorial for Beginners 2026.docx

---

## Variable product setup for size and color options
Use when: Adding apparel, footwear or any product sold in multiple sizes, colors or materials, or when shoppers cannot currently select a variant on the PDP.
- Create the product as normal, then under Product data select Variable product instead of Simple.
- Define attributes (e.g. Color, Size) and the values for each attribute; the source demonstrates this style of selection against a real store selling multiple colors and sizes.
- Generate variations from those attributes and edit each one individually.
- Set stock level, price and (where the option is offered) a variant-specific image for every combination, e.g. Size 10 / Red.
- Enforce the rule that a price must be set for each variation — otherwise that combination is not purchasable and the shopper hits a dead option.
- Preview the product page and click through each attribute combination to confirm prices, stock and images update as expected.
Caveat: Variation count multiplies quickly; every attribute combination is a row to price and stock, so keep attribute lists to what you actually sell.
Caveat: The source notes attributes only apply to variable products, so do not populate them on simple products.

Tags: store-setup, woocommerce, product-page, variants, inventory, pricing
Source: WooCommerce Tutorial for Beginners 2026.docx

---

## Upsell vs cross-sell placement in WooCommerce
Use when: Merchandising a product page or cart to raise average order value with complementary items.
- Treat an Upsell as a recommendation shown while the shopper is viewing the current product — it appears at the bottom of that product page in a 'You may also like' style block.
- Treat a Cross-sell as a recommendation shown at checkout/cart after the item is added — used to attach lower-priced or complementary items to an existing basket.
- Populate both fields from the product edit screen when creating the product; the source demonstrates an upsell with a snapback cap on a t-shirt product.
- Choose the relationship deliberately: on the PDP, offer a comparable or upgraded item (the source's example pairs the shirt with a cap); at cart/checkout, offer additions that complement what is already in the basket.
- Verify on the live product page and cart that the correct products surface in each slot.
Caveat: The source illustrates the mechanism but gives no AOV results; treat uplift from upsells/cross-sells as something to test on your own catalog rather than an assumed gain.
Caveat: Adding too many recommendations can clutter the PDP or checkout — the source shows a single slot in each location.

Tags: store-setup, woocommerce, upsell, cross-sell, merchandising, average-order-value, product-page
Source: WooCommerce Tutorial for Beginners 2026.docx

---

## Elementor container and flexbox layout for ecommerce pages
Use when: Building or fixing a homepage, category or landing page layout in Elementor — e.g. getting two buttons to sit side by side or making an image column narrower than a text column.
- Add a container (click plus) and choose Flexbox rather than Grid — the source calls flexbox easier and the common choice.
- Drag elements into the container; note that plain elements such as two buttons stack vertically with no control, so wrap side-by-side items (e.g. 'Shop now' + 'Contact us') inside their own container.
- On the container, switch the flex Direction to Horizontal to place children side by side, or Vertical to stack them; use reversed direction to swap order.
- Use Justify content to position children — center, start, end, space-between, space-around, space-evenly — rather than adding manual padding.
- Adjust per-column Width when one column should be smaller (e.g. an image column narrower than the text column).
- For a full-height hero, set the container's Minimum height to 100VH on the section rather than the inner container — the interface itself labels this as the way to achieve full-height containers.
- Editing each element exposes three tabs: Content (the text/media itself), Style (typography, colors, sizes) and Advanced (padding/margins and motion effects such as entrance animations).
- Use the responsive breakpoints (desktop, tablet portrait, mobile portrait) to re-apply flex settings per device — centering, changing a background image, resizing type or hiding elements only on that device.
Caveat: Do not put too many items horizontal in a narrow box: the source shows elements render badly when there is not enough space and recommends vertical plus centered instead.
Caveat: The source opinion that Gutenberg 'is terrible' and Elementor is the number-one builder is a presenter preference; if you already have a working builder stack, changing it is optional.
Caveat: Elementor has released 'Atomic Elements' aimed at developers; the tutorial recommends deactivating them while building a store and notes the interface may change.

Tags: store-setup, elementor, landing-page, page-builder, responsive-design, merchandising, wordpress
Source: WooCommerce Tutorial for Beginners 2026.docx

---

## Starter-site import and why to remove conflicting plugins
Use when: Setting up a new store quickly and needing a working shop layout — header, hero, category blocks, product grid — before replacing demo content with real products.
- In the theme's dashboard, open Starter Sites, filter to Free plans and select the Elementor builder.
- Pick a template and click Import; choose Elementor when prompted for a page builder.
- Keep the import options for theme options, widgets and content selected, and confirm it is a clean install so the demo imports without leftovers.
- Keep the plugin list selected on the next step — typically the page builder, a contact-form plugin and WooCommerce (the shopping-cart integration) — then click install and wait roughly a minute.
- After import, view the site: the starter provides a menu, hero landing section, trust badges (free delivery, 30-day returns, secure payment), dummy products, category blocks (jackets, sweaters, accessories), a popular-products section and a shop page with a filterable sidebar gallery.
- Delete or trash demo products afterwards (Products > select all > bulk actions > Move to trash, recoverable from Trash) and replace images and copy with your own.
- Import demo pages (shop, services, about us) and adapt them rather than building every page from scratch.
Caveat: Delete pre-installed host plugins before importing — the source says they can conflict with the demo import.
Caveat: The imported content is demo data: replace dummy products, images and text before launch so the storefront is not visibly a template.
Caveat: Starter-site availability and the import wizard change over time; verify the current flow in your theme.

Tags: store-setup, wordpress, theme, starter-site, elementor, product-page, plugins
Source: WooCommerce Tutorial for Beginners 2026.docx

---

## Header settings that block page building and product imagery
Use when: Troubleshooting an Elementor editing experience where the menu collides with the builder, or a hero image pushing up under the menu and hiding content.
- Open the theme customizer (Websites > Customize) and go to Header > Global Header.
- Turn off the sticky-header option if the fixed menu blocks or collides with the builder while you are working — the source disables it purely to remove that friction during building.
- Turn off transparent header if the starter template uses one: a transparent header forces page content up under the menu, cuts access to those areas and can push hero imagery into the navigation.
- After changing header settings, publish and refresh the Elementor editor to confirm the page now starts below the header and you have space to add sections.
- Re-enable sticky header after the build if you want the persistent navigation for shoppers — the source's reason for disabling it was editorial convenience, not a storefront recommendation.
- While a hero is being styled, remove any custom position on the background first and set display size to Cover, then pick a focal position (center right vs center center etc.) so subjects are not cropped out.
Caveat: These are theme-specific settings; the exact labels live under the theme customizer and may differ by theme.
Caveat: Disabling sticky or transparent headers changes shopper-facing navigation behavior — decide the final setting on user experience, not just build convenience.

Tags: store-setup, theme, wordpress, landing-page, navigation, elements
Source: WooCommerce Tutorial for Beginners 2026.docx

---

## Responsive optimization pass across desktop, tablet and mobile
Use when: Doing the mobile/tablet pass on a store homepage, category page or landing page before launch, or fixing text that is illegible over an image on small screens.
- Switch the editor to each device view (desktop, tablet portrait, mobile portrait) — settings changed while a device view is active are saved scoped to that device.
- Center stacked content per device: select the flexbox container and set justify-content to center for tablet and mobile instead of leaving left-aligned rows.
- Change background images per device where the desktop crop does not work on mobile — Elementor stores a separate image for the tablet or mobile breakpoint.
- Add a background overlay with a darker color and increased opacity when light imagery makes overlaid text unreadable, and scope the overlay to the device that needs it.
- Adjust typography size per device for text that reads too small or too large (e.g. enlarge a heading only on tablet portrait).
- Hide elements that do not fit small screens: open the element's Advanced settings, find Responsive, and hide it on tablet/mobile — the same controls work for sections and columns.
- Re-check the default auto-generated sections; the source notes WooCommerce product displays are automatically responsive, but manual sections and footers still need review.
Caveat: Changing a background per device makes maintenance heavier — keep one image across devices unless the desktop crop genuinely fails.
Caveat: Hiding elements removes information for that audience; check the hidden element is not a required CTA or price.

Tags: store-setup, responsive-design, elementor, landing-page, product-page, mobile, elements
Source: WooCommerce Tutorial for Beginners 2026.docx

---

## Elementor element editing, copy-paste style and AI page drafts
Use when: Building a reusable store page (About, Team, landing section) and needing to keep typography, colors and spacing consistent without restyling each element by hand.
- Select any element to get three tabs: Content for the text, image or link; Style for typography, colors and size; Advanced for padding/margins and motion effects such as entrance animations.
- Right-click an element or container to Duplicate or Delete; duplicating a container clones a whole column so you can build repeated card rows quickly.
- Configure one element fully, then right-click it and Copy, and on each matching element use Paste style — the source notes this works between the same element type and keeps a page consistent.
- For the button link field, type the page name and the builder resolves the page URL automatically, so 'shop now' can be pointed at the Shop page without copying a URL.
- For a quick page draft, use Elementor AI: prompt it for a layout (e.g. a three-column row) and click Use layouts, then clean up the result.
- Treat AI-generated pages as a starting point: the source's own test requested three columns and got four, so delete extra sections and replace placeholder images and names before publishing.
Caveat: The source explicitly rates Elementor's AI builder as 'not the best' but occasionally useful — do not ship its output unchecked.
Caveat: The demo used a specific font choice (Poppins bold) as a personal preference, not a conversion recommendation; pick one brand font family and apply it consistently.

Tags: store-setup, elementor, page-builder, workflow, landing-page, typography, ai-tools
Source: WooCommerce Tutorial for Beginners 2026.docx

---

## Creating pages, menus and dropdown navigation for a store
Use when: Building out an online store's site structure — adding an Our Team or Services page, organizing the navigation under shop and contact, or linking to an off-site channel.
- In Pages > Add Page, create the new page, publish it, then open the Elementor builder to design it (the source drafts a Team page with a three-column layout of images, names and roles).
- Go to Appearance > Menus — the menu created at import holds the starter item structure.
- Under Pages click View all, tick the new page (e.g. Our Team) and click Add to menu.
- Drag the item to the desired position; nest it under a parent (e.g. under Services) to create a dropdown that appears on hover.
- To link off-site destinations (a Facebook group or school), use the Custom Links section: paste the URL, give it a label, click Add to menu, then position it (e.g. under a Contact item) and click Save menu.
- Visit the live site to confirm the dropdown opens on hover and the custom link resolves to the right destination.
Caveat: Menu structure is theme-driven; the dropdown behavior and depth limits come from the theme.
Caveat: Custom links point off-site, so they take shoppers away from checkout — place them where abandonment risk is low.

Tags: store-setup, wordpress, navigation, menus, content, customer-experience
Source: WooCommerce Tutorial for Beginners 2026.docx

---

## WooCommerce admin surfaces for running the store after launch
Use when: Setting up the operational side of a WooCommerce store — reviewing orders, tracking customers, issuing coupons and checking sales reporting after launch.
- Use Orders to review everything customers have purchased; each order appears here as it is placed.
- Use Customers to see everyone who has purchased, with username and email, so you can identify repeat buyers or export a list for retention work.
- Use Coupons to create and manage discount codes applied on the storefront.
- Use Reports for the legacy sales report listing.
- Use WooCommerce Analytics for the upgraded view showing total sales, net sales, orders, products sold and related metrics — the source treats this as the primary reporting surface.
- Use Settings as the central configuration screen for the store (the source flags it as the most important section, covering the store-level configuration used for payments, shipping and tax).
Caveat: The source admits to skipping many WooCommerce options as unnecessary for a basic store; the depth you configure should match your sales volume and tax/shipping complexity.
Caveat: Metric definitions in Reports vs Analytics differ (total vs net sales) — confirm which figure you are quoting before acting on it.

Tags: store-setup, woocommerce, analytics, orders, coupons, measurement, customers
Source: WooCommerce Tutorial for Beginners 2026.docx

---

## Create variable products with size/color attributes and variation images
Use when: Setting up a product with multiple options (sizes, colors) on the PDP so customers see the correct image and price per choice.
- Create the product and set Product Data to 'Variable product'.
- Open the Attributes tab and add your first attribute (e.g. 'Size'), entering each term (e.g. 10, 11, 12). To enter multiple terms in the field, hold Shift and press the key above your keyboard's Enter key to separate values. Click Save attributes.
- Add a second attribute (e.g. 'Color' with gray, red, beige), save attributes again.
- Open the Variations tab and click Generate variations — WooCommerce combines every term of both attributes (size 10 gray, size 10 red, size 11 gray, etc.).
- Edit each variation individually: assign the matching image, set the price, and optionally weight. This is the tedious part but you must do it per variation.
- Set the product short description, then set the main Product image and Default form values (default size and color) so the default selection matches the default image shown.
- Publish. Confirm the storefront displays a price range (e.g. $50–$80) and that selecting a different combination swaps the image and price.
Caveat: Every variation must have a price — a variation without a price cannot be added to the cart.
Caveat: Attribute term entry, the generate-variations button and default-form-values labels can shift between WooCommerce versions; verify the current interface.

Tags: store-setup, product-page, merchandising, variations, woocommerce, attributes, pdp
Source: WooCommerce Tutorial for Beginners 2026.docx

---

## Configure selling locations, shipping locations and customer location sensibly
Use when: Configuring store-wide General settings on a new store so checkout country fields and shipping match where you actually do business.
- Enter the store address first — it drives tax and shipping calculations.
- Under General > Selling locations choose 'Sell to specific countries' and select only the countries you actually serve (e.g. United States and Canada). This is the most commonly used setting in the source's web-design experience.
- Set shipping location to the countries you sell to rather than all countries, so you only ship where you do business.
- Set the default customer location to Shop country rather than Geolocate — the source recommends this because many customers use VPNs, so geolocation is unreliable.
- Skip address autocomplete unless you are willing to add the third-party plugin it requires.
- Enable taxes and enable the use of coupons, check the remaining boxes, and choose your store currency. Save.
Caveat: The source's preference for shop-country default over geolocation is a practitioner recommendation, not a rule — test it against your actual buyer mix.

Tags: store-setup, fulfillment, tax, shipping, woocommerce, settings, checkout
Source: WooCommerce Tutorial for Beginners 2026.docx

---

## Decide add-to-cart redirect behavior and product review permissions
Use when: Setting up Products settings on a multi-product store to reduce cart-page bounce and choose a review policy.
- In WooCommerce > Settings > Products, review the 'Add to cart behavior' option. The source advises against redirecting to the cart page when you have multiple products, because users get pulled away from browsing every time they add something.
- Choose measurement and dimension units matching your market (pounds/ounces for the US; kilograms/grams for Europe; inches or centimeters for dimensions).
- Under Reviews, decide whether to enable reviews at all, and whether to only allow reviews from customers who actually purchased. Star ratings can be enabled independently.
- Save changes.
- Optionally visit Inventory settings to enable stock management, and the Downloadable products settings if you sell digital goods.
Caveat: The source's own store leaves verified-purchase-only reviews unchecked; treat this as a policy choice, not a recommendation.
Caveat: The no-redirect advice is attributed to the source and suits catalog browsing; a single-product store may reasonably differ.

Tags: store-setup, cart, product-page, reviews, woocommerce, settings
Source: WooCommerce Tutorial for Beginners 2026.docx

---

## Set tax calculation basis correctly by origin vs destination state
Use when: Configuring WooCommerce tax settings before going live in the US, to avoid collecting tax on the wrong basis.
- In WooCommerce > Settings > Tax, keep 'Prices entered with tax' unchecked so product prices display without tax, which the source says is what most stores do.
- Set 'Calculate tax based on' to the correct basis: a handful of states (the source names Arizona, California, Ohio, Pennsylvania, Tennessee as examples) are origin-based, meaning you charge tax based on where you are physically located — use Shop base address. For most other states, use Customer shipping address.
- Verify your own state's status with a current tax reference (the source cites taxjar.com's map and state lists) rather than relying on the example list.
- Leave 'Shipping tax class' based on cart items unless you charge a single flat rate, in which case select Standard.
- Set rounding and rate naming as you prefer, and save — then add rates under Standard rates by inserting a row with country code (US), state code (CA), postcode, rate (e.g. 7.25), a tax name, priority for competing rates, whether the rate compounds, and whether shipping is taxable in that state.
Caveat: Origin-state lists and rates change over time — confirm with a current tax source; the source's list is illustrative, not authoritative.
Caveat: Enabled taxes are required before any of these settings matter.

Tags: store-setup, tax, woocommerce, pricing, checkout, compliance
Source: WooCommerce Tutorial for Beginners 2026.docx

---

## Use reduced tax rates for special product classes
Use when: Selling a catalog mixing physical and digital (or otherwise differently taxed) items on one store.
- Under Tax > Reduced rates, insert rows for special rates — for example in California, digital products carry no sales tax, so enter a 0% rate named 'Digital'. Save.
- Edit the affected product and open the General tab under Product data.
- Set Tax status and change Tax class from Standard to your reduced class (e.g. 'Reduced rate'). Update the product.
- Result: standard products use your general rate (e.g. 7.25%) while the digital product is charged at 0%.
- Confirm with a test checkout that the correct rate applies to each product type.
Caveat: Rate treatment per category varies by state/country — verify the actual taxability of digital goods where you are registered.
Caveat: Reduced-rate handling and labels may differ in current WooCommerce versions; check the interface.

Tags: store-setup, tax, digital-products, woocommerce, compliance, pricing
Source: WooCommerce Tutorial for Beginners 2026.docx

---

## Automate tax rates with the WooCommerce Tax plugin
Use when: You want hands-off sales-tax rates across many jurisdictions instead of hand-building standard and reduced rate rows.
- Go to Plugins > Add new, search for 'WooCommerce Tax', install and activate the plugin published by WooCommerce.
- Click Connect and create/authorize a free WordPress.com account when prompted — this uses the WordPress.com API.
- When connected, return to WooCommerce > Settings > Tax and enable automated taxes, then save.
- Rates are drawn from the connected tax service (the source cites TaxJar) which WooCommerce partners with, so they stay current.
- If you prefer full manual control, you can still maintain Standard and Reduced rate rows instead of enabling automation.
Caveat: Requires a WordPress.com connection and a live service; plugin name, connection flow and settings screens may change — verify in the current interface.
Caveat: Automation may not cover every edge case (mixed digital/physical rules), so spot-check representative products.

Tags: store-setup, tax, woocommerce, automation, plugins, compliance
Source: WooCommerce Tutorial for Beginners 2026.docx

---

## Build shipping zones with free shipping, flat rate and local pickup
Use when: Setting up shipping options for a store that ships to specific countries or regions.
- Go to WooCommerce > Shipping and click Add shipping zone; name it (e.g. 'United States').
- Set zone regions to 'Everywhere' if the zone name already reflects your selling countries and you ship to all of them, or restrict to specific states/regions if you only ship to some.
- Add a shipping method: choose Free shipping, then set its requirement — the options are no requirement, a valid free-shipping coupon, a minimum order amount, or a combination. The source uses a $100 minimum order amount as the free-shipping threshold.
- Add a second method: Flat rate, and enter a default rate (the source uses $5) for orders that don't qualify for free shipping.
- Add a third method: Local pickup, typically with a zero fee, and mark it not taxable.
- Save each method; the storefront cart then offers these options to the customer.
Caveat: All three methods being offered together assumes you accept pickup — omit it if you only ship.
Caveat: Zone and method labels differ slightly between WooCommerce versions; verify the current interface.

Tags: store-setup, shipping, fulfillment, woocommerce, checkout, cart
Source: WooCommerce Tutorial for Beginners 2026.docx

---

## Charge per-product shipping with shipping classes and per-class calculation
Use when: Your catalog contains items with very different shipping costs (small apparel vs heavy/bulky goods) and you need item-level pricing.
- Go to WooCommerce > Shipping > Shipping classes and add a class (e.g. 'Heavy' / heavy packages) and create it.
- Return to the shipping zone's Flat rate method and edit it. Keep the default flat rate (e.g. $5) for normal products, then add a per-class cost row for your heavy class (e.g. $10).
- Set Calculation type to 'Per class' rather than 'Per order'. Per class charges the rate for each item in the cart; per order applies only the most expensive shipping class across the cart, which undercharges mixed carts.
- Save the method.
- Edit each product that should use the class, open the Shipping tab under Product data, set its Shipping class to the heavy class, and update.
- Test with a cart containing both a normal and a heavy item to confirm both class rates apply as expected.
Caveat: Per-class is the source's recommendation for accuracy; per-order is a simpler but less precise alternative.
Caveat: The example rates ($5 default, $10 heavy) are illustrative — set your own based on real carrier costs.

Tags: store-setup, shipping, fulfillment, woocommerce, pricing, cart
Source: WooCommerce Tutorial for Beginners 2026.docx

---

## Connect Stripe and PayPal payment gateways
Use when: Enabling card and PayPal checkout on a new WooCommerce store.
- In Plugins > Add new, search for the Stripe plugin from the 'payment plugins' developer. The source specifically does not recommend the official Stripe plugin, stating it malfunctions often; the third-party plugin is described as an official Stripe partner and shows high ratings. Install and activate it.
- Likewise install and activate the payment-plugins PayPal extension when prompted.
- Create a free Stripe account — the source notes Stripe has no setup cost, no credit check and no monthly fee, only a per-transaction fee. Connect it from the plugin's settings, login in the browser, select the business, and connect; leave it in Test mode until ready for real payments.
- Create a PayPal Business account (a personal account will not sync with the site) and use the plugin's click-to-connect flow.
- Save changes; a card field and PayPal option then appear at checkout.
Caveat: The anti-official-Stripe-plugin opinion is the presenter's from his own experience — re-evaluate current plugin quality and Stripe's own recommended integrations before choosing.
Caveat: Fees, onboarding and whether a personal PayPal account works can change; verify current terms and interface.

Tags: store-setup, checkout, payments, woocommerce, stripe, paypal, plugins
Source: WooCommerce Tutorial for Beginners 2026.docx

---

## Run a test order to verify shipping, tax and checkout end to end
Use when: Pre-launch QA of checkout, shipping options and tax configuration in a new store.
- Add a product to the cart and view the cart: confirm the flat rate (e.g. $5) and local pickup appear and choose as appropriate.
- Increase quantity until the cart passes the free-shipping threshold (the source uses $100) and click Update; confirm free shipping becomes selectable, then proceed to checkout.
- Fill in billing details: confirm the country dropdown only lists your configured selling countries (e.g. US and Canada).
- Uncheck 'ship to a different address' if shipping to the billing address, or enter an alternate shipping address to verify separate shipping fields.
- With Stripe in test mode, enter test card number 4242 across the card field and any future expiry/CVC, then place the order.
- Confirm the order appears under WooCommerce > Orders with totals, line items, billing and shipping addresses — and that the My Account page shows the order for the customer.
Caveat: The 4242 test card only works while Stripe is in test mode; switch to live mode for real transactions.
Caveat: Tax shown depends on your origin/destination configuration — confirm it matches your intended rule.

Tags: store-setup, checkout, shipping, tax, testing, woocommerce, payments
Source: WooCommerce Tutorial for Beginners 2026.docx

---

## Manage and fulfill orders, issue refunds, and understand the customer My Account page
Use when: Post-purchase operations: fulfilling orders, handling refund requests, and supporting customer self-service.
- Go to WooCommerce > Orders and open an order to see status, order details, and billing/shipping addresses.
- Change the status to Completed and click Update, which notifies the customer that the order is done and shipping. (The source notes auto-fulfillment is an option you can configure, but by default orders sit as 'Processing'.)
- To refund, scroll to the bottom of the order and use the Refund action, entering the refund amount and confirming; test orders show $0 because no real funds exist.
- Direct customers to the automatically created My Account page, where they can view their past orders and totals, update addresses, update payment methods, and log in or out.
- Optionally offer social-login via a third-party WordPress plugin to simplify customer sign-in.
Caveat: Refund amounts on test orders will read $0 by design; real refunds require live payments.
Caveat: Status names and available actions may vary by WooCommerce version and installed extensions.

Tags: store-setup, fulfillment, retention, refunds, woocommerce, customer-accounts, orders
Source: WooCommerce Tutorial for Beginners 2026.docx

---

## Organize product categories and handle undeletable defaults
Use when: Tidying catalog navigation and category structure after a theme import on a new store.
- Go to Products > Categories in the dashboard. Themes often import categories you don't need.
- Select the unwanted categories and delete them.
- Note that one default category cannot be deleted. The source's workaround is to rename and repurpose it as a real category (e.g. rename it to your brand gear such as 'Daryl's Gear') and update it.
- Use that repurposed category as a legitimate part of your navigation, and make sure any products that land in it intentionally belong there.
Caveat: If you create categories, the source advises using the existing undeletable category as one of yours rather than fighting it.
Caveat: Category labels and the delete/rename flow may differ slightly by WooCommerce version.

Tags: store-setup, merchandising, categories, woocommerce, navigation, catalog
Source: WooCommerce Tutorial for Beginners 2026.docx

---

## Check email deliverability and customize transactional emails
Use when: After store setup, before launch, and when customers report missing order emails.
- Recognize that on a brand-new WooCommerce install, emails to customers often fail to send — plan to fix this before launch rather than after complaints.
- Configure SMTP settings (the source points to a separate free-plugin walkthrough) so order emails reliably reach customers.
- Review email recipients in WooCommerce > Settings > Emails: new-order notifications go to you, while processing/on-hold and similar status emails go to customers.
- Leave the default subject lines and headings as-is — the source recommends defaults for simplicity.
- If you want branded emails, install a free drag-and-drop email builder plugin and design templates visually, since the built-in email cannot be edited directly.
Caveat: The source warns plugin pop-ups and marketing nags appear in the WordPress admin; expect and dismiss them.
Caveat: Specific SMTP plugin and email-builder names are not given in this source — verify current options.

Tags: store-setup, retention, fulfillment, email, woocommerce, deliverability, notifications
Source: WooCommerce Tutorial for Beginners 2026.docx

---

## Tune coupon and review settings for a workable default configuration
Use when: Final pass through WooCommerce Products and General settings before launch.
- In General settings, enable coupons alongside taxes so coupon functionality is available for promotions.
- In Products settings, set weight and dimension units matching your market so shipping calculations and product details are correct.
- Decide the review policy: leave reviews open, or require a verified purchase, and independently enable star ratings.
- Leave the remaining product settings at their defaults unless you sell inventory-tracked or downloadable goods, then visit Inventory or Downloadable products settings accordingly.
- Revisit General > Accounts and privacy: the source calls disabling guest checkout 'a terrible idea' and treats the default account/privacy options as standard for ecommerce.
Caveat: The guest-checkout opinion is attributed to the source and reflects his experience; evaluate against your own conversion and account strategy.
Caveat: Default labels and option placement vary between WooCommerce versions.

Tags: store-setup, checkout, reviews, coupons, woocommerce, settings, conversion-optimization
Source: WooCommerce Tutorial for Beginners 2026.docx