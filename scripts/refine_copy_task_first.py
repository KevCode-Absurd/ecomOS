"""One bounded follow-up to the observed v1.3 regression; preserve all outcomes."""
import argparse,copy,json
from concurrent.futures import ThreadPoolExecutor
import refine_copy_bridge as b
from build_library import read,write
from calibration_client import ROOT
from benchmark_copy_playbook import COMMON

OUT=ROOT/'data/ad-copy-bridge-v2'
PACK=ROOT/'playbooks/ad-copy-v1.4'
PROMPT='''Write finished ecommerce ad copy that answers this shopper's buying question. Start with the requested job and essential facts: an ad about value must explain value, and an ad about installation must explain the available help. Do not let a scene, a component or a copywriting formula displace that job. Each requested ad must stand on its own.
Write in natural, familiar English, aiming below a 10th-grade reading level. Short clear sentences, concrete words and a warm tone. Say it as a person would. Avoid jargon, stock praise, filler and robotic caveats. Keep necessary policy terms accurate rather than simplifying them into a stronger promise.
Connect a recognisable unwanted situation or buying hesitation to a realistic improvement through a supported product feature. This bridge may be implicit. The product helps the person make a practical change; it does not promise a transformed life. A feature or direct answer can lead when that is what this shopper needs. A concrete moment is useful only if it helps answer the buying question. Do not force every variant into a tiny household scene or a before/after story.
Give each variant a different useful reason or execution within the brief. Swapping a cabinet for a socket is not automatically a new angle. When the evidence supports only one benefit, vary how you explain it honestly rather than inventing benefits. Include enough product identity and any price or offer essential to the brief in each standalone ad. Select relevant details rather than repeating the full inventory. The headline makes the message clear, the body adds a reason to care, and the CTA gives a natural next step.
Use only supplied product facts. Cards offer writing methods, not evidence about this product. Do not invent proof, compatibility, quantities, setup time, ease, savings, urgency, guarantees or safety outcomes. Hypothetical situations are not customer research. Keep policy eligibility intact. Include material qualifications concisely; do not repeatedly narrate uncertainty or replace the benefit with instructions to check everything. Put genuinely missing facts in internal_notes.
Edit once before delivery: does each ad answer the brief, sound natural, fit the avatar, show a credible benefit and differ from the others? Remove padding and unsupported claims. Return the requested JSON with finished copy and separate internal_notes. Do not show planning, browse or publish.'''
NEW='Write three static Meta ad copy variants for a parent who has already seen the Peach Bucket kit and wants to know what help is available if they get stuck with installation. Answer that buying question directly using the supplied support claim. Do not make up support hours, appointment availability, tools or setup time. This is a hypothetical retargeting brief, not observed campaign data.'

def configure():
 b.OUT=OUT;b.PACK=PACK;b.ARMS=('generic','v1.2','v1.4');b.REPORT_STEM='AD_COPY_TASK_FIRST'
 b.FRESH={**b.FRESH,'support-retargeting':NEW}

def prepare():
 old_rows=b.rows();configure();b.setup()
 if (OUT/'manifest.json').exists():return
 old=ROOT/'playbooks/ad-copy-v1.2';pack=read(old/'ad-copy-deployment/playbook.json')
 pack['version']='1.4.0-experimental';pack['system_prompt']=PROMPT
 pack['evidence_method']='Thirteen-card editorial synthesis, user language/bridge criteria, and the observed v1.3 task-focus regression. Experimental, not market-validated.'
 pack['editorial_principles'] += [{'id':'task-first-plain-bridge','guidance':'Answer the buying question first. Use plain language and a credible problem-to-benefit connection when useful; never let a scene or formula replace the requested answer.','source_card_ids':[],'origin':'User preferences and v1.3 failure analysis; editorial rule.'}]
 for w in pack['workflows']:
  w['steps'].insert(0,'Identify the exact buying question, avatar and facts each standalone output must communicate.')
  w['steps'].append('Read aloud for plain language and check that a scene or formula has not displaced the buying question. Edit once.')
  w['output_checks'] += ['Each standalone ad answers the requested buying question.', 'Plain language below grade 10 is a target, not a reason to remove necessary precision.', 'The benefit follows credibly from a supplied product feature.']
 write(PACK/'ad-copy-deployment/playbook.json',pack)
 for name in ('ad-copy-deployment/source-evidence.json','catalog.json','OPERATING_CONTRACT.md'):
  p=PACK/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text((old/name).read_text(encoding='utf-8'),encoding='utf-8')
 (PACK/'SYSTEM_PROMPT.md').write_text(PROMPT+'\n',encoding='utf-8')
 (PACK/'EDITOR_CHECKLIST.md').write_text((ROOT/'playbooks/ad-copy-v1.3/EDITOR_CHECKLIST.md').read_text(encoding='utf-8')+'\nFirst check: does every standalone ad answer the actual buying question? A vivid scene or simple wording cannot compensate for missing that answer.\n',encoding='utf-8')
 write(OUT/'rubric.json',read(ROOT/'data/ad-copy-bridge-v1/rubric.json'))
 baseline=read(b.o.OLD/'manifest-corrected.json')['jobs'];base=next(j for j in baseline if j['task']=='value' and j['arm']=='generic')
 reused=[];jobs=[]
 for r in old_rows:
  if r['arm'] not in ('generic','v1.2'):continue
  r=copy.deepcopy(r)
  if not r.get('source'):r['source']=str(ROOT/'data/ad-copy-bridge-v1/runs'/(r['id']+'.json'))
  reused.append(r)
  if r['arm']=='generic':
   u=json.loads(base['payload']['input'][0]['content']);u['brief']=r['brief'];u['brand']=r['facts'];jobs.append(b.make_job(base,r['task'],'v1.4',u))
 for arm in b.ARMS:
  u=json.loads(base['payload']['input'][0]['content']);u['brief']=NEW;jobs.append(b.make_job(base,'support-retargeting',arm,u))
 write(OUT/'manifest.json',{'jobs':jobs,'reused':reused,'writer':'gpt-6-luna','design':'Six matched briefs, three arms; ten saved generic/v1.2 sets reused and eight new sets generated. Five briefs informed the revision; support-retargeting is the sole fresh same-brand brief, not independent brand validation. Same facts, model, reasoning and limits within each brief. All 18 sets receive new blinded ratings under the unchanged rubric. Historical outputs and v1.3 loss are preserved. No extra cards. At most this one follow-up; no further prompt tuning in this run.','cap_usd':2})

def generate():
 configure();b.setup();m=read(OUT/'manifest.json')
 def one(j):
  p=OUT/'runs'/(j['id']+'.json')
  if p.exists():return
  r=b.o.call(j['payload'],j['id'])
  if len(r['output'].get('variants',[]))!=3:raise ValueError('Invalid output retained')
  write(p,{**{k:j[k] for k in ('id','task','arm','facts','brief')},'output':r['output']})
  print(j['id'],r['response']['cost_upper_estimate_usd'],flush=True)
 with ThreadPoolExecutor(max_workers=2) as pool:list(pool.map(one,m['jobs']))

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('phase',choices=['prepare','generate','review','report']);a=p.parse_args()
 if a.phase in ('prepare','generate'):globals()[a.phase]()
 else:
  configure();getattr(b,a.phase)()
