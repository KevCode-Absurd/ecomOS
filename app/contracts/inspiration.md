# Inspiration layer: contract (S4.1, 28 Sep 2026)

The inspiration layer shows a founder or an agent outside references next to the brand's own work: what competitors and category leaders run, how public email programs are built, how landing pages are laid out, what creators post, how offers move. References are signals, never proven winners. Every reference carries the reason it is relevant to this brand, and that reason is computed in code from brain fields, never written by a model.

## 1. What a reference is

One record in `app/inspiration/<brand>/<domain>.json`:

```
{
  "id": "insp.<domain>.<source>.<hash>",
  "domain": "creative | email | landing | organic | offers | research",
  "source": "<registry source id>",
  "captured_at": "YYYY-MM-DD",
  "origin": {"brand": "Comrad Socks", "role": "competitor | leader | own", "url": "<public url>", "page_id": "<optional>"},
  "signals": {"format": "video", "hook_type": "first_person", "run_days": 41, "layout": "problem then proof", "offer_type": "bundle", "cadence_days": 3},
  "quote": "<at most 140 characters of public text as evidence, never the whole copy>",
  "media": {"kind": "image | video | page | none", "path": "<git-ignored local path or null>", "thumbnail": "<path or null>", "remote_url": "<signed or public url>", "expires": "YYYY-MM-DD or null", "rights": "reference_only | own_brand"},
  "relevance": {"score": 0.0, "reasons": [{"rule": "same_category", "brain_field": "identity.category", "match": "socks"}]},
  "tags": ["compression", "durability"],
  "notes": "<optional>"
}
```

Records validate against `app/inspiration/reference.schema.json` (S4.2a writes it from this shape). Text beyond the 140-character quote is never stored. Faces, logos and product shots from competitors are never cropped out for reuse.

## 2. Registry

`app/inspiration/registry.json` lists every source per domain: id, domain, kind (api, scrape, apify_actor, upload, manual), access (public, key, paid), what it yields, the puller that reads it, cost notes, and its fixture path. A source that needs a key or money is never called without a card and the Apify ledger caps from `app/contracts/connectors/apify.md`. Fixture mode is mandatory: every puller runs offline on saved items under `app/inspiration/fixtures/<source>/` and the fixture is what tests use.

## 3. Relevance, as code-able rules

Relevance is a score in 0 to 1 built from rules that read brain fields. Each rule adds a weight when its condition holds and writes one `reasons` entry naming the brain field and the matched value. No rule reads free text from a model.

| Rule | Condition on brain fields | Weight | Domains |
|---|---|---|---|
| same_category | reference tags share a term with `identity.category` or `products.lines` | 0.30 | all |
| same_avatar | reference tags share a pain or situation term with any `avatars` record | 0.20 | creative, organic, landing |
| same_offer_type | reference `signals.offer_type` matches an `offers` record type (bundle, first order code, free shipping threshold, guarantee, gift) | 0.20 | creative, email, offers, landing |
| same_price_band | reference price sits within 0.6 to 1.6 of the brand's `products.price_ladder` median for the matched line | 0.15 | email, offers, landing |
| same_calendar | reference date sits inside a `calendar` window the brand also runs (BFCM, holiday gifting, back to school) | 0.10 | email, creative, offers |
| same_margin_band | reference discount depth fits inside the brand's modelled gross margin minus red line (`economics.gross_margin_model`, `economics.red_line`) | 0.15 | offers |
| answers_objection | reference tags match an `objection_ladders` theme with 10 or more complaint quotes | 0.20 | creative, landing, email, research |
| competitor_in_frame | origin brand is in `competitors.competitor_frame` or a Reddit recommended-instead record | 0.10 | all |
| own_brand | origin role is own | shown always, score 1.0, rights own_brand | all |

Score is the capped sum. A reference under 0.3 is stored but not shown. Reasons render as a sentence built from a template per rule, for example "Same offer type: a 20 percent first-order code, like COMFORT20", never a model paraphrase.

## 4. Rights

- Own-brand references are stored in full (images, video, copy) and may feed generation.
- Competitor and leader references are reference_only: image, video thumbnail and remote url kept; shown to people for layout, mood, format and cadence; never passed to a generation call, a copy call or a creative brief as an asset. The generation boundary checks `media.rights` and refuses reference_only files. A test proves the refusal.
- Public text is kept as a quote of at most 140 characters as evidence. Full ad copy, email bodies and page copy are never stored.
- Reddit and review text is never a testimonial. Usernames are never stored.
- Media links from platforms expire, so media downloads at pull time into `app/inspiration/media/` (git-ignored); a reference whose media is gone reads media kind none, never a broken image.
- A brand can delete every reference about it in one call (`--purge <origin brand>`), for takedown requests.

## 5. Domains and sources (summary; the registry is the source of truth)

| Domain | Sources | Kept | Puller |
|---|---|---|---|
| creative | Meta Ad Library by page id (Apify, existing connector), TikTok Creative Center top ads (public), own ad account | format, hook type, run length, platforms, promo, media | S4.2a |
| email | Milled and ReallyGoodEmails public archives, own Klaviyo, competitor sign-up inbox (a dedicated mailbox, manual) | cadence, subject pattern, structure, offer pattern, send day | S4.2b |
| landing | competitor PDPs and landers (polite crawl of public pages), Baymard-style public galleries, own site | section order, proof types, offer placement, above-the-fold elements | S4.2c |
| organic | creator and brand posts with public metrics (Instagram, TikTok, YouTube public pages), Reddit threads (via the existing Apify lane) | format, hook, series, cadence, engagement band | S4.2d |
| offers | competitor promos over time from the Ad Library pull and site crawls, Amazon listing prices | thresholds, bundle math, guarantee wording, discount depth by calendar | S4.2a plus offers extractor |
| research | reviews, Reddit, search demand (public autocomplete and trends pages) | unmet needs, language, questions | existing brain extractors, re-read as references |

## 6. UI (S4.3)

One kit component, `inspiration-block`: a horizontal strip of references for the screen's domain, each card with the thumbnail or a format glyph, origin brand and role, 2 signal chips, the relevance sentence and a rights note ("reference only" or "yours"). A "why this" toggle shows the rules that fired. No decision row on a reference; the decision row belongs to the proposal that cites it. Shown on creative, copy, landing pages and email first.

## 7. Freshness

Creative and offers refresh weekly from the Ad Library pull already scheduled by the keeper. Email and landing refresh monthly. Organic refreshes weekly. A reference older than 90 days is shown faded and dropped at 180 unless it is a long runner (run_days over 60), which is kept as a durable signal.

## 8. Decisions taken here

- Relevance is rules on brain fields, not embeddings, so the reason is always explainable and the layer works with no model call.
- Media is kept (decided with Kevin on 28 Sep) with the rights split above, enforced at the generation boundary in code.
- One registry for all domains, so the keeper can offer sources the same way it offers connectors.
