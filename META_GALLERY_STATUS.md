# Meta ad gallery: handoff (23 Sep 2026)

## Update 8: competitor pills, 3 more brands

- **Pills** at the top of Competitors: All brands, then one pill per brand with its active ad count. All shows a side-by-side table (formats, median and longest days live, new in 14 days, share pushing an offer, main button). A brand pill shows that brand's numbers, its top ideas and its ads.
- **New brands:** BlueStone (page 158294897592584, about 97 active ads), Candere by Kalyan Jewellers (671337662931060, about 438) and Jewelbox (101266742327321, about 55). 30 active ads each, with images, pulled from Ad Library on 23 Sep 2026. The first 30 the library shows are mostly the newest ads, so their "longest running" reads low.
- **Catalog ads** (text with {{product.name}}) now show as "Catalog", not carousel.

## Update 7: tests to run, sales on the action plan

- **Tests to run this week** (top of Action plan, `web/testlab.js`). Ranked test briefs built from website sales and Meta together. Each has why (with numbers), the test, budget and time, win rule and stop rule, plus Add to tests, Copy brief and Make the creative. Types today: best seller with no ad, category budget gap, on/off measurement test, weekday budget, price point message, and EMI, custom made or COD messages when buyers use them but ads do not.
- **Best sellers with no ad.** Top 10 pieces from the last 3 months that no ad names, each with "Make an ad".
- **Action plan cards** show how the ad's product category sells on the website vs its share of product ad spend (last 30 days).
- **Ad side panel** shows the ad's daily spend next to website sales of its category, 1 Aug to 23 Sep, with a note that this is not proof of cause.
- **Product role in the builder.** The pasted image can be "A layout to borrow" or "The product to show". Product mode puts a new piece into your winning ad's layout. `/api/variants` takes `ref_role`.
- Tests: 49 passing.

## Update 6: paste a reference image, daily Metabase sales

- **Reference image.** Creative studio has "Make variants from a reference". Pick your ad, then paste (Ctrl+V), drop or choose any image. Both go to the AI. `/api/variants`, `/api/ask` and `/api/competitor-variants` take `ref_image` (base64 JPEG, PNG or WebP, max 2.5 MB). "Use as reference" on the Competitors tab opens this panel.
- **Daily sales.** Brand sales has a Months / Days switch. Days covers 1 Aug to 23 Sep 2026, pulled per day from Metabase dashboard 6 (the same cards, date filter set to 1 day). Presets, From/To, KPIs vs the same number of days before, a daily chart with Meta spend and claimed value, a sortable day table with CSV export, category vs ad spend, price bands, payment method and top products.
- **Check.** Daily sums match the monthly cards exactly: Aug ₹87,45,057 and 307 items, Sep to date ₹56,13,022 and 177 items.
- Data: `sales.json` key `daily` (date → cards). To refresh, ask Claude to pull the dashboard again day by day.

## Update 5: competitor ads in the page, competitor reference for new ads

- **Competitor cards.** The Competitors tab shows each ad from the Ad Library snapshot in the page: image, headline, text, CTA, days live, versions, and a Video or Carousel badge. 40 of 48 ads have a picture. The other 8 say "Preview unavailable". "View in Ad Library" stays as a second link.
- **Top ideas to borrow.** A ranked list of the 8 strongest competitor ads. Score = 65% days live (capped at 180) + 35% versions live (capped at 5). Meta shows no spend for these ads, so the page calls it a signal, not proof.
- **Filters.** Brand and format (image, carousel, video). Each brand header shows its format mix.
- **Use as reference.** Pick one of your image ads and one competitor ad. Both images go to the AI. The prompt says to borrow layout, framing, format and mood only, and never to copy text, logo, product, models or faces.
  - Shared page: Claude gets both images and writes 3 ideas with copy.
  - Local app: `/api/ask` takes `comp_ad_id`. `/api/competitor-variants` reads `comp.ad_id`, sends both images to the text model and to the image model (2 `image[]` parts).
- **Data.** `data/meta-gallery/comp_media.json` (40 ads, images as base64 JPEG). Served at `/comp_media.json`.
- **Clean-up for clients.** Removed "Ideas only here. Images are made from the desktop version of this gallery." and "New image versions are made from the desktop version of this gallery." The footer and client report now say "Meta Ads Manager, read-only" instead of the connector name. A code comment no longer names the settings file.

Tests: 48 passing (new: competitor reference goes to both models).

