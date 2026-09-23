"""Local source references and routing hints; never certify authorship from headers."""
import json
import re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]


def main():
    rows=json.loads((ROOT/'data/snapshot-report.json').read_text(encoding='utf-8'))['results']
    catalog=[]
    for row in rows:
        if row['status']!='parsed': continue
        parsed=json.loads((ROOT/'data/snapshots'/row['id']/(row['sha256']+'.parsed.json')).read_text(encoding='utf-8'))
        opening='\n'.join(b['text'] for b in parsed['blocks'][:40])[:20000]
        folder=re.search(r'/\d{2}-([A-Z]{3})(?:-|/|$)',row['folder_path'])
        modules=sorted(set(m for group in re.findall(r'\bmodules\s*:\s*\[([^\]]+)\]',opening,re.I)
                           for m in re.findall(r'\b[A-Z]{3}\b',group)))
        urls=sorted(set(re.findall(r'\burl\s*:\s*(https?://[^\s<>]+)',opening,re.I)))
        catalog.append({'source_id':row['id'],'source_sha256':row['sha256'],'name':row['name'],
                        'drive_reference':'https://drive.google.com/file/d/'+row['id']+'/view',
                        'folder':row['folder_path'],'folder_module_hint':folder.group(1) if folder else None,
                        'header_module_hints':modules,'asserted_header_urls':urls,
                        'routing_disagreement':bool(folder and modules and folder.group(1) not in modules),
                        'provenance':'user_supplied_library; underlying_authorship_not_verified',
                        'hint_policy':'Folders and headers are discovery hints, not authoritative unit classification.'})
    result={'sources':catalog,'summary':{'documents':len(catalog),
            'with_asserted_header_url':sum(bool(c['asserted_header_urls']) for c in catalog),
            'routing_disagreements':sum(c['routing_disagreement'] for c in catalog)},
            'limitations':'Only plaintext header URL fields in the opening 20,000 characters are indexed here; absence does not prove no URL exists elsewhere. No external URL was fetched.'}
    (ROOT/'data/source-catalog.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result['summary']))


if __name__=='__main__': main()
