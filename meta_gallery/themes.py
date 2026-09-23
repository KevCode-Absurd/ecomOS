"""Rule-based creative theme tags.

Each ad gets 3 tags from its ad name, campaign name, headline and primary text:
  angle    what the ad leans on (offer, social proof, founder story, ...)
  product  which product line it shows
  hook     the kind of opening line in the primary text

The rules are plain keyword matches, so they can be wrong. Every tag keeps the
word that triggered it, and the page shows it as the reason.
"""
import re

ANGLES = [
    ('offer', 'Offer / urgency', ['hours left', 'hours to go', 'days to go', 'day to go', 'days left', 'sale', 'eoss', 'bfcm',
                                  '% off', 'off with code', 'gehna5', 'deal of the day', 'countdown', 'presale', 'discount',
                                  'under 30k', 'under ₹35k', 'flat ']),
    ('catalog', 'Catalog (Meta picks products)', []),
    ('social_proof', 'Social proof / reviews', ['review', 'reviews', 'social proof', 'testimonial', 'customers', '4.8/5', 'trust',
                                                'came back', 'rated', 'loved by', 'happy customer']),
    ('founder', 'Founder / brand story', ['founder', 'from our hands', 'our story', 'behind the scenes', 'craftsmanship', 'craftsmen']),
    ('ugc', 'UGC / unboxing', ['ugc', 'unboxing', 'influencer', 'asmr', 'athisha', 'aarya', 'stop motion', 'creator']),
    ('occasion', 'Gifting / occasion', ['gift', 'gifts', 'gifting', 'diwali', 'festive', 'navratri', 'navratna', 'navrathna', 'akshaya', 'birthstone', 'milestone',
                                        'valentine', 'rakhi', 'anniversary', 'wedding', 'celebrate', 'celebration']),
    ('education', 'Education / objection handling', ['educational', 'problem/solution', 'thinking of buying', 'lab grown',
                                                     'how to', 'guide', 'ready to ship', 'plan ahead', 'pay your way',
                                                     'hallmark', 'hallmarked', 'certified', 'exchange']),
]
DEFAULT_ANGLE = ('showcase', 'Product showcase')

PRODUCTS = [
    ('earrings', 'Earrings', ['earring', 'stud', 'hoop', 'jhumka']),
    ('bracelets', 'Bracelets', ['bracelet', 'tennis', 'bangle', 'kada']),
    ('rings', 'Rings', ['ring', 'eternity', 'band']),
    ('pendants', 'Pendants', ['pendant', 'navrat', 'mangalsutra']),
    ('chains', 'Chains / necklaces', ['chain', 'necklace', 'choker']),
]
MIXED = ('mixed', 'Mixed range')

HOOKS = [
    ('question', 'Question', lambda t: '?' in t[:120]),
    ('offer', 'Price or offer', lambda t: bool(re.search(r'₹|\brs\.?\s?\d|%|\boff\b|\bcode\b|\bsale\b', t[:120]))),
    ('proof', 'Proof or number', lambda t: bool(re.search(r'\d[\d,.]*\s?(k|\+|customers|reviews|years|/5)', t[:120]))),
    ('urgency', 'Urgency', lambda t: bool(re.search(r'hurry|last|left|ends|today only|now or never|limited', t[:120]))),
]
DEFAULT_HOOK = ('statement', 'Statement')


def _first_match(text, rules, whole_word=False):
    """whole_word=False: the phrase must stand alone (so "sale" does not match "sales").
    whole_word=True: the word must start at a word edge but may continue ("earring" matches "earrings")."""
    for code, label, words in rules:
        for w in words:
            pat = r'\b' + re.escape(w) if whole_word else r'(?<![a-z])' + re.escape(w) + r'(?![a-z])'
            if re.search(pat, text):
                return code, label, w
    return None


def tag(ad):
    """Return {'angle': {...}, 'product': {...}, 'hook': {...}} for one ad record."""
    c = ad.get('creative') or {}
    name = (ad.get('name') or '').lower()
    camp = (ad.get('campaign_name') or '').lower()
    head = (c.get('headline') or '').lower()
    body = (c.get('primary_text') or '').lower()
    cards = ' '.join((k.get('headline') or '') + ' ' + (k.get('description') or '') for k in c.get('cards') or []).lower()

    if c.get('type') == 'catalog_dynamic' and not _first_match(name + ' ' + camp, ANGLES[:1]):
        angle = {'code': 'catalog', 'label': 'Catalog (Meta picks products)', 'why': 'catalog ad'}
    else:
        m = None
        for source in (name, camp, head, body, cards):  # the ad name says the most about intent
            m = _first_match(source, [a for a in ANGLES if a[0] != 'catalog'])
            if m:
                break
        angle = {'code': m[0], 'label': m[1], 'why': f'"{m[2]}"'} if m else {'code': DEFAULT_ANGLE[0], 'label': DEFAULT_ANGLE[1], 'why': 'no angle word found'}

    p = None
    for source in (name, camp, head, cards, body):
        p = _first_match(source, PRODUCTS, whole_word=True)
        if p:
            break
    if c.get('type') == 'catalog_dynamic' or any(w in name + camp for w in ('all products', 'generic', 'bestseller', 'catalogue')):
        product = {'code': MIXED[0], 'label': MIXED[1], 'why': 'catalog or range ad'}
    elif p:
        product = {'code': p[0], 'label': p[1], 'why': f'"{p[2]}"'}
    else:
        product = {'code': MIXED[0], 'label': MIXED[1], 'why': 'no product word found'}

    opening = (c.get('primary_text') or c.get('headline') or '').strip().lower()
    hook = None
    if opening:
        for code, label, test in HOOKS:
            if test(opening):
                hook = {'code': code, 'label': label, 'why': opening[:60]}
                break
        hook = hook or {'code': DEFAULT_HOOK[0], 'label': DEFAULT_HOOK[1], 'why': opening[:60]}
    else:
        hook = {'code': 'none', 'label': 'No text', 'why': 'no primary text or headline'}
    return {'angle': angle, 'product': product, 'hook': hook}
