"""Exact o200k_base counts; proxy only for provider-specific billable usage."""
import json
import os
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'.runtime'))
os.environ['TIKTOKEN_CACHE_DIR']=str(ROOT/'data/tokenizer-cache')
import tiktoken

def main():
    encoder=tiktoken.get_encoding('o200k_base')
    snapshot=json.loads((ROOT/'data/snapshot-report.json').read_text(encoding='utf-8'))
    documents=[]
    for source in snapshot['results']:
        if source['status']!='parsed': continue
        parsed=json.loads((ROOT/'data/snapshots'/source['id']/(source['sha256']+'.parsed.json')).read_text(encoding='utf-8'))
        text='\n'.join(b['text'] for b in parsed['blocks'])
        documents.append({'source_id':source['id'],'tokens':len(encoder.encode(text,disallowed_special=()))})
    segment_tokens=0
    max_segment=0
    count=0
    with (ROOT/'data/evidence-segments.jsonl').open(encoding='utf-8') as source:
        for line in source:
            row=json.loads(line)
            tokens=len(encoder.encode(row['text'],disallowed_special=()))
            segment_tokens+=tokens
            max_segment=max(max_segment,tokens)
            count+=1
    summary={'encoding':'o200k_base','billing_accuracy':'proxy; verify actual provider usage',
             'raw_document_tokens':sum(d['tokens'] for d in documents),
             'segment_tokens_with_overlap':segment_tokens,'segments':count,'largest_segment_tokens':max_segment,
             'largest_document_tokens':max(d['tokens'] for d in documents),
             'excludes':'prompts, schemas, metadata, outputs, reasoning, retries and verification'}
    (ROOT/'data/token-report.json').write_text(json.dumps({'summary':summary,'documents':documents},indent=2),encoding='utf-8')
    print(json.dumps(summary))

if __name__=='__main__': main()
