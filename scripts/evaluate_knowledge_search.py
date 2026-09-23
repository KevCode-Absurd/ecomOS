"""Small retrieval smoke/latency evaluation, not a business-quality benchmark."""
import sys,time,json,statistics
from calibration_client import ROOT
from search_knowledge import engine
from search_library import retrieve
from build_library import DEST,write
CASES=[
 ('Plan Black Friday discounts without destroying contribution margin.',['discount','margin','contribution','black friday']),
 ('Build an ecommerce creative testing and production plan.',['creative','testing','production']),
 ('Use honest scarcity and customer social proof on product pages.',['scarcity','proof','trust']),
 ('How should an ecommerce brand diagnose profitable growth bottlenecks?',['growth','profit','diagnos','margin']),
 ('Improve mobile product page loading speed and LCP.',['speed','lcp','performance','loading']),
 ('Prevent checkout card testing and payment fraud.',['fraud','security','card testing']),
 ('Improve Klaviyo abandoned cart email flows.',['klaviyo','cart','email']),
 ('Forecast inventory replenishment and avoid stockouts.',['inventory','stock','replenish']),
]
def main():
 t=time.perf_counter();e=engine();cold=(time.perf_counter()-t)*1000;rows=[]
 for q,expected in CASES:
  r=e.search(q,max_cards=8);again=e.search(q,max_cards=8)
  titles=[e.cards[k]['title'] for k in r['card_ids']]
  topical=sum(any(x in title.lower() for x in expected) for title in titles[:5])
  old=retrieve(q,token_budget=8000,max_cards=8)
  old_size=len(e.encoding.encode(json.dumps(old,ensure_ascii=False)))
  new_size=len(e.encoding.encode(json.dumps(r,ensure_ascii=False)))
  rows.append(dict(query=q,titles=titles,topical_title_hits_at_5=topical,first_ms=r['elapsed_ms'],warm_ms=again['elapsed_ms'],
   knowledge_tokens=r['knowledge_tokens'],full_tool_response_tokens=new_size,legacy_response_tokens=old_size,
   old_titles=[c['title'] for c in old['cards']],method=r['method']))
 write(DEST/'retrieval-v4-evaluation.json',{'cold_load_ms':round(cold,2),'warm_median_ms':statistics.median(x['warm_ms'] for x in rows),'cases':rows,
 'limitations':'Eight developer-authored smoke cases. Title matches are coarse topic checks, not independent relevance judgments. Cached-query timing excludes first-time embedding latency.'})
 print(json.dumps({'cold_load_ms':round(cold,2),'warm_median_ms':statistics.median(x['warm_ms'] for x in rows),'cases':rows},ensure_ascii=False))
if __name__=='__main__':main()
