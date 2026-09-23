"""One-time local editorial recovery of failed landing-page adaptations. No API calls."""
from build_library import DEST, read, write, export
from intelligence.library import card_id, validate_cards

jobs = read(DEST/'manifest.json')['jobs']

def card(title, summary, steps, tags, caveats=None):
    return dict(title=title, summary=summary, use_when=summary, steps=steps,
                tags=['ecommerce','landing-pages']+tags,
                caveats=(caveats or [])+['Merchant application of the source framework; not a source-demonstrated ecommerce result.'])

quiz = [
card('Use product-quiz answers for recommendations and customer research',
     'When building a store quiz that must select products and reveal buyer preferences.',
     ['Define which SKU, size, format or bundle each question can change before adding the question.',
      'Ask about intended use, current routine, preferences, compatibility and previous product frustrations. Skip demographic or health questions that do not affect a valid product choice.',
      'Map answers to real recommendation rules and export answer distributions by traffic source.',
      'Compare frequent needs with the assumed avatar; use the language in new ad hooks and identify gaps in the assortment.'],
     ['quiz','product-matching','customer-research'], ['Respondents represent the traffic sent to the quiz, not the entire market.']),
card('Place useful explanation screens between product-quiz questions',
     'When shoppers abandon a quiz or cannot understand why a preference matters.',
     ['Test an explanation after roughly three to five questions, the source heuristic.',
      'Branch the explanation on actual answers: explain why a selected use case needs a particular material, fit or format.',
      'Use genuine customer evidence only; a percentage comparison needs an actual measured population.',
      'Measure step abandonment and downstream purchases, not completion alone.'],
     ['quiz','completion','education'], ['Three to five questions is a source heuristic, not an optimum.']),
card('Choose quiz input controls that fit product decisions',
     'When a product quiz repeats many identical button screens.',
     ['Use single choice for mutually exclusive formats, multi-select for preferences, and numeric input for a relevant size or consumption amount.',
      'Avoid adding questions merely to lengthen the quiz. Each field must improve selection or useful research.',
      'Keep keyboard and mobile interaction usable; map every control to a stable exported field.',
      'Test a preference slider only if it is easier than buttons for this choice.'],
     ['quiz','forms','mobile'], ['The source had not tested its proposed slider interaction.']),
card('Reflect product preferences in later quiz copy',
     'When a recommendation quiz feels generic despite collecting useful answers.',
     ['Branch later copy on selected use, format and prior frustrations.',
      'Show how a recommended product solves the named practical constraint; never claim every shopper needs the same SKU while implying individualized matching.',
      'Limit branches to combinations the team can test and maintain.',
      'Test incompatible and contradictory answer combinations before launch.'], ['quiz','personalization']),
card('Reveal the product-match explanation before the buy box',
     'When shoppers need to understand why a quiz recommends a particular SKU or bundle.',
     ['Summarize the actual answers that determine the recommendation.',
      'Show the matching SKU, size or bundle and explain the rule connecting it to those answers.',
      'If calculating replenishment, show the consumption assumption and let the shopper correct it.',
      'Follow with product details, price, relevant genuine reviews, delivery and returns, then a purchase CTA.'],
     ['quiz','recommendation','buy-box'], ['Do not simulate computation or invent medical outcomes, future-body projections or guaranteed result dates.']),
card('Use an occasion date to check product delivery suitability',
     'When recommending products for gifts, travel, events or a move.',
     ['Ask the occasion and needed-by date only if timing changes the recommendation.',
      'Compare that date with actual stock, handling and delivery estimates.',
      'Show suitable products and explain any delivery uncertainty before checkout.',
      'Use genuine order deadlines where applicable; do not add resetting scarcity timers.'], ['quiz','gifting','delivery']),
card('Use routine and consumption to recommend a starter configuration',
     'When a store must choose a product format, starter kit or replenishment interval.',
     ['Ask what the shopper already uses, how often, what failed previously and what routine is realistic.',
      'Map those answers to a starter configuration or replenishment interval.',
      'Respect exclusions and explicit dislikes in both the main recommendation and cross-sells.',
      'Let the shopper adjust the suggested quantity or subscription before purchase.'], ['quiz','bundles','replenishment'], ['Self-reported usage is an estimate.']),
card('Keep the quiz result page focused on a transparent product offer',
     'When quiz completion is strong but product purchases are weak.',
     ['Make the answer summary, recommended product and offered price consistent.',
      'Remove unrelated outbound distractions while preserving access to delivery, returns, product details and support.',
      'If offering to email results, explain what will be sent and capture marketing preferences separately.',
      'Compare the full quiz-to-purchase journey with direct-to-PDP traffic; test one major change at a time.'],
     ['quiz','offer','conversion'], ['The source uses a subscription-app example. Long quizzes and commitment steps are hypotheses, not guaranteed retail improvements.'])
]

