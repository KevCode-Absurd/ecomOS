"""Adapt earlier cards to concrete ecommerce tasks; reuse saved extraction, no source re-extraction."""
import argparse
import re
from concurrent.futures import ThreadPoolExecutor
from build_library import DEST, ROOT, read, write, export
from calibration_client import run_call
from intelligence.library import validate_cards, card_id


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--folder',required=True)
    parser.add_argument('--broad-sources',action='store_true')
    parser.add_argument('--cro',action='store_true',help='Apply the stronger merchant-focused adaptation to all CRO sections')
    parser.add_argument('--landing-pages',action='store_true',help='Adapt landing-page sections with service-funnel or unsupported-proof content')
    args=parser.parse_args()
    if args.cro and args.folder!='09':parser.error('--cro requires --folder 09')
    if args.landing_pages and args.folder!='07':parser.error('--landing-pages requires --folder 07')
    jobs=read(DEST/'manifest.json')['jobs']
    selected=[j for j in jobs if j['folder'].startswith('/'+args.folder)]
    if args.broad_sources:
        selected=[j for j in selected if j['source_name'].startswith(('$100M Offers_', 'How to Create Irresistible Offers'))]
    if args.landing_pages:
        def needs_adaptation(job):
            path=DEST/'results'/(job['id']+'.json')
            if not path.exists():return False
            if job['source_name'].startswith(('Best 2026 Ecommerce Quiz','Copy my $20k_day','Guide_ $100k_day')):return True
            return any(re.search(r'lead.gen|speed.to.lead|consultation|booked.call|call.booking|course|fictitious',c['title']+' '+c['use_when'],re.I) for c in read(path)['cards'])
        selected=[j for j in selected if needs_adaptation(j)]
    prompt=(ROOT/'prompts/cards-v3.md').read_text(encoding='utf-8')
    prompt+='\nYou are adapting existing extracted cards, not re-extracting source documents. Preserve useful expert detail and qualifications. Make every retained card directly useful for a specific ecommerce task. Drop service-only cards that do not transfer. Return the same cards JSON schema. Preserve already ecommerce-specific cards without needless rewriting. Never claim an adapted ecommerce example was demonstrated by the source.'
    if args.broad_sources:
        prompt+='\nThese broader business-book cards still contain service-sales advice. REWRITE operational steps for a merchant selling products online. Every card must name a specific store decision and concrete merchant actions, not merely mention ecommerce in use_when. Remove sales-call scripts, agency onboarding, coaching tactics and health protocols. For example, translate reducing effort into product setup, bundle selection or replenishment; translate fast wins into post-purchase usage guidance and onboarding, not an agency closing a sale. Retain non-ecommerce examples only when clearly labeled as source illustrations and immediately explain the merchant application. Remove ungrounded guaranteed outcomes and check obvious arithmetic; do not preserve a numerical claim contradicted by its own inputs. If no useful merchant application exists, omit that card. Keep scope narrow and avoid padding.'
    if args.cro:
        prompt+='\nCRO cleanup: every retained card must help a merchant improve or measure a shoppers journey to product purchase or repeat purchase. Preserve useful experimentation, statistics, analytics and session-recording techniques, but anchor use_when and steps to store decisions and purchase/revenue/margin outcomes. Remove service sales-call scripts, free agency growth-plan funnels, consultation/proposal followups, monetizing unqualified service leads, and sales-close-rate heuristics. Do not force these into ecommerce by renaming leads as shoppers. Transfer useful CTA/proof/objection principles into PDP, cart, checkout, product quiz or email signup tasks only where the underlying mechanism really transfers. Email signup is a supporting outcome, never equivalent to a purchase. Remove source promotion and unsupported numerical guarantees. Keep thresholds explicitly qualified as source heuristics, and retain the requirement to calculate actual experiment sample size. Preserve substantive ecommerce advice, tools, caveats and examples; do not turn everything into generic best practices. No fixed number of cards; an entirely service-only section may yield an empty cards list. Merchant-oriented adaptations should be framed as applications of the source principle, not source-demonstrated ecommerce results.'
    if args.landing_pages:
        prompt+='\nLanding-page cleanup: rewrite transferable hero, CTA, objection-handling and page-structure principles into physical-product PDPs, campaign pages or advertorial-to-product journeys. Drop course sales, consultation booking and speed-to-lead dialer procedures rather than renaming them. Adapt fitness-app quiz mechanics into honest product matching using fit, preferences, routine, compatibility and consumption; omit medical diagnosis, weight predictions and irrelevant health interrogation. Quiz answers must actually inform recommendations and education, not create fake personalization. Remove fabricated doctors, invented reviews, fictitious experts presented as real, false urgency and unsupported scientific root-cause claims. Disclaimers do not turn invented proof into authentic evidence. Keep useful evidence-backed mechanism explanation, genuine customer stories and clearly identified advertising. Do not create a card teaching dishonest tactics just because a source recommends them. Preserve distinctive useful detail and source-specific caveats; fewer substantive merchant cards are better than forced adaptations.'
    def process(job):
        path=DEST/'results'/(job['id']+'.json')
        if not path.exists():return
        old=read(path)
        version=4 if args.landing_pages else (3 if args.cro else (2 if args.broad_sources else 1))
        if old.get('ecommerce_scope_version',0)>=version:return
        user={'source_name':job['source_name'],'domain':job['domain'],
              'cards':[{k:c[k] for k in ('title','summary','use_when','steps','caveats','tags')} for c in old['cards']]}
        stronger=args.broad_sources or args.cro or args.landing_pages
        result=run_call('library-ecommerce-v1','openai' if stronger else 'deepseek','low' if stronger else 'none',prompt,user,limit=16384,stage_limit=200)
        if result['finish_reason']!='stop':raise ValueError('Incomplete adaptation saved for inspection')
        cards=validate_cards(result['output'])
        for c in cards:
            c.update(id=card_id(job['source_id'],c),**{k:job[k] for k in ('source_id','source_sha256','source_name','folder','domain','section')})
        backup=DEST/'before-ecommerce-focus'/path.name
        if not backup.exists():write(backup,old)
        write(path,{'cards':cards,'request_id':result['request_id'],'original_request_id':old['request_id'],'ecommerce_scope_version':version})
        print(f"Focused {job['source_name']} section {job['section']}: {len(cards)} cards",flush=True)
    with ThreadPoolExecutor(max_workers=6) as pool:list(pool.map(process,selected))
    export(jobs)


if __name__=='__main__':main()
