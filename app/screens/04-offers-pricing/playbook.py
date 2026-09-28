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
