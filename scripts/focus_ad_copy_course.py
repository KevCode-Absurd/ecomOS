"""Targeted ecommerce cleanup of the mixed freelancer/copywriting course."""
from concurrent.futures import ThreadPoolExecutor
from build_library import DEST, ROOT, read, write
from calibration_client import run_call
from intelligence.library import validate_cards, card_id

def main():
    jobs=[j for j in read(DEST/'manifest.json')['jobs'] if j['folder'].startswith('/11') and j['source_name'].startswith('8 Hour') and j['section']>0]
    prompt=(ROOT/'prompts/cards-v3.md').read_text(encoding='utf-8')+'''
You are editing previously extracted cards from a mixed copywriting/freelancer course. Be selective. This library serves merchants selling physical products online, NOT freelancers selling copywriting services. Delete cold outreach, prospect lists, booking calls, closing clients, portfolio pitching, freelancer pricing, personal branding, course-study advice, motivational filler and service/coaching enrollment. Do not disguise these by changing client to shopper. Entire sections may correctly return {"cards": []}.
Preserve substantive transferable copywriting techniques and concrete examples of wording, structure, research, editing, proof, offers, product-page flows, purchase tracking and store lifecycle emails. Rewrite their steps around product buyers, actual SKUs, genuine product evidence, product preferences, carts, purchase or repeat purchase; don't merely replace use_when. Replace irrelevant agency/fitness-coaching examples with clearly labeled merchant applications, not invented source results. Preserve named frameworks and distinctive reasoning. Keep source-specific thresholds qualified. Do not fabricate scarcity, testimonials, authority or scientific mechanisms. Treat source email deliverability claims and tool prices as historical assumptions to verify, not universal facts. Optimize for fewer substantive actionable cards, not a quota. Return only the cards JSON schema.
'''
    def process(j):
        p=DEST/'results'/(j['id']+'.json');old=read(p)
        if old.get('ecommerce_scope_version',0)>=5:return
        if j['section'] in (6,7):
            cards=[];rid=old['request_id']
        else:
            user={'source_name':j['source_name'],'domain':j['domain'],'section':j['section'],'cards':[{k:c[k] for k in ('title','summary','use_when','steps','caveats','tags')} for c in old['cards']]}
            r=run_call('library-ad-copy-focus-v1','deepseek','none',prompt,user,limit=16384,stage_limit=200)
            if r['finish_reason']!='stop':raise ValueError('Incomplete adaptation; inspect saved response')
            cards=validate_cards(r['output']);rid=r['request_id']
        for c in cards:c.update(id=card_id(j['source_id'],c),**{k:j[k] for k in ('source_id','source_sha256','source_name','folder','domain','section')})
        b=DEST/'before-ad-copy-focus'/p.name
        if not b.exists():write(b,old)
        write(p,{'cards':cards,'request_id':rid,'original_request_id':old['request_id'],'ecommerce_scope_version':5})
        print(f"Merchant copy cleanup section {j['section']}: {len(old['cards'])} -> {len(cards)} cards",flush=True)
    with ThreadPoolExecutor(max_workers=4) as pool:
        for start in range(0,len(jobs),4):
            futures=[pool.submit(process,j) for j in jobs[start:start+4]]
            for f in futures:f.result()

if __name__=='__main__':main()
