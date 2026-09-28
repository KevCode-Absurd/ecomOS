"""The offer strategist's judgement for screen 04, written as data. Brand-agnostic: every entry names the kind of
offer that answers a kind of doubt, the brain records that may already cover it, and how its cost is counted.
Brand facts (the doubt, the counts, the policy text, the prices) come from the brain and the tables at run time.

THEME_OFFERS keys are objection ladder themes (brain.objection_ladders value.theme). A theme that is missing
here falls back to DEFAULT_OFFER. `covers` lists brain record keys (section.field) whose text can be the answer
when they exist; `cost` names the claim a shopper makes when the promise is used:
  replacement  a new item goes out, nothing comes back: landed cost per item + outbound label + pick and pack + box
  exchange     the item comes back and another goes out: returns processing + outbound label + pick and pack + box
  none         the move is proof on a page or a listing; it costs nothing per order
`rate_key` is the brain record whose value holds the planned claim rate (percent of orders), if one exists.
"""

THEME_OFFERS = {
    'durability': {
        'name': 'Wear promise: a free replacement if a hole shows',
        'gets': 'A named promise: if a hole or seam gives out, we send a new one. No return needed.',
        'kind': 'offer', 'cost': 'replacement', 'covers': ['policies.exchanges', 'policies.happiness_guarantee'],
        'rate_key': ('economics.return_share_model', 'replacement_under_guarantee_pct'),
        'where': 'product page under the price, the cart, the ads that meet this doubt',
    },
    'fit_and_sizing': {
        'name': 'Fit swap: the first size exchange is free',
        'gets': 'Order your size. If it does not fit, the first exchange is free both ways.',
        'kind': 'offer', 'cost': 'exchange', 'covers': ['policies.exchanges', 'policies.returns_window_days'],
        'rate_key': None,
        'where': 'size selector, product page, the cart',
    },
    'order_and_delivery': {
        'name': 'Make-it-right promise: a named reply time and a fix',
        'gets': 'If an order comes short, wrong or late, a person replies within a set time and we fix it.',
        'kind': 'offer', 'cost': 'replacement', 'covers': ['policies.happiness_guarantee', 'policies.shipping_options'],
        'rate_key': None,
        'where': 'order confirmation email, the help page, the cart',
    },
    'comfort_and_feel': {
        'name': 'Wear test: wear them, and return them if they do not do the job',
        'gets': 'Wear a pair. If it does not do what the page says, send it back for a refund.',
        'kind': 'offer', 'cost': 'exchange', 'covers': ['policies.happiness_guarantee', 'policies.returns_window_days'],
        'rate_key': None,
        'where': 'product pages for performance and support lines',
    },
    'marketplace_trust': {
        'name': 'Real-product proof on every marketplace listing',
        'gets': 'Sold by the brand, the pack count in the title, and the same guarantee as the site.',
        'kind': 'listing_fix', 'cost': 'none', 'covers': ['policies.happiness_guarantee'],
        'rate_key': None,
        'where': 'marketplace title, first image and first bullet',
    },
    'price_and_value': {
        'name': 'Cost per wear proof next to the pack price',
        'gets': 'The pack price shown as price per pair and per wear, beside what the shopper gets back.',
        'kind': 'page_section', 'cost': 'none', 'covers': ['offers.bundles_pack_ladder', 'policies.happiness_guarantee'],
        'rate_key': None,
        'where': 'product page price block',
    },
    'mission_trust': {
        'name': 'Giving receipt proof',
        'gets': 'A count of what was given, with the partner, on the page where the promise is made.',
        'kind': 'page_section', 'cost': 'none', 'covers': [],
        'rate_key': None,
        'where': 'product page and the order confirmation',
    },
}

DEFAULT_OFFER = {
    'name': 'Risk-removal offer for this doubt',
    'gets': 'A plain promise that takes the risk of this doubt off the shopper.',
    'kind': 'offer', 'cost': 'replacement', 'covers': ['policies.happiness_guarantee'], 'rate_key': None,
    'where': 'product page and the cart',
}


def offer_for(theme):
    return THEME_OFFERS.get(theme) or DEFAULT_OFFER


# Pack ladder judgement (screen 04, OFFER-R07 and OFFER-R09).
# Categories bought in multiples, where a line with no multi-pack is a gap. Category names come from the brand's
# products table; these are the generic apparel basics names the data layer uses.
REPEAT_CATEGORIES = ('socks', 'underwear', 'tshirts', 't-shirts', 'basics')
MIN_SAVING = 0.10         # a multi-pack that saves less than 10 percent per item gives little reason to trade up
TARGET_SAVING = 0.15      # the per-item saving a deeper pack price would test
SINGLE_SHARE_PUSH = 0.30  # singles above 30 percent of a line's packs: the ladder is not moving shoppers up
VIABLE_TRADE_UP = 0.25    # a price test is worth running when under 25 percent of single buyers must trade up to pay
NEW_PACK_SAVING = 0.10    # a new pack on a single-only basics line starts at 10 percent off per item
DEFAULT_NEW_PACK = 3


