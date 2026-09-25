---
name: technical-crawl-audit
owner: ORG
version: 1
invoke_when: quarterly
inputs: live site URL, prior audit baseline, robots.txt/CDN settings, Site's speed baseline
outputs: prioritized fix list with evidence, an AI-crawler access report, a speed hand-off note to Site
---
# Technical SEO and AI-crawlability audit

## Purpose
Find and prioritize the technical floor a site needs before any content work matters: indexing, canonicals, sitemap, robots.txt, redirects, heading structure, and whether AI crawlers can even read the site, while handing anything speed-related to the Site specialist rather than re-doing that work here.

## Steps
1. Crawl the whole site with mobile and JS rendering for indexing, canonical, sitemap, robots and heading-structure problems.
2. Check AI-bot access explicitly (GPTBot, PerplexityBot, Google-Extended) against robots.txt and CDN bot rules; this is not covered by a classic crawl.
3. Log a speed baseline from the existing instrument without diagnosing or fixing it here.
4. Order findings with the technical floor first.
5. Attach verifiable evidence to every finding: URL, response code, screenshot or quoted setting.
6. Split findings into ones this agent can brief directly and speed items that go to Site with a developer-brief hand-off note.
7. Package the prioritized fix list and hand-off note.

## Checks
- Every finding has verifiable evidence.
- AI-crawler access checked explicitly.
- Speed items only handed off, never fixed here.

## Output
{fix_list[], ai_crawler_access_report, speed_handoff_note}

## Example
Finding: "12 product pages return a soft-404 with 200 status", evidence: 12 URLs with screenshot, priority: technical floor, fixed by a canonical/redirect brief; a slow LCP finding is handed to Site instead of diagnosed further here.
