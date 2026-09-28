"""Products and research audit (screen 01, round 0). Findings in the shape of app/contracts/audit.md.

Sales numbers come from app/metrics.py (`units`, `product_net_sales` from products_monthly). Review
numbers come from the brand brain: the `products.reviews_*` records (public own-site review totals) and
the `objection_ladders` records that were built from them. No connector, no model call. Same tables,
same brain and same window give the same findings, byte for byte.

A line is a SKU title without its pack size (metrics.product_line). The trend window is the last 3
whole months before the window end, against the same 3 months a year earlier, so season does not
read as trend.

Rules
  PROD-R01  Declining line: a line whose units fell on last year over the last 3 whole months, or
            whose unit growth trails the whole store's by 1 point or more, so it is losing share of
            what the store sells. Money: (store growth - line growth) x the line's units a year ago
            x its net sales per unit now: the net sales it would have made had it kept its share.
            Agreement: each of the 3 months where the line also trailed the store. Capability
            PROD-C05 (read trend and saturation together, agent does). Owner: 01-market-research.
  PROD-R02  Review issue: a line whose share of 1 and 2 star reviews is 10 percent or more and at
            least 1.5 times the median across the brand's reviewed lines. Money: the line's net
            sales in the last whole month x (its low-star share - the median share): sales that
            went out into the extra bad experiences. Evidence carries the top issues and the
            objection ladder rungs built from the same reviews. Capability PROD-C06 (sharpen the
            line and its angle, agent does). Owner: 01-market-research; 04-offers reads the ladder.

  PROD-R04  Category behind its market: a category whose 12-month unit growth is below the public growth a
            year of its market in the web pass fixture (fixtures/market_trends.json, url and date on every
            number). Money: (market growth - our growth) x our net sales 12 months. Confidence 0.3 (one
            window, peer baseline). Capability PROD-C05. Owner: 01-market-research.
  PROD-R05  Growing sub-category the brand sells and does not advertise: a market in the web pass growing 4
            percent a year or more (or the gift window, 1 Nov, inside 90 days) whose words appear in the
            brand's product, claim or site records and in none of its active-ad signals. Money: null.
            Capability PROD-C05 (agent does). Owner: 01-market-research.
  PROD-R06  Competitor-pushed lane we do not advertise: a lane (compression, merino, performance, guarantee
            proof, style drops, gifting, underwear, footwear, apparel, creator proof) that 2 or more competitor
            pages push in the Ad Library with at least one ad live 30 days or more, and that none of the
            brand's active-ad signals name. Sold or not, it is a gap. Money: null (signals, not proof).
            Capability PROD-C03 (scout ad libraries, agent does). Owner: 01-market-research.
  PROD-R07  Unanswered conversation theme: a review theme (from the objection ladders, plus Reddit mentions and
            the social keyword pull) with 10 or more quotes, more complaint than praise quotes, and no
            active-ad signal of ours that carries its answer words. Money: null (a test prices it).
            Capability PROD-C12 (hand the validated angle to creative, human assist; the desk drafts and a
            person approves). Owner: 01-market-research. Reputation override: 4 (a deal-breaker rung).
  PROD-R08  Preference gap: a shopper preference the web pass shows rising or holding (sustainability, natural
            fibres, durability, giving, made in USA, resale, compression, gifting) that at least one competitor
            page claims in its ads and none of the brand's own records (claims, products, site, offers) carries.
            Money: null. Capability PROD-C05. Owner: 01-market-research. The action is a claim plan or a
            counter-position; a claim is never invented.
  PROD-R09  Positioning frame gap: Reddit frames the category with a proof word (buy it for life, worth the
            price) in 3 or more posts and never names the brand in it, a competitor is recommended instead,
            and the brand's active ads carry proof in a smaller share of hook types than the median
            competitor page with a price band. One finding for the brand, severity high (a competitor
            position gap named in the brain). Money: null. Capability PROD-C06. Owner: 01-market-research.
  PROD-R10  Avatar not served: an avatar record in the brain with no evidence quote or record that names a line
            we sell, while at least one competitor page pitches to them (2 or more of the avatar's words in its
            pitch). Money: null. Capability PROD-C01 (screen the candidate, agent does). Owner: 01-market-research.
  PROD-R11  Avatar under-served: an avatar with a share estimate of 10 percent or more (or high intensity) whose
            theme (from its own words) is complaint-led in the objection ladders. Money: share_estimate x
            28-day net revenue x complaint share of the theme's quotes, the revenue sitting with buyers whose
            main doubt goes unanswered, times the 12-month repeat rate (the repeat revenue at risk). Severity by
            the stake ladder, capped at high (a structural gap, not a break in the buy path). Capability PROD-C12. Owner:
            01-market-research. Satisfaction override: 4 (a review theme in a deal-breaker rung).
  PROD-R12  Search data not connected: one unavailable finding while the search_console table is absent, so the
            brand and category term groups show demand as unavailable, never 0. Owner: 01-market-research.
  PROD-R13  Term group without a page: a term group (brand, category, competitor, problem) with impressions in
            the last 28 days of Search Console and no url in the brain's site map whose path carries the group's
            page words. Only runs when the data is there. Money: null. Capability PROD-C05. Owner: 01-market-research.
  PROD-R14  Candidate stalled: a pipeline candidate whose days since screen-in exceed its time box and whose stage
            is not go or killed. Severity low (hygiene), confidence 0.9. Capability PROD-C04. Owner: 01-market-research.
  PROD-R15  Demand screen failed: a candidate with 2 or more of the 3 fast checks (demand, competition, store fit)
            failed and still open. Capability PROD-C01. Owner: 01-market-research.
  PROD-R16  Margin gate failed: an open candidate with a planned price whose modelled contribution margin,
            (price - landed cost - donated item - fulfilment - payment fee) / price, every term from the candidate,
            the finance inputs or the brain, is below finance_inputs.target_contribution_margin. Landed cost is
            the entered estimate, else the median of single-unit SKUs in the category. Capability PROD-C08.
  PROD-R17  Actual margin unavailable: contribution_margin by SKU needs order rows joined to landed costs; one
            connect finding while the store is not connected. Capability PROD-C08. Owner: 01-market-research.
  PROD-R18  Seasonal without a cash plan: a candidate whose demand pattern reads seasonal (the category's top 2
            months carry 25 percent or more of 12-month units, or the name says gift) and whose cash_plan is empty.
            Trending reads from market growth of 8 percent a year or 3 launches in 24 months; else evergreen.
            Capability PROD-C07 (classify demand pattern and plan cash, agent does). Owner: 01-market-research.
  PROD-R19  Growing but full: a lane whose trend score ((market growth - 4) / 6 clamped, plus 0.1 per launch by
            another brand in 24 months, up to 0.3) is 0.3 or more and whose sellers (competitor pages pushing it
            plus those launches) number 5 or more, the red rung of the bank's PRD-052 ladder. Severity low.
            Capability PROD-C05. Owner: 01-market-research.
  PROD-R20  Sustained spend found: a product lane where 3 or more competitor pages keep an ad live 90 days or
            more (a funded test, bank idea PRD-023) and the pipeline holds no open candidate whose name or angle
            sits on the lane. Capability PROD-C03 (scout ad libraries, agent does). Owner: 01-market-research.
  PROD-R21  Review price gap: the median of per-pair price mentions in review quotes (Amazon, the brand site,
            Trustpilot, retailers; 3 to 60 dollars; never Reddit) against an open sock candidate's planned price per
            unit in its pack; fires when the plan is more than 15 percent above the median. Capability PROD-C04.
  PROD-R22  Unresolved listing complaint: an Amazon listing of the brand with 20 or more mined reviews whose top
            complaint theme (general left out) is over 15 percent of the mined reviews. The complaint is the gap to
            build the next angle on. Capability PROD-C31 (mine reviews for opportunity, agent does). Owner: 01-market-research.
  PROD-R23  Angle missing: a candidate at researched or later with an empty angle. Angle confidence is 0 to 3: filled,
            names a source (review, Reddit, web pass, finding, teardown, field), and not a competitor's own claim (3 or
            more distinctive words shared with one competitor's pitch reads as theirs). Capability PROD-C06.
  PROD-R24  Compliance gate incomplete: a candidate that passed 2 or more of the 5 go-live gates (provable claim, owned
            difference, brand threshold, contribution margin, ad-cost ceiling: contribution an order against
            target_cac) while labelling and category certification have not run. Capability PROD-C10.
  PROD-R25  Shortlist review due: an open candidate whose review date (set on the memo, or 14 days after the window
            end by default) is on or before the window end. The scorecard scores demand, margin, differentiation,
            compliance and cash timing 0 to 5 in code with the brand's weights (learnings.shortlist_weights, else
            30, 30, 20, 10, 10). Capability PROD-C11 (go or no-go memo, founder gate). Owner: 01-market-research.
  PROD-R26  Single-source video signal: a lane with an open candidate where demand shows on exactly one platform
            (5 or more Instagram posts on the lane tag, 3 or more Reddit mentions, or a competitor page running
            creator-style ads). One platform's demand is a lead, not proof (bank idea PRD-022). Severity low.
            Capability PROD-C02 (validate demand on video-commerce platforms, agent does). Owner: 01-market-research.
  PROD-R27  Spec missing: a candidate at gated or later whose newest tech pack lacks tolerances, a BOM or a packaging
            cost line, or has none. Packs are versioned on the candidate (tech_packs, newest last). Capability
            PROD-C13 (build tech packs, BOMs and packaging specs, agent does). Owner: 01-market-research.
  PROD-R28  Research sprawl: an open candidate whose hours logged pass the hours allowed through its stage (the per-stage
            budgets summed: 4 screened, 16 researched, 8 gated, 4 shortlisted by default; a brand sets its own in
            learnings.research_hours_budget). Severity low. Capability PROD-C04. Owner: 01-market-research.
  PROD-R29  Trend without history: a lane with an open candidate whose market series in the web pass holds no 3 years
            of history (forecast only, or none), or whose last-year growth is more than twice its multi-year rate
            (a spike). Bank ideas PRD-044 and PRD-045. Severity low. Capability PROD-C05. Owner: 01-market-research.
  PROD-R30  Surface with reach and no presence: a place the category conversation runs (a subreddit in the Reddit pull,
            a review source in the ladders, a social surface) with reach at or over the floor (20 quotes or 1,000 upvotes
            for a forum, 30 quotes for a review source, 50 posts for a social pull) and no channel, identity, site map,
            marketplace, offer or policy record naming the brand there. Severity medium; high at 10,000 upvotes. Money
            null. Capability PROD-C12 (field research discipline, human assist). Owner: 01-market-research.
  PROD-R31  Brand not the seller on Amazon: the presence record says no offer read was sold by the brand and no brand
            store showed. Severity high. Money null (reseller sales are not in our orders). Capability PROD-C29 (Brand
            Registry and brand protection, human assist). Owner: 01-market-research.
  PROD-R32  Listing price spread: an Amazon listing with 20 or more ratings whose price per pair (listing price over the
            pairs named in the title) is 25 percent or more off the site per-pair price either way. Severity medium.
            Money null. Capability PROD-C46 (monitor reseller pricing and MAP, agent does). Owner: 01-market-research.
  PROD-R33  Lane in play with none of ours: a lane we sell where competitors launched 2 or more times over 12 months (or
            2 or more brands over 24) and nothing of ours launched there in 24 months, from the web pass launches (a url
            and a date each). Severity medium. Money null. Capability PROD-C06 (extend the line, agent does). Owner:
            01-market-research.
  PROD-R34  Line returning at 1.5 times the store median rate on 20 or more returns over 12 whole months (units from
            order line items, returns from the return leg of reversed orders), with the reasons. Room metric
            sku_return_rate. Severity medium. Money null (refund value is not in the orders table). Capability PROD-C06.
            Owner: 01-market-research.
  PROD-R35  Open question for the founder (brain open_questions) with 5 or more complaint quotes behind it, never asked or
            asked 14 or more days ago with no answer. Severity medium at 20 quotes, else low. Money null (priced on the
            theme card). Capability PROD-C12 (field research, human assist). Owner: 01-market-research.
  PROD-R36  Pull due: a pull this desk reads (Reddit, Amazon reviews, Ad Library, listings, the seller of record, Instagram,
            the web pass) whose last capture is older than its window, or that never ran, stands on a mock file, or has no
            actor set. Severity medium for due or mock, else low. Money null. Every run is a paid call a person approves
            under the brand's caps. Capability PROD-C04. Owner: 01-market-research.
  PROD-R37  First run at full MOQ: a candidate at gated or later with no first production run on file, or a first run whose
            cash is 25 percent or more of 28-day net revenue (or revenue unknown), or whose format MOQ is above the units
            wanted, with no lower-MOQ alternative noted. Money: the first run cash. Bank idea BRD-249. Severity medium.
            Capability PROD-C07 (demand pattern and cash timing, agent does). Owner: 01-market-research.
  PROD-R38  Override without a reason: an open candidate carried past screening with a failed fast check, or past gated with
            a failed compliance line, whose log holds no line naming the reason (bank idea PRD-113). Severity medium. Money
            null. Capability PROD-C04. Owner: 01-market-research.
  PROD-R39  Trend alone: a candidate tagged trending at gated or later with no evergreen line in the store and no evergreen
            candidate open beside it (bank idea PRD-047). Severity medium. Money null. Capability PROD-C07. Owner:
            01-market-research.
  PROD-R40  Order-by date: a seasonal candidate at gated or later whose order must go in inside 30 days (peak month less
            the lead time less 14 days of safety) or already passed, with no first run decided; or whose lead time is not
            on file (candidate field, else learnings.lead_time_days, else an operations record). High when the date is
            inside the window, medium when the lead time is missing. Capability PROD-C07. Owner: 01-market-research.
  PROD-R41  Stale brain section: a section this desk reads that is past its contract TTL (brand-brain.md), holds stale
            records, or has an open conflict waiting on the founder (medium; else low). Money null. Capability PROD-C04.
            Owner: 01-market-research.
  PROD-R42  Unconfirmed assumption: a calibration assumption (assumptions.json) that a money rule here prices with, whose
            status is sourced, derived or modelled rather than founder. Severity low. Money null. Capability PROD-C08
            (product economics, agent does; the confirmation is the founder's). Owner: 01-market-research.
  PROD-R03  Hero line with no next SKU: a line with 25 percent or more of its category's net sales in
            the last 3 whole months while the candidate pipeline holds no open next-SKU candidate for
            that category. Money: null (an unlaunched SKU has no baseline). Capability PROD-C06
            (extend the line and sharpen the angle, agent does). Owner: 01-market-research.

Money uses net sales, not margin. Review counts are public and real; sales are simulated.
"""
import importlib.util
import json
import re
import statistics
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
APP = HERE.parents[1]
SCREEN = '01-market-research'

TREND_MONTHS = 3
SHARE_GAP_POINTS = 1.0
LOW_STAR_FLOOR = 0.10
LOW_STAR_TIMES_MEDIAN = 1.5
HERO_SHARE = 0.25  # a line with this share of its category's net sales is a hero

RULES = [
    {'rule_id': 'PROD-R01', 'name': 'Line units down on last year, or growing 1 point or more slower than the store',
     'entity_type': 'sku', 'inputs': ['products_monthly', 'products'], 'capability': 'PROD-C05', 'owner_screen': SCREEN},
    {'rule_id': 'PROD-R02', 'name': 'Line with 10 percent or more 1 and 2 star reviews, 1.5 times the brand median',
     'entity_type': 'sku', 'inputs': ['brain.products.reviews_*', 'brain.objection_ladders', 'products_monthly'],
     'capability': 'PROD-C06', 'owner_screen': SCREEN},
    {'rule_id': 'PROD-R03', 'name': 'Hero line with 25 percent or more of its category and no next SKU in the pipeline',
     'entity_type': 'sku', 'inputs': ['products_monthly', 'products', 'fixtures.pipeline'], 'capability': 'PROD-C06',
     'owner_screen': SCREEN},
    {'rule_id': 'PROD-R04', 'name': 'Category units growing slower than its public market growth a year (web pass)',
     'entity_type': 'sku', 'inputs': ['products_monthly', 'fixtures.market_trends'], 'capability': 'PROD-C05', 'owner_screen': SCREEN},
    {'rule_id': 'PROD-R05', 'name': 'Sub-category growing 4 percent a year or more (or the gift window within 90 days) that the brand sells and no active ad names',
     'entity_type': 'metric', 'inputs': ['fixtures.market_trends', 'brain.products', 'brain.learnings'], 'capability': 'PROD-C05', 'owner_screen': SCREEN},
    {'rule_id': 'PROD-R06', 'name': 'Lane 2 or more competitors push with an ad live 30 days or more, and no active ad of ours names it',
     'entity_type': 'metric', 'inputs': ['brain.competitors', 'brain.learnings', 'fixtures.market_trends'], 'capability': 'PROD-C03', 'owner_screen': SCREEN},
    {'rule_id': 'PROD-R07', 'name': 'Conversation theme with 10 or more review quotes, more complaints than praise, and no active ad answering it',
     'entity_type': 'ladder_rung', 'inputs': ['brain.objection_ladders', 'brain.language_bank', 'brain.claims', 'brain.learnings', 'fixtures.social_pull'],
     'capability': 'PROD-C12', 'owner_screen': SCREEN},
    {'rule_id': 'PROD-R08', 'name': 'Preference rising or holding in public surveys that competitors claim and no record of ours does',
     'entity_type': 'metric', 'inputs': ['fixtures.market_trends', 'brain.claims', 'brain.competitors', 'brain.learnings'], 'capability': 'PROD-C05', 'owner_screen': SCREEN},
    {'rule_id': 'PROD-R09', 'name': 'Category framed by a proof word on Reddit (3 or more posts, brand never named), a competitor recommended instead, and our proof share of hooks below the competitor median',
     'entity_type': 'brand', 'inputs': ['brain.positioning', 'brain.competitors', 'brain.learnings', 'products'], 'capability': 'PROD-C06', 'owner_screen': SCREEN},
    {'rule_id': 'PROD-R10', 'name': 'Avatar in the brain with no record or quote tying them to a line we sell, while a competitor pitches to them',
     'entity_type': 'brand', 'inputs': ['brain.avatars', 'brain.products', 'brain.competitors'], 'capability': 'PROD-C01', 'owner_screen': SCREEN},
    {'rule_id': 'PROD-R11', 'name': 'Avatar with 10 percent or more of buyers (or high intensity) whose theme is complaint-led; money = share x 28-day net revenue x complaint share',
     'entity_type': 'brand', 'inputs': ['brain.avatars', 'brain.objection_ladders', 'daily', 'brain.learnings'], 'capability': 'PROD-C12', 'owner_screen': SCREEN},
    {'rule_id': 'PROD-R12', 'name': 'Search Console not connected: search demand for the brand and the category cannot be read',
     'entity_type': 'brand', 'inputs': ['search_console'], 'capability': 'PROD-C05', 'owner_screen': SCREEN},
    {'rule_id': 'PROD-R13', 'name': 'Term group with impressions in 28 days and no answering page in the site map',
     'entity_type': 'page', 'inputs': ['search_console', 'google_rows', 'brain.site_map', 'brain.objection_ladders'], 'capability': 'PROD-C05', 'owner_screen': SCREEN},
    {'rule_id': 'PROD-R14', 'name': 'Candidate past its research time box with no decision', 'entity_type': 'sku', 'inputs': ['fixtures.pipeline'], 'capability': 'PROD-C04', 'owner_screen': SCREEN},
    {'rule_id': 'PROD-R15', 'name': 'Candidate that failed 2 or more of the 3 fast checks (demand, competition, store fit) and is still open', 'entity_type': 'sku', 'inputs': ['fixtures.pipeline'], 'capability': 'PROD-C01', 'owner_screen': SCREEN},
    {'rule_id': 'PROD-R16', 'name': 'Open candidate whose modelled contribution margin is below the brand floor', 'entity_type': 'sku',
     'inputs': ['fixtures.pipeline', 'finance_inputs', 'brain.economics', 'monthly'], 'capability': 'PROD-C08', 'owner_screen': SCREEN},
    {'rule_id': 'PROD-R17', 'name': 'Actual contribution margin by SKU unavailable (needs order rows joined to landed costs)', 'entity_type': 'metric',
     'inputs': ['orders', 'order_lines', 'finance_inputs'], 'capability': 'PROD-C08', 'owner_screen': SCREEN},
    {'rule_id': 'PROD-R18', 'name': 'Seasonal candidate (top 2 months carry 25 percent of the category, or a gift by name) with no cash plan attached', 'entity_type': 'sku',
     'inputs': ['fixtures.pipeline', 'products_monthly', 'fixtures.market_trends'], 'capability': 'PROD-C07', 'owner_screen': SCREEN},
    {'rule_id': 'PROD-R19', 'name': 'Lane growing (trend score 0.3 or more) with 5 or more sellers: growing, but full', 'entity_type': 'metric',
     'inputs': ['fixtures.market_trends', 'brain.competitors'], 'capability': 'PROD-C05', 'owner_screen': SCREEN},
    {'rule_id': 'PROD-R20', 'name': 'Product lane with 3 or more advertisers keeping an ad live 90 days or more and no open candidate on it', 'entity_type': 'metric',
     'inputs': ['brain.competitors', 'fixtures.pipeline'], 'capability': 'PROD-C03', 'owner_screen': SCREEN},
    {'rule_id': 'PROD-R21', 'name': 'Candidate planned more than 15 percent above the per-pair price reviewers say a pair is worth', 'entity_type': 'sku',
     'inputs': ['brain.language_bank', 'fixtures.pipeline'], 'capability': 'PROD-C04', 'owner_screen': SCREEN},
    {'rule_id': 'PROD-R22', 'name': 'Listing with 20 or more mined reviews whose top complaint is over 15 percent of them', 'entity_type': 'sku',
     'inputs': ['brain.products.amazon_*_issues', 'brain.products.amazon_*_praise', 'brain.marketplaces'], 'capability': 'PROD-C31', 'owner_screen': SCREEN},
    {'rule_id': 'PROD-R23', 'name': 'Candidate past screening with no stated point of difference', 'entity_type': 'sku', 'inputs': ['fixtures.pipeline', 'brain.competitors'], 'capability': 'PROD-C06', 'owner_screen': SCREEN},
    {'rule_id': 'PROD-R24', 'name': 'Candidate with 2 or more go-live gates passed and the compliance check not run', 'entity_type': 'sku',
     'inputs': ['fixtures.pipeline', 'finance_inputs', 'brain.products'], 'capability': 'PROD-C10', 'owner_screen': SCREEN},
    {'rule_id': 'PROD-R25', 'name': 'Open candidate whose scheduled review date has arrived', 'entity_type': 'sku', 'inputs': ['fixtures.pipeline'], 'capability': 'PROD-C11', 'owner_screen': SCREEN},
    {'rule_id': 'PROD-R26', 'name': 'Lane with an open candidate whose demand shows on exactly one platform (Instagram pull, Reddit, creator ads)', 'entity_type': 'metric',
     'inputs': ['fixtures.social_pull', 'brain.language_bank', 'brain.content', 'fixtures.pipeline'], 'capability': 'PROD-C02', 'owner_screen': SCREEN},
    {'rule_id': 'PROD-R27', 'name': 'Candidate at gated or later with no current versioned spec (tolerances, BOM, packaging cost)', 'entity_type': 'sku',
     'inputs': ['fixtures.pipeline'], 'capability': 'PROD-C13', 'owner_screen': SCREEN},
    {'rule_id': 'PROD-R28', 'name': 'Open candidate whose research hours pass the cumulative hours budget for its stage', 'entity_type': 'sku',
     'inputs': ['fixtures.pipeline', 'brain.learnings'], 'capability': 'PROD-C04', 'owner_screen': SCREEN},
    {'rule_id': 'PROD-R29', 'name': 'Candidate lane whose market trend rests on a forecast or one year, with no 3-year history on file, or reads as a spike', 'entity_type': 'metric',
     'inputs': ['fixtures.market_trends', 'fixtures.pipeline'], 'capability': 'PROD-C05', 'owner_screen': SCREEN},
    {'rule_id': 'PROD-R30', 'name': 'Surface where the category conversation has reach (forum, review source or social) and no record shows the brand present', 'entity_type': 'metric',
     'inputs': ['brain.language_bank', 'brain.objection_ladders', 'brain.channels', 'brain.identity', 'brain.site_map', 'fixtures.social_pull'], 'capability': 'PROD-C12', 'owner_screen': SCREEN},
    {'rule_id': 'PROD-R31', 'name': 'Brand is not the seller of record and holds no brand store on its own Amazon listings', 'entity_type': 'brand',
     'inputs': ['brain.marketplaces'], 'capability': 'PROD-C29', 'owner_screen': SCREEN},
    {'rule_id': 'PROD-R32', 'name': 'Amazon listing with 20 or more ratings priced 25 percent or more off the site per-pair price', 'entity_type': 'sku',
     'inputs': ['brain.marketplaces', 'brain.products', 'products'], 'capability': 'PROD-C46', 'owner_screen': SCREEN},
    {'rule_id': 'PROD-R33', 'name': 'Lane we sell where competitors launched 2 or more times in 12 months (or 2 brands in 24) and none of ours in 24 months', 'entity_type': 'metric',
     'inputs': ['fixtures.market_trends', 'brain.products'], 'capability': 'PROD-C06', 'owner_screen': SCREEN},
    {'rule_id': 'PROD-R34', 'name': 'Line returning at 1.5 times the store median rate on 20 or more returns in 12 months', 'entity_type': 'sku',
     'inputs': ['orders', 'reversed_orders', 'products'], 'capability': 'PROD-C06', 'owner_screen': SCREEN},
    {'rule_id': 'PROD-R35', 'name': 'Open question for the founder with 5 or more complaint quotes behind it, never asked or unanswered 14 days', 'entity_type': 'ladder_rung',
     'inputs': ['brain.open_questions', 'brain.objection_ladders'], 'capability': 'PROD-C12', 'owner_screen': SCREEN},
    {'rule_id': 'PROD-R36', 'name': 'Pull the desk reads that is due, never run, mock, or has no actor set', 'entity_type': 'metric',
     'inputs': ['brain.*.source', 'brain.config.apify', 'fixtures.market_trends', 'fixtures.social_pull'], 'capability': 'PROD-C04', 'owner_screen': SCREEN},
    {'rule_id': 'PROD-R37', 'name': 'Candidate at gated or later with no first run on file, or a full-MOQ first run with no lower-MOQ alternative noted', 'entity_type': 'sku',
     'inputs': ['fixtures.pipeline', 'daily'], 'capability': 'PROD-C07', 'owner_screen': SCREEN},
    {'rule_id': 'PROD-R38', 'name': 'Candidate carried past a failed check or gate with no override reason in its log', 'entity_type': 'sku',
     'inputs': ['fixtures.pipeline'], 'capability': 'PROD-C04', 'owner_screen': SCREEN},
    {'rule_id': 'PROD-R39', 'name': 'Trending candidate at gated or later with no evergreen line or candidate beside it', 'entity_type': 'sku',
     'inputs': ['fixtures.pipeline', 'products_monthly', 'fixtures.market_trends'], 'capability': 'PROD-C07', 'owner_screen': SCREEN},
    {'rule_id': 'PROD-R40', 'name': 'Seasonal candidate whose order-by date is inside 30 days or past with no first run, or whose lead time is not on file', 'entity_type': 'sku',
     'inputs': ['fixtures.pipeline', 'products_monthly', 'brain.learnings', 'brain.operations'], 'capability': 'PROD-C07', 'owner_screen': SCREEN},
    {'rule_id': 'PROD-R41', 'name': 'Brain section this desk reads that is past its TTL, holds stale records, or has an open conflict', 'entity_type': 'brand',
     'inputs': ['brain.freshness', 'brain.review.conflicts'], 'capability': 'PROD-C04', 'owner_screen': SCREEN},
    {'rule_id': 'PROD-R42', 'name': 'Calibration assumption a money rule prices with that the founder has not confirmed', 'entity_type': 'brand',
     'inputs': ['brain.assumptions'], 'capability': 'PROD-C08', 'owner_screen': SCREEN},
]
CAPABILITY = {'PROD-R01': {'id': 'PROD-C05', 'autonomy': 'agent_does'},
              'PROD-R02': {'id': 'PROD-C06', 'autonomy': 'agent_does'},
              'PROD-R03': {'id': 'PROD-C06', 'autonomy': 'agent_does'},
              'PROD-R04': {'id': 'PROD-C05', 'autonomy': 'agent_does'},
              'PROD-R05': {'id': 'PROD-C05', 'autonomy': 'agent_does'},
              'PROD-R06': {'id': 'PROD-C03', 'autonomy': 'agent_does'},
              'PROD-R07': {'id': 'PROD-C12', 'autonomy': 'human_assist'},
              'PROD-R08': {'id': 'PROD-C05', 'autonomy': 'agent_does'},
              'PROD-R09': {'id': 'PROD-C06', 'autonomy': 'agent_does'},
              'PROD-R10': {'id': 'PROD-C01', 'autonomy': 'agent_does'},
              'PROD-R11': {'id': 'PROD-C12', 'autonomy': 'human_assist'},
              'PROD-R12': {'id': 'PROD-C05', 'autonomy': 'agent_does'},
              'PROD-R13': {'id': 'PROD-C05', 'autonomy': 'agent_does'},
              'PROD-R14': {'id': 'PROD-C04', 'autonomy': 'agent_does'},
              'PROD-R15': {'id': 'PROD-C01', 'autonomy': 'agent_does'},
              'PROD-R16': {'id': 'PROD-C08', 'autonomy': 'agent_does'},
              'PROD-R17': {'id': 'PROD-C08', 'autonomy': 'agent_does'},
              'PROD-R18': {'id': 'PROD-C07', 'autonomy': 'agent_does'},
              'PROD-R19': {'id': 'PROD-C05', 'autonomy': 'agent_does'},
              'PROD-R20': {'id': 'PROD-C03', 'autonomy': 'agent_does'},
              'PROD-R21': {'id': 'PROD-C04', 'autonomy': 'agent_does'},
              'PROD-R22': {'id': 'PROD-C31', 'autonomy': 'agent_does'},
              'PROD-R23': {'id': 'PROD-C06', 'autonomy': 'agent_does'},
              'PROD-R24': {'id': 'PROD-C10', 'autonomy': 'agent_does'},
              'PROD-R25': {'id': 'PROD-C11', 'autonomy': 'founder_gate'},
              'PROD-R26': {'id': 'PROD-C02', 'autonomy': 'agent_does'},
              'PROD-R27': {'id': 'PROD-C13', 'autonomy': 'agent_does'},
              'PROD-R28': {'id': 'PROD-C04', 'autonomy': 'agent_does'},
              'PROD-R29': {'id': 'PROD-C05', 'autonomy': 'agent_does'},
              'PROD-R30': {'id': 'PROD-C12', 'autonomy': 'human_assist'},
              'PROD-R31': {'id': 'PROD-C29', 'autonomy': 'human_assist'},
              'PROD-R32': {'id': 'PROD-C46', 'autonomy': 'agent_does'},
              'PROD-R33': {'id': 'PROD-C06', 'autonomy': 'agent_does'},
              'PROD-R34': {'id': 'PROD-C06', 'autonomy': 'agent_does'},
              'PROD-R35': {'id': 'PROD-C12', 'autonomy': 'human_assist'},
              'PROD-R36': {'id': 'PROD-C04', 'autonomy': 'agent_does'},
              'PROD-R37': {'id': 'PROD-C07', 'autonomy': 'agent_does'},
              'PROD-R38': {'id': 'PROD-C04', 'autonomy': 'agent_does'},
              'PROD-R39': {'id': 'PROD-C07', 'autonomy': 'agent_does'},
              'PROD-R40': {'id': 'PROD-C07', 'autonomy': 'agent_does'},
              'PROD-R41': {'id': 'PROD-C04', 'autonomy': 'agent_does'},
              'PROD-R42': {'id': 'PROD-C08', 'autonomy': 'agent_does'}}
SEVERITY_ORDER = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}

# Review records name their line in a short key; the store names it by SKU title.
REVIEW_LINE = {'ankle': 'Ankle Sock', 'calf': 'Calf Sock', 'no_show': 'No Show Sock',
               'merino': 'Merino Wool Calf Sock', 'slippers': 'Gripper Slipper', 'underwear': 'Boxer Brief',
               't_shirts': 'Pima Cotton Tee', 'compression': 'Compression Sock'}

_MODS = {}


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def metrics():
    if 'metrics' not in _MODS:
        _MODS['metrics'] = _load('ecomos_metrics_research', APP / 'metrics.py')
    return _MODS['metrics']


def brand_data(brand):
    if 'tables' not in _MODS:
        _MODS['tables'] = _load('ecomos_tables_research', APP / 'data' / 'tables.py')
    return _MODS['tables'].brand_data(brand)


def brain(brand, today=None):
    """The brand's brain store, or None when the brand has no brain folder."""
    import sys
    if str(APP / 'brain') not in sys.path:
        sys.path.insert(0, str(APP / 'brain'))
    import store
    if not (APP / 'brain' / str(brand)).is_dir():
        return None
    return store.Brain(brand, today=today)


def slug(line):
    return str(line).lower().replace(' ', '-')


def month_add(month, k):
    y, m = int(month[:4]), int(month[5:7]) + k
    y += (m - 1) // 12
    return f'{y}-{(m - 1) % 12 + 1:02d}'


def month_end(month):
    return metrics().month_end(month)


def last_full_day(data, brand):
    source = brand_data(brand) if brand else data
    return date.fromisoformat(source.brand['as_of'])


def last_whole_month(ends_on):
    """The last month that ends on or before ends_on."""
    m = ends_on.strftime('%Y-%m')
    return m if month_end(m) <= ends_on else month_add(m, -1)


