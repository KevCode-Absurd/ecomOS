import json
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from intelligence.segmentation import split_block
from intelligence.parsing import digest

def main():
    report=json.loads((ROOT/'data/snapshot-report.json').read_text(encoding='utf-8'))
    count=0
    total_chars=0
    with (ROOT/'data/evidence-segments.jsonl').open('w',encoding='utf-8') as output:
        for source in report['results']:
            if source['status']!='parsed':
                continue
            parsed=json.loads((ROOT/'data/snapshots'/source['id']/(source['sha256']+'.parsed.json')).read_text(encoding='utf-8'))
            for block in parsed['blocks']:
                covered=0
                for piece in split_block(block['text']):
                    if piece['start']>covered:
                        raise ValueError('Coverage gap')
                    covered=piece['end']
                    identity=f"{source['id']}:{source['sha256']}:{block['locator']}:{piece['start']}:{piece['end']}"
                    row={'id':digest(identity.encode()),'source_id':source['id'],'source_sha256':source['sha256'],
                         'locator':block['locator'],'origin':'unknown',**piece}
                    output.write(json.dumps(row,ensure_ascii=False)+'\n')
                    count+=1
                    total_chars+=len(piece['text'])
                if covered!=len(block['text']):
                    raise ValueError('Incomplete block')
    print(json.dumps({'segments':count,'characters_including_overlap':total_chars,
                      'coverage':'all extracted body text covered','token_count':'not measured'}))

if __name__=='__main__':
    main()
