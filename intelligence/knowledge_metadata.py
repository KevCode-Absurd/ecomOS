"""Conservative, auditable metadata; never infer verification or expiry."""
import hashlib
import json
import re

VERSION = 1
INTENTS = {
 'checkout-conversion': r'checkout|cart abandonment|abandoned cart',
 'product-page': r'product page|\bpdp\b',
 'creative-testing': r'creative|ad hooks?|ugc|ad fatigue',
 'offer-design': r'bundle|discount|offer design|guarantee|pricing',
 'customer-research': r'customer research|review mining|interview|avatar|persona',
 'retention': r'retention|repeat purchase|lifecycle|win.?back|loyalty',
 'email-sms': r'email|sms|klaviyo|deliverability',
 'search-acquisition': r'google ads|shopping|pmax|merchant center',
 'organic-discovery': r'\bseo\b|\baeo\b|organic search|answer engine',
 'measurement': r'attribution|incrementality|tracking|analytics|measurement',
 'profitability': r'cash flow|contribution|margin|profit|cogs|break.?even',
 'site-speed': r'site speed|page speed|performance budget|lcp|core web vitals|load time',
 'security': r'security|fraud|bot attack|access control|authentication',
 'inventory-sourcing': r'inventory|supplier|sourcing|replenishment|stockout',
 'team-operations': r'hiring|onboarding|team|delegation|operating procedure',
 'marketplace': r'amazon|marketplace|fba',
}
PLATFORMS = {'shopify':r'\bshopify\b','woocommerce':r'\bwoocommerce\b','meta':r'\bmeta\b|facebook|instagram',
 'google-ads':r'google ads|pmax|merchant center','amazon':r'\bamazon\b|\bfba\b','klaviyo':r'\bklaviyo\b',
 'tiktok':r'\btiktok\b'}
STOP = set('a an and are as at be brand business can do ecommerce for from how i in is it of on or our should store that the their this to we what when with you your'.split())

def terms(text):
 return set(re.findall(r'[a-z0-9]+',text.lower())) - STOP

def matches(text, rules):
 return [name for name,pattern in rules.items() if re.search(pattern,text,re.I)]

def fingerprint(card):
 return hashlib.sha256(json.dumps(card,sort_keys=True,ensure_ascii=False).encode()).hexdigest()

def classify(card):
 # Title, summary and existing tags are stronger labeling signals than incidental mentions in long steps.
 head=' '.join([card['title'],card['summary'],' '.join(card['tags'])]); low=head.lower()
 intents=matches(head,INTENTS); roles=[]
 if set(intents)&{'security'}: roles.append('protection')
 if set(intents)&{'team-operations','inventory-sourcing','site-speed','profitability'}: roles.append('operations')
 if set(intents)-{'security','team-operations','inventory-sourcing'}: roles.append('growth')
 kind='unknown'
 if re.search(r'case study|case example|teardown',low): kind='case-study'
 elif re.search(r'diagnos|audit|troubleshoot|root cause',low): kind='diagnostic'
 elif re.search(r'principle|fundamental|foundation',low): kind='principle'
 elif re.search(r'configure|install|set up|setup|implement',low): kind='procedure'
 elif re.search(r'\btest\b|experiment|tactic',low): kind='tactic'
 if kind=='principle': roles.append('foundation')
 platforms=matches(head,PLATFORMS)
 durability='unknown'
 if re.search(r'\b20[2-3][0-9]\b|algorithm|platform update|bidding|campaign structure',head,re.I): durability='volatile'
 elif platforms or kind=='procedure': durability='periodically-changing'
 elif kind=='principle': durability='durable'
 caveats=' '.join(card['caveats'])
 evidence='source-guidance-unverified'
 if re.search(r'adapt(?:ation|ed)|transfer is a hypothesis',caveats,re.I): evidence='ecommerce-adaptation'
 elif kind=='case-study': evidence='case-example-unverified'
 return dict(card_id=card['id'],content_hash=fingerprint(card),schema_version=VERSION,
  classification_method='deterministic-inference-v1',classification_status='inferred',
  domain=card['domain'],knowledge_type=kind,roles=sorted(set(roles)),durability=durability,
  tasks=intents,platform_mentions=platforms,applies_when=card['use_when'],conditions=card['caveats'],
  evidence_type=evidence,source_date=None,last_verified_at=None,next_review_at=None,
  verification_policy='check-current-details-before-execution' if durability in ('volatile','periodically-changing') else 'assess-source-and-task-fit')

def build_metadata(cards, overrides=None):
 overrides=overrides or {}; result={}
 allowed={'knowledge_type','roles','durability','tasks','applies_when','conditions','evidence_type','source_date','last_verified_at','next_review_at'}
 for c in cards:
  m=classify(c); override=overrides.get(c['id'])
  if override and override.get('content_hash')==m['content_hash']:
   changes=override.get('fields',{})
   if set(changes)-allowed: raise ValueError('Unsupported metadata override')
   m.update(changes);m['classification_method']='reviewed-override';m['classification_status']='reviewed'
  result[c['id']]=m
 return result