## Update 4: themes, campaigns, insights, video, compare, notes, CSV, competitors

The local app and the shared claude.ai page now run the same web page (`meta_gallery/web`). The old page is still at `/old`.

New tabs and features:

- **Campaigns**: campaign rows open to show ad sets. Spend, share, value, ROAS, CPA, change vs previous, verdict. CSV export. Campaign rows add up to the account total.
- **Insights**:
  - Anomaly alerts: days where spend or ROAS moved 50% or more vs the median of the 14 days before, with the 3 ads that moved most.
  - Weekly trend: spend bars (excluded campaigns in grey) and a separate ROAS line, whole year, selected dates shaded.
  - Budget shift: moves a share of running Cut ads' daily spend to running Scale ads. Controls for share (default 50%) and how much ROAS Scale ads keep (default 70%). A guide only. The page cannot change budgets.
  - Creative themes: angle, product and opening line tags from ad name, campaign name and copy (`meta_gallery/themes.py`). Rule based, each tag shows the word that set it.
  - Video metrics: hook rate (3s plays ÷ impressions), hold rate (ThruPlays ÷ 3s plays), avg watch, 25% and 100% reached. 3s plays = spend ÷ cost per 3s play (Meta has no 3s play count at ad level). Ads where video played in under 20% of impressions are flagged "mostly shown as image" and left out of averages.
  - Creative lifecycle: median days live, to peak 7-day ROAS and to fatigue by format, plus stopped ads worth relaunching.
  - Day of week and platform: spend per day and ROAS by weekday; platform split for the dates and by month.
- **Competitors**: active Ad Library ads for CaratLane, GIVA, Melorra and Mia by Tanishq, grouped by headline, longest running first. Meta shows no spend for these.
- **Gallery**: tag chips, video hook and hold on cards, compare up to 4 ads side by side, Export CSV of the grid.
- **Team notes** on each ad (side panel). Local app saves to `data/meta-gallery/notes.json`.

Data: the 1-year capture now has `video_daily` (2,479 ad-days). Competitors are in `data/meta-gallery/competitors.json`. Rebuild the cache after pulling: `python -m meta_gallery.snapshot`.

Server: new routes `/data.json` (cache without CDN links), `/settings.json`, `/notes.json`, `/competitors.json`, and `POST /api/save/settings.json` and `/api/save/notes.json` (validated, same-origin only). Everything else is still read-only. Tests: 38 passing.

## Update 3: one year of data, date picker, exclusions, verdicts, fatigue, client report

**Data.** One year, 23 Sep 2025 to 22 Sep 2026, pulled through the MCP connector (read tools only):

- 472 ads that spent, 9,294 ad-day rows (spend, purchases, purchase value, impressions, link clicks).
- Monthly age, gender and platform rows for every ad (4,963, 2,226 and 2,931 rows).
- Details for all 364 creatives, 110 videos, 55 carousel card images and 330 ad sets.
- Checks:
  - Daily rows add up to ₹1,29,30,745. Meta's per-ad yearly totals add up to ₹1,29,30,671, and the account total is ₹1,29,31,741.
  - Every monthly breakdown matches the daily rows for the same month within ₹39.
  - The last 3 months still give ₹33,07,577 spend, ₹1,23,63,068 value and 3.74x, the same as before.
- Raw file: `data/meta-gallery/raw/mcp_capture_2026-09-23_1y.json` (git-ignored).

**New in the page:**

1. **Dates.** Presets (7, 14, 30, 90, 180 or 365 days, this month, last month) or any custom From/To inside the stored year. "Compare to previous period" puts the same number of days just before next to the totals. Change figures only show when that whole period is inside the stored year.
2. **Exclusions.** Type words (for example `sale, eoss, bfcm`), or tick campaigns in "Pick campaigns". Matching campaigns leave every figure: totals, the format table, the top 30 and the charts. The note under the bar lists what was left out and its spend. "Save as preset" keeps the combination for later.
3. **Targets and verdicts.** Target ROAS and CPA default to the average for the selected dates. You can save your own. Each ad in the top 30 gets a verdict:
   - **Scale:** ROAS at or above target.
   - **Watch:** ROAS within 30% below target, or no purchases yet with spend under 2x target CPA.
   - **Cut:** ROAS more than 30% below target, or no purchases after spending 2x target CPA.
   - **Not enough data:** spent less than 1 target CPA.
