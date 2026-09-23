import json,statistics,sqlite3,re
from peach_writing_v2 import OUT
from peach_visual import ROOT,MODELS
from build_library import read,write
def main():
 s=read(OUT/'summary.json');rows=s['metrics'];assert len(rows)==9
 for model in MODELS:
  runs=[read(OUT/'runs'/f'{model}-{a}.json') for a in ['none','old','routed']]
  inputs=[]
  for r in runs:
   u=json.loads(r['call']['payload']['input'][0]['content']);u.pop('expert_context');inputs.append(u)
  assert inputs[0]==inputs[1]==inputs[2]
  assert len({r['call']['payload']['instructions'] for r in runs})==1
  ret=runs[-1]['retrieval'];ids=[k for x in ret for k in x['result']['card_ids']];assert len(ids)==len(set(ids))
  assert not any(c['domain'] in {'bot-and-agent-security','team-and-management'} for x in ret for c in x['cards'])
 review=read(OUT/'review.json');assert review['valid']
 superseded=read(OUT/'review-incomplete-evidence.json')['result']['booked_cost_usd'] if (OUT/'review-incomplete-evidence.json').exists() else 0
 added=s['generation_cost_usd']+review['result']['booked_cost_usd']+superseded
 db=sqlite3.connect(OUT.parent/'spend.sqlite');budget=db.execute('select status,count(*),sum(coalesce(actual,reserved))/1000000.0 from spend group by status').fetchall();db.close()
 lines=['# Writing retrieval: first improvement cycle','', 'Implemented explicit creative routes and a copywriting-principles route. Completed nine new copy packages: three models × no cards / previous retrieval / routed retrieval. Fourteen retrieval regression tests passed. Original visual outputs and library card text were preserved.','', '## Controlled results','', '| Model | No cards | Previous retrieval | Routed + principles |','|---|---:|---:|---:|']
 for m in MODELS:lines.append('| '+m+' | '+' | '.join(str(next(r['copy_score'] for r in rows if r['model']==m and r['arm']==a)) for a in ['none','old','routed'])+' |')
 lines+=['','Scores are 0–4 from one blinded GPT-6 Sol review simulating an agency owner. Copy only; not a live conversion test or real customer satisfaction measure. One sample per condition and same-family reviewer bias limit inference.','',review['result']['output']['summary'],'','## What changed','', '- Avatar, landing-page, static-ad and writing-principles searches now use explicit category and topic eligibility. General search is unchanged.','- The writing-principles route specifically uses ad-copy material. Retrieved sources include Cashvertising, Copy Hackers and the copywriting course; avatar sources include Competing Against Luck.','- Repeated card IDs are removed across the four searches. Applicability and caveats are retained.','- The revised prompt asks for direct brand voice and keeps internal research qualifications out of customer copy. All three conditions use this same revised prompt, so its effect is not credited to retrieval.','', '## Cost and context','', '| Model | Condition | Knowledge tokens | Input / output tokens | Generation USD | Generation seconds |','|---|---|---:|---:|---:|---:|']
 for r in rows:lines.append(f'| {r["model"]} | {r["arm"]} | {r["knowledge_tokens"]} | {r["input_tokens"]} / {r["output_tokens"]} | ${r["cost_upper_usd"]:.5f} | {r["model_seconds"]:.1f} |')
 lines += ['',f'Additional generation plus copy-review estimate: **${added:.2f}**, plus very small query-embedding charges. Uses the existing capped visual-benchmark ledger; no images were regenerated. Planning/research was reused and is not charged again in this table. Output tokens include reasoning; input pricing is conservative and does not subtract cache discounts.','', 'Cumulative text ledger for the visual benchmark and this improvement cycle: '+json.dumps(budget)+'. Earlier image-tool billing remains unexposed and is not treated as zero.','', '## Remaining problems and next gate','', 'The clearly unrelated security and staff-permissions categories no longer enter these creative packets. This is verified mechanically, not a claim of 90% relevance. The routing still lacks full task constraints: Sol retrieved offer-tier advice despite a fixed-offer brief, and some matches require adaptation to a non-consumable product. Correct category alone does not prove usefulness.','', 'Book-derived cards contain examples from other industries. Those examples illustrate a principle; they are not facts or claims to copy into Peach Bucket marketing. A later context-compaction pass can keep the actionable principle and its conditions while removing irrelevant examples; this cycle did not rewrite the corpus.','', 'We have not passed the proposed 80/20 launch gate. This is one brand and one campaign brief, not the required representative multi-brand task set. Next: add explicit fixed-offer/product/proof constraints to selection and validate on several different briefs before connecting autonomous execution.','', '## Review details','']
 for g in review['result']['output']['reviews']:
  m=review['mapping'][g['label']];lines += [f'### {m["model"]} — {m["arm"]}',g['main_weakness'],'Before launch: '+g['change_before_launch'],'']
 lines+=['## Files','','PEACH_BUCKET_WRITING_V2.html: side-by-side final copy, prompts, exact context, source cards, costs and review.','data/peach-visual-benchmark/writing-v2/: frozen packets, runs, protocol hashes, review and CSV metrics.','CREATIVE_RETRIEVAL.md: how to use the routed helper.']
 (ROOT/'PEACH_BUCKET_WRITING_V2_READOUT.md').write_text('\n'.join(lines),encoding='utf-8')
 write(OUT/'audit.json',{'runs':9,'paired_inputs_equal_except_context':True,'same_revised_prompt':True,'no_repeated_routed_card_ids':True,'security_and_team_domains_excluded':True,'additional_cost_estimate':added,'cumulative_text_budget':budget})
 print(json.dumps({'additional_cost':added,'scores':[{k:r[k] for k in ['model','arm','copy_score']} for r in rows]},indent=2))
if __name__=='__main__':main()