guide = [
card('Sequence an ecommerce advertorial around the next buyer objection',
     'When cold traffic needs product education before reaching the purchase page.',
     ['Map ad promise, hook, researched customer situation, alternatives, product mechanism, proof, objections, price and guarantee in that order as a starting structure.',
      'Make each section answer the question raised by the preceding section.',
      'Identify the page as advertising and carry the same angle from ad to page to product offer.',
      'Test against the existing product-page journey using purchases, acquisition cost and contribution margin.'], ['advertorial','page-structure'], ['Source conversion and revenue figures are case claims, not benchmarks.']),
card('Align the cold-traffic ad with the advertorial hook',
     'When ad clicks do not turn into engaged product-page visitors.',
     ['Choose one researched shopper problem and a supportable product benefit.',
      'Let the ad introduce a specific question that the page answers promptly.',
      'Match the audience, promise and tone in the opening headline; do not borrow the source example medical claims.',
      'Test alternative hooks while holding the downstream offer stable.'], ['advertorial','ad-congruence','hook']),
card('Write a specific product-use story from customer research',
     'When an advertorial describes abstract benefits instead of a recognizable buying situation.',
     ['Identify the practical moment that creates demand: the task, place, friction and desired outcome.',
      'Use authentic customer language and observed details rather than invented personal testimony.',
      'Show how the product changes that moment, then connect to the next objection.',
      'If presenting a real customer story, preserve its actual limitations and permission.'], ['advertorial','customer-research','story']),
card('Compare real alternatives before explaining product differentiation',
     'When shoppers see the product as interchangeable with cheaper alternatives.',
     ['List the alternatives customers actually consider, including keeping the current solution.',
      'Compare relevant limitations using accurate features, total cost, compatibility or effort.',
      'Explain the specific tradeoff the product addresses and acknowledge who may prefer another option.',
      'Avoid unsupported competitor failures or claims that retail products replace professional treatment.'], ['advertorial','comparison','differentiation']),
card('Explain a supported product mechanism before the offer',
     'When the buyer needs to understand why product features address their problem.',
     ['Identify a genuine, supportable cause of the practical product-use problem.',
      'Connect each relevant feature to that problem with a clear explanation or demonstration.',
      'Use specifications only when verified for the actual SKU; label uncertainty where evidence is limited.',
      'Move to proof and the offer once the buyer can explain the connection.'], ['advertorial','mechanism','product-education'], ['The source medical root-cause and percentage examples are not reusable evidence. Do not invent an expert or proprietary scientific cause.']),
card('Match authentic product reviews to purchase objections',
     'When shoppers need proof relevant to fit, use, value or reliability.',
     ['List the major buying objections and find genuine reviews addressing each.',
      'Preserve the customer wording and actual result; do not write testimonial personas.',
      'Use real usage timelines only where documented, without promising the same result to everyone.',
      'Answer remaining delivery, compatibility and returns questions in the FAQ.'], ['advertorial','reviews','objections']),
card('Reveal the price against a defensible product comparison',
     'When the advertorial must explain value before the purchase CTA.',
     ['Use a genuine comparable product, bundle contents or total ownership cost as the anchor.',
      'Show the actual price, quantity, recurring charges if any, and delivery costs clearly.',
      'Use a compare-at price or stock deadline only when accurate.',
      'Place a guarantee the merchant can honor beside the CTA with its relevant terms.'], ['advertorial','pricing','offer']),
card('Close an advertorial with useful questions and genuine proof',
     'When the bottom of the page leaves shoppers unsure about ordering.',
     ['Recap the product benefit, what is included, price and purchase action.',
      'Answer real shipping, gifting, stock and returns questions.',
      'Display authentic customer comments if available, or clearly label merchant-written answers as an FAQ.',
      'Check that the CTA leads to the promised SKU and offer.'], ['advertorial','faq','cta'], ['Do not fabricate comment threads, customer avatars or expert endorsements.'])
]

for job in jobs:
    if not job['folder'].startswith('/07'): continue
    path=DEST/'results'/(job['id']+'.json'); old=read(path); cards=old['cards']
    if job['id']=='43e62b74b4b297ff74e94ddd': cards=quiz
    elif job['id']=='dc82bb05a1d9c68b33b3e00f': cards=guide
    elif job['id'] in ('10d5619b05ce4828004f102f','43404033fb2f3ea886f048dc'):
        cards=[c for c in cards if 'speed-to-lead' not in c['title'].lower()]
        for c in cards:
            if 'Thank You' in c['title']:
                c.update(title='Track product-quiz or signup completion separately from purchases',
                         summary='Measure supporting store form completions without counting them as sales.',
                         use_when='When a campaign landing page collects quiz results or email signups.',
                         steps=['Fire a named form-completion event only after a successful submission.', 'Use a confirmation page or explicit success event and deduplicate repeat loads.', 'Track downstream purchase events separately and compare revenue by landing-page variant.'],
                         caveats=['Form completion is a supporting outcome, not purchase conversion.'])
    elif job['id']=='ee442c52ea517a2e058f21e8':
        cards=[c for c in cards if not c['title'].startswith(('Fictitious credibility','Niche risk management'))]
        for c in cards:
            if c['title']=='Advertorial page structure (top to bottom)':
                c['steps'][1]='Use genuine customer evidence or a real qualified expert with accurate attribution to support a narrow, substantiated claim.'
                c['caveats']=['Clearly identify the page as advertising; a disclosure does not make invented endorsements acceptable.', 'Build for mobile viewing and substantiate product comparisons and price anchors.']
            if c['title']=='Advertorial hook and headline patterns':
                c['caveats'].append('Use urgency, savings and before/after claims only when supported by this merchant and product; source dental claims are not evidence.')
    else: continue
    backup=DEST/'before-ecommerce-focus'/path.name
    if not backup.exists(): write(backup,old)
    validate_cards({'cards':cards})
    for c in cards:
        c.update(id=card_id(job['source_id'],c),**{k:job[k] for k in ('source_id','source_sha256','source_name','folder','domain','section')})
    write(path,{**old,'cards':cards,'ecommerce_scope_version':4,'local_editorial_recovery':'Targeted merchant adaptation of saved extraction after transport failure; no new API request.'})
export(jobs)
print('Landing-page local cleanup exported')
