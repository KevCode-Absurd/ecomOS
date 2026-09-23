"""Reconcile explicit pre-generation HTTP 400 rejections; never clear uncertain dispatches."""
import sqlite3
import calibration_client as c
from peach_web_case import OUT
from build_library import read,write

def main():
 db=sqlite3.connect(OUT/'spend.sqlite');pending=[x[0] for x in db.execute('SELECT request_id FROM spend WHERE actual IS NULL')];db.close()
 fixed=[]
 for rid in pending:
  p=OUT/'attempts'/f'{rid}.json'
  if not p.exists():continue
  a=read(p)
  if a.get('status')!='uncertain_or_failed' or not a.get('error','').startswith('HTTP 400'):continue
  # API rejected these parameter requests; no generated response/usage exists.
  for path,working,absolute in [(OUT/'spend.sqlite',23,23),(c.ROOT/'data/spend.sqlite',160,200)]:
   b=c.Budget(path,working,absolute)
   row=b.db.execute('SELECT actual FROM spend WHERE request_id=?',(rid,)).fetchone()
   if row and row[0] is None:b.settle(rid,0)
   b.close()
  a['status']='rejected_before_generation';a['booked_cost_usd']=0;a['billing_note']='Explicit HTTP 400 parameter rejection, not timeout. Provider invoice remains authoritative.';write(p,a);fixed.append(rid)
 write(OUT/'reconciled-http400.json',{'request_ids':fixed,'note':'Uncertain interrupted requests retain full reservations.'});print('Reconciled',len(fixed),'HTTP400 rejections; interrupted calls remain reserved.')
if __name__=='__main__':main()
