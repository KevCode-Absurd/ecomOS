"""Local CRO checkpoint report; no API traffic."""
import json,sqlite3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
    directory=ROOT/'data/cro-folder-v1'
    rows=[json.loads(p.read_text(encoding='utf-8')) for p in directory.glob('batch-*-round-*.json')]
    db=sqlite3.connect(directory/'spend.sqlite')
    spend=[{'provider':p,'booked_usd':a/1e6,'reserved_usd':b/1e6,'unknown_or_running':n} for p,a,b,n in db.execute('SELECT provider,COALESCE(SUM(actual),0),COALESCE(SUM(CASE WHEN actual IS NULL THEN reserved ELSE 0 END),0),SUM(CASE WHEN actual IS NULL THEN 1 ELSE 0 END) FROM spend GROUP BY provider')]
    db.close()
    result={'initial_batches':52,'batches_with_responses':len({r['batch'] for r in rows}),'responses':len(rows),'candidates':sum(len(r['candidates']) for r in rows),'held':sum(len(r['held']) for r in rows),'response_errors':sum(bool(r['errors']) for r in rows),'spend':spend,'approved_cards':0,'coverage':'Independent review pending; self-reported completion is not verified coverage.'}
    (directory/'progress.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result))
if __name__=='__main__':main()