class Reader:
    """One brand, one window end. m(name, first_month, last_month, **kw) is metrics.compute over whole months."""

    def __init__(self, data, brand, ends_on):
        self.data, self.brand, self.ends_on = data, brand, ends_on
        self.last_month = last_whole_month(ends_on)

    def m(self, name, first, last, **kw):
        start = date.fromisoformat(first + '-01')
        end = month_end(last)
        q = {'window': f'{(end - start).days + 1}d', 'end': end.isoformat(), **kw}
        if self.brand:
            q['brand'] = self.brand
        return metrics().compute(name, self.data, **q)

    def lines(self, first, last):
        r = self.m('units', first, last, by='line')
        return r, ({g['line']: g for g in r['groups']} if not r.get('unavailable') else {})


# ---------------------------------------------------------------- trend

def trend(rd):
    """Per line: units in the last 3 whole months against the same months a year back, and against the store."""
    last = rd.last_month
    first = month_add(last, 1 - TREND_MONTHS)
    now_r, now = rd.lines(first, last)
    ago_r, ago = rd.lines(month_add(first, -12), month_add(last, -12))
    if now_r.get('unavailable') or ago_r.get('unavailable'):
        bad = now_r if now_r.get('unavailable') else ago_r
        return {'unavailable': True, 'reason': bad.get('reason'), 'fix': bad.get('fix')}
    store_growth = now_r['value'] / ago_r['value'] - 1 if ago_r['value'] else None
    monthly = []  # (month, {line: growth}, store growth) for each of the 3 months
    for k in range(TREND_MONTHS):
        mo = month_add(first, k)
        a_r, a = rd.lines(mo, mo)
        b_r, b = rd.lines(month_add(mo, -12), month_add(mo, -12))
        if a_r.get('unavailable') or b_r.get('unavailable') or not b_r['value']:
            continue
        monthly.append((mo, {l: a[l]['units'] / b[l]['units'] - 1 for l in a if l in b and b[l]['units']},
                        a_r['value'] / b_r['value'] - 1))
    rows = []
    for line, g in now.items():
        p = ago.get(line)
        growth = g['units'] / p['units'] - 1 if p and p['units'] else None
        gap = round((growth - store_growth) * 100, 2) if growth is not None and store_growth is not None else None
        trailed = sum(1 for _, lg, sg in monthly if line in lg and lg[line] < sg)
        rows.append({'line': line, 'skus': g['skus'], 'units': g['units'], 'units_year_ago': p['units'] if p else None,
                     'net_sales': g['net_sales'], 'net_per_unit': g['net_per_unit'],
                     'growth': round(growth, 4) if growth is not None else None, 'gap_points': gap,
                     'months_trailing_store': trailed, 'months_checked': len(monthly)})
    rows.sort(key=lambda r: -r['units'])
    return {'unavailable': False, 'first': first, 'last': last, 'year_ago': [month_add(first, -12), month_add(last, -12)],
            'store_units': now_r['value'], 'store_units_year_ago': ago_r['value'],
            'store_growth': round(store_growth, 4) if store_growth is not None else None, 'lines': rows,
            'freshness': now_r.get('freshness')}


def declining(row):
    """'down' when units fell on last year, 'losing_share' when growth trails the store by the gap, else None."""
    if row['growth'] is None or row['gap_points'] is None:
        return None
    if row['growth'] < 0:
        return 'down'
    if row['gap_points'] <= -SHARE_GAP_POINTS:
        return 'losing_share'
    return None


# ---------------------------------------------------------------- reviews

def review_lines(br):
    """One row per reviewed line from the brain's products.reviews_* records."""
    if br is None:
        return []
    out = []
    for rec in br.records('products'):
        v = rec.get('value')
        if not rec['id'].startswith(f'{br.brand}.products.reviews_') or not isinstance(v, dict):
            continue
        dist = v.get('yotpo_star_distribution') or {}
        total = v.get('yotpo_review_total')
        low = (dist.get('1') or 0) + (dist.get('2') or 0) if dist else None
        out.append({'key': v.get('product_line'), 'line': REVIEW_LINE.get(v.get('product_line')),
                    'record': rec['id'], 'product': v.get('yotpo_product'), 'pdp': v.get('pdp'),
                    'reviews': total, 'rating': v.get('yotpo_average'),
                    'low_star': low, 'low_star_share': round(low / total, 4) if total and low is not None else None,
                    'praise': v.get('praise') or [], 'issues': v.get('issues') or [],
                    'captured_at': (rec.get('source') or {}).get('captured_at')})
    return out


def ladders(br):
    """Objection ladders with the review records each rung was built from."""
    if br is None:
        return []
    out = []
    for rec in br.records('objection_ladders'):
        v = rec.get('value') or {}
        rungs = []
        for r in v.get('rungs') or []:
            c = r.get('counts') or {}
            rungs.append({'level': r.get('level'), 'doubt': r.get('doubt'), 'one_star': c.get('one_star'),
                          'five_star': c.get('five_star'), 'proof': bool(r.get('proof')),
                          'from_reviews': [d for d in r.get('derived_from') or [] if '.products.reviews_' in d]})
        counts = v.get('counts') or {}
        out.append({'id': rec['id'], 'theme': v.get('theme'), 'what_works': v.get('what_works') or [],
                    'what_fails': v.get('what_fails') or [], 'one_star': counts.get('one_star'),
                    'five_star': counts.get('five_star'), 'rungs': rungs,
                    'reviews_records': sorted({d for r in rungs for d in r['from_reviews']})})
    return out


def median_low_star(reviews):
    shares = [r['low_star_share'] for r in reviews if r['low_star_share'] is not None]
    return round(statistics.median(shares), 4) if len(shares) >= 3 else None


# ---------------------------------------------------------------- findings

def _ev(metric, value, unit, ends_on, window, baseline=None, baseline_kind=None, source='products_monthly',
        simulated=True, freshness_days=1, **extra):
    out = {'metric': metric, 'value': value, 'unit': unit, 'window': window, 'ends_on': ends_on,
           'freshness_days': freshness_days, 'baseline': baseline, 'baseline_kind': baseline_kind, 'source': source,
           'simulated': simulated}
    out.update(extra)
    return out


def _confidence(windows_agree):
    return 0.9 if windows_agree >= 4 else 0.7 if windows_agree >= 2 else 0.5


def _severity(stake, net_28d, windows_agree):
    if stake is not None and net_28d and stake > 0.05 * net_28d:
        return 'critical'
    if windows_agree >= 2 or (stake is not None and net_28d and stake > 0.01 * net_28d):
        return 'high'
    return 'medium'


def _finding(rule_id, line, ends_on, severity, evidence, sentence, stake, confidence, brain_refs=(), money_reason=None):
    out = {'id': f'{SCREEN}.{rule_id}.{slug(line)}', 'screen': SCREEN, 'rule_id': rule_id, 'severity': severity,
           'entity': {'type': 'sku', 'id': slug(line), 'label': f'{line} (product line)'}, 'evidence': evidence,
           'sentence': sentence, 'capability': dict(CAPABILITY[rule_id]), 'money_at_stake': stake,
           'confidence': confidence, 'brain_refs': list(brain_refs), 'first_seen': ends_on.isoformat(),
           'last_seen': ends_on.isoformat(), 'status': 'open', 'unavailable': None}
    if stake is None:
        out['money_reason'] = money_reason or 'no baseline'
    return out


def _unavailable(rule_id, ends_on, reason, inputs, connector, fix):
    return {'id': f'{SCREEN}.{rule_id}.brand', 'screen': SCREEN, 'rule_id': rule_id, 'severity': 'medium',
            'entity': {'type': 'brand', 'id': 'brand', 'label': 'Product lines'}, 'evidence': [],
            'sentence': reason, 'capability': dict(CAPABILITY[rule_id]), 'money_at_stake': None,
            'money_reason': 'inputs unavailable', 'confidence': 0.1, 'brain_refs': [],
            'first_seen': ends_on.isoformat(), 'last_seen': ends_on.isoformat(), 'status': 'unavailable',
            'unavailable': {'inputs': inputs, 'connector': connector, 'fix': fix}}


def _span(first, last):
    a = date.fromisoformat(first + '-01').strftime('%b')
    b = date.fromisoformat(last + '-01').strftime('%b %Y')
    return f'{a} to {b}'


def declining_findings(tr, ends_on, net_28d):
    out = []
    end = month_end(tr['last']).isoformat()
    window = f'{TREND_MONTHS} months'
    for r in tr['lines']:
        kind = declining(r)
        if not kind:
            continue
        sg = tr['store_growth']
        lost_units = round((sg - r['growth']) * r['units_year_ago'])
        usd = max(round(lost_units * r['net_per_unit']), 0) if r['net_per_unit'] else None
        stake = None if usd is None else {
            'usd': usd, 'formula': '(store_growth - line_growth) * units_year_ago * net_per_unit',
            'inputs': {'store_growth': sg, 'line_growth': r['growth'], 'units_year_ago': r['units_year_ago'],
                       'net_per_unit': r['net_per_unit']}, 'window': window}
        agree = r['months_trailing_store']
        evidence = [
            _ev('units', r['units'], 'count', end, window, r['units_year_ago'], 'own_median',
                note=f'baseline is the same {TREND_MONTHS} months a year earlier'),
            _ev('unit_growth', r['growth'], 'ratio', end, window, sg, 'threshold',
                note=f'baseline is the whole store; the rule fires at {SHARE_GAP_POINTS:g} point behind'),
            _ev('months_trailing_store', agree, 'count', end, window, r['months_checked'], 'threshold'),
            _ev('net_per_unit', r['net_per_unit'], 'usd', end, window)]
        span = _span(tr['first'], tr['last'])
        if kind == 'down':
            sentence = (f'{r["line"]} sold {r["units"]:,} units from {span}, down {abs(round(r["growth"] * 100, 1))} '
                        f'percent on last year. The store grew {round(sg * 100, 1)} percent.')
        else:
            sentence = (f'{r["line"]} units grew {round(r["growth"] * 100, 1)} percent on last year from {span}. '
                        f'The store grew {round(sg * 100, 1)} percent, so the line is losing share.')
        out.append(_finding('PROD-R01', r['line'], ends_on, _severity(usd, net_28d, agree), evidence, sentence, stake,
                            _confidence(agree)))
    return out


def review_findings(reviews, lads, rd, tr, ends_on, net_28d):
    out = []
    base = median_low_star(reviews)
    if base is None:
        return out
    last = tr.get('last') if not tr.get('unavailable') else None
    month = rd.lines(last, last)[1] if last else {}
    for rv in reviews:
        share = rv['low_star_share']
        if share is None or share < LOW_STAR_FLOOR or share < LOW_STAR_TIMES_MEDIAN * base:
            continue
        line = rv['line'] or rv['key']
        month_net = (month.get(rv['line']) or {}).get('net_sales')
        stake, reason = None, None
        if month_net is None:
            reason = 'no sales for this line in the last whole month'
        else:
            stake = {'usd': round(month_net * (share - base)), 'formula': 'net_sales_last_month * (low_star_share - median_low_star_share)',
                     'inputs': {'net_sales_last_month': month_net, 'low_star_share': share, 'median_low_star_share': base},
                     'window': f'1 month ({last})'}
        fresh = (ends_on - date.fromisoformat(rv['captured_at'][:10])).days if rv['captured_at'] else None
        rung_hits = [(l, g) for l in lads for g in l['rungs'] if rv['record'] in g['from_reviews']]
        evidence = [
            _ev('low_star_share', share, 'ratio', ends_on.isoformat(), 'all reviews to capture', base, 'own_median',
                source=rv['record'], simulated=False, freshness_days=max(fresh or 0, 0),
                note='baseline is the median across the brand\'s reviewed lines'),
            _ev('reviews', rv['reviews'], 'count', ends_on.isoformat(), 'all reviews to capture', source=rv['record'],
                simulated=False, freshness_days=max(fresh or 0, 0)),
            _ev('rating', rv['rating'], 'stars', ends_on.isoformat(), 'all reviews to capture', source=rv['record'],
                simulated=False, freshness_days=max(fresh or 0, 0), top_issues=rv['issues'][:3])]
        for l, g in rung_hits:
            evidence.append(_ev('ladder_rung_one_star', g['one_star'], 'count', ends_on.isoformat(), 'at ladder build',
                                source=l['id'], simulated=False, rung=f'{l["theme"]}.level_{g["level"]}', doubt=g['doubt'],
                                proof_on_file=g['proof']))
        if month_net is not None:
            evidence.append(_ev('net_sales', month_net, 'usd', month_end(last).isoformat(), '1 month'))
        top = rv['issues'][0] if rv['issues'] else 'no issue named'
        sentence = (f'{round(share * 100, 1)} percent of {rv["reviews"]:,} {line} reviews are 1 or 2 stars. '
                    f'The brand median is {round(base * 100, 1)} percent. The top issue is: {top}.')
        usd = stake['usd'] if stake else None
        refs = [rv['record']] + sorted({l['id'] for l, _ in rung_hits})
        out.append(_finding('PROD-R02', line, ends_on, _severity(usd, net_28d, 1), evidence, sentence, stake,
                            _confidence(1), refs, reason))
    return out



# ---------------------------------------------------------------- hero line, pipeline

PIPELINE_PATH = HERE / 'fixtures' / 'pipeline.json'
STAGES = ['screened', 'researched', 'gated', 'shortlisted', 'go']
CLOSED_STAGES = ('go', 'killed', 'kill')
SCREEN_CHECKS = ('demand', 'competition', 'store_fit')
SCREEN_FAIL_AT = 2


def pipeline(brand):
    """Candidates from this screen's pipeline file (fixtures/pipeline.json, rows). Empty when absent."""
    if not PIPELINE_PATH.is_file():
        return []
    doc = json.loads(PIPELINE_PATH.read_text(encoding='utf-8'))
    rows = doc.get('rows') if isinstance(doc, dict) else doc
    return [r for r in rows or [] if r.get('brand') in (None, brand or 'sample')]


def candidate_view(r, ends_on):
    """A candidate row with the numbers the rules and the desk read: age, time left, failed checks, stage index."""
    since = r.get('screen_in_date')
    age = (ends_on - date.fromisoformat(since)).days if since else None
    box = r.get('time_box_days')
    checks = r.get('screen_result') or {}
    failed = [k for k in SCREEN_CHECKS if checks.get(k) == 'fail']
    unchecked = [k for k in SCREEN_CHECKS if checks.get(k) not in ('pass', 'fail')]
    return dict(r, age_days=age, days_left=(box - age) if box is not None and age is not None else None,
                over_box=bool(box is not None and age is not None and age > box and r.get('stage') not in CLOSED_STAGES),
                failed_checks=failed, unchecked_checks=unchecked, stage_index=STAGES.index(r['stage']) if r.get('stage') in STAGES else None,
                closed=r.get('stage') in CLOSED_STAGES)


def pipeline_funnel(rows):
    """How many candidates reached each stage (a candidate at 'gated' has passed screened and researched)."""
    out = []
    for i, st in enumerate(STAGES):
        n = sum(1 for r in rows if r.get('stage_index') is not None and r['stage_index'] >= i)
        out.append({'stage': st, 'n': n})
    return out


def pipeline_findings(brand, ends_on):
    """PROD-R14: a candidate past its time box with no decision. PROD-R15: a candidate that failed 2 or more of the
    3 fast checks and is still open."""
    out = []
    for r in [candidate_view(x, ends_on) for x in pipeline(brand)]:
        cid = r.get('candidate_id') or slug(r.get('name'))
        if r['over_box']:
            ev = [_ev('candidate_pipeline_age_days', r['age_days'], 'days', ends_on.isoformat(), 'since screen-in', r['time_box_days'], 'threshold', source='fixtures.pipeline', simulated=False, freshness_days=0,
                      stage=r.get('stage')),
                  _ev('research_hours_logged', r.get('hours_logged'), 'hours', ends_on.isoformat(), 'since screen-in', source='fixtures.pipeline', simulated=False, freshness_days=0)]
            sentence = f'{r["name"]} has sat at {r["stage"]} for {r["age_days"]} days, past its {r["time_box_days"]}-day box. Decide or kill it.'
            f = _finding('PROD-R14', cid, ends_on, 'low', ev, sentence, None, 0.9, [], money_reason='research time, not revenue')
            f['entity'] = {'type': 'sku', 'id': cid, 'label': r['name'], 'stage': r.get('stage'), 'candidate': True}
            f['id'] = f'{SCREEN}.PROD-R14.{cid}'
            out.append(f)
        if len(r['failed_checks']) >= SCREEN_FAIL_AT and not r['closed']:
            ev = [_ev('demand_screen_failed_checks', len(r['failed_checks']), 'count', ends_on.isoformat(), 'at screening', SCREEN_FAIL_AT, 'threshold', source='fixtures.pipeline', simulated=False, freshness_days=0,
                      failed=r['failed_checks'])]
            sentence = f'{r["name"]} failed {len(r["failed_checks"])} of the 3 fast checks ({", ".join(c.replace("_", " ") for c in r["failed_checks"])}). Killing it now saves the research hours.'
            f = _finding('PROD-R15', cid, ends_on, 'medium', ev, sentence, None, 0.7, [], money_reason='a killed candidate saves hours, not revenue')
            f['entity'] = {'type': 'sku', 'id': cid, 'label': r['name'], 'stage': r.get('stage'), 'candidate': True, 'failed': r['failed_checks']}
            f['id'] = f'{SCREEN}.PROD-R15.{cid}'
            out.append(f)
    return out


def line_category(line, prods):
    """The category of a line from the products table, else the line itself when lines are categories."""
    for p in prods or []:
        if metrics().product_line(p.get('title')) == line:
            return p.get('category') or line
    return line


def hero_findings(tr, ends_on, prods, pipe):
    """PROD-R03: the biggest line of each category with 25 percent or more of it and no open candidate."""
    out = []
    cats = {}
    for r in tr['lines']:
        cats.setdefault(line_category(r['line'], prods), []).append(r)
    open_by_cat = {}
    for p in pipe:
        if p.get('stage') not in ('go', 'kill', 'killed'):
            open_by_cat.setdefault(p.get('category'), []).append(p)
    end = month_end(tr['last']).isoformat()
    window = f'{TREND_MONTHS} months'
    for cat, rows in cats.items():
        total = sum(r['net_sales'] for r in rows)
        if not total or len(rows) < 2:
            continue
        top = max(rows, key=lambda r: r['net_sales'])
        share = top['net_sales'] / total
        if share < HERO_SHARE or open_by_cat.get(cat):
            continue
        evidence = [
            _ev('category_share_net_sales', round(share, 4), 'ratio', end, window, HERO_SHARE, 'threshold',
                note=f'share of {cat} net sales across {len(rows)} lines'),
            _ev('net_sales', top['net_sales'], 'usd', end, window),
            _ev('open_candidates', 0, 'count', ends_on.isoformat(), 'pipeline now', 1, 'threshold', source='fixtures.pipeline',
                simulated=False, freshness_days=0)]
        sentence = (f'{top["line"]} brings in {round(share * 100)} percent of {cat} net sales over {_span(tr["first"], tr["last"])}. '
                    f'No next SKU for {cat} is open in the pipeline.')
        f = _finding('PROD-R03', top['line'], ends_on, 'medium', evidence, sentence, None, 0.7,
                     money_reason='an unlaunched SKU has no baseline to price the gap')
        f['entity']['category'] = cat
        out.append(f)
    return out


def net_28d(rd):
    r = metrics().compute('aov', rd.data, window='28d', end=rd.ends_on.isoformat(),
                          **({'brand': rd.brand} if rd.brand else {}))
    return (r.get('inputs') or {}).get('net_revenue') if not r.get('unavailable') else None


def run(brand, window=None, data=None):
    """Findings for one brand and window ({ends_on, days, trailing}), sorted by severity then stake."""
    data = data if data is not None else (brand_data(brand) if brand else None)
    last = last_full_day(data, brand)
    ends_on = min(date.fromisoformat(window['ends_on']), last) if window and window.get('ends_on') else last   # never past the data
    rd = Reader(data, brand, ends_on)
    tr = trend(rd)
    net = net_28d(rd)
    br = brain(brand, today=ends_on) if brand else None
    out = []
    if tr.get('unavailable'):
        out.append(_unavailable('PROD-R01', ends_on, 'Product sales by month are not connected, so line trends cannot be read.',
                                ['products_monthly'], tr.get('fix') or 'shopify', 'Connect the store (read only).'))
    else:
        out += declining_findings(tr, ends_on, net)
        try:
            prods = (data if data is not None else brand_data(brand)).table('products')
        except (KeyError, ValueError):
            prods = None
        out += hero_findings(tr, ends_on, prods, pipeline(brand))
    reviews = review_lines(br)
    if not reviews:
        out.append(_unavailable('PROD-R02', ends_on, 'No review totals are on file for any line, so review issues cannot be read.',
                                ['brain.products.reviews_*'], 'reviews', 'Add the review capture for each line to the brand brain.'))
    else:
        out += review_findings(reviews, ladders(br), rd, tr, ends_on, net)
    out += trend_findings(br, category_mix(data, brand, rd), ends_on)
    out += subcategory_findings(br, ends_on)
    out += conversation_findings(br, ends_on)
    out += preference_findings(br, ends_on)
    try:
        prods_for_map = (data if data is not None else brand_data(brand)).table('products')
    except (KeyError, ValueError):
        prods_for_map = None
    out += positioning_findings(br, prods_for_map, ends_on)
    out += avatar_findings(br, ends_on, net, prods_for_map)
    out += search_findings(br, data, brand, ends_on)
    out += pipeline_findings(brand, ends_on)
    out += margin_findings(brand, data, br, rd, ends_on)
    out += pattern_findings(brand, data, rd, ends_on)
    out += lane_map_findings(br, ends_on)
    out += spend_findings(br, brand, ends_on)
    out += review_price_findings(br, brand, ends_on)
    out += complaint_findings(br, ends_on)
    out += gate_findings(brand, data, br, rd, ends_on)
    out += shortlist_findings(brand, data, br, rd, ends_on)
    out += video_findings(br, brand, ends_on)
    out += tech_pack_findings(brand, ends_on)
    out += hours_findings(brand, br, ends_on)
    out += trend_check_findings(br, brand, ends_on)
    out += audience_findings(br, ends_on)
    out += marketplace_findings(br, prods_for_map, ends_on)
    out += cadence_findings(br, ends_on)
    out += return_findings(data, brand, ends_on, net)
    out += question_findings(br, ends_on)
    out += pull_findings(br, brand, ends_on)
    out += first_run_findings(brand, ends_on, net)
    out += override_findings(brand, ends_on)
    out += companion_findings(brand, data, rd, ends_on)
    out += order_findings(brand, data, br, rd, ends_on)
    out += freshness_findings(br, ends_on)
    out += assumption_findings(br, ends_on)
    out.sort(key=lambda f: (SEVERITY_ORDER[f['severity']], -((f['money_at_stake'] or {}).get('usd') or 0), f['id']))
    return out


# ---------------------------------------------------------------- category mix, 12 whole months

MIX_MONTHS = 12


def orders_monthly(data):
    """products_monthly-shaped rows built from order line items when a brand has no monthly product table: month, category
    (the product's type), units and net sales (line total less the order's discount, shared by line value). Cancelled orders
    are left out. Raises KeyError when orders or products are not connected."""
    orders = data.table('orders')
    products = data.table('products')
    cat_of = {p.get('sku'): (p.get('type') or p.get('category') or 'other') for p in products if p.get('sku')}
    out = {}
    for o in orders:
        if o.get('cancelled_at'):
            continue
        month = str(o.get('created_at') or '')[:7]
        lines = o.get('line_items') or []
        subtotal = float(o.get('subtotal') or sum(float(l.get('line_total') or 0) for l in lines) or 0)
        discount = float(((o.get('discount') or {}).get('amount') if isinstance(o.get('discount'), dict) else o.get('discount')) or 0)
        for l in lines:
            cat = cat_of.get(l.get('sku'), 'other')
            value = float(l.get('line_total') or 0)
            net = value - (discount * value / subtotal if subtotal else 0)
            g = out.setdefault((month, cat), {'month': month, 'category': cat, 'units': 0, 'net_sales': 0.0})
            g['units'] += int(l.get('qty') or 0)
            g['net_sales'] += net
    return [dict(g, net_sales=round(g['net_sales'], 2)) for g in sorted(out.values(), key=lambda g: (g['month'], g['category']))]


def mix_rows(data, brand):
    """The monthly product rows the mix reads: products_monthly when connected, else order line items by product type."""
    source = brand_data(brand) if brand else data
    try:
        return source.table('products_monthly'), 'products_monthly'
    except (KeyError, ValueError) as exc:
        first = exc
    try:
        return orders_monthly(source), 'order line items by product type (no monthly product table)'
    except (KeyError, ValueError):
        raise first


def category_mix(data, brand, rd):
    """Our units and net sales by category over the last 12 whole months against the 12 before, from products_monthly, or
    from order line items when a brand has no monthly product table."""
    try:
        rows, basis = mix_rows(data, brand)
    except (KeyError, ValueError) as exc:
        return {'unavailable': True, 'reason': f'products_monthly is not connected ({exc})', 'fix': 'shopify', 'rows': []}
    last = rd.last_month
    first = month_add(last, 1 - MIX_MONTHS)
    p_first, p_last = month_add(first, -12), month_add(last, -12)
    now, ago, series = {}, {}, {}
    months = [month_add(first, k) for k in range(MIX_MONTHS)]
    for r in rows:
        cat = r.get('category') or 'other'
        m = r.get('month')
        if first <= m <= last:
            g = now.setdefault(cat, {'units': 0, 'net_sales': 0.0})
            g['units'] += r.get('units') or 0
            g['net_sales'] += r.get('net_sales') or 0.0
            series.setdefault(cat, {mm: None for mm in months})[m] = (series.get(cat, {}).get(m) or 0) + (r.get('units') or 0)
        elif p_first <= m <= p_last:
            g = ago.setdefault(cat, {'units': 0, 'net_sales': 0.0})
            g['units'] += r.get('units') or 0
            g['net_sales'] += r.get('net_sales') or 0.0
    total_units = sum(g['units'] for g in now.values())
    total_net = sum(g['net_sales'] for g in now.values())
    ago_months = {r.get('month') for r in rows if p_first <= (r.get('month') or '') <= p_last}
    covered = len(ago_months) >= MIX_MONTHS   # growth needs the whole prior year on file; a partial year reads as unavailable
    if not covered:
        ago = {}
    out = []
    for cat, g in now.items():
        a = ago.get(cat)
        out.append({'category': cat, 'units': g['units'], 'net_sales': round(g['net_sales'], 2),
                    'unit_share': round(g['units'] / total_units, 4) if total_units else None,
                    'net_share': round(g['net_sales'] / total_net, 4) if total_net else None,
                    'growth': round(g['units'] / a['units'] - 1, 4) if a and a['units'] else None,
                    'net_growth': round(g['net_sales'] / a['net_sales'] - 1, 4) if a and a['net_sales'] else None,
                    'series': [series[cat][m] for m in months]})
    out.sort(key=lambda r: -r['net_sales'])
    return {'unavailable': False, 'first': first, 'last': last, 'months': months, 'rows': out, 'basis': basis,
            'growth_note': None if covered else f'growth on last year is unavailable: the data holds {len(ago_months)} of the 12 prior months',
            'store_growth': round(sum(g['units'] for g in now.values()) / sum(g['units'] for g in ago.values()) - 1, 4) if ago and sum(g['units'] for g in ago.values()) else None}



# ---------------------------------------------------------------- the web pass (fixtures/market_trends.json)

def market_trends():
    """The public web pass this screen keeps as a fixture: markets, preferences, launches, each with url and date.
    None when the file is absent. Never a number without a source."""
    path = HERE / 'fixtures' / 'market_trends.json'
    if not path.is_file():
        return None
    import json
    return json.loads(path.read_text(encoding='utf-8'))


# words that tie a public market or sub-category to what the brand sells; the brand side is read from the brain
def brand_of(x):
    """The brand name behind a Brain, a brand string or None."""
    return getattr(x, 'brand', x) if x is not None else None


def web_pass(x):
    """The web pass for this brand: fixtures/web_pass/<brand>.json when it exists (written by web_pass.py), else the legacy
    fixture when its brand field matches (or it names no brand); None for any other brand, so a kitchen brand never reads a
    sock brand's markets, lanes or launches."""
    b = brand_of(x)
    if b:
        own = HERE / 'fixtures' / 'web_pass' / f'{b}.json'
        if own.is_file():
            try:
                doc = json.loads(own.read_text(encoding='utf-8'))
            except ValueError:
                doc = None
            if isinstance(doc, dict) and doc.get('brand') == b:
                return doc
    fx = market_trends()
    if not fx:
        return None
    return fx if not fx.get('brand') or (b and fx.get('brand') == b) else None


def lanes_for(x):
    """The lanes (key, label, terms) this desk follows for the brand: the web pass fixture's lanes, else the module default
    when the fixture matches the brand and names none, else nothing."""
    fx = web_pass(x)
    if fx is None:
        return []
    lanes = fx.get('lanes')
    if lanes:
        return [(l['key'], l['label'], list(l.get('terms') or [])) for l in lanes]
    return list(SUBCATS)


def listing_pull():
    path = HERE / 'fixtures' / 'amazon_listings.json'
    return json.loads(path.read_text(encoding='utf-8')) if path.is_file() else None


def listing_pull_for(x):
    """The listing seller pull for this brand (fixtures/amazon_listings.json) when its brand matches; else None."""
    lp = listing_pull()
    if not lp:
        return None
    b = brand_of(x)
    return lp if not lp.get('brand') or (b and lp.get('brand') == b) else None


def social_pull_for(x):
    """The social pull fixture for this brand: the file when its brand field matches (or it names no brand); else None."""
    sp = social_pull()
    if not sp:
        return None
    b = brand_of(x)
    return sp if not sp.get('brand') or (b and sp.get('brand') == b) else None


MARKET_CATEGORY = {'socks_us': 'socks', 'socks_global': 'socks', 'slippers_us': 'slippers', 'mens_underwear_us': 'underwear',
                   'womens_underwear_us': 'underwear', 'basics_tshirts': 'tshirts', 'footwear_casual': 'footwear',
                   'compression_socks': 'socks', 'athletic_socks': 'socks', 'merino_wool_socks': 'socks',
                   'gifting_socks': 'socks', 'sustainable_apparel': None}
MARKET_WORDS = {'compression_socks': ['compression'], 'athletic_socks': ['athletic', 'performance', 'running', 'sport'],
                'merino_wool_socks': ['merino'], 'gifting_socks': ['gift'], 'sustainable_apparel': ['sustainab', 'recycled', 'organic'],
                'slippers_us': ['slipper'], 'mens_underwear_us': ['underwear', 'boxer', 'brief'], 'womens_underwear_us': ['underwear', 'bralette', 'hipster'],
                'basics_tshirts': ['t-shirt', 'tshirt', ' tee ', ' tees'], 'footwear_casual': ['clog', 'moccasin', 'sandal', 'footwear'], 'socks_us': ['sock'], 'socks_global': ['sock']}


def brand_words(br):
    """Lower-case text of the brain's product, claim and site records, for keyword coverage checks."""
    if br is None:
        return ''
    parts = []
    for sec in ('products', 'claims', 'site_map', 'offers'):
        for r in br.records(sec):
            parts.append(str(r.get('text') or ''))
            v = r.get('value')
            parts.append(v if isinstance(v, str) else __import__('json').dumps(v))
    return ' '.join(parts).lower()


def market_covered(key, words):
    """True when the brand's own records name the sub-category the market row describes."""
    return any(w in words for w in MARKET_WORDS.get(key, [key.split('_')[0]]))


def ad_words(br):
    """Lower-case text of the brand's own active-ad signals in the brain (learnings with role self, offers seen in ads)."""
    if br is None:
        return ''
    parts = []
    rivals = [c['name'].lower() for c in competitor_signals(br)]
    for r in br.records('learnings'):
        v = r.get('value')
        if isinstance(v, dict) and v.get('role') == 'competitor':
            continue
        if (r.get('source') or {}).get('type') != 'ad_library':
            continue
        if any(n in str(r.get('text') or '').lower() for n in rivals):
            continue   # a read of competitor ads, not our own
        parts.append(str(r.get('text') or ''))
        parts.append(json.dumps(v))
        for e in r.get('evidence') or []:
            parts.append(str(e.get('quote') or ''))
    for r in br.records('offers'):
        if (r.get('source') or {}).get('type') == 'ad_library':
            parts.append(str(r.get('text') or ''))
    return ' '.join(parts).lower()


TREND_MIN_CAGR = 4.0
GIFT_WINDOW_DAYS = 90


