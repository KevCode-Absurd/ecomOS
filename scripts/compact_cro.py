"""Offline compaction measurement using the cached tokenizer; no API calls."""
import copy,json,sys,os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'.runtime')]
os.environ['TIKTOKEN_CACHE_DIR']=str(ROOT/'data/tokenizer-cache')
import tiktoken
from intelligence.capsules import compact_card

def main():
    enc=tiktoken.get_encoding('o200k_base');d=ROOT/'data/cro-folder-v1';cards=json.loads((d/'revision-index.json').read_text(encoding='utf-8'))['cards'];capsules=[];before=after=0
    for c in cards:
        compact=compact_card(c);capsules.append(compact)
        original={k:copy.deepcopy(c[k]) for k in ['id','unit','evidence']}
        if 'resolved_relations' in c:original['unit']['relations']=copy.deepcopy(c['resolved_relations'])
        for k in ['source_support_verdict','review_output_valid','provenance','source_limitations','batch_validation_errors','batch_held_units','evidence_role_hints','needs_primary_body_evidence','publication_allowed']:original[k]=compact[k]
        before+=len(enc.encode(json.dumps(original,ensure_ascii=False,separators=(',',':')),disallowed_special=()))
        after+=len(enc.encode(json.dumps(compact,ensure_ascii=False,separators=(',',':')),disallowed_special=()))
    (d/'compact-capsules.json').write_text(json.dumps({'cards':capsules,'publication_allowed':False},ensure_ascii=False),encoding='utf-8')
    report={'cards':len(cards),'encoding':'o200k_base','before_tokens':before,'after_tokens':after,'reduction_percent':round(100*(before-after)/before,2),'scope':'Equivalent source-card fields including limitations and review gates; excludes API wrappers and brand profile. This is not a retrieval, answer-quality or billing benchmark.'}
    (d/'compaction-report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
if __name__=='__main__':main()
