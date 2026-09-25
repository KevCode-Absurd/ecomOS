# Shopify for Beginners: Everything From Setup to Your First Sale

source_id: 14IqjWo1w9zow-528ogyCrcKOs44cVS3R | folder: /05-SET-store-setup | cards: 124 | words: 79,117 | type: course (full-length video transcript, screen-recorded walkthrough)

credibility: A single unnamed YouTube creator/course presenter walks through building a Shopify store end to end, using a real demo store (a fictional activewear brand) built live during recording. The presenter identifies as someone who has set up stores for clients ("so many of my clients," "my clients") and cites a specific past client example (a premium pasta brand) once. Evidence is personal practitioner experience and live demonstration, not studies, published data, or audited results. The presenter openly states opinions as opinions in several places (theme preference, cart drawer vs page, tax display, checkout customization) and flags several claims as things to verify (plan-gating, feature availability, current pricing). There is a commercial angle: the video contains an affiliate signup link for Shopify and repeatedly offers a free companion "guide" in exchange for a comment, both promotional mechanics external to the course content itself and not reproduced here.

date signals: The presenter explicitly references "Shopify Winter Edition" changes happening during filming (a mid-recording update that altered the AI image-generation tool and added checkout flexibility), calls Shopify Markets "fairly new," calls the Shopify product Category/metafield system "relatively new," calls per-order quantity limits and self-return/store-credit features "new," and describes Shopify's ChatGPT product-listing integration as "still rolling out... not available for everyone," initially US-only. These are strong signals the source reflects a Shopify feature set from a specific recent release window, not a stable long-term baseline. Given how fast Shopify's admin UI, plan structure, pricing, and AI features change, treat every concrete number, price, plan name, and menu path in this file as dated and needing a live check, not as durable fact.

## 1. What this source is for

This source is a start-to-finish operator's walkthrough for building a Shopify store from an empty account to a launched, sellable storefront: signing up, choosing a plan, preparing brand assets, adding products and collections, choosing and customizing a theme (header, footer, homepage, collection pages, product pages), configuring checkout, discounts, gift cards, apps, speed, SEO, international markets, taxes, shipping, languages, payment gateways, pre-launch testing, order management, customer support, and analytics. It is written for a solo founder or small team setting up their own store, or an agency operator doing it for a client, with no assumed prior Shopify experience. Use it as the operational reference for "how do I actually configure X in Shopify" during a store build, not as a source of proven conversion benchmarks.

## 2. Principles

1. **Prepare brand assets before touching the theme.** Condition: before any theme customization work starts. Evidence: the source's own workflow order — logo, favicon, a 4–5 color palette with light and dark values, one or two Shopify-library fonts, and product/collection lists prepared up front, because doing so "makes our work way, way easier" later. [285d3b5212e7]
2. **Sign up with an email you personally control, never a contractor's.** Condition: whenever an agency, freelancer or employee is helping set up the store. Evidence: only the store owner can change currency, delete the store, and take other critical actions — the source states this as a hard operational rule, not a preference. [63c65895f090]
3. **Decide a collection's type (manual vs. smart) with future catalog growth in mind, because it cannot be changed later.** Condition: any time a new collection is created. Evidence: stated directly and repeated twice as a platform constraint, not an opinion. [f46060533ad6][221]
4. **Tag-based smart collections are the safest default organizing method.** Condition: building collections in a small-to-medium catalog. Evidence: the source's stated reasoning — "I think you can never get it wrong this way" — is presented as personal preference, but the mechanical risk it describes (typos silently breaking a rule) is a factual platform behavior, demonstrated live when a "bras" tag was mistyped as "browse." [12b8ef266d4c]
5. **A theme is a multi-year decision, not a cosmetic one — plan around future catalog size and required sections, not only current looks.** Condition: before shortlisting or trialing themes. Evidence: source frames this explicitly ("this is a one-time choice... think about it as something that's going to live with your brand for at least four or five years") and ties it to conversion, not just aesthetics. [0875899454b9][d936f750ed9d]
6. **Use dynamic sources (brand colors, metafields) instead of retyping the same value everywhere.** Condition: any time a value (a color, an image, text) needs to be reused across the theme or repeated with variation across many collections/products. Evidence: demonstrated for brand colors (change once at Settings > Brand, cascades to every linked theme field) and for collection/product content (metafields let one shared template show different content per record). [8de64df0eaa7][79db08591c6b][1b74e6a6d37e]
7. **Use a template only when the whole layout must differ; use a metafield when only the content must differ.** Condition: deciding how to vary a page across products/collections. Evidence: source states this explicitly as the dividing rule after demonstrating both mechanisms on collections and products. [79db08591c6b][1b74e6a6d37e]
8. **Build the product-page case from real objections, not assumptions.** Condition: before designing any product page. Evidence: source's method — study large competitors' PDPs and mine competitor/Amazon reviews for the specific hesitations buyers voice — illustrated with a real client case (premium pasta, taste and price-justification objections). [d4eba16b7f05][14e4f605117f]
9. **Scale product-page depth to price and complexity.** Condition: deciding how much proof/content a given product's page needs. Evidence: source's explicit heuristic — "the more complicated your product, the more expensive your product, the more detailed your product page should be" — contrasted against its own low-objection activewear example (size chart, fabric, durability) versus the high-objection pasta example (taste proof, scientific backing). [d1dc0a44255a]
10. **Repeat the same core claim in more than one format on a long page.** Condition: designing PDP or other content-heavy page sections. Evidence: stated directly ("people consume information in different ways"), illustrated with dog-supplement stores repeating benefit claims in both gallery images and page sections. [92d28259c9cb]
11. **Always configure a shipping rate for every country you intend to sell to, and prefer flat rates with a free-shipping threshold.** Condition: shipping and delivery setup for any market. Evidence: platform mechanic (no rate = Shopify marks the product unshippable there) plus a stated conversion argument (flat rates are easier for customers to estimate, reducing checkout abandonment). [4b035d79d6ee]
12. **Separate transactional consent from marketing consent, and only market to people who opted in.** Condition: setting up checkout's marketing-signup checkbox. Evidence: stated as a legal requirement (especially cited for Europe/UK) as well as a deliverability argument (opted-in subscribers open more). [ed38e3fd032c]
13. **Judge any Shopify app by reviews, its own demo store, and support responsiveness — not by its marketing claims.** Condition: before installing any third-party app. Evidence: stated directly ("so many apps are not as good as they claim to be"), demonstrated on the Judge.me install. [3f5560597133]
14. **Analytics need a long time window and, ideally, a comparison period before you draw a conclusion.** Condition: any analytics review. Evidence: explicit warning that a single day's conversion rate is not a representative average; demonstrated using 12-month and year-over-year views. [63acdbeb3fff]
15. **Retention/cohort data is not meaningful for a brand-new store.** Condition: interpreting the customer cohort/retention report. Evidence: stated directly — needs "roughly a year" of real order history to be readable. [d90fa94f0b55]

## 3. Procedures

### 3.1 Sign up and choose a plan
1. Click the signup link/button; enter a business email you check often (a personal Gmail is acceptable to start, but plan a branded address later). [63c65895f090]
2. Set a password, answer Shopify's basic business questions, add a payment method (card or PayPal). [63c65895f090] `[web check: current trial length and introductory pricing — the source describes both "7 or 14 day trial" and, separately, "3-day trial then $1/month for 3 months" in the same breath, an internal inconsistency in the transcript itself; verify the live offer.]`
3. Choose a plan: Basic, Grow, or Advanced (Shopify Plus sits outside these, ~$2,000–2,300/month `[web check]`, and is the only plan letting you fully customize the checkout page). [8c79cd592233][6f0629590ba6]
4. If your account is old/legacy, open Settings and audit which features you actually have rather than assuming your nominal plan tier's feature set — the source reports legacy accounts were migrated with inconsistent entitlements. [8c79cd592233]
5. Fill in business information and billing/legal address (drives which payment and shipping options, and which market features, Shopify offers you) and set the store name. Both can be edited later, but the source recommends doing them right the first time since the store name already appears in customer-facing emails. [e6e96ea93d3][63c65895f090]

### 3.2 Pre-build asset checklist (do before opening the theme editor)
1. Logo as a transparent PNG (use Canva, CapCut, or an AI background remover if you only have a colored-background version). [285d3b5212e7]
2. A simple square favicon (a single brand letter is enough). [285d3b5212e7]
3. A locked palette of 4–5 hex colors with both light and dark values for contrast flexibility, chosen to fit the niche (e.g. blues for water-related products). [285d3b5212e7]
4. One or two fonts from Shopify's font library (custom/non-library fonts need custom coding or a developer) — also check the same font (or a close match) is available in Canva for cross-channel consistency. [285d3b5212e7]
5. Product list, collection list, product photos, lifestyle photos, About Us copy — all prepared before building. [285d3b5212e7]

