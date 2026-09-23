"""Offline structural audit. Heuristic origin flags are not evidence labels."""
import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MARKERS = re.compile(r'generated|editorial|scope_hint|source_url|source_id|transcript|actionable|summary',re.I)

def main():
    report = json.loads((ROOT/'data/snapshot-report.json').read_text(encoding='utf-8'))
    groups, binary, by_folder = defaultdict(list), defaultdict(list), defaultdict(list)
    records, samples = [], []
    for source in report['results']:
        if source['status'] != 'parsed':
            continue
        parsed = json.loads((ROOT/'data/snapshots'/source['id']/(source['sha256']+'.parsed.json')).read_text(encoding='utf-8'))
        text = '\n'.join(b['text'] for b in parsed['blocks'])
        normalized = re.sub(r'\s+',' ',text).strip()
        fingerprint = hashlib.sha256(normalized.encode()).hexdigest()
        groups[fingerprint].append(source['id'])
        binary[source['sha256']].append(source['id'])
        flags = [{'locator':b['locator'],'markers':sorted(set(m.lower() for m in MARKERS.findall(b['text'])))}
                 for b in parsed['blocks'] if MARKERS.search(b['text'])]
        row = {**source,'normalized_text_sha256':fingerprint,
               'longest_block_characters':max(len(b['text']) for b in parsed['blocks']),
               'origin_review_flags':flags,
               'origin_status':'unclassified'}
        records.append(row)
        by_folder[source['folder_path']].append(row)
    # Two candidate passages per domain, retaining locators; not human-labeled gold data.
    for folder, sources in sorted(by_folder.items()):
        selected = sorted(sources,key=lambda r:r['characters'])
        for source in [selected[len(selected)//2],selected[-1]]:
            parsed = json.loads((ROOT/'data/snapshots'/source['id']/(source['sha256']+'.parsed.json')).read_text(encoding='utf-8'))
            substantial = [b for b in parsed['blocks'] if len(b['text'])>=300]
            if not substantial:
                substantial=parsed['blocks']
            block=substantial[len(substantial)//2]
            samples.append({'source_id':source['id'],'source_sha256':source['sha256'],
                            'folder':folder,'locator':block['locator'],'text':block['text'],
                            'label_status':'needs_human_or_supervised_review'})
    summary = {'documents':len(records),'folder_groups':len(by_folder),
               'exact_binary_duplicate_groups':sum(len(v)>1 for v in binary.values()),
               'normalized_text_duplicate_groups':sum(len(v)>1 for v in groups.values()),
               'documents_with_origin_review_markers':sum(bool(r['origin_review_flags']) for r in records),
               'documents_over_100000_characters':sum(r['characters']>100000 for r in records),
               'documents_with_blocks_over_12000_characters':sum(1 for r in records if r['longest_block_characters']>12000),
               'evaluation_candidate_passages':len(samples),
               'note':'Markers only flag review candidates. No origin classifications, model-token counts or semantic duplicate judgments are inferred.'}
    (ROOT/'data/corpus-audit.json').write_text(json.dumps({'summary':summary,'documents':records,
        'normalized_duplicate_groups':[v for v in groups.values() if len(v)>1]},indent=2),encoding='utf-8')
    (ROOT/'data/evaluation-candidates.json').write_text(json.dumps(samples,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(summary))
    print(json.dumps({'largest_documents':[{'name':r['name'],'characters':r['characters'],'words':r['words']} for r in sorted(records,key=lambda r:-r['characters'])[:5]]}))

if __name__=='__main__':
    main()