def trend_findings(br, mix, ends_on):
    """PROD-R04 and PROD-R05 from the web pass fixture against our category mix and our active ads."""
    fx = web_pass(br)
    if not fx:
        return [_unavailable('PROD-R05', ends_on, 'No web pass is on file, so the category trend cannot be read.',
                             ['fixtures/market_trends.json'], 'web_pass', 'Run the research web pass for this brand.')]
    words = brand_words(br)
    ads = ad_words(br)
    ours = {r['category']: r for r in (mix.get('rows') or [])} if not mix.get('unavailable') else {}
    out = []
    for m in fx.get('markets') or []:
        key = m.get('key')
        cagr = m.get('cagr_pct')
        src = (m.get('sources') or [{}])[0]
        cite = f"{src.get('publisher') or 'public source'}, {src.get('date') or 'undated'}"
        cat = MARKET_CATEGORY.get(key)
        our = ours.get(cat) if cat else None
        # R04: our category grows slower than its public market
        if our and our.get('growth') is not None and isinstance(cagr, (int, float)) and our['growth'] * 100 < cagr:
            lost = round((cagr / 100 - our['growth']) * our['net_sales'])
            stake = {'usd': max(lost, 0), 'formula': '(market_cagr - our_growth) * our_net_sales_12m',
                     'inputs': {'market_cagr': cagr / 100, 'our_growth': our['growth'], 'our_net_sales_12m': our['net_sales']}, 'window': '12 months'}
            ev = [_ev('unit_growth_12m', our['growth'], 'ratio', month_end(mix['last']).isoformat(), '12 months', cagr / 100, 'peer_band',
                      note=f'baseline is the public market growth a year ({cite})'),
                  _ev('net_sales_12m', our['net_sales'], 'usd', month_end(mix['last']).isoformat(), '12 months')]
            sentence = (f'{cat} units grew {round(our["growth"] * 100, 1)} percent in 12 months. The {m.get("label")} market grows '
                        f'{cagr} percent a year ({cite}), so the line is losing share of its market.')
            out.append(_finding('PROD-R04', cat, ends_on, 'medium', ev, sentence, stake, 0.3, [f'fixtures.market_trends.{key}']))
        # R05: a growing sub-category the brand sells and does not advertise
        growing = isinstance(cagr, (int, float)) and cagr >= TREND_MIN_CAGR and m.get('direction') == 'up'
        gifting = key == 'gifting_socks' and 0 <= (date(ends_on.year, 11, 1) - ends_on).days <= GIFT_WINDOW_DAYS
        if not (growing or gifting):
            continue
        if not words or not market_covered(key, words):
            continue
        if any(w in ads for w in MARKET_WORDS.get(key, [])):
            continue
        size = m.get('size_usd')
        ev = [_ev('market_cagr_pct', cagr, 'percent', src.get('date') or ends_on.isoformat(), m.get('cagr_window') or 'forecast', TREND_MIN_CAGR, 'threshold',
                  source=src.get('url'), simulated=False, freshness_days=0, note=cite),
              _ev('market_size_usd', size, 'usd', str(m.get('size_year') or ''), 'year', source=src.get('url'), simulated=False, freshness_days=0),
              _ev('active_ads_naming_it', 0, 'count', ends_on.isoformat(), 'active ads now', 1, 'threshold', source='brain.learnings', simulated=False, freshness_days=0)]
        if gifting:
            sentence = (f'Socks are a holiday gift category ({cite}) and the window opens in {(date(ends_on.year, 11, 1) - ends_on).days} days. '
                        f'No active ad names a gift.')
        else:
            sentence = (f'{m.get("label")} grows {cagr} percent a year' + (f' on ${size / 1e9:,.1f} billion' if size else '') +
                        f' ({cite}). The brand\'s own records carry it and no active ad names it.')
        f = _finding('PROD-R05', key, ends_on, 'medium', ev, sentence, None, 0.5, [f'fixtures.market_trends.{key}', f'{br.brand}.learnings.hook_types' if br else ''],
                     money_reason='no share of the sub-category is measurable without search or marketplace data')
        f['entity'] = {'type': 'metric', 'id': key, 'label': m.get('label') or key, 'category': cat}
        f['id'] = f'{SCREEN}.PROD-R05.{key}'
        f['brain_refs'] = [x for x in f['brain_refs'] if x]
        out.append(f)
    return out


# ---------------------------------------------------------------- sub-categories: what competitors push, what launched

# the structure is fixed; which lanes fire depends on the brain and the web pass
PROOF_LANES = {'guarantee', 'creator'}   # proof types, not products: "sold" reads as "proof on file"
SUBCATS = [
    ('compression', 'Compression and relief', ['compression', 'relief', 'plantar', 'nurse', 'pots', 'circulation', 'mmhg']),
    ('merino', 'Merino and wool', ['merino', 'wool']),
    ('performance', 'Run, hike and sport', ['running sock', 'run sock', 'runner', 'hiking', 'hike', 'trail', 'athlete', 'sport', 'performance', 'ski sock', 'studio']),
    ('guarantee', 'Guarantee and durability proof', ['lifetime guarantee', 'guarantee', 'durab', 'made in usa', 'made in the usa']),
    ('style', 'Style, drops and collabs', ['style-led', 'style and', 'self expression', 'new arrival', 'limited drop', 'limited edition', 'collab', 'pokemon', 'jurassic', 'minions', 'embroider']),
    ('gifting', 'Gifting', ['gift']),
    ('underwear', 'Underwear', ['underwear', 'boxer', 'briefs', 'boxer brief', 'thong', 'bralette']),
    ('footwear', 'Slippers and footwear', ['slipper', 'clog', ' boots', 'sneaker', 'slip-on', 'footwear', 'moccasin', 'sandal']),
    ('apparel', 'Apparel beyond basics', ['sweats', 'denim', 'jean', 'hoody', 'hoodie', 'swim', ' tee ', ' tees', 't-shirt', 'jacket']),
    ('creator', 'Creator and first-person proof', ['first person', 'first_person', 'creator', 'testimonial', 'review quote', 'nurse count', 'listicle', 'advertorial']),
]
FOLLOW_MIN_COMPETITORS = 2
FOLLOW_MIN_RUN_DAYS = 30
IGNORE_MAX_RUN_DAYS = 14


def competitor_signals(br):
    """One row per competitor page from the brain: active ads, longest run, hooks and what they push, as text."""
    if br is None:
        return []
    pages = {}
    for r in br.records('competitors'):
        v = r.get('value')
        if not isinstance(v, dict):
            continue
        name = v.get('page') or v.get('name')
        if not name:
            continue
        key = name.lower().replace(' socks', '').replace(' vermont', '').strip()
        p = pages.setdefault(key, {'name': name, 'records': [], 'active_ads': None, 'longest_run_days': None, 'text': ''})
        p['records'].append(r['id'])
        ads = v.get('active_ads') or v.get('active_ads_seen')
        if ads is not None:
            p['active_ads'] = max(p['active_ads'] or 0, ads)
        run = v.get('longest_run_days') or (v.get('longest_running_ad') or {}).get('days_running')
        if run is not None:
            p['longest_run_days'] = max(p['longest_run_days'] or 0, run)
        hooks = v.get('hook_types')
        parts = [str(v.get('what_they_push') or ''), str(v.get('positioning') or '')]
        parts += list(hooks) if isinstance(hooks, list) else list(hooks.keys()) if isinstance(hooks, dict) else []
        parts += [str(e.get('quote') or '') for e in r.get('evidence') or []]
        p['text'] = (p['text'] + ' ' + ' '.join(parts)).lower()
    for r in br.records('learnings'):
        v = r.get('value')
        if isinstance(v, dict) and v.get('role') == 'competitor' and v.get('page'):
            key = v['page'].lower().replace(' socks', '').replace(' vermont', '').strip()
            if key in pages:
                pages[key]['median_run_days'] = v.get('median_run_days')
                pages[key]['long_runners_30d'] = v.get('long_runners_30d')
    return sorted(pages.values(), key=lambda p: -(p['active_ads'] or 0))


def subcategory_table(br, ends_on):
    """Each lane: which competitors push it (ads and run length), what launched in it (web pass), whether the brand
    sells it and advertises it, and the verdict: follow, watch or ignore, by the rule constants above."""
    comps = competitor_signals(br)
    fx = web_pass(br) or {}
    launches = fx.get('launches') or []
    words = brand_words(br)
    ads = ad_words(br)
    brand_name = (br.brand if br else '').lower()
    out = []
    for key, label, terms in lanes_for(br):
        pushing = [c for c in comps if any(t in c['text'] for t in terms)]
        long_run = [c for c in pushing if (c.get('longest_run_days') or 0) >= FOLLOW_MIN_RUN_DAYS]
        lane_launches = [l for l in launches if l.get('sub_category') == key or any(t in (l.get('what') or '').lower() for t in terms)]
        theirs = [l for l in lane_launches if (l.get('brand') or '').lower() != brand_name]
        ours = [l for l in lane_launches if (l.get('brand') or '').lower() == brand_name]
        sold = (any(t in words for t in terms) or bool(ours)) if words else None
        advertised = any(t in ads for t in terms) if ads else None
        if len(pushing) >= FOLLOW_MIN_COMPETITORS and long_run:
            verdict = 'follow'
        elif pushing and all((c.get('longest_run_days') or 0) <= IGNORE_MAX_RUN_DAYS for c in pushing) and not theirs:
            verdict = 'ignore'
        elif pushing or theirs:
            verdict = 'watch'
        else:
            verdict = 'ignore'
        out.append({'key': key, 'label': label, 'competitors': [{'name': c['name'], 'active_ads': c['active_ads'], 'longest_run_days': c['longest_run_days'],
                                                                   'long_runners_30d': c.get('long_runners_30d')} for c in pushing],
                    'competitors_n': len(pushing), 'long_run_n': len(long_run),
                    'ads_sum': sum(c['active_ads'] or 0 for c in pushing) if pushing else None,
                    'launches': [{'brand': l.get('brand'), 'what': l.get('what'), 'date': l.get('date'), 'price_usd': l.get('price_usd'),
                                  'url': (l.get('sources') or [{}])[0].get('url')} for l in lane_launches],
                    'launches_theirs': len(theirs), 'launches_ours': len(ours), 'sold': sold, 'advertised': advertised, 'verdict': verdict,
                    'kind': 'proof' if key in PROOF_LANES else 'product',
                    'finding_id': f'{SCREEN}.PROD-R06.{key}'})
    order = {'follow': 0, 'watch': 1, 'ignore': 2}
    out.sort(key=lambda r: (order[r['verdict']], -(r['ads_sum'] or 0)))
    return out


def subcategory_findings(br, ends_on):
    """PROD-R06: a lane 2 or more competitors push with an ad running 30 days or more, that the brand does not name
    in any active ad. Sold or not, it is a gap: brief it or screen it."""
    out = []
    for row in subcategory_table(br, ends_on):
        if row['verdict'] != 'follow' or row['advertised']:
            continue
        top = max(row['competitors'], key=lambda c: c['longest_run_days'] or 0)
        ev = [_ev('competitors_pushing', row['competitors_n'], 'count', ends_on.isoformat(), 'active ads now', FOLLOW_MIN_COMPETITORS, 'threshold',
                  source='brain.competitors', simulated=False, freshness_days=0, names=[c['name'] for c in row['competitors']]),
              _ev('competitor_active_ads', row['ads_sum'], 'count', ends_on.isoformat(), 'active ads now', source='brain.competitors', simulated=False, freshness_days=0),
              _ev('longest_run_days', top['longest_run_days'], 'days', ends_on.isoformat(), 'active ads now', FOLLOW_MIN_RUN_DAYS, 'threshold',
                  source='brain.competitors', simulated=False, freshness_days=0, note=top['name']),
              _ev('our_active_ads_naming_it', 0, 'count', ends_on.isoformat(), 'active ads now', 1, 'threshold', source='brain.learnings', simulated=False, freshness_days=0),
              _ev('launches_24m', row['launches_theirs'], 'count', ends_on.isoformat(), '24 months', source='fixtures.market_trends', simulated=False, freshness_days=0)]
        names = ', '.join(c['name'] for c in row['competitors'][:3])
        if row['kind'] == 'proof':
            sold = 'The brand has the proof on file' if row['sold'] else 'The brand has no proof on file for it'
        else:
            sold = 'The brand sells it' if row['sold'] else 'The brand has no line on file for it'
        sentence = (f'{row["competitors_n"]} competitors push {row["label"].lower()} with {row["ads_sum"]} active ads; {top["name"]} has run one '
                    f'{top["longest_run_days"]} days. {sold} and no active ad names it.')
        f = _finding('PROD-R06', row['key'], ends_on, 'medium', ev, sentence, None, 0.5,
                     [f'{br.brand}.competitors.competitor_set', f'{br.brand}.learnings.hook_types'],
                     money_reason='competitor ads are signals, not proof; no spend or share is measurable')
        f['entity'] = {'type': 'metric', 'id': row['key'], 'label': row['label'], 'sold': row['sold'], 'kind': row['kind'], 'names': names}
        f['id'] = f'{SCREEN}.PROD-R06.{row["key"]}'
        out.append(f)
    return out


# ---------------------------------------------------------------- what people are talking about

# theme vocabulary is the adapter's (app/connectors/apify_adapters.THEMES); ladders name the same themes their way
LADDER_THEME = {'durability': 'durability', 'price_and_value': 'price_value', 'fit_and_sizing': 'fit_sizing',
                'comfort_and_feel': 'comfort', 'order_and_delivery': 'delivery', 'marketplace_trust': 'authenticity',
                'mission_trust': 'mission'}
THEME_LABEL = {'durability': 'Durability and wear life', 'price_value': 'Price and worth', 'fit_sizing': 'Fit and sizing',
               'comfort': 'Comfort and feel', 'delivery': 'Orders and delivery', 'authenticity': 'Marketplace trust',
               'mission': 'Mission and giving', 'general': 'General'}
# what an answer to each theme sounds like in the brand's own claims and ads
ANSWER_WORDS = {'durability': ['guarantee', 'durab', 'lasts', 'lifetime', 'wear life', 'reinforced', 'y-stitched heel'],
                'price_value': ['worth', 'per wear', 'value', 'guarantee', 'lasts'],
                'fit_sizing': ['size guide', 'fit finder', 'stay-up', 'stays up', 'stay up', 'size chart', 'true to size'],
                'comfort': ['comfort', 'soft', 'cushion', 'seamless', 'blister tab', 'arch support'],
                'delivery': ['free shipping', 'ships', 'delivery', 'arrives'],
                'authenticity': ['sold by', 'official', 'authorized', 'brand store'],
                'mission': ['donate', 'donated', 'one purchased', 'give', 'giving']}
CONVERSATION_MIN_VOLUME = 10


def social_pull():
    path = HERE / 'fixtures' / 'social_pull.json'
    return json.loads(path.read_text(encoding='utf-8')) if path.is_file() else None


def conversation(br):
    """One row per theme: volume and sentiment by source (review ladders, Reddit, the social pull), and whether the
    brand answers it on the site (claims, offers, policies) and in its active ads."""
    if br is None:
        return {'rows': [], 'sources': [], 'social': None}
    rows = {}
    for rec in br.records('objection_ladders'):
        v = rec.get('value') or {}
        th = LADDER_THEME.get(v.get('theme') or rec.get('field'))
        if not th:
            continue
        c = v.get('counts') or {}
        r = rows.setdefault(th, {'theme': th, 'label': THEME_LABEL.get(th, th), 'review_complaints': 0, 'review_praise': 0,
                                 'by_source': {}, 'reddit_mentions': 0, 'reddit_upvotes': 0, 'reddit_praise': 0, 'reddit_complaint': 0,
                                 'social_posts': None, 'social_engagement': None, 'social_praise': None, 'social_complaint': None,
                                 'ladder': rec['id'], 'top_rung': None, 'proof_missing': 0})
        r['review_complaints'] += c.get('one_star') or 0
        r['review_praise'] += c.get('five_star') or 0
        for src, n in (c.get('sources') or v.get('sources') or {}).items():
            r['by_source'][src] = r['by_source'].get(src, 0) + (n or 0)
        rungs = v.get('rungs') or []
        if rungs:
            top = max(rungs, key=lambda g: ((g.get('counts') or {}).get('one_star') or 0))
            r['top_rung'] = {'doubt': top.get('doubt'), 'one_star': (top.get('counts') or {}).get('one_star'), 'proof': bool(top.get('proof'))}
            r['proof_missing'] = sum(1 for g in rungs if not g.get('proof'))
    for rec in br.records('language_bank'):
        v = rec.get('value') or {}
        if not v.get('subreddit'):
            continue
        for th in v.get('themes') or ['general']:
            r = rows.setdefault(th, {'theme': th, 'label': THEME_LABEL.get(th, th), 'review_complaints': 0, 'review_praise': 0, 'by_source': {},
                                     'reddit_mentions': 0, 'reddit_upvotes': 0, 'reddit_praise': 0, 'reddit_complaint': 0,
                                     'social_posts': None, 'social_engagement': None, 'social_praise': None, 'social_complaint': None,
                                     'ladder': None, 'top_rung': None, 'proof_missing': 0})
            r['reddit_mentions'] += 1
            r['reddit_upvotes'] += v.get('weight') or 0
            if v.get('theme') == 'praise':
                r['reddit_praise'] += 1
            elif v.get('theme') == 'complaint':
                r['reddit_complaint'] += 1
    social = social_pull_for(br)
    for th, g in ((social or {}).get('themes') or {}).items():
        r = rows.get(th)
        if r is None:
            continue
        r['social_posts'] = g.get('posts')
        r['social_engagement'] = (g.get('likes') or 0) + (g.get('comments') or 0)
        r['social_praise'] = g.get('praise')
        r['social_complaint'] = g.get('complaint')
    site = brand_words(br)
    ads = ad_words(br)
    out = []
    for th, r in rows.items():
        words = ANSWER_WORDS.get(th, [th])
        r['answered_on_site'] = any(w in site for w in words) if site else None
        r['answered_in_ads'] = any(w in ads for w in words) if ads else None
        tot = r['review_complaints'] + r['review_praise']
        r['praise_share'] = round(r['review_praise'] / tot, 4) if tot else None
        r['volume'] = tot + r['reddit_mentions'] + (r['social_posts'] or 0)
        r['complaint_led'] = tot >= CONVERSATION_MIN_VOLUME and r['review_complaints'] > r['review_praise']
        r['verdict'] = ('gap' if r['complaint_led'] and not r['answered_in_ads'] else 'answered' if r['complaint_led'] else
                        'strength' if r['praise_share'] is not None and r['praise_share'] >= 0.7 else 'watch')
        r['finding_id'] = f'{SCREEN}.PROD-R07.{th}'
        out.append(r)
    out.sort(key=lambda r: (-(1 if r['verdict'] == 'gap' else 0), -r['volume']))
    srcs = sorted({s for r in out for s in r['by_source']})
    return {'rows': out, 'sources': srcs, 'social': {k: social[k] for k in ('captured_at', 'mode', 'actor', 'run_id', 'usd', 'estimate_usd', 'hashtags', 'items', 'co_hashtags', 'samples', 'note') if k in social} if social else None}


def conversation_findings(br, ends_on):
    """PROD-R07: a theme with 10 or more review quotes, more complaints than praise, and no active ad that answers it."""
    out = []
    for r in conversation(br)['rows']:
        if r['verdict'] != 'gap':
            continue
        srcs = ', '.join(f'{k} {v}' for k, v in sorted(r['by_source'].items(), key=lambda kv: -kv[1]) if v)
        ev = [_ev('complaint_quotes', r['review_complaints'], 'count', ends_on.isoformat(), 'all reviews to capture', r['review_praise'], 'threshold',
                  source=r['ladder'] or 'brain.objection_ladders', simulated=False, freshness_days=0, note='baseline is the praise count on the same theme; sources: ' + srcs),
              _ev('praise_share', r['praise_share'], 'ratio', ends_on.isoformat(), 'all reviews to capture', 0.5, 'threshold', source=r['ladder'] or 'brain.objection_ladders', simulated=False, freshness_days=0),
              _ev('reddit_mentions', r['reddit_mentions'], 'count', ends_on.isoformat(), 'past year', source='brain.language_bank', simulated=False, freshness_days=0, upvotes=r['reddit_upvotes']),
              _ev('active_ads_answering', 0, 'count', ends_on.isoformat(), 'active ads now', 1, 'threshold', source='brain.learnings', simulated=False, freshness_days=0)]
        if r['social_posts'] is not None:
            ev.append(_ev('social_posts', r['social_posts'], 'count', ends_on.isoformat(), 'hashtag pull', source='fixtures.social_pull', simulated=False, freshness_days=0,
                          engagement=r['social_engagement']))
        rung = r.get('top_rung') or {}
        site = 'The site answers it' if r['answered_on_site'] else 'Nothing on the site answers it'
        sentence = (f'{r["label"]}: {r["review_complaints"]} complaint quotes against {r["review_praise"]} praise across reviews and Reddit. '
                    f'{site} and no active ad does.')
        if rung.get('doubt'):
            sentence = sentence[:-1] + f'. The top doubt is "{rung["doubt"]}" ({rung.get("one_star")} one-star).'
        f = _finding('PROD-R07', r['theme'], ends_on, 'medium', ev, sentence, None, 0.7, [x for x in [r['ladder'], f'{br.brand}.learnings.hook_types'] if x],
                     money_reason='lost orders from an unanswered doubt are not measurable without a test')
        f['entity'] = {'type': 'ladder_rung', 'id': r['theme'], 'label': r['label'], 'answered_on_site': r['answered_on_site'], 'doubt': rung.get('doubt')}
        f['id'] = f'{SCREEN}.PROD-R07.{r["theme"]}'
        out.append(f)
    return out


# ---------------------------------------------------------------- shifting preferences

# what each preference sounds like in a claim, an ad or a competitor's pitch
PREFERENCE_WORDS = {'sustainability': ['sustainab', 'recycled', 'b corp', 'organic', 'carbon', 'planet'],
                    'natural_fibres': ['cotton', 'merino', 'wool', 'natural fib', 'natural material'],
                    'durability': ['guarantee', 'durab', 'lasts', 'lifetime', 'wear life', 'buy it for life'],
                    'giving': ['donate', 'donated', 'one purchased', 'give back', 'giving', 'mission'],
                    'made_in_usa': ['made in usa', 'made in the usa', 'made in vermont', 'american made', 'made in america'],
                    'secondhand_resale': ['resale', 'secondhand', 'second hand', 'pre-owned', 'take back', 'recycl'],
                    'compression_wellness': ['compression', 'circulation', 'relief', 'mmhg'],
                    'gifting': ['gift']}
PREFERENCE_THEME = {'durability': 'durability', 'giving': 'mission', 'compression_wellness': 'comfort'}


def preferences(br, conv=None):
    """Each rising preference from the web pass against the brand's own claims (site), its active ads, the
    competitors' pitches and the category conversation. Verdict by rule: lead, prove, gap, watch."""
    fx = web_pass(br) or {}
    site = brand_words(br)
    ads = ad_words(br)
    comps = competitor_signals(br)
    themes = {r['theme']: r for r in (conv or conversation(br))['rows']} if br else {}
    out = []
    for p in fx.get('preferences') or []:
        key = p.get('key')
        words = PREFERENCE_WORDS.get(key, [key or ''])
        on_site = any(w in site for w in words) if site else None
        in_ads = any(w in ads for w in words) if ads else None
        rivals = [c['name'] for c in comps if any(w in c['text'] for w in words)]
        th = themes.get(PREFERENCE_THEME.get(key, ''))
        rising = p.get('direction') in ('up', 'flat')
        if on_site and in_ads:
            verdict = 'lead'
        elif on_site and rising:
            verdict = 'prove'
        elif not on_site and rising and rivals:
            verdict = 'gap'
        else:
            verdict = 'watch'
        src = (p.get('sources') or [{}])[0]
        out.append({'key': key, 'label': p.get('label'), 'direction': p.get('direction'), 'evidence': p.get('evidence'),
                    'cite': f"{src.get('publisher') or 'public source'}, {src.get('date') or 'undated'}", 'url': src.get('url'), 'sources': p.get('sources') or [],
                    'on_site': on_site, 'in_ads': in_ads, 'competitors': rivals,
                    'conversation': {'complaints': th['review_complaints'], 'praise': th['review_praise'], 'reddit': th['reddit_mentions']} if th else None,
                    'verdict': verdict, 'finding_id': f'{SCREEN}.PROD-R08.{key}'})
    order = {'gap': 0, 'prove': 1, 'lead': 2, 'watch': 3}
    out.sort(key=lambda r: (order[r['verdict']], r['label'] or ''))
    return out


def preference_findings(br, ends_on):
    """PROD-R08: a preference rising or holding in public surveys that competitors claim and the brand's own
    records do not. The fix is a claim plan or a counter-position, never an invented claim."""
    out = []
    for r in preferences(br):
        if r['verdict'] != 'gap':
            continue
        ev = [_ev('preference_direction', 1 if r['direction'] == 'up' else 0, 'flag', ends_on.isoformat(), 'public surveys', source=r['url'], simulated=False,
                  freshness_days=0, note=r['evidence'], cite=r['cite']),
              _ev('competitors_claiming_it', len(r['competitors']), 'count', ends_on.isoformat(), 'active ads now', 1, 'threshold', source='brain.competitors',
                  simulated=False, freshness_days=0, names=r['competitors']),
              _ev('own_records_claiming_it', 0, 'count', ends_on.isoformat(), 'brain now', 1, 'threshold', source='brain.claims', simulated=False, freshness_days=0)]
        sentence = (f'{r["label"]}: {r["evidence"]} ({r["cite"]}). {", ".join(r["competitors"][:3])} claim it and no record of ours does.')
        f = _finding('PROD-R08', r['key'], ends_on, 'medium', ev, sentence, None, 0.5, [f'{br.brand}.claims.brand_positioning', f'{br.brand}.positioning.proof_points'],
                     money_reason='a preference gap has no order count until a test runs')
        f['entity'] = {'type': 'metric', 'id': r['key'], 'label': r['label'], 'names': ', '.join(r['competitors'][:3])}
        f['id'] = f'{SCREEN}.PROD-R08.{r["key"]}'
        out.append(f)
    return out


# ---------------------------------------------------------------- the positioning map

PROOF_WORDS = ['guarantee', 'lab tested', 'review quote', 'review', 'testimonial', 'made in usa', 'number one', 'nurse count',
               'social proof', 'athlete', 'clinically', 'doctor', 'proof', 'demo', 'wear test', 'tested']
MAP_MIN_POINTS = 3


def proof_share(hooks):
    """Share of hook types that carry proof (guarantee, lab, review, testimonial, made in USA). Hooks: list or dict of type names."""
    names = list(hooks.keys()) if isinstance(hooks, dict) else list(hooks or [])
    if not names:
        return None
    proof = sum(1 for h in names if any(w in str(h).lower() for w in PROOF_WORDS))
    return round(proof / len(names), 4)


def our_price_per_pair(prods, br):
    """Median per-pair sock list price from the catalog when connected; else the brain's entry price for a single pair."""
    if prods:
        per = [p['price'] / p['items_per_unit'] for p in prods if p.get('category') == 'socks' and p.get('price') and p.get('items_per_unit')]
        if per:
            return {'value': round(statistics.median(per), 2), 'basis': 'median list price per pair across sock packs, simulated catalog'}
    v = br.get(f'{br.brand}.products.price_ladder_socks') if br else None
    if v and isinstance(v.get('value'), dict) and v['value'].get('min_usd'):
        return {'value': float(v['value']['min_usd']), 'basis': 'entry price of a single pair in the public catalog (catalog not connected)'}
    return {'value': None, 'basis': 'no catalog and no price ladder on file'}


def positioning_map(br, prods):
    """Us and the competitor pages as points: x price per pair (median), y proof share of hook types, size active ads.
    Pages without a price band are listed apart, never guessed."""
    if br is None:
        return {'points': [], 'unpriced': [], 'x': None, 'y': None}
    from_named = {}
    for rec in br.records('competitors'):
        v = rec.get('value')
        if not isinstance(v, dict) or not v.get('name') or 'hook_types' not in v:
            continue
        text = v.get('price_band_usd') or ''
        med = re.search(r'median (?:about )?(\d+(?:\.\d+)?)', text)
        from_named[v['name'].lower().replace(' socks', '').replace(' vermont', '').strip()] = {
            'label': v['name'], 'x': float(med.group(1)) if med else None, 'y': proof_share(v.get('hook_types')),
            'hooks': list(v.get('hook_types') or []), 'record': rec['id'], 'price_ref': v.get('price_ref')}
    pages = {c['name'].lower().replace(' socks', '').replace(' vermont', '').strip(): c for c in competitor_signals(br)}
    points, unpriced = [], []
    for key, c in pages.items():
        n = from_named.get(key)
        p = {'label': n['label'] if n else c['name'], 'x': n['x'] if n else None, 'y': n['y'] if n else None, 'size': c['active_ads'],
             'us': False, 'hooks': n['hooks'] if n else [], 'longest_run_days': c['longest_run_days'], 'records': c['records']}
        (points if p['x'] is not None and p['y'] is not None else unpriced).append(p)
    hooks = brain_value_hooks(br)
    price = our_price_per_pair(prods, br)
    own = br.get(f'{br.brand}.learnings.active_ads_snapshot')
    ours = {'label': br.brand.title(), 'x': price['value'], 'y': proof_share(hooks), 'size': (own or {}).get('value', {}).get('active_ads') if own else None,
            'us': True, 'hooks': list(hooks or []), 'price_basis': price['basis'], 'note': price['basis']}
    if ours['x'] is not None and ours['y'] is not None:
        points.append(ours)
    xs = [p['x'] for p in points if not p['us']]
    ys = [p['y'] for p in points if not p['us']]
    mid_x = statistics.median(xs) if xs else None
    mid_y = statistics.median(ys) if ys else None
    quads = {'tl': [], 'tr': [], 'bl': [], 'br': []}
    for p in points:
        if mid_x is None or mid_y is None:
            break
        q = ('t' if p['y'] >= mid_y else 'b') + ('l' if p['x'] < mid_x else 'r')
        quads[q].append(p['label'])
    names = {'tl': 'value with proof', 'tr': 'premium with proof', 'bl': 'value on feel', 'br': 'premium on feel'}
    empty = [q for q, members in quads.items() if not members] if xs else []
    return {'points': points, 'unpriced': unpriced, 'ours': ours, 'mid_x': mid_x, 'mid_y': mid_y, 'quadrants': names, 'members': quads,
            'empty': empty, 'x': {'label': 'price per pair, median', 'unit': '$'}, 'y': {'label': 'share of hook types that carry proof', 'unit': '%'},
            'proof_words': PROOF_WORDS, 'enough': len(points) >= MAP_MIN_POINTS}


def brain_value_hooks(br):
    r = br.get(f'{br.brand}.learnings.hook_types') if br else None
    return (r or {}).get('value') if r else None


def reddit_frames(br):
    """The category frames Reddit uses and who it recommends instead, from the brain's positioning and competitor records."""
    frames, instead = [], []
    if br is None:
        return frames, instead
    for r in br.records('positioning'):
        v = r.get('value')
        if isinstance(v, dict) and v.get('frame') and 'mentions' in v:
            frames.append({'frame': v['frame'], 'mentions': v.get('mentions') or 0, 'mentions_brand': v.get('mentions_brand') or 0, 'record': r['id']})
    for r in br.records('competitors'):
        v = r.get('value')
        if isinstance(v, dict) and v.get('recommended_instead'):
            instead.append({'competitor': v.get('competitor'), 'n': v['recommended_instead'], 'upvotes': v.get('upvotes') or 0, 'record': r['id']})
    frames.sort(key=lambda f: -f['mentions'])
    instead.sort(key=lambda f: (-f['n'], -f['upvotes']))
    return frames, instead


def positioning_findings(br, prods, ends_on):
    """PROD-R09: the category conversation is framed by a proof word (buy it for life, worth the price) the brand
    is not named in, a competitor is recommended instead, and our ads carry proof in fewer hook types than the
    competitor median. One finding for the brand."""
    if br is None:
        return []
    frames, instead = reddit_frames(br)
    m = positioning_map(br, prods)
    ours = m.get('ours') or {}
    top = frames[0] if frames else None
    if not top or top['mentions'] < 3 or top['mentions_brand'] > 0 or not instead:
        return []
    if ours.get('y') is None or m.get('mid_y') is None or ours['y'] >= m['mid_y']:
        return []
    lead = instead[0]
    ev = [_ev('frame_mentions', top['mentions'], 'count', ends_on.isoformat(), 'past year', 3, 'threshold', source=top['record'], simulated=False, freshness_days=0,
              frame=top['frame'], mentions_brand=top['mentions_brand']),
          _ev('recommended_instead', lead['n'], 'count', ends_on.isoformat(), 'past year', source=lead['record'], simulated=False, freshness_days=0,
              competitor=lead['competitor'], upvotes=lead['upvotes']),
          _ev('proof_share_of_hooks', ours['y'], 'ratio', ends_on.isoformat(), 'active ads now', m['mid_y'], 'peer_band', source=f'{br.brand}.learnings.hook_types',
              simulated=False, freshness_days=0, note='baseline is the median across competitor pages with a price band'),
          _ev('price_per_pair', ours.get('x'), 'usd', ends_on.isoformat(), 'catalog', m.get('mid_x'), 'peer_band', source='products', simulated=prods is not None, freshness_days=0,
              note=ours.get('price_basis'))]
    frame = top['frame'].replace('_', ' ')
    sentence = (f'Reddit frames the category as "{frame}" in {top["mentions"]} posts and never names the brand in it. {lead["competitor"]} is recommended instead '
                f'{lead["n"]} times ({lead["upvotes"]} upvotes). Our ads carry proof in {round(ours["y"] * 100)} percent of hook types against a competitor median of {round(m["mid_y"] * 100)}.')
    empty = [m['quadrants'][q] for q in m.get('empty') or []]
    f = _finding('PROD-R09', 'brand', ends_on, 'high', ev, sentence, None, 0.7,
                 [top['record'], lead['record'], f'{br.brand}.positioning.proof_points', f'{br.brand}.learnings.hook_types'],
                 money_reason='a positioning gap has no order count until the proof runs in an ad')
    f['entity'] = {'type': 'brand', 'id': 'brand', 'label': 'Positioning', 'frame': frame, 'competitor': lead['competitor'], 'empty_quadrants': empty,
                   'proof_share': ours['y'], 'peer_proof_share': m['mid_y']}
    f['id'] = f'{SCREEN}.PROD-R09.brand'
    return [f]


# ---------------------------------------------------------------- avatars by line: served and not served

# line groups are a fixed structure; which ones exist for a brand comes from products.lines in the brain
LINE_GROUPS = [('socks', 'Socks', ['sock']), ('underwear', 'Underwear', ['underwear', 'boxer', 'brief', 'bralette', 'thong', 'hipster']),
               ('tshirts', 'T-shirts', ['t-shirt', 'tshirt', ' tee', 'shirt']), ('slippers', 'Slippers', ['slipper', 'bootie']),
               ('footwear', 'Footwear', ['clog', 'moccasin', 'sandal', 'slip-on', 'shoe', 'sneaker', 'boot']),
               ('gifting', 'Gifts and gift cards', ['gift'])]
STOP = set('the and for that with from into over under after before when than then this these those their there them they its our your his her '
           'she he who what which where while about above after again against all any are been being between both but can did does doing down '
           'during each few had has have having here how just more most not now off once only other out own same some such too very was were will '
           'would you socks sock clothing brand brands pair pairs buying buy order orders one first new like size sizes wear wearing day'.split())
AVATAR_MIN_WORDS = 2
UNDER_SERVED_MIN_SHARE = 0.10