### 3.3 General settings
1. **Store details** (Settings > General): set store name (appears on order-confirmation emails) and store email (ideally a branded address you check often, e.g. hello@yourstore.com); set phone; set billing/legal address to your actual registration region — this drives available payment methods, shipping options, and market behavior. [e6e96ea93d3]
2. **Store defaults**: set currency to your registered region (e.g. EUR for a France-registered business); set the backup region (where customers outside your defined markets land by default); set unit system (e.g. kg); set order ID prefix/suffix if you want to obscure true order volume from customers (e.g. add "20" as a prefix). [e6e96ea93d3][285d3b5212e7]
3. **Store assets / Brand** (Settings > General > Brand): upload the rectangular logo, then a square logo (reuse the favicon here since favicons are already square); add hex colors — a primary, a light contrasting color, and secondary colors (4–5 total); optionally add a cover image, slogan, short description; add social links, at minimum Instagram, TikTok, Facebook — the source notes many new visitors check Instagram first, so missing links cost credibility. [1513317a812c]
4. **Users and permissions** (Settings > Users): upgrade plan if you need more staff seats than Basic allows; add a user by email (they get a staff invite); build a **custom role** — name it, describe it, then tick exact admin-area permissions (home, products, orders, markets, etc.) rather than a blanket default role; be deliberate about Orders access specifically, since it exposes sales figures. `[verify UI]` As a workaround to the seat limit, use **Collaborator access**: share your myshopify.com domain plus a collaboration code so a developer/app can request access without a paid seat. [b03f3e640118]
5. **Domains** (Settings > Domains): check domain availability when you first pick your brand name, before it's finalized. Buy either directly through Shopify (simplest, auto-linked) or through a registrar like GoDaddy and use "Connect existing"; if auto-link isn't available, manually add the DNS records the tool specifies (type, name, value — usually about 3 records) under the registrar's "Manage DNS" section, then wait for propagation. Prefer .com for recognizability; consider defensively buying other extensions (.co, .ae, etc.) so no one else takes them. Your default `storename.myshopify.com` domain stays important internally (support, some app configs) even though customers never see it. Apply the same DNS-record workflow later for Klaviyo/Omnisend sender-domain verification and review-app integrations. [b30915400ab6] `[web check: GoDaddy's cited "$0.01 first-year" domain price is a time-of-recording promotion, not a standing price.]`
6. **Policies** (Settings > Policies): use "Insert template" for each policy (privacy, terms of service, shipping, contact information, terms of sale, legal notice), then edit to match your actual business — do not publish templates unmodified. Configure the newer **Return rules** feature (set return window and return shipping rates) so customers can self-serve returns from their account. Note: the shipping *policy* is informational text only and does not affect actual checkout shipping rates, which are configured separately under Shipping and delivery. Publish (not just save) every policy before linking to it elsewhere, or the link won't resolve. Link all policies in the footer at minimum (the source treats this as required before running ads); link shipping/return policy on the product page too where relevant. Recommend legal review, especially for the EU and UAE; the UK is flagged as having its own distinct privacy-policy rules. [fe40994519f8] `[web check: current legal requirements by region.]`
7. **Customer support tooling**: start with the free **Shopify Inbox** for a new/simple store (shows customer order history alongside the chat so replies have context). For large catalogs or education-heavy niches (cosmetics, skincare, electronics), plan to move to an AI-assisted support tool — the source names **Gorgias** and **Tidio** as examples (its own audio said "Juy"/"TDO," which the card data resolves to these two names — treat the exact product match as uncertain and verify). [275ea2cf320b] `[web check: current tool names, pricing, capabilities.]`

### 3.4 Adding products
1. Products > Add product. For a small catalog, add manually one at a time; for a large catalog, use import; bulk editing (a spreadsheet-style grid) is available but described as "a little advanced." [c673b25c3ccd][f119acb5c204]
2. **Title**: saving auto-generates the URL slug; if you rename the title later, manually revisit and update the URL handle. [c673b25c3ccd]
3. **Description**: keep the inline description short — treat it as the copy next to the product photos, not the full sales argument; put deeper information into a properly structured product page below the fold for complex/technical products instead. Shopify has a built-in AI description generator; the source prefers ChatGPT. [c673b25c3ccd]
4. **Media**: upload all images in one batch, in one consistent ratio across the whole catalog (the source prefers square specifically because it can't mismatch). [c673b25c3ccd]
5. **Type**: set to the most specific descriptive term (e.g. "legging," not just "clothing") — this field feeds collection filters later, so precision now avoids rework. [59de72e661ee]
6. **Vendor**: your own brand name, or the actual third-party brand if reselling other labels. [59de72e661ee]
7. **Collection**: optionally assign manually; unassigned products default into the Home page collection. [59de72e661ee]
8. **Tags**: treat as internal organizing properties, not hashtags — decide the collections you intend to build first, then tag products to match (e.g. "leggings," "black leggings"). [59de72e661ee][12b8ef266d4c]
9. **Category**: pick the most precise Shopify category via the suggestion. This unlocks extra category metafields (e.g. legging → closing features; makeup → skin type, coverage) and can auto-suggest values like color from images — review auto-detected values before accepting, since accuracy is close but not perfect. [59de72e661ee]
10. **Pricing**: enter **Price** as what the customer pays today; to show a sale, put the original higher figure in **Compare at price** so customers see it struck through next to the current price (worked example: €100 compare-at, €60 price). Enter **Cost per item** (cost of goods only, not full landed cost) to enable later margin/audit calculations (worked example: €60 price, €20 cost). Use "sell by unit" only where genuinely applicable. [c7f6802299ac]
11. **Inventory**: turn tracking ON rather than managing stock outside Shopify. Fields: "in hand" (total), "available" (sellable — drops as orders come in), "committed" (rises with each order), "unavailable" (for damaged or intentionally-hidden stock, so it isn't lost from records). Enter at least one of SKU or barcode (a warehouse needs one to match what was ordered — the source notes you can even reuse the same value in both fields). Multiple warehouse locations each get their own quantity field once configured. Decide deliberately on "continue selling when out of stock." [23e7b8e73e4c]
12. **Shipping**: switch the weight toggle ON and enter a weight (worked example: 0.25 in the chosen unit) — leaving it off makes Shopify treat the item as **digital** and skip shipping entirely at checkout, even if you don't bill by weight (some warehouses still require a weight value). Fill customs/duties fields if shipping internationally. [530b3d95d941][e08f40db23df]
13. **Variants**: click "Add options" to define axes (worked example: Size — Small/Medium/Large; then Color — Navy/Red). Assign an image per variant/color; edit price and quantity per variant (worked example: 100 units each) if they differ. [0df57c8635cd][530b3d95d941]
14. **Color swatches**: Shopify links color variants to category metafields automatically, but default color extraction is not accurate — verify or override. Add new hex-coded entries as needed (search "[color] hex" if unsure); for patterns/textures (e.g. a lip-butter texture), upload a label image instead of a hex value. "Show only selected-variant images" on the storefront requires theme support — usually paid themes, not free ones. [4cb4b173c437]
15. **SEO fields** (per product): title, meta description, URL handle — fill these in for every product and collection as baseline SEO. [c673b25c3ccd][e076d09149bf]
16. Worked example: a yoga mat product in 3 colors (red pre-defined; "dark blue" and "dark green" had to be manually added with hex codes), priced at 45/45/45, quantity 100/100/100 per variant. [4cb4b173c437]

### 3.5 Bulk editing and cleanup
1. Products > select products > Bulk edit opens a spreadsheet-style grid. Use "Columns" to expose the fields you need (price, inventory tracking, tags, product type, metafields). [f119acb5c204]
2. Fill missing prices/quantities by dragging values down like a spreadsheet. [f119acb5c204]
3. Tag consistently — copy-paste tag text rather than retyping, to avoid silent typos (worked mistake caught live: "bras" mistyped as "browse," which broke the smart collection until fixed). [12b8ef266d4c][f119acb5c204]
4. Bulk edit has real limits for heavy/complex catalog changes; the source says a dedicated third-party bulk-edit app may be needed beyond a point. [f119acb5c204]

### 3.6 Collections
1. Products > Collections > Add collection. Name it, optionally add a description and image. [f46060533ad6]
2. Choose **Manual** (hand-pick products) or **Smart/automated** (rule-based) — this choice is **permanent once saved**. [f46060533ad6]
3. For smart collections, set one or more conditions (tag, product type, category, vendor, weight, inventory level, price, metafield) and choose whether products must match **all** or **any** condition. Worked example: an "Active wear" parent collection built with "any condition" across tag=leggings OR tag=bras OR tag=overall, pooling several tag-based sub-groups into one parent. [f46060533ad6][646e5b63a24f]
4. A single product can belong to multiple collections at once. [f46060533ad6]
5. Worked examples built live: Leggings (tag=leggings), Bras (tag=bra/bras), Accessories (tag=accessories), Overalls (tag=overall), Bestsellers (tag=bestsellers, applied to ~4–5 hand-picked products via bulk edit). [8a469102152c]
6. Other collection strategies beyond tags: price (e.g. a sub-$50 gift guide), inventory level (e.g. a clearance collection of near-sold-out items), category, vendor, weight, variant. [f46060533ad6][528c1525c249]

### 3.7 Filters (storefront navigation)
1. Install the free **Search and Discovery** app (native Shopify). It covers filters, on-site search, and product recommendations. [236052ce217f][d21ee63adb13]
2. Filters > default filters are Availability and Price (remove if not useful) > Add filter > choose a source: a category metafield, a standard field (e.g. vendor), or a custom product metafield. [236052ce217f]
3. To check which categories a given category metafield applies to: Settings > Custom data (metafields and metaobjects) > Products > "Assigned to categories." [236052ce217f]
4. To add a filter beyond the default category metafields: Settings > Custom data > Products > Add definition > name it > choose "List of values" if one product can hold multiple values for that filter (e.g. a product available in both gold and white gold) > set field type (e.g. single line text) > assign to specific categories or leave open > Save > fill the field per product (individually or via bulk edit) > return to Search and Discovery > Add filter > select the new metafield as the source. [3ce1b240ca4f]
5. Populate the underlying product data — a filter with only one visible value usually means the field isn't filled on other products yet; bulk-edit to fix it. Keep spelling/casing consistent ("legging" vs "leggings" will fragment into two separate filter options). [b9eb3390c92d]
6. Order filters within the app (order is app-controlled, not theme-controlled). [b9eb3390c92d]
7. Choose which filters to expose by studying (a) Shopify's own auto-suggested category metafields as a baseline, and (b) competitor/large-store filter choices in your niche, and (c) how customers actually phrase searches — don't expose every possible attribute. [528c1525c249]

### 3.8 Choosing a theme
1. Before browsing, list the features/sections you want (visual effects, comparison tables, before/after sliders, UGC galleries, ingredient panels) based on competitor research and your own plan for the store's future. [0875899454b9]
2. Online Store > Themes shows the current free default (source cites "Horizon") plus more free themes on scroll, or click "Visit theme store" for the full library with filters: Industry (niche, e.g. Beauty), Catalog size (roughly 11–100 vs 500+ products — larger catalogs push toward heavier search/navigation-focused themes), and Features (before/after slider, color swatches, combined listing, age verifier, RTL/Arabic support, mega menus, sticky header). `[verify UI]` [36f8551b5974]
3. The source generally prefers **paid** themes ($100–$400 one-time `[web check]`) over free ones for quality/features, framed explicitly as its own opinion. [36f8551b5974]
4. Open each shortlisted theme's demo store: check section variety, PDP layout, social-proof placement — and note that any feature/section shown in **any** demo preset of a theme is available across the whole theme (presets can be mixed and matched). [35eac0a86ba9][e5fb740fbeed]
5. Check the mobile preview specifically — most traffic is mobile. [35eac0a86ba9]
6. Vet the developer/company behind the theme: click through their profile, see how many themes they publish, Google them (worked example cited: "Clean Canva," an unpaid mention, praised for a large catalog and being well-maintained). [36f8551b5974]
7. Confirm the theme's actual section library includes anything niche-critical (e.g. a before/after slider for a skincare brand) before committing — a missing section can't reliably be added later without custom work or the AI section generator. [e5fb740fbeed]
8. Click **"Try theme"** to install a full, free, editable-but-not-publishable trial on your store; build it out (home, PDP, coming-soon page) to confirm fit before buying — clicking **Buy** later preserves all trial work. [e0fbc88d7b2]
9. Before major edits or updates, **duplicate the theme** (three-dot menu > Duplicate) as a restore point; use a dedicated backup app for versioned/scheduled backups if you need more than a snapshot. [851254972d2]
10. The source explicitly advises against relying on Shopify's one-click AI whole-store theme generator as your final storefront — treat it as a rough starting idea at most, and instead design deliberately for conversion (legibility, easy product discovery, visible social proof), calling this its own stated opinion. [d936f750ed9d]

### 3.9 Coming-soon / password page and early access
1. Every new Shopify store is password-locked by default (Settings > Preferences, or the account's password page settings) `[verify UI]`; verify by opening your live domain in an incognito window — you should see a "coming soon" page with a password field. [b8f482b2f3d9][a5598af5de1a]
2. Customize the coming-soon page under Online Store > Themes > Password — it behaves like any other theme page (sections, background image, etc.); check text contrast if you add a background image. [b8f482b2f3d9][a99b97dacf98]
3. Turn off password protection when ready to launch, or customers will keep seeing the coming-soon page. [b8f482b2f3d9]
4. Optional tactic: share the password with a waitlist a few hours before public launch for early access (source's own client example, presented as one approach, not a guaranteed outcome). [a5598af5de1a]

### 3.10 Theme editor orientation
1. Location selector: start on **Store Default**; per-market/per-country customization (e.g. a French-flag banner shown only in France) is available on higher plans — presenter believes this is not available on the base plan, but is unsure; verify. `[web check]` [e5222e8988f5]
2. Page selector defaults to Homepage; switch to edit Products (default template), Collections, Pages, etc. [e5222e8988f5]
3. **Sidekick** button opens Shopify's AI assistant — useful for quick data questions (e.g. "how many of X have I sold") without leaving the editor. [e5222e8988f5]
4. **Inspector** toggle: on, hovering highlights clickable elements; off, navigate via the sidebar section list instead. [e5222e8988f5]
5. Desktop/Mobile/Full-screen view toggles — treat the in-editor mobile view as "accurate but not 100% accurate"; always confirm with a real preview link. [e5222e8988f5][81776b16a7c]
6. Getting a shareable preview link: for an **unpublished/trial** theme, three-dot menu > Preview > "Copy preview link." For the **published/live** theme, three-dot menu > Preview > right-click > "Copy link address" (a different flow). `[verify UI]` [81776b16a7c]
7. Since a recent update, product/collection/page **content** (title, description, rules) can be edited directly from inside the theme editor via an "Edit" popup on the section, without leaving to the backend admin — though richer product data entry, menu creation, etc. still require the backend. [540e68dc8bce]
8. Sections vs. blocks: a section is a page component (e.g. header, featured collection); a block is an item inside it (e.g. one announcement message). Clicking the section edits section settings; clicking a block edits that block's settings. [53605e79474b]

### 3.11 Theme settings: colors, typography, product cards
1. Define brand colors first under Settings > Brand (see 3.3.3), then in the theme editor's **Colors** panel click the dynamic-source icon on each field and connect it to a saved brand color instead of retyping hex codes — a later brand-color change then cascades everywhere it's linked. [8de64df0eaa7]
2. Map deliberately: text/headings to primary, links to an accent color, sale badge to accent (so it stands out); leave states you won't use (e.g. low-inventory label) unstyled to save time. [8de64df0eaa7]
3. Configure primary button (background, hover background, text) and secondary button (often white background, bordered) — these apply across the store (Add to cart, checkout, etc.). [868b9d497999]
4. Full-store background: keep white for readability; an image background is possible but not recommended (adds repeat/tile complexity). [868b9d497999]
5. Header colors: background, text, main menu link color, hover color, featured-link color. [868b9d497999]
6. Image overlays: an adjustable-opacity dark layer over hero images to make text pop — tune this after real images are uploaded, not during initial setup. [868b9d497999]
7. **Section color schemes**: pre-built combinations of your brand colors (background/heading/text/links/buttons) that let sections alternate visually instead of looking monotonous. Build at least 2 schemes and assign them to alternating sections. Availability and count vary by theme; some themes don't support schemes at all and only expose color at the theme or section level. [868b9d497999]
8. Typography: choose fonts from Shopify's library (see 3.2.4). Set heading font (with optional all-caps, letter spacing), body/button text font, navigation font, store-name font — check the style/weight dropdown after picking a font. Set sizes for heading/base/navigation/store-name separately. Choose button text case and corner rounding if the theme offers it (avoids needing custom CSS). [65f4ccd810fb]
9. **Product cards** (how a product looks in a grid/listing — a term recurring across all Shopify themes): choose image shape (square/portrait/landscape). If images aren't uniformly pre-sized, most themes will **crop** to force the chosen shape — set the crop alignment (top/middle/bottom) to control what survives; the reliable fix is uploading pre-sized, consistent images from the start. Set mobile products-per-row (the source recommends **2**, not 1, for usability); set card text alignment (center is common); optionally enable a second image on hover; configure quick-buy behavior (button vs. "whole product" opens the PDP) and overlay-label position/behavior (e.g. show sale reduction as percent or value). [88cfe2d43556]

### 3.12 Header and menus
1. **Announcement bar**: add up to ~3 messages (a common theme limit `[verify UI]`); each can link out (e.g. to the shipping policy) and optionally show a countdown timer with an end date; style per-message or inherit the section style. Optionally enable a country/region selector (important for multi-market sellers so shoppers see correct stock/pricing/shipping for their own region) and a language selector. [53605e79474b]
2. **Header**: set logo width and mobile logo size; enable **sticky header** (source recommends this — keeps navigation visible while scrolling); optionally enable a transparent header (can assign a separate logo variant for it). [53605e79474b]
3. **Menu / navigation**: build the menu under Content > Menus (Shopify auto-creates a default "Main menu" with Home/Catalog/Contact). Add menu items, nest them by dragging to create up to 3 levels; use "#" for a non-clickable parent, or link directly to a Product/Collection/Page/URL. This nested structure renders as a **mega menu** automatically. Link the finished menu in the header's Navigation setting. [53605e79474b][1eaac2268d09]
4. Build navigation around **multiple mental models** a shopper might use (e.g. Shop > Clothes > Leggings AND a separate Shop by Activity > Yoga path to the same products) since different shoppers search differently — some want a specific product type, others browse a broad category. The source's example draws on the navigation pattern of "Decathlon" (named twice in the transcript audio; note this conflicts with the card index, which names "Lululemon" for the same example — see section 9). [1eaac2268d09]
5. Some themes support a **menu promotion** block attached to a top-level menu item (an image + CTA panel inside a mega-menu dropdown) — useful for spotlighting a featured collection, especially in higher-end niches. [1eaac2268d09]
6. Keep the header group minimal — anything added there repeats on every page, so avoid stuffing it with extra marketing content beyond navigation and maybe a slim trust-message bar. [53605e79474b]

### 3.13 Footer
1. Set footer background/text/heading colors globally in theme Colors settings first. [5b24de26c78a]
2. In the footer section, add blocks: Text (logo + short copy), Link list(s), Newsletter (optional — the source suggests hiding it if popups already capture signups). [5b24de26c78a][7ac89fa59ccf]
3. Build the footer menus in the backend first: Content > Menus > create separate menus (e.g. "Helpful Links" for all policies, "Quick Links" for About Us/Contact/Support) rather than one long list — modeled on how larger retailers split footer navigation into service/help/about columns. [7ac89fa59ccf]
4. Generate and publish every policy (Settings > Policies) and create an About Us page (Online Store > Pages) **before** trying to link them, since unpublished pages have no URL. [7ac89fa59ccf][5b24de26c78a]
5. Back in the theme editor, point each footer Link-list block at one of the menus you built; add multiple Link-list blocks side by side and rename each block's heading (e.g. "Support") for scannability. [7ac89fa59ccf]
6. Avoid adding unrelated sections (e.g. a scrolling press-logo banner) into the footer group beyond links/policies, for the same "appears on every page" reason as the header. [5b24de26c78a]

### 3.14 Homepage
1. Build in a deliberate order: (1) hero — slideshow or short background video, 1 image or up to 2–3 slides max, each stating what you sell/announcing a collection and linking directly to it; (2) a USP/logo-list section (each block = one selling point: image, title, link — the same section type also works for press logos/certifications); (3) a Featured Collection section for **bestsellers** (source's stated position: "bestsellers are bestsellers for a reason... always show them"); (4) a Collection List section; (5) an Image-with-text section linking to About Us; (6) a Testimonial section with real reviews/photos; (7) anything else only as needed (blog teaser, rich text) — delete unused theme defaults rather than keeping them. [c92800a72acd]
2. Hero settings: click the **section** (not a slide) for height mode — "adapt to first image" (best if images are pre-sized correctly, shows the full image uncropped), "full screen," or "fixed height" (worked example used ~600px on both desktop and mobile as a starting point, not a benchmark). Set a separate mobile image if the theme supports it, rather than accepting a bad automatic crop. For images that still crop badly, open the image editor and set a **focal point** (e.g. a model's face) so cropping preserves it. Give each slide a full-slide link as an alternative to a visible button. Avoid "show text below image on mobile" when a dedicated mobile image is available. [72785e7b693e]
3. Use **Duplicate** to create sibling blocks with identical dimensions (e.g. size the first USP logo correctly, then duplicate rather than resizing each one individually — the source explicitly regrets not doing this the first time). Use **Copy** on a section, then **Paste**/"Paste after" on another page to reuse a whole section elsewhere in the store. [333ea959bee7]
4. Worked bestsellers build: tag ~4–5 hand-picked products "bestsellers" via bulk edit > create a smart collection with condition tag=bestsellers > add a Featured Collection section pointing at it > optionally assign a different color scheme to that band. [8a469102152c]

### 3.15 Collection pages
1. Open Edit theme > Collections > **Default collection** — this one shared template applies to every collection not otherwise assigned (worked example: 6 collections shared one default template). Configure once: show/hide title, show/hide header image + height + overlay + description, products-per-page and per-row (source chose 3-per-row for bigger images), show/hide vendor, show/hide product count, default sort order (bestselling, alphabetical, price). [7516ecaaead1]
2. Only create a **separate named template** (Collections > Create template) when a specific collection needs a genuinely different layout (e.g. a subcollection banner row); assign it to that collection from the collection's admin page once the theme is published. [7516ecaaead1]
3. To simulate a subcollection row inside a parent collection page: create a dedicated template for that collection, add a Multicolumn section above the grid, fully configure the first block (image, title, link to the subcollection), then **Duplicate** it per remaining subcollection (preserves sizing) and swap image/title/link; hide the parent collection's own title/count so the row reads as primary navigation; consider transparent-background product images for a cleaner look. [19d381b1ed94]
4. **Color swatches** on the collection grid: enable in the theme's swatch settings, then choose **color list** (define each variant's name + hex — search "[color] hex" if unsure) or **variant image** (theme pulls the actual per-variant photo — the source's own preference); for custom swatch graphics, upload an image file named exactly after the variant value (e.g. `red.png`). [dfd27ace3b6b]
5. **Collection metafields** for varying content within one shared template: Settings > Custom data > Collections > Add definition — create typed fields for each element that must vary (e.g. an image-type "promotion section image," single-line-text "promotion section title," rich-text "promotion section text," URL-type "promotion section link"). In the theme editor, connect each section field to its metafield via "connect dynamic source." **Troubleshooting rule**: if a metafield doesn't appear as a selectable source, its type doesn't match what that field expects (worked example: a "Link" type metafield didn't work for a button link, but "URL" type did — trial the type). Fill the metafield per collection (individually or via bulk edit); an empty metafield renders nothing. [79db08591c6b]

### 3.16 Product pages
1. Research first: list competitor PDPs' sections; read reviews (including Amazon) for the objections buyers actually raise; convert each objection into a page element (client example: a premium pasta brand needed reviews/video proof for the taste objection, and numerical/scientific facts for the price-justification objection). [d4eba16b7f05][14e4f605117f]
2. Build the **default** product template first with everything common to all products (benefit blocks, dividers, description placement); create additional templates only where a category's layout genuinely differs (e.g. one for bras+leggings, one for accessories); use metafields, not new templates, when only content (not layout) needs to vary per product. [1b74e6a6d37e]
3. Section settings to decide deliberately: **"select first available variant"** — keep ON for frictionless checkout, or turn OFF if you're worried customers will buy without consciously choosing size/color (fewer wrong-variant complaints, more clicks required); hide the vendor block unless reselling multiple brands; keep **sticky add-to-cart** ON, especially on mobile; keep breadcrumbs (helps SEO); keep image zoom ON if photos are high quality. [2efef89fb3bf]
4. Media layout: choose image size/layout (large single images suit jewelry/luxury; smaller/collage layouts suit stores wanting more images visible) — test combinations, since some (e.g. left-side thumbnails) can break scroll behavior in a given theme. Enable "show alt text over image" to display each photo's alt text on the storefront (worked example: "legging front view," "full body view"). [2efef89fb3bf]
5. **Variant image grouping** (showing only the selected color's photos): check if the theme has a native toggle (most professional themes do); if not, the fallback is tagging each image's alt text with the exact variant name (e.g. "red") and uploading all of one color's images together before the next color's. Check the theme's help center if a demo shows grouping but you can't find the setting. [08b36113927c]
6. Content order above the buy button: move the short description above the buy buttons (not below the media); add a 3–4 bullet benefits list for solution-type products, built as a rich-text **metafield** (e.g. "USP/benefits") connected via dynamic source so it's per-product and empty where unfilled. [458ba19e94c4]
7. **Size chart**: enable the theme's size-guide option and link either (a) one shared static Page (Online Store > Pages — build a table, or use "Show HTML code" to hand the raw HTML to an AI tool for a cleaner table, then paste it back; must be published and the editor refreshed before it's selectable) or (b) a page-type **metafield** ("size chart page") per product if charts genuinely differ by category. [99e2ef1ab894]
8. **Collapsible tabs** for FAQ-style content: Description (link to the product description rather than retype it), Fitting, Shipping and returns (source's practice: a short summary in the tab — e.g. "free shipping over $100," "30-day money-back guarantee" — plus a link to the full policy, rather than pasting the whole policy inline; publish the policy page first), Care guide. Use a metafield if the tab's content must vary per product; type it directly if universal. Add small icons per tab where supported. [922844ff8bf9]
9. **Fit/true-to-size rating** block, if the theme offers one (source cites Symmetry's version, likened to Adidas's) — make it per-product via a metafield. [6eff9d71aa70]
10. **Buy buttons**: "Buy it now" is a Shopify dynamic one-click button that only appears with Shopify Payments active, and displays the shopper's most-used wallet (Apple Pay/Google Pay/PayPal); keep it for single-item-purchase products, hide it if customers typically buy multiple items (so they go through the cart instead). Hide the quantity selector if multi-unit purchases are rare, to save space. [fd255645fcbc]
11. **Complimentary products** (Search and Discovery app > product recommendations): manually choose 1–2 tightly-relevant add-ons per product (e.g. a bra as the complimentary item for a legging) — the analogy given is an iPad case/screen-protector recommended alongside an iPad. Related products auto-populate by default and are editable; the complimentary slot is empty until manually set. Keep it to 1–2 items, not many. [10f587c95a2d]
12. Below the buy area: copy a homepage USP/trust section onto the PDP (sections copy between pages in seconds) and adjust its color scheme to contrast; optionally add a **hotspot**/feature-highlight section (an image with named, clickable feature callouts), theme-dependent, and make its content per-product via metafields. [a9c942e14d9d]
13. If the theme is missing a needed section (e.g. a comparison table), buying the theme unlocks Shopify's **AI section generator**: Add section > Generate > describe what you want; refine with follow-up prompts before saving; a useful tactic is asking a general AI chat tool to write the prompt for you first. Output quality is described as unpredictable and can carry device-specific bugs — the source does not recommend this as a first-choice method for total beginners, preferring a theme that already has the needed sections natively. Once generated, a section is reusable everywhere via "AI generated sections." [82e21838aca5]

### 3.17 Other storefront pages
1. **All-collections page**: hide the default flat list and rebuild with grouped Collection List sections (worked example: one "Active wear" group with Leggings/Bras/Overalls at 3-per-row, a separate Accessories group) — modeled loosely on how large-catalog stores group sub-collections into themed blocks. [b69485cbf3ff]
2. **Gift cards**: Products > Gift cards > create a gift card product like any other (name, description, image/design, preset denominations — worked example: $10/$25/$50/$100). Shopify gift cards are **digital-only** by default; buyers choose to send to themselves or a recipient email, with a message and a scheduled send date. A physical-card option must be offered and fulfilled manually if wanted (source has seen clients do this). Run gift-card promotions right before holidays for last-minute buyers who've missed shipping cutoffs. [74d169e9b59c]
3. **Cart page/drawer**: choose **Drawer** (popup overlay on Add to cart — source's preference, since a full Cart Page redirect forces an extra click back to keep shopping) or **Page**; test which actually converts for your own store rather than assuming. Optionally add a free-shipping progress bar to the drawer. Keep this page/drawer simple; app blocks or product recommendations can be added but aren't required. [ed834e77dbd7][bb2d96464355]
4. **Static pages** (About Us, etc.): a page with only pasted text renders as plain/static. To design it, create a page **template** and build with sections (image-with-text-overlay, rich text for the story, video-with-text, scrolling panel) exactly like any other page, then assign the template from the page's admin selector. Since static pages don't vary per record, metafields aren't needed here. [fe0d110afd3a]
5. **Blogs**: Content > Blog posts to add posts; Manage Blogs to create separate blog "families" (worked example: default "News" blog plus a new "Workout" blog) so different content types can be organized and linked separately (e.g. link "Workout" specifically in the main menu). Configure the blog **listing** page (list vs. grid, image ratio, show/hide author and date) separately from the individual post template. [84395806f96]
6. **Search page, password page, error page**: adjust search-page settings (optionally add sections like product recommendations); treat the password/coming-soon page like any normal page (background image, form) but check text contrast; leave the 404/error page alone — the source explicitly advises not touching it. [a99b97dacf98]
7. **Advanced/custom CSS**: currency formats and "advanced" filter/link settings are minor and usually fine at defaults. Theme-level custom CSS overrides display globally without touching theme files (a lighter, lower-risk alternative to editing theme code); section-level custom CSS scopes to just that section. Skip entirely if you're not comfortable with CSS — everything works without it. [cfa8eb8e67cf]
8. **Theme style presets**: a quick way to switch between a theme's built-in demo styles as a starting point — useful mainly if you'll keep most default section content; less useful if you plan to replace nearly everything anyway (in which case verify your brand colors/typography survive the switch). [5a6b353794866]

### 3.18 Checkout and customer accounts
1. **Platform constraint**: checkout customization is heavily locked on all non-Plus plans. Only Shopify Plus allows adding checkout blocks, notes, upsells/cross-sells, or forcing dropdown-style address fields. On non-Plus plans, apps can still show/hide specific **payment methods** by country/audience (worked example: showing Cash on Delivery only to France). The source frames the lock partly as a deliberate security/trust design choice — a consistent, familiar checkout across all Shopify stores — while also noting Shopify has been progressively adding checkout flexibility over recent releases, so re-verify current limits. [6f0629590ba6][b7733d8e8e98]
2. Checkout > Customize (theme editor): add a logo (worked example: sized to 170 `[verify UI]`), set alignment; set background color(s) to match brand; set the accent color (buttons, error messages) to match your storefront's contrasting color for consistency; choose **one-page checkout** over multi-step (source's explicit recommendation). Blocks addable to Review/Thank-you/Order-status/Orders/Profile pages are limited to what your installed apps provide. [77c72b3e8b087]
3. **Contact method**: set to **email only** (not phone) so every buyer supplies an email; collect phone separately and make it **required** at the shipping-address step instead — especially important if offering Cash on Delivery. Require **last name only** (customers fill first name anyway); skip company name unless B2B; leave address-field defaults unless your warehouse needs something specific; don't force account creation before checkout. [47c8ccf3f338][d96aa79663]
4. **Marketing consent checkbox**: giving an email/phone for order fulfillment is not marketing consent. Turn on the checkout subscribe checkbox (separately for email and SMS). Pre-selected (checked by default) yields more subscribers but lower engagement; unchecked yields fewer but more engaged ones — source's own rule of thumb is pre-select for a new business, leave unchecked for an established one with heavy traffic. Shopify supports configuring this **per country** (e.g. pre-selected in the US, unchecked where pre-selection isn't legal, cited as parts of Europe/the UK `[web check]`). Only send marketing to people who actually consented. [ed38e3fd032c]
5. **Abandoned checkout email**: turn on Shopify's native version if you don't yet have a dedicated ESP (Marketing > Automations > "Recover abandoned checkout"); if you already run Klaviyo or Omnisend, build the flow there instead and leave Shopify's native version off to avoid duplicate messages. This is distinct from Shopify's fixed **notification** templates (order confirmation, shipped) which are separate and Shopify-controlled. [67507a55b77]
6. **Per-order quantity limit** (a newer feature): checkout advanced preferences let you cap units per product per order (worked example: cap at 10) — used both to protect scarce stock from one buyer and to obscure your true inventory depth from customers. [f6e33255728a]
7. **Customer accounts**: choose the newer **passwordless** "Customer accounts" (login via emailed passcode) over "Legacy" (email+password) — legacy is only worth considering for marketplace-style stores needing formal merchant signup. Optionally brand the customer-account/order-status domain (requires the same DNS-record process as domains). Optionally enable social sign-in (Shop/Google/Facebook), self-return (requires return rules configured first), and store credit (customers can spend a refund as store credit instead of cash). [abc432db1669]
8. **Tipping**: available but the source leaves it off by default. [d96aa7966303]

### 3.19 Discounts and gift cards (promotions)
1. Discounts > Create discount. Choose one of 4 types: **Amount off products**, **Buy X get Y** (BOGO), **Amount off order**, **Free shipping**. Each can be a manual **code** (customer types it) or **automatic** (applies with no action). [bd76d7f8a46b]
2. Use a **code** specifically when you need attribution/distribution (an influencer's unique coupon so sales are traceable to them, or a code embedded in a welcome-email flow); default to **automatic** otherwise, since it's more frictionless. [bd76d7f8a46b]
3. Configure per discount: eligible customers (all / a segment / specific customers), minimum purchase requirement, usage limit (e.g. one use per customer), combinability with other active discounts, start/end date, and whether the discount is visible on connected channels (Facebook/Instagram) — explicitly turn this **off** if you don't want it applying to those channel's sales. Worked example: code "BlackFriday30," 30% off, on 2 specific products. [bd76d7f8a46b]
4. After saving, share a **pre-applied discount link** (not just the raw code) for email/ad buttons so the discount auto-applies at checkout with zero customer effort; keep the raw code available separately for cases needing manual entry (e.g. printed on packaging, spoken by an influencer). [fc3d5032c0d2]
5. **Known platform gap**: Shopify cannot natively cap the *maximum* amount saved on a percentage discount (e.g. "30% off, capped at $100 saved") — this matters most at high average order value (worked illustration: a $1,000 AOV store offering uncapped 30% off). A third-party discount app is the workaround; no single app is named as covering every case. [447fe9aa14c2]
6. **Gift cards**: see 3.17.2 above. [74d169e9b59c]

### 3.20 Apps
1. Vet every app before installing: read the listing's feature description and screenshots, read merchant reviews (many apps "are not as good as they claim to be"), open the app's own **demo store** if offered, and verify support actually responds — before committing budget or time. A low review count isn't automatically disqualifying for a genuinely niche need. [3f5560597133]
2. **Installing an app is not enough** — you must also enable its **App embed** in the theme editor (Edit theme > App embeds tab) or its storefront-facing blocks/widgets won't appear. [3f5560597133][00e6bb4974e0]
3. **Reviews app** (source's top recommendation): should support automated post-purchase email review requests, ideally letting customers review directly inside the email. Named recommendation: **Judge.me** (source calls it currently one of the best-reviewed apps, cheap, practical, good support; the source previously preferred **Stamped.io** and still suggests it if you specifically also want loyalty-program features). `[web check: current app landscape, features, pricing.]` [13d14684d9ef]
4. **Judge.me setup walkthrough**: install > "install review widget" (opens theme editor at the product-page level; the "leave a review" block is pre-placed) > add a **star ratings** block via Product information > Add block > Apps > Star ratings, positioned under the price > if the store already has customers, consider holding back visible widgets until you've bulk-requested reviews from past customers (last 6–12 months) so the storefront doesn't launch showing zero reviews > pricing: a forever-free plan plus a paid "Awesome" plan (~$15/month `[web check]`, with a 15-day trial shown in the demo). [00e6bb4974e0]
5. **Judge.me review-request emails**: set request delay under "manage email review request" (defaults shown: 14 days domestic, 5 days for another order type — treat as illustrative, verify current app defaults) with separate delays possible for international/POS orders; edit templates (trigger style — button vs. stars, subject line, copy) and apply global template styling (logo, brand colors, fonts) across all its emails; build a fully custom drag-and-drop template (e.g. a "classic form" block) if you want customers to review directly inside the email rather than clicking through; set moderation rules to require manual approval before reviews go live if you want full editorial control. [fd106fda6cf6]
6. **Judge.me extra features**: import existing reviews (e.g. from Amazon or a spreadsheet); **product groups** to share reviews across related listings (e.g. a bundle and its standalone component product); per-widget "Customize" editors with live preview for matching brand colors/fonts; source specifically calls out Judge.me's support responsiveness as a standout. [07c9c7d8dbc9]
7. **Bundling app**: Shopify's own free native app combines products and auto-manages combined inventory (buying a bundle decrements each component's stock); adequate for beginners but with real limits for more sophisticated bundle logic, per the source. Pair bundles with a small discount to lift average order value. [a517b976f014]
8. **Subscription app**: Shopify's own free native app. Explicit niche-fit judgment required — good fits cited: supplements, food, coffee, makeup; poor fit cited: electronics. Frame subscriptions as a retention tool. [a517b976f014]
9. **Search and Discovery**: reiterated as a free, must-have native app that now covers filters, search, and product recommendations — the source explicitly recommends uninstalling older paid apps that did the same jobs and consolidating here. [d21ee63adb13]
10. Other app categories mentioned without a specific pick: post-purchase upsell apps, video-testimonial-on-PDP apps, loyalty/rewards apps, affiliate-program apps — evaluate each via the same vetting method above. [3f5560597133]

### 3.21 Speed
1. Track Shopify's built-in speed metrics under Online Store analytics once you have traffic — the source names **LCP** and layout shift among the metrics to watch (audio was garbled here; likely refers to Core Web Vitals — verify exact current metric names in your admin). `[web check]` [cb7f3ba4e5c9]
2. Uninstall apps you don't actually use — apps inject code into the theme and can slow it down. [cb7f3ba4e5c9]
3. Don't upload unnecessarily large/high-resolution images; many good paid themes already auto-compress, and dedicated compression apps exist as a fallback. [cb7f3ba4e5c9]
4. Re-check speed metrics after any change (new app, new theme) to attribute a regression to a specific cause; don't over-index on speed, but do monitor it. [cb7f3ba4e5c9]

### 3.22 SEO and AI-era discovery
1. Fill SEO fields on every product and collection (title, meta description, URL handle); complete store-wide SEO under Online Store > Preferences (social sharing image, homepage title, homepage meta description). [e076d09149bf]
2. Publish blog content over time — the source's framing (its own opinion, flagged as such) is that this now matters as much for signaling "trustworthy/authentic" to AI recommendation systems as for direct search-ranking traffic, since shopper behavior has shifted toward asking AI assistants directly. `[web check: unverified/forward-looking claim.]` [e076d09149bf]
3. The source describes Shopify integrating with ChatGPT so merchant products can be surfaced/checked-out within ChatGPT — stated as still rolling out, initially US-only, and "not available for everyone" at recording time. `[web check: current availability, mechanics, and naming of this integration.]` [e076d09149bf]

### 3.23 Shopify Markets (international selling)
1. Find **Markets** in the left sidebar (or under Settings if that update hasn't rolled out to your store `[verify UI]`). Your registered business country becomes the first/default market automatically. [8597c5d851d5]
2. Create a market > name it (e.g. "Europe") > add countries via "add condition," grouping by shared tax/regulatory treatment rather than rough geography (worked example: Italy + Germany grouped together; Switzerland deliberately excluded from that same market because it's non-EU with different tax rules). [8597c5d851d5]
3. **Currency per market requires Shopify Payments** (which itself requires a registered business to activate) — it is the only gateway the source states it knows of that supports true per-market currency display. Choose currency and rounding rule (e.g. round to nearest .95, recommended for a natural-looking price) or set fully independent per-market prices/compare-at prices. [8597c5d851d5][6474521ce75a]
4. Create a per-market **catalog** (Markets > [market] > Catalog > "create catalog") to exclude specific products from that market (worked example: excluding gift cards) and/or override prices per product per market — worked use case: absorbing extra import duties into a market's prices rather than surprising customers at checkout. [6474521ce75a]
5. Markets can be nested (worked example: France set as a sub-market of Europe) — view the hierarchy in "graph view." [8597c5d851d5]
6. **Per-market theme customization**: Markets > [market] > "Add theme customization" opens the theme editor scoped to just that market/country (e.g. swap the hero image for a France-only holiday banner) without touching the default store or other markets; a small diamond marker flags any market-level override, and the market's dashboard logs a note whenever one is made, for auditing. Presenter believes this may require a plan above the base tier — unconfirmed. `[web check]` [01109f418218]
7. Each market can carry its own language (see 3.24) and its own tax/duty configuration (see 3.25). [8597c5d851d5]

### 3.24 Languages
1. Install the free **Shopify Translate and Adapt** app. [018a6b7b5f0e]
2. Settings > Languages > Add language > select the language (worked example: Arabic) > optionally assign a dedicated subdomain. [018a6b7b5f0e]
3. Run "Auto translate" — it machine-translates the whole store (product info, pages, templates) in one pass; described as a good baseline needing human review, not a final result. Review side-by-side (original vs. translated) and re-run auto-translate for anything missed. [018a6b7b5f0e]
4. Images with embedded text can have a separate per-language version uploaded rather than needing multilingual text baked into one image. [018a6b7b5f0e]
5. Assign the finished language to the relevant market (Markets > [market] > Language). [018a6b7b5f0e]
6. Free tier supports **up to 2 languages**; more requires a paid upgrade. `[web check: current pricing/limits.]` [018a6b7b5f0e]
7. Shopify auto-detects a visitor's browser language and serves the matching configured language by default; a manual switcher is still available in header/footer. [018a6b7b5f0e]

### 3.25 Currency and payment gateways
1. With **Shopify Payments** active: Shopify auto-detects visitor location and shows both correct local language and local currency seamlessly, including at checkout. [36508e46b0c9]
2. Without Shopify Payments available in your country: a third-party currency app can still show converted prices on product/collection/cart pages, but **checkout will always revert to your store's base currency** — no app can change price at the checkout step itself. Given this gap, set your base currency to something widely understood internationally (source recommends USD or EUR) rather than a less-recognized local currency (its own example: avoiding AED as a base for this reason). [36508e46b0c9]
3. Settings > Payments: if Shopify Payments is available in your country, use it as primary (cheapest, bundles card processing + Apple Pay per the source) — activation requires a registered business and its registration paperwork. Add **PayPal** alongside it regardless, given how widely recognized it is. If Shopify Payments isn't available, use **Stripe** as the next-best option (cards + Apple Pay). [6303d6cb8521]
4. Research and add well-known **regional** payment methods for your important markets even if unavailable in your home country — named examples: Klarna for the UK (the transcript audio said "Clara," almost certainly a mistranscription of Klarna — verify), Tabby for UAE/KSA, and Cash on Delivery specifically called out as needed for Lebanon. `[web check: current regional gateway availability and names — these shift.]` [6303d6cb8521]

### 3.26 Taxes
1. Settings > Taxes and duties > configure per region (worked example: EU business info entered for a France registration). [e86ad9540ade]
2. The source's own stated preference: **never itemize B2C tax as a separate checkout line** — bake tax into the listed product price and remit it yourself, to avoid surprising the buyer at checkout — while acknowledging some jurisdictions (Europe specifically) require formal tax configuration/remittance regardless of how it's displayed. [e86ad9540ade]
3. If you do collect taxes, configure the differing rate per market/country here, and disclose it on the product page. [e86ad9540ade]
4. The source repeatedly recommends double-checking all tax setup with a real legal/tax advisor, since rules vary sharply by country. [e86ad9540ade]

### 3.27 Locations and shipping
1. Settings > Locations > Add location for each physical warehouse (worked example: "Paris warehouse," "USA warehouse," with address). [68a2525c5b79]
2. Assign per-location inventory on each product (Product > Inventory > "Edit location") or manage centrally via Products > Inventory, filterable by warehouse. [68a2525c5b79]
3. Settings > Shipping and delivery: a country with **no configured rate is unshippable** — Shopify will mark any product as unavailable to that destination at checkout. Every country you intend to sell into needs an explicit rate. [4b035d79d6ee]
4. For each shipping zone, set the fulfillment **location** it's served from, then use "Use flat rate" — the source strongly recommends flat rates specifically because they're easiest for shoppers to understand and estimate, reducing checkout abandonment, and recommends **always** pairing a flat rate with a free-shipping threshold. Worked examples: France (existing default) — free above €50, €8.80 flat 0–€50; Germany (built live, same Paris warehouse) — €10 flat for orders 0–100, free for 101+; United States (built live, separate "USA warehouse" location) — flat $20, no free tier in this specific demo. [4b035d79d6ee]
5. Add a delivery-time estimate to a rate's customer-facing label where possible, to reduce checkout uncertainty. [4b035d79d6ee]
6. Also available in this section: Pickup (in-store), Local delivery, and other delivery customizations — relevant especially to certain business types (groceries cited as an example). [4b035d79d6ee]

### 3.28 Pre-launch testing
1. Do **not** rely only on Shopify's simulated "test order" — place **real** orders through the actual payment gateway and actual warehouse fulfillment, especially for multi-warehouse stores, high-SKU catalogs, or bundles (a common confusion point for warehouses/integrations). [c7fe3611980d]
2. Checklist to verify before removing password protection: (1) warehouse integration genuinely working end-to-end — orders reaching the warehouse, tracking numbers flowing back; (2) payment gateway genuinely **live** (gateways can silently deactivate if business-verification info was left incomplete — this blocks all checkouts if missed); (3) shipping rates exist for every country you intend to sell to at launch; (4) tax settings match your actual intent (a common post-launch surprise is discovering Shopify was charging tax unintentionally); (5) for US/Canada-bound cross-border shipments specifically, add a clear, visible disclosure that customers may owe additional import duties/taxes on arrival, since Shopify cannot predict or itemize these — contrasted with e.g. EU-to-EU shipping where buyers typically pay no such extra fee. [c7fe3611980d]
3. Once verified, Settings > Preferences > remove password protection to go live. [c7fe3611980d][b8f482b2f3d9]

### 3.29 Order settings, notifications, fulfillment
1. Settings > General > Orders `[verify UI]`: use the order-ID prefix/suffix to obscure your true order count from customers; keep "require confirmation step" **ON** (customers see an order summary before completing checkout); leave "automatically fulfill orders" at its default/OFF for physical products (gift cards are the stated exception, since Shopify emails them instantly with no real fulfillment step); decide auto-archive-on-fulfillment purely based on your own workflow. [04689a1d2d66][d57d8a18c963]
2. Settings > Notifications: these are Shopify's fixed, pre-templated transactional emails — timing and send mechanics cannot be changed, which the source treats as a benefit (lowers error risk). The two flagged as most important: **Order confirmation** (fires immediately; only reaches the customer by SMS if a phone number was given, which is exactly why the source recommends making email required at checkout) and **Shipping confirmation** (fires automatically the moment a tracking number is attached to the order, whether added manually or via a warehouse integration). Edit sparingly (light text/color changes only) and always send a test after any edit; deeper changes require working in the underlying HTML. [1259e2e7f080]
3. With a warehouse integration: the warehouse's own Shopify app typically auto-pushes new orders to it and pushes the tracking number back once fulfilled, which is what triggers Shopify's shipping-confirmation email; order/customer notifications remain entirely Shopify-controlled throughout. Without an app, the warehouse needs direct store permissions to build its own integration. Manual fulfillment: print the label, prepare/ship, then add the tracking number to the Shopify order yourself. [98bfe80fc295]

### 3.30 Customer support
1. Have a working contact email/form live on launch — expect emails immediately once the store goes live, and treat slow/poor replies as directly reputation-damaging from day one. [62f0dece472c]
2. For an early-stage brand, keep support **in-house** (yourself, family, or an employee) rather than outsourcing, explicitly to retain full control at the start (source's own stated preference for that stage only). [62f0dece472c]
3. Expect most tickets to be shipping/delivery/order-status related, not product questions, **if** the product pages are thorough — a spike in product questions is a signal to fix the PDP, not to keep answering the same question. A detailed shipping policy reduces (not eliminates) ticket volume. [62f0dece472c][e2fd26e10b5]
4. Orders can be edited directly in Shopify admin (e.g. correcting a customer's email or address) — described as "not difficult at all." [62f0dece472c]
5. For real-time contact, a free live-chat app exists (likely Shopify Inbox, referenced again here); for larger catalogs needing first-line automated triage before human escalation, consider an AI chat tool (see 3.3.7 naming caveat). [62f0dece472c]

### 3.31 Analytics
1. Analytics has two views: **Reports** (a browsable, filterable library by category — Acquisition, Behavior, Customers, Sales, Finance — plus any custom reports you or teammates saved) and **Live view** (real-time activity, useful specifically during a launch). [ef0c00c5061f][a6c3105bd9d3]
2. Set the **time window** deliberately before drawing conclusions — presets include Today, Yesterday, Last 30 minutes, Last 7 days, Last 12 months, week/month/quarter/year-to-date, and a dedicated Black Friday/Cyber Monday view. A single day's number (e.g. seeing "6% conversion" today) is not a representative average — use a multi-month window for real judgment. [63acdbeb3fff]
3. Optionally set a **comparison window** (e.g. this year vs. last year) to see whether a change actually moved the business — the source notes it personally finds this sometimes confusing and turns it off, treating that as a matter of preference. [63acdbeb3fff]
4. Change the display **currency** if you sell in a currency other than the one you personally think in (a relatively new capability). [63acdbeb3fff]
5. "New exploration" opens an **AI query tool**: type a plain-language question (worked example: "show my conversion rate improvement in the last two years") and it writes the query and returns the report; described as basic in the demo but capable of more with a more detailed ask. [2232708393e1]
6. Key metrics walked through, in order: total sales, returning-customer rate, orders fulfilled, total orders (summary tiles); total sales over time; **total sales breakdown** (explicitly worth learning — gross vs. net sales vs. discounts, per Shopify's own definitions); total sales by sales channel; **average order value over time** (called "a very important metric"); total sales per product (the real way to find actual bestsellers, vs. gut assumption); sessions, conversion rate, and a **conversion-rate funnel breakdown** (add-to-cart rate → reach-checkout rate → completed-purchase rate). Worked example figures for the source's own demo store, explicitly presented as an example for that store/niche, not a benchmark: ~10% add-to-cart, ~5.32% reach-checkout, ~2.63% completed-purchase, called "acceptable for our niche." Diagnostic rule: a large drop specifically between add-to-cart and completed-checkout points to a **shipping cost/rate problem**, not a product-page problem; a low add-to-cart rate instead points upstream, to traffic quality or PDP persuasion. [a6c3105bd9d3][873a72ed8762]
7. **Customer cohort/retention report** — called one of the most important reports on the platform: shows month-by-month what share of a cohort returns to buy again (month 1, 2, 3, 6...). Use it to (a) estimate long-term customer value and (b) time win-back emails (worked logic: if customers typically return by month 4, trigger a win-back email with an incentive to anyone who hasn't by then). Explicitly **not meaningful for a brand-new store** — needs roughly a year of real order history. [d90fa94f0b55]
8. The dashboard is fully drag-and-drop customizable — rearrange, add, or remove metric tiles to match your own priorities rather than keeping Shopify's stock layout; understand the default metrics first before rearranging. [ef0c00c5061f]

## 4. Rules, thresholds and numbers

| Rule / setting | Number or threshold | Condition | Source's basis | Card id |
|---|---|---|---|---|
| Basic plan card/transaction rate | 1.5% | Basic plan, store payments | Presenter's stated figure at recording | 8c79cd592233 |
| Grow plan card/transaction rate | 1.3% | Grow plan | Presenter's stated figure at recording | 8c79cd592233 |
| Advanced plan card/transaction rate | 1.1% | Advanced plan | Presenter's stated figure at recording | 8c79cd592233 |
| Basic plan staff seats | ~1–2 | Basic plan | Presenter's stated figure at recording | 8c79cd592233 |
| Grow plan staff seats | up to 5 | Grow plan | Presenter's stated figure at recording | 8c79cd592233 |
| Advanced plan staff seats | up to 15 | Advanced plan | Presenter's stated figure at recording | 8c79cd592269 |
| Shopify Plus price | ~$2,000–$2,300/month | Only plan allowing full checkout customization | Presenter's stated figure | 8c79cd592233 |
| Brand color palette size | 4–5 hex colors, light + dark | Pre-build asset checklist | Presenter's working habit | 285d3b5212e7 |
| Theme price (paid) | ~$100–$400 one-time | Choosing a theme; presenter prefers paid over free | Presenter's opinion, not universal | 36f8551b5974 |
| Announcement bar message count | ~3 (theme-typical limit) | Header setup | Observed in the demo theme | 53605e79474b |
| Menu nesting depth | up to 3 levels | Building mega menus | Observed in the demo theme | 1eaac2268d09 |
| Mobile products per row (product card) | 2 (recommended) | Product-card/collection-grid mobile display | Presenter's preference | 88cfe2d43556 |
| Hero slideshow fixed height (example) | ~600px, desktop and mobile | Homepage hero, "fixed height" mode | Presenter's own worked example, not a benchmark | 72785e7b693e |
| Complimentary product count | 1–2 items | Product-page cross-sell | Presenter's explicit "don't bombard" rule | 10f587c95a2d |
| Judge.me paid plan price | ~$15/month, 15-day trial | Review app, "Awesome" tier | As shown at recording | 13d14684d9ef |
| Translate & Adapt free tier | up to 2 languages | Multi-language setup | Stated app limit at recording | 018a6b7b5f0e |
| Per-order quantity cap (worked example) | 10 units | Checkout advanced preferences | Presenter's own example, not a rule | f6e33255728a |
| Example flat shipping rate, France | free above €50; €8.80 for €0–50 | Default seen in demo store | Presenter's own store's existing setup | 4b035d79d6ee |
| Example flat shipping rate, Germany (built live) | €10 for €0–100; free for €101+ | Worked example | Presenter's own demo, not a universal rate | 4b035d79d6ee |
| Example flat shipping rate, USA (built live) | $20 flat, no free tier | Worked example | Presenter's own demo, not a universal rate | 4b035d79d6ee |
| Review-request email delay (Judge.me default, cited) | 14 days domestic / 5 days other | Post-purchase review request timing | App default as shown; verify current default | fd106fda6cf6 |
| Discount app "gap" limitation | no native max-savings cap on % discounts | Percentage-off discounts, high-AOV stores | Stated platform limitation | 447fe9aa14c2 |
| Analytics funnel example (own demo store) | ~10% add-to-cart, ~5.32% reach-checkout, ~2.63% completed purchase | Presenter's own store/niche, explicitly not a benchmark | Presenter's own dashboard reading | a6c3105bd9d3 |
| Cohort/retention data usefulness threshold | ~1 year of order history | Reading the customer cohort report | Presenter's stated rule of thumb | d90fa94f0b55 |
| Gift card example denominations | $10 / $25 / $50 / $100 | Gift card product setup | Presenter's own worked example | 74d169e9b59c |

All prices, percentages, and plan/feature names in this table carry `[web check]` — the source itself flags several of them ("Shopify Winter Edition," "fairly new," "still rolling out") as tied to a specific, recent Shopify release.

## 5. Diagnostics and checks

- **Weak product pages vs. weak logistics communication**: classify incoming support tickets in the first weeks after launch. A high share of *product* questions signals a thin PDP — fix the page content, don't keep re-answering. A high share of *shipping/delivery* questions signals a thin shipping policy — expand it (it reduces, not eliminates, ticket volume). Don't try to patch either problem by editing the fixed order-confirmation/shipping-confirmation notification emails. [e2fd26e10b51]
- **Conversion funnel drop-off location**: read the funnel (sessions → add-to-cart → reach-checkout → completed purchase). A large drop specifically between add-to-cart and completed-checkout points to a shipping-cost/rate problem at checkout, not a PDP problem. A low add-to-cart rate itself points upstream — traffic quality or PDP persuasion, not checkout. [a6c3105bd9d3]
- **Filter showing only one value**: usually means the underlying field isn't filled on other products — check and bulk-edit rather than assuming the app is broken. [b9eb3390c92d]
- **Metafield not appearing as a "connect dynamic source" option**: the metafield's defined type doesn't match what that theme field expects — redefine the type (e.g. Link vs. URL, single-line vs. rich text) rather than assuming the feature doesn't work. [79db08591c6b]
- **Store checking as "not shippable" to a country**: no shipping rate has been configured for that country/zone — add one; this is not a bug. [4b035d79d6ee]
- **Payment gateway silently failing checkouts**: check whether required business-verification information is incomplete; a gateway can deactivate post-setup without an obvious warning. Verify with a real test order, not just Shopify's simulated one. [c7fe3611980d]
- **Post-launch tax surprise**: if Shopify is charging tax at checkout unexpectedly, check Settings > Taxes and duties against your actual intent — this is called out as a common mistake. [c7fe3611980d]
- **Speed regression after a change**: re-check Shopify's built-in speed metrics right after installing an app or updating the theme to attribute any drop to that specific change. [cb7f3ba4e5c9]
- **Cohort/retention numbers that look noisy or meaningless**: check whether the store has enough order history yet (roughly a year, per the source) before trusting the pattern. [d90fa94f0b55]

## 6. Tools, settings and named features

- **Shopify Translate and Adapt** — free native app for adding/auto-translating additional store languages; free tier caps at 2 languages. `[web check]` [018a6b7b5f0e]
- **Search and Discovery** — free native app covering storefront filters, on-site search, and product recommendations; source recommends uninstalling older paid apps that did the same jobs. [236052ce217f][d21ee63adb13]
- **Sidekick** — Shopify's built-in AI assistant, usable inside the theme editor (quick data questions, "ask for changes" section edits) and inside Analytics (natural-language report queries). Its in-editor edits change theme *settings*, not code, so a change can unexpectedly propagate to other sections sharing the same setting. `[verify UI/behavior — actively evolving.]` [e5222e8988f5][e431785d2758][2232708393e1]
- **Shopify's built-in product-image editor** — crop, rotate, flip, resize, background removal + solid-color replace, and an AI text-prompt background generator (described as unreliable at recording time; source prefers Canva for that specific task). [8e20230d8bd8]
- **Shopify's AI section generator** — unlocked after buying a theme; generates custom sections (e.g. a comparison table) from a text prompt inside the theme editor; output quality is prompt-dependent and can carry bugs; not recommended as a first-choice method for beginners. [82e21838aca5]
- **Judge.me** — source's currently recommended reviews app (free + ~$15/month "Awesome" tier `[web check]`); automated email review requests, drag-and-drop custom email templates, product-review grouping, moderation controls. [13d14684d9ef][00e6bb4974e0][fd106fda6cf6][07c9c7d8dbc9]
- **Stamped.io** — alternative reviews app the source names specifically for stores also wanting loyalty-program features. `[web check]` [13d14684d9ef]
- **Gorgias** and **Tidio** — named (via the card data, correcting an ambiguous transcript) as example AI-assisted customer-support tools for larger/education-heavy catalogs. `[web check]` [275ea2cf320b][62f0dece472c]
- **Shopify's native free bundling app** — combines products, manages combined inventory automatically; limited for advanced bundle logic. [a517b976f014]
- **Shopify's native free subscription app** — fits consumables (supplements, food, coffee, makeup); poor fit for one-time-purchase categories like electronics. [a517b976f014]
- **Shopify Payments** — required for true per-market currency display and for the "Buy it now" dynamic wallet button; requires a registered business; availability varies by country (unavailable in some Middle East markets per the source). [8597c5d851d5][36508e46b0c9][fd255645fcbc]
- **Stripe** — recommended next-best gateway when Shopify Payments isn't available. [6303d6cb8521]
- **PayPal** — recommended as an add-on gateway alongside Shopify Payments regardless of region. [6303d6cb8521]
- **Klarna** (UK) and **Tabby** (UAE/KSA) — named regional payment methods worth adding for those markets specifically; transcript audio rendered "Klarna" as "Clara," treat with care. `[web check]` [6303d6cb8521]
- **Collaborator access** — a Shopify mechanism for giving developers/apps store access via a collaboration code + your myshopify.com domain, without consuming a paid staff seat. [b03f3e640118]
- **Custom data (metafields and metaobjects)** — Settings area used repeatedly for building custom filters, per-collection/per-product dynamic content, and category-driven attributes. [3ce1b240ca4f][79db08591c6b][1b74e6a6d37e]

## 7. Examples and case results

- **Client example — premium pasta brand** (only named real client case in the source): priced roughly 3x standard supermarket pasta; the #1 identified objection was taste, addressed with customer reviews and visible people tasting/endorsing the product; the price-justification objection was addressed with numerical/scientific facts on the page proving the health/quality claim. Presented as an illustration of the *method* (mine reviews for objections, answer them on the page), not a measured conversion result. [d4eba16b7f05][14e4f605117f]
- **Demo store — activewear brand** (the source's own build, used throughout): products included leggings, bras, overalls/jumpsuits, a yoga mat, and a water bottle. Worked numbers: yoga mat priced 45/45/45 across 3 colors, 100 units each; legging weight entered as 0.25; a €60 price with €20 cost of goods and a €100 compare-at price shown as one PDP example. [4cb4b173c437][c7f6802299ac][530b3d95d941]
- **Domain-buying example**: searching for the brand's exact name plus ".com" was unavailable; a longer alternative with a double letter was available but the presenter explicitly said "I wouldn't recommend using it" even while buying it for the demo — an example of a bad-fit domain accepted only for demonstration purposes, not a recommendation to copy. [b30915400ab6]
- **Collection typo caught live**: a product intended to be tagged "bras" was mistakenly tagged "browse," which silently excluded it from the Bras smart collection until the presenter noticed and corrected it via bulk edit — a direct demonstration of the "exact tag spelling" risk. [12b8ef266d4c]
- **Shopify Markets worked example**: created a "Europe" market containing Italy and Germany, deliberately excluding Switzerland (non-EU, different tax rules); nested France as a sub-market of Europe; built a separate "United States" market; demonstrated a France-only hero-image swap via per-market theme customization, marked by a small diamond indicator. [8597c5d851d5][01109f418218]
- **Analytics funnel reading (own store)**: ~10% add-to-cart rate, ~5.32% reach-checkout rate, ~2.63% completed-purchase rate — the presenter's own dashboard, called "acceptable for our niche," explicitly not offered as an industry benchmark. [a6c3105bd9d3]

## 8. Mistakes the source warns about

- Signing up to Shopify using a contractor's or agency's email instead of your own, risking loss of true store ownership/control. [63c65895f090]
- Creating a collection as manual when it should be smart (or vice versa) — this cannot be undone later, only worked around by creating a new collection. [f46060533ad6]
- Inconsistent tag spelling/casing across products, which silently breaks smart collections and filters (demonstrated live: "bras" vs. "browse"; "legging" vs. "leggings" fragmenting a filter into two options). [12b8ef266d4c][b9eb3390c92d]
- Uploading product photos in inconsistent ratios/dimensions, forcing awkward automatic cropping on product cards later. [c673b25c3ccd][88cfe2d43556]
- Leaving the "physical product" weight toggle off on a physical item, which makes Shopify treat it as digital and skip shipping at checkout entirely. [530b3d95d941][e08f40db23df]
- Editing a product's title/URL later without going back to fix the URL handle, leaving a mismatched slug. [c673b25c3ccd]
- Installing an app but forgetting to enable its App Embed in the theme editor — the app's storefront elements silently never appear. [3f5560597133]
- Choosing a theme without first confirming it has a niche-critical section (e.g. a before/after slider for skincare) — a hard constraint discovered too late if skipped during shopping. [e5fb740fbeed]
- Assuming Shopify's simulated "test order" is sufficient pre-launch verification instead of placing real orders through real payment and fulfillment. [c7fe3611980d]
- Letting a payment gateway silently deactivate post-setup due to incomplete business verification, discovered only when customers can't check out. [c7fe3611980d]
- Charging tax at checkout unintentionally because tax settings weren't checked against actual intent before launch. [c7fe3611980d]
- Not disclosing to US/Canada-bound customers that additional import duties may apply on arrival. [c7fe3611980d]
- Forcing account creation before checkout, which the source says many customers actively dislike. [47c8ccf3f338]
- Enabling both Shopify's native abandoned-checkout email and a separate ESP's abandoned-cart flow at the same time, risking duplicate messages to the same customer. [67507a55b77]
- Treating order-confirmation/shipping-confirmation notification emails as something to patch when the real problem is a thin product page or shipping policy. [e2fd26e10b51]
- Over-editing Shopify's core transactional email templates without being confident in what you're changing, risking a broken order-confirmation email. [1259e2e7f080]
- Reading a single day's conversion rate as if it were a representative average. [63acdbeb3fff]
- Trusting the customer cohort/retention report before the store has enough real order history (roughly a year) to be meaningful. [d90fa94f0b55]
- Overwhelming a product page's cross-sell slot with too many "complimentary product" recommendations instead of 1–2 genuinely relevant ones. [10f587c95a2d]

## 9. Caveats, conflicts and what is missing

- **Internal inconsistency on the free-trial offer**: within the same passage, the source states both "Shopify offers a free trial of 7 or 14 days" and, separately, "3 days trial then $1/month for the first 3 months" as though describing the same signup flow. These do not obviously reconcile from the transcript alone. `[web check: current Shopify trial structure.]`
- **Navigation example attribution conflict**: the transcript audio names "Decathlon" (twice, clearly) as the reference retailer for multi-angle navigation (shop by sport, shop by gender); the card-level summary of the same passage instead names "Lululemon." One of these is very likely a transcription or summarization error, but this file cannot determine which without re-checking the source video directly — treat the specific retailer name as unconfirmed, while the underlying navigation *pattern* it illustrates (letting the same catalog be browsed by multiple mental models) is not in doubt.
- **Ambiguous tool names from audio transcription**: "Cupcat" (background-remover, likely a mis-hearing of a known tool), "Juy"/"TDO" and later "Juie AI" (AI chat/support tools, which the card data resolves to Gorgias and Tidio), "Clara" (payment gateway, almost certainly Klarna). These are flagged in-line above; do not treat the phonetic transcript spellings as real product names.
- **Presenter opinions stated as if settled, worth separating from platform fact**: preference for paid themes over free ones; preference for cart drawer over cart page; the claim that a locked, uniform Shopify checkout is *better* for buyer trust than a customizable one; the recommendation to fold B2C tax into product price rather than itemizing it at checkout (which may not be legally available or advisable in every jurisdiction, notably parts of the EU); pre-selecting marketing consent for new businesses. None of these are backed by measured data in the source — they are the presenter's professional judgment, sometimes explicitly flagged as such, sometimes not.
- **Feature-availability claims the presenter itself is unsure of**: whether per-market theme customization requires a plan above Basic; whether the current Shopify base/Basic plan even shows the Markets item in the sidebar for every store. Both are called out in-source as uncertain and worth verifying live.
- **Fast-moving, dated claims**: the ChatGPT/AI product-listing integration ("still rolling out... not available for everyone... USA"), the "Shopify Winter Edition" changes to the AI image tool and checkout flexibility, and the framing that "Shopify Markets is fairly new" all place this source at a specific point in Shopify's release cycle. Given the pace of platform change this file's own project context notes (Shopify admin changes often), essentially every concrete UI path, price, plan feature, and app default in this file should be treated as a hypothesis to re-verify live, not a settled fact — tagged throughout as `[verify UI]` and `[web check]`.
- **What the source does not cover**: it does not give any A/B-tested or measured before/after conversion result for any of its recommendations (theme choice, cart drawer vs. page, description length, size-chart presence, etc.) — every design/merchandising claim is presenter judgment or a single anecdote (the pasta client), not a benchmark. It also does not cover: setting up a formal experiment/testing program for the storefront itself (that lives in the `09-CRO-testing` domain, not here); email marketing build-out beyond mentioning Klaviyo/Omnisend by name (the presenter refers viewers to a separate, uncaptured course); paid acquisition/ad setup; and any brand-specific voice, product, or pricing decisions, which this file cannot supply and which belong in each brand's own record. `[needs brand data: actual product catalog, pricing, brand colors/fonts, policies text, warehouse locations, and target countries — none of this can be filled from the source and must come from the brand being set up.]`

## 10. Card index

285d3b5212e7 - Pre-launch asset preparation checklist
8c79cd592233 - Choosing a Shopify plan by card rate and staff seats
e6e96ea93d37 - Store details, currency, and order numbering configuration
63c65895f090 - Registering Shopify with your own owner email
b03f3e640118 - Using role-based staff permissions instead of blanket access
b30915400ab6 - Connecting a custom domain and handling DNS records
fe40994519f8 - Setting up store policies and return rules
275ea2cf320b - Choosing customer support tooling by catalog complexity
c673b25c3ccd - Adding a product: title, description and image ratios
59de72e661ee - Configuring product type, vendor, tags and category
c7f6802299ac - Pricing fields: compare-at and cost of goods
23e7b8e73e4c - Independent inventory, SKUs and warehouse coordination
530b3d95d941 - Product weight, shipping profile and variants
1513317a812c - Defining brand assets in Shopify settings
54788a0aefff - Orienting yourself in the Shopify admin navigation
e08f40db23df - Create Physical Products with Weight to Enable Shipping
0df57c8635cd - Set Up Product Variants for Size and Color
f46060533ad6 - Build Manual vs Smart Collections
12b8ef266d4c - Tag Products Consistently for Smart Collections
f119acb5c204 - Use Bulk Edit for Prices, Quantities, and Tags
8e20230d8bd8 - Edit Product Images In-Shopify: Crop, Resize, Remove Background
5254ed89ca51 - Generate Product Images with Sidekick AI
4cb4b173c437 - Configure Variant Color Swatches with Hex or Pattern Images
236052ce217f - Set Up Storefront Filters with the Search and Discovery App
3ce1b240ca4f - Create Custom Product Filters When Category Meta Fields Fall Short
528c1525c249 - Choose Filters from Customer Search Language
36f8551b5974 - Filter Shopify Themes by Industry, Catalog Size, and Required Features
35eac0a86ba9 - Preview Mobile and Desktop Before Buying a Theme
e0fbc88d7b20 - Trial a Theme Before Buying to Preserve Work
851254972d2b - Duplicate Your Theme as a Backup Before Big Changes
b8f482b2f3d9 - Set Up a Password-Protected Coming Soon Page
d936f750ed9d - Reject One-Click AI Whole-Store Theming; Design for Conversion
0875899454b9 - Plan Theme Around Site Structure and Future Catalog
a5598af5de1a - Lock the store with password during setup and use it for early access
540e68dc8bce - Edit products, collections and pages inside the theme editor
e5222e8988f5 - Navigate the theme editor: locations, pages, inspector and view modes
81776b16a7c1 - Get a shareable preview link for draft and published themes
8de64df0eaa7 - Set brand colors once and connect theme colors to them via dynamic sources
868b9d497999 - Configure buttons, background, header and section color schemes
65f4ccd810fb - Set typography, sizes and button shapes from theme settings
88cfe2d43556 - Customize product cards: image shape, cropping, alignment and mobile per-row count
53605e79474b - Set up header: announcement bar, sticky header and menus
1eaac2268d09 - Build multi-level and mega menus that mirror how shoppers think
ed834e77dbd7 - Configure cart behavior: drawer vs page and free shipping bar
cfa8eb8e67cf - Use currency formats, advanced settings and custom CSS carefully
5a6b353794866 - Use theme style presets as a starting point
5b24de26c78a - Build the footer with link lists, blocks and policies
7ac89fa59ccf - Build footer policy and support menus before linking them in the theme
e5fb740fbeed - Choose theme sections by first checking the available section library
c92800a72acd - Assemble the homepage in a deliberate section order
72785e7b693e - Set hero slideshow height and focal point to prevent bad crops
333ea959bee7 - Use duplicate and copy-paste to build section sets quickly and consistently
8a469102152c - Create a bestsellers collection with tags and feature it
646e5b63a24f - Build automated collections with AND-style tag conditions
b9eb3390c92d - Configure collection filters using Shopify Search & Discovery
dfd27ace3b6b - Turn on colour swatches with defined colours or variant images
7516ecaaead1 - Work on the default collection template first, then branch to custom templates
19d381b1ed94 - Add a visual subcollection row with a multicolumn section
79db08591c6b - Use collection metafields to vary content inside a shared collection template
d4eba16b7f05 - Research competitor PDPs and reviews before designing your product page
e431785d2758 - Use Sidekick to make editor changes — with eyes open about scope
14e4f605117f - Mine competitor PDPs and reviews for objections
d1dc0a44255a - Answer objections in proportion to price and complexity
92d28259c9cb - Repeat key information in multiple formats on the PDP
1b74e6a6d37e - Decide product page templates by category vs. meta fields for per-product content
2efef89fb3bf - Configure Shopify product page section settings
08b36113927c - Group variant images by color using theme logic
458ba19e94c4 - Place short benefit bullets and description above the buy button
99e2ef1ab894 - Deliver sizing confidence with a size chart page or meta field
922844ff8bf9 - Use collapsible tabs for FAQ-type PDP content
6eff9d71aa70 - Show fit/true-to-size rating when the theme supports it
fd255645fcbc - Choose between Add to cart and Buy it now
10f587c95a2d - Set complimentary products to lift average order value
a9c942e14d9d - Add brand-trust and feature sections below the buy area
82e21838aca5 - Generate missing PDP sections with Shopify's AI section tool
b69485cbf3ff - Design the collections list ('all collections') page
bb2d96464355 - Keep the cart page and cart drawer simple
fe0d110afd3a - Build richer static pages with templates instead of plain text
84395806f962 - Organize content into multiple blog families
a99b97dacf98 - Customize search, password and error pages
6f0629590ba6 - Expect limited checkout customization outside Shopify Plus
b7733d8e8e98 - Locked Shopify Checkout: What You Can Adjust Without Plus
47c8ccf3f338 - Configure Contact Method and Required Fields at Checkout
ed38e3fd032c - Separate Transactional Consent From Marketing Consent at Checkout
67507a55b77b - Turn On Abandoned Checkout Recovery Emails
f6e33255728a - Limit Quantity Per Order to Protect Inventory
abc432db1669 - Configure the Customer Account Page and Its Domain
bd76d7f8a46b - Choose Discount Code vs Automatic Discount
fc3d5032c0d2 - Share a Pre-Applied Discount Link Instead of a Code
447fe9aa14c2 - Know Shopify's Gap Limit and When to Add a Discount App
74d169e9b59c - Set Up a Gift Card Product for Last-Minute Buyers
3f5560597133 - Choosing and Vetting Shopify Apps Before Committing
13d14684d9ef - Install a Review App and Collect Reviews by Email
a517b976f014 - Add Bundling and Subscription Apps Only Where the Niche Supports Them
d21ee63adb13 - Use Shopify Search & Discovery for Filters and Recommendations
cb7f3ba4e5c9 - Reduce Apps and Image Weight to Protect Store Speed
e076d09149bf - Cover the Evergreen SEO Basics on Products, Collections and Store Settings
77c72b3e8b08 - Match Checkout Branding to Your Store's Design System
d96aa7966303 - Decide on Tipping, B2B Fields and Address Defaults at Checkout
00e6bb4974e0 - Install and Configure the Judge.me Review Widget on Product Pages
fd106fda6cf6 - Set Up Automated Review Request Emails (Delays, Templates, Branding)
07c9c7d8dbc9 - Enable Judge.me Features: Import Reviews, Product Groups, Widget Branding
8597c5d851d5 - Create Shopify Markets for Multi-Country Selling
6474521ce75a - Adjust Prices and Catalog per Market
01109f418218 - Apply Market-Specific Theme Customizations
e86ad9540ade - Configure Taxes and Duties per Market
68a2525c5b79 - Add and Manage Warehouse Locations
4b035d79d6ee - Set Up Shipping Zones and Flat Rates per Country
018a6b7b5f0e - Add a Second Store Language with Translate & Adapt
36508e46b0c9 - Handle Currency Display When Shopify Payments Isn't Available
6303d6cb8521 - Choose and Set Up Payment Gateways by Market
98bfe80fc295 - Manage Orders and Fulfillment Notifications
c7fe3611980d - Run Real Test Orders Across All Locations Before Launch
04689a1d2d66 - Set Order ID Format and Order Processing Preferences
d57d8a18c963 - Order ID and order-processing settings to configure at launch
1259e2e7f080 - Configure Shopify customer notifications without breaking checkout emails
62f0dece472c - Set up customer support before launch, not after
a6c3105bd9d3 - Read conversion-rate funnel breakdowns to find where buyers drop
63acdbeb3fff - Choose the analytics time window and comparison before drawing conclusions
ef0c00c5061f - Customize the Shopify analytics dashboard around your own metrics
d90fa94f0b55 - Use the customer cohort/retention report to time win-back emails
2232708393e1 - Ask Shopify's AI agent for custom analytics reports
873a72ed8762 - Read the sales breakdown and by-channel metrics correctly
e2fd26e10b51 - Don't rely on default Shopify emails to fix weak product pages