4. **Fatigue.** Compares each ad's last 7 days with the 21 days before:
   - **Declining:** link CTR down 25% or more, and ROAS down 30% or more (or purchases stopped).
   - **CTR falling** or **ROAS falling:** only one of the two dropped.
   - The panel shows daily spend plus rolling 7-day ROAS and link CTR lines.
5. **Client report.** The "Client report" button opens a printable page for the same dates and exclusions. It has:
   - Totals with change, the format table and age/gender charts.
   - The top 12 ads, Scale and Cut lists, and fatigue alerts.
   - Your agency and client name.
   - Use "Print or save as PDF".

**Limits:**

- Age, gender and platform rows are stored by calendar month, so the charts cover every month that overlaps the dates you pick. The page says which months.
- Settings (targets, presets, branding) live in `data/meta-gallery/settings.json`. `POST /api/settings` is the only write the server accepts. It only takes JSON from the local page, and it never touches Meta.
- `graph_client capture` now writes the same one-year format, but it is still untested (API route deferred).

Tests: 29, all on synthetic data.

## Update 2: value, ROAS and age/gender charts

- **Format table** (open under the title) now shows ads, spend, share, purchase value and ROAS for each format, plus an "All formats" total. It covers every ad that spent in the period, not only the 30 shown. ROAS = purchase value ÷ spend. Ads with no reported value count their spend and add no value, and the note under the table says how many.
  - Check: the 3-month "All formats" row (₹33,07,532 spend, ₹1,23,63,068 value, 3.74x) matches the account-level totals Meta reported for the same dates.
  - For 6 months I re-read all 242 ads with purchase value so this table is complete.
- **Spend and ROAS by age and gender**: four small bar charts (amount spent by age, ROAS by age, amount spent by gender, ROAS by gender). They cover the ads currently shown and follow the Format, Period and filter choices. Each group's ROAS is its summed purchase value ÷ its summed spend. A group where Meta reported no purchases shows "No purchases reported", not 0x. Hover a row for spend, share, value and purchases.
  - The charts come from breakdown rows, so they are a separate view of the same spend, not extra results.
- Tests: 15 (added format value/ROAS and age/gender grouping).

## Update: all ad formats added

The gallery now covers every format, not only single images. A new **Format** menu picks the view:

| View | 1 month | 3 months | 6 months |
|---|---|---|---|
| All formats (top 30 by spend across everything) | 30 | 30 | 30 |
| Single image | 8 | 30 | 30 |
| Video | 15 | 30 | 30 |
| Carousel | 4 | 4 | 4 |
| Catalog | 11 | 22 | 25 |
| Flexible / mixed | 13 | 18 | 30 |

Each view is its own top 30 by spend (or fewer when fewer ads spent). "All formats" is the default. The single-image views hold exactly the same ads as before.

What each format shows:

- **Single image:** full image, same as before.
- **Carousel:** first card as the picture. The panel lists every card with its headline, text, image and landing-page URL. Carousels are the only format where Meta's connector returns landing pages.
- **Video:** Meta's 160px video thumbnail, the video length and a "Watch video on Facebook" link.
- **Catalog:** Meta picks products per viewer, so no single image represents the ad. It shows Meta's small 64px thumbnail and the product set ID.
- **Flexible / mixed:** Meta exposes no single image or video. It shows the 64px thumbnail.
- **Every format:** has an "Open post" link to the Facebook post behind the ad, and a note explaining what the picture does and does not show.

New checks for this update:

- 156 ads now have full detail across the 3 periods. Creatives, video details, carousel card images and ad set attribution were read for all of them.
- ROAS matches Meta's own figure for all 144 ad-period pairs where both exist.
- Breakdown rows match ad totals for all but 8 ads. For those 8 the rows run up to ₹18.51 above the total (under 0.02%). The breakdowns were read about 30 minutes after the totals, and Meta's figures shifted slightly in between. The panel says so when this happens.

After updating, run `python -m meta_gallery.server --prefetch-images` again to download the new pictures.

---

A private, read-only gallery of the top 30 static image ads by spend for ad account `577226564072364` (Gehna - 1, INR, Asia/Kolkata). It is a separate addition. The intelligence cards, library and retrieval code were not changed.

## 1. Connection method

**Working: the Meta Ads MCP connector (`mcp.facebook.com/ads`) connected in Claude.** Claude's connector flow is already authorized for this Meta user. It listed 20 ad accounts. Account `577226564072364` is active, queryable and MCP-enabled. All data in the gallery came from this route on 23 Sep 2026.

