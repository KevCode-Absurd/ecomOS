"""Propose structural origin labels without certifying original provenance."""
import hashlib
import json
import re
from collections import Counter,defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
EDITORIAL=re.compile(r'^(?:Topics|Look for|Skip|Scope mix|Volume|Goes here|Not here|Header)\s*[.:]',re.I)
META=re.compile(r'^(?:url|date|rights|why|modules|mode|topics|tier|scope_hint|source_id)\s*:',re.I)
ROUTING=re.compile(r'^\d{2}-[A-Z]{3}\s*/')

def classify_blocks(blocks):
    labels=[]
    # Only a bounded, closed opening block is frontmatter. Horizontal rules
    # inside transcripts must never turn the remaining document into metadata.
    frontmatter_end=-1
    if blocks and blocks[0]['text'].strip()=='---':
        size=0
        for i,b in enumerate(blocks[1:51],1):
            size+=len(b['text'])
            if size>16000: break
            if b['text'].strip()=='---':
                if any(META.match(row['text'].strip()) for row in blocks[1:i]):
                    frontmatter_end=i
                break
    for i,b in enumerate(blocks):
        text=b['text'].strip()
        if i<=frontmatter_end or (len(text)<=2000 and META.match(text)): kind='metadata_candidate'
        elif EDITORIAL.match(text) or ROUTING.match(text): kind='editorial_candidate'
        elif len(text)>=3000: kind='body_candidate'
        else: kind='needs_review'
        labels.append({'locator':b['locator'],'characters':len(b['text']),'proposed_origin':kind,
                       'verified_origin':'unknown','reason':'structural_heuristic_only'})
    return labels

def main():
    sources=json.loads((ROOT/'data/snapshot-report.json').read_text(encoding='utf-8'))['results']
    records=[]
    candidates=defaultdict(list)
    counts=Counter()
    characters=Counter()
    by_id={}
    for source in sources:
        if source['status']!='parsed': continue
        by_id[source['id']]=source
        parsed=json.loads((ROOT/'data/snapshots'/source['id']/(source['sha256']+'.parsed.json')).read_text(encoding='utf-8'))
        labels=classify_blocks(parsed['blocks'])
        records.append({'source_id':source['id'],'sha256':source['sha256'],'labels':labels})
        body={b['locator'] for b in labels if b['proposed_origin']=='body_candidate'}
        for label in labels:
            counts[label['proposed_origin']]+=1
            characters[label['proposed_origin']]+=label['characters']
        for locator in body:
            candidates[source['folder_path']].append((source['id'],locator))
    segments=defaultdict(list)
    with (ROOT/'data/evidence-segments.jsonl').open(encoding='utf-8') as f:
        for line in f:
            row=json.loads(line)
            segments[(row['source_id'],row['locator'])].append(row)
    selected=[]
    for folder,options in sorted(candidates.items()):
        # Stable choice: median-size source with an eligible long body, then central span.
        options=sorted(set(options),key=lambda x:(by_id[x[0]]['characters'],x))
        source_id,locator=options[len(options)//2]
        spans=sorted(segments[(source_id,locator)],key=lambda r:r['start'])
        span=spans[len(spans)//2]
        selected.append({'folder':folder,'document':by_id[source_id]['name'],**span,
                         'provenance_status':'unverified_body_candidate','approved_for_transmission':False})
    summary={'documents':len(records),'block_counts':dict(counts),'character_counts':dict(characters),
             'proposed_body_samples':len(selected),'verified_original_passages':0,
             'warning':'Length and labels cannot establish original provenance. Uncertain text is retained, not deleted.'}
    (ROOT/'data/origin-review.json').write_text(json.dumps({'summary':summary,'documents':records},indent=2),encoding='utf-8')
    (ROOT/'data/body-evaluation-proposal.json').write_text(json.dumps({'status':'local_review_only','passages':selected},ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(summary))

if __name__=='__main__': main()