def avatar_words(v):
    """Distinctive words of an avatar from its job, triggers and pains: lower case, 5 letters or more, no stop words."""
    text = ' '.join([str(v.get('job') or ''), ' '.join(v.get('triggers') or []), ' '.join(v.get('pains') or []), str(v.get('situation') or '')]).lower()
    words = {w.strip('.,;:()"\'') for w in re.split(r'[\s/]+', text)}
    return sorted(w for w in words if len(w) >= 5 and w not in STOP and w.isalpha())


def avatar_coverage(br, prods=None):
    """Rows: avatars from the brain. Cols: the brand's line groups. Cell us: the avatar's own evidence and text that
    names the line (quotes and records). Cell them: competitor pages whose pitch carries 2 or more of the avatar's
    words and names the line. Avatars with no line evidence anywhere are not served by anything we can point at."""
    if br is None:
        return {'rows': [], 'cols': [], 'cells': {}}
    lines = [l.lower() for l in (brain_value_lines(br) or [])]
    line_text = ' '.join(lines) + ' ' + brand_words(br)
    cols = [{'key': k, 'label': lab, 'terms': t} for k, lab, t in LINE_GROUPS if any(term in line_text for term in t)]
    comps = competitor_signals(br)
    themes = {r['theme']: r for r in conversation(br)['rows']}
    from_ads = ad_words(br)
    rows, cells = [], {}
    for rec in br.records('avatars'):
        v = rec.get('value') or {}
        name = v.get('name') or (v.get('situation') or rec.get('field') or '').replace('_', ' ').title()
        words = avatar_words(v)
        quotes = [str(e.get('quote') or '') for e in rec.get('evidence') or []]
        own_text = (' '.join(quotes) + ' ' + str(rec.get('text') or '') + ' ' + json.dumps(v)).lower()
        served = [c for c in comps if sum(1 for w in words if w in c['text']) >= AVATAR_MIN_WORDS]
        row_cells = {}
        total_us = 0
        for c in cols:
            us = sum(1 for q in quotes if any(t in q.lower() for t in c['terms'])) + (1 if any(t in own_text for t in c['terms']) else 0)
            them = sum(1 for s in served if any(t in s['text'] for t in c['terms']))
            if us or them:
                row_cells[c['key']] = {'us': us, 'them': them, 'unit': 'n', 'n': len(quotes)}
            total_us += us
        # the theme the avatar lives on: the adapter's theme words counted in its job, pains and triggers (not its quotes)
        theme_row = themes.get(avatar_theme(v) or '')
        in_ads = any(w in from_ads for w in words[:12]) if from_ads else None
        rows.append({'key': rec['id'].split('.')[-1], 'record': rec['id'], 'label': name, 'share': v.get('share_estimate'), 'intensity': v.get('intensity'),
                     'job': v.get('job'), 'words': words[:12], 'quotes': len(quotes), 'served_by': [c['name'] for c in served],
                     'lines_us': total_us, 'in_ads': in_ads, 'theme': theme_row['theme'] if theme_row else None,
                     'theme_verdict': theme_row['verdict'] if theme_row else None,
                     'complaint_share': (round(1 - theme_row['praise_share'], 4) if theme_row and theme_row.get('praise_share') is not None else None),
                     'not_served': total_us == 0, 'finding_id': None})
        cells[rec['id'].split('.')[-1]] = row_cells
    rows.sort(key=lambda r: (-(r['share'] or 0), r['label']))
    return {'rows': rows, 'cols': [{'key': c['key'], 'label': c['label']} for c in cols], 'cells': cells,
            'competitors': [c['name'] for c in comps], 'note': 'us: the avatar\'s own quotes and records that name the line; them: competitor pages whose pitch carries 2 or more of the avatar\'s words and names the line'}


GENERIC_THEME_TERMS = {'last', 'lasted', 'small', 'large', 'fine', 'sale', 'opened'}
EXTRA_THEME_TERMS = {'durability': ['hole', 'holes', 'shedding', 'pilling', 'wear out', 'fall apart', 'hold up', 'go thin'],
                     'fit_sizing': ['size chart', 'fit', 'slip', 'ride down', 'tight', 'pull on'],
                     'price_value': ['price', 'cheaper', 'worth', 'premium', 'per-pair', 'per pair', 'multi-pack'],
                     'delivery': ['arriv', 'mis-shipped', 'missing order', 'on time'],
                     'comfort': ['comfort', 'seam', 'rub', 'pinch', 'foot pain', 'warm'],
                     'mission': ['giving', 'donat', 'mission']}


def avatar_theme(v):
    """The theme with the most term hits in the avatar's job, pains and triggers, or None."""
    try:
        from app.connectors.apify_adapters import THEMES  # noqa: WPS433
    except Exception:  # noqa: BLE001
        THEMES = {}
    text = ' ' + ' '.join([str(v.get('job') or ''), ' '.join(v.get('pains') or []), ' '.join(v.get('triggers') or [])]).lower() + ' '
    best, best_n = None, 0
    for th in sorted(set(THEMES) | set(EXTRA_THEME_TERMS)):   # sorted: a tie breaks the same way in every process
        terms = [t for t in (THEMES.get(th) or []) if t not in GENERIC_THEME_TERMS] + EXTRA_THEME_TERMS.get(th, [])
        n = sum(1 for t in terms if t in text)
        if n > best_n:
            best, best_n = th, n
    return best


def brain_value_num(br, rid):
    r = br.get(rid) if br else None
    v = (r or {}).get('value') if r else None
    return float(v) if isinstance(v, (int, float)) else None


def brain_value_lines(br):
    r = br.get(f'{br.brand}.products.lines') if br else None
    return (r or {}).get('value') if r else None


def avatar_findings(br, ends_on, net_28d_value, prods=None):
    """PROD-R10: an avatar the brain holds with no line evidence on our side and a competitor serving it.
    PROD-R11: an avatar with 10 percent or more of buyers (or high intensity) whose theme is complaint-led;
    money = share x 28-day net revenue x complaint share of the theme's quotes."""
    out = []
    cov = avatar_coverage(br, prods)
    for r in cov['rows']:
        rid = r['key']
        if r['not_served'] and r['served_by']:
            ev = [_ev('own_line_evidence', 0, 'count', ends_on.isoformat(), 'brain now', 1, 'threshold', source=r['record'], simulated=False, freshness_days=0),
                  _ev('competitors_serving', len(r['served_by']), 'count', ends_on.isoformat(), 'active ads now', source='brain.competitors', simulated=False, freshness_days=0, names=r['served_by'])]
            sentence = (f'{r["label"]} is in the brain with no record or quote that ties them to a line we sell. {", ".join(r["served_by"][:3])} pitch to them.')
            f = _finding('PROD-R10', rid, ends_on, 'medium', ev, sentence, None, 0.5, [r['record']], money_reason='no line evidence, so no order count')
            f['entity'] = {'type': 'brand', 'id': rid, 'label': r['label'], 'names': ', '.join(r['served_by'][:3]), 'job': r['job']}
            f['id'] = f'{SCREEN}.PROD-R10.{rid}'
            out.append(f)
            r['finding_id'] = f['id']
            continue
        big = (r['share'] or 0) >= UNDER_SERVED_MIN_SHARE or r['intensity'] == 'high'
        if big and r['theme_verdict'] == 'gap' and r['complaint_share'] is not None:
            stake = None
            reason = None
            repeat = brain_value_num(br, f'{br.brand}.economics.repeat_rate_12m')
            if net_28d_value and r['share'] and repeat:
                usd = round(r['share'] * net_28d_value * r['complaint_share'] * repeat)
                stake = {'usd': usd, 'formula': 'share_estimate * net_revenue_28d * complaint_share_of_theme * repeat_rate_12m',
                         'inputs': {'share_estimate': r['share'], 'net_revenue_28d': round(net_28d_value, 2), 'complaint_share_of_theme': r['complaint_share'],
                                    'repeat_rate_12m': repeat}, 'window': '28d'}
            else:
                reason = ('no share estimate for this avatar' if not r['share'] else 'net revenue for 28 days unavailable' if not net_28d_value
                          else 'no repeat rate in the brain (economics.repeat_rate_12m)')
            th = THEME_LABEL.get(r['theme'], r['theme'])
            ev = [_ev('share_estimate', r['share'], 'ratio', ends_on.isoformat(), 'brain now', UNDER_SERVED_MIN_SHARE, 'threshold', source=r['record'], simulated=False, freshness_days=0, intensity=r['intensity']),
                  _ev('complaint_share_of_theme', r['complaint_share'], 'ratio', ends_on.isoformat(), 'all reviews to capture', 0.5, 'threshold', source='brain.objection_ladders', simulated=False, freshness_days=0, theme=r['theme']),
                  _ev('net_revenue_28d', round(net_28d_value, 2) if net_28d_value else None, 'usd', ends_on.isoformat(), '28d'),
                  _ev('in_active_ads', 1 if r['in_ads'] else 0, 'flag', ends_on.isoformat(), 'active ads now', 1, 'threshold', source='brain.learnings', simulated=False, freshness_days=0)]
            sentence = (f'{r["label"]}: about {round(r["share"] * 100)} percent of buyers with {r["intensity"]} intensity. Their theme, {th.lower()}, is '
                        f'{round(r["complaint_share"] * 100)} percent complaint quotes' + (' and no active ad speaks to them.' if not r['in_ads'] else '.'))
            sev = _severity(stake['usd'] if stake else None, net_28d_value, 1)
            sev = 'high' if sev == 'critical' else sev   # a structural gap, not a break in the buy path
            f = _finding('PROD-R11', rid, ends_on, sev, ev, sentence, stake, 0.5, [r['record'], f'{br.brand}.economics.repeat_rate_12m'], reason)
            f['entity'] = {'type': 'brand', 'id': rid, 'label': r['label'], 'theme': r['theme'], 'job': r['job'], 'in_ads': r['in_ads']}
            f['id'] = f'{SCREEN}.PROD-R11.{rid}'
            out.append(f)
            r['finding_id'] = f['id']
    return out


# ---------------------------------------------------------------- search terms for the brand and the industry

SEARCH_GROUPS = [('brand', 'Brand terms'), ('category', 'Category terms'), ('competitor', 'Competitor and versus terms'), ('problem', 'Problem and question terms')]
SEARCH_WINDOW_DAYS = 28
PAGE_WORDS = {'problem': ['size-guide', 'sock-tech', 'fit', 'faq', 'guarantee', 'returns', 'shipping', 'care'],
              'brand': ['about', 'giving', 'b-corp', 'donated', 'sustainability'],
              'category': ['collections', 'socks', 'underwear', 'slippers'],
              'competitor': ['compare', 'vs', 'why-bombas', 'difference']}


def search_groups(br):
    """Term groups from the brain: brand (identity), category (lines and materials), competitor (names and versus),
    problem (the ladder rung doubts, the brand's own Reddit searches, the Reddit questions in seo_facts)."""
    if br is None:
        return []
    brand = br.brand.lower()
    lines = [str(l).lower() for l in (brain_value_lines(br) or []) if str(l).lower() not in ('giftcard', 'bags')]
    mats = br.get(f'{brand}.products.materials')
    mats = [str(m).lower().split('/')[0] for m in ((mats or {}).get('value') or [])] if mats else []
    comps = [c['name'] for c in competitor_signals(br)]
    reddit_inst = [i['competitor'] for i in reddit_frames(br)[1]]
    doubts = []
    for rec in br.records('objection_ladders'):
        for g in (rec.get('value') or {}).get('rungs') or []:
            if g.get('doubt'):
                doubts.append(g['doubt'])
    cfg_path = APP / 'brain' / br.brand / 'config' / 'apify.json'
    searches = []
    if cfg_path.is_file():
        searches = list((json.loads(cfg_path.read_text(encoding='utf-8')).get('reddit') or {}).get('searches') or [])
    questions = [((r.get('value') or {}).get('question'), (r.get('value') or {}).get('upvotes'), (r.get('value') or {}).get('subreddit'))
                 for r in br.records('seo_facts') if (r.get('value') or {}).get('question')]
    cat_terms = [f'{l}' for l in lines[:8]] + [f'{m} socks' for m in mats[:4]]
    groups = [
        {'key': 'brand', 'terms': [brand, f'{brand} socks', f'{brand} review', f'{brand} sale', f'{brand} promo code'] + [f'{brand} {l}' for l in lines[:4]],
         'match': [brand]},
        {'key': 'category', 'terms': cat_terms + ['best socks', 'comfortable socks'], 'match': [l.rstrip('s') for l in lines] + mats + ['sock']},
        {'key': 'competitor', 'terms': [f'{brand} vs {c.lower()}' for c in (reddit_inst + comps)[:6]] + [c.lower() for c in comps[:6]], 'match': [c.lower().split(' ')[0] for c in comps + reddit_inst] + [' vs ']},
        {'key': 'problem', 'terms': [s for s in searches if brand not in s.lower()] + doubts[:8], 'match': ['hole', 'slip', 'stay up', 'worth', 'size', 'tight', 'pill', 'shrink', 'itch', 'blister', 'sweat', 'warm', 'how ', 'why ', 'best ', 'do ', 'does ']},
    ]
    labels = dict(SEARCH_GROUPS)
    for g in groups:
        g['label'] = labels[g['key']]
        g['terms'] = list(dict.fromkeys(t for t in g['terms'] if t))
    return groups, questions


def site_pages(br):
    """Every url the brain's site map holds, flat."""
    urls = []
    if br is None:
        return urls
    for r in br.records('site_map'):
        v = r.get('value')
        if isinstance(v, dict) and v.get('url'):
            urls.append(v['url'])
        elif isinstance(v, list):
            urls += [x.get('url') for x in v if isinstance(x, dict) and x.get('url')]
    return urls


def group_of(query, groups):
    q = ' ' + str(query or '').lower() + ' '
    for key in ('brand', 'competitor', 'problem', 'category'):
        g = next(x for x in groups if x['key'] == key)
        if any(m and m in q for m in g['match']):
            return key
    return None


def search_demand(data, brand, groups, ends_on):
    """Search Console and Google search-term rows summed per group over 28 days. Unavailable, never 0, when a table is absent."""
    source = brand_data(brand) if brand else data
    out = {g['key']: {'impressions': None, 'clicks': None, 'position': None, 'queries': 0, 'top': [], 'paid_spend': None, 'paid_clicks': None, 'paid_conversions': None} for g in groups}
    start = (ends_on - timedelta(days=SEARCH_WINDOW_DAYS - 1)).isoformat()
    organic = paid = None
    try:
        rows = source.table('search_console')
        organic = {k: {'imp': 0, 'clk': 0, 'pos': [], 'q': {}} for k in out}
        for r in rows:
            d = str(r.get('date') or '')[:10]
            if d and not (start <= d <= ends_on.isoformat()):
                continue
            k = group_of(r.get('query'), groups)
            if not k:
                continue
            o = organic[k]
            o['imp'] += r.get('impressions') or 0
            o['clk'] += r.get('clicks') or 0
            if r.get('position') is not None:
                o['pos'].append((r['position'], r.get('impressions') or 0))
            o['q'][r.get('query')] = o['q'].get(r.get('query'), 0) + (r.get('impressions') or 0)
        for k, o in organic.items():
            out[k].update(impressions=o['imp'], clicks=o['clk'], queries=len(o['q']), top=sorted(o['q'].items(), key=lambda kv: -kv[1])[:5],
                          position=round(sum(p * w for p, w in o['pos']) / sum(w for _, w in o['pos']), 1) if o['pos'] and sum(w for _, w in o['pos']) else None)
    except (KeyError, ValueError):
        organic = None
    try:
        rows = source.table('google_rows')
        paid = {k: {'spend': 0.0, 'clk': 0, 'conv': 0.0} for k in out}
        for r in rows:
            if not r.get('search_term'):
                continue
            d = str(r.get('date') or '')[:10]
            if d and not (start <= d <= ends_on.isoformat()):
                continue
            k = group_of(r.get('search_term'), groups)
            if not k:
                continue
            paid[k]['spend'] += r.get('spend') or 0
            paid[k]['clk'] += r.get('clicks') or 0
            paid[k]['conv'] += r.get('conversions') or 0
        for k, p in paid.items():
            out[k].update(paid_spend=round(p['spend'], 2), paid_clicks=p['clk'], paid_conversions=round(p['conv'], 1))
    except (KeyError, ValueError):
        paid = None
    return out, {'organic': organic is not None, 'paid': paid is not None, 'window_days': SEARCH_WINDOW_DAYS}


def search_table(br, data, brand, ends_on):
    if br is None:
        return {'groups': [], 'questions': [], 'available': {'organic': False, 'paid': False}}
    groups, questions = search_groups(br)
    demand, avail = search_demand(data, brand, groups, ends_on)
    pages = site_pages(br)
    for g in groups:
        g.update(demand[g['key']])
        g['pages'] = [u for u in pages if any(w in u.lower() for w in PAGE_WORDS.get(g['key'], []))]
        g['finding_id'] = f'{SCREEN}.PROD-R13.{g["key"]}'
    return {'groups': groups, 'questions': [{'question': q, 'upvotes': u, 'subreddit': s} for q, u, s in questions], 'available': avail, 'pages_known': len(pages)}


def search_findings(br, data, brand, ends_on):
    """PROD-R12: no search data connected (one connect finding). PROD-R13: a term group with impressions in the
    window and no answering page in the brain's site map (only when the data is there)."""
    if br is None:
        return []
    t = search_table(br, data, brand, ends_on)
    out = []
    if not t['available']['organic']:
        out.append(_unavailable('PROD-R12', ends_on, 'Search Console is not connected, so search demand for the brand and the category cannot be read.',
                                ['search_console'], 'google_search_console', 'Connect Search Console (read only) in Setup.'))
        out[-1]['entity'] = {'type': 'brand', 'id': 'brand', 'label': 'Search demand'}
        return out
    for g in t['groups']:
        if (g.get('impressions') or 0) > 0 and not g['pages']:
            ev = [_ev('impressions', g['impressions'], 'count', ends_on.isoformat(), f'{SEARCH_WINDOW_DAYS}d', 1, 'threshold', source='search_console'),
                  _ev('clicks', g['clicks'], 'count', ends_on.isoformat(), f'{SEARCH_WINDOW_DAYS}d', source='search_console'),
                  _ev('answering_pages', 0, 'count', ends_on.isoformat(), 'site map now', 1, 'threshold', source='brain.site_map', simulated=False, freshness_days=0)]
            sentence = (f'{g["label"]} drew {g["impressions"]:,} impressions and {g["clicks"]:,} clicks in {SEARCH_WINDOW_DAYS} days. '
                        f'No page in the site map answers them.')
            f = _finding('PROD-R13', g['key'], ends_on, 'medium', ev, sentence, None, 0.5, [f'{br.brand}.site_map.facts_pages'], money_reason='no conversion value per click on file')
            f['entity'] = {'type': 'page', 'id': g['key'], 'label': g['label'], 'terms': g['terms'][:5]}
            f['id'] = f'{SCREEN}.PROD-R13.{g["key"]}'
            out.append(f)
    return out


# ---------------------------------------------------------------- the margin gate per candidate

CATEGORY_SKU_PREFIX = {'BMB-SK': 'socks', 'BMB-UW': 'underwear', 'BMB-TS': 'tshirts', 'BMB-SL': 'slippers', 'BMB-FW': 'footwear'}
BANK_DOLLAR_FLOOR = 30.0     # idea PRD-079: at least 30 dollars a unit and 3 times landed cost, shown as the bank's reference, not the gate
BANK_MULTIPLE = 3.0
CHEAPEST_LABEL_KEYS = ('usps:zones_1_4', 'usps:zone_1_4')


def finance_rows(data, brand):
    source = brand_data(brand) if brand else data
    try:
        return source.table('finance_inputs')
    except (KeyError, ValueError):
        path = Path(getattr(source, 'folder', '') or '') / 'finance_inputs.json'
        if path.is_file():
            doc = json.loads(path.read_text(encoding='utf-8'))
            return doc.get('rows') if isinstance(doc, dict) else doc
    return None


def units_per_order(data, brand, rd):
    """Average units per order over the last whole month, from the monthly aggregate. None when absent."""
    source = brand_data(brand) if brand else data
    try:
        rows = source.table('monthly')
    except (KeyError, ValueError):
        try:
            rows = source.table('aggregates/monthly')
        except (KeyError, ValueError):
            return None
    row = next((r for r in rows if r.get('month') == rd.last_month), None)
    if not row or not row.get('orders') or row.get('units') is None:
        return None
    return round(row['units'] / row['orders'], 3)


def cogs_estimate_for(cand, fin, day):
    """The candidate's landed cost: the entered estimate, else the median landed cost of single-unit SKUs in its category."""
    if cand.get('cogs_estimate') is not None:
        return {'value': float(cand['cogs_estimate']), 'basis': 'entered on the candidate', 'estimated': False}
    if fin is None:
        return {'value': None, 'basis': 'no finance inputs', 'estimated': True}
    vals = []
    for r in fin.in_force('cogs_landed', day):
        sku = str(r.get('scope_key') or '')
        cat = next((c for p, c in CATEGORY_SKU_PREFIX.items() if sku.startswith(p)), None)
        if cat == cand.get('category') and sku.endswith('-1') and isinstance(r.get('value'), (int, float)):
            vals.append(float(r['value']))
    if not vals:
        return {'value': None, 'basis': f'no single-unit {cand.get("category")} SKU with a landed cost on file', 'estimated': True}
    pack = int(cand.get('pack_units') or 1)
    return {'value': round(statistics.median(vals) * pack, 2),
            'basis': f'median landed cost of {len(vals)} single-unit {cand.get("category")} SKUs (finance inputs)' + (f' x {pack} units in the pack' if pack > 1 else ''), 'estimated': True}


def margin_gate(cand, fin, br, day, upo, floor_pct):
    """Contribution margin modelled = (price - landed cost - donated item - fulfilment - payment fee) / price, every term
    from the candidate, the finance inputs or the brain, with the source named. Unavailable when a term is missing."""
    price = cand.get('planned_price')
    steps, missing = [], []
    if not isinstance(price, (int, float)) or price <= 0:
        return {'unavailable': True, 'reason': 'no planned price on the candidate', 'steps': [], 'margin_pct': None}
    cogs = cogs_estimate_for(cand, fin, day)
    steps.append({'label': 'planned price', 'value': round(price, 2), 'kind': 'total', 'source': 'candidate'})
    if cogs['value'] is None:
        missing.append('landed cost: ' + cogs['basis'])
    steps.append({'label': 'landed cost', 'value': cogs['value'], 'kind': 'down', 'source': cogs['basis']})
    give = brain_value_num_path(br, 'economics.gross_margin_model', 'donated_item_cost_pct')
    if give is not None:
        steps.append({'label': 'donated item', 'value': round(price * give / 100, 2), 'kind': 'down', 'source': f'brain economics.gross_margin_model, {give:g} percent of net price'})
    if fin is None:
        missing.append('fulfilment and payment: no finance inputs')
        steps += [{'label': 'fulfilment', 'value': None, 'kind': 'down', 'source': 'finance inputs missing'}, {'label': 'payment fee', 'value': None, 'kind': 'down', 'source': 'finance inputs missing'}]
    else:
        per_order = 0.0
        parts = []
        label = next((fin.value('shipping_label', day, k) for k in CHEAPEST_LABEL_KEYS if fin.value('shipping_label', day, k) is not None), None)
        if label is not None:
            per_order += label
            parts.append(f'label {label:g}')
        pk = fin.value('packaging', day)
        if pk is not None:
            per_order += pk
            parts.append(f'packaging {pk:g}')
        pp = fin.value('threepl_pick_pack', day, unit='usd_per_order')
        if pp is not None:
            per_order += pp
            parts.append(f'pick and pack {pp:g}')
        pu = fin.value('threepl_pick_pack', day, unit='usd_per_unit') or 0.0
        share = per_order / upo if upo else per_order
        fulfil = round(share + pu, 2)
        steps.append({'label': 'fulfilment', 'value': fulfil, 'kind': 'down',
                      'source': f'per order ({", ".join(parts)}) over {upo if upo else 1:g} units an order, plus {pu:g} a unit'})
        pct = fin.value('payment_fee_percent', day, 'online_store')
        fixed = fin.value('payment_fee_fixed', day, 'online_store')
        if pct is None:
            missing.append('payment fee percent for online_store')
            steps.append({'label': 'payment fee', 'value': None, 'kind': 'down', 'source': 'no payment_fee_percent for online_store'})
        else:
            fee = round(price * pct / 100 + ((fixed or 0) / upo if upo else (fixed or 0)), 2)
            steps.append({'label': 'payment fee', 'value': fee, 'kind': 'down', 'source': f'{pct:g} percent plus {fixed or 0:g} an order'})
    if missing:
        return {'unavailable': True, 'reason': '; '.join(missing), 'steps': steps, 'margin_pct': None, 'cogs': cogs}
    contribution = round(price - sum(s['value'] for s in steps if s['kind'] == 'down'), 2)
    steps.append({'label': 'contribution', 'value': None, 'kind': 'sub', 'source': 'price minus the steps above'})
    margin_pct = round(contribution / price * 100, 1)
    multiple = round(price / cogs['value'], 2) if cogs['value'] else None
    return {'unavailable': False, 'steps': steps, 'contribution_usd': contribution, 'margin_pct': margin_pct, 'floor_pct': floor_pct,
            'passes_floor': (margin_pct >= floor_pct) if floor_pct is not None else None, 'cogs': cogs,
            'multiple': multiple, 'bank_multiple': BANK_MULTIPLE, 'bank_dollar_floor': BANK_DOLLAR_FLOOR,
            'bank_rule_ok': (contribution >= BANK_DOLLAR_FLOOR and (multiple or 0) >= BANK_MULTIPLE),
            'formula': '(price - landed cost - donated item - fulfilment - payment fee) / price'}


def brain_value_num_path(br, rid_tail, key):
    r = br.get(f'{br.brand}.{rid_tail}') if br else None
    v = (r or {}).get('value') if r else None
    x = v.get(key) if isinstance(v, dict) else None
    return float(x) if isinstance(x, (int, float)) else None


def margin_findings(brand, data, br, rd, ends_on):
    """PROD-R16: an open candidate with a planned price whose modelled margin is below the brand floor.
    PROD-R17: actual margin by SKU unavailable (needs order rows), one connect finding."""
    fin_rows = finance_rows(data, brand)
    fin = metrics().finance.Finance(fin_rows) if fin_rows else None
    floor = fin.value('target_contribution_margin', ends_on.isoformat()) if fin else None
    upo = units_per_order(data, brand, rd)
    out = []
    for cand in pipeline(brand):
        if cand.get('stage') in CLOSED_STAGES:
            continue
        g = margin_gate(cand, fin, br, ends_on.isoformat(), upo, floor)
        if g.get('unavailable') or g.get('passes_floor') is not False:
            continue
        cid = cand.get('candidate_id') or slug(cand.get('name'))
        ev = [_ev('contribution_margin_pct_modelled', g['margin_pct'], 'percent', ends_on.isoformat(), 'model now', floor, 'threshold', source='finance_inputs', simulated=True, freshness_days=0,
                  formula=g['formula'], steps=[{s['label']: s['value']} for s in g['steps']]),
              _ev('landed_cost', g['cogs']['value'], 'usd', ends_on.isoformat(), 'model now', source='finance_inputs', simulated=True, freshness_days=0, note=g['cogs']['basis']),
              _ev('planned_price', cand.get('planned_price'), 'usd', ends_on.isoformat(), 'candidate', source='fixtures.pipeline', simulated=False, freshness_days=0)]
        sentence = (f'{cand["name"]}: modelled margin is {g["margin_pct"]:g} percent at ${cand["planned_price"]:g}, below the {floor:g} percent floor. '
                    f'It cannot move to sourcing spend without a price, cost or channel change.')
        f = _finding('PROD-R16', cid, ends_on, 'medium', ev, sentence, None, 0.7, [f'{br.brand}.economics.gross_margin_model'] if br else [],
                     money_reason='a candidate has no sales yet; the gap is per unit')
        f['entity'] = {'type': 'sku', 'id': cid, 'label': cand['name'], 'candidate': True, 'margin_pct': g['margin_pct'], 'floor_pct': floor, 'price': cand.get('planned_price'),
                       'contribution_usd': g.get('contribution_usd'), 'estimated_cogs': g['cogs']['estimated']}
        f['id'] = f'{SCREEN}.PROD-R16.{cid}'
        out.append(f)
    r = metrics().compute('contribution_margin', data, window='28d', end=ends_on.isoformat(), **({'brand': brand} if brand else {}))
    if r.get('unavailable'):
        u = _unavailable('PROD-R17', ends_on, 'Actual contribution margin by SKU cannot be read: it needs order rows and landed costs together.',
                         ['orders', 'order_lines', 'finance_inputs.cogs_landed'], r.get('fix') or 'shopify', 'Connect the store (read only) so orders join the landed costs on file.')
        u['entity'] = {'type': 'metric', 'id': 'contribution_margin', 'label': 'Actual margin by SKU'}
        u['sentence'] = u['sentence'] + (f' ({r.get("reason")})' if r.get('reason') else '')
        out.append(u)
    return out


# ---------------------------------------------------------------- demand pattern: evergreen, seasonal, trending

SEASONAL_TOP2_SHARE = 0.25    # the top 2 months carry this share of the year's units (an even year is 16.7 percent)
TRENDING_CAGR = 8.0           # a public market growing this fast a year, or 3 launches in 24 months, reads trending
TRENDING_LAUNCHES = 3
GIFT_WORDS = ['gift', 'holiday', 'christmas']


def demand_pattern(category, mix, fx, name='', lane_key=None):
    """The tag and its numbers: from our 12-month unit series for the category, the market growth and the launches in
    the web pass. Deterministic; every input named."""
    row = next((r for r in (mix.get('rows') or []) if r.get('category') == category), None) if mix and not mix.get('unavailable') else None
    months = (mix or {}).get('months') or []
    top2_share = peak = None
    if row and row.get('series') and sum(v or 0 for v in row['series']):
        total = sum(v or 0 for v in row['series'])
        pairs = sorted(zip(months, row['series']), key=lambda p: -(p[1] or 0))
        top2_share = round(sum(v or 0 for _, v in pairs[:2]) / total, 4)
        peak = [m[5:7] for m, _ in pairs[:2]]
    markets = [m for m in (fx or {}).get('markets') or [] if MARKET_CATEGORY.get(m.get('key')) == category]
    cagr = max([m['cagr_pct'] for m in markets if isinstance(m.get('cagr_pct'), (int, float))] or [None]) if markets else None
    launches = [l for l in (fx or {}).get('launches') or [] if (lane_key and l.get('sub_category') == lane_key) or (not lane_key and category in (l.get('sub_category') or ''))]
    gift = any(w in (name or '').lower() for w in GIFT_WORDS)
    if gift or (top2_share is not None and top2_share >= SEASONAL_TOP2_SHARE):
        tag, why = 'seasonal', (f'the top 2 months carry {round(top2_share * 100)} percent of {category} units' if top2_share is not None else 'a gift product by name')
    elif (cagr is not None and cagr >= TRENDING_CAGR) or len(launches) >= TRENDING_LAUNCHES:
        tag, why = 'trending', (f'market growth {cagr:g} percent a year' if cagr is not None and cagr >= TRENDING_CAGR else f'{len(launches)} launches in 24 months')
    elif row is not None:
        tag, why = 'evergreen', (f'even shape: the top 2 months carry {round(top2_share * 100)} percent of units' if top2_share is not None else 'an even 12-month series')
    else:
        tag, why = None, 'no 12-month series for the category'
    cash = None
    if tag == 'seasonal' and peak:
        cash = f'cash in lands in months {" and ".join(peak)}; stock must be paid for before the peak, so the order date is the lead time back from month {min(peak)}'
    elif tag == 'trending':
        cash = 'cash moves early: a first small run reads demand before a full order'
    elif tag == 'evergreen':
        cash = 'cash moves evenly: reorder points, not a launch spike'
    return {'category': category, 'tag': tag, 'why': why, 'top2_share': top2_share, 'peak_months': peak, 'market_cagr': cagr,
            'launches_24m': len(launches), 'cash_timing': cash, 'gift': gift}


def pattern_findings(brand, data, rd, ends_on):
    """PROD-R18: a seasonal candidate with no cash plan attached cannot reach the shortlist."""
    mix = category_mix(data, brand, rd)
    fx = web_pass(brand)
    out = []
    for cand in pipeline(brand):
        if cand.get('stage') in CLOSED_STAGES:
            continue
        p = demand_pattern(cand.get('category'), mix, fx, cand.get('name'))
        if p['tag'] == 'seasonal' and not cand.get('cash_plan'):
            cid = cand.get('candidate_id') or slug(cand.get('name'))
            ev = [_ev('demand_pattern_tag', 1, 'flag', ends_on.isoformat(), '12 months', source='products_monthly', tag=p['tag'], why=p['why']),
                  _ev('top2_month_share', p['top2_share'], 'ratio', month_end(mix['last']).isoformat() if not mix.get('unavailable') else ends_on.isoformat(), '12 months', SEASONAL_TOP2_SHARE, 'threshold', source='products_monthly'),
                  _ev('cash_plan_attached', 0, 'flag', ends_on.isoformat(), 'candidate now', 1, 'threshold', source='fixtures.pipeline', simulated=False, freshness_days=0)]
            sentence = f'{cand["name"]} is tagged seasonal ({p["why"]}), but no cash plan is attached for its spike window. It cannot reach the shortlist without one.'
            f = _finding('PROD-R18', cid, ends_on, 'medium', ev, sentence, None, 0.7, [], money_reason='a cash plan sizes the order; the gap is timing, not revenue')
            f['entity'] = {'type': 'sku', 'id': cid, 'label': cand['name'], 'candidate': True, 'peak_months': p['peak_months'], 'cash_timing': p['cash_timing']}
            f['id'] = f'{SCREEN}.PROD-R18.{cid}'
            out.append(f)
    return out


# ---------------------------------------------------------------- trend against saturation, per lane

