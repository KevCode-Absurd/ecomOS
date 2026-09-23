"""Flag editorial-only evidence without inferring authorship or deleting source text."""
import collections,json
from calibration_client import ROOT
from prepare_origin_review import classify_blocks

def main():
    d=ROOT/'data/cro-folder-v1';manifest=json.loads((ROOT/'data/cro-folder-proposal.json').read_text(encoding='utf-8'));roles={}
    for doc in manifest['documents']:
        blocks=json.loads((ROOT/'data/snapshots'/doc['source_id']/(doc['sha256']+'.parsed.json')).read_text(encoding='utf-8'))['blocks']
        for label in classify_blocks(blocks):roles[(doc['source_id'],label['locator'])]=label['proposed_origin']
    index=json.loads((d/'revision-index.json').read_text(encoding='utf-8'));flagged=[]
    for card in index['cards']:
        hints=sorted({roles.get((e['source_id'],e['locator']),'needs_review') for e in card['evidence'] if e['field'] in ['claim','action']})
        only_editorial=bool(hints) and set(hints)<={'editorial_candidate','metadata_candidate'}
        card['evidence_role_hints']=hints;card['needs_primary_body_evidence']=only_editorial
        if only_editorial:flagged.append({'candidate_id':card['id'],'batch':card['batch'],'title':card['unit']['title']})
    (d/'revision-index.json').write_text(json.dumps(index,ensure_ascii=False,indent=2),encoding='utf-8')
    report={'flagged_cards':flagged,'policy':'Structural hints only; do not infer verified original authorship or discard uncertain text. Editorial-only recommendations need source-body evidence before promotion.'}
    (d/'editorial-evidence-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'cards_checked':len(index['cards']),'editorial_only_evidence_flags':len(flagged),'api_requests':0}))
if __name__=='__main__':main()
