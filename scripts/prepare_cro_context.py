"""Local context expansion across chunk boundaries; no API dispatch."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def packet(batch,blocks,neighbor_chars=4000):
    text='';spans=[];by_locator={}
    for block in blocks:
        if text:text+='\n\n'
        start=len(text);text+=block['text'];spans.append((start,len(text),block));by_locator[block['locator']]=start
    target_start=min(by_locator[s['locator']]+s['start'] for s in batch['segments'])
    target_end=max(by_locator[s['locator']]+s['end'] for s in batch['segments'])
    left=max(0,target_start-neighbor_chars);right=min(len(text),target_end+neighbor_chars)
    evidence=[]
    for start,end,block in spans:
        a=max(left,start);b=min(right,end)
        if a<b:evidence.append({'locator':block['locator'],'source_start':a-start,'source_end':b-start,'packet_start':a-left,'packet_end':b-left,'text':text[a:b]})
    return {'source_id':batch['source_id'],'source_sha256':batch['segments'][0]['source_sha256'],
        'text':text[left:right],'primary_start':target_start-left,'primary_end':target_end-left,
        'document_start':left,'document_end':right,'document_characters':len(text),'evidence_spans':evidence,
        'outer_context_truncated':left>0 or right<len(text),
        'policy':'Extract primary-span advice; use surrounding text to preserve conditions and continuations. Request more source context if this window is insufficient.'}
def main():
    p=ROOT/'data/cro-folder-proposal.json';auth=json.loads((ROOT/'data/cro-folder-authorization.json').read_text());assert hashlib.sha256(p.read_bytes()).hexdigest()==auth['manifest_sha256']
    manifest=json.loads(p.read_text(encoding='utf-8'));packets=[]
    for i,batch in enumerate(manifest['batches']):
        first=batch['segments'][0];raw=ROOT/'data/snapshots'/batch['source_id']/(first['source_sha256']+'.parsed.json')
        blocks=json.loads(raw.read_text(encoding='utf-8'))['blocks'];result=packet(batch,blocks)
        for span in result['evidence_spans']:
            block=next(b for b in blocks if b['locator']==span['locator'])
            assert block['text'][span['source_start']:span['source_end']]==span['text']
            assert result['text'][span['packet_start']:span['packet_end']]==span['text']
        packets.append({'batch':i,**result})
    out=ROOT/'data/cro-folder-v1/context-packets.json';out.write_text(json.dumps({'status':'local_preparation_only_not_dispatched','packets':packets},ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'context_packets':len(packets),'source_span_checks':'passed','api_requests':0}))
if __name__=='__main__':main()