LANE_MARKET = {'compression': ['compression_socks'], 'merino': ['merino_wool_socks'], 'performance': ['athletic_socks'], 'gifting': ['gifting_socks'],
               'underwear': ['mens_underwear_us', 'womens_underwear_us'], 'footwear': ['footwear_casual', 'slippers_us'], 'apparel': ['basics_tshirts'],
               'guarantee': ['socks_us'], 'creator': ['socks_us'], 'style': ['socks_us']}
TREND_ZERO_CAGR = 4.0      # a market growing 4 percent a year scores 0; 10 scores 1; minus 2 scores minus 1
TREND_SPAN_CAGR = 6.0
LAUNCH_BONUS = 0.1         # each launch by another brand in 24 months adds 0.1, up to 0.3
SATURATION_LADDER = [(1, 'green'), (4, 'amber')]   # idea PRD-052: 0 to 1 sellers green, 2 to 4 amber, 5 or more red
SATURATION_FULL = 5
TREND_UP = 0.3


def saturation_grade(n):
    for cap, grade in SATURATION_LADDER:
        if n <= cap:
            return grade
    return 'red'


def lane_map(br, ends_on):
    """Each lane as a point: x sellers (competitor pages pushing it plus launches by others), y trend score from the
    web pass growth plus launches. Named quadrants; the rule constants above are the grid lines."""
    fx = web_pass(br) or {}
    markets = {m.get('key'): m for m in fx.get('markets') or []}
    pts = []
    for row in subcategory_table(br, ends_on):
        keys = LANE_MARKET.get(row['key'], [])
        cagrs = [markets[k]['cagr_pct'] for k in keys if k in markets and isinstance(markets[k].get('cagr_pct'), (int, float))]
        cagr = round(sum(cagrs) / len(cagrs), 2) if cagrs else None
        base = max(-1.0, min(1.0, (cagr - TREND_ZERO_CAGR) / TREND_SPAN_CAGR)) if cagr is not None else None
        bonus = min(0.3, LAUNCH_BONUS * row['launches_theirs'])
        trend = round(min(1.0, base + bonus), 3) if base is not None else (round(bonus, 3) if row['launches_theirs'] else None)
        sellers = row['competitors_n'] + row['launches_theirs']
        pts.append({'key': row['key'], 'label': row['label'], 'x': sellers, 'y': trend, 'size': row['ads_sum'], 'sold': row['sold'], 'advertised': row['advertised'],
                    'competitors_n': row['competitors_n'], 'launches_theirs': row['launches_theirs'], 'market_cagr': cagr, 'market_keys': keys,
                    'grade': saturation_grade(sellers), 'verdict': row['verdict'], 'finding_id': f'{SCREEN}.PROD-R19.{row["key"]}',
                    'quadrant': (('growing' if (trend or 0) >= TREND_UP else 'flat') + (', full' if sellers >= SATURATION_FULL else ', room left')) if trend is not None else 'trend unavailable'})
    return {'points': pts, 'mid_x': SATURATION_FULL - 0.5, 'mid_y': TREND_UP, 'quadrants': {'tl': 'growing, room left', 'tr': 'growing, full', 'bl': 'flat, open', 'br': 'flat, crowded'},
            'rule': f'trend score: (market growth a year - {TREND_ZERO_CAGR:g}) / {TREND_SPAN_CAGR:g}, clamped to minus 1 to 1, plus {LAUNCH_BONUS:g} per launch by another brand in 24 months (up to 0.3); sellers: competitor pages pushing the lane plus those launches; bank ladder PRD-052: 0 to 1 green, 2 to 4 amber, 5 or more red'}


def lane_map_findings(br, ends_on):
    """PROD-R19: a lane growing (trend score 0.3 or more) with 5 or more sellers: growing, but full."""
    out = []
    if br is None:
        return out
    for p in lane_map(br, ends_on)['points']:
        if p['key'] in PROOF_LANES or p['y'] is None or p['y'] < TREND_UP or p['x'] < SATURATION_FULL:
            continue
        ev = [_ev('trend_direction_score', p['y'], 'score', ends_on.isoformat(), 'web pass', TREND_UP, 'threshold', source='fixtures.market_trends', simulated=False, freshness_days=0, market_cagr=p['market_cagr']),
              _ev('competitive_saturation_count', p['x'], 'count', ends_on.isoformat(), 'active ads and 24 months of launches', SATURATION_FULL, 'threshold', source='brain.competitors', simulated=False, freshness_days=0,
                  pages=p['competitors_n'], launches=p['launches_theirs'])]
        sentence = (f'{p["label"]} is growing (trend score {p["y"]:g}' + (f', market {p["market_cagr"]:g} percent a year' if p['market_cagr'] is not None else '') +
                    f'), but {p["x"]} sellers already compete in it ({p["competitors_n"]} pages advertising, {p["launches_theirs"]} launches in 24 months). Room left is smaller than the trend line suggests.')
        f = _finding('PROD-R19', p['key'], ends_on, 'low', ev, sentence, None, 0.5, [f'{br.brand}.competitors.competitor_set'], money_reason='a saturation read has no order count')
        f['entity'] = {'type': 'metric', 'id': p['key'], 'label': p['label'], 'sellers': p['x'], 'trend': p['y'], 'sold': p['sold']}
        f['id'] = f'{SCREEN}.PROD-R19.{p["key"]}'
        out.append(f)
    return out


# ---------------------------------------------------------------- sustained ad spend per lane (idea PRD-023: run length is a live, funded test, not proof of profit)

RUN_BANDS = [(0, 13, 'under 14 days'), (14, 29, '14 to 29 days'), (30, 89, '30 to 89 days'), (90, 10 ** 6, '90 days or more')]
FUNDED_MIN_DAYS = 90
FUNDED_MIN_ADVERTISERS = 3
LIVE_TEST_MIN_DAYS = 14


def run_band(days):
    if days is None:
        return None
    return next(label for lo, hi, label in RUN_BANDS if lo <= days <= hi)


def candidate_lanes(brand):
    """Which lanes each open candidate sits on, by the lane terms in its name and angle."""
    out = {}
    for c in pipeline(brand):
        if c.get('stage') in CLOSED_STAGES:
            continue
        text = f'{c.get("name") or ""} {c.get("angle_text") or ""} {c.get("category") or ""}'.lower()
        for key, _, terms in lanes_for(brand):
            if any(t in text for t in terms):
                out.setdefault(key, []).append(c.get('name'))
    return out


def spend_signal(br, brand, ends_on):
    """Per lane: advertisers by run-length band, those with an ad live 90 days or more, and the verdict:
    funded test (3 or more at 90 days), live test (1 or more at 14 days), noise."""
    lanes = subcategory_table(br, ends_on)
    cands = candidate_lanes(brand)
    out = []
    for row in lanes:
        bands = {label: 0 for _, _, label in RUN_BANDS}
        funded, live = [], []
        for c in row['competitors']:
            b = run_band(c.get('longest_run_days'))
            if b:
                bands[b] += 1
            if (c.get('longest_run_days') or 0) >= FUNDED_MIN_DAYS:
                funded.append(c['name'])
            if (c.get('longest_run_days') or 0) >= LIVE_TEST_MIN_DAYS:
                live.append(c['name'])
        verdict = 'funded' if len(funded) >= FUNDED_MIN_ADVERTISERS else 'live' if live else 'noise' if row['competitors'] else 'none'
        out.append({'key': row['key'], 'label': row['label'], 'kind': row['kind'], 'bands': bands, 'funded': funded, 'live': live, 'longest': max([c.get('longest_run_days') or 0 for c in row['competitors']] or [None]),
                    'long_runners_30d': sum(c.get('long_runners_30d') or 0 for c in row['competitors']), 'verdict': verdict,
                    'sold': row['sold'], 'advertised': row['advertised'], 'candidates': cands.get(row['key'], []), 'finding_id': f'{SCREEN}.PROD-R20.{row["key"]}'})
    order = {'funded': 0, 'live': 1, 'noise': 2, 'none': 3}
    out.sort(key=lambda r: (order[r['verdict']], -len(r['funded']), -(r['longest'] or 0)))
    return {'rows': out, 'bands': [label for _, _, label in RUN_BANDS],
            'rule': f'funded test: {FUNDED_MIN_ADVERTISERS} or more advertisers with an ad live {FUNDED_MIN_DAYS} days or more; live test: 1 or more at {LIVE_TEST_MIN_DAYS} days; run length is a funded test, never proof of profit (bank idea PRD-023)'}


def spend_findings(br, brand, ends_on):
    """PROD-R20: a product lane with a funded test (3 or more advertisers at 90 days) and no open candidate on it."""
    out = []
    if br is None:
        return out
    for r in spend_signal(br, brand, ends_on)['rows']:
        if r['verdict'] != 'funded' or r['kind'] == 'proof' or r['candidates']:
            continue
        ev = [_ev('ad_library_spend_signal', len(r['funded']), 'count', ends_on.isoformat(), 'active ads now', FUNDED_MIN_ADVERTISERS, 'threshold', source='brain.competitors', simulated=False, freshness_days=0,
                  names=r['funded'], min_days=FUNDED_MIN_DAYS),
              _ev('longest_run_days', r['longest'], 'days', ends_on.isoformat(), 'active ads now', source='brain.competitors', simulated=False, freshness_days=0),
              _ev('open_candidates_on_lane', 0, 'count', ends_on.isoformat(), 'pipeline now', 1, 'threshold', source='fixtures.pipeline', simulated=False, freshness_days=0)]
        sentence = (f'{len(r["funded"])} advertisers have kept an ad live {FUNDED_MIN_DAYS}+ days on {r["label"].lower()} ({", ".join(r["funded"][:3])}; longest {r["longest"]} days). '
                    f'That is a real spend signal, not a trend, and no candidate on the lane is open.')
        f = _finding('PROD-R20', r['key'], ends_on, 'medium', ev, sentence, None, 0.5, [f'{br.brand}.competitors.competitor_set'], money_reason='competitor run length is a signal; no spend or revenue is measurable')
        f['entity'] = {'type': 'metric', 'id': r['key'], 'label': r['label'], 'names': ', '.join(r['funded'][:3]), 'sold': r['sold']}
        f['id'] = f'{SCREEN}.PROD-R20.{r["key"]}'
        out.append(f)
    return out


# ---------------------------------------------------------------- the review price signal: what buyers say a pair is worth

PRICE_RE = re.compile(r'\$\s?(\d{1,3}(?:\.\d{1,2})?)|(\d{1,3}(?:\.\d{1,2})?)\s?(?:dollars|bucks)', re.I)
PRICE_MIN, PRICE_MAX = 3.0, 60.0
PRICE_CONTEXT = 60
REVIEW_PRICE_GAP = 0.15     # room spec: a planned price more than 15 percent above what reviewers say
PRICE_SOURCES = ('amazon', 'own_site_yotpo', 'trustpilot', 'retailer', 'nordstrom', 'sitejabber')


def review_price_signal(br):
    """Price mentions in review quotes (never Reddit, which prices other things): per-pair mentions where the words
    around the number say pair and not pack, between 3 and 60 dollars. Median, count, by source and star, short quotes."""
    if br is None:
        return {'n': 0, 'median_per_pair': None, 'mentions': [], 'by_source': {}, 'by_star': {}}
    mentions = []
    for rec in br.records('language_bank'):
        v = rec.get('value') or {}
        for rv in v.get('reviews') or []:
            src = str(rv.get('source') or '')
            if not any(src.startswith(s) for s in PRICE_SOURCES):
                continue
            q = str(rv.get('quote') or '')
            for m in PRICE_RE.finditer(q):
                val = float(m.group(1) or m.group(2))
                ctx = q[max(0, m.start() - PRICE_CONTEXT):m.end() + PRICE_CONTEXT].lower()
                if not (PRICE_MIN <= val <= PRICE_MAX) or 'sock' not in q.lower() and 'pair' not in ctx:
                    continue
                per_pair = ('pair' in ctx or 'each' in ctx) and not any(w in ctx for w in ('pairs', 'pack', 'package', '4 ', 'four'))
                if not per_pair:
                    continue
                mentions.append({'usd': val, 'source': src.split('_')[0], 'star': rv.get('star'), 'record': rec['id'], 'url': rv.get('url'),
                                 'quote': re.sub(r'\s+', ' ', q[max(0, m.start() - 70):m.end() + 70]).strip()[:140]})
    vals = [m['usd'] for m in mentions]
    by_source, by_star = {}, {}
    for m in mentions:
        by_source[m['source']] = by_source.get(m['source'], 0) + 1
        by_star[str(m['star'] or 'unknown')] = by_star.get(str(m['star'] or 'unknown'), 0) + 1
    return {'n': len(mentions), 'median_per_pair': round(statistics.median(vals), 2) if vals else None,
            'low': min(vals) if vals else None, 'high': max(vals) if vals else None, 'mentions': sorted(mentions, key=lambda m: m['usd'])[:20],
            'by_source': by_source, 'by_star': by_star,
            'rule': f'per-pair mentions between ${PRICE_MIN:g} and ${PRICE_MAX:g} in review quotes (Amazon, the brand site, Trustpilot, retailers); Reddit is left out; the gap rule is {round(REVIEW_PRICE_GAP * 100)} percent above the median'}


def review_price_findings(br, brand, ends_on):
    """PROD-R21: an open candidate whose planned price per unit in the pack is more than 15 percent above what reviewers say a pair is worth."""
    out = []
    sig = review_price_signal(br)
    med = sig.get('median_per_pair')
    if med is None:
        return out
    for cand in pipeline(brand):
        if cand.get('stage') in CLOSED_STAGES or not isinstance(cand.get('planned_price'), (int, float)) or cand.get('category') != 'socks':
            continue
        per = cand['planned_price'] / (cand.get('pack_units') or 1)
        gap = per / med - 1
        if gap <= REVIEW_PRICE_GAP:
            continue
        cid = cand.get('candidate_id') or slug(cand.get('name'))
        ev = [_ev('review_price_signal', med, 'usd', ends_on.isoformat(), 'all reviews to capture', source='brain.language_bank', simulated=False, freshness_days=0, mentions=sig['n']),
              _ev('planned_price_per_pair', round(per, 2), 'usd', ends_on.isoformat(), 'candidate', med * (1 + REVIEW_PRICE_GAP), 'threshold', source='fixtures.pipeline', simulated=False, freshness_days=0)]
        sentence = (f'Reviewers put a pair at around ${med:g} ({sig["n"]} price mentions). {cand["name"]} is planned at ${per:g} a pair, '
                    f'{round(gap * 100)} percent above that. Recheck positioning before funding.')
        f = _finding('PROD-R21', cid, ends_on, 'medium', ev, sentence, None, 0.5, [], money_reason='a price signal has no order count until a test runs')
        f['entity'] = {'type': 'sku', 'id': cid, 'label': cand['name'], 'candidate': True, 'planned_per_pair': round(per, 2), 'review_median': med, 'gap': round(gap, 4)}
        f['id'] = f'{SCREEN}.PROD-R21.{cid}'
        out.append(f)
    return out


# ---------------------------------------------------------------- complaint bars per listing (review mining on the brand's own Amazon listings)

COMPLAINT_RATE = 0.15    # room spec: the top recurring complaint over 15 percent of mined reviews is the gap to build the angle on
UNSORTED_THEME = 'general'


def listing_complaints(br):
    """Per Amazon listing in the brain: mined issue and praise counts by theme, the top complaint and its share of
    mined reviews, the listing's public stars, ratings count and price."""
    if br is None:
        return []
    issues, praise, listings = {}, {}, {}
    for r in br.records('products'):
        v = r.get('value') or {}
        if isinstance(v, dict) and v.get('asin') and v.get('kind') in ('issues', 'praise'):
            (issues if v['kind'] == 'issues' else praise)[v['asin']] = {k: int(n or 0) for k, n in (v.get('themes') or {}).items()}
    for r in br.records('marketplaces'):
        v = r.get('value') or {}
        if isinstance(v, dict) and v.get('asin'):
            l = listings.setdefault(v['asin'], {})
            for k in ('title', 'stars', 'reviews_count', 'price_usd', 'review_count'):
                if v.get(k) is not None and l.get(k) is None:
                    l[k] = v[k]
    out = []
    for asin in sorted(set(issues) | set(praise)):
        iss, pr = issues.get(asin, {}), praise.get(asin, {})
        mined = sum(iss.values()) + sum(pr.values())
        sorted_iss = sorted(((k, n) for k, n in iss.items() if k != UNSORTED_THEME), key=lambda kv: -kv[1])
        top = sorted_iss[0] if sorted_iss else (None, 0)
        l = listings.get(asin, {})
        out.append({'asin': asin, 'title': l.get('title') or asin, 'stars': l.get('stars'), 'ratings': l.get('reviews_count') or l.get('review_count'), 'price_usd': l.get('price_usd'),
                    'mined': mined, 'issues': iss, 'praise': pr, 'complaints': sum(iss.values()), 'praises': sum(pr.values()),
                    'top_complaint': top[0], 'top_count': top[1], 'top_rate': round(top[1] / mined, 4) if mined and top[0] else None,
                    'praise_share': round(sum(pr.values()) / mined, 4) if mined else None,
                    'finding_id': f'{SCREEN}.PROD-R22.{asin.lower()}'})
    out.sort(key=lambda r: -(r['top_rate'] or 0))
    return out


def complaint_findings(br, ends_on):
    """PROD-R22: a listing with 20 or more mined reviews whose top complaint is over 15 percent of them."""
    out = []
    for r in listing_complaints(br):
        if r['mined'] < 20 or r['top_rate'] is None or r['top_rate'] <= COMPLAINT_RATE:
            continue
        ev = [_ev('review_complaint_rate', r['top_rate'], 'ratio', ends_on.isoformat(), 'reviews mined', COMPLAINT_RATE, 'threshold', source=f'{br.brand}.products.amazon_{r["asin"].lower()}_issues',
                  simulated=False, freshness_days=0, complaint=r['top_complaint'], mined=r['mined']),
              _ev('praise_share', r['praise_share'], 'ratio', ends_on.isoformat(), 'reviews mined', source=f'{br.brand}.products.amazon_{r["asin"].lower()}_praise', simulated=False, freshness_days=0),
              _ev('listing_stars', r['stars'], 'stars', ends_on.isoformat(), 'listing now', source='brain.marketplaces', simulated=False, freshness_days=0, ratings=r['ratings'])]
        th = THEME_LABEL.get(r['top_complaint'], r['top_complaint']).lower()
        sentence = (f'{round(r["top_rate"] * 100)} percent of {r["mined"]} mined reviews on {r["title"]} ({r["asin"]}) mention the same complaint: {th}. '
                    f'That is the gap to build the angle on.')
        f = _finding('PROD-R22', r['asin'].lower(), ends_on, 'medium', ev, sentence, None, 0.5, [f'{br.brand}.products.amazon_{r["asin"].lower()}_issues'],
                     money_reason='listing sales are not connected; the rate is a share of mined reviews')
        f['entity'] = {'type': 'sku', 'id': r['asin'].lower(), 'label': r['title'], 'asin': r['asin'], 'complaint': r['top_complaint'], 'rate': r['top_rate']}
        f['id'] = f'{SCREEN}.PROD-R22.{r["asin"].lower()}'
        out.append(f)
    return out


# ---------------------------------------------------------------- differentiation angle and the 5 go-live gates

ANGLE_COPY_WORDS = 3     # an angle sharing 3 or more distinctive words with one competitor's pitch reads as their claim, not ours
GATES = ['provable_claim', 'owned_difference', 'brand_threshold', 'contribution_margin', 'ad_cost_ceiling']
GATE_LABEL = {'provable_claim': 'Provable claim', 'owned_difference': 'Owned difference', 'brand_threshold': 'Brand threshold', 'contribution_margin': 'Contribution margin', 'ad_cost_ceiling': 'Ad-cost ceiling'}
SOURCE_WORDS = ['review', 'reddit', 'web pass', 'finding', 'teardown', 'field', 'ladder', 'survey', 'circana', 'prod-r']


def angle_confidence(cand, comps):
    """0 to 3: the angle is filled, it names a source, and it is not a copy of a competitor's own claim."""
    text = str(cand.get('angle_text') or '').strip()
    src = str(cand.get('angle_source') or '').strip().lower()
    filled = bool(text)
    sourced = filled and any(w in src for w in SOURCE_WORDS)
    words = {w.strip('.,;:()"\'') for w in re.split(r'[\s/]+', text.lower())}
    words = {w for w in words if len(w) >= 5 and w not in STOP and w.isalpha()}
    copied = None
    if filled and comps:
        for c in comps:
            hits = [w for w in words if w in c['text']]
            if len(hits) >= ANGLE_COPY_WORDS:
                copied = {'competitor': c['name'], 'words': sorted(hits)[:5]}
                break
    owned = filled and copied is None
    score = int(filled) + int(sourced) + int(owned)
    return {'score': score, 'label': ['none', 'weak', 'fair', 'solid'][score], 'filled': filled, 'sourced': sourced, 'owned': owned, 'copied': copied}


def go_live_gates(cand, angle, gate, lines, fin, day, upo):
    """The 5 gates as pass, fail or unavailable, each with its reason."""
    out = {}
    out['provable_claim'] = {'status': 'pass' if angle['sourced'] else ('fail' if angle['filled'] else 'unavailable'),
                             'why': 'the angle names its source' if angle['sourced'] else ('the angle has no named source' if angle['filled'] else 'no angle yet')}
    out['owned_difference'] = {'status': 'pass' if angle['owned'] else ('fail' if angle['filled'] else 'unavailable'),
                               'why': ('not a competitor claim' if angle['owned'] else (f'reads like {angle["copied"]["competitor"]}: ' + ', '.join(angle['copied']['words']) if angle['copied'] else 'no angle yet'))}
    cat = str(cand.get('category') or '').lower()
    in_lines = any(cat.rstrip('s') in str(l).lower() for l in lines) if lines else None
    fit = (cand.get('screen_result') or {}).get('store_fit')
    out['brand_threshold'] = {'status': 'pass' if in_lines and fit == 'pass' else ('fail' if fit == 'fail' or in_lines is False else 'unavailable'),
                              'why': ('category in the brand\'s lines and store fit passed' if in_lines and fit == 'pass' else 'store fit failed' if fit == 'fail' else 'category not in the brand\'s lines' if in_lines is False else 'store fit not run')}
    if gate.get('unavailable'):
        out['contribution_margin'] = {'status': 'unavailable', 'why': gate.get('reason') or 'inputs missing'}
    else:
        out['contribution_margin'] = {'status': 'pass' if gate.get('passes_floor') else ('fail' if gate.get('passes_floor') is False else 'unavailable'),
                                      'why': f'{gate["margin_pct"]:g} percent against a {gate["floor_pct"]:g} percent floor' if gate.get('floor_pct') is not None else 'no floor on file'}
    cac = fin.value('target_cac', day) if fin else None
    if cac is None or gate.get('unavailable'):
        out['ad_cost_ceiling'] = {'status': 'unavailable', 'why': 'no target_cac in the finance inputs' if cac is None else 'no contribution model'}
    else:
        per_order = gate['contribution_usd'] * (upo or 1)
        out['ad_cost_ceiling'] = {'status': 'pass' if per_order >= cac else 'fail', 'why': f'contribution an order ${per_order:,.2f} against a target CAC of ${cac:,.2f}'}
    passed = sum(1 for g in out.values() if g['status'] == 'pass')
    return {'gates': out, 'passed': passed, 'of': len(GATES)}


def compliance_status(cand):
    c = cand.get('compliance') or {}
    vals = [c.get('labelling'), c.get('category_certification')]
    if any(v == 'fail' for v in vals):
        return 'fail'
    if all(v == 'pass' for v in vals):
        return 'pass'
    return 'unavailable'


def candidate_gates(brand, data, br, rd, ends_on):
    fin_rows = finance_rows(data, brand)
    fin = metrics().finance.Finance(fin_rows) if fin_rows else None
    floor = fin.value('target_contribution_margin', ends_on.isoformat()) if fin else None
    upo = units_per_order(data, brand, rd)
    comps = competitor_signals(br)
    lines = brain_value_lines(br) or []
    out = []
    for cand in pipeline(brand):
        angle = angle_confidence(cand, comps)
        gate = margin_gate(cand, fin, br, ends_on.isoformat(), upo, floor)
        gl = go_live_gates(cand, angle, gate, lines, fin, ends_on.isoformat(), upo)
        out.append({'candidate_id': cand.get('candidate_id'), 'name': cand.get('name'), 'stage': cand.get('stage'), 'closed': cand.get('stage') in CLOSED_STAGES,
                    'stage_index': STAGES.index(cand['stage']) if cand.get('stage') in STAGES else None, 'angle': angle, 'gates': gl['gates'], 'passed': gl['passed'], 'of': gl['of'],
                    'compliance': compliance_status(cand), 'angle_text': cand.get('angle_text'), 'angle_source': cand.get('angle_source')})
    return out


def gate_findings(brand, data, br, rd, ends_on):
    """PROD-R23: a candidate past screening with no stated angle. PROD-R24: 2 or more gates passed and the compliance check not run."""
    out = []
    for r in candidate_gates(brand, data, br, rd, ends_on):
        if r['closed']:
            continue
        cid = r['candidate_id'] or slug(r['name'])
        if (r['stage_index'] or 0) >= 1 and not r['angle']['filled']:
            ev = [_ev('differentiation_angle_confidence', 0, 'score', ends_on.isoformat(), 'candidate now', 1, 'threshold', source='fixtures.pipeline', simulated=False, freshness_days=0, stage=r['stage'])]
            sentence = f'{r["name"]} has no stated point of difference at {r["stage"]}. It cannot reach a funding gate without one.'
            f = _finding('PROD-R23', cid, ends_on, 'medium', ev, sentence, None, 0.9, [], money_reason='an angle gap has no order count')
            f['entity'] = {'type': 'sku', 'id': cid, 'label': r['name'], 'candidate': True, 'stage': r['stage']}
            f['id'] = f'{SCREEN}.PROD-R23.{cid}'
            out.append(f)
        if r['passed'] >= 2 and r['compliance'] == 'unavailable':
            ev = [_ev('go_live_gate_pass_count', r['passed'], 'count', ends_on.isoformat(), 'candidate now', 2, 'threshold', source='fixtures.pipeline', simulated=False, freshness_days=0, of=r['of']),
                  _ev('compliance_gate_status', None, 'flag', ends_on.isoformat(), 'candidate now', source='fixtures.pipeline', simulated=False, freshness_days=0, note='labelling and category certification not run')]
            sentence = f'{r["name"]} has cleared {r["passed"]} of {r["of"]} gates but the compliance check has not run. It is not fundable yet.'
            f = _finding('PROD-R24', cid, ends_on, 'medium', ev, sentence, None, 0.9, [], money_reason='a compliance gap blocks funding; it has no order count')
            f['entity'] = {'type': 'sku', 'id': cid, 'label': r['name'], 'candidate': True, 'passed': r['passed'], 'of': r['of']}
            f['id'] = f'{SCREEN}.PROD-R24.{cid}'
            out.append(f)
    return out


# ---------------------------------------------------------------- the shortlist scorecard and the go or no-go memo

CRITERIA = ['demand', 'margin', 'differentiation', 'compliance', 'cash_timing']
CRITERIA_LABEL = {'demand': 'Demand', 'margin': 'Margin', 'differentiation': 'Differentiation', 'compliance': 'Compliance', 'cash_timing': 'Cash timing'}
DEFAULT_WEIGHTS = {'demand': 30, 'margin': 30, 'differentiation': 20, 'compliance': 10, 'cash_timing': 10}
GO_TOTAL, KILL_TOTAL = 70, 40
REVIEW_DAYS = 14


def shortlist_weights(br):
    """The brand's scorecard weights from a learnings record (learnings.shortlist_weights), else the defaults. Set once per brand."""
    r = br.get(f'{br.brand}.learnings.shortlist_weights') if br else None
    v = (r or {}).get('value') if r else None
    if isinstance(v, dict) and all(k in v and isinstance(v[k], (int, float)) for k in CRITERIA) and sum(v[k] for k in CRITERIA) > 0:
        w = {k: float(v[k]) for k in CRITERIA}
        return {k: round(x * 100 / sum(w.values()), 2) for k, x in w.items()}, r['id']
    return dict(DEFAULT_WEIGHTS), 'defaults (no learnings.shortlist_weights record)'


def score_candidate(cand, gates_row, gate, pattern, spend_rows):
    """Each criterion 0 to 5 from fields that already exist, None when its input is missing (scored at the neutral 2.5, written down)."""
    checks = cand.get('screen_result') or {}
    passed = sum(1 for k in SCREEN_CHECKS if checks.get(k) == 'pass')
    ran = sum(1 for k in SCREEN_CHECKS if checks.get(k) in ('pass', 'fail'))
    lanes = [r for r in spend_rows if cand.get('name') in r.get('candidates', [])]
    funded = any(r['verdict'] == 'funded' for r in lanes)
    demand = None if ran == 0 else min(5, {0: 0, 1: 1, 2: 3, 3: 4}[passed] + (1 if funded else 0))
    if gate.get('unavailable') or gate.get('floor_pct') is None:
        margin = None
    else:
        gap = gate['margin_pct'] - gate['floor_pct']
        margin = 5 if gap >= 10 else 4 if gap >= 0 else 2 if gap >= -5 else 1
    differentiation = {0: 0, 1: 2, 2: 3, 3: 5}[gates_row['angle']['score']]
    compliance = {'pass': 5, 'fail': 0, 'unavailable': None}[gates_row['compliance']]
    tag = pattern.get('tag')
    cash = None if not tag else (5 if tag == 'seasonal' and cand.get('cash_plan') else 1 if tag == 'seasonal' else 4 if tag == 'evergreen' else 3)
    return {'demand': demand, 'margin': margin, 'differentiation': differentiation, 'compliance': compliance, 'cash_timing': cash}


def scorecard(brand, data, br, rd, ends_on):
    weights, source = shortlist_weights(br)
    fin_rows = finance_rows(data, brand)
    fin = metrics().finance.Finance(fin_rows) if fin_rows else None
    floor = fin.value('target_contribution_margin', ends_on.isoformat()) if fin else None
    upo = units_per_order(data, brand, rd)
    mix = category_mix(data, brand, rd)
    fx = web_pass(brand)
    spend_rows = spend_signal(br, brand, ends_on)['rows'] if br else []
    gates_rows = {g['candidate_id']: g for g in candidate_gates(brand, data, br, rd, ends_on)}
    rows = []
    for cand in pipeline(brand):
        cid = cand.get('candidate_id')
        g = margin_gate(cand, fin, br, ends_on.isoformat(), upo, floor)
        gr = gates_rows.get(cid) or {'angle': angle_confidence(cand, []), 'compliance': compliance_status(cand), 'passed': 0, 'of': len(GATES)}
        p = demand_pattern(cand.get('category'), mix, fx, cand.get('name'))
        sc = score_candidate(cand, gr, g, p, spend_rows)
        total = round(sum(weights[k] * ((sc[k] if sc[k] is not None else 2.5) / 5) for k in CRITERIA), 1)
        closed = cand.get('stage') in CLOSED_STAGES
        failed_screen = sum(1 for k in SCREEN_CHECKS if (cand.get('screen_result') or {}).get(k) == 'fail') >= SCREEN_FAIL_AT
        if closed:
            verdict = cand.get('stage')
        elif failed_screen or total < KILL_TOTAL:
            verdict = 'no_go'
        elif total >= GO_TOTAL and gr['passed'] == gr['of'] and gr['compliance'] == 'pass':
            verdict = 'go'
        else:
            verdict = 'hold'
        review = cand.get('review_date') or (ends_on + timedelta(days=REVIEW_DAYS)).isoformat()
        rows.append({'candidate_id': cid, 'name': cand.get('name'), 'stage': cand.get('stage'), 'closed': closed, 'scores': sc, 'total': total, 'verdict': verdict,
                     'gates_passed': gr['passed'], 'gates_of': gr['of'], 'compliance': gr['compliance'], 'angle': gr['angle']['label'], 'margin_pct': g.get('margin_pct'),
                     'pattern': p.get('tag'), 'review_date': review, 'review_due': (not closed) and review <= ends_on.isoformat(), 'planned_price': cand.get('planned_price'),
                     'hours_logged': cand.get('hours_logged'), 'unavailable': [k for k in CRITERIA if sc[k] is None]})
    rows.sort(key=lambda r: (r['closed'], -r['total'], r['name'] or ''))
    for i, r in enumerate(rows):
        r['rank'] = i + 1
    return {'rows': rows, 'weights': weights, 'weights_source': source, 'criteria': CRITERIA, 'labels': CRITERIA_LABEL, 'go_total': GO_TOTAL, 'kill_total': KILL_TOTAL,
            'rule': f'go at {GO_TOTAL} or more with all gates and compliance passed; no-go under {KILL_TOTAL} or a failed screen; else hold. A criterion with no input scores the neutral 2.5, written down.'}


def memo_text(row, weights):
    """The go or no-go memo in plain words, from the numbers only."""
    lines = [f'{row["name"]}: {row["verdict"].replace("_", " ")} at {row["total"]:g} of 100', '']
    for k in CRITERIA:
        v = row['scores'][k]
        lines.append(f'{CRITERIA_LABEL[k]} ({weights[k]:g} percent): ' + ('n/a, scored at the neutral 2.5' if v is None else f'{v} of 5'))
    lines += ['', f'Gates: {row["gates_passed"]} of {row["gates_of"]} passed. Compliance: {row["compliance"]}. Angle: {row["angle"]}.',
              f'Modelled margin: ' + (f'{row["margin_pct"]:g} percent' if row['margin_pct'] is not None else 'unavailable') + f'. Demand pattern: {row["pattern"] or "unavailable"}.',
              f'Review date: {row["review_date"]}.', '', 'Decision: go (fund and move to sourcing), hold (name the open question and the new box), or kill (log the reason).']
    return '\n'.join(lines)


