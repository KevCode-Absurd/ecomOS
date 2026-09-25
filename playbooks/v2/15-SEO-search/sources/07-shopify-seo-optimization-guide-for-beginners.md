# Shopify SEO Optimization Guide for Beginners 2026

source_id: 1VxQ6RxvsNZTOPGWxQAiPrhBVh9vjxQy1  |  folder: 15-SEO-search  |  cards: 17  |  words: 10,359  |  type: transcript (YouTube video, screen-recorded walkthrough)

credibility: Presenter identifies himself as "Christian," says he has "helped hundreds of Shopify store owners grow their businesses over the past 10 years." No client names, no before/after data, no case studies with numbers are given for his own results — this is a stated track record, not documented evidence. The whole video is a live screen-recorded demo on his own "demo store" (soap and shampoo store), so the steps are shown, not just described. The video ends with an extended promotional segment for a specific app ("SEO Ant" / "AI SEO"), including a 35% discount code ("shopo") for the first 3 months — this is an affiliate/sponsored placement and is flagged throughout. Treat the how-to steps as a practitioner's standard workflow; treat the app recommendation as promotional content requiring independent evaluation.

date signals: Title says "2026." Tools named as current at time of recording: Google Keyword Planner (inside Google Ads), Google Trends, the "Glimpse" Chrome extension, Ahrefs, Semrush, Shopify's Dawn theme, Shopify Sidekick (AI assistant used to locate the brand settings tab), Google PageSpeed Insights, Google Search Console, and the SEO Ant / "AI SEO" Shopify app. Shopify admin UI paths given (Online Store > Preferences, Search engine listing fields, Content > Files, Settings > Domains) are current as of recording but Shopify changes its admin UI often — every UI path below is tagged `[verify UI]`.

## 1. What this source is for

Gives a beginner, end-to-end walkthrough of on-page and technical Shopify SEO: finding keywords, writing them into the homepage/product/collection/page/blog SEO fields, fixing image and heading issues, checking mobile and speed, adding rich snippets, and submitting a sitemap. It is a single operator's demonstrated sequence for taking one already-live Shopify store from no SEO effort to a reasonably optimized state, ending with a pitch to automate the same tasks with a paid app.

## 2. Principles

1. **SEO is about matching your pages to what customers actually type into Google.** Google ranks pages by authority (trust signals like backlinks) and relevancy (on-page content matching the query); optimizing your pages/content raises relevancy. Evidence: presenter's stated framing, no external citation. [2fc78c801ced]
2. **Every page needs its own keyword set, not one set reused everywhere.** Homepage, each product, each collection, and each blog post should target a distinct main keyword + 2 supporting keywords based on that page's actual content. Evidence: demonstrated on the presenter's demo store across homepage, one product, and one collection. [2fc78c801ced][1f41cebc6554][7b577e884e60]
3. **Search intent should route the keyword to the right page type.** Informational queries ("how to make homemade soap") belong on blog/guide content; transactional queries ("homemade soap for sale," "homemade soap near me") belong on product/collection pages where the visitor can buy immediately. Evidence: presenter's classification of two example keywords by intent shift ("homemade soap" -> "homemade soap near me" flips from informational to transactional per Semrush's intent label). [6c1d36ed15c3]
4. **One H1 per page, no exceptions.** Multiple H1 tags on one page "confuse Google" about the page's real topic and hurt ranking. Evidence: presenter's stated rule, demonstrated by inspecting element source on homepage/collection/product pages. [30ee2355cc6d]
5. **AI-drafted title/description text must be edited to match brand voice before publishing**, not used verbatim. Evidence: presenter edits ChatGPT output each time before pasting it into Shopify. [1f41cebc6554][7b577e884e60]
6. **Meta descriptions optimize for clicks, not keyword density**; the title tag is where keywords matter most. Evidence: presenter's explicit statement when writing the product meta description. [e9c397c88109]
7. **Broken/changed URLs must redirect, or you lose bookmarked and linked traffic to 404s.** Evidence: presenter's stated rationale each time a handle is changed. [e7c0a899bee0][04a11dea33db]
8. **Collection descriptions are worth the SEO value even if merchants dislike how they look**, because the workaround (move it below the grid) preserves both crawlable content and product-first visual layout. Evidence: presenter's stated compromise, not a documented Google requirement. [04a11dea33db]
9. **Internal linking speeds up Google's discovery of new pages** — crawling one linked page leads Google to the next. Evidence: presenter's stated mechanism, no external citation. [1e1031d336d4]
10. **Never lazy-load the image that is the Largest Contentful Paint (LCP) element** (e.g., a hero/banner or the main product image above the fold); lazy-load everything else. Evidence: presenter's stated technical SEO rule, tied to Google's page-experience ranking factor. [cc5014d16cd8]
11. **Uncontrolled third-party apps can silently slow a store down** because their code runs on third-party servers outside the merchant's control; audit and remove unused apps. Evidence: presenter's stated caution, not measured in the video. [cc5014d16cd8]
12. **Backlinks transfer authority**: being linked from a high-authority site passes some of that trust to your store. Evidence: presenter's stated claim, no external citation or study referenced. [ec29d900d61f]
13. **Regular content publishing is rewarded by Google** ("at least two times a month if not four, like a post each week"). Evidence: presenter's opinion/recommendation, explicitly not tied to any documented Google ranking threshold (see card caveats). [1e1031d336d4][ec29d900d61f]
14. **App-generated SEO "scores" are prioritization guides, not ranking targets.** A page can rank fine without hitting 100 in a third-party app's score. Evidence: presenter's own demo raised one product page's app score from a low baseline to 91, then 94, without reaching 100, while treating that as a good outcome. [8a330a3d4691]

