# The Ultimate Guide to Web Performance

source_id: 1ket4M_Zd7LiPyCcX37SEQ5RN_x2S_kxi  |  folder: /08-SPD-speed  |  cards: 9  |  words: 1993  |  type: transcript (YouTube video)
credibility: Fireship, a developer education YouTube channel that sells a Pro membership (fireship.io). Aimed at web developers, not store operators. Evidence: definitions of Google's metrics, a demo of the Web Vitals Chrome extension on fireship.io, and quick Unlighthouse runs on Amazon, Google, Reddit and Astro. No controlled tests or client data.
date signals: Uses First Input Delay (FID) as a Core Web Vital, so it predates INP replacing FID (2024). Calls the Web Vitals extension "just released" and "new". Names Next.js, React lazy, Qwik, Partytown, Firebase, Vercel.

## 1. What this source is for

Use it for developer-level fixes and tools behind the 3 original Core Web Vitals: how to find the LCP bottleneck (network waterfall, Web Vitals extension), how to speed up LCP (compress, fewer fonts, CDN, no render-blocking JS, preload, fetchpriority), how to cut interaction delay (less JS on the main thread: Web Workers with Partytown, lazy loading), how to stop CLS (width and height, CSS `aspect-ratio`, `srcset`), and how to audit every page of a large site at once with Unlighthouse.

## 2. Principles

1. **Initial page load performance loses or makes money.** People want instant gratification; if the site is slow, they bounce. No number given. [a2d2451f8d9f]
2. **LCP measures loading.** Time to render the largest image or text block. First contentful paint comes first; LCP when the big images and videos arrive. Good within 2.5 s; beyond 4 s is bad and "will likely have an impact on" SEO. [a2d2451f8d9f]
3. **FID measures interactivity.** Time from a user's first interaction (for example a click) until the browser processes its event handlers. Good 100 ms or less; bad at 300 ms. "You don't want a website to render if the actual things on it don't work." The card notes FID is replaced by INP. [a2d2451f8d9f] [717cf5ec82fd]
4. **CLS measures visual stability.** Elements should not jump in unexpected ways. No numeric threshold given in this source. [a2d2451f8d9f]
5. **Render-blocking JavaScript before the main image delays LCP; avoid it "at all cost".** This is why server-side frameworks (Next.js) have gained favor over single-page apps (plain React), which must run a lot of JS before rendering main content. Condition: architecture choice; a rebuild, not a quick fix (card caveat). [cc2d433b9ede]
6. **Tell the browser what matters first.** Preload links make important assets be discovered first; `fetchpriority` high or low stops low-priority images at the bottom from loading before important ones. Do not mark everything high (card caveat). [958af3150188]
7. **The only way to improve interactivity is to cut JavaScript execution time**, but you cannot just delete JS; move it (Web Workers, Partytown) or lazy-load it (React lazy, Qwik). [717cf5ec82fd]
8. **Images must always have width and height, or CSS `aspect-ratio`.** For responsive images that change aspect ratio by viewport, use `srcset`. Ads injected into the page and over-ambitious animations also cause CLS. [3932af95de46]
9. **Use the fewest fonts needed.** Fonts are assets too. [cc2d433b9ede]
10. **Big sites need site-wide audits.** You cannot check hundreds or thousands of pages by hand; outlier slow pages hide. [08cf33a0563a]
11. **Scores are for triage.** Major sites averaged about 90 in the presenter's quick runs; a near-perfect marketing site is not a fair target for an image-heavy catalog (card's reading). [b906791efd1b]

## 3. Procedures

### 3.1 Find the LCP bottleneck with the waterfall
1. Open the page. Open DevTools > Network tab. [verify UI]
2. Reload and read the network waterfall.
3. Very wide bars are the bottlenecks.
4. Check whether the slowest asset is the largest rendered element (hero image, headline). [457e4a26802c]

### 3.2 Name the exact problem element with the Web Vitals extension
1. Install the Web Vitals Chrome extension (from the Chrome team). [verify UI]
2. Open its settings and turn on console logging. [verify UI]
3. Open the page and the browser console.
4. LCP log: names the element that is the LCP and breaks timing into subparts, such as time to first byte and element render delay.
5. CLS log: lists the DOM elements that shifted. Investigate each.
6. Click something: you get an interaction log (FID at the time of the video), then more logs for later interactions. [11d184a954ab] [web check: current extension features; Chrome may have moved these into DevTools]

### 3.3 Speed up LCP
1. Compress images; use modern formats such as WebP.
2. Load only the fonts the page needs.
3. Serve assets from a CDN. Hosts like Firebase or Vercel do this automatically.
4. Remove render-blocking JavaScript that runs before the main image shows.
5. Add a preload link for the critical asset.
6. Set `fetchpriority="high"` on the critical image and low on images far down the page.
7. Retest with Lighthouse or the extension. [cc2d433b9ede] [958af3150188]

### 3.4 Cut interaction delay
1. Measure (source: FID via the extension; card: measure INP and profile slow add-to-cart, variant and filter controls in current browser tools). [717cf5ec82fd]
2. Move third-party scripts to a Web Worker with Partytown. Card caveat: check each tool still works; not every script is compatible.
3. Lazy-load non-critical components (framework option, for example React lazy).
4. When rebuilding, frameworks like Qwik use "highly aggressive lazy loading" for instant interactivity.