# First-order offer alternatives (screen 04, OFFER-R08). Each is a way to pay for a first order. `keeps_price`:
# the list price is never cut, so it does not train buyers to wait for a code. `answers`: the doubt it speaks to.
FIRST_ORDER_OPTIONS = [
    {'key': 'code', 'name': 'Percent-off code (today)', 'keeps_price': False, 'answers': 'price'},
    {'key': 'gwp', 'name': 'Free item with the first order', 'keeps_price': True, 'answers': 'value'},
    {'key': 'free_ship', 'name': 'Free shipping on the first order', 'keeps_price': True, 'answers': 'shipping cost'},
    {'key': 'dollar_off', 'name': 'Dollars off at the free shipping line', 'keeps_price': False, 'answers': 'price, and lifts the basket'},
    {'key': 'pack', 'name': 'First-order price on the best-selling pack', 'keeps_price': False, 'answers': 'value, and moves shoppers up the ladder'},
]
CODE_ADS_SHARE = 0.5      # a percent code in more than half the active ads is the default way in: check what it costs

# Margin red line (screen 04, OFFER-R10). A first order must at least pay its own paid media (contribution after
# media per first order >= this many dollars); every other order is held to finance_inputs target_contribution_margin.
RED_LINE_FIRST_ORDER = 0.0


# Promo calendar (screen 04, OFFER-R11). US retail windows by date rule; a brand in another market swaps this list.
# rule: ('fixed', month, day, days) | ('nth_weekday', month, weekday 0=Mon, n, days) where n=-1 is the last one |
#       ('bfcm',) Friday after the 4th Thursday of November through Cyber Monday.
# lead: days before the start the offer must be approved. offer: the strategist's default for the window.
PROMO_WINDOWS = [
    {'key': 'valentines', 'name': "Valentine's Day", 'rule': ('fixed', 2, 7, 8), 'lead': 21,
     'offer': 'A gift pack with a gift note, no sitewide percent.', 'gifting': True},
    {'key': 'mothers_day', 'name': "Mother's Day", 'rule': ('nth_weekday', 5, 6, 2, -10), 'lead': 30,
     'offer': 'A gift pack and a gift card push, last ship date on the page.', 'gifting': True},
    {'key': 'memorial_day', 'name': 'Memorial Day', 'rule': ('nth_weekday', 5, 0, -1, -3), 'lead': 21,
     'offer': 'A pack offer on the summer lines, not a sitewide code.', 'gifting': False},
    {'key': 'fathers_day', 'name': "Father's Day", 'rule': ('nth_weekday', 6, 6, 3, -10), 'lead': 30,
     'offer': 'A gift pack and a gift card push, last ship date on the page.', 'gifting': True},
    {'key': 'back_to_school', 'name': 'Back to school', 'rule': ('fixed', 8, 1, 31), 'lead': 30,
     'offer': 'A kids and multi-pack offer at the free shipping line.', 'gifting': False},
    {'key': 'labor_day', 'name': 'Labor Day', 'rule': ('nth_weekday', 9, 0, 1, -3), 'lead': 21,
     'offer': 'A pack offer, not a sitewide code.', 'gifting': False},
    {'key': 'bfcm', 'name': 'Black Friday to Cyber Monday', 'rule': ('bfcm',), 'lead': 45,
     'offer': 'A tiered offer that lifts the basket (a free item or a better pack price at set order values), '
              'capped at last year\'s depth.', 'gifting': False},
    {'key': 'holiday_gifting', 'name': 'Holiday gifting', 'rule': ('fixed', 12, 2, 19), 'lead': 45,
     'offer': 'Gift boxes, gift cards and bulk gifting, with the last ship date on every page.', 'gifting': True},
]
PROMO_ALERT_DAYS = 30     # a window is due when its approval date is within 30 days, or past

# Gifting (screen 04, OFFER-R12 and the holiday window). A line is gift-led when its November and December share of
# its 12-month revenue is at least GIFT_LED_RATIO times the store's own November and December share.
GIFT_LED_RATIO = 1.3
GIFT_DAY = (12, 24)       # the day a gift must arrive by
GIFT_PACK_MIN = 6         # packs this size or bigger are the gift box candidates on the holiday page

# Guarantee as an offer (screen 04, OFFER-R14 and OFFER-R15). The brain records that make up the guarantee, and the
# page types where a doubt is met. A url path is classified by the first rule that matches.
GUARANTEE_KEYS = ['offers.guarantee', 'policies.happiness_guarantee', 'claims.guarantee_promise', 'policies.exchanges',
                  'policies.returns_window_days']
