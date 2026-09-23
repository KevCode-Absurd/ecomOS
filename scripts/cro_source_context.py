"""Expand only within the authorized document; retain original paragraph offsets."""
import json
from calibration_client import ROOT
from prepare_cro_context import packet
from prepare_origin_review import classify_blocks

def expanded_source(batch):
    first=batch['segments'][0]
    blocks=json.loads((ROOT/'data/snapshots'/batch['source_id']/(first['source_sha256']+'.parsed.json')).read_text(encoding='utf-8'))['blocks']
    p=packet(batch,blocks)
    source={'source_id':p['source_id'],'source_sha256':p['source_sha256'],'locator':'expanded-context-batch','start':0,'text':p['text'],
            'primary_start':p['primary_start'],'primary_end':p['primary_end'],'outer_context_truncated':p['outer_context_truncated']}
    visible={s['locator'] for s in p['evidence_spans']}
    source['structural_role_hints']=[label for label in classify_blocks(blocks) if label['locator'] in visible]
    source['role_hint_policy']='Heuristic only; not proof of authorship. Routing/editorial metadata is not automatically an execution recommendation.'
    spans=[(s['packet_start'],s['packet_end'],{'locator':s['locator'],'start':s['source_start'],'text':s['text']}) for s in p['evidence_spans']]
    return source,spans
