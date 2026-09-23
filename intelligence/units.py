"""V2 candidate validation and exact evidence binding; no publication authority."""
import hashlib
import json

FIELDS={'id','kind','title','claim','action','trigger','prerequisites','exclusions',
        'completion','unknowns','relations'}
KINDS={'action','principle','example','warning','unresolved_claim'}


def bind(statement, source, field):
    if not isinstance(statement,dict) or set(statement)!={'text','quote'}:
        raise ValueError(field+': expected text and quote')
    if any(not isinstance(statement[k],str) or not statement[k].strip() for k in statement):
        raise ValueError(field+': empty statement')
    quote=statement['quote']
    start=source['text'].find(quote)
    if start<0: raise ValueError(field+': quote_not_exact')
    if source['text'].find(quote,start+1)>=0:
        raise ValueError(field+': ambiguous_quote')
    return {'field':field,'source_id':source['source_id'],'source_sha256':source['source_sha256'],
            'locator':source['locator'],'start':source['start']+start,
            'end':source['start']+start+len(quote),'quote':quote}


def bind_group(group,source,field,depth=0):
    if depth>12: raise ValueError(field+': nesting limit')
    if isinstance(group,dict) and set(group)=={'text','quote'}:
        return [bind(group,source,field)]
    if not isinstance(group,dict) or set(group)!={'op','args'} or group['op'] not in ('all','any') or not isinstance(group['args'],list):
        raise ValueError(field+': expected ALL/ANY group or evidenced statement')
    result=[]
    for index,arg in enumerate(group['args']):
        result.extend(bind_group(arg,source,field+'.'+str(index),depth+1))
    return result


def validate_unit(unit,source):
    if not isinstance(unit,dict) or set(unit)!=FIELDS: raise ValueError('invalid_unit_fields')
    if any(not isinstance(unit[k],str) or not unit[k].strip() for k in ['id','title','kind']):
        raise ValueError('invalid_unit_identity')
    if unit['kind'] not in KINDS: raise ValueError('invalid_unit_kind')
    evidence=[bind(unit['claim'],source,'claim')]
    if unit['action'] is not None:
        if unit['kind']!='action': raise ValueError('non_action_unit_has_action')
        evidence.append(bind(unit['action'],source,'action'))
    elif unit['kind']=='action': raise ValueError('action_unit_without_action')
    for field in ['trigger','prerequisites','exclusions']:
        evidence.extend(bind_group(unit[field],source,field))
    if not isinstance(unit['completion'],list): raise ValueError('invalid_completion')
    for i,statement in enumerate(unit['completion']):
        evidence.append(bind(statement,source,'completion.'+str(i)))
    if not isinstance(unit['unknowns'],list) or not all(isinstance(x,str) and x.strip() for x in unit['unknowns']):
        raise ValueError('invalid_unknowns')
    if not isinstance(unit['relations'],list): raise ValueError('invalid_relations')
    for relation in unit['relations']:
        if not isinstance(relation,dict) or set(relation)!={'kind','target'} or relation['kind'] not in ('depends_on','alternative_to','conflicts_with') or not isinstance(relation['target'],str):
            raise ValueError('invalid_relation')
    identity=json.dumps([source['source_id'],source['source_sha256'],source['locator'],source['start'],unit],sort_keys=True)
    return {'id':hashlib.sha256(identity.encode()).hexdigest(),'unit':unit,'evidence':evidence,
            'status':'candidate','provenance':'unverified','semantic_review':'required'}


def validate_output(output,source,max_units=16):
    if type(max_units) is not int or not 1<=max_units<=64:raise ValueError("Invalid unit limit")
    if not isinstance(output,dict) or set(output)!={'units','more_units','unresolved'}:
        return {'errors':['invalid_top_level'],'candidates':[],'held':[]}
    if type(output['more_units']) is not bool or not isinstance(output['unresolved'],list) or not all(isinstance(x,str) and x.strip() for x in output['unresolved']):
        return {'errors':['invalid_coverage'],'candidates':[],'held':[]}
    if not isinstance(output['units'],list) or len(output['units'])>max_units:
        return {'errors':['invalid_units'],'candidates':[],'held':[]}
    candidates=[]; held=[]; ids=[]
    for i,unit in enumerate(output['units']):
        try:
            candidate=validate_unit(unit,source)
            if unit['id'] in ids: raise ValueError('duplicate_unit_id')
            ids.append(unit['id']); candidates.append(candidate)
        except (ValueError,TypeError,KeyError) as error:
            held.append({'index':i,'reason':str(error)})
    known={c['unit']['id'] for c in candidates}
    errors=[]
    for candidate in candidates:
        for relation in candidate['unit']['relations']:
            if relation['target'] not in known or relation['target']==candidate['unit']['id']:
                errors.append('invalid_relation_target')
    graph={c['unit']['id']:[r['target'] for r in c['unit']['relations'] if r['kind']=='depends_on'] for c in candidates}
    visited=set()
    def visit(uid,stack):
        if uid in stack: raise ValueError('dependency_cycle')
        if uid in visited or uid not in graph: return
        for dep in graph[uid]: visit(dep,stack|{uid})
        visited.add(uid)
    try:
        for uid in graph: visit(uid,set())
    except ValueError:
        errors.append('dependency_cycle')
    return {'errors':errors,'candidates':candidates,'held':held,
            'more_units':output['more_units'],'unresolved':output['unresolved']}