def shortlist_findings(brand, data, br, rd, ends_on):
    """PROD-R25: a candidate whose review date has arrived and who is still open."""
    out = []
    sc = scorecard(brand, data, br, rd, ends_on)
    for r in sc['rows']:
        if not r['review_due']:
            continue
        cid = r['candidate_id'] or slug(r['name'])
        ev = [_ev('shortlist_review_date_status', 1, 'flag', ends_on.isoformat(), 'candidate now', source='fixtures.pipeline', simulated=False, freshness_days=0, review_date=r['review_date']),
              _ev('shortlist_score', r['total'], 'score', ends_on.isoformat(), 'scorecard now', GO_TOTAL, 'threshold', source='fixtures.pipeline', simulated=False, freshness_days=0, verdict=r['verdict'])]
        sentence = f'{r["name"]}\'s review date ({r["review_date"]}) has arrived. It scores {r["total"]:g} of 100 ({r["verdict"].replace("_", " ")}). Bring it back to the founder for a fresh decision.'
        f = _finding('PROD-R25', cid, ends_on, 'medium', ev, sentence, None, 0.9, [], money_reason='a decision, not a revenue gap')
        f['entity'] = {'type': 'sku', 'id': cid, 'label': r['name'], 'candidate': True, 'total': r['total'], 'verdict': r['verdict'], 'memo': memo_text(r, sc['weights'])}
        f['id'] = f'{SCREEN}.PROD-R25.{cid}'
        out.append(f)
    return out


# ---------------------------------------------------------------- video-commerce demand signals per lane (PROD-C02: one clip or a real pattern)

LANE_TAGS = {'compression': ['compressionsocks'], 'merino': ['merinosocks'], 'performance': ['runningsocks'], 'gifting': ['sockgift'], 'guarantee': ['buyitforlife'],
             'style': ['sockstyle'], 'underwear': ['underwear'], 'footwear': ['slippers'], 'apparel': ['tshirt'], 'creator': []}
SOCIAL_MIN_POSTS = 5
REDDIT_MIN_MENTIONS = 3
PATTERN_MIN_PLATFORMS = 2


def reddit_lane_mentions(br):
    """Reddit language bank records whose text carries a lane's terms: mentions and upvotes per lane."""
    lanes = lanes_for(br)
    out = {k: {'mentions': 0, 'upvotes': 0} for k, _, _ in lanes}
    if br is None:
        return out
    for rec in br.records('language_bank'):
        v = rec.get('value') or {}
        if not v.get('subreddit'):
            continue
        text = (str(v.get('phrase') or '') + ' ' + ' '.join(str(q.get('quote') or '') for q in v.get('reviews') or [])).lower()
        for key, _, terms in lanes:
            if any(t in text for t in terms):
                out[key]['mentions'] += 1
                out[key]['upvotes'] += int(v.get('weight') or 0)
    return out


def video_signals(br, brand, ends_on):
    """Per lane: the independent platforms that show demand (Instagram pull by hashtag, Reddit mentions, competitor creator-style
    ads, our own creator ads) and the verdict: pattern (2 or more platforms above the floor), single source (exactly 1), none."""
    social = social_pull_for(br) or {}
    by_tag = {k.lower(): v for k, v in (social.get('posts_by_tag') or {}).items()}
    themes = social.get('themes') or {}
    reddit = reddit_lane_mentions(br)
    creator_pages = {}
    if br is not None:
        for rec in br.records('content'):
            v = rec.get('value') or {}
            if isinstance(v, dict) and v.get('creator_style_ads') and v.get('page'):
                creator_pages[v['page'].lower().replace(' socks', '').replace(' vermont', '').strip()] = int(v['creator_style_ads'])
        own = br.get(f'{br.brand}.learnings.creator_ads')
        own_n = len(((own or {}).get('value') or {}).get('ads') or []) if own else 0
    else:
        own_n = 0
    cands = candidate_lanes(brand)
    out = []
    for row in subcategory_table(br, ends_on):
        key = row['key']
        posts = sum(by_tag.get(t, 0) for t in LANE_TAGS.get(key, []))
        r = reddit.get(key, {'mentions': 0, 'upvotes': 0})
        creators = [c['name'] for c in row['competitors'] if c['name'].lower().replace(' socks', '').replace(' vermont', '').strip() in creator_pages]
        platforms = []
        if posts >= SOCIAL_MIN_POSTS:
            platforms.append('instagram')
        if r['mentions'] >= REDDIT_MIN_MENTIONS:
            platforms.append('reddit')
        if creators:
            platforms.append('creator ads')
        verdict = 'pattern' if len(platforms) >= PATTERN_MIN_PLATFORMS else 'single' if len(platforms) == 1 else 'none'
        out.append({'key': key, 'label': row['label'], 'kind': row['kind'], 'instagram_posts': posts if LANE_TAGS.get(key) else None, 'instagram_mode': social.get('mode'),
                    'reddit_mentions': r['mentions'], 'reddit_upvotes': r['upvotes'], 'creator_pages': creators, 'own_creator_ads': own_n if row['advertised'] else 0,
                    'platforms': platforms, 'verdict': verdict, 'candidates': cands.get(key, []), 'finding_id': f'{SCREEN}.PROD-R26.{key}'})
    order = {'pattern': 0, 'single': 1, 'none': 2}
    out.sort(key=lambda x: (order[x['verdict']], -len(x['platforms']), -x['reddit_mentions']))
    return {'rows': out, 'rule': f'a platform counts at {SOCIAL_MIN_POSTS} or more Instagram posts on the lane tag, {REDDIT_MIN_MENTIONS} or more Reddit mentions, or a competitor page running creator-style ads on the lane; pattern at {PATTERN_MIN_PLATFORMS} platforms, single source at 1',
            'social_mode': social.get('mode'), 'social_note': social.get('note')}


def video_findings(br, brand, ends_on):
    """PROD-R26: a lane with an open candidate whose demand shows on exactly one platform: unverified until a second source confirms."""
    out = []
    if br is None:
        return out
    for r in video_signals(br, brand, ends_on)['rows']:
        if r['verdict'] != 'single' or not r['candidates']:
            continue
        ev = [_ev('video_commerce_demand_signal', len(r['platforms']), 'count', ends_on.isoformat(), 'pulls on file', PATTERN_MIN_PLATFORMS, 'threshold', source='fixtures.social_pull, brain.language_bank, brain.content',
                  simulated=False, freshness_days=0, platforms=r['platforms']),
              _ev('reddit_mentions', r['reddit_mentions'], 'count', ends_on.isoformat(), 'past year', source='brain.language_bank', simulated=False, freshness_days=0, upvotes=r['reddit_upvotes']),
              _ev('instagram_posts', r['instagram_posts'], 'count', ends_on.isoformat(), 'hashtag pull', source='fixtures.social_pull', simulated=False, freshness_days=0, mode=r['instagram_mode'])]
        sentence = (f'{", ".join(r["candidates"][:2])}: demand on {r["label"].lower()} shows on one platform only ({r["platforms"][0]}). '
                    f'Treat it as unverified until a second source confirms it.')
        f = _finding('PROD-R26', r['key'], ends_on, 'low', ev, sentence, None, 0.5, [], money_reason='a demand signal has no order count')
        f['entity'] = {'type': 'metric', 'id': r['key'], 'label': r['label'], 'platform': r['platforms'][0], 'candidates': r['candidates']}
        f['id'] = f'{SCREEN}.PROD-R26.{r["key"]}'
        out.append(f)
    return out


# ---------------------------------------------------------------- tech pack and spec versions per candidate (PROD-C13)

TECH_PACK_LINES = ('tolerances', 'bom', 'packaging_cost')
SPEC_STAGE_MIN = 2   # gated or later needs a current spec before sourcing


def tech_pack_status(cand):
    """current: the newest pack has tolerances, a BOM and a packaging cost line and status current; partial: a pack exists
    with a line missing; none: no pack."""
    packs = cand.get('tech_packs') or []
    if not packs:
        return {'status': 'none', 'version': None, 'missing': list(TECH_PACK_LINES), 'pack': None}
    latest = packs[-1]
    missing = [k for k in TECH_PACK_LINES if latest.get(k) in (None, '', False)]
    status = 'current' if not missing and latest.get('status', 'current') == 'current' else 'partial'
    return {'status': status, 'version': latest.get('version'), 'missing': missing, 'pack': latest}


def tech_pack_findings(brand, ends_on):
    """PROD-R27: a candidate at gated or later with no current versioned spec."""
    out = []
    for cand in pipeline(brand):
        if cand.get('stage') in CLOSED_STAGES or cand.get('stage') not in STAGES or STAGES.index(cand['stage']) < SPEC_STAGE_MIN:
            continue
        tp = tech_pack_status(cand)
        if tp['status'] == 'current':
            continue
        cid = cand.get('candidate_id') or slug(cand.get('name'))
        ev = [_ev('tech_pack_status', 0, 'flag', ends_on.isoformat(), 'candidate now', 1, 'threshold', source='fixtures.pipeline', simulated=False, freshness_days=0,
                  version=tp['version'], missing=tp['missing'], stage=cand.get('stage'))]
        what = ('no spec yet' if tp['status'] == 'none' else f'{tp["version"]} is missing {", ".join(m.replace("_", " ") for m in tp["missing"])}')
        sentence = f'{cand["name"]} is at {cand["stage"]} with no current versioned spec ({what}). Sourcing cannot quote it.'
        f = _finding('PROD-R27', cid, ends_on, 'medium', ev, sentence, None, 0.9, [], money_reason='a spec gap delays sourcing; it has no order count')
        f['entity'] = {'type': 'sku', 'id': cid, 'label': cand['name'], 'candidate': True, 'stage': cand.get('stage'), 'missing': tp['missing'], 'version': tp['version']}
        f['id'] = f'{SCREEN}.PROD-R27.{cid}'
        out.append(f)
    return out


# ---------------------------------------------------------------- research hours budget per stage (PROD-C04: a fixed time budget that research cannot sprawl past)

DEFAULT_HOURS_BUDGET = {'screened': 4, 'researched': 16, 'gated': 8, 'shortlisted': 4, 'go': 0}
SPRAWL_TIMES = 1.0     # fires when hours logged pass the cumulative budget for the stage


def hours_budget(br):
    """Hours a candidate may use per stage, from a learnings record (learnings.research_hours_budget) else the defaults."""
    r = br.get(f'{br.brand}.learnings.research_hours_budget') if br else None
    v = (r or {}).get('value') if r else None
    if isinstance(v, dict) and all(isinstance(v.get(k), (int, float)) for k in STAGES):
        return {k: float(v[k]) for k in STAGES}, r['id']
    return dict(DEFAULT_HOURS_BUDGET), 'defaults (no learnings.research_hours_budget record)'


def hours_table(brand, br):
    budget, source = hours_budget(br)
    rows = []
    for cand in pipeline(brand):
        st = cand.get('stage')
        idx = STAGES.index(st) if st in STAGES else None
        allowed = sum(budget[s] for s in STAGES[:idx + 1]) if idx is not None else None
        used = float(cand.get('hours_logged') or 0)
        rows.append({'candidate_id': cand.get('candidate_id'), 'name': cand.get('name'), 'stage': st, 'closed': st in CLOSED_STAGES, 'hours_logged': used,
                     'hours_allowed': allowed, 'used_share': round(used / allowed, 4) if allowed else None, 'over_by': round(used - allowed, 1) if allowed is not None and used > allowed else 0,
                     'finding_id': f'{SCREEN}.PROD-R28.{cand.get("candidate_id")}'})
    total_used = sum(r['hours_logged'] for r in rows)
    rows.sort(key=lambda r: (r['closed'], -(r['used_share'] or 0)))
    return {'rows': rows, 'budget': budget, 'budget_source': source, 'stages': STAGES, 'total_hours': round(total_used, 1),
            'rule': 'the allowed hours at a stage are the budgets of every stage up to it, summed; research sprawl fires when hours logged pass that'}


def hours_findings(brand, br, ends_on):
    """PROD-R28: an open candidate whose hours logged pass the cumulative hours budget for its stage."""
    out = []
    t = hours_table(brand, br)
    for r in t['rows']:
        if r['closed'] or r['hours_allowed'] is None or r['hours_logged'] <= r['hours_allowed'] * SPRAWL_TIMES:
            continue
        ev = [_ev('research_time_used', r['used_share'], 'ratio', ends_on.isoformat(), 'since screen-in', SPRAWL_TIMES, 'threshold', source='fixtures.pipeline', simulated=False, freshness_days=0,
                  hours_logged=r['hours_logged'], hours_allowed=r['hours_allowed'], stage=r['stage'], budget_source=t['budget_source'])]
        sentence = (f'{r["name"]} has used {r["hours_logged"]:g} research hours against {r["hours_allowed"]:g} allowed through {r["stage"]} '
                    f'({round(r["used_share"] * 100)} percent). Decide or kill it; no more hours without a named question.')
        f = _finding('PROD-R28', r['candidate_id'], ends_on, 'low', ev, sentence, None, 0.9, [], money_reason='research hours, not revenue')
        f['entity'] = {'type': 'sku', 'id': r['candidate_id'], 'label': r['name'], 'candidate': True, 'stage': r['stage'], 'hours_logged': r['hours_logged'], 'hours_allowed': r['hours_allowed']}
        f['id'] = f'{SCREEN}.PROD-R28.{r["candidate_id"]}'
        out.append(f)
    return out


# ---------------------------------------------------------------- 12-month against multi-year trend checks (bank ideas PRD-044 and PRD-045: the exact term, several years, not one graph)

HISTORY_MIN_YEARS = 3    # a trend read needs 3 or more years of history before a forecast is trusted


def trend_history(market, as_of_year):
    """Split a market's series into history (years up to as_of) and forecast; short-term growth from the last 2 history points,
    long-term growth a year from the first to the last history point; forecast growth from the last history point to the last forecast."""
    pts = sorted((p for p in (market.get('series') or []) if isinstance(p.get('value_usd'), (int, float)) and isinstance(p.get('year'), int)), key=lambda p: p['year'])
    hist = [p for p in pts if p['year'] <= as_of_year]
    fcst = [p for p in pts if p['year'] > as_of_year]
    out = {'history_years': (hist[-1]['year'] - hist[0]['year']) if len(hist) >= 2 else 0, 'history_points': len(hist), 'forecast_points': len(fcst),
           'short_growth': None, 'long_growth': None, 'forecast_growth': None, 'first_year': hist[0]['year'] if hist else None, 'last_year': hist[-1]['year'] if hist else None}
    if len(hist) >= 2:
        a, b = hist[-2], hist[-1]
        yrs = b['year'] - a['year']
        out['short_growth'] = round((b['value_usd'] / a['value_usd']) ** (1 / yrs) - 1, 4) if yrs and a['value_usd'] else None
        a, b = hist[0], hist[-1]
        yrs = b['year'] - a['year']
        out['long_growth'] = round((b['value_usd'] / a['value_usd']) ** (1 / yrs) - 1, 4) if yrs and a['value_usd'] else None
    if hist and fcst:
        a, b = hist[-1], fcst[-1]
        yrs = b['year'] - a['year']
        out['forecast_growth'] = round((b['value_usd'] / a['value_usd']) ** (1 / yrs) - 1, 4) if yrs and a['value_usd'] else None
    if out['history_years'] >= HISTORY_MIN_YEARS and out['short_growth'] is not None and out['long_growth'] is not None:
        out['verdict'] = 'fad_risk' if out['short_growth'] > 2 * max(out['long_growth'], 0.0) + 0.02 else 'steady' if out['long_growth'] > 0 else 'falling'
    elif out['history_points'] >= 1:
        out['verdict'] = 'forecast_only'
    else:
        out['verdict'] = 'no_series'
    return out


def trend_checks(br, brand, ends_on):
    fx = web_pass(br) or {}
    markets = {m.get('key'): m for m in fx.get('markets') or []}
    cands = candidate_lanes(brand)
    rows = []
    for key, label, _ in lanes_for(br):
        keys = LANE_MARKET.get(key, [])
        best = None
        for k in keys:
            m = markets.get(k)
            if not m:
                continue
            h = trend_history(m, ends_on.year)
            src = (m.get('sources') or [{}])[0]
            row = dict(h, key=key, label=label, market=m.get('label'), market_key=k, cagr_pct=m.get('cagr_pct'), cite=f"{src.get('publisher') or 'public source'}, {src.get('date') or 'undated'}", url=src.get('url'))
            if best is None or row['history_years'] > best['history_years']:
                best = row
        if best is None:
            best = {'key': key, 'label': label, 'market': None, 'market_key': None, 'verdict': 'no_series', 'history_years': 0, 'history_points': 0, 'forecast_points': 0,
                    'short_growth': None, 'long_growth': None, 'forecast_growth': None, 'cagr_pct': None, 'cite': None, 'url': None, 'first_year': None, 'last_year': None}
        best['candidates'] = cands.get(key, [])
        best['finding_id'] = f'{SCREEN}.PROD-R29.{key}'
        rows.append(best)
    order = {'fad_risk': 0, 'forecast_only': 1, 'no_series': 2, 'falling': 3, 'steady': 4}
    rows.sort(key=lambda r: (order[r['verdict']], r['label']))
    return {'rows': rows, 'rule': f'a trend read is trusted with {HISTORY_MIN_YEARS} or more years of history on the exact lane term; fad risk when the last-year growth is more than twice the multi-year rate; forecast only when the series holds a current point and a projection but no history'}


def trend_check_findings(br, brand, ends_on):
    """PROD-R29: a lane with an open candidate whose market trend rests on a forecast (or on one year) and has no multi-year history on file, or reads as a fad."""
    out = []
    for r in trend_checks(br, brand, ends_on)['rows']:
        if not r['candidates'] or r['verdict'] not in ('forecast_only', 'fad_risk', 'no_series'):
            continue
        ev = [_ev('trend_history_years', r['history_years'], 'years', ends_on.isoformat(), 'web pass', HISTORY_MIN_YEARS, 'threshold', source=r['url'] or 'fixtures.market_trends', simulated=False, freshness_days=0,
                  verdict=r['verdict'], history_points=r['history_points'], forecast_points=r['forecast_points']),
              _ev('short_growth', r['short_growth'], 'ratio', ends_on.isoformat(), 'last 2 history points', source='fixtures.market_trends', simulated=False, freshness_days=0),
              _ev('long_growth', r['long_growth'], 'ratio', ends_on.isoformat(), 'history', source='fixtures.market_trends', simulated=False, freshness_days=0)]
        if r['verdict'] == 'fad_risk':
            what = f'last-year growth {round(r["short_growth"] * 100)} percent against {round(r["long_growth"] * 100)} percent a year over {r["history_years"]} years: a spike, not a trend yet'
        elif r['verdict'] == 'forecast_only':
            what = f'the {r["market"]} series holds {r["history_points"]} current point and {r["forecast_points"]} forecast point{"s" if r["forecast_points"] != 1 else ""} ({r["cite"]}), no multi-year history'
        else:
            what = 'no market series is on file for the lane'
        sentence = f'{", ".join(r["candidates"][:2])} rests on {r["label"].lower()}: {what}. Check 3 or more years of history on the exact term before funding.'
        f = _finding('PROD-R29', r['key'], ends_on, 'low', ev, sentence, None, 0.7, [], money_reason='a trend check has no order count')
        f['entity'] = {'type': 'metric', 'id': r['key'], 'label': r['label'], 'verdict': r['verdict'], 'candidates': r['candidates'], 'market': r['market']}
        f['id'] = f'{SCREEN}.PROD-R29.{r["key"]}'
        out.append(f)
    return out


# ---------------------------------------------------------------- audience surfaces (round 3.6)

# reach floors per surface kind: below the floor a surface is a watch, not a gap
SURFACE_FLOOR = {'forum': {'quotes': 20, 'upvotes': 1000}, 'reviews': {'quotes': 30}, 'social': {'posts': 50}}
SURFACE_LABEL = {'amazon': 'Amazon reviews', 'own_site': 'Own site reviews', 'trustpilot': 'Trustpilot', 'retailer': 'Retailer reviews',
                 'other': 'Other review sites', 'amazon_customers_say': 'Amazon reviews'}
# social surfaces the brand can own an account on, and the words that show it does in its own records
SOCIAL_SURFACES = [('instagram', 'Instagram', ['instagram']), ('tiktok', 'TikTok', ['tiktok']), ('youtube', 'YouTube', ['youtube']),
                   ('pinterest', 'Pinterest', ['pinterest']), ('strava', 'Strava', ['strava']), ('facebook', 'Facebook', ['facebook'])]
PRESENCE_SECTIONS = ('channels', 'identity', 'site_map', 'marketplaces', 'offers', 'policies')


def presence_words(br):
    """Lower-case text of the records that say where the brand itself is present: channels, identity, site map, marketplaces, offers, policies."""
    if br is None:
        return ''
    parts = []
    for sec in PRESENCE_SECTIONS:
        for r in br.records(sec):
            if (r.get('value') or {}).get('role') == 'competitor' if isinstance(r.get('value'), dict) else False:
                continue
            parts.append(str(r.get('text') or ''))
            parts.append(json.dumps(r.get('value')))
    return ' '.join(parts).lower()


def _surface_row(key, label, kind, url=None):
    return {'key': key, 'label': label, 'kind': kind, 'url': url, 'quotes': 0, 'upvotes': None, 'posts': None, 'praise': 0, 'complaint': 0,
            'themes': {}, 'top_theme': None, 'top_theme_label': None, 'present': None, 'present_how': None, 'answered_on_site': None,
            'status': 'read', 'verdict': 'watch'}


def audience_surfaces(br, ends_on):
    """Where buyers of the category talk, one row per surface: the subreddits in the Reddit pull (quotes, upvotes, praise against
    complaint, loudest theme), each review source in the objection ladders (quotes, loudest theme), and the social surfaces the
    brand's own records name (the Instagram pull gives posts; the rest read unavailable). Presence is whether the brand's own
    records (channels, identity, site map, marketplaces, offers, policies) name the surface. Configured subreddits with no pull
    yet show as not pulled, never as 0. Usernames are never read; the rows are counts."""
    if br is None:
        return {'rows': [], 'rule': None, 'note': None}
    rows = {}
    site = brand_words(br)
    present = presence_words(br)
    # forums: the Reddit language bank
    for rec in br.records('language_bank'):
        v = rec.get('value') or {}
        sub = v.get('subreddit')
        if not sub:
            continue
        key = 'reddit:' + str(sub).lower()
        r = rows.setdefault(key, _surface_row(key, 'r/' + str(sub), 'forum', f'https://www.reddit.com/r/{sub}/'))
        r['quotes'] += 1
        r['upvotes'] = (r['upvotes'] or 0) + int(v.get('weight') or 0)
        if v.get('theme') == 'praise':
            r['praise'] += 1
        elif v.get('theme') == 'complaint':
            r['complaint'] += 1
        for th in v.get('themes') or ['general']:
            r['themes'][th] = r['themes'].get(th, 0) + 1
    cfg_path = APP / 'brain' / br.brand / 'config' / 'apify.json'
    cfg = json.loads(cfg_path.read_text(encoding='utf-8')) if cfg_path.is_file() else {}
    for sub in (cfg.get('reddit') or {}).get('subreddits') or []:
        key = 'reddit:' + str(sub).lower()
        if key not in rows:
            r = rows.setdefault(key, _surface_row(key, 'r/' + str(sub), 'forum', f'https://www.reddit.com/r/{sub}/'))
            r['status'] = 'not_pulled'
            r['upvotes'] = None
    # review sources: the objection ladders carry counts per source per theme
    for rec in br.records('objection_ladders'):
        v = rec.get('value') or {}
        th = LADDER_THEME.get(v.get('theme') or rec.get('field'))
        c = v.get('counts') or {}
        for src, n in (c.get('sources') or v.get('sources') or {}).items():
            if not n or src == 'reddit':
                continue
            src = 'amazon' if src == 'amazon_customers_say' else src
            key = 'reviews:' + src
            r = rows.setdefault(key, _surface_row(key, SURFACE_LABEL.get(src, pretty_source(src)), 'reviews'))
            r['quotes'] += int(n)
            if th:
                r['themes'][th] = r['themes'].get(th, 0) + int(n)
    # social surfaces named in the brand's own records; the Instagram pull gives posts
    social = social_pull_for(br) or {}
    for key, label, words in SOCIAL_SURFACES:
        if not any(w in present for w in words) and key != 'instagram':
            continue
        r = rows.setdefault('social:' + key, _surface_row('social:' + key, label, 'social'))
        if key == 'instagram' and social:
            r['posts'] = social.get('items')
            r['status'] = 'mock' if social.get('mode') != 'live' else 'read'
            for th, g in (social.get('themes') or {}).items():
                r['themes'][th] = r['themes'].get(th, 0) + int(g.get('posts') or 0)
                r['praise'] += int(g.get('praise') or 0)
                r['complaint'] += int(g.get('complaint') or 0)
        elif key == 'instagram':
            r['status'] = 'not_pulled'
        else:
            r['status'] = 'no_pull'
    # presence, loudest theme, verdict
    out = []
    for r in rows.values():
        kind = r['kind']
        name = r['label'].lower().replace('r/', '')
        if kind == 'forum':
            r['present'] = ('reddit' in present) or ('r/' + name in present)
            r['present_how'] = 'a record names Reddit' if r['present'] else 'no channel, identity or site record names Reddit'
        elif kind == 'reviews':
            src = r['key'].split(':', 1)[1]
            words = {'amazon': ['amazon'], 'own_site': ['review', 'yotpo', 'okendo', 'stamped'], 'trustpilot': ['trustpilot'], 'retailer': ['nordstrom', 'target', 'dsw', "dick's", 'athleta', 'wholesale'], 'other': []}.get(src, [src])
            r['present'] = any(w in present for w in words) if words else None
            r['present_how'] = ('a record names the surface' if r['present'] else 'no record names it') if r['present'] is not None else 'presence not readable'
        else:
            r['present'] = any(w in present for w in dict((k, ws) for k, _, ws in SOCIAL_SURFACES)[r['key'].split(':', 1)[1]])
            r['present_how'] = 'the brand runs an account here' if r['present'] else 'no channel record names it'
        themes = {k: v for k, v in r['themes'].items() if k != 'general'} or r['themes']
        if themes:
            top = max(themes.items(), key=lambda kv: kv[1])
            r['top_theme'], r['top_theme_label'] = top[0], THEME_LABEL.get(top[0], top[0])
            words = ANSWER_WORDS.get(top[0], [top[0]])
            r['answered_on_site'] = any(w in site for w in words) if site else None
        pc = r['praise'] + r['complaint']
        r['praise_share'] = round(r['praise'] / pc, 4) if pc else None
        floor = SURFACE_FLOOR[kind]
        if r['status'] in ('not_pulled', 'no_pull'):
            r['verdict'] = 'not_pulled'
        elif kind == 'forum':
            r['reach'] = r['quotes'] >= floor['quotes'] or (r['upvotes'] or 0) >= floor['upvotes']
        elif kind == 'reviews':
            r['reach'] = r['quotes'] >= floor['quotes']
        else:
            r['reach'] = (r['posts'] or 0) >= floor['posts']
        if r['verdict'] != 'not_pulled':
            r['verdict'] = 'gap' if r['reach'] and not r['present'] else 'present' if r['present'] else 'watch'
        r['finding_id'] = f'{SCREEN}.PROD-R30.{r["key"].replace(":", "-")}'
        out.append(r)
    order = {'gap': 0, 'present': 1, 'watch': 2, 'not_pulled': 3}
    out.sort(key=lambda r: (order[r['verdict']], -(r['upvotes'] or 0), -(r['quotes'] or 0), -(r['posts'] or 0), r['label']))
    return {'rows': out, 'floors': SURFACE_FLOOR,
            'rule': 'a surface has reach at 20 quotes or 1,000 upvotes (forum), 30 quotes (review source) or 50 posts (social); a gap is reach with no record of the brand on it',
            'note': 'Reddit rows are counts of public posts and comments in the language bank; usernames are never read and no Reddit user is quoted as a testimonial.'}


def pretty_source(src):
    return str(src).replace('_', ' ').capitalize()


def audience_findings(br, ends_on):
    """PROD-R30: a surface where the category conversation has reach (floor per kind) and no record shows the brand present on it."""
    out = []
    if br is None:
        return out
    for r in audience_surfaces(br, ends_on)['rows']:
        if r['verdict'] != 'gap':
            continue
        floor = SURFACE_FLOOR[r['kind']]
        ev = [_ev('quotes', r['quotes'] if r['kind'] != 'social' else r['posts'], 'count', ends_on.isoformat(), 'past year' if r['kind'] == 'forum' else 'all to capture',
                  floor.get('quotes') or floor.get('posts'), 'threshold', source='brain.language_bank' if r['kind'] == 'forum' else 'brain.objection_ladders' if r['kind'] == 'reviews' else 'fixtures.social_pull',
                  simulated=False, freshness_days=0, surface=r['label']),
              _ev('brand_records_naming_surface', 0, 'count', ends_on.isoformat(), 'brain now', 1, 'threshold', source='brain.channels', simulated=False, freshness_days=0)]
        if r['upvotes'] is not None:
            ev.insert(1, _ev('upvotes', r['upvotes'], 'count', ends_on.isoformat(), 'past year', floor.get('upvotes'), 'threshold', source='brain.language_bank', simulated=False, freshness_days=0))
        reach = (f'{r["quotes"]} quotes and {r["upvotes"]:,} upvotes' if r['kind'] == 'forum' else f'{r["quotes"]} review quotes' if r['kind'] == 'reviews' else f'{r["posts"]} posts')
        theme = f' The loudest theme there is {r["top_theme_label"].lower()}' + (', which the site does not answer.' if r['answered_on_site'] is False else '.') if r['top_theme_label'] else ''
        sentence = f'{r["label"]} carries {reach} about the category and no record shows the brand present on it.{theme}'
        sev = 'high' if (r['upvotes'] or 0) >= 10 * SURFACE_FLOOR['forum']['upvotes'] else 'medium'
        f = _finding('PROD-R30', r['key'].replace(':', '-'), ends_on, sev, ev, sentence, None, 0.6, [f'{br.brand}.content.reddit_topics'] if r['kind'] == 'forum' else [],
                     money_reason='reach on a surface the brand does not own has no order count until a listening post runs')
        f['entity'] = {'type': 'metric', 'id': r['key'], 'label': r['label'], 'kind': r['kind'], 'url': r['url'], 'top_theme': r['top_theme_label'],
                       'answered_on_site': r['answered_on_site'], 'quotes': r['quotes'], 'upvotes': r['upvotes'], 'posts': r['posts']}
        f['id'] = f'{SCREEN}.PROD-R30.{r["key"].replace(":", "-")}'
        out.append(f)
    return out


# ---------------------------------------------------------------- marketplace seller read (round 3.7)

PACK_RE = re.compile(r'(\d+)\s*[- ]?\s*(?:pair|pairs|pack|pcs|pk)\b', re.I)
PRICE_SPREAD = 0.25          # a listing per-pair price 25 percent off the site per-pair price either way is a spread
LISTING_MIN_RATINGS = 20     # below this a listing is thin: read, not judged
UNVERIFIED_MAX_RATINGS = 10  # a listing with fewer ratings than this and no seller read is unverified as the brand's


def pack_units_from_title(title):
    """Pairs in a listing from its title (4 Pair, 6-Pack, 2pcs, 8 Pairs); 1 when the title says nothing."""
    m = PACK_RE.search(str(title or ''))
    n = int(m.group(1)) if m else 1
    return n if 0 < n <= 30 else 1


def marketplace_read(br, prods):
    """Who sells the brand on Amazon and at what price per pair. Rows come from the brain's marketplace listing records
    (one per ASIN, price, stars, ratings, seller when read); the presence record says whether a brand store, A+ content or
    a brand-as-seller offer showed and which resellers did. Price per pair is the listing price over the pairs in the
    title, against the site's per-pair price from our_price_per_pair. Seller null reads not read, never the brand."""
    if br is None:
        return {'presence': None, 'rows': [], 'site_per_pair': None, 'summary': None, 'rule': None}
    presence = None
    listings = {}
    for r in br.records('marketplaces'):
        v = r.get('value') or {}
        if not isinstance(v, dict):
            continue
        if r.get('field') == 'amazon_presence' or 'brand_store' in v:
            presence = {'record': r['id'], 'brand_store': v.get('brand_store'), 'sold_by_brand': v.get('sold_by_bombas_on_listings_read', v.get('sold_by_brand')),
                        'resellers': list(v.get('resellers_seen') or []), 'aplus': v.get('aplus_content_seen'), 'asins_read': list(v.get('asins_read') or []),
                        'lines_not_found': list(v.get('lines_not_found') or []), 'in_stock': v.get('listings_in_stock'), 'text': r.get('text'),
                        'captured_at': (r.get('source') or {}).get('captured_at'), 'url': (r.get('source') or {}).get('ref') if str((r.get('source') or {}).get('ref', '')).startswith('http') else None}
            continue
        if v.get('asin') and v.get('channel', 'amazon') == 'amazon':
            l = listings.setdefault(v['asin'], {'asin': v['asin'], 'title': None, 'price_usd': None, 'stars': None, 'ratings': None, 'seller': None, 'url': None, 'variants': None})
            for k, src in (('title', 'title'), ('price_usd', 'price_usd'), ('stars', 'stars'), ('ratings', 'reviews_count'), ('seller', 'seller'), ('url', 'url'), ('variants', 'variants_seen')):
                if v.get(src) is not None and l.get(k) is None:
                    l[k] = v[src]
    site = our_price_per_pair(prods, br)
    site_pp = site.get('value')
    lp = listing_pull_for(br) or {}
    pull = {'mode': lp.get('mode'), 'captured_at': lp.get('captured_at'), 'rows': len(lp.get('rows') or []), 'actor': lp.get('actor'), 'usd': lp.get('usd'),
            'sellers_used': lp.get('mode') == 'live'} if lp else None
    if lp.get('mode') == 'live':   # a mock row is an invented shape: its seller is never read as fact
        for pr in lp.get('rows') or []:
            l = listings.get(pr.get('asin'))
            if l is None:
                continue
            for k, src in (('seller', 'seller'), ('price_usd', 'price_usd'), ('stars', 'stars'), ('ratings', 'ratings'), ('title', 'title'), ('url', 'url')):
                if pr.get(src) is not None and (k == 'seller' or l.get(k) is None):
                    l[k] = pr[src]
    rows = []
    for l in listings.values():
        l['pack_units'] = pack_units_from_title(l['title'])
        l['per_pair'] = round(l['price_usd'] / l['pack_units'], 2) if l['price_usd'] else None
        l['spread'] = round(l['per_pair'] / site_pp - 1, 4) if l['per_pair'] and site_pp else None
        l['seller_read'] = l['seller'] is not None
        l['sold_by_brand'] = (str(l['seller']).lower().startswith(br.brand.lower())) if l['seller'] else None
        l['url'] = l['url'] or f'https://www.amazon.com/dp/{l["asin"]}'
        if (l['ratings'] or 0) < UNVERIFIED_MAX_RATINGS and not l['seller_read']:
            l['verdict'] = 'unverified'
        elif l['sold_by_brand']:
            l['verdict'] = 'brand_sells'
        elif l['spread'] is not None and abs(l['spread']) >= PRICE_SPREAD and (l['ratings'] or 0) >= LISTING_MIN_RATINGS:
            l['verdict'] = 'price_spread'
        elif l['sold_by_brand'] is False or (presence and presence.get('sold_by_brand') is False and l['asin'] in presence.get('asins_read', [])):
            l['verdict'] = 'reseller'
        else:
            l['verdict'] = 'seller_not_read'
        l['finding_id'] = f'{SCREEN}.PROD-R32.{l["asin"].lower()}' if l['verdict'] == 'price_spread' else f'{SCREEN}.PROD-R31.amazon'
        rows.append(l)
    order = {'price_spread': 0, 'reseller': 1, 'seller_not_read': 2, 'brand_sells': 3, 'unverified': 4}
    rows.sort(key=lambda l: (order[l['verdict']], -(l['ratings'] or 0)))
    judged = [l for l in rows if l['verdict'] != 'unverified']
    ratings = sum(l['ratings'] or 0 for l in judged)
    pps = [l['per_pair'] for l in judged if l['per_pair'] and (l['ratings'] or 0) >= LISTING_MIN_RATINGS]
    summary = {'listings': len(rows), 'judged': len(judged), 'unverified': len(rows) - len(judged), 'ratings': ratings,
               'median_per_pair': round(statistics.median(pps), 2) if pps else None, 'spread_listings': sum(1 for l in rows if l['verdict'] == 'price_spread'),
               'sellers_read': sum(1 for l in rows if l['seller_read'])}
    return {'presence': presence, 'rows': rows, 'site_per_pair': site, 'summary': summary, 'pull': pull,
            'rule': f'the brand should be the seller of record or hold the brand store on its own listings; a listing per-pair price {int(PRICE_SPREAD * 100)} percent off the site price either way on {LISTING_MIN_RATINGS} or more ratings is a spread; under {UNVERIFIED_MAX_RATINGS} ratings with no seller read is unverified as the brand\'s'}