## 3. Procedures

### A. Keyword research (per page)
1. Open a Google Ads account (required even if you don't run ads) and go to Tools > Planning > Keyword Planner. `[verify UI]`
2. Set the target language and country to match your market.
3. Enter a seed term describing the product/category (example used: "homemade soap"). Read monthly search volume, competition level, and CPC range.
4. Pick 1 main keyword and 2 supporting keywords per page, favoring healthy volume for the main term and more specific/lower-volume terms as support.
5. Cross-check with Google Trends (optionally with the Glimpse Chrome extension for more depth) — scroll to "related queries" at the bottom, judge buying intent vs. informational intent, then re-check any promising term's volume back in Keyword Planner.
6. Type a candidate query into plain Google search and harvest autocomplete predictions as extra keyword candidates; validate each in Keyword Planner.
7. Optionally paste a competitor's URL into Keyword Planner's "start with website" option to see keywords that URL already ranks for; select gaps or ideas to target.
8. Assign a distinct keyword set to each page based on that page's actual content — do not reuse the homepage set on every product.
[card 2fc78c801ced]

### B. Homepage / global store SEO
1. In Shopify admin: Online Store > Preferences > Search engine listing. `[verify UI]`
2. Write the Title field with the main keyword included; respect the character limit shown in the field (presenter's example: 70-character limit, used 63 characters, fit main keyword "homemade soap" plus "body wash" and "healthier skin"). `[verify UI: field limit may change]`
3. Write the Description field with supporting keywords, optionally the main keyword again, and a description that reflects the store's actual offering.
4. Optionally draft both fields with ChatGPT first, then hand-edit for brand voice and to remove anything too broad or off-niche.
5. Save. Verify by searching the target keyword in Google to see how the live listing renders (may take time to update).
[card 1f41cebc6554]

### C. Product page SEO
1. Open the product in Shopify admin > Products.
2. Copy the product's existing specs/description into ChatGPT; ask for high-volume keyword candidates relevant to those specs.
3. Validate each candidate in Keyword Planner; discard weak-volume or low-relevance ones.
4. Feed the validated list back to ChatGPT, ask for title options, and pick one containing at least the main keyword plus a supporting keyword. Paste into the product Title field (this is also the on-page H1). Save.
5. If the new (usually longer) title breaks the theme's title layout, go to the theme customizer and reduce the title font size. `[verify UI]`
6. Ask ChatGPT to write a product description from the specs, instructing it to weave in the researched keywords while sounding natural/human, not obviously AI-written. Target at least 100 words; 300–400 words is called ideal.
7. Format the description (bold key points, add images inside it) and edit for brand voice before saving.
8. For every image in the product's media gallery: write alt text combining keyword + product + a visual descriptor (example given: "summer fragment bath bomb purple frontal" = keyword + product + color + angle), then rename the actual image file using that same text so the file name is descriptive rather than gibberish/numbers.
9. Repeat alt-text/file-name cleanup for store-wide media under Content > Files, since a lot of the media library will show meaningless numeric file names by default. `[verify UI]`
10. Scroll to the product's own Search engine listing section. If the title changed, the listing preview title updates automatically.
11. Write a meta description around 160 characters (have ChatGPT draft one from the description, then edit) — this field should sell the click more than pack in keywords; a good product-description excerpt can be left as-is if it already reads well.
12. Edit the URL handle: strip filler words, keep it descriptive (grammar/special characters are not needed in a handle).
13. Before saving, confirm the checkbox for automatic redirect from old URL to new URL is checked. `[verify UI]`
14. Save.
[cards 7b577e884e60][c9f57a4f6f3e][e9c397c88109][e7c0a899bee0]

### D. Collection page SEO
1. Do keyword research for the specific collection (per section A).
2. Write a descriptive collection title naming what's actually in it (presenter's example: turn a vague "Bath" into something like "Summer Inspired Bath Bombs — Sweet Floral Fruity Scents").
3. Write a 100–400 word collection description containing the collection's keywords, so Google has crawlable content on the page.
4. If you don't want the description pushing the product grid down visually, use the theme editor to move the description block below the product grid — keep the text on the page either way.
5. Set the collection's own Search engine listing title (auto-updates if the collection title changed) and write a shorter meta description.
6. Edit the URL handle to remove filler words / reflect the real collection contents.
7. Confirm the automatic-redirect checkbox is checked before saving.
8. Repeat for every collection on the store.
[cards 04a11dea33db][1e1031d336d4 for the general title/desc/handle pattern]

### E. Regular pages and blog posts
1. Every Shopify Page and Blog Post has the same fields: Title (main keyword + optionally a secondary keyword), body content/description (with real keywords and real value, not filler), and its own Search engine listing meta description + URL handle.
2. Fill in all of the above for every existing page/post.
3. Publish new blog content on a regular cadence — presenter's stated minimum is 2 posts/month, ideally weekly — researched via Keyword Planner and topically close to what you sell.
4. Within page/post body content, add internal links wherever there's a natural opportunity (e.g., a "benefits of X" page or blog post links directly to the relevant product).
5. Do this broadly across the site so that crawling any one page leads Google to discover the next.
[card 1e1031d336d4]

### F. Mobile-friendliness and speed audit
1. Chrome: right-click > Inspect > toggle device toolbar > pick a device to preview (presenter used iPhone 12 Pro). `[verify UI]`
2. Safari: Develop menu > Enter Responsive Design Mode. `[verify UI]`
3. Check for: content overflowing the screen, distorted/shrunken images, unreachable elements. If none, the page passes.
4. Run Google PageSpeed Insights on the store URL; read the report. Note: the historical/field-data graphs reflect roughly the past 28 days, so a fix made today will not show in those graphs immediately.
5. Compress every image before upload — target under 2MB per image, and keep total page weight around 2MB. Use a free image-compression website (unnamed specific tool in transcript beyond "a free website"); presenter's own example: a 1.4MB uncompressed image cut roughly in half after compression. An SEO app can also bulk-compress already-uploaded images.
6. Do not apply `loading="lazy"` to any image that is above the fold / the Largest Contentful Paint element (hero banners, primary product image). Apply `loading="lazy"` to all other, off-screen images.
7. Audit installed apps: uninstall anything not actively delivering value (you can reinstall later); each app's code runs on third-party infrastructure you don't control and can slow the store.
8. Re-run PageSpeed Insights after fixes and continue addressing flagged issues.
[card cc5014d16cd8]

### G. Rich snippets / structured data
1. Add genuine, useful FAQ content (real pre-purchase questions) to blog posts or product pages.
2. Implement schema either via custom code (presenter references an external guide, not reproduced here — `[web check: current FAQ/product schema spec]`) or via an SEO app that generates FAQ and product-review schema without code.
3. For app-based snippets: toggle on the desired snippet type (FAQ, product grid, image, etc.), then run the app's built-in test tool to confirm correct injection.
4. Monitor Google Search Console for rich-result eligibility and errors.
[card 161c91717301]

### H. Sitemap submission
1. Settings > Domains: confirm/set your custom (non-`myshopify.com`) domain as the Primary domain. Do this BEFORE submitting the sitemap. `[verify UI]`
2. Visit `yourstore.com/sitemap.xml` in a browser and copy that URL.
3. In Google Search Console, create/link the property for your site if not already done.
4. Go to Indexing > Sitemaps, paste the sitemap URL, and submit. `[verify UI]`
5. If you change the primary domain again after submitting, submit a new sitemap.
[card b3744583a367]

### I. Brand information
1. Locate Shopify's brand settings tab (presenter couldn't recall the exact menu location and used Shopify Sidekick, Shopify's AI admin assistant, to find it — indicates this setting is not in an obvious top-level menu). `[verify UI]`
2. Add logo(s), brand colors, and identity assets.
3. Keep this current — Facebook, Google, and other sales channels pull this data to represent the brand when products sync to those channels.
[card 334b579ab369]

### J. Optional: SEO app setup (SEO Ant / "AI SEO") — promotional segment
1. Install from the Shopify App Store (search "SEO Ant"). Free plan available; paid plans carry a presenter-disclosed 35%-off-first-3-months code ("shopo") — **affiliate/sponsored, evaluate independently.**
2. Use the dashboard's speed score and "uncompressed images" flag; one-click "optimize" bulk-compresses product/collection images.
3. Use "speed up now" for further store speed help (some options may require a paid plan; "Instant Page" preload noted as free).
4. Use the per-page SEO score view to find and fix flagged on-page issues (e.g., missing H2s with keywords, too few in-body images, meta description missing target keyword).
5. Use "Search appearance" to toggle rich-snippet types (FAQ, product grid, image) on/off without code, then run the built-in test.
6. Use link management to find and fix broken links.
7. Use backlink tracking to see inbound links.
8. Use the built-in keyword-research tool and "analyze my keywords" (see Diagnostics, section 5) as a partial Keyword-Planner/Ahrefs replacement.
9. Use competitor tracking by entering a competitor's URL to monitor their ranking keywords over time.
[card 8a330a3d4691]

## 4. Rules, thresholds and numbers

| Rule | Number / threshold | Condition | Source's basis | Card id |
|---|---|---|---|---|
| Keywords per page | 1 main + 2 supporting | Every distinct page (homepage, each product, each collection, each post) | Presenter's stated method | 2fc78c801ced |
| "Homemade soap" example volume | 1,000–10,000 searches/month | Example seed keyword in Keyword Planner, presenter's demo | Google Keyword Planner (presenter's screen) | 2fc78c801ced |
| Example CPC range | $0.20–$1.54 per click | Same example keyword | Google Keyword Planner (presenter's screen) | 2fc78c801ced |
| Secondary keyword volume example | 100–1,000 searches/month | Presenter's chosen supporting keyword | Google Keyword Planner (presenter's screen) | 2fc78c801ced |
| Homepage title character limit | 70 characters (63 used in demo) | Shopify's Online Store > Preferences title field, at time of recording | Presenter's screen `[verify UI]` | 1f41cebc6554 |
| Product/description word count | at least 100 words; 300–400 ideal | Product description body | Presenter's stated rule of thumb | 7b577e884e60 |
| Meta description length | ~160 characters | Any per-page Search engine listing meta description | Presenter's stated target, matches common SEO convention | e9c397c88109 |
| Image file size | under 2MB per image | Any image uploaded to Shopify | Presenter's stated rule | c9f57a4f6f3e / cc5014d16cd8 |
| Total page weight | roughly 2MB | Whole page, informal target | Presenter's stated rule | cc5014d16cd8 |
| Example compression result | 1.4MB image, ~50% size reduction after compression | Presenter's demo upload | Presenter's screen | cc5014d16cd8 |
| PageSpeed field-data lag | ~28 days | Reading Google PageSpeed Insights historical graphs after a fix | Presenter's stated caveat | cc5014d16cd8 |
| Collection description length | 100–400 words | Any collection page description | Presenter's stated rule | 04a11dea33db |
| Blog/content cadence | at least 2 posts/month, ideally 1/week | Ongoing content strategy | Presenter's opinion, explicitly not a documented Google requirement | 1e1031d336d4 / ec29d900d61f |
| SEO Ant discount | 35% off, first 3 months, code "shopo" | Paid plan signup at time of recording | Presenter disclosure — promotional/affiliate | 8a330a3d4691 |
| App SEO score example (before H2 fix) | rose to 91% | After adding a keyword-bearing H2 to one product's description | SEO Ant app score (presenter's demo) `[verify UI: app-specific]` | 8a330a3d4691 |
| App SEO score example (after images + meta keyword) | rose to 94% | After adding 1–4 in-description images and the meta keyword | SEO Ant app score (presenter's demo) `[verify UI: app-specific]` | 8a330a3d4691 |

## 5. Diagnostics and checks

- **H1 audit**: right-click any page element > Inspect; confirm exactly one `<h1>` exists. On Shopify's Dawn theme the homepage H1 is typically the store logo; collection pages use the collection title as H1; product pages use the product title as H1. Custom sections built by a developer or the merchant can silently add a second H1 — check these specifically. If 2+ H1s are found, demote the extra one(s) to H2 or lower and re-inspect. `[verify UI: theme-dependent, verify on non-Dawn themes]` [30ee2355cc6d]
- **Mobile rendering check**: Chrome DevTools device toolbar or Safari Responsive Design mode; look for overflow, distorted images, unreachable content. Pass/fail is visual judgment, no numeric score given. [cc5014d16cd8]
- **Speed check**: Google PageSpeed Insights on the store URL; remember the graphed "field data" lags ~28 days behind a fix. Large uncompressed images and above-the-fold lazy-loading are the two specific causes named. [cc5014d16cd8]
- **App SEO score (SEO Ant example)**: a low/bad baseline score on an unoptimized page rose to 91% after adding an H2 containing the target keyword, then to 94% after adding 1–4 in-body images and including the target keyword in the meta description; one issue (more images) remained unresolved at 94%. Treat these percentages as one app's internal heuristic, not a Google ranking signal — no ranking outcome (traffic, position) was shown to follow from the score change. `[verify UI: app-specific score algorithm]` [8a330a3d4691]
- **Existing-ranking audit**: in an SEO app's "analyze my keywords" feature (SEO Ant shown), list which keywords a page currently ranks for; flag pages ranking for zero-volume or irrelevant terms (blog posts most often cited) and adjust that content toward keywords with real relevance/volume. [f70db477cc54]
- **Competitor ranking check**: enter a competitor's URL into Keyword Planner ("start with website") or an SEO app's competitor tracker to see keywords they already rank for and how those change over time; use this to find keyword gaps or strategies to adapt. [2fc78c801ced][f70db477cc54]
- **Domain check before sitemap submission**: Settings > Domains; confirm the custom domain (not the `myshopify.com` one) is set as Primary before submitting the sitemap. `[verify UI]` [b3744583a367]

## 6. Tools, settings and named features

| Tool / feature | Used for | Notes |
|---|---|---|
| Google Ads > Keyword Planner | Search volume, competition, CPC by keyword; "start with website" for competitor keyword gaps | Free, requires a Google Ads account. `[verify UI]` |
| Google Trends | Related/adjacent query discovery | Free. Look at "related searches" at page bottom. |
| Glimpse (Chrome extension) | Adds more depth/detail to Google Trends data | Named specifically; not evaluated for cost/limits in transcript. `[web check: current pricing/features]` |
| Ahrefs | Deeper keyword research, intent labeling, country-level volume | Presenter notes it is "high-end" and "kind of expensive." `[web check: current pricing]` |
| Semrush | Deeper keyword research, explicit intent labels (informational vs. transactional), keyword variations | Presenter notes pricing "might not fit a lot of budgets." `[web check: current pricing]` |
| ChatGPT | Drafting titles, descriptions, meta descriptions from specs/keywords | Every output is edited by the presenter before publishing; explicitly warned not to sound "obviously AI-created." |
| Google search autocomplete | Free keyword-candidate source | Validate any candidate back in Keyword Planner. |
| Chrome DevTools (Inspect > device toolbar) | Mobile rendering preview; also used to inspect which element is the H1 | Free, built into Chrome. `[verify UI]` |
| Safari Develop > Responsive Design Mode | Mobile rendering preview (Safari equivalent) | `[verify UI]` |
| Google PageSpeed Insights | Site speed diagnostics, LCP and other Core Web Vitals data | Free. Field data lags ~28 days. |
| Free image compression website | Reduce image file size before upload | Presenter does not name the specific site; described only as "a free website." `[web check: which tool]` |
| Google Search Console | Sitemap submission, indexing status, rich-result eligibility/errors | Free, requires domain property verification. `[verify UI]` |
| Shopify Sidekick | AI admin assistant; presenter used it to locate the Brand settings tab | Native Shopify feature. `[verify UI]` |
| Shopify Dawn theme | Default/reference theme for H1 behavior example (homepage H1 = logo) | Theme-specific finding; other themes not verified in source. |
| SEO Ant ("AI SEO") Shopify app | Bulk image compression, speed tools, per-page SEO scoring, no-code rich snippets, broken-link management, backlink tracking, built-in keyword research and competitor tracking, rank-tracking | **Sponsored/affiliate**: presenter provides a 35%-off first-3-months discount code ("shopo"). Free tier exists. Evaluate independently; do not treat the recommendation as neutral. `[web check: current app, pricing, features]` |

## 7. Examples and case results

- Example: presenter's own "demo store" (soap and shampoo). Main keyword chosen: "homemade soap" (1,000–10,000 monthly searches, high competition, $0.20–$1.54 CPC). This is a demonstration, not a documented business outcome (no traffic or sales numbers given for the demo store itself). [2fc78c801ced]
- Example: homepage title used 63 of a 70-character limit, containing "homemade soap," "body wash," "healthier skin." [1f41cebc6554]
- Example: a product originally titled "Sweet Honey Bomb" (uninformative to Google and shoppers) was rewritten using ChatGPT-assisted, Keyword-Planner-validated keywords into a descriptive, keyword-bearing title. No before/after ranking or traffic data given — illustrates the method only. [7b577e884e60]
- Example: alt text pattern demonstrated — "summer fragment bath bomb purple frontal" (keyword + product + color + angle). [c9f57a4f6f3e]
- Example: one uncompressed product image was 1.4MB; the free compression tool cut it roughly 50%. Presented as a general speed-fix example, not a measured store-wide speed improvement. [cc5014d16cd8]
- Example: collection titled "Bath" (uninformative) reframed to something like "Summer Inspired Bath Bombs — Sweet Floral Fruity Scents." No ranking outcome given. [04a11dea33db]
- Example (app score): one product page's SEO Ant score moved from a poor baseline to 91% (after adding a keyword H2) to 94% (after adding description images and a meta-description keyword), stopping short of 100% for lack of more images. Marked explicitly in the source's own card caveats as an app-specific heuristic, not a ranking outcome. [8a330a3d4691]

## 8. Mistakes the source warns about

- Not putting thought into the homepage title/meta description — "many Shopify owners... don't put a lot of thought into them... that's why they miss out on a lot of traffic." [1f41cebc6554]
- Leaving vague, non-descriptive product titles (e.g., "Sweet Honey Bomb") that tell Google nothing about the product. [7b577e884e60]
- Writing product descriptions that are only specs with no real copy — "this is not enough usually" — under the ~100-word floor. [7b577e884e60]
- Leaving image file names as gibberish/numbers instead of descriptive, keyword-bearing names. [c9f57a4f6f3e]
- Uploading images straight from a camera, uncompressed and oversized, which slows the whole store. [cc5014d16cd8]
- Lazy-loading above-the-fold / LCP images. [cc5014d16cd8]
- Leaving the "create a redirect" checkbox unchecked when changing a URL handle, causing 404s on bookmarked/linked URLs and lost conversions. [e7c0a899bee0]
- Skipping collection descriptions entirely just to avoid pushing the product grid down (the source treats this as a mistake with an easy fix: move the description below the grid, don't delete it). [04a11dea33db]
- Installing and keeping apps that aren't actually used or valuable — third-party app code you don't control can degrade performance. [cc5014d16cd8]
- Multiple H1 tags on one page, often introduced unknowingly through a custom-built section. [30ee2355cc6d]
- Submitting the sitemap before setting the correct primary (custom) domain. [b3744583a367]
- Publishing AI-generated copy unedited, so it reads as obviously AI-written rather than in the brand's voice. [7b577e884e60]
- Pages/blog posts ranking for keywords with no search volume or no commercial relevance and never being corrected. [f70db477cc54]

## 9. Caveats, conflicts and what is missing

- The entire back half of the video is a paid/affiliate placement for the SEO Ant app, including a personal discount code. Every claim about that app's effectiveness comes from the presenter's own demo on his own store, with no independent verification, and should be weighed as marketing, not as neutral tooling advice. [8a330a3d4691]
- The source gives no numeric ranking or traffic outcome tied to any of its own recommendations (no before/after organic traffic, no keyword position tracked over time on the demo store). All "this will help you rank" statements are asserted, not measured, in this source.
- Blog-cadence claims ("2x/month minimum, ideally weekly") and the backlink-authority-transfer claim are explicitly marked in the cards as the presenter's opinion / stated mechanism, not documented Google policy or a cited study. Do not treat these as fixed ranking thresholds. [1e1031d336d4][ec29d900d61f]
- The Dawn-theme "homepage H1 = logo" finding is stated as verified only for Dawn; the source explicitly says it does not know whether this holds on other themes. [30ee2355cc6d]
- App SEO score percentages (91%, 94%) are internal to SEO Ant and not explained in terms of methodology; they should not be read as a ranking or traffic proxy. [8a330a3d4691]
- The source does not name the "free" image-compression website it uses on screen, so that specific tool cannot be verified or linked. `[web check: which tool]`
- No treatment of technical SEO topics that are common in other SEO sources: canonical tags, structured data beyond FAQ/product schema, hreflang/international SEO, Core Web Vitals beyond LCP/lazy-loading, robots.txt, or crawl budget. This source is scoped to a beginner's on-page/technical checklist, not a comprehensive technical SEO reference.
- No conflict with other ecomOS sources was identifiable from this document alone (no other 15-SEO-search mini playbooks existed at the time this was written); flag any conflict found later during the pass-2 merge, particularly around blog cadence claims and app-score usage, which may be treated differently by other sources.

## 10. Card index

- [2fc78c801ced] Keyword Research Workflow with Google Keyword Planner and Trends
- [6c1d36ed15c3] Separate Informational vs Transactional Search Intent
- [1f41cebc6554] Edit Global Store SEO: Homepage Title and Meta Description
- [30ee2355cc6d] Enforce a Single H1 Tag Per Page
- [7b577e884e60] Write SEO Product Titles from Specs Using Keyword Data
- [c9f57a4f6f3e] Image SEO: Alt Text, File Names, and Formatting
- [e9c397c88109] Write Product Meta Descriptions That Earn Clicks
- [e7c0a899bee0] Clean URL Handles and Enable 301 Redirects
- [04a11dea33db] Optimize Collection Pages Without Pushing Products Down
- [1e1031d336d4] Optimize Pages and Blog Posts, Then Interlink Them
- [cc5014d16cd8] Mobile-Friendliness and Page Speed Checks for Ranking
- [161c91717301] Add Rich Snippets (FAQ and Product Schema)
- [b3744583a367] Submit the Shopify XML Sitemap to Search Console
- [334b579ab369] Set Brand Information for Search and Sales Channels
- [ec29d900d61f] Build Backlinks and Recurring Content for Authority
- [f70db477cc54] Audit Existing Rankings to Fix Wasted Content
- [8a330a3d4691] Deciding Whether to Automate Shopify SEO with an App