### 3.5 Stop CLS
1. Add width and height to every image, or use CSS `aspect-ratio`.
2. For responsive images whose ratio changes by viewport, use `srcset` to serve different images.
3. Reserve space for injected ads; tone down animations that "try to do too much".
4. Measure with a Lighthouse report in Chrome DevTools or with the extension. [3932af95de46]

### 3.6 Audit every page with Unlighthouse
1. Create a new directory.
2. Run `npx unlighthouse --site <url>`.
3. A UI opens and shows results in real time. Lighthouse runs on every page in parallel; hundreds of pages take "a couple of minutes".
4. Find the outlier pages with very poor scores and fix them.
5. Optional: use the Unlighthouse SDK in your continuous integration pipeline.
6. Card caveats: can load a production server hard (use staging or throttle); verify flags in current docs; treat as triage and confirm key pages with field data. [08cf33a0563a] [verify UI]

## 4. Rules, thresholds and numbers

| rule | number or threshold | condition | source's basis | card id |
|---|---|---|---|---|
| LCP good | 2.5 s or less | loading | Google, as stated | [a2d2451f8d9f] |
| LCP bad | beyond 4 s; likely SEO impact | | Google, as stated | [a2d2451f8d9f] |
| FID good | 100 ms or less | first interaction; now replaced by INP | Google, as stated | [a2d2451f8d9f] |
| FID bad | 300 ms | | Google, as stated | [a2d2451f8d9f] |
| CLS | no number given | | | [3932af95de46] |
| Unlighthouse speed | hundreds of pages in a couple of minutes | parallel runs | presenter | [08cf33a0563a] |
| Major sites' score | around 90 average | presenter's quick runs | observation | [b906791efd1b] |
| Hook | "next five seconds" attention | opener, not a benchmark | rhetoric | none |

## 5. Diagnostics and checks

| check | how | good | bad | next |
|---|---|---|---|---|
| LCP bottleneck | Network waterfall | no single very wide bar before the main content | wide bars on hero or scripts | 3.3 |
| LCP element and subparts | Web Vitals extension console | element known; TTFB and render delay small | large render delay | preload, fetchpriority, remove blocking JS |
| Shifting elements | extension CLS log; Lighthouse | none listed | images without size, ads, animations | 3.5 |
| Interaction delay | extension logs (FID then; INP now) | 100 ms or less (FID) | 300 ms or more | 3.4 |
| Outlier pages | Unlighthouse | all pages similar | a few pages far worse | fix outliers |
| SPA rendering | view page with JS off or check render order | main content in server HTML | content waits on JS | consider SSR at rebuild time |

## 6. Tools, settings and named features

- Chrome DevTools Network tab waterfall; Lighthouse in DevTools. [verify UI]
- Web Vitals Chrome extension: console logging setting, LCP element and subparts, CLS elements, interaction logs. [verify UI]
- Unlighthouse: `npx unlighthouse --site <url>`, real-time UI, SDK for CI. [verify UI]
- HTML: `<link rel="preload">`, `fetchpriority="high"` / `"low"`, `srcset`, `width` / `height`.
- CSS: `aspect-ratio`.
- Partytown: moves third-party scripts to a Web Worker.
- Frameworks: Next.js (server-side rendering), React (SPA, React lazy), Qwik.
- Hosting with built-in CDN: Firebase, Vercel.
- Image format: WebP.

## 7. Examples and case results

Observations from quick runs, not benchmarks.
- Amazon: did "quite well" on Unlighthouse despite many images, but the extension showed many CLS issues.
- Google: performed very well.
- Reddit and other major sites: average around 90.
- astro.build: almost perfect 100s.
- fireship.io: most pages great, a few unexpected pages very poor, found only through the site-wide audit.

## 8. Mistakes the source warns about

- Running JavaScript before the main image can display. [cc2d433b9ede]
- Single-page apps that need a lot of JS before main content. [cc2d433b9ede]
- Images without dimensions. [3932af95de46]
- Injected ads and animations that do too much. [3932af95de46]
- Loading more fonts than needed. [cc2d433b9ede]
- Checking only a few pages on a large site. [08cf33a0563a]

## 9. Caveats, conflicts and what is missing

- Developer audience; examples are not ecommerce. Store mapping (PDP image, add to cart, filters) comes from the cards, not the video.
- FID is outdated; INP replaced it (card editorial). [717cf5ec82fd] [web check: current INP thresholds]
- No CLS number given here (other sources give 0.1).
- `fetchpriority` and preload syntax should be checked against current browser support (card caveat). [958af3150188]
- Over-preloading can make things worse (card caveat, not in source).
- Switching from SPA to server rendering is a rebuild.
- No platform steps for Shopify or WordPress.

## 10. Card index

- [a2d2451f8d9f] Understand the Three Core Web Vitals and Their Thresholds
- [457e4a26802c] Diagnose LCP Bottlenecks with the Network Waterfall
- [cc2d433b9ede] Optimize LCP: Compress, Serve via CDN, Unblock Rendering
- [958af3150188] Make the LCP Element Explicit with Preload and Fetchpriority
- [717cf5ec82fd] Reduce product-page interaction delay by cutting JavaScript execution
- [3932af95de46] Prevent CLS with Explicit Image Dimensions and aspect-ratio
- [11d184a954ab] Use the Web Vitals Chrome Extension to Name the Exact Problem Element
- [08cf33a0563a] Run Site-Wide Audits in Parallel with Unlighthouse
- [b906791efd1b] Use Lighthouse Scores to Triage, Not to Judge Vendors
