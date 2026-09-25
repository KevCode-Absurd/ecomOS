# Google PageSpeed Insights: Step-by-Step Tutorial to Boost Site Speed

source_id: 1TOW4yOCvuB0RbkEc_o8nsRhR2xxi8VuG  |  folder: /08-SPD-speed  |  cards: 10  |  words: 4649  |  type: transcript (YouTube tutorial)
credibility: Jack from Rank Math, a WordPress SEO plugin company. The video promotes Rank Math and uses WP Rocket (a paid WordPress speed plugin) for the fixes. Evidence: a live walkthrough of PageSpeed Insights on WP Rocket's own homepage and 1 before/after (69 to 99) on an unnamed page. Metric thresholds are read from Google's report. No client data.
date signals: Mentions the 2021 page experience update. Treats INP as a Core Web Vital and still shows First Input Delay (FID) in field data, which places it around 2024, when INP replaced FID. Refers to an older own video (recommends changing image width from 800 px to 1,200 px for Google Discover).

## 1. What this source is for

Use it to read a PageSpeed Insights (PSI) report correctly: field data vs lab data, URL vs Origin, what each metric means and its Good / Needs improvement / Poor bands, where to find the LCP element, how to pick the highest-impact fix, and how to fix Total Blocking Time and CLS on WordPress with WP Rocket settings using a safe 1-setting-at-a-time test loop.

## 2. Principles

