# ORG rooms: what they show that common tools do not

## Organic and content
Ties every post to the order it produced, by SKU and hook, using the post's own UTM tag or promo code. Metricool, Later, Hootsuite and Sprout Social show reach and engagement, and Hootsuite and Sprout add social listening, but none join a post to a matched order, flag a viral-but-not-selling post against the brand's own order floor, or run a claims and safety gate before publish. The room also tracks creator seeding cost and content yield against the same tagged asset library the calendar draws from, and tracks an asset's reuse across PDP, email, DM and post-purchase flow, which no scheduler does.

Hardest data: revenue joined to a specific post (needs UTM or promo-code discipline on every link), a claims-gate log (must be built, not pulled from a platform), and a WhatsApp/Discord roster matched to orders by phone or email.

## SEO
Computes organic revenue from the store's own order ledger, not GA4's own model; Search Console gives clicks, impressions, CTR and position only, never revenue. The refresh backlog is sequenced by revenue at risk, not traffic alone the way Semrush or Ahrefs audits do. The technical audit checks AI-crawler access (GPTBot, PerplexityBot, Google-Extended) alongside classic crawl health, which Screaming Frog does not do, and flags a discontinued page that 404s instead of redirecting, tied to the product feed.

Hardest data: a reliable GA4-session-to-order join (most stores never wire this), page-level revenue history to rank the refresh backlog, and a maintained AI-crawler robots.txt snapshot.

## Answer engines
Closes the loop that AI-visibility trackers (Semrush AI Toolkit, Ahrefs Brand Radar, Profound, Otterly) leave open: it re-checks a shipped correction on a fixed cadence to confirm the engine picked it up, scores fact consistency across site, schema, feed and directories before an engine asks, and checks what a shopping agent would tell a buyer about price and stock against the live feed, which no AI-visibility product does.

Hardest data: running the frozen prompt set itself (a scripted, repeatable pull per engine, not a one-off query), finding which third-party page an engine likely cites for a wrong fact, and building the agentic listing spot-check against the live feed.

## Files
- `ORG.rooms.json`: 3 rooms, JSON-validated.
- `ORG.rooms.md`: this file.