def marketplace_findings(br, prods, ends_on):
    """PROD-R31: the brand is not the seller of record and holds no brand store on its own Amazon listings (from the presence
    record). PROD-R32: a listing with 20 or more ratings priced 25 percent or more off the site per-pair price either way."""
    out = []
    m = marketplace_read(br, prods)
    p = m['presence']
    s = m['summary'] or {}
    if p and p.get('sold_by_brand') is False and not p.get('brand_store'):
        ev = [_ev('listings_sold_by_brand', 0, 'count', ends_on.isoformat(), 'listings read', len(p.get('asins_read') or []), 'threshold', source=p['record'], simulated=False, freshness_days=0,
                  resellers=p.get('resellers'), in_stock=p.get('in_stock'), captured_at=p.get('captured_at')),
              _ev('brand_store', 0, 'count', ends_on.isoformat(), 'now', 1, 'threshold', source=p['record'], simulated=False, freshness_days=0, aplus_content=p.get('aplus')),
              _ev('public_ratings_on_listings', s.get('ratings'), 'count', ends_on.isoformat(), 'all time', source='brain.marketplaces', simulated=False, freshness_days=0, listings=s.get('judged'))]
        missing = ', '.join(x.replace('_', ' ') for x in p.get('lines_not_found') or [])
        sentence = (f'On Amazon every in-stock offer read ({p.get("in_stock")} of {len(p.get("asins_read") or [])} listings) is a third-party reseller ({", ".join(p.get("resellers") or []) or "names not read"}); '
                    f'no brand store and no A+ content showed. {s.get("judged")} listings carry {s.get("ratings"):,} public ratings.' + (f' Not found on Amazon: {missing}.' if missing else ''))
        f = _finding('PROD-R31', 'amazon', ends_on, 'high', ev, sentence, None, 0.8, [p['record']], money_reason='reseller sales on the marketplace are not in our order data')
        f['entity'] = {'type': 'brand', 'id': 'amazon', 'label': 'Amazon', 'resellers': p.get('resellers'), 'listings': s.get('judged'), 'ratings': s.get('ratings'),
                       'lines_not_found': p.get('lines_not_found'), 'median_per_pair': s.get('median_per_pair'), 'site_per_pair': (m['site_per_pair'] or {}).get('value')}
        f['id'] = f'{SCREEN}.PROD-R31.amazon'
        out.append(f)
    site_pp = (m['site_per_pair'] or {}).get('value')
    for l in m['rows']:
        if l['verdict'] != 'price_spread':
            continue
        ev = [_ev('listing_price_per_pair', l['per_pair'], 'usd', ends_on.isoformat(), 'listing now', site_pp, 'threshold', source=l['url'], simulated=False, freshness_days=0,
                  pack_units=l['pack_units'], price_usd=l['price_usd'], note=(m['site_per_pair'] or {}).get('basis')),
              _ev('price_spread', l['spread'], 'ratio', ends_on.isoformat(), 'listing now', PRICE_SPREAD, 'threshold', source=l['url'], simulated=False, freshness_days=0),
              _ev('ratings', l['ratings'], 'count', ends_on.isoformat(), 'all time', LISTING_MIN_RATINGS, 'threshold', source='brain.marketplaces', simulated=False, freshness_days=0)]
        way = 'above' if l['spread'] > 0 else 'below'
        sentence = (f'{l["title"]} ({l["asin"]}) lists at ${l["price_usd"]:,.2f} for {l["pack_units"]} pair{"s" if l["pack_units"] != 1 else ""}, ${l["per_pair"]:,.2f} a pair, '
                    f'{abs(round(l["spread"] * 100))} percent {way} the site per-pair price of ${site_pp:,.2f}, with {l["ratings"]:,} ratings and the seller {("read as " + l["seller"]) if l["seller"] else "not read"}.')
        f = _finding('PROD-R32', l['asin'].lower(), ends_on, 'medium', ev, sentence, None, 0.6, [], money_reason='units sold on the listing are not visible; a price spread is a brand price integrity risk, not a measured loss')
        f['entity'] = {'type': 'sku', 'id': l['asin'], 'label': l['title'], 'url': l['url'], 'per_pair': l['per_pair'], 'site_per_pair': site_pp, 'spread': l['spread'], 'way': way, 'ratings': l['ratings'], 'seller': l['seller']}
        f['id'] = f'{SCREEN}.PROD-R32.{l["asin"].lower()}'
        out.append(f)
    return out


# ---------------------------------------------------------------- competitor launch cadence (round 3.8)

CADENCE_MIN_LAUNCHES_12M = 2     # competitor launches in a lane over 12 months that make it a lane in play
CADENCE_MIN_BRANDS_24M = 2       # or distinct competitor brands launching in the lane over 24 months
CADENCE_QUIET_MONTHS = 24        # our lane is quiet when we launched nothing in it for this long


def launch_date(text):
    """A launch date from the web pass (2026-09-24, 2026-09 or 2026) as a date: the 15th for a month, 1 July for a year, None otherwise."""
    t = str(text or '').strip()
    try:
        if len(t) >= 10:
            return date.fromisoformat(t[:10])
        if len(t) == 7:
            return date(int(t[:4]), int(t[5:7]), 15)
        if len(t) == 4:
            return date(int(t), 7, 1)
    except ValueError:
        return None
    return None


def months_between(a, b):
    return (b.year - a.year) * 12 + (b.month - a.month) + (b.day - a.day) / 30.0


def brain_launches(br, lane_defs=None):
    """Our own launches from the brain calendar (records whose field starts with launch_): what launched, when, and the lanes
    its category words name, in the web pass launch shape, so the cadence read sees more than what the press covered."""
    out = []
    if br is None:
        return out
    lane_defs = lane_defs if lane_defs is not None else lanes_for(br)
    for rec in br.records('calendar'):
        if not str(rec.get('field') or '').startswith('launch_'):
            continue
        v = rec.get('value') or {}
        when = v.get('date') or v.get('month') or (str(v.get('year')) if v.get('year') else None)
        cats = [c for c in ([v.get('category')] if v.get('category') else []) + list(v.get('categories') or [])]
        cat_text = ' ' + ' '.join(cats).lower().replace('-', ' ').replace('_', ' ') + ' '
        lanes = [k for k, _, terms in lane_defs if any(t.replace('-', ' ') in cat_text for t in terms)]
        if not lanes:   # no category words: fall back to the record's sentence
            text = str(rec.get('text') or '').lower().replace('-', ' ')
            lanes = [k for k, _, terms in lane_defs if any(t.replace('-', ' ') in text for t in terms)]
        out.append({'brand': br.brand, 'self': True, 'what': str(rec.get('text') or '')[:160], 'sub_category': lanes[0] if lanes else (cats[0] if cats else 'other'),
                    'lanes': lanes or [cats[0] if cats else 'other'], 'date': when, 'price_usd': v.get('price_usd'), 'channel': 'dtc',
                    'sources': [{'url': (rec.get('source') or {}).get('ref'), 'publisher': (rec.get('source') or {}).get('type'), 'date': str((rec.get('source') or {}).get('captured_at') or '')}],
                    'from': 'brain.calendar', 'record': rec.get('id')})
    return out


def launch_cadence(br, ends_on):
    """Who launches, how often, and in which lanes, from the web pass launches (a url and a date on each). Per brand: launches
    in the last 12 and 24 months, months since the last, the lanes and channels, median price. Per lane: competitor launches
    in 12 months and the brands behind them, ours in 24 months, whether we sell the lane, and the verdict: in play (competitors
    launching, none of ours), matched (both), quiet (nobody), not sold."""
    fx = web_pass(br) or {}
    launches = fx.get('launches') or []
    lane_defs = lanes_for(br)
    brand_name = (br.brand if br else '').lower()
    words = brand_words(br)
    rows = []
    for l in launches:
        d = launch_date(l.get('date'))
        if d is None or d > ends_on:
            continue
        lanes = [k for k, _, terms in lane_defs if l.get('sub_category') == k or any(t in (l.get('what') or '').lower() for t in terms)]
        rows.append({'brand': l.get('brand'), 'self': (l.get('brand') or '').lower() == brand_name, 'what': l.get('what'), 'date': d, 'date_text': l.get('date'),
                     'months_ago': months_between(d, ends_on), 'lanes': lanes or [l.get('sub_category') or 'other'], 'price_usd': l.get('price_usd'),
                     'channel': l.get('channel'), 'url': (l.get('sources') or [{}])[0].get('url'), 'from': 'web_pass'})
    ours_seen = [(r['date'], set(r['lanes'])) for r in rows if r['self']]
    for l in brain_launches(br, lane_defs):   # the brand's own launch history from the brain calendar, unless the web pass already has it
        d = launch_date(l.get('date'))
        if d is None or d > ends_on:
            continue
        if any(abs((d - od).days) <= 60 and (set(l['lanes']) & olanes) for od, olanes in ours_seen):
            continue
        rows.append({'brand': l['brand'], 'self': True, 'what': l['what'], 'date': d, 'date_text': l['date'], 'months_ago': months_between(d, ends_on), 'lanes': l['lanes'],
                     'price_usd': l.get('price_usd'), 'channel': l['channel'], 'url': (l.get('sources') or [{}])[0].get('url'), 'from': 'brain.calendar'})
    brands = {}
    for r in rows:
        b = brands.setdefault(r['brand'], {'brand': r['brand'], 'self': r['self'], 'n_12m': 0, 'n_24m': 0, 'last': None, 'lanes': set(), 'channels': set(), 'prices': [], 'launches': []})
        if r['months_ago'] <= 12:
            b['n_12m'] += 1
        if r['months_ago'] <= 24:
            b['n_24m'] += 1
        if b['last'] is None or r['date'] > b['last']:
            b['last'] = r['date']
        b['lanes'] |= set(r['lanes'])
        if r['channel']:
            b['channels'].add(r['channel'])
        if r['price_usd']:
            b['prices'].append(float(r['price_usd']))
        b['launches'].append({'what': r['what'], 'date': r['date_text'], 'lanes': r['lanes'], 'price_usd': r['price_usd'], 'url': r['url'], 'from': r.get('from')})
    brand_rows = []
    for b in brands.values():
        brand_rows.append({'brand': b['brand'], 'self': b['self'], 'n_12m': b['n_12m'], 'n_24m': b['n_24m'], 'last': b['last'].isoformat(),
                           'months_since_last': round(months_between(b['last'], ends_on), 1), 'lanes': sorted(b['lanes']), 'channels': sorted(b['channels']),
                           'median_price': round(statistics.median(b['prices']), 2) if b['prices'] else None, 'launches': sorted(b['launches'], key=lambda x: x['date'] or '', reverse=True)})
    for b in brand_rows:
        b['from_brain'] = sum(1 for r in rows if r['brand'] == b['brand'] and r.get('from') == 'brain.calendar')
    brand_rows.sort(key=lambda b: (-b['n_12m'], -b['n_24m'], b['months_since_last']))
    comp_n12 = [b['n_12m'] for b in brand_rows if not b['self']]
    ours = next((b for b in brand_rows if b['self']), None)
    lane_rows = []
    for key, label, terms in lane_defs:
        theirs_12 = [r for r in rows if not r['self'] and key in r['lanes'] and r['months_ago'] <= 12]
        theirs_24 = [r for r in rows if not r['self'] and key in r['lanes'] and r['months_ago'] <= 24]
        ours_24 = [r for r in rows if r['self'] and key in r['lanes'] and r['months_ago'] <= CADENCE_QUIET_MONTHS]
        ours_any = [r for r in rows if r['self'] and key in r['lanes']]
        sold = (any(t in words for t in terms) or bool(ours_any)) if words else None
        brands_24 = sorted({r['brand'] for r in theirs_24})
        in_play = len(theirs_12) >= CADENCE_MIN_LAUNCHES_12M or len(brands_24) >= CADENCE_MIN_BRANDS_24M
        newest = max(theirs_24, key=lambda r: r['date']) if theirs_24 else None
        last_ours = max(ours_any, key=lambda r: r['date']) if ours_any else None
        if key in PROOF_LANES:
            verdict = 'proof'
        elif sold is False:
            verdict = 'not_sold'
        elif in_play and not ours_24:
            verdict = 'in_play'
        elif theirs_24 and ours_24:
            verdict = 'matched'
        elif theirs_24 or ours_24:
            verdict = 'watch'
        else:
            verdict = 'quiet'
        lane_rows.append({'key': key, 'label': label, 'theirs_12m': len(theirs_12), 'theirs_24m': len(theirs_24), 'brands_24m': brands_24, 'ours_24m': len(ours_24), 'sold': sold,
                          'newest': {'brand': newest['brand'], 'what': newest['what'], 'date': newest['date_text'], 'url': newest['url']} if newest else None,
                          'our_last': {'what': last_ours['what'], 'date': last_ours['date_text']} if last_ours else None,
                          'months_since_ours': round(months_between(last_ours['date'], ends_on), 1) if last_ours else None,
                          'verdict': verdict, 'finding_id': f'{SCREEN}.PROD-R33.{key}'})
    order = {'in_play': 0, 'matched': 1, 'watch': 2, 'quiet': 3, 'proof': 4, 'not_sold': 5}
    lane_rows.sort(key=lambda r: (order[r['verdict']], -r['theirs_12m'], -r['theirs_24m']))
    return {'brands': brand_rows, 'lanes': lane_rows, 'launches_read': len(rows),
            'ours': {'n_12m': ours['n_12m'] if ours else 0, 'n_24m': ours['n_24m'] if ours else 0, 'months_since_last': ours['months_since_last'] if ours else None} if brand_name else None,
            'competitor_median_12m': statistics.median(comp_n12) if comp_n12 else None, 'captured_at': fx.get('captured_at'),
            'rule': f'a lane is in play when competitors launched {CADENCE_MIN_LAUNCHES_12M} or more times in it over 12 months, or {CADENCE_MIN_BRANDS_24M} or more brands launched in it over 24 months, and we sell it with nothing of ours launched there in {CADENCE_QUIET_MONTHS} months'}


def cadence_findings(br, ends_on):
    """PROD-R33: a lane we sell where competitors launched 2 or more times in 12 months (or 2 or more brands in 24) and nothing of ours launched in 24 months."""
    out = []
    if br is None:
        return out
    for r in launch_cadence(br, ends_on)['lanes']:
        if r['verdict'] != 'in_play':
            continue
        ev = [_ev('competitor_launches_12m', r['theirs_12m'], 'count', ends_on.isoformat(), 'past 12 months', CADENCE_MIN_LAUNCHES_12M, 'threshold', source='fixtures.market_trends', simulated=False, freshness_days=0, brands=r['brands_24m']),
              _ev('competitor_brands_24m', len(r['brands_24m']), 'count', ends_on.isoformat(), 'past 24 months', CADENCE_MIN_BRANDS_24M, 'threshold', source='fixtures.market_trends', simulated=False, freshness_days=0),
              _ev('our_launches_24m', r['ours_24m'], 'count', ends_on.isoformat(), 'past 24 months', 1, 'threshold', source='fixtures.market_trends', simulated=False, freshness_days=0,
                  months_since_ours=r['months_since_ours'])]
        nw = r['newest'] or {}
        last = f' Our last launch there was {r["months_since_ours"]:.0f} months ago.' if r['months_since_ours'] is not None else ' Nothing of ours launched there on file.'
        sentence = (f'{", ".join(r["brands_24m"])} launched {r["theirs_24m"]} time{"s" if r["theirs_24m"] != 1 else ""} in {r["label"].lower()} over 24 months '
                    f'({r["theirs_12m"]} in the last 12), newest {nw.get("brand")} {nw.get("date")}: {(nw.get("what") or "")[:90]}.{last}')
        f = _finding('PROD-R33', r['key'], ends_on, 'medium', ev, sentence, None, 0.6, [], money_reason='an unlaunched SKU has no baseline; the lane\'s net sales are in the trend strip')
        f['entity'] = {'type': 'metric', 'id': r['key'], 'label': r['label'], 'brands': r['brands_24m'], 'theirs_12m': r['theirs_12m'], 'theirs_24m': r['theirs_24m'], 'newest': nw, 'months_since_ours': r['months_since_ours']}
        f['id'] = f'{SCREEN}.PROD-R33.{r["key"]}'
        out.append(f)
    return out


# ---------------------------------------------------------------- return rate by line (round 4.3)

RETURN_MIN_RETURNS = 20      # a line is judged on 20 or more returns
RETURN_MEDIAN_X = 1.5        # ... returning at 1.5 times the store median or more
RETURN_MONTHS = 12


def return_rates(data, brand, ends_on):
    """Per line: units sold over the last 12 whole months (order line items), returns opened on those lines in the same span
    (reversed orders of type return, by SKU), the rate, the top reasons, against the store median. Unavailable, never 0, when
    orders or reversed orders are not connected. Room metric sku_return_rate."""
    source = brand_data(brand) if brand else data
    try:
        orders = source.table('orders')
        products = source.table('products')
    except (KeyError, ValueError) as exc:
        return {'unavailable': True, 'reason': f'orders are not connected ({exc})', 'fix': 'shopify', 'rows': []}
    try:
        reversed_rows = source.table('reversed_orders')
    except (KeyError, ValueError) as exc:
        return {'unavailable': True, 'reason': f'returns are not connected ({exc})', 'fix': 'shopify', 'rows': []}
    last = last_whole_month(ends_on)
    first = month_add(last, 1 - RETURN_MONTHS)
    line_of = {p.get('sku'): metrics().product_line(p.get('title')) or p.get('sku') for p in products if p.get('sku')}
    cat_of = {p.get('sku'): (p.get('type') or p.get('category') or 'other') for p in products if p.get('sku')}
    sold, ret, reasons, cats = {}, {}, {}, {}
    for o in orders:
        if o.get('cancelled_at'):
            continue
        m = str(o.get('created_at') or '')[:7]
        if not (first <= m <= last):
            continue
        for l in o.get('line_items') or []:
            line = line_of.get(l.get('sku'), l.get('title') or l.get('sku'))
            sold[line] = sold.get(line, 0) + int(l.get('qty') or 0)
            cats.setdefault(line, cat_of.get(l.get('sku'), 'other'))
    for r in reversed_rows:
        if r.get('type') != 'return':
            continue
        m = str(r.get('opened_at') or '')[:7]
        if not (first <= m <= last):
            continue
        line = line_of.get(r.get('sku'), r.get('sku'))
        ret[line] = ret.get(line, 0) + 1
        rs = reasons.setdefault(line, {})
        rs[r.get('reason') or 'unstated'] = rs.get(r.get('reason') or 'unstated', 0) + 1
    rows = []
    for line, units in sold.items():
        n = ret.get(line, 0)
        rate = round(n / units, 4) if units else None
        top = sorted(reasons.get(line, {}).items(), key=lambda kv: -kv[1])
        rows.append({'line': line, 'category': cats.get(line), 'units': units, 'returns': n, 'rate': rate, 'reasons': top[:3],
                     'top_reason': top[0][0] if top else None, 'top_reason_share': round(top[0][1] / n, 4) if top and n else None,
                     'finding_id': f'{SCREEN}.PROD-R34.{slug(line)}'})
    rates = [r['rate'] for r in rows if r['rate'] is not None and r['returns'] >= RETURN_MIN_RETURNS]
    median = round(statistics.median(rates), 4) if rates else None
    total_units = sum(sold.values())
    total_ret = sum(ret.values())
    for r in rows:
        r['x_median'] = round(r['rate'] / median, 2) if r['rate'] is not None and median else None
        r['verdict'] = ('high' if r['returns'] >= RETURN_MIN_RETURNS and median and r['rate'] >= RETURN_MEDIAN_X * median
                        else 'thin' if r['returns'] < RETURN_MIN_RETURNS else 'normal')
    order = {'high': 0, 'normal': 1, 'thin': 2}
    rows.sort(key=lambda r: (order[r['verdict']], -(r['rate'] or 0)))
    return {'unavailable': False, 'first': first, 'last': last, 'rows': rows, 'median': median, 'store_rate': round(total_ret / total_units, 4) if total_units else None,
            'units': total_units, 'returns': total_ret,
            'rule': f'a line is judged on {RETURN_MIN_RETURNS} or more returns; high at {RETURN_MEDIAN_X} times the store median rate; units are order line items and returns are the return leg of reversed orders, both over the last 12 whole months'}


def return_findings(data, brand, ends_on, net_28d):
    """PROD-R34: a line returning at 1.5 times the store median rate on 20 or more returns. Money: the returns above the
    median rate times the line's net sales per unit (the refunds the line would not have given at the store rate)."""
    out = []
    rr = return_rates(data, brand, ends_on)
    if rr.get('unavailable'):
        if 'returns are not connected' in rr['reason']:   # orders exist, returns do not: say so once; no orders at all is PROD-R17's connect card
            out.append(_unavailable('PROD-R34', ends_on, rr['reason'], ['orders', 'reversed_orders'], 'shopify', 'connect the store\'s returns (reversed orders) so return rates by line can be read'))
        return out
    for r in rr['rows']:
        if r['verdict'] != 'high':
            continue
        excess = r['returns'] - rr['median'] * r['units']
        ev = [_ev('return_rate', r['rate'], 'ratio', ends_on.isoformat(), f'{rr["first"]} to {rr["last"]}', rr['median'], 'median', source='reversed_orders', simulated=True, freshness_days=0,
                  returns=r['returns'], units=r['units'], x_median=r['x_median']),
              _ev('returns', r['returns'], 'count', ends_on.isoformat(), f'{rr["first"]} to {rr["last"]}', RETURN_MIN_RETURNS, 'threshold', source='reversed_orders', simulated=True, freshness_days=0),
              _ev('top_reason_share', r['top_reason_share'], 'ratio', ends_on.isoformat(), f'{rr["first"]} to {rr["last"]}', source='reversed_orders', simulated=True, freshness_days=0, reason=r['top_reason'])]
        reasons = ', '.join(f'{k} {v}' for k, v in r['reasons'])
        sentence = (f'{r["line"]} returns {round(r["rate"] * 100, 1)} percent of units ({r["returns"]} of {r["units"]:,}), {r["x_median"]} times the store median of '
                    f'{round(rr["median"] * 100, 1)} percent. Reasons: {reasons}.')
        f = _finding('PROD-R34', slug(r['line']), ends_on, 'medium', ev, sentence, None, 0.7, [],
                     money_reason=f'{round(excess)} returns above the store rate; refund value per return is not in the orders table')
        f['entity'] = {'type': 'sku', 'id': r['line'], 'label': r['line'], 'category': r['category'], 'rate': r['rate'], 'median': rr['median'], 'returns': r['returns'],
                       'units': r['units'], 'top_reason': r['top_reason'], 'reasons': r['reasons']}
        f['id'] = f'{SCREEN}.PROD-R34.{slug(r["line"])}'
        out.append(f)
    return out


# ---------------------------------------------------------------- open questions (round 4.4)

QUESTION_MIN_QUOTES = 5     # a question earns a card at 5 or more complaint quotes behind it
QUESTION_WAIT_DAYS = 14     # ... or when asked this long ago with no answer
_QUOTES_RE = re.compile(r'(\d+)\s+complaint quotes')
_DOUBT_RE = re.compile(r'"([^"]+)"')
_LADDER_FIELD_RE = re.compile(r'^ladder_(.+?)_(\d+)$')


def open_questions(br, ends_on):
    """The questions the brain holds for the founder (open_questions), each tied to its theme and the complaint quotes behind
    it, with whether it was asked, answered, or never asked; and whether the brand's records now answer the theme anyway."""
    if br is None:
        return {'rows': [], 'rule': None}
    site = brand_words(br)
    rows = []
    for rec in br.records('open_questions'):
        v = rec.get('value') or {}
        q = v.get('question') or rec.get('text') or ''
        m = _LADDER_FIELD_RE.match(str(rec.get('field') or ''))
        ladder_theme = m.group(1) if m else None
        theme = LADDER_THEME.get(ladder_theme) if ladder_theme else None
        quotes = int(_QUOTES_RE.search(q).group(1)) if _QUOTES_RE.search(q) else None
        doubt = _DOUBT_RE.search(q).group(1) if _DOUBT_RE.search(q) else None
        asked, answered = v.get('asked_on'), v.get('answered_on')
        days_open = (ends_on - date.fromisoformat(str(asked)[:10])).days if asked and not answered else None
        words = ANSWER_WORDS.get(theme, []) if theme else []
        on_site = any(w in site for w in words) if (site and words) else None
        if answered:
            verdict = 'answered'
        elif asked and days_open is not None and days_open >= QUESTION_WAIT_DAYS:
            verdict = 'overdue'
        elif asked:
            verdict = 'asked'
        else:
            verdict = 'never_asked'
        rows.append({'id': rec['id'], 'question': q, 'doubt': doubt, 'theme': theme, 'theme_label': THEME_LABEL.get(theme, theme) if theme else None,
                     'quotes': quotes, 'who': v.get('who_can_answer'), 'why': v.get('why'), 'asked_on': asked, 'answered_on': answered, 'days_open': days_open,
                     'records_answer_theme': on_site, 'verdict': verdict, 'rung': int(m.group(2)) if m else None,
                     'finding_id': f'{SCREEN}.PROD-R35.{rec["field"]}'})
    order = {'overdue': 0, 'never_asked': 1, 'asked': 2, 'answered': 3}
    rows.sort(key=lambda r: (order[r['verdict']], -(r['quotes'] or 0)))
    return {'rows': rows, 'rule': f'a question earns a card at {QUESTION_MIN_QUOTES} or more complaint quotes behind it and never asked, or asked {QUESTION_WAIT_DAYS} or more days ago with no answer'}


def question_findings(br, ends_on):
    """PROD-R35: an open question for the founder with 5 or more complaint quotes behind it, never asked or asked 14 or more days ago with no answer."""
    out = []
    for r in open_questions(br, ends_on)['rows']:
        if r['verdict'] not in ('never_asked', 'overdue') or (r['quotes'] or 0) < QUESTION_MIN_QUOTES:
            continue
        ev = [_ev('complaint_quotes', r['quotes'], 'count', ends_on.isoformat(), 'all reviews to capture', QUESTION_MIN_QUOTES, 'threshold', source=r['id'], simulated=False, freshness_days=0, doubt=r['doubt']),
              _ev('days_since_asked', r['days_open'], 'days', ends_on.isoformat(), 'brain now', QUESTION_WAIT_DAYS, 'threshold', source=r['id'], simulated=False, freshness_days=0, asked_on=r['asked_on'])]
        state = f'asked {r["days_open"]} days ago with no answer' if r['verdict'] == 'overdue' else 'never asked'
        sentence = f'{r["question"]} The founder is the one who can answer it and it was {state}.'
        f = _finding('PROD-R35', r['id'].split('.')[-1], ends_on, 'medium' if (r['quotes'] or 0) >= 4 * QUESTION_MIN_QUOTES else 'low', ev, sentence, None, 0.8, [r['id']],
                     money_reason='a doubt with no proof is priced on its theme card, not twice')
        f['entity'] = {'type': 'ladder_rung', 'id': r['theme'] or r['id'], 'label': r['theme_label'] or 'question', 'doubt': r['doubt'], 'question': r['question'], 'quotes': r['quotes'],
                       'who': r['who'], 'why': r['why'], 'verdict': r['verdict'], 'record': r['id']}
        f['id'] = r['finding_id']
        out.append(f)
    return out


# ---------------------------------------------------------------- the pulls and their freshness (round 4.5)

PULL_WINDOW_DAYS = {'reddit': 30, 'amazon_reviews': 60, 'ad_library': 30, 'ad_library_active': 7, 'amazon_listings': 30, 'instagram': 30, 'web_pass': 30, 'listing_seller': 30}
PULL_SECTIONS = ('language_bank', 'objections', 'objection_ladders', 'avatars', 'competitors', 'positioning', 'seo_facts', 'content', 'learnings',
                 'offers', 'story_bank', 'marketplaces', 'products')


def _apify():
    """The Apify connector module, read only: prices and the estimate. Never a client, never a run."""
    if 'apify' not in _MODS:
        import sys
        if str(APP.parent) not in sys.path:
            sys.path.insert(0, str(APP.parent))
        from app.connectors import apify as mod
        _MODS['apify'] = mod
    return _MODS['apify']


def _estimate(actor, items):
    if not actor or not items:
        return None
    try:
        return _apify().estimate_usd(actor, int(items))
    except Exception:  # noqa: BLE001  no price on file
        return None


def brain_pulls(br):
    """Per connector actor: how many brain records cite it and the newest capture date, from the records' source refs."""
    out = {}
    if br is None:
        return out
    for sec in PULL_SECTIONS:
        for r in br.records(sec):
            src = r.get('source') or {}
            ref = str(src.get('ref') or '')
            if not ref.startswith('apify:'):
                continue
            actor = ref.split(':')[1]
            g = out.setdefault(actor, {'records': 0, 'newest': None, 'sections': set()})
            g['records'] += 1
            g['sections'].add(sec)
            cap = str(src.get('captured_at') or '')[:10]
            if cap and (g['newest'] is None or cap > g['newest']):
                g['newest'] = cap
    for g in out.values():
        g['sections'] = sorted(g['sections'])
    return out