1. **Do not chase a 100 score or a Core Web Vitals pass for its own sake.** Condition: SEO decisions. The presenter says content depth and serving the audience drive rankings; speed still matters for users and ranking. A page that takes 5 to 10 seconds makes visitors wonder "is this page spam?". [693051f7daf7]
2. **Focus on mobile.** Reason given: most people use the web on mobile, "not because it is harder to optimize". [085b91000740]
3. **Field data and lab data differ, and both are valid.** Field data = Chrome UX Report (CrUX), real Chrome users on mobile, averaged over 28 days. Lab data = Lighthouse simulation of a mid-tier device on a mobile network. If CWV fail but lab looks good, that is why. [085b91000740]
4. **Optimize against lab data; field data follows after about 28 days.** Condition: when choosing what to fix. This is the presenter's rule. [085b91000740]
5. **Only the top 3 field metrics are Core Web Vitals (LCP, INP, CLS).** FCP, FID and TTFB are "notable metrics"; 1 was labelled experimental. [dfde1d811af8]
6. **Text is the best LCP element** because it loads fastest (presenter's opinion). If LCP is an image, resize it, get it under 250 KB, use AVIF or WebP. If a video, compress it. [eb9525bda54a]
7. **Poor FCP is usually the theme, plugins and page elements, not the web server** (presenter's opinion). [dfde1d811af8]
8. **Reserve space for anything injected late.** Ads, embeds, iframes need a placeholder; images need explicit width and height. [883371c7111c]
9. **Long tasks over 50 ms block the main thread.** The main thread parses HTML, renders content and processes input. TBT adds up the blocking time. A failing TBT means a lot of complex JavaScript. Fastest fix: minify JS, defer or delay JS. [8f0d567d9844]
10. **Change 1 speed setting at a time and test the live site.** Each JS setting can break the site; testing 1 at a time tells you which one did it. [8f0d567d9844]
11. **Make sure the test saw your latest version.** Use an above-fold marker and check the PSI screenshot. [f1a837edbfbe]

## 3. Procedures

### 3.1 Run a PSI test
1. Search "PageSpeed Insights" and open the pagespeed.web.dev result. Or, in WordPress with Rank Math: front-end stats bar, or Rank Math SEO > External tools > Google PageSpeed. [verify UI]
2. Paste the URL and click Analyze.
3. Use the Mobile tab first; Desktop is the other tab. [085b91000740]

### 3.2 Read field data (top section, "what your users are experiencing")
1. Note the 3 Core Web Vitals (expand view to see which are CWV) and the other metrics.
2. Check the URL / Origin toggle. URL = this page. Origin = average of all pages on the site.
3. If the URL option is blocked, this page lacked enough Chrome traffic in 28 days; the tooltip says so. Read Origin as a site-wide signal only.
4. If the whole site lacks 28 days of traffic, there is no field data; work from lab data. [7d6d1e80db3c] [085b91000740]

### 3.3 Read lab data (second section, "diagnose performance issues")
1. Read the performance score: green 90+, orange 50 to 89, red below 50.
2. Look at the above-the-fold screenshot beside the score.
3. Hover the score circle. PSI shows which metric would most improve the score (demo: TBT). [verify UI]
4. Scroll to the opportunities. They are grouped by metric. Open the flagged metric's group first and work it top-down, retesting after each change.
5. Expand an opportunity for tool hints. Demo: "Serve images in next-gen formats" suggested the Performance Lab plugin or Imagify via WP Rocket's Image Optimization tab to make WebP. [verify UI]
6. Find the LCP element: Diagnostics > "Largest Contentful Paint element". Demo showed a text element. [verify UI] [693051f7daf7] [eb9525bda54a]

### 3.4 Confirm the test saw your changes
1. Add a small visible marker above the fold (for example a line of text).
2. Rerun PSI.
3. Check the screenshot. Marker visible = test used the new version. Not visible = cached version; clear cache and rerun.
4. Remove the marker afterward. [f1a837edbfbe]

### 3.5 Fix CLS
1. Look for injected content: ads, embeds, iframes.
2. Give each a placeholder with fixed space. Presenter says this is technical; a designer may be needed.
3. Add explicit width and height to images.
4. Quick fix on WordPress: WP Rocket image dimension setting "Add missing width and height attributes". Presenter says it improves CLS "drastically". [verify UI]
5. Retest. [883371c7111c]

### 3.6 Fix TBT with WP Rocket (test loop)
1. WP Rocket > File Optimization tab. [verify UI]
2. Tick "Minify JavaScript files" only. A warning says it could break things.
3. Save. Clear the site cache.
4. Visit several pages (incognito per the curator note) and check every element is in place and works.
5. If nothing breaks, keep it. If something breaks, untick that one setting.
6. Repeat the same loop for "Combine JavaScript files".
7. Repeat for "Load JavaScript deferred". Add exclusions for scripts that must load first. Plugin and theme scripts can be deferred too.
8. Repeat for "Delay JavaScript execution".
9. Rerun PSI. Demo: 69 to 99, most issues fixed, nothing visibly broken. [8f0d567d9844]

### 3.7 Share the report
1. Click the copy-link control in PSI. [verify UI]
2. Send it to the developer or consultant. The link opens the same report. [f338ed52ce8f]

### 3.8 Other Lighthouse audits
1. Accessibility: descriptive labels on buttons for screen readers; contrast between background and foreground.
2. Best practices: modern standards for speed, security, user experience.
3. SEO: valid structured data, page not blocked from indexing, title and meta description. The presenter says Rank Math's on-page checklist goes deeper than Lighthouse. [d162377f3446]

## 4. Rules, thresholds and numbers

| rule | number or threshold | condition | source's basis | card id |
|---|---|---|---|---|
| LCP | good 2.5 s or less; needs improvement 2.5 to 4 s; poor over 4 s | field and lab | Google bands read from PSI | [eb9525bda54a] |
| INP | good 200 ms or less; 200 to 500 ms needs improvement; poor over 500 ms | field | Google | [dfde1d811af8] |
| CLS | good 0.1 or less; 0.1 to 0.25 needs improvement; poor over 0.25 | field and lab | Google | [883371c7111c] |
| FCP | good under 1.8 s; 1.8 to 3 s needs improvement; poor over 3 s | | Google | [dfde1d811af8] |
| FID | good under 100 ms; 100 to 300 ms needs improvement; poor over 300 ms | field only; now replaced by INP | Google | [dfde1d811af8] |
| TTFB | good below 0.8 s; should not exceed 1.8 s | | Google | [dfde1d811af8] |
| Long task | over 50 ms | main thread | Lighthouse definition | [8f0d567d9844] |
| Performance score | green 90+, orange 50 to 89, red below 50 | lab | PSI | [693051f7daf7] |
| CrUX window | 28 days | field data | Google | [085b91000740] |
| LCP image size | below 250 KB | when LCP is an image | presenter | [eb9525bda54a] |
| Image width | 1,200 px (was 800 px) | Google Discover eligibility, not speed | presenter | [eb9525bda54a] |
| Demo result | 69 to 99 | 1 page after WP Rocket settings | case | [693051f7daf7] |
| Demo field vs lab | field LCP 1.6 s; field FCP 1.6 s vs lab FCP 1.1 s | WP Rocket homepage | example | [085b91000740] |

## 5. Diagnostics and checks

| check | how | good | bad | next |
|---|---|---|---|---|
| Field vs lab mismatch | compare top and bottom sections | explained by real devices and networks | treating 1 as an error | fix lab issues; wait about 28 days |
| URL field data missing | URL toggle greyed | page has data | only Origin | use lab data for the page |
| Which metric to fix | hover score circle | flagged metric found | working the list in order | open that metric's opportunities |
| LCP element | Diagnostics > LCP element | text, or image under 250 KB in AVIF/WebP | large image or video | resize, compress, convert |
| CLS cause | look for ads, embeds, iframes, images without dimensions | reserved space | content jumps | placeholders, width/height |
| TBT | lab TBT | low | high: much complex JS | 3.6 loop |
| Stale test | above-fold marker in screenshot | marker shows | marker missing | clear cache, rerun |
| Site broken after JS setting | clear cache, browse pages incognito | all elements work | anything broken | untick that setting |
| Poor FCP | review theme, plugins, page elements | lean front end | heavy theme and plugins | audit front end before buying hosting (presenter's view) |

## 6. Tools, settings and named features

- PageSpeed Insights (pagespeed.web.dev): Mobile/Desktop tabs, field section, URL/Origin toggle, expand view, lab section, performance score with hover hint, screenshot, opportunities grouped by metric, Diagnostics > LCP element, Accessibility, Best Practices, SEO audits, copy link. [verify UI]
- Chrome UX Report (CrUX): field data source.
- Lighthouse: lab engine.
- WP Rocket: File Optimization tab (Minify JavaScript files, Combine JavaScript files, Load JavaScript deferred with exclusions, Delay JavaScript execution); image dimensions setting "Add missing width and height attributes"; Image Optimization tab (Imagify). [verify UI]
- Performance Lab plugin (WordPress): WebP conversion, suggested by PSI.
- Rank Math: front-end stats bar, External tools > Google PageSpeed. [verify UI]

## 7. Examples and case results

- WP Rocket homepage: field LCP 1.6 s; FCP 1.6 s in field vs 1.1 s in lab. Example of field and lab disagreeing.
- A WP Rocket page had the URL option blocked because of low traffic; Origin shown.
- After WP Rocket JS settings on a demo page: performance 69 to 99, "nothing breaking". 1 page, not a promise.
- Google's CLS example: a shopper on checkout accidentally selects 56 items because the layout shifted.

## 8. Mistakes the source warns about

- Chasing 100 or a CWV pass at the cost of content. [693051f7daf7]
- Reading field and lab data as the same thing. [085b91000740]
- Reading Origin data as if it were the page's data. [7d6d1e80db3c]
- Turning on several JS settings at once; you will not know which broke the site. [8f0d567d9844]
- Testing without clearing cache; the report may show the old page. [f1a837edbfbe]
- Blaming the web server for poor FCP before checking theme and plugins. [dfde1d811af8]
- Injecting ads, embeds or iframes without reserved space. [883371c7111c]

## 9. Caveats, conflicts and what is missing

- WordPress and WP Rocket only for fixes; no Shopify steps.
- FID is shown as current in the video. The card adds that FID was replaced by INP in 2024 and that FCP and TTFB are diagnostic, not CWV. [dfde1d811af8] [web check: current CWV list and thresholds at web.dev/articles/vitals]
- The FID and INP analogies: FID = time until the browser starts processing a click; INP = time from the interaction to the next visual change. The card adds that INP may not include an async cart request finishing; track cart completion separately (card editorial, not in source). [dfde1d811af8]
- Conflict with source 02: this source says to optimize against lab (Lighthouse) data; source 02 says tool scores are not the best measure and ranks a slow-4G visual test first.
- Conflict with source 04: 250 KB image guidance here vs source 04's 100 KB (product) and 200 KB (hero). Source 04 lists "slow server response" as a main LCP cause; this source says FCP problems are usually not the server.
- "Delay JavaScript execution" can break add-to-cart or sliders if needed scripts are delayed (card caveat). [8f0d567d9844]
- Speed Index is only defined ("how quickly above-the-fold content becomes visually displayed"); no threshold given. [d162377f3446]
- The marker trick confirms freshness of the test, not real-shopper experience. [f1a837edbfbe]

## 10. Card index

- [085b91000740] Read PageSpeed Insights: Field Data (CrUX) vs Lab Data (Lighthouse)
- [7d6d1e80db3c] Use the Origin vs URL toggle to read low-traffic page speed
- [eb9525bda54a] Fix LCP by identifying the largest element and optimizing it
- [883371c7111c] Fix CLS on checkout and product pages with reserved space and image dimensions
- [8f0d567d9844] Reduce TBT by unblocking the main thread with JS minify, defer, and delay
- [f1a837edbfbe] Cache-bust your speed tests with an above-the-fold indicator
- [693051f7daf7] Use the performance score's hover hint to pick your highest-impact fix
- [dfde1d811af8] Sequence metrics: TTFB, FCP, FID, INP and what each one actually measures
- [d162377f3446] Speed Index and the remaining Lighthouse audits beyond performance
- [f338ed52ce8f] Share a frozen PageSpeed report with your developer or agency