The Codex registration of the same endpoint still fails. Meta's server does not offer dynamic client registration or the CIMD method Codex tried. Claude's connector uses its own registered client, so it is not a fix you can copy into Codex. Treat Claude as the MCP route and the direct API as the route for automated refresh.

**Blocked: the direct Marketing API.** Your earlier requests returned error `200` "API access deactivated". I could not re-test it: neither this session's cloud sandbox nor the shell on your computer can reach `graph.facebook.com` (their network proxy returns 403). So the direct route is unverified from here. A check command is ready for you to run on Windows.

To reactivate the direct API:

1. Open [developers.facebook.com/apps](https://developers.facebook.com/apps) and select the app that issued the token.
2. Read the alert or restriction banner on the app dashboard. Complete what it asks (often a Data Use Checkup, verification or a policy item). Only the dashboard shows the real cause.
3. Confirm the Marketing API product is added to the app.
4. Create a new token with only `ads_read`. A Business Manager system user token assigned to this one ad account is the safest choice and does not expire every 60 days.
5. Put it in `.env` as `META_ACCESS_TOKEN=...` (keep `META_AD_ACCOUNT_ID=act_577226564072364`).
6. Run `python -m meta_gallery.graph_client check`. It prints token validity, type, expiry, scopes, account access and one reporting and one creative read. It never prints the token.

## 2. Permissions and token expiry

- **MCP route:** Meta authorized the connector through OAuth in Claude. Its scopes and expiry are not exposed to me, so I cannot report them. The connector itself is not read-only: it also offers create, update, activate and delete tools. I used only read tools (`ads_get_ad_accounts`, `ads_get_ad_entities`, `ads_get_creatives`, `ads_get_field_context`). Nothing was created, edited, paused, activated or published.
- **Direct route:** not verified (see above). `graph_client check` will report scopes and expiry, and warns if the token holds write scopes such as `ads_management`.
- The gallery server reads no credentials. It only reads the cache file. `graph_client.py` reads `.env` on the backend, only sends GET requests and scrubs the token from errors.

## 3. Checks completed (all read-only)

| Check | Result |
|---|---|
| Account access | 20 accounts listed; `577226564072364` active and queryable |
| Reporting, ad level | 51 ads with spend (1 month), 128 (3 months), 242 (6 months) |
| Completeness | Sum of ad spend vs account spend: 1 month ₹1,234,338.85 vs ₹1,234,368.51; 3 months ₹3,307,532.08 vs ₹3,307,566.01; 6 months ₹6,843,186.59 vs ₹6,844,213.68. The 6 month gap (₹1,027) is below the 30th ad's spend (₹2,287.55), so it cannot change the top 30 |
| Creative reads | Type checked for every creative that spent (179 creatives); detail read for the 28 creatives behind the selected ads |
| Breakdowns | Age x gender and platform x placement rows sum exactly to each ad's spend for all 68 ad-period pairs |
| ROAS math | Our ROAS (value ÷ spend) matches Meta's `purchase_roas` for all 18 ads where both exist (max difference 0.0000003) |
| Attribution | Read per ad set: `1d_view_7d_click_1d_ev` (7-day click, 1-day view, 1-day engaged view) for most, `1d_view_7d_click` for 4 of 34 ad sets |

**Ads Manager comparison: still to do by you.** I cannot open Ads Manager. Set the date range and an ad-level view, use the "Attribution setting" column, and compare these (3 months, 23 Jun to 22 Sep 2026):

| Ad ID | Name | Spend | Purchases | Purchase value | Impressions | Link clicks |
|---|---|---|---|---|---|---|
| 120245250941310138 | Review ads | ₹10,556.07 | none reported | none reported | 276,571 | 4,768 |
| 120243916091730138 | 2 | ₹10,049.89 | none reported | none reported | 92,994 | 1,703 |
| 120246163414290138 | 1 day to go | ₹9,700.07 | 2 | ₹121,965.50 | 165,962 | 13,176 |
| 120243916091770138 | 2 | ₹9,651.98 | none reported | none reported | 45,896 | 1,068 |
| 120246163414280138 | 2 days to go | ₹9,462.13 | 1 | ₹54,360.00 | 22,400 | 1,477 |

Purchases here are Meta's "purchases" metric (all sources, `omni_purchase`). Ads Manager's "Website purchases" column can differ.

## 4. Files changed and how to run

New files:

- `meta_gallery/metrics.py`: metric math. Missing values stay `None`.
- `meta_gallery/snapshot.py`: builds the cache from a raw capture. Picks the top 30 single-image ads by spend per period.
- `meta_gallery/server.py`: local read-only server on `127.0.0.1:8765`. Serves the cache and caches images to disk.
- `meta_gallery/graph_client.py`: direct API `check` and `capture` (GET only). Untested until the app is reactivated.
- `meta_gallery/static/index.html`, `app.js`, `style.css`: the grid and side panel.
- `tests/test_meta_gallery.py`: 13 tests (synthetic data only).
- `META_GALLERY_STATUS.md`: this file. `README.md` gained a short pointer section.
- Private, git-ignored under `data/meta-gallery/`: `raw/mcp_capture_2026-09-23.json` (the Meta responses), `cache/gallery.json` (built cache), `images/` (downloaded creatives).

Run from the project folder in PowerShell (Python 3.11+, standard library only):

```powershell
python -m meta_gallery.snapshot                    # rebuild cache from newest raw capture
python -m meta_gallery.server --prefetch-images    # download creative images once (do this before 27 Sep)
python -m meta_gallery.server                      # open http://127.0.0.1:8765
python -m unittest tests.test_meta_gallery -v
```

The image links Meta returned expire around 27 Sep 2026. Run the prefetch before then. After that, images are served from `data/meta-gallery/images/` and the page works offline. If an image is missing, the card says so instead of breaking.

To refresh data: once the direct API works, run `python -m meta_gallery.graph_client capture` and then `python -m meta_gallery.snapshot`. Until then, ask Claude to repeat the MCP capture. Browsing never calls Meta.

Nothing was committed or pushed. The local repo still has no commits, and `data/` and `.env` stay ignored.

## 5. Unsupported fields and reporting limits

- **Collection size:** 3 and 6 months have 30 ads each. The last 1 month has only 8 single-image ads with spend, so it shows 8 and says so.
- **Excluded formats:** only single-image creatives qualify. In 3 months, 93 of 128 spending ads were excluded: 49 video, 22 catalog, 18 flexible or mixed, 4 carousel. The page lists the excluded counts and top excluded spenders.
- **Flexible or mixed:** these creatives expose no single image hash (likely Advantage+ flexible creative or asset feeds). The MCP cannot return `asset_feed_spec`, so I could not confirm which. They are flagged and excluded, not shown as one image.
- **Purchases often missing:** 25 of the 30 ads in 3 months have no purchase data from Meta. Meta omits the field when nothing was attributed. The page shows "Unavailable", not 0, and the ROAS filter reports how many ads it hid for this reason. Collection ROAS (₹361,879 ÷ ₹111,373 = 3.25x) counts their spend with no value.
- **Landing page URL:** the MCP returned no `link_url` for any selected creative. Shown as unavailable. The direct API capture reads it from `object_story_spec`.
- **Shared images:** 21 of 30 ads in 3 months share an image with another selected ad (for example 10 ads use the same rings image). Each keeps its own metrics; the panel lists the siblings.
- **"Dynamic" campaign name:** 3 ads in the 6 month set sit in "Dynamic chains ad". Meta reports those ad sets do not use dynamic creative and each creative has one image. They are kept and carry a note.
- **Demographics:** breakdowns appear only in the side panel, labelled as splits of that ad's totals. No demographic filters yet, so every card metric covers the whole ad.
- **Dates:** "last N months" means the N months up to yesterday in account time (for example 23 Jun to 22 Sep). Nothing earlier than 6 months is fetched.
- **Attribution:** Meta's default per ad set setting. No override was applied.

## 6. What remains

1. Reactivate the Meta app and run `graph_client check`, then a first direct `capture`. Fix any field mapping issues it shows.
2. Run the image prefetch before 27 Sep.
3. Compare the 5 ads above with Ads Manager.
4. **Security:** `.env` has 3 lines without a `KEY=` name (lines 2, 3 and 6). Two look like API keys (OpenAI-style and DeepSeek-style). While checking the file I loaded it in a way that echoed those 3 values into this session's tool log. They were not sent anywhere else and are not in any project file. Please rotate those 2 keys and add the missing names to those lines.
5. Later, if wanted: demographic filters, videos, and a scheduled refresh.