PAGE_TYPES = [('/products/', 'product page'), ('/collections/', 'collection page'), ('/cart', 'cart'),
              ('/policies/', 'policy page'), ('/pages/', 'content page')]
SELLING_PAGES = ('product page', 'collection page', 'cart', 'home page')
CLAIM_OVER_PLAN = 1.5     # claims above 1.5 times the planned rate: the guarantee costs more than it was priced at

# Competitor price and offer position (screen 04, OFFER-R16). Signals only: competitor ads are never copied.
PROOF_HOOK_WORDS = ('guarantee', 'lab tested', 'made in usa', 'review')   # hook types that sell proof, not price
MIN_PROOF_LED = 2         # at least 2 competitors priced above us run no discount in ads: the set is proof-led

# Marketplace price parity (screen 04, OFFER-R17). A listing whose price per item is more than PARITY_GAP under the
# site's paid price per item at the same pack size undercuts the site. Pack counts are read from listing titles.
PARITY_GAP = 0.10
PACK_PATTERNS = (r'(\d+)\s*-?\s*(?:pack|pairs?|pcs|pk)\b', r'\((\d+)\s*(?:pack|pairs?)\)')

# Discount discipline (screen 04, OFFER-R18 and OFFER-R19).
CREEP_POINTS = 5          # room spec: discount share of gross up more than 5 points over 3 months is creep
PROMO_DAY_RATIO = 1.5     # a day whose discount share is 1.5 times the year's median is a promo day
ALWAYS_ON = 0.75          # more than 75 percent of discount dollars spent on ordinary days: the discount is always on

# Gift with purchase pick (screen 04, feature 2.4): a single item whose paid price is at least GWP_RATIO times its
# landed cost reads as worth a lot and costs little to give.
GWP_RATIO = 4.0

# Promo depth by line (screen 04, feature 2.7). Tiers a line can take in a promo window, deepest first.
DEPTH_TIERS = (0.30, 0.25, 0.20, 0.15, 0.10)

# Second-order offer (screen 04, OFFER-R21). Words in an offers record that mean an offer for past buyers already exists.
RETURNING_OFFER_WORDS = ('second_order', 'returning', 'loyalty', 'replenish', 'refill', 'subscribe')
CURVE_MONTHS = 6          # read the cohort curve over months 1 to 6 after the first order

# Cost against price (screen 04, OFFER-R22). Landed cost up more than COST_MOVE in a year while the paid price per
# item moved less than the cost did: margin dollars are leaking. The test restores them, rounded up to PRICE_STEP.
COST_MOVE = 0.03
PRICE_STEP = 1.0

# Experiment registry (screen 04, round 3). Registry entries are mapped to this screen's surfaces by words in their
# audience tags, hypothesis and variants: every word in a rule must appear. First match wins.
REGISTRY_SURFACES = [
    (('first_order',), 'first order offer'),
    (('guarantee', 'pdp'), 'product page guarantee block'),
    (('fit finder',), 'product page promise: fit and sizing'),
    (('amazon',), 'marketplace listing'),
    (('meta_prospecting',), 'ad angle'),
    (('threshold',), 'cart rewards'),
    (('price rise',), 'list price'),
    (('price point',), 'list price'),
]
PRICE_TEST_WORDS = ('price rise', 'price point', 'new price', 'price test', 'price cut')   # plus a dollar amount in a variant

# Referral and loyalty (screen 04, OFFER-R23 and OFFER-R24).
PROGRAM_WORDS = {'referral': ('referral', 'refer_a_friend', 'refer'), 'loyalty': ('loyalty', 'rewards', 'points', 'vip')}
REFERRAL_CAC_SHARE = 0.5  # room spec: referral should acquire for under half of paid CAC
LOYALTY_EARN = 0.05       # earn rate to design around: 5 percent back (the lowest common rate in loyalty tools)
LOYALTY_MARGIN_CAP = 0.25 # reward cost above 25 percent of gross margin is too rich (our own heuristic, not a benchmark)
WINDOW_CREEP_POINTS = 2   # a promo window 2 points deeper than the same window last year is creeping

# Bundle pairs (screen 04, OFFER-R26). Two products bought together more than chance says, often enough to matter.
PAIR_MIN_ORDERS = 30      # orders that hold both products in the window
PAIR_MIN_LIFT = 1.5       # bought together 1.5 times as often as chance
BUNDLE_SAVING = 0.10      # the bundle starts at 10 percent off the two paid prices
PAIR_DAYS = 90
STALE_DAYS = 90           # a move built on a brain record older than this says so and refreshes it first

