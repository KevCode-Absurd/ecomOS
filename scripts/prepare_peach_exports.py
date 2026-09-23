"""Read-only source CSV ingestion; preserve blanks, dates and report definitions."""
import csv,json,hashlib
from decimal import Decimal
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/peach-web-benchmark'
SOURCES={
 'shopify':Path('C:/Users/kevin/Downloads/Total sales over time - 2026-08-24 - 2026-09-23.csv'),
 'meta':Path('C:/Users/kevin/Downloads/GTM-and-GA-test-Campaigns-24-Aug-2026-22-Sep-2026.csv')}

def total(rows,key):
 values=[Decimal(r[key]) for r in rows if r.get(key) not in ('',None)]
 return {'reported_sum':str(sum(values,Decimal(0))),'rows_with_value':len(values),'blank_rows':len(rows)-len(values)}

def main():
 raw={};provenance={}
 for name,path in SOURCES.items():
  with path.open(encoding='utf-8-sig',newline='') as f:
   reader=csv.DictReader(f);raw[name]=list(reader);headers=reader.fieldnames
  assert len(set(headers))==len(headers),'Exact duplicate column names'
  provenance[name]={'path':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'rows':len(raw[name]),'headers':headers}
 s=raw['shopify'];m=raw['meta']
 assert len({r['Day'] for r in s})==len(s)
 assert {(r['Reporting starts'],r['Reporting ends']) for r in m}=={('2026-08-24','2026-09-22')}
 assert len({r['Campaign name'] for r in m})==len(m),'Repeated campaign names need review before aggregation'
 matched=[r for r in s if '2026-08-24'<=r['Day']<='2026-09-22']
 assert len(matched)==30
 fields=['Orders','Gross sales','Discounts','Sales reversals','Net sales','Shipping charges','Duties','Additional fees','Taxes','Total sales']
 for r in s:
  d=lambda k:Decimal(r[k])
  assert abs(d('Gross sales')+d('Discounts')+d('Sales reversals')-d('Net sales'))<Decimal('.02')
  assert abs(sum((d(k) for k in ['Net sales','Shipping charges','Duties','Additional fees','Taxes']),Decimal(0))-d('Total sales'))<Decimal('.02')
 trailing=[h for h in provenance['shopify']['headers'] if h.endswith(' ')]
 assert all(r[k]=='' for r in s for k in trailing),'Trailing-space comparison columns contain data; inspect'
 meta_fields=['Amount spent (INR)','Impressions','Clicks (all)','Landing page views','Adds to cart','Checkouts initiated','Purchases','Purchases conversion value']
 ss={k:total(matched,k) for k in fields};ms={k:total(m,k) for k in meta_fields}
 spend=Decimal(ms['Amount spent (INR)']['reported_sum']);pvalue=Decimal(ms['Purchases conversion value']['reported_sum']);purchases=Decimal(ms['Purchases']['reported_sum'])
 out={'status':'awaiting_owner_clarifications_before_paid_benchmark','provenance':provenance,'raw_reports':raw,
 'aligned_period':{'start':'2026-08-24','end':'2026-09-22','days':30,'timezone':'not supplied; same calendar dates do not prove timezone alignment'},
 'shopify_current':ss,'shopify_previous_reported':{k:total(s,k+' (previous_period)') for k in fields},
 'shopify_previous_dates':{'start':min(r['Day (previous_period)'] for r in s),'end':max(r['Day (previous_period)'] for r in s),'days':len(s)},
 'meta_current':ms,'derived':{'meta_reported_roas':str(pvalue/spend),'meta_cost_per_reported_purchase':str(spend/purchases),
 'shopify_net_sales_divided_by_meta_spend':str(Decimal(ss['Net sales']['reported_sum'])/spend),
 'shopify_total_sales_divided_by_meta_spend':str(Decimal(ss['Total sales']['reported_sum'])/spend)},
 'notes':['Shopify currency is not in export; INR is inferred from brand/Meta and needs confirmation.','Exclude Sep 23 for alignment; it is a zero row, so reported totals are unchanged.','Previous-period zero values preserved; no percentage growth computed from zero.','Meta blank cells remain unknown/unreported; reported sums include available numeric cells only.','Do not sum reach/frequency or average campaign ROAS.','Meta events are attributed aggregate events, not a sequential Shopify session funnel.','39 orders is a report count, not verified paid/delivered/non-refunded customers.','Sales reversals are not assumed to be refunds, RTO or test orders.','Ratios versus Meta spend are not contribution profit, incremental ROAS or total-marketing MER.'],
 'missing':['Shopify sessions/funnel/device breakdown','Meta previous-period data and attribution setting','Product and fulfilment economics','Current stock','Explanation for sales reversals and zero prior period','Account timezone and confirmed Shopify currency'],
 'validation':{'sales_arithmetic_ties':True,'campaign_rows_unique_by_name':True,'empty_trailing_space_columns_ignored':trailing}}
 OUT.mkdir(parents=True,exist_ok=True)
 (OUT/'export-snapshot.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps({'aligned_days':30,'orders':ss['Orders'],'net_sales':ss['Net sales'],'total_sales':ss['Total sales'],'meta_spend':ms['Amount spent (INR)'],'meta_purchases':ms['Purchases'],'derived':out['derived']},indent=2))
if __name__=='__main__':main()
