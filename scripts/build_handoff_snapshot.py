"""Read-only project audit for the handoff; never reads credential contents or calls APIs."""
import json,hashlib,sqlite3,subprocess
from pathlib import Path
from collections import Counter
from datetime import datetime,timezone

ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def git(*args):return subprocess.run(['git',*args],cwd=ROOT,capture_output=True,text=True).stdout.strip()
def main():
 cards=read(ROOT/'data/library-v3/cards.json')['cards']
 metadata=read(ROOT/'data/library-v3/metadata.json')['cards'];vectors=read(ROOT/'data/library-v3/vectors.json')
 db=sqlite3.connect((ROOT/'data/library-v3/search.sqlite').as_uri()+'?mode=ro',uri=True)
 search_rows=db.execute('select count(*) from search').fetchone()[0];db.close()
 ledgers={}
 for p in sorted((ROOT/'data').glob('**/spend.sqlite')):
  db=sqlite3.connect(p.as_uri()+'?mode=ro',uri=True)
  try:
   cfg=db.execute('select working,absolute from budget_config where id=1').fetchone()
   rows=db.execute('select status,count(*),sum(coalesce(actual,reserved)) from spend group by status').fetchall()
   ledgers[p.relative_to(ROOT).as_posix()]={'working_usd':cfg[0]/1e6,'absolute_usd':cfg[1]/1e6,'by_status':{s:{'requests':n,'usd':round(v/1e6,6)} for s,n,v in rows}}
  except sqlite3.Error as e:ledgers[p.relative_to(ROOT).as_posix()]={'schema_error':type(e).__name__}
  finally:db.close()
 evidence=[]
 for p in sorted(ROOT.glob('*.md')):
  if p.name.startswith(('CLAUDE_','HANDOFF_')):continue
  evidence.append({'path':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
 tracked_data=git('ls-files','data').splitlines()
 snapshot={'generated_utc':datetime.now(timezone.utc).isoformat(),'project_root':str(ROOT),
  'inspection_scope':'Local files, Git metadata, read-only SQLite queries. No fresh Drive/Meta/GitHub authorization check, no paid calls, no credential contents inspected.',
  'library':{'cards':len(cards),'unique_card_ids':len({c['id'] for c in cards}),'source_documents':len({c['source_id'] for c in cards}),
   'domain_counts':dict(Counter(c['domain'] for c in cards)),'card_fields':list(cards[0]),'cards_sha256':hashlib.sha256((ROOT/'data/library-v3/cards.json').read_bytes()).hexdigest(),
   'metadata_records':len(metadata),'vectors':len(vectors),'keyword_rows':search_rows,'missing_metadata':len({c['id'] for c in cards}-set(metadata)),'missing_vectors':len({c['id'] for c in cards}-set(vectors))},
  'git':{'head':git('rev-parse','--short','HEAD'),'branch':git('branch','--show-current'),'upstream':git('rev-parse','--abbrev-ref','@{upstream}'),'ahead_behind_local_tracking_ref':git('rev-list','--left-right','--count','HEAD...origin/main'),'recent_commits':git('log','-5','--format=%h %s').splitlines(),'index_data_files':len(tracked_data),'head_data_files':len(git('ls-tree','-r','--name-only','HEAD','--','data').splitlines()),'staged_file_count':len(git('diff','--cached','--name-only').splitlines()),'gitignore_changed_from_HEAD':bool(git('diff','--name-only','HEAD','--','.gitignore')),'warning':'Git state changed in another session during handoff preparation; these sequential observations are not an atomic snapshot. Working ignore policy removed data/ exclusion and unignored data/**/*.sqlite. No Git add/commit/push was performed by the handoff process. Do not infer current remote privacy or synchronization from cached tracking refs.'},
  'budget_ledgers':ledgers,'budget_note':'Do not sum global and stage ledgers: the same requests can be recorded in both. Reservations are not verified charges. Provider invoices and tool-based image costs are outside this audit.',
  'tests':{'command':'python -m unittest discover -s tests','date':'2026-09-24','count':148,'result':'PASS outside sandbox','initial_sandbox_result':'12 errors reading installed .retrieval-runtime/tiktoken/__init__.py; rerun outside sandbox passed all 148. No source fix required.','limits':'Local fixture/mock and structural checks, not live connector, semantic quality or conversion validation.'},
  'evidence_documents':evidence}
 (ROOT/'HANDOFF_PROJECT_SNAPSHOT.json').write_text(json.dumps(snapshot,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({'library':snapshot['library'],'git':snapshot['git'],'global_budget':ledgers.get('data/spend.sqlite'),'evidence_documents':len(evidence)},ensure_ascii=True))

if __name__=='__main__':main()