def pulls(br, brand, ends_on):
    """Every pull this desk reads, with its last capture, age, refresh window, next due date, the estimate for the configured
    size under the brand's caps, and the verdict: fresh, due, mock (a fixture stands in), never (no run on file), unset (no actor
    named). Nothing here runs anything; a person approves each paid call from the card."""
    if br is None:
        return {'rows': [], 'caps': None, 'rule': None}
    cfg_path = APP / 'brain' / br.brand / 'config' / 'apify.json'
    cfg = json.loads(cfg_path.read_text(encoding='utf-8')) if cfg_path.is_file() else {}
    caps = cfg.get('budget') or {}
    had = brain_pulls(br)
    open_cands = [c for c in pipeline(brand) if c.get('stage') not in CLOSED_STAGES]
    rd, am, ad = cfg.get('reddit') or {}, cfg.get('amazon_reviews') or {}, cfg.get('meta_ad_library') or {}
    fx = web_pass(br) or {}
    sp = social_pull_for(br) or {}
    rows = []

    def add(key, label, actor, items, window, fills, feeds, captured, mode=None, command=None, note=None):
        est = _estimate(actor, items)
        cap_run = caps.get('max_usd_per_run')
        cap_week = caps.get('max_usd_per_week')
        age = max((ends_on - date.fromisoformat(captured)).days, 0) if captured else None
        if actor is None and key != 'web_pass':
            verdict = 'unset'
        elif mode == 'mock':
            verdict = 'mock'
        elif captured is None:
            verdict = 'never'
        elif age >= window:
            verdict = 'due'
        else:
            verdict = 'fresh'
        rows.append({'key': key, 'label': label, 'actor': actor, 'items': items, 'window_days': window, 'fills': fills, 'feeds': feeds, 'captured_at': captured,
                     'age_days': age, 'next_due': (date.fromisoformat(captured) + timedelta(days=window)).isoformat() if captured else None,
                     'estimate_usd': est, 'over_run_cap': (est is not None and cap_run is not None and est > cap_run), 'mode': mode, 'command': command,
                     'note': note, 'verdict': verdict, 'finding_id': f'{SCREEN}.PROD-R36.{key}'})

    r = had.get(rd.get('actor') or '', {})
    add('reddit', 'Reddit threads and comments', rd.get('actor'), rd.get('max_items'), PULL_WINDOW_DAYS['reddit'], rd.get('fills_sections') or [],
        ['conversation', 'surfaces', 'positioning', 'video'], r.get('newest'), command=f'python3 app/brain/extract/apify_reddit.py --brand {br.brand}' if rd.get('actor') else None,
        note=f'{r.get("records", 0)} records cite it' if r else 'no record cites it')
    r = had.get(am.get('actor') or '', {})
    add('amazon_reviews', 'Amazon reviews on our listings', am.get('actor'), len(am.get('asins') or []) * 2 * int(am.get('max_reviews_per_asin_per_star') or 100), PULL_WINDOW_DAYS['amazon_reviews'],
        am.get('fills_sections') or [], ['conversation', 'complaints', 'price signal', 'reviews'], r.get('newest'), command=f'python3 app/brain/extract/apify_amazon.py --brand {br.brand}' if am.get('actor') else None,
        note=f'{r.get("records", 0)} records cite it; {len(am.get("asins") or [])} ASINs, 1 and 5 star first' if r else 'no record cites it')
    r = had.get(ad.get('actor') or '', {})
    add('ad_library', 'Meta Ad Library, by page id', ad.get('actor'), len(ad.get('pages') or []) * int(ad.get('limit_per_source') or 150),
        PULL_WINDOW_DAYS['ad_library_active'] if open_cands else PULL_WINDOW_DAYS['ad_library'], ad.get('fills_sections') or [],
        ['lanes', 'spend', 'positioning map', 'video'], r.get('newest'), command=f'python3 app/brain/extract/apify_adlibrary.py --brand {br.brand}' if ad.get('actor') else None,
        note=(f'{r.get("records", 0)} records cite it; {len(ad.get("pages") or [])} pages' if r else 'no record cites it') + (f'; {len(open_cands)} open candidates set the 7-day window' if open_cands else ''))
    listing_actor = 'junglee~amazon-crawler'
    r = had.get(listing_actor, {})
    add('amazon_listings', 'Amazon listings (title, price, stars, ratings)', listing_actor, len(am.get('asins') or []) or None, PULL_WINDOW_DAYS['amazon_listings'], ['marketplaces'],
        ['marketplace', 'complaints'], r.get('newest'), note=f'{r.get("records", 0)} records cite it; the search pull, expensive per result' if r else 'no record cites it')
    lp = listing_pull_for(br) or {}
    add('listing_seller', 'Amazon seller of record per listing', lp.get('actor') or am.get('listing_actor') or 'junglee~amazon-crawler', len(am.get('asins') or []) or None, PULL_WINDOW_DAYS['listing_seller'],
        ['fixtures.amazon_listings'], ['marketplace'], str(lp.get('captured_at') or '')[:10] or None, mode=lp.get('mode'),
        command=f'python3 app/screens/01-market-research/listing_pull.py --brand {br.brand} --mode live',
        note='a mock pull is on file; its sellers are never read as fact, the seller column waits for a live run' if lp.get('mode') == 'mock' else ('the seller column reads not read until it runs' if not lp else None))
    add('instagram', 'Instagram posts by hashtag', 'apify~instagram-hashtag-scraper', (sp.get('per_tag') or 25) * len(sp.get('hashtags') or ['x'] * 5), PULL_WINDOW_DAYS['instagram'], ['fixtures.social_pull'],
        ['conversation', 'surfaces', 'video'], str(sp.get('captured_at') or '')[:10] or None, mode=sp.get('mode'),
        command=f'python3 app/screens/01-market-research/social_pull.py --brand {br.brand} --mode live --per-tag {sp.get("per_tag") or 25}',
        note='the mock file stands in; the live pull was refused by the build session\'s permission check' if sp.get('mode') == 'mock' else None)
    add('web_pass', 'Public web pass (markets, preferences, launches, lanes)', None, None, PULL_WINDOW_DAYS['web_pass'], ['fixtures.market_trends'],
        ['trends', 'lanes', 'lane map', 'cadence', 'trend checks', 'preferences'], str(fx.get('captured_at') or '')[:10] or None,
        command=f'python3 app/screens/01-market-research/web_pass.py --brand {br.brand} --check', note='a session task with a url and a date per number; no actor')
    order = {'due': 0, 'never': 1, 'mock': 2, 'unset': 3, 'fresh': 4}
    rows.sort(key=lambda r: (order[r['verdict']], r['label']))
    return {'rows': rows, 'caps': {'per_run_usd': caps.get('max_usd_per_run'), 'per_week_usd': caps.get('max_usd_per_week')}, 'ledger': ledger_week(br.brand),
            'rule': 'a pull is due when its last capture is older than its window (Reddit 30 days, reviews 60, Ad Library 30 or 7 while a candidate is open, listings 30, Instagram 30, the web pass 30); a mock or a never-run pull that a block reads is a gap; every run is a paid call a person approves under the per-run and weekly caps'}


def pull_findings(br, brand, ends_on):
    """PROD-R36: a pull the desk reads that is due, never run, mock, or has no actor set."""
    out = []
    if br is None:
        return out
    p = pulls(br, brand, ends_on)
    for r in p['rows']:
        if r['verdict'] == 'fresh':
            continue
        ev = [_ev('pull_age_days', r['age_days'], 'days', ends_on.isoformat(), 'brain and fixtures now', r['window_days'], 'threshold', source=r['actor'] or 'fixture', simulated=False, freshness_days=0,
                  captured_at=r['captured_at'], verdict=r['verdict'], mode=r['mode']),
              _ev('estimate_usd', r['estimate_usd'], 'usd', ends_on.isoformat(), 'configured size', (p['caps'] or {}).get('per_run_usd'), 'threshold', source='app.connectors.apify', simulated=False, freshness_days=0,
                  items=r['items'])]
        what = {'due': f'last captured {r["captured_at"]}, {r["age_days"]} days ago against a {r["window_days"]}-day window',
                'never': 'never run', 'mock': 'filled by a mock file, not a live run', 'unset': 'no actor set'}[r['verdict']]
        est = f' A run at the configured size is about ${r["estimate_usd"]:,.2f}' + (' (over the per-run cap)' if r['over_run_cap'] else '') + '.' if r['estimate_usd'] is not None else ''
        sentence = f'{r["label"]}: {what}. It feeds {", ".join(r["feeds"])}.{est}'
        sev = 'medium' if r['verdict'] in ('due', 'mock') else 'low'
        f = _finding('PROD-R36', r['key'], ends_on, sev, ev, sentence, None, 0.9, [], money_reason='a stale read has no order count; the blocks it feeds carry the stake')
        f['entity'] = {'type': 'metric', 'id': r['key'], 'label': r['label'], 'actor': r['actor'], 'verdict': r['verdict'], 'command': r['command'], 'estimate_usd': r['estimate_usd'],
                       'per_run_cap': (p['caps'] or {}).get('per_run_usd'), 'per_week_cap': (p['caps'] or {}).get('per_week_usd'), 'feeds': r['feeds'], 'note': r['note']}
        f['id'] = r['finding_id']
        out.append(f)
    return out


# ---------------------------------------------------------------- the first run and its MOQ (round 4.9, bank idea BRD-249)

FIRST_RUN_STAGE_MIN = 2          # gated or later: the first production run is being sized
FIRST_RUN_CASH_SHARE = 0.25      # first run cash at 25 percent of 28-day net revenue or more is a risk without a lower-MOQ option


def first_run_read(brand, ends_on, net_28d):
    """Per candidate at gated or later: the first production run on file (units, the format's MOQ, the format, cash out, the
    lower-MOQ alternative considered), the cash as a share of 28-day net revenue, and the verdict: no plan, full-MOQ risk
    (cash at the share floor or more, or MOQ above the units wanted, with no lower-MOQ option noted), sized, or not yet
    (before gated). Bank idea BRD-249: a lower-MOQ format on the first run lets demand prove itself before capital goes in."""
    rows = []
    for c in pipeline(brand):
        st = c.get('stage')
        idx = STAGES.index(st) if st in STAGES else None
        fr = c.get('first_run') or {}
        cash = fr.get('cash_usd')
        share = round(cash / net_28d, 4) if cash is not None and net_28d else None
        moq_over = (fr.get('moq_units') or 0) > (fr.get('units') or 0) if fr.get('moq_units') is not None and fr.get('units') is not None else None
        option = bool(str(fr.get('lower_moq_option') or '').strip())
        if st in CLOSED_STAGES:
            verdict = 'closed'
        elif idx is None or idx < FIRST_RUN_STAGE_MIN:
            verdict = 'not_yet'
        elif not fr:
            verdict = 'no_plan'
        elif not option and ((share is not None and share >= FIRST_RUN_CASH_SHARE) or share is None or moq_over):
            verdict = 'full_moq_risk'
        else:
            verdict = 'sized'
        rows.append({'candidate_id': c.get('candidate_id'), 'name': c.get('name'), 'stage': st, 'closed': st in CLOSED_STAGES, 'units': fr.get('units'), 'moq_units': fr.get('moq_units'),
                     'format': fr.get('format'), 'cash_usd': cash, 'cash_share_28d': share, 'moq_over_units': moq_over, 'lower_moq_option': fr.get('lower_moq_option') or None,
                     'decided_on': fr.get('decided_on'), 'verdict': verdict, 'finding_id': f'{SCREEN}.PROD-R37.{c.get("candidate_id")}'})
    order = {'full_moq_risk': 0, 'no_plan': 1, 'sized': 2, 'not_yet': 3, 'closed': 4}
    rows.sort(key=lambda r: (order[r['verdict']], r['name'] or ''))
    return {'rows': rows, 'net_28d': net_28d, 'share_floor': FIRST_RUN_CASH_SHARE,
            'rule': f'from {STAGES[FIRST_RUN_STAGE_MIN]} on, a candidate needs a first run on file; the run is a risk when its cash is {int(FIRST_RUN_CASH_SHARE * 100)} percent or more of 28-day net revenue (or revenue is unknown), or the format\'s MOQ is above the units wanted, and no lower-MOQ alternative is noted (bank idea BRD-249)'}


def first_run_findings(brand, ends_on, net_28d):
    """PROD-R37: a candidate at gated or later with no first run on file, or a first run at full MOQ with no lower-MOQ alternative noted."""
    out = []
    fr = first_run_read(brand, ends_on, net_28d)
    for r in fr['rows']:
        if r['verdict'] not in ('no_plan', 'full_moq_risk'):
            continue
        cid = r['candidate_id']
        ev = [_ev('first_run_cash_share_28d', r['cash_share_28d'], 'ratio', ends_on.isoformat(), 'first run plan', FIRST_RUN_CASH_SHARE, 'threshold', source='fixtures.pipeline', simulated=False, freshness_days=0,
                  cash_usd=r['cash_usd'], net_28d=net_28d, units=r['units'], moq_units=r['moq_units'], format=r['format']),
              _ev('lower_moq_option_noted', 1 if r['lower_moq_option'] else 0, 'count', ends_on.isoformat(), 'first run plan', 1, 'threshold', source='fixtures.pipeline', simulated=False, freshness_days=0)]
        if r['verdict'] == 'no_plan':
            sentence = f'{r["name"]} is at {r["stage"]} with no first run on file: units, the format and its MOQ, and the cash it ties up are not written down yet.'
            stake = None
        else:
            why = (f'{round(r["cash_share_28d"] * 100)} percent of 28-day net revenue' if r['cash_share_28d'] is not None else 'an unknown share of revenue')
            if r['moq_over_units']:
                why += f' and an MOQ of {r["moq_units"]:,} above the {r["units"]:,} units wanted'
            sentence = f'{r["name"]}: the first run ({r["format"] or "format unstated"}) ties up ${(r["cash_usd"] or 0):,.0f}, {why}, with no lower-MOQ alternative noted.'
            stake = {'usd': round(r['cash_usd']), 'formula': 'first_run_cash_usd', 'inputs': {'cash_usd': r['cash_usd'], 'net_28d': net_28d}, 'window': 'first run plan'} if r['cash_usd'] else None
        f = _finding('PROD-R37', cid, ends_on, 'medium', ev, sentence, stake, 0.7, [], money_reason=None if stake else 'no first run cash on file')
        f['entity'] = {'type': 'sku', 'id': cid, 'label': r['name'], 'candidate': cid, 'stage': r['stage'], 'verdict': r['verdict'], 'cash_usd': r['cash_usd'], 'units': r['units'], 'moq_units': r['moq_units'], 'format': r['format']}
        f['id'] = f'{SCREEN}.PROD-R37.{cid}'
        out.append(f)
    return out


# ---------------------------------------------------------------- the spend ledger, read only (round 5.6)

LEDGER_PATH = APP.parent / 'data' / 'spend.sqlite'


def ledger_week(brand, today=None, path=None):
    """This ISO week's Apify spend for the brand from the shared spend ledger, read only: settled runs count at their actual
    cost, open reservations at their bound; runs that settled over their bound are counted. Unavailable when the ledger is
    absent. Nothing here writes, reserves or clears anything."""
    import sqlite3
    today = today or date.today()
    p = Path(path or LEDGER_PATH)
    week = f'{today.isocalendar()[0]}-W{today.isocalendar()[1]:02d}'
    if not p.is_file() or not brand:
        return {'available': False, 'week': week, 'reason': 'no spend ledger on file' if not p.is_file() else 'no brand'}
    try:
        con = sqlite3.connect(f'file:{p}?mode=ro', uri=True)
        try:
            rows = con.execute("SELECT request_id, reserved, actual, status FROM spend WHERE request_id LIKE ?", (f'apify:{brand}:%',)).fetchall()
        finally:
            con.close()
    except sqlite3.Error as exc:
        return {'available': False, 'week': week, 'reason': f'ledger unreadable ({exc})'}
    def usd(v):
        return (v or 0) / 1_000_000
    wk = [r for r in rows if r[0].split(':')[2] == week]
    return {'available': True, 'week': week, 'runs_week': len(wk),
            'spent_week_usd': round(sum(usd(r[2] if r[2] is not None else r[1]) for r in wk), 2),
            'reserved_open_usd': round(sum(usd(r[1]) for r in wk if r[2] is None), 2),
            'over_bound_week': sum(1 for r in wk if r[3] == 'bound_exceeded'),
            'spent_all_usd': round(sum(usd(r[2] if r[2] is not None else r[1]) for r in rows), 2), 'runs_all': len(rows),
            'by_actor_week': sorted(((a, round(sum(usd(r[2] if r[2] is not None else r[1]) for r in wk if r[0].split(':')[3] == a), 2)) for a in {r[0].split(':')[3] for r in wk}), key=lambda kv: -kv[1])}


# ---------------------------------------------------------------- overrides and the evergreen companion (round 5.8, bank ideas PRD-113 and PRD-047)

OVERRIDE_WORDS = ('override', 'because', 'reason', 'despite', 'accepted the fail', 'accept the fail')
OVERRIDE_STAGE_MIN = 1        # researched or later: a failed fast check has been carried past screening


def override_read(brand, ends_on):
    """Per open candidate carried past screening with a failed fast check, or past gated with a failed compliance line: whether
    the log names the reason (bank idea PRD-113: every rule override is written down with the exact signal that justified it)."""
    rows = []
    for c in pipeline(brand):
        st = c.get('stage')
        idx = STAGES.index(st) if st in STAGES else None
        if st in CLOSED_STAGES or idx is None:
            continue
        checks = c.get('screen_result') or {}
        failed_checks = [k for k in SCREEN_CHECKS if checks.get(k) == 'fail'] if idx >= OVERRIDE_STAGE_MIN else []
        comp = c.get('compliance') or {}
        failed_comp = [k for k, v in comp.items() if v == 'fail'] if idx >= SPEC_STAGE_MIN else []
        failed = failed_checks + [f'compliance {k}' for k in failed_comp]
        if not failed:
            continue
        notes = [l for l in c.get('log') or [] if any(w in str(l.get('what') or '').lower() for w in OVERRIDE_WORDS)]
        rows.append({'candidate_id': c.get('candidate_id'), 'name': c.get('name'), 'stage': st, 'failed': failed, 'override_note': notes[-1].get('what') if notes else None,
                     'override_on': notes[-1].get('on') if notes else None, 'verdict': 'logged' if notes else 'unlogged', 'finding_id': f'{SCREEN}.PROD-R38.{c.get("candidate_id")}'})
    return rows


def override_findings(brand, ends_on):
    """PROD-R38: a candidate carried past a failed check or gate with no override reason in its log."""
    out = []
    for r in override_read(brand, ends_on):
        if r['verdict'] != 'unlogged':
            continue
        cid = r['candidate_id']
        ev = [_ev('failed_checks_carried', len(r['failed']), 'count', ends_on.isoformat(), 'candidate now', 0, 'threshold', source='fixtures.pipeline', simulated=False, freshness_days=0, failed=r['failed'], stage=r['stage']),
              _ev('override_notes', 0, 'count', ends_on.isoformat(), 'candidate log', 1, 'threshold', source='fixtures.pipeline', simulated=False, freshness_days=0)]
        sentence = f'{r["name"]} is at {r["stage"]} with {", ".join(r["failed"])} failed and no line in its log says why the rule was overridden.'
        f = _finding('PROD-R38', cid, ends_on, 'medium', ev, sentence, None, 0.9, [], money_reason='an unlogged override has no order count; it is a discipline gap')
        f['entity'] = {'type': 'sku', 'id': cid, 'label': r['name'], 'candidate': True, 'stage': r['stage'], 'failed': r['failed']}
        f['id'] = r['finding_id']
        out.append(f)
    return out


def companion_read(brand, data, rd, ends_on):
    """Per open candidate at gated or later tagged trending: whether an evergreen companion exists (a category of the store
    tagged evergreen, or another open candidate tagged evergreen), bank idea PRD-047: never bet inventory on a trend alone."""
    mix = category_mix(data, brand, rd)
    fx = web_pass(brand)
    cands = [c for c in pipeline(brand) if c.get('stage') not in CLOSED_STAGES]
    tags = {c.get('candidate_id'): demand_pattern(c.get('category'), mix, fx, c.get('name')) for c in cands}
    evergreen_cats = [] if mix.get('unavailable') else [r['category'] for r in mix['rows'] if demand_pattern(r['category'], mix, fx)['tag'] == 'evergreen']
    evergreen_cands = [c.get('name') for c in cands if tags[c.get('candidate_id')]['tag'] == 'evergreen']
    rows = []
    for c in cands:
        st = c.get('stage')
        idx = STAGES.index(st) if st in STAGES else None
        p = tags[c.get('candidate_id')]
        if p['tag'] != 'trending' or idx is None or idx < SPEC_STAGE_MIN:
            continue
        companions = [f'{x} (line)' for x in evergreen_cats] + [f'{x} (candidate)' for x in evergreen_cands if x != c.get('name')]
        rows.append({'candidate_id': c.get('candidate_id'), 'name': c.get('name'), 'stage': st, 'tag': p['tag'], 'why': p['why'], 'companions': companions,
                     'verdict': 'covered' if companions else 'alone', 'finding_id': f'{SCREEN}.PROD-R39.{c.get("candidate_id")}'})
    return rows


def companion_findings(brand, data, rd, ends_on):
    """PROD-R39: a trending candidate at gated or later with no evergreen line or candidate beside it."""
    out = []
    for r in companion_read(brand, data, rd, ends_on):
        if r['verdict'] != 'alone':
            continue
        cid = r['candidate_id']
        ev = [_ev('demand_pattern_tag', 1, 'flag', ends_on.isoformat(), '12 months', source='products_monthly', tag=r['tag'], why=r['why']),
              _ev('evergreen_companions', 0, 'count', ends_on.isoformat(), 'store and pipeline now', 1, 'threshold', source='fixtures.pipeline', simulated=False, freshness_days=0)]
        sentence = f'{r["name"]} is tagged trending ({r["why"]}) and no evergreen line or candidate stands beside it; an MOQ on a trend alone is the whole bet.'
        f = _finding('PROD-R39', cid, ends_on, 'medium', ev, sentence, None, 0.6, [], money_reason='the bet is the first run cash, priced on the first-run card')
        f['entity'] = {'type': 'sku', 'id': cid, 'label': r['name'], 'candidate': True, 'stage': r['stage']}
        f['id'] = r['finding_id']
        out.append(f)
    return out


# ---------------------------------------------------------------- lead time and the order-by date (round 6.1)

ORDER_SAFETY_DAYS = 14        # stock lands this long before the peak month opens
ORDER_WARN_DAYS = 30          # the order-by date inside this window with no first run decided is a finding


def lead_time_for(cand, br):
    """The candidate's lead time in days: its own field first, else the brand's default from a learnings record
    (learnings.lead_time_days) or an operations record whose value carries lead_time_days; None when nothing is on file."""
    if cand.get('lead_time_days'):
        return int(cand['lead_time_days']), 'candidate'
    if br is not None:
        rec = br.get(f'{br.brand}.learnings.lead_time_days')
        if rec and isinstance(rec.get('value'), (int, float)):
            return int(rec['value']), rec['id']
        for r in br.records('operations'):
            v = r.get('value')
            if isinstance(v, dict) and isinstance(v.get('lead_time_days'), (int, float)):
                return int(v['lead_time_days']), r['id']
    return None, None


def order_by_date(peak_months, ends_on, lead_days):
    """The date a purchase order must go in so stock lands ORDER_SAFETY_DAYS before the next peak month opens."""
    if not peak_months or lead_days is None:
        return None, None
    m = int(peak_months[0])
    peak = date(ends_on.year, m, 1)
    if peak <= ends_on:
        peak = date(ends_on.year + 1, m, 1)
    return (peak - timedelta(days=int(lead_days) + ORDER_SAFETY_DAYS)).isoformat(), peak.isoformat()


def order_findings(brand, data, br, rd, ends_on):
    """PROD-R40: a seasonal candidate at gated or later whose order-by date (peak month less lead time and 14 days) is
    inside 30 days or past, with no first run decided; or one whose lead time is not on file at all."""
    mix = category_mix(data, brand, rd)
    fx = web_pass(brand)
    out = []
    for c in pipeline(brand):
        st = c.get('stage')
        idx = STAGES.index(st) if st in STAGES else None
        if st in CLOSED_STAGES or idx is None or idx < SPEC_STAGE_MIN:
            continue
        p = demand_pattern(c.get('category'), mix, fx, c.get('name'))
        if p['tag'] != 'seasonal':
            continue
        cid = c.get('candidate_id')
        lead, src = lead_time_for(c, br)
        order_by, peak = order_by_date(p.get('peak_months'), ends_on, lead)
        days = (date.fromisoformat(order_by) - ends_on).days if order_by else None
        sized = bool(c.get('first_run'))
        if lead is None:
            what, sev = 'no lead time is on file, so the order-by date cannot be set', 'medium'
        elif days is not None and days <= ORDER_WARN_DAYS and not sized:
            what, sev = (f'the order must go in by {order_by} ({days} days) for stock to land {ORDER_SAFETY_DAYS} days before the {peak[:7]} peak, and no first run is decided' if days >= 0
                         else f'the order-by date {order_by} passed {-days} days ago and no first run is decided'), 'high'
        else:
            continue
        ev = [_ev('days_to_order_by', days, 'days', ends_on.isoformat(), 'first run plan', ORDER_WARN_DAYS, 'threshold', source='fixtures.pipeline', simulated=False, freshness_days=0, order_by=order_by, peak=peak, lead_time_days=lead, lead_time_source=src),
              _ev('first_run_decided', 1 if sized else 0, 'flag', ends_on.isoformat(), 'candidate now', 1, 'threshold', source='fixtures.pipeline', simulated=False, freshness_days=0)]
        sentence = f'{c.get("name")} is seasonal ({p["why"]}) and {what}.'
        f = _finding('PROD-R40', cid, ends_on, sev, ev, sentence, None, 0.8, [], money_reason='a missed peak is priced on the first-run card once the run is sized')
        f['entity'] = {'type': 'sku', 'id': cid, 'label': c.get('name'), 'candidate': True, 'stage': st, 'order_by': order_by, 'peak': peak, 'lead_time_days': lead, 'days': days}
        f['id'] = f'{SCREEN}.PROD-R40.{cid}'
        out.append(f)
    return out


# ---------------------------------------------------------------- the brain's freshness for the sections this desk reads (round 6.2)

# TTL per section from app/contracts/brand-brain.md (how long a record is trusted before the keeper re-checks it)
SECTION_TTL_DAYS = {'identity': 180, 'diagnosis': 90, 'story_bank': 90, 'voice': 60, 'visual': 90, 'products': 7, 'offers': 1, 'policies': 30, 'claims': 30, 'avatars': 30,
                    'objections': 30, 'objection_ladders': 30, 'language_bank': 30, 'competitors': 14, 'positioning': 60, 'channels': 30, 'calendar': 30, 'economics': 30,
                    'operations': 30, 'marketplaces': 14, 'stack': 14, 'site_map': 7, 'content': 30, 'seo_facts': 30, 'team': 90, 'learnings': 90, 'decisions': None,
                    'open_questions': None, 'changes': None, 'freshness': 1}


def sections_read():
    """The brain sections this desk's rules and blocks read, from the rules' inputs plus the presence and hand-off reads."""
    out = set(PRESENCE_SECTIONS) | {'avatars', 'language_bank', 'objection_ladders', 'claims', 'competitors', 'positioning', 'learnings', 'products', 'seo_facts', 'content', 'calendar', 'economics', 'open_questions', 'operations'}
    for r in RULES:
        for i in r.get('inputs') or []:
            if i.startswith('brain.'):
                sec = i.split('.')[1]
                if sec and sec != '*':
                    out.add(sec)
    return sorted(sec for sec in out if sec in SECTION_TTL_DAYS and sec not in ('freshness', 'changes'))   # record sections only, never config or the review folder


def open_conflicts(br):
    """Open conflicts per section from the brain's review folder (needs_founder true, or not resolved)."""
    if br is None:
        return {}
    p = APP / 'brain' / br.brand / 'review' / 'conflicts.json'
    if not p.is_file():
        return {}
    try:
        rows = json.loads(p.read_text(encoding='utf-8'))
    except ValueError:
        return {}
    out = {}
    for c in rows if isinstance(rows, list) else []:
        if c.get('needs_founder') or not str(c.get('status') or '').startswith('resolved'):
            out.setdefault(c.get('section'), []).append({'id': c.get('id'), 'field': c.get('field'), 'status': c.get('status')})
    return out


def brain_freshness(br, ends_on):
    """Per section this desk reads: records, last update, age against the contract TTL, stale and conflict counts, confidence,
    the rules that read it, and the verdict: conflict (a founder decision waits), stale (past TTL or stale records), fresh,
    unknown (no freshness record)."""
    if br is None:
        return {'rows': [], 'rule': None}
    fresh = {r.get('field'): (r.get('value') or {}) for r in br.records('freshness')}
    conflicts = open_conflicts(br)
    readers = {}
    for r in RULES:
        for i in r.get('inputs') or []:
            if i.startswith('brain.'):
                readers.setdefault(i.split('.')[1], set()).add(r['rule_id'])
    rows = []
    for sec in sections_read():
        v = fresh.get(sec)
        ttl = SECTION_TTL_DAYS.get(sec)
        last = str((v or {}).get('last_updated') or '')[:10] or None
        age = max((ends_on - date.fromisoformat(last)).days, 0) if last else None
        stale = int((v or {}).get('stale_count') or 0)
        conf = int((v or {}).get('conflict_count') or 0) + len(conflicts.get(sec, []))
        if v is None and ttl is None:
            verdict = 'no_ttl'       # decisions and open questions never go stale by the contract
        elif v is None:
            verdict = 'unknown'
        elif conf:
            verdict = 'conflict'
        elif stale or (ttl is not None and age is not None and age > ttl):
            verdict = 'stale'
        else:
            verdict = 'fresh'
        rows.append({'section': sec, 'records': (v or {}).get('record_count'), 'last_updated': last, 'age_days': age, 'ttl_days': ttl, 'stale_count': stale, 'conflicts': conf,
                     'open_conflicts': conflicts.get(sec, []), 'confidence': (v or {}).get('confidence'), 'readers': sorted(readers.get(sec, [])), 'verdict': verdict,
                     'finding_id': f'{SCREEN}.PROD-R41.{sec}'})
    order = {'conflict': 0, 'stale': 1, 'unknown': 2, 'fresh': 3, 'no_ttl': 4}
    rows.sort(key=lambda r: (order[r['verdict']], -(r['age_days'] or 0), r['section']))
    return {'rows': rows, 'rule': 'a section is stale past its contract TTL (brand-brain.md) or with stale records, and in conflict when a founder decision waits on it; a section with no freshness record reads unknown, never fresh'}


def freshness_findings(br, ends_on):
    """PROD-R41: a brain section this desk reads that is stale past its TTL, holds stale records, or has an open conflict."""
    out = []
    if br is None:
        return out
    for r in brain_freshness(br, ends_on)['rows']:
        if r['verdict'] not in ('stale', 'conflict'):
            continue
        ev = [_ev('section_age_days', r['age_days'], 'days', ends_on.isoformat(), 'brain now', r['ttl_days'], 'threshold', source=f'{br.brand}.freshness.{r["section"]}', simulated=False, freshness_days=0,
                  stale_count=r['stale_count'], conflicts=r['conflicts'], confidence=r['confidence'])]
        why = (f'{r["conflicts"]} open conflict{"s" if r["conflicts"] != 1 else ""} wait on the founder' if r['verdict'] == 'conflict'
               else (f'{r["stale_count"]} stale records' if r['stale_count'] else f'last updated {r["last_updated"]}, {r["age_days"]} days ago against a {r["ttl_days"]}-day TTL'))
        sentence = f'The {r["section"].replace("_", " ")} section is read by {len(r["readers"])} rule{"s" if len(r["readers"]) != 1 else ""} here and {why}.'
        f = _finding('PROD-R41', r['section'], ends_on, 'medium' if r['verdict'] == 'conflict' else 'low', ev, sentence, None, 0.9, [f'{br.brand}.freshness.{r["section"]}'],
                     money_reason='a stale section has no order count; the rules that read it carry the stake')
        f['entity'] = {'type': 'brand', 'id': r['section'], 'label': r['section'].replace('_', ' '), 'verdict': r['verdict'], 'readers': r['readers'], 'ttl_days': r['ttl_days'], 'age_days': r['age_days'],
                       'open_conflicts': r['open_conflicts']}
        f['id'] = r['finding_id']
        out.append(f)
    return out


# ---------------------------------------------------------------- what the simulated numbers assume (round 6.3)

# the calibration assumptions this desk prices with, and the rules that read the number they shape
ASSUMPTION_USERS = {'revenue_band': ['PROD-R01', 'PROD-R02', 'PROD-R04', 'PROD-R11', 'PROD-R37'], 'seasonality': ['PROD-R18', 'PROD-R40'], 'repeat_rate_12m': ['PROD-R11'],
                    'aov_usd': ['PROD-R16', 'PROD-R24'], 'category_mix': ['PROD-R04', 'PROD-R05', 'PROD-R19'], 'gross_margin': ['PROD-R16', 'PROD-R37'], 'return_share': ['PROD-R34'],
                    'channel_mix': [], 'paid_channels_present': [], 'giving_units': [], 'retail_partners': [], 'paid_media_split': []}
CONFIRMED_STATUSES = ('founder',)


def assumptions(br):
    """The calibration assumptions behind the simulated tables (app/brain/<brand>/assumptions.json): value, unit, status
    (founder, sourced, derived, modelled), as-of, sources, and which rules here price with the number they shape."""
    if br is None:
        return {'rows': [], 'rule': None}
    rows = []
    for r in br.records('assumptions'):
        field = r.get('field')
        if not field:
            continue
        v = r.get('value')
        short = (f'{v:g}' if isinstance(v, (int, float)) else ', '.join(f'{k} {vv}' for k, vv in list(v.items())[:4] if not isinstance(vv, (list, dict))) if isinstance(v, dict)
                 else '; '.join(str(x)[:40] for x in v[:3]) if isinstance(v, list) else str(v))[:120]
        users = ASSUMPTION_USERS.get(field, [])
        status = str(r.get('status') or 'unverified')
        verdict = 'confirmed' if status in CONFIRMED_STATUSES else ('unconfirmed' if users else 'unused')
        rows.append({'field': field, 'label': field.replace('_', ' '), 'value': v, 'short': short, 'unit': r.get('unit'), 'status': status, 'as_of': r.get('as_of'),
                     'sources': list(r.get('source_refs') or [])[:3], 'source_ids': list(r.get('source_ids') or [])[:3], 'readers': users, 'verdict': verdict,
                     'finding_id': f'{SCREEN}.PROD-R42.{field}'})
    order = {'unconfirmed': 0, 'confirmed': 1, 'unused': 2}
    rows.sort(key=lambda r: (order[r['verdict']], -len(r['readers']), r['field']))
    return {'rows': rows, 'rule': 'an assumption a money rule prices with is confirmed only when its status is founder; sourced, derived and modelled numbers stay open until the founder confirms or corrects them'}


def assumption_findings(br, ends_on):
    """PROD-R42: an assumption a money rule here prices with whose status is not founder."""
    out = []
    if br is None:
        return out
    for r in assumptions(br)['rows']:
        if r['verdict'] != 'unconfirmed':
            continue
        ev = [_ev('assumption_status', 0, 'flag', ends_on.isoformat(), 'brain now', 1, 'threshold', source=f'{br.brand}.assumptions.{r["field"]}', simulated=False, freshness_days=0,
                  status=r['status'], as_of=r['as_of'], assumed=r['short'], readers=r['readers'])]
        sentence = f'The {r["label"]} assumption ({r["short"]}{", " + r["unit"] if r["unit"] else ""}) is {r["status"]}, not founder-confirmed, and {len(r["readers"])} rule{"s" if len(r["readers"]) != 1 else ""} here price with it.'
        f = _finding('PROD-R42', r['field'], ends_on, 'low', ev, sentence, None, 0.9, r['source_ids'], money_reason='the stake sits on the rules that read the assumption')
        f['entity'] = {'type': 'brand', 'id': r['field'], 'label': r['label'], 'status': r['status'], 'short': r['short'], 'unit': r['unit'], 'as_of': r['as_of'], 'readers': r['readers'], 'sources': r['sources']}
        f['id'] = r['finding_id']
        out.append(f)
    return out