# Pay in installments (screen 04, OFFER-R29). The lower bound is the US range on Shopify's Shop Pay Installments help
# page (read in web pass 2); lift claims were not read in full, so the move is a test, not a promise.
BNPL_MIN_USD = 35
BNPL_WORDS = ('installment', 'afterpay', 'klarna', 'affirm', 'sezzle', 'pay in 4', 'shop pay installments')
LOYALTY_FIRST_REWARD = (0.03, 0.10)   # first reward worth 3 to 10 percent of AOV (web pass 2: Smile.io)
LOYALTY_ORDERS_TO_FIRST = (1, 3)      # and reachable in 1 to 3 orders

# Discount-acquired cohorts (screen 04, OFFER-R31; web pass 2: Saras). Customers whose first order used a code,
# against full-price first orders, repeat within COHORT_DAYS. Fires when discounted ones repeat COHORT_GAP less.
COHORT_DAYS = 180
COHORT_GAP = 0.20
COHORT_MIN = 200          # customers needed in each group

# Welcome code economics (screen 04, OFFER-R32; room job LIFE-C02, the pop-up first-order offer). A code on first
# orders pays only if enough code orders are truly new: required share = code dollars / (margin after the code +
# code dollars). With no holdout on record, the move is a holdout test. Our own rule, written down.
WELCOME_DAYS = 90
WELCOME_MIN_ORDERS = 100       # code first orders in the window before the rule reads
WELCOME_FLAG = 0.25            # required new share at or above this is medium severity, else low
WELCOME_FLOW_WORDS = ('welcome',)
HOLDOUT_WORDS = ('holdout', 'hold-out', 'hold out', 'no code arm', 'pop-up', 'popup', 'welcome')

# Test trust (screen 04, OFFER-R33; room job LIFE-C47, "is any test untrustworthy"). Offer and price surfaces are
# judged on profit per visitor (web pass 2: Intelligems), never on AOV or conversion alone.
OFFER_SURFACES = ('first order offer', 'list price', 'pack price', 'cart rewards', 'bundles', 'new packs', 'loyalty',
                  'referral', 'product page pack selector', 'product page price block', 'pop-up')
BAD_OFFER_METRICS = ('aov', 'average_order_value', 'conversion_rate', 'cvr', 'revenue')
TEST_MIN_DAYS = 28

# Competitor and reseller price moves (screen 04, OFFER-R34; room job BRN-C11, PROD-C46). A move is the current
# captured price against the last value in the brain record's history. PRICE_MOVE or more either way is a move.
PRICE_MOVE = 0.05
RECAPTURE_DAYS = 30            # a single capture older than this is due for a second one

# Guarantee claims stress (screen 04, OFFER-R35; room job LIFE-C42, "does the guarantee remove risk without breaking
# margin if claims run high"). Claims at 1, 2 and 3 times the brain's planned rates, on top of today's contribution.
# Fires when claims at CLAIM_STRESS times the plan put contribution under the target. Our own rule, written down.
CLAIM_MULTIPLES = (1, 2, 3)
CLAIM_STRESS = 2

# Paid price per product (screen 04, OFFER-R36). What shoppers paid after codes against list price, from order rows.
# A product with CODE_DEPENDENT or more of its units sold with a code, and at least PAID_MIN_UNITS units, leans on
# the code. Our own rule, written down.
PAID_DAYS = 90
PAID_MIN_UNITS = 50
CODE_DEPENDENT = 0.45

# Attach rate by anchor product (screen 04, OFFER-R37; room job LIFE-C41, which placements convert). Orders with
# the product that carry a second product. Among the ATTACH_TOP products by orders, one ATTACH_GAP or more under the
# median attach rate is a cross-sell placement to build. Our own rule, written down.
ATTACH_DAYS = 90
ATTACH_TOP = 5
ATTACH_GAP = 0.05
ATTACH_MIN_ORDERS = 60

# Returns on code orders (screen 04, OFFER-R38). Orders 180 days long, ending 30 days back so returns can land.
# Code orders returning RETURN_RATIO times the full-price rate or more, each side RETURN_MIN orders, means the code
# buys orders that come back. Our own rule, written down.
RETURN_DAYS = 180
RETURN_LAG = 30
RETURN_RATIO = 1.25
RETURN_MIN = 200

# Test power (screen 04). Days a 50/50 test needs to see a POWER_LIFT relative change in conversion at 80 percent
# power and 5 percent two-sided significance: n per arm = POWER_K x (1 - p) / (p x lift^2), POWER_K = 2 x (1.96 +
# 0.84)^2. Sitewide traffic is the upper bound; a single page gets less, so its test runs longer.
POWER_LIFT = 0.10
POWER_K = 15.68
POWER_MAX_DAYS = 35           # a sitewide test that needs longer than this means traffic is too thin for the usual 28 days
